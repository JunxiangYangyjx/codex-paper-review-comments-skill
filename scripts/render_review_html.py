#!/usr/bin/env python3
"""Render a review-data JSON file to an HTML review page."""

from __future__ import annotations

import argparse
import html
import json
from datetime import date
from pathlib import Path
from typing import Any


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def para(value: str) -> str:
    return "<br>".join(esc(value).splitlines())


def field_html(obj: dict[str, Any], name: str) -> str:
    html_key = f"{name}_html"
    if html_key in obj:
        return str(obj[html_key])
    return para(str(obj.get(name, "")))


def load_data(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    for key in ["paper_id", "paper_title", "recommendation", "summary", "major_comments", "minor_comments"]:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")
    return data


def evidence_card(item: dict[str, Any], base: Path) -> str:
    page = item.get("page", "")
    kind = item.get("kind", "evidence")
    label = item.get("label", "")
    locator = item.get("locator_text", "")
    crop_file = item.get("crop_file", "")
    alt = item.get("alt") or label or kind
    caption = item.get("caption", "")

    source_bits = []
    if page != "":
        source_bits.append(f"p. {page}")
    if label:
        source_bits.append(str(label))
    if kind:
        source_bits.append(str(kind))
    source = " | ".join(source_bits)

    img_html = ""
    if crop_file:
        img_path = base / crop_file
        status = "" if img_path.exists() else " missing"
        img_html = f'<img class="{status.strip()}" src="{esc(crop_file)}" alt="{esc(alt)}">'

    locator_html = f'<p class="evidence-source">Locator: {para(locator)}</p>' if locator else ""
    source_html = f'<p class="evidence-source">{esc(source)}</p>' if source else ""
    caption_html = f"<figcaption>{para(caption)}</figcaption>" if caption else ""

    return f"""
            <figure class="material-card">
              {img_html}
              {source_html}
              {locator_html}
              {caption_html}
            </figure>"""


def evidence_block(comment: dict[str, Any], base: Path) -> str:
    evidence = comment.get("evidence") or []
    if not evidence:
        note = comment.get("evidence_note")
        if not note:
            return ""
        return f"""
        <div class="materials">
          <p class="materials-title">Supporting material / 对应材料</p>
          <p class="note">{para(note)}</p>
        </div>"""

    grid_class = "material-grid single" if len(evidence) == 1 else "material-grid"
    cards = "\n".join(evidence_card(item, base) for item in evidence)
    return f"""
        <div class="materials">
          <p class="materials-title">Supporting material / 对应材料</p>
          <div class="{grid_class}">
{cards}
          </div>
        </div>"""


def comment_article(comment: dict[str, Any], idx: int, kind: str, base: Path) -> str:
    tag = "Major" if kind == "major" else "Minor"
    return f"""
      <article class="comment {kind}">
        <h3><span class="tag {kind}">{tag} {idx}</span>{esc(comment.get("title_en", ""))} / {esc(comment.get("title_zh", ""))}</h3>
        <div class="comment-grid">
          <div><h4>English</h4><p>{field_html(comment, "en")}</p></div>
          <div><h4>中文</h4><p>{field_html(comment, "zh")}</p></div>
        </div>{evidence_block(comment, base)}
      </article>"""


def comments_to_editor_section(data: dict[str, Any]) -> str:
    editor = data.get("comments_to_editor") or {}
    en = editor.get("en", "")
    zh = editor.get("zh", "")
    if not en and not zh:
        return ""
    return f"""
    <section>
      <h2>Comments to Editor / 给编辑的话</h2>
      <div class="comment">
        <div class="comment-grid">
          <div><h4>English</h4><p>{field_html(editor, "en")}</p></div>
          <div><h4>中文</h4><p>{field_html(editor, "zh")}</p></div>
        </div>
      </div>
    </section>
"""


def auto_copy_ready(data: dict[str, Any]) -> str:
    lines: list[str] = []
    summary = data.get("summary", {}).get("en", "")
    if summary:
        lines.append(summary)
        lines.append("")

    for i, comment in enumerate(data.get("major_comments", []), start=1):
        lines.append(f"{i}. {comment.get('en', '').strip()}")
        lines.append("")

    minors = data.get("minor_comments", [])
    if minors:
        lines.append("In addition, the following minor issues should be addressed:")
        lines.append("")
        for i, comment in enumerate(minors, start=1):
            lines.append(f"{i}. {comment.get('en', '').strip()}")
    return "\n".join(lines).strip()


def render(data: dict[str, Any], output: Path) -> str:
    base = output.parent
    rec = data.get("recommendation", {})
    summary = data.get("summary", {})
    major_html = "\n".join(
        comment_article(comment, idx, "major", base)
        for idx, comment in enumerate(data.get("major_comments", []), start=1)
    )
    minor_html = "\n".join(
        comment_article(comment, idx, "minor", base)
        for idx, comment in enumerate(data.get("minor_comments", []), start=1)
    )
    copy_ready = data.get("copy_ready") or auto_copy_ready(data)
    today = data.get("date") or date.today().isoformat()

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(data.get("paper_id", ""))} Review Comments</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f9;
      --paper: #ffffff;
      --ink: #1d252c;
      --muted: #5b6672;
      --line: #d9dee5;
      --accent: #156f7a;
      --major: #9d2f2f;
      --minor: #6b5a12;
      --zh-bg: #f8fbfb;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 16px/1.65 "Segoe UI", Arial, "Microsoft YaHei", sans-serif;
    }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 36px 24px 64px; }}
    header {{ border-bottom: 2px solid var(--line); padding-bottom: 18px; margin-bottom: 24px; }}
    h1 {{ margin: 0 0 8px; font-size: 29px; line-height: 1.25; letter-spacing: 0; }}
    h2 {{ margin: 30px 0 14px; font-size: 20px; line-height: 1.35; letter-spacing: 0; }}
    h3 {{ margin: 0 0 8px; font-size: 17px; line-height: 1.4; letter-spacing: 0; }}
    h4 {{ margin: 0 0 8px; color: var(--muted); font-size: 13px; }}
    p {{ margin: 0 0 12px; }}
    .meta {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px 18px; margin-top: 14px; color: var(--muted); font-size: 14px; }}
    .summary, .comment {{ background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 17px 19px; margin: 12px 0; }}
    .summary {{ border-left: 5px solid var(--accent); }}
    .comment.major {{ border-left: 5px solid var(--major); }}
    .comment.minor {{ border-left: 5px solid var(--minor); }}
    .tag {{ display: inline-block; min-width: 58px; margin-right: 8px; color: #fff; border-radius: 4px; padding: 2px 6px; font-size: 12px; text-align: center; vertical-align: 1px; }}
    .tag.major {{ background: var(--major); }}
    .tag.minor {{ background: var(--minor); }}
    .comment-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 10px; }}
    .comment-grid > div {{ border: 1px solid var(--line); border-radius: 7px; padding: 13px 14px; }}
    .comment-grid > div:nth-child(2) {{ background: var(--zh-bg); }}
    .materials {{ margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--line); }}
    .materials-title {{ margin: 0 0 10px; color: var(--muted); font-size: 14px; font-weight: 700; }}
    .material-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }}
    .material-grid.single {{ grid-template-columns: 1fr; }}
    figure.material-card {{ margin: 0; border: 1px solid var(--line); border-radius: 8px; background: #fff; overflow: hidden; }}
    .material-card img {{ display: block; width: 100%; height: auto; background: #fff; }}
    .material-card img.missing {{ min-height: 80px; border: 2px solid #b00020; }}
    .material-card figcaption, .evidence-source {{ border-top: 1px solid var(--line); padding: 8px 10px; color: var(--muted); font-size: 13px; line-height: 1.45; }}
    .evidence-source {{ margin: 0; border-top: 0; font-family: Arial, "Microsoft YaHei", sans-serif; }}
    .copy-block {{ white-space: pre-wrap; background: #fbfcfd; border: 1px dashed var(--line); border-radius: 8px; padding: 16px 18px; margin-top: 20px; font-family: Georgia, "Times New Roman", "Microsoft YaHei", serif; line-height: 1.7; }}
    .note {{ color: var(--muted); font-size: 14px; }}
    @media (max-width: 780px) {{ main {{ padding: 24px 14px 48px; }} .comment-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{esc(data.get("paper_id", ""))} Review Comments | 中英对照</h1>
      <p>Manuscript: {esc(data.get("paper_title", ""))}</p>
      <div class="meta">
        <div>Recommendation: <strong>{esc(rec.get("decision", ""))}</strong></div>
        <div>Focus: {esc(data.get("focus", ""))}</div>
        <div>Date: {esc(today)}</div>
      </div>
    </header>

    <section class="summary">
      <h2>Review Judgment / 审稿判断</h2>
      <p>{field_html(rec, "basis_zh")}</p>
      <p>{field_html(rec, "basis_en")}</p>
    </section>{comments_to_editor_section(data)}

    <section class="summary">
      <h2>Overall Comment / 总体评价</h2>
      <p>{field_html(summary, "en")}</p>
      <p>{field_html(summary, "zh")}</p>
    </section>

    <section>
      <h2>Major Comments / 大问题</h2>{major_html}
    </section>

    <section>
      <h2>Minor Comments / 小问题</h2>{minor_html}
    </section>

    <section>
      <h2>Copy-Ready Draft</h2>
      <div class="copy-block">{esc(copy_ready)}</div>
    </section>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, help="review-data JSON file")
    parser.add_argument("--output", "-o", type=Path, help="output HTML path")
    args = parser.parse_args()

    data_path = args.data.resolve()
    output = (args.output or data_path.with_suffix(".html")).resolve()
    data = load_data(data_path)
    output.write_text(render(data, output), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
