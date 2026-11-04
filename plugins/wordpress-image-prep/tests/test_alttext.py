import os
import tempfile
import unittest

import helpers
import alttext


class CheckTest(unittest.TestCase):
    def test_good_alt_text(self):
        problems, warnings = alttext.check("Our tester stepping into the Renu Stoic 3.0 Cold Plunge",
                                           "Renu Stoic 3.0 Cold Plunge")
        self.assertEqual((problems, warnings), ([], []))

    def test_rejects_empty_image_of_and_too_long(self):
        for bad in ("", "  ", "Image of our tester in the DLX Mattress", "photo of the DLX Mattress",
                    "Picture of the DLX Mattress", "Our tester " + "x" * alttext.MAX_LEN + " DLX Mattress"):
            problems, _ = alttext.check(bad, "DLX Mattress")
            self.assertTrue(problems, bad)

    def test_warns_when_product_name_missing_or_long(self):
        _, warnings = alttext.check("Our tester lying on the mattress", "DLX Mattress")
        self.assertTrue(warnings)
        _, warnings = alttext.check("Our tester lying on her side on the DLX Mattress " + "x" * 90, "DLX Mattress")
        self.assertTrue(warnings)

    def test_tester_balance(self):
        self.assertIsNone(alttext.tester_balance(["our tester a", "our product tester b", "our tester c"]))
        self.assertIsNone(alttext.tester_balance(["no people here", "the tub"]))
        self.assertIsNotNone(alttext.tester_balance(["our product tester a", "Our product tester b", "c"]))
        self.assertIsNotNone(alttext.tester_balance(["our-tester-a", "our-tester-b", "our-tester-c", "our-product-tester"]))


class WriteFilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.out = os.path.join(self.tmp, "Renu Stoic 3.0 Cold Plunge + DLX Mattress - WordPress 2026-11-04")
        os.makedirs(self.out)
        self.entries = [
            {"output": os.path.join(self.out, "close-up-of-our-tester.webp"), "product": "Renu Stoic 3.0 Cold Plunge",
             "alt": "Close-up of our tester soaking in the Renu Stoic 3.0 Cold Plunge"},
            {"output": os.path.join(self.out, "full-view-dlx-mattress.webp"), "product": "DLX Mattress",
             "alt": "The DLX Mattress on a black bed frame"},
            {"output": os.path.join(self.out, "our-product-tester.webp"), "product": "Renu Stoic 3.0 Cold Plunge",
             "alt": "Our product tester stepping into the Renu Stoic 3.0 Cold Plunge"},
        ]
        self.slugs = {"Renu Stoic 3.0 Cold Plunge": "Renu Stoic 3.0", "DLX Mattress": "dlx"}

    def test_one_file_per_product_beside_the_folder(self):
        paths = alttext.write_files(self.out, self.entries, self.slugs)
        self.assertEqual(sorted(os.path.basename(p) for p in paths),
                         ["dlx-alt-text-descriptions.txt", "renu-stoic-3-alt-text-descriptions.txt"])
        self.assertTrue(all(os.path.dirname(p) == self.tmp for p in paths))
        self.assertEqual(len(os.listdir(self.out)), 0)
        with open(os.path.join(self.tmp, "renu-stoic-3-alt-text-descriptions.txt"), encoding="utf-8") as f:
            self.assertEqual(f.read().splitlines(), [
                "close-up-of-our-tester.webp: Close-up of our tester soaking in the Renu Stoic 3.0 Cold Plunge",
                "our-product-tester.webp: Our product tester stepping into the Renu Stoic 3.0 Cold Plunge"])

    def test_never_overwrites_a_file_from_another_batch(self):
        old = helpers.make_file(os.path.join(self.tmp, "dlx-alt-text-descriptions.txt"), b"older batch")
        paths = alttext.write_files(self.out, self.entries, self.slugs)
        self.assertIn(os.path.join(self.tmp, "dlx-alt-text-descriptions (2).txt"), paths)
        with open(old, "rb") as f:
            self.assertEqual(f.read(), b"older batch")


if __name__ == "__main__":
    unittest.main()
