# qual-research-simulator

A Claude Code plugin that simulates qualitative user research sessions against a Figma design — running it through data-grounded personas that react independently, like real participants in a moderated usability study. Personas are built from real behavioral/demographic data rather than recruited users.

Supports both **exploratory sessions** (no prior data — "how would these people react to this design?") and **explanatory sessions** (quant test results provided, with personas reacting blind to the design before the numbers are introduced).

**Every output is clearly labeled SIMULATED / not real user research.** This tool produces plausible, data-grounded hypotheses to inform design thinking — it does not replace real user research.

**Owner:** Audrey McGlynn. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

**Figma access.** This plugin's skill uses Figma MCP to view the design being tested. Each team member needs Figma MCP connected in their own Claude Desktop / Cowork setup before the skill can run. The plugin itself doesn't configure that connection.

## Use it

Start a request with a Figma link, a category (Sleep, Fitness, Aging, or Swolverine), and what the design is meant to do, e.g.:

> Run this pricing page through our Fitness personas — hypothesis is that simplifying the table reduces drop-off: `<figma link>`

If the category, design description/hypothesis, or Figma link is missing, the skill asks for exactly what's needed before running any personas.

**Optional: a live page URL.** If you also share a link to the live page a design would ship into (e.g. the current production page it's replacing), the skill loads it for real surrounding context — navigation, what's above/below the tested section, actual responsive behavior — in addition to the Figma frame. This isn't required, but it sharpens mobile-vs-desktop feedback in particular.

Each persona reacts to whichever device (mobile, tablet, or desktop) its own behavioral data actually skews toward, using the company's real breakpoints and reference resolutions rather than guessing — see `references/viewport-specs.md`. Personas with no stated device skew react to all frames present in one unified reaction.

## What's in this plugin

```
qual-research-simulator/
├── .claude-plugin/
│   └── plugin.json         # plugin manifest
├── skills/
│   └── qual-research-simulator/
│       ├── SKILL.md                       # the skill: intake → persona sessions → synthesis
│       └── references/
│           ├── personas-sleep.md          # Sleep category persona set
│           ├── personas-fitness.md        # Fitness category persona set
│           ├── personas-aging.md          # Aging category persona set
│           ├── personas-swolverine.md     # Swolverine category persona set
│           ├── viewport-specs.md          # company breakpoints + reference resolutions (mobile/tablet/desktop)
│           ├── interview-script.md        # narration prompt beats
│           ├── heuristics.md              # design heuristics reference
│           └── expansion-methods.md       # how to expand beyond the fixed persona set
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). In Claude Code, you can also ask Claude to "publish my update to the P4 marketplace".

If the underlying persona data has been updated at the source of truth, update the relevant `references/personas-*.md` file directly — personas never carry information across sessions on their own.
