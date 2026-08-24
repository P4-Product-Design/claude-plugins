---
name: product-block-gatherer
description: >
  Use this skill to gather and fill product block data for Fortune Shop and NCOA Shop pages,
  outputting both a Product Block Lite and a Foundational Product Block as a Word document.
  To use, provide all required inputs: (1) Product Name, (2) Category, (3) Superlative,
  (4) Product Link, (5) Organic Link or confirm none exists, (6) Live Page URL(s) or confirm
  the page does not yet exist. Supported categories: Creatine, Protein Powder, Pre-Workout,
  Hair Loss, NMN Supplements, Hearing Aids, Medical Alert Systems, and GLP-1 Medications.
  Also triggers for any request involving product block lite, foundational product block, or
  spec grids for the above categories.
---

# Product Block Gatherer

This skill extracts and structures product information into two standard block formats used on Fortune Shop and NCOA Shop pages, then delivers the output as a downloadable Word document (.docx).

## Document Structure

The document has three sections in this order:

### 1. Universal Header (appears once at the top, not repeated)
- Superlative (formerly "Award Label", e.g. "Best Overall")
- Customer Rating / Site Score — for Hearing Aids by Product and Medical Alert Systems by Product, use the placeholder: "A site rating is not needed for this product based on the template."
- Brand
- Product Name
- Deal (label + description + source URL where the deal was found; if no deal exists write "No deal exists for this brand")

### 2. Product Block Lite (summary card)
- PBL Bullets: 4 short highlight bullets (key specs or differentiators)

### 3. Foundational Product Block (full review card)
- Product Tags: 3 short tags based on objective, verifiable facts about the product (e.g. "Oral and Topical", "Fast Shipping", "NSF Certified"). Tags must not overlap with or echo any label used in the Who It's For grid. Tags should describe what the product is or has, not who it is for or why someone should buy it. Never use subjective or editorial language in tags.
- **Product Overview grid**: 4 rows of label + value (category-specific)
- **Who It's For / What You'll Love grid**: 3 rows of label + short description (category-specific)
- **Pros**: 3-5 bullet points
- **Cons**: 2-4 bullet points
- **Specs table**: 2-4 rows of label + value (category-specific)
- **Bottom Line**: 3-5 sentence editorial summary paragraph

---

## Required Inputs

Before doing anything else, confirm that all four required inputs have been provided. If any are missing, stop and ask for them before proceeding — do not guess or infer any of these.

**The required inputs are:**

| Input | Description |
|---|---|
| **Product Name** | The exact name of the product (e.g. "Thorne Creatine", "ELEHEAR Beyond Pro") |
| **Category** | One of the supported categories listed below |
| **Superlative** | The award label provided by the user (e.g. "Best Overall", "Best Value") — never infer this |
| **Product Link** | The URL of the specific product or brand page to pull information from |
| **Organic Link** | The URL of the corresponding organic editorial page (e.g. the Fortune or NCOA review page for this product). If no organic page exists, the user must explicitly state that. If provided, this page is used as the primary source for Pros, Cons, Bottom Line, and one Who It's For callout |
| **Live Page(s)** | The URL(s) of the page(s) where this product block will appear. Used to ensure the content written for this product does not duplicate what already exists for other products on that page. If the page does not yet exist, the user must state that |

If any of these are missing when the user sends their request, respond with a clear message listing exactly which inputs are needed before you can proceed. Do not start researching or generating any content until all are confirmed.

---

## Out of Scope

The following will cause the skill to stop and decline rather than attempt to proceed:

- **Unsupported categories** — if the requested category is not one of the ten supported categories listed above, do not attempt to map it to a similar one or proceed with a guess. Respond with: "This category is not currently supported. Supported categories are: Creatine, Protein Powder, Pre-Workout, Hair Loss, NMN Supplements, Hearing Aids (By Brand or By Product), Medical Alert Systems (By Brand or By Product), and GLP-1 Medications."
- **Missing required inputs** — do not begin research or generation if any of the four required inputs (Product Name, Category, Superlative, Product Link) are absent. List what is missing and wait.
- **Ambiguous category** — if the category provided does not clearly map to one of the ten supported options, ask for clarification rather than guessing.
- **Requests to generate content outside the defined block structure** — this skill produces exactly two outputs: a Product Block Lite and a Foundational Product Block, structured as defined. Do not add extra sections, reformat the document, or generate other content types (e.g. blog posts, social copy, ad copy) even if asked.
- **Requests to use a different template or override field definitions** — the category spec templates in `references/category-specs.md` are the source of truth for field labels and structure. Do not rename, reorder, or replace fields based on user instruction.
- **Requests to skip the missing field alert** — always surface missing fields to the user before generating the document. Do not silently proceed with incomplete data.

