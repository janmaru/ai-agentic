"""Demo 3 - an autonomous agent loop.

Claude gets a goal and a few tools over a sandboxed folder, then decides on its
own what to read, what to compute and when it is done. The SDK tool runner
drives the loop; writing a file needs human approval (human-in-the-loop).
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

from anthropic import beta_tool
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm

from common import REQUEST_DEFAULTS, check_refusal, console, get_client

WORKSPACE = (Path(__file__).parent / "workspace").resolve()


def safe_path(name: str) -> Path:
    """Resolve a file name inside the workspace; refuse anything outside it."""
    path = (WORKSPACE / name).resolve()
    if not path.is_relative_to(WORKSPACE):
        raise ValueError(f"Access outside the workspace is not allowed: {name}")
    return path


def log_tool(name: str, args: dict) -> None:
    console.print(f"[yellow]→ tool[/yellow] [bold]{name}[/bold] {json.dumps(args)}")


@beta_tool
def list_files() -> str:
    """List the files available in the workspace folder."""
    log_tool("list_files", {})
    return "\n".join(sorted(p.name for p in WORKSPACE.iterdir() if p.is_file()))


@beta_tool
def read_file(name: str) -> str:
    """Read a text file from the workspace.

    Args:
        name: File name relative to the workspace, e.g. sales.csv.
    """
    log_tool("read_file", {"name": name})
    return safe_path(name).read_text(encoding="utf-8")


@beta_tool
def aggregate_csv(name: str, group_by: str, value_column: str) -> str:
    """Sum a numeric column of a CSV file, grouped by another column. Use this for exact totals.

    Args:
        name: CSV file name in the workspace.
        group_by: Column to group rows by, e.g. region.
        value_column: Numeric column to sum, e.g. revenue_eur.
    """
    log_tool("aggregate_csv", {"name": name, "group_by": group_by, "value_column": value_column})
    totals: dict[str, float] = defaultdict(float)
    with safe_path(name).open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row[group_by]] += float(row[value_column])
    return json.dumps(dict(sorted(totals.items(), key=lambda kv: -kv[1])))


@beta_tool
def write_file(name: str, content: str) -> str:
    """Write a text file to the workspace. A human must approve each write.

    Args:
        name: File name relative to the workspace, e.g. report.md.
        content: Full text content of the file.
    """
    log_tool("write_file", {"name": name, "chars": len(content)})
    console.print(Panel(Markdown(content), title=f"Proposed {name}", border_style="magenta"))
    if not Confirm.ask(f"Allow the agent to write [bold]{name}[/bold]?", default=True):
        return "The user declined this write. Ask what to change instead."
    safe_path(name).write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} characters to {name}."


SYSTEM = (
    "You are an analyst agent working in a sandboxed folder. "
    "Use the tools to inspect files, compute exact numbers with aggregate_csv rather than "
    "doing arithmetic yourself, and save deliverables with write_file. "
    "Before each tool call, say in one short sentence what you are about to do."
)

GOAL = "Check the workspace for a request from the sales director and complete it."

client = get_client()
console.print(Panel(GOAL, title="Goal", border_style="cyan"))

runner = client.beta.messages.tool_runner(
    **REQUEST_DEFAULTS,
    output_config={"effort": "medium"},
    system=SYSTEM,
    tools=[list_files, read_file, aggregate_csv, write_file],
    messages=[{"role": "user", "content": GOAL}],
)

turn = 0
for message in runner:
    turn += 1
    console.rule(f"[dim]turn {turn} · stop_reason={message.stop_reason}[/dim]")
    if check_refusal(message):
        break
    for block in message.content:
        if block.type == "text" and block.text.strip():
            style = "green" if message.stop_reason == "end_turn" else "white"
            console.print(Markdown(block.text), style=style)

console.print(f"\n[bold green]Done in {turn} model turns.[/bold green]")
