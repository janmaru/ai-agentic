---
paths:
  - "slides/**"
---

# Regole per le slide

- **Chiare, brevi e concise.** Un solo messaggio per slide, poche righe, niente muri di testo.
- **Argomento complesso → più slide**, ma senza esagerare: di norma 2, al massimo 3 sullo stesso concetto.
- **Esempi concreti, sempre.** Ogni concetto va accompagnato da un esempio di sviluppo software: codice, prompt, comandi `claude`, output reali.
- **Struttura `.claude` e Claude Code:** gli esempi seguono la documentazione ufficiale (https://code.claude.com/docs). Si mostrano `CLAUDE.md`, `.claude/settings.json`, `.claude/rules/`, `.claude/commands/`, `.claude/agents/`, `.claude/skills/`, hook e permessi così come sono documentati. Niente nomi di file, chiavi o opzioni inventati: se non è nella documentazione, non va in slide.
- **Il testo dell'autore resta com'è.** Le slide derivate dal deck di formazione riportano le parole originali alla lettera. Non si aggiungono glosse, frasi a effetto o spiegazioni non richieste.
- **Niente cornice "chatbot".** Si parla di LLM e di agenti, senza contrapposizioni con i chatbot.
- **Lingua:** italiano. Termini tecnici in inglese dove sono d'uso (token, tool, prompt).
- **Verifica visiva** su `make serve` (http://localhost:8000/#/N): diagrammi Mermaid e codice non devono uscire dalla slide 1280×720.
