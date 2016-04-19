import dpkt, pcap
import argparse
import socket
import threading


class Resender(object):
    def __init__(self,pc):
        self.pc = pc
        self.resends = 0
        self.lastpacket = list()
    def resend(self,eth_packet,n,sig,delay):
        for i in range(0,n):
            func = lambda eth_packet=eth_packet: pc.inject(str(eth_packet),len(str(eth_packet)))
            self.lastpacket.append(sig)
            threading.Timer((i+1)*delay,func).start()
            self.resends += 1
    def seen(self,sig):
        return sig in self.lastpacket
    def seen_and_remove(self,sig):
        res = sig in self.lastpacket
        if (res):
            self.lastpacket.remove(sig)
        return res
    def signature(self, packet):
        return `packet`
    
class UDPResender(Resender):
    def __init__(self,pc):
        super(UDPResender,self).__init__(pc)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def resend(self,eth,n,sig,delay):
        ip = socket.inet_ntoa(eth.ip.dst)
        port = eth.ip.udp.dport
        data = eth.ip.udp.data
	print "Sending (%s,%s)" % (ip,port)
        for i in range(0,n):
            func = lambda data=data, ip=ip, port=port: self.sock.sendto(data,(ip,port))
            self.lastpacket.append(sig)
            threading.Timer((i+1)*delay,func).start()
            self.resends += 1
    def signature(self, udp_packet):
        return `udp_packet.data`

