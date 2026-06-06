---
name: paper-review-comments
description: Generate reviewer-style comments from local academic PDFs as token-efficient review-data JSON plus HTML evidence pages. Use for English/Chinese requests such as “审一下这篇文章”, “帮我审稿”, accept/reject/major/minor judgment, major/minor comments, 审稿HTML, 给编辑的话/comments to editor, editing existing review comments, evidence with page/figure/table/equation locators, or English-only copy-ready drafts.
---

# Paper Review Comments

## Purpose

Use this skill to turn a local manuscript PDF into reviewer-style comments and a browser-friendly HTML review page. Prefer a token-efficient source file named `PaperID-review-data.json`, then render HTML from that data. The output should follow the current review-page pattern: bilingual analysis sections, an optional Comments to Editor section, major/minor issue cards, evidence under each relevant issue, and an English-only Copy-Ready Draft for direct submission.

Do not require an existing review DOCX. If a DOCX is present, treat it only as optional style context when the user explicitly asks.

## Token-Saving Rules

- Treat `*-review-data.json` as the source of truth when it exists. Edit JSON first, then render HTML.
- For follow-up edits to an existing review, do not reread the PDF, references, or whole HTML unless the requested change needs them. Use `rg` to locate only the relevant JSON or HTML fields.
- Keep the Copy-Ready Draft generated from the English comments when possible. If hand-written, update it from the same JSON change.
- Delay expensive figure/table/equation cropping until the major/minor issue list is stable or the user explicitly asks for final HTML evidence.
- Do not paste large PDF text into chat. Record short evidence locators in JSON instead.

## Workflow

1. Inspect the local context.
   - Identify the manuscript PDF and output folder.
   - If several PDFs are present, choose the user-mentioned file first; otherwise ask only when the choice is genuinely ambiguous.
   - Read enough of the paper to understand the objective, technical method, claimed contributions, closest comparisons, assumptions, experiments, and conclusion.

2. Form the reviewer judgment.
   - State what the paper does and what it claims.
   - Recommend one of: reject, major revision, minor revision, or accept.
   - For normal first-round engineering-paper reviews, default to a small number of high-impact comments rather than a long research-note summary.

3. Draft the comments in `review-data.json`.
   - Use 5 major issues by default unless the user asks otherwise.
   - Add about 4-8 minor issues unless the user asks otherwise.
   - Keep comments concise, specific, and actionable.
   - Write like a domain reviewer. Avoid generic AI/ML review jargon unless it is native to the manuscript.
   - Read `references/reviewer-style.md` before finalizing wording.
   - For power electronics, WPT, converters, motor drives, charging, or control papers, also read `references/power-electronics-review-checks.md`.
   - Start from `assets/review-data-template.json` when creating a new review-data file.
   - Store paper metadata, recommendation, optional `comments_to_editor`, bilingual summary, major comments, minor comments, and evidence entries in JSON.
   - When `comments_to_editor` is requested or useful, write one concise bilingual paragraph that states what the paper does, its main contribution/innovation, and why the review decision is recommended. Keep this separate from the author-facing Copy-Ready Draft.

4. Build or update the HTML review page.
   - Prefer rendering from JSON:
     `python scripts/render_review_html.py path/to/review-data.json --output path/to/review.html`
   - If an older review has only HTML and the user requests a small wording edit, use targeted HTML edits instead of reverse-engineering JSON.
   - Use `assets/review-html-template.html` only as visual style reference when manual HTML editing is unavoidable.
   - Create a sibling asset folder named after the output file, for example `PaperID-review-assets/`.
   - Include:
     - title/header metadata
     - recommendation
     - Comments to Editor / 给编辑的话 when `comments_to_editor` is present
     - brief paper summary and contribution assessment
     - Major Comments / 大问题
     - Minor Comments / 小问题
     - Supporting material / 对应材料 below each issue when applicable
     - Copy-Ready Draft in English only
   - Analysis and issue cards may be bilingual when useful, but the Copy-Ready Draft must be English only.

5. Attach or plan supporting material.
   - For each issue that cites a figure, table, equation, or source passage, first add a compact evidence list entry in JSON.
   - Each evidence entry should include:
     - `page`: PDF page number.
     - `kind`: `figure`, `table`, `equation`, or `text`.
     - `label`: source label such as `Fig. 7`, `Table II`, or `Equation (19)`.
     - `locator_text`: the short caption, equation lead-in, nearby wording, or exact phrase used to locate the source.
     - `crop_file`: final crop path when an image crop exists; leave empty until cropped.
     - `caption`: one short sentence explaining why the evidence supports the comment.
   - Figures and tables should include only the figure/table itself and its title/caption.
   - Equation crops should include only the equation and the directly corresponding introductory or explanatory lines.
   - Do not include neighboring figures, neighboring section headings, unrelated paragraphs, page headers, or page footers.
   - Render PDF pages to PNG with a stable temporary folder such as `tmp/pdfs/`, then crop into the final asset folder.
   - Use a contact sheet for visual QA when there are multiple crops:
     `python scripts/make_contact_sheet.py path/to/review.html --output path/to/contact-sheet.png`
   - Delete temporary PDF page renders and QA contact sheets after final verification.

6. Validate before delivering.
   - If using JSON, render HTML first:
     `python scripts/render_review_html.py path/to/review-data.json --output path/to/review.html`
   - Run:
     `python scripts/validate_review_html.py path/to/review.html`
   - Fix any missing image refs, unreferenced assets, copy-ready Chinese text, raw HTML tags in the copy-ready block, or unrendered formula markers.
   - Manually inspect the important crops. The script cannot judge semantic crop quality.

7. Open the HTML preview for the user.
   - Do not ask the user to run a CMD, PowerShell script, or manual file opener.
   - Do not rely on direct `file://` navigation in the Codex in-app browser; local-file URLs may be blocked by browser security policy.
   - Start or reuse a local static server bound to `127.0.0.1` in the HTML output directory.
   - Prefer port `8766`; if it is unavailable, choose the next free local port.
   - Open the Codex in-app browser to `http://127.0.0.1:<port>/<html-file-name>`.
   - Keep the server local-only and do not expose review artifacts externally.
   - Final answer should link both the local HTML file path and the browser URL, then summarize checks performed.

## Output Rules

- Default chat language is Chinese unless the user requests English.
- The Copy-Ready Draft section must be English only and directly copyable into a review system.
- Use plain text formula notation in the Copy-Ready Draft, for example `Gvi = 1/(omega Lf1)`, not HTML tags or LaTeX markup.
- Keep the workspace clean: remove temporary render folders and unused image assets.
- If a Word document is open and locked, ask the user to close it instead of writing a duplicate.
