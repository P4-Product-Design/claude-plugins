#!/usr/bin/env bash
# Quick smoke-check that the four widget files exist and contain no obvious React/JSX leftovers.
# Usage: ./scripts/validate-output.sh experiments/<experiment-name>

set -e

EXP_DIR="${1}"

if [ -z "$EXP_DIR" ]; then
  echo "Usage: $0 experiments/<experiment-name>"
  exit 1
fi

OUT="$EXP_DIR/output/Optimizely"

for f in index.html styles.css script.js widget.json; do
  if [ ! -f "$OUT/$f" ]; then
    echo "Missing: $OUT/$f"
    exit 1
  fi
done

if grep -RnE "className=|useState|useEffect|import |from ['\"]react['\"]|^<>$" "$OUT" >/dev/null 2>&1; then
  echo "Framework syntax detected in $OUT:"
  grep -RnE "className=|useState|useEffect|import |from ['\"]react['\"]|^<>$" "$OUT"
  exit 1
fi

# Scoping smoke-test: warn on bare element selectors at column 1 of styles.css.
if grep -nE "^[a-zA-Z][a-zA-Z0-9_-]* *\{" "$OUT/styles.css" >/dev/null 2>&1; then
  echo "Warning: possible unscoped selectors in $OUT/styles.css:"
  grep -nE "^[a-zA-Z][a-zA-Z0-9_-]* *\{" "$OUT/styles.css"
fi

# widget.json must be a self-contained importable extension: top-level description + options{html,css,apply_js,undo_js}.
# Missing either is the #1 cause of Optimizely import failures ("Description/Options is a missing or invalid value").
node -e '
  const fs = require("fs");
  const p = process.argv[1];
  let j;
  try { j = JSON.parse(fs.readFileSync(p, "utf8")); }
  catch (e) { console.error("widget.json is not valid JSON: " + e.message); process.exit(1); }
  const errs = [];
  if (typeof j.description !== "string" || !j.description.trim()) errs.push("missing/empty top-level \"description\"");
  if (!j.options || typeof j.options !== "object") errs.push("missing top-level \"options\" object");
  else for (const k of ["html", "css", "apply_js", "undo_js"]) {
    if (typeof j.options[k] !== "string" || !j.options[k].trim()) errs.push("options." + k + " missing/empty");
  }
  if (Array.isArray(j.form_schema)) {
    const noOpt = j.form_schema.filter(f => !("options" in f)).map(f => f.name);
    if (noOpt.length) errs.push("form_schema entries missing \"options\" key: " + noOpt.join(", "));
  }
  if (errs.length) { console.error("widget.json import-readiness FAILED:\n  - " + errs.join("\n  - ")); process.exit(1); }
' "$OUT/widget.json"

echo "✅ Output structure looks valid."
