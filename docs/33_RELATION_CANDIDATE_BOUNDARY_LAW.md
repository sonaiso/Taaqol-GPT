# 33 — Relation Candidate Boundary Law

> **Status:** Constitutional law. Ratified in PR-19.
> This document binds every PR that constructs, consumes, or depends upon
> a `RelationCandidate`. It establishes the composition/relation boundary
> for contractable units: relation candidacy proves composition
> affordance, never meaning.

## 0. Governing principle

```text
RelationCandidate is relation affordance as candidate, not meaning.
No RelationCandidate without ContractableUnitGeometry.
No RelationCandidate without a PROVEN ContractableUnitState verdict.
RelationCandidate ≠ Meaning.
RelationCandidate ≠ Ifadah.
RelationCandidate ≠ Hukm.
RelationCandidate ≠ Reality.
ContractabilityProfile strings are affordance labels only.
RelationCandidate must not treat ContractabilityProfile as SyntaxRole.
RelationCandidate must re-gate admissible_roles.
No composition from raw candidates.
```

A `RelationCandidate` proves that two or more contractable units can
stand in a governed relation — that is, the units possess the geometric
standing to compose. The relation candidate itself carries no semantic
content, no meaning, no ifadah, no hukm, no reality. It is a structural
proof of relation affordance.

## 1. Required prior carriers

A `RelationCandidate` can only be constructed when ALL of the following
exist:

1. Two or more `ContractableUnitGeometry` instances — proven objecthood
   standing (PR-18, docs/32).
2. Each unit must have been produced by a PROVEN verdict
   (ContractableUnitState.PROVEN).
3. Relation evidence — a non-empty string describing the compositional
   basis.

If any input is absent, invalid, or from a non-PROVEN verdict, the
operation is refused with a named `FailureCode`.

### 1.1 Forbidden raw inputs

The operation does NOT accept:
- `DalOnlyCandidate` directly
- `VerbalMadlulCandidate` directly
- `DalMadlulBindingCandidate` directly
- Any carrier prior to `ContractableUnitGeometry`

Only `ContractableUnitGeometry` (proven objecthood) may enter the
relation gate.

## 2. RelationEvidence fields

```text
RelationEvidence:
    governor     : ContractableUnitGeometry  — the governing unit
    dependent    : ContractableUnitGeometry  — the governed unit
    relation_basis : str                     — composition evidence string
    governor_role_claim : str                — claimed role for governor
    dependent_role_claim : str               — claimed role for dependent
```

### 2.1 Role re-gating requirement

The `governor_role_claim` must appear in the governor's
`contractability_profile.admissible_roles` AND must NOT appear in its
`blocked_roles`.

The `dependent_role_claim` must appear in the dependent's
`contractability_profile.admissible_roles` AND must NOT appear in its
`blocked_roles`.

These role claims are re-gated at relation time — they are NOT
inherited as final syntax roles from the ContractabilityProfile. The
ContractabilityProfile only provides the affordance vocabulary; the
RelationCandidate performs an independent gate check.

## 3. RelationCandidate fields

```text
RelationCandidate:
    governor          : ContractableUnitGeometry
    dependent         : ContractableUnitGeometry
    relation_basis    : str
    governor_role     : str  — re-gated role (affordance, not final syntax)
    dependent_role    : str  — re-gated role (affordance, not final syntax)
    relation_rank     : Rank
    residuals         : tuple[Residual, ...]
    trace_ref         : str
```

## 4. Relation operation: `prove_relation_candidate()`

The operation is a **pure function** with the following signature:

```text
prove_relation_candidate(
    governor             : ContractableUnitGeometry,
    dependent            : ContractableUnitGeometry,
    relation_basis       : str,
    governor_role_claim  : str,
    dependent_role_claim : str,
) -> RelationVerdict
```

### Input boundary (refuses with named FailureCode):

- `governor` must be a `ContractableUnitGeometry` instance.
- `dependent` must be a `ContractableUnitGeometry` instance.
- `relation_basis` must be a non-empty string.
- `governor_role_claim` must be a non-empty string.
- `dependent_role_claim` must be a non-empty string.

### Role re-gating (refuses with named FailureCode):

- `governor_role_claim` must appear in
  `governor.contractability_profile.admissible_roles`.
- `governor_role_claim` must NOT appear in
  `governor.contractability_profile.blocked_roles`.
- `dependent_role_claim` must appear in
  `dependent.contractability_profile.admissible_roles`.
- `dependent_role_claim` must NOT appear in
  `dependent.contractability_profile.blocked_roles`.

