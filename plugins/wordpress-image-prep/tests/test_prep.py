import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date

from PIL import Image

import helpers


def run(*args):
    out = subprocess.run([sys.executable, helpers.PREP] + list(args), capture_output=True, text=True)
    return out.returncode, json.loads(out.stdout)


def digest(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


SLUGS = {"DLX Mattress": "DLX", "Saatva Classic": "Saatva Classic", "Helix Midnight Luxe": "Helix Midnight Luxe"}


def alt_file(folder, slug):
    with open(os.path.join(folder, f"{slug}-alt-text-descriptions.txt"), encoding="utf-8") as f:
        return f.read().splitlines()


class PrepTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp, "Batch")
        self.a = helpers.make_jpeg(os.path.join(self.src, "IMG_0001.jpg"), camera="A", taken="2025:06:19 10:00:00")
        self.b = helpers.make_jpeg(os.path.join(self.src, "IMG_0002.jpg"), camera="A", taken="2025:06:19 10:05:00")
        self.c = helpers.make_jpeg(os.path.join(self.src, "Saatva Classic", "IMG_0003.jpg"), camera="B",
                                   taken="2025:05:21 09:00:00")
        helpers.make_file(os.path.join(self.src, "clip.mov"))
        self.before = {p: digest(p) for p in (self.a, self.b, self.c)}

    def manifest(self, scan, names, products=("DLX Mattress", "DLX Mattress", "Saatva Classic"), alts=None,
                 site_type="sleep", **extra):
        alts = alts or [f"Our tester checking shot {n} of the {pr}" for n, pr in enumerate(products, 1)]
        data = {"output_parent": scan["output_parent"],
                "product_slugs": {pr: SLUGS[pr] for pr in products if pr in SLUGS}, "images": [
                    {"source": p, "name": n, "product": pr, "alt": a, "focus_y": 0.5}
                    for p, n, pr, a in zip((self.a, self.b, self.c), names, products, alts)]}
        if site_type is not None:
            data["site_type"] = site_type
        data.update(extra)
        path = os.path.join(scan["work_dir"], "manifest.json")
        with open(path, "w") as f:
            json.dump(data, f)
        return path

    def test_scan(self):
        code, scan = run("scan", self.src)
        self.assertEqual(code, 0)
        self.assertEqual(len(scan["images"]), 3)
        self.assertEqual(scan["skipped"], [{"path": os.path.join(self.src, "clip.mov"), "reason": "video"}])
        self.assertEqual([g["count"] for g in scan["groups"]], [1, 2])  # May shoot first, then June
        self.assertEqual(scan["output_parent"], self.tmp)
        by_path = {i["path"]: i for i in scan["images"]}
        self.assertEqual(by_path[self.c]["subfolder_hint"], "Saatva Classic")
        self.assertIsNone(by_path[self.a]["filename_hint"])
        self.assertTrue(all(os.path.isfile(s) for s in scan["sheets"]))

    def test_apply_writes_webps_and_leaves_originals(self):
        _, scan = run("scan", self.src)
        names = ["Side sleeper test on the DLX mattress", "side-sleeper-test-dlx-mattress", "full view saatva classic mattress"]
        code, result = run("apply", self.manifest(scan, names))
        self.assertEqual(code, 0, result)
        self.assertEqual(result["output_dir"],
                         os.path.join(self.tmp, f"DLX Mattress + Saatva Classic - WordPress {date.today().isoformat()}"))
        self.assertEqual([r["product"] for r in result["results"]], ["Saatva Classic", "DLX Mattress", "DLX Mattress"])
        outs = sorted(os.listdir(result["output_dir"]))
        self.assertEqual(outs, ["full-view-saatva-classic-mattress.webp", "side-sleeper-test-dlx-mattress-2.webp",
                                "side-sleeper-test-dlx-mattress.webp"])
        for name in outs:
            with Image.open(os.path.join(result["output_dir"], name)) as im:
                self.assertEqual(im.size, (800, 450))
        self.assertEqual({p: digest(p) for p in self.before}, self.before)
        self.assertTrue(all(os.path.isfile(s) for s in result["check_sheets"]))
        self.assertGreater(result["bytes_before"], result["bytes_after"])

        code, again = run("apply", self.manifest(scan, names))
        self.assertEqual(again["output_dir"], result["output_dir"] + " (2)")

    def test_apply_rejects_bad_manifest_and_writes_nothing(self):
        _, scan = run("scan", self.src)
        code, result = run("apply", self.manifest(scan, ["IMG_0001", "ok name", "ok name"]))
        self.assertEqual(code, 1)
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["problems"]), 1)
        self.assertEqual(os.listdir(self.tmp), ["Batch"])

    def test_apply_needs_a_product_for_every_photo(self):
        _, scan = run("scan", self.src)
        code, result = run("apply", self.manifest(scan, ["a dlx mattress", "b dlx mattress", "c dlx mattress"],
                                                  products=("DLX Mattress", "", "DLX Mattress")))
        self.assertEqual(code, 1)
        self.assertEqual([p["source"] for p in result["problems"]], [self.b])
        self.assertEqual(os.listdir(self.tmp), ["Batch"])

    def test_apply_preview_writes_into_work_dir(self):
        _, scan = run("scan", self.src)
        code, result = run("apply", "--preview", self.manifest(scan, ["a dlx mattress", "b dlx mattress", "c dlx mattress"]))
        self.assertEqual(code, 0)
        self.assertEqual(result["output_dir"], os.path.join(scan["work_dir"], "preview"))
        self.assertEqual(os.listdir(self.tmp), ["Batch"])
        self.assertIsNone(result["review_page"])
        self.assertFalse(os.path.exists(os.path.join(scan["work_dir"], "last-run.json")))

    def test_apply_writes_review_page_beside_folder(self):
        _, scan = run("scan", self.src)
        code, result = run("apply", self.manifest(scan, ["a dlx mattress", "b dlx mattress", "c saatva classic mattress"]))
        self.assertEqual(code, 0, result)
        page = result["review_page"]
        self.assertEqual(page, result["output_dir"] + " - review.html")
        self.assertTrue(os.path.isfile(page))
        self.assertNotIn("review.html", " ".join(os.listdir(result["output_dir"])))
        with open(page, encoding="utf-8") as f:
            html = f.read()
        for r in result["results"]:
            self.assertIn(os.path.basename(r["output"]), html)

    def redo(self, scan, names, **kw):
        return run("apply", "--redo", self.manifest(scan, names, **kw))

    def test_redo_rewrites_the_same_folder(self):
        _, scan = run("scan", self.src)
        _, first = run("apply", self.manifest(scan, ["a dlx mattress", "b dlx mattress", "c saatva classic mattress"]))
        out = first["output_dir"]
        helpers.make_file(os.path.join(out, ".DS_Store"))  # Finder adds these; they don't count as foreign files
        neighbour = helpers.make_file(os.path.join(self.tmp, "notes.txt"), b"keep me")
        code, result = self.redo(scan, ["back sleeper test dlx mattress", "b dlx mattress", "c saatva classic mattress"])
        self.assertEqual(code, 0, result)
        self.assertEqual(result["output_dir"], out)
        self.assertEqual(sorted(f for f in os.listdir(out) if not f.startswith(".")),
                         ["b-dlx-mattress.webp", "back-sleeper-test-dlx-mattress.webp", "c-saatva-classic-mattress.webp"])
        self.assertFalse(os.path.exists(out + " (2)"))
        with open(neighbour, "rb") as f:
            self.assertEqual(f.read(), b"keep me")
        self.assertEqual({p: digest(p) for p in self.before}, self.before)
        with open(result["review_page"], encoding="utf-8") as f:
            self.assertIn("back-sleeper-test-dlx-mattress.webp", f.read())

    def test_redo_renames_folder_when_products_change(self):
        _, scan = run("scan", self.src)
        _, first = run("apply", self.manifest(scan, ["a dlx mattress", "b dlx mattress", "c saatva classic mattress"]))
        names = ["a helix mattress", "b helix mattress", "c helix mattress"]
        code, result = self.redo(scan, names, products=("Helix Midnight Luxe",) * 3)
        self.assertEqual(code, 0, result)
        self.assertEqual(result["output_dir"],
                         os.path.join(self.tmp, f"Helix Midnight Luxe - WordPress {date.today().isoformat()}"))
        self.assertEqual(result["review_page"], result["output_dir"] + " - review.html")
        self.assertFalse(os.path.exists(first["output_dir"]))
        self.assertFalse(os.path.exists(first["review_page"]))
        self.assertEqual(len(os.listdir(result["output_dir"])), 3)

    def test_redo_refuses_without_a_record(self):
        _, scan = run("scan", self.src)
        code, result = self.redo(scan, ["a dlx mattress", "b dlx mattress", "c dlx mattress"])
        self.assertEqual(code, 1)
        self.assertFalse(result["ok"])
        self.assertIn("no earlier run", result["problems"][0]["problem"])
        self.assertEqual(os.listdir(self.tmp), ["Batch"])

    def test_redo_refuses_when_folder_has_other_files(self):
        _, scan = run("scan", self.src)
        _, first = run("apply", self.manifest(scan, ["a dlx mattress", "b dlx mattress", "c dlx mattress"]))
        extra = helpers.make_file(os.path.join(first["output_dir"], "extra.jpg"))
        code, result = self.redo(scan, ["x dlx mattress", "b dlx mattress", "c dlx mattress"])
        self.assertEqual(code, 1)
        self.assertIn("extra.jpg", result["problems"][0]["problem"])
        self.assertTrue(os.path.isfile(extra))
        self.assertTrue(all(os.path.isfile(r["output"]) for r in first["results"]))

    def test_site_type_is_required(self):
        _, scan = run("scan", self.src)
        for site_type in (None, "garden"):
            code, result = run("apply", self.manifest(scan, ["b dlx mattress", "c dlx mattress", "d saatva mattress"],
                                                      site_type=site_type))
            self.assertEqual(code, 1)
            self.assertIn("site_type", result["problems"][0]["problem"])
        self.assertEqual(os.listdir(self.tmp), ["Batch"])

    def test_fitness_names_keep_connecting_words(self):
        _, scan = run("scan", self.src)
        names = ["Our tester stepping into the DLX Mattress", "Our product tester lying on the DLX Mattress",
                 "Side view of the Saatva Classic"]
        code, result = run("apply", self.manifest(scan, names, site_type="fitness"))
        self.assertEqual(code, 0, result)
        self.assertEqual([os.path.basename(r["output"]) for r in result["results"]],
                         ["our-product-tester-lying-on-the-dlx-mattress.webp",
                          "our-tester-stepping-into-the-dlx-mattress.webp", "side-view-of-the-saatva-classic.webp"])

    def test_results_and_review_page_in_name_order(self):
        _, scan = run("scan", self.src)
        code, result = run("apply", self.manifest(scan, ["zebra view dlx mattress", "alpha view dlx mattress",
                                                         "zebra view dlx mattress"]))
        self.assertEqual(code, 0, result)
        names = [os.path.basename(r["output"]) for r in result["results"]]
        self.assertEqual(names, ["alpha-view-dlx-mattress.webp", "zebra-view-dlx-mattress.webp",
                                 "zebra-view-dlx-mattress-2.webp"])
        self.assertEqual([r["number"] for r in result["results"]], [1, 2, 3])
        with open(result["review_page"], encoding="utf-8") as f:
            page = f.read()
        self.assertEqual(sorted(names, key=page.index), names)

    def test_alt_text_files_beside_folder_one_per_product(self):
        _, scan = run("scan", self.src)
        alts = ["Our tester lying on the DLX Mattress", "Our product tester sitting on the DLX Mattress",
                "The Saatva Classic on a bed frame"]
        code, result = run("apply", self.manifest(scan, ["zebra dlx mattress", "alpha dlx mattress",
                                                         "full view saatva classic mattress"], alts=alts))
        self.assertEqual(code, 0, result)
        self.assertEqual(sorted(os.path.basename(p) for p in result["alt_text_files"]),
                         ["dlx-alt-text-descriptions.txt", "saatva-classic-alt-text-descriptions.txt"])
        self.assertTrue(all(os.path.dirname(p) == self.tmp for p in result["alt_text_files"]))
        self.assertFalse(any(f.endswith(".txt") for f in os.listdir(result["output_dir"])))
        self.assertEqual(alt_file(self.tmp, "dlx"), [
            "alpha-dlx-mattress.webp: Our product tester sitting on the DLX Mattress",
            "zebra-dlx-mattress.webp: Our tester lying on the DLX Mattress"])
        self.assertEqual(alt_file(self.tmp, "saatva-classic"),
                         ["full-view-saatva-classic-mattress.webp: The Saatva Classic on a bed frame"])

    def test_bad_alt_text_or_missing_slug_is_rejected(self):
        _, scan = run("scan", self.src)
        names = ["b dlx mattress", "c dlx mattress", "d saatva mattress"]
        code, result = run("apply", self.manifest(scan, names, alts=["Image of the DLX Mattress",
                                                                     "Our tester on the DLX Mattress",
                                                                     "The Saatva Classic"]))
        self.assertEqual(code, 1)
        self.assertIn("Image of", result["problems"][0]["problem"])
        code, result = run("apply", self.manifest(scan, names, product_slugs={"DLX Mattress": "dlx"}))
        self.assertEqual(code, 1)
        self.assertIn("Saatva Classic", result["problems"][0]["problem"])
        self.assertEqual(os.listdir(self.tmp), ["Batch"])

    def test_redo_rewrites_alt_text_files(self):
        _, scan = run("scan", self.src)
        names = ["b dlx mattress", "c dlx mattress", "d saatva classic mattress"]
        _, first = run("apply", self.manifest(scan, names))
        alts = ["Our tester kneeling on the Helix Midnight Luxe", "Our product tester on the DLX Mattress",
                "The Saatva Classic, side view"]
        code, result = self.redo(scan, ["b helix midnight luxe mattress", "c dlx mattress", "d saatva classic mattress"],
                                 products=("Helix Midnight Luxe", "DLX Mattress", "Saatva Classic"), alts=alts)
        self.assertEqual(code, 0, result)
        self.assertEqual(alt_file(self.tmp, "dlx"), ["c-dlx-mattress.webp: Our product tester on the DLX Mattress"])
        self.assertEqual(alt_file(self.tmp, "helix-midnight-luxe"),
                         ["b-helix-midnight-luxe-mattress.webp: Our tester kneeling on the Helix Midnight Luxe"])
        self.assertEqual(alt_file(self.tmp, "saatva-classic"),
                         ["d-saatva-classic-mattress.webp: The Saatva Classic, side view"])
        txt = sorted(f for f in os.listdir(self.tmp) if f.endswith(".txt"))
        self.assertEqual(txt, ["dlx-alt-text-descriptions.txt", "helix-midnight-luxe-alt-text-descriptions.txt",
                               "saatva-classic-alt-text-descriptions.txt"])

    def test_redo_removes_alt_file_of_a_product_that_left(self):
        _, scan = run("scan", self.src)
        names = ["b dlx mattress", "c dlx mattress", "d saatva classic mattress"]
        run("apply", self.manifest(scan, names))
        code, result = self.redo(scan, ["b dlx mattress", "c dlx mattress", "d dlx mattress"],
                                 products=("DLX Mattress",) * 3)
        self.assertEqual(code, 0, result)
        self.assertEqual(sorted(f for f in os.listdir(self.tmp) if f.endswith(".txt")),
                         ["dlx-alt-text-descriptions.txt"])
        self.assertEqual(len(alt_file(self.tmp, "dlx")), 3)

    def test_scan_zip(self):
        import shutil
        zip_path = shutil.make_archive(os.path.join(self.tmp, "Batch"), "zip", self.src)
        code, scan = run("scan", zip_path)
        self.assertEqual(code, 0)
        self.assertEqual(len(scan["images"]), 3)
        self.assertEqual(scan["output_parent"], self.tmp)


if __name__ == "__main__":
    unittest.main()
