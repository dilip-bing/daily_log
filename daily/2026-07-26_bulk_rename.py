"""
bulk_rename.py
Rename files in a folder using find-and-replace on the filename.

Usage:
    python bulk_rename.py ./photos old_prefix new_prefix --dry-run
"""

import argparse
import os


def bulk_rename(folder: str, find: str, replace: str, dry_run: bool = False):
    renamed = 0
    for filename in sorted(os.listdir(folder)):
        if find in filename:
            new_name = filename.replace(find, replace)
            src = os.path.join(folder, filename)
            dst = os.path.join(folder, new_name)
            print(f"  {filename}  ->  {new_name}")
            if not dry_run:
                os.rename(src, dst)
            renamed += 1
    tag = "[dry-run] " if dry_run else ""
    print(f"\n{tag}{renamed} file(s) renamed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk rename files by pattern.")
    parser.add_argument("folder", help="Target folder")
    parser.add_argument("find", help="String to find in filename")
    parser.add_argument("replace", help="Replacement string")
    parser.add_argument("--dry-run", action="store_true", help="Preview without renaming")
    args = parser.parse_args()
    bulk_rename(args.folder, args.find, args.replace, args.dry_run)
