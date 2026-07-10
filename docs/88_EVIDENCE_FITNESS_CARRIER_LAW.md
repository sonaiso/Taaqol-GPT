# 88 — Evidence Fitness Carrier Boundary Law (EVID-FIT-L0)

> Status: constitutional law document (law-only).
> Scope: shared pre-verifier evidence-fitness carrier boundary before TraceReplayVerifier and Rank/Domain policy.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
EVID-FIT-L0 = قانون الحامل المشترك لملاءمة الدليل قبل التحقق.

EvidenceFitnessCarrier DOES_NOT_IMPLY EvidenceFitnessCertificate
EvidenceFitnessCarrier DOES_NOT_IMPLY Ifadah
EvidenceFitnessCarrier DOES_NOT_IMPLY Hukm
EvidenceFitnessCarrier DOES_NOT_IMPLY Truth
EvidenceFitnessCarrier DOES_NOT_IMPLY RuntimeInference
VerbIdentityReadinessCandidate THROUGH EvidenceFitnessCarrier DOES_NOT_IMPLY EventTruth
NounIdentityReadinessCandidate THROUGH EvidenceFitnessCarrier DOES_NOT_IMPLY FinalMeaning
```

Constitutional rule:

```text
At this layer, the system may package evidence-fitness readiness as a shared carrier only.
No EvidenceFitnessCertificate and no semantic/syntactic/judgment/truth closure are licensed.
Any transition from carrier/readiness naming to certificate or runtime inference at EVID-FIT-L0 is a FORBIDDEN_LEAP.
```

## §2 Branch identity and scope

```text
FAMILY               = EVIDENCE_FITNESS
STEP                 = EVID-FIT-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = SHARED_PRE_VERIFIER_EVIDENCE_FITNESS
OBJECTIVE            = Shared contract surface for evidence-fitness readiness before replay/rank policy
TRANSITION_RULE      = MINIMUM_REQUIREMENT_KERNEL
```

This step is law-only and introduces no runtime carriers implementation, no gate engines,
no parser/morphology/syntax authority runtime, and no semantic/ifadah/hukm/truth execution.

## §3 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  EvidenceFitnessCarrier,
  EvidenceSurfaceRef,
  UpstreamReadinessRef,
  DomainScopeRef,
  RankCeilingRef,
  ResidualVisibilityRef,
  TraceReplayDemandSurface,
  RankPolicyDemandSurface,
  PolicyPreconditionSurface
}
```

## §4 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUT_ASSERTIONS = {
  EvidenceFitnessCarrier -> EvidenceFitnessCertificate,
  EvidenceFitnessCarrier -> RuntimeInferenceVerdict,
  EvidenceFitnessCarrier -> Ifadah,
  EvidenceFitnessCarrier -> Hukm,
  EvidenceFitnessCarrier -> Truth,
  VerbReadiness -> EventTruth via EvidenceFitnessCarrier,
  NounReadiness -> FinalMeaning via EvidenceFitnessCarrier
}
```

```text
FORBIDDEN_OUTPUTS = {
  EvidenceFitnessCertificate,
  RuntimeInferenceVerdict,
  FinalEventMeaning,
  FinalMeaning,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality,
  FinalSyntacticRole,
  FinalSourceCertificate
}
```

## §5 Minimum requirement kernel (MRK)

`MRK(EvidenceFitnessCarrier)` requires the declared surface fields:

1. `CarrierIdentity`
2. `EvidenceSurfaceRef`
3. `UpstreamReadinessRef`
4. `DomainScopeRef`
5. `RankCeilingRef`
6. `ResidualVisibilityRef`
7. `TraceReplayDemandSurface`
8. `RankPolicyDemandSurface`
9. `ForbiddenOutputs`
10. `TraceRef`

Constitutional note:

```text
MRK closes carrier identity only.
MRK does not issue certificate, runtime inference, ifadah, hukm, truth, or role closure.
```

## §6 Residual vocabulary (local)

```text
EVIDENCE_SURFACE_MISSING
UPSTREAM_READINESS_MISSING
TRACE_REF_MISSING
RANK_CEILING_UNDECLARED
DOMAIN_SCOPE_UNDECLARED
RESIDUAL_VISIBILITY_MISSING
CERTIFICATE_JUMP_BLOCKED
INFERENCE_JUMP_BLOCKED
TRUTH_CLOSURE_BLOCKED
IFADAH_HUKM_CLOSURE_BLOCKED
```

Classification discipline:

- `CERTIFICATE_JUMP_BLOCKED` blocks conversion from carrier to certificate.
- `INFERENCE_JUMP_BLOCKED` blocks any runtime inference claim at this layer.
- `TRUTH_CLOSURE_BLOCKED` and `IFADAH_HUKM_CLOSURE_BLOCKED` preserve pre-closure status.

## §7 Runtime embargo and safe sequencing

```text
RUNTIME_NOT_OPENED = {
  src_runtime_implementation,
  parser_changes,
  morphology_runtime,
  syntax_authority,
  semantic_runtime,
  ifadah_engine,
  hukm_engine,
  truth_engine,
  evidence_fitness_verifier_runtime,
  evidence_fitness_certificate_runtime,
  runtime_inference_engine
}
```

Safe constitutional sequencing:

```text
NOUN-L0 / VERB-L0 / REF-PRON-L0 / ZARF-L0 / LGE-LINK-L0
-> EvidenceFitnessCarrier
-> TraceReplayVerifier
-> RankVector/DomainPolicy
-> Branch-specific carrier/runtime steps (for example VERB-C1)
```

## §8 Constitutional minimum examples (surface-only)

Example 1:

```text
Input: VerbIdentityReadinessCandidate("ضرب")
Output: EvidenceFitnessCarrier LICENSED + TraceReplayDemandSurface + RankPolicyDemandSurface
Forbidden: EvidenceFitnessCertificate / EventTruth / Ifadah / Hukm / Truth
```

Example 2:

```text
Input: NounIdentityReadinessCandidate("جبل")
Output: EvidenceFitnessCarrier LICENSED + DomainScopeRef + ResidualVisibilityRef
Forbidden: FinalMeaning / RuntimeInferenceVerdict
```

Example 3:

```text
Input: EvidenceFitnessCarrier(without TraceRef)
Output: EvidenceFitnessCarrier remains pending with TRACE_REF_MISSING
Forbidden: EvidenceFitnessCertificate
```
