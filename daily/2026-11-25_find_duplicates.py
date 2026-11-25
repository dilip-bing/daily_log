"""
find_duplicates.py
Scan a folder recursively and report duplicate files by MD5 hash.

Usage:
    python find_duplicates.py ./downloads
"""

import hashlib
import os
import sys
from collections import defaultdict


def file_hash(path: str, chunk: int = 8192) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while data := f.read(chunk):
            h.update(data)
    return h.hexdigest()


def find_duplicates(root: str):
    seen: dict[str, list[str]] = defaultdict(list)
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                seen[file_hash(path)].append(path)
            except (OSError, PermissionError):
                pass

    dupes = {h: paths for h, paths in seen.items() if len(paths) > 1}
    if not dupes:
        print("No duplicates found.")
        return

    total_wasted = 0
    for h, paths in dupes.items():
        size = os.path.getsize(paths[0])
        wasted = size * (len(paths) - 1)
        total_wasted += wasted
        print(f"\n[{h[:8]}]  {len(paths)} copies  ({size:,} bytes each)")
        for p in paths:
            print(f"  {p}")

    print(f"\nTotal wasted space: {total_wasted / 1024:.1f} KB")


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    find_duplicates(folder)
