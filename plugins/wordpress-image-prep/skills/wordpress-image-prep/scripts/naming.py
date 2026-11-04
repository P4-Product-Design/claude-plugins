"""File-name rules for WordPress images (spec section 6): Sleep sites drop filler words, Fitness sites keep them."""
import re
import unicodedata

MAX_LEN = 80
SITE_TYPES = ("sleep", "fitness")
STOP_WORDS = {"a", "an", "the", "of", "on", "in", "at", "to", "for", "with", "and",
              "is", "are", "being", "our", "its", "this", "that"}
DROP_WORDS = {"image", "photo", "picture"}
_SIZE = re.compile(r"^\d+x\d+$")
_EXT = re.compile(r"\.(webp|jpe?g|png|heic|heif)$", re.I)
_CAMERA = re.compile(r"(?<![a-z])(img|dsc|dscn|pxl|mvimg)[_\- ]?\d+", re.I)
_POINT_ZERO = re.compile(r"(\d)\.0(?![\d.])")  # "Stoic 3.0" -> "Stoic 3"; "2.5" and "3.05" are left alone


def _tokens(text):
    ascii_text = unicodedata.normalize("NFKD", _POINT_ZERO.sub(r"\1", text)).encode("ascii", "ignore").decode()
    return [t for t in re.split(r"[^a-z0-9]+", ascii_text.lower()) if t]


def slug(text):
    """Lowercase hyphenated words, every word kept, a trailing .0 version dropped ("Renu Stoic 3.0" -> "renu-stoic-3")."""
    name = "-".join(_tokens(text))
    if not name:
        raise ValueError(f"{text!r} has no usable words")
    return name


def normalize_name(text, site_type="sleep"):
    """Turn a proposed name into a valid base file name: no extension, no duplicate number.

    Sleep names drop filler words; Fitness names are descriptive phrases that keep them.
    """
    if site_type not in SITE_TYPES:
        raise ValueError(f"site_type must be 'sleep' or 'fitness', got {site_type!r}")
    if _CAMERA.search(text):
        raise ValueError(f"{text!r} still contains a camera file name; describe the photo instead")
    stem = _EXT.sub("", text.strip())
    drop = DROP_WORDS | (STOP_WORDS if site_type == "sleep" else set())
    words = [t for t in _tokens(stem) if t not in drop and not _SIZE.match(t)]
    name = "-".join(words)
    if not name:
        raise ValueError(f"{text!r} has no usable words")
    if len(name) > MAX_LEN:
        raise ValueError(f"{name!r} is {len(name)} characters; the limit is {MAX_LEN}. "
                         "Shorten the description, never the product name")
    return name


def assign_unique(names):
    """The first use of a name keeps it; later uses get -2, -3 and so on, in order."""
    taken = set(names)
    last = {}
    out = []
    for name in names:
        if name not in last:
            last[name] = 1
            out.append(name)
            continue
        n = last[name] + 1
        while f"{name}-{n}" in taken:
            n += 1
        last[name] = n
        taken.add(f"{name}-{n}")
        out.append(f"{name}-{n}")
    return out


def _natural(name):
    return [int(part) if i % 2 else part for i, part in enumerate(re.split(r"(\d+)", name))]


def review_order(names):
    """Indexes of names sorted alphabetically, numbers compared as numbers (a, a-2, a-10, b)."""
    return sorted(range(len(names)), key=lambda i: _natural(names[i]))
