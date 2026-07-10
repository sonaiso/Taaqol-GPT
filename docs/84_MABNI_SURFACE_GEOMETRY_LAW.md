# 84 — Built-Form Surface Registry Boundary Law (MABNI-L0)

> Status: constitutional law document (law-only).
> Scope: built-form surface families and built construction cases as demand surfaces only.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
MABNI-L0 = قانون حدود سجل المبنيات السطحية، لا تنفيذ، ولا runtime، ولا معنى نهائي.

MabniSurface DOES_NOT_IMPLY FinalMeaning
MabniSurface DOES_NOT_IMPLY Ifadah
MabniSurface DOES_NOT_IMPLY Hukm
MabniSurface DOES_NOT_IMPLY Truth
MabniCandidate DOES_NOT_IMPLY SyntacticAuthority
```

Corrected constitutional rule:

```text
If a surface form matches or plausibly matches a built-form family,
MabniCandidate path must be tested before Weight/Derivation closure for that token.
```

This rule is token-scoped. It does not require closing all built forms in Arabic before any
weight branch operation.

## §2 Branch identity and scope

```text
FAMILY               = MABNI
STEP                 = MABNI-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = MABNI_SURFACE_REGISTRY
OBJECTIVE            = Built-form family/case registry with demand-surface discipline
TRANSITION_RULE      = MINIMUM_REQUIREMENT_KERNEL
```

This step is law-only and introduces no runtime carriers, no gate engines,
no parser/syntax authority runtime, and no semantic/ifadah/hukm/truth execution.

## §3 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  MabniCandidate,
  DemonstrativeCandidate,
  RelativeNounCandidate,
  InterrogativeCandidate,
  ConditionalNameCandidate,
  VerbNounCandidate,
  CompoundNumberCandidate,
  BuiltAdverbCandidate,
  VocativeBuiltCaseCandidate,
  LaNafiyaBuiltCaseCandidate,
  FunctionalDemandSurface,
  ReferenceDemandSurface,
  QuestionDemandSurface,
  ConditionDemandSurface,
  VocativeDemandSurface,
  ExclamativeStyleSurface,
  CompositionReadinessCandidate
}
```

