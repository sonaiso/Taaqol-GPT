# 114 — Rational Method Governance and Defect Audit Law (RMG-L0.1 Corrective)

> Status: constitutional law document (law-only).
> Scope: corrective hardening for governance hierarchy and type separation:
> keep rational governance as a governor under Z0, separate defect/cognitive/
> intent/evidence/rank axes, and preserve law-only status.
> Snapshot date: 2026-08-19.

## §1 Governing law

```text
Z0Constitution > RationalMethodGovernance > DomainMethod > Technique > Instrument.
```

The rational method layer is a governor over a bounded path, not a sequential
stage within that path:

```text
RMG != Stage_i
RMG = Governor(Path)
```

## §2 Constitutional transition chain

The governed bounded path is:

```text
Z0Kernel
-> RationalMethodGovernanceGovernor
-> [
     Claim
     -> ClaimType
     -> Scope
     -> Domain
     -> DomainRules
     -> MethodPossibilitySpace
     -> MethodContract
     -> Technique
     -> MeansOrInstrument(optional, typed)
     -> RawRecord
     -> EvidenceQualification
     -> Evidence
     -> Inference
     -> Assessment
     -> Audit
   ]
```

Forbidden shortcuts:

```text
Claim -> Method
DomainRules -> Method (automatic selection)
InstrumentOutput -> AcceptedEvidence
```

Method selection is licensed only by:

```text
MethodSelection = f(
  Domain,
  DomainRules,
  ClaimType,
  Scope,
  EvidenceRequirement
)
```

## §3 Rational-governance contract (envelope, not executor)

`RationalMethodGovernance` is the constitutional contract:

```text
RationalMethodGovernance = <
  ClaimBinding,
  ScopeBinding,
  DomainBinding,
  DomainRuleClosure,
  ClaimTypeBinding,
  MethodPossibilitySpace,
  MethodContractFit,
  EvidenceQualificationPolicy,
  InferenceLicense,
  RankControl,
  ResidualPolicy,
  DefectAuditPolicy,
  TraceRef
>
```

It is a governance boundary/envelope under Z0, not a runtime method executor.

## §4 Independent assessment axes

Assessment is multi-axis and typed, not a single defect bucket:

```text
RationalAssessmentEnvelope = <
  ClaimBinding,
  ClaimType,
  Scope,
  Domain,
  DomainRules,
  MethodContract,
  EvidenceContract,
  InferenceStatus,
  AssessmentMode,
  ResultStatus,
  EpistemicRank,
  PathDefects,
  CognitiveState,
  IntentionalState,
  EvidenceState,
  Residuals
  Trace
>
```

Constitutional distinctions:

```text
FalseResult != InvalidMethod
PathDefect != CognitiveState
PathDefect != IntentionalState
PathDefect != EvidenceState
Uncertainty != Defect
Conflict != Defect
ResultStatus != ExternalTruthStatus
```

## §5 Type-separation law (defect vs knowledge vs intent vs evidence)

Only path failures are defects:

```text
PathDefectType = {
  ERROR,
  FALLACY
}
```

Independent axis for cognitive condition:

```text
CognitiveState = {
  KNOWN,
  UNKNOWN,
  IGNORANT,
  FORGOTTEN,
  RETRIEVAL_UNCERTAIN
}
```

Independent axis for intentional stance:

```text
IntentionalState = {
  NOT_APPLICABLE,
  INTENT_UNKNOWN,
  SINCERE_ASSERTION,
  DELIBERATE_MISREPRESENTATION
}
```

Independent axis for evidence topology:

```text
EvidenceState = {
  COHERENT,
  INSUFFICIENT,
  CONFLICTED
}
```

`LIE` is not a base defect label. Deliberate misrepresentation is licensed only
when intentional conditions are evidenced.

## §6 Uncertainty and conflict are licensed states, not defects

```text
Uncertainty != Defect
Conflict != Defect
```

Allowed valid unresolved form:

```text
MethodStatus = VALID
InferenceStatus = VALID
ResultStatus = UNRESOLVED
EpistemicRank = PROBABLE
```

Defect opens only when rank inflation occurs:

```text
RankInflationFallacy = ProbableEvidence -> CertainClaim
```

## §7 Domain-scoped assessment mode and external-truth boundary

```text
AssessmentMode = f(Domain, ClaimType)
ResultStatus in StatusSet(AssessmentMode)
```

External-truth status is out of this layer and remains closed until:

```text
RealityClose
```

Illustrative distinctions:

```text
FormalProof != ExternalTruth
LinguisticValidity != RealityCorrespondence
```

## §8 Means/instrument boundary before evidence

```text
Technique
-> MeansOrInstrument(optional, typed)
-> RawRecord
-> EvidenceQualification
-> Evidence
```

No direct promotion is licensed:

```text
InstrumentOutput -> AcceptedEvidence  (forbidden)
```

## §9 Audit decomposition law (expanded)

Audit must expose domain and inference decomposition:

```text
ResultAudit =
  DomainAudit
+ ClaimTypeAudit
+ MethodFitAudit
+ EvidenceQualificationAudit
+ InferenceAudit
+ ScopeAudit
+ IdentityTraceAudit
+ RankAudit
+ DefectAudit
+ IntentAudit(optional)
```

No closure claim is licensed if these dimensions are collapsed into one verdict.

## §10 Origin and chain-authority declaration

```text
OriginLaw = docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md
ChainAuthority = docs/14_PR_CHAIN_ROADMAP.md
```

`docs/14` records chain position; it is not the origin law for this branch.

## §11 Boundaries and prohibitions of this step

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

## §12 Next licensed successors (reserved)

This law reserves bounded successors without opening them here:

1. `RMG-C1`: governance carriers only (`RationalAssessmentEnvelope`, policy carriers).
2. `RMG-C2`: defect-classification contract validator (contract-only checks).
3. `RMG-C3`: bounded audit decomposition runtime over existing traces.

Any runtime change before these explicit successors is a `FORBIDDEN_LEAP`.
