---
name: wordpress-image-prep
description: Turns Central Testing photos (HEIC, JPG or PNG, usually straight from Dropbox) into WordPress-ready images for the Sleep sites (Sleepopolis, Mattress Clarity, Mattress Nerd, Sleep Advisor). It converts to WebP at 800px wide, crops to at most 450px tall around the subject, strips location data, and renames each file with an SEO-friendly description plus the product name. Works on a folder or a Dropbox .zip of any size, including batches that mix several products. Use whenever someone wants testing photos converted, resized, cropped, compressed, renamed or "prepped" for WordPress or the media library, even if they only say "prep these images", "get these photos ready to upload", "convert these HEICs", "resize the testing pics" or "do the new CT photos".
---

# WordPress image prep

You're helping a writer, editor or publisher on the Sleep content team get Central Testing (CT) photos ready for WordPress. Most of them rarely use Claude and aren't technical.
- Talk plainly.
- Never show them JSON, commands, or paths from the temporary work folder.
- Ask only what you need, in as few questions as possible.

Every photo ends up as a `.webp`, 800px wide (never enlarged) and at most 450px tall, with the crop placed so the subject stays in frame. The file name says what's in the photo and which product. The originals are never changed. Nothing is uploaded; the writer uploads the new folder and writes alt text themselves.

## 1. Get the input

Ask for the folder or `.zip` if they haven't said which. Accept either. If they downloaded several things, ask which one.

## 2. Scan

```bash
python3 "<this skill's base directory>/scripts/prep.py" scan "<folder or zip>"
```

The JSON gives:
- `images`: index, path, size, `taken`, `camera`, `filename_hint`, `subfolder_hint`, `group`.
- `groups`: shoot groups.
- `skipped`: videos, other files, and anything unreadable.
- `sheets`: contact sheets.
- `output_parent` (where the new folder will go), `work_dir`, `heic_decoder`, `notes`.

If `heic_decoder` is null, HEIC files can't be processed on this computer. They'll be in `skipped`. Tell the writer in one sentence and carry on with the rest.

If `images` is empty, tell the writer what you did find (from `skipped`) and stop. Write nothing.

## 3. Look at every contact sheet

Open each sheet in `sheets` (6 numbered photos per sheet, ordered by shoot group). The red lines show where a centre crop would fall. For each photo, decide:
- **What's happening**, using the standard terms in section 5 where one fits.
- **`focus_y`**: the vertical centre of what matters, from 0 (top) to 1 (bottom). That's the tester's face and hands, the edge being pressed, the pressure map, the logo. Use 0.5 when the subject is already between the red lines. Nudge it up or down when the lines would cut through a head, hands, or the thing being tested.
- **`rotate`**: only if a photo still looks sideways or upside down on the sheet. Use 90, 180 or 270, clockwise.

## 4. Work out the product for every photo

A batch can hold more than one product. Never ask one question for the whole batch.

For each photo, use the first source that answers:
1. **`filename_hint`**: CT may put the product name in the file name. Use the product part (e.g. "Helix Midnight Luxe" from "helix midnight luxe edge support seated1").
2. **`subfolder_hint`**: a product-named subfolder inside the input.
3. **Ask, per shoot group.** Check that each group really is one product: same set, same bed frame, same product throughout. Split it if not. Then ask about all the unresolved groups in **one message**, like this:

   > I found 7 photos from 2 photo shoots. Which product is in each?
   > **Group 1:** 5 photos from Jun 19, bedroom set with a black bed frame; I can see a "DLX" logo on the side. (IMG_1949, IMG_1954, IMG_1955, IMG_1957, IMG_1959)
   > **Group 2:** 2 photos from May 21, unboxing in the warehouse. (IMG_7976, IMG_7979)
   >
   > You can answer with a product name, "same as Group 1", or "mixed" if a group has more than one product.

Rules:
- A logo or label you read is only a suggestion in the question. **Never fill in a product from it on your own.**
- If the input folder's own name looks like a product, offer it as the suggested answer. Don't use it on its own.
- If the file name and the subfolder disagree, ask.
- "Mixed" means ask about each photo in that group, a few at a time, by file name.
- If the writer stops or cancels, write nothing.

## 5. Name every photo

