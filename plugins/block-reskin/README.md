# block-reskin

Reskins a block copied from one P4 brand UI kit into another. It relinks every color, text style, corner radius, spacing value, button and nested component to the destination kit. For partner kits (AARP, NCOA, Fortune), it also removes every mention of other brands. It applies the best defaults on its own, then lists each judgment call as a follow-up for you to confirm.

**Owner:** Chance Chipman. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

- A Figma connection that can edit the destination UI kit.
- A Notion connection, if you hand it a Notion ticket.
- The block, already pasted into the destination kit's page. Claude can't copy between Figma files.

## Use it

> Reskin this: `<Notion ticket link>`. The copy is here: `<Figma link to the pasted frame in the destination kit>`

Claude asks for the source block link only if the ticket doesn't include one. It always asks for a reference block in the destination kit, which sets the look when the tokens alone don't decide it.

Supported kits: SO, GGR, SA, MN, MC, BB, SWOL, and the partner kits AARP, NCOA and FOR. Their links are in `skills/block-reskin/references/brands.md`.

## What's in this plugin

```
block-reskin/
├── .claude-plugin/
│   └── plugin.json              # plugin manifest: name, version, owner
├── skills/
│   └── block-reskin/
│       ├── SKILL.md             # the workflow
│       └── references/
│           ├── brands.md        # kit links, file keys, partner scrub rules
│           └── figma-recipes.md # tested Figma scripts and known traps
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). In Claude Code, you can also ask Claude to "publish my update to the P4 marketplace".
