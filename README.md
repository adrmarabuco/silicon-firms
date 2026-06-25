# Silicon Firms

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
