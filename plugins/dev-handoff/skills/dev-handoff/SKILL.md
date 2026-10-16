---
name: dev-handoff
description: Generate a complete dev handoff spec from a Figma design and feature context, write it into Figma as doc frames (Requirements, an optional {{SYNTAX}} token reference, and the Dev Spec Handoff), then apply native Dev Mode annotations for the changes between breakpoints. Use whenever someone provides a Figma link with feature context, a brand name, or KPIs and wants a dev-ready ticket — even if they just say "write up the handoff", "create the dev ticket", "build the spec", "document this for dev", or "write the requirements". Also triggers when someone is preparing to hand off a design to engineers and needs functional requirements and a user story documented. Always use this skill for any design-to-engineer handoff work.
---

## What this skill does

Takes a Figma design link, feature/test context, brand, and KPIs — reads the design thoroughly, produces a dev spec, and writes it into Figma as doc frames plus native Dev Mode annotations.

**Engineers are the client.** A handoff is done when an engineer can build the feature without coming back with questions.

**The governing principle: the docs carry only what Dev Mode cannot.** Engineers inspect the design in Figma and get every measurement, colour and type value on click. Duplicating those into a doc frame is redundant, goes stale the moment the design moves, and buries the handful of lines that actually matter. Write less than feels complete.

**Writing style for everything written into Figma** (doc frames and annotations):
- Fragments, not sentences. One line per bullet. No "because", no rationale, no intro sentence under a heading.
- Lead with the thing: `Primary CTA — no focus state`, not `It's worth noting that the primary CTA…`
- Anything with two or more attributes per item is a table row, not a bullet.
- If a line would still be true after deleting it, delete it.

---

## Step 0: Inputs

Ask only for these up front, then read the design before asking anything else:

1. **Figma link(s)** — the dev-ready frame(s), not the exploration file
2. **Audit notes** — "Are there notes from a pre-existing audit to take into consideration?" Audit notes named `Audit · <issue>` on the design's page are found automatically in Step 1, so ask only about notes stored anywhere else.

If the user already gave context, brand or KPIs, keep them. Don't ask for the rest yet.

---

## Step 1: Read the Figma design

Invoke the `figma:figma-use` skill. Read the entire design — every section, component, and state.

`get_metadata` on a large section will blow the token limit. Prefer a read-only `use_figma` script that walks each breakpoint frame and returns a compact digest: frame layout props (`layoutMode`, padding, `itemSpacing`, `layoutWrap`, width/height) down to a depth cap, a **deduplicated type ramp** (group text nodes by size + style + line-height + tracking, keep a few examples each), and every string containing `{{`. Run one call per breakpoint, in parallel.

Then a second pass for: component variant definitions (`componentPropertyDefinitions` from the **COMPONENT_SET**, never a variant COMPONENT), section background fills, divider/line nodes, and per-breakpoint presence counts of key elements.

Don't proceed until you have a thorough view of:

