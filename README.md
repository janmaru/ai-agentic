# Agentic AI — presentation + live demo

A talk on agentic AI: what an agent is, how the agent loop works, design patterns,
risks — plus three live demos built on Claude.

- **Slides (in Italian):** Markdown rendered with reveal.js via [MkSlides](https://github.com/MartenBE/mkslides), diagrams in Mermaid.
- **Demos:** run Claude Code headless (`claude -p`) with your Claude Code login — no API credit needed.
  The same demos also exist on the [`anthropic`](https://github.com/anthropics/anthropic-sdk-python) Python SDK.

## Requirements

- Python 3.12+ and `make`
- [Claude Code](https://code.claude.com) installed and logged in (`claude` on the PATH) for the live demos
- Optional: an Anthropic API key with credit, only for the `api-demo*` variants
- Internet access while presenting (the Mermaid plugin loads from a CDN)
- Any Chromium-based browser (Chrome, Edge, Opera...) to present and export PDF

## Setup

```bash
git clone https://github.com/janmaru/ai-agentic.git
cd ai-agentic
make setup                 # creates .venv, installs requirements, copies .env.example -> .env
```

For the API variants only, put your key in `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_WORKSPACE_ID=      # only if the key is not scoped to a workspace
```

## Slides

```bash
make serve                 # live-reload at http://localhost:8000
make build                 # static HTML in ./site (open site/index.html)
```

| Key | Action |
|---|---|
| `→` / `←` | Next / previous slide |
| `S` | Speaker notes window |
| `F` | Fullscreen |
| `Esc` | Slide overview |

- **Content:** `slides/slides.md` — `---` separates slides, `Note:` starts speaker notes.
- **Diagrams:** fenced ```` ```mermaid ```` blocks.
- **Styling:** `slides/theme.css` on top of the reveal.js `black` theme; deck settings in `mkslides.yml`.
- **PDF export:** open the deck with `?print-pdf` at the end of the URL and print to PDF from the browser.

## Live demos

| Command | What it shows |
|---|---|
| `make demo1` | A single LLM call: no tools, no loop |
| `make demo2` | Tool use: Claude reads `orders.json` to answer a customer |
| `make demo3` | An autonomous agent: finds the brief, reads `sales.csv`, drafts `report.md`, saved only after you approve |

Each step of the agent (tool calls and results) is printed live from Claude Code's `stream-json` output.

- The agent is read-only and restricted to its folder (`--allowedTools "Read(./**)"`); writing is done by our code after approval.
- `make clean` removes the generated report so demo 3 can be run again.
- `DEMO_CLI_MODEL=...` picks a model; otherwise your Claude Code default is used.
- Run all three demos once before the talk: answers vary between runs.

**API variants** — `make api-demo1`, `api-demo2`, `api-demo3` do the same through the Anthropic API with
custom tools (needs a key and API credit). The model defaults to `claude-opus-5-5`; override with `DEMO_MODEL=...`.

## Tests

```bash
make test
```

Runs offline, with no API key and no cost:

- the demo tools (exact CSV totals, sandbox path checks, approval on writes, order lookup)
- the `claude -p` stream renderer, with a fake CLI process
- a full build of the slides

The Claude calls themselves are not tested automatically — they need a key, cost money and
their answers change between runs. Do a manual run of the demos before presenting.

## Project structure

```
├── slides/
│   ├── slides.md          deck content and speaker notes
│   └── theme.css          style overrides
├── demo/
│   ├── claude_cli.py      runs `claude -p` and renders the agent loop live
│   ├── cli_01_simple_call.py, cli_02_tool_use.py, cli_03_agent.py
│   ├── common.py          API client and request defaults (API variants)
│   ├── 01_simple_llm_call.py, 02_tool_use.py, 03_agent_loop.py
│   ├── store/             orders.json for demo 2
│   └── workspace/         files the demo-3 agent works on
├── tests/                 offline tests (pytest)
├── mkslides.yml           reveal.js + plugin settings
├── Makefile
└── requirements.txt
```
