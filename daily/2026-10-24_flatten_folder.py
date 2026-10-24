"""
flatten_folder.py
Move all files from nested subdirectories into a single output folder.
Handles filename collisions by appending a counter.

Usage:
    python flatten_folder.py ./nested_photos ./flat_output --dry-run
"""

import argparse
import os
import shutil


def flatten(src: str, dst: str, dry_run: bool = False):
    os.makedirs(dst, exist_ok=True)
    moved = 0
    for dirpath, _, filenames in os.walk(src):
        if os.path.abspath(dirpath) == os.path.abspath(dst):
            continue
        for name in filenames:
            src_path = os.path.join(dirpath, name)
            dst_path = os.path.join(dst, name)
            # Resolve collision
            counter = 1
            stem, ext = os.path.splitext(name)
            while os.path.exists(dst_path):
                dst_path = os.path.join(dst, f"{stem}_{counter}{ext}")
                counter += 1
            print(f"  {src_path}  ->  {dst_path}")
            if not dry_run:
                shutil.copy2(src_path, dst_path)
            moved += 1

    tag = "[dry-run] " if dry_run else ""
    print(f"\n{tag}{moved} file(s) flattened into {dst}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="Source folder (nested)")
    parser.add_argument("dst", help="Destination folder (flat)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    flatten(args.src, args.dst, args.dry_run)
