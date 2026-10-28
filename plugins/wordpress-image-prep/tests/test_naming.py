import unittest

import helpers  # noqa: F401  (sets sys.path)
import naming


class NormalizeNameTest(unittest.TestCase):
    def test_removes_filler_words_and_lowercases(self):
        self.assertEqual(naming.normalize_name("Seated edge support test on the DLX mattress"),
                         "seated-edge-support-test-dlx-mattress")

    def test_transliterates_accents(self):
        self.assertEqual(naming.normalize_name("Thermal imaging of the Nécessaire pillow"),
                         "thermal-imaging-necessaire-pillow")

    def test_strips_size_suffix_and_extension(self):
        self.assertEqual(naming.normalize_name("seated-edge-support-test-dlx-mattress-768x432.webp"),
                         "seated-edge-support-test-dlx-mattress")

    def test_drops_image_photo_picture(self):
        self.assertEqual(naming.normalize_name("photo of the full view dlx mattress"),
                         "full-view-dlx-mattress")

    def test_keeps_meaning_words(self):
        self.assertEqual(naming.normalize_name("thermal imaging after use on the Helix mattress"),
                         "thermal-imaging-after-use-helix-mattress")

    def test_rejects_camera_names(self):
        for bad in ("IMG_1949 dlx mattress", "DSC0042-dlx-mattress", "PXL_20250619 dlx mattress"):
            with self.assertRaises(ValueError):
                naming.normalize_name(bad)

    def test_rejects_names_over_80_characters(self):
        with self.assertRaises(ValueError):
            naming.normalize_name("our tester measures the sinkage from weight plates along the edge "
                                  "of the serta perfect sleeper x mattress during testing")

    def test_rejects_names_with_no_words_left(self):
        with self.assertRaises(ValueError):
            naming.normalize_name("the of on")


class AssignUniqueTest(unittest.TestCase):
    def test_first_keeps_name_later_get_numbers(self):
        self.assertEqual(naming.assign_unique(["a", "b", "a", "a"]), ["a", "b", "a-2", "a-3"])

    def test_skips_numbers_already_in_use(self):
        self.assertEqual(naming.assign_unique(["a", "a-2", "a"]), ["a", "a-2", "a-3"])


if __name__ == "__main__":
    unittest.main()
