import dpkt, pcap
pc = pcap.pcap(name="lo")
pc.setfilter('udp')
udp = None
oscs = list()
for ts, pkt in pc:
    eth = dpkt.ethernet.Ethernet(pkt)
    ip = eth.data
    udp = ip.data
    if len(udp.data) > 0:
        if udp.data[0] == '/':
            oscs.append(pkt)
            print `udp`
