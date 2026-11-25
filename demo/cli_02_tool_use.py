"""Demo 2 (Claude Code CLI) - tool use.

Claude cannot see the order database; it has to ask for the Read tool.
The harness (Claude Code) executes it and feeds the result back.
"""

from pathlib import Path

from rich.panel import Panel

from claude_cli import console, run_claude, show_answer

STORE = Path(__file__).parent / "store"
PROMPT = "Buongiorno, sono il signor Rossi. Dove sono i miei ordini e quando arriveranno? Il database degli ordini è orders.json."


def main() -> None:
    console.print(Panel(PROMPT, title="Utente", border_style="cyan"))
    answer = run_claude(PROMPT, cwd=STORE, tools=["Read"], allowed=["Read(./**)"])
    show_answer(answer)


if __name__ == "__main__":
    main()
