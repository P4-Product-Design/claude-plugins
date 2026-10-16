# Checks

Walk the page the way a user would. Each check names what the user is trying to do.

**Applies:** All · Page (long-form, affiliate review, roundup, comparison, collection, homepage) · Landing (incl. quiz results, partner co-branded) · PDP · Block (product block) · Form (lead-gen form or quiz).
† = can't be confirmed from a static design. List it under **Verify in build**.

These are internal. Never show check names in the output.

## 1. Land — the first 5 seconds

| Check | User is trying to… | Red flags | Law | Applies |
|---|---|---|---|---|
| Relevance | Confirm this is what they clicked | Hero doesn't echo the ad's offer, product, or words | Information scent | Landing |
| Instant meaning | Grasp what it is and why it matters | Clever headline; the benefit only appears in body copy | Cognitive load | All |
| One next step | Spot the action without scrolling | Equal-weight CTAs; CTA below the first mobile screen | Hick's law, Von Restorff | All |
| Distraction | Stay on the path | Full nav, promos, or outbound links above the CTA; cross-sells between buyer and CTA | Hick's law | Landing, PDP |

## 2. Understand — answers in the order they decide

| Check | User is trying to… | Red flags | Law | Applies |
|---|---|---|---|---|
| Scannable | Get the answer from headings, bold text, and visuals | Walls of text; vague headings | Layer-cake scanning | Page, Landing, PDP |
| Decision order | Learn what → why → proof → price → act | Price or ask before the value; proof only after the ask | Serial position | All |
| Offer clarity | Understand the deal instantly | Discount math that doesn't add up; an offer with no way to act on it | Cognitive load | All |
| Objections | Settle doubts before deciding | Key questions answered only far from the CTA | Tesler's law | Landing, Page, PDP |

## 3. Trust — do they believe it?

| Check | User is trying to… | Red flags | Law | Applies |
|---|---|---|---|---|
| Proof at the ask | See ratings or reviews next to the action | Proof sits sections away from the CTA | Social proof | All |
| Credible claims | Believe the claims | Vague superlatives; asterisk with no footnote; unsourced claims | Aesthetic-usability | All |
| No pressure | Not feel tricked | Fake timers; pre-checked boxes; guilt-trip decline links | Peak-end rule | Landing, Form |

## 4. Act — choose and buy without friction

| Check | User is trying to… | Red flags | Law | Applies |
|---|---|---|---|---|
| Tap ease | Hit targets on the first try | Targets under 44px; links packed tight | Fitts's law | All |
| Clickable cues | Tell what's clickable | Links styled like body text; badges styled like buttons | Jakob's law | All |
| Selection | Pick a flavor or size before buying | Options hidden in a dropdown; no default; no prompt if skipped | Hick's law | Block, PDP |
| Add-to-cart response | Know the item was added and what's next | No loading, added, or error state; unclear result | Doherty threshold | Block, PDP |
| Consistency | Learn a pattern once | The same element looks or acts differently in different places | Jakob's law | All |
| Forms | Finish without errors | Extra fields; placeholder used as the label; no validation; no progress or back | Goal-gradient | Form |

## 5. Keep moving — always a next step

| Check | User is trying to… | Red flags | Law | Applies |
|---|---|---|---|---|
| Path to action | Act whenever they're ready | Long stretches with no CTA; page ends with no CTA | Serial position | All |
| Hidden content | Know there's more, and where they are | Carousel with no position indicator; back arrow looks active on the first slide | Visibility of status | All |
| Destination | Know where a link goes | Retailer not named; no cue that the link leaves the site | Information scent | Block, Page |
| Mobile flow | Follow the story on a phone | CTA stacked below long content; sticky bar covers content | Thumb zone | All |

## 6. Everyone — can all users read and use it?

| Check | User is trying to… | Red flags | Law | Applies |
|---|---|---|---|---|
| Readable | Read without strain | Text below 4.5:1 (3:1 for 24px+, or 18.7px+ bold); text under 14px; text over busy images | — | All |
| Not color alone | Understand states without color | Errors or sale prices shown by color only | — | All |
| Media | Control and understand media | Video with no pause control or captions; text baked into images | — | All |
| Focus | See where they are when tabbing | No focus state on interactive components | — | All |
| Keyboard † | Use the page without a mouse | Hover-only menus; custom controls | — | All |
| Structure † | Navigate with a screen reader | Headline split across nodes; skipped heading levels | — | Page, Landing |
| Text scaling † | Zoom text to 200% | Fixed-height containers clip text | — | All |

## 7. Real-world states — what users actually see

| Check | User is trying to… | Red flags | Law | Applies |
|---|---|---|---|---|
| Missing data | Shop a product with no rating, image, or tag | Empty gaps; "0 stars"; broken layout | — | Block, Page, PDP |
| Content extremes | Read long names or few results | Long names break cards; 1 item in a 3-up grid | — | All |
| Stock & sale | Know if it's available or discounted | No out-of-stock or sale state | — | Block, PDP |
| Loading | Wait without confusion | No placeholder; layout jumps when data arrives | Doherty threshold | Block, Page, PDP |
| No results | Recover from an empty filter | Empty area with no message or reset | — | Page |
