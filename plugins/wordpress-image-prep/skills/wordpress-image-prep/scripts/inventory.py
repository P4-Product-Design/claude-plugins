"""Find a batch's images, read when and on what they were shot, pull product hints, and group by shoot (spec sections 5, 7)."""
import os
import re
import zipfile
from datetime import datetime, timedelta

from PIL import Image

IMAGE_EXT = {".heic", ".heif", ".jpg", ".jpeg", ".png"}
VIDEO_EXT = {".mov", ".mp4", ".m4v", ".avi", ".hevc", ".3gp"}
GROUP_GAP = timedelta(minutes=30)
GENERIC_FOLDERS = {"images", "image", "photos", "photo", "pictures", "pics", "testing", "test", "tests",
                   "heic", "jpg", "jpeg", "png", "raw", "raws", "originals", "downloads", "desktop", "dropbox",
                   "central testing", "central testing images", "wordpress"}
_CAMERA = re.compile(r"(?<![A-Za-z])(img|dsc|dscn|pxl|mvimg)[_\- ]?\d+", re.I)
_DATE_LIKE = re.compile(r"^\d{4}[-_. ]?\d{2}([-_. ]?\d{2})?$")


def unpack(src, work_dir):
    """Return the folder to scan: src itself, or src extracted into work_dir/unzipped when it's a zip."""
    if os.path.isdir(src):
        return src
    if not zipfile.is_zipfile(src):
        raise ValueError(f"{src} isn't a folder or a zip file")
    dest = os.path.realpath(os.path.join(work_dir, "unzipped"))
    os.makedirs(dest, exist_ok=True)
    with zipfile.ZipFile(src) as z:
        safe = [m for m in z.infolist()
                if os.path.realpath(os.path.join(dest, m.filename)).startswith(dest + os.sep)
                and not m.filename.startswith("__MACOSX")]
        z.extractall(dest, members=safe)
    return dest


def list_files(root):
    """Return (image paths, skipped) in a stable order. Hidden files and __MACOSX are ignored entirely."""
    images, skipped = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d != "__MACOSX")
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            path = os.path.join(dirpath, name)
            ext = os.path.splitext(name)[1].lower()
            if ext in IMAGE_EXT:
                images.append(path)
            elif ext in VIDEO_EXT:
                skipped.append({"path": path, "reason": "video"})
            else:
                skipped.append({"path": path, "reason": "not an image"})
    return images, skipped


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(str(value).strip()[:19], "%Y:%m:%d %H:%M:%S")
    except ValueError:
        return None


def read_meta(path):
    """Upright pixel size, EXIF orientation, capture time and camera model. Doesn't decode the pixels."""
    with Image.open(path) as im:
        w, h = im.size
        exif = im.getexif()
    orientation = exif.get(0x0112, 1)
    if orientation in (5, 6, 7, 8):
        w, h = h, w
    taken = _parse_date(exif.get_ifd(0x8769).get(0x9003)) or _parse_date(exif.get(0x0132))
    camera = exif.get(0x0110)
    return {"width": w, "height": h, "orientation": orientation, "taken": taken,
            "camera": str(camera).strip("\x00 ") if camera else None}


def filename_hint(path):
    """Words left in the file name after removing camera names, copy numbers and bare numbers, or None."""
    stem = os.path.splitext(os.path.basename(path))[0]
    stem = _CAMERA.sub(" ", stem)
    words = [w for w in re.split(r"[\s_\-.()]+", stem) if w and not w.isdigit()]
    if not any(re.search(r"[A-Za-z]{2}", w) for w in words):
        return None
    return " ".join(words)


def _generic(folder):
    return folder.strip().lower() in GENERIC_FOLDERS or bool(_DATE_LIKE.match(folder.strip())) or folder.isdigit()


def subfolder_hint(path, root):
    """The nearest subfolder inside root with a non-generic name, or None. root's own name never counts."""
    rel = os.path.relpath(os.path.dirname(path), root)
    if rel in (".", ""):
        return None
    for folder in reversed(rel.split(os.sep)):
        if not _generic(folder):
            return folder
    return None


def _iso(dt):
    return dt.isoformat() if dt else None


def group_shoots(items):
    """Group items (dicts with index, taken, camera) by shoot. Sets item['group'] and returns group summaries."""
    dated = sorted((i for i in items if i["taken"]), key=lambda i: (i["taken"], i["index"]))
    groups, current, prev = [], None, None
    for item in dated:
        if current is None or item["camera"] != prev["camera"] or item["taken"] - prev["taken"] > GROUP_GAP:
            current = []
            groups.append(current)
        current.append(item)
        prev = item
    undated = [i for i in items if not i["taken"]]
    if undated:
        groups.append(undated)
    summaries = []
    for n, group in enumerate(groups, 1):
        for item in group:
            item["group"] = n
        summaries.append({"id": n, "count": len(group), "indexes": [i["index"] for i in group],
                          "camera": group[0]["camera"], "start": _iso(group[0]["taken"]),
                          "end": _iso(group[-1]["taken"])})
    return summaries


def free_dir(path):
    """path if it doesn't exist yet, otherwise 'path (2)', 'path (3)' and so on."""
    if not os.path.exists(path):
        return path
    n = 2
    while os.path.exists(f"{path} ({n})"):
        n += 1
    return f"{path} ({n})"


def output_dir_for(src):
    """'<input name> - WordPress' next to the input folder or zip, made unique."""
    src = os.path.abspath(src.rstrip("/\\"))
    base = os.path.basename(src)
    if base.lower().endswith(".zip"):
        base = base[:-4]
    return free_dir(os.path.join(os.path.dirname(src), f"{base} - WordPress"))
