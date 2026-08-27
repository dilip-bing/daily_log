"""
port_scan.py
Scan common ports on a host and report which are open.
No external deps — uses only stdlib socket.

Usage:
    python port_scan.py localhost
    python port_scan.py 192.168.1.1 --ports 22 80 443 8080
    python port_scan.py example.com --range 1 1024
"""

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465,
                587, 993, 995, 3306, 5432, 6379, 8080, 8443, 27017]

SERVICE_NAMES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 465: "SMTPS",
    587: "SMTP", 993: "IMAPS", 995: "POP3S", 3306: "MySQL",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-alt",
    8443: "HTTPS-alt", 27017: "MongoDB",
}


def scan_port(host: str, port: int, timeout: float) -> tuple[int, bool]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return port, False


def scan(host: str, ports: list[int], timeout: float):
    print(f"Scanning {host} on {len(ports)} port(s)...\n")
    open_ports = []

    with ThreadPoolExecutor(max_workers=50) as pool:
        futures = {pool.submit(scan_port, host, p, timeout): p for p in ports}
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)

    if not open_ports:
        print("No open ports found.")
        return

    print(f"{'Port':<8} {'Service':<14} Status")
    print("-" * 30)
    for port in sorted(open_ports):
        svc = SERVICE_NAMES.get(port, "unknown")
        print(f"{port:<8} {svc:<14} OPEN")

    print(f"\n{len(open_ports)} open port(s) found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("--ports", nargs="+", type=int)
    parser.add_argument("--range", nargs=2, type=int, metavar=("START", "END"))
    parser.add_argument("--timeout", type=float, default=1.0)
    args = parser.parse_args()

    if args.range:
        ports = list(range(args.range[0], args.range[1] + 1))
    elif args.ports:
        ports = args.ports
    else:
        ports = COMMON_PORTS

    scan(args.host, ports, args.timeout)
