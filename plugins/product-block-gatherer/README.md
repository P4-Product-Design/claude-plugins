# product-block-gatherer

A Claude Code plugin that gathers and structures product information into the two standard block formats used on Fortune Shop and NCOA Shop pages — **Product Block Lite** and **Foundational Product Block** — and delivers the result as a downloadable Word document (.docx).

Supported categories: Creatine, Protein Powder, Pre-Workout, Hair Loss, NMN Supplements, Hearing Aids, Medical Alert Systems, and GLP-1 Medications.

**Owner:** Audrey McGlynn. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Required inputs

Before generating anything, the skill needs all of the following:

1. **Product Name**
2. **Category** (one of the supported categories above)
3. **Superlative** (e.g. "Best Overall") — never inferred
4. **Product Link**
5. **Organic Link** (or confirmation that none exists)
6. **Live Page URL(s)** (or confirmation the page doesn't exist yet)

If any input is missing, the skill asks for it directly rather than guessing.

## Use it

Provide all six required inputs for a product, e.g.:

> Fill out the product block for Thorne Creatine — Category: Creatine, Superlative: "Best Overall", Product Link: `<url>`, Organic Link: `<url>` (or "none exists"), Live Page: `<url>` (or "doesn't exist yet").

If anything is missing, the skill lists exactly what's needed before drafting.

## What's in this plugin

```
product-block-gatherer/
├── .claude-plugin/
│   └── plugin.json         # plugin manifest
├── skills/
│   └── product-block-gatherer/
│       ├── SKILL.md              # the skill: required inputs → research → docx output
│       └── references/
│           └── category-specs.md # per-category grid/spec fields
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). In Claude Code, you can also ask Claude to "publish my update to the P4 marketplace".
