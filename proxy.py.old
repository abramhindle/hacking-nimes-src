import dpkt, pcap
import argparse
import socket
import threading
import resenders

parser = argparse.ArgumentParser(description='Chorus!')
parser.add_argument("--if",dest="interface",default="lo",help="Interface")
parser.add_argument("--proto",default="udp",help="Protocol")
parser.add_argument("--repeat",default=3,help="Repeats")
parser.add_argument("--delay",default=0,help="Delay")
parser.add_argument("--nospoof",default=False,action='store_true')
args = parser.parse_args()
interface = "lo"
proto = "udp"
interface = args.interface
proto = args.proto
repeats = int(args.repeat)
delay = float(args.delay)

def is_osc(packet):
    return packet[0] == '/'



pc = pcap.pcap(name=interface)
pc.setfilter(proto)

resender = None
if not args.nospoof:
    resender = resenders.Resender(pc)
else:
    resender = resenders.UDPResender(pc)

udp = None
oscs = list()
for ts, pkt in pc:
    eth = dpkt.ethernet.Ethernet(pkt)
    ip = eth.data
    udp = ip.data
    sig = resender.signature(udp)
    if not resender.seen_and_remove(sig):
        if len(udp.data) > 0:
            if is_osc(udp.data):
                print resender.resends
                print sig
                resender.resend(eth,repeats,sig,delay)
    else:
        print "Seen it %s" % sig
