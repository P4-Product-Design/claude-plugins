#!/usr/bin/env python3
"""Checks the marketplace layout and the rules that have broken installs before.

Run it through scripts/check.sh, which also runs `claude plugin validate`.
Set BASE to a git ref to turn on the version-bump guard (check.sh does this
for you before a push). Standard library only, so it runs anywhere.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKETPLACE = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
PLUGINS_DIR = os.path.join(ROOT, "plugins")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

errors = []


def fail(msg):
    errors.append(msg)


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        fail(f"{os.path.relpath(path, ROOT)} is missing.")
    except json.JSONDecodeError as e:
        fail(f"{os.path.relpath(path, ROOT)} is not valid JSON: {e}")
    return None


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)


def version_tuple(v):
    return tuple(int(x) for x in v.split("."))


def check_marketplace():
    m = load_json(MARKETPLACE)
    if m is None:
        return {}
    if "description" in m:
        fail('marketplace.json: move the top-level "description" under "metadata". Claude Code rejects it at the top level.')
    if m.get("name") != "p4-product-design":
        fail('marketplace.json: "name" must stay "p4-product-design". Changing it breaks every teammate\'s install.')
    entries = {}
    for p in m.get("plugins", []):
        name = p.get("name", "<no name>")
        if name in entries:
            fail(f"marketplace.json: {name} is listed twice.")
        entries[name] = p
        if p.get("source") != f"./plugins/{name}":
            fail(f'marketplace.json: {name} needs "source": "./plugins/{name}" (got {p.get("source")!r}).')
        if "version" in p:
            fail(f"marketplace.json: remove \"version\" from {name}. The version lives only in plugins/{name}/.claude-plugin/plugin.json.")
        if not p.get("description"):
            fail(f"marketplace.json: {name} needs a description. It's what teammates see on the plugin card.")
    return entries


def check_plugin(name):
    d = os.path.join(PLUGINS_DIR, name)
    pj = load_json(os.path.join(d, ".claude-plugin", "plugin.json"))
    if pj is None:
        return
    if pj.get("name") != name:
        fail(f'plugins/{name}: plugin.json "name" is {pj.get("name")!r}; it must match the folder name.')
    if not SEMVER.match(str(pj.get("version", ""))):
        fail(f'plugins/{name}: plugin.json needs a "version" like 1.2.3.')
    if not (pj.get("author") or {}).get("name"):
        fail(f'plugins/{name}: plugin.json needs "author": {{"name": "<owner>"}} so people know who owns it.')
    if os.path.exists(os.path.join(d, ".claude-plugin", "marketplace.json")):
        fail(f"plugins/{name}: delete .claude-plugin/marketplace.json. The repo root has the only marketplace.")
    for dirpath, _, files in os.walk(os.path.join(d, "skills")):
        if "SKILL.md" in files:
            path = os.path.join(dirpath, "SKILL.md")
            rel = os.path.relpath(path, ROOT)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            fm = re.match(r"^---\n(.*?)\n---", text, re.S)
            if not fm:
                fail(f"{rel}: needs frontmatter between --- lines at the top.")
                continue
            for key in ("name", "description"):
                if not re.search(rf"^{key}:", fm.group(1), re.M):
                    fail(f"{rel}: frontmatter needs a {key}:")


def check_readme(names):
    try:
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            readme = f.read()
    except FileNotFoundError:
        fail("README.md is missing.")
        return
    for n in names:
        if f"plugins/{n}" not in readme:
            fail(f"README.md: add {n} to the plugin table (link it to plugins/{n}).")


def check_version_bumps(base, names):
    if git("rev-parse", "--verify", "--quiet", f"{base}^{{commit}}").returncode != 0:
        print(f"note: skipping the version-bump check ({base} isn't a commit here).")
        return
    for n in names:
        if git("diff", "--quiet", base, "HEAD", "--", f"plugins/{n}").returncode == 0:
            continue
        old = git("show", f"{base}:plugins/{n}/.claude-plugin/plugin.json")
        if old.returncode != 0:
            continue  # new plugin, nothing to compare against
        try:
            old_v = json.loads(old.stdout)["version"]
            new_v = json.loads(git("show", f"HEAD:plugins/{n}/.claude-plugin/plugin.json").stdout)["version"]
        except (KeyError, json.JSONDecodeError):
            continue  # the manifest checks above report this
        if not (SEMVER.match(old_v) and SEMVER.match(new_v)):
            continue
        if version_tuple(new_v) <= version_tuple(old_v):
            fail(f"plugins/{n} changed but its version is still {new_v}. Bump it in plugins/{n}/.claude-plugin/plugin.json "
                 "(patch for fixes, minor for new behavior), or teammates won't get the change.")


def main():
    entries = check_marketplace()
    folders = sorted(n for n in os.listdir(PLUGINS_DIR) if os.path.isdir(os.path.join(PLUGINS_DIR, n)))
    for n in folders:
        if n not in entries:
            fail(f"plugins/{n} isn't listed in .claude-plugin/marketplace.json, so nobody can install it.")
    for n in entries:
        if n not in folders:
            fail(f"marketplace.json lists {n}, but plugins/{n} doesn't exist.")
    for n in folders:
        check_plugin(n)
    check_readme(folders)
    base = os.environ.get("BASE")
    if base:
        check_version_bumps(base, folders)

    if errors:
        print("Marketplace check failed:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"Marketplace check passed ({len(folders)} plugins).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
