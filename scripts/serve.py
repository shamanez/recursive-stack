#!/usr/bin/env python3
"""Serve the dashboard over HTTP for checking it in a browser.

    python3 scripts/serve.py [port]     # default 8765

Stdlib only. Serves the repository root regardless of the directory it is run
from, and sends no-cache headers so a rebuild is always what you see. See
playbooks/check-page.md for why to use this instead of opening index.html in an
agent's preview pane.
"""
import functools
import http.server
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):  # keep the terminal quiet
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    handler = functools.partial(Handler, directory=str(ROOT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"serving {ROOT} at http://127.0.0.1:{port}  (Ctrl-C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()
