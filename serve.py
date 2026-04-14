#!/usr/bin/env python3
"""Local dev server that serves 404.html for missing paths, matching GitHub Pages routing."""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class Router(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open(os.path.join(os.path.dirname(__file__), "404.html"), "rb") as f:
                self.wfile.write(f.read())
        else:
            super().send_error(code, message, explain)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(("", 8080), Router)
    print("Serving at http://localhost:8080")
    server.serve_forever()
