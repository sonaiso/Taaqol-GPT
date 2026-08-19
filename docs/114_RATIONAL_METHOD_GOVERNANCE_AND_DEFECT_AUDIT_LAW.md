# 114 — Rational Method Governance and Defect Audit Law (RMG-L0)

> Status: constitutional law document (law-only).
> Scope: define the rational-governance layer above domain-specific methods,
> and separate result truth from method validity and defect causality.
> Snapshot date: 2026-08-19.

## §1 Governing law

```text
Rational method is the constitutional governor.
Domain rules constrain it.
Method specializes it.
Technique executes it.
Instrument serves it.
```

Stronger form:

```text
No method before domain.
No method-license before domain rules.
No evidence-license outside the domain rules that define evidence kind,
scope coverage, and closure criterion.
```

## §2 Constitutional transition chain

The bounded chain is:

```text
Claim
-> Scope
-> Domain
-> DomainRules
-> RationalMethodGovernance
-> Method
-> Technique
-> Instrument
-> Evidence
-> Inference
-> Result
-> Audit
```

This law forbids the shortcut:

```text
Claim -> Method
```

without explicit `Domain` and `DomainRules` binding.

## §3 Rational-governance contract

`RationalMethodGovernance` is the constitutional contract:

```text
RationalMethodGovernance = <
  ClaimBinding,
  ScopeBinding,
  DomainBinding,
  DomainRuleClosure,
  MethodFit,
  EvidenceFit,
  InferenceLicense,
  RankControl,
  ResidualPolicy,
  DefectAuditPolicy,
  TraceRef
>
```

It is a governance boundary, not a runtime method executor.

## §4 Independent assessment axes

Result assessment is multi-axis, not single-boolean:

```text
ResultAssessment = <
  TruthStatus,
  MethodStatus,
  InferenceStatus,
  Rank,
  Defects,
  Residuals
>
```

Constitutional distinctions:

```text
FalseResult != InvalidMethod
LowRank != Falsehood
TruthStatus != EpistemicRank
```

## §5 Defect algebra boundary

This law distinguishes defect classes by failure locus and license type.

```text
DefectType = {
  ERROR,
  FALLACY,
  LIE,
  FORGETTING,
  IGNORANCE,
  UNCERTAINTY,
  CONFLICT
}
```

With constitutional meaning:

```text
ERROR      = FaultInExecution
FALLACY    = FaultInInferenceLicense
LIE        = IntentionalMisrepresentation (only when intention evidence exists)
FORGETTING = PreviouslyAvailableTrace - CurrentRetrievability
IGNORANCE  = MissingRequiredKnowledgeWithoutPriorPossessionProof
UNCERTAINTY = LicensedInsufficientClosureRank
CONFLICT   = Non-reconcilable competing licensed supports in current scope
```

## §6 Repair test (error vs fallacy)

```text
If local correction of value/measurement/transcription restores path validity:
-> ERROR

If correction requires changing the inference license, scope bridge,
or evidence mode:
-> FALLACY
```

This law forbids collapsing both into a single opaque `ERROR` bucket.

## §7 Domain-scoped truth modes

Truth-mode is domain-scoped:

```text
TruthMode = f(Domain, ClaimType)
```

Illustrative constraints:

```text
FormalProof != EmpiricalOccurrenceProof
LinguisticValidity != ExternalRealityClaim
```

Cross-domain transfer remains gated:

```text
Method_D1 -> Method_D2 requires BridgeContract
```

## §8 Audit decomposition law

Audit must expose independent sub-audits:

```text
ResultAudit =
  TruthAudit
+ MethodValidityAudit
+ EvidenceAudit
+ ScopeAudit
+ RankAudit
+ DefectAudit
```

No closure claim is licensed if these dimensions are collapsed into one verdict.

## §9 Boundaries and prohibitions of this step

This step is law-only and does not open runtime execution.

```text
RUNTIME_NOT_OPENED = {
  RationalMethodGovernanceRuntime,
  DefectClassifierRuntime,
  IntentInferenceRuntime,
  NewCertificateOrCommitAuthority,
  SemanticOrHukmOrTruthExternalClosure
}
```

Forbidden in this law step:

- introducing runtime carriers/gates/executors for this branch,
- asserting speaker intent without declared evidence,
- promoting rank from uncertainty to certainty without licensed evidence,
- converting instrument output directly into accepted evidence.

## §10 Next licensed successors (reserved)

This law reserves bounded successors without opening them here:

1. `RMG-C1`: governance carriers only (`ResultAssessment`, `DefectRecord`, policy carriers).
2. `RMG-C2`: defect-classification contract validator (contract-only checks).
3. `RMG-C3`: bounded audit decomposition runtime over existing traces.

Any runtime change before these explicit successors is a `FORBIDDEN_LEAP`.
