---
name: paper-review-comments
description: Generate concise reviewer-style comments from local academic paper PDFs, especially engineering and power electronics manuscripts. Use when the user asks in English or Chinese to review a paper, such as “审一下这篇文章”, “帮我审稿”, “看看这篇论文该接收还是拒稿”, “生成审稿意见”, “写五个大问题和若干小问题”, “做一个审稿HTML”, or asks to judge accept/reject/major/minor revision, draft reviewer comments, create an HTML review page in the established bilingual format, attach figure/table/equation evidence under each issue, or produce an English-only copy-ready draft for a review submission system.
---

# Paper Review Comments

## Purpose

Use this skill to turn a local manuscript PDF into reviewer-style comments and a browser-friendly HTML review page. The output should follow the current review-page pattern: bilingual analysis sections, major/minor issue cards, evidence crops under each relevant issue, and an English-only Copy-Ready Draft for direct submission.

Do not require an existing review DOCX. If a DOCX is present, treat it only as optional style context when the user explicitly asks.

## Workflow

1. Inspect the local context.
   - Identify the manuscript PDF and output folder.
   - If several PDFs are present, choose the user-mentioned file first; otherwise ask only when the choice is genuinely ambiguous.
   - Read enough of the paper to understand the objective, technical method, claimed contributions, closest comparisons, assumptions, experiments, and conclusion.

2. Form the reviewer judgment.
   - State what the paper does and what it claims.
   - Recommend one of: reject, major revision, minor revision, or accept.
   - For normal first-round engineering-paper reviews, default to a small number of high-impact comments rather than a long research-note summary.

3. Draft the comments.
   - Use 5 major issues by default unless the user asks otherwise.
   - Add about 6-12 minor issues.
   - Keep comments concise, specific, and actionable.
   - Write like a domain reviewer. Avoid generic AI/ML review jargon unless it is native to the manuscript.
   - Read `references/reviewer-style.md` before finalizing wording.
   - For power electronics, WPT, converters, motor drives, charging, or control papers, also read `references/power-electronics-review-checks.md`.

4. Build the HTML review page.
   - Use `assets/review-html-template.html` as the visual and structural template.
   - Create a sibling asset folder named after the output file, for example `PaperID-review-assets/`.
   - Include:
     - title/header metadata
     - recommendation
     - brief paper summary and contribution assessment
     - Major Comments / 大问题
     - Minor Comments / 小问题
     - Supporting material / 对应材料 below each issue when applicable
     - Copy-Ready Draft in English only
   - Analysis and issue cards may be bilingual when useful, but the Copy-Ready Draft must be English only.

5. Attach supporting material.
   - For each issue that cites a figure, table, or equation, add the corresponding crop below that issue.
   - Figures and tables should include only the figure/table itself and its title/caption.
   - Equation crops should include only the equation and the directly corresponding introductory or explanatory lines.
   - Do not include neighboring figures, neighboring section headings, unrelated paragraphs, page headers, or page footers.
   - Render PDF pages to PNG with a stable temporary folder such as `tmp/pdfs/`, then crop into the final asset folder.
   - Use a contact sheet for visual QA when there are multiple crops:
     `python scripts/make_contact_sheet.py path/to/review.html --output path/to/contact-sheet.png`
   - Delete temporary PDF page renders and QA contact sheets after final verification.

6. Validate before delivering.
   - Run:
     `python scripts/validate_review_html.py path/to/review.html`
   - Fix any missing image refs, unreferenced assets, copy-ready Chinese text, raw HTML tags in the copy-ready block, or unrendered formula markers.
   - Manually inspect the important crops. The script cannot judge semantic crop quality.
   - Final answer should link the HTML file and summarize checks performed.

## Output Rules

- Default chat language is Chinese unless the user requests English.
- The Copy-Ready Draft section must be English only and directly copyable into a review system.
- Use plain text formula notation in the Copy-Ready Draft, for example `Gvi = 1/(omega Lf1)`, not HTML tags or LaTeX markup.
- Keep the workspace clean: remove temporary render folders and unused image assets.
- If a Word document is open and locked, ask the user to close it instead of writing a duplicate.
