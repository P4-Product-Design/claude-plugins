# PLUGIN-NAME

One or two sentences on what this plugin does.

**Owner:** OWNER NAME. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

Anything a teammate needs first (a Figma connection, an app, a folder). Delete this section if there's nothing.

## Use it

An example request, e.g.:

> Do the thing with this Figma link: `<figma link>`

## What's in this plugin

```
PLUGIN-NAME/
├── .claude-plugin/
│   └── plugin.json         # plugin manifest: name, version, owner
├── skills/
│   └── PLUGIN-NAME/
│       └── SKILL.md        # the skill
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). In Claude Code, you can also ask Claude to "publish my update to the P4 marketplace".
