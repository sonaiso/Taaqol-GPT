# 04 — Forbidden Straight-Line Transitions

> **Status:** Constitutional skeleton in PR-0. Bound in PR-5: the
> typed registry lives in
> [`src/taaqqul_slot_geometry/core/forbidden_lines.py`](../src/taaqqul_slot_geometry/core/forbidden_lines.py).

A *forbidden straight line* is a direct transition from a lower layer
to a higher layer **without** an intervening `TransitionGate` that
carries `Evidence`, satisfies the `RankLattice`, and clears the
`ResidualPolicy`.

Forbidden does **not** mean impossible. It means: not as a direct move.
Every forbidden transition has a *required bridge gate* whose name the
registry carries; each bridge's preconditions belong to the future PR
that opens it.

## Canonical forbidden transitions

| Forbidden transition              | Why it is forbidden                                          | Required bridge                  |
| --------------------------------- | ------------------------------------------------------------ | -------------------------------- |
| `Binary → Text`                   | Bytes carry no script identity.                              | `EncodingIdentityGate`           |
| `Unicode → ArabicLetter`          | A code point is an encoding trace, not a letter identity.    | `LetterIdentityGate`             |
| `CodePoint → Phoneme`             | A code point is not a sound.                                 | `PhoneticRealisationGate`        |
| `Grapheme → FunctionalLetter`     | A graphical mark is not a functional letter.                 | `LetterFunctionGate`             |
| `HarakaMark → CaseFunction`       | A vowel mark is not a case role without position and syntax. | `HarakaFunctionGate`             |
| `Orthography → Pronunciation`     | Spelling is not pronunciation.                               | `PhoneticRealisationGate`        |
| `Pronunciation → Syllable`        | Sounds are not syllables without prosodic structure.         | `SyllableStructureGate`          |
| `Syllable → Word`                 | Syllables are not words without lexical identity.            | `LexicalIdentityGate`            |
| `Signifier → WordForm`            | A signifier is not a word-form without morphological law.    | `MorphologicalRealisationGate`   |
| `WordForm → Meaning`              | A form is not a meaning without context and convention.      | `SignificationGate`              |
| `Root → LexicalMeaning`           | A root is not a meaning; it is a derivational locus.         | `DerivationGate`                 |
| `Weight → Agency`                 | A morphological pattern is not a syntactic role.             | `RelationRoleGate`               |
| `Pattern → SyntaxRole`            | Pattern is not role without relation and context.            | `RelationRoleGate`               |
| `VerbalSignified → PureConcept`   | A signified is not a pure concept.                           | `ConceptualAbstractionGate`      |
| `Wadʿ → Dalālah` (no domain)      | Convention is not signification without a stated domain.     | `DomainBoundDalalahGate`         |
| `Dalālah → ContextualMeaning`     | Signification is not contextual meaning without context.     | `ContextualResolutionGate`       |
| `PureConcept → IntendedMeaning`   | A concept is not an intended meaning without an utterer.     | `IntentAttributionGate`          |
| `Context → Relation`              | Context is not a relation.                                   | `RelationDeclarationGate`        |
| `Relation → Ifādah`               | Relation is not informative content.                         | `IfadahGate`                     |
| `Ifādah → Judgment`               | Informative content is not a judgment.                       | `JudgmentGate`                   |
| `Judgment → Application`          | A judgment is not its application.                           | `ApplicationGate`                |
| `Evidence → Certainty`            | Evidence has a rank; it never equals certainty.              | `RankLattice` (no auto-promote)  |
| `LexiconEntry → Candidate`        | A lexicon entry is a witness, not a generator.               | `LexiconEvidenceGate`            |
| `Candidate → Certificate`         | A candidate becomes a certificate only with higher evidence. | `CertificationGate`              |
| `ResidualHidden → ApprovedOutput` | Hidden residuals block all approved outputs.                 | `ResidualPolicy` (visibility)    |
| `RankBelow → RankAbove`           | No rank promotion without a gate verdict.                    | `TransitionGate` + `RankLattice` |
| `Tool/Number/LCNV → Knowledge`    | An instrument or measurement is not knowledge.               | `ToolBoundaryGate`               |

The full registry, including all of the above plus the
technical-terminology cases from
[`10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md`](10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md),
is expressed as data (not code) in PR-5 and queried by
`is_forbidden_direct(src, tgt)`.

## Pre-text declared-entry transitions

