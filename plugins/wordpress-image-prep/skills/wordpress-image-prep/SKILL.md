---
name: wordpress-image-prep
description: Turns Central Testing photos (HEIC, JPG or PNG, usually straight from Dropbox) into WordPress-ready WebP images for the Sleep sites (Sleep Advisor, Mattress Nerd, Mattress Clarity, Sleepopolis) and the Fitness sites (Garage Gym Reviews, BarBend), 800px wide, cropped to at most 450px tall around the subject, location data stripped, with SEO file names, a review page and a draft alt-text file. Format, size and naming are the team's fixed standard, so load this skill before asking anything and never ask about them; the one setup question is Sleep or Fitness. Works on a folder or a Dropbox .zip of any size, including batches with several products. Use whenever someone wants testing photos converted, resized, cropped, compressed, renamed or "prepped" for WordPress or the media library, even if they only say "prep these images", "get these photos ready to upload", "convert these HEICs", "resize the testing pics", "do the new CT photos" or name a site like GGR or BarBend.
---

# WordPress image prep

You're helping a writer, editor or publisher on the Sleep or Fitness content team get Central Testing (CT) photos ready for WordPress. Most of them rarely use Claude and aren't technical.
- Talk plainly.
- Never show them JSON, commands, or paths from the temporary work folder.
- Ask only what you need, in as few questions as possible.

**The output settings are fixed. Never ask about them, and don't offer options or alternatives:** WebP (no JPG), 800px wide, at most 450px tall, quality 90, metadata stripped, and names in the patterns in section 5. If the writer asks for something different, explain that this is the team's WordPress standard. The only things you ever ask are whether the images are for a Sleep or a Fitness site and which folder or zip, if they didn't say (section 1); which product a group of photos shows (section 4); and, at the end, whether the finished images look right (section 8).

Every photo ends up as a `.webp`, 800px wide (never enlarged) and at most 450px tall, with the crop placed so the subject stays in frame. The file name says what's in the photo and which product. Beside the folder go a review page and a draft alt-text file per product. The originals are never changed. Nothing is uploaded; the writer uploads the new folder and pastes in the alt text.

## 1. Get the site type and the input

**Confirm Sleep or Fitness before running anything.** The two use different naming rules (section 5).

| Site type | Sites |
|---|---|
| Sleep | SA Sleep Advisor, MN Mattress Nerd, MC Mattress Clarity, SO Sleepopolis |
| Fitness | GGR Garage Gym Reviews, BB BarBend |

- Skip the question only if the writer already said "Sleep" or "Fitness", or named one of these sites (by name or abbreviation).
- **Never work it out from the photos.** A mattress or a cold plunge in the pictures doesn't settle it.
- Ask for the folder or `.zip` too if they haven't said which. Accept either, and if they downloaded several things, ask which one.
- Put both questions in one message, for example:

  > Are these for a Sleep site (Sleep Advisor, Mattress Nerd, Mattress Clarity, Sleepopolis) or a Fitness site (Garage Gym Reviews, BarBend)?

The answer goes in the manifest as `"site_type": "sleep"` or `"fitness"`. The script refuses to run without it.

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
- **What's happening**, using the standard terms in section 5 for Sleep, or a descriptive phrase for Fitness. Note what's visible for the alt text (section 6) too.
- **`focus_y`**: the vertical centre of what matters, from 0 (top) to 1 (bottom). That's the tester's face and hands, the edge being pressed, the pressure map, the logo. Use 0.5 when the subject is already between the red lines. Nudge it up or down when the lines would cut through a head, hands, or the thing being tested.
- **`rotate`**: only if a photo still looks sideways or upside down on the sheet. Use 90, 180 or 270, clockwise.

## 4. Work out the product for every photo

A batch can hold more than one product. Never ask one question for the whole batch.

For each photo, use the first source that answers:
1. **`filename_hint`**: CT may put the product name in the file name. Use the product part (e.g. "Helix Midnight Luxe" from "helix midnight luxe edge support seated1").
2. **`subfolder_hint`**: a product-named subfolder inside the input.
3. **Ask, per shoot group.** Check that each group really is one product: same set, same bed frame or rack, same product throughout. Split it if not. Then ask about all the unresolved groups in **one message**, like this:

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

Don't add `.webp` or a number; the script adds both, numbering repeats `-2`, `-3` in order. **Both site types:**
- Write versions as given, with the dot. The script drops a trailing `.0` (Stoic 3.0 → `stoic-3`) and keeps any other version (2.5 → `2-5`).
- Never use a tester's real name, a camera name (`IMG_1949`), dates, sizes (`768x432`), or "image", "photo" or "picture".
- 80 characters is the limit. Shorten the description, never the product name.

### Sleep sites (SA, MN, MC, SO)

Pattern: `{description}-{brand}-{model}-{category}`. Description first, then the product, then the category word (`mattress`, `pillow`, `topper`, `sheets`, `bed-frame` and so on).

- Use **lowercase words**. The script turns spaces into hyphens and removes accents.
- **Keep words people search for:** brand, model, category, and the test or feature.
- **Remove filler words:** a, an, the, of, on, in, at, to, for, with, and, is, are, being, our, its, this, that. The script removes these anyway.
- **Keep words that change the meaning:** before, after, under, vs, side, back, stomach.
- **Length:** aim for 60 characters or fewer.
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

### Fitness sites (GGR, BB)

