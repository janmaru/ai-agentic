#!/usr/bin/env bash
# Hash dei file che definiscono il deck: cambia a ogni modifica di slide, stile o config.
set -euo pipefail
cd "$(dirname "$0")/.."
cat slides/slides.md slides/theme.css mkslides.yml | sha256sum | cut -d' ' -f1
