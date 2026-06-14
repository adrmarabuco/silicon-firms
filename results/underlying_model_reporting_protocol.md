# Minimum Reporting Protocol for the Underlying-Model Layer

## Purpose

This protocol defines the minimum reporting standard that future `agentic trading` papers should satisfy when they rely on an `underlying model`.

It is motivated by a recurring problem in the strengthened frontier corpus:

- papers often describe role structure, tool orchestration, or evaluator loops more clearly than they describe the model layer that actually powers those systems

That weakens:

- reproducibility
- causal interpretation
- deployment credibility

The goal is not to rank models.
The goal is to make the model layer legible enough that system-level claims can be evaluated more rigorously.

---

## Core Position

Large language models are already partially opaque substrates for scientific investigation:

- internal reasoning is not fully inspectable
- latent representations are hard to interpret directly
- output behavior is only partially observable through prompts, traces, and responses

When the `underlying model` is also `closed-source/API-based`, a second layer of opacity is added:

- weights are unavailable
- training data and fine-tuning history are often unavailable
- version drift may occur outside the researcher's control
- inference-time behavior may change without a stable local artifact

This does **not** make such papers invalid.
But it does mean that scientific reporting must compensate by making the model layer more explicit.

---

## Minimum Required Fields

Every paper in scope should report, at minimum, the following fields for the underlying-model layer when applicable.

### 1. Underlying-model release type

Allowed values:

- `open-weight`
- `closed-source/API-based`
- `mixed`
- `unspecified`

### 2. Model family

Examples:

- `general-purpose proprietary`
- `open-weight general-purpose`
- `finance-specialized`
- `hybrid`

### 3. Allocation pattern

Allowed values:

- `single-model homogeneous`
- `multi-model heterogeneous`
- `unspecified`

This field asks whether:

- the same model powers all roles
- or different roles rely on different models

### 4. Specification quality

Allowed values:

- `exact`
- `partial`
- `vague`

This field captures whether the paper tells the reader enough to know what was actually used.

### 5. Sensitivity evidence

Allowed values:

- `none`
- `weak mention`
- `explicit comparison`
- `architecture-controlled comparison`

This field captures whether the paper actually studies:

- how sensitive the system is to underlying-model choice

---

## Reporting Expectations by Claim Strength

### If the paper makes a system-design claim

It should report:

- release type
- model family
- allocation pattern
- exact or partial specification quality

### If the paper makes a performance claim

It should additionally report:

- whether the result was tested under more than one underlying model
- whether the same architecture was held fixed while the model changed

### If the paper makes a deployment-credible or reproducibility claim

It should additionally report:

- whether the model artifact is locally reproducible
- whether the system depends on a versioned external API
- whether model updates outside the paper's control could change behavior

---

## Best-Practice Extensions

The following are not required for minimal inclusion, but should become best practice.

### 1. Architecture-controlled model sensitivity

Hold the system fixed and swap:

- model size
- model family
- release type

This is the cleanest way to separate:

- architecture effects
- from underlying-model effects

### 2. Role-to-model allocation disclosure

For multi-agent systems, report:

- which role uses which model
- why that mapping was chosen
- whether faster/smaller models and slower/reasoning-heavy models were deliberately mixed

### 3. Version pinning

If a model is API-based, report:

- provider
- model name
- version or date
- any relevant inference settings

### 4. Cost and latency sensitivity

If a paper relies on multiple models or different model sizes, report:

- cost consequences
- latency consequences
- whether performance gains survive cheaper/faster substitutions

---

## What This Protocol Lets the Survey Say

If this minimum layer is reported consistently, the literature becomes easier to evaluate on three important fronts:

### 1. Reproducibility

Readers can tell whether a result depends on:

- a stable open-weight artifact
- a drifting proprietary API
- or an under-specified black box

### 2. Causal interpretation

Readers can better judge whether a gain comes from:

- the architecture
- the evaluator loop
- the tool stack
- or the underlying model itself

### 3. Organizational realism

Readers can see whether role-rich systems actually specify:

- model assignment across roles
- or only role names without a concrete model-allocation design

---

## Current Survey Position

For this revision, the survey uses this protocol as a **normative benchmark** and as a **descriptive-analytical reading aid**.

That means:

- the paper does not become a model leaderboard
- the underlying-model layer is not ignored
- and future papers can be judged against a clearer minimum reporting standard

The present revision does **not** yet force this layer into the main evidence tier itself.
That additional formalization remains a separate methodological decision.
