"""
TCP Port Scanner
Scans a target host for open ports with optional banner grabbing.
Usage: python scanner.py <target> [start-end]
"""

import socket
import threading
import sys
from datetime import datetime

# Printed banner that displays when the scan starts
def print_banner(target, start_time, ports):
    print("-" * 50)
    print(f"Scanner target: {target}")
    print(f"Ports: {ports}")
    print(f"Started at: {start_time}")
    print("-" * 50)

# Handling of both IP addresses and hostnames
def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)   # DNS lookup
        return ip
    except socket.gaierror:
        print(f"Error: Could not resolve hostname '{target}'")
        sys.exit()

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 8080, 8443]

def get_ports(args):
    if len(args) == 3:
        try:
            start, end = args[2].split('-')
            return range(int(start), int(end) + 1)
        except:
            print("Error: Port range must be in format start-end")
            sys.exit()
    return COMMON_PORTS

lock = threading.Lock()
open_ports = []

def grab_banner(sock, port):
    try:
        sock.settimeout(2)
        if port in [80, 8080, 8443]:
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        else:
            sock.send(b"\r\n")
        banner = sock.recv(1024).decode(errors='ignore').strip()
        banner = banner.splitlines()[0]
        return banner[:60] if banner else "No banner"
    except:
        return "No banner"

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))

        if result == 0:
            banner = grab_banner(sock, port)
            with lock:
                open_ports.append((port, banner))
                print(f"Port {port:<5} OPEN | {banner}")
        sock.close()
    except Exception:
        pass


def main():
    if len(sys.argv) < 2:
        print("Usage: python scanner.py <target> [start-end]")
        print("Example: python scanner.py 192.168.1.1")
        print("Example: python scanner.py scanme.nmap.org 1-1024")
        sys.exit()

    target = sys.argv[1]
    ip = resolve_target(target)
    ports = get_ports(sys.argv)
    start_time = datetime.now()

    print_banner(ip, start_time.strftime("%m/%d/%Y %I:%M:%S %p"), ports)

    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(ip, port), daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = datetime.now()
    duration = end_time - start_time

    print("-" * 50)
    print(f"Scan completed in {duration.total_seconds():.2f} seconds")
    print("-" * 50)

if __name__ == "__main__":
    main()