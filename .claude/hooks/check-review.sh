#!/usr/bin/env bash
# Hook PreToolUse su `git commit`: se il deck è cambiato rispetto a HEAD
# e non ha superato slide-reviewer, blocca il commit (exit 2, motivo su stderr).
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
git diff HEAD --name-only -- slides mkslides.yml | grep -q . || exit 0
if [ "$(cat .claude/review/ok 2>/dev/null)" = "$(scripts/review-hash.sh)" ]; then
  exit 0
fi
echo "Slide modificate senza revisione: delega a slide-reviewer prima di committare." >&2
exit 2
