# 97 — Theory of Governed Acts (TGovA) Condensation Law

> **Status:** Constitutional law. Ratified as PR-138.
> **Type:** Law-only condensation and formalization step.
> **Scope:** Condense the governed-acts constitutional posture from 20 repeated
> clauses into 7 governing laws and 3 formal theorems, without opening runtime.

## §1 Origin and authority

This law refines the governed-acts constitutional posture into a minimal
non-redundant structure that can be implemented in staged runtime PRs without
chain ambiguity.

This law is binding under:

- `docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md`
- `docs/13_CONSTITUTIONAL_PR_GEOMETRY.md`
- `docs/14_PR_CHAIN_ROADMAP.md`
- `docs/52_CONSTITUTIONAL_TEST_ORIGIN_COVENANT.md`

## §2 Condensed governing laws (Q1..Q7)

The governed-acts boundary is defined by exactly seven laws:

- `Q1: Separation Law` — executor, guardian, and trace registry are distinct constitutional roles.
- `Q2: Contract Law` — each transition is bounded by explicit domain and guardian contracts.
- `Q3: Identity Law` — no transition without explicit input/output identity continuity rules.
- `Q4: Rank Law` — approved rank is lattice-bounded and never self-promoted.
- `Q5: Residual Law` — residual visibility is mandatory; hidden residual approval is forbidden.
- `Q6: Evidence Law` — no approval without visible evidence; guardian does not fabricate evidence.
- `Q7: Multiplicity Law` — one operation may have multiple admissible guarded paths, each contract-bounded.

## §3 Mapping of prior 20 clauses to Q1..Q7

The previous governed-acts clause set is normalized as:

- `Q1 ← {1,2,3,4,16}`
- `Q2 ← {5,6,17}`
- `Q3 ← {8,18}`
- `Q4 ← {9,19}`
- `Q5 ← {10}`
- `Q6 ← {11,14,15}`
- `Q7 ← {12,13}`

No additional clause may be introduced if it is logically subsumed by `Q1..Q7`.

## §4 Formal theorem surface (T1..T3)

Exactly three formal theorem statements govern admissibility:

- `T1 (No self-approval): ¬∃E: Executor(E) ∧ CanSelfApprove(E)`
- `T2 (No unlicensed jump): ∀i,j: Transition(L_i, L_j) ∧ j > i+1 ⇒ ∃G: LicensedGate(G, L_i, L_j)`
- `T3 (Rank boundedness): ∀o: Rank(o) ≤ min(Rank(input(o)), Rank(evidence(o)), Rank(closure(o)))`

`T1..T3` are the formal theorem surface for PR-chain implementation gates.

## §5 Non-contradiction clarifications

To remove prior ambiguity:

- Guardian classification is allowed; guardian execution is forbidden.
- Guardian may emit constitutional approval context but may not create domain entities.
- Executor may produce candidate outputs but may not self-license transitions.

## §6 Runtime boundary and admission rule

PR-138 is law-only and does not open runtime code.

PR-138 licenses exactly this order:

1. `PR-140` (matrix-to-code binding under finalized contracts)
2. `PR-139` (executor/guardian staged separation in sensitive modules)

Any runtime mutation under PR-138 itself is a `FORBIDDEN_LEAP`.

## §7 Forbidden surface

Under PR-138, the repository MUST NOT:

- mutate `src/taaqqul_slot_geometry/**`;
- change `FailureCode` global inventory;
- collapse executor and guardian roles into a single self-licensing runtime path;
- open semantic/hukm/truth/certainty/reality outputs beyond current chain rights.

## §8 Local residual vocabulary

PR-138 uses local residual names only:

- `CONDENSATION_MAPPING_INCOMPLETE`
- `THEOREM_SURFACE_UNDECLARED`
- `SELF_APPROVAL_SURFACE_LEAK`
- `UNLICENSED_JUMP_SURFACE_LEAK`
- `RANK_BOUND_SURFACE_MISSING`

## §9 Constitutional test expectations

Acceptance tests for this law MUST prove:

- presence of `Q1..Q7` and uniqueness of the condensed law set;
- presence of exact `T1..T3` theorem statements;
- explicit law-only boundary;
- explicit sequencing `PR-140` before `PR-139`;
- explicit forbidden runtime mutation surface.

## §10 Constitutional effect

This law is an interim constitutional consolidation that removes redundancy and
locks formal theorem surface prior to runtime refactoring.

It does not itself implement executor/guardian runtime separation.
