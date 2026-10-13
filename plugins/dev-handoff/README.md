# dev-handoff

A Claude Code plugin that turns a Figma design into a complete, engineer-ready handoff. From a Figma link plus feature context, brand, and KPIs, it reads the whole design, drafts an exhaustive spec, and writes it back into Figma as two frames — **Requirements & Edge Cases** and **Dev Spec Handoff** — then applies native **Dev Mode** annotations to the design across breakpoints.

The bar it holds to: a handoff is done when an engineer can build the feature without coming back with questions. It marks every interactive state, maps affiliate product fields to GPV, flags unknowns with an owner, and treats mobile as equal to desktop.

## Prerequisites

**Figma access with write capability.** This plugin's skill uses Figma's `figma:figma-use` skill and the Figma Plugin API (`figma.annotations`, `node.annotations`) to read designs *and write frames and Dev Mode annotations back into the file*. Each team member needs Figma MCP connected — with edit access to the target file — in their own Claude Desktop / Cowork setup before the skill can run. The plugin itself doesn't configure that connection.

This repo is public, so no GitHub login, token, or git setup is needed to install it.

## Install (one time, per person)

**Easiest way — no GitHub knowledge needed:**

1. In Claude Desktop, click **Customize** in the sidebar.
2. Next to **Personal plugins**, click **+** → **Add** → **Add marketplace**.
3. Paste `P4-Product-Design/dev-handoff` into the URL field and click **Sync**. No token needed.
4. Adding the marketplace and installing the plugin are two separate steps. Open the **Directory** (click **Plugins** in the Customize sidebar), find the `dev-handoff` tab, and click the **+** on the "Dev handoff" card — that's what actually installs it.

**Alternative — typed commands:** Claude Desktop has three tabs: Chat, Cowork, and Code. `/plugin` commands only work in **Code** (typing them in Chat or Cowork gives a "not available in this environment" error — that just means you're in the wrong tab). In the **Code tab**, type:

```
/plugin marketplace add P4-Product-Design/dev-handoff
/plugin install dev-handoff@dev-handoff
```

Either way, once installed it shows up under **Customize → Manage plugins**, where you can update or remove it.

## Update

Since the repo is public, updates need no token or login setup — background auto-update just works. To update manually, type this in the Code tab, or re-run the Add marketplace steps above to re-sync:

```
/plugin marketplace update dev-handoff
```

## Use it

Start a request with a Figma link and the feature context, e.g.:

> Write up the dev handoff for this comparison tool: `<figma link with node-id>` — brand is SO, primary KPI is Take Rate.

If you don't give enough to start (a dev-ready Figma link, feature/test context, brand, and KPIs), the skill asks for exactly what's missing before drafting — it won't guess. It presents both drafts for your approval before writing anything to Figma, and asks which breakpoint frames to annotate before touching the design.

## What's in this repo

```
dev-handoff/
├── .claude-plugin/
│   ├── plugin.json         # plugin manifest
│   └── marketplace.json    # marketplace catalog (this repo is both, for a single-plugin install)
├── skills/
│   └── dev-handoff/
│       └── SKILL.md        # the skill: intake → spec drafts → Figma frames → Dev Mode annotations
└── README.md
```

## Updating the skill itself

Edit `skills/dev-handoff/SKILL.md`, bump the `version` in both `.claude-plugin/plugin.json` and the plugin entry in `.claude-plugin/marketplace.json`, commit, and push. Everyone who's installed the plugin picks up the change the next time they run the update command above.
