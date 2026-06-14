# Survey Protocol

## 0) Methodological Positioning
This review uses a **PRISMA-informed systematic review protocol**.

That means the paper intentionally adopts the strengths associated with PRISMA-style rigor:

- explicit search logic
- documented screening stages
- traceable inclusion and exclusion decisions
- frozen selection counts tied to a reproducible ledger

At the same time, the paper does **not** depend on claiming strict literal PRISMA compliance in every formal sense.

The intended methodological stance is:

- systematic
- auditable
- protocol-driven
- PRISMA-style in rigor
- not fragilely dependent on whether every historical workflow element maps one-to-one onto formal PRISMA reporting conventions

This is an affirmative design choice, not an apology.
The review uses PRISMA as a model for rigor and traceability while remaining faithful to the actual research object and workflow of this project.

## 1) Research Goal and Contribution
This review maps the literature on LLM-enabled trading systems through two orthogonal lenses: structural system type and strength of empirical validation. The scope wedge versus broader "LLMs in finance" surveys is deliberate: we focus on systems that contribute directly to trading, portfolio construction, execution-facing environments, tool-mediated financial workflows, or governance/control infrastructure that materially shapes how such systems are built and evaluated.

The ambition is not to be a broad review of AI in finance.
The ambition is to be especially strong and defensible on the literature of **agentic and tool-assisted trading systems**.

## 2) Operational Definitions
- **Agentic (A)**: the paper describes an implemented feedback-bearing loop involving evaluation/environment feedback that revises later planning or action.
- **Tool-assisted (T)**: the paper has explicit tool, retrieval, checker, planner, or orchestration interfaces with financial-task linkage, but no explicit adaptive evaluator loop.
- **Non-agentic (N)**: feedforward prediction, optimization, or analysis systems without explicit tool-mediated control or adaptive feedback loops.
- Promotion is based on implemented structure, not vocabulary such as "agentic", "planner", or "multi-agent" alone.

## 3) Research Questions
- How do papers intervene across the trading stack: signal, portfolio, execution, and monitoring/governance?
- Which structural families recur once papers are mapped as constrained system graphs?
- How strong is the evidence base once architecture is separated from evaluation rigor?
- Where do governance, security, and market-integrity concerns enter the literature?
- What remains missing for deployment-credible validation beyond Tier 2?

## 4) Eligibility Criteria
### Inclusion
A paper is in scope if it makes a direct contribution to at least one of the following:
- LLM/foundation-model trading or portfolio decision systems
- financial tool-use agents or benchmark environments that directly support trading/system evaluation
- factor, signal, or code-generation systems that materially change a trading pipeline
- governance/control substrates that directly constrain financial-agent behavior

### Exclusion
A paper is excluded if it is primarily:
- a generic survey, review, or bibliometric study
- a non-finance AI/agent paper
- a finance paper without direct LLM/foundation-model relevance
- a finance/LLM paper without direct contribution to trading systems, portfolio systems, execution, or directly enabling benchmarks/infrastructure
- a broken link, non-paper web artifact, or duplicate version of an included work
- a broader AI-finance paper that does not materially strengthen the core object of the review: agentic trading

### Edge-case Rules
- Enabling infrastructure papers may be included even without direct alpha claims if they materially shape evaluation, orchestration, or governance for financial agents.
- Adjacent RL/AutoML/proprietary systems are discussed as context or limitations, but are not admitted into the main corpus unless they satisfy the same direct LLM/trading-system contribution rule.
- The submission freeze is conservative: potentially relevant late-stage snowballed candidates are excluded unless they were fully audited and extracted.
- Scope discipline is intentional: stronger depth inside agentic trading is preferred over broader but weaker AI-finance coverage.

