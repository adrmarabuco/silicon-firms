# Underlying-Model Layer: Frontier Audit

## Scope

This audit expands the earlier pilot into a complete frontier slice.
It covers every `A` and `T` paper in the active corpus, so the model-layer claims can be audited without relying on a convenience subset.

- audited frontier rows: `34`
- `A` papers: `22`
- `T` papers: `12`

The coded rows are in:

- [underlying_model_layer_frontier_audit.csv](/home/maradev/apps/trading-survey/results/underlying_model_layer_frontier_audit.csv)

## Field Distribution

### Model family

- `general-purpose proprietary`: `11`
- `mixed`: `9`
- `unspecified`: `8`
- `open-weight general-purpose`: `4`
- `finance-specialized`: `2`

### Release type

- `closed-source/API-based`: `11`
- `mixed`: `9`
- `unspecified`: `8`
- `open-weight`: `6`

### Allocation pattern

- `single-model homogeneous`: `14`
- `unspecified`: `11`
- `multi-model heterogeneous`: `9`

### Sensitivity evidence

- `none`: `17`
- `explicit comparison`: `8`
- `weak mention`: `6`
- `architecture-controlled comparison`: `3`

### Specification quality

- `exact`: `18`
- `partial`: `10`
- `vague`: `6`

## Release Type by System Type

| Release type | A | T |
| --- | ---: | ---: |
| `closed-source/API-based` | 8 | 3 |
| `mixed` | 4 | 5 |
| `open-weight` | 3 | 3 |
| `unspecified` | 7 | 1 |

## What This Audit Shows

### 1. The underlying-model layer is informative beyond governance bookkeeping

Even in this bounded frontier slice, `release_type` is not random noise.
There is a real split between `open-weight`, `closed-source/API-based`, `mixed`, and `unspecified` papers, and that split matters when we interpret reproducibility and deployment credibility.

### 2. Release type alone is too narrow

The most informative rows are not defined only by `open-weight` versus `closed-source/API-based`.
They are defined by whether the paper:

- compares underlying models explicitly
- allocates different models across roles
- or specifies the model layer with enough precision to make replication meaningful

Rows with explicit or architecture-controlled sensitivity evidence: `A021`, `A023`, `A032`, `A041`, `A065`, `A067`, `A069`, `A076`, `A078`, `A081`, `A082`.

### 3. Heterogeneous model allocation is still rare

Only `9` rows in this frontier slice clearly report `multi-model heterogeneous` allocation.
Examples: `A050`, `A055`, `A059`, `A065`, `A067`, `A069`, `A074`, `A078`.

This matters because many papers are now rich on role architecture, but still weak on the concrete question of which underlying model powers which role.

### 4. Tool-assisted papers are often stronger than frontier agentic papers on model comparison

Several of the clearest model-sensitivity cases come from tool-use benchmarks or execution-adjacent task papers rather than from the most architecturally ambitious agentic trading systems.
That is a useful result for the paper: the literature is moving faster on organizational and agentic structure than on isolating the contribution of the underlying model layer.

### 5. Under-specification remains a frontier bottleneck

Agentic rows with only `partial` or `vague` model-layer specification: `13` out of `22`.
Examples: `A013`, `A015`, `A021`, `A024`, `A025`, `A026`, `A030`, `A068`, `A070`, `A071`.

This gives the paper a concrete and durable claim:

- the frontier has matured faster in organizational design than in reporting or isolating the underlying-model layer

## Working Interpretation

The frontier audit strengthens the case for treating the `underlying model` as a real analytical layer.
But it also shows why `release_type` should not carry that whole burden alone.

A good paper-level treatment now looks like this:

- keep `release_type` because it captures reproducibility and deployment opacity
- pair it with allocation, sensitivity, and specification fields
- use the combined layer to qualify claims about architecture, evidence, and maturity

This supports the current recommendation:

- do not turn the paper into a model leaderboard
- do not ignore the underlying-model layer either
- treat it as a descriptive-analytical layer first, and only then decide how much enters the formal framework
