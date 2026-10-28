"""Contact sheets: numbered thumbnails Claude looks at instead of full-size photos."""
import os

from PIL import Image, ImageDraw, ImageFont

PER_SHEET = 6
COLS = 2
THUMB_W = 600
LABEL_H = 30


def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow older than 10.1
        return ImageFont.load_default()


def make_sheets(thumbs, out_dir, prefix, crop_guide=False):
    """thumbs: (label, image no wider than THUMB_W) pairs. Writes <prefix>-N.jpg into out_dir; returns the paths.

    crop_guide draws red lines where an 800x450 centre crop would fall, so Claude can judge focus_y.
    """
    font = _font(18)
    paths = []
    for start in range(0, len(thumbs), PER_SHEET):
        batch = thumbs[start:start + PER_SHEET]
        rows = (len(batch) + COLS - 1) // COLS
        cell_h = max(im.height for _, im in batch) + LABEL_H
        sheet = Image.new("RGB", (COLS * THUMB_W, rows * cell_h), "white")
        draw = ImageDraw.Draw(sheet)
        for i, (label, im) in enumerate(batch):
            x, y = (i % COLS) * THUMB_W, (i // COLS) * cell_h
            draw.rectangle([x, y, x + THUMB_W - 1, y + LABEL_H - 1], fill="black")
            draw.text((x + 6, y + 6), label[:64], fill="yellow", font=font)
            sheet.paste(im.convert("RGB"), (x, y + LABEL_H))
            band = round(im.width * 450 / 800)
            if crop_guide and im.height > band:
                top = y + LABEL_H + (im.height - band) // 2
                for line_y in (top, top + band):
                    draw.line([x, line_y, x + im.width - 1, line_y], fill=(230, 0, 0), width=3)
        path = os.path.join(out_dir, f"{prefix}-{start // PER_SHEET + 1}.jpg")
        sheet.save(path, quality=85)
        paths.append(path)
    return paths
