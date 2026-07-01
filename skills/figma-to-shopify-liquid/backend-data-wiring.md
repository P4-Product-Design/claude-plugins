# Backend Data Wiring — Pattern Reference

Use this when Step 0 confirmed the component needs live Shopify data — product info, reviews, or a third-party app widget — instead of (or alongside) static, merchant-edited content.

## The pattern: real data first, schema-setting fallback always

For every dynamic value, pull from the real source, then fall back to a manual setting if it's blank. A missing metafield or unconfigured app must never produce empty or visibly-broken markup.

```liquid
{%- liquid
  assign dynamic_value = product.metafields[namespace][key].value
  if dynamic_value == blank
    assign dynamic_value = block.settings.manual_fallback_setting
  endif
-%}
```

## Common sources

| Content | Real source | Fallback |
|---|---|---|
| Product title / description / price | `product.title`, `product.description`, `variant.price` | None needed — always present on a product |
| Structured lists (benefits, FAQs, specs) | `product.metafields[ns][key].value` — a list of metaobjects | Loop over numbered schema settings instead (`benefit_1_title`, `benefit_2_title`, …), capped at a reasonable count |
| Review rating / count | The review app's metafield namespace (e.g. `judgeme.all_reviews_rating`, or the generic `reviews.rating`) | Manual `review_rating` / `review_count` schema settings |
| Review list widget | The app's rendered widget metafield (e.g. `product.metafields.judgeme.widget`), re-skinned with scoped CSS overriding the app's own classes | Hide the whole block if the metafield is blank |
| Cross-sell / bundle widget | The app's data attributes and templated markup (e.g. Rebuy's `data-rebuy-id` plus its `v-for`/`v-bind` template, hydrated client-side by the app's own script) | Hide the block if the app ID setting is blank |
| Free-shipping / cart-based progress | A live `fetch('/cart.js')` on page load, computed client-side | A static schema setting for the threshold amount |
| Variant-specific data (price, image, availability) | `product.variants` (as JSON for client-side variant switching) or `product.selected_or_first_available_variant` | None needed — always present |

## Rules

- Never hardcode a value that changes per product or per order (price, title, rating, inventory) — always read it from the real Shopify object.
- Every metafield or app read gets a fallback path. A blank metafield should degrade to a manual setting or hide the element — never render broken/empty markup.
- Namespaces and keys for custom metafields are usually store-specific and not guessable — expose them as text settings (e.g. `mf_namespace`, `mf_benefits_key`) rather than hardcoding, so a merchant or future editor can point the block at whatever metafields the store actually uses.
- Document the wiring in a header comment: what pulls from where, and what the fallback is. A future editor shouldn't have to reverse-engineer which fields are live vs. manual.
