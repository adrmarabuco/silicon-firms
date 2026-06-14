from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "results" / "underlying_model_layer_frontier_audit.csv"
MD_PATH = ROOT / "results" / "underlying_model_layer_frontier_audit.md"


def read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fmt_counter(counter: Counter[str]) -> list[str]:
    lines = []
    for key, value in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- `{key}`: `{value}`")
    return lines


def collect_examples(rows: list[dict[str, str]], field: str, value: str) -> str:
    ids = [r["record_id"] for r in rows if r[field] == value]
    return ", ".join(f"`{rid}`" for rid in ids[:8]) if ids else "none"


def build_markdown(rows: list[dict[str, str]]) -> str:
    total = len(rows)
    by_type = Counter(r["system_type"] for r in rows)
    by_release = Counter(r["release_type"] for r in rows)
    by_family = Counter(r["model_family"] for r in rows)
    by_alloc = Counter(r["allocation_pattern"] for r in rows)
    by_sens = Counter(r["sensitivity_evidence"] for r in rows)
    by_spec = Counter(r["specification_quality"] for r in rows)

    rows_a = [r for r in rows if r["system_type"] == "A"]
    rows_t = [r for r in rows if r["system_type"] == "T"]

    def cross(rows_subset: list[dict[str, str]], field: str) -> dict[str, Counter[str]]:
        out: dict[str, Counter[str]] = defaultdict(Counter)
        for row in rows_subset:
            out[row[field]][row["system_type"]] += 1
        return dict(out)

    release_by_type = cross(rows, "release_type")
    sens_explicit = [
        r["record_id"]
        for r in rows
        if r["sensitivity_evidence"] in {"explicit comparison", "architecture-controlled comparison"}
    ]
    hetero = [r["record_id"] for r in rows if r["allocation_pattern"] == "multi-model heterogeneous"]
    weak_spec_a = [r["record_id"] for r in rows_a if r["specification_quality"] in {"vague", "partial"}]

    lines: list[str] = [
        "# Underlying-Model Layer: Frontier Audit",
        "",
        "## Scope",
        "",
        "This audit expands the earlier pilot into a complete frontier slice.",
        "It covers every `A` and `T` paper in the active corpus, so the model-layer claims can be audited without relying on a convenience subset.",
        "",
        f"- audited frontier rows: `{total}`",
        f"- `A` papers: `{by_type.get('A', 0)}`",
        f"- `T` papers: `{by_type.get('T', 0)}`",
        "",
        "The coded rows are in:",
        "",
        f"- [underlying_model_layer_frontier_audit.csv]({CSV_PATH})",
        "",
        "## Field Distribution",
        "",
        "### Model family",
        "",
        *fmt_counter(by_family),
        "",
        "### Release type",
        "",
        *fmt_counter(by_release),
        "",
        "### Allocation pattern",
        "",
        *fmt_counter(by_alloc),
        "",
        "### Sensitivity evidence",
        "",
        *fmt_counter(by_sens),
        "",
        "### Specification quality",
        "",
        *fmt_counter(by_spec),
        "",
        "## Release Type by System Type",
        "",
        "| Release type | A | T |",
        "| --- | ---: | ---: |",
    ]

    for release_type, counts in sorted(release_by_type.items()):
        lines.append(f"| `{release_type}` | {counts.get('A', 0)} | {counts.get('T', 0)} |")

    lines.extend(
        [
            "",
            "## What This Audit Shows",
            "",
            "### 1. The underlying-model layer is informative beyond governance bookkeeping",
            "",
            "Even in this bounded frontier slice, `release_type` is not random noise.",
            "There is a real split between `open-weight`, `closed-source/API-based`, `mixed`, and `unspecified` papers, and that split matters when we interpret reproducibility and deployment credibility.",
            "",
            "### 2. Release type alone is too narrow",
            "",
            "The most informative rows are not defined only by `open-weight` versus `closed-source/API-based`.",
            "They are defined by whether the paper:",
            "",
            "- compares underlying models explicitly",
            "- allocates different models across roles",
            "- or specifies the model layer with enough precision to make replication meaningful",
            "",
            f"Rows with explicit or architecture-controlled sensitivity evidence: {', '.join(f'`{rid}`' for rid in sens_explicit) if sens_explicit else 'none'}.",
            "",
            "### 3. Heterogeneous model allocation is still rare",
            "",
            f"Only `{len(hetero)}` rows in this frontier slice clearly report `multi-model heterogeneous` allocation.",
            f"Examples: {', '.join(f'`{rid}`' for rid in hetero[:8]) if hetero else 'none'}.",
            "",
            "This matters because many papers are now rich on role architecture, but still weak on the concrete question of which underlying model powers which role.",
            "",
            "### 4. Tool-assisted papers are often stronger than frontier agentic papers on model comparison",
            "",
            "Several of the clearest model-sensitivity cases come from tool-use benchmarks or execution-adjacent task papers rather than from the most architecturally ambitious agentic trading systems.",
            "That is a useful result for the paper: the literature is moving faster on organizational and agentic structure than on isolating the contribution of the underlying model layer.",
            "",
            "### 5. Under-specification remains a frontier bottleneck",
            "",
            f"Agentic rows with only `partial` or `vague` model-layer specification: `{len(weak_spec_a)}` out of `{len(rows_a)}`.",
            f"Examples: {', '.join(f'`{rid}`' for rid in weak_spec_a[:10]) if weak_spec_a else 'none'}.",
            "",
            "This gives the paper a concrete and durable claim:",
            "",
            "- the frontier has matured faster in organizational design than in reporting or isolating the underlying-model layer",
            "",
            "## Working Interpretation",
            "",
            "The frontier audit strengthens the case for treating the `underlying model` as a real analytical layer.",
            "But it also shows why `release_type` should not carry that whole burden alone.",
            "",
            "A good paper-level treatment now looks like this:",
            "",
            "- keep `release_type` because it captures reproducibility and deployment opacity",
            "- pair it with allocation, sensitivity, and specification fields",
            "- use the combined layer to qualify claims about architecture, evidence, and maturity",
            "",
            "This supports the current recommendation:",
            "",
            "- do not turn the paper into a model leaderboard",
            "- do not ignore the underlying-model layer either",
            "- treat it as a descriptive-analytical layer first, and only then decide how much enters the formal framework",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    rows = read_rows()
    MD_PATH.write_text(build_markdown(rows), encoding="utf-8")
    print(f"Wrote {MD_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
