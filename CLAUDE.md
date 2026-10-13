# Working in the P4 plugin marketplace

This repo is the one Claude plugin marketplace the whole P4 Product Design team installs from. Its name is `p4-product-design`. Each plugin is a folder in `plugins/`. **Whatever is on `main` reaches every teammate on their next sync.** A broken manifest stops everyone's install. A change without a version bump reaches no one.

If the person wants to add or publish a plugin, use the `publish-to-p4` skill from the p4-publisher plugin if it's installed. Otherwise follow CONTRIBUTING.md, which has the same steps.

## Rules

- **Stay in scope.** Edit only the plugin folder the person asked about. Before changing another owner's plugin (`author` in its `plugin.json`), or a root file (`.claude-plugin/marketplace.json`, `scripts/`, `.github/`, `.claude/`, this file), say what you're about to change and why.
- **Start current.** Run `git pull --rebase` before making changes, and again right before pushing. Several people push to `main` directly.
- **Bump the version** in `plugins/<name>/.claude-plugin/plugin.json` whenever anything in that plugin changes:
  - **Patch:** fixes and wording.
  - **Minor:** new behavior.
  - **Major:** existing use of the plugin breaks.

  The version lives only there. Never add `version` to `marketplace.json`.
- **Adding a plugin:**
  - Copy `template/` to `plugins/<name>/`.
  - Add an entry in alphabetical order to `.claude-plugin/marketplace.json` with `"source": "./plugins/<name>"`.
  - Add a row to the README plugin table.
- **Manifest rules.** Each one broke installs before:
  - `source` is always `"./plugins/<name>"`. Claude Code rejects `"."`.
  - No top-level `description` in `marketplace.json`. It goes under `metadata`.
  - No `marketplace.json` inside a plugin folder.
  - Never rename the marketplace, a plugin, or a plugin folder.
- **Scripts reference their own files** through `${CLAUDE_PLUGIN_ROOT}/...`. A relative path resolves against the user's working directory, not the plugin.
- **Run `scripts/check.sh` and fix everything it reports before pushing.** The project hook runs it on `git push` and blocks failures. Fix the cause. Never bypass the hook or edit the check to make a failure pass.
- **Commits:**
  - Use a repo-local git identity: `git config user.name` and `user.email`, never `--global`. Ask the person if it's unset.
  - Write a message saying what changed and why. Use `"<plugin> <version>: <change>"` for updates.
  - Show the person what you'll commit, and get a yes before committing.
- **Never force-push, rewrite history on `main`, or delete branches or tags you didn't create.**

## After pushing

1. Check https://github.com/P4-Product-Design/claude-plugins/actions, where the newest "Marketplace check" run should go green. If it fails, fix it right away.
2. Tell the person the plugin and new version, and how teammates get it:
   - **Updates:** automatic on their next sync, or via Customize → Manage plugins.
   - **New plugins:** Customize → Plugins → the p4-product-design tab, then + on the card.

## Layout

```
.claude-plugin/marketplace.json   # the only marketplace: one entry per plugin
plugins/<name>/                   # one plugin per folder, with its own plugin.json and version
template/                         # starter plugin for new ones
scripts/check.sh                  # the check (hook, GitHub, and you all run it)
scripts/check.py                  # the rules check.sh runs
scripts/pre-push-hook.sh          # blocks `git push` when the check fails
.claude/settings.json             # wires up that hook
.github/workflows/check.yml       # same check on GitHub: every push, plus weekly
```
