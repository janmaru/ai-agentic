"""Demo 1 (Claude Code CLI) - a plain LLM call: no tools, no loop."""

import tempfile
from pathlib import Path

from rich.panel import Panel

from claude_cli import console, run_claude, show_answer

PROMPT = "Spiega in tre brevi punti cos'è la finestra di contesto di un LLM."


def main() -> None:
    console.print(Panel(PROMPT, title="Utente", border_style="cyan"))
    # Cartella vuota: Claude Code non vede il nostro repository e risponde solo alla domanda.
    with tempfile.TemporaryDirectory() as empty, console.status("Sto pensando..."):
        answer = run_claude(PROMPT, cwd=Path(empty), tools=[""])
    show_answer(answer, title="Claude")


if __name__ == "__main__":
    main()
