"""The slide demo server, with a fake `claude -p` (no real Claude call)."""

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

import claude_cli
import live_server
from test_claude_cli import FakePopen

ORIGIN = "http://localhost:8000"


@pytest.fixture
def server(monkeypatch, tmp_path):
    monkeypatch.setattr(claude_cli.shutil, "which", lambda name: "/usr/bin/claude")
    monkeypatch.setattr(claude_cli.subprocess, "Popen", FakePopen)
    monkeypatch.setattr(live_server.demo3, "WORKSPACE", tmp_path)
    live_server.last_report.clear()
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), live_server.Handler)
    monkeypatch.setattr(live_server, "PORT", httpd.server_address[1])
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def request(url, origin=ORIGIN, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"Origin": origin})
    return urllib.request.urlopen(req, timeout=5)


def events(url):
    with request(url) as res:
        body = res.read().decode()
    return [json.loads(chunk[len("data: "):]) for chunk in body.split("\n\n") if chunk.startswith("data: ")]


def test_run_streams_steps_with_the_demo_settings(server):
    steps = events(f"{server}/run?demo=2&prompt=Dove%20sono%20i%20miei%20ordini%3F")

    assert [s["kind"] for s in steps] == ["text", "tool", "tool_result", "text", "done", "end"]
    assert steps[4]["result"] == "FINAL ANSWER"
    cmd = FakePopen.cmd
    assert cmd[cmd.index("-p") + 1] == "Dove sono i miei ordini?"      # prompt from the slide
    assert cmd[cmd.index("--tools") + 1] == "Read"                    # tools from demo 2, not the slide
    assert FakePopen.kwargs["cwd"] == live_server.demo2.STORE


def test_follow_up_resumes_the_same_session(server):
    live_server.sessions.clear()
    events(f"{server}/run?demo=2")
    assert "--resume" not in FakePopen.cmd                            # first question: new session

    events(f"{server}/run?demo=2&continue=1&prompt=E%20l%27altro%3F")
    assert FakePopen.cmd[FakePopen.cmd.index("--resume") + 1] == "sess-123"

    events(f"{server}/run?demo=2&continue=0")
    assert "--resume" not in FakePopen.cmd                            # "Nuova": starts over


def test_rejects_other_origins_and_unknown_demos(server):
    with pytest.raises(urllib.error.HTTPError) as err:
        request(f"{server}/run?demo=1", origin="http://evil.example")
    assert err.value.code == 403
    with pytest.raises(urllib.error.HTTPError) as err:
        request(f"{server}/run?demo=9")
    assert err.value.code == 400


def test_save_writes_only_the_agent_report(server, tmp_path):
    with pytest.raises(urllib.error.HTTPError) as err:
        request(f"{server}/save-report", method="POST")
    assert err.value.code == 409                                      # nothing to approve yet

    done = events(f"{server}/run?demo=3")[-2]
    assert done["can_save"] is True
    with request(f"{server}/save-report", method="POST") as res:
        assert res.status == 200
    assert (tmp_path / "report.md").read_text() == "FINAL ANSWER\n"


def test_demo_4_is_text_only_and_uses_the_slide_prompt(server):
    steps = events(f"{server}/run?demo=4&prompt=Spiega%20REST")

    assert steps[-1]["kind"] == "end"
    cmd = claude_cli_cmd = __import__("test_claude_cli").FakePopen.cmd
    assert cmd[cmd.index("-p") + 1] == "Spiega REST"
    assert cmd[cmd.index("--tools") + 1] == ""                        # nessuno strumento


def test_demo_5_is_text_only_and_uses_the_slide_prompt(server):
    steps = events(f"{server}/run?demo=5&prompt=Dammi%20cinque%20nomi")

    assert steps[-1]["kind"] == "end"
    cmd = claude_cli_cmd = __import__("test_claude_cli").FakePopen.cmd
    assert cmd[cmd.index("-p") + 1] == "Dammi cinque nomi"
    assert cmd[cmd.index("--tools") + 1] == ""                        # nessuno strumento


def test_demo_6_is_text_only_and_uses_the_slide_prompt(server):
    steps = events(f"{server}/run?demo=6&prompt=Ricava%20la%20skill")

    assert steps[-1]["kind"] == "end"
    cmd = __import__("test_claude_cli").FakePopen.cmd
    assert cmd[cmd.index("-p") + 1] == "Ricava la skill"
    assert cmd[cmd.index("--tools") + 1] == ""                        # nessuno strumento


def test_demo_7_is_text_only_and_uses_the_slide_prompt(server):
    steps = events(f"{server}/run?demo=7&prompt=Rivedi%20il%20file")

    assert steps[-1]["kind"] == "end"
    cmd = __import__("test_claude_cli").FakePopen.cmd
    assert cmd[cmd.index("-p") + 1] == "Rivedi il file"
    assert cmd[cmd.index("--tools") + 1] == ""                        # nessuno strumento


def test_demo_8_is_text_only_and_uses_the_slide_prompt(server):
    steps = events(f"{server}/run?demo=8&prompt=Intervistami")

    assert steps[-1]["kind"] == "end"
    cmd = __import__("test_claude_cli").FakePopen.cmd
    assert cmd[cmd.index("-p") + 1] == "Intervistami"
    assert cmd[cmd.index("--tools") + 1] == ""                        # nessuno strumento