- All sections and layouts at every breakpoint
- All interactive states: hover, click, empty, error, loading — **and which ones have no design at all**
- All variants and conditional displays, plus **which breakpoint each variant switch fires at** (it is often not the breakpoint you'd assume)
- Elements present at one breakpoint and absent at another
- Any annotations or notes already in the file

Verify anything surprising with a targeted screenshot before writing it down. Node data and a visual check disagree often enough to matter.

**Audit notes.** Always search the design's page for nodes of any type (frames, groups, text) named `Audit · …`, plus any notes the user pointed to.

- `Audit · Summary` — its **Not designed** list goes into Card 3's missing states and Known Unknowns; its **Verify in build** list goes into the Dev Spec's build notes.
- `Audit · Rec · …` and `Audit · Recommendations` — research suggestions. Spec them only if the design adopted them.
- Every other `Audit · <issue>` — one finding, drawn as a marker rectangle beside the element it flags.

Notes often sit on a **copy** of the design in a separate audit section, not on the dev-ready frames. Map each marker to the dev-ready frame with the same name (`Mobile` → `Mobile`) by its offset inside the copy:

```js
// top-level notes only: a note's own parts (· note, · target, · line) share the prefix
const notes = page.findAll(n => n.name.startsWith('Audit · ') && !n.parent.name.startsWith('Audit · '));
const marker = n => ('children' in n && n.children.find(c => c.type === 'RECTANGLE')) || n;
// copy = audit-section frame the marker overlaps; dev = dev-ready frame with the same name
const map = (b, copy, dev) => ({ x: dev.absoluteBoundingBox.x + b.x - copy.absoluteBoundingBox.x,
                                 y: dev.absoluteBoundingBox.y + b.y - copy.absoluteBoundingBox.y });
// target = smallest visible node in `dev` whose bounds contain the mapped point
```

Then diff each copy against its dev-ready frame (node count + visible text). If they're identical, no fix is visible yet: say so and ask in Step 1b which findings to treat as resolved.

Carry unresolved findings into Card 3's missing states, the Dev Spec's build notes, or Known Unknowns. Drop the ones the design fixed. Audit notes and audit copies get no annotations.

---

## Step 1b: Ask what the design couldn't answer

Now that you've read the design, ask one `AskUserQuestion` call (max 4 questions) with options drawn from what you saw. Skip anything the user already gave or the design settles.

- **Feature context** — offer your read of what the page/feature is as the first option
- **Brand** — infer from the file when obvious (e.g. Swolverine → SWOL). Internal: AIP, BB, GGR, MC, MN, P4, SO, SA, SWOL. Partner: AARP, AUD, FOR, EAR, MA, MG, NCOA.
- **Primary KPI** — options by feature type: comparison tools → Take Rate · CTAs, product blocks, landing pages → Conversion · navigation, filtering → Engagement · trust signals, reviews → Conversion · lead-gen forms → Form Conversion Rate
- **Breakpoint intent** — for any frame that isn't obviously a breakpoint (odd widths, misnamed frames, stand-alone component frames): real breakpoint, reference only, or exploration
- **Scope** — shared components the design contains (header, footer, nav, overridden global bands): in or out. Out-of-scope components get no spec and no annotations, anywhere in this skill.
- **Dev build status** — for each component: existing dev build or new dev build, when the file doesn't make it clear
- **Design ambiguities** — anything the read left unclear

If the user skips a question or says to move on, infer and tag it `[Inferred]`. Never leave User Story or Business Impact blank.

---

## Step 2: Draft the Requirements

The Requirements frame is a **short reference doc, not a description of the design**.

**The filter: if looking at the design gives it, cut it.** Cut at the section level, not line by line.

**Do NOT write:**
- **Per-section / per-component walkthroughs.** No "S1 Hero", "S2 Stats" behaviour sections. This is the single biggest source of bloat and the first thing reviewers delete.
- **A standalone Accessibility section.** Missing focus/pressed states go in Card 3 and Known Unknowns; heading semantics go in the Dev Spec's build notes.
- **Measurement tables** — global layout grids, type ramps, padding/gap/width tables, image dimensions, colour values.
- Anything an engineer gets by clicking one node.

**Three cards, with hard caps.** Known Unknowns live once, in the Dev Spec (Step 3), not here.

**1 · Scope & Breakpoints** (≤ 6 lines + section key)
- One line per breakpoint: `Mobile 0–767 · baseline`, `Desktop 1024+`, `1440 · reference only, don't build`
- `Out of scope:` one line
- Section key on one line: `S1 Hero · S2 Stats · S3 …`

**2 · Cross-Breakpoint Rules** (≤ 5 bullets). Only synthesis an engineer can't get from one node. Write them like this:
- `Tablet is layout-only — no type changes at 768`
- `Only 2 type changes on the page, both at 1024`
- `S1 is the one section whose padding doesn't step up`

**3 · Components & States** (table + ≤ 5 bullets)
- Table: `Component | Figma | Dev | Count | Variants used`
  - Figma: `Existing component` or `New design (not a component)`
  - Dev: `Existing dev build` or `New dev build`; `[Confirm]` if the user didn't say
- Bullets: missing states only — `No focus-visible on Primary CTA`, `No loading/error state for form`. Each one also goes in Known Unknowns.

**Callouts:** at most one per card, one line. Amber `EDGE CASE`, green `CONFIRMED`, blue `INTERACTION`.

### Data source

**SWOL** sells its own products on **Shopify**. Map product fields to Shopify (`product.title`, `variant.price`, metafields…); GPV never applies. Flag fields with no Shopify source as `[Need to make field]`.

**Affiliate products** come from GPV:

- Use site-specific GPV attributes before falling back to global
- Flag any UI field with no current GPV equivalent: `[Need to make field]`
- Format mappings clearly, e.g.: `Customer Score → Customer Rating` or `Side Sleeper Score (Under 130 lbs) → [Need to make field]`

**If the design shows no product data** — a location page, lead-gen landing page, or form flow — skip product mapping and give the data contract for whatever drives the content (Step 2b).

---

## Step 2b: Draft the {{SYNTAX}} token reference (when applicable)

**Trigger:** the design uses `{{TOKEN}}` placeholders, or the user asks for a separate list of the `{{SYNTAX}}` callouts. Templated surfaces — location pages, clinic pages, programmatic landing pages — always hit this.

Give tokens their **own frame**. Don't bury them in Requirements: this is the data contract engineers keep open beside their editor.

**Table 1 — Tokens in the design.** Number, token, instance count, where it appears (by section key), notes. Notes carry what bites:
- Format constraints the design assumes — "drawn as a single line; constrain upstream or let the row grow"
- Tokens that look like one field but are two — `{{STATE}}` full name vs `{{STATE_ABBR}}`
- Mixed styling inside one text node — a `tel:` link plus an unlinked parenthetical
- Whether the value is a link target

Confirm counts across every breakpoint frame and state whether they match. A token present at one breakpoint and not another is a finding.

**Table 2 — Tokens that need to exist but don't.** Usually the highest-value table in the whole handoff. Hunt for:
- **Repeated components sharing one token set.** If three cards all render `{{ADDRESS}}`, the design cannot be built as drawn — it needs indexed fields (`{{NEARBY_1_ADDRESS}}`…). This is a blocker, not a nit.
- **CTAs with no destination token**
- **Image slots with no source or alt binding**
- **Embeds** (maps, forms, video) with no ID or data binding

Mirror every one of these into Known Unknowns.

---

## Step 3: Draft the Dev Spec Handoff

The Notion ticket source. Every line is a fragment an engineer can act on; no sentence explains why. Use this template exactly — headings in this order, nothing added:

---

### User Story
As a [user], I want to [action] so that [outcome].
**Workaround:** [N, or Y — ≤ 10 words]

### Functional Requirements
**Scope**
- In: [one line]
- Out: [already-built components]
- Visual specs: Dev Mode

**Data**
- One line per field: `UI field → Shopify field`, `GPV attribute` or `{{TOKEN}}`, gaps as `[Need to make field]`

**Build notes** (≤ 8 bullets, one line each — only what applies)
Look for: DOM order where columns flip · behaviour that persists where you'd expect it to stop · variant switches and their breakpoint · spacing exceptions · elements at only some breakpoints · focus/ARIA where the library has no state · heading levels that don't match visual size.

### Business Impact
[One line] · **Primary:** [KPI] · **Secondary:** [KPIs]

### Design
- File: [dev-ready link]

### Known Unknowns
One line each — every blocker, design gap, missing state, placeholder copy, and compliance gap (e.g. an asterisk with no footnote). If none: `None at handoff.`

### Related Tickets
Design: · QA: · Release:

---

## Step 4: Run the clean handoff checklist

Fix any failure before showing the user.

- [ ] User story is from the end user's POV; business impact is one line with primary + secondary KPIs
- [ ] Design link is the dev-ready frame; every affected page is named (no "and similar")
- [ ] Figma and dev build status stated for every component; already-built components named as out of scope
- [ ] Every data field mapped (Shopify, GPV or `{{TOKEN}}`) or flagged `[Need to make field]`; repeated components have per-instance bindings
- [ ] Every interactive state (error, empty, loading, focus) is designed or a Known Unknown
- [ ] Placeholder copy flagged in Known Unknowns
- [ ] Release dependencies linked or marked TBD
- [ ] Every frame passes the length limits in Step 2 and Step 3

---

## Step 5: Present for confirmation

Show every drafted frame to the user. Ask for feedback before writing anything to Figma.

If approved with no changes, proceed. If changes are requested, revise and confirm again before touching Figma.

When a reviewer cuts a section, **apply the principle behind the cut, not just the literal cut.** "These are obvious from the designs" means every comparable section goes too — including ones they didn't name. Say what you extended and why so they can reverse it.

---

## Step 6: Write to Figma

Invoke `figma:figma-use`. Before creating anything:
- Confirm you have the correct **dev-specific** Figma link and page (not the exploration file)
- If unsure which page to write to, ask the user before proceeding
- Scan the page for the rightmost existing frame. Place new frames starting at that x position + 120px gap.

> ### CRITICAL — set the page before appending
>
> `use_figma` resets `figma.currentPage` to the document's **first page** at the start of every call. `getNodeByIdAsync` resolves nodes across pages, so *reading* the design works fine and gives no warning — but `figma.currentPage.appendChild(frame)` then silently drops your frames on the wrong page (usually "Cover"). The frames are created successfully and the script returns clean; nothing looks wrong until the user says they can't find them.
>
> ```js
> // resolve the design's page by walking up from the design section
> let page = await figma.getNodeByIdAsync(SECTION_ID);
> while (page && page.type !== 'PAGE') page = page.parent;
> await figma.setCurrentPageAsync(page);
> // ...create frames, then:
> page.appendChild(frame);
> ```
>
> `setCurrentPageAsync` may be called **at most once per `use_figma` call**. After the final write, verify each frame's page by walking its parent chain — do not assume.

Create frames in this order, left to right, with the content from Steps 2, 2b and 3:

1. `Requirements & Edge Cases`
2. `Dynamic Content · {{SYNTAX}} Reference` — only when the design uses tokens. Subtitle: token count, instance count, whether counts match across breakpoints.
3. `Dev Spec Handoff` — what the user copies into the Notion ticket.

Build incrementally — one `use_figma` call per frame, or per few cards for long frames — and screenshot to verify before moving on.

---

### Frame styling — apply to all frames

All frames share this visual system. Match it exactly.

**Outer frame**
- Background: `#FFFFFF`
- Width: `1400`px, height: auto (hug contents)
- Auto-layout: vertical, padding `64`px all sides, gap `48`px
- No corner radius, no stroke

**Document header**
- Title: Inter Bold, 28px, color `#1B3A6B`
- Subtitle (brand + date, e.g., "SO Comparison Widget Tool · May 2026"): Inter Regular, 13px, color `#9CA3AF`
- Gap between title and subtitle: `6`px
- Optional one-line scope note below, in body style

**Section card**
- Background: `#FFFFFF`
- Border: `1`px solid `#E5E7EB`
- Corner radius: `8`px
- Padding: `32`px all sides
- Auto-layout: vertical, gap `20`px
- Width: fill container

**Section title**
- Inter Semi Bold, 17px, color `#1D5C5C`

**Sub-header label** (e.g., SCOPE, DATA CONNECTIONS, CTA TIERS)
- Inter Semi Bold, 10px, UPPERCASE, letter-spacing `1.5`px, color `#9CA3AF`

**Body text / bullet items**
- Inter Regular, 14px, color `#374151`

**Flagged gap text** (`[Need to make field]` lines)
- Inter Regular, 14px, color `#B91C1C`

**Edge case callout box**
- Background: `#FFF8F0`
- Left border: `3`px solid `#F59E0B`
- Padding: `16`px
- Label "EDGE CASE": Inter Semi Bold, 10px, uppercase, letter-spacing `1.5`px, color `#D97706`
- Body text: color `#92400E`

**Confirmed/decision callout box**
- Background: `#F0FDF4`
- Left border: `3`px solid `#22C55E`
- Padding: `16`px
- Label "CONFIRMED": Inter Semi Bold, 10px, uppercase, letter-spacing `1.5`px, color `#16A34A`
- Body text: color `#166534`

**Interaction callout box**
- Background: `#EFF6FF`
- Left border: `3`px solid `#3B82F6`
- Padding: `16`px
- Label "INTERACTION": Inter Semi Bold, 10px, uppercase, letter-spacing `1.5`px, color `#2563EB`
- Body text: color `#1E40AF`

**Build notes**
- Inter styles are `"Semi Bold"` and `"Extra Bold"` — not `"SemiBold"`. Load every style with `loadFontAsync` before setting characters.
- Tables: a vertical auto-layout of horizontal rows; cells are TEXT with `textAutoResize = 'HEIGHT'` and a fixed width, set to `layoutSizingHorizontal = 'FIXED'` after append. Column widths plus gaps must equal the card's inner width (1400 − 128 outer − 64 card = **1208**).
- Row separators: `strokeTopWeight = 1` in `#F3F4F6` with the other three weights at 0.
- Left-border callouts: `strokeLeftWeight = 3`, other weights 0, `strokeAlign = 'INSIDE'`.

---

## Step 7: Confirm annotation scope

Annotate only the breakpoint frames the user names.

**If the user has already told you which frames** — in the original brief, or by naming which breakpoints exist and which are reference-only — **do not ask again.** Re-asking a settled question is noise. Say what you're about to annotate and proceed.

Ask only when scope is genuinely unresolved:

> **"The doc frames are in Figma. Which breakpoint frames should I annotate?"**

Also confirm what is **out of scope inside** those frames. Already-built shared components (header, footer, nav) get no annotations even though they sit within the frame. Verify this after writing by walking each annotated node's parent chain for those component names.

If the user provides frame names, use `get_metadata` or `use_figma` to resolve them to node IDs before continuing.

---

## Step 8: Resolve annotation categories

`Development` and `Content` are Figma's built-in annotation categories — do not create them. Just fetch and use their IDs.

```js
const cats = await figma.annotations.getAnnotationCategoriesAsync();
const DEV = cats.find(c => c.label === 'Development').id;
const CONTENT = cats.find(c => c.label === 'Content').id;
```

**Category rules:**
- `Development` — spacing: padding, gap, itemSpacing, width, column count, column gap, layout mode shifts
- `Content` — typography: font size, font weight, font family, line height, letter spacing

---

## Step 9: Apply native annotations

### Annotate changes only — the baseline frame gets nothing

**The mobile (baseline) frame receives ZERO annotations.** Mobile is what engineers build from first, and they read every one of its values in Dev Mode. Annotating it restates what is already on screen.

Annotate **only genuine visual or font changes** at each larger breakpoint, relative to the breakpoint below it. Reference-only frames (max-width) also get zero.

**Annotate:**
- Layout-mode changes — stacked → columns, column-count shifts, wrap-count changes
- Order changes — columns flipping left/right between breakpoints
- Elements that appear or disappear at a breakpoint
- Component variant switches, and the breakpoint they fire at
- Spacing-scale steps that apply broadly (section padding, sub-block gap)
- Font-size changes
- Behaviour changes — scroll/carousel turning on or off

**Do NOT annotate:**
- **Unchanged values.** Drop the "same as mobile, increases at desktop" pattern entirely. If nothing changed, say nothing.
- **Derived measurements** that follow automatically from a parent layout change — column widths, image dimensions, row heights that shrink because text stopped wrapping. Dev Mode gives these on click, and the parent annotation already explains why they moved.
- Anything inside an out-of-scope shared component.

**One annotation per rule, not per node.** If every section's padding steps 48 → 80, annotate the first section with `All sections: padding 80 (was 48)` and leave the rest alone.

No count target. Annotate every real change between breakpoints and nothing else.

**Where a counterintuitive NON-change matters** — a carousel that stays in scroll mode at tablet, a section that doesn't step its padding — put it in the Dev Spec's build notes, not in an annotation. It stays documented, and the annotation layer stays a pure change log.

Run **one `use_figma` call per breakpoint** so page context stays clean.

### Helper function

```js
async function annotate(id, label, properties, categoryId) {
  const node = await figma.getNodeByIdAsync(id);
  if (!node) return;
  node.annotations = [{ label, properties: properties.map(p => ({ type: p })), categoryId }];
}
```

### Property type rules — strictly enforced

**FRAME / INSTANCE nodes** — layout properties only:
`padding`, `itemSpacing`, `width`, `height`, `gridColumnCount`, `gridColumnGap`, `gridRowCount`, `gridRowGap`, `layoutMode`, `cornerRadius`, `fills`, `strokes`

**TEXT nodes** — text properties only:
`fontSize`, `fontWeight`, `fontFamily`, `fontStyle`, `lineHeight`, `letterSpacing`, `textAlignHorizontal`, `textStyleId`

**LINE nodes** accept `strokes`.

Mixing the wrong property type for a node type throws `"Invalid property X for a FRAME node"`. When in doubt, use `width` for frames — it always works.

### Label format

The pinned properties already show the current value in Dev Mode, so the label says only what changed. Under ~50 characters, no full stop.

```
[change] (was [previous])
```

- `48px (was 32)`
- `2 columns, gap 48 (was stacked)`
- `Order flips: image right`
- `New at 768: divider`
- `Carousel off (was scrolling)`

> **Never use straight double quotes (`"`) in a label.** The annotation API HTML-escapes them and stores the literal string `&quot;` — which is exactly what engineers then read in Dev Mode. Rewrite the phrase without quotes, or use curly quotes.

### Clearing stale annotations

When re-annotating, clear the whole frame rather than a hand-listed set:

```js
for (const fid of FRAME_IDS) {
  const r = await figma.getNodeByIdAsync(fid);
  for (const n of r.findAll(x => x.annotations && x.annotations.length > 0)) n.annotations = [];
}
// findAll can miss nested instance children — clear those by id too
for (const id of NESTED_INSTANCE_IDS) {
  const n = await figma.getNodeByIdAsync(id);
  if (n && n.annotations && n.annotations.length) n.annotations = [];
}
```

**Important API rules:**
- `node.annotations` is a `ReadonlyArray` — always assign a full new array, never push
- Each annotation object: `{ label, labelMarkdown?, properties?, categoryId? }`
- Categories are file-scoped — always check for existing ones before creating (Step 8 handles this)
- Annotations appear in **Dev Mode only** — not visible in Edit mode or screenshots, so verify via the API, never visually
- `findAll` on a frame can **miss annotated TEXT nodes nested inside component instances** (ids shaped `I123:456;789:012`). Sweep counts under-report; verify those ids individually before reporting a discrepancy as a failure.

---

## Step 10: Verify annotations

Sweep every frame, then spot-check the nested-instance ids directly:

```js
// category ids differ per file — run Step 8's lookup at the top of this call
const CAT = { [DEV]: 'Development', [CONTENT]: 'Content' };
const out = {};
for (const k in FRAMES) {
  const r = await figma.getNodeByIdAsync(FRAMES[k]);
  const hits = r.findAll(n => n.annotations && n.annotations.length > 0);
  out[k] = hits.map(n => ({
    id: n.id,
    name: n.name,
    count: n.annotations.length,
    cat: CAT[n.annotations[0].categoryId] || 'NONE',
    label: n.annotations[0].label.slice(0, 60),
    escaped: /&(quot|amp|lt|gt|#\d+);/.test(n.annotations[0].label)
  }));
}
return out;
```

**Checklist before finishing:**
- [ ] The mobile/baseline frame has **zero** annotations
- [ ] Reference-only frames (max-width) have **zero** annotations
- [ ] No annotated node sits inside an out-of-scope shared component — verified by walking parent chains
- [ ] All target nodes have exactly one annotation
- [ ] Layout-change nodes are `Development`; font-change nodes are `Content`
- [ ] No label contains `&quot;`, `&amp;`, `&lt;`, `&gt;` or a numeric entity
- [ ] Nested-instance text nodes verified individually, not via `findAll`
- [ ] Every label describes a change — none says "same as" or "unchanged"
- [ ] Doc frames confirmed to be on the **design's page**, not the document's first page

Report counts per frame. If a sweep count disagrees with what you applied, resolve it with a per-node check before telling the user anything failed.
