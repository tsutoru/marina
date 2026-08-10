import subprocess, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        # Seuls "/" et "/solve" sont des routes valides
        if parsed.path not in ("/", "/solve"):
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found\n")
            return

        query = parse_qs(parsed.query)
        prop = query.get("prop", ["(a&b | c)->d  <->  ~e"])[0]

        result = subprocess.run(["./marina", prop], capture_output=True, text=True)

        if result.returncode != 0:
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            body = f"400 Bad Request: proposition invalide\n{result.stderr}"
            self.wfile.write(body.encode())
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(result.stdout.encode())

port = int(os.environ.get("PORT", 8080))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()