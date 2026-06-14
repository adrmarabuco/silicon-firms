#!/usr/bin/env python3
"""
Export the paper's public supplement package into `paper_repo/`.

The exported package contains the corpus data, audit artifacts, and regeneration
scripts that support the published paper, while keeping the working LaTeX and
revision environment outside the public artifact repository.
"""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper_repo"

FILES_TO_COPY = [
    "papers.json",
    "search.md",
    "data/selection.csv",
    "data/decisions/protocol.md",
    "data/decisions/direct_import_log.csv",
    "data/decisions/exclusion_log.csv",
    "data/decisions/snowballing_log.forward-2026-03-15.round-6.csv",
    "data/decisions/dual_coding_audit.csv",
    "results/master_selection_table.csv",
    "results/master_selection_summary.md",
    "results/master_table_appendix.tex",
    "results/formal_spine_analysis.json",
    "results/formal_spine_analysis.md",
    "results/agreement_proxy_analysis.json",
    "results/agreement_proxy_analysis.md",
    "results/dual_coding_summary.json",
    "results/dual_coding_summary.md",
    "results/evidence_coordinate_distribution.csv",
    "results/evidence_coordinate_distribution.md",
    "results/underlying_model_release_type_audit.csv",
    "results/underlying_model_release_type_audit.md",
    "results/underlying_model_layer_frontier_audit.csv",
    "results/underlying_model_layer_frontier_audit.md",
    "results/underlying_model_layer_analysis.md",
    "results/underlying_model_reporting_protocol.md",
    "results/organizational_failure_modes.md",
    "results/research_agenda_experiments.md",
    "results/tier_sensitivity_analysis.json",
    "results/tier_sensitivity_analysis.md",
    "scripts/build_master_selection_table.py",
    "scripts/finalize_snowball_round6.py",
    "scripts/build_revision_audit.py",
    "scripts/build_underlying_model_frontier_audit.py",
    "scripts/build_underlying_model_layer_analysis.py",
    "scripts/build_master_table_appendix.py",
    "scripts/formal_spine_analysis.py",
    "scripts/agreement_proxy_analysis.py",
    "scripts/export_paper_repo_snapshot.py",
]


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_file(rel_path: str) -> None:
    src = ROOT / rel_path
    dst = OUT / rel_path
    ensure_parent(dst)
    shutil.copy2(src, dst)