## §4 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUT_ASSERTIONS = {
  MabniSurface -> FinalMeaning,
  DemonstrativeCandidate -> ReferenceResolved,
  RelativeNounCandidate -> ReferenceResolved,
  InterrogativeCandidate -> Answer,
  ConditionalNameCandidate -> Hukm,
  VerbNounCandidate -> VerbRuntimeMeaning,
  CompoundNumberCandidate -> QuantitativeTruth,
  BuiltAdverbCandidate -> MafulFihFinal,
  VocativeBuiltCaseCandidate -> FinalReferenceCertificate,
  LaNafiyaBuiltCaseCandidate -> ExistentialTruth,
  MabniCandidate -> SyntacticAuthority
}
```

```text
FORBIDDEN_OUTPUTS = {
  FinalMeaning,
  ContextualMeaning,
  ReferenceResolved,
  FinalReferenceCertificate,
  FinalSyntacticRole,
  SyntacticAuthority,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality,
  NaqliMadlulLicensed_without_NaqlGate,
  MajaziMadlulLicensed_without_MajazGate
}
```

## §5 Built-form families and case openings

G0.1 identity anchors:

1. Demonstratives (`هذا`, `هذه`, `هذي`, `ها`, `ذاك`, `ذلك`, `تلك`, `هنا`, `هنالك`, `هؤلاء`, `أولئك`) open `DemonstrativeCandidate` + `DeicticDemandSurface` + `ReferenceDemandSurface`.
2. Relatives (`الذي`, `التي`, `الذين`, `اللاتي`, `اللائي`, `من`, `ما`) open `RelativeNounCandidate` + `SilaDemandSurface` + `ReferenceDemandSurface`.

Exception discipline:

```text
هذان / هاتان are dual i'rab exceptions, not simple built anchors.
اللذان / اللتان are dual i'rab exceptions, not absolute built forms.
```

G0.2 functional anchors:

3. Interrogatives (`من`, `ما`, `أين`, `كيف`, `متى`, `أيان`, `أنى`, `كم`) open `InterrogativeCandidate` + `QuestionDemandSurface` + `ExpectedAnswerSlot`.
4. Condition names (`من`, `ما`, `مهما`, `متى`, `أيان`, `أنى`, `حيثما`, `إذا`) open `ConditionalNameCandidate` + `ConditionDemandSurface` + `AnswerDemandSurface`.
5. Verb-nouns (`هيهات`, `شتان`, `وي`, `أف`, `صه`, `مه`) open `VerbNounCandidate` + `FunctionalDemandSurface` + `SpeechForceReadiness`.

Exception discipline:

```text
أيّ is a mu'rab exception and cannot be treated as absolutely built.
```

G0.3 quantitative anchors:

6. Compound numbers (`أحد عشر`, `إحدى عشرة`, `ثلاثة عشر` ... `تسعة عشر`) open `CompoundNumberCandidate` + `QuantitySurface` + `CountDemandSurface`.

Exception discipline:

```text
اثنا عشر / اثنتا عشرة are i'rab exceptions and not the same built pattern.
```

G0.4 adverbial anchors:

7. Built adverbs (`أمس`, `حيث`, `إذ`, `إذا`, `الآن`, `مذ`, `منذ`, `قط`, `بينما`, `هنا`, `هناك`, `هنالك`) open `BuiltAdverbCandidate` + `AdverbialReadinessCandidate` + `AttachmentDemandSurface`.

Special built construction cases:

8. Vocative built case (e.g., `يا خالدُ`, `يا رجلُ`) opens `VocativeBuiltCaseCandidate` + `VocativeDemandSurface` + `CallingSurface`.
9. La-nafiya built case (e.g., `لا رجلَ`) opens `LaNafiyaBuiltCaseCandidate` + `NegationConstructionReadiness` + `GenusNegationSurface`.

Boundary discipline:

```text
MawsulCandidate => SilaDemandSurface
MawsulCandidate DOES_NOT_IMPLY ReferenceResolved

IstifhamCandidate => ExpectedAnswerSlot
IstifhamCandidate DOES_NOT_IMPLY Answer

ConditionalNameCandidate => ConditionDemandSurface
ConditionalNameCandidate DOES_NOT_IMPLY Hukm

LaNafiyaConstruction => GenusNegationSurface
LaNafiyaConstruction DOES_NOT_IMPLY ExistentialTruth

