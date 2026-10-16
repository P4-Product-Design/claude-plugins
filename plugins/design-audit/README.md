# design-audit

Judges whether a design is the best it can be for its context: a new Figma design, a live page, or an email. It returns a short, prioritized list of issues based on how users will actually behave on the page, recommendations for best practices the design is missing, and notes on the Figma canvas next to each issue.

**Owner:** Chance Chipman. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

- The Figma connector, so Claude can read the file and write notes to it.
- For live pages: Claude's browser.
- Web search, which is optional. It's used only for page types the built-in playbooks don't cover.

## Use it

> Audit this design: `<figma link>`

> Review this PDP before handoff: `<figma link>`

> Audit this live page: `<url>`, and this email: `<figma link>`

Claude takes a screenshot, asks a few intake questions (input type, brand, page type, traffic source, primary action, breakpoints, and what's out of scope), then:

1. Posts the audit in chat: issue tables in priority groups, recommendations from research, states that aren't designed, and items to verify in the build.
2. After you review it, writes `Audit · <issue>` notes into Figma beside each issue, plus a summary card and a recommendations table. It never edits the design frames.

## What it checks against

- **Playbooks** for each page type: PDP, collection, homepage, long-form content, affiliate review and roundup, comparison, quiz results, partner co-branded, landing pages (paid social, paid search / PMax, email, lead-gen), and emails. Trust factors, the conversion zone, and section jobs are always checked, and an older-adults (50+) modifier is added for those audiences.
- **UX laws:** Fitts's law, Hick's law, Jakob's law, social proof, and more.
- **Accessibility:** 44px targets, WCAG contrast, and states that rely on color alone.

The not-designed and verify-in-build lists feed straight into **dev-handoff**'s Known Unknowns.

This plugin replaces the older redesign-audit skill. Its live-page and email audits, brand context, conversion-zone checks, and section jobs are all built in.

## What's in this plugin

```
design-audit/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── design-audit/
│       ├── SKILL.md              # workflow, output format, Figma notes
│       └── references/
│           ├── playbooks.md      # best practices per page type
│           ├── checks.md         # user-behavior checks
│           ├── scoring.md        # severity, effort, priority groups
│           └── ux-laws.md        # UX laws and what they mean on a page
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). In Claude Code, you can also ask Claude to "publish my update to the P4 marketplace".
