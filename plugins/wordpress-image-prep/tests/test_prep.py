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

    def manifest(self, scan, names, products=("DLX Mattress", "DLX Mattress", "Saatva Classic"), **extra):
        data = {"output_parent": scan["output_parent"], "images": [
            {"source": p, "name": n, "product": pr, "focus_y": 0.5}
            for p, n, pr in zip((self.a, self.b, self.c), names, products)]}
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
        self.assertEqual([r["product"] for r in result["results"]], ["DLX Mattress", "DLX Mattress", "Saatva Classic"])
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

    def test_scan_zip(self):
        import shutil
        zip_path = shutil.make_archive(os.path.join(self.tmp, "Batch"), "zip", self.src)
        code, scan = run("scan", zip_path)
        self.assertEqual(code, 0)
        self.assertEqual(len(scan["images"]), 3)
        self.assertEqual(scan["output_parent"], self.tmp)


if __name__ == "__main__":
    unittest.main()
