#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / 'results' / 'underlying_model_layer_frontier_audit.csv'
MD_PATH = ROOT / 'results' / 'underlying_model_layer_analysis.md'


def read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def crosstab(rows: list[dict[str, str]], row_key: str, col_key: str) -> dict[str, Counter[str]]:
    out: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        out[row[row_key]][row[col_key]] += 1
    return dict(out)


def render_table(tab: dict[str, Counter[str]], cols: list[str], row_order: list[str]) -> list[str]:
    lines = ["| Group | " + " | ".join(cols) + " |", "| --- | " + " | ".join(["---:" for _ in cols]) + " |"]
    for row in row_order:
        counts = tab.get(row, Counter())
        lines.append("| {} | {} |".format(row, " | ".join(str(counts.get(col, 0)) for col in cols)))
    return lines


def ids_for(rows: list[dict[str, str]], predicate) -> str:
    ids = [r['record_id'] for r in rows if predicate(r)]
    return ', '.join(f'`{rid}`' for rid in ids) if ids else 'none'


def build_markdown(rows: list[dict[str, str]]) -> str:
    by_type = Counter(r['system_type'] for r in rows)
    by_tier = Counter(r['evidence_tier'] for r in rows)
    spec_by_type = crosstab(rows, 'system_type', 'specification_quality')
    sens_by_type = crosstab(rows, 'system_type', 'sensitivity_evidence')
    alloc_by_type = crosstab(rows, 'system_type', 'allocation_pattern')
    sens_by_tier = crosstab(rows, 'evidence_tier', 'sensitivity_evidence')
    spec_by_tier = crosstab(rows, 'evidence_tier', 'specification_quality')

    a_rows = [r for r in rows if r['system_type'] == 'A']
    t_rows = [r for r in rows if r['system_type'] == 'T']
    a_tier2 = [r for r in rows if r['system_type'] == 'A' and r['evidence_tier'] == '2']

    a_exact = sum(1 for r in a_rows if r['specification_quality'] == 'exact')
    t_exact = sum(1 for r in t_rows if r['specification_quality'] == 'exact')
    a_sens = sum(1 for r in a_rows if r['sensitivity_evidence'] in {'explicit comparison', 'architecture-controlled comparison'})
    t_sens = sum(1 for r in t_rows if r['sensitivity_evidence'] in {'explicit comparison', 'architecture-controlled comparison'})
    a_hetero = sum(1 for r in a_rows if r['allocation_pattern'] == 'multi-model heterogeneous')
    t_hetero = sum(1 for r in t_rows if r['allocation_pattern'] == 'multi-model heterogeneous')
    tier2_exact = sum(1 for r in a_tier2 if r['specification_quality'] == 'exact')
    tier2_sens = sum(1 for r in a_tier2 if r['sensitivity_evidence'] in {'explicit comparison', 'architecture-controlled comparison'})

    lines: list[str] = [
        '# Underlying-Model Layer Analysis',
        '',
        '## Scope',
        '',
        'This note turns the frontier audit into manuscript-facing analytical findings.',
        'It is not a model leaderboard and it is not a second evidence tier.',
        'Its purpose is to show what the `m_i` layer adds once we stop treating underlying-model information as mere metadata.',
        '',
        f'- audited frontier rows: `{len(rows)}`',
        f'- `A` rows: `{by_type.get("A", 0)}`',
        f'- `T` rows: `{by_type.get("T", 0)}`',
        f'- Tier split inside this frontier audit: `Tier 0 = {by_tier.get("0", 0)}`, `Tier 1 = {by_tier.get("1", 0)}`, `Tier 2 = {by_tier.get("2", 0)}`',
        '',
        '## Key Quantitative Contrasts',
        '',
        '### 1. Agentic papers are richer in organizational structure than in model-layer reporting',
        '',
        f'Only `{a_exact}` of `{len(a_rows)}` agentic rows report the underlying-model layer exactly, while `{len(a_rows) - a_exact}` remain `partial` or `vague`.',
        f'By contrast, `{t_exact}` of `{len(t_rows)}` tool-assisted rows are `exact` on the model layer.',
        '',
        *render_table(spec_by_type, ['exact', 'partial', 'vague'], ['A', 'T']),
        '',
        'This is one of the most useful durable findings from the strengthened corpus: frontier agentic systems have become more interesting as organizations than as well-specified model-layer experiments.',
        '',
        '### 2. Tool-assisted papers are currently better laboratories for model sensitivity than agentic papers',
        '',
        f'Rows with strong sensitivity evidence (`explicit comparison` or `architecture-controlled comparison`): `{a_sens}` of `{len(a_rows)}` for `A`, versus `{t_sens}` of `{len(t_rows)}` for `T`.',
        '',
        *render_table(sens_by_type, ['architecture-controlled comparison', 'explicit comparison', 'weak mention', 'none'], ['A', 'T']),
        '',
        'This matters because it limits how confidently we can attribute frontier gains to architecture alone. The literature is still better at building agentic trading workflows than at isolating the contribution of the underlying model inside those workflows.',
        '',
        '### 3. Heterogeneous model allocation is real, but still concentrated outside the core agentic block',
        '',
        f'Only `{a_hetero}` of `{len(a_rows)}` agentic rows clearly report `multi-model heterogeneous` allocation, compared with `{t_hetero}` of `{len(t_rows)}` tool-assisted rows.',
        '',
        *render_table(alloc_by_type, ['multi-model heterogeneous', 'single-model homogeneous', 'unspecified'], ['A', 'T']),
        '',
        f'Clear heterogeneous-allocation examples are: {ids_for(rows, lambda r: r["allocation_pattern"] == "multi-model heterogeneous")}.',
        '',
        'This supports a stronger paper-level statement than the early draft could make: the literature says much more about role decomposition than about model-to-role allocation.',
        '',
        '### 4. Tier 2 does not imply model-layer clarity',
        '',
        f'Among the `{len(a_tier2)}` agentic Tier-2 rows in the frontier audit, only `{tier2_exact}` have `exact` model-layer specification and only `{tier2_sens}` show strong sensitivity evidence.',
        '',
        *render_table(spec_by_tier, ['exact', 'partial', 'vague'], ['0', '1', '2']),
        '',
        *render_table(sens_by_tier, ['architecture-controlled comparison', 'explicit comparison', 'weak mention', 'none'], ['0', '1', '2']),
        '',
        f'Agentic Tier-2 rows with strong sensitivity evidence: {ids_for(a_tier2, lambda r: r["sensitivity_evidence"] in {"explicit comparison", "architecture-controlled comparison"})}.',
        '',
        'This is exactly why the `m_i` layer should remain parallel to `z_i` in this revision. A paper can have meaningful trading evidence without having isolated the underlying-model effect cleanly.',
        '',
        '### 5. What the layer now lets the paper say',
        '',
        'The strengthened corpus now supports four claims that were previously too thin:',
        '',
        '- the frontier is materially stronger on agentic systems than before, but still under-specified on the model layer',
        '- closed-source/API-based dependence is not the whole story; allocation, sensitivity, and specification matter too',
        '- model-layer opacity and under-specification are now measurable bottlenecks, not just abstract concerns',
        '- a minimum reporting protocol for the underlying-model layer is justified as a normative contribution',
        '',
        '## Working Manuscript Use',
        '',
        'This artifact should feed three places in the paper:',
        '',
        '- the framework section, to explain why `m_i` exists',
        '- the findings section, to qualify architecture claims',
        '- the agenda section, to justify sensitivity experiments and reporting standards',
        '',
        'It should **not** be used to rank models or to imply that closed-source work is invalid by default.',
    ]
    return '\n'.join(lines) + '\n'


def main() -> None:
    rows = read_rows()
    MD_PATH.write_text(build_markdown(rows), encoding='utf-8')
    print(f'Wrote {MD_PATH.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
