# Second-Pass Coding Audit Summary

This artifact compares the frozen corpus labels (`reviewer1`) against a second-pass internal recoding (`reviewer2`).
It is an audit of stability and borderline cases, not a claim of blinded dual-independent annotation.
For this revision snapshot, the adjudicated labels remain the frozen corpus labels after conservative review of mismatches.

## Structural Boundary

- Task: `Frozen A vs non-A compared with second-pass recoding`
- Accuracy: `0.889`
- Cohen's kappa: `0.715`
- Counts: `TP=17`, `TN=55`, `FP=4`, `FN=5`

Mismatches:
- `A003`: reviewer1=`N`, reviewer2=`T`
- `A004`: reviewer1=`N`, reviewer2=`T`
- `A005`: reviewer1=`N`, reviewer2=`A`
- `A007`: reviewer1=`N`, reviewer2=`T`
- `A008`: reviewer1=`N`, reviewer2=`T`
- `A010`: reviewer1=`N`, reviewer2=`A`
- `A011`: reviewer1=`N`, reviewer2=`T`
- `A012`: reviewer1=`N`, reviewer2=`A`
- `A014`: reviewer1=`N`, reviewer2=`T`
- `A016`: reviewer1=`N`, reviewer2=`T`
- `A017`: reviewer1=`N`, reviewer2=`T`
- `A018`: reviewer1=`N`, reviewer2=`T`
- `A020`: reviewer1=`N`, reviewer2=`T`
- `A031`: reviewer1=`N`, reviewer2=`T`
- `A034`: reviewer1=`N`, reviewer2=`T`
- `A035`: reviewer1=`N`, reviewer2=`T`
- `A038`: reviewer1=`N`, reviewer2=`T`
- `A039`: reviewer1=`N`, reviewer2=`T`
- `A042`: reviewer1=`N`, reviewer2=`T`
- `A043`: reviewer1=`N`, reviewer2=`A`
- `A044`: reviewer1=`N`, reviewer2=`T`
- `A046`: reviewer1=`N`, reviewer2=`T`
- `A049`: reviewer1=`N`, reviewer2=`T`
- `A052`: reviewer1=`N`, reviewer2=`T`
- `A053`: reviewer1=`N`, reviewer2=`T`
- `A054`: reviewer1=`N`, reviewer2=`T`
- `A061`: reviewer1=`N`, reviewer2=`T`
- `A062`: reviewer1=`N`, reviewer2=`T`
- `A063`: reviewer1=`N`, reviewer2=`T`
- `A064`: reviewer1=`N`, reviewer2=`T`
- `A066`: reviewer1=`N`, reviewer2=`T`
- `A071`: reviewer1=`A`, reviewer2=`T`
- `A073`: reviewer1=`A`, reviewer2=`T`
- `A074`: reviewer1=`A`, reviewer2=`T`
- `A079`: reviewer1=`A`, reviewer2=`T`
- `A080`: reviewer1=`N`, reviewer2=`T`
- `A081`: reviewer1=`A`, reviewer2=`T`

## Tier Boundary

- Task: `Frozen Tier2+ vs Tier<2 compared with second-pass recoding`
- Accuracy: `0.840`
- Cohen's kappa: `0.655`
- Counts: `TP=22`, `TN=46`, `FP=12`, `FN=1`

Mismatches:
- `A002`: reviewer1=`1`, reviewer2=`2`
- `A009`: reviewer1=`1`, reviewer2=`2`
- `A011`: reviewer1=`0`, reviewer2=`1`
- `A014`: reviewer1=`0`, reviewer2=`1`
- `A015`: reviewer1=`1`, reviewer2=`2`
- `A016`: reviewer1=`1`, reviewer2=`2`
- `A021`: reviewer1=`1`, reviewer2=`2`
- `A022`: reviewer1=`0`, reviewer2=`1`
- `A024`: reviewer1=`1`, reviewer2=`2`
- `A027`: reviewer1=`0`, reviewer2=`1`
- `A028`: reviewer1=`0`, reviewer2=`1`
- `A029`: reviewer1=`0`, reviewer2=`1`
- `A031`: reviewer1=`1`, reviewer2=`2`
- `A033`: reviewer1=`0`, reviewer2=`1`
- `A034`: reviewer1=`0`, reviewer2=`1`
- `A035`: reviewer1=`0`, reviewer2=`1`
- `A036`: reviewer1=`0`, reviewer2=`1`
- `A038`: reviewer1=`0`, reviewer2=`1`
- `A040`: reviewer1=`0`, reviewer2=`1`
- `A041`: reviewer1=`1`, reviewer2=`2`
- `A042`: reviewer1=`1`, reviewer2=`2`
- `A043`: reviewer1=`1`, reviewer2=`2`
- `A044`: reviewer1=`0`, reviewer2=`1`
- `A046`: reviewer1=`0`, reviewer2=`1`
- `A048`: reviewer1=`0`, reviewer2=`1`
- `A049`: reviewer1=`0`, reviewer2=`1`
- `A051`: reviewer1=`0`, reviewer2=`1`
- `A053`: reviewer1=`2`, reviewer2=`1`
- `A054`: reviewer1=`0`, reviewer2=`1`
- `A055`: reviewer1=`0`, reviewer2=`1`
- `A059`: reviewer1=`0`, reviewer2=`1`
- `A065`: reviewer1=`0`, reviewer2=`1`
- `A067`: reviewer1=`0`, reviewer2=`1`
- `A069`: reviewer1=`0`, reviewer2=`1`
- `A077`: reviewer1=`1`, reviewer2=`2`
- `A082`: reviewer1=`1`, reviewer2=`2`
