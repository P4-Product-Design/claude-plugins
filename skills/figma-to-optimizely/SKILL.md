---
name: figma-to-optimizely
description: Convert a Figma design into an Optimizely Web Experiment widget (HTML, CSS, JS, widget.json) and spin up a local preview. Use when the user shares a Figma URL/frame selection and wants Optimizely-ready widget code, asks to "ship", "convert", "code", or "implement" a Figma design "for Optimizely" or "for the experiment", mentions handing off to an Optimizely engineer for an A/B test, or is working in a repo with `experiments/` and `design/figma/`.
---

# figma-to-optimizely

Turn a Figma frame into a production-ready Optimizely Web Experiment widget. Output is four files:

- `index.html` — widget markup using `{{extension.fieldName}}` template variables
- `styles.css` — scoped CSS, transparent root background
- `script.js` — Optimizely widget API for mounting and targeting
- `widget.json` — widget config with `form_schema` defining every editable field, PLUS a top-level `description` and an `options` object that inlines the html/css/apply_js/undo_js

The engineer can either paste the first three files pane-by-pane (with `widget.json` supplying the form_schema), OR import `widget.json` alone — it is self-contained, so its `options` carries the full code. Both paths must work, so `widget.json` is never just the form_schema.

## Prerequisites

Before generating files, confirm the user has:
1. A Figma URL or frame selection (desktop + mobile breakpoints ideally).
2. Figma MCP available (the `mcp__plugin_figma_figma__*` tools, or `mcp__figma-desktop__*`). If not, ask them to install the Figma plugin first — without it you cannot read the design as source of truth.

The plugin creates folders on the fly. The canonical layout it produces:

```
experiments/<experiment-name>/
  output/Optimizely/   (index.html, styles.css, script.js, widget.json)
  qa/                  (implementation-notes.md)
  preview.html         (local-only preview wrapper)
```

There is no `input/` folder — the team tracks briefs, hypotheses, and copy variants elsewhere (Notion). The plugin only produces what Optimizely needs plus a thin set of QA notes for the engineer.

## Workflow

### 1. Read the design

- Parse the Figma URL: extract `fileKey` and `nodeId` (convert `-` to `:` in nodeId).
- Call `mcp__plugin_figma_figma__get_design_context` with the nodeId and fileKey for each breakpoint frame (desktop, tablet, mobile).
- The output is React+Tailwind — treat it as a **reference, not final code**. You will rewrite it as plain HTML/CSS/JS.
- Read fill colors from actual swatch fills via Figma MCP, not text labels. Hex labels in the design lie.

### 2. Generate the four output files

Write to `experiments/<experiment-name>/output/Optimizely/`. The four files together form one widget.

#### index.html
- Single root element: `<div id="optimizely-extension-{{ extension.$instance }}" class="<scoped-wrapper>">`
- Every customizable string, image src, URL, rating value: `{{extension.fieldName}}`
- Semantic markup. No framework syntax.
- Add HTML comments calling out A/B-testable elements (brand, rating, headline, promo, CTA, etc.).

#### styles.css
- All selectors scoped under the root wrapper class — never bare element selectors that could leak into the host page.
- Root background: `transparent`. The widget sits inside the host page; no white wrapper.
- No global resets, no fragile selectors.
- Responsive media queries:
  - Mobile: `@media (max-width: 619px)`
  - Tablet: `@media (min-width: 620px) and (max-width: 1023px)`
  - Desktop: `@media (min-width: 1024px)`
- Flatten Tailwind utilities into explicit declarations.

#### script.js
- Use Optimizely widget API: `optimizely.get('utils')`, `widget.selector`, `widget.$html`.
- Idempotent — prevent duplicate render on repeated execution.
- Fail safely if mount target is missing.
- No global scope pollution. No imports/modules/build steps.
- Reference shape: `references/widget-bootstrap.js`.

#### widget.json
- `form_schema` defines every `{{extension.fieldName}}` from `index.html` with the correct `field_type` (`text`, `image`, `selector`, etc.).
- Every templatized field in HTML must appear here, or the engineer can't edit it in Optimizely.
- Each `form_schema` entry includes its own `options` key — set it to `null` for `text`/`image`/`selector` fields.
- **Top-level `description`** (string): a one-line human summary. REQUIRED — Optimizely rejects the import with "Description is a missing or invalid value" without it.
- **Top-level `options`** (object): the widget's code inlined as `{ "html", "css", "apply_js", "undo_js" }`. REQUIRED — without it the import fails with "options is missing or has an invalid value". This makes `widget.json` a self-contained, one-shot importable extension.
  - `html` = exact contents of `index.html`
  - `css` = exact contents of `styles.css`
  - `apply_js` = exact contents of `script.js`
  - `undo_js` = teardown that removes the widget on revert:
    `const extensionElement = document.getElementById('optimizely-extension-' + extension.$instance); if (extensionElement) { extensionElement.parentElement.removeChild(extensionElement); }`
- Keep `options` byte-for-byte in sync with the three code files. Easiest path: write `index.html` / `styles.css` / `script.js` first, then read them back and embed their contents (properly JSON-escaped) into `options`. Don't hand-escape — use a JSON serializer so quotes/newlines are correct.
- Reference shape: `references/widget-json-example.json`.

