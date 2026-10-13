# qual-research-simulator

A Claude Code plugin that simulates qualitative user research sessions against a Figma design — running it through data-grounded personas that react independently, like real participants in a moderated usability study. Personas are built from real behavioral/demographic data rather than recruited users.

Supports both **exploratory sessions** (no prior data — "how would these people react to this design?") and **explanatory sessions** (quant test results provided, with personas reacting blind to the design before the numbers are introduced).

**Every output is clearly labeled SIMULATED / not real user research.** This tool produces plausible, data-grounded hypotheses to inform design thinking — it does not replace real user research.

## Prerequisites

**Figma access.** This plugin's skill uses Figma MCP to view the design being tested. Each team member needs Figma MCP connected in their own Claude Desktop / Cowork setup before the skill can run. The plugin itself doesn't configure that connection.

This repo is public, so no GitHub login, token, or git setup is needed to install it.

## Install (one time, per person)

**Easiest way — no GitHub knowledge needed:**

1. In Claude Desktop, click **Customize** in the sidebar.
2. Next to **Personal plugins**, click **+** → **Add** → **Add marketplace**.
3. Paste `P4-Product-Design/qual-research-simulator` into the URL field and click **Sync**. No token needed.
4. Adding the marketplace and installing the plugin are two separate steps. Open the **Directory** (click **Plugins** in the Customize sidebar), find the `qual-research-simulator` tab, and click the **+** on the card — that's what actually installs it.

**Alternative — typed commands:** Claude Desktop has three tabs: Chat, Cowork, and Code. `/plugin` commands only work in **Code** (typing them in Chat or Cowork gives a "not available in this environment" error — that just means you're in the wrong tab). In the **Code tab**, type:

```
/plugin marketplace add P4-Product-Design/qual-research-simulator
/plugin install qual-research-simulator@qual-research-simulator
```

Either way, once installed it shows up under **Customize → Manage plugins**, where you can update or remove it.

## Update

Since the repo is public, updates need no token or login setup — background auto-update just works. To update manually, type this in the Code tab, or re-run the Add marketplace steps above to re-sync:

```
/plugin marketplace update qual-research-simulator
```

## Use it

Start a request with a Figma link, a category (Sleep, Fitness, Aging, or Swolverine), and what the design is meant to do, e.g.:

> Run this pricing page through our Fitness personas — hypothesis is that simplifying the table reduces drop-off: `<figma link>`

If the category, design description/hypothesis, or Figma link is missing, the skill asks for exactly what's needed before running any personas.

**Optional: a live page URL.** If you also share a link to the live page a design would ship into (e.g. the current production page it's replacing), the skill loads it for real surrounding context — navigation, what's above/below the tested section, actual responsive behavior — in addition to the Figma frame. This isn't required, but it sharpens mobile-vs-desktop feedback in particular.

Each persona reacts to whichever device (mobile, tablet, or desktop) its own behavioral data actually skews toward, using the company's real breakpoints and reference resolutions rather than guessing — see `references/viewport-specs.md`. Personas with no stated device skew react to all frames present in one unified reaction.

## What's in this repo

```
qual-research-simulator/
├── .claude-plugin/
│   ├── plugin.json         # plugin manifest
│   └── marketplace.json    # marketplace catalog (this repo is both, for a single-plugin install)
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

## Updating the skill itself

Edit `skills/qual-research-simulator/SKILL.md` (or the reference files), bump the `version` in both `.claude-plugin/plugin.json` and the plugin entry in `.claude-plugin/marketplace.json`, commit, and push. Everyone who's installed the plugin picks up the change the next time they run the update command above.

If the underlying persona data has been updated at the source of truth, update the relevant `references/personas-*.md` file directly — personas never carry information across sessions on their own.
