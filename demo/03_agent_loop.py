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


class Conferma(Confirm):
    """Domanda sì/no che accetta s/n."""

    choices = ["s", "n"]
    validate_error_message = "[prompt.invalid]Rispondi s oppure n"


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
    """Elenca i file disponibili nella cartella di lavoro."""
    log_tool("list_files", {})
    return "\n".join(sorted(p.name for p in WORKSPACE.iterdir() if p.is_file()))


@beta_tool
def read_file(name: str) -> str:
    """Legge un file di testo dalla cartella di lavoro.

    Args:
        name: nome del file relativo alla cartella di lavoro, es. sales.csv.
    """
    log_tool("read_file", {"name": name})
    return safe_path(name).read_text(encoding="utf-8")


@beta_tool
def aggregate_csv(name: str, group_by: str, value_column: str) -> str:
    """Somma una colonna numerica di un CSV, raggruppando per un'altra colonna. Usalo per totali esatti.

    Args:
        name: nome del file CSV nella cartella di lavoro.
        group_by: colonna per cui raggruppare, es. regione.
        value_column: colonna numerica da sommare, es. ricavi_eur.
    """
    log_tool("aggregate_csv", {"name": name, "group_by": group_by, "value_column": value_column})
    totals: dict[str, float] = defaultdict(float)
    with safe_path(name).open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row[group_by]] += float(row[value_column])
    return json.dumps(dict(sorted(totals.items(), key=lambda kv: -kv[1])))


@beta_tool
def write_file(name: str, content: str) -> str:
    """Scrive un file di testo nella cartella di lavoro. Ogni scrittura va approvata da una persona.

    Args:
        name: nome del file relativo alla cartella di lavoro, es. report.md.
        content: contenuto completo del file.
    """
    log_tool("write_file", {"name": name, "chars": len(content)})
    console.print(Panel(Markdown(content), title=f"{name} proposto", border_style="magenta"))
    if not Conferma.ask(f"Permettere all'agente di scrivere [bold]{name}[/bold]?", default=True):
        return "L'utente ha rifiutato questa scrittura. Chiedi cosa cambiare."
    safe_path(name).write_text(content, encoding="utf-8")
    return f"Scritti {len(content)} caratteri in {name}."


SYSTEM = (
    "Sei un agente analista che lavora in una cartella isolata. "
    "Usa gli strumenti per esaminare i file, calcola i numeri esatti con aggregate_csv invece di "
    "fare i conti da solo, e salva i documenti con write_file. Scrivi in italiano. "
    "Prima di ogni chiamata a uno strumento, di' in una breve frase cosa stai per fare."
)

GOAL = "Cerca nella cartella di lavoro una richiesta del direttore commerciale e portala a termine."

def main() -> None:
    client = get_client()
    console.print(Panel(GOAL, title="Obiettivo", border_style="cyan"))

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
        console.rule(f"[dim]turno {turn} · stop_reason={message.stop_reason}[/dim]")
        if check_refusal(message):
            break
        for block in message.content:
            if block.type == "text" and block.text.strip():
                style = "green" if message.stop_reason == "end_turn" else "white"
                console.print(Markdown(block.text), style=style)

    console.print(f"\n[bold green]Fatto in {turn} turni del modello.[/bold green]")


if __name__ == "__main__":
    main()
