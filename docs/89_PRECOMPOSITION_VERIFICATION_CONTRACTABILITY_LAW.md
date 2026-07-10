# 89 — Pre-Composition Verification and Contractability Law (PRECOMP-L0)

> Status: constitutional law document (law-only).
> Scope: pre-composition verification layers that produce contractability readiness only.
> Snapshot date: 2026-07-10.

## §1 Governing law

```text
PRECOMP-L0 = قانون التحقق قبل التركيب وقابلية التعاقد.

No Composition Before Verification.
Verification before composition yields ContractabilityReadiness only.
ContractabilityReadiness DOES_NOT_IMPLY FinalSyntax.
ContractabilityReadiness DOES_NOT_IMPLY FinalMeaning.
ContractabilityReadiness DOES_NOT_IMPLY Ifadah.
ContractabilityReadiness DOES_NOT_IMPLY Hukm.
ContractabilityReadiness DOES_NOT_IMPLY Truth.
AtomicSurfaceReadiness DOES_NOT_IMPLY DerivationFinal.
AtomicSurfaceReadiness DOES_NOT_IMPLY SyntaxFinal.
AtomicSurfaceReadiness DOES_NOT_IMPLY WadiMeaning.
```

Constitutional rule:

```text
No composition claim is admissible before visible multi-layer verification.
Pre-composition verification is readiness geometry, not certificate geometry.
No final syntactic role, no final meaning, and no judgment/truth closure are licensed at PRECOMP-L0.
Any transition from readiness/candidate naming to final closure naming at PRECOMP-L0 is a FORBIDDEN_LEAP.
```

## §2 Branch identity and scope

```text
FAMILY               = PRECOMPOSITION
STEP                 = PRECOMP-L0
STEP_KIND            = LAW_ONLY
DOMAIN               = PRECOMPOSITION_VERIFICATION_AND_CONTRACTABILITY
OBJECTIVE            = Verify atomic/word/path/lexeme readiness before composition without semantic or syntactic closure
TRANSITION_RULE      = READINESS_ONLY_WITH_VISIBLE_RESIDUALS
```

This step is law-only and introduces no runtime verifier, no parser/morphology/syntax authority runtime, and no semantic/ifadah/hukm/truth runtime.

## §3 Layered verification model (A0..A4)

```text
A0: Atomic Surface Verification
A1: Word Surface Verification
A2: Path Readiness Verification
A3: Lexeme Contractability Verification
A4: Composition Precondition Verification
```

Layer discipline:

```text
AtomicUnit -> AtomicSurfaceReadiness
WordSurface -> WordSurfaceReadinessCandidate
PathSurface -> PathReadinessCandidate
LexemeSurface -> LexemeContractabilityReadiness
PreCompBoundary -> CompositionPreconditionCandidate
```

Forbidden jump:

```text
AtomicUnit -> Derivation + Syntax + Wadi
```

## §4 A0 atomic boundary (letter + haraka)

Allowed at A0:

```text
AtomicSurfaceUnit
LetterIdentity
HarakaIdentity
LetterHarakaCompatibility
OrthographicTrace
PhoneticTrace
PositionInWord
AtomicResiduals
```

Forbidden at A0:

```text
DerivationFinal
MorphologyFinal
SyntaxFinal
WadiMeaning
Truth
```

Atomic rule:

```text
PHONETIC_TENSION_VISIBLE is residual-visible, not automatic failure.
PASS_WITH_RESIDUAL is admissible where hard prohibition is absent.
Atomic rank remains SurfaceReadiness and may not be promoted to LICENSED/STRONG composition authority.
```

MRK:

```text
MRK(AtomicSurfaceUnit) =
LetterIdentity
+ HarakaIdentity
+ OrthographicValidity
+ PhoneticArticulationTrace
+ PositionInWord
+ TraceRef
+ VisibleResiduals
```

## §5 A1 word surface boundary

Questions:

```text
OrderPreserved?
OrthographicBoundaryDeclared?
VocalizationStatusDeclared?
SurfaceAmbiguityVisible?
ShaddaTanwinStatusDeclared?
```

Output:

```text
WordSurfaceReadinessCandidate
```

Not:

