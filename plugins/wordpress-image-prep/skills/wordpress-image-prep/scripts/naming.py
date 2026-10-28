"""File-name rules for WordPress images (spec section 6)."""
import re
import unicodedata

MAX_LEN = 80
STOP_WORDS = {"a", "an", "the", "of", "on", "in", "at", "to", "for", "with", "and",
              "is", "are", "being", "our", "its", "this", "that"}
DROP_WORDS = {"image", "photo", "picture"}
_SIZE = re.compile(r"^\d+x\d+$")
_EXT = re.compile(r"\.(webp|jpe?g|png|heic|heif)$", re.I)
_CAMERA = re.compile(r"(?<![a-z])(img|dsc|dscn|pxl|mvimg)[_\- ]?\d+", re.I)


def _tokens(text):
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return [t for t in re.split(r"[^a-z0-9]+", ascii_text.lower()) if t]


def normalize_name(text):
    """Turn a proposed name into a valid base file name: no extension, no duplicate number."""
    if _CAMERA.search(text):
        raise ValueError(f"{text!r} still contains a camera file name; describe the photo instead")
    stem = _EXT.sub("", text.strip())
    words = [t for t in _tokens(stem)
             if t not in STOP_WORDS and t not in DROP_WORDS and not _SIZE.match(t)]
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
