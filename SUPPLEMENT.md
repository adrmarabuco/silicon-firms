# Supplementary Audit Bundle

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
