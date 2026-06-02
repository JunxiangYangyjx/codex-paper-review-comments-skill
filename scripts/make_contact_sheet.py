#!/usr/bin/env python3
"""Create a visual QA contact sheet for image refs in a review HTML page."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw


IMG_RE = re.compile(r'<img\s+[^>]*src="([^"]+)"', re.IGNORECASE)


def collect_refs(html_path: Path) -> list[Path]:
    content = html_path.read_text(encoding="utf-8")
    refs: list[Path] = []
    seen: set[Path] = set()
    for ref in IMG_RE.findall(content):
        path = (html_path.parent / ref).resolve()
        if path not in seen:
            seen.add(path)
            refs.append(path)
    return refs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Path to the review HTML file")
    parser.add_argument("--output", type=Path, required=True, help="Output PNG contact sheet")
    parser.add_argument("--thumb-width", type=int, default=520, help="Thumbnail width in pixels")
    parser.add_argument("--columns", type=int, default=2, help="Number of columns")
    args = parser.parse_args()

    html_path = args.html.resolve()
    refs = collect_refs(html_path)
    if not refs:
        print("No image refs found.")
        return 1

    pad = 18
    label_h = 34
    cards: list[Image.Image] = []
    for path in refs:
        if not path.exists():
            raise FileNotFoundError(path)
        im = Image.open(path).convert("RGB")
        scale = min(1.0, args.thumb_width / im.width)
        thumb = im.resize((int(im.width * scale), int(im.height * scale)))
        card = Image.new("RGB", (args.thumb_width + pad * 2, label_h + thumb.height + pad), "white")
        draw = ImageDraw.Draw(card)
        draw.text((pad, 8), path.name, fill=(20, 40, 65))
        card.paste(thumb, (pad, label_h))
        draw.rectangle((0, 0, card.width - 1, card.height - 1), outline=(210, 220, 230))
        cards.append(card)

    cols = max(1, args.columns)
    col_w = args.thumb_width + pad * 2
    row_h = max(card.height for card in cards) + 16
    rows = math.ceil(len(cards) / cols)
    sheet = Image.new("RGB", (cols * col_w + (cols - 1) * 16, rows * row_h), (245, 247, 250))
    for i, card in enumerate(cards):
        x = (i % cols) * (col_w + 16)
        y = (i // cols) * row_h
        sheet.paste(card, (x, y))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, optimize=True)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
