---
paths:
  - "slides/**"
---

# Regole per le slide

- **Chiare, brevi e concise.** Un solo messaggio per slide, poche righe, niente muri di testo.
- **Argomento complesso → più slide**, ma senza esagerare: di norma 2, al massimo 3 sullo stesso concetto.
- **Esempi concreti, sempre.** Ogni concetto va accompagnato da un esempio di sviluppo software: codice, prompt, comandi `claude`, output reali.
- **Struttura `.claude` e Claude Code:** gli esempi seguono la documentazione ufficiale (https://code.claude.com/docs). Si mostrano `CLAUDE.md`, `.claude/settings.json`, `.claude/rules/`, `.claude/commands/`, `.claude/agents/`, `.claude/skills/`, hook e permessi così come sono documentati. Niente nomi di file, chiavi o opzioni inventati: se non è nella documentazione, non va in slide.
- **Comandi `claude` e prompt: finestra live, non testo statico.** Dove una slide mostra un comando `claude` o un prompt, il concetto si rende interattivo con `claude -p` in una finestra live, come nelle slide delle demo: `<div class="live" data-demo="N">` con `live-cmd-src` (il comando) e `live-prompt-src` (il prompt modificabile). Chi guarda cambia il prompt e vede la risposta. Ogni finestra corrisponde a una demo predefinita in `demo/live_server.py` (cartella, strumenti e permessi fissi: dalla slide si cambia solo il prompt); una slide nuova richiede quindi anche la sua voce nel server, con il suo test, mai comandi arbitrari. Un prompt senza strumenti riusa la configurazione della demo 1.
- **Il testo dell'autore resta com'è.** Le slide derivate dal deck di formazione riportano le parole originali alla lettera. Non si aggiungono glosse, frasi a effetto o spiegazioni non richieste.
- **Niente cornice "chatbot".** Si parla di LLM e di agenti, senza contrapposizioni con i chatbot.
- **Lingua:** italiano. Termini tecnici in inglese dove sono d'uso (token, tool, prompt).
- **Verifica visiva** su `make serve` (http://localhost:8000/#/N): diagrammi Mermaid e codice non devono uscire dalla slide 1280×720.
- **Palette:** solo i colori definiti in `slides/theme.css` (`--bg`, `--text`, `--accent`, `--accent-soft`, `--accent-2`, `--accent-2-soft`, `--muted`, `--surface`, `--node`; sfondo bianco, testo e grigi nella famiglia del blu, accento arancio), mai colori scritti a mano. Accent pieno = scelta giusta o focus; muted tratteggiato = scartato o fuori; accent-2 (azzurro) = elementi tecnici. Per i diagrammi Mermaid la palette è in `mkslides.yml`.
- **Colori derivati dallo sfondo:** su uno sfondo colorato, tutti i colori di supporto (testo secondario, superfici, riquadri, linee, bordi) derivano dalla tinta dello sfondo: variazioni più chiare o più scure della stessa tinta, oppure bianco semitrasparente. Mai grigi neutri su uno sfondo colorato. I grigi neutri si usano solo con uno sfondo neutro. Un solo accento, che stacchi dalla tinta dello sfondo. Non cambiare solo lo sfondo di una palette esistente: si ricostruisce tutta.
- **Visuale prima del testo:** quando un concetto si può mostrare (confronto, flusso, struttura), meglio un disegno o un diagramma di una lista di punti.
