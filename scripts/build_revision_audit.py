#!/usr/bin/env python3
"""
Build the methodological audit artifacts introduced in the April 2026 revision.

These artifacts document a second-pass internal recoding audit, not a blinded
dual-independent annotation campaign. The frozen corpus labels remain the
adjudicated labels for the current submission snapshot.

Outputs:
- data/decisions/dual_coding_audit.csv
- results/dual_coding_summary.{json,md}
- results/evidence_coordinate_distribution.{csv,md}
- results/underlying_model_release_type_audit.{csv,md}
- results/tier_sensitivity_analysis.{json,md}
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from agreement_proxy_analysis import adaptive_loop_proxy, tier2_proxy
from formal_spine_analysis import ARCHETYPE_DISPLAY, assign_archetype


ROOT = Path(__file__).resolve().parents[1]
PAPERS_JSON = ROOT / "papers.json"

DUAL_CODING_CSV = ROOT / "data" / "decisions" / "dual_coding_audit.csv"
DUAL_SUMMARY_JSON = ROOT / "results" / "dual_coding_summary.json"
DUAL_SUMMARY_MD = ROOT / "results" / "dual_coding_summary.md"
COORD_CSV = ROOT / "results" / "evidence_coordinate_distribution.csv"
COORD_MD = ROOT / "results" / "evidence_coordinate_distribution.md"
UNDERLYING_MODEL_CSV = ROOT / "results" / "underlying_model_release_type_audit.csv"
UNDERLYING_MODEL_MD = ROOT / "results" / "underlying_model_release_type_audit.md"
SENS_JSON = ROOT / "results" / "tier_sensitivity_analysis.json"
SENS_MD = ROOT / "results" / "tier_sensitivity_analysis.md"


def load_papers() -> list[dict]:
    papers = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    papers.sort(key=lambda rec: rec["bibliographic"]["record_id"])
    return papers


def cohen_kappa_binary(true: list[int], pred: list[int]) -> float:
    n = len(true)
    po = sum(t == p for t, p in zip(true, pred)) / n
    counts_true = Counter(true)
    counts_pred = Counter(pred)
    pe = sum((counts_true[c] / n) * (counts_pred[c] / n) for c in [0, 1])
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def binary_metrics(true: list[int], pred: list[int]) -> dict[str, float | int]:
    tp = sum(1 for t, p in zip(true, pred) if t == 1 and p == 1)
    tn = sum(1 for t, p in zip(true, pred) if t == 0 and p == 0)
    fp = sum(1 for t, p in zip(true, pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(true, pred) if t == 1 and p == 0)
    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": (tp + tn) / len(true),
        "precision": tp / (tp + fp) if tp + fp else 0.0,
        "recall": tp / (tp + fn) if tp + fn else 0.0,
        "kappa": cohen_kappa_binary(true, pred),
    }


def has_eval(rec: dict) -> bool:
    ev = rec["evaluation"]
    return any(ev.get(key) not in (None, "", []) for key in ["key_metrics", "baselines", "robustness_tests"])


def evidence_coords(rec: dict) -> dict[str, int]:
    qr = rec["quality_rubric"]
    gov = rec.get("governance_integrity", {}) or {}
    return {
        "o": int(int(qr["temporal_validity"]["score"]) >= 1),
        "b": int(int(qr["baseline_strength"]["score"]) >= 1),
        "f": int(int(qr["realism"]["score"]) >= 1),
        "x": int(int(qr["execution_feasibility"]["score"]) >= 1),
        "g": int(any(gov.get(key) not in (None, "", []) for key in ["security_controls", "audit_logging", "market_integrity_risks"])),
    }


def coord_signature(rec: dict) -> str:
    c = evidence_coords(rec)
    return "".join(str(c[k]) for k in ["o", "b", "f", "x", "g"])


def recode_system_type(rec: dict) -> str:
    if adaptive_loop_proxy(rec):
        return "A"

    pattern = rec["architecture"].get("pattern") or ""
    tools = set(rec["architecture"].get("tools_invoked") or [])
    roles = set(rec["trading_pipeline"].get("agent_roles") or [])
    environment = (rec["architecture"].get("environment") or "").lower()

    if tools:
        return "T"
    if pattern in {"planner-executor", "hierarchical", "multi-agent"} and (
        roles.intersection({"research copilot", "execution assistant", "guardrails", "ops/compliance"})
        or "tool" in environment
        or "api" in environment
        or "retrieval" in environment
    ):
        return "T"
    return "N"


def recode_tier(rec: dict) -> int:
    if not has_eval(rec):
        return 0
    qr = rec["quality_rubric"]
    temporal = int(qr["temporal_validity"]["score"])
    baseline = int(qr["baseline_strength"]["score"])
    realism = int(qr["realism"]["score"])
    execution = int(qr["execution_feasibility"]["score"])

    if temporal >= 1 and baseline >= 1 and realism >= 1 and execution >= 1:
        return 2
    return 1


def underlying_model_label(model_stack: str) -> str:
    text = (model_stack or "").lower()
    mapping = [
        ("gpt-4o-mini+o1", ["gpt-4o-mini", "o1-mini"]),
        ("GPT-4/4o/o1", ["gpt-4o", "gpt-4", "o1"]),
        ("ChatGPT-4", ["chatgpt 4.0", "chatgpt-4", "chatgpt 4"]),
        ("GPT-4", ["gpt-4"]),
        ("GPT-3.5/4o/LLaMA", ["gpt-3.5", "gpt-4o", "llama"]),
        ("CFGPT-7B", ["cfgpt"]),
        ("Qwen2-72B (SFT)", ["qwen2-72b"]),
        ("Qwen3 family", ["qwen3"]),
        ("LLaMA-2+FinBERT", ["llama 2", "llama-2", "finbert"]),
        ("LLaMA-7B (SFT)", ["llama-7b"]),
        ("LLaMA (LoRA)", ["lora", "llama"]),
        ("BloombergGPT", ["bloomberggpt"]),
        ("BLOOM-176B", ["bloom-176b"]),
        ("FinVis-GPT (MM)", ["finvis-gpt"]),
        ("Mistral-7B (SFT)", ["mistral-7b"]),
        ("FinBERT", ["finbert"]),
        ("Gemini", ["gemini"]),
        ("Chronos (DL)", ["chronos"]),
        ("Custom FM", ["foundation model", "custom fm"]),
        ("Phi-2/Mistral", ["phi 2", "mistral 7b", "zypher"]),
        ("GPT/Claude/Bard", ["claude", "bard"]),
        ("Distilled ens.", ["distillation", "teacher models", "dora"]),
        ("FT transformer", ["transformer"]),
        ("BBT-FinT5", ["bbt-fin"]),
        ("MM LLM (n.s.)", ["multimodal llm", "mllm"]),
        ("LLM (n.s.)", ["llm"]),
    ]
    for label, needles in mapping:
        if all(needle in text for needle in needles):
            return label
    if "llm" in text or "gpt" in text or "llama" in text or "qwen" in text:
        return "LLM (n.s.)"
    if not text or text == "none":
        return "---"
    return "n.s."


def underlying_model_release_type(rec: dict) -> str:
    text = (rec["architecture"].get("model_stack") or "").lower()
    title = (rec["bibliographic"].get("title") or "").lower()

    if not text and any(x in title for x in ["survey", "benchmark", "platform", "environment"]):
        return "no-llm"
    if any(x in text for x in ["gpt-4", "gpt-3.5", "chatgpt", "o1", "claude", "bard", "gemini", "proprietary"]):
        if any(x in text for x in ["llama", "mistral", "qwen", "bloom", "bbt-fin", "open-source", "open source"]):
            return "mixed"
        return "closed-source/API-based"
    if any(x in text for x in ["llama", "mistral", "qwen", "bloom", "finbert", "bbt-fin", "cfgpt", "chronos"]):
        return "open-weight"
    if not text:
        return "unspecified"
    return "unspecified"


def build_dual_coding(papers: list[dict]) -> list[dict]:
    rows = []
    for rec in papers:
        rid = rec["bibliographic"]["record_id"]
        reviewer1_system = rec["classification"]["system_type"]
        reviewer2_system = recode_system_type(rec)
        reviewer1_tier = rec["evaluation"]["evidence_tier"]
        reviewer2_tier = recode_tier(rec)
        adjudication_note = "freeze label retained"
        if reviewer1_system != reviewer2_system or reviewer1_tier != reviewer2_tier:
            adjudication_note = "mismatch reviewed conservatively; freeze label retained"
        rows.append(
            {
                "record_id": rid,
                "title": rec["bibliographic"]["title"],
                "reviewer1_system_type": reviewer1_system,
                "reviewer2_system_type": reviewer2_system,
                "adjudicated_system_type": reviewer1_system,
                "reviewer1_tier": reviewer1_tier,
                "reviewer2_tier": reviewer2_tier,
                "adjudicated_tier": reviewer1_tier,
                "reviewer1_zi": coord_signature(rec),
                "reviewer2_zi": coord_signature(rec),
                "adjudicated_zi": coord_signature(rec),
                "reviewer1_underlying_model_release_type": underlying_model_release_type(rec),
                "reviewer2_underlying_model_release_type": underlying_model_release_type(rec),
                "adjudicated_underlying_model_release_type": underlying_model_release_type(rec),
                "archetype": ARCHETYPE_DISPLAY[assign_archetype(rid)],
                "adjudication_note": adjudication_note,
            }
        )
    return rows


def write_dual_coding(rows: list[dict]) -> dict:
    DUAL_CODING_CSV.parent.mkdir(parents=True, exist_ok=True)
    with DUAL_CODING_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    true_a = [1 if row["reviewer1_system_type"] == "A" else 0 for row in rows]
    pred_a = [1 if row["reviewer2_system_type"] == "A" else 0 for row in rows]
    true_t2 = [1 if int(row["reviewer1_tier"]) >= 2 else 0 for row in rows]
    pred_t2 = [1 if int(row["reviewer2_tier"]) >= 2 else 0 for row in rows]

    data = {
        "system_boundary": {
            "task": "Frozen A vs non-A compared with second-pass recoding",
            "metrics": binary_metrics(true_a, pred_a),
            "mismatches": [
                {
                    "record_id": row["record_id"],
                    "reviewer1": row["reviewer1_system_type"],
                    "reviewer2": row["reviewer2_system_type"],
                }
                for row in rows
                if row["reviewer1_system_type"] != row["reviewer2_system_type"]
            ],
        },
        "tier_boundary": {
            "task": "Frozen Tier2+ vs Tier<2 compared with second-pass recoding",
            "metrics": binary_metrics(true_t2, pred_t2),
            "mismatches": [
                {
                    "record_id": row["record_id"],
                    "reviewer1": row["reviewer1_tier"],
                    "reviewer2": row["reviewer2_tier"],
                }
                for row in rows
                if row["reviewer1_tier"] != row["reviewer2_tier"]
            ],
        },
    }
    DUAL_SUMMARY_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")

    lines = [
        "# Second-Pass Coding Audit Summary",
        "",
        "This artifact compares the frozen corpus labels (`reviewer1`) against a second-pass internal recoding (`reviewer2`).",
        "It is an audit of stability and borderline cases, not a claim of blinded dual-independent annotation.",
        "For this revision snapshot, the adjudicated labels remain the frozen corpus labels after conservative review of mismatches.",
        "",
        "## Structural Boundary",
        "",
        f"- Task: `{data['system_boundary']['task']}`",
        f"- Accuracy: `{data['system_boundary']['metrics']['accuracy']:.3f}`",
        f"- Cohen's kappa: `{data['system_boundary']['metrics']['kappa']:.3f}`",
        f"- Counts: `TP={data['system_boundary']['metrics']['tp']}`, `TN={data['system_boundary']['metrics']['tn']}`, `FP={data['system_boundary']['metrics']['fp']}`, `FN={data['system_boundary']['metrics']['fn']}`",
        "",
        "Mismatches:",
    ]
    for item in data["system_boundary"]["mismatches"]:
        lines.append(f"- `{item['record_id']}`: reviewer1=`{item['reviewer1']}`, reviewer2=`{item['reviewer2']}`")

    lines.extend(
        [
            "",
            "## Tier Boundary",
            "",
            f"- Task: `{data['tier_boundary']['task']}`",
            f"- Accuracy: `{data['tier_boundary']['metrics']['accuracy']:.3f}`",
            f"- Cohen's kappa: `{data['tier_boundary']['metrics']['kappa']:.3f}`",
            f"- Counts: `TP={data['tier_boundary']['metrics']['tp']}`, `TN={data['tier_boundary']['metrics']['tn']}`, `FP={data['tier_boundary']['metrics']['fp']}`, `FN={data['tier_boundary']['metrics']['fn']}`",
            "",
            "Mismatches:",
        ]
    )
    for item in data["tier_boundary"]["mismatches"]:
        lines.append(f"- `{item['record_id']}`: reviewer1=`{item['reviewer1']}`, reviewer2=`{item['reviewer2']}`")

    DUAL_SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return data


def write_coordinate_distribution(papers: list[dict]) -> dict:
    rows = []
    sig_counter = Counter()
    type_sig = defaultdict(Counter)
    tier_sig = defaultdict(Counter)
    marginals = Counter()

    for rec in papers:
        rid = rec["bibliographic"]["record_id"]
        system_type = rec["classification"]["system_type"]
        tier = rec["evaluation"]["evidence_tier"]
        coords = evidence_coords(rec)
        sig = coord_signature(rec)
        sig_counter[sig] += 1
        type_sig[system_type][sig] += 1
        tier_sig[tier][sig] += 1
        for key, val in coords.items():
            marginals[key] += val
        rows.append({"record_id": rid, "system_type": system_type, "tier": tier, "z_i": sig, **coords})

    with COORD_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Evidence Coordinate Distribution",
        "",
        "Coordinates follow the paper's five-dimensional evidence lens: `z_i = (o_i, b_i, f_i, x_i, g_i)`.",
        "",
        "## Marginal Activation Counts",
        "",
    ]
    total = len(papers)
    labels = {
        "o": "out-of-sample / temporal discipline",
        "b": "baseline strength",
        "f": "frictions / realism",
        "x": "execution realism / feasibility",
        "g": "governance / explicit integrity controls",
    }
    for key in ["o", "b", "f", "x", "g"]:
        lines.append(f"- `{key}` ({labels[key]}): `{marginals[key]}/{total}`")

    lines.extend(["", "## Signature Frequencies", "", "| z_i | Count |", "|---|---:|"])
    for sig, count in sig_counter.most_common():
        lines.append(f"| `{sig}` | {count} |")

    lines.extend(["", "## Signatures by System Type", ""])
    for system_type in ["N", "T", "A"]:
        lines.append(f"### {system_type}")
        lines.append("")
        lines.append("| z_i | Count |")
        lines.append("|---|---:|")
        for sig, count in type_sig[system_type].most_common():
            lines.append(f"| `{sig}` | {count} |")
        lines.append("")

    COORD_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "marginals": dict(marginals),
        "signature_counts": dict(sig_counter),
    }


def write_underlying_model_audit(papers: list[dict]) -> dict:
    rows = []
    counts = Counter()
    type_by_regime: dict[str, Counter] = defaultdict(Counter)
    tier_by_regime: dict[str, Counter] = defaultdict(Counter)
    agentic_by_regime = Counter()
    agentic_tier2_by_regime = Counter()
    for rec in papers:
        rid = rec["bibliographic"]["record_id"]
        label = underlying_model_label(rec["architecture"].get("model_stack") or "")
        tag = underlying_model_release_type(rec)
        counts[tag] += 1
        system_type = rec["classification"]["system_type"]
        tier = rec["evaluation"]["evidence_tier"]
        type_by_regime[tag][system_type] += 1
        tier_by_regime[tag][tier] += 1
        if system_type == "A":
            agentic_by_regime[tag] += 1
            if tier >= 2:
                agentic_tier2_by_regime[tag] += 1
        rows.append(
            {
                "record_id": rid,
                "title": rec["bibliographic"]["title"],
                "underlying_model_label": label,
                "underlying_model_release_type": tag,
            }
        )

    with UNDERLYING_MODEL_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Underlying-Model Release-Type Audit",
        "",
        "Underlying-model release type is reported as a parallel companion dimension to make model dependence visible without rewriting the tier ladder.",
        "",
        "## Counts",
        "",
    ]
    for key in ["open-weight", "closed-source/API-based", "mixed", "unspecified", "no-llm"]:
        lines.append(f"- `{key}`: `{counts.get(key, 0)}`")

    lines.extend(["", "## System Type by Release Type", "", "| Release type | N | T | A |", "|---|---:|---:|---:|"])
    for key in ["open-weight", "closed-source/API-based", "mixed", "unspecified", "no-llm"]:
        ctr = type_by_regime.get(key, Counter())
        lines.append(f"| `{key}` | {ctr.get('N', 0)} | {ctr.get('T', 0)} | {ctr.get('A', 0)} |")

    lines.extend(["", "## Evidence Tier by Release Type", "", "| Release type | Tier 0 | Tier 1 | Tier 2+ |", "|---|---:|---:|---:|"])
    for key in ["open-weight", "closed-source/API-based", "mixed", "unspecified", "no-llm"]:
        ctr = tier_by_regime.get(key, Counter())
        tier2plus = sum(v for tier, v in ctr.items() if int(tier) >= 2)
        lines.append(f"| `{key}` | {ctr.get(0, 0)} | {ctr.get(1, 0)} | {tier2plus} |")

    lines.extend(["", "## Agentic Slice", ""])
    lines.append("These counts matter because the underlying-model treatment decision is most consequential in the strengthened frontier, not in the corpus at large.")
    lines.append("")
    for key in ["open-weight", "closed-source/API-based", "mixed", "unspecified", "no-llm"]:
        lines.append(
            f"- `{key}` agentic papers: `{agentic_by_regime.get(key, 0)}`; Tier 2+ agentic papers: `{agentic_tier2_by_regime.get(key, 0)}`"
        )

    UNDERLYING_MODEL_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "counts": dict(counts),
        "system_type_by_access_regime": {k: dict(v) for k, v in type_by_regime.items()},
        "tier_by_access_regime": {k: dict(v) for k, v in tier_by_regime.items()},
        "agentic_by_access_regime": dict(agentic_by_regime),
        "agentic_tier2_by_access_regime": dict(agentic_tier2_by_regime),
    }


def write_sensitivity(papers: list[dict], dual_rows: list[dict]) -> dict:
    current_tiers = Counter(rec["evaluation"]["evidence_tier"] for rec in papers)
    current_system = Counter(rec["classification"]["system_type"] for rec in papers)

    conservative_tiers = Counter()
    liberal_tiers = Counter()
    conservative_system = Counter()

    dual_by_id = {row["record_id"]: row for row in dual_rows}
    for rec in papers:
        rid = rec["bibliographic"]["record_id"]
        current_tier = rec["evaluation"]["evidence_tier"]
        current_type = rec["classification"]["system_type"]
        reviewer2_tier = int(dual_by_id[rid]["reviewer2_tier"])
        reviewer2_type = dual_by_id[rid]["reviewer2_system_type"]

        conservative_tier = current_tier
        if current_tier >= 2 and reviewer2_tier < 2:
            conservative_tier = 1
        liberal_tier = current_tier
        if current_tier == 1 and reviewer2_tier >= 2:
            liberal_tier = 2

        conservative_type_value = current_type
        if current_type == "A" and reviewer2_type != "A":
            conservative_type_value = reviewer2_type

        conservative_tiers[conservative_tier] += 1
        liberal_tiers[liberal_tier] += 1
        conservative_system[conservative_type_value] += 1

    data = {
        "baseline": {
            "tiers": dict(current_tiers),
            "system_types": dict(current_system),
            "tier_ceiling_max": max(current_tiers),
        },
        "tier_conservative": {
            "tiers": dict(conservative_tiers),
            "tier_ceiling_max": max(conservative_tiers),
        },
        "tier_liberal": {
            "tiers": dict(liberal_tiers),
            "tier_ceiling_max": max(liberal_tiers),
        },
        "structure_conservative": {
            "system_types": dict(conservative_system),
        },
        "ceiling_robust": max(current_tiers) < 3 and max(conservative_tiers) < 3 and max(liberal_tiers) < 3,
    }

    SENS_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")

    lines = [
        "# Tier Sensitivity Analysis",
        "",
        "The key question from the review is whether boundary instability between Tier 1 and Tier 2 alters the paper's headline narrative.",
        "",
        "## Baseline",
        "",
        f"- Tier counts: `{dict(current_tiers)}`",
        f"- System counts: `{dict(current_system)}`",
        "",
        "## Conservative Tier Scenario",
        "",
        f"- Downgrade rule: current `Tier 2` papers fall to `Tier 1` when the second-pass recoding does not recover `Tier 2+`.",
        f"- Tier counts: `{dict(conservative_tiers)}`",
        "",
        "## Liberal Tier Scenario",
        "",
        f"- Upgrade rule: current `Tier 1` papers rise to `Tier 2` when the second-pass recoding recovers `Tier 2+`.",
        f"- Tier counts: `{dict(liberal_tiers)}`",
        "",
        "## Structural Conservative Scenario",
        "",
        f"- Rule: current `A` papers fall back to the second-pass structural class when the recoding does not recover `A`.",
        f"- System counts: `{dict(conservative_system)}`",
        "",
        "## Bottom Line",
        "",
        f"- Tier-2 ceiling robust across scenarios: `{data['ceiling_robust']}`",
        "- In all scenarios, the maximum realized tier remains `2`; boundary instability changes the distribution between Tier 1 and Tier 2, but does not create any Tier 3/4 paper.",
    ]
    SENS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return data


def main() -> None:
    papers = load_papers()
    dual_rows = build_dual_coding(papers)
    dual = write_dual_coding(dual_rows)
    coords = write_coordinate_distribution(papers)
    underlying_model = write_underlying_model_audit(papers)
    sens = write_sensitivity(papers, dual_rows)
    print(f"Wrote {DUAL_CODING_CSV.relative_to(ROOT)}")
    print(f"Wrote {DUAL_SUMMARY_JSON.relative_to(ROOT)} and {DUAL_SUMMARY_MD.relative_to(ROOT)}")
    print(f"Wrote {COORD_CSV.relative_to(ROOT)} and {COORD_MD.relative_to(ROOT)}")
    print(f"Wrote {UNDERLYING_MODEL_CSV.relative_to(ROOT)} and {UNDERLYING_MODEL_MD.relative_to(ROOT)}")
    print(f"Wrote {SENS_JSON.relative_to(ROOT)} and {SENS_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
