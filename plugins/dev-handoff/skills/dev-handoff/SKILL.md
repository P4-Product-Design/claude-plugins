---
name: dev-handoff
description: Generate a complete dev handoff spec from a Figma design and feature context, write it into Figma as doc frames (Requirements, an optional {{SYNTAX}} token reference, and the Dev Spec Handoff), then apply native Dev Mode annotations for the changes between breakpoints. Use whenever someone provides a Figma link with feature context, a brand name, or KPIs and wants a dev-ready ticket — even if they just say "write up the handoff", "create the dev ticket", "build the spec", "document this for dev", or "write the requirements". Also triggers when someone is preparing to hand off a design to engineers and needs functional requirements and a user story documented. Always use this skill for any design-to-engineer handoff work.
---

## What this skill does

Takes a Figma design link, feature/test context, brand, and KPIs — reads the design thoroughly, produces a dev spec, and writes it into Figma as doc frames plus native Dev Mode annotations.

**Engineers are the client.** A handoff is done when an engineer can build the feature without coming back with questions.

**The governing principle: the docs carry only what Dev Mode cannot.** Engineers inspect the design in Figma and get every measurement, colour and type value on click. Duplicating those into a doc frame is redundant, goes stale the moment the design moves, and buries the handful of lines that actually matter. Write less than feels complete.

---

## Step 0: If no context was provided

If the skill was invoked without any inputs, respond with this prompt before doing anything else:

> **To get started, grab the following:**
>
> 1. **Figma link(s)** — link(s) to the dev-ready frame(s). Not the exploration file.
> 2. **Feature/test context** — a plain-language description of what this is and how it works. Include what triggers it, what the user sees, and what they can do.
> 3. **Brand** — which brand is this for?
>    - Internal: AIP, BB, GGR, MC, MN, P4, SO, SA, SWOL
>    - Partner: AARP, AUD, FOR, EAR, MA, MG, NCOA
> 4. **KPIs** — why does this feature matter? What are we measuring?
>    - One line on the business rationale
>    - Primary KPI (Take Rate, Conversion, RPV, etc.)
>    - Secondary KPIs (Rev/Visit, Engagement, etc.)
>
> Drop all of the above and I'll take it from there.

Once inputs are provided, continue to Step 1.

---

## Inputs

Collect any of these that weren't provided upfront. Use `AskUserQuestion` for anything missing before proceeding.

- **Figma link** — link to the dev-ready frame (not the exploration file)
- **Feature/test context** — what this is and how it works
- **Brand** — internal (AIP, BB, GGR, MC, MN, P4, SO, SA, SWOL) or partner (AARP, AUD, FOR, EAR, MA, MG, NCOA)
- **KPIs** — one line on why this matters + primary KPI (Take Rate, Conversion, RPV, etc.) + secondary KPIs
- **What's already built** — shared components (header, footer, nav) that exist and are out of scope. Ask if the design obviously contains them and the user hasn't said. Out-of-scope components get **no spec and no annotations**, even though they sit inside the breakpoint frames.
- **Breakpoint intent** — which frames are real breakpoints and which are reference only (a max-width frame showing container caps is not a breakpoint). Getting this wrong produces a whole frame of pointless annotations.

**Context example:**
> "On-page comparison tool that opens in a bottom drawer. Users can select a mattress to compare from the drawer or by clicking 'compare' within a product block. Once ready, they hit compare and an on-page modal opens showing each mattress with: dropdown, image, title, customer score, CTA, best-for tags, mattress details, sleeper type scores, overall score, and individual performance scores."

### Handling missing user story or business context

If the user hasn't provided a user story, business rationale, or KPIs — don't block on it or leave those fields blank. Work through this order:

**1. Ask a scoping question first.** Before drafting, use `AskUserQuestion` to ask one targeted question that surfaces the business context. Keep it focused — one question, not a form.

Good prompts to pull out business context:
- "What's the primary goal of this feature — is this primarily a conversion play, an engagement improvement, or something else?"
- "Is there a hypothesis or test goal behind this? What would make this a win?"
- "Who's the main user this helps, and what problem does it solve for them?"

Bundle genuine design ambiguities into the same call (max 4 questions) rather than asking twice — e.g. a component whose internal breakpoints don't match the page's, or a data source that isn't settled.

**2. If no answer is given or the user says to move forward,** use the Figma design and feature context to infer reasonable values. Apply judgment:
- The user story should reflect the actual end user's action and goal (not the team's goal)
- Business impact should map to the closest plausible KPI for the feature type:
  - Comparison tools → Take Rate, RPV
  - CTAs, product blocks → Conversion, Click Rate
  - Navigation, filtering → Engagement, Time on Page
  - Trust signals, reviews → Conversion, Bounce Rate
  - Lead-gen / form landing pages → Form Conversion Rate, Call Rate
