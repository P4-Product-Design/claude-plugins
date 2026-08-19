# product-block-gatherer

A Claude Code plugin that gathers and structures product information into the two standard block formats used on Fortune Shop and NCOA Shop pages — **Product Block Lite** and **Foundational Product Block** — and delivers the result as a downloadable Word document (.docx).

Supported categories: Creatine, Protein Powder, Pre-Workout, Hair Loss, NMN Supplements, Hearing Aids, Medical Alert Systems, and GLP-1 Medications.

## Required inputs

Before generating anything, the skill needs all of the following:

1. **Product Name**
2. **Category** (one of the supported categories above)
3. **Superlative** (e.g. "Best Overall") — never inferred
4. **Product Link**
5. **Organic Link** (or confirmation that none exists)
6. **Live Page URL(s)** (or confirmation the page doesn't exist yet)

If any input is missing, the skill asks for it directly rather than guessing.

This repo is public, so no GitHub login, token, or git setup is needed to install it.

## Install (one time, per person)

**Easiest way — no GitHub knowledge needed:**

1. In Claude Desktop, click **Customize** in the sidebar.
2. Next to **Personal plugins**, click **+** → **Add** → **Add marketplace**.
3. Paste `P4-Product-Design/product-block-gatherer` into the URL field and click **Sync**. No token needed.
4. Adding the marketplace and installing the plugin are two separate steps. Open the **Directory** (click **Plugins** in the Customize sidebar), find the `product-block-gatherer` tab, and click the **+** on the card — that's what actually installs it.

**Alternative — typed commands:** Claude Desktop has three tabs: Chat, Cowork, and Code. `/plugin` commands only work in **Code** (typing them in Chat or Cowork gives a "not available in this environment" error — that just means you're in the wrong tab). In the **Code tab**, type:

```
/plugin marketplace add P4-Product-Design/product-block-gatherer
/plugin install product-block-gatherer@product-block-gatherer
```

Either way, once installed it shows up under **Customize → Manage plugins**, where you can update or remove it.

## Update

Since the repo is public, updates need no token or login setup — background auto-update just works. To update manually, type this in the Code tab, or re-run the Add marketplace steps above to re-sync:

```
/plugin marketplace update product-block-gatherer
```

## Use it

Provide all six required inputs for a product, e.g.:

> Fill out the product block for Thorne Creatine — Category: Creatine, Superlative: "Best Overall", Product Link: `<url>`, Organic Link: `<url>` (or "none exists"), Live Page: `<url>` (or "doesn't exist yet").

If anything is missing, the skill lists exactly what's needed before drafting.

## What's in this repo

```
product-block-gatherer/
├── .claude-plugin/
│   ├── plugin.json         # plugin manifest
│   └── marketplace.json    # marketplace catalog (this repo is both, for a single-plugin install)
├── skills/
│   └── product-block-gatherer/
│       ├── SKILL.md              # the skill: required inputs → research → docx output
│       └── references/
│           └── category-specs.md # per-category grid/spec fields
└── README.md
```

## Updating the skill itself

Edit `skills/product-block-gatherer/SKILL.md`, bump the `version` in both `.claude-plugin/plugin.json` and the plugin entry in `.claude-plugin/marketplace.json`, commit, and push. Everyone who's installed the plugin picks up the change the next time they run the update command above.