These transitions are forbidden by the **Declared Entry Boundary
Law** (see
[`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md)
§13). The current operational entry is `ArabicVocalizedText`; the
pre-text chain is preserved as prior trace but is out of current
execution. Each row's required bridge is **declared, not
implemented**: opening any of them requires an explicit future PR
that satisfies the Forbidden Straight-Line Law.

| Forbidden transition              | Why it is forbidden                                          | Required bridge (declared)        |
| --------------------------------- | ------------------------------------------------------------ | --------------------------------- |
| `HumanVoice → ArabicText`         | A voice event is not a written text without decoding and ASR. | `AudioDecodingGate` + `ASRGate`  |
| `BinaryAudio → Text`              | Audio bytes carry no text identity.                          | `AudioDecodingGate`               |
| `BinaryAudio → UnicodeText`       | Audio bytes are not code points.                             | `AudioDecodingGate` + `ASRGate`   |
| `BinaryAudio → Meaning`           | Audio bytes are not meaning.                                 | Full pre-text + interpretation chain |
| `BinaryText → Unicode`            | Bytes are not code points without a stated encoding.         | `EncodingDecodeGate`              |
| `BinaryText → ArabicLetter`       | Bytes are not letters.                                       | `EncodingDecodeGate` + `LetterIdentityGate` |
| `Unicode → ArabicText`            | Code points are an encoding trace, not normalised script.    | `UnicodeTextNormalizationGate`    |
| `Unicode → ArabicLetter`          | A code point is an encoding trace, not a letter identity.    | `ArabicLetterIdentityGate`        |
| `CodePoint → Phoneme`             | A code point is not a sound.                                 | `PhonemeEvidenceBridge`           |
| `Grapheme → FunctionalLetter`     | A graphical mark is not a functional letter.                 | `FunctionalLetterGate`            |
| `VocalizedText → ValidAnalysis`   | A vocalized text is a `TextTraceCandidate`, not an analysis. | `TextEntryValidationGate`         |
| `DeclaredEntry → OntologicalOrigin` | A declared operational entry is not the origin of the trace. | none — refusal is constitutional |

Until each bridge is opened by a future PR, every one of these
transitions emits `FORBIDDEN_STRAIGHT_LINE` (the failure code was
named in PR-1; the typed registry landed in PR-5).

## PR-5 binding

The registry lives in
[`src/taaqqul_slot_geometry/core/forbidden_lines.py`](../src/taaqqul_slot_geometry/core/forbidden_lines.py)
and is pure data behind pure queries:

- `ForbiddenLine` — one layer-leap row: `source`, `target`, `reason`,
  `required_bridge`, `origin_law`, and the named `failure_code`
  (always `FORBIDDEN_STRAIGHT_LINE`).
- `TerminologyTransfer` — one docs/10 domain-leap row: `(term,
  source_domain, target_domain, required_bridge)` plus origin and
  failure code. Kept as a *separate* carrier behind a separate query
  surface so the two laws never collapse into one mechanism.
- `ForbiddenLineRegistry` — the immutable registry value holding both
  surfaces; queried by `find` / `is_forbidden_direct` (layer leaps)
  and `find_term_transfer` / `is_forbidden_term_transfer` (docs/10).
  Matching is exact after strip + casefold, so `Layer` enum names
  meet the constitutional row names.
- `FORBIDDEN_STRAIGHT_LINES` — every canonical row above, every
  pre-text declared-entry row, and the six docs/16 §4 chain lines
  merged in as the constitution requires.
- `CANONICAL_REGISTRY` — the constitutional instance;
  `is_forbidden_direct(src, tgt)` at module level answers over it.

Transcription notes: the compound row `Tool/Number/LCNV → Knowledge`
is entered as three rows so the query contract answers each name;
pairs stated by both tables (`CodePoint → Phoneme`,
`Grapheme → FunctionalLetter`, `Unicode → ArabicLetter`) keep both
rows, and `find` returns the canonical-table row first. The
`DeclaredEntry → OntologicalOrigin` row carries
`none — refusal is constitutional` as its bridge: no future PR may
open it.

`TransitionGate.decide` step 2 consults `CANONICAL_REGISTRY`
(docs/08 — PR-5 binding): a registered line is fatal before any
retryable refusal. No bridge gate is implemented in PR-5: the
`CertificationGate` and every other named bridge remain declared
residuals of their own future PRs.
