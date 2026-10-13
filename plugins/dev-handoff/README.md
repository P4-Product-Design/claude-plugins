# dev-handoff

A Claude Code plugin that turns a Figma design into a complete, engineer-ready handoff. From a Figma link plus feature context, brand, and KPIs, it reads the whole design, drafts an exhaustive spec, and writes it back into Figma as two frames — **Requirements & Edge Cases** and **Dev Spec Handoff** — then applies native **Dev Mode** annotations to the design across breakpoints.

The bar it holds to: a handoff is done when an engineer can build the feature without coming back with questions. It marks every interactive state, maps affiliate product fields to GPV, flags unknowns with an owner, and treats mobile as equal to desktop.

**Owner:** Chance Chipman. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

**Figma access with write capability.** This plugin's skill uses Figma's `figma:figma-use` skill and the Figma Plugin API (`figma.annotations`, `node.annotations`) to read designs *and write frames and Dev Mode annotations back into the file*. Each team member needs Figma MCP connected — with edit access to the target file — in their own Claude Desktop / Cowork setup before the skill can run. The plugin itself doesn't configure that connection.

## Use it

Start a request with a Figma link and the feature context, e.g.:

> Write up the dev handoff for this comparison tool: `<figma link with node-id>` — brand is SO, primary KPI is Take Rate.

If you don't give enough to start (a dev-ready Figma link, feature/test context, brand, and KPIs), the skill asks for exactly what's missing before drafting — it won't guess. It presents both drafts for your approval before writing anything to Figma, and asks which breakpoint frames to annotate before touching the design.

## What's in this plugin

```
dev-handoff/
├── .claude-plugin/
│   └── plugin.json         # plugin manifest
├── skills/
│   └── dev-handoff/
│       └── SKILL.md        # the skill: intake → spec drafts → Figma frames → Dev Mode annotations
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). In Claude Code, you can also ask Claude to "publish my update to the P4 marketplace".
