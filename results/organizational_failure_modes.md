# Organizational Failure-Mode Taxonomy

## Purpose

This document upgrades the paper's organizational reading from a small archetype count into a more actionable taxonomy of why agentic trading systems remain fragile.

The goal is not to claim that every failure mode is already proven at production scale.
The goal is to separate:

- failure modes directly supported by the corpus
- failure modes strongly implied by comparative evidence
- failure modes that remain hypotheses for the research agenda

This lets the paper say something sharper than "role-decomposed systems are rare".
It lets the paper say **what tends to break, why it breaks, and what design choices seem to help**.

---

## Evidence Status Labels

- `Observed in-paper`: directly supported by a paper's reported ablation, comparison, or discussion
- `Cross-paper supported`: not isolated in one paper, but supported by multiple aligned papers
- `Research hypothesis`: plausible and important, but not yet strongly isolated in the public literature

---

## Taxonomy

### 1. Coordination Noise and Debate Dilution

**What fails**

As more agents are added, inter-agent debate can inject noise, inconsistent signals, or prompt-sensitive conflict instead of genuine complementarity.

**Why it matters**

This is one of the central reasons why multi-agent trading systems may look conceptually rich but fail to outperform leaner designs.

**Evidence status**

- `Observed in-paper`
- `Cross-paper supported`

**Corpus anchors**

- `A076` AlphaQuanter: argues and shows that, except for GPT-4o, single-agent variants outperform multi-agent prompt-based baselines on key metrics, suggesting that debate can amplify hallucinations and inconsistency.
- `A077` Expert Investment Teams: shows that not all additional roles help; some agents inject redundancy or noise when coordination is weak.
- `A024` TradingAgents: rich role structure is attractive, but evidence remains thin on whether the committee reliably helps under stronger realism.

**Design implication**

The paper should not equate "more agents" with "better organization".
The operative question is whether the system has a disciplined communication and aggregation mechanism.

---

### 2. Task Granularity Mismatch

**What fails**

Coarse role prompts such as "analyze fundamentals" or "act as a portfolio manager" often underspecify the actual workflow, producing shallow or unstable reasoning.

**Why it matters**

This is a more precise explanation for why some role-based systems underperform: the problem is not only role count, but whether the task decomposition mirrors real analytical work.

**Evidence status**

- `Observed in-paper`

**Corpus anchors**

- `A077` Expert Investment Teams: the clearest evidence in the current corpus. Fine-grained task decomposition significantly improves Sharpe outcomes over coarse-grained prompting in 4 of 5 portfolio sizes, with 50 trials and significance testing.
- `A075` TradingGroup: role specialization plus targeted reflection helps align decision quality, risk control, and post-training data generation.

**Design implication**

Role decomposition should be treated as a task-design problem, not a theatrical persona-design problem.

---

### 3. Misaligned Information Propagation

**What fails**

Signals produced by lower-level agents are not necessarily propagated in a way that preserves their value for downstream decision-makers.

**Why it matters**

A system can contain good local analysts and still fail globally if their outputs are misrouted, diluted, or overweighted at the wrong stage.

**Evidence status**

- `Observed in-paper`
- `Cross-paper supported`

**Corpus anchors**

- `A077` Expert Investment Teams: explicitly shows that alignment between intermediate analytical outputs and downstream decision preferences is a key driver of performance; technical signals are propagated better under fine-grained coordination.
- `A075` TradingGroup: style agent, forecasting agent, and decision agent are linked through reflection and risk-aware gating rather than isolated outputs.
- `A071` unified regime-aware framework: controller-level gating turns upstream sentiment/regime signals into filtered portfolio actions rather than direct uncontrolled responses.

**Design implication**

The paper should emphasize routing and aggregation quality, not only the presence of multiple specialist agents.

---

### 4. Reflection Without Grounded Outcome Memory

**What fails**

"Reflection" can collapse into generic retrieval or narrative restatement when the system lacks grounded links between prior reasoning, actions, and realized outcomes.

**Why it matters**

This is one of the easiest places for agent papers to overclaim learning without truly closing the loop.

**Evidence status**

- `Observed in-paper`
- `Cross-paper supported`

**Corpus anchors**

- `A075` TradingGroup: explicitly critiques generic RAG-style case retrieval and instead logs execution outcomes, agent traces, and daily evaluation metrics to build higher-quality post-training data.
- `A023` FinMem: memory architecture is central, but the literature still often leaves the quality of memory-grounding underspecified.
- `A050` FinVision: reward/reflection cycle exists, but evidence remains lighter and the setting narrower.

