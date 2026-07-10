# 87 — Isolated Verb Identity Readiness Law (VERB-L0)

> Status: constitutional law document (law-only).
> Scope: isolated verb identity readiness before composition; no final event meaning, role closure, or judgment.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
VERB-L0 = قانون جاهزية هوية الفعل المفرد قبل التركيب.

VerbSurface DOES_NOT_IMPLY EventTruth
VerbIdentityReadinessCandidate DOES_NOT_IMPLY Ifadah
VerbIdentityReadinessCandidate DOES_NOT_IMPLY Hukm
VerbIdentityReadinessCandidate DOES_NOT_IMPLY Truth
PastForm DOES_NOT_IMPLY ExternalPastEvent
ImperativeForm DOES_NOT_IMPLY CommandJudgment
TransitivityReadiness DOES_NOT_IMPLY FinalObjectSlots
VerbOntologyDemand DOES_NOT_IMPLY SubjectCompatibilityFinal
```

Constitutional rule:

```text
At this layer, isolated verb processing produces readiness only.
No VerbIdentityCertificate and no final semantic/syntactic/judgment closure are licensed.
Any transition from Readiness/Candidate naming to Certificate or Truth/Hukm/Ifadah at VERB-L0 is a FORBIDDEN_LEAP.
The isolated verb opens event/tense/mode/subject-object/maqam demands and does not close truth.
```

## §2 Branch identity and scope

```text
FAMILY               = VERB
STEP                 = VERB-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = ISOLATED_VERB_IDENTITY_READINESS
OBJECTIVE            = Event-demand readiness surface for later composition/contract only
TRANSITION_RULE      = MINIMUM_REQUIREMENT_KERNEL
```

This step is law-only and introduces no runtime carriers, no gate engines,
no parser/morphology/syntax authority runtime, and no semantic/ifadah/hukm/truth execution.

## §3 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  VerbIdentityReadinessCandidate,
  SourceReadinessCandidate,
  TenseFormCandidate,
  PastFormCandidate,
  PresentFormCandidate,
  ImperativeFormCandidate,
  TransitivityReadinessCandidate,
  ObjectDemandSurface,
  SubjectDemandSurface,
  ModeDemandSurface,
  MaqamDemandSurface,
  VerbOntologyDemandSurface,
  AttachedPronounDemandSurface,
  AdverbialDemandSurface,
  PrepositionalTransitivityDemand,
  CompositionReadinessCandidate
}
```

