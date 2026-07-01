# figma-to-shopify-liquid

A Claude Code plugin that converts a Figma design into a pixel-exact Shopify Liquid theme section or block — same tokens, spacing, fonts, and breakpoints as the design — plus a documentation file and a static HTML preview for verification.

Built from the process used on Swolverine's PDP and Stack & Save hero components: read the design's own Dev Mode annotations instead of guessing at behavior, verify every breakpoint with measured values instead of assuming, and ask before assuming anything the design doesn't explicitly answer.

## Prerequisite

This plugin's skill uses Figma's Dev Mode MCP tools (`get_design_context`, `get_variable_defs`, screenshots) to read designs. Each team member needs Figma MCP access connected in their own Claude Code / Cowork setup before the skill can pull a design — the plugin itself doesn't configure that connection.

## Install (one time, per person)

```bash
/plugin marketplace add <your-github-org-or-username>/figma-to-shopify-liquid
/plugin install figma-to-shopify-liquid@figma-to-shopify-liquid
```

Replace `<your-github-org-or-username>` with wherever this repo actually lives on GitHub.

## Update

Whenever the repo gets new commits (skill fixes, process improvements):

```bash
/plugin marketplace update figma-to-shopify-liquid
```

## Use it

Start a request with a Figma link and what you want built, e.g.:

> Turn this Figma frame into a Shopify section: `<figma link with node-id>` — it should replace the current hero on the /pages/some-page template.

If you don't give enough to start (a Figma link, whether it replaces something existing, how exact it needs to be, whether it needs live product/review data, and what files you want back), the skill will ask for exactly what's missing before doing any research — it won't guess.

## What's in this repo

```
figma-to-shopify-liquid/
├── .claude-plugin/
│   ├── plugin.json         # plugin manifest
│   └── marketplace.json    # marketplace catalog (this repo is both, for a single-plugin install)
├── skills/
│   └── figma-to-shopify-liquid/
│       ├── SKILL.md              # the skill: step-0 intake checklist + the 11-step process
│       └── backend-data-wiring.md # pattern reference for wiring live product/review/app data
└── README.md
```

## Updating the skill itself

Edit `skills/figma-to-shopify-liquid/SKILL.md` (or `backend-data-wiring.md`), bump the `version` in both `.claude-plugin/plugin.json` and the plugin entry in `.claude-plugin/marketplace.json`, commit, and push. Everyone who's installed the plugin picks up the change the next time they run the update command above.
