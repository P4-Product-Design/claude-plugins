# Figma → CSS traps

Measured differences between how Figma lays out a node and how CSS does. Each one cost a revision on a real build. Check the relevant ones during Process step 4, and measure rather than eyeball: most of these are invisible in a screenshot.

## Text

- **Line-height rounds to whole pixels in Figma.** Figma lays text out on `round(fontSize × pct)` (16px @ 170% → 27, not 27.2). Author line-heights in px wherever text can wrap, or multi-line blocks drift a pixel or more per paragraph.
- **Hug width excludes the last glyph's letter-spacing.** Figma's hug width, and its line-breaking in a fixed box, ignore the tracking after the final character; CSS includes it. Compensate with `margin-right: -<tracking>em`, or on a padded button `padding-inline-end: calc(<pad> - <tracking>em)`.
- **Figma counts a trailing space in a hug width; CSS drops it.** If a hug box is about one space too narrow, check the copy for a trailing space and use `white-space: break-spaces`.
- **Check `textTruncation` / `maxLines` before calling a line clamp an invention.** If set, ship `-webkit-line-clamp`.
- **Check `textDecoration`.** An underline in the default state doesn't show up in a node dump scan, and it changes the hover (it can't be "add underline").
- **A 1px font-metric difference between Figma's bundled font and the webfont can flip a line break.** No CSS lever fixes it; note it and move on.
- **Literal arrows (→) may not be in the served webfont subset** and silently fall back to a system font. Draw them as SVG or load a subset that covers them.

## Strokes and boxes

- **INSIDE stroke** = CSS `border` with `box-sizing: border-box` (it shrinks the content box, not the outer box). Where the stroke must not change size at all, `box-shadow: inset 0 0 0 Npx` plus a `forced-colors` fallback.
- **OUTSIDE stroke** adds no height in Figma: use `box-shadow: 0 0 0 Npx` or `outline`, never `border`. Inside a scroll container the ring needs `padding: 1px; margin: -1px` on the track, and with scroll-snap also `scroll-padding: 1px` (the snapport is the padding box).
- **A zero-height LINE** contributes 0 to its parent: `height: 0; margin: -1px 0; border-top: 2px`.
- **FILL/HUG maps to different CSS depending on the parent's direction.** In a horizontal parent FILL is `flex: 1 1 auto`; in a vertical parent it's `align-self: stretch`. A CSS grid or flex item stretches where a Figma child HUGs: add `align-items: start` / `align-self: flex-start`.
- **A negative auto-layout gap is an overlap.** Measure child positions to find what actually overlaps what; a negative gap bigger than the next child is not the overlap amount. Prefer one grid (the overlapping band as its own grid item) over a negative margin when content moves between the band and the row across breakpoints.
- **When Figma moves a node between parents across breakpoints,** `display: contents` on the in-between wrapper lets one element take part in different layouts without duplicating it.
- **An asymmetric two-column split** is often `flex: 1 1 0` on both plus `max-width` on one, with no media query.

## Images and vectors

- **An exported vector's ink can be smaller (or larger) than its layout box.** Compare `absoluteRenderBounds` with `width`/`height`. Keep the layout box and centre the ink with the `viewBox`, or every icon renders at the wrong size.
- **One icon at two sizes with proportional strokes is one asset** (40px/3px and 32px/2.4px is the same 40×40 viewBox).
- **Before rebuilding a layered image composition,** look on the canvas for a flattened export, and check the layers' alpha: a fully opaque top layer means the ones below never render.
- **An image box may be a ratio, not a height.** Compare across breakpoints; if the ratio is constant, use `aspect-ratio`, and keep `height: auto` beside it (`image_tag`'s width/height attributes become presentational CSS).
- **A Figma MULTIPLY gradient over a photo** can usually be rewritten as a plain black-alpha gradient (black at `a × (1 − g)`).
- **Figma layer blur is about 2× CSS `blur()`** (Figma 32 ≈ CSS 16 by pixel diff).
- **Ship WebP for anything with alpha.** A 3000px PNG-24 hero was 4.75 MB; WebP q88 was 210 KB.

## The Figma file itself

- **Dev Mode annotations can be wrong.** Several builds found annotations that contradicted their own frames. Check each one against the measured frame; the frame wins.
- **Requirements doc frames can hold build rules that no frame shows** (e.g. an overlay that's absent from every dev-ready frame). Read them.
- **Frames named like scaffolding (`Empty Frame`) can be real** — e.g. a background band that starts the next section's colour early.
- **Check component properties before assuming two instances match.** The same card component can have boolean properties on in one section and off in another.
- **Layer names can differ between copies of the same card** (`Title` vs `Article Title 3`). A `findAll` by name can silently miss nodes.
- **Compare against Figma's rendered PNG at least once per section.** The node dump doesn't surface everything.

## Verifying in a browser

- **Sticky belongs on Shopify's section wrapper.** Each section renders inside its own element that is exactly as tall as the section, so `position: sticky` inside it has zero travel. Use `.shopify-section:has(> .your-sticky-root)` or the theme's own pattern. A preview only proves stickiness if it renders that wrapper.
- **Test against the live theme CSS.** Load the theme's CSS into the preview *before* the section's style (production order), plus its `:root` variables. Theme globals reach any property a section leaves unset: `img { max-width: 100% }` caps overhanging images, heading `letter-spacing` leaks into every `h2`, `.input:focus` can kill a focus ring.
- **Sweep the whole page width, not just the section's boxes** (`documentElement.scrollWidth`). An absolutely positioned visually-hidden span with no positioned ancestor inside its scroller can widen the page on phones.
- **A stretched link with the ring on `::after` draws two focus rings** unless the link's own `:focus-visible` sets `outline: none`.
- **Synthetic pointer moves don't trigger real `:hover`** in an automated browser: verify hover through the CSSOM. `:focus-visible` can be verified with real Tab presses.
- **Headless Chrome has a ~500px minimum window.** Capture mobile widths through a wrapper page with a fixed-width iframe.
- **Remove any style you injected while testing** (and reload) before handing a preview back.
