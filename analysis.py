import scapy.all as scapy
from scapy_http import http


def data_collecting(iface):
    scapy.sniff(iface=iface, store=False, prn=data_analysis)


def data_analysis(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)


data_collecting("eth0")
