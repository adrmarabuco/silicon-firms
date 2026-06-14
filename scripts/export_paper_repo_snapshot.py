#!/usr/bin/env python3
"""
Export a publication-oriented snapshot into `paper_repo/`.

This staging area is designed for a future branch or repository split that
contains the paper's data, scripts, and supplementary audit artifacts without
mixing them with the working LaTeX environment of the broader survey repo.
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
        "snapshot_date": str(date.today()),
        "purpose": "staging area for future paper-only branch/repository split",
        "root": "paper_repo",
        "copied_files": copied,
        "notes": [
            "This package intentionally excludes the working LaTeX manuscript files.",
            "The goal is to preserve reproducible data, screening logs, audit artifacts, and the scripts that regenerate them.",
        ],
    }

    write_text(
        "README.md",
        """# Paper Repo Snapshot

This directory is a staging area for a future branch or repository split that will host the paper's reproducible assets without mixing them with the working LaTeX environment of the broader survey repository.

When promoted to the root of its own branch or repository, this README is intended to become the landing page referenced by the manuscript's supplementary-material statement. In other words: the future GitHub branch should resolve the old placeholder-link criticism by making this package itself the public supplement destination.

## What is included

- frozen corpus data
- search and screening logs
- methodological audit artifacts
- regeneration scripts for the selection and evidence analyses

## Important current state

This package is still a staging export.

At the moment, the repository contains:

- an active strengthened corpus that has moved beyond the older 66-paper freeze
- preserved legacy-freeze provenance artifacts that still document the earlier reconciled snapshot

That split is currently intentional and should remain explicit until the next manuscript freeze reconciles them into one release-ready snapshot.

## What is intentionally excluded

- `main.tex` and the surrounding manuscript build environment
- exploratory notes that are not part of the reproducible audit trail
- historical working artifacts that are useful for development but not for the paper package

## Recommended split workflow

1. Create a clean branch for the paper package export.
2. Promote the contents of `paper_repo/` to the repository root of that branch.
3. Keep manuscript sources in a separate fork or companion repository.
4. Treat the files under `data/`, `results/`, and `scripts/` here as the frozen supplementary core for the paper.
""",
    )

    write_text(
        "SUPPLEMENT.md",
        """# Supplementary Audit Bundle

This package is the intended public supplement target for the paper revision.

## What a reviewer should find here

- the frozen corpus snapshot used in the manuscript
- the reconciled selection ledger with `pending = 0`
- the preserved snowballing freeze log
- the direct-import reconciliation log
- the exclusion log
- the second-pass recoding audit
- the evidence-coordinate and sensitivity outputs
- the appendix master table
- the scripts required to regenerate those artifacts

## Why this exists

One review criticism was that the GitHub reference in the manuscript behaved like a placeholder rather than a real supplementary package. The future paper-only branch/repository should therefore expose this file and the surrounding structure directly, so the manuscript points to an actual audit bundle rather than to an unfinished location.

## Snapshot honesty rule

Do not publish this staging package as if every artifact already belongs to a single refreshed manuscript freeze.

Until the next explicit freeze, the package may contain:

- active strengthened-corpus artifacts
- preserved legacy-freeze provenance artifacts

That is acceptable in staging.
It is not acceptable to present that mixed state as a fully reconciled public supplement.

## Release rule

Do not publish the branch until the contents of `paper_repo/` have been promoted to repository root and this file is reachable as a first-class landing page.
""",
    )

    write_text(
        "RELEASE_CHECKLIST.md",
        """# Release Checklist

Use this checklist before turning `paper_repo/` into a standalone branch or repository.

- Promote the contents of `paper_repo/` to repository root.
- Confirm `README.md` and `SUPPLEMENT.md` render correctly on GitHub.
- Confirm `results/master_selection_table.csv` shows `pending = 0`.
- Confirm the corpus snapshot named in the manuscript matches the counts in `papers.json`.
- Confirm any legacy-freeze artifacts are clearly labeled as legacy provenance or replaced by refreshed freeze artifacts.
- Confirm `results/master_table_appendix.tex` does not contain excluded records such as `A057`.
- Confirm the manuscript no longer points to a placeholder GitHub URL.
- Confirm the branch contains only paper data, scripts, and supplement artifacts, not the working LaTeX environment.
""",
    )

    write_text(
        "STRUCTURE.md",
        """# Package Structure

- `data/`
  - corpus snapshot and preserved selection decisions
- `results/`
  - generated audit outputs used in the paper and supplement
- `scripts/`
  - scripts required to rebuild the selection and evidence artifacts

## Separation policy

This package is designed to stay close to a paper supplement / reproducibility repository.
The manuscript text can live elsewhere, but should cite the artifacts preserved here.

## Snapshot note

Until the next explicit freeze, some files here may document:

- the active strengthened corpus
- older preserved provenance freezes

That distinction should stay explicit rather than being flattened prematurely.
""",
    )

    write_text(
        "STATE_OF_SNAPSHOT.md",
        """# State of Snapshot

This export is a **staging package**, not yet the final public supplement.

## Why this note exists

The project is currently between:

- an older reconciled legacy freeze used for provenance and audit continuity
- a newer strengthened active corpus used for the next manuscript round

Those two states are both useful, but they should not be silently treated as identical.

## Current rule

- preserved legacy-freeze artifacts remain in the package for provenance
- active strengthened-corpus artifacts remain in the package for current analysis
- a future release-ready supplement should reconcile these into one clearly named manuscript freeze

## Publication rule

Do not present this package as a final supplement until the manuscript-facing freeze has been refreshed and the count lineage is fully aligned.
""",
    )

    write_text(
        "manuscript/README.md",
        """# Manuscript Separation

The working LaTeX manuscript is intentionally not copied into `paper_repo/`.

Rationale:

- avoid coupling the paper supplement repository to the draft-writing environment
- keep the future paper repository focused on reproducibility artifacts
- allow the manuscript to evolve in a separate branch or fork without polluting the audit package
""",
    )

    write_text(
        "supplement/README.md",
        """# Supplement Guide

This snapshot already contains the core files needed for an anonymized audit bundle:

- selection protocol
- reconciled master selection table
- frozen snowballing log
- exclusion log
- second-pass coding audit
- evidence coordinate distribution
- underlying-model release-type audit
- tier sensitivity analysis
- appendix master table

When the branch split happens, this directory can become the public-facing supplement landing page.
""",
    )

    write_text("MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote staged paper package to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
