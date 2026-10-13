#!/usr/bin/env bash
# Claude Code PreToolUse hook (wired up in .claude/settings.json).
# Runs scripts/check.sh before any Bash command that pushes with git, and blocks the push if it fails.
input="$(cat)"
cmd="$(printf '%s' "$input" | python3 -I -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)"
case "$cmd" in
  *"git push"*|*"git -C "*" push"*) ;;
  *) exit 0 ;;
esac
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
if out="$("$root/scripts/check.sh" 2>&1)"; then
  exit 0
fi
{
  echo "Push blocked: scripts/check.sh failed. Fix these, commit, and push again."
  printf '%s\n' "$out"
} >&2
exit 2
