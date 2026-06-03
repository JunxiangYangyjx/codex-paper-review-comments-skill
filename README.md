# Paper Review Comments Skill

`paper-review-comments` is a Codex skill for drafting concise academic paper review comments and generating an HTML review page with supporting figure/table/equation evidence.

这个 skill 适合用来做论文审稿辅助，尤其是工程、电力电子、无线电能传输、变换器、控制和实验型论文。它会按照固定流程生成：

- 论文做了什么、主要贡献和审稿建议
- 5 个 major comments 和若干 minor comments
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

- review recommendation
- paper summary
- major comments / 大问题
- minor comments / 小问题
- supporting material / 对应材料 under each relevant issue
- English-only `Copy-Ready Draft`

For each issue that cites a figure, table, or equation, the skill asks Codex to crop and embed the corresponding material below the issue. Crops should include only the relevant figure/table/equation and its directly corresponding caption or explanatory lines.

## Opening Generated HTML

Codex in-app browser may block direct `file://` URLs for local files. When this skill generates an HTML review page, Codex should serve the output folder through a local-only `127.0.0.1` static server and open the corresponding `http://127.0.0.1:<port>/<review-file>.html` URL automatically.

Users should not need to run a separate CMD or PowerShell launcher. The local server is only for previewing generated review artifacts on the same machine.

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

## Confidentiality

Do not upload confidential manuscripts, reviewer comments, generated review HTML files, or cropped manuscript figures to a public repository. This repository should contain only the reusable skill files.

## License

MIT License. See [LICENSE](LICENSE).