Pattern: `{description}-{brand}-{model}-{category}`. Description first, then the product, then the category word (`mattress`, `pillow`, `topper`, `sheets`, `bed-frame` and so on). Don't add `.webp` or a number; the script adds both.

- Use **lowercase words**. The script turns spaces into hyphens and removes accents.
- **Keep words people search for:** brand, model, category, and the test or feature.
- **Remove filler words:** a, an, the, of, on, in, at, to, for, with, and, is, are, being, our, its, this, that. The script removes these anyway.
- **Keep words that change the meaning:** before, after, under, vs, side, back, stomach.
- **Leave out:** tester names, camera names (`IMG_1949`), dates, sizes (`768x432`), and "image", "photo" or "picture".
- **Length:** aim for 60 characters or fewer; 80 is the limit. Shorten the description, never the product name.
- **Describe, don't stuff:** use one short phrase and don't repeat keywords.

| Term | Use when the photo shows |
|---|---|
| `side-sleeper-test`, `back-sleeper-test`, `stomach-sleeper-test`, `combination-sleeper-test` | A tester lying in that position |
| `seated-edge-support-test`, `lying-edge-support-test` | A tester sitting or lying on the edge |
| `edge-sinkage-test` | Weights or a tape measure at the edge |
| `pressure-map` | A pressure-mapping mat or its screen |
| `thermal-imaging-before-use`, `thermal-imaging-after-use` | A heat-camera image |
| `motion-isolation-test` | A glass of water, bowling ball or drop test |
| `partner-test` | Two testers on the product |
| `firmness-test` | A hand press or firmness gauge |
| `inside-layers` | The cover open, with layers showing |
| `cover-closeup`, `side-panel-logo`, `handles` | A close-up of a detail |
| `full-view` | The whole product, nothing being tested |
| `unboxing`, `expanding-after-unboxing` | A box, plastic, or the product still compressed |

If no term fits, write a short plain description that follows the same rules (e.g. `pillow-loft-measurement`).

Examples: `seated-edge-support-test-helix-midnight-luxe-mattress`, `thermal-imaging-after-use-brooklyn-bedding-aurora-luxe-mattress`, `unboxing-saatva-classic-mattress`.

## 6. Write the manifest and preview

Save `manifest.json` in `work_dir`:

```json
{
  "output_parent": "<output_parent from the scan>",
  "images": [
    {"source": "<path from the scan>", "name": "seated-edge-support-test-helix-midnight-luxe-mattress", "product": "Helix Midnight Luxe", "focus_y": 0.35, "rotate": 0}
  ]
}
```

List the images in scan order. `product` is the product as the writer typed it (or as it appears in the file or folder name), spelled the same way for every photo of that product. The script names the new folder after it. Then run a preview:

```bash
python3 "<this skill's base directory>/scripts/prep.py" apply --preview "<work_dir>/manifest.json"
```

- If `ok` is false, fix each item in `problems` and run the preview again.
- Open every image in `check_sheets`. Each crop must keep the subject: heads, hands, the edge being tested, the readout. If a crop cuts something off, change that photo's `focus_y` (lower moves the crop up, higher moves it down) and preview again.

## 7. Write the real folder

```bash
python3 "<this skill's base directory>/scripts/prep.py" apply "<work_dir>/manifest.json"
```

This creates a new folder next to the originals, named after the products and today's date, so back-to-back batches never share a folder:
- one product: `Helix Midnight Luxe - WordPress 2026-10-28`
- two: `Helix Midnight Luxe + DLX Mattress - WordPress 2026-10-28`
- three or more: `Helix Midnight Luxe + 2 more - WordPress 2026-10-28`

If that name is taken (the same product twice in one day), it adds ` (2)`. It never overwrites anything. The folder's path is `output_dir` in the result.

## 8. Report

Tell the writer the new folder's name and where it is, then show a table:

| Original | New name | Product | Product from | Size |
|---|---|---|---|---|

"Product from" is "file name", "folder" or "you told me". Then list:
- skipped files and why (videos are expected);
- any `error` results;
- photos under 800px wide, which were kept at their own width;
- total size before and after.

End with one line reminding them to write alt text in WordPress.

## Rules

- Never change, move or delete the originals. Never upload anything.
- Never guess a product from a logo alone.
- Always look at the check sheets before the real run.
- If something fails, say plainly what happened and what you need from them.
