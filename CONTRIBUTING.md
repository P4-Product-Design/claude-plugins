# Adding or updating a plugin

Everyone installs from this one repo. Whatever is on `main` reaches the whole team on their next sync, including mistakes. The steps below and the automatic checks keep it working.

## The easy way: ask Claude

1. Install **p4-publisher** from the marketplace (see the [README](README.md#install-one-time-per-person)).
2. In the **Code** tab of Claude Desktop, ask for what you want:
   - "Publish my brand-audit skill to the P4 marketplace. It's in ~/Claude/Skills/brand-audit."
   - "I updated qual-research-simulator. Publish it."

Claude handles the folder, version, checks, test install, and push. It asks before committing.

## Before you start

- **Write access:** pushing needs membership in the P4-Product-Design GitHub org. Message Chance with your GitHub username for an invite. The invite expires after 7 days.
- **A copy of the repo:** `git clone https://github.com/P4-Product-Design/claude-plugins.git`. Run `git pull --rebase` before every change.

## Add a new plugin by hand

1. **Pick a name:** lowercase-with-hyphens, such as `brand-audit`. Teammates install it as `brand-audit@p4-product-design`.
2. **Copy the template:** copy `template/` to `plugins/<name>/`, then rename `skills/PLUGIN-NAME` to `skills/<name>`.
3. **Add your skill:** write it in `skills/<name>/SKILL.md`, or replace that folder with your existing skill folder. Commands go in `commands/`, agents in `agents/`, and scripts in `scripts/`. Scripts must reference their own files as `${CLAUDE_PLUGIN_ROOT}/...`, never by a relative path.
4. **Fill in `plugins/<name>/.claude-plugin/plugin.json`:** name, a one-sentence description, and you as `author`. Start at version `0.1.0`.
5. **Fill in `plugins/<name>/README.md`.**
6. **List it:** add an entry to `.claude-plugin/marketplace.json`, in alphabetical order:
   ```json
   {
     "name": "<name>",
     "source": "./plugins/<name>",
     "description": "<same sentence as plugin.json>",
     "category": "<design | development | research | content | productivity>"
   }
   ```
7. **Add it to the plugin table** in `README.md`.
8. **Check and test:** run the check and the test install (see below).
9. **Commit and push:** `git pull --rebase`, then `git push`.
10. **Add it to the org homepage:** add a matching row to the plugin table in `profile/README.md` of the [`P4-Product-Design/.github`](https://github.com/P4-Product-Design/.github) repo, in alphabetical order. That table is what shows on https://github.com/P4-Product-Design. Do the same when you remove a plugin or change its summary.
11. **Tell the team:** "Customize → Plugins → p4-product-design tab, click + on <name>."

## Update a plugin

1. **Edit only inside its folder:** `plugins/<name>/`. If you aren't the plugin's owner (`author` in its `plugin.json`), check with them first.
2. **Bump `version` in `plugins/<name>/.claude-plugin/plugin.json`:**
   - **Patch** (`0.2.0` → `0.2.1`): fixes and wording.
   - **Minor** (`0.2.1` → `0.3.0`): new behavior.
   - **Major:** only when people's existing use of the plugin would break.

   Without a bump, nobody receives your change, and the check blocks the push.
3. **Check, commit, and push.** Teammates get the update on their next sync.

## Check and test

From the repo root:

```
scripts/check.sh
```

It must pass before you push. It runs `claude plugin validate` on the marketplace and every plugin, plus these rules:

| Rule | Why |
|---|---|
| Every folder in `plugins/` has exactly one entry in `marketplace.json`, and vice versa | A folder without an entry can't be installed. An entry without a folder breaks the sync. |
| `source` is `"./plugins/<name>"` | Claude Code rejects `"."`. That broke four installs in October 2026. |
| No top-level `description` in `marketplace.json`; it goes under `metadata` | Claude Code rejects it at the top level. |
| No `marketplace.json` inside a plugin folder | The repo root has the only one. |
| `version` lives only in the plugin's `plugin.json`, and goes up whenever the plugin changes | One number to bump, and without a bump nobody gets the update. |
| `plugin.json` has `name` matching the folder, a version, and an `author` | So installs resolve and people know who owns what. |
| Every `SKILL.md` starts with `name:` and `description:` frontmatter | Claude uses these to find and trigger the skill. |
| Every plugin is in the README table | So teammates can find it. |

To try installing a new plugin without touching your own setup:

```
T="$(mktemp -d)"
CLAUDE_CONFIG_DIR="$T" claude plugin marketplace add "$(pwd)"
CLAUDE_CONFIG_DIR="$T" claude plugin install <name>@p4-product-design
CLAUDE_CONFIG_DIR="$T" claude plugin list
rm -rf "$T"
```

## The safety nets

- **Push guard:** when you push from Claude Code inside this repo, a hook (`.claude/settings.json`) runs `scripts/check.sh` first and blocks a push that fails. Claude Code asks you to trust the folder the first time you open it. Say yes.
- **GitHub check:** every push to `main` runs the same check on GitHub, and it also runs weekly to catch Claude Code rule changes. If it fails, GitHub emails whoever pushed. The badge at the top of the README turns red. Fix it right away, since a broken `main` can stop everyone's sync.
- **Notes for Claude:** [CLAUDE.md](CLAUDE.md) tells anyone's Claude how to work in this repo.

## Don't

- Force-push or rewrite history on `main`.
- Rename the marketplace (`p4-product-design`) or move plugin folders. Both break teammates' installs.
- Rename a published plugin. Add the new one and retire the old one instead.
