"""Run Claude Code headless (`claude -p`) and render its agent loop live.

Uses your Claude Code login (subscription), not API credits.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

MODEL = os.getenv("DEMO_CLI_MODEL")  # unset = your Claude Code default


def run_claude(prompt: str, cwd: Path, tools: list[str], allowed: list[str] | None = None,
               system: str | None = None) -> str:
    """Run one headless Claude Code session, print each step, return the final text."""
    if shutil.which("claude") is None:
        console.print("[red]Claude Code CLI not found.[/red] Install it and run `claude` once to log in.")
        sys.exit(1)

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
    if MODEL:
        cmd += ["--model", MODEL]

    final = ""
    pending: list[str] = []  # text is shown only once a tool call follows; the last text is the answer
    with subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True) as proc:
        for line in proc.stdout:
            event = json.loads(line)
            kind = event.get("type")
            if kind == "assistant":
                for block in event["message"]["content"]:
                    if block["type"] == "tool_use":
                        for text in pending:
                            console.print(Markdown(text), style="dim")
                        pending.clear()
                        console.print(f"[yellow]→ tool[/yellow] [bold]{block['name']}[/bold] {json.dumps(block['input'])}")
                    elif block["type"] == "text" and block["text"].strip():
                        pending.append(block["text"])
            elif kind == "user":
                for block in event["message"]["content"]:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        content = block["content"]
                        text = content if isinstance(content, str) else json.dumps(content)
                        style = "red" if block.get("is_error") else "magenta"
                        console.print(f"[{style}]← result[/{style}] {text[:160].replace(chr(10), ' ')}…")
            elif kind == "result":
                final = event.get("result", "")
                console.print(
                    f"[dim]turns: {event.get('num_turns')}  time: {event.get('duration_ms', 0) / 1000:.1f}s  "
                    f"stop: {event.get('stop_reason') or event.get('subtype')}[/dim]"
                )
    if proc.returncode:
        console.print(f"[red]claude exited with code {proc.returncode}[/red]")
        sys.exit(proc.returncode)
    return final


def show_answer(text: str, title: str = "Claude - final answer") -> None:
    console.print(Panel(Markdown(text), title=title, border_style="green"))
