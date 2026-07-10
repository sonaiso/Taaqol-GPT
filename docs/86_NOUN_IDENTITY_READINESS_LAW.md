# 86 — Isolated Noun Identity Readiness Law (NOUN-L0)

> Status: constitutional law document (law-only).
> Scope: isolated noun identity readiness before composition; no final meaning, role, or judgment.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
NOUN-L0 = قانون جاهزية هوية الاسم المفرد قبل التركيب.

IsolatedNoun DOES_NOT_IMPLY FinalMeaning
NounIdentityReadinessCandidate DOES_NOT_IMPLY Ifadah
NounIdentityReadinessCandidate DOES_NOT_IMPLY Hukm
NounIdentityReadinessCandidate DOES_NOT_IMPLY Truth
WadiReadinessCandidate DOES_NOT_IMPLY Naql/Majaz
MabniCandidate DOES_NOT_IMPLY FinalReference
```

Constitutional rule:

```text
At this layer, isolated noun processing produces readiness only.
No NounIdentityCertificate and no final semantic/syntactic closure are licensed.
```

## §2 Branch identity and scope

```text
FAMILY               = NOUN
STEP                 = NOUN-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = ISOLATED_NOUN_IDENTITY_READINESS
OBJECTIVE            = Identity-readiness surface for later composition/contract only
TRANSITION_RULE      = MINIMUM_REQUIREMENT_KERNEL
```

This step is law-only and introduces no runtime carriers, no gate engines,
no parser/morphology/syntax authority runtime, and no semantic/ifadah/hukm/truth execution.

## §3 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  NounIdentityReadinessCandidate,
  DalSurfaceReadiness,
  LafziReadiness,
  WadiReadinessCandidate,
  MabniPathCandidate,
  MurabPathCandidate,
  GenderNumberReadiness,
  DefinitenessReadiness,
  CompositionReadinessCandidate,
  LexicalWitnessCandidate,
  ReferenceDemandSurface,
  AdverbialReadinessCandidate,
  RelativeNounReadiness,
  DemonstrativeReadiness
}
```

## §4 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUT_ASSERTIONS = {
  IsolatedNoun -> FinalMeaning,
  NounReadiness -> Ifadah,
  NounReadiness -> Hukm,
  NounReadiness -> Truth,
  LexicalWitness -> NounTruth,
  WadiReadiness -> Naql/Majaz,
  MabniCandidate -> ReferenceResolved,
  ZarfReadiness -> MafulFihFinal,
  RelativeReadiness -> ReferenceResolved
}
```

```text
FORBIDDEN_OUTPUTS = {
  NounIdentityCertificate,
  FinalMeaning,
  ContextualMeaning,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality,
  FinalSyntacticRole,
  ReferenceResolved,
  FinalReferenceCertificate,
  NaqliMadlulLicensed_without_NaqlGate,
  MajaziMadlulLicensed_without_MajazGate
}
```

## §5 Readiness axes before composition

NOUN-L0 defines four readiness axes:

1. `DalSurfaceReadiness` (surface identity, stem/pattern candidacy, mabni/mu'rab possibility).
2. `LafziReadiness` (orthographic form, pronunciation/haraka trace when present, visible ambiguity).
3. `WadiReadinessCandidate` (lexical attestation witness-only, source type, usage candidacy, rank ceiling).
4. `CompositionReadinessCandidate` (contract demand surface, not final role assignment).

Boundary discipline:

```text
Readiness gives carrier capability; composition gives functional closure.
```

## §6 Minimal requirement kernel (MRK)

`MRK(NounReadiness)` requires the declared surface fields:

1. `SurfaceIdentity`
2. `NounFamily`
3. `MabniMurabPathStatus`
4. `NumberGenderDefinitenessReadiness`
5. `LexicalWitnessStatus`
6. `CompositionDemandSurface`
7. `TraceRef`
8. `VisibleResiduals`
9. `ForbiddenOutputs`

Constitutional note:

```text
MRK closes readiness identity only.
MRK does not issue final meaning, ifadah, hukm, truth, reference resolution, or final syntactic role.
```

## §7 Boundary continuity with neighboring laws

NOUN-L0 inherits boundary constraints from current lexical and surface branches:

```text
No duplication of LEX-DATA-1: lexical sources remain witness-only (docs/81).
No duplication of LEX-BOUNDARY-L0: wad'i readiness does not imply naql/majaz (docs/82).
No duplication of MABNI-L0: mabni path is token-scoped readiness, not final reference (docs/84).
No duplication of ZARF-L0: adverbial readiness remains readiness, not maf'ul-fih final (docs/85).
No duplication of REF-PRON-L0: pronoun-like forms open reference-demand surfaces only.
```

## §8 Residual vocabulary (local)

```text
NOUN_SURFACE_IDENTITY_INCOMPLETE
NOUN_FAMILY_AMBIGUOUS
MABNI_MURAB_PATH_AMBIGUOUS
NUMBER_GENDER_PENDING
DEFINITENESS_PENDING
LEXICAL_WITNESS_MISSING
LEXICAL_WITNESS_AMBIGUOUS
SENSE_AMBIGUITY_VISIBLE
COMPOSITION_DEMAND_OPEN
REFERENCE_DEMAND_UNRESOLVED
NAQL_GATE_REQUIRED
MAJAZ_GATE_REQUIRED
```

Classification discipline:

- `SENSE_AMBIGUITY_VISIBLE` keeps polysemous nouns non-resolved at readiness layer.
- `REFERENCE_DEMAND_UNRESOLVED` blocks final reference closure for demonstratives/relatives/pronoun-like forms.
- `NAQL_GATE_REQUIRED` and `MAJAZ_GATE_REQUIRED` enforce independent-gate discipline from docs/82.

## §9 Runtime embargo and safe sequencing

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
  certainty_engine,
  reality_engine,
  noun_identity_gate_runtime,
  noun_identity_certificate_runtime,
  naql_gate_runtime,
  majaz_gate_runtime
}
```

Safe constitutional sequencing:

```text
NOUN-L0
-> EvidenceFitnessCarrier
-> TraceReplayVerifier
-> RankVector/DomainPolicy
-> NOUN-C1
-> NOUN-G1
```

## §10 Constitutional minimum examples (surface-only)

Example 1:

```text
Input: "جبل"
Output: NounIdentityReadinessCandidate LICENSED + WadiReadinessCandidate + CompositionReadinessCandidate
Forbidden: FinalMeaning / Truth / Hukm
```

Example 2:

```text
Input: "هذا"
Output: MabniPathCandidate LICENSED + DemonstrativeReadiness + ReferenceDemandSurface
Forbidden: ReferenceResolved / FinalMeaning
```

Example 3:

```text
Input: "عين"
Output: NounIdentityReadinessCandidate LICENSED
Residuals: SENSE_AMBIGUITY_VISIBLE
Forbidden: SenseResolved / Truth
```

Example 4:

```text
Input: "مساء"
Output: NounIdentityReadinessCandidate LICENSED + AdverbialReadinessCandidate
Forbidden: MafulFihFinal before composition
```

Example 5:

```text
Input: "الذي"
Output: RelativeNounReadiness LICENSED + ReferenceDemandSurface + CompositionReadinessCandidate
Forbidden: ReferenceResolved / Ifadah
```