## 5) Information Sources and Search Strategy
- Primary sources: arXiv, SSRN, IEEE Xplore, ACM Digital Library, SpringerLink, and ScienceDirect/Elsevier.
- Complementary discovery: manual venue sweeps (major ML/NLP and finance/FinNLP venues) plus backward and forward snowballing.
- Time window: 2018-present.
- Query logic: pair LLM/foundation-model/agent/tool-use terminology with trading/portfolio/quantitative-investment terminology.
- The structured seeded-search sheet is preserved in `data/selection.csv`; the latest frozen snowballing log is `data/decisions/snowballing_log.forward-2026-03-15.round-6.csv`.
- Direct imports discovered outside preserved intake logs are reconciled through `data/decisions/direct_import_log.csv`.
- The focused frontier-strengthening strategy is governed by `planning/frontier-search-strategy.md`.

## 6) Screening Process
- Pass 1: title/abstract or title/metadata screening.
- Pass 2: full-text eligibility and structured extraction for admitted papers.
- Current frozen audit snapshot: 440 reconciled candidate rows, 66 included studies, 373 excluded candidates, 1 duplicate published version, and 0 pending items.
- Unresolved snowballed items were closed in round 6 at title/metadata level using explicit contribution-based exclusion rules rather than left pending.
- Exclusions are logged in `data/decisions/exclusion_log.csv`.

## 7) Data Extraction Schema
Each included paper is represented as a structured JSON record in `papers.json`, with fields for:
- bibliographic identity
- structural class (`N/T/A`)
- trading-pipeline stages and agent roles
- underlying-model layer, when recoverable, including:
  - model family
  - underlying-model release type
  - allocation pattern across roles
  - model-sensitivity evidence
  - specification quality
- architecture/tool/environment notes
- market setting and data sources
- evidence tier and supporting evaluation details
- quality-rubric dimensions
- synthesis notes for narrative use

## 8) Evidence Grading and Quality Assessment
- Evidence tiers follow the `0-4` policy in `skills/phd-advisor-agentic-trading-survey/references/evidence-grading.md`.
- The paper reports two parallel dimensions:
  - evidence dimension: `z_i = (o_i,b_i,f_i,x_i,g_i)`
  - underlying-model dimension: `m_i = (r_i,a_i,s_i,q_i)` when recoverable
- Tiering is conservative: missing critical realism or temporal details trigger downgrade.
- The April 2026 revision adds a second-pass recoding and adjudication artifact, replacing the earlier reliance on proxy-only stability reporting.
- The `m_i` layer is interpretive and normative in this revision; it qualifies interpretation but does not directly change the evidence tier.

## 9) Synthesis Plan
- Narrative structure: corpus/audit trail -> formal taxonomy -> computational archetypes -> evidence lens -> governance/integrity -> agenda.
- Quantitative claims must always be tied to tier context.
- Underlying models are treated as a descriptive-analytical layer, not as a model leaderboard.
- The paper may use underlying-model release type to qualify reproducibility and deployment opacity, but it should not collapse the whole model layer into release type alone.
- The paper will make interpretive and normative claims about the underlying-model layer:
  - interpretive in findings and limitations
  - normative in the reporting protocol and future agenda
- Role-decomposed systems should not be overclaimed from a thin subcorpus; interpretation should first be strengthened through targeted frontier expansion and then through failure-mode analysis.
- Broader adjacent literatures and proprietary systems are discussed as coverage boundaries, not silently mixed into the core corpus.

## 10) Reproducibility Artifacts
The submission freeze should preserve at least the following:
- this protocol
- `search.md` and Appendix-B search strings
- `results/master_selection_table.csv`
- `data/decisions/direct_import_log.csv`
- frozen snowballing round log(s)
- exclusion log
- second-pass recoding/adjudication sheet
- coordinate/tier sensitivity outputs
- appendix master table and paper-level summaries
- public supplement and reproducibility package

## 11) Submission-Freeze Policy
- The corpus is frozen only when `pending = 0` in the reconciled selection table.
- Numerical claims in the manuscript must be derived from the frozen ledger and `papers.json`, not manually maintained.
- Late candidate papers discovered after freeze may be tracked separately but are not admitted without full extraction and adjudicated coding.
