# swolverine-product-photos

A Claude Code plugin that turns raw studio shots of Swolverine (SWOL) supplement packaging into website-ready product images: a cut-out on a 3247px transparent canvas with the house tone curve and a soft contact shadow, saved as an sRGB PNG (plus a small WebP) for the site and a layered 16-bit TIFF master.

It reproduces the look Chance built by hand in Photoshop. **It never uses generative fill, AI upscaling or inpainting.** Every step only masks, moves, resamples or tone-maps real camera pixels, so label fine print (the Net Wt line, nutrition facts, Lot/EXP) survives untouched.

**Owner:** Chance Chipman. Install it from the [P4 plugin marketplace](../../README.md#install-one-time-per-person), which has every P4 plugin in one place.

## Prerequisites

1. **A Mac with Adobe Photoshop 2026.** The pipeline drives Photoshop through AppleScript (Select Subject for the mask, and building the layered TIFF). It won't run on Windows or Linux. If your Photoshop has a different name, set `SWOL_PS_APP` (for example `SWOL_PS_APP="Adobe Photoshop 2027"`).
2. **Python 3.** The skill builds a private virtualenv at `~/.cache/swolverine-product-photos/venv` (numpy, opencv, tifffile, pillow, scipy) the first time it runs.
3. **Your own product-images folder.** It holds `Raw/` (camera TIFFs named `<Product>-<View>.tif`), `WIP/` (layered masters) and `Final/` (web images: `Final/PNG/` and `Final/WebP/`). Each of `WIP/`, `Final/PNG/` and `Final/WebP/` has a `Bundles/` subfolder for group shots. Nothing in this plugin is tied to anyone's location. Tell it where yours is by any one of:
   - `export SWOL_PHOTO_ROOT="/path/to/your/Product images"` in your shell
   - saving `{"root": "/path/to/your/Product images"}` in `~/.config/swolverine-product-photos/config.json`
   - passing `--root /path/to/folder` on each run

   If none is set, the script stops and says so. Claude will ask you for the folder.

## Use it

Point Claude at new raws and ask for the usual treatment, e.g.:

> Process the new shots in my Raw folder, same as the creatine and whey ones.

or "do the next product", or "make these look like the other product images". Claude previews the raws, cuts out the product, matches exposure to the house podium, renders, and runs QA crops on the fine print. **It stops for your approval before anything is written to `Final/` or `WIP/`**, and never overwrites an existing export unless you say so.

**Edited a master by hand?** If you retouch a layered TIFF in `WIP/` (say, trim the bottom of a bag), the shadow stays where the old edge was. Ask Claude to "reshadow" it. It shows you a before/after first. Once you approve, it swaps only the Shadow layer, checks that nothing else in the file changed, and refreshes the PNG and WebP. The old files go to `WIP/Previous versions/`.

**Exposure matching.** Exposure is matched per capture session (the EXIF capture date). `assets/config.json` holds the approved gain for each known session and the reference raw it was measured against. If a reference raw isn't in your `Raw/` or `Archive/` folder, the approved session gain is still applied, but within-session exposure drift isn't corrected, and the script says so. A new session gets an estimated gain only; check it against the existing Finals and get the look approved before adding it to `config.json`.

## What's in this plugin

```
swolverine-product-photos/
├── .claude-plugin/
│   └── plugin.json         # plugin manifest
├── skills/
│   └── swolverine-product-photos/
│       ├── SKILL.md                 # the skill: rules, folder layout, and the step-by-step run
│       ├── scripts/
│       │   ├── setup.sh             # one-time Python environment setup
│       │   └── swolphoto.py         # the pipeline (preview, mask, podium-cut, render, qa, export, ...)
│       ├── assets/
│       │   ├── config.json          # house spec and approved capture-session gains
│       │   ├── look_curves.json     # tone curve points
│       │   ├── tone_lut.npy         # tone lookup table
│       │   ├── shadow_template.npz  # the contact shadow, lifted from the old website image
│       │   └── AdobeRGB1998.icc     # colour profile for the raws
│       └── references/
│           ├── spec-and-decisions.md       # why each number in config.json is what it is
│           ├── troubleshooting.md          # Photoshop crashes, mask problems, fixes
│           └── multiview-outline-match.md  # matching several views to one approved outline
└── README.md
```

## Updating this plugin

Edit the files in this folder, bump `version` in `.claude-plugin/plugin.json`, and push to `main`. Teammates get the new version on their next sync. The full steps are in [CONTRIBUTING.md](../../CONTRIBUTING.md). In Claude Code, you can also ask Claude to "publish my update to the P4 marketplace".

The house look in `assets/config.json` (canvas, baseline, tone curve, contact shadow, session gains) should only change with Chance's sign-off.
