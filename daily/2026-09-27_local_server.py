"""
local_server.py
Spin up a local HTTP file server with optional file upload support.
Great for quickly sharing files on a LAN.

Usage:
    python local_server.py                  # serve current dir on port 8000
    python local_server.py ./dist -p 9000   # serve ./dist on port 9000
    python local_server.py --upload         # enable file upload via POST
"""

import argparse
import http.server
import os
import socket


class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)
        filename = self.headers.get("X-Filename", "uploaded_file")
        safe_name = os.path.basename(filename)
        dest = os.path.join(os.getcwd(), safe_name)
        with open(dest, "wb") as f:
            f.write(data)
        print(f"  [upload] {safe_name}  ({len(data):,} bytes)")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} - {fmt % args}")


def get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "localhost"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default=".")
    parser.add_argument("-p", "--port", type=int, default=8000)
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()

    os.chdir(args.directory)
    handler = UploadHandler if args.upload else http.server.SimpleHTTPRequestHandler
    local_ip = get_local_ip()

    print(f"\nServing {os.getcwd()}")
    print(f"  Local:   http://localhost:{args.port}")
    print(f"  Network: http://{local_ip}:{args.port}")
    if args.upload:
        print(f"  Upload:  curl -X POST -H 'X-Filename: file.txt' --data-binary @file.txt http://localhost:{args.port}")
    print("\nCtrl+C to stop\n")

    with http.server.HTTPServer(("", args.port), handler) as httpd:
        httpd.serve_forever()
