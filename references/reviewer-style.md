# Reviewer Style

## Default Voice

- Lead with the technical concern, then state what the authors should add, clarify, or revise.
- Prefer compact, review-system-ready wording.
- Avoid long paper-summary paragraphs inside the issue list.
- Avoid exaggerated language. Use "not sufficiently demonstrated", "not clearly isolated", "requires clarification", "the evidence is too narrow", or "the claim should be narrowed".
- Do not invent citations or facts. If a comparison requires literature support, ask the authors for a focused comparison rather than fabricating references.
- Include only major and minor comments addressing actual manuscript weaknesses. Omit desirable extensions and future-work wish lists.
- Prefer clarification, corrected reasoning, reanalysis of existing results, or narrowed claims before requesting new experiments.

## Major Comment Pattern

Use this shape:

1. Problem sentence: identify the specific weakness.
2. Evidence sentence: point to the relevant claim, table, figure, model, or experiment.
3. Required action: give the least burdensome change that resolves the concern. Request a new experiment only when the central claim cannot be supported by clarification, correction, existing data, or a narrower claim.

Example:

`The application claim is broader than the verified operating conditions. The method is demonstrated only under fixed or calibrated coupling, while the conclusion is written for general misalignment. Please align the claim with the demonstrated range and explain why the existing evidence is sufficient. If wide-range misalignment is essential to the claimed contribution, provide one focused validation that directly tests it.`

## Evidence Proportionality

- Base requests on the logical burden created by the authors' claim, not on an idealized checklist for a complete research program.
- A missing parameter is a review issue only when it prevents interpretation, verification, or fair comparison of a central result.
- State the concrete consequence of a missing condition or parameter for the conclusion being evaluated. Do not ask for a complete experimental specification merely because some details are absent.
- A missing experiment is a major issue only when the manuscript's central conclusion depends on an untested relationship or when the existing experiment does not measure the claimed outcome.
- An experiment request must name the conclusion, cite the current evidence, and explain the specific validation gap. Review the theory-to-simulation-to-experiment reasoning before deciding more data are needed; do not assume a longer test campaign is inherently better.
- Do not ask for many variants of the same validation. Identify the single most discriminating comparison or measurement when additional evidence is genuinely necessary.
- If the evidence is credible but limited, recommend narrowing the conclusion instead of automatically expanding the experimental campaign.
- After narrowing, judge whether the remaining result still preserves a sufficient novel contribution. If the advertised novelty disappears, narrowing alone does not resolve the publication concern.

## Novelty Judgment

- Distinguish an unclear contribution statement from a substantiated lack of novelty. Missing citations or comparison tables alone do not establish that the method is unoriginal.
- Identify the closest established approach and the substantive difference in mechanism, method, capability, or insight. System integration can be a contribution when the integration itself offers a meaningful advance; familiar components alone do not disprove novelty.
- If the available literature evidence is insufficient for a firm judgment, ask the authors to clarify the specific distinction and describe novelty as not yet established, rather than asserting it is absent.

## Minor Comment Pattern

Use one or two sentences per item. Minor comments should cover clarity, terminology, table headings, material missing definitions, symbol consistency, and reporting definitions. Avoid accumulating minor requests for nonessential implementation detail.

## Recommendation Tone

- `Reject`: use when supported analysis shows that the core mechanism fails, the contribution lacks sufficient novelty or significance, or repair would require replacing the central contribution or redoing the main research. An unclear explanation or a missing experiment alone is not sufficient.
- `Major revision`: use when the contribution is potentially publishable and substantive flaws can reasonably be repaired while preserving it, for example by correcting a derivation, clarifying a comparison, analyzing existing results, or closing a specific validation gap.
- `Minor revision`: use when the technical story is mostly complete and only presentation or limited clarification is needed.
- `Accept`: use when the contribution and supporting argument are sufficient and no substantive revision is needed. Do not impose a prior preference for rejection or revision.
