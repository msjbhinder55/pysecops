#!/usr/bin/env python3
# nmap_scanner.py - A basic Nmap-like port scanner in Python

import socket
import concurrent.futures
from datetime import datetime

def scan_port(target, port):
    """Scan a single port on the target host"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"Port {port}: OPEN")
                return port
    except Exception as e:
        pass
    return None

def port_scan(target, ports):
    """Scan multiple ports on a target host"""
    print(f"\nScanning target {target}")
    print(f"Time started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            result = future.result()
            if result:
                open_ports.append(result)
    
    print(f"\nScan completed in {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Open ports: {sorted(open_ports)}")

if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")
    port_range = input("Enter port range (e.g., 1-100): ")
    
    start_port, end_port = map(int, port_range.split('-'))
    ports = range(start_port, end_port + 1)
    
    port_scan(target, ports)