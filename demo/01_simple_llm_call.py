"""Demo 1 - a plain LLM call: one prompt in, one answer out. No tools, no loop."""

from rich.markdown import Markdown
from rich.panel import Panel

from common import REQUEST_DEFAULTS, check_refusal, console, get_client

PROMPT = "In three short bullet points: what is the difference between a chatbot and an AI agent?"

def main() -> None:
    client = get_client()

    console.print(Panel(PROMPT, title="User", border_style="cyan"))

    with console.status("Thinking..."):
        response = client.beta.messages.create(
            **REQUEST_DEFAULTS,
            output_config={"effort": "low"},
            messages=[{"role": "user", "content": PROMPT}],
        )

    if not check_refusal(response):
        text = "".join(b.text for b in response.content if b.type == "text")
        console.print(Panel(Markdown(text), title=f"Claude ({response.model})", border_style="green"))

    console.print(
        f"[dim]tokens in: {response.usage.input_tokens}  out: {response.usage.output_tokens}  "
        f"stop_reason: {response.stop_reason}[/dim]"
    )


if __name__ == "__main__":
    main()