---

### Step 1: Identify category and source

**Supported categories:**
1. Creatine
2. Protein Powder
3. Pre-Workout
4. Hair Loss
5. NMN Supplements
6. Hearing Aids — By Brand (roundup)
7. Hearing Aids — By Product (single-brand review)
8. Medical Alert Systems — By Brand (roundup)
9. Medical Alert Systems — By Product (single-brand review)
10. GLP-1 Medications (unified template, covers both roundup and single-brand pages)

**IMPORTANT:** If the user says the category is "hearing aids" or "medical alert systems" without specifying which variant, always stop and ask before proceeding:

"Is this for a specific product, or for the brand as a whole?"

Present this as a checkbox/single-select question and wait for the answer. Do not assume. The answer determines which spec template to use.

### Step 2: Load the category spec template
Read `references/category-specs.md` and locate the section for the product's category. This defines:
- Which 4 fields go in the Product Overview grid
- Which 3 rows go in the Who It's For grid
- Which fields go in the Specs table

**Do not invent or rename fields.** Use the exact labels from the template. (The one exception is the Who It's For grid for GLP-1 Medications, which the template explicitly marks as illustrative rather than fixed — see that category's notes in `references/category-specs.md`.)

### Step 3: Gather the product information

**If a URL is provided:** Use web_fetch to retrieve the page. Extract every field visible on the page.

**If a required field is not on the page provided, do not immediately treat it as missing.** This applies to every category, not just the Specs Table. Brands routinely split this kind of information across their site: a homepage or product page rarely spells out full payment methods, refund terms, shipping specifics, or subscription/billing mechanics, but a Terms and Conditions, Refund Policy, Shipping, or FAQ page on that same site usually does. Before flagging a field as missing, search the brand's own site for it (a site-restricted web search such as `site:brand.com refund policy` works well, or check obvious footer links like Terms, FAQ, Shipping). Only fall back to asking the user once a genuine site-wide search has turned up nothing, or the site doesn't disclose the information anywhere.

**If no URL is provided:** Ask the user to share the product URL, or ask them to paste or describe the key product information. You can also search the web for the product.

**Only use information dated 2026 or later.** Discard any reviews, articles, or data from 2025 or earlier as potentially outdated.

**When the source is a brand's own website** (not a review page), also search for:
- Competitive positioning (to understand what makes this brand distinct)
- Real user reviews from 2026 (Trustpilot, ConsumerAffairs, Reddit, etc.)
Use this research to write the editorial fields, but keep competitor names out of the output.

**If an Organic Link is provided**, fetch that page and use it as follows:
- **Pros and Cons** — copy these directly from the organic page's product block. Do not rewrite or paraphrase; use the exact text as it appears
- **Bottom Line** — summarize the organic page's editorial content about the product, including any tester notes or first-person observations. Do not copy verbatim; synthesize into a 3 to 5 sentence paragraph
- **Who It's For** — use one of the Who It's For callouts from the organic page's product block as one of the three entries in this document. The other two should be sourced or written independently to avoid full repetition

If no Organic Link exists, write Pros, Cons, Bottom Line, and Who It's For from user reviews and available research as usual.

