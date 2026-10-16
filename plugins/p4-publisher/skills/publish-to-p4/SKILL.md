---
name: publish-to-p4
description: Add a new plugin or skill to the P4 Product Design plugin marketplace (GitHub P4-Product-Design/claude-plugins), or publish an update to one that's already there. Use whenever someone wants to share a skill or plugin with the P4 team, says "publish this to the P4 marketplace", "add my skill to the team plugins", "push my plugin update", "ship the new version of <plugin>", or has edited a P4 plugin and wants teammates to get it. Also use when someone asks how to contribute to the P4 plugins. Keeps the P4-Product-Design GitHub org homepage's plugin list in sync.
---

# Publish to the P4 marketplace

Every P4 plugin lives in one repo, `P4-Product-Design/claude-plugins`, one folder per plugin under `plugins/`. Teammates install from that repo, so whatever lands on `main` reaches everyone on their next sync. That includes anything broken. This skill gets a change there safely.

Work in two modes:
- **Add:** a new plugin goes in a new folder.
- **Update:** a change goes into an existing plugin's folder.

Ask which one if it isn't clear.

## 1. Get a clean, current copy of the repo

1. Look for an existing clone. Ask the person if you can't find one. If there's none, ask where they keep projects, then run:
   ```
   git clone https://github.com/P4-Product-Design/claude-plugins.git
   ```
2. Run `git status`. If there are uncommitted changes that aren't part of this task, stop and ask what to do with them.
3. Run `git pull --rebase`.
4. Read `CLAUDE.md` at the repo root. Its rules apply to everything below.
5. Check the git identity: `git config user.name` and `git config user.email`. If either is empty, ask for the person's name and work email and set them for this repo only, with `git config user.name ...`. Never use `--global`.

## 2a. Add a new plugin

1. **Gather the basics:**
   - **Name:** lowercase-with-hyphens. It becomes the folder, the plugin name, and the install name `<name>@p4-product-design`.
   - **One-sentence description:** it shows on the plugin card.
   - **Owner:** name and email.
   - **Whether there's an existing skill to bring in.** If there is, get the path to its folder (the one with `SKILL.md`), or to a whole plugin folder.

   Check that `plugins/<name>` doesn't already exist.
2. Copy `template/` to `plugins/<name>/`. Rename `skills/PLUGIN-NAME` to `skills/<name>`, unless the plugin's skills have their own names.
3. Bring in the person's files, replacing the template skill:
   - **A skill folder:** copy it into `skills/<skill-name>/`.
   - **A whole plugin:** copy its `skills/`, `commands/`, `agents/`, and `scripts/` folders as they are.
   - Never copy a `marketplace.json` or `.git` folder.
   - Scripts must reference their own files through `${CLAUDE_PLUGIN_ROOT}`. A relative path breaks once the plugin is installed.
4. Fill in `plugins/<name>/.claude-plugin/plugin.json` with the name, description, and owner. Version is `0.1.0` (or `1.0.0` if it's already battle-tested).
5. Fill in `plugins/<name>/README.md`. Delete any section that doesn't apply.
6. Add an entry to `.claude-plugin/marketplace.json`, in alphabetical order:
   ```json
   {
     "name": "<name>",
     "source": "./plugins/<name>",
     "description": "<same sentence as plugin.json>",
     "category": "<design | development | research | content | productivity>"
   }
   ```
   Don't add a `version` here. It lives only in `plugin.json`.
7. Add a row to the plugin table in the root `README.md`, matching the existing rows.

## 2b. Update an existing plugin

1. Confirm which plugin, and make the edits only inside `plugins/<name>/`. If the plugin's `author` isn't the person you're working with, say so before changing it. It's someone else's plugin.
2. Bump `version` in `plugins/<name>/.claude-plugin/plugin.json`:
   - **Patch** (`0.2.0` → `0.2.1`): fixes and wording.
   - **Minor** (`0.2.1` → `0.3.0`): new behavior or new files.
   - **Major:** only when the plugin's skills would break for people who use them the old way.

   Without a bump, teammates never receive the change. The check enforces this.
3. If the description changed, update it in both `plugin.json` and the plugin's entry in `.claude-plugin/marketplace.json`.

## 3. Check it

Run from the repo root:
```
scripts/check.sh
```
Fix everything it reports, then run it again until it passes. Don't work around a failure. Each rule exists because breaking it stopped teammates from installing.

For a new plugin, also do a test install that doesn't touch the person's own setup:
```
T="$(mktemp -d)"
CLAUDE_CONFIG_DIR="$T" claude plugin marketplace add "$(pwd)"
CLAUDE_CONFIG_DIR="$T" claude plugin install <name>@p4-product-design
CLAUDE_CONFIG_DIR="$T" claude plugin list
rm -rf "$T"
```
The plugin should show as installed at the new version.

## 4. Commit and push

1. Show the person `git status` and a short summary of the diff. Get a yes before committing.
2. Commit only the files for this task. Say what changed and why, e.g.:
   - "Add brand-audit plugin"
   - "dev-handoff 0.3.1: fix annotation label escaping"
3. Run `git pull --rebase`, then run `scripts/check.sh` again, since someone else may have pushed.
4. Run `git push`. The repo's hook runs the check again and blocks the push if anything fails.
5. **If the push is rejected for permissions,** the person doesn't have write access yet. Tell them to message Chance with their GitHub username for an invite to the P4-Product-Design org. Leave the commit in place so they can push once they're added.
6. Never force-push, and never rewrite history on `main`.

## 5. Update the org homepage

The org homepage at https://github.com/P4-Product-Design shows the plugin table from a separate repo: `P4-Product-Design/.github`, file `profile/README.md`. Update it whenever a plugin is **added or removed**, or its **"What it does" summary changes**. Skip this step for a version-only update.

1. Find a clone of `P4-Product-Design/.github`, or clone it next to `claude-plugins`:
   ```
   git clone https://github.com/P4-Product-Design/.github.git P4-Product-Design-.github
   ```
   Run `git status` (stop and ask if it has unrelated changes), `git pull --rebase`, and check the repo-local git identity, the same as in step 1.
2. Edit `profile/README.md`:
   - **Added:** add a row to the Plugins table in alphabetical order. Link the name to `https://github.com/P4-Product-Design/claude-plugins/tree/main/plugins/<name>`, and give a one-sentence summary (shorter than the plugin.json description) and the owner, matching the existing rows.
   - **Removed:** delete its row.
   - **Changed:** update the summary in this table and in the claude-plugins `README.md` table, so the two match.
   - If the plugin adds a new kind of work, update the intro sentence that lists the plugin areas ("Figma-to-code, dev handoff, ...").
3. Show the person the diff and get a yes. Then commit (`"Profile: add <name>"`, `"Profile: remove <name>"`, or `"Profile: update <name> summary"`), run `git pull --rebase`, and `git push`. This repo has no check script. Same push access as claude-plugins.
4. Open https://github.com/P4-Product-Design and confirm the table shows the change. The org page can take a minute to refresh.

## 6. Confirm and tell the team

1. Check the GitHub check: https://github.com/P4-Product-Design/claude-plugins/actions. Wait a couple of minutes for the newest run to go green. If it fails, read the log and fix it.
2. Give the person a short message they can post. Include:
   - What's new, and the version.
   - Who it's for.
   - **For a new plugin:** "In Claude Desktop, go to Customize → Plugins → the p4-product-design tab and click + on <name>."
   - **For an update:** "You'll get it automatically on your next sync, or now via Customize → Manage plugins."
