"""
file_age_report.py
Show files in a folder grouped by how old they are: today, this week,
this month, this year, older.

Usage:
    python file_age_report.py ./downloads
"""

import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict


def categorize(mtime: float, now: datetime) -> str:
    dt = datetime.fromtimestamp(mtime)
    delta = now - dt
    if delta < timedelta(days=1):
        return "today"
    if delta < timedelta(weeks=1):
        return "this week"
    if delta < timedelta(days=30):
        return "this month"
    if delta < timedelta(days=365):
        return "this year"
    return "older"


ORDER = ["today", "this week", "this month", "this year", "older"]


def report(folder: str):
    now = datetime.now()
    buckets: dict[str, list[tuple[float, str]]] = defaultdict(list)

    for dirpath, _, filenames in os.walk(folder):
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                mtime = os.path.getmtime(path)
                size  = os.path.getsize(path)
                bucket = categorize(mtime, now)
                buckets[bucket].append((size, path))
            except OSError:
                pass

    for label in ORDER:
        files = buckets.get(label, [])
        total = sum(s for s, _ in files)
        print(f"\n── {label.upper()}  ({len(files)} files, {total/1024:.0f} KB total) ──")
        for size, path in sorted(files, key=lambda x: -x[0])[:10]:
            print(f"  {size/1024:>8.1f} KB  {path}")
        if len(files) > 10:
            print(f"  ... and {len(files)-10} more")


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    report(folder)
