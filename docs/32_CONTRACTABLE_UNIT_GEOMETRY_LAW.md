# 32 — Contractable Unit Geometry Law

> **Status:** Constitutional law. Ratified in PR-18.
> This document binds every PR that constructs, consumes, or depends upon
> a `ContractableUnitGeometry`. It establishes the objecthood boundary
> for a bound dal-madlul unit: a contractable unit proves its standing
> as a geometric object before any composition.

## 0. Governing principle

```text
ContractableUnitGeometry is objecthood, not meaning.
No ContractableUnitGeometry without a DalMadlulBindingCandidate.
No ContractableUnitGeometry without binding verdict BOUND.
ContractableUnitGeometry ≠ Meaning.
ContractableUnitGeometry ≠ Ifadah.
ContractableUnitGeometry ≠ Hukm.
ContractableUnitGeometry ≠ Reality.
ContractableUnitGeometry ≠ RelationCandidate.
ContractableUnitGeometry ≠ CompositionCandidate.
ContractabilityProfile ≠ SyntaxRole.
ContractabilityProfile is affordance, not assignment.
```

A `ContractableUnitGeometry` proves that a bound dal-madlul pair can
stand as a contractable object — that is, it has the geometric
standing to participate in composition. The geometry itself carries
no semantic content, no relation, no composition result. It is a
structural proof of objecthood.

## 1. Required prior carriers

A `ContractableUnitGeometry` can only be constructed when ALL of the
following exist:

1. A `DalMadlulBindingCandidate` — proven binding standing (PR-17,
   docs/31).
2. The binding must have been produced by a BOUND verdict
   (BindingState.BOUND).

If the input is absent, invalid, or from a non-BOUND verdict, the
operation is refused with a named `FailureCode`.

## 2. ContractabilityProfile fields

```text
ContractabilityProfile:
    admissible_roles      : tuple[str, ...]  — roles the unit CAN fill
    blocked_roles         : tuple[str, ...]  — roles the unit CANNOT fill
    path_profile          : str              — weight-path summary
    word_class_affordance : str              — word-class affordance tag
    inflection_affordance : str              — inflection affordance tag
    derivational_affordance : str            — derivational affordance tag
```

These fields are affordances/profile only — they do NOT assign a
syntactic role, they do NOT produce meaning, and they do NOT
constitute a final grammatical judgment.

## 3. ContractableUnitGeometry fields

```text
ContractableUnitGeometry:
    binding_candidate       : DalMadlulBindingCandidate
    unit_identity           : str
    contractability_profile : ContractabilityProfile
    objecthood_rank         : Rank
    residuals               : tuple[Residual, ...]
    trace_ref               : str
```

## 4. Contractability operation: `prove_contractable_unit()`

The operation is a **pure function** with the following signature:

```text
prove_contractable_unit(
    binding_candidate       : DalMadlulBindingCandidate,
    admissible_roles        : tuple[str, ...],
    blocked_roles           : tuple[str, ...],
    path_profile            : str,
    word_class_affordance   : str,
    inflection_affordance   : str,
    derivational_affordance : str,
) -> ContractableUnitVerdict
```

### Input boundary (refuses with named FailureCode):

- `binding_candidate` must be a `DalMadlulBindingCandidate` instance.
- `admissible_roles` must be a non-empty tuple of strings.
- `blocked_roles` must be a tuple of strings (may be empty).
- `path_profile` must be a non-empty string.
- `word_class_affordance` must be a non-empty string.
- `inflection_affordance` must be a non-empty string.
- `derivational_affordance` must be a non-empty string.

### Residual governance:

Residuals are carried from the binding candidate:
`binding_candidate.residuals`

Any `ResidualKind.HIDDEN_FORBIDDEN` or `ResidualKind.BLOCKING`
residual triggers an immediate refusal:
- HIDDEN_FORBIDDEN → `FailureCode.HIDDEN_RESIDUAL`
- BLOCKING → `FailureCode.BLOCKING_RESIDUAL_PRESENT`

### Rank bounding:

```text
objecthood_rank = RankLattice.meet(binding_candidate.binding_rank, CONTRACTABLE_UNIT_RANK_CEILING)
```

The contractable unit rank ceiling equals `BINDING_RANK_CEILING`.

### Output:

- On success: `PROVEN` with a `ContractableUnitGeometry`.
- On refusal: `REFUSED` with a named `FailureCode`.

## 5. ContractableUnitVerdict

```text
ContractableUnitVerdict:
    candidate       : ContractableUnitGeometry | None
    verdict_state   : ContractableUnitState (PROVEN | REFUSED)
    failure_code    : FailureCode | None
    verdict_rank    : Rank
    residuals       : tuple[Residual, ...]
    trace_ref       : str
```

State invariants:
- PROVEN → candidate is not None, failure_code is None.
- REFUSED → candidate is None, failure_code is a named FailureCode.

## 6. Forbidden outputs (proven absent)

- meaning, reference, denotation, concept
- ifadah, hukm, reality, ontology, truth-value
- RelationCandidate, CompositionCandidate (PR-19)
- ExtraLetterLicense, C_Aug
- semantic/wadʿi/dalālah lexicon access
- new FailureCode members
- new runtime dependencies
- SyntaxRole assignment (the profile is an affordance, not an assignment)

## 7. Constitutional invariants

1. `ContractableUnitGeometry ≠ Meaning` — the geometry is structural,
   never semantic.
2. `ContractableUnitGeometry ≠ Ifadah` — the geometry does not produce
   propositions.
3. `ContractableUnitGeometry ≠ Hukm` — the geometry does not judge.
4. `ContractableUnitGeometry ≠ Reality` — the geometry does not
   correspond to reality.
5. `ContractableUnitGeometry ≠ RelationCandidate` — the geometry is
   a single unit, not a composition.
6. `ContractabilityProfile` is an affordance profile, not a syntactic
   assignment.
7. The contractable unit proves objecthood and licenses PR-19
   (Composition / RelationCandidate) and nothing else.
8. Every refusal carries a named `FailureCode`.
9. No rank promotion beyond `CONTRACTABLE_UNIT_RANK_CEILING`.
10. No hidden or blocking residuals pass.
11. `prove_contractable_unit()` is pure: no I/O, no ledger, no network.
