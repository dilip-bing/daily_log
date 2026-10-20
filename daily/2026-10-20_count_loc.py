"""
count_loc.py
Count lines of code per file extension in a project directory.
Ignores blank lines and comment-only lines.

Usage:
    python count_loc.py ./my_project
"""

import os
import sys
from collections import defaultdict

CODE_EXTS = {".py", ".js", ".ts", ".go", ".rs", ".c", ".cpp", ".java",
             ".rb", ".sh", ".swift", ".kt", ".cs", ".html", ".css"}

COMMENT_PREFIXES = ("#", "//", "--", "/*", "*", "'''", '"""')


def is_blank_or_comment(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith(COMMENT_PREFIXES)


def count_loc(root: str):
    stats: dict[str, tuple[int, int]] = defaultdict(lambda: (0, 0))  # ext -> (files, lines)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "__pycache__", ".venv"}]
        for name in filenames:
            _, ext = os.path.splitext(name)
            if ext not in CODE_EXTS:
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8", errors="ignore") as f:
                    lines = sum(1 for l in f if not is_blank_or_comment(l))
                files, total = stats[ext]
                stats[ext] = (files + 1, total + lines)
            except OSError:
                pass

    if not stats:
        print("No code files found.")
        return

    print(f"{'Ext':<10} {'Files':>6}  {'Code lines':>12}")
    print("-" * 32)
    total_lines = 0
    for ext, (files, lines) in sorted(stats.items(), key=lambda x: -x[1][1]):
        print(f"{ext:<10} {files:>6}  {lines:>12,}")
        total_lines += lines
    print("-" * 32)
    print(f"{'TOTAL':<10} {'':>6}  {total_lines:>12,}")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    count_loc(root)
