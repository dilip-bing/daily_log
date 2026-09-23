"""
tree_view.py
Print a Unix-style tree of a directory. No external deps.

Usage:
    python tree_view.py ./my_project --depth 3 --show-hidden
"""

import argparse
import os


def tree(path: str, prefix: str, depth: int, max_depth: int, show_hidden: bool):
    if depth > max_depth:
        return
    try:
        entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        return

    entries = [e for e in entries if show_hidden or not e.name.startswith(".")]
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        print(prefix + connector + entry.name)
        if entry.is_dir(follow_symlinks=False):
            extension = "    " if i == len(entries) - 1 else "│   "
            tree(entry.path, prefix + extension, depth + 1, max_depth, show_hidden)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--show-hidden", action="store_true")
    args = parser.parse_args()
    print(args.path)
    tree(args.path, "", 1, args.depth, args.show_hidden)
