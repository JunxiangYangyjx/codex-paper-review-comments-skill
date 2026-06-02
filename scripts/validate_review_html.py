#!/usr/bin/env python3
"""Validate a paper review HTML page produced by the paper-review-comments skill."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


IMG_RE = re.compile(r'<img\s+[^>]*src="([^"]+)"', re.IGNORECASE)
COPY_RE = re.compile(r"<h2>\s*Copy-Ready Draft\s*</h2>\s*<div[^>]*class=\"copy-block\"[^>]*>(.*?)</div>", re.IGNORECASE | re.DOTALL)
CJK_RE = re.compile(r"[\u3400-\u9fff]")
RAW_SUBSCRIPT_RE = re.compile(r"[A-Za-z]_\{")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Path to the review HTML file")
    parser.add_argument("--allow-dollar", action="store_true", help="Allow dollar signs in the HTML")
    args = parser.parse_args()

    html_path = args.html.resolve()
    if not html_path.exists():
        print(f"ERROR: HTML file not found: {html_path}")
        return 2

    content = html_path.read_text(encoding="utf-8")
    base = html_path.parent

    refs = IMG_RE.findall(content)
    unique_refs = sorted(set(refs))
    missing = [ref for ref in unique_refs if not (base / ref).exists()]

    copy_match = COPY_RE.search(content)
    copy_block = copy_match.group(1) if copy_match else ""
    copy_cjk = len(CJK_RE.findall(copy_block))
    copy_span = copy_block.lower().count("<span")
    copy_img = copy_block.lower().count("<img")

    major_count = len(re.findall(r">\s*Major\s+\d+\s*<", content))
    minor_count = len(re.findall(r">\s*Minor\s+\d+\s*<", content))
    material_blocks = content.count('class="materials"')
    dollar_count = content.count("$")
    raw_subscripts = len(RAW_SUBSCRIPT_RE.findall(content))

    asset_dirs = sorted({(base / ref).parent for ref in unique_refs})
    unreferenced_assets: list[Path] = []
    ref_paths = {(base / ref).resolve() for ref in unique_refs}
    for asset_dir in asset_dirs:
        if asset_dir.exists() and asset_dir.is_dir():
            for path in asset_dir.iterdir():
                if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
                    if path.resolve() not in ref_paths:
                        unreferenced_assets.append(path)

    checks = {
        "copy_block_found": bool(copy_match),
        "copy_block_cjk_chars": copy_cjk,
        "copy_block_span_tags": copy_span,
        "copy_block_img_tags": copy_img,
        "major_comments": major_count,
        "minor_comments": minor_count,
        "material_blocks": material_blocks,
        "image_refs": len(refs),
        "unique_image_refs": len(unique_refs),
        "missing_refs": len(missing),
        "unreferenced_assets": len(unreferenced_assets),
        "dollar_chars": dollar_count,
        "raw_subscript_patterns": raw_subscripts,
    }

    for key, value in checks.items():
        print(f"{key}: {value}")

    if missing:
        print("\nMissing image refs:")
        for ref in missing:
            print(f"- {ref}")

    if unreferenced_assets:
        print("\nUnreferenced image assets:")
        for path in unreferenced_assets:
            print(f"- {path}")

    errors = []
    if not copy_match:
        errors.append("Copy-Ready Draft block was not found.")
    if copy_cjk:
        errors.append("Copy-Ready Draft contains CJK characters.")
    if copy_span or copy_img:
        errors.append("Copy-Ready Draft contains HTML tags that should not be copied to review systems.")
    if missing:
        errors.append("One or more image references are missing.")
    if raw_subscripts:
        errors.append("Raw LaTeX-style subscript patterns were found.")
    if dollar_count and not args.allow_dollar:
        errors.append("Dollar signs were found; verify formulas are rendered or intentionally plain text.")

    if errors:
        print("\nFAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
