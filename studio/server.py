#!/usr/bin/env python3
"""MIRACDX Studio — local editing server.
Serves the repo over http://127.0.0.1:7799 and adds two endpoints:
  GET  /__list           -> JSON list of editable .html files in the repo
  POST /__save           -> {"path": "...", "html": "..."} writes the file
Local-only (binds 127.0.0.1). No password by design.
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 7799
# repo root = parent of this /studio folder
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def list_html():
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for f in files:
            if f.lower().endswith(".html"):
                rel = os.path.relpath(os.path.join(base, f), ROOT).replace("\\", "/")
                out.append(rel)
    out.sort()
    return out


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def _json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/__list":
            return self._json(200, {"files": list_html()})
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/__save":
            return self._json(404, {"ok": False, "error": "unknown endpoint"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            rel = (data.get("path") or "").lstrip("/").replace("\\", "/")
            html = data.get("html", "")
            if not rel.lower().endswith(".html"):
                return self._json(400, {"ok": False, "error": "only .html files allowed"})
            target = os.path.abspath(os.path.join(ROOT, rel))
            # safety: must stay inside repo
            if not target.startswith(ROOT + os.sep) and target != ROOT:
                return self._json(403, {"ok": False, "error": "path outside repo"})
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(html)
            return self._json(200, {"ok": True, "path": rel, "bytes": len(html)})
        except Exception as e:  # noqa
            return self._json(500, {"ok": False, "error": str(e)})

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass  # quiet


def main():
    os.chdir(ROOT)
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = "http://127.0.0.1:%d/studio/studio.html" % PORT
    sys.stdout.write("MIRACDX Studio running at " + url + "\n")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == "__main__":
    main()
