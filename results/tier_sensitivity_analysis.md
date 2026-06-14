# Tier Sensitivity Analysis

The key question from the review is whether boundary instability between Tier 1 and Tier 2 alters the paper's headline narrative.

## Baseline

- Tier counts: `{2: 23, 1: 30, 0: 28}`
- System counts: `{'N': 47, 'T': 12, 'A': 22}`

## Conservative Tier Scenario

- Downgrade rule: current `Tier 2` papers fall to `Tier 1` when the second-pass recoding does not recover `Tier 2+`.
- Tier counts: `{2: 22, 1: 31, 0: 28}`

## Liberal Tier Scenario

- Upgrade rule: current `Tier 1` papers rise to `Tier 2` when the second-pass recoding recovers `Tier 2+`.
- Tier counts: `{2: 35, 1: 18, 0: 28}`

## Structural Conservative Scenario

- Rule: current `A` papers fall back to the second-pass structural class when the recoding does not recover `A`.
- System counts: `{'N': 47, 'T': 17, 'A': 17}`

## Bottom Line

- Tier-2 ceiling robust across scenarios: `True`
- In all scenarios, the maximum realized tier remains `2`; boundary instability changes the distribution between Tier 1 and Tier 2, but does not create any Tier 3/4 paper.
