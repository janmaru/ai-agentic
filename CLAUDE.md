# Agentic AI – presentazione

Slide reveal.js in italiano generate da `slides/slides.md` con mkslides; demo live in `demo/`.
Regole di dettaglio in `.claude/rules/` (slide e demo).

- `make build` e `make test` devono passare prima di ogni commit.
- `.env` non va mai committato.
- Dopo ogni modifica alle slide, delega a `slide-reviewer` (`.claude/agents/`) prima del commit: un hook blocca `git commit` finché la revisione non è passata.

## Contesto

- Prima di lavorare leggi `docs/STATO.md` (a che punto siamo) e `docs/NARRAZIONE.md` (pubblico, idea centrale genio/jailing/harness, come si lavora). La skill `riprendi` lo fa e rilancia `make serve`.
- A fine sessione aggiorna `docs/STATO.md`.
- Fai solo ciò che è scritto: niente modifiche, opzioni o offerte in più; se è ambiguo, una sola domanda corta.
