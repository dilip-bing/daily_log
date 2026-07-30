"""
find_large_files.py
Recursively find files over a size threshold and list them sorted by size.

Usage:
    python find_large_files.py ./projects --min-mb 10 --top 20
"""

import argparse
import os


def find_large(root: str, min_bytes: int, top: int):
    results = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(path)
                if size >= min_bytes:
                    results.append((size, path))
            except OSError:
                pass

    results.sort(reverse=True)
    results = results[:top]

    if not results:
        print("No files found above threshold.")
        return

    print(f"{'Size':>12}  Path")
    print("-" * 60)
    for size, path in results:
        if size >= 1_073_741_824:
            label = f"{size/1_073_741_824:.2f} GB"
        elif size >= 1_048_576:
            label = f"{size/1_048_576:.2f} MB"
        else:
            label = f"{size/1024:.1f} KB"
        print(f"{label:>12}  {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--min-mb", type=float, default=50)
    parser.add_argument("--top", type=int, default=25)
    args = parser.parse_args()
    find_large(args.root, int(args.min_mb * 1_048_576), args.top)
