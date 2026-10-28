# wordpress-image-prep

Turns Central Testing photos into WordPress-ready images for the Sleep sites: WebP, 800px wide, cropped to at most 450px tall around the subject, with SEO-friendly file names like `seated-edge-support-test-helix-midnight-luxe-mattress.webp`. Handles HEIC and JPG, folders or Dropbox zips, and batches with more than one product.

**Owner:** Chance Chipman. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

- A paid Claude seat and the Claude desktop app (Windows or Mac). Use it in Cowork.
- Python is set up automatically the first time the skill runs.

## Use it

1. Download the photos from Dropbox (a .zip is fine).
2. In Cowork, give Claude access to that folder and ask:

> Prep the images in my Downloads folder for WordPress.

3. Answer Claude's question about which product each group of photos shows.
4. Upload the new folder to the site and write alt text. It's next to the originals and named after the product and the date, e.g. `Helix Midnight Luxe - WordPress 2026-10-28`.

## What's in this plugin

```
wordpress-image-prep/
├── .claude-plugin/plugin.json
├── skills/wordpress-image-prep/
│   ├── SKILL.md                         # the steps Claude follows
│   ├── references/spec-and-decisions.md # why it works the way it does
│   └── scripts/                         # prep.py and its helpers (all the image work)
├── tests/                               # run: python -m unittest discover -s tests
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). Run the tests first.
