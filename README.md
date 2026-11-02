# Paper Review Comments Skill

`paper-review-comments` is a Codex skill for drafting concise academic paper review comments and generating an HTML review page with supporting figure/table/equation evidence. It now prefers a token-efficient `review-data.json` source file and renders the HTML from that structured data.

这个 skill 适合用来做论文审稿辅助，尤其是工程、电力电子、无线电能传输、变换器、控制和实验型论文。它会按照固定流程生成：

- 论文做了什么、主要贡献和审稿建议
- 通用的论文理解问答：研究问题、背景应用、关键理论、仿真、实验、结果、创新与边界
- 正文直接展示关键结构、机理、原型和结果配图，附中文看图要点及原文定位
- 按实际问题生成 major/minor comments，不为凑数量增加要求
- `review-data.json` 结构化源文件，方便后续低 token 修改
- 带对应材料截图的 HTML 审稿页面
- 英文-only 的 `Copy-Ready Draft`，方便直接粘贴到审稿系统

## Install

Clone this repository into your local Codex skills directory. The target folder name should be `paper-review-comments`, matching the skill name in `SKILL.md`.

PowerShell:

```powershell
git clone https://github.com/JunxiangYangyjx/codex-paper-review-comments-skill.git "$env:USERPROFILE\.codex\skills\paper-review-comments"
```

Bash:

```bash
git clone https://github.com/JunxiangYangyjx/codex-paper-review-comments-skill.git ~/.codex/skills/paper-review-comments
```

After installation, start a new Codex thread or refresh the skill environment so the skill can be discovered.

## Usage

You can invoke it explicitly:

```
Use $paper-review-comments 审一下这篇本地论文 PDF，生成审稿意见和带对应材料截图的 HTML 页面。
```

Chinese trigger phrases are also included in the skill description, for example:

- 审一下这篇文章
- 帮我审稿
- 看看这篇论文该接收还是拒稿
- 生成审稿意见
- 写五个大问题和若干小问题
- 做一个审稿HTML

## Expected Output

The generated HTML review page follows this structure:

- illustrated paper understanding with reusable questions, source locators, and reading tips
- review recommendation
- comments to editor / 给编辑的话, when needed
- paper summary
- major comments / 大问题
- minor comments / 小问题
- supporting material / 对应材料 under each relevant issue
- English-only `Copy-Ready Draft`

For each issue that cites a figure, table, or equation, the skill asks Codex to crop and embed the corresponding material below the issue. Crops should include only the relevant figure/table/equation and its directly corresponding caption or explanatory lines.

For token efficiency, the preferred source artifact is `PaperID-review-data.json`. Evidence entries should identify where the source comes from before cropping:

Use the optional `comments_to_editor` field for an editor-only summary of what the paper does, its main contribution or innovation, and why the review decision is recommended. Keep this separate from the author-facing `Copy-Ready Draft`.

- `page`: PDF page number
- `kind`: figure, table, equation, or text
- `label`: for example `Fig. 7`, `Table II`, or `Equation (19)`
- `locator_text`: short caption, equation lead-in, nearby wording, or exact phrase used to locate the source
- `crop_file`: image path when a crop exists
- `caption`: short explanation for the review page

Render HTML from JSON:

```powershell
python scripts/render_review_html.py path\to\review-data.json --output path\to\review.html
```

For small follow-up edits, Codex should update the JSON and re-render the HTML instead of rereading the PDF or editing the full HTML by hand.

The optional `paper_understanding` module is rendered from the same JSON. Add `illustrations` to each section instead of embedding repeated figure markup. Main illustrations appear near the explanation; auxiliary figures can be expanded. See [the schema and question guide](references/paper-understanding.md). Older JSON without this module remains supported. Understanding content and editor comments are excluded from the English submission draft.

## Opening Generated HTML

Open the saved HTML with the system-default browser/application, for example `Start-Process -FilePath <absolute-html-path>` on Windows. Users should not need to run a launcher. A server bound to `127.0.0.1` is only a fallback when local-file behavior prevents previewing; open that URL in the system browser as well.

## Dependencies

The skill itself is plain text plus helper scripts. Depending on the task, Codex may use:

- Python 3
- Pillow, for the contact-sheet helper script
- Poppler / `pdftoppm`, for rendering PDF pages before cropping figures and equations

The validation script can be run manually:

```powershell
python scripts/validate_review_html.py path\to\review.html
```

The contact-sheet helper can be run manually:

```powershell
python scripts/make_contact_sheet.py path\to\review.html --output contact-sheet.png
```

Run the renderer regression checks with:

```powershell
python scripts/test_render_review_html.py
```

## Confidentiality

Do not upload confidential manuscripts, reviewer comments, generated review HTML files, or cropped manuscript figures to a public repository. This repository should contain only the reusable skill files.

## License

MIT License. See [LICENSE](LICENSE).
