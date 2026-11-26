/* Finestra demo live: un <div class="live" data-demo="N"> con <code class="live-cmd-src"> e
   <span class="live-prompt-src"> nelle slide
   diventa un riquadro con prompt modificabile, pulsante Esegui e output di `claude -p`
   in tempo reale, servito da demo/live_server.py (make serve). */
window.LiveDemo = {
  id: 'live-demo',
  init(deck) {
    const SERVER = 'http://127.0.0.1:8765';
    const md = deck.getPlugin && deck.getPlugin('markdown');
    const toHtml = (text) => {
      const safe = text.replace(/&/g, '&amp;').replace(/</g, '&lt;');  // niente HTML dal modello
      try {
        return md.marked.parse(safe);  // istanza Marked del plugin markdown di reveal.js
      } catch {
        return safe.replace(/\n/g, '<br>');
      }
    };
    const el = (tag, cls, text) => {
      const node = document.createElement(tag);
      if (cls) node.className = cls;
      if (text !== undefined) node.textContent = text;
      return node;
    };

    document.querySelectorAll('.reveal .live').forEach((box) => {
      const demo = box.dataset.demo;
      const cmd = box.querySelector('.live-cmd-src').textContent.trim();
      const prompt = box.querySelector('.live-prompt-src').textContent.trim();
      box.textContent = '';

      const head = el('div', 'live-head');
      head.append(el('span', 'live-dots', '● ● ●'), el('code', 'live-cmd', '$ ' + cmd));
      const input = el('textarea', 'live-prompt');
      input.value = prompt;
      input.rows = 2;
      const fit = () => {  // la casella cresce col testo (fino a un massimo), così il prompt si legge tutto
        if (input.offsetParent === null) return;  // slide non visibile: niente misure
        input.style.height = 'auto';
        const twoRows = input.offsetHeight;  // altezza di partenza: rows = 2
        const height = Math.max(twoRows, Math.min(input.scrollHeight + 2, 190));
        input.style.height = height + 'px';
        // se il prompt è lungo, l'area di output si accorcia: la finestra resta della stessa altezza
        const base = parseInt(box.dataset.out, 10) || 260;  // data-out: altezza dell'output nelle slide con altro sopra
        out.style.height = Math.max(120, base - (height - twoRows)) + 'px';
      };
      input.addEventListener('input', fit);
      const run = el('button', 'live-run', '▶ Esegui');
      const reset = el('button', 'live-reset', 'Nuova');
      reset.hidden = true;
      const save = el('button', 'live-save', 'Salva report');
      save.hidden = true;
      const status = el('span', 'live-status');
      const actions = el('div', 'live-actions');
      actions.append(run, reset, save, status);
      const out = el('div', 'live-out');
      box.append(head, input, actions, out);
      fit();
      deck.on('slidechanged', fit);
      deck.on('ready', fit);

      let source = null;
      let inConversation = false;  // dopo la prima risposta le domande riprendono la stessa sessione
      const line = (cls, text) => {
        const node = el('div', cls, text);
        out.append(node);
        out.scrollTop = out.scrollHeight;
        return node;
      };
      const stop = () => {
        if (source) source.close();
        source = null;
        run.disabled = false;
      };

      reset.addEventListener('click', () => {
        stop();
        inConversation = false;
        out.textContent = '';
        input.value = prompt;
        fit();
        run.textContent = '▶ Esegui';
        reset.hidden = save.hidden = true;
        status.textContent = '';
      });

      run.addEventListener('click', () => {
        const question = input.value.trim();
        if (inConversation && !question) {
          status.textContent = 'Scrivi la domanda successiva nella casella, poi premi Continua.';
          input.focus();
          return;
        }
        stop();
        if (!inConversation) out.textContent = '';
        line('live-user', '› ' + (question || prompt));
        input.value = '';
        save.hidden = true;
        run.disabled = true;
        status.textContent = 'Claude sta lavorando…';
        let pending = [];  // il commento si mostra solo se segue uno strumento; l'ultimo testo è la risposta
        const url = `${SERVER}/run?demo=${demo}&continue=${inConversation ? 1 : 0}`
          + `&prompt=${encodeURIComponent(question)}`;
        source = new EventSource(url);
        source.onmessage = (msg) => {
          const step = JSON.parse(msg.data);
          if (step.kind === 'text') {
            pending.push(step.text);
          } else if (step.kind === 'tool') {
            pending.forEach((t) => line('live-think', t));
            pending = [];
            line('live-tool', `→ ${step.name} ${JSON.stringify(step.input)}`);
          } else if (step.kind === 'tool_result') {
            line(step.error ? 'live-error' : 'live-result',
                 `← ${step.text.slice(0, 160).replace(/\n/g, ' ')}…`);
          } else if (step.kind === 'done') {
            const answer = el('div', 'live-answer');
            answer.innerHTML = toHtml(step.result);
            out.append(answer);
            out.scrollTop = out.scrollHeight;
            status.textContent = `turni: ${step.turns} · ${step.seconds}s · stop: ${step.stop}`;
            save.hidden = !step.can_save;
            inConversation = true;
            run.textContent = '▶ Continua';
            reset.hidden = false;
            input.placeholder = 'Domanda successiva: Claude ricorda la conversazione…';
          } else if (step.kind === 'error') {
            line('live-error', step.text);
            status.textContent = '';
          } else if (step.kind === 'end') {
            stop();
          }
        };
        source.onerror = () => {
          if (!source) return;
          line('live-error', 'Server demo non raggiungibile: avvia `make serve`.');
          status.textContent = '';
          stop();
        };
      });

      save.addEventListener('click', async () => {
        save.disabled = true;
        try {
          const res = await fetch(`${SERVER}/save-report`, { method: 'POST' });
          const body = await res.json();
          status.textContent = res.ok ? `Salvato ${body.saved}` : body.error;
          save.hidden = res.ok;
        } catch {
          status.textContent = 'Server demo non raggiungibile.';
        } finally {
          save.disabled = false;
        }
      });
    });
  },
};
