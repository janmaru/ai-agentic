# Stato del deck

Da aggiornare a fine di ogni sessione di lavoro. Narrazione e criteri: `docs/NARRAZIONE.md`.

**Ultimo aggiornamento:** 2026-11-28, dopo il commit `074a9fa` (119 slide).

## Mappa delle slide (indici URL, `#/N`, la copertina è 0)

| # | Slide |
|---|-------|
| 1 | Di che cosa parleremo (navigator) |
| 2 | Copertina «1. Che cos'è un agente?» |
| 3 | L'agente come black box (prompt → Agente (Claude Code) → `<code>`) |
| 4 | Deterministico e stocastico (interno nascosto, due caselle colorate) |
| 5 | Sistemi deterministici |
| 6 | Sistemi stocastici |
| 7 | Che cos'è Claude Code? (schema completo) |
| 8 | Il genio della lampada (Jailing blu, Harness arancione) |
| 9 | Il genio della gabbia |
| 10 | Copertina Skill (titolo metà arancione, metà blu) |
| 11 | Voce di vocabolario «skill» |
| 12 | Che cos'è una skill |
| 13-20 | Il prompt e la skill, board Azure DevOps, user story, flusso azdo, … fino a «La definizione» |
| 97 | Jailing e harness |

Gli indici dopo la 12 sono cambiati di +3 rispetto a prima del 28/11. Per un indice preciso: `scripts/snap.sh N` e guardare lo screenshot (indice = separatori `---` con riga vuota sopra e sotto che precedono la slide).

## Rivisto e da rivedere

- Rivisto con l'autore: dalla copertina fino al flusso azdo (circa fino alla `#/16`).
- Da rivedere insieme: dalla `#/17` in poi.

## Aperti

- «(o al massimo 3 tentativi)» nella slide dell'errore che istruisce: `azdo.py` non ha retry.
- Nota «la decide chi pianifica» sulla Priority.
- Controlli di `pr-ready` fuori dal flusso azdo.
- Anatomia di un agente vs overview; sezione 2 lunga; sezione 4 mista; sforature in Tokenizer e MCP.
- Commenti in `slides/theme.css` con indici vecchi.
- Il genio e la lampada: le due slide ripetono la stessa riga sotto lo schema.

## Come riprendere

`make serve` (slide su http://localhost:8000, demo live su :8765), poi `git log --oneline -5` e questo file. La skill `riprendi` fa i tre passi.
