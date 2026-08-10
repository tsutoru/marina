import subprocess, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        prop = query.get("prop", ["(a&b | c)->d  <->  ~e"])[0]
        result = subprocess.run(["./marina", prop], capture_output=True, text=True)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(result.stdout.encode())

port = int(os.environ.get("PORT", 8080))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()