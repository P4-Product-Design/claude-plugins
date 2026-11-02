# Swolverine theme reference

Read this in Step 0 of every build. It settles most of Step 0 item 4 (backend data) and the file conventions in items 6–7. Anything here that conflicts with the target file loses to the target file. Check the local `Theme/` folder in the Swolverine project when one exists; if it doesn't, `shopify theme pull` gets the live theme.

## Sources

- **Figma:** "Swolverine Mini UI Kit", file `DVt76xoNBw8gjUTHUl5KuP`. Every component and page design is in this one file. Component states are in the `Components` frame (`9514:10956`, page `↳ Homepage`); `Button` is on `↳ Styles & Brand Components`.
- **Prior builds to learn the process from:** the `swol-*` sections in the theme. Each opens with a long header comment (Figma nodes, annotations, decisions, gotchas). `swol-homepage-reviews`, `swol-stack-save-v2-builder` and `swol-homepage-stack-bundles` are the most complete.
- **Shared state reference:** `Builds/Homepage/_component-states.md` in the Swolverine project lists every component's Figma-defined states. Read it before building anything interactive.

## Naming and files

- New sections and blocks are always **new, dedicated files** named `swol-<page>-<section>.liquid` (e.g. `swol-homepage-reviews`, `swol-rts-hero`, `swol-stack-save-v2-builder`). Never edit an existing theme file. When a section replaces an older one, the old file stays in the theme untouched as the rollback.
- A file that uses `block.id` is a theme block (`blocks/`); one that uses `section.id` is a section (`sections/`).
- Any exception (an edit to a shared theme file) must be agreed with the user, backed up first, and logged in the project's `Builds/_theme-changes.md`. Changes logged there must deploy with the sections that need them (e.g. the `main.js` carousel fix).
- Deliverables live in `Builds/<Area>/<Name>/`: `<theme-name>.liquid`, `<theme-name>.md` (real documentation: revision history, Figma node table, decisions — not a code copy), `<theme-name>-preview.html`, `assets/`. At handoff, copy the files into `Theme/` too.
- **Previews are generated, never hand-edited.** `Builds/Homepage/_gen-preview.py` builds a preview's CSS/JS from the `.liquid` and refuses unbalanced braces, undefined `swol-` classes, Liquid tags inside the style block and `{{ sid }}` classes in scripts. Write section JS against `data-*` hooks so it survives the copy.
- Static previews are served from the `swol-liquid-previews` launch config (port 8812, rooted at `Builds`); `file://` previews break relative asset paths.

## CSS scoping

- Scope per instance: `assign sid = section.id | replace: '_', '' | downcase`, then a unique, stable prefix per section, e.g. `.swol-rv-{{ sid }}__card`.
- Put tokens on the section's own root, never `:root`.
- No bare element selectors and no generic class names. `.card`, `.grid`, `.btn`, `.drawer`, `.modal` are global in the theme's `main.css`, and `.drawer` freezes page scroll.
- **Never use a Liquid tag inside the `{% style %}` block, even inside a CSS comment.** Liquid doesn't know about CSS comments; an unclosed tag stops the section rendering at all.
- Theme globals that reach unset properties: `img { max-width: 100% }` (set `max-width: none` on overhanging images); `h2` heading tracking (always set `letter-spacing`, even 0); `input { background-clip: padding-box }` (set `border-box`); `.input:focus { outline: 0 }` kills the focus ring on anything with the theme's `.input` class.

## Layout and type

- **Breakpoints:** mobile-first. `1024px` is the only typographic breakpoint on most pages (type steps up, header and footer switch). Layout can also change at `768px`; `1440px` and `1280px` appear only where measured. Mobile gutter is 24px from 375px, 16px below it (`max-width: 374px`).
- **Content cap:** `max-width: 1500px`, centred. It is a max-width, not a breakpoint.
- **Vertical rhythm:** a section owns the space above it. It takes its group's padding-top (first child) or the group gap above it, and no bottom padding; the last child of a group also takes the group's padding-bottom.
- **Card rows:** horizontal scroll comes from a 300px card minimum (`flex: 1 0 300px` on a 24px-gap row), not a per-breakpoint rule.
- **Fonts:** Saira Semi Condensed 700 for headings, Inter 400/500/700 for body and buttons, loaded from Google Fonts. Current sections each load them in their own `<link>` tags (async preload pattern); match that unless the user says the fonts have been moved into `theme.liquid`. The served Inter has no `→`, so draw arrows as SVG.

## States and tokens

- `#f2f6fa` is the universal hover/pressed fill (the main exception is `Button`).
- Desktop components define Hover, mobile ones define Pressed: put hover inside `@media (hover: hover)`, pressed on `:active`. `Button` has no Pressed or Disabled variant; reuse its Hover for `:active`.
- Focus ring: `outline: 2px solid #4b4efc; outline-offset: 0` (from `.formInput State=Focused`; the "Default focus state color" swatch showing INSIDE is a decoy). It is only 2.56:1 on the footer's `#2b2b2b`; flag it on dark surfaces.
- Motion: every measured Figma transition is `300ms cubic-bezier(.42, 0, .58, 1)` (SMART_ANIMATE, EASE_IN_AND_OUT); chips and tabs are 0.5s. Older homepage sections still use a 150ms placeholder. Always add a `prefers-reduced-motion: reduce` fallback.
- Carousel arrows follow the scroll, not the breakpoint: show them wherever the row can actually scroll, even if Figma draws them where it can't.
- Button: radius 99, 1px inside stroke. Primary `#ccff00` → hover `#f0ffb2`, Secondary `#111827` → `#374151`, Tertiary `#1de2ff` → `#85efff`. Text link hover `#4b4efc` → `#1a1a1a`. Neutrals: 900 `#1a1a1a`, 800 `#313131`, 600 `#67696f`, 200 `#e5e7eb`, card ring `#d6ddeb`.
- No form has designed loading/success/error states. Submitting reuses `.formInput` Disabled plus `aria-disabled` on the button.

