# Underlying-Model Layer Analysis

## Scope

This note turns the frontier audit into manuscript-facing analytical findings.
It is not a model leaderboard and it is not a second evidence tier.
Its purpose is to show what the `m_i` layer adds once we stop treating underlying-model information as mere metadata.

- audited frontier rows: `34`
- `A` rows: `22`
- `T` rows: `12`
- Tier split inside this frontier audit: `Tier 0 = 8`, `Tier 1 = 14`, `Tier 2 = 12`

## Key Quantitative Contrasts

### 1. Agentic papers are richer in organizational structure than in model-layer reporting

Only `9` of `22` agentic rows report the underlying-model layer exactly, while `13` remain `partial` or `vague`.
By contrast, `9` of `12` tool-assisted rows are `exact` on the model layer.

| Group | exact | partial | vague |
| --- | ---: | ---: | ---: |
| A | 9 | 7 | 6 |
| T | 9 | 3 | 0 |

This is one of the most useful durable findings from the strengthened corpus: frontier agentic systems have become more interesting as organizations than as well-specified model-layer experiments.

### 2. Tool-assisted papers are currently better laboratories for model sensitivity than agentic papers

Rows with strong sensitivity evidence (`explicit comparison` or `architecture-controlled comparison`): `6` of `22` for `A`, versus `5` of `12` for `T`.

| Group | architecture-controlled comparison | explicit comparison | weak mention | none |
| --- | ---: | ---: | ---: | ---: |
| A | 3 | 3 | 5 | 11 |
| T | 0 | 5 | 1 | 6 |

This matters because it limits how confidently we can attribute frontier gains to architecture alone. The literature is still better at building agentic trading workflows than at isolating the contribution of the underlying model inside those workflows.

### 3. Heterogeneous model allocation is real, but still concentrated outside the core agentic block

Only `4` of `22` agentic rows clearly report `multi-model heterogeneous` allocation, compared with `5` of `12` tool-assisted rows.

| Group | multi-model heterogeneous | single-model homogeneous | unspecified |
| --- | ---: | ---: | ---: |
| A | 4 | 9 | 9 |
| T | 5 | 5 | 2 |

Clear heterogeneous-allocation examples are: `A050`, `A055`, `A059`, `A065`, `A067`, `A069`, `A074`, `A078`, `A081`.

This supports a stronger paper-level statement than the early draft could make: the literature says much more about role decomposition than about model-to-role allocation.

### 4. Tier 2 does not imply model-layer clarity

Among the `12` agentic Tier-2 rows in the frontier audit, only `5` have `exact` model-layer specification and only `3` show strong sensitivity evidence.

| Group | exact | partial | vague |
| --- | ---: | ---: | ---: |
| 0 | 6 | 1 | 1 |
| 1 | 7 | 5 | 2 |
| 2 | 5 | 4 | 3 |

| Group | architecture-controlled comparison | explicit comparison | weak mention | none |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0 | 3 | 1 | 4 |
| 1 | 1 | 4 | 3 | 6 |
| 2 | 2 | 1 | 2 | 7 |

Agentic Tier-2 rows with strong sensitivity evidence: `A032`, `A076`, `A078`.

This is exactly why the `m_i` layer should remain parallel to `z_i` in this revision. A paper can have meaningful trading evidence without having isolated the underlying-model effect cleanly.

### 5. What the layer now lets the paper say

The strengthened corpus now supports four claims that were previously too thin:

- the frontier is materially stronger on agentic systems than before, but still under-specified on the model layer
- closed-source/API-based dependence is not the whole story; allocation, sensitivity, and specification matter too
- model-layer opacity and under-specification are now measurable bottlenecks, not just abstract concerns
- a minimum reporting protocol for the underlying-model layer is justified as a normative contribution

## Working Manuscript Use

This artifact should feed three places in the paper:

- the framework section, to explain why `m_i` exists
- the findings section, to qualify architecture claims
- the agenda section, to justify sensitivity experiments and reporting standards

It should **not** be used to rank models or to imply that closed-source work is invalid by default.
