---
name: slide-screenshot
description: Fa lo screenshot di una slide del deck per controllarla a occhio. Usalo per verificare leggibilità e che niente esca dalla slide 1280×720.
---

# Screenshot di una slide

1. Serve il server di `make serve` su http://localhost:8000. Se non risponde, fermati e chiedi di lanciarlo.
2. Lancia `scripts/snap.sh N`, dove N è l'indice della slide nell'URL (`#/N`, la copertina è 0).
3. Lo script stampa il percorso del PNG: aprilo con Read e guardalo.

Indice di una slide: conta i separatori `---` (riga vuota sopra e sotto) che la precedono in `slides/slides.md`.

Limite noto: Opera headless impagina la slide più piccola, in alto a sinistra dell'immagine. Valuta proporzioni, leggibilità e overflow dentro quell'area; il resto dell'immagine (solo sfondo) non è un errore.