### 3. Star ratings (Sleepopolis-specific, common pattern)

If the design has star ratings:
- Use **individual SO-branded star SVGs** with `viewBox="0 0 20 19"`, empty fill `#FFEED5`, filled fill `#FFC468`.
- Each star has its own `--fill` CSS variable for partial fills (e.g., 4.6 stars → 4 full + 1 at 60%).
- Do NOT use a single combined SVG, and do NOT use a third-party star icon font.
- Reference markup: `references/so-star.html`. Reference styles: `references/so-stars.css`.

### 4. Generate `preview.html`

After the four widget files are written, also write `experiments/<name>/preview.html`. This wrapper renders the widget locally with default values from `widget.json`, so the user can see it before handing off.

The preview must:
- Inline `styles.css` in a `<style>` tag inside `<head>`.
- Render `index.html` with every `{{extension.fieldName}}` substituted by the corresponding `default_value` from `widget.json`'s `form_schema`.
- Substitute `{{ extension.$instance }}` with `preview` so the root id is stable.
- Include a small note at the top of the page (`<header>`) reading "Local preview — substitutions from widget.json defaults. Real widget runs through Optimizely's widget API."
- NOT include `script.js` — that script depends on the live `optimizely` global and `widget` object, which don't exist locally.

### 5. Spin up the local preview server

Mandatory. Don't mark the task done until the user has eyeballed the preview.

1. From the experiment directory, start a Python HTTP server in the background:
   ```bash
   cd experiments/<name> && python3 -m http.server 8765
   ```
   Use the `run_in_background` Bash flag.
2. Open the preview in the user's default browser:
   ```bash
   open http://localhost:8765/preview.html
   ```
3. Tell the user the URL and ask them to confirm it looks right. If the port 8765 is in use, increment to 8766, 8767, etc.
4. After they confirm (or after they've had a chance to look), kill the background server.

If `python3` isn't available, fall back to `python -m SimpleHTTPServer 8765` or `npx http-server -p 8765`.

### 6. Write the QA notes

After preview confirmation, write `experiments/<name>/qa/implementation-notes.md` with:
- What goes in Optimizely's HTML / CSS / JS / widget JSON panes
- DOM target / insertion assumption (the `selector` field's default value)
- Any risks the engineer should QA (host-page collisions, mount selector fragility, mobile breakpoint edges)

### 7. Self-review against the constraints checklist

Before reporting done, verify:
1. No React, JSX, imports, hooks, modules, or Tailwind utilities in any output file
2. CSS fully scoped under one root wrapper
3. JS prevents duplicate render and fails safely on missing mount
4. All three responsive breakpoints present
5. Every `{{extension.fieldName}}` in HTML has a matching entry in `widget.json` `form_schema`, and every `form_schema` entry has its own `options` key (`null` for text/image/selector)
6. Root wrapper background is `transparent`, not white or any solid color
7. Star ratings (if present) use individual SO SVGs with `--fill` CSS variable
8. `widget.json` has a top-level `description` (non-empty string) AND a top-level `options` object with all four keys (`html`, `css`, `apply_js`, `undo_js`), each a non-empty string. `options.html`/`css`/`apply_js` match the three code files. Missing `description` or `options` is the #1 cause of Optimizely import failures ("Description/Options is a missing or invalid value").
9. `preview.html` was generated AND the local server was spun up AND the user confirmed it visually

For the full constraint reference: `references/optimizely-constraints.md`. For widget template rules: `references/widget-template-rules.md`. For the star pattern: `references/star-rating-pattern.md`.

## Hard constraints — Optimizely platform

Optimizely Web Experiments supports HTML, CSS, JavaScript only. Never emit:
- React, JSX, Vue, Svelte
- Tailwind runtime / utility classes (flatten them)
- npm imports, ES modules, `import` / `require`
- Component libraries
- Build tools, bundlers, transpilation steps

If the Figma MCP output references any of the above, rewrite — don't pass through.

## Output handoff

The engineer receiving the code needs the four files in `experiments/<name>/output/Optimizely/`. Two deployment paths, both supported:
- **Pane-by-pane** — paste `index.html`, `styles.css`, `script.js` into Optimizely's HTML/CSS/JS panes; `widget.json` supplies the form_schema.
- **One-shot import** — import `widget.json` alone. Its `options` object already carries the html/css/apply_js/undo_js and its top-level `description` satisfies the importer.

Tell the user both work, so less-technical teammates can just import the JSON. Zip the folder or hand off the files directly.

## Common corrections (learned from prior runs)

- **Read swatch fills, not hex labels** — in Figma, the text next to a swatch is often stale. Always read the actual fill color via Figma MCP.
- **Use real components from the UI Kit, not recreations** — if the design uses a published component (PBL, button, star), inspect that component for spacing/typography rather than approximating.
- **Stars must be customizable per-star** — the engineer needs to set rating values via Optimizely's widget form, so each star reads its `--fill` from CSS.
- **No white background on the root wrapper** — widgets live inside host pages; a white wrapper visually breaks the page.
- **All A/B-testable content must be templatized** — if the engineer can't edit it in Optimizely's form, it's not really testable.
- **Always preview before handoff** — render `preview.html` in a local server and have the user look at it. Visual bugs hide in static code.
