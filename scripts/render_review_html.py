#!/usr/bin/env python3
"""Render a review-data JSON file to an HTML review page."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import quote


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


def understanding_section(data: dict[str, Any]) -> str:
    """Render authored understanding content without adding it to submission text."""
    module = data.get("paper_understanding") or {}
    sections = module.get("sections") or []
    if not sections:
        return ""
    seen: set[str] = set()
    cards, toc = [], []
    source_pdf = str(data.get("source_pdf", ""))
    for idx, section in enumerate(sections, start=1):
        key = str(section.get("key", ""))
        if not re.fullmatch(r"[a-z][a-z0-9-]*", key) or key in seen:
            raise ValueError(f"Understanding section needs a unique slug key: {key!r}")
        seen.add(key)
        title = esc(section.get("title", key))
        toc.append(f'<a href="#qa-{key}">{idx} {title}</a>')
        body = str(section["answer_html"]) if "answer_html" in section else para(str(section.get("answer", "")))
        main_figures, detail_figures = [], []
        for figure in section.get("illustrations", []):
            src = str(figure.get("src", ""))
            placement = figure.get("placement", "main")
            if not src or placement not in {"main", "detail"}:
                raise ValueError("Illustrations need src and placement main/detail")
            label = str(figure.get("label", ""))
            source = " · ".join(str(x) for x in [label, f"PDF p. {figure['page']}" if figure.get("page") else ""] if x)
            markup = f'''<div class="qa-visual">
              <h4>{esc(figure.get("title", label))}</h4>
              <figure class="qa-figure qa-figure-featured">
                <a href="{esc(src)}" target="_blank" rel="noreferrer" aria-label="放大查看 {esc(label)}">
                  <img loading="lazy" src="{esc(src)}" alt="{esc(figure.get('alt') or figure.get('title') or label)}">
                </a><figcaption>{esc(source)} · 点击图片查看大图</figcaption>
              </figure>
              <p class="qa-reading-tip"><strong>看图要点：</strong>{para(str(figure.get('tip', '')))}</p>
            </div>'''
            (main_figures if placement == "main" else detail_figures).append(markup)
        # Put the teaching figure near the explanation, rather than below a long card.
        lead, separator, rest = body.partition("</p>")
        body = lead + separator + "".join(main_figures) + rest if separator else "".join(main_figures) + body
        if detail_figures:
            body += '<details class="qa-detail"><summary>展开辅助图示</summary>' + "".join(detail_figures) + '</details>'
        sources = []
        for source in section.get("sources", []):
            page = source.get("page")
            label = " · ".join(str(x) for x in [f"PDF p. {page}" if page else "", source.get("label", "")] if x)
            if source_pdf:
                url = quote(source_pdf, safe="/:@") + (f"#page={quote(str(page), safe='')}" if page else "")
                sources.append(f'<a href="{esc(url)}" target="_blank" rel="noreferrer">{esc(label)}</a>')
            else:
                sources.append(esc(label))
        trail = '<p class="qa-sources">原文定位：' + " · ".join(sources) + '</p>' if sources else ""
        cards.append(f'''<article class="qa-card" id="qa-{key}">
          <div class="qa-card-heading"><span class="qa-index">{idx:02}</span><div>
            <h3>{title}</h3><p class="qa-question">{esc(section.get('question', ''))}</p>
          </div></div><div class="qa-answer">{body}</div>{trail}</article>''')
    overview = f'<div class="qa-overview"><strong>本稿要点</strong><p>{para(str(module["overview"]))}</p></div>' if module.get("overview") else ""
    updated = f'<span class="qa-updated">更新于 {esc(module["updated_at"])}</span>' if module.get("updated_at") else ""
    return f'''<nav class="report-nav" aria-label="报告导航">
      <a href="#paper-understanding">论文理解</a><a href="#review-judgment">审稿判断</a>
      <a href="#major-comments">主要意见</a><a href="#minor-comments">次要意见</a><a href="#copy-ready">英文提交稿</a></nav>
      <section class="understanding" id="paper-understanding" aria-labelledby="understanding-title">
        <div class="qa-section-heading"><div><h2 id="understanding-title">{esc(module.get('title', '论文理解与证据梳理'))}</h2>
          <p>{esc(module.get('subtitle', '围绕通用问题理解论文，再判断贡献与证据是否匹配。'))}</p></div>{updated}</div>
        {overview}<nav class="qa-toc" aria-label="论文理解目录">{''.join(toc)}</nav>{''.join(cards)}</section>'''


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
    understanding = understanding_section(data)
    understanding_css = (Path(__file__).resolve().parent.parent / "assets" / "review-understanding.css").read_text(encoding="utf-8") if understanding else ""

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
    {understanding_css}
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
    {understanding}

    <section class="summary" id="review-judgment">
      <h2>Review Judgment / 审稿判断</h2>
      <p>{field_html(rec, "basis_zh")}</p>
      <p>{field_html(rec, "basis_en")}</p>
    </section>{comments_to_editor_section(data)}

    <section class="summary">
      <h2>Overall Comment / 总体评价</h2>
      <div>{field_html(summary, "en")}</div>
      <div>{field_html(summary, "zh")}</div>
    </section>

    <section>
      <h2 id="major-comments">Major Comments / 大问题</h2>{major_html}
    </section>

    <section>
      <h2 id="minor-comments">Minor Comments / 小问题</h2>{minor_html}
    </section>

    <section id="copy-ready">
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
