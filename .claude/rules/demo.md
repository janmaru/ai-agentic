---
paths:
  - "demo/**"
---

# Regole per le demo

- Le demo live usano `claude -p` (`make demo1|demo2|demo3`); le versioni con SDK sono `make api-demo*`.
- Prompt e output delle demo in italiano.
- `make clean` prima della presentazione.
- Le slide delle demo hanno una finestra live (`slides/live.js` + `demo/live_server.py`): il server esegue solo le demo predefinite, con cartella, strumenti e permessi fissi; dalla slide si cambia solo il prompt.
