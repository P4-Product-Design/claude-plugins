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


class FitnessNameTest(unittest.TestCase):
    """Shane Johnson's GGR/BarBend examples: descriptive phrases that keep the connecting words."""

    def test_shanes_examples(self):
        cases = {
            "Our product tester stepping into the Renu Stoic 3.0 Cold Plunge":
                "our-product-tester-stepping-into-the-renu-stoic-3-cold-plunge",
            "Temperature display on the control panel of a Renu Stoic 3.0 Cold Plunge tub":
                "temperature-display-on-the-control-panel-of-a-renu-stoic-3-cold-plunge-tub",
            "Close-up of our tester soaking in the Renu Stoic 3.0 Cold Plunge":
                "close-up-of-our-tester-soaking-in-the-renu-stoic-3-cold-plunge",
        }
        for text, expected in cases.items():
            self.assertEqual(naming.normalize_name(text, "fitness"), expected)

    def test_sleep_still_drops_connecting_words(self):
        self.assertEqual(naming.normalize_name("Our tester stepping into the Renu Stoic 3.0 Cold Plunge", "sleep"),
                         "tester-stepping-into-renu-stoic-3-cold-plunge")

    def test_fitness_length_limit(self):
        with self.assertRaises(ValueError):
            naming.normalize_name("our product tester carefully stepping into the deep end of the renu stoic 3.0 "
                                  "cold plunge tub in the garage", "fitness")

    def test_fitness_still_rejects_camera_names(self):
        with self.assertRaises(ValueError):
            naming.normalize_name("IMG_1949 our tester on the bench", "fitness")

    def test_unknown_site_type(self):
        with self.assertRaises(ValueError):
            naming.normalize_name("full view", "garden")


class VersionTest(unittest.TestCase):
    def test_trailing_point_zero_drops(self):
        for site in ("sleep", "fitness"):
            self.assertEqual(naming.normalize_name("full view renu stoic 3.0 cold plunge", site),
                             "full-view-renu-stoic-3-cold-plunge")
            self.assertEqual(naming.normalize_name("full view stoic 10.0", site), "full-view-stoic-10")

    def test_other_dotted_versions_stay(self):
        self.assertEqual(naming.normalize_name("full view stoic 2.5 cold plunge"), "full-view-stoic-2-5-cold-plunge")
        self.assertEqual(naming.normalize_name("full view stoic 3.05"), "full-view-stoic-3-05")

    def test_slug(self):
        self.assertEqual(naming.slug("Renu Stoic 3.0"), "renu-stoic-3")
        self.assertEqual(naming.slug("The Nécessaire Pillow 2.5"), "the-necessaire-pillow-2-5")
        with self.assertRaises(ValueError):
            naming.slug(" ? ")


class ReviewOrderTest(unittest.TestCase):
    def order(self, names):
        return [names[i] for i in naming.review_order(names)]

    def test_alphabetical_with_copies_in_number_order(self):
        names = naming.assign_unique(["b"] + ["a"] * 11 + ["a-b"])
        self.assertEqual(self.order(names), ["a"] + [f"a-{n}" for n in range(2, 12)] + ["a-b", "b"])

    def test_base_before_copies_mid_name_numbers(self):
        names = ["stoic-3-cold-plunge-10", "stoic-3-cold-plunge-2", "stoic-3-cold-plunge", "stoic-10", "stoic-2"]
        self.assertEqual(self.order(names), ["stoic-2", "stoic-3-cold-plunge", "stoic-3-cold-plunge-2",
                                             "stoic-3-cold-plunge-10", "stoic-10"])


class AssignUniqueTest(unittest.TestCase):
    def test_first_keeps_name_later_get_numbers(self):
        self.assertEqual(naming.assign_unique(["a", "b", "a", "a"]), ["a", "b", "a-2", "a-3"])

    def test_skips_numbers_already_in_use(self):
        self.assertEqual(naming.assign_unique(["a", "a-2", "a"]), ["a", "a-2", "a-3"])


if __name__ == "__main__":
    unittest.main()
