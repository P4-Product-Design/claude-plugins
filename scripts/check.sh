#!/usr/bin/env bash
# The one check for this repo. The pre-push hook, the GitHub check, and Claude all run it.
#
#   scripts/check.sh                 # before pushing: compares against origin/main
#   BASE=<ref> scripts/check.sh      # compare against another commit
#   BASE= scripts/check.sh           # skip the version-bump check
#
# Set REQUIRE_CLAUDE=1 to fail when the claude CLI isn't installed (CI does).
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ -z "${BASE+x}" ]; then
  git fetch -q origin main 2>/dev/null || true
  if git rev-parse --verify --quiet origin/main >/dev/null; then
    BASE=origin/main
  else
    BASE=
  fi
fi

status=0
BASE="$BASE" python3 -I scripts/check.py || status=1

if command -v claude >/dev/null 2>&1; then
  for target in . plugins/*/; do
    out="$(claude plugin validate "$target" 2>&1)"
    if ! printf '%s' "$out" | grep -q 'Validation passed'; then
      echo "claude plugin validate failed for $target:"
      printf '%s\n' "$out" | grep -E '❯|✘|rror' | sed 's/^/  /'
      status=1
    fi
  done
  [ $status -eq 0 ] && echo "claude plugin validate passed for the marketplace and every plugin."
elif [ "${REQUIRE_CLAUDE:-0}" = "1" ]; then
  echo "The claude CLI isn't installed, so claude plugin validate couldn't run."
  status=1
else
  echo "note: claude CLI not found; skipped claude plugin validate."
fi

exit $status