```text
WordMeaning
```

Local residual vocabulary:

```text
UNVOCALIZED_SURFACE_RESIDUAL
LETTER_ORDER_CONFIRMED
ORTHOGRAPHIC_AMBIGUITY_VISIBLE
SHADDA_OR_TANWIN_PENDING
```

## §6 A2 path readiness boundary

Allowed path candidates:

```text
NounPathCandidate
VerbPathCandidate
HarfPathCandidate
MabniPathCandidate
PronounPathCandidate
ZarfPathCandidate
ResidualPathCandidate
```

Path law:

```text
No forced path closure under unresolved ambiguity.
No weight/derivation closure before testing the mabni path when mabni is plausible.
```

Example ambiguity:

```text
surface: من
possible_paths: RelativeNounCandidate / InterrogativeCandidate / ConditionalCandidate / PrepositionalHarfCandidate
status: AMBIGUOUS
residual: MABNI_FAMILY_AMBIGUOUS
forbidden: FinalMeaning / FinalSyntax / Truth
```

## §7 A3 lexeme contractability boundary

Neighbor-law continuity:

- `NOUN-L0` (docs/86): `NounIdentityReadinessCandidate`.
- `VERB-L0` (docs/87): `VerbIdentityReadinessCandidate`.
- `LGE-LINK-L0` (docs/83): `LinkOperatorCandidate`.
- `REF-PRON-L0` (docs/83): `ReferenceDemandSurface`.
- `MABNI-L0` (docs/84): `MabniCandidate`.
- `ZARF-L0` (docs/85): `AdverbialReadinessCandidate`.
- `LEX-DATA-1` witness-only (docs/81) and `LEX-BOUNDARY-L0` block on wad'i -> naql/majaz jumps (docs/82).

Unified output:

```text
LexemeContractabilityReadiness
```

Not:

```text
FinalMeaning
FinalSyntax
Ifadah
```

## §8 A4 composition precondition boundary

Composition opens only when contractability is visible:

```text
CompositionPrecondition =
At least one contractable relation set:
NounReadiness + VerbReadiness
or
NounReadiness + LinkOperatorCandidate
or
MabniFunctionalDemand + RequiredComplement
```

Triad regularity rule:

```text
No full composition claim without visible or residualized noun/verb/link regularity.
NounIdentityReadinessCandidate + VerbIdentityReadinessCandidate + LinkOperatorCandidate
is a higher-order regularity surface for complete composition claims.
Missing members must remain explicit as visible residuals.
```

Before composition only:

```text
SlotEligibilityCandidate
```

Not:

```text
FinalSyntacticSlot
FinalSyntacticRole
```

## §9 Allowed outputs in this law boundary

```text
ALLOWED_OUTPUTS = {
  AtomicSurfaceReadiness,
  WordSurfaceReadinessCandidate,
  PathReadinessCandidate,
  LexemeContractabilityReadiness,
  SlotEligibilityCandidate,
  CompositionPreconditionCandidate,
  PreCompositionAuditResult
}
```

## §10 Forbidden shortcuts and outputs

```text
FORBIDDEN_SHORTCUT_ASSERTIONS = {
  AtomicUnit -> DerivationFinal,
  AtomicUnit -> SyntaxFinal,
  AtomicUnit -> WadiMeaning,
  PathCandidate -> FinalPathCertificate,
  LexemeContractabilityReadiness -> FinalMeaning,
  LexemeContractabilityReadiness -> FinalSyntax,
  CompositionPreconditionCandidate -> Ifadah,
  CompositionPreconditionCandidate -> Hukm,
  CompositionPreconditionCandidate -> Truth
}
```

```text
FORBIDDEN_OUTPUTS = {
  AtomicMeaning,
  FinalWordMeaning,
  FinalMeaning,
  FinalSyntax,
  FinalSyntacticRole,
  FinalSyntacticSlot,
  NounIdentityCertificate,
  VerbIdentityCertificate,
  ParticleIdentityCertificate,
  ReferenceResolved,
  FinalRelation,
  Ifadah,
  Hukm,
  Truth,
  Certainty,
  Reality
}
```

## §11 Runtime embargo and sequencing

