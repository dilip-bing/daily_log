"""
multi_ping.py
Ping multiple hosts and display round-trip latency.
Works on Linux/macOS using subprocess ping.

Usage:
    python multi_ping.py google.com github.com 8.8.8.8
    python multi_ping.py hosts.txt --count 5
"""

import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def ping_host(host: str, count: int) -> tuple[str, float | None, str]:
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", "2", host],
            capture_output=True, text=True, timeout=count * 3
        )
        output = result.stdout
        match = re.search(r"avg[^=]*=\s*[\d.]+/([\d.]+)", output)
        if match:
            return host, float(match.group(1)), "ok"
        if "100% packet loss" in output or "100.0% packet loss" in output:
            return host, None, "unreachable"
        return host, None, "no avg in output"
    except subprocess.TimeoutExpired:
        return host, None, "timeout"
    except FileNotFoundError:
        return host, None, "ping not found"


def load_targets(args_list: list[str]) -> list[str]:
    targets = []
    for a in args_list:
        if "." in a or ":" in a:
            targets.append(a)
        else:
            try:
                with open(a) as f:
                    targets += [l.strip() for l in f if l.strip() and not l.startswith("#")]
            except FileNotFoundError:
                print(f"File not found: {a}")
    return targets


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="+")
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()

    hosts = load_targets(args.targets)
    if not hosts:
        print("No hosts to ping.")
        sys.exit(1)

    results = []
    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(ping_host, h, args.count): h for h in hosts}
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda x: (x[1] is None, x[1] or 0))

    print(f"\n{'Host':<30} {'Avg RTT':>10}  Status")
    print("-" * 50)
    for host, rtt, status in results:
        rtt_str = f"{rtt:.2f} ms" if rtt is not None else "—"
        print(f"{host:<30} {rtt_str:>10}  {status}")
