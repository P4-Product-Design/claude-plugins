# Sleepopolis star rating pattern

Star ratings are NOT a single combined SVG. Each star is an individual element with empty + filled layers and a CSS `--fill` variable for partial fills.

## Why per-star

The engineer needs to set rating values via Optimizely's widget form, e.g.:

- `prod1star1: "100%"`
- `prod1star2: "100%"`
- `prod1star3: "100%"`
- `prod1star4: "100%"`
- `prod1star5: "60%"` ← partial 5th star for a 4.6 rating

A single combined SVG can't be customized per-star in the widget UI.

## Markup (one star)

```html
<span class="so-star" style="--fill: {{extension.prod1star1}};">
  <svg class="so-star-empty" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 19" aria-hidden="true">
    <path d="M9.37975 0.289347C9.55895 -0.0965191 10.1075 -0.0965183 10.2867 0.289348L12.8325 5.77116C12.9054 5.92804 13.0541 6.03612 13.2258 6.05693L19.226 6.78414C19.6484 6.83533 19.8179 7.35705 19.5063 7.64672L15.0795 11.7619C14.9528 11.8796 14.896 12.0545 14.9292 12.2243L16.0918 18.1555C16.1736 18.573 15.7298 18.8955 15.358 18.6886L10.0763 15.7501C9.92517 15.666 9.7413 15.666 9.59015 15.7501L4.30844 18.6886C3.93665 18.8955 3.49285 18.573 3.57468 18.1555L4.73723 12.2243C4.7705 12.0545 4.71368 11.8796 4.58699 11.7619L0.16017 7.64672C-0.151435 7.35705 0.018083 6.83533 0.440439 6.78414L6.44064 6.05693C6.61235 6.03612 6.76111 5.92804 6.83397 5.77116L9.37975 0.289347Z" fill="#FFEED5"/>
  </svg>
  <span class="so-star-fill">
    <svg class="so-star-full" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 19" aria-hidden="true">
      <path d="M9.37975 0.289347C9.55895 -0.0965191 10.1075 -0.0965183 10.2867 0.289348L12.8325 5.77116C12.9054 5.92804 13.0541 6.03612 13.2258 6.05693L19.226 6.78414C19.6484 6.83533 19.8179 7.35705 19.5063 7.64672L15.0795 11.7619C14.9528 11.8796 14.896 12.0545 14.9292 12.2243L16.0918 18.1555C16.1736 18.573 15.7298 18.8955 15.358 18.6886L10.0763 15.7501C9.92517 15.666 9.7413 15.666 9.59015 15.7501L4.30844 18.6886C3.93665 18.8955 3.49285 18.573 3.57468 18.1555L4.73723 12.2243C4.7705 12.0545 4.71368 11.8796 4.58699 11.7619L0.16017 7.64672C-0.151435 7.35705 0.018083 6.83533 0.440439 6.78414L6.44064 6.05693C6.61235 6.03612 6.76111 5.92804 6.83397 5.77116L9.37975 0.289347Z" fill="#FFC468"/>
    </svg>
  </span>
</span>
```

## Styles

```css
.so-star {
  position: relative;
  display: inline-block;
  width: 14px;
  height: 14px;
  flex: 0 0 14px;
  overflow: hidden;
}

.so-star-empty {
  display: block;
  width: 14px;
  height: 14px;
}

.so-star-fill {
  position: absolute;
  top: 0;
  left: 0;
  width: var(--fill, 100%);
  height: 14px;
  overflow: hidden;
}

.so-star-full {
  display: block;
  width: 14px;
  height: 14px;
  max-width: none;
}
```

Wrap a row of 5 stars in `display: flex; align-items: center; gap: 1px`.

## Constants
- viewBox: `0 0 20 19`
- Empty fill color: `#FFEED5`
- Filled fill color: `#FFC468`
- Star size: 14×14 (adjust per design, but keep both layers the same size)

## form_schema entries

For a row of 5 stars on product 1:

```json
{ "name": "prod1star1", "label": "prod1star1", "default_value": "100%", "field_type": "text", "options": null },
{ "name": "prod1star2", "label": "prod1star2", "default_value": "100%", "field_type": "text", "options": null },
{ "name": "prod1star3", "label": "prod1star3", "default_value": "100%", "field_type": "text", "options": null },
{ "name": "prod1star4", "label": "prod1star4", "default_value": "100%", "field_type": "text", "options": null },
{ "name": "prod1star5", "label": "prod1star5", "default_value": "60%",  "field_type": "text", "options": null }
```
