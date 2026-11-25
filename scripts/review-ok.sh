#!/usr/bin/env bash
# Registra che la versione attuale del deck ha superato la revisione (usato da slide-reviewer).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .claude/review
scripts/review-hash.sh > .claude/review/ok
echo "Revisione registrata: $(cat .claude/review/ok)"
