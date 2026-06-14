# Release Checklist

Use this checklist before turning `paper_repo/` into a standalone branch or repository.

- Promote the contents of `paper_repo/` to repository root.
- Confirm `README.md` and `SUPPLEMENT.md` render correctly on GitHub.
- Confirm `results/master_selection_table.csv` shows `pending = 0`.
- Confirm the corpus snapshot named in the manuscript matches the counts in `papers.json`.
- Confirm any legacy-freeze artifacts are clearly labeled as legacy provenance or replaced by refreshed freeze artifacts.
- Confirm `results/master_table_appendix.tex` does not contain excluded records such as `A057`.
- Confirm the manuscript no longer points to a placeholder GitHub URL.
- Confirm the branch contains only paper data, scripts, and supplement artifacts, not the working LaTeX environment.
