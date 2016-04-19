import dpkt, pcap
import argparse
import socket
import threading
import resenders

parser = argparse.ArgumentParser(description='Watch!')
parser.add_argument("--if",dest="interface",default="lo",help="Interface")
parser.add_argument("--proto",default="udp",help="Protocol")
parser.add_argument("--nospoof",default=False,action='store_true')
args = parser.parse_args()
interface = "lo"
proto = "udp"
interface = args.interface
proto = args.proto

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
    if is_osc(udp.data):
        print sig