## §4 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUT_ASSERTIONS = {
  VerbSurface -> EventTruth,
  PastForm -> ExternalPastEvent,
  ImperativeForm -> CommandJudgment,
  TransitivityReadiness -> FinalObjecthood,
  VerbOntologyDemand -> SubjectCompatibilityFinal,
  SourceReadiness -> FinalSourceCertificate,
  VerbReadiness -> Ifadah,
  VerbReadiness -> Hukm,
  VerbReadiness -> Truth
}
```

```text
FORBIDDEN_OUTPUTS = {
  VerbIdentityCertificate,
  FinalEventMeaning,
  FinalSourceCertificate,
  ExternalPastEvent,
  FinalTransitivityCertificate,
  FinalSyntacticRole,
  SubjectCompatibilityFinal,
  ObjectSlotFinal,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality,
  CommandJudgment,
  ObligationJudgment
}
```

## §5 Readiness axes before composition

VERB-L0 defines five readiness axes:

1. `SourceReadinessCandidate` (source path candidacy only; never final source certificate).
2. `TenseFormCandidate` (form tense only; never external event truth).
3. `TransitivityReadinessCandidate` (transitivity demand only; never final object role closure).
4. `ModeDemandSurface` + `MaqamDemandSurface` (speech-force readiness only; never hukm).
5. `VerbOntologyDemandSurface` (ontological demand only; never final subject compatibility).

Boundary discipline:

```text
IsolatedVerbReadiness opens demands; composition closes assignment.
```

## §6 Minimal requirement kernel (MRK)

`MRK(VerbReadiness)` requires the declared surface fields:

1. `SurfaceIdentity`
2. `VerbFormFamily`
3. `SourceReadiness`
4. `TenseForm`
5. `SubjectDemand`
6. `TransitivityReadiness`
7. `ModeMaqamDemand`
8. `OntologyDemand`
9. `TraceRef`
10. `VisibleResiduals`
11. `ForbiddenOutputs`

Constitutional note:

```text
MRK closes readiness identity only.
MRK does not issue event truth, ifadah, hukm, final objecthood, or final subject compatibility.
```

## §7 Boundary continuity with neighboring laws

VERB-L0 does not duplicate neighboring branches:

```text
No duplication of NOUN-L0: noun branch proves carrier readiness; verb branch proves event-demand readiness (docs/86).
No duplication of REF-PRON-L0: attached pronouns open AttachedPronounDemandSurface only (docs/83).
No duplication of LGE-LINK-L0: prepositional transitivity remains demand-only before link licensing.
No duplication of LEX-DATA-1 and LEX-BOUNDARY-L0: lexical witness is evidence only and does not open majaz/naql.
No duplication of ZARF-L0: adverbial requirement here is demand surface only.
```

## §8 Residual vocabulary (local)

```text
SOURCE_EVIDENCE_MISSING
SOURCE_PATTERN_AMBIGUOUS
TENSE_FORM_AMBIGUOUS
PAST_FORM_NOT_REAL_EVENT
PRESENT_MODE_PENDING
IMPERATIVE_ADDRESSEE_REQUIRED
SUBJECT_DEMAND_UNFILLED
OBJECT_DEMAND_UNFILLED
TRANSITIVITY_ALTERNATION_VISIBLE
PREPOSITIONAL_GOVERNANCE_PENDING
ONTOLOGICAL_SUBJECT_COMPATIBILITY_PENDING
RATIONAL_AGENT_REQUIRED
MAQAM_CONTEXT_REQUIRED
VERB_FORM_MABNI_MURAB_AMBIGUITY
COMMAND_FORCE_NOT_HUKM
```

Classification discipline:

- `PAST_FORM_NOT_REAL_EVENT` blocks form-to-reality jumps.
- `TRANSITIVITY_ALTERNATION_VISIBLE` keeps transitivity non-final at this layer.
- `PREPOSITIONAL_GOVERNANCE_PENDING` keeps prepositional transitivity deferred to link licensing.
- `RATIONAL_AGENT_REQUIRED` is an ontology demand, not final subject judgment.
- `COMMAND_FORCE_NOT_HUKM` blocks imperative-form to obligation jump.

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
  verb_identity_gate_runtime,
  verb_identity_certificate_runtime,
  transitivity_gate_runtime,
  source_gate_runtime,
  mode_gate_runtime
}
```

Safe constitutional sequencing:

```text
VERB-L0
-> EvidenceFitnessCarrier
-> TraceReplayVerifier
-> RankVector/DomainPolicy
-> VERB-C1
-> VERB-G1
```

## §10 Constitutional minimum examples (surface-only)

Example 1:

```text
Input: "ضرب"
Output: PastFormCandidate LICENSED + SourceReadinessCandidate + TransitivityReadinessCandidate + SubjectDemandSurface + ObjectDemandSurface
Forbidden: ExternalPastEvent / FinalObjecthood / Ifadah / Truth
```

Example 2:

```text
Input: "ذهب"
Output: PastFormCandidate LICENSED + TransitivityReadinessCandidate + SubjectDemandSurface
Residuals: PREPOSITIONAL_GOVERNANCE_PENDING
Forbidden: FinalTransitivityCertificate
```

Example 3:

```text
Input: "يكتب"
Output: PresentFormCandidate LICENSED + ModeDemandSurface + SubjectDemandSurface + ObjectDemandSurface
Forbidden: PresentRealityTruth
```

Example 4:

```text
Input: "اكتب"
Output: ImperativeFormCandidate LICENSED + MaqamDemandSurface + SubjectDemandSurface
Residuals: IMPERATIVE_ADDRESSEE_REQUIRED + COMMAND_FORCE_NOT_HUKM
Forbidden: CommandJudgment / ObligationJudgment / Truth
```

Example 5:

```text
Input: "قال"
Output: VerbOntologyDemandSurface LICENSED + RATIONAL_AGENT_REQUIRED
Forbidden: SubjectCompatibilityFinal
```

Example 6:

```text
Input: "أمطر"
Output: VerbIdentityReadinessCandidate LICENSED + VerbOntologyDemandSurface + SubjectDemandSurface
Forbidden: WeatherTruth / Reality
```
