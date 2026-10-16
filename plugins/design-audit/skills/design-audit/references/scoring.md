# Scoring

Each finding gets a severity and an effort. Together they set its priority group.

## Severity — what the user does

| Level | User behavior |
|---|---|
| Critical | Can't complete the primary action, or most users leave before trying |
| High | Many users hesitate, mis-tap, or drop off before acting |
| Medium | Slows down or confuses some users |
| Low | Minor friction or polish |

Judge the base level by the user behavior alone. Where the issue sits is already part of that judgment.

**Escalation (narrow):** move up one level only when the issue is on the primary CTA itself: the button, a selection required to use it, or the price shown next to it.
- **Never escalate into Critical.** Critical has to be earned at the base level.
- **First-screen placement doesn't escalate.**
- **Accessibility follows the same rule.**

**Sanity check:** if more than a third of findings are Critical or High, re-score. Keep only issues that truly stop or turn away many users.

## Effort

- **S:** copy, color, spacing, or a variant swap
- **M:** a new state or variant, or reworking one section
- **L:** a new component, a layout restructure, or a cross-team dependency

## Priority groups

| | Effort S | Effort M / L |
|---|---|---|
| **Critical / High** | Do first | Plan next |
| **Medium / Low** | Fill-ins | Backlog |

Within a group, sort by severity, then by position on the page (highest first).
