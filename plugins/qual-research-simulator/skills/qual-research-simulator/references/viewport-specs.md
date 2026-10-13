# Viewport & Breakpoint Specs

These are fixed, company-wide breakpoints and reference resolutions that design files and the live site are built to, regardless of persona category. Use them in Step 3 to correctly classify which frame is which and to set accurate browser viewport sizes when loading a live page — don't guess frame/device boundaries from arbitrary pixel widths.

## Breakpoints

- **Mobile:** 320px – 619px
- **Tablet:** 620px – 1023px
- **Desktop:** 1024px+

## Reference resolutions

| Resolution | Represents |
|---|---|
| 390×844 | Primary mobile user |
| 320×693 | Worst-case mobile user |
| 621×800 | Worst-case tablet user |
| 768×1024 | Ideal tablet user |
| 1023×1360 (contained at column width) | Worst-case tablet user |
| 1024×1360 (contained at column width) | Worst-case desktop user |
| 1920×1080 (contained at column width) | Primary desktop user |

## How to use these

- When identifying frames in a Figma file (`get_metadata`/`get_design_context`), classify each by width against the breakpoints above — a 768px-wide frame is **tablet**, not "kind of mobile" or "kind of desktop."
- When emulating a viewport for a live page (`resize_window`/device emulation), default to the **primary** resolution for whichever device is in play (390×844 mobile, 1920×1080 desktop). Use the matching **worst-case** resolution as a secondary check if there's a specific reason to (a persona known to be on an older/smaller device, or a layout that looks like it might break at an edge size).
- Tablet is a real, distinct breakpoint in this design system — don't collapse it into mobile or desktop. It's used when a design file includes a tablet frame, or when checking a live page's tablet behavior is relevant to what's being tested, even though current persona reference files don't yet note tablet-specific behavioral skew (see Step 4 — persona device matching is currently mobile/desktop only, based on what the data supports).
