# 99 — Constitutional Lexicon Licensing Architecture Law (LEXICON-L1)

> Status: constitutional law document (law-only).
> Scope: declarative boundary for a multi-layer lexical licensing architecture.
> Snapshot date: 2026-08-03.

## §1 Governing role and constitutional equation

```text
LEXICON_NOT_EQUAL = {MeaningGenerator, Ifadah, Hukm, Truth, Certainty, Reality}
LEXICON_ROLE = LicensedConventionRegistry + EvidenceGraph + ConceptualCapability + ResidualAudit
LICENSED_TRANSITION = ContractableUnit -> LexicalMadlulCandidate
```

A constitutional lexicon is an auditable licensing surface.
It is not a final-meaning engine and not a hukm/truth engine.

## §2 Constitutional knowledge-transition graph

This branch is governed as a knowledge constitution, not a linear
meaning shortcut:

```text
Reality/Usage
-> Source Evidence
-> Identity Constitution
-> Lexical Constitution
-> Ontological Constitution
-> Semantic Constitution
-> Relational Constitution
-> Ifadah Constitution
-> Judgment Constitution
-> Application
```

The transition is graph-shaped (directed with bounded rollback), not a
single irreversible line.

```text
Source -> Identity -> Lexical -> Ontology -> Semantics -> Ifadah -> Judgment
                                             ^                         |
                                             |----- Residual Review ---|
```

Residual-triggered rollback is mandatory with trace preservation.

## §2 Top-level lexical entity discipline

Root-centric extraction is insufficient as a universal lexical top node.
The top unit is `LexicalEntity` with bounded paths:

```text
LexicalEntity
├── RootEntity
├── JamidStemEntity
├── DerivedLexemeEntity
├── MabniEntity
├── FunctionUnitEntity
├── ProperNameEntity
├── BorrowedEntity
├── CompoundLexicalEntity
└── ResidualOrUnresolvedEntity
```

No path may force every lexical unit into a root-derived claim.

## §2.1 Source constitution boundary

Source layer output is witness-only and must preserve:

```text
SourceRecord = {
  SourceID, Text, Edition, Evidence, Trace, Residuals, ReviewState
}
```

Law marker:

```text
NO_KNOWLEDGE_WITHOUT_PRESERVED_SOURCE
```

## §2.2 Identity constitution boundary

Identity proof establishes carrier continuity for the lexical entry
before any lexical/semantic transition.

Law marker:

```text
NO_TRANSITION_BEFORE_IDENTITY_PRESERVATION
```

## §3 Layered lexicon architecture (source -> licensing)

### §3.1 Preserved source layer

```text
SourceDocument
SourcePage
SourcePassage
SourceTokenSpan
SourceImageRegion
ExtractionRun
```

Raw source text is preserved and never silently replaced by corrected text.

### §3.2 Reading and critical verification layer

```text
RawReading NOT_EQUAL CriticalReading
```

Every extracted form may produce multiple `ReadingCandidate` rows with:
- reading status
- confidence
- evidence refs
- residual visibility

### §3.3 Lexeme identity layer

`LexemeIdentity` separates script-form identity, phonological identity,
lexeme identity, and root identity. Identity conflation is forbidden.

### §3.4 Root path discipline

```text
SurfaceForm DOES_NOT_IMPLY RootIdentity
RootIdentity requires RootPathGate
```

`RootPathGate` checks radicals, substitution/weakness behavior,
assimilation constraints, jamid possibility, mabni possibility,
borrowed possibility, and source-backed path evidence.

### §3.5 Conceptual-origin claim layer

`MaqayisConceptualOrigin` is a source-attributed conceptual anchor,
not final semantic closure:

```text
MaqayisOrigin = SourceAssertedConceptualAnchor
```

### §3.6 Lexical-sense and usage layer

The following surfaces are constitutionally distinct:

```text
SourceGloss NOT_EQUAL ConceptualOrigin
ConceptualOrigin NOT_EQUAL LexicalSense
LexicalSense NOT_EQUAL ContextualSenseCandidate
```

Each lexical sense must carry `UsageEvidence` (citation, era, domain,
usage type, and evidence rank).

### §3.7 Derivational operation layer

No generic `DERIVED_FROM` edge is sufficient by itself.
Every derivational relation must be represented as `DerivationOperation`
with declared invariants, licensed changes, and evidence.

## §3.8 Ontological constitution boundary (mandatory before semantic closure)

`Ontological Constitution` does not ask only for lexical designation.
It asks for the ontological profile of the designated referent class:

```text
OntologicalProfile = {
  Genus,
  Species,
  EssentialProperties,
  AccidentalProperties,
  Capabilities,
  Constraints
}
```

`Capability` is a possibility condition, not an automatic effect:

```text
Capability NOT_EQUAL Containment
Capability NOT_EQUAL Commitment
```

Definition marker:

```text
CAPABILITY = existential possibility under conditions and no blockers,
             without implying necessary occurrence.
```

## §3.9 Semantic constitution transition discipline

Correspondence/containment/commitment transitions are licensed in this
order:

```text
LexicalForm -> Genus -> Identity -> CorrespondenceCandidate
Genus -> EssentialProperties -> Capability -> ContainmentCandidate
Capability -> NecessaryRelations -> Context -> CommitmentCandidate
```

No direct shortcut from lexical form to commitment is constitutional.

## §3.10 Knowledge-domain separation

Three knowledge domains are constitutionally distinct:

```text
LexicalKnowledge      = what language users placed by convention
OntologicalKnowledge  = genus/species/properties/capabilities of referent class
EmpiricalKnowledge    = observed/tested actual state in reality/usage
```