If any role is not admissible or is blocked, the operation refuses
with `FailureCode.GATE_REQUIRED`.

### Residual governance:

Residuals are merged from both unit inputs:
`governor.residuals + dependent.residuals`

Any `ResidualKind.HIDDEN_FORBIDDEN` or `ResidualKind.BLOCKING`
residual triggers an immediate refusal:
- HIDDEN_FORBIDDEN -> `FailureCode.HIDDEN_RESIDUAL`
- BLOCKING -> `FailureCode.BLOCKING_RESIDUAL_PRESENT`

### Rank bounding:

```text
relation_rank = RankLattice.meet(
    governor.objecthood_rank,
    dependent.objecthood_rank,
    RELATION_CANDIDATE_RANK_CEILING,
)
```

The relation candidate rank ceiling equals
`CONTRACTABLE_UNIT_RANK_CEILING`.

### Output:

- On success: `COMPOSED` with a `RelationCandidate`.
- On refusal: `REFUSED` with a named `FailureCode`.

## 5. RelationVerdict

```text
RelationVerdict:
    candidate       : RelationCandidate | None
    verdict_state   : RelationState (COMPOSED | REFUSED)
    failure_code    : FailureCode | None
    verdict_rank    : Rank
    residuals       : tuple[Residual, ...]
    trace_ref       : str
```

State invariants:
- COMPOSED -> candidate is not None, failure_code is None.
- REFUSED -> candidate is None, failure_code is a named FailureCode.

## 6. Forbidden outputs (proven absent)

- meaning, reference, denotation, concept
- ifadah, hukm, reality, ontology, truth-value
- IfadahCandidate (PR-20)
- HukmCandidate (PR-21)
- ExtraLetterLicense, C_Aug
- semantic/wadʿi/dalālah lexicon access
- dalālah mutabaqah/tadammun/iltizam
- new FailureCode members
- new runtime dependencies
- SyntaxRole assignment (role claims are re-gated affordance, not final)
- direct raw candidate input (DalOnlyCandidate, VerbalMadlulCandidate,
  DalMadlulBindingCandidate)

## 7. Constitutional invariants

1. `RelationCandidate ≠ Meaning` — the relation is structural,
   never semantic.
2. `RelationCandidate ≠ Ifadah` — the relation does not produce
   propositions.
3. `RelationCandidate ≠ Hukm` — the relation does not judge.
4. `RelationCandidate ≠ Reality` — the relation does not correspond
   to reality.
5. `ContractabilityProfile` strings are affordance labels — they are
   NOT final syntax roles.
6. `RelationCandidate` must re-gate admissible_roles; it does not
   inherit role standing from the profile.
7. The relation candidate proves composition affordance and licenses
   PR-20 (IfadahCandidate) and nothing else.
8. Every refusal carries a named `FailureCode`.
9. No rank promotion beyond `RELATION_CANDIDATE_RANK_CEILING`.
10. No hidden or blocking residuals pass.
11. `prove_relation_candidate()` is pure: no I/O, no ledger, no network.
12. No composition from raw candidates — only ContractableUnitGeometry
    may enter.

## 8. Open residuals (declared but not closed by PR-19)

The following capabilities are **not licensed** by PR-19 and remain
open residuals to be closed by later PRs:

1. **Arabic formal shape vocabulary** — `ContractabilityProfile` strings
   (`admissible_roles`, `blocked_roles`, `word_class_affordance`,
   `inflection_affordance`, `derivational_affordance`) are open strings.
   PR-19 does not supply a proven formal shape dictionary. The strings
   are affordance labels only — they carry no proven Arabic grammatical
   standing until a Formal Shape Registry (PR-F1 through PR-F7) closes
   them with proven types.
2. **Formal role re-gating** — the role re-gating in §4 checks string
   membership only. It does not prove that the claimed role is a
   constitutionally licensed Arabic grammatical category. Proven
   category standing requires a Formal Shape Registry entry.
3. **Composition pattern classification** — `relation_basis` is a
   free-form evidence string. PR-19 does not classify composition
   patterns (nominal sentence, verbal sentence, iḍāfa, etc.) into
   proven types.
4. **Semantic eligibility gate** — PR-19 produces a RelationCandidate
   but does not gate semantic lexicon access. The gate from composition
   affordance to IfādahCandidate (PR-20) is not opened here.

These residuals do not invalidate PR-19 — they declare the boundary
between what PR-19 proves (generic relation affordance) and what
later PRs must prove (formal Arabic categories, composition patterns,
and semantic eligibility).
