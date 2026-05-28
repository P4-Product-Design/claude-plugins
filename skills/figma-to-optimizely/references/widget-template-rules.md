# Widget template rules

## Root element
Every widget has exactly one root element with this id pattern:

```html
<div id="optimizely-extension-{{ extension.$instance }}" class="<scoped-wrapper>">
  ...
</div>
```

The `{{ extension.$instance }}` is substituted by Optimizely at render time so multiple instances of the same widget on a page don't collide.

## Template variables

Every customizable string, image src, URL, rating value, or color must use `{{extension.fieldName}}` syntax. Examples:

- Text: `<h2>{{extension.headline}}</h2>`
- Image: `<img src="{{extension.imageone}}" alt="{{extension.imageonealt}}">`
- URL: `<a href="{{extension.cta1url}}">{{extension.cta1text}}</a>`
- Rating value driving CSS: `<span class="so-star" style="--fill: {{extension.prod1star1}};">`

## form_schema rules

Every `{{extension.fieldName}}` in `index.html` must have a matching entry in `widget.json`'s `form_schema` array. If it doesn't, the engineer can't edit it in Optimizely's widget UI.

Field types:
- `text` — plain text strings (headlines, body copy, ratings as strings, CTA labels)
- `image` — image URLs (uploads or external)
- `selector` — CSS selector for the mount target (one per widget, named `selector`)
- `html` — when you need rich content; rare

Required fields in every widget.json:
- `plugin_type`: `"widget"`
- `name`: human-readable widget name (becomes the widget label in Optimizely)
- `edit_page_url`: URL of the page where the widget will be edited/previewed
- `form_schema`: array of field definitions (each entry needs its own `options` key — `null` for `text`/`image`/`selector`)
- `description`: one-line human summary of the widget. **Required** — Optimizely rejects the import with "Description is a missing or invalid value" if absent.
- `options`: object holding the widget's code, inlined: `{ "html": ..., "css": ..., "apply_js": ..., "undo_js": ... }`. **Required** — without it the import fails with "options is missing or has an invalid value".

### The `options` object (combined import)

`widget.json` is not just a form_schema config — it is a self-contained, importable Optimizely extension. The `options` object carries the same code that lives in the separate files:

- `html` — exact contents of `index.html`
- `css` — exact contents of `styles.css`
- `apply_js` — exact contents of `script.js` (the mount/apply logic)
- `undo_js` — teardown that removes the widget when the variation is reverted. Standard snippet:
  ```js
  const extensionElement = document.getElementById('optimizely-extension-' + extension.$instance); if (extensionElement) { extensionElement.parentElement.removeChild(extensionElement); }
  ```

Keep `options` in sync with the three code files — they are the same content, escaped as JSON strings. The separate files remain for engineers who paste pane-by-pane; the combined `options` is for teammates who import the single JSON.

## Field naming convention

Use lowercase, no separators, repeated index suffixes for arrays:
- `brand1`, `brand2`, `brand3` (not `brand-1` or `brand_1`)
- `prod1star1` through `prod1star5` for star fills on product 1
- `cta1text`, `cta1url`, `cta2text`, `cta2url`

This matches Luke's existing widgets and keeps `form_schema` field names valid as Optimizely identifiers.

## What goes in HTML vs JSON vs CSS vs JS

| Optimizely pane | Pastes from |
|---|---|
| HTML / Custom Markup | `index.html` |
| CSS | `styles.css` |
| JavaScript | `script.js` |
| Widget config (form_schema) | `widget.json` |

The four files are deployed together as one widget. Alternatively, the whole widget can be deployed in one shot by importing `widget.json` — its `options` object already contains the HTML/CSS/apply_js/undo_js, so no pane-by-pane pasting is needed.
