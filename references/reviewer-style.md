# Reviewer Style

## Default Voice

- Lead with the technical concern, then state what the authors should add, clarify, or revise.
- Prefer compact, review-system-ready wording.
- Avoid long paper-summary paragraphs inside the issue list.
- Avoid exaggerated language. Use "not sufficiently demonstrated", "not clearly isolated", "requires clarification", "the evidence is too narrow", or "the claim should be narrowed".
- Do not invent citations or facts. If a comparison requires literature support, ask the authors for a focused comparison rather than fabricating references.

## Major Comment Pattern

Use this shape:

1. Problem sentence: identify the specific weakness.
2. Evidence sentence: point to the relevant claim, table, figure, model, or experiment.
3. Required action: tell the authors what to add or change.

Example:

`The application claim is broader than the verified operating conditions. The method is demonstrated only under fixed or calibrated coupling, while the motivation includes scenarios where distance variation and misalignment are common. Please either narrow the claim to fixed-coupling receiver-constrained chargers, or add experiments under varied distance, lateral offset, and coupling coefficient, reporting regulation error, efficiency, and transition behavior.`

## Minor Comment Pattern

Use one or two sentences per item. Minor comments should cover clarity, terminology, table headings, missing implementation details, symbol consistency, and reporting definitions.

## Recommendation Tone

- `Reject`: use when the core technical claim is unsupported, novelty is insufficient, or experiments cannot support the conclusions.
- `Major revision`: use when the idea may be publishable but key evidence, comparisons, assumptions, or experiments are missing.
- `Minor revision`: use when the technical story is mostly complete and only presentation or limited clarification is needed.
- `Accept`: use rarely, only when no material technical issues remain.
