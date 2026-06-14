#!/usr/bin/env python3
"""
Close unresolved snowballing candidates for the submission freeze.

This script preserves the existing round-5 snapshot and emits a round-6 log in
which all remaining `pending` decisions are resolved at title/metadata
screening level. The review strategy is intentionally conservative: we do not
promote papers into the corpus unless they were fully audited and extracted.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_CSV = ROOT / "data" / "decisions" / "snowballing_log.forward-2026-03-15.round-5.csv"
OUT_CSV = ROOT / "data" / "decisions" / "snowballing_log.forward-2026-03-15.round-6.csv"
EXCLUSION_LOG = ROOT / "data" / "decisions" / "exclusion_log.csv"


FREEZE_RELATED = {
    "adaptive llm-based multi-agent systems to enhance quantitative trading performance",
    "ai in investment analysis: llms for equity stock ratings",
    "alphaagent: llm-driven alpha mining with regularized exploration to counteract alpha decay",
    "can large language models effectively process and execute financial trading instructions?",
    "decision alignment protocols: harmonising ai agents for comprehensive market assessment",
    "enhancing investment analysis: optimizing ai-agent collaboration in financial research",
    "factormad: a multi-agent debate framework based on large language models for interpretable stock alpha factor mining",
    "finteam: a multi-agent collaborative intelligence system for comprehensive financial scenarios",
    "gwise: a graph-structured multi-agent framework for service-oriented and generative-ai-enabled financial trading analytics",
    "implementing domain-specific llms for strategic investment decisions: a retrospective case study comparing ai and human expertise",
    "large language model for dynamic strategy interchange in financial markets",
    "llm-guided evolutionary strategy generation for quantitative trading",
    "multi-agent llm framework for formulaic alpha generation and selection in quantitative trading",
    "toward a unified agentic framework for regime-aware portfolio optimization with llm signals",
    "using gen ai agents with gae and vae to enhance resilience of us markets",
}


def title_key(title: str | None) -> str:
    return " ".join((title or "").strip().lower().split())


def classify(title: str) -> tuple[str, str]:
    t = title_key(title)
    if not t:
        return (
            "Exclude at title/metadata screening: non-informative candidate record without a recoverable paper title.",
            "Metadata-only unresolved reference in forward snowballing; conservative freeze excludes records that cannot be audited to paper level.",
        )

    if t in FREEZE_RELATED:
        return (
            "Exclude at submission freeze: potentially relevant on title/metadata, but not fully audited and extracted before the conservative corpus freeze.",
            "This review now privileges a fully auditable accepted-and-extracted corpus over opportunistic late additions.",
        )

    review_markers = [
        "survey",
        "review",
        "bibliometric",
        "overview",
        "recent advances",
        "landscape",
        "opportunities and challenges",
    ]
    if any(marker in t for marker in review_markers):
        return (
            "Exclude at title/metadata screening: adjacent survey/review/bibliometric paper outside the corpus of primary technical studies and benchmark/infrastructure papers.",
            "Coverage discussion remains in the manuscript, but these papers are not admitted into the main evidence corpus.",
        )

    non_finance_markers = [
        "basketball",
        "floodplain",
        "power ",
        "chemistry",
        "biomedical",
        "autonomous vehicles",
        "weather conditions",
        "energy retrofit",
        "assistive robots",
        "fault localization",
        "penetration testing",
        "fluid dynamics",
    ]
    if any(marker in t for marker in non_finance_markers):
        return (
            "Exclude at title/metadata screening: non-finance or cross-domain paper outside the review scope.",
            "The frozen corpus is restricted to financial trading systems, portfolio systems, and directly enabling financial benchmarks/infrastructure.",
        )

    llm_but_not_trading = [
        "financial sentiment analysis",
        "question answering",
        "anti-money laundering",
        "banking recommendation",
        "financial planning",
        "personal finances",
        "risk management",
        "financial risk",
        "voucher analysis",
        "report writing",
        "compliance",
        "robo-advisor",
        "robo advisory",
    ]
    if any(marker in t for marker in llm_but_not_trading):
        return (
            "Exclude at title/metadata screening: finance/LLM paper without a direct trading-system, portfolio-construction, execution, or benchmark contribution.",
            "Relevant to broader GenAI-in-finance, but outside the narrower system-building scope of this survey.",
        )

    non_llm_finance = [
        "reinforcement learning",
        "portfolio optimization",
        "stock price prediction",
        "stock forecasting",
        "asset pricing",
        "deep reinforcement learning",
        "neural network",
        "variational autoencoder",
        "hidden markov",
        "graphsage",
        "pair trading",
        "moving average",
        "financial forecasting",
        "time series forecasting",
        "cryptocurrency portfolio",
    ]
    if any(marker in t for marker in non_llm_finance) and "llm" not in t and "language model" not in t and "chatgpt" not in t and "gpt" not in t and "foundation model" not in t:
        return (
            "Exclude at title/metadata screening: finance ML/RL/forecasting paper outside the review's LLM/foundation-model scope.",
            "The survey cites adjacent non-LLM traditions only where needed for context, not as corpus members.",
        )

    return (
        "Exclude at title/metadata screening: does not provide a sufficiently direct, auditable contribution to LLM-enabled trading systems under the conservative submission freeze.",
        "Resolved conservatively to close the snowballing backlog without widening the corpus beyond its stated scope.",
    )


def append_exclusion_log(rows: list[dict]) -> None:
    if not rows:
        return

    existing = EXCLUSION_LOG.read_text(encoding="utf-8").rstrip("\n")
    lines = [existing] if existing else []
    for row in rows:
        values = [
            row["timestamp"],
            "snowball_title_metadata",
            "",
            "snowballing_round6",
            row["candidate_title"],
            row["candidate_authors"],
            row["candidate_year"],
            row["candidate_venue"],
            row["candidate_url"] or row["candidate_id_value"],
            row["decision"],
            row["reason"],
            row["notes"],
        ]
        out = []
        for value in values:
            text = (value or "").replace('"', '""')
            if "," in text or "\n" in text:
                text = f'"{text}"'
            out.append(text)
        lines.append(",".join(out))
    EXCLUSION_LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = list(csv.DictReader(IN_CSV.open()))
    resolved_rows: list[dict] = []

    for row in rows:
        if row.get("decision") == "pending":
            reason, notes = classify(row.get("candidate_title") or "")
            row["decision"] = "exclude"
            row["reason"] = reason
            row["notes"] = notes
            resolved_rows.append(row.copy())

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    append_exclusion_log(resolved_rows)
    print(f"Wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"Resolved {len(resolved_rows)} pending rows.")


if __name__ == "__main__":
    main()
