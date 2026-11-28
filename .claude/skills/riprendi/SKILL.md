---
name: riprendi
description: Riprende il lavoro sul deck all'inizio di una sessione. Usalo quando l'utente dice «riprendiamo», «lanciamo le slide» o simili.
---

# Riprendere il lavoro

1. Leggi `docs/STATO.md` e `docs/NARRAZIONE.md`.
2. Controlla `git status --short` e `git log --oneline -5`: se il codice è più avanti di `docs/STATO.md`, dillo.
3. Se http://localhost:8000 non risponde, lancia `make serve` in background e verifica che :8000 e :8765 rispondano.
4. Rispondi in poche righe: dove eravamo, cosa è aperto, nient'altro. Non fare domande e non proporre cambiamenti: aspetta cosa chiede l'utente.

A fine sessione aggiorna `docs/STATO.md` (ultimo commit, mappa degli indici, aperti).