def write_text(rel_path: str, text: str) -> None:
    dst = OUT / rel_path
    ensure_parent(dst)
    dst.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    copied = []
    for rel_path in FILES_TO_COPY:
        copy_file(rel_path)
        copied.append(rel_path)

    manifest = {
        "release_date": str(date.today()),
        "purpose": "public supplement and reproducibility package for the paper",
        "repository_name": "silicon-firms",
        "copied_files": copied,
        "notes": [
            "This package intentionally excludes the working LaTeX manuscript files.",
            "The package preserves reproducible data, screening logs, audit artifacts, and the scripts that regenerate them.",
        ],
    }

    write_text(
        "README.md",
        """# Silicon Firms

Public supplement and reproducibility package for the paper on agentic and tool-assisted LLM trading systems.

This repository contains the data, audit artifacts, and regeneration scripts needed to inspect the paper's corpus construction, system classifications, evidence tiers, and supporting analyses. It is intentionally narrower than the private writing and revision workspace: the goal here is to make the paper's empirical basis inspectable, not to expose every draft, note, PDF, or internal planning file.

## What is included

- corpus metadata in `papers.json`
- search and screening records under `data/`
- generated audit outputs under `results/`
- scripts used to regenerate the public tables and analyses under `scripts/`
- supplement navigation in `SUPPLEMENT.md` and `supplement/README.md`

## What is intentionally excluded

- the working LaTeX manuscript environment
- private review notes, chats, and planning documents
- source PDFs that cannot be redistributed cleanly
- temporary build files and exploratory artifacts

## How to read this repository

Start with:

- `SUPPLEMENT.md` for the audit-bundle map
- `papers.json` for the corpus-level metadata
- `results/master_table_appendix.tex` for the paper-level classification crosswalk
- `results/evidence_coordinate_distribution.md` for evidence-coordinate counts
- `results/tier_sensitivity_analysis.md` for tier sensitivity
- `results/underlying_model_reporting_protocol.md` for the underlying-model reporting protocol

## Reproducibility

The scripts in `scripts/` are included to document and regenerate the main public artifacts. They assume the repository layout preserved here.

## Citation

If you use this repository, cite the accompanying paper and refer to this repository as its public supplement.
""",
    )

    write_text(
        "SUPPLEMENT.md",
        """# Supplementary Audit Bundle

This repository is the public supplementary audit bundle for the paper.

## What a reviewer should find here

- the corpus metadata used by the paper
- the reconciled selection ledger
- the snowballing and direct-import decision logs
- the direct-import reconciliation log
- the exclusion log
- the second-pass recoding audit
- the evidence-coordinate and sensitivity outputs
- the appendix master table
- the scripts required to regenerate those artifacts

## Audit Map

- `papers.json`: corpus metadata and coding fields.
- `data/selection.csv`: selection sheet.
- `data/decisions/`: protocol, direct-import, exclusion, snowballing, and recoding logs.
- `results/master_selection_table.csv`: reconciled selection table.
- `results/master_table_appendix.tex`: appendix-ready paper-level crosswalk.
- `results/evidence_coordinate_distribution.md`: evidence-coordinate distribution.
- `results/tier_sensitivity_analysis.md`: tier robustness checks.
- `results/underlying_model_*`: underlying-model reporting and release-type analyses.
- `results/organizational_failure_modes.md`: organizational failure-mode synthesis.
- `results/research_agenda_experiments.md`: falsifiable research agenda.

## Scope Boundary

This repository supports the paper's corpus and audit trail. It does not include the private writing workspace, reviewer-response planning files, or redistributable copies of all source PDFs.
""",
    )

    write_text(
        "RELEASE_CHECKLIST.md",
        """# Public Package Checklist

Use this checklist before each public update.

- Confirm `README.md` and `SUPPLEMENT.md` render correctly on GitHub.
- Confirm `results/master_selection_table.csv` shows `pending = 0`.
- Confirm the corpus snapshot named in the manuscript matches the counts in `papers.json`.
- Confirm `results/master_table_appendix.tex` does not contain excluded records such as `A057`.
- Confirm the repository contains only paper data, scripts, and supplement artifacts, not the private writing workspace.
- Confirm the public repository remains synchronized with the approved supplement package.
""",
    )

    write_text(
        "STRUCTURE.md",
        """# Package Structure

- `data/`
  - corpus selection records and preserved selection decisions
- `results/`
  - generated audit outputs used in the paper and supplement
- `scripts/`
  - scripts required to rebuild the selection and evidence artifacts
- `supplement/`
  - compact guide to the audit bundle

## Separation policy

This repository is the public supplement and reproducibility package. It excludes the private manuscript-drafting environment, exploratory notes, and temporary build files.
""",
    )

    write_text(
        "STATE_OF_SNAPSHOT.md",
        """# Release State

This repository is the public supplementary artifact package for the paper.

## Current Contents

- corpus metadata and selection records
- decision logs for direct import, exclusion, snowballing, and recoding
- generated evidence, sensitivity, underlying-model, and organizational analyses
- scripts used to regenerate the public audit artifacts

## Maintenance Rule

Updates should be made through a controlled refresh from the private working repository so the public package stays synchronized with the manuscript and does not accumulate unrelated drafting artifacts.
""",
    )

    write_text(
        "manuscript/README.md",
        """# Manuscript Separation

The working LaTeX manuscript is intentionally not included in this repository.

Rationale:

- avoid coupling the paper supplement repository to the draft-writing environment
- keep this repository focused on reproducibility artifacts
- avoid exposing private review notes, temporary builds, and drafting history
""",
    )

    write_text(
        "supplement/README.md",
        """# Supplement Guide

This directory points to the core files in the public audit bundle:

- selection protocol
- reconciled master selection table
- snowballing log
- exclusion log
- second-pass coding audit
- evidence coordinate distribution
- underlying-model release-type audit
- tier sensitivity analysis
- appendix master table

The top-level `SUPPLEMENT.md` provides the full map.
""",
    )

    write_text("MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote public supplement package to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
