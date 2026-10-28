import os
import tempfile
import unittest

from PIL import Image

import helpers
import imaging

RED, BLUE, WHITE, GREY = (220, 20, 20), (20, 20, 220), (255, 255, 255), (128, 128, 128)


class ProcessImageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def path(self, name):
        return os.path.join(self.tmp, name)

    def test_landscape_4_3_becomes_800x450_webp(self):
        src = helpers.make_jpeg(self.path("a.jpg"), size=(4032, 3024))
        info = imaging.process_image(src, self.path("a.webp"))
        with Image.open(self.path("a.webp")) as out:
            self.assertEqual(out.format, "WEBP")
            self.assertEqual(out.size, (800, 450))
        self.assertEqual((info["width"], info["height"]), (800, 450))
        self.assertFalse(info["narrow"])

    def test_applies_exif_orientation(self):
        # Stored with red on top and orientation 3 (180°), so upright the top is blue.
        src = helpers.make_jpeg(self.path("o.jpg"), fills=[((0, 0, 1600, 600), RED), ((0, 600, 1600, 1200), BLUE)],
                                orientation=3)
        imaging.process_image(src, self.path("o.webp"))
        with Image.open(self.path("o.webp")) as out:
            r, g, b = out.convert("RGB").getpixel((400, 10))
        self.assertGreater(b, r)

    def test_rotate_turns_clockwise_after_orientation(self):
        src = helpers.make_jpeg(self.path("r.jpg"), size=(1600, 900))
        imaging.process_image(src, self.path("r.webp"), rotate=90)
        with Image.open(self.path("r.webp")) as out:
            self.assertEqual(out.size, (800, 450))  # 900x1600 -> 800x1422 -> cropped to 450

    def test_focus_y_moves_the_crop(self):
        # White band in the top 100 original rows (top 50 after scaling to 800 wide).
        src = helpers.make_jpeg(self.path("f.jpg"), fills=[((0, 0, 1600, 100), WHITE)])
        imaging.process_image(src, self.path("top.webp"), focus_y=0.0)
        imaging.process_image(src, self.path("bottom.webp"), focus_y=1.0)
        with Image.open(self.path("top.webp")) as top, Image.open(self.path("bottom.webp")) as bottom:
            self.assertGreater(min(top.convert("RGB").getpixel((400, 10))), 230)
            self.assertLess(max(bottom.convert("RGB").getpixel((400, 10))), 160)

    def test_never_upscales_narrow_images(self):
        src = helpers.make_png(self.path("n.png"), size=(600, 900))
        info = imaging.process_image(src, self.path("n.webp"))
        self.assertEqual((info["width"], info["height"]), (600, 450))
        self.assertTrue(info["narrow"])

    def test_short_images_are_not_cropped(self):
        src = helpers.make_jpeg(self.path("s.jpg"), size=(1600, 600))
        info = imaging.process_image(src, self.path("s.webp"))
        self.assertEqual((info["width"], info["height"]), (800, 300))

    def test_strips_metadata(self):
        src = helpers.make_jpeg(self.path("m.jpg"), camera="iPhone 12 Pro Max", taken="2025:06:19 17:25:37")
        imaging.process_image(src, self.path("m.webp"))
        with Image.open(self.path("m.webp")) as out:
            self.assertNotIn("exif", out.info)
            self.assertNotIn("icc_profile", out.info)
            self.assertEqual(len(out.getexif()), 0)

    def test_heic(self):
        try:
            import pillow_heif
        except ImportError:
            self.skipTest("pillow-heif not installed")
        src = self.path("h.heic")
        pillow_heif.from_pillow(Image.new("RGB", (1200, 900), RED)).save(src, quality=90)
        info = imaging.process_image(src, self.path("h.webp"))
        self.assertEqual((info["width"], info["height"]), (800, 450))


class FitTest(unittest.TestCase):
    def test_crop_is_clamped_inside_the_image(self):
        out = imaging.fit(Image.new("RGB", (800, 600)), focus_y=1.0)
        self.assertEqual(out.size, (800, 450))


if __name__ == "__main__":
    unittest.main()
