# 25 — Lexical / Samāʿ / Qiyās License Boundary Law

> **Status:** Constitutional law. Ratified in PR-14; chain position
> ratified by Amendment-3
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). This
> document is the law that the licensing boundary verdicts implement.
>
> PR-13 weighed minimally — pattern-space fit only.
> PR-14 decides boundary eligibility — never meaning.
>
> PR-14 does not produce lexical meaning.
> PR-14 does not license qiyās generation.
> PR-14 does not generalize samāʿ.
> PR-14 only decides whether the pre-lexical weight-fit result
> may approach lexical / samāʿ / qiyās licensing boundaries.

## 1. The governing principle

```text
PR-13 = fit in pattern-space.
PR-14 = license boundary in lexical / samāʿ / qiyās space.
PR-14 does not produce lexical madlul.

WeightFitCandidate + BoundaryEvidence
→ LicensingBoundaryVerdict

LicensingBoundaryVerdict ≠ LexicalMadlulCandidate.
LicensingBoundaryVerdict ≠ LicensedWeight.
LicensingBoundaryVerdict ≠ DiscoverWeightAlgorithm.
LicensingBoundaryVerdict ≠ GeneratedQiyasForm.
LicensingBoundaryVerdict ≠ meaning.
LicensingBoundaryVerdict ≠ ifādah.
LicensingBoundaryVerdict ≠ agency.
LicensingBoundaryVerdict ≠ hukm.
LicensingBoundaryVerdict ≠ reality.

LicensingBoundaryVerdict is a boundary eligibility assessment.
It tells whether the fit-assessed form may approach a licensing
boundary — nothing more.
```

## 2. The three boundary kinds

### 2.1 Lexical boundary

```text
LexicalBoundaryVerdict decides whether a WeightFitCandidate
is eligible to approach the lexical licensing gate.

LexicalBoundaryVerdict ≠ LexicalMeaning.
LexicalBoundaryVerdict ≠ LexicalEntry.
LexicalBoundaryVerdict ≠ LexicalMadlul.

Lexical boundary is not lexical meaning.
It is eligibility, not content.
```

### 2.2 Samāʿ boundary

```text
SamāʿBoundaryVerdict decides whether a WeightFitCandidate
has attested occurrence evidence.

Samāʿ licenses attested occurrence only, not generalization.
An attested form does not license analogy upon itself.
An attested form does not license extension beyond its attestation.

SamāʿBoundaryVerdict ≠ GeneralizedRule.
SamāʿBoundaryVerdict ≠ QiyāsBase.
SamāʿBoundaryVerdict ≠ LexicalMeaning.
```

### 2.3 Qiyās boundary

```text
QiyāsBoundaryVerdict decides whether a WeightFitCandidate
is eligible to approach the qiyās licensing gate.

Qiyās boundary eligibility requires:
  1. A preserved root (asl mahfuz).
  2. An effective description (wasf mu'aththir).
  3. Absence of a disqualifying difference (farq qadih).

QiyāsBoundaryVerdict ≠ GeneratedWord.
QiyāsBoundaryVerdict ≠ LicensedWeight.
QiyāsBoundaryVerdict ≠ LexicalMeaning.
QiyāsBoundaryVerdict ≠ QiyāsDerivation.

Qiyās licenses boundary eligibility only, not generation.
A qiyās-eligible form is not a generated form.
```

## 3. The assess_license() operation

### 3.1 Signature

```text
assess_license : (candidate: WeightFitCandidate,
                  evidence: BoundaryEvidence,
                  governance: ResidualGovernanceVerdict)
               → LicensingBoundaryResult

The boundary kind is carried inside BoundaryEvidence.kind.
```

### 3.2 Input boundary

```text
assess_license() accepts ONLY a WeightFitCandidate.

Refused inputs (named FailureCode on refusal):
  - raw carriers (SyllableCandidate, WordCarrierCandidate, etc.)
  - PathKind values
  - PathGateVerdict values
  - WeightReadinessCandidate (must be weighed first)
  - any object that is not a WeightFitCandidate

The input boundary is absolute: no shortcut from any earlier
stage to licensing boundary assessment is permitted.
```

### 3.3 Evidence requirement

```text
assess_license() requires a BoundaryEvidence.
A missing or invalid evidence produces a named refusal.

BoundaryEvidence carries:
  - kind: LicenseBoundaryKind (LEXICAL | SAMAA | QIYAS)
  - attestation: str (the evidence surface)
  - evidence_rank: Rank (bounded)
  - domain: str (the evidence domain)

For QIYAS kind, additional fields are required:
  - preserved_root: str (the asl)
  - effective_description: str (the wasf)
  - no_disqualifying_difference: bool (farq qadih absent)
```

### 3.4 Governance requirement

```text
assess_license() requires a ResidualGovernanceVerdict from Ω.
A non-GRANTED governance produces a named refusal.
Only GRANTED governance permits the boundary assessment to proceed.
```

### 3.5 Output: LicensingBoundaryResult

```text
LicensingBoundaryResult contains:
  - state: LicensingBoundaryState (ELIGIBLE | REFUSED | DEFERRED)
  - failure_code: FailureCode | None
  - verdict: LicensingBoundaryVerdict | None
  - rank: Rank (bounded)
  - residuals: tuple[Residual, ...]
  - trace_ref: str

Invariants:
  - ELIGIBLE iff failure_code is None and verdict is not None
  - REFUSED iff failure_code is not None and verdict is None
  - DEFERRED iff failure_code is not None (verdict is None)
  - rank never exceeds LICENSE_BOUNDARY_RANK_CEILING
  - residuals are always visible
```

