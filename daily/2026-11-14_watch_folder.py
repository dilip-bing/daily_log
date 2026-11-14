"""
watch_folder.py
Poll a directory every N seconds and print when files are added,
removed, or modified. No external dependencies.

Usage:
    python watch_folder.py ./downloads --interval 2
"""

import argparse
import os
import time


def snapshot(folder: str) -> dict[str, float]:
    state = {}
    for dirpath, _, filenames in os.walk(folder):
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                state[path] = os.path.getmtime(path)
            except OSError:
                pass
    return state


def watch(folder: str, interval: float):
    print(f"Watching {folder}  (interval={interval}s)  Ctrl+C to stop\n")
    before = snapshot(folder)

    while True:
        time.sleep(interval)
        after = snapshot(folder)

        added   = set(after) - set(before)
        removed = set(before) - set(after)
        modified = {p for p in before if p in after and before[p] != after[p]}

        for p in sorted(added):
            print(f"  [+] {p}")
        for p in sorted(removed):
            print(f"  [-] {p}")
        for p in sorted(modified):
            print(f"  [~] {p}")

        before = after


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", nargs="?", default=".")
    parser.add_argument("--interval", type=float, default=3.0)
    args = parser.parse_args()
    watch(args.folder, args.interval)
