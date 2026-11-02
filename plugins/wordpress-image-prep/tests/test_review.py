import os
import re
import tempfile
import unittest
from urllib.parse import quote

import helpers  # noqa: F401  (sets sys.path)
import review


class ReviewPageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.out = os.path.join(self.tmp, "DLX Mattress + Helix - WordPress 2026-11-02")
        os.makedirs(self.out)
        self.results = []
        for i, name in enumerate(["side-sleeper-test-dlx-mattress", "full-view-helix-mattress"], 1):
            path = helpers.make_file(os.path.join(self.out, name + ".webp"), b"x")
            self.results.append({"source": f"/in/IMG_000{i}.HEIC", "product": "DLX <b>Mattress</b>", "output": path,
                                 "width": 800, "height": 450, "kb": 70, "narrow": False})
        self.results.append({"source": "/in/broken.jpg", "product": "Helix", "error": "can't be opened"})
        self.page = review.write_page(self.out, self.results, 5_000_000, 150_000,
                                      skipped=[{"path": "/in/clip.MOV", "reason": "video"}])
        with open(self.page, encoding="utf-8") as f:
            self.html = f.read()

    def test_page_sits_beside_the_folder_not_inside(self):
        self.assertEqual(self.page, self.out + " - review.html")
        self.assertEqual(sorted(os.listdir(self.out)),
                         ["full-view-helix-mattress.webp", "side-sleeper-test-dlx-mattress.webp"])

    def test_references_every_output_by_relative_path(self):
        folder = quote(os.path.basename(self.out))
        for r in self.results[:2]:
            self.assertIn(f'src="{folder}/{quote(os.path.basename(r["output"]))}"', self.html)

    def test_self_contained(self):
        self.assertNotRegex(self.html, r"(?i)https?:|src=\"//|href=\"//|@import")
        self.assertIn("<style>", self.html)

    def test_numbers_details_and_header(self):
        self.assertIn(">1<", self.html)
        self.assertIn(">2<", self.html)
        self.assertIn("IMG_0001.HEIC", self.html)
        self.assertIn("800 × 450", self.html)
        self.assertIn("2 images", self.html)
        self.assertIn("4.8 MB", self.html)
        self.assertIn("146 KB", self.html)
        self.assertIn("clip.MOV", self.html)
        self.assertIn("broken.jpg", self.html)

    def test_escapes_text(self):
        self.assertIn("DLX &lt;b&gt;Mattress&lt;/b&gt;", self.html)
        self.assertNotIn("<b>Mattress", self.html)

    def test_is_valid_utf8_html_document(self):
        self.assertTrue(self.html.startswith("<!doctype html>"))
        self.assertIn('<meta charset="utf-8">', self.html)
        self.assertEqual(len(re.findall(r"<img ", self.html)), 2)


if __name__ == "__main__":
    unittest.main()