**Design implication**

Reflection should be treated as credible only when tied to outcome-bearing trajectories, not just recalled text.

---

### 5. Risk Gating as a Bottleneck and Safety Valve

**What fails**

Risk control can either stabilize the system or suppress profitable behavior, depending on how thresholds and intervention layers are designed.

**Why it matters**

This failure mode is central to any paper that wants to move from idea generation to trading deployment logic.

**Evidence status**

- `Observed in-paper`

**Corpus anchors**

- `A075` TradingGroup: turning off risk management improves NFLX in one case but degrades other assets, showing that risk gating can both constrain and protect performance.
- `A068` adaptive LLM-based multi-agent system: black-swan and market-risk agents contribute to improved stability.
- `A071` unified regime-aware framework: Sharpe-gated controller and turnover budgeting reduce unnecessary rebalance churn.
- `A021` WebCryptoAgent: explicitly decouples strategic reasoning from a faster risk-control layer.

**Design implication**

The field needs to stop treating risk control as an add-on and treat it as a first-class organizational design variable.

---

### 6. Governance and Compliance Escalation Friction

**What fails**

Control layers, approval gates, or checker modules can become serial bottlenecks that slow action, add brittle handoff points, or create the appearance of safety without materially improving decisions.

**Why it matters**

For agentic trading, governance cannot be treated only as a yes/no safety feature. It changes the speed, shape, and economic viability of the entire decision loop.

**Evidence status**

- `Observed in-paper`
- `Cross-paper supported`

**Corpus anchors**

- `A021` WebCryptoAgent: separates strategic reasoning from a faster real-time risk layer, implicitly acknowledging that governance has to operate at a different clock speed from planning.
- `A071` unified regime-aware framework: controller gating helps, but it also shows that the decision pipeline becomes more mediated and potentially slower.
- `A075` TradingGroup: risk module and reflection improve quality, but they also add a sequential control structure that would matter more under tighter latency budgets.
- `A067` FinMCP-Bench: multi-tool, multi-turn financial tasks become much harder once realistic operational steps and checks are introduced.

**Design implication**

The field should treat governance as a throughput and coordination design problem, not only as a safety ornament.

---

### 7. Tool-Use Inefficiency and Search Collapse

**What fails**

Tool-rich agents may over-query, query the wrong sources, or fail to acquire information in a strategically useful order.

**Why it matters**

This is especially important for the paper's tool-assisted frontier: tool access is not automatically competence.

**Evidence status**

- `Observed in-paper`
- `Cross-paper supported`

**Corpus anchors**

- `A076` AlphaQuanter: tool-use policy is learned and ablations show that removing tool/process rewards sharply lowers ARR.
- `A067` FinMCP-Bench: benchmark evidence shows multi-tool and multi-turn settings are substantially harder than simple tool invocation.
- `A069` trading-instruction execution paper: even seemingly narrow execution-assistance tasks remain brittle in follow-up behavior and field completion.

**Design implication**

The paper should distinguish between nominal tool access and learned tool orchestration.

---

### 8. Operational Cost and Latency Overhead

**What fails**

Agentic systems accumulate sequential model calls, tool calls, and coordination hops that may exceed the time or cost budget of the claimed trading horizon.

**Why it matters**

A system can look strong on backtest logic while remaining operationally implausible once latency, token cost, or synchronization overhead are considered.

**Evidence status**

- `Cross-paper supported`
- `Research hypothesis`

**Corpus anchors**

- `A076` AlphaQuanter: learned tool policy matters partly because indiscriminate tool use is too expensive and too noisy.
- `A067` FinMCP-Bench: multi-tool, multi-turn financial tasks degrade rapidly in success rate, implying meaningful operational overhead.
- `A021` WebCryptoAgent: architectural separation between slow strategic reasoning and fast risk response suggests an implicit latency-management problem.
- `A077` Expert Investment Teams: fine-grained coordination improves results, but it also implies more communication and synchronization cost than coarse prompting.

**Design implication**

Future papers should report decision-latency fit, tool-call budgets, and coordination cost alongside return metrics.

---

### 9. Role Drift and Mandate Creep

**What fails**

Agents that are nominally specialized begin to produce overlapping, ambiguous, or weakly bounded outputs, reducing accountability and making downstream aggregation brittle.

**Why it matters**

This is one reason multi-agent designs can look more sophisticated than they really are: specialization on paper does not guarantee stable functional separation in practice.

**Evidence status**

- `Cross-paper supported`
- `Research hypothesis`

**Corpus anchors**

