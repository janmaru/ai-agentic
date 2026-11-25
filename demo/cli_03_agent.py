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


class Conferma(Confirm):
    """Domanda sì/no che accetta s/n."""

    choices = ["s", "n"]
    validate_error_message = "[prompt.invalid]Rispondi s oppure n"

GOAL = "Cerca in questa cartella una richiesta del direttore commerciale e portala a termine."

SYSTEM = (
    "Sei un agente analista con accesso in sola lettura alla cartella corrente. "
    "Esplorala con i tuoi strumenti, calcola i numeri con attenzione a partire dai dati "
    "e prima di ogni chiamata a uno strumento di' in una breve frase cosa stai per fare. "
    "Non puoi scrivere file: la tua risposta finale viene salvata così com'è dopo la revisione. "
    "Deve essere solo il documento richiesto, in Markdown e in italiano, "
    "a partire dal titolo (# ...), senza introduzioni né commenti. "
    "Nel documento non parlare di file, permessi o salvataggio: scrivi per il direttore commerciale."
)


def main() -> None:
    console.print(Panel(GOAL, title="Obiettivo", border_style="cyan"))
    report = run_claude(GOAL, cwd=WORKSPACE, tools=["Read", "Glob", "Grep"],
                        allowed=["Read(./**)", "Glob", "Grep"], system=SYSTEM)
    # Per sicurezza: tutto quello che precede il primo titolo non fa parte del documento.
    lines = report.splitlines()
    first_heading = next((i for i, line in enumerate(lines) if line.startswith("# ")), 0)
    report = "\n".join(lines[first_heading:]).strip() + "\n"
    show_answer(report, title="report.md proposto")

    if Conferma.ask("Salvare il report dell'agente come [bold]report.md[/bold]?", default=True):
        (WORKSPACE / "report.md").write_text(report, encoding="utf-8")
        console.print("[bold green]Salvato demo/workspace/report.md[/bold green]")
    else:
        console.print("[yellow]Rifiutato: nessun file scritto.[/yellow]")


if __name__ == "__main__":
    main()
