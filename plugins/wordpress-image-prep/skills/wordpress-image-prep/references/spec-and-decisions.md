# WordPress Image Prep: design spec

**Date:** 2026-10-28
**Owner:** Chance Chipman
**Requested by:** Mel Kassel (Managing Editor, Sleep)
**Ticket:** [Claude skill for converting images](https://app.notion.com/p/3fa930dda5e0809193dee79f7b8258be)
**Status:** draft. Implementation waits on Chance's review.

## 1. Purpose

The Sleep editorial team publishes Central Testing (CT) photos on Sleepopolis, Mattress Clarity, Mattress Nerd and Sleep Advisor. CT drops the photos in Dropbox as large HEIC or JPG files with camera names like `IMG_1949.HEIC`, often 50+ per product. Today writers convert, resize and rename each batch by hand with online tools, which takes hours.

The skill turns a folder of CT photos into WordPress-ready images in one step: converted to WebP, resized, cropped and given an SEO-friendly name.

**Users:** writers, editors and the publisher on the Sleep content team. Most have barely used Claude, and most are on Windows. The skill has to work from plain requests like "prep these images for WordPress" with no settings to learn.

## 2. Scope

**In scope**
- Input: a folder, or a Dropbox `.zip`, of HEIC, HEIF, JPG, JPEG or PNG files, any number.
- Convert to WebP, resize, crop and rename (sections 4–6).
- Work out which product each photo shows, including batches with more than one product (section 5).
- Write the results to a new folder and report what was done (section 7).

**Out of scope**
- Alt text. Writers still write it in WordPress.
- Uploading to WordPress.
- Videos and other non-image files. They're skipped and listed.
- Connecting to Dropbox. Writers download the files first.
- Editing the photos themselves (colour, retouching, background removal).

## 3. User flow

1. The writer downloads the photos from Dropbox to their computer. A `.zip` is fine.
2. In the Claude desktop app (Cowork), they point Claude at the folder or zip: "Prep the images in Downloads/Helix Midnight Luxe for WordPress."
3. Claude scans the batch and works out the product for each photo. It asks only about photos it can't place (section 5).
4. Claude processes every image and writes the new folder.
5. Claude shows a table: original name → new name, product, where the product name came from, and final size. Skipped files are listed below it.
6. The writer uploads the new folder to WordPress and writes alt text.

## 4. Image processing rules

Applied to every image, in this order:

1. **Decode.** HEIC/HEIF go through `pillow-heif`. JPG and PNG go through Pillow.
2. **Orientation.** Apply the EXIF orientation flag (`ImageOps.exif_transpose`). This matters: `IMG_7976.JPG` in the test set is stored upside down (orientation 3) and comes out flipped if the flag is ignored. If Claude sees a photo is still sideways after this (no flag set), it can request a 90°, 180° or 270° rotation in the manifest.
3. **Resize.** Scale to 800px wide, keeping the aspect ratio, with Lanczos resampling. **Never upscale.** A photo narrower than 800px keeps its width.
4. **Crop.** If the result is taller than 450px, crop to 450px tall. The crop window is centred on the subject's vertical position (`focus_y` in the manifest, 0 = top and 1 = bottom), clamped so it stays inside the image. Claude sets `focus_y` by looking at each photo. Default is 0.5. Images 450px tall or shorter aren't cropped. Width is never cropped.
5. **Colour.** Convert to sRGB. iPhone HEICs are Display P3, so embedded ICC profiles are converted rather than dropped, so colours don't shift.
6. **Encode.** WebP, quality 90, method 6.
7. **Metadata.** Strip all EXIF, GPS and XMP. iPhone photos carry the test facility's location.

A 4:3 iPhone photo becomes 800×600 and is then cropped to 800×450. Every photo in the test set needs the crop.

## 5. Working out the product

A batch may hold more than one product, so the skill never asks a single "which product is this?" for the whole batch. For each photo it uses the first source that gives an answer:

1. **File name.** If CT added a product name (e.g. `Helix Midnight Luxe IMG_1949.HEIC`), use it. CT is expected to start doing this; Mel is confirming with CT.
2. **Subfolder name.** If the photo sits in a subfolder *inside* the input that's named for a product (e.g. `Batch/Helix Midnight Luxe/`), use the subfolder name. Generic names like `Images`, `Photos`, `Testing`, `HEIC` or dates don't count. The input folder's own name is never used automatically, because it's often something like `Central Testing Images` or `Downloads`. If it looks like a product name, Claude offers it as the suggested answer in step 3.
3. **Shoot group, then ask.** The remaining photos are grouped by photo shoot. The script sorts them by EXIF `DateTimeOriginal` and camera model, and starts a new group when the camera changes or there's a gap of more than 30 minutes. Claude then checks each group's contact sheet and splits a group if the set, bed frame or product clearly changes partway. It asks about all unresolved groups in one message. Each group is described by photo count, date, setting and any logo or label Claude can read, followed by its original file names:
   > **Group 1:** 5 photos, Jun 19, bedroom set, "DLX" logo on the side panel. Which product is this?

   The writer can answer with a product name, "same as Group 1", or "mixed". "Mixed" makes Claude ask about each photo in that group one at a time.

**Rules**
- Never fill in a product name from a logo or label alone. What Claude reads only goes into the question as a suggestion.
- If sources disagree, for example the file name says one product and the folder another, ask rather than pick.
- Photos without EXIF dates form their own group.
- Product names are normalised for the file name (section 6), but the report shows them as the writer typed them.

## 6. Naming

**Pattern:** `{description}-{brand}-{model}-{category}.webp`

Description first, then the product, then the product category (`mattress`, `pillow`, `topper`, `sheets` and so on). Example: `seated-edge-support-test-helix-midnight-luxe-mattress.webp`.

**SEO rules**
- Lowercase ASCII letters and digits, with hyphens between words. No spaces, underscores or accents (`é` → `e`).
- **Keep keywords people search for:** brand, model, product category, and the test or feature name. Use the standard terms below so names stay consistent across writers.
- **Remove filler words:** a, an, the, of, on, in, at, to, for, with, and, is, are, being, our, its, this, that. Keep words that change the meaning: before, after, under, vs, side, back, stomach.
- **Leave out:** tester names, camera names (`IMG_1949`), dates, sizes (`-768x432`), and words that add nothing (`image`, `photo`, `picture`).
- **Length:** aim for 60 characters or fewer before `.webp`, with a hard limit of 80. Shorten the description first and never cut the product name.
- **Describe, don't stuff:** one short phrase about what's in the photo. Don't repeat the keyword.
- **Duplicates:** the first photo gets no number. Later ones get `-2`, `-3` and so on, in original file order. WordPress handles any collisions with files already uploaded.

**Standard test and feature terms** (with the photo that each describes)

| Term | Photo shows |
|---|---|
| `side-sleeper-test`, `back-sleeper-test`, `stomach-sleeper-test`, `combination-sleeper-test` | Tester lying in that position |
| `seated-edge-support-test`, `lying-edge-support-test` | Tester sitting or lying on the edge |
| `edge-sinkage-test` | Weights or a tape measure at the edge |
| `pressure-map` | Pressure-mapping mat or its screen |
| `thermal-imaging-before-use`, `thermal-imaging-after-use` | Heat-camera image |
| `motion-isolation-test` | Glass of water, bowling ball or drop test |
| `partner-test` | Two testers on the mattress |
| `firmness-test` | Hand press or firmness gauge |
| `inside-layers` | Cover unzipped, layers showing |
| `cover-closeup`, `side-panel-logo`, `handles` | Close-up of a detail |
| `full-view` | Whole product, nothing being tested |
| `unboxing`, `expanding-after-unboxing` | Box, plastic, compressed product |

Claude can use a plain description when no term fits (`pillow-loft-measurement`), following the same rules.

**Test set, with `dlx` standing in for the product name**

| Original | New name |
|---|---|
| IMG_1949 2.HEIC | `side-sleeper-test-dlx-mattress.webp` |
| IMG_1954 2.HEIC | `seated-edge-support-test-dlx-mattress.webp` |
| IMG_1955 2.HEIC | `inside-layers-dlx-mattress.webp` |
| IMG_1957 2.HEIC | `side-panel-logo-dlx-mattress.webp` |
| IMG_1959 2.HEIC | `full-view-dlx-mattress.webp` |
| IMG_7976.JPG | `unboxing-dlx-mattress.webp` |
| IMG_7979.jpg | `expanding-after-unboxing-dlx-mattress.webp` |

## 7. Output

- **Location:** a new folder next to the input folder or zip, named `<input name> - WordPress`. If that name is taken, use `<input name> - WordPress (2)`, and so on. Never overwrite anything, and never change the originals. If the input is inside a synced Dropbox folder, the output syncs back on its own.
- **Contents:** only the `.webp` files. No logs or sidecar files.
- **Report in chat:** a table of original → new name, product, product source (file name, folder, or "you told me"), and final pixel size. Below it: skipped files with the reason, and the total size before and after.

## 8. How it's built

A plugin in the P4 marketplace, `plugins/wordpress-image-prep/`, laid out like `swolverine-product-photos`:

```
plugins/wordpress-image-prep/
  .claude-plugin/plugin.json
  README.md
  skills/wordpress-image-prep/
    SKILL.md                       # flow, product and naming rules, how to ask
    scripts/prep.py                # CLI: installs dependencies, runs scan and apply, prints JSON
    scripts/naming.py              # file-name rules and de-duplication
    scripts/imaging.py             # open upright in sRGB, resize, crop, save WebP
    scripts/inventory.py           # find files, unzip, metadata, name hints, shoot groups, output folder
    scripts/sheets.py              # contact sheets
    references/spec-and-decisions.md   # this spec, kept current
  tests/                           # unittest suite for the scripts
```

**Who does what.** Claude makes the judgment calls: product, description, `focus_y`, extra rotation. The script does everything else, the same way every time, so it can be tested without Claude.

**`prep.py scan <folder-or-zip>`**
- Unzips a zip into a temporary folder.
- Lists every file. Images get: path, pixel size, EXIF orientation, `DateTimeOriginal`, camera model, and a product name if one is found in the file or folder name. Other files go on a skipped list with the reason.
- Proposes shoot groups (section 5).
- Writes contact sheets: 6 numbered thumbnails per sheet, each about 600px wide and already turned upright, with a line showing where an 800×450 centre crop would fall. Claude views the sheets, not the full-size files, which keeps a 50-photo batch to about 9 images. Claude can still open a single photo larger when it needs a closer look.
- Prints JSON for Claude.

**`prep.py apply [--preview] <manifest.json>`**
- Manifest: the output folder, plus for each image its source path, new file name, `focus_y`, and optional `rotate`.
- `--preview` writes into the temporary work folder instead. Claude previews first, checks the crops, adjusts `focus_y`, and only then writes the real folder. That way the real folder is written once.
- Checks the manifest (names follow section 6, no duplicates, `focus_y` between 0 and 1), then processes each image (section 4).
- Writes a crop-check contact sheet of the finished files for Claude to look over before reporting.
- Prints JSON: per file, the output path, size in pixels and KB, or an error.

**Dependencies.** Python 3 with Pillow and `pillow-heif`. The skill installs `pillow-heif` with pip on first run if it's missing. If HEIC still can't be opened, macOS falls back to `sips`. On any other system the skill stops with a plain message naming the files it couldn't open, and still processes the JPGs and PNGs.

## 9. Error handling

| Situation | Behavior |
|---|---|
| File can't be opened (corrupt, unsupported) | Skip it, list it with the reason, keep going |
| Video, PDF or other non-image file | Skip and list |
| Image narrower than 800px | Keep its size, crop height only if over 450px, note it in the report |
| Output folder name taken | Add ` (2)`, ` (3)` and so on |
| No images found | Say so, list what was found, write nothing |
| Writer cancels partway through the product questions | Write nothing |
| `pillow-heif` won't install | macOS falls back to `sips`. Elsewhere, process JPG/PNG and list the HEICs that weren't done |

## 10. Testing

**Test set:** the 5 HEIC and 2 JPG files in `~/Desktop/Central Testing Images/`. They come from two shoots: 5 HEICs on an iPhone 12 Pro Max on 2025-06-19 in the bedroom set, and 2 JPGs on an iPhone 15 Pro Max on 2025-05-21 in the warehouse.

**Script checks** (run without Claude):
- Every output is `.webp`, exactly 800×450.
- `IMG_7976` comes out right side up.
- No EXIF or GPS data in any output.
- Originals unchanged (checksums match before and after).
- `scan` proposes two groups (5 and 2).
- Re-running doesn't overwrite; it creates `… - WordPress (2)`.
- A 600px-wide test image isn't upscaled.
- A `.mov` in the folder is skipped and listed.

**Skill checks** (run in Cowork):
- With the current file names, Claude asks about exactly two groups.
- With product names added to the file names, Claude asks nothing.
- With two products' names mixed into one folder, each photo gets the right product.
- Names follow section 6.
- Chance reviews the crop-check sheet. Heads and hands in `IMG_1954` and `IMG_1955` must stay in frame.

**Pilot:** Mel runs one real batch on Windows before rollout.

## 11. Rollout

1. Publish to the P4 marketplace (`publish-to-p4`).
2. Mel asks Meredith Massey, who manages Claude seats, for seats for the content team.
3. Chance helps Mel add the skill to her account, then Mel pilots it on Windows.
4. Chance helps the rest of the team (writers, editors, the publisher) add the skill after the pilot.
5. Write a one-page how-to for writers, editors and the publisher. It covers adding the skill, downloading, pointing Claude at the folder, answering product questions and uploading. Store it with the team's image guidelines.

## 12. Open items

| Item | Owner |
|---|---|
| Will CT add product names to file names? The skill works either way; product names just mean fewer questions. | Mel, with CT |
| Paid Claude seats for the content team | Mel, with Meredith Massey |
| HEIC decoding in Cowork on Windows is untested | Mel's pilot |
| Plugin name `wordpress-image-prep` is permanent once published (plugins can't be renamed) | Chance |
