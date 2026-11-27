/* Colori del codice come negli IDE: highlight.js mette in `hljs-built_in` sia i tipi (str, string)
   sia le funzioni predefinite (print). Qui si separano: un built_in seguito da "(" è una chiamata
   di funzione e prende la classe `hljs-builtin-fn` (ocra, come negli IDE); uno preceduto da "." è un attributo
   (b.type, c.id) e prende `hljs-builtin-attr` (colore normale); gli altri restano tipi (teal). */
window.CodeColors = {
  id: 'code-colors',
  init(deck) {
    const fix = () => {
      document.querySelectorAll('pre code.hljs .hljs-built_in').forEach((el) => {
        const next = el.nextSibling;
        const isCall = next && next.nodeType === 3 && next.textContent.startsWith('(');
        const prev = el.previousSibling;
        const isAttr = prev && prev.nodeType === 3 && prev.textContent.endsWith('.');
        el.classList.toggle('hljs-builtin-fn', !!isCall);
        el.classList.toggle('hljs-builtin-attr', !!isAttr);
      });
    };
    // La colorazione la fa il plugin highlight: si rilancia finché non ha finito.
    deck.on('ready', () => { fix(); setTimeout(fix, 300); setTimeout(fix, 1500); });
    deck.on('slidechanged', fix);
  },
};
