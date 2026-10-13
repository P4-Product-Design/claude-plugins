---
description: QA an existing experiment's widget output against the Optimizely constraints checklist and re-open the local preview.
argument-hint: <experiment-name>
---

Run a constraints-checklist QA pass on `experiments/$1/output/Optimizely/`. If `$1` is empty, list the experiment folders under `experiments/` and ask which one.

Steps:

1. **Verify the four files exist:**
   - `experiments/$1/output/Optimizely/index.html`
   - `experiments/$1/output/Optimizely/styles.css`
   - `experiments/$1/output/Optimizely/script.js`
   - `experiments/$1/output/Optimizely/widget.json`

   If any are missing, report which and stop.

2. **Run the constraints checklist** (full reference: `references/optimizely-constraints.md` and `references/widget-template-rules.md` in the figma-to-optimizely skill):
   - No React, JSX, imports, modules, hooks, or Tailwind utilities anywhere.
   - `styles.css` is fully scoped under one root wrapper — no bare element selectors at column 1.
   - `script.js` uses `optimizely.get('utils')`, `widget.selector`, `widget.$html`. Idempotent (won't double-render). Fails safely if mount target missing.
   - All three responsive breakpoints present (mobile ≤619px, tablet 620–1023px, desktop ≥1024px).
   - Every `{{extension.fieldName}}` referenced in `index.html` has a matching entry in `widget.json`'s `form_schema`. Flag missing ones.
   - Root wrapper background is `transparent` (not white or any solid color).
   - If star ratings are present, each star is an individual SVG with `--fill` (not a single combined SVG).
   - Root element id is `optimizely-extension-{{ extension.$instance }}`.

3. **Refresh `preview.html`** using current `widget.json` defaults so the preview reflects the latest output.

4. **Spin up the local preview server** at `http://localhost:8765/preview.html` (or next open port) and `open` it.

5. **Update QA files:**
   - Append findings to `experiments/$1/qa/implementation-notes.md`.
   - List unresolved issues in `experiments/$1/qa/known-issues.md`.

6. **Print a summary**: ✅ PASSED items, ❌ FAILED items, and the preview URL.
