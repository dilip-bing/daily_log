"""
my_ip_info.py
Fetch your current public IP address and geo-location info.
Uses the free ipinfo.io API — no key required.

Usage:
    python my_ip_info.py
    python my_ip_info.py --json
"""

import argparse
import json
import urllib.request


def fetch_ip_info() -> dict:
    url = "https://ipinfo.io/json"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode())


def display(info: dict):
    fields = [
        ("IP",       info.get("ip", "N/A")),
        ("Hostname", info.get("hostname", "N/A")),
        ("City",     info.get("city", "N/A")),
        ("Region",   info.get("region", "N/A")),
        ("Country",  info.get("country", "N/A")),
        ("Org",      info.get("org", "N/A")),
        ("Timezone", info.get("timezone", "N/A")),
        ("Location", info.get("loc", "N/A")),
    ]
    width = max(len(k) for k, _ in fields)
    print()
    for key, val in fields:
        print(f"  {key:<{width}}  {val}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print raw JSON")
    args = parser.parse_args()

    info = fetch_ip_info()
    if args.json:
        print(json.dumps(info, indent=2))
    else:
        display(info)
