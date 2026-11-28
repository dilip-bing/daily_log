"""
organize_by_ext.py
Sort files in a folder into subfolders by file extension.
e.g. report.pdf -> pdf/report.pdf

Usage:
    python organize_by_ext.py ./downloads --dry-run
"""

import argparse
import os
import shutil


EXT_MAP = {
    "images":    {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"},
    "videos":    {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "audio":     {".mp3", ".wav", ".flac", ".aac", ".ogg"},
    "docs":      {".pdf", ".doc", ".docx", ".odt", ".txt", ".md"},
    "sheets":    {".xls", ".xlsx", ".csv", ".tsv"},
    "code":      {".py", ".js", ".ts", ".go", ".rs", ".c", ".cpp", ".java", ".sh"},
    "archives":  {".zip", ".tar", ".gz", ".bz2", ".7z", ".rar"},
    "data":      {".json", ".yaml", ".yml", ".xml", ".toml"},
}


def ext_to_folder(ext: str) -> str:
    for folder, exts in EXT_MAP.items():
        if ext.lower() in exts:
            return folder
    return "misc"


def organize(folder: str, dry_run: bool):
    moved = 0
    for name in sorted(os.listdir(folder)):
        src = os.path.join(folder, name)
        if not os.path.isfile(src):
            continue
        _, ext = os.path.splitext(name)
        subfolder = ext_to_folder(ext) if ext else "no_ext"
        dst_dir = os.path.join(folder, subfolder)
        dst = os.path.join(dst_dir, name)
        print(f"  {name}  ->  {subfolder}/")
        if not dry_run:
            os.makedirs(dst_dir, exist_ok=True)
            shutil.move(src, dst)
        moved += 1

    tag = "[dry-run] " if dry_run else ""
    print(f"\n{tag}{moved} file(s) organized.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", nargs="?", default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    organize(args.folder, args.dry_run)
