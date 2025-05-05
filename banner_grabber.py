#!/usr/bin/env python3
# banner_grabber.py - A tool to grab service banners from open ports

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def grab_banner(ip, port, timeout=2):
    """Attempt to grab banner from specified IP and port"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            s.send(b"GET / HTTP/1.1\r\n\r\n")
            banner = s.recv(1024).decode().strip()
            return banner if banner else "No banner received"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Network Banner Grabber Tool")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="21,22,80,443", 
                      help="Comma-separated list of ports (default: 21,22,80,443)")
    parser.add_argument("-t", "--threads", type=int, default=5,
                      help="Number of threads (default: 5)")
    args = parser.parse_args()

    ports = [int(p) for p in args.ports.split(",")]
    
    print(f"\n[+] Banner Grabbing {args.target}")
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = {executor.submit(grab_banner, args.target, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(results):
            port = results[future]
            banner = future.result()
            print(f"[+] Port {port}: {banner[:100]}...")  # Show first 100 chars

if __name__ == "__main__":
    main()