## Apps and data sources

| Need | Source | How |
|---|---|---|
| Star rating + count | Judge.me, synced to Shopify's native metafields | `product.metafields.reviews.rating` / `rating_count` (product cards). The PDP uses `product.metafields.judgeme.all_reviews_rating` / `all_reviews_count` |
| Review widget / badge | Judge.me app blocks | `judge-me-reviews/blocks/review_widget`, `preview_badge`; the `judgeme_core` app embed is on. Legacy code reads `product.metafields.judgeme.widget` / `.badge` (pre-rendered HTML). `stamped` references are dead legacy |
| Testimonial cards (named reviews) | Section blocks the merchant fills in | Judge.me gives Liquid no per-review text, name or verified flag, so designed review rails can't be driven by it. Stars and "Verified Buyer" are per-block settings; a store-wide review count is a free-text setting |
| Cart drawer | Rebuy Smart Cart | Loaded in `theme.liquid` (`rebuy.js` + `rebuy-smartcart-extensions`). Restyled only through Rebuy's Custom CSS, never theme code. Hidden by `div#rebuy-cart { display: none; }` in `theme.liquid` until go-live |
| Cross-sell widgets | Rebuy | `snippets/rebuy-complete-the-look.liquid` |
| Subscriptions | Recharge | `recharge-subscriptions/blocks/subscription-widget-v2` app block on the PDP |
| Build-your-own bundles | Recharge Bundles, on product `build-stack` (`product.recharge-bundle` template) | Custom UI over Recharge, never a replacement. Read tiers from Recharge (`getCDNBundleSettings`) rather than hardcoding them; never write `_rc_bundle*` properties yourself (`getDynamicBundleItems` does) |
| Prebuilt stacks / Add to Cart | Standalone Shopify products | The theme's `<product-form>`, not Recharge |
| Email signup | Klaviyo | Client-side POST to Klaviyo's Client API (public key + list ID as settings, never a private key), inside Shopify's customer form so no-JS still subscribes. Check the API `revision` is current |
| Blog cards | Shopify blog `/blogs/blog` | Mirror `sections/featured-blog.liquid`. Category is `article.tags \| first` (there is no article category metafield) |
| Product fields | Product metafields, namespace `custom` | `short_description` (exists, correct), `category`, `card_badge`, `stacked_with` (doesn't exist yet). `custom.stack_products` and `custom.cost_per_serving` don't exist; `custom.stack` is an article metafield. Expose namespace/keys as settings and collapse silently when empty |
| Flavour / size | Product options | The option named "Flavor"; servings = an option containing "serving"/"size". Sold-out variants disabled |
| Military discount | GovX ID | `govx-id-exclusive-discounts/blocks/govx-id-button` app block; page `/pages/swolverine-govx` |
| Legacy pages | PageFly (`pf-*` sections), Bloggle (blog/articles) | Leave alone |

Collection handles don't match their titles (`pre-workout` = "Energy & Focus", `post-cycle-therapy` = "Recovery Supplements", `intra-workout` = "Build Strength"). Look up handles; don't derive them from names.

## Theme components to reuse

- **`<carousel-slider>`** (`assets/main.js`). DOM contract: `.slider[id] > .slider__grid > .slider__item` (at least 2), and exactly one `.slider-nav` with `.slider-nav__btn[name][aria-controls]` **inside** the element (a sibling nav silently does nothing). It sets `inactive` and hides the arrows when nothing can scroll. Use `display: none` for a nav in a flex column (`visibility` leaves a hole). It only re-measures on the theme's breakpoint changes (640/768/1024/1280/1536); a carousel in a hidden tab measures 0, so call its `handleBreakpointChange()` when the tab opens. A gutter must be track margin, not padding, or it's counted as card space.
- **`<product-form>`** (`assets/main.js`). Contract: a `.js-product-form` form with `[name="id"]` inside it, a `[name="add"]` button and a `.js-form-error` element.
- **`<modal-dialog>`** for Quick View-style modals.
- **Search:** `SearchDrawer` binds one `.header-search-toggle`; a section with a second entry point must call `.open()` itself. `SideDrawer.open()` needs `.js-overlay`.
- **Localization:** the `localization-form` snippet reads `enable_country_selector` / `enable_language_selector` from whatever section renders it.

## Theme gotchas

- **Never use `ul.grid`** for a product grid. A global infinite-scroll script in `theme.liquid` latches onto it.
- **Add to cart:** call `/cart/add.js` with a string URL. `theme.liquid` patches `fetch` and refreshes the cart only for string URLs. `product-form.js` writes to `#cart-icon-bubble` unconditionally, so a custom header must render it or every add throws.
- **Sticky:** sticky goes on the Shopify section wrapper (`.swol-hd-section:has(> .swol-hd--sticky)`), not inside the section. Offsets are header minus announcement bar; the theme's `--header-height` is never set with the new header.
- **No literal `{{` inside a `{% javascript %}` block** (it breaks the money format).
- `collection.products` returns at most 50 products per collection inside a section.
- iOS zooms into selects and inputs under 16px; Stack & Save uses 16px/44px selects.
