---
name: slide-check
description: Checklist per rivedere una slide del deck secondo le regole del progetto. Usala quando revisioni o scrivi slide.
---

# Checklist di una slide

Per ogni slide da rivedere, verifica i punti e annota quelli che non passano.

1. **Un messaggio.** La slide dice una cosa sola; il titolo la riassume.
2. **Breve.** Al massimo ~40 parole di testo (codice e diagrammi esclusi), al massimo 3 punti elenco. Se è di più, proponi di dividerla o di renderla visuale.
3. **Visuale.** Se il concetto è un confronto, un flusso o una struttura, c'è un disegno o un diagramma, non una lista.
4. **Esempio.** C'è un esempio concreto di sviluppo: codice, prompt, comando `claude`, output.
5. **Palette.** Solo variabili di `slides/theme.css` (`--bg`, `--text`, `--accent`, `--accent-soft`, `--accent-2`, `--accent-2-soft`, `--muted`, `--surface`, `--node`). Nessun colore scritto a mano in `slides.md` o in nuove regole CSS. Diagrammi Mermaid: palette in `mkslides.yml`.
6. **Testo dell'autore.** Le slide qui sotto vengono dal deck di formazione dell'autore: il loro testo resta alla lettera. Si possono aggiungere esempi sotto, mai cambiare o glossare le sue frasi.
   Che cos'è un LLM · Token: i pezzi del testo · Prevedere il token successivo · Generare = ripetere · Temperatura · Allucinazioni · Perché succede · Finestra di contesto · Niente memoria tra conversazioni · Il contesto costa · Esempio · L'LLM non esegue niente · Razionalità limitata · Come si progetta un sistema AI? · Bug Fix · Dove guarda il modello · Ancoraggio + compiacenza · L'ancora pericolosa… · Lisca di pesce (Ishikawa) · Passo 1 – Estrazione · Passo 2 – Diagnosi · Euristica della familiarità · Satisficing · Anche l'AI usa euristiche · Claude Code · Il contesto del progetto: CLAUDE.md · La cartella .claude · Permessi · I limiti · Cosa non delegare · La responsabilità resta nostra · citazione di Box
7. **Niente chatbot.** Nessuna contrapposizione chatbot/agente.
8. **Claude Code.** File, chiavi e opzioni di `.claude` devono esistere nella documentazione ufficiale (https://code.claude.com/docs). Se hai dubbi, segnalalo.
9. **Italiano.** Testo in italiano; termini tecnici in inglese solo se d'uso.
10. **Esempi dichiarati.** Numeri o tokenizzazioni non misurati sono segnati come indicativi.
