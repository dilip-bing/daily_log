"""
safe_delete.py
Move files to a ~/.trash folder instead of permanently deleting them.
Acts as a safer alternative to `rm`.

Usage:
    python safe_delete.py file1.txt file2.log ./old_folder
"""

import os
import shutil
import sys
from datetime import datetime

TRASH = os.path.expanduser("~/.trash")


def safe_delete(paths: list[str]):
    os.makedirs(TRASH, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for path in paths:
        if not os.path.exists(path):
            print(f"  [skip] not found: {path}")
            continue

        name = os.path.basename(path.rstrip("/"))
        dest = os.path.join(TRASH, f"{timestamp}__{name}")

        shutil.move(path, dest)
        kind = "dir" if os.path.isdir(dest) else "file"
        print(f"  [{kind}] {path}  ->  {dest}")

    print(f"\nRestore from: {TRASH}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: safe_delete.py <path> [path ...]")
        sys.exit(1)
    safe_delete(sys.argv[1:])
