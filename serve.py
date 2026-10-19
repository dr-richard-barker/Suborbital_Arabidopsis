#!/usr/bin/env python3
"""
serve.py — Directory-bound local web server for the CoSE presentation portal.
Follows the canonical CoSE hardened web server pattern.
"""
import sys
import os
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent / "docs"

def run_server(port=8080):
    handler = partial(SimpleHTTPRequestHandler, directory=str(DOCS_DIR))
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, handler)
    print(f"🚀 Serving CoSE Suborbital Arabidopsis Portal at http://127.0.0.1:{port}/")
    print(f"📁 Root directory: {DOCS_DIR}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(p)