BuiltAdverbCandidate DOES_NOT_IMPLY MafulFihFinal
```

## §6 Minimal requirement kernel (MRK)

`MRK(MabniCandidate)` requires the declared surface fields:

1. `surface_identity`
2. `built_family`
3. `subfamily`
4. `exception_status`
5. `functional_or_reference_demand`
6. `required_attachment_or_context`
7. `trace_ref`
8. `visible_residuals`
9. `forbidden_outputs`

Constitutional note:

```text
After MRK, output remains demand-surface/readiness only.
MRK does not issue semantic closure, reference certificate, syntactic authority,
or truth.
```

## §7 Residual vocabulary (local)

```text
MABNI_FAMILY_AMBIGUOUS
DUAL_EXCEPTION_REQUIRES_IRAB_DISCIPLINE
AYY_MURAB_EXCEPTION
REFERENCE_DEMAND_UNFILLED
SILA_DEMAND_UNFILLED
QUESTION_ANSWER_SLOT_OPEN
CONDITION_ANSWER_MISSING
VOCATIVE_CONTEXT_REQUIRED
LA_NAFIYA_CONSTRUCTION_REQUIRED
COMPOUND_NUMBER_EXCEPTION
ADVERBIAL_ATTACHMENT_REQUIRED
MABNI_STATUS_PENDING
WEIGHT_PATH_BLOCKED_BY_MABNI_CANDIDATE
```

Classification discipline:

- `MABNI_FAMILY_AMBIGUOUS` keeps multi-family forms (like `من`) open and blocks premature final classification.
- `WEIGHT_PATH_BLOCKED_BY_MABNI_CANDIDATE` enforces testing the mabni path before weight/derivation closure for the token under analysis.
- `DUAL_EXCEPTION_REQUIRES_IRAB_DISCIPLINE` and `AYY_MURAB_EXCEPTION` prevent false absolute-built closure.

## §8 Anti-duplication and boundary integration

This layer does not duplicate neighboring branches:

```text
No duplication of REF-PRON-L0: pronouns remain PronounSurface -> ReferenceDemandSurface.
No duplication of LGE-LINK-L0: link tools remain LinkTool -> RelationDemandSurface.
No duplication of LEX-DATA-1: lexical data is witness-only.
No duplication of LEX-BOUNDARY-L0: Wad'i does not jump to Naql/Majaz without a licensed gate.
No duplication of ZARF-L0: isolated lexeme adverbial readiness remains governed by docs/85.
```

Integration law:

```text
Multiple axes may co-exist on one token, but no axis may absorb the others.
```

Example:

```text
"حيث" may carry MabniSurface + BuiltAdverbCandidate + AttachmentDemandSurface,
but does not close into FinalMeaning.
```

## §9 Runtime embargo and safe sequencing

```text
RUNTIME_NOT_OPENED = {
  src_runtime_implementation,
  parser_changes,
  executable_registry_runtime,
  syntax_authority,
  reference_resolver_runtime,
  semantic_runtime,
  ifadah_engine,
  hukm_engine,
  truth_engine,
  certainty_engine,
  reality_engine,
  new_rank_engine,
  external_grounding_api
}
```

Safe constitutional sequencing:

```text
MABNI-L0 (law-only)
-> EvidenceFitnessCarrier
-> TraceReplayVerifier
-> RankVector/DomainPolicy
-> MABNI-C1 carrier surface
-> MABNI-G1 gates
-> MABNI-T1 stress fixtures
```

## §10 Constitutional minimum examples (surface-only)

Example 1:

```text
Input: "هذا"
Allowed: DemonstrativeCandidate
Required: DeicticDemandSurface
Forbidden: ExternalReferent, FinalReferenceCertificate, Truth
```

Example 2:

```text
Input: "الذي"
Allowed: RelativeNounCandidate
Required: SilaDemandSurface
Forbidden: ReferenceResolved, Ifadah, Hukm, Truth
```

Example 3:

```text
Input: "أين"
Allowed: InterrogativeCandidate
Required: ExpectedAnswerSlot
Forbidden: Answer, Hukm, Truth
```

Example 4:

```text
Input: "من"
Expected: MABNI_FAMILY_AMBIGUOUS
Possible families: Interrogative / Conditional / Relative
Forbidden: Direct final classification without context
```

Example 5:

```text
Input: "هيهات"
Allowed: VerbNounCandidate
Forbidden: VerbRuntimeMeaning, Hukm, Truth
```

Example 6:

```text
Input: "أحد عشر"
Allowed: CompoundNumberCandidate
Forbidden: QuantitativeTruth
```

Example 7:

```text
Input: "أمس"
Allowed: BuiltAdverbCandidate
Residual: ADVERBIAL_ATTACHMENT_REQUIRED
Forbidden: MafulFihFinal before composition
```

Example 8:

```text
Input: "يا خالدُ"
Allowed: VocativeBuiltCaseCandidate
Forbidden: FinalReferenceCertificate
```

Example 9:

```text
Input: "لا رجلَ"
Allowed: LaNafiyaBuiltCaseCandidate
Forbidden: ExistentialTruth
```
