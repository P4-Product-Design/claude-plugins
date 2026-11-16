---
name: block-reskin
description: Reskins a block or component that has been copied from one P4 brand UI kit into another (SO, GGR, SA, MN, MC, BB, SWOL, and partner kits AARP, NCOA, Fortune). It relinks every color, text style, corner radius, spacing value, button and nested component to the destination kit, builds local versions of components the destination kit lacks, renames the brand prefixes, and rewrites component descriptions in neutral language. For partner kits it also removes every mention of other brands. It then lists each judgment call as a follow-up question and applies the answers. Use it whenever someone shares a Notion reskin ticket or a Figma link to a block pasted into another brand's UI kit and says "reskin this", "relink this to the MN kit", "copy the product row to GGR", "swap this over to the AARP styles", "reskin for <brand>", or "do the reskin ticket".
---

# Block Reskin

This skill takes a block that has already been pasted into a destination brand's UI kit and makes it fully native to that kit. Colors, type, radius, spacing, buttons and nested components all end up linked to the destination kit and nothing is still linked to the source. The person stays hands-off: the skill makes the best default call for everything, then asks only about the calls that weren't direct matches.

**Brands, kit links and partner rules:** `references/brands.md`
**Tested scripts and traps:** `references/figma-recipes.md`

The Figma tools can't copy between files, so the person pastes the block into the destination kit first.

## Inputs (ask in one message, up front)

1. **Notion ticket.** Fetch it to get the brand, the scope (which variant, such as "promo card") and the source design link. Read the dev requirements too, so the rebuilt components keep the same properties.
2. **The pasted copy:** a link to the frame or page in the destination kit. If the person sends the page link, find the pasted frame on that page.
3. **The source block link.** Take it from the ticket. Ask for it only if the ticket has none.
4. **A visual reference block** in the destination kit. Always ask for it: it decides the look when tokens alone don't, such as a button role or card treatment. MN used Media & Text.

Work out the source and destination brands from the file keys in `brands.md`. If a key isn't listed there, ask which brand it belongs to.

Before reading any Figma file, call `create_session` with the destination file key. Load `figma-use` before every `use_figma` call, and also load `figma-generate-library` before any call that writes.

## Steps

### 1. Inventory (read-only)
- **Pasted frame:** recipe 1. Collect bound variables, text, fill and stroke styles, raw hex colors, radii, fonts, and every remote component with its key.
- **Destination kit:** recipe 2, plus the Button set's variants with their fill, stroke, radius, label, size and `layoutMode`. Call `get_libraries`, then `search_design_system` for each remote component's name.
- **Reference block:** card fill, border and radius, image placeholder, headline and body styles, which button roles it uses, and link color.
- **Doc chrome:** compare the `.header` / `.section` keys in the pasted frame against the destination kit's own pages.
- Screenshot the source block once to compare against later.

### 2. Map (defaults, applied without asking)
For each source token, pick the destination equivalent in this order:
1. Same name.
2. Same role: primary, hover border, tint, placeholder, link, star, tag.
3. Closest value.
4. What the reference block uses.

Spacing and radius are matched **by value**: the same name means a different value in each brand. Record every pick that wasn't a direct same-name, same-value match. These become the follow-ups.

Defaults that have worked well:

| Situation | Default |
|---|---|
| Source header size missing in the destination kit | The nearest destination header size that fits the card width |
| Source button style missing (for example an outline button) | The destination role the reference block uses for that job |
| Card / pill / image radius | The reference block's radius |
| Image placeholder gray | The placeholder color the destination kit's own blocks use |
| Stars, tags, promo tints | The destination colors its own product blocks use for them |
| Partner kit missing a token | The closest partner value. Never leave it linked to another brand |

### 3. Rebuild components the destination kit lacks (recipe 3)
For each remote source component with no destination match, make a local copy, working leaf-first. Combine variant sets back into component sets. Put the copies in a `.<dst>Subcomponents` frame (for example `.mnSubcomponents`) to the right of the block. Relink every instance to the local copy, and check that none are still linked to the source.

### 4. Swap buttons and doc chrome (recipe 4)
- Swap each source button to the destination Button variant from step 2. Keep each button's label and sizing.
- Swap `.header` / `.section` when the keys differ. For partners, always swap them to the partner kit's own versions. If the partner kit has none, make local copies and remove any brand text from them.

### 5. Rebind (recipe 5)
- Rebind fill and stroke styles, text styles per segment, text fills, leftover SO-era variables, raw brand hex values, radius, and spacing.
- Work on component definitions first, then the remaining overrides inside instances.

### 6. Clean up (recipe 6)
- Rename the source abbreviation and prefix to the destination's: "MC Product Row" → "MN Product Row", `.mcProductRowParent` → `.mnProductRowParent`.
- **Component descriptions:** rewrite every one in neutral language, one or two sentences on what the component is and which properties it exposes. No brand names, and no live CSS class names that carry a brand. Empty the descriptions on individual variants.
- **Partners:** run the full scrub from `brands.md` across names, visible text, descriptions and library links. Rewrite or rename every hit. Hits on "FOR" and "SA" may be ordinary words, so check them before changing anything. P4 / Pillar Four is allowed.

### 7. Verify
- Run recipe 7. Remote source components, styles and variables must all be 0. For partners, scrub hits must also be 0. Fonts must be the destination's families only.
- Screenshot the destination frame and compare it with the source screenshot. Look at the whole frame, the component set with every state, and one desktop and one mobile preset.
- Fix clipped labels, overlaps, and anything that is empty or missing, then recheck only that area.
- Re-read the destination components you swapped to. If one changed during the run, say so in the report.

### 8. Report, then apply the answers
Write it in chat, using tables only:

**Done**
| Area | Change |
|---|---|
| Colors | e.g. 37 styles relinked; MC Blue/40 → Dark Blue/50 |
| Type | … |
| Radius / spacing | … |
| Buttons | … |
| Components | e.g. 9 local copies built in `.mnSubcomponents`, 32 instances relinked |
| Names / descriptions | … |
| Partner scrub | 0 hits (partners only) |

**Follow-ups:** one row for each call that wasn't a direct match.
| Choice | Used | Why flagged |
|---|---|---|
| "View Sale" outline button | Tertiary | MN has no outline blue button |

Then ask one question: "Reply with any corrections, and I'll apply them." Apply the answers, re-run recipe 7 and a single screenshot, then report what changed.

## Rules

- Never ask the person to do Figma work you can do. The one exception is pasting the block between files.
- Never change the destination kit's existing styles, variables or components. Only touch the pasted frame and the sub-components you build. If one of the kit's own components is broken, flag it.
- Follow-up answers apply to this run only. Don't save them for future runs.
- Stop at the reskin. Don't start a dev handoff or update the Notion ticket unless asked.
- Keep the output short and in tables. Name what changed and why, with no node IDs and no filler.
- Treat placeholder content ("$X,XXX.XX", "Product Name") as real values.
