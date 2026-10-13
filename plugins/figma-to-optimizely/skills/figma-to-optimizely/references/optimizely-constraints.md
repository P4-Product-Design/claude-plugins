# Optimizely Constraints

## Supported
- HTML
- CSS
- JavaScript

## Unsupported for final deliverables
- React
- JSX
- Vue, Svelte, any other framework
- Tailwind runtime / utility classes
- component libraries
- imports
- ES modules
- build tooling, bundlers
- npm dependency assumptions
- TypeScript syntax (compile away)

## Required implementation behavior
- CSS must be scoped to a single root wrapper class.
- JS must fail safely if the target node is not found.
- JS must avoid duplicate rendering on repeated execution.
- Markup should be semantic where possible.
- Output should be easy to paste into Optimizely's widget editors.
- Root wrapper background must be `transparent`.

## Responsive breakpoints
- Mobile: 619px and below — `@media (max-width: 619px)`
- Tablet: 620px to 1023px — `@media (min-width: 620px) and (max-width: 1023px)`
- Desktop: 1024px and above — `@media (min-width: 1024px)`

## Optimizely widget API surface (the only globals you can rely on)
- `optimizely.get('utils')` — exposes `waitForElement(selector)` returning a Promise
- `widget.selector` — the CSS selector chosen in the widget config's `selector` field
- `widget.$html` — the rendered HTML string with `{{extension.fieldName}}` already substituted
