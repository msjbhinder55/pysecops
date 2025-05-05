#!/usr/bin/env python3
# port_scanner.py - Advanced TCP Port Scanner with banner grabbing

import socket
import concurrent.futures
import argparse
from datetime import datetime

def scan_port(target, port, timeout=1.5, grab_banner=False):
    """Scan a single port with optional banner grabbing"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            
            if result == 0:  # Port is open
                banner = ""
                if grab_banner:
                    try:
                        s.send(b"GET / HTTP/1.1\r\n\r\n")
                        banner = s.recv(1024).decode().strip()
                    except:
                        banner = "No banner"
                return (port, "OPEN", banner[:100] if banner else "")
    except Exception:
        pass
    return (port, "CLOSED/FILTERED", "")

def port_scan(target, ports, threads=100, grab_banners=False):
    """Perform a port scan on target"""
    print(f"\n[+] Scanning {target} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, target, port, 1.5, grab_banners): port for port in ports}
        
        for future in concurrent.futures.as_completed(futures):
            port, status, banner = future.result()
            if status == "OPEN":
                print(f"[+] Port {port}: {status} | {banner}" if banner else f"[+] Port {port}: {status}")
                open_ports.append(port)
    
    print(f"\n[+] Scan completed. Found {len(open_ports)} open ports.")
    return open_ports

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range (e.g., 20-80) or list (e.g., 22,80,443)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Thread count (default: 100)")
    parser.add_argument("-b", "--banners", action="store_true", help="Attempt banner grabbing")
    args = parser.parse_args()

    # Parse port range
    if "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports = range(start, end + 1)
    else:
        ports = [int(p) for p in args.ports.split(",")]

    port_scan(args.target, ports, args.threads, args.banners)