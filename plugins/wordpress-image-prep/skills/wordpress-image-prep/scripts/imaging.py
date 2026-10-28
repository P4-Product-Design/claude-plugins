"""Pixel work (spec section 4): open any supported image upright and in sRGB, resize, crop, save as WebP."""
import io
import os
import shutil
import subprocess
import tempfile

from PIL import Image, ImageCms, ImageOps

TARGET_W = 800
MAX_H = 450
WEBP_QUALITY = 90
HEIC_EXT = {".heic", ".heif"}
_ROTATE = {90: Image.Transpose.ROTATE_270, 180: Image.Transpose.ROTATE_180, 270: Image.Transpose.ROTATE_90}

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_DECODER = "pillow-heif"
except ImportError:
    HEIC_DECODER = "sips" if shutil.which("sips") else None


def is_heic(path):
    return os.path.splitext(path)[1].lower() in HEIC_EXT


def open_image(path):
    """Open and load an image. HEIC goes through pillow-heif, or macOS sips when pillow-heif is missing."""
    if is_heic(path) and HEIC_DECODER != "pillow-heif":
        if HEIC_DECODER != "sips":
            raise RuntimeError("HEIC support isn't available on this computer")
        return _open_with_sips(path)
    im = Image.open(path)
    im.load()
    return im


def _open_with_sips(path):
    fd, tmp = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        subprocess.run(["sips", "-s", "format", "png", path, "--out", tmp], check=True, capture_output=True)
        im = Image.open(tmp)
        im.load()
        return im
    finally:
        os.remove(tmp)


def to_srgb(im, icc):
    """Convert from the embedded profile (iPhone HEICs are Display P3) to sRGB, keeping alpha if there is any."""
    mode = "RGBA" if ("A" in im.getbands() or "transparency" in im.info) else "RGB"
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            im = ImageCms.profileToProfile(im, src, ImageCms.createProfile("sRGB"), outputMode=mode)
        except (ImageCms.PyCMSError, OSError, ValueError):
            pass
    return im if im.mode == mode else im.convert(mode)


def open_upright(path, rotate=0):
    """Open, apply the EXIF orientation, then turn `rotate` degrees clockwise, in sRGB."""
    im = open_image(path)
    icc = im.info.get("icc_profile")
    im = ImageOps.exif_transpose(im)
    if rotate:
        im = im.transpose(_ROTATE[rotate])
    return to_srgb(im, icc)


def fit(im, focus_y=0.5):
    """Scale to TARGET_W wide (never up), then crop the height to MAX_H, centred on focus_y (0 top, 1 bottom)."""
    w, h = im.size
    if w > TARGET_W:
        h = round(h * TARGET_W / w)
        w = TARGET_W
        im = im.resize((w, h), Image.Resampling.LANCZOS)
    if h > MAX_H:
        top = round(focus_y * h - MAX_H / 2)
        top = max(0, min(top, h - MAX_H))
        im = im.crop((0, top, w, top + MAX_H))
    return im


def thumbnail(path, width, rotate=0):
    im = open_upright(path, rotate)
    im.thumbnail((width, width * 3), Image.Resampling.LANCZOS)
    return im


def process_image(src, dest, focus_y=0.5, rotate=0):
    """Write one WordPress-ready WebP. Returns its pixel size, file size and whether the source was under 800px wide."""
    im = open_upright(src, rotate)
    narrow = im.width < TARGET_W
    im = fit(im, focus_y)
    im.info.pop("exif", None)
    im.info.pop("icc_profile", None)
    im.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
    return {"width": im.width, "height": im.height, "kb": round(os.path.getsize(dest) / 1024), "narrow": narrow}
