# Python script to scan and list active devices on your local Wi-Fi network.
# Requires admin/root privileges to access the ARP table.

import os
import platform
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def ping(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', str(ip)]
    result = subprocess.run(command, stdout=subprocess.DEVNULL)
    return result.returncode == 0

def get_arp_table():
    if platform.system().lower() == 'windows':
        output = subprocess.check_output('arp -a', shell=True).decode()
    else:
        output = subprocess.check_output(['arp', '-a']).decode()
    return output

def scan_network(network_cidr):
    print(f"Scanning network: {network_cidr}")
    net = ipaddress.ip_network(network_cidr, strict=False)
    live_hosts = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(ping, net.hosts()))

    for ip, alive in zip(net.hosts(), results):
        if alive:
            live_hosts.append(str(ip))

    return live_hosts

if __name__ == "__main__":
    # Change this to match your network subnet
    subnet = "192.168.1.0/24"

    devices = scan_network(subnet)
    print("\nLive Devices:")
    for device in devices:
        print(f" - {device}")

    print("\nARP Table (MAC addresses):")
    print(get_arp_table())
