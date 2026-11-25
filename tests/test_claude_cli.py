"""The `claude -p` stream renderer, fed by a fake CLI process (no real Claude call)."""

import io
import json

import claude_cli

EVENTS = [
    {"type": "system", "subtype": "init"},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "Reading the file."},
                                                  {"type": "tool_use", "name": "Read", "input": {"file_path": "x"}}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "file body"}]}},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "FINAL ANSWER"}]}},
    {"type": "result", "result": "FINAL ANSWER", "num_turns": 2, "duration_ms": 1200, "stop_reason": "end_turn"},
]


class FakePopen:
    def __init__(self, cmd, **kwargs):
        FakePopen.cmd, FakePopen.kwargs = cmd, kwargs
        self.stdout = io.StringIO("".join(json.dumps(e) + "\n" for e in EVENTS))
        self.returncode = 0

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_run_claude_streams_steps_and_returns_final_answer(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(claude_cli.shutil, "which", lambda name: "/usr/bin/claude")
    monkeypatch.setattr(claude_cli.subprocess, "Popen", FakePopen)

    answer = claude_cli.run_claude("goal", cwd=tmp_path, tools=["Read"], allowed=["Read(./**)"])

    assert answer == "FINAL ANSWER"
    out = capsys.readouterr().out
    assert "Reading the file." in out and "Read" in out and "file body" in out
    assert "FINAL ANSWER" not in out          # shown once by the caller, not while streaming
    assert FakePopen.kwargs["stdin"] is claude_cli.subprocess.DEVNULL
    assert FakePopen.cmd[FakePopen.cmd.index("--tools") + 1] == "Read"
    assert "--strict-mcp-config" in FakePopen.cmd