**If Live Page URL(s) are provided**, fetch each page and review the existing product blocks already present. When writing subjective fields (Who It's For descriptions, Pros, Cons, Bottom Line), ensure the content written for this product is meaningfully different from what already exists on that page for other products. Objective fields (specs, serving sizes, certifications) do not need to be differentiated. If the live page does not yet exist, note that and proceed without this constraint.

**Fields to gather:**
- Superlative (provided by user)
- Customer Rating / Site Score (from the page; or placeholder for by-product categories)
- Brand, Product Name
- Deal: label, description (no prices), and source URL. If no deal exists, write "No deal exists for this brand"
- PBL Bullets: 4 highlight bullets
- Product Tags: 3 short tags
- All Product Overview grid values (per category template)
- All Who It's For grid values (per category template)
- Pros list
- Cons list
- All Specs table values (per category template)
- Bottom Line paragraph

**Avoid repetition across fields — treat each section as a unique information layer:**

Every section of the document serves a distinct purpose and should introduce new information about the product. Before writing each section, check what has already been covered and ensure the new section adds something different. Use this as a guide:

- **Product Tags** — objective, factual attributes about the product itself (what it is, what it contains, how it is certified)
- **PBL Bullets** — the four most compelling user-facing benefits, framed simply
- **Product Overview Grid** — raw specs and factual product details (values, types, formats, features)
- **Who It's For** — audience fit based on lifestyle, need, or use case. Should not repeat spec facts already in the Overview Grid or echo the Product Tags
- **Pros** — specific positives reported by real users; should not restate what is already in the PBL Bullets or Overview Grid
- **Cons** — specific negatives reported by real users; should not repeat or mirror the Pros in reverse
- **Bottom Line** — synthesis of the full picture; may reference key themes from other sections but should not be a list of what has already been written

If completing a section would require repeating information already covered elsewhere, find a different angle, a more specific detail, or a different user-reported insight to fill it instead.

**If the product page and available sources do not provide enough unique information to populate all sections without repetition, stop before generating and tell the user explicitly what is missing and what kind of information would help.** For example:

> "I have enough information to complete most sections, but to avoid repeating the same points across Who It's For and Pros, I need more detail on how different types of users are experiencing this product. Could you share any additional user reviews, or a link to a review roundup for this product?"

Do not pad sections with vague or generic content to avoid this — flag the gap instead.

### Step 4: Flag any missing fields

Before writing the document, audit every required field against what was gathered. If anything is missing, first search the brand's own site for it (see Step 3 — check Terms, Refund Policy, Shipping, and FAQ pages, not just the product page provided) before concluding it's genuinely unavailable. Only after that search comes up empty should you alert the user — do not silently skip fields or fill them with invented content.

Present missing fields in a simple list, for example:

> "Before I generate the document, I need a few things I could not find on the product page:
> - Price per Serving — the page did not render pricing; please share a screenshot or the figure directly
> - Deal — no active promotion found; confirm if one exists or if I should write 'No deal exists for this brand'
> - Rating — no rating found on the product page; please provide or confirm it should be omitted"

Wait for the user to respond before generating the document. Do not use [MISSING] placeholders as a substitute for asking — only use them if the user explicitly says to proceed without a field.

### Step 5: Write the Word document

Read the docx SKILL.md at `/mnt/skills/public/docx/SKILL.md` before generating the file.

Structure the document as follows:

```
[Document Title: Product Name - Block Data]

-- UNIVERSAL INFORMATION --
Superlative:        [value]
Rating:             [value]  (or placeholder for by-product categories)
Brand:              [value]
Product Name:       [value]
Deal Label:         [value]  (or "No deal exists for this brand")
Deal Description:   [value]
Deal Source:        [URL]

-- PRODUCT BLOCK LITE --
PBL Bullets:
  * [bullet 1]
  * [bullet 2]
  * [bullet 3]
  * [bullet 4]

-- FOUNDATIONAL PRODUCT BLOCK --
Product Tags:       [tag 1] | [tag 2] | [tag 3]

-- PRODUCT OVERVIEW GRID --
[Field Label 1]:    [value]
[Field Label 2]:    [value]
[Field Label 3]:    [value]
[Field Label 4]:    [value]

-- WHO IT'S FOR --
[Label 1]:          [short description]
[Label 2]:          [short description]
[Label 3]:          [short description]

-- PROS --
+ [pro 1]
+ [pro 2]
+ [pro 3]

-- CONS --
x [con 1]
x [con 2]

-- SPECS --
[Spec Label 1]:     [value]
[Spec Label 2]:     [value]

-- BOTTOM LINE --
[Full paragraph]
```

If the user provides multiple products at once, repeat the full structure for each product, clearly separated.

---

## Output Delivery
- Save the .docx to `/mnt/user-data/outputs/` with a descriptive filename
- Use `present_files` to share it with the user
- After sharing, briefly note any fields that were flagged as missing

---

## Tips
- When fetching a roundup page, look for the "Our Review" section for the most complete data
- The Lite block data is usually found in the "Key Product Information" section higher on the page
- Product Tags are typically 3 short phrases on the foundational block card header
- For NCOA pages, the tab label may be "What You'll Love" instead of "Who It's For" — treat identically
- Always include the source URL for any deal found. Look for it on the brand's site or the review page
- If the only deal available is a Subscribe and Save offer, use "Subscribe & Save" as the Deal Label and include the savings percentage in the description using this exact format: "Subscribe and save for [X]% off" — no other phrasing is acceptable
- If no deal of any kind exists, write "No deal exists for this brand" with no description or source
- Do not infer or fabricate rating scores — only use values explicitly stated on the page

## Writing Rules (apply to all generated content)
- **No em dashes** — never use the character. Use a comma, colon, semicolon, or rewrite the sentence
- **No colons** — never use the colon character anywhere in the body content (field labels in the document layout are fine, but not within the content values themselves). Rewrite the sentence instead
- **No pricing** — never include dollar amounts, monthly costs, subscription fees, or any cost figures anywhere. The only exceptions are: (1) the Deal Description field, where a dollar-off savings amount is allowed (e.g. "Save $120 off"); (2) the Price per Serving field in the Specs table for nutrition categories (Creatine, Protein Powder, Pre-Workout, NMN); (3) the Price per Day field in the Product Overview grid for GLP-1 Medications. For Price per Serving and Price per Day, only use pricing found on the specific product page URL provided by the user — do not pull prices from Amazon, third-party retailers, or any other source. Use the lowest available cost on that page (e.g. if a larger size, longer plan, or subscribe and save option is offered on that page, use whichever gives the lowest per-serving or per-day cost)
- **No CTA buttons** — not included in the output; handled by the website
- **No competitor mentions** — never name another brand. Research competitors to understand positioning, but keep that invisible in the output
- **Pros and Cons must come from real user feedback** — base these only on what actual users report in reviews (Trustpilot, ConsumerAffairs, Reddit, verified review platforms, etc.). Never reference lab test scores, testing methodology, or what was found "in testing." If a finding appears in user reviews, it can be included; if it only appears in expert or lab evaluations, leave it out
- **No outdated sources** — only use information dated 2026 or later
- **Keep Product Tags short, scannable, and objective** — two or three words maximum per tag, regardless of category. Tags must be based on verifiable facts about the product (e.g. "Oral and Topical", "NSF Certified", "Fast Shipping", "Rechargeable Case"). Never use subjective or editorial language (e.g. avoid "Great Value", "Highly Rated", "Top Performer"). Tags must not overlap with or echo any label used in the Who It's For grid — they describe what the product is or has, not who it is for
- **Keep Who It's For descriptions short** — one sentence, 15 words or fewer. Lead with the benefit
- **Keep Pros and Cons short** — one punchy phrase per point, 12 words or fewer. No sub-clauses
- **PBL Bullets should be benefit-led, not spec-led** — write for a general audience who may not know technical terms. Never reference proprietary technology names, version numbers, or spec labels (e.g. "VOCCLEAR 2.0", "Bluetooth 5.3", "IPX5") in PBL bullets. Instead, describe what the feature does for the user in plain language. Technical detail belongs in the Product Overview Grid, What You'll Love, or Pros. For brand-level blocks, the deal description can say "Save up to $X off"; for product-level blocks, use the specific product's deal amount
- **For nutrition categories, the first PBL bullet is always the key nutrient per serving**, written in plain language as a statement of fact. Use the following format for each category:
  - Creatine: "[X] g of creatine per serving"
  - Protein Powder: "[X] g of protein per serving"
  - Pre-Workout: "[X] mg of caffeine per serving"
  - NMN Supplements: "[X] mg of NMN per serving" (or NMN/NAD if both are present)
  Then provide 3 additional benefit-led highlights as usual. This first bullet follows the same length rule as the others (eight words or fewer) but is factual, not benefit-framed
- **For GLP-1 Medications, the first PBL bullet is always what type of medication the platform offers** — compounded, FDA-approved brand-name, or both — stated as fact, not benefit-framed. Base it on what the brand's site actually offers rather than defaulting to one type. Examples: "Offers compounded GLP-1 options", "Offers FDA-approved GLP-1s like Wegovy®, Zepbound®, Ozempic®", "Offers brand-name GLP-1s and compounded alternatives". Then provide 3 additional benefit-led highlights as usual, following the normal PBL Bullet rules (benefit-led, eight words or fewer, no proprietary tech names)
- **Subscribe and Save deal descriptions must follow this exact format** — "Subscribe and save for [X]% off" where [X] is the percentage. Never use variations like "Save [X]% when you subscribe" or "Subscribe to save [X]%"
- **No repetition across sections** — each section must introduce information not already covered elsewhere in the document. Product Tags, PBL Bullets, Who It's For, Pros, Cons, and Bottom Line each serve a distinct purpose. If the same point would appear in two sections, cut it from the less appropriate one and find a different angle for that section instead
- **PBL Bullets must be short** — eight words or fewer per bullet. No asides, no qualifiers, no sub-clauses (e.g. avoid "even in noisy environments", "for extended use", "and more"). State the benefit, stop.
