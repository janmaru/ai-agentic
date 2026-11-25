#!/usr/bin/env bash
# Screenshot della slide N dal server di `make serve`. Uso: scripts/snap.sh N
# Stampa il percorso del PNG (in .claude/review/shots/, fuori da git).
set -euo pipefail
n="${1:?uso: scripts/snap.sh N}"
root="$(cd "$(dirname "$0")/.." && pwd)"
out_dir="$root/.claude/review/shots"
mkdir -p "$out_dir"
curl -sf http://localhost:8000/ >/dev/null || { echo "Server non attivo: lancia make serve" >&2; exit 1; }
# Opera installato come snap può scrivere solo nella home: si passa da lì.
tmp="$HOME/slide-shots"
mkdir -p "$tmp"
# Opera lanciato due volte di fila a volte produce un'immagine bianca (pochi KB): si riprova.
for _ in 1 2 3; do
  rm -f "$tmp/review-$n.png"
  timeout 60 "${OPERA:-/snap/bin/opera}" --headless=new --window-size=1280,720 --virtual-time-budget=10000 \
    --screenshot="$tmp/review-$n.png" "http://localhost:8000/?v=$(date +%s)#/$n" >/dev/null 2>&1 || true
  [ "$(stat -c %s "$tmp/review-$n.png" 2>/dev/null || echo 0)" -gt 10000 ] && break
  sleep 2
done
[ -s "$tmp/review-$n.png" ] || { echo "Screenshot non riuscito per la slide $n" >&2; exit 1; }
mv "$tmp/review-$n.png" "$out_dir/slide-$n.png"
echo "$out_dir/slide-$n.png"
