import subprocess, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):

    def _respond(self, status, body):
        body_bytes = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    def _solve(self, prop):
        prop = prop.strip()
        if not prop:
            self._respond(400, "Erreur: parametre 'prop' manquant\n")
            return
        result = subprocess.run(["./marina", prop], capture_output=True, text=True)
        if result.returncode != 0:
            self._respond(400, f"Erreur: proposition invalide\n{result.stderr}")
        else:
            self._respond(200, result.stdout)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/health":
            self._respond(200, "ok")

        elif parsed.path == "/what":
            self._respond(200,
                "marina SAT solver.\n"
                "GET  /solve?prop=<expr>\n"
                "POST /solve  (body = expr)\n")

        elif parsed.path == "/solve":
            query = parse_qs(parsed.query)
            prop = query.get("prop", [""])[0]
            self._solve(prop)

        else:
            self._respond(404, "Not found\n")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/solve":
            self._respond(404, "Not found\n")
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else ""
        self._solve(body)

port = int(os.environ.get("PORT", 8080))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()