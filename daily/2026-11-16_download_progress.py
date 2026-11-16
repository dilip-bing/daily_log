"""
download_progress.py
Download a file from a URL and show a live progress bar.
No external dependencies.

Usage:
    python download_progress.py https://example.com/file.zip
    python download_progress.py https://example.com/file.zip -o ./output/file.zip
"""

import argparse
import os
import sys
import urllib.request
from urllib.parse import urlparse


def progress_hook(count, block_size, total_size):
    if total_size <= 0:
        downloaded = count * block_size
        sys.stdout.write(f"\r  Downloaded {downloaded:,} bytes")
        sys.stdout.flush()
        return

    percent = min(count * block_size / total_size, 1.0)
    bar_len = 40
    filled = int(bar_len * percent)
    bar = "█" * filled + "░" * (bar_len - filled)
    downloaded = min(count * block_size, total_size)
    total_mb = total_size / 1_048_576
    done_mb = downloaded / 1_048_576
    sys.stdout.write(f"\r  [{bar}] {percent*100:5.1f}%  {done_mb:.2f}/{total_mb:.2f} MB")
    sys.stdout.flush()


def download(url: str, dest: str):
    print(f"Downloading: {url}")
    print(f"Saving to:   {dest}\n")
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    urllib.request.urlretrieve(url, dest, reporthook=progress_hook)
    size = os.path.getsize(dest)
    print(f"\n\nDone — {size/1_048_576:.2f} MB saved to {dest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-o", "--output", default=None)
    args = parser.parse_args()

    filename = os.path.basename(urlparse(args.url).path) or "download"
    dest = args.output or os.path.join(".", filename)
    download(args.url, dest)