- `A077` Expert Investment Teams: some roles add less value than others, which is exactly what we would expect when specialization quality and boundary discipline vary.
- `A075` TradingGroup: style, forecast, decision, and risk roles are more effective because the architecture gives them clearer functional separation.
- `A024` TradingAgents: role diversity is conceptually rich, but the public evidence is still thinner on whether mandates remain distinct under realistic pressure.
- `A050` FinVision: multiple agents exist, but the literature still rarely documents role-level failure, confusion, or takeover dynamics explicitly.

**Design implication**

Role-decomposed systems should specify mandate boundaries and information contracts, not just agent personas.

---

### 10. Shared-Retrieval Bias and Correlated Views

**What fails**

Different agents appear diverse on paper but rely on overlapping evidence streams or similarly framed prompts, causing false diversity.

**Why it matters**

This can make committees look richer than they are, while increasing agreement for the wrong reason.

**Evidence status**

- `Cross-paper supported`
- `Research hypothesis`

**Corpus anchors**

- `A077` Expert Investment Teams: some agents seem to add noise or redundant information rather than complementary signal.
- `A075` TradingGroup: retrieval quality and role-specific reflection matter precisely because not all information sources are equally useful.
- `A076` AlphaQuanter: learned tool preference becomes selective over time, implying that naive breadth of evidence is not enough.

**Design implication**

Future agentic trading benchmarks should track source overlap and effective evidence diversity, not only the number of agents.

---

### 11. Underlying-Model and Agent Quality Coupling

**What fails**

Agentic behavior quality depends strongly on the underlying model and tool policy, so apparent architectural gains may partly reflect underlying-model choice rather than organization alone.

**Why it matters**

This is one of the most important unresolved issues for the paper's framework.

**Evidence status**

- `Cross-paper supported`
- `Research hypothesis`

**Corpus anchors**

- `A076` AlphaQuanter: 7B and 3B variants learn materially different tool policies and risk behavior.
- `A021` WebCryptoAgent: results depend strongly on proprietary underlying models and memory configuration.
- `A071` unified regime-aware framework: depends on a specific textual underlying model for sentiment/regime input.
- `A067` FinMCP-Bench: model rankings vary substantially on financial tool-use tasks.

**Design implication**

This is the strongest reason the paper still needs an explicit methodological decision on how underlying-model dependence enters the framework.

---

### 12. Evaluation Short-Horizon Fragility

**What fails**

A system may look strong over a narrow set of assets or a short backtest window while remaining fragile across regimes.

**Why it matters**

This is a recurrent ceiling on the public literature and a direct reason not to overclaim frontier maturity.

**Evidence status**

- `Cross-paper supported`

**Corpus anchors**

- `A075`: five assets and a short out-of-sample window.
- `A076`: five large-cap tech names and 122 test days.
- `A050`: three tech stocks in a bullish period.
- `A024`: short backtest and weak friction modeling.

**Design implication**

The frontier is stronger than before, but still not mature enough to treat short-horizon success as robust deployment evidence.

---

### 13. Frontier Papers Solve Different Problems but Get Flattened Together

**What fails**

The field mixes distinct problem classes: role-decomposed trading teams, tool-orchestrated single agents, evaluator-coupled alpha search, portfolio controllers, and tool-use benchmarks.

**Why it matters**

If these are flattened into one bucket, both evidence interpretation and research agenda become muddled.

**Evidence status**

- `Cross-paper supported`

**Corpus anchors**

- `A075` and `A077`: organizational systems
- `A076`: tool-orchestrated single-agent policy learner
- `A070`, `A072`, `A073`: artifact-search systems
- `A071`: controller-style portfolio agent
- `A067`: enabling benchmark infrastructure

**Design implication**

The manuscript should explicitly exploit this taxonomy rather than treating the frontier as a single undifferentiated family.

---

## What the Taxonomy Changes in the Paper

This taxonomy supports four stronger moves in the manuscript:

1. It lets the paper explain why role-decomposed systems are still rare or fragile without pretending the answer is only corpus size.
2. It turns the organizational reading into a substantive contribution rather than a small-count observation.
3. It creates a clean bridge into the research agenda by linking each failure mode to a testable experiment.
4. It strengthens the claim that the frontier is now better covered, but still uneven across organizational, evaluative, and deployment dimensions.

---

## Most Important Takeaway

The public frontier is no longer so thin that the paper can only say "there are very few agentic trading systems".

A stronger claim is now available:

- the frontier is real,
- it spans multiple organizational forms,
- but it remains bottlenecked by recurring coordination, routing, tooling, and evaluation failures.
