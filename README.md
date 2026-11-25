# Agentic AI — presentation + live demo

Slides are written in Markdown and rendered with reveal.js ([MkSlides](https://github.com/MartenBE/mkslides)).
The live demos use Claude through the official `anthropic` Python SDK.

## Setup

```bash
make setup                 # creates .venv, installs requirements, copies .env.example -> .env
# then put your key in .env:  ANTHROPIC_API_KEY=sk-ant-...
```

## Slides

```bash
make serve                 # live-reload at http://localhost:8000
make build                 # static HTML in ./site (open site/index.html)
```

- Content: `slides/slides.md` — `---` separates slides, `Note:` starts speaker notes (press `S`).
- Diagrams: fenced ```` ```mermaid ```` blocks (rendered by reveal.js-mermaid-plugin, loaded from CDN — needs internet).
- Styling: `slides/theme.css` on top of the reveal.js `black` theme; settings in `mkslides.yml`.
- Export to PDF: open the deck with `?print-pdf` appended to the URL and print from Chrome.

## Live demos

| Command | What it shows |
|---|---|
| `make demo1` | A single LLM call: no tools, no loop |
| `make demo2` | Tool use step by step, with an explicit loop (order-status lookup) |
| `make demo3` | An autonomous agent: reads a brief, aggregates `sales.csv`, writes `report.md` after human approval |

Demo 3 works only inside `demo/workspace/`; paths outside it are refused.
Model defaults to `claude-opus-5-5`; override it with `DEMO_MODEL=...` in `.env`.
`make clean` removes the generated report so the demo can be run again.
