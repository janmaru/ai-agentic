"""Local server behind the live demo windows in the slides.

The slide sends a prompt; this server runs `claude -p` for one of the three
predefined demos (same folder, tools and permissions as `make demo1/2/3`) and
streams each step back as Server-Sent Events. The slide can change the prompt,
never the command, the tools or the folder. Follow-up questions in the same
window resume the same Claude Code session (`--resume`), so it remembers.

Only listens on 127.0.0.1 and only answers pages served by `make serve`.
"""

import json
import os
import tempfile
import threading
from functools import cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import cli_01_simple_call as demo1
import cli_02_tool_use as demo2
import cli_03_agent as demo3
from claude_cli import ClaudeNotFound, stream_claude

PORT = int(os.getenv("LIVE_DEMO_PORT", "8765"))
ALLOWED_ORIGINS = {"http://localhost:8000", "http://127.0.0.1:8000"}
MAX_PROMPT = 2000


@cache
def empty_folder() -> Path:
    # Demo 1: cartella vuota, Claude Code non vede il nostro repository.
    # Resta la stessa finché il server è acceso, così la conversazione si può riprendere.
    return Path(tempfile.mkdtemp(prefix="demo1-"))


DEMOS = {
    "1": {"prompt": demo1.PROMPT, "folder": empty_folder, "tools": [""], "allowed": None, "system": None},
    "2": {"prompt": demo2.PROMPT, "folder": lambda: demo2.STORE,
          "tools": demo2.TOOLS, "allowed": demo2.ALLOWED, "system": None},
    "3": {"prompt": demo3.GOAL, "folder": lambda: demo3.WORKSPACE,
          "tools": demo3.TOOLS, "allowed": demo3.ALLOWED, "system": demo3.SYSTEM},
}

run_lock = threading.Lock()   # una demo alla volta
sessions: dict[str, str] = {}     # sessione Claude Code di ogni finestra, per le domande successive
last_report: dict[str, str] = {}  # ultimo report della demo 3, in attesa di approvazione


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # niente log rumorosi durante la presentazione
        pass

    def _origin_ok(self) -> bool:
        host = self.headers.get("Host", "")
        return host in (f"localhost:{PORT}", f"127.0.0.1:{PORT}") and self.headers.get("Origin") in ALLOWED_ORIGINS

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", self.headers.get("Origin", ""))
        self.send_header("Vary", "Origin")

    def _json(self, status: int, body: dict):
        data = json.dumps(body).encode()
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/run":
            return self._json(404, {"error": "not found"})
        if not self._origin_ok():
            return self._json(403, {"error": "origin not allowed"})
        query = parse_qs(url.query)
        key = query.get("demo", [""])[0]
        demo = DEMOS.get(key)
        if demo is None:
            return self._json(400, {"error": "demo sconosciuta"})
        prompt = (query.get("prompt", [""])[0].strip() or demo["prompt"])[:MAX_PROMPT]
        # continue=1: stessa conversazione della finestra; altrimenti si riparte da zero.
        resume = sessions.get(key) if query.get("continue", ["0"])[0] == "1" else None

        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        def send(step: dict):
            self.wfile.write(f"data: {json.dumps(step)}\n\n".encode())
            self.wfile.flush()

        if not run_lock.acquire(blocking=False):
            send({"kind": "error", "text": "C'è già una demo in esecuzione."})
            return send({"kind": "end"})
        try:
            for step in stream_claude(prompt, demo["folder"](), demo["tools"], demo["allowed"],
                                      demo["system"], resume):
                if step["kind"] == "done":
                    if step.get("session"):
                        sessions[key] = step["session"]
                    if key == "3":
                        last_report["text"] = demo3.clean_report(step["result"])
                        step["result"] = last_report["text"]
                        step["can_save"] = True
                send(step)
            send({"kind": "end"})
        except ClaudeNotFound as exc:
            send({"kind": "error", "text": str(exc)})
            send({"kind": "end"})
        except (BrokenPipeError, ConnectionResetError):
            pass  # la slide si è chiusa: stream_claude ha già fermato Claude Code
        finally:
            run_lock.release()

    def do_OPTIONS(self):
        if not self._origin_ok():
            return self._json(403, {"error": "origin not allowed"})
        self.send_response(204)
        self._cors()
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.end_headers()

    def do_POST(self):
        if urlparse(self.path).path != "/save-report":
            return self._json(404, {"error": "not found"})
        if not self._origin_ok():
            return self._json(403, {"error": "origin not allowed"})
        report = last_report.pop("text", None)
        if report is None:
            return self._json(409, {"error": "Nessun report da salvare: esegui prima la demo 3."})
        # Si salva solo il report prodotto dall'agente, mai testo inviato dal browser.
        (demo3.WORKSPACE / "report.md").write_text(report, encoding="utf-8")
        self._json(200, {"saved": "demo/workspace/report.md"})


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Demo live su http://127.0.0.1:{PORT} (Ctrl+C per fermare)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
