"""Shared setup for the live demos: client, model, request defaults, console."""

import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

console = Console()

MODEL = os.getenv("DEMO_MODEL", "claude-opus-5-5")

# Applied to every request. "default" fallbacks re-run the request on a
# server-chosen model if the main model declines for policy reasons.
REQUEST_DEFAULTS = {
    "model": MODEL,
    "max_tokens": 16000,
    "betas": ["server-side-fallback-2026-07-01"],
    "fallbacks": "default",
}


def get_client() -> anthropic.Anthropic:
    # Credentials come from ANTHROPIC_API_KEY (.env) or an `ant auth login` profile.
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
        if os.environ.get(var) == "":
            del os.environ[var]  # an empty line in .env would otherwise shadow a profile
    has_env = any(os.getenv(v) for v in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"))
    has_profile = (Path.home() / ".config" / "anthropic").is_dir()
    if not (has_env or has_profile):
        console.print("[red]No Anthropic credentials found.[/red] Set ANTHROPIC_API_KEY in .env.")
        sys.exit(1)
    return anthropic.Anthropic()


def check_refusal(message) -> bool:
    """Print a notice and return True if the model declined the request."""
    if message.stop_reason == "refusal":
        category = message.stop_details.category if message.stop_details else None
        console.print(f"[red]Request declined[/red] (category: {category})")
        return True
    return False
