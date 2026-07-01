---
name: figma-to-shopify-liquid
description: Use when converting a Figma design into a Shopify theme section or block (.liquid) — especially with separate mobile/tablet/desktop frames, an "exact match, no deviations" requirement, an existing component to match structurally, or live product/review data to wire in. Triggers on a Figma link plus a request for Liquid, a theme section/block, or a pixel-perfect implementation.
---

# Figma to Shopify Liquid

## Overview

Turns a Figma design into a production Shopify `.liquid` section/block that matches it exactly — same tokens, spacing, fonts, breakpoints — plus a documentation file and a static HTML preview. The core discipline: **read the design's own annotations instead of eyeballing the screenshot, verify breakpoints with measured values instead of assuming, and ask before assuming anything the design doesn't explicitly answer.**

## Step 0 — If you weren't given enough to start

Check the request against the list below. **Anything already provided is settled — don't re-ask for it.** Anything missing from the "Required" list gets asked in one short, numbered message before any research starts. Don't guess a Figma link, don't assume the target file, don't invent scope.

**Required:**
1. **Figma link(s), one per breakpoint that behaves differently.** Each must be a node-specific URL (contains `node-id=`) — a file-only link with no node ID isn't enough. **If exactly one link was given, don't silently assume it's the only breakpoint and don't silently assume there must be more — ask directly**: "Is this the only breakpoint, or are there separate mobile/tablet/desktop frames I should pull too?" Guessing wrong here means redoing structural work later, so this is always a direct question, never an inference.
2. **Target location** — is this a new component, or does it replace/extend something that already exists? If it exists, its path/link.
3. **Fidelity bar** — exact 1:1 match (tokens/spacing/fonts, zero deviation), or is some interpretation OK?
4. **Backend data** — does this need live Shopify data (product info, price, reviews, inventory, apps like Judge.me/Rebuy/Recharge), or is it fully static content?
5. **Deliverables** — file types default to `.liquid` + a docs file + a static HTML preview unless told otherwise, but always ask one thing explicitly: should the docs file be **real documentation**, or a plain copy of the code, or something else? Never assume this one — a prior project's ".md" might turn out to be a literal duplicate of the code, not documentation.

**Nice to have — mention once, don't block on them:**
6. A prior similar component in this codebase, to learn the *process* (research → build → ship pattern) and the *file conventions* (naming, folder layout) from.
7. Any naming/folder convention for the output.

Don't turn the Dev Mode annotations into a question — they get read regardless of what the user says, so just note that in passing rather than asking permission for it.

Once required items 1–5 are answered, move straight to Process step 1.

## Process

1. **Learn the codebase's conventions, separately for process and structure.** If a prior similar build exists, read it for *process* (how it was researched, audited, and shipped) and for *file conventions* (deliverable naming/layout). Read the *current/target* file (if one exists) for the *architecture* to match — block vs. section, `{% style %}` vs. a raw `<style>` tag, how granular the settings are, CSS scoping convention, existing breakpoint values. When the reference project and the target file disagree on structure, match the target — that's what you're actually editing alongside.
2. **Pull every Figma frame.** One `get_design_context` call per breakpoint node (not just the overview frame — it usually returns sparse metadata only). Add `get_variable_defs` for exact token names/values, and keep the screenshots for visual reference.
3. **Read every annotation, don't skip them.** Figma Dev Mode annotations surface in the `get_design_context` response as `data-development-annotations`, `data-accessibility-annotations`, and `data-content-annotations` attributes on the relevant elements. These carry the precise, unambiguous version of things a screenshot only implies — exact breakpoint pixel values, responsive image behavior, "make this adjustable" requirements. Quote them in the implementation's header comment with their node IDs, so a future editor can trace every non-obvious decision back to its source.
4. **Diff the breakpoints using measured values, not assumptions.** Use the actual position/size numbers the tool returns to determine what really changes and at what exact pixel threshold. Breakpoints often don't land where you'd guess — two frames can be pixel-identical and only diverge at a threshold called out in an annotation (e.g. exactly 1024px, not a generic device width).
5. **Decide fixed vs. settings-driven, per value.** Match the codebase's existing convention for how much is merchant-editable. When there's no precedent, default to: hardcode exact layout/spacing values (guarantees the match holds even if someone fat-fingers a setting), expose settings for anything an annotation calls out as needing adjustability, and for anything naturally editorial (copy, images, brand colors).
6. **Wire backend data if needed, static otherwise.** See `backend-data-wiring.md` in this skill folder for the pull-real-data-with-a-fallback pattern. If nothing needs live data, say so in a comment — saves the next editor from wondering why it isn't wired up.
7. **Surface real ambiguities before writing any code.** In particular: blast radius (are you about to edit a shared component that other pages depend on — build a dedicated one instead if so), CMS structure for anything that doesn't map to a native setting type (e.g. multi-color text needs split fields — most rich-text editors can't preserve a custom color span), any scope decision that goes beyond what Figma explicitly shows, and deliverable format. Ask, don't assume — the annotations answer a lot, but not everything.
8. **Present the design — architecture, tokens/breakpoints, new settings, file plan — and get explicit approval before creating any files.**
9. **Build:** the component (matching the target's exact architecture), the docs file (per what was agreed in Step 0), and a static HTML preview — same CSS as the component with placeholder/real content substituted for template tags, and a small banner flagging it as a static mock.
10. **Verify in an actual browser**, at every real breakpoint including the exact pixel value where behavior changes (not just generic device presets — a custom threshold like 1024px falls between "tablet" and "desktop" presets and will be missed by them). Use computed-style inspection to confirm measured values match Figma's numbers exactly, not just a visual glance. Check console/network for errors. Validate that any JSON schema block actually parses.
11. **Deliver with a summary of what was verified**, not just what was built.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Assuming a docs file's format from a prior project's precedent | Ask — a prior ".md" may be a literal copy of the code, not real documentation |
| Assuming tablet gets its own distinct styling | Verify with measured values — breakpoints can collapse together or land on non-standard thresholds |
| Editing a shared/generic component in place | Check blast radius first; build a dedicated component if other pages might depend on the shared one |
| One rich-text field for multi-color or multi-style text | Split into separate fields — native rich-text editors usually can't preserve a custom color span through re-edits |
| Generic `alt` text on a purely decorative background image | Use `alt=""` — the real message should already exist as on-page text, not be baked into the image |
| Lazy-loading an above-the-fold hero image | Only lazy-load below-fold images; eager-load the hero (`fetchpriority="high"` if it's genuinely the LCP element) |
| Assuming an `image_picker` setting has a default image | Shopify doesn't support one — always add a graceful fallback (solid color, etc.) for the unset state |
| Verifying only at generic device presets (375/768/1280) | Also test the exact pixel value from the annotation/measurement — presets can sit on the wrong side of a custom breakpoint |

## Reference

- `backend-data-wiring.md` — the pull-real-data-with-a-fallback pattern for product info, reviews, and app widgets (Judge.me, Rebuy, etc.). Load this only when Step 0 confirms backend data is in scope.