- Mark any inferred values clearly: `[Inferred — confirm before shipping]`

**3. Never leave User Story or Business Impact blank in the spec.** A placeholder is worse than a reasonable inference — engineers need something to work from. If you're inferring, say so.

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

If anything is ambiguous after reading, ask follow-up questions using `AskUserQuestion` before drafting. It's better to ask now than to produce a spec with gaps.

---

## Step 2: Draft the Requirements

The Requirements frame is a **short reference doc, not a description of the design**.

**The filter: if looking at the design gives it, cut it.** Cut at the section level, not line by line.

**Do NOT write:**
- **Per-section / per-component walkthroughs.** No "S1 Hero", "S2 Stats" behaviour sections. This is the single biggest source of bloat and the first thing reviewers delete.
- **A standalone Accessibility section.** Fold the genuinely non-derivable a11y gaps into the surviving cards instead: missing focus/pressed variants go in the component inventory and Known Unknowns; heading-semantics instructions go in the Dev Spec's technical requirements.
- **Measurement tables** — global layout grids, type ramps, padding/gap/width tables, image dimensions, colour values.
- Anything an engineer gets by clicking one node.

**Target: four cards.**

**1 · Scope & Breakpoint System.** Breakpoint ranges and what each frame is for. Flag any reference-only frame (max-width) so nobody builds or annotates from it. State what is out of scope. Include a short section key (S1…Sn) the other frames reference.

**2 · Cross-Breakpoint Rules.** Only the *synthesis* an engineer can't get from one node. These are the highest-value lines in the document:
- "Tablet is a pure layout breakpoint — nothing in the type ramp changes at 768."
- "There are exactly two type changes on the page and both fire at 1024."
- "The hero is the one section that doesn't step its vertical padding up."
- "Gutters live at two levels — full-bleed sections put the gutter on the inner container, boxed sections on the section itself."

**3 · Component & CTA Inventory.** CTA tiers with instance counts, the width/placement rule and its exceptions, and **what variants exist in the component library vs. what the design actually uses**. Missing states — no focus-visible, no pressed, no loading/success/error — belong here as edge cases. A gap where no design exists is exactly what Dev Mode cannot show.

**4 · Known Unknowns.** Unknown + owner + needed-by. Everything blocking the build, all placeholder copy (lorem ipsum, "Customer Name", unresolved link text), every design gap, every compliance gap (an asterisk with no footnote).

**Callout boxes still apply** — amber `EDGE CASE`, green `CONFIRMED`, blue `INTERACTION` — used inside the four cards, not as a fifth section.

### GPV field mapping (for features involving affiliate products)

GPV (Global Product Vault) is the universal product data system. It stores every affiliate product — mattresses, sleep accessories, fitness equipment, supplements, fitness accessories — organized by category (sleep, fitness, aging). It connects to all brand sites: engineers select a product ID and GPV populates the fields automatically.

When a feature displays affiliate product data, map each Figma UI field to its GPV attribute:

- Use site-specific GPV attributes before falling back to global
- Flag any UI field with no current GPV equivalent: `[Need to make field]`
- Format mappings clearly, e.g.: `Customer Score → Customer Rating` or `Side Sleeper Score (Under 130 lbs) → [Need to make field]`

**If the design is not an affiliate-product surface** — a location page, lead-gen landing page, or form flow — GPV does not apply. Say so in one line rather than forcing a mapping, then produce the equivalent data contract for whatever does drive the content (Step 2b).

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

Mirror every one of these into Known Unknowns with an owner.

---

## Step 3: Draft the Dev Spec Handoff

This is the engineer's Notion ticket source of truth. Keep it scannable. Focus only on what the engineer needs to configure and connect.

Use this template exactly:

---

### User Story
As a [user type], I want to [action] so that [outcome].

**Workaround available? (Y/N)**
[Y or N, plus brief note if yes]

