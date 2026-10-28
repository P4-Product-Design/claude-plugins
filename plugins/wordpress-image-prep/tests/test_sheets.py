import os
import tempfile
import unittest

from PIL import Image

import helpers  # noqa: F401
import sheets


class SheetsTest(unittest.TestCase):
    def test_six_per_sheet_two_columns(self):
        out = tempfile.mkdtemp()
        thumbs = [(str(i), Image.new("RGB", (600, 450), "grey")) for i in range(1, 8)]
        paths = sheets.make_sheets(thumbs, out, "scan")
        self.assertEqual([os.path.basename(p) for p in paths], ["scan-1.jpg", "scan-2.jpg"])
        with Image.open(paths[0]) as first, Image.open(paths[1]) as second:
            self.assertEqual(first.width, 1200)
            self.assertEqual(first.height, 3 * (450 + sheets.LABEL_H))
            self.assertEqual(second.height, 450 + sheets.LABEL_H)

    def test_crop_guide_draws_red_lines(self):
        out = tempfile.mkdtemp()
        paths = sheets.make_sheets([("1", Image.new("RGB", (600, 450), "grey"))], out, "g", crop_guide=True)
        band = round(600 * 450 / 800)
        top = sheets.LABEL_H + (450 - band) // 2
        with Image.open(paths[0]) as im:
            r, g, b = im.convert("RGB").getpixel((300, top))
        self.assertGreater(r, 150)
        self.assertLess(g, 100)


if __name__ == "__main__":
    unittest.main()
