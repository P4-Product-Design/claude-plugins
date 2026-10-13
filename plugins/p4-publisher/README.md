# p4-publisher

Gets a plugin or skill into the P4 marketplace, or ships an update to one that's already there. It runs every check before pushing, so a mistake doesn't break installs for the rest of the team.

**Owner:** Chance Chipman. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

- **Claude Code.** Use the Code tab in Claude Desktop, or the terminal. The skill runs git commands, so the Chat and Cowork tabs won't work.
- **Write access to the P4-Product-Design GitHub org.** It's only needed to push. Message Chance with your GitHub username for an invite.

## Use it

In the Code tab:

> Publish my brand-audit skill to the P4 marketplace. It's in ~/Claude/Skills/brand-audit.

> I fixed a bug in dev-handoff. Publish the update.

Claude gets a current copy of the repo and puts your files in the right place. It bumps the version, runs the checks, and test-installs a new plugin. It shows you what it will push and asks before committing. Then it confirms GitHub's check passed and gives you a short message to post for the team.

## What's in this plugin

```
p4-publisher/
├── .claude-plugin/
│   └── plugin.json         # plugin manifest
├── skills/
│   └── publish-to-p4/
│       └── SKILL.md        # the skill: add or update → check → test install → push → confirm
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md).
