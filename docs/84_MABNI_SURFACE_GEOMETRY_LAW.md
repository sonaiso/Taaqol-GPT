# 84 — Built-Form Surface Geometry Law (MABNI-L0)

> Status: constitutional law document (law-only).
> Scope: built-form surface geometry for mawsul/ishara/istifham/nida/taajjub as demand surfaces only.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
MABNI-L0 = قانون مجال المبنيات، لا تنفيذ، ولا runtime، ولا معنى نهائي.

MabniSurface DOES_NOT_IMPLY FinalMeaning
MabniSurface DOES_NOT_IMPLY Ifadah
MabniSurface DOES_NOT_IMPLY Hukm
MabniSurface DOES_NOT_IMPLY Truth
```

Constitutional rule:

```text
Built forms are licensed as demand surfaces only.
No demand surface closes into semantic or judgmental authority at this layer.
ContractReadinessCandidate DOES_NOT_IMPLY FinalReferenceCertificate.
```

## §2 Branch identity and scope

```text
FAMILY               = MABNI
STEP                 = MABNI-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = MABNI_SURFACE_GEOMETRY
OBJECTIVE            = Built-form demand surfaces only
TRANSITION_RULE      = MINIMUM_REQUIREMENT_KERNEL
```

This step is law-only and introduces no runtime carriers, no gate engines,
no parser/syntax authority runtime, and no semantic/ifadah/hukm/truth execution.

## §3 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  MabniCandidate,
  MawsulCandidate,
  IsharaCandidate,
  IstifhamCandidate,
  NidaCandidate,
  TaajjubCandidate,
  FunctionalDemandSurface,
  ReferenceDemandSurface,
  QuestionDemandSurface,
  VocativeDemandSurface,
  ExclamativeStyleSurface,
  ContractReadinessCandidate
}
```

## §4 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUT_ASSERTIONS = {
  MabniSurface -> FinalMeaning,
  MawsulCandidate -> ReferenceResolved,
  IsharaCandidate -> ExternalReferent,
  IstifhamCandidate -> Answer,
  NidaCandidate -> FinalReferenceCertificate,
  TaajjubCandidate -> Truth,
  MabniCandidate -> Ifadah,
  MabniCandidate -> Hukm
}
```

```text
FORBIDDEN_OUTPUTS = {
  FinalMeaning,
  ContextualMeaning,
  ReferenceResolved,
  FinalReferenceCertificate,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality,
  SyntacticAuthority,
  SemanticClosure
}
```

## §5 Built-form families and demand openings

1. Relative-name family (`الذي` and cognates): opens `MawsulCandidate` + `ReferenceDemandSurface`
2. Demonstrative family (`هذا` and cognates): opens `IsharaCandidate` + `ReferenceDemandSurface`
3. Interrogative family (`أين` and cognates): opens `IstifhamCandidate` + `QuestionDemandSurface`
4. Vocative family (`يا ...`): opens `NidaCandidate` + `VocativeDemandSurface`
5. Exclamative family (`ما أفعل`/`أفعل به` patterns): opens `TaajjubCandidate` + `ExclamativeStyleSurface`

Boundary discipline:

```text
Demand opening is not reference resolution.
Demand opening is not answer closure.
Demand opening is not final attribute judgment.
```

## §6 Minimal requirement kernel (MRK)

`MRK(MabniCandidate)` requires the declared surface fields:

1. `BuiltFormIdentity`
2. `BuiltFormFamily`
3. `DemandSurfaceType`
4. `ScopeOrAnchorDemand`
5. `MaqamContextNeed`
6. `ResidualVisibility`
7. `TraceRef`
8. `ForbiddenOutputs`

Constitutional note:

```text
After MRK, output remains demand-surface/readiness only.
MRK does not issue semantic closure, reference certificate, or truth.
```

## §7 Residual vocabulary (local)

```text
SILA_DEMAND_REQUIRED
DEICTIC_DEMAND_REQUIRED
EXPECTED_ANSWER_SLOT_OPEN
VOCATIVE_TARGET_PENDING
EXCLAMATIVE_MEASURE_PENDING
MAQAM_CONTEXT_REQUIRED
TRACE_REF_MISSING
FORBIDDEN_SHORTCUT_ATTEMPT
```

Classification discipline:

- `SILA_DEMAND_REQUIRED` blocks relative-reference closure and keeps demand surface open.
- `DEICTIC_DEMAND_REQUIRED` blocks external referent claims without context.
- `EXPECTED_ANSWER_SLOT_OPEN` is non-closing and forbids answer-as-fact.
- `VOCATIVE_TARGET_PENDING` blocks final reference certificate.
- `EXCLAMATIVE_MEASURE_PENDING` blocks final attribute judgment and truth.
- `TRACE_REF_MISSING` is blocking for constitutional acceptance.

## §8 Anti-duplication and boundary integration

This layer does not duplicate neighboring branches:

```text
No duplication of REF-PRON-L0: pronouns remain PronounSurface -> ReferenceDemandSurface.
No duplication of LGE-LINK-L0: link tools remain LinkTool -> RelationDemandSurface.
No duplication of LEX-DATA: lexical data is witness-only.
No duplication of LEX-BOUNDARY-L0: Wad'i does not jump to Naql/Majaz without a licensed gate.
```

`MABNI-L0` is restricted to built forms as:

```text
functional/reference/question/vocative/exclamative demand surfaces only.
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
  new_rank_engine,
  external_grounding_api
}
```

Safe constitutional sequencing:

```text
MABNI-L0
-> EvidenceFitnessCarrier
-> TraceReplayVerifier
-> RankVector/DomainPolicy
-> MABNI-C1
```

## §10 Constitutional minimum examples (surface-only)

Example 1:

```text
Input: "الذي"
Output: MawsulCandidate LICENSED + SilaDemandSurface
Forbidden: ReferenceResolved / Ifadah / Hukm / Truth
```

Example 2:

```text
Input: "هذا"
Output: IsharaCandidate LICENSED + DeicticDemandSurface
Forbidden: ExternalReferent without Maqam/Context
```

Example 3:

```text
Input: "أين"
Output: IstifhamCandidate LICENSED + ExpectedAnswerSlot
Forbidden: Answer / Hukm / Truth
```

Example 4:

```text
Input: "يا زيد"
Output: NidaCandidate LICENSED + VocativeDemandSurface
Forbidden: FinalReferenceCertificate
```

Example 5:

```text
Input: "ما أجمل السماء"
Output: TaajjubCandidate LICENSED + ExclamativeStyleSurface
Forbidden: FinalAttributeJudgment / Truth
```
