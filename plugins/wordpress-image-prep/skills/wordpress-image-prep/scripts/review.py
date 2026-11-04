"""The review page: a numbered grid of every finished image that the writer opens before uploading."""
import html
import os
import re
from urllib.parse import quote

CSS = """
:root { --bg: #f6f6f4; --card: #fff; --text: #1d1d1b; --muted: #6b6b66; --line: #e2e2dd; --badge: #1d1d1b; --badge-text: #fff; --warn: #9a3412; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #161615; --card: #22221f; --text: #f1f1ec; --muted: #a3a39c; --line: #34342f; --badge: #f1f1ec; --badge-text: #161615; --warn: #fdba74; }
}
* { box-sizing: border-box; }
body { margin: 0; padding: 24px 16px 48px; background: var(--bg); color: var(--text);
       font: 15px/1.45 -apple-system, "Segoe UI", system-ui, sans-serif; }
main { max-width: 1400px; margin: 0 auto; }
h1 { font-size: 22px; margin: 0 0 4px; word-break: break-word; }
.summary { color: var(--muted); margin: 0 0 8px; }
.how { margin: 0 0 20px; }
.notes { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 12px 16px; margin: 0 0 20px; }
.notes h2 { font-size: 15px; margin: 0 0 6px; color: var(--warn); }
.notes ul { margin: 0; padding-left: 18px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
figure { margin: 0; background: var(--card); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; position: relative; }
figure img { display: block; width: 100%; height: auto; background: var(--line); }
.num { position: absolute; top: 8px; left: 8px; min-width: 32px; height: 32px; padding: 0 8px; border-radius: 16px;
       background: var(--badge); color: var(--badge-text); font-weight: 700; display: flex; align-items: center; justify-content: center; }
figcaption { padding: 10px 12px 12px; }
.name { font-family: ui-monospace, Consolas, Menlo, monospace; font-size: 13px; word-break: break-all; margin: 0 0 6px; }
.meta { color: var(--muted); font-size: 13px; margin: 0; }
.alt { font-size: 13px; margin: 6px 0 0; }
"""


def _size(n):
    return f"{n / 1048576:.1f} MB" if n >= 1048576 else f"{round(n / 1024)} KB"


def _base(path):
    return re.split(r"[\\/]", path)[-1]


def page_path(out_dir):
    """The review page sits beside the output folder, so uploading the folder never picks it up."""
    return out_dir.rstrip("/\\") + " - review.html"


def write_page(out_dir, results, bytes_before, bytes_after, skipped=()):
    """Write the review page for a finished run and return its path.

    results: apply's per-file results in review order (source, product, alt, output, width, height, kb; or
    source, error). Cards are numbered in that order, matching the chat report.
    Images are linked by relative path to the files in out_dir, so the page has no copies and no network requests.
    """
    e = html.escape
    folder = os.path.basename(out_dir.rstrip("/\\"))
    done = [r for r in results if "output" in r]
    failed = [r for r in results if "error" in r]
    cards = []
    for n, r in enumerate(done, 1):
        name = os.path.basename(r["output"])
        cards.append(
            f'<figure id="image-{n}"><span class="num">{n}</span>'
            f'<img src="{quote(folder)}/{quote(name)}" alt="{e(name)}" loading="lazy" '
            f'width="{r["width"]}" height="{r["height"]}">'
            f'<figcaption><p class="name">{e(name)}</p>'
            f'<p class="meta">{e(r["product"])}</p>'
            f'<p class="meta">from {e(_base(r["source"]))} · {r["width"]} × {r["height"]} · {r["kb"]} KB</p>'
            + (f'<p class="alt">Alt text: {e(r["alt"])}</p>' if r.get("alt") else "")
            + "</figcaption></figure>")
    notes = []
    if failed:
        items = "".join(f"<li>{e(_base(r['source']))}: {e(r['error'])}</li>" for r in failed)
        notes.append(f'<section class="notes"><h2>Couldn\'t be processed</h2><ul>{items}</ul></section>')
    if skipped:
        items = "".join(f"<li>{e(_base(s['path']))}: {e(s['reason'])}</li>" for s in skipped)
        notes.append(f'<section class="notes"><h2>Skipped</h2><ul>{items}</ul></section>')
    count = f"{len(done)} image" + ("" if len(done) == 1 else "s")
    doc = (
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{e(folder)} - review</title><style>{CSS}</style></head><body><main>"
        f"<h1>{e(folder)}</h1>"
        f'<p class="summary">{count} · {_size(bytes_before)} before → {_size(bytes_after)} after</p>'
        '<p class="how">Check each image\'s crop, file name, product and alt text. To change one, tell Claude its number, '
        'for example "fix 4: the crop cuts off her head".</p>'
        + "".join(notes)
        + f'<div class="grid">{"".join(cards)}</div></main></body></html>\n')
    path = page_path(out_dir)
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    return path
