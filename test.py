from scapy.layers.http import HTTPRequest

try:
    import scapy.all as scapy
except ImportError:
    import scapy

    # If you installed this package via pip, you just need to execute this
from scapy.layers import http

packets = scapy.rdpcap('example_network_traffic.pcap')
for p in packets:
    print('=' * 78)
    if p.haslayer(HTTPRequest):
        p.show()

        request = p.getlayer(HTTPRequest)
        try:
            print request.getfieldval('Accept-Language')
        except AttributeError:
            print None
        # print request.Host + request.Path +