### Functional Requirements
[Three labelled groups:

**Scope** — what's in, what's out (already-built components), and a line pointing engineers to Dev Mode for all visual specs.

**Data connections** — GPV mappings, or `{{TOKEN}}` bindings for templated pages. Flag gaps as `[Need to make field]`.

**Non-obvious technical requirements** — the things that cost hours if guessed:
- DOM-order requirements where column order flips between breakpoints
- Behaviour that persists at a breakpoint you'd expect it to stop (a carousel still overflowing at tablet)
- Variant switches and the exact breakpoint they fire at
- Spacing exceptions (one section that doesn't follow the scale)
- Elements present at only some breakpoints
- Content-driven heights where text wraps at smaller widths
- Focus indicators and ARIA requirements where the library has no state for them
- Semantic heading levels where visual size doesn't imply hierarchy

Do NOT include visual requirements here — engineers see those directly in Figma.]

### Business Impact / Value
[One line on why this matters]

**Primary KPI:** [Take Rate, Conversion, RPV, etc.]
**Secondary KPIs:** [Rev/Visit, Engagement, etc.]

### Design
- Design file: [link to dev-ready frame]
- Frames: [each breakpoint frame with node id; mark reference-only frames]
- Related design ticket: [link if known]

### Known Unknowns
[Unknown + who owns resolving it + date needed by]
[If none: "None at time of handoff."]

### Related Tickets
- Design:
- QA:
- Release:

---

## Step 4: Run the clean handoff checklist

Before showing anything to the user, check every item. If any item fails, fix it first.

**Structure**
- [ ] User story is written from the user's POV, not the stakeholder's
- [ ] Functional requirements cover data connections and non-obvious technical constraints only
- [ ] Requirements frame is four cards — no per-section walkthroughs, no standalone accessibility section, no measurement tables
- [ ] Every interactive state is either defined or listed as a Known Unknown with an owner
- [ ] Business impact stated in one line
- [ ] KPIs listed (primary + secondary)
- [ ] Design link points to the dev-ready frame, not the exploration file

**Content**
- [ ] Every affiliate product field mapped to GPV (or flagged `[Need to make field]`) — or, for non-affiliate surfaces, every `{{TOKEN}}` mapped in the token frame
- [ ] Repeated components verified to have per-instance data bindings, not one shared token set
- [ ] Every data dependency named
- [ ] Every affected page enumerated — no "and similar pages" language
- [ ] All copy is final, or flagged with an owner and date — placeholder copy (lorem ipsum, "Customer Name") called out explicitly
- [ ] Known unknowns called out with an owner and a resolution date

**Fit with existing build**
- [ ] New blocks or components explicitly flagged (don't assume WP block library match)
- [ ] Already-built components named as out of scope
- [ ] Responsive behaviour lives in annotations, not prose
- [ ] Accessibility gaps with no design (focus states, missing ARIA patterns) are in Known Unknowns

**Common engineer questions — all must be answerable before sending**
- "Where does this live?" → dev-ready Figma frame is linked
- "What's the WP/CMS setup?" → editable fields and data connections covered
- "Is this a new block or existing?" → stated explicitly
- "What happens on error / empty / loading?" → defined, or flagged as undesigned
- "Is the copy final?" → yes, or flagged with owner and date
- "Which pages exactly?" → enumerated, no "and similar"
- "What pulls from GPV / what fills the tokens?" → all fields mapped or flagged
- "What's the responsive behavior?" → annotated on the changed breakpoints
- "Any accessibility constraint?" → stated where no design exists
- "What's the release dependency?" → related tickets linked or noted as TBD

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

Create frames in this order: Requirements → {{SYNTAX}} Reference (if applicable) → Dev Spec Handoff.

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

### Frame 1: Requirements & Edge Cases
- Document header title: `Requirements & Edge Cases`
- One-line scope note: what's out of scope, and that visual specs live in Dev Mode annotations
- Four cards: Scope & Breakpoint System → Cross-Breakpoint Rules → Component & CTA Inventory → Known Unknowns
- Edge cases in amber callouts, confirmed decisions in green, behaviour in blue
- GPV mappings where applicable (green = existing field, red = `[Need to make field]`)

---

### Frame 2: Dynamic Content · {{SYNTAX}} Reference *(only when the design uses tokens)*
- Document header title: `Dynamic Content · {{SYNTAX}} Reference`
- Subtitle line with total token count, total instances, and whether counts match across breakpoints
- Two cards: Tokens in the design → Tokens that need to exist but don't
- An amber callout naming the single biggest data blocker

---

### Frame 3: Dev Spec Handoff
- Document header title: `Dev Spec Handoff`
- The completed spec template: User Story → Functional Requirements → Business Impact → Design → Known Unknowns → Related Tickets
- This is what the user copies into the Notion dev ticket

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

Expect roughly **10–15 annotations per changed breakpoint**. If a frame is over that, you are restating the design.

**Where a counterintuitive NON-change matters** — a carousel that stays in scroll mode at tablet, a section that doesn't step its padding — put it in the Dev Spec's non-obvious technical requirements, not in an annotation. It stays documented, and the annotation layer stays a pure change log.

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

```
[Current value] — [what changed from the breakpoint below]
```

Examples:
- `48px / Libre Baskerville Bold (↑ from 32px at mobile and tablet).`
- `2-column, gap 48px — was a single stacked column at mobile.`
- `Column order FLIPS: checklist left / image right. Tablet has the image on the left.`
- `Divider: 2px #F3F4F6, full column height. New at 768 — no dividers exist in the mobile frame.`

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
const CAT = { '428:0': 'Development', '428:3': 'Content' };
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
