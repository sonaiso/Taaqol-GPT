# 85 — Isolated Lexeme Adverbial Readiness Law (ZARF-L0)

> Status: constitutional law document (law-only).
> Scope: isolated time/place lexeme readiness before composition; no final syntactic role.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
ZARF-L0 = قانون الجاهزية الظرفية للفظ المفرد قبل التركيب.

IsolatedLexeme DOES_NOT_IMPLY MafulFihFinal
AdverbialReadinessCandidate DOES_NOT_IMPLY FinalSyntacticRole
AdverbialReadinessCandidate DOES_NOT_IMPLY Ifadah
AdverbialReadinessCandidate DOES_NOT_IMPLY Hukm
AdverbialReadinessCandidate DOES_NOT_IMPLY Truth
```

Constitutional rule:

```text
The isolated lexeme carries adverbial readiness, not final adverbial function.
Composition tests factor-demand and attachment-demand before any syntactic closure.
No lexical readiness closes into relation/ifadah/hukm/truth at this layer.
```

## §2 Branch identity and scope

```text
FAMILY               = ZARF
STEP                 = ZARF-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = ISOLATED_ADVERBIAL_READINESS
OBJECTIVE            = Time/place readiness surface only
TRANSITION_RULE      = MINIMUM_REQUIREMENT_KERNEL
```

This step is law-only and introduces no runtime carriers, no gate engines,
no parser/syntax authority runtime, and no semantic/ifadah/hukm/truth execution.

## §3 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  AdverbialReadinessCandidate,
  TimeAdverbCandidate,
  PlaceAdverbCandidate,
  TimePlaceAmbivalentCandidate,
  BuiltZarfCandidate,
  MutasarrifZarfCandidate,
  NonMutasarrifZarfCandidate,
  AttachmentDemandSurface,
  FactorDemandSurface,
  CompositionReadinessCandidate
}
```

## §4 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUT_ASSERTIONS = {
  IsolatedLexeme -> MafulFihFinal,
  ZarfReadiness -> FinalSyntacticRole,
  BuiltZarf -> Ifadah,
  TimePlaceLexeme -> Truth,
  Weight -> ZarfFinal,
  LexicalAttestation -> AdverbialTruth
}
```

```text
FORBIDDEN_OUTPUTS = {
  MafulFihFinal,
  FinalSyntacticRole,
  FinalRelation,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality,
  ExternalTemporalFact,
  ExternalSpatialFact
}
```

## §5 Adverbial readiness tiers

Three distinct tiers must remain separated:

1. Lexical adverbiality (`يوم`, `صباح`, `مساء`, `حين`, `وقت`, `مكان`, `جهة`).
2. Built/surface adverbial opening (`حيث`, `إذ`, `إذا`, `أين`, `هنا`, `هناك`, `ثم`).
3. Compositional maf'ul-fih role (only after valid factor + attachment).

Boundary discipline:

```text
AdverbialLexemeReadiness != MafulFihFinal
Readiness gives capability; composition gives function.
```

## §6 Minimal requirement kernel (MRK)

`MRK(ZarfReadiness)` requires the declared surface fields:

1. `LexemeIdentity`
2. `TimePlaceFamily`
3. `MutasarrifOrNonMutasarrifStatus`
4. `MabniOrMurabSurface`
5. `EvidenceSource`
6. `ExpectedAttachmentDemand`
7. `ExpectedFactorDemand`
8. `TraceRef`
9. `VisibleResiduals`
10. `ForbiddenOutputs`

Constitutional note:

```text
MRK closes only readiness identity.
MRK does not issue final syntactic role, relation closure, ifadah, hukm, or truth.
```

## §7 Lexeme-specific constitutional clarifications

```text
"عند" = place/proximity adverbial candidate, murab surface, typically idafa-demanding.
"حيث" = built locative/contextual candidate with clause/attachment demand.
"أمس" = usage-conditioned; built/murab behavior remains residual-visible until context closes.
"قط" = restricted usage surface (typically under negation); no free adverbial closure by default.
```

Weight discipline:

```text
Weight => PlaceOrTimeCandidate
Weight DOES_NOT_IMPLY ZarfFinal
```

## §8 Residual vocabulary (local)

```text
ADVERBIAL_EVIDENCE_MISSING
TIME_PLACE_AMBIGUITY
MABNI_STATUS_AMBIGUOUS
MUTASARRIF_STATUS_PENDING
FACTOR_REQUIRED
ATTACHMENT_REQUIRED
IDAFHA_COMPLEMENT_REQUIRED
LEXICAL_POLYSEMY_VISIBLE
WEIGHT_ONLY_NOT_SUFFICIENT
CONTEXT_REQUIRED_FOR_ADVERBIAL_ROLE
```

Classification discipline:

- `FACTOR_REQUIRED` blocks final syntactic-role claims.
- `ATTACHMENT_REQUIRED` blocks maf'ul-fih closure.
- `WEIGHT_ONLY_NOT_SUFFICIENT` blocks weight-only jumps.
- `IDAFHA_COMPLEMENT_REQUIRED` keeps idafa-dependent items non-closed.
- `CONTEXT_REQUIRED_FOR_ADVERBIAL_ROLE` is deferred/blocking by declared policy.

## §9 Anti-duplication and boundary integration

This layer does not duplicate neighboring branches:

```text
No duplication of MABNI-L0: builtness is not equivalent to adverbial readiness.
No duplication of LGE-LINK-L0: link operators are not adverbial candidates by default.
MabniStatus != ZarfReadiness
LinkOperator != ZarfCandidate
```

Intersections are allowed only as axis-preserving surfaces:

```text
"حيث" may carry MabniSurface + ZarfReadiness + AttachmentDemand,
but never FinalMeaning at this layer.
```

## §10 Runtime embargo and safe sequencing

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
  new_rank_engine,
  external_grounding_api
}
```

Safe constitutional sequencing:

```text
ZARF-L0
-> EvidenceFitnessCarrier
-> TraceReplayVerifier
-> RankVector/DomainPolicy
-> ZARF-C1
-> ZARF-G1
-> ZARF-T1
```

## §11 Constitutional minimum examples (surface-only)

Example 1:

```text
Input: "مساء"
Output: TimeAdverbCandidate LICENSED + FactorDemandSurface + AttachmentDemandSurface
Forbidden: MafulFihFinal / Ifadah / Hukm / Truth
```

Example 2:

```text
Input: "حيث"
Output: BuiltZarfCandidate LICENSED + AttachmentDemandSurface
Residuals: ATTACHMENT_REQUIRED + CONTEXT_REQUIRED_FOR_ADVERBIAL_ROLE
Forbidden: FinalRelation / Ifadah / Hukm / Truth
```

Example 3:

```text
Input: "عند"
Output: PlaceAdverbCandidate LICENSED + IDAFHA_COMPLEMENT_REQUIRED
Forbidden: MafulFihFinal before composition
```
