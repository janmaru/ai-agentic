# Stato del deck

Da aggiornare a fine di ogni sessione di lavoro. Narrazione e criteri: `docs/NARRAZIONE.md`.

**Ultimo aggiornamento:** 2026-11-28, dopo il commit `bc7daaa`, con le slide 6-8 in lavorazione (121 slide).

## Mappa delle slide (indici URL, `#/N`, la copertina è 0)

| # | Slide |
|---|-------|
| 1 | Di che cosa parleremo (navigator) |
| 2 | Copertina «1. Che cos'è un agente?» |
| 3 | L'agente come black box (prompt → Agente (Claude Code) → `<code>`) |
| 4 | Deterministico e stocastico (interno nascosto, due caselle colorate) |
| 5 | Sistemi deterministici |
| 6 | Sistemi stocastici (ML, deep learning, LLM: testi e testo atteso → rete neurale → modello) |
| 7 | Imparare è un ciclo (grafo di strati, errore rispetto al token atteso, pesi corretti) |
| 8 | Il token successivo (uso del modello: probabilità e token estratto) |
| 9 | Che cos'è Claude Code? (schema completo) |
| 10 | Il genio della lampada (Jailing blu, Harness arancione) |
| 11 | Il genio della gabbia |
| 12 | Copertina Skill (titolo metà arancione, metà blu) |
| 13 | Voce di vocabolario «skill» |
| 14 | Che cos'è una skill |
| 15-22 | Il prompt e la skill, board Azure DevOps, user story, flusso azdo, … fino a «La definizione» |
| 99 | Jailing e harness |

Gli indici dopo la 14 sono cambiati di +5 rispetto a prima del 28/11. Per un indice preciso: `scripts/snap.sh N` e guardare lo screenshot (indice = separatori `---` con riga vuota sopra e sotto che precedono la slide).

## Rivisto e da rivedere

- Rivisto con l'autore: dalla copertina fino al flusso azdo (circa fino alla `#/18`).
- Da rivedere insieme: dalla `#/19` in poi.

## Aperti

- «(o al massimo 3 tentativi)» nella slide dell'errore che istruisce: `azdo.py` non ha retry.
- Nota «la decide chi pianifica» sulla Priority.
- Controlli di `pr-ready` fuori dal flusso azdo.
- Anatomia di un agente vs overview; sezione 2 lunga; sezione 4 mista; sforature in Tokenizer e MCP.
- Commenti in `slides/theme.css` con indici vecchi.
- Il genio e la lampada: le due slide ripetono la stessa riga sotto lo schema.
- «Prevedere il token successivo» nella sezione 2 e la nuova «Il token successivo» (`#/8`) dicono cose vicine: decidere se unirle.

## Come riprendere

`make serve` (slide su http://localhost:8000, demo live su :8765), poi `git log --oneline -5` e questo file. La skill `riprendi` fa i tre passi.
