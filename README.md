# figma-to-optimizely

Claude Code plugin that converts Figma designs into production-ready Optimizely Web Experiment widgets (HTML, CSS, JS, `widget.json`) with a local preview server.

## What it does

You hand Claude a Figma URL. Claude reads the design through Figma MCP, generates the four files Optimizely needs, and spins up a local preview in your browser so you can eyeball the widget before sending it to the engineer.

Output for every experiment:

- `index.html` — widget markup using `{{extension.fieldName}}` template variables
- `styles.css` — scoped CSS, transparent root background, three responsive breakpoints
- `script.js` — Optimizely widget API for mounting and targeting
- `widget.json` — widget config with `form_schema` defining every editable field

## Install (Claude Code desktop app)

You only need Claude Code open. Type these two commands into the chat input:

```
/plugin marketplace add P4-Product-Design/figma-to-optimizely-plugin
/plugin install figma-to-optimizely
```

That's it. The slash commands appear in your menu next time you open Claude Code.

## Prerequisite: Figma MCP

This plugin reads designs through Figma MCP. Install the official Figma plugin first (one-time setup):

```
/plugin marketplace add anthropics/claude-code
/plugin install figma
```

Then sign into Figma when Claude prompts you.

## How to use it

### 1. Convert Figma to widget code

Paste your Figma frame URL and run:

```
/figma-to-optimizely https://www.figma.com/design/<fileKey>/...?node-id=<nodeId> <experiment-name>
```

Claude will:

1. Create the folder `experiments/<experiment-name>/output/Optimizely/` if it doesn't exist
2. Read the design through Figma MCP (desktop, tablet, mobile if available)
3. Generate `index.html`, `styles.css`, `script.js`, `widget.json`, plus a local `preview.html`
4. Spin up a local preview server and open it in your browser
5. Wait for you to confirm it looks right before reporting done

### 2. QA an existing experiment

```
/qa-widget expandable-pbl
```

Runs the constraints checklist (no React, scoped CSS, all template fields wired up, etc.) and updates `qa/implementation-notes.md`.

## Handing off to the engineer

The deliverable is the contents of `experiments/<name>/output/Optimizely/`. Zip the folder or paste each file's contents into Optimizely's widget editor.

## Updating the plugin

When a new version ships:

```
/plugin marketplace update figma-to-optimizely
```

Then restart Claude Code.