## 4. LicensingBoundaryVerdict

### 4.1 Shape

```text
LicensingBoundaryVerdict carries:
  - source: WeightFitCandidate (the fit that was assessed)
  - boundary_kind: LicenseBoundaryKind
  - eligibility_verdict: str (the boundary assessment)
  - eligibility_rank: Rank (bounded)
  - evidence_summary: str (what evidence was evaluated)

LicensingBoundaryVerdict does NOT carry:
  - meaning, madlul, dalālah, ifādah
  - agency, patienthood, fāʿil, mafʿūl
  - hukm, iʿrāb, real events
  - lexical entry content, lexical definition
  - generated qiyās form
  - weight family, weight discovery algorithm
  - extra-letter license
  - augmentation category (𝒞_Aug)
  - ContractableUnitGeometry
  - LicensedWeight
```

### 4.2 Identity discipline

```text
LicensingBoundaryVerdict is a boundary eligibility assessment.
It tells whether the form may approach a licensing gate.
It does not tell what the form means.
It does not generate new forms.
It does not generalize attested forms.
It does not license the form to act.
```

## 5. Rank discipline

```text
LICENSE_BOUNDARY_RANK_CEILING = WEIGHT_FIT_RANK_CEILING = Rank.HYPOTHESIS

assess_license() may not promote rank beyond this ceiling.
LicensingBoundaryVerdict.eligibility_rank ≤ LICENSE_BOUNDARY_RANK_CEILING.
No rank promotion without a gate.
```

## 6. Residual governance inheritance

```text
assess_license() inherits PR-12 residual governance:
  - HIDDEN_FORBIDDEN → REJECTED
  - BLOCKING → refused
  - DEFERRABLE → deferred
  - NON_BLOCKING + EXPLANATORY → may proceed

Residuals from the governance verdict are carried onto the result.
No residual is erased or hidden by assess_license().
```

## 7. Samāʿ / qiyās specific rules

### 7.1 Samāʿ attestation is not generalization

```text
Samāʿ attestation licenses occurrence.
It does not license generalization.
An attested form is evidence of existence, not of rule.
No system may use a samāʿ-attested form as a qiyās base
without an independent qiyās eligibility assessment.
```

### 7.2 Qiyās eligibility is not generation

```text
Qiyās eligibility decides whether the path to analogy is open.
It does not walk that path.
It does not produce a new form.
It does not prove the analogy valid.

Three conditions must be present for ELIGIBLE:
  1. preserved_root is non-empty (the asl exists).
  2. effective_description is non-empty (the wasf is articulated).
  3. no_disqualifying_difference is True (no farq qadih).

If any condition fails, the result is REFUSED with a named
FailureCode. No partial eligibility.
```

## 8. Trace discipline

```text
trace_ref in LicensingBoundaryResult is a reference.
trace_ref is NOT an audit ledger commit.
trace_ref documents the decision path, not a ledger write.
TraceRef ≠ TraceLedgerCommit.
```

## 9. FailureCode discipline

```text
PR-14 uses ONLY existing FailureCode members from the PR-1A taxonomy.
No new FailureCode members are introduced.

Mapping:
  - missing/invalid candidate → GATE_REQUIRED
  - missing/invalid evidence → GATE_REQUIRED
  - unlicensed boundary approach → UNLICENSED_OPENING
  - qiyās without preserved root → FORBIDDEN_STRAIGHT_LINE
  - qiyās without effective description → FORBIDDEN_STRAIGHT_LINE
  - qiyās with disqualifying difference → FORBIDDEN_STRAIGHT_LINE
  - samāʿ without attestation → GATE_REQUIRED
  - governance non-GRANTED → inherits governance failure_code
  - hidden residual → HIDDEN_RESIDUAL
  - blocking residual → BLOCKING_RESIDUAL_PRESENT
  - rank above ceiling → RANK_EXCEEDS_CEILING
```

## 10. Forbidden content in PR-14

```text
No LexicalMadlulCandidate.
No LicensedWeight.
No DiscoverWeightAlgorithm.
No GeneratedQiyasForm.
No WeightFamilyCandidate.
No ExtraLetterLicense.
No ContractableUnitGeometry.
No AugmentationCategory / 𝒞_Aug.
No meaning, ifādah, agency, hukm, or reality fields.
No new FailureCode members.
No new runtime dependencies.
No audit ledger writes.
No adapter or audit layer changes.
No kernel, gate, or schema changes.
```

## 11. Closing deferred samāʿ preventers

```text
The samāʿ-grounded preventers left DEFERRED by PR-11 and PR-12
close here as follows:

A samāʿ-attested form that was DEFERRED in an earlier path gate
may now be assessed: if BoundaryEvidence of kind SAMAA carries
a non-empty attestation and passes Ω governance, the verdict is
ELIGIBLE — the deferral is resolved.

If the attestation is empty or governance is non-GRANTED, the
deferral becomes a REFUSED with a named FailureCode.

No samāʿ attestation retroactively overrides a REFUSED path gate.
Only DEFERRED verdicts from earlier stages can be closed here.
```

## 12. Golden law

```text
PR-13 weighs minimally — pattern-space fit only.
PR-14 assesses boundary eligibility — never meaning.

The boundary verdict is an eligibility assessment, not a license.
It opens a gate to the next layer, it does not cross it.

PathGateVerdict opens the path.
μ-chain prepares the carrier.
ΩResidualGovernance governs residuals.
WeightReadinessCandidate establishes readiness.
WeightFitCandidate establishes fit.
LicensingBoundaryVerdict establishes eligibility.
None of them licenses the final weight.
```
