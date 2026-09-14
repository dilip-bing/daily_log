"""
url_health_check.py
Check if a list of URLs return HTTP 200. Useful for monitoring
a set of personal APIs, services, or endpoints.

Usage:
    python url_health_check.py urls.txt
    python url_health_check.py https://api.github.com https://example.com
"""

import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed


def check(url: str) -> tuple[str, int | str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "healthcheck/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return url, resp.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except Exception as e:
        return url, str(e)


def load_urls(args: list[str]) -> list[str]:
    urls = []
    for arg in args:
        if arg.startswith("http"):
            urls.append(arg)
        else:
            try:
                with open(arg) as f:
                    urls += [l.strip() for l in f if l.strip() and not l.startswith("#")]
            except FileNotFoundError:
                print(f"File not found: {arg}")
    return urls


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: url_health_check.py <url|file> [...]")
        sys.exit(1)

    urls = load_urls(sys.argv[1:])
    if not urls:
        print("No URLs to check.")
        sys.exit(1)

    ok = fail = 0
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(check, u): u for u in urls}
        for future in as_completed(futures):
            url, status = future.result()
            symbol = "OK " if status == 200 else "ERR"
            print(f"  [{symbol}] {status:<6}  {url}")
            if status == 200:
                ok += 1
            else:
                fail += 1

    print(f"\n{ok} up  |  {fail} down  |  {len(urls)} total")
