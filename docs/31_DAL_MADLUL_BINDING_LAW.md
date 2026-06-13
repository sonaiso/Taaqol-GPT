# 31 — Dal-Madlul Binding Candidate Boundary Law

> **Status:** Constitutional law. Ratified in PR-17.
> This document binds every PR that constructs, consumes, or depends upon
> a `DalMadlulBindingCandidate`. It establishes the binding boundary
> between signifier (DalOnlyCandidate) and verbal signified
> (VerbalMadlulCandidate) under rank/residual/trace governance.

## 0. Governing principle

```text
DalMadlulBindingCandidate is a binding proof, not meaning.
No DalMadlulBindingCandidate without a proven DalOnlyCandidate.
No DalMadlulBindingCandidate without a proven VerbalMadlulCandidate.
No DalMadlulBindingCandidate without registry evidence for both parties.
DalMadlulBindingCandidate ≠ Meaning.
DalMadlulBindingCandidate ≠ Ifadah.
DalMadlulBindingCandidate ≠ Hukm.
DalMadlulBindingCandidate ≠ Reality.
DalMadlulBindingCandidate is a pre-semantic binding candidate, never a semantic verdict.
```

The binding candidate proves that a signifier (dal) and a verbal
signified (madlul) can be formally bound under constitutional
governance. The binding itself carries no semantic content: it is
a structural proof that both parties have been independently proven,
registered, and can be associated — nothing more.

## 1. Required prior carriers

A `DalMadlulBindingCandidate` can only be constructed when ALL of the
following exist:

1. A `DalOnlyCandidate` — proven signifier standing (PR-15, docs/26).
2. A `VerbalMadlulCandidate` — proven verbal signified standing
   (PR-16, docs/27), whose `.dal_only` field is the SAME
   `DalOnlyCandidate` as (1).
3. A `RegistryLookupResult` for the DAL_ONLY domain with state FOUND.
4. A `RegistryLookupResult` for the VERBAL_MADLUL domain with state
   FOUND.

If any of these are absent or invalid, the binding is refused with a
named `FailureCode`.

## 2. DalMadlulBindingCandidate fields

```text
DalMadlulBindingCandidate:
    dal_candidate       : DalOnlyCandidate       — the proven signifier
    madlul_candidate    : VerbalMadlulCandidate   — the proven verbal signified
    dal_registry_proof  : RegistryLookupResult    — FOUND proof for DAL_ONLY
    madlul_registry_proof : RegistryLookupResult  — FOUND proof for VERBAL_MADLUL
    binding_rank        : Rank                    — bounded via meet
    residuals           : tuple[Residual, ...]    — merged, visible only
    trace_ref           : str                     — reference, not ledger commit
```

## 3. Binding operation: `bind_dal_madlul()`

The binding operation is a **pure function** with the following
signature:

```text
bind_dal_madlul(
    dal_candidate      : DalOnlyCandidate,
    madlul_candidate   : VerbalMadlulCandidate,
    dal_registry       : RegistryLookupResult,
    madlul_registry    : RegistryLookupResult,
) -> DalMadlulBindingVerdict
```

### Input boundary (refuses with named FailureCode):

- `dal_candidate` must be a `DalOnlyCandidate` instance.
- `madlul_candidate` must be a `VerbalMadlulCandidate` instance.
- `madlul_candidate.dal_only` must be the same instance as
  `dal_candidate` (identity match).
- `dal_registry` must be a `RegistryLookupResult` with state FOUND.
- `madlul_registry` must be a `RegistryLookupResult` with state FOUND.

### Residual governance:

Residuals are merged from both candidates:
`dal_candidate.residuals + madlul_candidate.residuals`

Any `ResidualKind.HIDDEN_FORBIDDEN` or `ResidualKind.BLOCKING`
residual in the merged set triggers an immediate refusal:
- HIDDEN_FORBIDDEN → `FailureCode.HIDDEN_RESIDUAL`
- BLOCKING → `FailureCode.BLOCKING_RESIDUAL_PRESENT`

### Rank bounding:

```text
binding_rank = RankLattice.meet(dal_candidate.dal_rank, madlul_candidate.madlul_rank)
binding_rank = RankLattice.meet(binding_rank, BINDING_RANK_CEILING)
```

The binding rank ceiling equals `MADLUL_BOUNDARY_RANK_CEILING`.

### Output:

- On success: `BOUND` with a `DalMadlulBindingCandidate`.
- On refusal: `REFUSED` with a named `FailureCode`.

## 4. DalMadlulBindingVerdict

```text
DalMadlulBindingVerdict:
    candidate       : DalMadlulBindingCandidate | None
    verdict_state   : BindingState (BOUND | REFUSED)
    failure_code    : FailureCode | None
    verdict_rank    : Rank
    residuals       : tuple[Residual, ...]
    trace_ref       : str
```

State invariants:
- BOUND → candidate is not None, failure_code is None.
- REFUSED → candidate is None, failure_code is a named FailureCode.

## 5. Forbidden outputs (proven absent)

- meaning, reference, denotation, concept
- ifadah, hukm, reality, ontology, truth-value
- ContractableUnitGeometry (PR-18)
- RelationCandidate, CompositionCandidate (PR-19)
- ExtraLetterLicense, C_Aug
- semantic/wadʿi/dalālah lexicon access
- new FailureCode members
- new runtime dependencies

## 6. Constitutional invariants

1. `DalMadlulBindingCandidate ≠ Meaning` — the binding is structural,
   never semantic.
2. `DalMadlulBindingCandidate ≠ Ifadah` — the binding does not produce
   propositions.
3. `DalMadlulBindingCandidate ≠ Hukm` — the binding does not judge.
4. `DalMadlulBindingCandidate ≠ Reality` — the binding does not
   correspond to reality.
5. The binding candidate is a pre-semantic structural proof that
   licenses PR-18 (ContractableUnitGeometry) and nothing else.
6. Every refusal carries a named `FailureCode`.
7. No rank promotion beyond `BINDING_RANK_CEILING`.
8. No hidden or blocking residuals pass.
9. `bind_dal_madlul()` is pure: no I/O, no ledger, no network.
