"""Demo 1 (Claude Code CLI) - a plain LLM call: no tools, no loop."""

from pathlib import Path

from rich.panel import Panel

from claude_cli import console, run_claude, show_answer

PROMPT = "In three short bullet points: what is the difference between a chatbot and an AI agent?"


def main() -> None:
    console.print(Panel(PROMPT, title="User", border_style="cyan"))
    with console.status("Thinking..."):
        answer = run_claude(PROMPT, cwd=Path(__file__).parent, tools=[""])
    show_answer(answer, title="Claude")


if __name__ == "__main__":
    main()
