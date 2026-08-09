# 107 — Intended-Class Structurality Attack (V0.29a)

> Status: constitutional structurality boundary + bounded runtime/specification document.
> Scope: define a fragment-local intended class structurally and independently of downstream claim/checker/extractor surfaces.
> Snapshot date: 2026-08-09.

## §1 Constitutional role and stop gate

V0.29a is a hard stop-gate step before any projection/equivalence/cutoff work.

It proves or refuses exactly one question:

```text
Can the selected intended class K_i be defined structurally,
non-circularly, and independently of later claim-evaluation predicates?
```

If this step fails (`STRUCTURALITY_FAIL`), downstream work must not be opened by smuggling
claim/correctness/checker vocabulary into the class definition.

## §2 Frozen distinction (non-collapse law)

The development keeps four objects disjoint:

```text
Model != Realization != Context != IntendedClass
```

No object above may serve as an implicit definition of another.

## §3 Structural signature and anti-smuggling

For the selected minimal fragment (`K_S0_CARRIER_NODE_FRAGMENT`), the structural signature is:

```text
Σ_K_S0 = {
  Node,
  node_id,
  boundary_id,
  domain_id,
  scope_id,
  trace_ref
}
```

The defining theory over `Σ_K_S0` must satisfy anti-smuggling:

```text
Forbidden token surface (non-exhaustive runtime list):
  psi, correct, accept, checker, extractor, b_min, cutoff,
  contextual_equivalence, claim_truth, algorithm_success,
  representation_adequacy

AntiSmuggling(T_K) :=
  no forbidden token occurs in Σ_K
  and no forbidden token occurs in any axiom id/symbol surface of T_K.
```

This is executable and testable; it is not prose-only.

## §4 Fragment-local structural theory

The selected class is fragment-wise, not Arabic-total:

```text
K_S0 := Mod(T_K_S0)
```

with structural axioms:

```text
TK_S0_A1_NON_EMPTY_NODE_SET:
  model has at least one Node.

TK_S0_A2_UNIQUE_NODE_IDS:
  node_id is injective over nodes in one model.

TK_S0_A3_TOTAL_STRUCTURAL_FIELDS:
  node_id/boundary_id/domain_id/scope_id/trace_ref are all non-empty.

TK_S0_A4_TRACE_REF_INJECTIVE:
  trace_ref is injective over nodes in one model.
```

Membership is structural only:

```text
M in K_S0  <=>  M satisfies all TK_S0 axioms.
```

## §5 Structural non-membership and witness schema

Non-membership must be falsifiable with explicit witness:

```text
M not in K_S0 => exists w : Violation_K(M, w)
```

Witness schema:

```text
w = <model_id, axiom_id, locus, observed, expected>
```

`locus` names the exact structural position (example: `nodes[2].trace_ref`).

Known labels may be partial; witness existence does not require a closed global taxonomy at this stage.

## §6 Claim-independence / Structurality theorem

Let `M1`, `M2` be extended models that may differ on downstream fields
(claim truth value, checker output, extractor output, `B_min`, cutoff,
contextual-equivalence, algorithm success). If their `Σ_K` projection is equal:

```text
M1|Σ_K = M2|Σ_K
```

then structural membership is invariant:

```text
M1 in K_S0 <=> M2 in K_S0
```

This is the central V0.29a theorem/test.

## §7 What V0.29a does NOT prove

V0.29a does not prove any of the following:

- Representation Adequacy (`RA_{n,psi}`)
- finite representative property (FRP)
- finite quotient or finite number of claim-equivalence classes
- cutoff theorems
- candidate completeness
- context completeness
- checker completeness
- general Arabic correctness

All are downstream obligations.

## §8 Methodological result format

V0.29a ends with exactly one substantive outcome:

```text
STRUCTURALITY_PASS
or
STRUCTURALITY_FAIL
```

No repair by semantic broadening is licensed in this step.
