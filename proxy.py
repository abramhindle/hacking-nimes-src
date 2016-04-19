import dpkt, pcap
import argparse
import socket
import threading
import resenders
import pythonosc
import pythonosc.osc_message
import oscbuilder

parser = argparse.ArgumentParser(description='Chorus!')
parser.add_argument("--if",dest="interface",default="lo",help="Interface")
parser.add_argument("--proto",default="udp",help="Protocol")
parser.add_argument("--proxy-port",dest="pport",default=9997,help="Listen Port")
parser.add_argument("--proxy-host",dest="phost",default="127.0.0.1",help="Listen Host")
parser.add_argument("--client-port",dest="cport",default=57120,help="Client Port")
parser.add_argument("--client-host",dest="chost",default="127.0.0.1",help="Client Host")
parser.add_argument("--repeat",default=3,help="Repeats")
parser.add_argument("--delay",default=0,help="Delay")
args = parser.parse_args()
interface = "lo"
proto = "udp"
interface = args.interface
proto = args.proto
repeats = int(args.repeat)
delay = float(args.delay)
pport = int(args.pport)
phost = args.phost
cport = int(args.cport)
chost = args.chost


def is_osc(packet):
    return packet[0] == '/'

pc = pcap.pcap(name=interface)
pc.setfilter(proto)

resender = resenders.UDPResender(pc)

ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind and ignore
ssock.bind((phost,pport))

def unicode_to_string(ustr):
    if isinstance(ustr,unicode):
        return str(ustr)
    else:
        return ustr

udp = None
oscs = list()
for ts, pkt in pc:
    eth = dpkt.ethernet.Ethernet(pkt)
    ip = eth.data
    udp = ip.data
    dport = udp.dport
    sport = udp.sport
    sig = resender.signature(udp)    
    if not (dport == pport or sport == pport):
        if not resender.seen_and_remove(sig):
            if len(udp.data) > 0:
                if is_osc(udp.data):
                    # send the OSC packet to our client
                    message = pythonosc.osc_message.OscMessage(bytearray(udp.data))
                    path = unicode_to_string(message.address)
                    params = map(unicode_to_string,message.params)
                    msg = oscbuilder.OscMessageBuilder(address = path)
                    msg.add_arg("%s:%s" % (socket.inet_ntoa(ip.dst),udp.dport))
                    for param in params:
                        msg.add_arg(param)
                    dgram = msg.build_dgram()
                    print "Passing to client %s:%s %s" % (chost,cport,`udp.data`)
                    ssock.sendto(dgram,(chost,cport))                    
        else:
            print "Seen it %s" % sig
    elif dport == pport:
        # this is a packet to our sys
        if is_osc(udp.data):
            print "Forwarding message %s" % `udp.data`
            # parse it
            message = pythonosc.osc_message.OscMessage(bytearray(udp.data))
            path = message.address
            target = message.params[0]
            (cchost,ccport) = target.split(':')
            ccport = int(ccport)
            params = message.params[1:]
            
            msg = oscbuilder.OscMessageBuilder(address = path)
            for param in params:
                msg.add_arg(param)
            dgram = msg.build_dgram()
            # not spoofing
            print "Sending off %s:%s %s" % (cchost,ccport,`dgram`)
            ssock.sendto(dgram,(cchost,ccport))
