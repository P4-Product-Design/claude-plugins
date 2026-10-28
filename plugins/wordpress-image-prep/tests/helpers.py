"""Shared test helpers: puts the skill's scripts on sys.path and builds synthetic images."""
import os
import sys

from PIL import Image

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(PLUGIN, "skills", "wordpress-image-prep", "scripts")
PREP = os.path.join(SCRIPTS, "prep.py")
sys.path.insert(0, SCRIPTS)


def make_jpeg(path, size=(1600, 1200), color=(128, 128, 128), fills=(), orientation=None, camera=None, taken=None):
    """Save a JPEG. fills: ((x0, y0, x1, y1), (r, g, b)) boxes painted on top. taken: 'YYYY:MM:DD HH:MM:SS'."""
    im = Image.new("RGB", size, color)
    for box, fill in fills:
        im.paste(fill, box)
    exif = Image.Exif()
    if orientation:
        exif[0x0112] = orientation
    if camera:
        exif[0x0110] = camera
    if taken:
        exif[0x0132] = taken
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "JPEG", exif=exif.tobytes(), quality=92)
    return path


def make_png(path, size=(600, 900), color=(30, 160, 90)):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.new("RGB", size, color).save(path, "PNG")
    return path


def make_file(path, data=b"not an image"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return path
