import os
import tempfile
import unittest
import zipfile
from datetime import date, datetime

import helpers
import inventory


class HintTest(unittest.TestCase):
    def test_filename_hint(self):
        self.assertIsNone(inventory.filename_hint("/x/IMG_1949 2.HEIC"))
        self.assertIsNone(inventory.filename_hint("/x/DSC0042.jpg"))
        self.assertEqual(inventory.filename_hint("/x/Helix Midnight Luxe IMG_1949.HEIC"), "Helix Midnight Luxe")
        self.assertEqual(inventory.filename_hint("/x/helix-midnight-luxe_IMG_1949.jpg"), "helix midnight luxe")

    def test_subfolder_hint(self):
        root = "/batch"
        self.assertEqual(inventory.subfolder_hint("/batch/Helix Midnight Luxe/a.jpg", root), "Helix Midnight Luxe")
        self.assertEqual(inventory.subfolder_hint("/batch/Saatva Classic/HEIC/a.heic", root), "Saatva Classic")
        self.assertIsNone(inventory.subfolder_hint("/batch/Photos/a.jpg", root))
        self.assertIsNone(inventory.subfolder_hint("/batch/2025-06-19/a.jpg", root))
        self.assertIsNone(inventory.subfolder_hint("/batch/a.jpg", root))


class FolderNameTest(unittest.TestCase):
    DAY = date(2026, 10, 28)

    def test_one_product(self):
        self.assertEqual(inventory.folder_name(["DLX Mattress", "dlx mattress"], self.DAY),
                         "DLX Mattress - WordPress 2026-10-28")

    def test_two_products_in_batch_order(self):
        self.assertEqual(inventory.folder_name(["Helix Midnight Luxe", "DLX Mattress", "Helix Midnight Luxe"], self.DAY),
                         "Helix Midnight Luxe + DLX Mattress - WordPress 2026-10-28")

    def test_three_or_more_products(self):
        self.assertEqual(inventory.folder_name(["DLX Mattress", "Helix", "Saatva Classic"], self.DAY),
                         "DLX Mattress + 2 more - WordPress 2026-10-28")

    def test_removes_characters_windows_rejects(self):
        self.assertEqual(inventory.folder_name(['Nectar 14" / Premier: v2?.'], self.DAY),
                         "Nectar 14 Premier v2 - WordPress 2026-10-28")

    def test_long_names_are_shortened(self):
        long_a, long_b = "Brooklyn Bedding Aurora Luxe Cooling Hybrid", "Serta Perfect Sleeper X Mattress"
        self.assertEqual(inventory.folder_name([long_a, long_b], self.DAY),
                         long_a + " + 1 more - WordPress 2026-10-28")
        name = inventory.folder_name(["x" * 100], self.DAY)
        self.assertEqual(name, "x" * inventory.MAX_LABEL + " - WordPress 2026-10-28")

    def test_needs_a_product(self):
        with self.assertRaises(ValueError):
            inventory.folder_name(["", " ? "], self.DAY)


class GroupTest(unittest.TestCase):
    def item(self, index, camera, hhmm):
        taken = datetime(2025, 6, 19, int(hhmm[:2]), int(hhmm[2:])) if hhmm else None
        return {"index": index, "camera": camera, "taken": taken}

    def test_splits_on_gap_camera_and_missing_date(self):
        items = [self.item(1, "A", "1000"), self.item(2, "A", "1010"), self.item(3, "A", "1100"),
                 self.item(4, "B", "1101"), self.item(5, None, None)]
        groups = inventory.group_shoots(items)
        self.assertEqual([g["indexes"] for g in groups], [[1, 2], [3], [4], [5]])
        self.assertEqual([i["group"] for i in items], [1, 1, 2, 3, 4])
        self.assertEqual(groups[0]["start"], "2025-06-19T10:00:00")


class FilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_list_files_sorts_and_skips(self):
        root = os.path.join(self.tmp, "in")
        helpers.make_jpeg(os.path.join(root, "b.jpg"))
        helpers.make_png(os.path.join(root, "sub", "a.png"))
        helpers.make_file(os.path.join(root, "clip.MOV"))
        helpers.make_file(os.path.join(root, "notes.txt"))
        helpers.make_file(os.path.join(root, ".DS_Store"))
        helpers.make_file(os.path.join(root, "__MACOSX", "._b.jpg"))
        images, skipped = inventory.list_files(root)
        self.assertEqual([os.path.relpath(p, root) for p in images], ["b.jpg", os.path.join("sub", "a.png")])
        self.assertEqual(sorted((os.path.basename(s["path"]), s["reason"]) for s in skipped),
                         [("clip.MOV", "video"), ("notes.txt", "not an image")])

    def test_unpack_zip_ignores_escaping_entries(self):
        src = os.path.join(self.tmp, "batch.zip")
        with zipfile.ZipFile(src, "w") as z:
            z.writestr("Helix/a.jpg", b"x")
            z.writestr("../evil.txt", b"x")
        root = inventory.unpack(src, os.path.join(self.tmp, "work"))
        self.assertTrue(os.path.isfile(os.path.join(root, "Helix", "a.jpg")))
        self.assertFalse(os.path.exists(os.path.join(root, "evil.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "work", "evil.txt")))

    def test_unpack_folder_returns_it(self):
        self.assertEqual(inventory.unpack(self.tmp, self.tmp), self.tmp)

    def test_free_dir(self):
        base = os.path.join(self.tmp, "Batch - WordPress")
        self.assertEqual(inventory.free_dir(base), base)
        os.makedirs(base)
        self.assertEqual(inventory.free_dir(base), base + " (2)")
        os.makedirs(base + " (2)")
        self.assertEqual(inventory.free_dir(base), base + " (3)")

    def test_output_parent_for_zip_and_folder(self):
        folder = os.path.join(self.tmp, "Central Testing Images")
        os.makedirs(folder)
        self.assertEqual(inventory.output_parent_for(folder + os.sep), self.tmp)
        self.assertEqual(inventory.output_parent_for(os.path.join(self.tmp, "batch.zip")), self.tmp)

    def test_read_meta(self):
        p = helpers.make_jpeg(os.path.join(self.tmp, "m.jpg"), size=(1600, 1200), orientation=6,
                              camera="iPhone 15 Pro Max", taken="2025:05:21 20:28:05")
        meta = inventory.read_meta(p)
        self.assertEqual((meta["width"], meta["height"]), (1200, 1600))  # orientation 6 is portrait
        self.assertEqual(meta["camera"], "iPhone 15 Pro Max")
        self.assertEqual(meta["taken"], datetime(2025, 5, 21, 20, 28, 5))


if __name__ == "__main__":
    unittest.main()
