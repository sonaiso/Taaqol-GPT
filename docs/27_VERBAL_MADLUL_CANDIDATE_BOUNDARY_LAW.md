# 27 — VerbalMadlulCandidate Boundary Law

> **Status:** Constitutional law. Ratified in PR-16; chain position
> ratified by Amendment-4
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). This
> document is the law that the VerbalMadlulCandidate boundary
> implements.
>
> PR-15 proved the signifier alone — never signified.
> PR-16 proves the verbal signified alone — never meaning.
>
> PR-16 does not produce meaning (dalālah).
> PR-16 does not produce reference certainty.
> PR-16 does not produce binding (dal-madlul).
> PR-16 does not produce ifādah, hukm, or reality.
> PR-16 only proves that a verbal signified surface stands
> independently as a bounded candidate that may later enter the
> dal-madlul binding assessment (PR-17).

## 1. The governing principle

```text
PR-15 = signifier-alone candidacy in pre-semantic space.
PR-16 = verbal-signified-alone candidacy in pre-semantic space.
PR-16 does not produce meaning.

DalOnlyCandidate + wadʿ/usage boundary evidence
-> VerbalMadlulCandidate

VerbalMadlulCandidate != Meaning.
VerbalMadlulCandidate != Reference.
VerbalMadlulCandidate != DalMadlulBindingCandidate.
VerbalMadlulCandidate != ContractableUnitGeometry.
VerbalMadlulCandidate != RelationCandidate.
VerbalMadlulCandidate != Ifādah.
VerbalMadlulCandidate != Hukm.
VerbalMadlulCandidate != Reality.
VerbalMadlulCandidate != ExtraLetterLicense.
VerbalMadlulCandidate != 𝒞_Aug.

VerbalMadlulCandidate is a verbal signified candidacy proof.
It tells whether a verbal signified can stand independently
as a bounded candidate from a proven signifier — nothing more.

DalBoundaryVerdict proves signifier candidacy only.
It does not prove signified candidacy.
```

## 2. What VerbalMadlulCandidate carries

### 2.1 Required fields

```text
VerbalMadlulCandidate carries:
  - dal_only: DalOnlyCandidate (the proven signifier from PR-15)
  - wadʿ_usage_boundary: str (the wadʿ/usage evidence boundary)
  - correspondence_candidate: str (conceptual correspondence as
    candidate, not as final denotation)
  - inclusion_candidate: str (inclusion as candidate,
    not as final concept)
  - iltizam_condition: str (iltizām as condition,
    not as conclusion)
  - existence_carrier_candidate: str (existence affordance as
    candidate, not as ontological claim)
  - event_carrier_candidate: str (event affordance as
    candidate, not as real event)
  - relation_affordance_candidate: str (relation affordance as
    candidate, not as RelationCandidate)
  - madlul_rank: Rank (bounded)
  - residuals: tuple[Residual, ...] (governed)
  - trace_ref: str (reference, not ledger commit)
```

### 2.2 Forbidden fields

```text
VerbalMadlulCandidate does NOT carry:
  - meaning, dalālah, conceptual_meaning, final_meaning
  - reference, final_denotation, reference_certainty
  - binding (dal-madlul), dal_madlul_binding
  - agency, patienthood, fa'il, maf'ul
  - hukm, i'rab, real events
  - ifādah, proposition
  - ContractableUnitGeometry
  - RelationCandidate (as type)
  - ExtraLetterLicense
  - augmentation category (𝒞_Aug)
  - LicensedWeight
  - HukmCandidate
  - TanzilCandidate
```

## 3. Input boundary

```text
VerbalMadlulCandidate requires a DalOnlyCandidate as prior
(or a DalBoundaryVerdict with PROVEN state).
A verbal signified without a proven signifier is ungated.

Refused inputs (named FailureCode on refusal):
  - raw surface strings without a dal boundary verdict
  - LicensingBoundaryVerdict alone (must pass through prove_dal first)
  - WeightFitCandidate alone (too early in the chain)
  - any object that is not a DalOnlyCandidate
  - a DalOnlyCandidate without wadʿ/usage boundary evidence

The input boundary is absolute: no shortcut from any earlier
stage to verbal signified candidacy is permitted.
```

## 4. VerbalMadlulBoundaryVerdict

### 4.1 Shape

