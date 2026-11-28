# Narrazione e criteri del deck

Contesto che non si ricava dal codice. Lo stato corrente (a che punto siamo, cosa è aperto) è in `docs/STATO.md`.

## Pubblico e obiettivo

Il pubblico è fatto di **sviluppatori**: vogliono leggere codice vero e capire. Obiettivo (dalla copertina): capire cos'è un agente, come funziona dentro, quali trappole ha, vederne uno dal vivo.

Cinque sezioni: 1 Che cos'è un agente, 2 Come funziona, 3 Le trappole, 4 Un agente dal vivo (Claude Code + demo), 5 Rischi e responsabilità. Si parte dall'agente (Claude, GPT), non dall'LLM.

## Idea centrale: il genio e la gabbia

La parte deterministica sostiene il mondo stocastico dell'agente. Non lo imprigiona.

- **Genio** = il modello (nuvola stocastica). **Gabbia** o **lampada** = i mezzi deterministici.
- **Jailing** (blu): la parte deterministica, cioè CLI, script, librerie, permessi, hook.
- **Harness** (arancione): ciò che governa il modello, cioè `CLAUDE.md`, regole, skill, testo letto da Claude. È in `.claude/` e include anche testo non deterministico.
- Il jailing da solo non basta: bisogna lavorare anche sul genio per contenerlo.
- Una **skill** impiega entrambi (testo per Claude più script): si mostra con entrambi i colori, mai con uno solo.
- «Gabbia» in senso lato è più ampio di «harness». Nelle slide il termine inglese è **jailing**.
- Un'immagine, non un diagramma, quando il concetto è una metafora (il genio è un'immagine generata, `slides/img/`).

Esempio reale di riferimento: la skill `azdo` con lo script `azdo.py`. I dati del cliente non vanno mai nelle slide.

## Come si lavora sulle slide

- **Fai solo quello che è scritto.** Niente modifiche, offerte o opzioni in più. Se una frase è ambigua, una sola domanda corta.
- **Leggi per intero i file forniti** prima di costruire sopra; non inventare flussi o esempi.
- **Il testo dell'autore resta alla lettera** (slide derivate dal deck di formazione https://github.com/mauroghiani-blx/Formazione-Sistemya). Le slide nuove sono dell'assistente.
- **Esempi anonimi:** niente nomi di cliente, organizzazione, progetto, ID reali (repo pubblico).
- **Coerenza grafica:** prima di inventare una soluzione grafica, riguarda le slide già fatte e riusa; se la cambi, cambiala ovunque. Regole di stile e colore in `.claude/rules/slides.md`.
- **Termini in inglese dove sono d'uso** (black box, jailing, harness, prompt, token).
- **Comandi `claude` e prompt in slide** sono finestre live (`data-demo`); i comandi di Claude Code si verificano sulla documentazione ufficiale prima di metterli.
- **Dopo ogni modifica** si guarda lo screenshot (`scripts/snap.sh N`). Prima di ogni commit: `slide-reviewer`, `make test`, `make build`.
- **Immagini:** i prompt per Gemini devono stare in piedi da soli, senza allegati.
