# 100 — Licensed Lexicon Slot Geometry Boundary Law (LEXICON-SLOT-L0)

> Status: constitutional law document (law-only).
> Scope: declares the lexicon as a licensing surface, not a meaning/truth engine.
> Constitutional continuity: docs/81 + docs/82 + docs/89 + docs/99.

## §1 Constitutional definition of lexicon responsibility

```text
LEXICON_NOT_EQUAL = {FinalContextualMeaning, OntologicalFact, EmpiricalFact, Ifadah, Hukm, Truth, RealityCertificate}
LEXICON_ROLE = SourceRegistry + IdentityRegistry + WadRegistry + UsageEvidence + LicensedTransitions + ResidualAudit + Trace
LEXICON_OUTPUT = LexicalEntity ↛ LexicalMadlulCandidate
```

The lexicon does not own final contextual meaning. It licenses bounded lexical-transition candidates.

## §2 Licensed slot geometry for lexical outputs

Every lexical output must be a licensed slot, never a free meaning value:

```text
LexicalSlot = <
  Anchor,
  Identity,
  Type,
  Domain,
  Boundary,
  Source,
  Operation,
  Invariant,
  Evidence,
  RankVector,
  Trace,
  Residuals,
  Closure
>
```

No lexical output without this geometry.

## §3 Identity separation discipline

```text
GraphicIdentity != PhonologicalIdentity != LexemeIdentity != RootIdentity != SenseIdentity
```

No path may collapse these identities into one field.

## §4 Rank-vector discipline

A lexical result must carry independent rank channels:

```text
RankVector = (
  r_source,
  r_reading,
  r_identity,
  r_root,
  r_wad,
  r_sense,
  r_usage,
  r_ontology
)
```

No single scalar rank may replace this vector in this branch.

## §5 Contract-only transition surface

The initial execution package opens contracts only:

```text
TC_SR : SourceSlot        ↛ ReadingCandidate
TC_RI : ReadingCandidate  ↛ IdentityCarrier
TC_IL : IdentityCarrier   ↛ LexicalEntitySlot
TC_LW : LexicalEntitySlot ↛ WadCandidate
TC_WS : WadCandidate      ↛ LexicalSenseSlot
TC_SD : LexicalSenseSlot  ↛ DalalahCandidateSlot
```

No semantic/hukm/truth runtime is opened in this law step.

## §6 Vertical pilot boundary (bounded)

A bounded pilot path is licensed from real source evidence to a lexical dalalah candidate slot:

```text
SourceSlot -> ReadingSlot -> IdentitySlot -> LexicalEntitySlot -> WadSlot -> LexicalSenseSlot -> UsageSlot -> DalalahCandidateSlot
```

The pilot remains candidate-only and must preserve visible residuals.

## §7 Final constitutional rules

```text
No Lexical Output Without LicensedSlot
No LicensedSlot Without Source+Identity+Type+Domain+Evidence+RankVector+Residuals+Trace
LexiconClosure != MeaningClosure
```

RUNTIME_NOT_OPENED = {
  semantic_truth_engine,
  contextual_meaning_closure,
  hukm_closure,
  reality_certificate
}

This document is law-only: it introduces no direct semantic/hukm/truth closure runtime.
