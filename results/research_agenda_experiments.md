# Research Agenda: Falsifiable Experiments

## Purpose

This document upgrades the paper's future-work section into a concrete research program.

Each experiment is designed to test a weakness identified in the strengthened corpus, rather than offering generic suggestions.

---

## Experiment 1: Fine-Grained Tasks vs Coarse Role Prompts

**Hypothesis**

Fine-grained task decomposition improves risk-adjusted performance and interpretability relative to coarse role prompts in role-decomposed trading systems.

**Motivation from corpus**

- `A077` provides the strongest current signal that task granularity matters.
- `A024` and `A075` suggest that role design quality may matter more than raw agent count.

**Setup**

- Take one role-decomposed trading framework.
- Hold the underlying model, data, tools, and portfolio rules fixed.
- Compare:
  - coarse role prompts
  - fine-grained task prompts
  - fine-grained prompts plus explicit routing constraints

**Metrics**

- Sharpe, ARR, MDD
- turnover
- output consistency across runs
- intermediate-text alignment with downstream decisions

**Success criterion**

Fine-grained or routed variants beat coarse variants on Sharpe without worsening turnover and maintain more interpretable intermediate reasoning.

**Failure interpretation**

If performance does not improve, role decomposition alone may be less important than underlying-model quality or risk control.

---

## Experiment 2: Single-Agent Tool Orchestration vs Multi-Agent Debate

**Hypothesis**

Under matched data sources and action budgets, a well-trained single-agent tool-orchestrated system can outperform debate-style multi-agent systems on both economic performance and decision consistency.

**Motivation from corpus**

- `A076` strongly suggests this possibility.
- `A024`, `A050`, and `A075` show that multi-agent systems remain appealing but not automatically superior.

**Setup**

- Fix one market universe, one backtest engine, and one tool suite.
- Compare:
  - single-agent ReAct-style policy learner
  - multi-agent debate system
  - multi-agent routed system with strict aggregation rules
- Keep the underlying-model family as matched as possible.

**Metrics**

- ARR, Sharpe, MDD
- action disagreement rate
- tool-call efficiency
- latency / token cost per decision
- decision reproducibility across seeds

**Success criterion**

One design dominates the others on risk-adjusted return and efficiency, with clear evidence about where coordination helps or hurts.

**Failure interpretation**

If no design dominates, the correct conclusion is conditional: organization quality depends on task class, not a universal single-agent vs multi-agent rule.

---

## Experiment 3: Grounded Reflection vs Retrieval-Only Memory

**Hypothesis**

Reflection tied to outcome-bearing trajectories produces better generalization than retrieval-only memory or ungrounded verbal reflection.

**Motivation from corpus**

- `A075` explicitly motivates this gap.
- `A023` and `A050` show memory/reflection designs but do not fully settle the grounding question.

**Setup**

Compare three variants inside one agentic trading system:

- retrieval-only historical memory
- verbal reflection over prior cases
- reflection grounded in trajectories with reasoning, action, and realized outcome labels

**Metrics**

- out-of-sample Sharpe
- degradation under regime shift
- reflection usefulness judged by downstream action improvement
- memory hit rate and action correction rate

**Success criterion**

Grounded reflection materially improves out-of-sample performance and reduces repeated bad actions relative to weaker memory variants.

**Failure interpretation**

If grounded reflection adds little, then current claims about reflection may be overstated and the true driver may be stronger risk gating or baseline model quality.

---

## Experiment 4: Governance Gates as Performance-Protection Tradeoffs

**Hypothesis**

Risk and governance gates improve stability and drawdown control, but only when calibrated to the market regime and decision horizon.

**Motivation from corpus**

- `A075` and `A071` show that gating matters.
- `A068` and `A021` also suggest specialized risk layers are not optional.

**Setup**

Take one agentic system and vary:

- no gate
- fixed conservative gate
- adaptive regime-aware gate
- adaptive gate plus turnover budget

