# Supplementary Audit Bundle

This repository is the public supplementary audit bundle for the paper.

## What a reviewer should find here

- the corpus metadata used by the paper
- the reconciled selection ledger
- the snowballing and direct-import decision logs
- the direct-import reconciliation log
- the exclusion log
- the second-pass recoding audit
- the independent second evaluation of predefined borderline cases
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
- `second_evaluation/`: independent second-evaluation artifacts for predefined borderline cases.
- `results/organizational_failure_modes.md`: organizational failure-mode synthesis.
- `results/research_agenda_experiments.md`: falsifiable research agenda.

## Scope Boundary

This repository supports the paper's corpus and audit trail. It does not include the private writing workspace, reviewer-response planning files, or redistributable copies of all source PDFs.
