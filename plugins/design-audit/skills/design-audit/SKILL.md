---
name: design-audit
description: Judges whether a new Figma design is the best it can be for its context. Covers PDPs, collection pages, homepages, quiz results, partner co-branded pages, long-form content pages, affiliate reviews and best-of roundups, comparison pages, landing pages (paid social, paid search / PMax, email, lead-gen / quiz), and product blocks. Benchmarks the design against best practices for its traffic source and against UX laws, then returns a short, scannable list of issues grounded in how users will actually behave on the page. Use when someone shares a Figma design and asks to "audit this design", "review this landing page", "is this the best it can be", "QA this before handoff", "check this product block", "review this PDP", or "is this ready for dev". For auditing a live page or email to plan a redesign, use redesign-audit. For writing the dev spec, use dev-handoff.
---

# Design Audit

Answers one question: **is this the best design for its context, and is it ready to build?**

| Skill | Question | Input | When |
|---|---|---|---|
| redesign-audit | What's wrong with what's live? | Live page, email, or current design | Before a redesign |
| **design-audit** | Is this new design the best it can be? | New Figma design | After design, before handoff |
| dev-handoff | Can dev build it without questions? | Approved Figma design | Handoff |

**The bar:** the best practices for this design type and traffic source (`references/playbooks.md`), plus UX laws (`references/ux-laws.md`). A finding is any gap between the design and that bar. Don't just critique how the design was executed.

**User behavior first:** 90% of findings must describe how a real user will behave on the page: what they'll miss, hesitate on, mis-tap, misread, or leave over. Design-system hygiene (tokens, layer names, component structure) gets at most two lines, under Build notes.

## Output rules

- Use the tables in Step 6. No paragraphs.
- **Issue:** 8 words max. **Why:** 10 words max, naming the user behavior. Add the UX law when it adds weight.
- No filler, intro, recap, praise, or methodology.
- No fixes unless asked. The one exception is **Recommendations from research** (Step 6).
- Never show check names or IDs.
- Treat placeholder content as real: "X,XXX reviews" is a number, "$XX.XX" is a price, "Product Name" is a name. Never flag placeholder copy.
- Report gaps only. Skip anything that already meets the bar.
- If something can't be confirmed from a static design, list it under **Verify in build**. Don't guess.
- Chat first. Once the user has reviewed the chat output, write the notes to Figma (Step 7).

## Step 0 — Look, then ask

Take one `get_screenshot` of the linked node first, so your questions can name real frames and sections. Then use AskUserQuestion only for what's still missing:

- **Brand**, if it isn't visible in the design
- **Design type:** PDP · collection / category page · homepage · long-form content page · affiliate review / best-of roundup · comparison page · quiz results page · partner co-branded page · landing page (and traffic source: paid social, paid search / PMax, email, lead-gen / quiz) · product block
- **Audience**, if it skews 50+ (loads the older-adults modifier)
- **Primary action**, and the KPI if known
- **Breakpoints:** which frames are real breakpoints and which are reference only
- **Out of scope:** already-built components (header, footer, nav). Still check *which version* the page uses (e.g. full nav on a paid landing page), but not the component's internals.
- **Landing pages:** the ad or email creative, if available

These match dev-handoff's intake. If dev-handoff runs next, reuse the answers.

## Step 1 — Set the bar

- From `references/playbooks.md`, load the design-type playbook, **Trust factors** (always), and **Older adults** if the audience skews 50+. Load all of `references/ux-laws.md`.
- If the context isn't covered (a new platform, vertical, or format), run 2–3 web searches for current best practices. Prefer Baymard, NN/g, and platform docs (Meta, Google Ads).
- For paid social, judge mobile first.

## Step 2 — Read the design

- Invoke `figma:figma-use` before any `use_figma` call.
- For each breakpoint (in parallel), run a read-only `use_figma` script that returns all text, a deduplicated type ramp, and contrast against the nearest solid background. Don't call `get_metadata` on large sections.
- Second pass: component variant definitions (from the COMPONENT_SET), interactive element sizes, and media fills (image or video).
- Mark contrast for text over photos or video as "estimated."
- Take section screenshots to see what the user actually sees.

