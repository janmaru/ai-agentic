"""Demo 2 - tool use, step by step.

Written as an explicit loop so the audience can see every hop:
user -> Claude asks for a tool -> our code runs it -> result goes back -> answer.
"""

import json

from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

from common import REQUEST_DEFAULTS, check_refusal, console, get_client

# A fake backend the model cannot see directly - it has to ask for it.
ORDERS = {
    "A-1001": {"stato": "spedito", "corriere": "DHL", "consegna_prevista": "2026-11-28"},
    "A-1002": {"stato": "in preparazione", "corriere": None, "consegna_prevista": "2026-12-02"},
}

TOOLS = [
    {
        "name": "get_order_status",
        "description": "Cerca lo stato di spedizione di un ordine cliente tramite il suo ID (formato A-NNNN).",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string", "description": "ID dell'ordine, es. A-1001"}},
            "required": ["order_id"],
            "additionalProperties": False,
        },
    }
]


def get_order_status(order_id: str) -> str:
    order = ORDERS.get(order_id)
    if order is None:
        return json.dumps({"errore": f"Ordine {order_id} non trovato"})
    return json.dumps(order)


PROMPT = "Buongiorno, dove sono i miei ordini A-1001 e A-1002? Quando arriveranno?"

def main() -> None:
    client = get_client()
    messages = [{"role": "user", "content": PROMPT}]
    console.print(Panel(PROMPT, title="Utente", border_style="cyan"))

    step = 1
    while True:
        with console.status(f"Passo {step}: chiamo Claude..."):
            response = client.beta.messages.create(
                **REQUEST_DEFAULTS,
                output_config={"effort": "low"},
                tools=TOOLS,
                messages=messages,
            )
        if check_refusal(response):
            break

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            text = "".join(b.text for b in response.content if b.type == "text")
            console.print(Panel(Markdown(text), title="Claude - risposta finale", border_style="green"))
            break

        # Claude asked for one or more tools: run them all, send all results back together.
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for call in tool_calls:
            console.print(
                Panel(
                    Syntax(json.dumps(call.input, indent=2), "json"),
                    title=f"Claude chiede lo strumento: {call.name}",
                    border_style="yellow",
                )
            )
            output = get_order_status(**call.input)
            console.print(Panel(Syntax(output, "json"), title="Il nostro codice restituisce", border_style="magenta"))
            results.append({"type": "tool_result", "tool_use_id": call.id, "content": output})
        messages.append({"role": "user", "content": results})
        step += 1


if __name__ == "__main__":
    main()