```text
RUNTIME_NOT_OPENED = {
  src_runtime_implementation,
  precomp_verifier_runtime,
  parser_changes,
  morphology_runtime,
  syntax_authority,
  semantic_runtime,
  ifadah_engine,
  hukm_engine,
  truth_engine
}
```

Safe sequencing:

```text
A0 atomic verification
-> A1 word surface verification
-> A2 path readiness verification
-> A3 lexeme contractability verification
-> A4 composition precondition verification
-> PRECOMP-C1 carrier surface
-> PRECOMP-G1 verifier gates
-> PRECOMP-T1 stress fixtures
```

## §12 Pre-composition checklist

```text
PRECOMP-L0 CHECKLIST

1. Atomic units verified?
   - every letter identified
   - every haraka identified or marked missing
   - every atomic trace present
   - no blocking atomic residual

2. Word surface verified?
   - order preserved
   - orthographic boundary declared
   - vocalization status declared
   - surface residuals visible

3. Path candidates declared?
   - noun / verb / harf / mabni / pronoun / zarf / residual
   - ambiguity visible
   - no forced path closure

4. Neighbor laws respected?
   - NOUN-L0
   - VERB-L0
   - LGE-LINK-L0
   - REF-PRON-L0
   - MABNI-L0
   - ZARF-L0
   - LEX-DATA witness-only
   - LEX-BOUNDARY blocks wad'i -> naql/majaz

5. Contractability declared?
   - identity readiness present
   - demand surface declared
   - trace_ref present
   - visible residuals present
   - forbidden outputs carried

6. Composition precondition satisfied?
   - no final syntax required before Comp
   - only slot eligibility allowed
   - triad regularity visible or residualized
   - no forbidden direct jump

7. Forbidden outputs absent?
   - FinalSyntax
   - FinalMeaning
   - Ifadah
   - Hukm
   - Truth
   - Certainty
   - Reality
```

## §13 Constitutional minimum examples

Example 1 (atomic):

```json
{
  "unit": "بَ",
  "allowed_output": "AtomicSurfaceReadiness",
  "forbidden_outputs": ["WadiMeaning", "SyntaxFinal", "Truth"]
}
```

Example 2 (atomic residual-visible):

```json
{
  "unit": "ضِ",
  "allowed_output": "AtomicSurfaceReadiness",
  "status": "PASS_WITH_RESIDUAL",
  "residuals": ["PHONETIC_TENSION_VISIBLE"],
  "forbidden_outputs": ["SyntaxFinal", "WadiMeaning", "Truth"]
}
```

Example 3 (unvocalized word):

```json
{
  "surface": "كتب",
  "allowed_output": "WordSurfaceReadinessCandidate",
  "residuals": ["UNVOCALIZED_SURFACE_RESIDUAL"],
  "forbidden_outputs": ["FinalMeaning", "Truth"]
}
```

Example 4 (noun lexeme):

```json
{
  "surface": "جبل",
  "allowed_outputs": [
    "NounIdentityReadinessCandidate",
    "LexemeContractabilityReadiness"
  ],
  "forbidden_outputs": ["FinalMeaning", "Truth"]
}
```

Example 5 (verb lexeme):

```json
{
  "surface": "ضرب",
  "allowed_outputs": [
    "VerbIdentityReadinessCandidate",
    "SubjectDemandSurface",
    "ObjectDemandSurface"
  ],
  "forbidden_outputs": ["ExternalPastEvent", "Ifadah", "Truth"]
}
```

Example 6 (path ambiguity):

```json
{
  "surface": "من",
  "allowed_outputs": [
    "LinkOperatorCandidate",
    "MabniPathCandidate"
  ],
  "residuals": ["MABNI_FAMILY_AMBIGUOUS"],
  "forbidden_outputs": ["FinalRelation", "Ifadah", "Truth"]
}
```

Example 7 (composition precondition only):

```json
{
  "surface": "ضرب زيد",
  "allowed_output": "CompositionPreconditionCandidate",
  "residuals": ["LINK_OPERATOR_TRIAD_PARTIAL_OR_IMPLICIT"],
  "forbidden_outputs": ["Ifadah", "Hukm", "Truth"]
}
```