## Step 3 — Coverage map

List every section or component × breakpoint × state: default, hover, focus, selected, loading, added/success, error, missing data, and content extremes. Any state with no design goes under **Not designed**.

## Step 4 — Walk the page as the user

Run `references/checks.md` in order: land → understand → trust → act → keep moving → everyone → real-world states. Skip checks whose **Applies** doesn't match the design type.

Then compare the design against every item in the loaded playbooks. Anything recommended there that is **absent** from the design becomes a recommendation, unless a finding already covers it.

## Step 5 — Score

Assign severity and effort per `references/scoring.md`, then sort into priority groups.

## Step 6 — Output

```
**[Design name] — [n] issues** (Critical x · High x · Medium x · Low x)

**Do first**
| Sev | Where | Issue | Why |
|---|---|---|---|
| High | Product card | Flavor picker 34px tall | Fitts's law: mis-taps stall add to cart |

**Plan next**
(same table)

**Fill-ins**
(same table)

**Backlog**
(same table)

**Recommendations from research**
| Recommendation | Why | Source |
|---|---|---|
| Add gallery zoom and full-screen view | Images are the first stop; detail builds confidence | Baymard |

**Not designed**
- Add to cart: loading, added, error

**Verify in build**
- Carousels: keyboard operation

**Not checked**
- Ad message match: no ad creative provided

**Build notes**
- (max 2 lines; hygiene only)
```

Leave out empty groups. Stop after the list, then wait for the user to review before Step 7.

## Step 7 — Write notes to Figma

Run this after the user reviews the chat output, or when they ask for notes in Figma. Never edit the design frames themselves.

- **Which breakpoint:** put notes on the mobile frame. Add notes to the desktop frame only for issues that differ from mobile (desktop-only layout, line length, empty columns). If there's no mobile frame, put every note on desktop.
- **Where:** a column of notes in the empty space to the right of each annotated frame, inside the same section, 30px from the frame. If the section is too narrow for the column, widen the section (`resizeWithoutConstraints`). Never move the frames. Each note sits at the height of its issue. Notes stack downward without overlapping, and a note drops below any element that sticks out into the column.
- **One group per finding, named `Audit · <issue>`.** Each group holds:
  - `· note`: a card, 300px wide, auto-layout. It shows `SEVERITY · PRIORITY GROUP` (11px bold), the issue (14px semibold), and the why (12px regular).
  - `· target`: a dashed outline 4px outside the element, or around the whole region for page-level issues.
  - `· line`: a straight connector from the outline to the card.
- **Severity colors:** High #D92D20 on #FEF3F2 · Medium #DC6803 on #FFFAEB · Low #475467 on #F2F4F7. Critical uses High's red with a 3px stroke.
- **Recommendations:** blue cards (#1570EF on #EFF8FF), named `Audit · Rec · <recommendation>`. Each card's label reads `RECOMMENDATION · <SOURCE>`, and it points to where the missing element would go.
- **`Audit · Summary` card** at the top of the column: issue counts by severity, the number of recommendations, **Not designed**, **Verify in build**, and which breakpoint the notes sit on.
- **`Audit · Recommendations` card:** the Recommendations from research table (Recommendation · Why · Source), 480px wide, placed at the top of the rightmost notes column. Size the column widths so the text fits inside the 448px content area. Widen the section if it doesn't fit.
- **Re-running:** first delete existing nodes in the section whose names start with `Audit · ` (and only those), then rebuild.
- **Check:** confirm every outline lands on the intended element (match on full text, not prefixes), then take one screenshot.
- **Report back** in one line: the number of notes and where they are.

## Handing off

**Not designed** and **Verify in build** become dev-handoff **Known Unknowns**. If dev-handoff runs next in the same session, pass them through as they are.
