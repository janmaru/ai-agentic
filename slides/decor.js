/* Decorazioni delle slide: sulla copertina due nautili grandi; su ogni slide successiva due disegni in fil di ferro
   (uno in alto a destra, uno in basso a sinistra, lontano dalle frecce), presi da img/sprite/
   e ricolorati con una tinta blu della palette. Stessa dimensione per tutti; abbinamenti
   mescolati ma fissi tra un caricamento e l'altro. */
window.Decor = {
  id: 'decor',
  init(deck) {
    // Ritagli: immagine, dimensioni dell'immagine, zona [x, y, larghezza, altezza] del disegno
    // e, per i pezzi tagliati dal bordo dell'immagine, l'angolo da cui vengono ('tl' / 'br').
    const S = (file, w, h, box, cut = null) => ({ src: `img/sprite/${file}`, w, h, box, cut });
    const SPRITES = [
      S('creature.jpg', 1408, 768, [90, 85, 370, 250]),      // balena
      S('creature.jpg', 1408, 768, [520, 80, 380, 260]),     // calamaro
      S('creature.jpg', 1408, 768, [975, 95, 345, 220]),     // tartaruga
      S('creature.jpg', 1408, 768, [175, 415, 140, 290]),    // cavalluccio
      S('creature.jpg', 1408, 768, [535, 460, 345, 195]),    // tonni
      S('creature.jpg', 1408, 768, [1055, 425, 200, 270]),   // medusa
      S('narvalo.jpg', 1408, 768, [250, 210, 945, 345]),     // narvalo
      S('conchiglie.jpg', 1376, 768, [0, 0, 450, 390], 'tl'),
      S('conchiglie.jpg', 1376, 768, [900, 370, 476, 398], 'br'),
      S('nautili-wireframe.jpg', 1376, 768, [0, 0, 450, 390], 'tl'),
      S('nautili-wireframe.jpg', 1376, 768, [900, 370, 476, 398], 'br'),
    ];
    const NAUTILUS_TL = 9, NAUTILUS_BR = 10;
    // Un pezzo tagliato in alto va solo in alto, uno tagliato in basso solo in basso.
    const POOL = {
      'top-right': SPRITES.map((sp, i) => i).filter((i) => SPRITES[i].cut !== 'br'),
      'bottom-left': SPRITES.map((sp, i) => i).filter((i) => SPRITES[i].cut !== 'tl'),
    };
    // Stessa area per tutti i disegni (in vw²), così nessuno risulta più piccolo degli altri.
    const AREA = 160, MAX_SIDE = 15;

    // Tinte lette dalla palette in theme.css (testo, accento tecnico, grigio-blu).
    const css = getComputedStyle(document.documentElement);
    const TINTS = ['--text', '--accent-2', '--muted'].map((v) => css.getPropertyValue(v).trim());

    const NS = 'http://www.w3.org/2000/svg';
    const svgEl = (tag, attrs) => {
      const node = document.createElementNS(NS, tag);
      Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
      return node;
    };

    // Filtri: il fondo quasi bianco delle immagini diventa bianco puro (LIFT)
    // e le linee scure prendono la tinta.
    const LIFT = 1.06;
    const defs = svgEl('svg', { width: 0, height: 0, style: 'position:absolute' });
    TINTS.forEach((hex, i) => {
      const [r, g, b] = [1, 3, 5].map((o) => parseInt(hex.slice(o, o + 2), 16) / 255);
      const row = (c) => [0.2126, 0.7152, 0.0722].map((k) => (1 - c) * k * LIFT).join(' ') + ` 0 ${c}`;
      const filter = svgEl('filter', { id: `decor-tint-${i}`, 'color-interpolation-filters': 'sRGB' });
      filter.append(svgEl('feColorMatrix', { type: 'matrix', values: `${row(r)} ${row(g)} ${row(b)} 0 0 0 1 0` }));
      defs.append(filter);
    });
    document.body.append(defs);

    // Generatore pseudo-casuale con seme fisso: stesso mescolamento a ogni caricamento.
    let seed = 7;
    const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const shuffled = (n) => {
      const a = [...Array(n).keys()];
      for (let i = n - 1; i > 0; i--) {
        const j = Math.floor(rand() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    };

    const corner = (sprite, tint, place, scale = 1) => {
      const [x, y, w, h] = sprite.box;
      let width = Math.sqrt(AREA * w / h), height = Math.sqrt(AREA * h / w);
      const fit = Math.min(1, MAX_SIDE / Math.max(width, height));
      width *= fit * scale;
      height *= fit * scale;
      // Il bordo tagliato del pezzo deve combaciare con il bordo della slide: un pezzo
      // dall'angolo sinistro dell'immagine va riflesso quando sta a destra, e viceversa.
      const mirror = (place === 'top-right' && sprite.cut === 'tl') || (place === 'bottom-left' && sprite.cut === 'br');
      const svg = svgEl('svg', { class: `decor decor-${place}`, viewBox: `${x} ${y} ${w} ${h}`,
                                 preserveAspectRatio: 'none', 'aria-hidden': 'true',
                                 style: `width:${width.toFixed(2)}vw;height:${height.toFixed(2)}vw;`
                                   + (mirror ? 'transform:scaleX(-1);' : '')
                                   // pezzi tagliati: attaccati al bordo, senza margine
                                   + (sprite.cut ? (place === 'top-right' ? 'top:0;right:0;' : 'bottom:0;left:0;') : '') });
      const image = svgEl('image', { href: sprite.src, width: sprite.w, height: sprite.h });
      image.setAttribute('filter', `url(#decor-tint-${tint})`);
      svg.append(image);
      return svg;
    };

    deck.on('ready', () => {
      const backgrounds = document.querySelectorAll('.reveal .backgrounds > .slide-background');
      const queues = { 'top-right': [], 'bottom-left': [] };
      const next = (place, avoid) => {
        const q = queues[place];
        if (q.length < 2) shuffled(POOL[place].length).forEach((k) => q.push(POOL[place][k]));
        const k = q[0] === avoid ? 1 : 0;
        return q.splice(k, 1)[0];
      };
      backgrounds.forEach((bg, i) => {
        const content = bg.querySelector('.slide-background-content') || bg;
        if (i === 0) {
          // Copertina: i due nautili in fil di ferro, più grandi, nella tinta del testo.
          content.append(corner(SPRITES[NAUTILUS_TL], 0, 'top-right', 1.7),
                         corner(SPRITES[NAUTILUS_BR], 0, 'bottom-left', 1.7));
          return;
        }
        const top = next('top-right', -1);
        const bottom = next('bottom-left', top);
        content.append(corner(SPRITES[top], Math.floor(rand() * TINTS.length), 'top-right'),
                       corner(SPRITES[bottom], Math.floor(rand() * TINTS.length), 'bottom-left'));
      });
    });
  },
};
