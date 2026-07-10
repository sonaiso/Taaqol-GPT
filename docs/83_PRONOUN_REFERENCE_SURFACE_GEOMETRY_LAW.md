# 83 — Pronoun Reference Surface Geometry Law (REF-PRON-L0)

> Status: constitutional law document (law-only).
> Scope: pronoun-reference surface geometry as reference-demand openers only.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
A pronoun does not resolve reference by itself.
A pronoun opens a reference-demand surface only.

PronounSurface DOES_NOT_IMPLY ReferenceResolved
PronounSurface DOES_NOT_IMPLY Ifadah
PronounSurface DOES_NOT_IMPLY Hukm
PronounSurface DOES_NOT_IMPLY Truth
```

Constitutional rule:

```text
PronounCandidate -> ReferenceDemandSurface only.
ReferenceDemandSurface -> ContractReadiness only after MRK.
ContractReadiness DOES_NOT_IMPLY FinalReferenceCertificate.
```

## §2 Branch identity and scope

```text
FAMILY               = REF-PRON
STEP                 = REF-PRON-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = PRONOUN_REFERENCE_SURFACE_GEOMETRY
OBJECTIVE            = PronounSurface -> ReferenceDemandSurface -> ContractReadinessCandidate
TRANSITION_RULE      = MINIMUM_REQUIREMENT_KERNEL
```

This step is law-only and introduces no runtime carriers, no gate engines,
no parser/syntax authority, and no semantic/ifadah/hukm/truth execution.

## §3 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  DetachedPronounCandidate,
  AttachedPronounCandidate,
  ReferenceDemandSurface,
  ReferenceContractReadiness,
  CompositionReadinessCandidate,
  RoleReadinessCandidate,
  IdafaReadinessCandidate
}
```

## §4 Pronoun classes and attachment modes

```text
DETACHED_PRONOUN_SET = {
  أنا، نحن، أنتَ، أنتِ، أنتما، أنتم، أنتن، هو، هي، هما، هم، هن
}
```

```text
ATTACHED_PRONOUN_SET = {
  VerbAttachedPronoun,
  NounAttachedPronoun,
  ParticleAttachedPronoun
}
```

Boundary rules:

```text
AttachedPronoun DOES_NOT_IMPLY FinalReference
AttachedPronoun DOES_NOT_IMPLY SyntacticRoleFinal
AttachedPronoun DOES_NOT_IMPLY Ifadah
```

## §5 Minimal requirement kernel (MRK)

`MRK(PronounCandidate)` requires all declared surface dimensions:

1. `PronounIdentity`
2. `PronounClass`
3. `AttachmentMode`
4. `PersonNumberGenderFeatures`
5. `HostOrAntecedentDemand`
6. `CaseRoleReadinessSurface`
7. `ReferenceSearchDomain`
8. `VisibleResiduals`
9. `TraceRef`
10. `ForbiddenOutputs`

Constitutional note:

```text
After MRK, pronoun output is ReferenceContractReadiness only.
MRK completion does not issue FinalReferenceCertificate.
```

## §6 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUTS = {
  PronounSurface -> ReferenceResolved,
  PronounSurface -> Ifadah,
  PronounSurface -> Hukm,
  PronounSurface -> Truth,
  PronounCandidate -> FinalReferenceCertificate,
  AttachedPronoun -> FinalReference,
  AttachedPronoun -> SyntacticRoleFinal
}
```

```text
FORBIDDEN_OUTPUTS = {
  ReferenceResolved,
  FinalReferenceCertificate,
  FinalReference,
  FinalMeaning,
  FinalOwnershipMeaning,
  FinalObjecthood,
  SyntacticAuthority,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality
}
```

## §7 Residual vocabulary (local)

```text
ANTECEDENT_MISSING
ANTECEDENT_AMBIGUOUS
HOST_MISSING
ATTACHMENT_TYPE_AMBIGUOUS
PERSON_NUMBER_GENDER_MISMATCH
CASE_ROLE_PENDING
MAQAM_CONTEXT_REQUIRED
REFERENCE_DOMAIN_UNDECLARED
REFERENCE_SEARCH_REQUIRED
TRACE_REF_MISSING
```

Classification discipline:

- `ANTECEDENT_MISSING` is blocking for final reference and non-blocking for demand-surface opening.
- `ANTECEDENT_AMBIGUOUS` keeps `ReferenceDemandSurface` open and blocks final certificate.
- `CASE_ROLE_PENDING` keeps role claims in readiness only.
- `MAQAM_CONTEXT_REQUIRED` is deferred.
- `TRACE_REF_MISSING` is blocking for constitutional acceptance.

## §8 Anti-duplication and scope discipline

This layer does not duplicate neighboring branches:

```text
No duplication of LGE-LINK: link tools open relation demand, pronouns open reference demand.
No duplication of LEX-DATA: lexical data is witness only.
No duplication of LEX-BOUNDARY: wad'i boundary does not open naql or majaz here.
```

This step is restricted to:

```text
PronounSurface -> ReferenceDemandSurface -> ContractReadinessCandidate
```

## §9 Runtime embargo and safe sequencing

```text
RUNTIME_NOT_OPENED = {
  src_runtime_implementation,
  parser_changes,
  syntax_authority,
  reference_resolver_runtime,
  semantic_runtime,
  ifadah_engine,
  hukm_engine,
  truth_engine,
  certainty_engine,
  reality_engine,
  global_rank_engine,
  external_grounding_api
}
```

Safe sequencing:

```text
1. REF-PRON-L0 law-only
2. EvidenceFitnessCarrier
3. TraceReplayVerifier
4. RankVector/DomainPolicy
5. REF-PRON-C1 carrier surface
6. REF-PRON-G1 reference demand gate
7. REF-PRON-T1 stress fixtures
```

## §10 Constitutional examples (surface-only)

Example A:

```text
Input: "هو"
Output: DetachedPronounCandidate LICENSED + ReferenceDemandSurface
Residual: ANTECEDENT_MISSING or MAQAM_CONTEXT_REQUIRED
Forbidden: ReferenceResolved
```

Example B:

```text
Input: "جاء زيد ثم سلّم عليه"
Output: AttachedPronounCandidate LICENSED + ReferenceDemandSurface
Residual (if unresolved in this layer): ANTECEDENT_AMBIGUOUS or REFERENCE_SEARCH_REQUIRED
Forbidden: FinalReferenceCertificate
```

Example C:

```text
Input: "كتابه"
Output: NounAttachedPronoun LICENSED + IdafaReadinessCandidate
Forbidden: FinalOwnershipMeaning
```

Example D:

```text
Input: "ضربته"
Output: VerbAttachedPronoun LICENSED + RoleReadinessCandidate
Forbidden: FinalObjecthood / SyntacticAuthority
```
