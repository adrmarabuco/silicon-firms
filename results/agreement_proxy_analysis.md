# Agreement Proxy Analysis

These are rule-based stability proxies, not dual independent annotations.

## Adaptive Boundary Proxy

- Task: `A vs non-A`
- Accuracy: `0.908`
- Precision: `0.800`
- Recall: `0.842`
- Cohen's kappa: `0.759`
- Counts: `TP=16`, `TN=53`, `FP=4`, `FN=3`

Mismatches:
- `A005`: assigned `N`, proxy `A`
- `A010`: assigned `N`, proxy `A`
- `A012`: assigned `N`, proxy `A`
- `A043`: assigned `N`, proxy `A`
- `A071`: assigned `A`, proxy `non-A`
- `A073`: assigned `A`, proxy `non-A`
- `A074`: assigned `A`, proxy `non-A`

## Tier Boundary Proxy

- Task: `Tier2+ vs Tier<2`
- Accuracy: `0.816`
- Precision: `0.632`
- Recall: `0.632`
- Cohen's kappa: `0.509`
- Counts: `TP=12`, `TN=50`, `FP=7`, `FN=7`

Mismatches:
- `A001`: assigned `2`, proxy `Tier<2`
- `A008`: assigned `2`, proxy `Tier<2`
- `A015`: assigned `1`, proxy `Tier2+`
- `A021`: assigned `1`, proxy `Tier2+`
- `A024`: assigned `1`, proxy `Tier2+`
- `A026`: assigned `2`, proxy `Tier<2`
- `A031`: assigned `1`, proxy `Tier2+`
- `A041`: assigned `1`, proxy `Tier2+`
- `A042`: assigned `1`, proxy `Tier2+`
- `A052`: assigned `2`, proxy `Tier<2`
- `A053`: assigned `2`, proxy `Tier<2`
- `A062`: assigned `2`, proxy `Tier<2`
- `A064`: assigned `2`, proxy `Tier<2`
- `A077`: assigned `1`, proxy `Tier2+`
