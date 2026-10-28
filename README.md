# P4 Product Design plugins for Claude

[![Marketplace check](https://github.com/P4-Product-Design/claude-plugins/actions/workflows/check.yml/badge.svg)](https://github.com/P4-Product-Design/claude-plugins/actions/workflows/check.yml)

Every P4 Product Design plugin for Claude, in one place. Add this marketplace once, then install the plugins you need. Updates arrive on their own.

This repo is public, so you don't need a GitHub account, login, or token to install anything.

## Install (one time, per person)

**Point-and-click (recommended):**

1. In Claude Desktop, click **Customize** in the sidebar.
2. Next to **Personal plugins**, click **+** → **Add** → **Add marketplace**.
3. Paste `P4-Product-Design/claude-plugins` into the URL field. Leave **Sync automatically** on and click **Sync**.
4. Syncing adds the marketplace but doesn't install anything yet. Click **Plugins** in the Customize sidebar, open the **p4-product-design** tab, and click **+** on each plugin you want.

Installed plugins show up under **Customize → Manage plugins**, where you can update or remove them.

**Typed commands (Code tab only):** `/plugin` commands work only in the **Code** tab of Claude Desktop or in the terminal. The Chat and Cowork tabs say "not available in this environment".

```
/plugin marketplace add P4-Product-Design/claude-plugins
/plugin install dev-handoff@p4-product-design
```

Swap in any plugin name from the table below.

## Plugins

| Plugin | What it does | Owner |
|---|---|---|
| [design-audit](plugins/design-audit) | Audits a Figma design, live page, or email against page-type best practices and UX laws, then adds prioritized notes and research recommendations to Figma. | Chance Chipman |
| [dev-handoff](plugins/dev-handoff) | Turns a Figma design into an engineer-ready handoff: Requirements and Dev Spec frames, plus native Dev Mode annotations for what changes between breakpoints. | Chance Chipman |
| [figma-to-optimizely](plugins/figma-to-optimizely) | Turns a Figma design into an Optimizely Web Experiment widget (HTML, CSS, JS, widget.json) with a local preview. | Andy Ramos |
| [figma-to-shopify-liquid](plugins/figma-to-shopify-liquid) | Converts a Figma design into a pixel-exact Shopify Liquid section or block, with matching docs and a static preview. | Chance Chipman |
| [p4-publisher](plugins/p4-publisher) | Adds your plugin or skill to this marketplace, or publishes an update to one, with every check run first. | Chance Chipman |
| [product-block-gatherer](plugins/product-block-gatherer) | Gathers and fills product block data for Fortune Shop and NCOA Shop pages, as a Word document. | Audrey McGlynn |
| [qual-research-simulator](plugins/qual-research-simulator) | Runs a Figma design past data-grounded personas, like a simulated usability study. | Audrey McGlynn |
| [swolverine-product-photos](plugins/swolverine-product-photos) | Turns raw Swolverine studio shots into website-ready product images with no generative fill. Needs a Mac with Photoshop 2026. | Chance Chipman |

Each plugin's page lists what it needs and how to use it.

**Most plugins read designs from Figma.** If you haven't connected Figma yet, paste this into any Claude Desktop tab:

> Help me connect my Figma account to Claude Desktop so design skills can read Figma files. Walk me through it step by step.

## Add a new plugin or get the latest version

**Already added the marketplace?** Don't add it again. Claude will say it's already added. Instead, refresh the marketplace so new plugins and versions show up:

1. In Claude Desktop, click **Customize** → **Plugins**, then open the **P4 Product Design** tab.
2. Click the **Add** dropdown → **Manage marketplaces**.
3. Find **P4 Product Design**, click the **⋯** next to it, and click **Update**.
4. Go back to the **Plugins** tab and click **+** on the new plugin.

Do the same update whenever a teammate announces a new plugin or version that you don't see yet.

**Typed commands (Code tab only):**

```
/plugin marketplace update p4-product-design
/plugin install <plugin-name>@p4-product-design
```

## Switching from the old one-repo-per-plugin setup

If you installed a P4 plugin before October 2026, it came from its own marketplace (like `P4-Product-Design/dev-handoff`). Those repos are archived and won't get updates.

1. In **Customize → Manage plugins**, remove the old P4 plugins and their marketplaces.
2. Follow **Install** above.

If you keep both, you'll have two copies of the same skill.

## Add or update a plugin

Install **p4-publisher** and ask Claude in the Code tab, e.g. "publish my brand-audit skill to the P4 marketplace". [CONTRIBUTING.md](CONTRIBUTING.md) covers the manual steps and the rules. To push changes, you need to be a member of the P4-Product-Design org. Message Chance with your GitHub username.

## Stuck?

Paste this into Claude wherever you got stuck:

> I'm trying to install a plugin from the P4-Product-Design/claude-plugins marketplace in Claude Desktop and it's not working. Help me figure out why and fix it.

Or message Chance.
