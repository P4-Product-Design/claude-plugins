# Expanding a Session: Intensity Variants & Blended Personas

The base persona set (5-7 fixed personas per category) is always the default, always-run baseline for any session. Everything in this file is OPTIONAL and only invoked when the user explicitly asks for more breadth or more nuance. Never expand a session automatically.

These two expansion methods serve **different purposes** and must stay visibly separate in the output — never merge their results into one undifferentiated list of "responses."

---

## Method 1: Intensity Variants (for statistical-feeling breadth)

**Purpose:** simulate a small distribution within one persona, so the user can see whether a design holds up across the range of that persona, or only works for one end of it. Used when the user wants something that feels like "X out of Y leaned toward Z."

**How to construct variants:**
1. Pick ONE axis that's already implied by that persona's own grounding data (e.g. the Budget-Anchoring Deliberator's price sensitivity, the Late-Night Impulse Shopper's degree of urgency). Don't invent a new axis that isn't supported by the persona's existing data/behavior.
2. Create 2-3 labeled points along that axis (e.g. "High Price Sensitivity" / "Moderate Price Sensitivity"). Cap at 3 variants per persona — beyond that, variants blur together and stop being traceable, which defeats the purpose of a data-grounded system.
3. Each variant keeps the full persona identity (motivations, trusts/distrusts, demographics) — only the one named axis shifts.
4. Label every variant clearly: `[Persona Name] — [Variant Label]`.

**How to report results:**
- Any tally or count (e.g. "3 of 4 variants reacted negatively") MUST be presented under a heading like "Simulated Distribution (not a real sample)" and MUST include this caveat inline, not buried in a footnote:
  > These are simulated variations generated from one persona's underlying data, not independent human responses. A count here reflects how one grounded profile behaves across a plausible range — it is not a statistical sample and shouldn't be reported as one (e.g. avoid phrasing like "60% of users").
- Keep this section separate from the qualitative synthesis themes drawn from the base persona set.

---

## Method 2: Blended Personas (for qualitative depth/nuance)

**Purpose:** capture a psychologically distinct sub-case that neither parent persona alone would surface — usually because the two motivations create an internal tension (e.g. urgency vs. need for reassurance) that's itself revealing about the design. This is NOT about generating more responses for volume; it's about surfacing a specific scenario worth a deeper look.

**Selection criteria — only blend personas when:**
- The combination is behaviorally plausible (a real person could genuinely hold both motivations at once)
- The blend creates an actual tension or new consideration, not just an average of two profiles
- There's a specific reason to think this sub-case matters for the design being tested

Do NOT auto-generate every possible pair of personas in a category — most combinations won't meet the bar above, and mechanically producing all of them dilutes the value of the ones that do.

**How to author a blended persona:**
1. Name it clearly as a blend: `[Persona A] + [Persona B]`
2. Write a short line identifying the specific tension the blend creates (e.g. "urgency to act now vs. need for brand reassurance before committing")
3. Merge trusts/distrusts only where they don't conflict; where they DO conflict, that conflict IS the interesting part — describe it explicitly rather than resolving it
4. Write a sample voice line that reflects the tension, not just one parent persona's voice
5. Present blended-persona reactions in a clearly separate "Qualitative Deep Dive" section — never folded into the counted/tallied output from Method 1, and never presented as part of the base persona set's transcript.

**Example (illustrative, not a stored persona):**
> **Late-Night Impulse Shopper + Decision-Ready Premium Buyer**
> Tension: driven to act right now by an acute problem, but still wants brand reassurance and zero friction before committing — won't tolerate a long comparison process, but also won't just grab anything.
> Sample voice: "I need this fixed tonight, but I'm not buying some random brand I've never heard of at midnight. Show me the one that's clearly the safe choice, fast."

---

## Keeping outputs separated

A session that uses either expansion method should structure its output in this order:
1. Base persona set transcript (always present)
2. Cross-persona synthesis from the base set (always present)
3. *(if requested)* Simulated Distribution section — intensity variants, with the mandatory caveat
4. *(if requested)* Qualitative Deep Dive section — blended personas
5. Heuristic notes and recommendations, drawing from whichever of the above is relevant

Never let a reader come away thinking the expanded sections are additional independent "users" on par with the base set.
