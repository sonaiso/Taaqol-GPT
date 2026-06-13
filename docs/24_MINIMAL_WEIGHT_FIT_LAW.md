# 24 — Minimal Weight Fit Law

> **Status:** Constitutional law. Ratified in PR-13; chain position
> ratified by Amendment-3
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). This
> document is the law that the minimal `weigh()` operation and
> `WeightFitCandidate` implement.
>
> PR-12 introduced Ω governance and the μ chain.
> PR-12 prepared the lawful object for weighing.
> PR-13 weighs minimally.
> PR-13 does not license weight as meaning, family, lexicon, samāʿ,
> qiyās, or augmentation.

## 1. The governing principle

```text
PR-12 = governance without weighing.
PR-13 = weighing without meaning.

WeightReadinessCandidate is the only lawful input to weigh().
WeightFitCandidate is the only lawful output of weigh().

WeightFitCandidate ≠ LicensedWeight.
WeightFitCandidate ≠ WeightFamilyCandidate.
WeightFitCandidate ≠ LexicalMadlul.
WeightFitCandidate ≠ meaning.
WeightFitCandidate ≠ agency.
WeightFitCandidate ≠ hukm.
WeightFitCandidate ≠ reality.

WeightFitCandidate is a pattern-space fit assessment.
It tells whether the form fits its pattern — nothing more.
```

## 2. The weigh() operation

### 2.1 Signature

```text
weigh : (candidate: WeightReadinessCandidate,
         governance: ResidualGovernanceVerdict)
      → WeightFitResult
```

### 2.2 Input boundary

```text
weigh() accepts ONLY a WeightReadinessCandidate.

Refused inputs (named FailureCode on refusal):
  - raw carriers (SyllableCandidate, WordCarrierCandidate, etc.)
  - PathKind values
  - PathGateVerdict values
  - PreWeightSurface without weight-readiness wrapping
  - any object that is not a WeightReadinessCandidate

The input boundary is absolute: no shortcut from any earlier
stage to weighing is permitted.
```

### 2.3 Governance requirement

```text
weigh() requires a ResidualGovernanceVerdict from Ω.
A non-GRANTED governance produces a named refusal.
Only GRANTED governance permits the fit operation to proceed.
```

### 2.4 Output: WeightFitResult

```text
WeightFitResult contains:
  - state: WeightFitState (FITTED | REFUSED | DEFERRED)
  - failure_code: FailureCode | None
  - candidate: WeightFitCandidate | None
  - rank: Rank (bounded)
  - residuals: tuple[Residual, ...]
  - trace_ref: str

Invariants:
  - FITTED iff failure_code is None and candidate is not None
  - REFUSED iff failure_code is not None and candidate is None
  - DEFERRED iff failure_code is not None (candidate may be None)
  - rank never exceeds WEIGHT_FIT_RANK_CEILING
  - residuals are always visible
```

## 3. WeightFitCandidate

### 3.1 Shape

```text
WeightFitCandidate carries:
  - the 9 mandatory WeightCarrierBase fields
  - source: WeightReadinessCandidate (the input that was weighed)
  - fit_verdict: str (the pattern-space fit assessment)
  - fit_rank: Rank (the fit quality rank, bounded)

WeightFitCandidate does NOT carry:
  - meaning, madlul, dalālah
  - agency, patienthood, fāʿil, mafʿūl
  - hukm, iʿrāb, real events
  - lexical entry, samāʿ attestation, qiyās derivation
  - weight family, weight discovery algorithm
  - extra-letter license
  - augmentation category (𝒞_Aug)
```

### 3.2 Identity discipline

```text
WeightFitCandidate is a bounded fit assessment.
It tells whether the form fits a pattern shape.
It does not tell what the form means.
It does not tell what the form does.
It does not license the form to act.
```

## 4. Rank discipline

```text
WEIGHT_FIT_RANK_CEILING = MU_CHAIN_RANK_CEILING = Rank.HYPOTHESIS

weigh() may not promote rank beyond this ceiling.
WeightFitCandidate.fit_rank ≤ WEIGHT_FIT_RANK_CEILING.
No rank promotion without a gate.
```

## 5. Residual governance inheritance

```text
weigh() inherits PR-12 residual governance:
  - HIDDEN_FORBIDDEN → REJECTED
  - BLOCKING → refused
  - DEFERRABLE → deferred
  - NON_BLOCKING + EXPLANATORY → may proceed

Residuals from the governance verdict are carried onto the result.
No residual is erased or hidden by weigh().
```

## 6. Trace discipline

```text
trace_ref in WeightFitResult is a reference.
trace_ref is NOT an audit ledger commit.
trace_ref documents the decision path, not a ledger write.
TraceRef ≠ TraceLedgerCommit.
```

## 7. Forbidden content in PR-13

```text
No LicensedWeight.
No DiscoverWeightAlgorithm.
No WeightFamilyCandidate.
No lexical / samāʿ / qiyās licensing.
No extra-letter licensing.
No ContractableUnitGeometry.
No AugmentationCategory / 𝒞_Aug.
No meaning, agency, hukm, or reality fields.
No new runtime dependencies.
No audit ledger writes.
No adapter or audit layer changes.
No kernel, gate, or schema changes.
No new FailureCode members.
```

## 8. Golden law

```text
PR-12 prepares the lawful object for weighing.
PR-13 weighs minimally.
PR-13 does not license weight as meaning, family, lexicon,
samāʿ, qiyās, or augmentation.

The fit is a PatternSpace operation.
The fit produces a candidate, not a license.
```
