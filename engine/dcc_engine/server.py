"""Localhost table. The player page and the GM page are the eyes. Discord is still the voice."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from dcc_engine.pages import GM_HTML, PLAYER_HTML
from dcc_engine.table import Table


class TableHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in {"/", "/player"}:
            self._bytes(200, PLAYER_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/gm":
            self._bytes(200, GM_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        with self.server.lock:
            if path == "/api/player":
                self._json(200, self.server.table.player_view())
                return
            if path == "/api/gm":
                self._json(200, self.server.table.gm_view())
                return
        self._json(404, {"error": "not found"})

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            body = self._body()
        except ValueError as exc:
            self._json(400, {"error": str(exc)})
            return
        try:
            with self.server.lock:
                table = self.server.table
                if path == "/api/line":
                    rng = None
                    scripts = getattr(self.server, "scripts", None)
                    if scripts:
                        from dcc_engine.table import ScriptedRng
                        rng = ScriptedRng(scripts.pop(0))
                    result = table.resolve_line(body.get("text", ""), rng=rng)
                    self._json(200, result)
                    return
                if path == "/api/seat":
                    self._json(200, {"view": table.seat(body)})
                    return
                if path == "/api/undo":
                    self._json(200, {"view": table.undo()})
                    return
                if path == "/api/correct":
                    self._json(200, {"view": table.correct_hp(body.get("id"), body.get("hp"))})
                    return
        except ValueError as exc:
            self._json(400, {"error": str(exc)})
            return
        self._json(404, {"error": "not found"})

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length > 8000:
            raise ValueError("body too large")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("body must be JSON") from exc
        if not isinstance(data, dict):
            raise ValueError("body must be a JSON object")
        return data

    def _json(self, status, payload):
        data = json.dumps(payload).encode("utf-8")
        self._bytes(status, data, "application/json; charset=utf-8")

    def _bytes(self, status, data, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def make_server(host, port, party_size=2):
    import threading

    httpd = ThreadingHTTPServer((host, port), TableHandler)
    httpd.table = Table(party_size=party_size)
    httpd.scripts = []
    httpd.lock = threading.Lock()
    return httpd


def serve_background(host, port, party_size=2):
    import threading

    httpd = make_server(host, port, party_size=party_size)
    thread = threading.Thread(target=httpd.serve_forever, name="dcc-table", daemon=True)
    thread.start()
    httpd.thread = thread
    return httpd
