# Master Selection Table Summary

- Generated from `data/selection.csv`, `data/decisions/direct_import_log.csv`, `data/decisions/snowballing_log.forward-2026-03-15.round-6.csv`, and `papers.json`.
- Unique candidate rows after reconciliation: `440`.
- Final included studies linked to `papers.json`: `66`.
- Pending screened candidates: `0`.
- Excluded screened candidates: `373`.
- Snowball `include` decisions not yet linked to the final corpus snapshot: `0`.

## Reconciliation Status Counts

- `included_reconciled_both`: `2`
- `included_reconciled_direct_import`: `3`
- `included_reconciled_seeded_search`: `17`
- `included_reconciled_snowballing`: `44`
- `screened_duplicate_version`: `1`
- `screened_excluded`: `373`

## Primary Pathway Counts

- `direct_import`: `3`
- `seeded_search`: `17`
- `seeded_search+snowballing`: `2`
- `snowballing`: `418`

## Notes

- `included_unreconciled_in_snapshot` means the paper exists in `papers.json`, but this repository snapshot does not yet preserve a matching search or snowballing event for it.
- `screened_include_not_imported` usually indicates a duplicate, a related version, or a candidate marked `include` in the snowballing snapshot without a direct final linkage.
- This table is audit-oriented: it favors preserving provenance over forcing a cleaner but less defensible PRISMA count.
