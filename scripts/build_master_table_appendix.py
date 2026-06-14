#!/usr/bin/env python3
"""
Generate the LaTeX appendix table used to audit the frozen corpus.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from formal_spine_analysis import ARCHETYPE_DISPLAY, assign_archetype


ROOT = Path(__file__).resolve().parents[1]
PAPERS_JSON = ROOT / "papers.json"
OUTPUT_TEX = ROOT / "results" / "master_table_appendix.tex"

APPENDIX_ARCHETYPE_DISPLAY = {
    "Context-to-decision": "Context-decision",
    "Evaluator-coupled artifact search": "Artifact search",
    "Role-decomposed organizations": "Role-decomposed",
    "Environment and governance substrate": "Substrate",
}


def latex_escape(text: str | None) -> str:
    text = str(text or "")
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def short_title(title: str, limit: int = 78) -> str:
    title = " ".join((title or "").split())
    if len(title) <= limit:
        return title
    return title[: limit - 3].rstrip() + "..."


def citation_stub(authors: str | None, year: str | int | None) -> str:
    authors = (authors or "").strip()
    year_str = str(year or "n.d.")
    if not authors:
        return year_str

    first = authors
    if ";" in first:
        first = first.split(";", 1)[0].strip()
    elif " and " in first:
        first = first.split(" and ", 1)[0].strip()
    elif ", " in first and not re.match(r"^[A-Z][a-z-]+,\s*[A-Z]\.?$", first):
        first = first.split(", ", 1)[0].strip()

    if "," in first:
        surname = first.split(",", 1)[0].strip()
    else:
        surname = first.split()[-1].strip()

    multi_author = any(sep in authors for sep in [";", " and ", ", "]) and authors.strip() != first
    return f"{surname} et al. ({year_str})" if multi_author else f"{surname} ({year_str})"


def evidence_signature(rec: dict) -> str:
    qr = rec["quality_rubric"]
    gov = rec.get("governance_integrity", {}) or {}
    values = [
        int(int(qr["temporal_validity"]["score"]) >= 1),
        int(int(qr["baseline_strength"]["score"]) >= 1),
        int(int(qr["realism"]["score"]) >= 1),
        int(int(qr["execution_feasibility"]["score"]) >= 1),
        int(any(gov.get(key) not in (None, "", []) for key in ["security_controls", "audit_logging", "market_integrity_risks"])),
    ]
    return "".join(str(v) for v in values)


def underlying_model_label(rec: dict) -> str:
    text = (rec["architecture"].get("model_stack") or "").lower()
    title = (rec["bibliographic"].get("title") or "").lower()

    if not text or text == "none":
        if any(word in title for word in ["survey", "benchmark", "platform", "environment"]):
            return "---"
        return "---"

    mapping = [
        ("GPT-4o-mini+o1", ["gpt-4o-mini", "o1"]),
        ("GPT-4/4o/o1", ["gpt-4"]),
        ("GPT-4/4o/o1", ["gpt-4o"]),
        ("GPT-4/4o/o1", ["o1"]),
        ("ChatGPT-4", ["chatgpt 4"]),
        ("GPT-3.5/4o/LLaMA", ["gpt-3.5", "gpt-4o", "llama"]),
        ("FinBERT+DDPG", ["finbert", "ddpg"]),
        ("LLaMA-2+FinBERT", ["llama 2", "finbert"]),
        ("Qwen2-72B (SFT)", ["qwen2-72b"]),
        ("CFGPT-7B", ["cfgpt"]),
        ("FinVis-GPT (MM)", ["finvis-gpt"]),
        ("BloombergGPT", ["bloomberggpt"]),
        ("BLOOM-176B", ["bloom-176b"]),
        ("BBT-FinT5", ["bbt-fin"]),
        ("Mistral-7B (SFT)", ["mistral-7b"]),
        ("FinBERT", ["finbert"]),
        ("Chronos (DL)", ["chronos"]),
        ("FT transformer", ["transformer"]),
        ("Distilled ens.", ["distillation"]),
        ("Custom FM", ["foundation model"]),
        ("MM LLM (n.s.)", ["multimodal llm"]),
    ]
    for label, needles in mapping:
        if all(needle in text for needle in needles):
            return label

    if sum(token in text for token in ["gpt", "claude", "qwen", "llama", "gemini", "deepseek"]) >= 3:
        return "Multi-LLM"
    if "llm" in text or "gpt" in text or "llama" in text or "qwen" in text or "claude" in text:
        return "LLM (n.s.)"
    return "n.s."


def main() -> None:
    papers = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    papers.sort(key=lambda rec: rec["bibliographic"]["record_id"])

    lines = [
        r"\begingroup",
        r"\scriptsize",
        r"\setlength{\LTleft}{0pt}",
        r"\setlength{\LTright}{0pt}",
        r"\begin{longtable}{p{0.7cm} p{1.9cm} p{3.85cm} p{1.7cm} p{0.65cm} p{0.55cm} p{1.2cm} p{1.8cm} p{2.0cm}}",
        r"\caption{Corpus master table used in the survey. The table maps internal record IDs to a citation stub, computational archetype, N/T/A system type, evidence tier, a compact evidence signature, primary underlying model, and pipeline stages so that numerical claims in the main text can be audited directly. The evidence signature is ordered as $(o,b,f,x,g)$: temporal/out-of-sample discipline, baseline strength, friction or cost realism, execution realism, and governance or integrity evidence. Underlying model: ``n.s.'' = not specified; ``---'' = no explicit LLM underlying model or infrastructure-only item.}\label{tab:master-corpus}\\",
        r"\toprule",
        r"\textbf{ID} & \textbf{Citation} & \textbf{Paper} & \textbf{Archetype} & \textbf{Type} & \textbf{Tier} & \textbf{$z_i$} & \textbf{Underlying model} & \textbf{Stages} \\",
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        r"\textbf{ID} & \textbf{Citation} & \textbf{Paper} & \textbf{Archetype} & \textbf{Type} & \textbf{Tier} & \textbf{$z_i$} & \textbf{Underlying model} & \textbf{Stages} \\",
        r"\midrule",
        r"\endhead",
        r"\midrule",
        r"\multicolumn{9}{r}{\emph{Continued on next page}}\\",
        r"\midrule",
        r"\endfoot",
        r"\bottomrule",
        r"\endlastfoot",
    ]

    for rec in papers:
        bib = rec["bibliographic"]
        citation = citation_stub(bib.get("authors"), bib.get("year"))
        archetype = APPENDIX_ARCHETYPE_DISPLAY[ARCHETYPE_DISPLAY[assign_archetype(bib.get("record_id", ""))]]
        row = " & ".join(
            [
                latex_escape(bib.get("record_id")),
                latex_escape(citation),
                latex_escape(short_title(bib.get("title", ""))),
                latex_escape(archetype),
                latex_escape(rec["classification"].get("system_type", "")),
                latex_escape(str(rec["evaluation"].get("evidence_tier", ""))),
                latex_escape(evidence_signature(rec)),
                latex_escape(underlying_model_label(rec)),
                latex_escape(", ".join(rec["trading_pipeline"].get("stages", []))),
            ]
        )
        lines.append(row + r" \\")

    lines.extend([r"\end{longtable}", r"\endgroup"])
    OUTPUT_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_TEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