**Metrics**

- Sharpe
- MDD
- turnover
- number of avoided bad trades
- number of suppressed good trades

**Success criterion**

Adaptive gating dominates fixed gating or no gating on a joint objective of Sharpe and drawdown.

**Failure interpretation**

If gating mainly suppresses profitable behavior, the field needs a better theory of when governance layers help and when they become bottlenecks.

---

## Experiment 5: Underlying-Model Swap and Tool Policy Robustness

**Hypothesis**

Apparent architectural gains shrink substantially when the underlying model is swapped or when tool availability changes, revealing hidden dependency on model-specific competence.

**Motivation from corpus**

- `A076`, `A021`, `A071`, and `A067` all point toward underlying-model dependence.

**Setup**

For one or two representative agentic systems, run:

- multiple underlying models within the same family scale band
- open vs closed underlying-model regimes where possible
- reduced tool suite vs full tool suite

**Metrics**

- change in Sharpe / ARR / MDD
- change in tool-call pattern
- reasoning path divergence
- action agreement rate across underlying models

**Success criterion**

If architecture remains strong under swaps, the paper can argue for architectural robustness.
If performance collapses, underlying-model dependence must become a first-class explanatory variable.

**Failure interpretation**

A large drop would mean current literature is over-attributing gains to architecture that may actually be driven by backbone/tool coupling.

---

## Experiment 6: Source Diversity vs Shared-Retrieval Bias

**Hypothesis**

Adding more agents does not help if their evidence sources are highly correlated; explicit source diversity constraints produce better committee behavior.

**Motivation from corpus**

- `A077` suggests some agents add redundant or noisy information.
- `A076` shows selective tool policy matters more than raw breadth.

**Setup**

Construct multi-agent teams under three evidence regimes:

- unconstrained shared sources
- source-partitioned agents
- source-partitioned agents plus aggregation penalties for redundancy

**Metrics**

- Sharpe
- disagreement diversity
- source-overlap statistics
- contribution of each agent to the final decision

**Success criterion**

Source-partitioned systems outperform shared-source systems or achieve similar returns with lower redundancy and better interpretability.

**Failure interpretation**

If source partitioning does not help, the main bottleneck may be reasoning quality rather than evidence diversity.

---

## Experiment 7: Coordination Quality Under Latency and Cost Budgets

**Hypothesis**

Agentic trading organizations only outperform simpler designs when their coordination overhead fits the decision horizon; under tight latency or call-budget constraints, architectural complexity can become a net negative.

**Motivation from corpus**

- `A076` suggests that selective tool policy matters as much as nominal access breadth.
- `A067` shows that multi-tool, multi-turn financial tasks are operationally much harder than simple invocations.
- `A021` and `A075` imply that strategic reasoning and risk control may need different clocks.
- `A077` suggests that better task granularity can help, but also increases coordination burden.

**Setup**

Evaluate one organizational multi-agent system and one stronger single-agent tool-orchestrated system under:

- unconstrained call budget
- fixed model/tool-call budget
- fixed end-to-end latency budget
- matched economic horizon settings such as daily, hourly, and event-driven decisions

**Metrics**

- Sharpe, ARR, MDD
- end-to-end latency
- model/tool calls per decision
- token or compute cost per decision
- missed-opportunity rate due to slow execution
- mandate-overlap or redundant-message rate across agents

**Success criterion**

The organizational system remains superior only within clearly identifiable operating envelopes, and those envelopes can be described in terms of latency, call budget, and task horizon.

**Failure interpretation**

If performance degrades sharply once cost and latency budgets are realistic, the literature is overestimating the practical benefit of organizational complexity.

---

## What This Agenda Does for the Paper

This agenda improves the paper in three ways:

1. It ties future work directly to failure modes observed in the strengthened corpus.
2. It makes the paper look agenda-setting rather than merely diagnostic.
3. It gives the writing agent concrete material for a much stronger discussion section.