Each name is a **descriptive phrase** that reads like the start of an alt text. Keep the connecting words (the, of, a, on, in, into, our, for and so on); the script keeps them for Fitness.
- **People** are "our tester" or "our product tester", never a name. Across the batch use the two about equally; alternating is fine. If a name runs long, use "our tester".
- **Product:** the full product name, lowercase. Prefer the order brand, product, version, product type when you can tell the parts apart, e.g. "Stoic 3.0 Cold Plunge by Renu" → `renu stoic 3.0 cold plunge`. When you can't, keep the full name as given. Never invent a version or a product type.

Examples (from the GGR team):
- `our-product-tester-stepping-into-the-renu-stoic-3-cold-plunge`
- `temperature-display-on-the-control-panel-of-a-renu-stoic-3-cold-plunge-tub-2`
- `close-up-of-our-tester-soaking-in-the-renu-stoic-3-cold-plunge`

## 6. Write the alt text, the manifest, and preview

**Alt text**, both site types. Write one for every photo, from what's actually visible:
- One plain sentence, about 125 characters. The script refuses anything over 150.
- Include the full product name, as the writer gave it.
- People are "our tester" or "our product tester". Use the two about equally across each product's photos; the alt text doesn't have to repeat the file name's wording.
- Near-identical shots get different descriptions.
- Never start with "Image of", "Photo of" or "Picture of"; the script refuses those.

Example (Sleep): `seated-edge-support-test-nectar-classic-hybrid-mattress.webp: Our tester performing a seated edge support test on the Nectar Classic Hybrid mattress`

Save `manifest.json` in `work_dir`:

```json
{
  "site_type": "sleep",
  "output_parent": "<output_parent from the scan>",
  "skipped": [<the skipped list from the scan, as is>],
  "product_slugs": {"Helix Midnight Luxe": "Helix Midnight Luxe"},
  "images": [
    {"source": "<path from the scan>", "name": "seated-edge-support-test-helix-midnight-luxe-mattress", "product": "Helix Midnight Luxe", "alt": "Our tester sitting on the edge of the Helix Midnight Luxe mattress to test edge support", "focus_y": 0.35, "rotate": 0}
  ]
}
```

- `site_type` is the writer's answer from section 1.
- List the images in scan order.
- `product` is the product as the writer typed it (or as it appears in the file or folder name), spelled the same way for every photo of that product. The script names the new folder after it.
- `product_slugs` gives each product's brand and model, without the category word. It names the alt-text file: Renu Stoic 3.0 Cold Plunge → `"Renu Stoic 3.0"` → `renu-stoic-3-alt-text-descriptions.txt`.

Then run a preview:

```bash
python3 "<this skill's base directory>/scripts/prep.py" apply --preview "<work_dir>/manifest.json"
```

- If `ok` is false, fix each item in `problems` and run the preview again.
- Fix the `warnings` too, unless there's a good reason not to: alt text that's long or missing the product name, and "our tester" / "our product tester" used unevenly.
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

It also writes these beside the folder, never inside it, so they aren't uploaded:
- **A review page**, `<folder name> - review.html` (`review_page` in the result). It shows every finished image, numbered in alphabetical order of the new file names, with its new name, product, alt text, original file name and size.
- **A draft alt-text file per product**, `<brand-model>-alt-text-descriptions.txt` (`alt_text_files`). It has one `<file>.webp: <alt text>` line per image, in review-page order.

## 8. Report

Tell the writer the new folder's name and where it is, then show a table. List the rows in the order of `results`, numbered with each result's `number`; these match the review page.

| # | Original | New name | Product | Product from | Size |
|---|---|---|---|---|---|

"Product from" is "file name", "folder" or "you told me". Then list:
- skipped files and why (videos are expected);
- any `error` results;
- photos under 800px wide, which were kept at their own width;
- total size before and after.

Then ask them to check every image before uploading:

> Open **<folder name> - review.html** (it's next to the new folder; double-click it to open it in your browser) and check each image's crop, file name, product and alt text. Reply "looks good", or give me the numbers to fix and what's wrong, like "fix 4: the crop cuts off her head" or "fix 2 and 7: that's the Helix Midnight Luxe".

End by pointing them to the draft alt text:

> Here's the draft alt-text file: **<file name>**, next to the new folder. Review it before pasting each line into WordPress.

Name every file if there are several products.

## 9. Fix what the writer asks for

For each number they give, change that photo's entry in `manifest.json`: `focus_y` for a crop (lower moves the crop up, higher moves it down), `rotate` for a sideways photo, `name` for a wrong description, `alt` for wrong alt text, `product` (and the product part of `name` and `alt`, and `product_slugs`) for a wrong product. Leave every other entry as it is. Then run:

```bash
python3 "<this skill's base directory>/scripts/prep.py" apply --redo "<work_dir>/manifest.json"
```

`--redo` rewrites the same folder instead of making a ` (2)` copy, and regenerates the review page and the alt-text files. Numbers can shift when a name changes, so use the new numbers from here on. If a product change changes the folder name, it renames the folder and the review page to match; tell the writer the new name. If it refuses because the folder holds files it didn't write, tell the writer which files and ask them to move them out first. Then ask them to refresh the review page and check again. Repeat until they say it looks good.

## Rules

- Never change, move or delete the originals. Never upload anything.
- Never guess a product from a logo alone, or the site type from the photos.
- Always look at the check sheets before the real run, and always send the writer to the review page after it.
- If something fails, say plainly what happened and what you need from them.
