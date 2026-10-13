# figma-to-shopify-liquid

A Claude Code plugin that converts a Figma design into a pixel-exact Shopify Liquid theme section or block — same tokens, spacing, fonts, and breakpoints as the design — plus a documentation file and a static HTML preview for verification.

Built from the process used on Swolverine's PDP and Stack & Save hero components: read the design's own Dev Mode annotations instead of guessing at behavior, verify every breakpoint with measured values instead of assuming, and ask before assuming anything the design doesn't explicitly answer.

## Prerequisites

**Figma access.** This plugin's skill uses Figma's Dev Mode MCP tools (`get_design_context`, `get_variable_defs`, screenshots) to read designs. Each team member needs Figma MCP access connected in their own Claude Desktop / Cowork setup before the skill can pull a design — the plugin itself doesn't configure that connection.

This repo is public, so no GitHub login, token, or git setup is needed to install it.

## Install (one time, per person)

**Easiest way — no GitHub knowledge needed:**

1. In Claude Desktop, click **Customize** in the sidebar.
2. Next to **Personal plugins**, click **+** → **Add** → **Add marketplace**.
3. Paste `P4-Product-Design/figma-to-shopify-liquid` into the URL field and click **Sync**. No token needed.
4. Adding the marketplace and installing the plugin are two separate steps. Open the **Directory** (click **Plugins** in the Customize sidebar), find the `figma-to-shopify-liquid` tab, and click the **+** on the "Figma to shopify liquid" card — that's what actually installs it.

**Alternative — typed commands:** Claude Desktop has three tabs: Chat, Cowork, and Code. `/plugin` commands only work in **Code** (typing them in Chat or Cowork gives a "not available in this environment" error — that just means you're in the wrong tab). In the **Code tab**, type:

```
/plugin marketplace add P4-Product-Design/figma-to-shopify-liquid
/plugin install figma-to-shopify-liquid@figma-to-shopify-liquid
```

Either way, once installed it shows up under **Customize → Manage plugins**, where you can update or remove it.

## Update

Since the repo is public, updates need no token or login setup — background auto-update just works. To update manually, type this in the Code tab, or re-run the Add marketplace steps above to re-sync:

```
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
