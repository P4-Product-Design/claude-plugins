# figma-to-shopify-liquid

A Claude Code plugin that converts a Figma design into a pixel-exact Shopify Liquid theme section or block — same tokens, spacing, fonts, and breakpoints as the design — plus a documentation file and a static HTML preview for verification.

Built from the process used on Swolverine's PDP and Stack & Save hero components: read the design's own Dev Mode annotations instead of guessing at behavior, verify every breakpoint with measured values instead of assuming, and ask before assuming anything the design doesn't explicitly answer.

**Owner:** Chance Chipman. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

**Figma access.** This plugin's skill uses Figma's Dev Mode MCP tools (`get_design_context`, `get_variable_defs`, screenshots) to read designs. Each team member needs Figma MCP access connected in their own Claude Desktop / Cowork setup before the skill can pull a design — the plugin itself doesn't configure that connection.

## Use it

Start a request with a Figma link and what you want built, e.g.:

> Turn this Figma frame into a Shopify section: `<figma link with node-id>` — it should replace the current hero on the /pages/some-page template.

If you don't give enough to start (a Figma link, whether it replaces something existing, how exact it needs to be, whether it needs live product/review data, and what files you want back), the skill will ask for exactly what's missing before doing any research — it won't guess.

## What's in this plugin

```
figma-to-shopify-liquid/
├── .claude-plugin/
│   └── plugin.json         # plugin manifest
├── skills/
│   └── figma-to-shopify-liquid/
│       ├── SKILL.md              # the skill: step-0 intake checklist + the 11-step process
│       └── backend-data-wiring.md # pattern reference for wiring live product/review/app data
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). In Claude Code, you can also ask Claude to "publish my update to the P4 marketplace".
