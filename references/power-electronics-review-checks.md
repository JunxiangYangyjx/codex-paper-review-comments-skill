# Power Electronics Review Checks

Use this reference for WPT, IPT, converters, motor drives, charging, rectifiers, resonant networks, compensation networks, and power-control papers. These are diagnostic prompts, not a completeness checklist. Raise only the items that materially affect novelty, correctness, or support for a central conclusion.

## Primary Review Questions

- Novelty isolation: comparison against the closest topology, control, tuning, modulation, rectifier, or compensation method under comparable conditions.
- Theoretical consistency: dimensionally correct equations, stated assumptions, valid approximations, physically meaningful equivalent circuits, and a clear chain from model to claimed behavior.
- Evidence-to-claim alignment: simulations and experiments should measure the outcome being claimed and distinguish the proposed contribution from the relevant baseline.
- Internal coherence: topology, control description, simulation conditions, experiment, and conclusion should use compatible assumptions and operating points.

## Conditional Checks

Use these only when they are central to a claim or needed to interpret the presented result:

- Application boundary: fixed coupling versus misalignment, load variation, charging profile, or deployment assumptions. If the evidence is narrower than the prose, prefer narrowing the prose before requesting a broad test campaign.
- Theory-to-hardware link: measured-versus-predicted agreement or the effect of a dominant nonideality. Do not demand exhaustive parasitic, tolerance, or temperature studies unless robustness is a claimed contribution.
- Experimental scope: request one discriminating operating case when the existing test does not demonstrate the claimed mechanism. Do not routinely ask for full input/load/coupling/thermal maps.
- Efficiency definition: require clear measurement boundaries when efficiency is a principal result. Detailed auxiliary-loss accounting or uncertainty analysis is optional unless it could change the conclusion.
- Dynamic validation: require transient evidence only when dynamic performance, stability, or disturbance rejection is central to the contribution.
- Reproducibility: request only the parameters needed to understand or reproduce the novel mechanism; ordinary commercial part numbers and complete instrument lists are not default review requirements.

## Request Restraint

- Do not convert every plausible limitation into a major comment.
- Do not require additional experiments merely because they would make the paper more comprehensive.
- Prefer correction of equations, clearer assumptions, comparison with the closest method, analysis of existing waveforms/data, or narrowed conclusions.
- When new evidence is indispensable, ask for the smallest experiment or simulation that directly resolves the disputed claim.

## Useful Supporting Material

- Tables: system parameters, comparison tables, experimental result tables, loss breakdown tables.
- Figures: topology diagrams, gain/frequency curves, tuning characteristics, waveforms, efficiency maps, thermal/loss plots.
- Equations: key model equations, control objectives, equivalent component models, sensitivity relations, and transient equations.

## Wording Preferences

- Prefer "comparative operating cases" over "ablation" unless the paper itself uses ablation-style terminology.
- Prefer "operating boundary" and "measured-versus-predicted agreement" when those concepts are central; do not introduce them mechanically.
- Be precise about symbols and operating points: output power, load resistance, coupling coefficient, coil distance, efficiency, frequency, duty ratio, and bias/control current.
