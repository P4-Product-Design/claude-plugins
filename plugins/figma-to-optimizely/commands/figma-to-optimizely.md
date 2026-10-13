---
description: Convert a Figma frame into Optimizely widget files (HTML, CSS, JS, widget.json) and open a local preview in the browser.
argument-hint: <figma-url> [experiment-name]
---

The user wants to convert a Figma design into an Optimizely Web Experiment widget. Run the full figma-to-optimizely workflow.

Inputs from arguments:
- `$1` — Figma URL (required). If empty, ask the user for it.
- `$2` — experiment name (optional). If empty, infer from the Figma frame name or ask.

Procedure:

1. **Invoke the `figma-to-optimizely` skill.** The skill is bundled with this plugin. Follow its workflow exactly:
   - Parse the Figma URL (extract `fileKey` and `nodeId`, convert `-` to `:` in nodeId).
   - Verify Figma MCP is available (`mcp__plugin_figma_figma__*` or `mcp__figma-desktop__*`). If not, stop and tell the user to install the Figma plugin.
   - Create `experiments/$2/output/Optimizely/` and `experiments/$2/qa/` if they don't already exist (use `mkdir -p`). No `input/` folder — the team tracks briefs and hypotheses elsewhere.
   - Read the Figma design context across breakpoints (desktop / tablet / mobile if available).

2. **Generate the four widget files** in `experiments/$2/output/Optimizely/`:
   - `index.html` — semantic markup with `{{extension.fieldName}}` template variables and the root id `optimizely-extension-{{ extension.$instance }}`.
   - `styles.css` — fully scoped under one root wrapper class, transparent background, all three responsive breakpoints (mobile ≤619px, tablet 620–1023px, desktop ≥1024px).
   - `script.js` — uses `optimizely.get('utils')`, `widget.selector`, `widget.$html`. Idempotent. Reference `references/widget-bootstrap.js` for shape.
   - `widget.json` — `form_schema` with one entry per `{{extension.fieldName}}` in the HTML (each entry has its own `options` key, `null` for text/image/selector), PLUS a top-level `description` string and a top-level `options` object inlining the html/css/apply_js/undo_js. Both are required or Optimizely rejects the import ("Description/Options is a missing or invalid value"). Read the three code files back and embed them with a JSON serializer — don't hand-escape.

3. **Generate `experiments/$2/preview.html`** — a local-only wrapper that:
   - Inlines `styles.css` in `<style>`.
   - Renders the HTML with every `{{extension.fieldName}}` substituted by the corresponding `default_value` from `widget.json`.
   - Substitutes `{{ extension.$instance }}` with `preview`.
   - Includes a small banner reading "Local preview — substitutions from widget.json defaults. Real widget runs through Optimizely's widget API."
   - Does NOT include `script.js` (it depends on globals that don't exist locally).

4. **Spin up the local preview server** (mandatory — don't skip):
   - Start `python3 -m http.server 8765` in the background from `experiments/$2/`.
   - If port 8765 is in use, increment until you find an open one.
   - Run `open http://localhost:<port>/preview.html` to launch the user's browser.
   - Tell the user the URL and ask them to confirm the widget renders correctly.

5. **Self-review against the constraints checklist** (see `references/optimizely-constraints.md`):
   - No React, JSX, imports, hooks, modules, or Tailwind utilities.
   - CSS fully scoped under one wrapper class.
   - JS prevents duplicate render and fails safely on missing mount.
   - All three responsive breakpoints present.
   - Every `{{extension.fieldName}}` in HTML matches a `form_schema` entry.
   - `widget.json` has a top-level `description` and a top-level `options` object (`html`/`css`/`apply_js`/`undo_js`), all non-empty.
   - Root background is `transparent`.
   - Star ratings (if present) use individual SO SVGs with `--fill`.
   - Optionally run `"${CLAUDE_PLUGIN_ROOT}/scripts/validate-output.sh" experiments/$2` to smoke-check structure and widget.json import-readiness.

6. **Write QA notes** to `experiments/$2/qa/implementation-notes.md` covering:
   - What pastes into Optimizely's HTML / CSS / JS / widget JSON panes.
   - The mount selector default.
   - Risks (host-page collisions, breakpoint edge cases).

7. **Confirm with the user** before reporting done. If they spot a visual issue in the preview, iterate on the output files and refresh.

Hand off note to print at the end:

```
Done. Deliverables for the engineer:
  experiments/<name>/output/Optimizely/index.html
  experiments/<name>/output/Optimizely/styles.css
  experiments/<name>/output/Optimizely/script.js
  experiments/<name>/output/Optimizely/widget.json

Two ways to deploy:
  - Paste index.html / styles.css / script.js into Optimizely's HTML/CSS/JS panes (widget.json supplies the form_schema), OR
  - Import widget.json on its own — it's self-contained (options carries the code + description).
```
