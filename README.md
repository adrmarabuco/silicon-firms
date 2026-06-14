# Paper Repo Snapshot

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
