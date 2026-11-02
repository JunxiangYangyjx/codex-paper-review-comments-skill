# Paper Understanding and Explanatory Figures

Add this module before the formal review judgment. Its purpose is to help a reader understand the manuscript before judging it. Keep questions general enough to reuse across papers; make answers concrete and traceable to this manuscript. It is reviewer reading support, not part of the submission draft.

## Seven Reusable Questions

| Key | Topic | Question |
| --- | --- | --- |
| `work` | Research problem and main work | What problem is studied, what is proposed, and what is compared? |
| `background` | Background and application | Why does the problem matter, what limits existing approaches, and which application is actually evaluated? |
| `theory` | Method and key theory | Why should the method work, which equations or mechanisms matter, and under which assumptions? |
| `simulation` | Simulation and numerical validation | What does each calculation or simulation test, using which model, conditions, and baseline? |
| `experiment` | Experimental design and scope | What prototype or study was run, what was measured, and are comparisons compatible? |
| `results` | Results and evidence | What quantitative results were obtained, which were predicted or measured, and under what conditions? |
| `novelty` | Innovation and boundaries | What is new relative to established work, what kind of contribution is it, and how far does the evidence support it? |

Adapt these topics to nonexperimental or nonengineering papers. Explicitly state that no hardware experiment or simulation is presented when appropriate. Do not require authors to add an inapplicable evidence category merely to fill the module.

## Explain Before Critiquing

- Begin with a short main-point paragraph, then explain the problem, mechanism, and evidence. Avoid copying long abstract passages.
- Distinguish application motivation from demonstrated applications, analytical parameter sweeps from independently solved simulations, and predicted quantities from measurements.
- In a result table, include conditions or an evidence-type column. Preserve absolute output power, load, frequency, and efficiency boundaries when needed to interpret comparisons; do not compare different normalizations as if they were the same operating point.
- Distinguish a new principle from a new use, comparison, optimization, or integration of an existing principle. State literature-access limitations instead of inferring duplication from an unavailable source.
- Keep full reviewer requests in the major/minor comments. The introduction should explain the work without becoming a second issue list.

## Figures That Teach

Prefer original source crops in this order when applicable:

1. Architecture/topology or the compared physical structures.
2. Operating principle, current paths, equivalent models, or modes.
3. A simulation/field/result figure that reveals the mechanism.
4. Prototype and test setup.
5. The most informative measured waveform or performance curve.

Place key figures directly next to their explanation using `placement: "main"`. Use `detail` for auxiliary circuits, parameter tables, or raw readings. Choose the number according to explanatory value; do not fill a quota or display every figure. A figure can also support a review comment by reusing its existing asset.

Each figure needs a reading tip: identify the panels, axes or paths to look at; explain the actual observation; and distinguish what the figure does and does not establish. Describe shared color scales and different curve normalizations when material. Crop out surrounding text, unrelated figures, headers and footers, while preserving the figure caption. Do not repair author labels silently in a source crop.

## JSON Contract

Use the `paper_understanding` object in `assets/review-data-template.json`:

- Module: `title`, optional `subtitle`, `overview`, `updated_at`, and `sections`.
- Section: unique lowercase slug `key`, `title`, general `question`, `answer` (plain text) or `answer_html` (authored HTML), `sources`, and `illustrations`.
- Source: PDF `page` and `label` (figure/table/equation/section locator).
- Illustration: relative `src`, `title`, `tip`, PDF `page`, original `label`, and `placement` (`main` or `detail`); optional `alt`.
- Top-level optional `source_pdf`: local PDF path relative to the output HTML, used to make page links. Without it, source locators remain readable text.

`answer_html` may contain tables, MathML, and expandable details. Use the CSS classes in `assets/review-understanding.css` (`qa-table-wrap`, `qa-table`, `qa-equation`, `qa-detail`, `qa-callout`). The renderer inserts main figures after the first paragraph and auxiliary figures in expandable details. Keep figure definitions in `illustrations`, rather than duplicating the rendered figure markup in the answer.

This is trusted authored HTML; do not copy arbitrary executable HTML from a source document. The renderer does not compile LaTeX or sanitize an uploaded HTML document. Preserve LaTeX sources separately when useful, but render important equations with MathML or local equation images so the report works offline.

Legacy JSON without `paper_understanding` continues to render. Re-rendering must preserve comments and the English-only copy-ready draft, and must not leak understanding text or editor comments into that draft.
