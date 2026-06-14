#!/usr/bin/env python3
"""
Build conservative agreement/stability proxies for the survey labels.

This is not a substitute for dual independent annotation. The goal is to
quantify how stable the most important classification boundaries remain under a
second rule-based recoding that only uses structured extraction fields.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_JSON = ROOT / "papers.json"
OUT_JSON = ROOT / "results" / "agreement_proxy_analysis.json"
OUT_MD = ROOT / "results" / "agreement_proxy_analysis.md"


def load_papers() -> list[dict]:
    return json.loads(PAPERS_JSON.read_text())


def cohen_kappa_binary(true: list[int], pred: list[int]) -> float:
    n = len(true)
    po = sum(t == p for t, p in zip(true, pred)) / n
    c_true = Counter(true)
    c_pred = Counter(pred)
    pe = sum((c_true[c] / n) * (c_pred[c] / n) for c in [0, 1])
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def binary_metrics(true: list[int], pred: list[int]) -> dict:
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


def adaptive_loop_proxy(rec: dict) -> int:
    """Independent structural recoding for A vs non-A."""
    pattern = rec["architecture"].get("pattern") or ""
    roles = set(rec["trading_pipeline"].get("agent_roles") or [])
    tools = rec["architecture"].get("tools_invoked") or []
    environment = (rec["architecture"].get("environment") or "").lower()

    if "code/backtest agent" in roles and (
        "backtesting engine" in tools or "code execution" in tools
    ):
        return 1
    if pattern in {"planner-executor", "hierarchical", "multi-agent"} and (
        "guardrails" in roles or "allocator" in roles
    ) and ("backtest" in environment or "simul" in environment):
        return 1
    return 0


def tier2_proxy(rec: dict) -> int:
    """Independent evidence recoding for Tier 2+ vs Tier < 2."""
    qr = rec["quality_rubric"]
    has_eval = any(
        rec["evaluation"].get(key) not in (None, "", [])
        for key in ["key_metrics", "baselines", "robustness_tests"]
    )
    if not has_eval:
        return 0

    o_i = int(qr["temporal_validity"]["score"]) >= 2
    b_i = int(qr["baseline_strength"]["score"]) >= 1
    f_i = int(qr["realism"]["score"]) >= 1 and int(qr["execution_feasibility"]["score"]) >= 1
    return int(o_i and b_i and f_i)


def build() -> dict:
    papers = load_papers()

    true_a = [1 if rec["classification"]["system_type"] == "A" else 0 for rec in papers]
    pred_a = [adaptive_loop_proxy(rec) for rec in papers]
    a_metrics = binary_metrics(true_a, pred_a)
    a_mismatches = [
        {
            "record_id": rec["bibliographic"]["record_id"],
            "title": rec["bibliographic"]["title"],
            "assigned": rec["classification"]["system_type"],
            "proxy": "A" if pred else "non-A",
        }
        for rec, pred, truth in zip(papers, pred_a, true_a)
        if pred != truth
    ]

    true_t2 = [1 if rec["evaluation"]["evidence_tier"] >= 2 else 0 for rec in papers]
    pred_t2 = [tier2_proxy(rec) for rec in papers]
    t2_metrics = binary_metrics(true_t2, pred_t2)
    t2_mismatches = [
        {
            "record_id": rec["bibliographic"]["record_id"],
            "title": rec["bibliographic"]["title"],
            "assigned_tier": rec["evaluation"]["evidence_tier"],
            "proxy": "Tier2+" if pred else "Tier<2",
        }
        for rec, pred, truth in zip(papers, pred_t2, true_t2)
        if pred != truth
    ]

    return {
        "adaptive_boundary_proxy": {
            "task": "A vs non-A",
            "description": "Rule-based recoding from architecture pattern, agent roles, tool-use, and environment cues.",
            "metrics": a_metrics,
            "mismatches": a_mismatches,
        },
        "tier_boundary_proxy": {
            "task": "Tier2+ vs Tier<2",
            "description": "Rule-based recoding from quality-rubric coordinates only.",
            "metrics": t2_metrics,
            "mismatches": t2_mismatches,
        },
    }


def write_markdown(data: dict) -> None:
    a = data["adaptive_boundary_proxy"]
    t = data["tier_boundary_proxy"]
    lines = [
        "# Agreement Proxy Analysis",
        "",
        "These are rule-based stability proxies, not dual independent annotations.",
        "",
        "## Adaptive Boundary Proxy",
        "",
        f"- Task: `{a['task']}`",
        f"- Accuracy: `{a['metrics']['accuracy']:.3f}`",
        f"- Precision: `{a['metrics']['precision']:.3f}`",
        f"- Recall: `{a['metrics']['recall']:.3f}`",
        f"- Cohen's kappa: `{a['metrics']['kappa']:.3f}`",
        f"- Counts: `TP={a['metrics']['tp']}`, `TN={a['metrics']['tn']}`, `FP={a['metrics']['fp']}`, `FN={a['metrics']['fn']}`",
        "",
        "Mismatches:",
    ]
    for item in a["mismatches"]:
        lines.append(
            f"- `{item['record_id']}`: assigned `{item['assigned']}`, proxy `{item['proxy']}`"
        )

    lines.extend(
        [
            "",
            "## Tier Boundary Proxy",
            "",
            f"- Task: `{t['task']}`",
            f"- Accuracy: `{t['metrics']['accuracy']:.3f}`",
            f"- Precision: `{t['metrics']['precision']:.3f}`",
            f"- Recall: `{t['metrics']['recall']:.3f}`",
            f"- Cohen's kappa: `{t['metrics']['kappa']:.3f}`",
            f"- Counts: `TP={t['metrics']['tp']}`, `TN={t['metrics']['tn']}`, `FP={t['metrics']['fp']}`, `FN={t['metrics']['fn']}`",
            "",
            "Mismatches:",
        ]
    )
    for item in t["mismatches"]:
        lines.append(
            f"- `{item['record_id']}`: assigned `{item['assigned_tier']}`, proxy `{item['proxy']}`"
        )

    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> None:
    data = build()
    OUT_JSON.write_text(json.dumps(data, indent=2))
    write_markdown(data)
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
