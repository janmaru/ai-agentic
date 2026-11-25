"""Demo 3 (Claude Code CLI) - an autonomous agent with a human approval gate.

Claude Code explores the workspace on its own (read-only), works out the task
and drafts the deliverable. Writing it to disk is our code's job, and only
after a human approves.
"""

from pathlib import Path

from rich.panel import Panel
from rich.prompt import Confirm

from claude_cli import console, run_claude, show_answer

WORKSPACE = Path(__file__).parent / "workspace"

GOAL = "Check this folder for a request from the sales director and complete it."

SYSTEM = (
    "You are an analyst agent with read-only access to the current folder. "
    "Explore it with your tools, compute the numbers carefully from the data, "
    "and before each tool call say in one short sentence what you are about to do. "
    "You cannot write files: reply with the full content of the requested deliverable "
    "as Markdown and nothing else, and it will be saved for you after review."
)


def main() -> None:
    console.print(Panel(GOAL, title="Goal", border_style="cyan"))
    report = run_claude(GOAL, cwd=WORKSPACE, tools=["Read", "Glob", "Grep"],
                        allowed=["Read(./**)", "Glob", "Grep"], system=SYSTEM)
    show_answer(report, title="Proposed report.md")

    if Confirm.ask("Allow the agent's report to be saved as [bold]report.md[/bold]?", default=True):
        (WORKSPACE / "report.md").write_text(report, encoding="utf-8")
        console.print("[bold green]Saved demo/workspace/report.md[/bold green]")
    else:
        console.print("[yellow]Declined - nothing written.[/yellow]")


if __name__ == "__main__":
    main()
