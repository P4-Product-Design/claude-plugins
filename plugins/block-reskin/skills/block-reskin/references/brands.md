# Brand UI kits

Read each kit live on every run. This file only records where the kits are and the rules for each brand type. Don't store token values here.

## Kits

| Brand | Abbr | Name prefix | Type | Kit | File key | Where styles and buttons live |
|---|---|---|---|---|---|---|
| Sleepopolis | SO | `.so` | Baseline: most kits started from it | [SO UI Kit](https://www.figma.com/design/j2c1kPiEBk954qhPZyzXQG/SO-UI-Kit--UPDATED-) | `j2c1kPiEBk954qhPZyzXQG` | Atoms (Typography, Colors, Spacing), Molecules → Buttons |
| Garage Gym Reviews | GGR | `.ggr` | Full kit | [GGR UI Kit](https://www.figma.com/design/BSLKyFV4r9H4skydDtjx0p/GGR-UI-Kit--UPDATED-) | `BSLKyFV4r9H4skydDtjx0p` | Atoms (incl. Corner Radius), Molecules → Buttons |
| Sleep Advisor | SA | `.sa` | Older kit, being revived | [SA UI Kit](https://www.figma.com/design/0OpxY5Nh9m3cDHZiio8hzc/SA-UI-Kit) | `0OpxY5Nh9m3cDHZiio8hzc` | Style Guide, Design System → Buttons |
| Mattress Nerd | MN | `.mn` | Older kit, being revived | [MN UI Kit](https://www.figma.com/design/CyqPWUZidz6KBPyH4RnLiU/MN-UI-Kit) | `CyqPWUZidz6KBPyH4RnLiU` | Atoms, Molecules → Buttons |
| Mattress Clarity | MC | `.mc` | Sleep | [MC UI Kit](https://www.figma.com/design/KHWiIq3dD3cVR9ccK59BqG/MC-UI-Kit) | `KHWiIq3dD3cVR9ccK59BqG` | Atoms, Molecules → Buttons |
| BarBend | BB | `.bb` | Fitness | [BB UI Kit](https://www.figma.com/design/hsihgLHasjAjBoS2bnIEya/BB-UI-Kit) | `hsihgLHasjAjBoS2bnIEya` | Style Guide; Site Components → Buttons (other site components are marked "DO NOT USE") |
| Swolverine | SWOL | `.swol` | Internal, on Shopify. Same reskin process as the others | [SWOL Mini UI Kit](https://www.figma.com/design/DVt76xoNBw8gjUTHUl5KuP/Swolverine-Mini-UI-Kit) | `DVt76xoNBw8gjUTHUl5KuP` | UI Kit → Styles & Brand Components |
| AARP | AARP | `.aarp` | **Partner** | [AARP Designs – Internal](https://www.figma.com/design/nZQRxu8OmyAel83r7OO6w8/AARP-Designs---Internal) | `nZQRxu8OmyAel83r7OO6w8` | Workspace → Block Library / Components (no Buttons page) |
| NCOA | NCOA | `.ncoa` | **Partner** | [NCOA UI Kit](https://www.figma.com/design/RtTpJzWwfwC0OcWNbPDkbl/NCOA-UI-Kit) | `RtTpJzWwfwC0OcWNbPDkbl` | Style Guide → Typography, Colors, Buttons & Links |
| Fortune | FOR | `.for` | **Partner** | [Fortune UI Kit](https://www.figma.com/design/EFHxrM1xbrW60imXgxk7U0/Fortune-UI-Kit) | `EFHxrM1xbrW60imXgxk7U0` | ⭐ Fortune Style Guide |

The "Where" column is a starting hint from November 2026. Pages move, so confirm them live.

To work out a brand:
- **Destination:** the file key in the pasted-copy link.
- **Source:** the file key in the source link. If that's missing, use the name of the library the pasted frame's remote components and styles come from (for example "MC UI Kit").

## Rules by brand type

### Internal brands (SO, GGR, SA, MN, MC, BB, SWOL)
- Relink everything to the destination kit.
- Keep shared P4 doc chrome (`.header`, `.section` / `.Section`). If the destination kit's own pages use a different `.section`, swap to that one.
- Rewrite component descriptions in neutral language, with no brand names.

### Partner brands (AARP, NCOA, FOR)

The partner's file must show no other brand anywhere. **P4 / Pillar Four is allowed.**

Scrub all four of these:
1. **Component descriptions:** rewrite them in neutral language.
2. **Layer, frame and component names.**
3. **Visible text on the canvas:** headers, labels, sample copy and notes.
4. **Library links:** no instance, style or variable may stay linked to an internal brand's kit or library.
   - Swap `.header` / `.section` to the partner kit's own versions.
   - If the partner kit has none, make local copies and remove any brand text from them.

When the partner kit is missing a token (a color, text style, spacing or radius value):
- Use the closest partner value.
- List it as a follow-up.
- Never leave it linked to another brand's library.

### Terms the partner scrub searches for

Match these case-insensitively, and as whole words only, so "SO" doesn't match "SOLID".

- Brand names: Sleepopolis, Garage Gym Reviews, Sleep Advisor, Mattress Nerd, Mattress Clarity, BarBend, Swolverine, AARP, NCOA, Fortune. Skip the destination partner's own name.
- Abbreviations: SO, GGR, SA, MN, MC, BB, SWOL, FOR. Skip the destination partner's own abbreviation.
  - "FOR" and "SA" are also ordinary words. Report hits on them for review, and don't rename automatically.
- Prefixes: `.so`, `.ggr`, `.sa`, `.mn`, `.mc`, `.bb`, `.swol`, `.aarp`, `.ncoa`, `.for`, followed by an uppercase letter (as in `.mcProductRowParent`).
- Token-name leftovers: `so/…`, `so-gray`, `Sleepopolis Gray`, `Sleepopolis Blue`, `wp--preset--color--so-…`.