None may collapse into another without an explicit licensed bridge and
trace evidence.

## §4 Ingestion and review pipeline

Raw extracted entries may not enter licensed lexicon storage directly.
The minimum constitutional flow is:

```text
HTML Entry
-> RawImportedEntry
-> StructuralValidation
-> ReadingCandidateSet
-> RootIdentityCandidate
-> SourceClaimCandidate
-> Human/Rule Review
-> LicensedLexicalRecord
```

`AUTO_AGREED` is extraction agreement only. It does not imply
`HUMAN_VERIFIED` and does not imply `CONSTITUTIONALLY_LICENSED`.

## §5 Residual taxonomy and severity

`REVIEW_REQUIRED` alone is insufficient as a constitutional residual surface.
Minimum residual classes include:

```text
OCR_UNCERTAIN
ROOT_BOUNDARY_UNCERTAIN
WRONG_BAB_SUSPECTED
INDEX_FRAGMENT
EMPTY_ROOT
SINGLE_LETTER_NOISE
DUPLICATE_ENTRY
SOURCE_TEXT_TRUNCATED
ORIGIN_COUNT_UNCERTAIN
GLOSS_UNCERTAIN
ROOT_LETTER_CONFUSION
HAMZA_NORMALIZATION_UNRESOLVED
WEAK_LETTER_UNRESOLVED
LEXEME_ROOT_CONFLICT
SOURCE_DISAGREEMENT
HUMAN_REVIEW_REQUIRED
BLOCKING
DEFERRED
REPAIRABLE
NON_BLOCKING
CONTRADICTORY
```

Blocking residuals must prevent lexical licensing.

## §6 Rank discipline (component-wise, not scalar-only)

Each lexical claim surface carries an independent rank channel.
Minimum bounded vocabulary:

```text
RAW
EXTRACTED
AUTO_ALIGNED
SOURCE_ASSERTED
CROSS_SOURCE_SUPPORTED
HUMAN_VERIFIED
CONSTITUTIONALLY_LICENSED
DISPUTED
BLOCKED
```

No single scalar confidence may erase per-surface rank differences.

## §7 Lexical license gate

Lexical licensing is defined by:

```text
LexicalLicense(x)=1 iff
IdentityProof(x)
AND SourceBound(x)
AND ClassificationDeclared(x)
AND EvidenceExists(x)
AND NoBlockingResidual(x)
AND Rank >= MinimumLexicalRank
```

Allowed opening from this law boundary:

```text
ALLOWED_OUTPUTS = {
  LexicalMadlulCandidate,
  CompositionReadiness
}
```

Forbidden opening from this law boundary:

```text
FORBIDDEN_OUTPUTS = {
  RelationCandidate,
  IfadahCandidate,
  HukmCandidate,
  RealityCandidate,
  FinalMeaning,
  Truth,
  Certainty
}
```

## §7.1 Transition-contract registry (TC-01..TC-06)

Every transition requires an explicit contract with conditions, output,
residual policy, and trace obligations.

```text
TC-01 Source -> Identity
conditions:
  preserved_source
  identity_stability
  trace_recorded
  no_blocking_residual
output: IdentityCarrier

TC-02 Identity -> Lexical Constitution
conditions:
  identity_verified
  attested_lexical_placement
  unresolved_lexical_conflict_absent
output: LexicalMeaning

TC-03 Lexical -> Ontological Constitution
conditions:
  genus_declared
  species_declared_if_available
  essential_properties_extracted
  capabilities_extracted
  potential_blockers_recorded
output: OntologicalProfile

TC-04 Ontological -> Semantic Constitution
conditions:
  genus_proven
  essential_properties_proven
  capability_conditions_satisfied
  blocking_residual_absent_for_transition
output:
  CorrespondenceCandidate
  ContainmentCandidate
  CommitmentCandidate

TC-05 Semantic -> Ifadah Constitution
conditions:
  compositional_relations_complete
  isnad_verified
  relation_graph_closed
  non_blocking_residuals_visible
output: IfadahCandidate

TC-06 Ifadah -> Judgment Constitution
conditions:
  sufficient_evidence
  no_blocking_residual
  review_passed
  judgment_scope_declared
output: JudgmentCandidate
```

Judgment transition is forbidden before `IfadahCandidate`.

## §8 Minimum first runtime scope (deferred)

When runtime is admitted in a future licensed step, minimum first scope is:

```text
Root
SourcePassage
CriticalReading
ConceptualOrigin
Lexeme
LexicalSense
DerivationLink
Evidence
Rank
Residual
Trace
```

With exactly three initial paths:

```text
ROOT_BASED
JAMID
UNRESOLVED
```

## §9 Runtime embargo in this step

```text
RUNTIME_NOT_OPENED = {
  lexical_license_gate_runtime,
  root_path_gate_runtime,
  reading_resolver_runtime,
  claim_alignment_runtime,
  lexical_meaning_runtime,
  ifadah_runtime,
  hukm_runtime,
  truth_engine
}
```

LEXICON-L1 is law-only and introduces no runtime code, no carriers,
no parser extension, no database migration, and no semantic/hukm/truth/reality execution.

## §10 Boundary continuity

- Continuity with docs/81: lexical evidence remains witness-bound and source-attested.
- Continuity with docs/82: wad'i licensing does not imply naql/majaz licensing.
- Continuity with docs/89: `ContractableUnit` remains the admissible upstream unit for lexical licensing.
- Continuity with docs/41..46: ifadah/judgment/application remain licensed downstream steps with no shortcut from lexical layer.
- No straight line is licensed from lexical entry to final meaning/hukm/reality.
