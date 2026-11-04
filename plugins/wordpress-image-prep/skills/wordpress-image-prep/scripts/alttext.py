"""Draft alt-text files: one per product, written beside the output folder so they're never uploaded."""
import os
import re

import naming

TARGET_LEN = 125  # what to aim for; longer gets a warning
MAX_LEN = 150     # longer is refused
_BANNED_START = re.compile(r"^\s*(an?\s+)?(image|photo|picture|photograph)\s+of\b", re.I)
_PRODUCT_TESTER = re.compile(r"\bour[\s-]+product[\s-]+tester", re.I)
_TESTER = re.compile(r"\bour[\s-]+tester", re.I)


def check(alt, product):
    """Problems (refuse the run) and warnings (worth fixing) for one image's alt text."""
    alt = (alt or "").strip()
    if not alt:
        return ["every image needs alt text"], []
    problems, warnings = [], []
    if _BANNED_START.match(alt):
        problems.append(f"alt text can't start with \"{alt.split()[0]} {alt.split()[1]}\": {alt!r}")
    if len(alt) > MAX_LEN:
        problems.append(f"alt text is {len(alt)} characters; keep it to about {TARGET_LEN}: {alt!r}")
    elif len(alt) > TARGET_LEN:
        warnings.append(f"alt text is {len(alt)} characters; aim for about {TARGET_LEN}: {alt!r}")
    if product and product.lower() not in alt.lower():
        warnings.append(f"alt text doesn't include the full product name {product!r}: {alt!r}")
    return problems, warnings


def tester_balance(texts):
    """A warning if "our product tester" and "our tester" aren't used about equally across texts, else None."""
    product_tester = sum(len(_PRODUCT_TESTER.findall(t)) for t in texts)
    tester = sum(len(_TESTER.findall(t)) for t in texts)
    if abs(product_tester - tester) <= 1:
        return None
    return (f"'our product tester' is used {product_tester} times and 'our tester' {tester} times; "
            "use the two about equally")


def _free_file(path):
    if not os.path.exists(path):
        return path
    stem, ext = os.path.splitext(path)
    n = 2
    while os.path.exists(f"{stem} ({n}){ext}"):
        n += 1
    return f"{stem} ({n}){ext}"


def file_name(product_slug):
    return f"{naming.slug(product_slug)}-alt-text-descriptions.txt"


def write_files(out_dir, entries, slugs):
    """entries: dicts with output, product and alt, in review-page order. slugs: product -> brand-model.

    Writes '<brand-model>-alt-text-descriptions.txt' per product beside out_dir, one '<file>.webp: <alt>' line
    per image. Never overwrites a file from another batch. Returns the paths.
    """
    parent = os.path.dirname(out_dir.rstrip("/\\"))
    by_product = {}
    for e in entries:
        by_product.setdefault(e["product"], []).append(e)
    paths = []
    for product, items in by_product.items():
        path = _free_file(os.path.join(parent, file_name(slugs[product])))
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            for e in items:
                f.write(f"{os.path.basename(e['output'])}: {' '.join(e['alt'].split())}\n")
        paths.append(path)
    return paths
