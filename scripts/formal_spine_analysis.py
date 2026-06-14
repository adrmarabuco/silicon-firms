#!/usr/bin/env python3
"""
Build descriptive formal-analysis artifacts for the survey's graph/archetype spine.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_JSON = ROOT / "papers.json"
OUT_JSON = ROOT / "results" / "formal_spine_analysis.json"
OUT_MD = ROOT / "results" / "formal_spine_analysis.md"


ARTIFACT_SEARCH = {
    "A013",
    "A015",
    "A025",
    "A026",
    "A030",
    "A032",
    "A039",
    "A041",
    "A042",
    "A045",
    "A058",
    "A070",
    "A072",
    "A073",
    "A078",
    "A079",
    "A080",
    "A081",
}

ROLE_DECOMPOSED = {"A021", "A024", "A050", "A075", "A077"}

CONTEXT_TO_DECISION = {
    "A001",
    "A002",
    "A003",
    "A004",
    "A005",
    "A006",
    "A007",
    "A008",
    "A016",
    "A017",
    "A018",
    "A020",
    "A047",
    "A052",
    "A053",
    "A056",
    "A061",
    "A063",
    "A066",
}

ARCHETYPE_LABELS = [
    "context_to_decision",
    "artifact_search",
    "role_decomposed",
    "substrate",
]

ARCHETYPE_DISPLAY = {
    "context_to_decision": "Context-to-decision",
    "artifact_search": "Evaluator-coupled artifact search",
    "role_decomposed": "Role-decomposed organizations",
    "substrate": "Environment and governance substrate",
}

SYSTEM_LABELS = ["N", "T", "A"]
TIER_LABELS = [0, 1, 2]


def load_papers() -> list[dict]:
    return json.loads(PAPERS_JSON.read_text())


def assign_archetype(record_id: str) -> str:
    if record_id in ARTIFACT_SEARCH:
        return "artifact_search"
    if record_id in ROLE_DECOMPOSED:
        return "role_decomposed"
    if record_id in CONTEXT_TO_DECISION:
        return "context_to_decision"
    return "substrate"


def contingency(rows: list[str], cols: list[int], assignments: list[tuple[str, int]]) -> list[list[int]]:
    table = [[0 for _ in cols] for _ in rows]
    r_idx = {label: i for i, label in enumerate(rows)}
    c_idx = {label: j for j, label in enumerate(cols)}
    for row, col in assignments:
        if row in r_idx and col in c_idx:
            table[r_idx[row]][c_idx[col]] += 1
    return table


def chi_square_stat(table: list[list[int]]) -> float:
    row_sums = [sum(row) for row in table]
    col_sums = [sum(table[i][j] for i in range(len(table))) for j in range(len(table[0]))]
    total = sum(row_sums)
    stat = 0.0
    for i, row_sum in enumerate(row_sums):
        for j, col_sum in enumerate(col_sums):
            expected = row_sum * col_sum / total if total else 0.0
            if expected > 0:
                stat += (table[i][j] - expected) ** 2 / expected
    return stat


def cramers_v(table: list[list[int]]) -> float:
    total = sum(sum(row) for row in table)
    if total == 0:
        return 0.0
    k = min(len(table) - 1, len(table[0]) - 1)
    if k <= 0:
        return 0.0
    return math.sqrt(chi_square_stat(table) / (total * k))


def permutation_p_value(row_labels: list[str], col_values: list[int], iterations: int = 20000, seed: int = 7) -> float:
    rng = random.Random(seed)
    observed_pairs = list(zip(row_labels, col_values))
    rows = sorted(set(row_labels), key=row_labels.index)
    cols = sorted(set(col_values))
    observed = contingency(rows, cols, observed_pairs)
    observed_stat = chi_square_stat(observed)

    count = 0
    perm_cols = list(col_values)
    for _ in range(iterations):
        rng.shuffle(perm_cols)
        stat = chi_square_stat(contingency(rows, cols, list(zip(row_labels, perm_cols))))
        if stat >= observed_stat - 1e-12:
            count += 1
    return (count + 1) / (iterations + 1)


def bootstrap_v_ci(assignments: list[tuple[str, int]], rows: list[str], cols: list[int], iterations: int = 2000, seed: int = 11) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(assignments)
    vals = []
    for _ in range(iterations):
        sample = [assignments[rng.randrange(n)] for _ in range(n)]
        vals.append(cramers_v(contingency(rows, cols, sample)))
    vals.sort()
    lo = vals[int(0.025 * len(vals))]
    hi = vals[int(0.975 * len(vals))]
    return lo, hi


def build() -> dict:
    papers = load_papers()
    assignments_system = []
    assignments_arch = []
    rows = []
    for rec in papers:
        rid = rec["bibliographic"]["record_id"]
        system_type = rec["classification"]["system_type"]
        tier = rec["evaluation"]["evidence_tier"]
        archetype = assign_archetype(rid)
        assignments_system.append((system_type, tier))
        assignments_arch.append((archetype, tier))
        rows.append(
            {
                "record_id": rid,
                "title": rec["bibliographic"]["title"],
                "system_type": system_type,
                "tier": tier,
                "archetype": archetype,
            }
        )

    sys_table = contingency(SYSTEM_LABELS, TIER_LABELS, assignments_system)
    arch_table = contingency(ARCHETYPE_LABELS, TIER_LABELS, assignments_arch)

    sys_p = permutation_p_value(
        [r for r, _ in assignments_system], [c for _, c in assignments_system]
    )
    arch_p = permutation_p_value(
        [r for r, _ in assignments_arch], [c for _, c in assignments_arch]
    )
    sys_v = cramers_v(sys_table)
    arch_v = cramers_v(arch_table)
    sys_ci = bootstrap_v_ci(assignments_system, SYSTEM_LABELS, TIER_LABELS)
    arch_ci = bootstrap_v_ci(assignments_arch, ARCHETYPE_LABELS, TIER_LABELS)

    return {
        "system_type_x_tier": {
            "rows": SYSTEM_LABELS,
            "cols": TIER_LABELS,
            "table": sys_table,
            "cramers_v": sys_v,
            "permutation_p": sys_p,
            "bootstrap_ci": sys_ci,
        },
        "archetype_x_tier": {
            "rows": ARCHETYPE_LABELS,
            "cols": TIER_LABELS,
            "table": arch_table,
            "cramers_v": arch_v,
            "permutation_p": arch_p,
            "bootstrap_ci": arch_ci,
        },
        "archetype_counts": dict(Counter(row["archetype"] for row in rows)),
        "records": rows,
    }


def write_markdown(data: dict) -> None:
    lines = [
        "# Formal Spine Analysis",
        "",
        "## Archetype Counts",
        "",
    ]
    for key in ARCHETYPE_LABELS:
        lines.append(f"- `{ARCHETYPE_DISPLAY[key]}`: `{data['archetype_counts'].get(key, 0)}`")

    lines.extend(["", "## System Type x Tier", ""])
    sys = data["system_type_x_tier"]
    lines.append(f"- Cramer's V: `{sys['cramers_v']:.3f}`")
    lines.append(f"- Bootstrap 95% CI: `[{sys['bootstrap_ci'][0]:.3f}, {sys['bootstrap_ci'][1]:.3f}]`")
    lines.append(f"- Permutation p-value: `{sys['permutation_p']:.4f}`")
    lines.append("")
    lines.append("| Type | Tier 0 | Tier 1 | Tier 2 |")
    lines.append("|---|---:|---:|---:|")
    for label, row in zip(sys["rows"], sys["table"]):
        lines.append(f"| {label} | {row[0]} | {row[1]} | {row[2]} |")

    lines.extend(["", "## Archetype x Tier", ""])
    arch = data["archetype_x_tier"]
    lines.append(f"- Cramer's V: `{arch['cramers_v']:.3f}`")
    lines.append(f"- Bootstrap 95% CI: `[{arch['bootstrap_ci'][0]:.3f}, {arch['bootstrap_ci'][1]:.3f}]`")
    lines.append(f"- Permutation p-value: `{arch['permutation_p']:.4f}`")
    lines.append("")
    lines.append("| Archetype | Tier 0 | Tier 1 | Tier 2 |")
    lines.append("|---|---:|---:|---:|")
    for label, row in zip(arch["rows"], arch["table"]):
        lines.append(f"| {ARCHETYPE_DISPLAY[label]} | {row[0]} | {row[1]} | {row[2]} |")

    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> None:
    data = build()
    OUT_JSON.write_text(json.dumps(data, indent=2))
    write_markdown(data)
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
