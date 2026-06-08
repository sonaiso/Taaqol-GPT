# 04 — Forbidden Straight-Line Transitions

> **Status:** Constitutional skeleton in PR-0. The typed registry and
> the full table land in PR-4.

A *forbidden straight line* is a direct transition from a lower layer
to a higher layer **without** an intervening `TransitionGate` that
carries `Evidence`, satisfies the `RankLattice`, and clears the
`ResidualPolicy`.

Forbidden does **not** mean impossible. It means: not as a direct move.
Every forbidden transition has a *required bridge gate* whose name and
preconditions will be specified in PR-4.

## Canonical forbidden transitions (partial — full registry in PR-4)

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
will be expressed as data (not code) in PR-4 and queried by
`is_forbidden_direct(src, tgt)`.
