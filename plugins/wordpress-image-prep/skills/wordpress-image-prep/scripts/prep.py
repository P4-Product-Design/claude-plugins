#!/usr/bin/env python3
"""WordPress image prep.

  prep.py scan <folder-or-zip>          list the batch, group it by shoot, draw contact sheets
  prep.py apply [--preview] <manifest>  write the WebP files the manifest describes

Both print JSON on stdout. See SKILL.md for the manifest format.
"""
import argparse
import importlib
import json
import os
import site
import subprocess
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _pip_install(package):
    base = [sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check"]
    for extra in ([], ["--user"], ["--user", "--break-system-packages"]):
        if subprocess.run(base + extra + [package], capture_output=True).returncode == 0:
            return True
    return False


def ensure_deps():
    """Install Pillow and pillow-heif for this Python if they're missing. Returns notes for the report."""
    notes = []
    for module, package in (("PIL", "pillow"), ("pillow_heif", "pillow-heif")):
        try:
            importlib.import_module(module)
            continue
        except ImportError:
            pass
        if _pip_install(package):
            site.addsitedir(site.getusersitepackages())
            importlib.invalidate_caches()
            try:
                importlib.import_module(module)
                notes.append(f"installed {package}")
                continue
            except ImportError:
                pass
        notes.append(f"couldn't install {package}")
    return notes


def emit(data, code=0):
    print(json.dumps(data, indent=2, default=str))
    return code


def cmd_scan(args, notes):
    import imaging
    import inventory
    import sheets

    src = os.path.abspath(args.source)
    work = tempfile.mkdtemp(prefix="wordpress-image-prep-")
    root = inventory.unpack(src, work)
    paths, skipped = inventory.list_files(root)
    images, thumbs = [], {}
    for path in paths:
        try:
            thumb = imaging.thumbnail(path, sheets.THUMB_W)
        except Exception as err:  # unreadable file or no HEIC decoder: skip it and keep going
            skipped.append({"path": path, "reason": f"can't be opened ({err})"})
            continue
        try:
            meta = inventory.read_meta(path)
        except Exception:  # HEIC opened through sips has no readable EXIF here; it lands in the undated group
            meta = {"width": None, "height": None, "orientation": 1, "taken": None, "camera": None}
        item = dict(index=len(images) + 1, path=path, filename_hint=inventory.filename_hint(path),
                    subfolder_hint=inventory.subfolder_hint(path, root), **meta)
        images.append(item)
        thumbs[item["index"]] = thumb
    groups = inventory.group_shoots(images)
    ordered = [(f"{i}  (group {g['id']})", thumbs[i]) for g in groups for i in g["indexes"]]
    sheet_paths = sheets.make_sheets(ordered, work, "scan", crop_guide=True)
    return emit({"input": src, "work_dir": work, "output_parent": inventory.output_parent_for(src),
                 "heic_decoder": imaging.HEIC_DECODER, "notes": notes, "images": images,
                 "groups": groups, "skipped": skipped, "sheets": sheet_paths})


def _check(entries):
    import inventory
    import naming

    problems, names = [], []
    for e in entries:
        src = e.get("source", "")
        try:
            names.append(naming.normalize_name(e.get("name", "")))
        except ValueError as err:
            problems.append({"source": src, "problem": str(err)})
        focus = e.get("focus_y", 0.5)
        if isinstance(focus, bool) or not isinstance(focus, (int, float)) or not 0 <= focus <= 1:
            problems.append({"source": src, "problem": f"focus_y must be between 0 and 1, got {focus!r}"})
        if e.get("rotate", 0) not in (0, 90, 180, 270):
            problems.append({"source": src, "problem": f"rotate must be 0, 90, 180 or 270, got {e.get('rotate')!r}"})
        if not inventory.clean_product(e.get("product", "")):
            problems.append({"source": src, "problem": "every photo needs a product"})
        if not os.path.isfile(src):
            problems.append({"source": src, "problem": "file not found"})
    return problems, names


def cmd_apply(args, notes):
    import imaging
    import inventory
    import naming
    import sheets
    from PIL import Image

    with open(args.manifest) as f:
        manifest = json.load(f)
    entries = manifest.get("images", [])
    problems, names = _check(entries)
    if not args.preview and not os.path.isdir(manifest.get("output_parent", "")):
        problems.append({"problem": f"output_parent {manifest.get('output_parent')!r} isn't a folder"})
    if problems or not entries:
        return emit({"ok": False, "problems": problems or [{"problem": "the manifest lists no images"}]}, 1)
    names = naming.assign_unique(names)
    if args.preview:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(args.manifest)), "preview")
        if os.path.isdir(out_dir):
            for old in os.listdir(out_dir):
                os.remove(os.path.join(out_dir, old))
    else:
        out_dir = inventory.free_dir(os.path.join(
            manifest["output_parent"], inventory.folder_name([e["product"] for e in entries], date.today())))
    os.makedirs(out_dir, exist_ok=True)
    results, before, after = [], 0, 0
    for e, name in zip(entries, names):
        dest = os.path.join(out_dir, name + ".webp")
        try:
            info = imaging.process_image(e["source"], dest, e.get("focus_y", 0.5), e.get("rotate", 0))
        except Exception as err:
            results.append({"source": e["source"], "product": e["product"], "error": str(err)})
            continue
        before += os.path.getsize(e["source"])
        after += os.path.getsize(dest)
        results.append(dict(source=e["source"], product=e["product"], output=dest, **info))
    done = [r for r in results if "output" in r]
    if not done:
        os.rmdir(out_dir)
    thumbs = []
    for r in done:
        with Image.open(r["output"]) as im:
            small = im.convert("RGB")
            small.thumbnail((sheets.THUMB_W, sheets.THUMB_W))
            thumbs.append((os.path.basename(r["output"]), small))
    check_dir = tempfile.mkdtemp(prefix="wordpress-image-prep-check-")
    return emit({"ok": bool(done), "output_dir": out_dir if done else None, "preview": args.preview,
                 "notes": notes, "results": results, "bytes_before": before, "bytes_after": after,
                 "check_sheets": sheets.make_sheets(thumbs, check_dir, "check") if thumbs else []})


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan")
    scan.add_argument("source")
    apply_ = sub.add_parser("apply")
    apply_.add_argument("--preview", action="store_true")
    apply_.add_argument("manifest")
    args = parser.parse_args()
    notes = ensure_deps()
    try:
        importlib.import_module("PIL")
    except ImportError:
        return emit({"ok": False, "problems": [{"problem": "Pillow isn't installed and couldn't be installed"}]}, 2)
    try:
        return cmd_scan(args, notes) if args.command == "scan" else cmd_apply(args, notes)
    except (ValueError, OSError) as err:
        return emit({"ok": False, "problems": [{"problem": str(err)}]}, 2)


if __name__ == "__main__":
    sys.exit(main())
