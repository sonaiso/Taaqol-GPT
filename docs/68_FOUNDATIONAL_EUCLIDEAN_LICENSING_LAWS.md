# 68 — Foundational Euclidean Licensing Laws

> Status: foundational definition surface for X0R/X0L hardening follow-up.
> This document closes the shared definition layer for the foundational
> Euclidean transition licensing package without opening a new runtime layer.

---

## 1) Scope

This law defines the foundational Euclidean licensing concepts used by the
runtime contract surfaces in:

- `src/taaqqul_slot_geometry/x0r/transition_contract.py`
- `src/taaqqul_slot_geometry/x0r/learning_loop.py`

No parser, morphology, syntax, semantics, hukm, or new branch is licensed here.

---

## 2) Canonical definitions

The package definitions are fixed as:

- **Origin**: declared upstream identity-preserving source.
- **Branch**: declared downstream candidate linked to origin through licensed path.
- **Origin/Branch Link**: bidirectional, trace-visible linkage proof.
- **Differentiating Feature**: verified discriminator preventing branch collapse.
- **Qadih Difference**: explicit checked status (`UNCHECKED`, `BLOCKING`, `CLEAR`, `RESIDUAL`).
- **Condition / Sabab / Mani**: distinct gate checks, not interchangeable.
- **Rank Force Ceiling**: meet-preserving maximum admissible rank.
- **Residual Visibility**: no approved output with hidden residuals.
- **Named Handoff**: explicit transition handoff string; no silent transfer.
- **Failed Stage**: first failing stage captured and surfaced.

---

## 3) Gate evaluation order

Foundational evaluation order is:

`DOMAIN → TRACE → ORIGIN → BRANCH → DIFFERENTIATING_FEATURE → QADIH → EVIDENCE → RANK_CEILING → RESIDUALS → HANDOFF`.

Every refusal/defer/block verdict is attached to the first failing stage.

---

## 4) Public carrier invariants

For `JumpTestResult`:

- `allowed=True` requires:
  - `readiness_state=LINK_READY`
  - `failed_stage=None`
  - `failure_code=None`
- `allowed=False` requires:
  - `readiness_state!=LINK_READY`
  - `failed_stage is not None`
  - `failure_code is not None`

For `EuclideanGateDecision`:

- `transition_allowed=True` requires:
  - `readiness_state=LINK_READY`
  - `failed_stage=None`
  - `failure_code=None`
- `transition_allowed=False` requires:
  - `readiness_state!=LINK_READY`
  - `failed_stage is not None`
  - `failure_code is not None`

---

## 5) Forbidden surface

Forbidden in this step:

- opening partition/identity/necessity runtime layers;
- adding parser or semantic runtime behavior;
- adding unlicensed direct transitions;
- approving output while residuals are hidden;
- widening global failure taxonomy without contract need.

---

## 6) Evidence anchors

- Runtime contract: `src/taaqqul_slot_geometry/x0r/transition_contract.py`
- Runtime tests: `tests/test_pr_x0r_runtime_contract_hooks.py`
- Golden fixtures: `data/x0r_foundational_transition_fixtures.json`
- Fixture tests: `tests/test_x0r_foundational_transition_fixtures.py`
