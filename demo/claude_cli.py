"""Run Claude Code headless (`claude -p`) and render its agent loop live.

Uses your Claude Code login (subscription), not API credits.
`stream_claude` yields the steps as plain dicts (used by the slide server);
`run_claude` prints them in the terminal.
"""

import json
import os
import shutil
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

MODEL = os.getenv("DEMO_CLI_MODEL")  # unset = your Claude Code default


class ClaudeNotFound(RuntimeError):
    """The `claude` CLI is not installed or not on PATH."""


def build_command(prompt: str, tools: list[str], allowed: list[str] | None = None,
                  system: str | None = None, resume: str | None = None) -> list[str]:
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "stream-json", "--verbose",
        "--strict-mcp-config",              # no MCP servers: only the tools we list
        "--tools", ",".join(tools),         # "" = no tools at all
    ]
    if allowed:
        cmd += ["--allowedTools", *allowed]
    if system:
        cmd += ["--append-system-prompt", system]
    if resume:
        cmd += ["--resume", resume]        # stessa sessione: Claude ricorda le domande precedenti
    if MODEL:
        cmd += ["--model", MODEL]
    return cmd


def stream_claude(prompt: str, cwd: Path, tools: list[str], allowed: list[str] | None = None,
                  system: str | None = None, resume: str | None = None) -> Iterator[dict]:
    """Run one headless Claude Code session and yield its steps.

    Kinds: text (Claude's commentary), tool (a tool call), tool_result,
    done (final answer, stats and the session id to resume), error (non-zero exit).
    """
    if shutil.which("claude") is None:
        raise ClaudeNotFound("Claude Code CLI non trovato: installalo ed esegui `claude` una volta per il login.")

    cmd = build_command(prompt, tools, allowed, system, resume)
    with subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True) as proc:
        try:
            for line in proc.stdout:
                event = json.loads(line)
                kind = event.get("type")
                if kind == "assistant":
                    for block in event["message"]["content"]:
                        if block["type"] == "tool_use":
                            yield {"kind": "tool", "name": block["name"], "input": block["input"]}
                        elif block["type"] == "text" and block["text"].strip():
                            yield {"kind": "text", "text": block["text"]}
                elif kind == "user":
                    for block in event["message"]["content"]:
                        if isinstance(block, dict) and block.get("type") == "tool_result":
                            content = block["content"]
                            text = content if isinstance(content, str) else json.dumps(content)
                            yield {"kind": "tool_result", "text": text, "error": bool(block.get("is_error"))}
                elif kind == "result":
                    yield {
                        "kind": "done",
                        "result": event.get("result", ""),
                        "turns": event.get("num_turns"),
                        "seconds": round(event.get("duration_ms", 0) / 1000, 1),
                        "stop": event.get("stop_reason") or event.get("subtype"),
                        "session": event.get("session_id"),
                    }
        finally:
            # Consumer gone early (e.g. the browser left the slide): stop Claude Code too.
            if proc.poll() is None:
                proc.kill()
    if proc.returncode:
        yield {"kind": "error", "text": f"claude è terminato con codice {proc.returncode}"}


def run_claude(prompt: str, cwd: Path, tools: list[str], allowed: list[str] | None = None,
               system: str | None = None) -> str:
    """Run one headless Claude Code session, print each step, return the final text."""
    final = ""
    pending: list[str] = []  # text is shown only once a tool call follows; the last text is the answer
    try:
        for step in stream_claude(prompt, cwd, tools, allowed, system):
            if step["kind"] == "tool":
                for text in pending:
                    console.print(Markdown(text), style="dim")
                pending.clear()
                console.print(f"[yellow]→ strumento[/yellow] [bold]{step['name']}[/bold] {json.dumps(step['input'])}")
            elif step["kind"] == "text":
                pending.append(step["text"])
            elif step["kind"] == "tool_result":
                style = "red" if step["error"] else "magenta"
                console.print(f"[{style}]← risultato[/{style}] {step['text'][:160].replace(chr(10), ' ')}…")
            elif step["kind"] == "done":
                final = step["result"]
                console.print(f"[dim]turni: {step['turns']}  tempo: {step['seconds']:.1f}s  stop: {step['stop']}[/dim]")
            elif step["kind"] == "error":
                console.print(f"[red]{step['text']}[/red]")
                sys.exit(1)
    except ClaudeNotFound as exc:
        console.print(f"[red]{exc}[/red]")
        sys.exit(1)
    return final


def show_answer(text: str, title: str = "Claude - risposta finale") -> None:
    console.print(Panel(Markdown(text), title=title, border_style="green"))
