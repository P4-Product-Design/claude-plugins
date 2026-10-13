# Default Narration Prompts (Think-Aloud Monologue Format)

This skill runs sessions as a **continuous first-person think-aloud monologue** per persona, not a Q&A transcript. This mirrors how real unmoderated and moderated usability studies actually work: a participant narrates their thoughts, hesitations, and actions in a real-time stream as they encounter a design, rather than answering a list of discrete questions one at a time (see: NN/g, "Unmoderated User Tests: How and Why to Do Them" — verbalizing thoughts and actions as they happen is what actually reveals usability problems; a participant who is just answering isolated questions afterward, disconnected from the moment-to-moment experience, gives much thinner signal).

## Why monologue instead of Q&A

A real participant doesn't experience a design as six separate interview questions — they look at it, form an impression, start figuring out what it is, notice things that reassure or worry them, maybe hesitate, and either act or don't, all as one continuous train of thought. Breaking that into discrete Q&A pairs loses the moment-to-moment texture (what did they notice first, in what order, what changed their mind partway through) that's often the most useful signal in a usability session.

## The prompt beats (not questions to answer one by one)

Use these as beats the monologue should naturally pass through, in roughly this order, but written as one flowing narration — not "Q1: ... A1: ..." pairs:

1. **First impression** — what they see first, their gut reaction
2. **Comprehension** — figuring out what this is/does, in real time, including any confusion along the way
3. **Trust** — what's building or undermining confidence as they keep looking
4. **Hesitation** — any point where they slow down, second-guess, or consider leaving
5. **Comparison** — how it stacks up against what they'd expect elsewhere, if it comes to mind naturally
6. **Action** — what they'd actually do next, and why

A persona's monologue doesn't need to hit every beat explicitly or in this exact order — a real train of thought wanders, backtracks, and skips things that don't feel relevant to that particular person. Force-fitting all six beats into every monologue in the same order for every persona would make them sound like they're following a script, which defeats the purpose.

## Usage modes

- **Standard mode**: personas narrate a monologue that naturally covers the beats above as they look over the design. Attention should go wherever the persona's real behavioral profile would take it — not toward whatever the researcher happens to be evaluating. It's normal and expected for a persona to never mention a given element if their profile wouldn't realistically draw them to it.
- **Task mode** (when the user provides a task — see SKILL.md Step 1): run in TWO phases, never merged. Phase 1 is the standard general monologue above, generated with no awareness that a task is coming. Phase 2, run only after Phase 1 is complete, directs the persona to attempt the specific task, narrating in real time: where they look for the thing they need, what they click or tap, where they get confused or stuck, whether they complete it, and how they feel about the process along the way. This mirrors real usability testing structure — observe the unprompted first look, then give the instruction. Lean into specific navigation/interaction detail in Phase 2 ("I'd look for a price near the top... I don't see one, so I'd click the green button expecting it to show me...").
- **Custom mode**: the user supplies specific things they want covered (in addition to or instead of the standard beats) — fold these into the monologue naturally rather than treating them as separate questions tacked onto the end.
- **Explanatory mode** (quant data provided): personas are NOT told about the quant data. They narrate the same monologue exactly as they would in exploratory mode, blind to any test results. The quant data is only brought in afterward, as a separate analytical step comparing the completed qualitative synthesis against the numbers — see `SKILL.md` Step 6. This keeps the qualitative read uncontaminated by foreknowledge of what "worked."

Always let the user drive the level of customization for a given session — don't force a rigid structure if they've given you something more tailored to ask instead.
