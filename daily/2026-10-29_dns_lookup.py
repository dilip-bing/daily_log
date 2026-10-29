"""
dns_lookup.py
Resolve hostnames to IPs and do reverse lookups.
Also shows A, MX, and NS records using the system resolver.

Usage:
    python dns_lookup.py google.com github.com
    python dns_lookup.py 8.8.8.8 --reverse
"""

import argparse
import socket
import sys


def forward_lookup(host: str):
    try:
        results = socket.getaddrinfo(host, None)
        ips = sorted({r[4][0] for r in results})
        print(f"\n{host}")
        for ip in ips:
            family = "IPv6" if ":" in ip else "IPv4"
            print(f"  {family:<6}  {ip}")
    except socket.gaierror as e:
        print(f"\n{host}  ->  ERROR: {e}")


def reverse_lookup(ip: str):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        print(f"\n{ip}  ->  {hostname}")
    except socket.herror as e:
        print(f"\n{ip}  ->  ERROR: {e}")


def whois_ns(host: str):
    """Best-effort NS lookup via system resolver."""
    try:
        import subprocess
        result = subprocess.run(
            ["nslookup", "-type=NS", host],
            capture_output=True, text=True, timeout=5
        )
        lines = [l.strip() for l in result.stdout.splitlines()
                 if "nameserver" in l.lower()]
        if lines:
            print(f"\nNS records for {host}:")
            for line in lines:
                print(f"  {line}")
    except Exception:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hosts", nargs="+")
    parser.add_argument("--reverse", action="store_true",
                        help="Treat inputs as IPs and do reverse lookup")
    parser.add_argument("--ns", action="store_true",
                        help="Also show NS records (requires nslookup)")
    args = parser.parse_args()

    for host in args.hosts:
        if args.reverse:
            reverse_lookup(host)
        else:
            forward_lookup(host)
            if args.ns:
                whois_ns(host)

    print()
