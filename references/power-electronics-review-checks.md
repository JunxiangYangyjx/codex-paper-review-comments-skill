# Power Electronics Review Checks

Use this reference for WPT, IPT, converters, motor drives, charging, rectifiers, resonant networks, compensation networks, and power-control papers.

## Common Major Issues

- Application boundary: fixed coupling versus misalignment, variable distance, load variation, battery charging profile, thermal stress, or field deployment constraints.
- Novelty isolation: comparison against the closest topology, control, tuning, modulation, rectifier, or compensation method under comparable conditions.
- Theory-to-hardware link: measured-versus-predicted values, calibration, parasitics, nonlinear magnetics, temperature drift, timing errors, device tolerances, and sensitivity.
- Experimental scope: input voltage, load range, coupling range, power level, operating frequency, current or voltage stages, dynamic transitions, and efficiency map.
- Efficiency definition: whether auxiliary supplies, gate drivers, bias supplies, sensing, control power, and magnetic or semiconductor losses are included.
- Dynamic validation: settling time, overshoot/undershoot, ripple, transition loss, detuning, stability margin, and sensitivity to sampling or zero-crossing errors.
- Hardware reproducibility: part numbers, magnetics geometry, winding details, capacitor values/tolerances, semiconductor devices, sensor bandwidth, controller platform, and measurement instruments.

## Useful Supporting Material

- Tables: system parameters, comparison tables, experimental result tables, loss breakdown tables.
- Figures: topology diagrams, gain/frequency curves, tuning characteristics, waveforms, efficiency maps, thermal/loss plots.
- Equations: key model equations, control objectives, equivalent component models, sensitivity relations, and transient equations.

## Wording Preferences

- Prefer "comparative operating cases" over "ablation" unless the paper itself uses ablation-style terminology.
- Prefer "implementation sensitivity", "calibration procedure", "operating boundary", "loss accounting", and "measured-versus-predicted agreement" for power electronics reviews.
- Be precise about symbols and operating points: output power, load resistance, coupling coefficient, coil distance, efficiency, frequency, duty ratio, and bias/control current.