```text
VerbalMadlulBoundaryVerdict carries:
  - candidate: VerbalMadlulCandidate (the proven verbal signified)
  - verdict_state: MadlulBoundaryState (PROVEN | REFUSED)
  - failure_code: FailureCode | None
  - verdict_rank: Rank (bounded)
  - residuals: tuple[Residual, ...] (visible)
  - trace_ref: str (reference, not ledger commit)

VerbalMadlulBoundaryVerdict does NOT carry:
  - meaning, dalālah, final_meaning
  - reference, final_denotation
  - binding (dal-madlul)
  - hukm, i'rab, real events
  - ContractableUnitGeometry
  - ExtraLetterLicense
  - augmentation category (𝒞_Aug)
  - LicensedWeight
```

### 4.2 Identity discipline

```text
VerbalMadlulBoundaryVerdict is a verbal signified candidacy proof.
It tells whether a verbal signified can stand independently.
It does not tell what the signifier means.
It does not produce meaning or reference.
It does not bind signifier to signified.
It does not generate new forms.
It does not license denotation.
```

## 5. Rank discipline

```text
MADLUL_BOUNDARY_RANK_CEILING = DAL_BOUNDARY_RANK_CEILING = Rank.HYPOTHESIS

VerbalMadlulCandidate.madlul_rank <= MADLUL_BOUNDARY_RANK_CEILING.
VerbalMadlulBoundaryVerdict.verdict_rank <= MADLUL_BOUNDARY_RANK_CEILING.
No rank promotion without a gate.
```

## 6. Residual governance

```text
VerbalMadlulCandidate inherits residual governance from PR-15:
  - HIDDEN_FORBIDDEN -> REFUSED
  - BLOCKING -> REFUSED
  - DEFERRABLE -> deferred
  - NON_BLOCKING + EXPLANATORY -> may proceed

Residuals from the dal boundary verdict are carried onto the candidate.
No residual is erased or hidden by VerbalMadlulCandidate construction.
```

## 7. Trace discipline

```text
trace_ref in VerbalMadlulCandidate is a reference.
trace_ref is NOT an audit ledger commit.
trace_ref documents the decision path, not a ledger write.
TraceRef != TraceLedgerCommit.
```

## 8. FailureCode discipline

```text
PR-16 uses ONLY existing FailureCode members from the PR-1A taxonomy.
No new FailureCode members are introduced.

Mapping:
  - missing/invalid DalOnlyCandidate -> GATE_REQUIRED
  - missing wadʿ/usage boundary -> BOUNDARY_MISSING
  - rank above ceiling -> RANK_EXCEEDS_CEILING
  - hidden residual -> HIDDEN_RESIDUAL
  - blocking residual -> BLOCKING_RESIDUAL_PRESENT
  - construction from raw surface without verdict -> GATE_REQUIRED
```

## 9. Forbidden content in PR-16

```text
No DalMadlulBindingCandidate.
No Meaning.
No Reference certainty.
No Ifādah.
No Hukm.
No Reality.
No ContractableUnitGeometry.
No ExtraLetterLicense.
No AugmentationCategory / 𝒞_Aug.
No RelationCandidate (as a type — relation_affordance_candidate
is a string field, not a RelationCandidate carrier).
No composition.
No new FailureCode members.
No new runtime dependencies.
No audit ledger writes.
No adapter or audit layer changes.
No kernel, gate, or schema changes.
```

## 10. The candidate-is-not-meaning principle

```text
VerbalMadlulCandidate is a candidate declaration.
It is not a meaning verdict.
It does not decide what the signifier denotes.
It declares that a verbal signified surface exists as a proven
boundary-eligible entity that may later enter the dal-madlul
binding assessment (PR-17).

Candidate declaration != meaning.
Candidate declaration != reference.
Candidate declaration != binding.
Candidate declaration != ifādah.

correspondence_candidate is not final denotation.
inclusion_candidate is not final concept.
iltizam_condition is a condition, not a conclusion.
```

## 11. Golden law

```text
PR-15 proves the signifier alone — never signified.
PR-16 proves the verbal signified alone — never meaning.

The verbal signified candidate is a boundary proof, not a meaning claim.
It opens a gate to the next layer (PR-17), it does not cross it.

DalOnlyCandidate establishes signifier identity.
VerbalMadlulCandidate establishes verbal signified candidacy.
Neither establishes meaning.
Neither establishes binding.

Pre-semantic success is the prevention of meaning claims,
not their production.
```
