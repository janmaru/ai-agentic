# Agentic AI — presentation + live demo

A talk on agentic AI: what an agent is, how the agent loop works, design patterns,
risks — plus three live demos built on Claude.

- **Slides:** Markdown rendered with reveal.js via [MkSlides](https://github.com/MartenBE/mkslides), diagrams in Mermaid.
- **Demos:** Python scripts using the official [`anthropic`](https://github.com/anthropics/anthropic-sdk-python) SDK.

## Requirements

- Python 3.12+ and `make`
- An Anthropic API key (only for the live demos)
- Internet access while presenting (the Mermaid plugin loads from a CDN)
- Any Chromium-based browser (Chrome, Edge, Opera...) to present and export PDF

## Setup

```bash
git clone https://github.com/janmaru/ai-agentic.git
cd ai-agentic
make setup                 # creates .venv, installs requirements, copies .env.example -> .env
```

Then put your key in `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
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
| `make demo2` | Tool use step by step, with an explicit loop (order-status lookup) |
| `make demo3` | An autonomous agent: reads a brief, aggregates `sales.csv`, writes `report.md` after human approval |

- Demo 3 can only touch files inside `demo/workspace/`; paths outside it are refused.
- `make clean` removes the generated report so demo 3 can be run again.
- The model defaults to `claude-opus-5-5`; override it with `DEMO_MODEL=...` in `.env`.
- Run all three demos once before the talk: they call the real API (small cost) and answers vary between runs.

## Tests

```bash
make test
```

Runs offline, with no API key and no cost:

- the demo tools (exact CSV totals, sandbox path checks, approval on writes, order lookup)
- a full build of the slides

The Claude calls themselves are not tested automatically — they need a key, cost money and
their answers change between runs. Do a manual run of the demos before presenting.

## Project structure

```
├── slides/
│   ├── slides.md          deck content and speaker notes
│   └── theme.css          style overrides
├── demo/
│   ├── common.py          client, model and request defaults shared by the demos
│   ├── 01_simple_llm_call.py
│   ├── 02_tool_use.py
│   ├── 03_agent_loop.py
│   └── workspace/         files the demo-3 agent works on
├── tests/                 offline tests (pytest)
├── mkslides.yml           reveal.js + plugin settings
├── Makefile
└── requirements.txt
```
