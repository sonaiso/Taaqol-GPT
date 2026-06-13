# 26 — DalOnlyCandidate Boundary Law

> **Status:** Constitutional law. Ratified in PR-15; chain position
> ratified by Amendment-4
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). This
> document is the law that the DalOnlyCandidate boundary implements.
>
> PR-14 closed boundary eligibility — never meaning.
> PR-15 proves the signifier alone — never signified.
>
> PR-15 does not produce verbal signified (madlul lafzi).
> PR-15 does not produce binding (dal-madlul).
> PR-15 does not produce meaning, ifadah, hukm, or reality.
> PR-15 only proves that a signifier surface stands independently
> before any signified is considered.

## 1. The governing principle

```text
PR-14 = boundary eligibility in lexical / samaa / qiyas space.
PR-15 = signifier-alone candidacy in pre-semantic space.
PR-15 does not produce verbal signified.

LicensingBoundaryVerdict + signifier surface
-> DalOnlyCandidate

DalOnlyCandidate != VerbalMadlulCandidate.
DalOnlyCandidate != DalMadlulBindingCandidate.
DalOnlyCandidate != LexicalMadlul.
DalOnlyCandidate != Meaning.
DalOnlyCandidate != Ifadah.
DalOnlyCandidate != Hukm.
DalOnlyCandidate != Reality.
DalOnlyCandidate != ContractableUnitGeometry.
DalOnlyCandidate != ExtraLetterLicense.
DalOnlyCandidate != RelationCandidate.

DalOnlyCandidate is a signifier identity proof.
It tells whether the signifier surface can stand independently
as a boundary-proven candidate — nothing more.
```

## 2. What DalOnlyCandidate carries

### 2.1 Required fields

```text
DalOnlyCandidate carries:
  - signifier_identity: str (the signifier surface identity)
  - phonetic_trace_ref: str (reference to phonetic trace)
  - graphic_trace_ref: str (reference to graphic trace, may be empty
    for oral-only forms)
  - prior_licensing_verdict: LicensingBoundaryVerdict (from PR-14)
  - dal_rank: Rank (bounded)
  - residuals: tuple[Residual, ...] (governed)
  - trace_ref: str (reference, not ledger commit)
```

### 2.2 Forbidden fields

```text
DalOnlyCandidate does NOT carry:
  - meaning, madlul, dalalah, ifadah
  - agency, patienthood, fa'il, maf'ul
  - hukm, i'rab, real events
  - verbal signified (madlul lafzi)
  - binding (dal-madlul)
  - conceptual correspondence
  - lexical entry content, lexical definition
  - generated qiyas form
  - weight family, weight discovery algorithm
  - extra-letter license
  - augmentation category (C_Aug)
  - ContractableUnitGeometry
  - LicensedWeight
  - RelationCandidate
  - IfadahCandidate
  - HukmCandidate
  - TanzilCandidate
```

## 3. Input boundary

```text
DalOnlyCandidate requires a LicensingBoundaryVerdict as prior.
A signifier without a prior licensing boundary verdict is ungated.

Refused inputs (named FailureCode on refusal):
  - raw surface strings without a licensing verdict
  - WeightFitCandidate alone (must pass through assess_license first)
  - WeightReadinessCandidate (must be weighed and licensed first)
  - any object that is not a LicensingBoundaryVerdict

The input boundary is absolute: no shortcut from any earlier
stage to signifier candidacy is permitted.
```

## 4. DalBoundaryVerdict

### 4.1 Shape

```text
DalBoundaryVerdict carries:
  - candidate: DalOnlyCandidate (the proven signifier)
  - verdict_state: DalBoundaryState (PROVEN | REFUSED)
  - failure_code: FailureCode | None
  - verdict_rank: Rank (bounded)
  - residuals: tuple[Residual, ...] (visible)
  - trace_ref: str (reference, not ledger commit)

DalBoundaryVerdict does NOT carry:
  - meaning, madlul, dalalah, ifadah
  - agency, patienthood, fa'il, maf'ul
  - hukm, i'rab, real events
  - verbal signified (madlul lafzi)
  - ContractableUnitGeometry
  - ExtraLetterLicense
  - augmentation category (C_Aug)
  - LicensedWeight
```

### 4.2 Identity discipline

```text
DalBoundaryVerdict is a signifier candidacy proof.
It tells whether the signifier surface can stand independently.
It does not tell what the signifier means.
It does not produce a verbal signified.
It does not bind signifier to signified.
It does not generate new forms.
It does not license meaning.
```

## 5. Rank discipline

```text
DAL_BOUNDARY_RANK_CEILING = LICENSE_BOUNDARY_RANK_CEILING = Rank.HYPOTHESIS

DalOnlyCandidate.dal_rank <= DAL_BOUNDARY_RANK_CEILING.
DalBoundaryVerdict.verdict_rank <= DAL_BOUNDARY_RANK_CEILING.
No rank promotion without a gate.
```

## 6. Residual governance

```text
DalOnlyCandidate inherits residual governance from PR-14:
  - HIDDEN_FORBIDDEN -> REFUSED
  - BLOCKING -> refused
  - DEFERRABLE -> deferred
  - NON_BLOCKING + EXPLANATORY -> may proceed

Residuals from the licensing verdict are carried onto the candidate.
No residual is erased or hidden by DalOnlyCandidate construction.
```

## 7. Trace discipline

```text
trace_ref in DalOnlyCandidate is a reference.
trace_ref is NOT an audit ledger commit.
trace_ref documents the decision path, not a ledger write.
TraceRef != TraceLedgerCommit.
```

## 8. FailureCode discipline

```text
PR-15 uses ONLY existing FailureCode members from the PR-1A taxonomy.
No new FailureCode members are introduced.

Mapping:
  - missing/invalid licensing verdict -> GATE_REQUIRED
  - missing signifier identity -> IDENTITY_BROKEN
  - missing phonetic trace ref -> TRACE_MISSING
  - rank above ceiling -> RANK_EXCEEDS_CEILING
  - hidden residual -> HIDDEN_RESIDUAL
  - blocking residual -> BLOCKING_RESIDUAL_PRESENT
  - construction from raw surface without verdict -> FORBIDDEN_STRAIGHT_LINE
```

## 9. Forbidden content in PR-15

```text
No VerbalMadlulCandidate.
No DalMadlulBindingCandidate.
No LexicalMadlul.
No Meaning.
No Ifadah.
No Hukm.
No Reality.
No ContractableUnitGeometry.
No ExtraLetterLicense.
No AugmentationCategory / C_Aug.
No RelationCandidate.
No composition.
No new FailureCode members.
No new runtime dependencies.
No audit ledger writes.
No adapter or audit layer changes.
No kernel, gate, or schema changes.
```

## 10. The candidate-is-not-verdict principle

```text
DalOnlyCandidate is a candidate declaration.
It is not a semantic verdict.
It does not decide what the signifier means.
It declares that the signifier surface exists as a proven
boundary-eligible entity that may later enter the verbal
signified assessment (PR-16).

Candidate declaration != semantic verdict.
Candidate declaration != meaning.
Candidate declaration != binding.
Candidate declaration != ifadah.
```

## 11. Golden law

```text
PR-14 assesses boundary eligibility — never meaning.
PR-15 proves the signifier alone — never signified.

The signifier candidate is a boundary proof, not a meaning claim.
It opens a gate to the next layer (PR-16), it does not cross it.

LicensingBoundaryVerdict establishes eligibility.
DalOnlyCandidate establishes signifier identity.
Neither establishes meaning.

Pre-semantic success is the prevention of meaning claims,
not their production.
```
