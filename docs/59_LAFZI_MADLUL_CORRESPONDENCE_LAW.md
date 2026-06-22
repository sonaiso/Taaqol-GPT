# 59 — Lafzi Madlul Correspondence Law

> **Status:** Constitutional law document. Ratified in LAFZI-B0.
> Constitutional origin: docs/58 (DalAlone Atomic Closure Law), docs/47
> (Post-Vertical Roadmap), docs/51 (Maʿqūl Branch Discipline Law), docs/52
> (Constitutional Test Origin Covenant), and docs/14 (PR Chain Roadmap).
>
> This document defines the **LafziMadlul correspondence boundary**. It is
> law-only: it introduces no runtime code, no carriers, no enums, no
> operations, no adapter change, no audit change, and no global `FailureCode`
> expansion.
>
> Numbering note: docs/56 and docs/57 remain reserved for GPT reasonableness
> boundary documents, docs/58 is the DalAlone Atomic Closure Law, so this law
> uses docs/59.

---

## §1 Governing principle

```text
No LafziMadlulCandidateSet before DalAloneClosed.
No LafziMadlulClosed from DalAloneClosed alone.
NoAutomaticOneToOneMapping.
Correspondence is an opened gate, not closure.
No lafzi output may emit wadʿī meaning, mutābaqah, taḍammun, iltizām,
relation, composition, ifādah, hukm, tanzīl, or reality.
```

`DalAloneClosed` proves only that the signifier-alone surface is atomically
closed. It opens the next verbal-signified boundary, but it does not decide
what verbal signified has closed.

The only lawful first transition is:

```text
DalAloneClosed
  -> LafziMadlulGate
  -> LafziMadlulCandidateSet
```

The following shortcut is forbidden:

```text
DalAloneClosed -> LafziMadlulClosed
```

The law therefore installs the correspondence discipline:

```text
DalAloneClosed opens LafziMadlulGate.
LafziMadlulGate may produce LafziMadlulCandidateSet.
LafziMadlulCandidateSet is not LafziMadlulClosed.
```

---

## §2 Domain and non-domain

### §2.1 Domain

`LafziMadlulGate` may inspect only the licensed post-DAL verbal-signified
surface:

```text
DalAloneClosedRef
WordKindCandidate
SourceIdentityCandidate
FormStateCandidate
InternalWordPathCandidate
LafziScope
LafziResidualAudit
```

The domain is lafẓī: it concerns the bounded verbal-signified candidacy of a
closed signifier. It is not a semantic lexicon and not a syntactic relation.

### §2.2 Non-domain

`LafziMadlulGate` and `LafziMadlulCandidateSet` must not emit or infer:

```text
Wad'iMadlul
WadiMadlul
Wad'iMeaning
LexicalMeaning
MutabaqahCandidate
TadammunCandidate
IltizamCandidate
RelationCandidate
CompositionCandidate
IfadahCandidate
HukmCandidate
TanzilCandidate
ActualFa'il
ActualSubject
ActualObject
ActualRelation
Reality
Ontology
TruthValue
```

A successful correspondence opens only lafzi candidacy. It does not cross into
wadʿī madlūl, dalālah relations, composition, ifādah, hukm, or reality.

---

## §3 Correspondence mapping states

The correspondence from a closed dal to lafzi madlul candidates is not
permanently one-to-one.

```text
MappingState =
    ONE_TO_ONE
  | ONE_TO_MANY
  | BLOCKED
  | DEFERRED
```

Required meanings of the mapping states:

```text
ONE_TO_ONE   : one visible lafzi candidate is licensed by the gates.
ONE_TO_MANY  : multiple lafzi candidates remain visible; closure is not automatic.
BLOCKED      : the path is forbidden or unused and cannot open lafzi candidacy.
DEFERRED     : evidence is incomplete but non-blocking residuals remain visible.
```

Examples:

| DalAloneClosed | permitted correspondence result |
| -------------- | -------------------------------- |
| `مِنْ`         | `ONE_TO_ONE` harf/operator candidate |
| `رَجُل`        | `ONE_TO_ONE` ism/entity-carrier candidate |
| `ضَرَبَ`       | `ONE_TO_ONE` fiʿl/masdar-temporal candidate |
| `علم`          | `ONE_TO_MANY` or `DEFERRED` because vocalization is incomplete |
| unused lafẓ    | `BLOCKED` |

---

## §4 Candidate-set contract

The later `LafziMadlulCandidateSet` carrier must carry at least:

```text
LafziMadlulCandidateSet =
    dal_alone_closed_ref
    mapping_state
    candidates
    lafzi_scope
    residuals
    trace_ref
```

It must not carry:

```text
meaning
wad_i_madlul
mutabaqa
tadammun
iltizam
relation
composition
ifada
hukm
reality
```

The candidate set may be empty only when `mapping_state = BLOCKED` and a
visible blocking residual explains the refusal.

---

## §5 Later carrier vocabulary opened by this law

This law opens, but does not implement, the following LAFZI-B1 carrier surface:

```text
LafziMadlulCandidate
LafziMadlulCandidateSet
LafziMadlulClosed
WordKindCandidate
SourceIdentityCandidate
FormStateCandidate
InternalWordPathCandidate
LafziResidual
LafziScope
```

The required shape of a later `LafziMadlulCandidate` is:

```text
LafziMadlulCandidate =
    dal_alone_closed_ref
    word_kind_candidate
    source_identity_candidate
    form_state_candidate
    internal_word_path_candidate
    lafzi_scope
    residuals
    state
    trace_ref
```

A later carrier must not include:

```text
meaning
mutabaqa
tadammun
iltizam
relation
ifada
hukm
```

---

## §6 WordKindGate law opened for LAFZI-B2

The first post-correspondence question is word kind, not meaning and not
syntactic function.

```text
WordKindGate =
    ISM
  | FIIL
  | HARF
  | AMBIGUOUS
  | BLOCKED
```

Binding laws:

```text
NoLafziMadlulWithoutWordKind.
NoWordKindFromUnclosedDal.
NoWordKindIfMultipleCandidatesWithoutResiduals.
```

Examples:

| DalAloneClosed | WordKindGate result |
| -------------- | ------------------- |
| `مِنْ`         | `HARF` |
| `رَجُل`        | `ISM` |
| `ضَرَبَ`       | `FIIL` |
| `علم`          | `AMBIGUOUS` / `DEFERRED` |
| `هو`           | `ISM` built/reference path |
| `لا`           | `HARF` / operator-family candidate, no wadʿī meaning yet |

Existing formal-shape definitions for `ISM`, `FI'L`, and `HARF` may be used
only as formal evidence. They do not produce meaning.

---

## §7 SourceIdentityGate law opened for LAFZI-B3

Word kind is insufficient. A lafzi candidate also requires source identity or
visible residuals.

```text
WordKind -> SourceIdentity
```

For ism:

```text
Ism = IdentityCarrier
```

Permitted source-identity paths include:

```text
JAMID_ENTITY
MUSHTAQ_MASDAR_ROLE
MASDAR_ABSTRACT_TRANSFORMATION
PROPER_SELF_DESIGNATION
PRONOUN_BUILT_REFERENCE
DEMONSTRATIVE_PRESENT_REFERENCE
RELATIVE_LATER_LINK
DEFERRED_SOURCE
```

For fiʿl:

```text
Fiil = MasdarIdentity + TemporalOrRequestImage
NoFiilWithoutMasdarOrVisibleResidual.
```

For harf:

```text
Harf = RelationOperatorIdentity.
HarfLafziMadlul != RelationActual.
```

Binding law:

```text
NoSourceIdentity => DeferredLafziMadlul.
```

---

## §8 FormStateGate law opened for LAFZI-B4

No lafzi candidate closes without internal form state or visible residuals.

```text
FormState =
    MABNI
  | MURAB_POTENTIAL
  | VERB_BUILT_FORM
  | IMPERFECT_IRAB_POTENTIAL
  | DEFERRED
```

Binding laws:

```text
NoLafziMadlulWithoutFormStateOrResidual.
Mu'rabPotential != ActualI'rab.
Mabni != SemanticFunction.
```

Examples:

| DalAloneClosed | FormState |
| -------------- | --------- |
| `مِنْ`         | `MABNI` |
| `هذا`          | `MABNI` |
| `رَجُل`        | `MURAB_POTENTIAL` |
| `ضَرَبَ`       | `VERB_BUILT_FORM` |
| `يَضْرِبُ`     | `IMPERFECT_IRAB_POTENTIAL` |
| `علم`          | `DEFERRED` |

---

## §9 InternalWordPathGate law opened for LAFZI-B5

After word kind, source identity, and form state, a lafzi candidate requires an
internal word path or visible residuals.

### §9.1 Ism path

```text
IsmPath =
    JAMID
  | MUSHTAQ
  | MASDAR
  | PROPER
  | REFERENCE
  | BUILT_NAME
  | DEFERRED
```

Binding laws:

```text
NoIsmWithoutInternalPathOrResidual.
NoMushtaqWithoutMasdar.
NoProperWithoutSelfDesignation.
NoPronounWithoutBuiltReference.
```

### §9.2 Fiʿl path

```text
FiilPath =
    Masdar
  + ValencyPotential
  + VoicePotential
  + TemporalOrRequestImage
```

Binding laws:

```text
NoFiilWithoutMasdar.
NoActualTransitivityWithoutMasdar.
NoFa'ilFromIsolatedFiil.
NoMaf'ulFromIsolatedFiil.
```

### §9.3 Harf path

```text
HarfPath =
    BuiltOperator
  + RelationNeed
  + OperandNeed
  + NoIndependence
```

Binding laws:

```text
HarfLafziMadlul names relation-operator candidacy.
HarfLafziMadlul != RelationActual.
NoActualRelationFromIsolatedHarf.
```

---

## §10 LafziScope law

No lafzi candidate closes without a bounded scope.

```text
LafziScope =
    LanguageScope
  + RegisterScope
  + UsageScope
  + VocalizationScope
  + LoanOrNativeScope
```

Examples:

| surface state | scope |
| ------------- | ----- |
| fully vocalized Arabic lafẓ | general Arabic scope |
| unvocalized lafẓ | candidate scope |
| loan/arabized lafẓ | loan/arabized scope |
| unused lafẓ | blocked/unused scope |
| symbol or abbreviation | symbolic scope |

Binding law:

```text
NoScope => DeferredLafziMadlul.
```

---

## §11 Local lafzi residual vocabulary

Lafzi residuals are local to this boundary unless a later law promotes one into
the global `FailureCode` taxonomy. They are qualitative / identity residuals,
not DAL acoustic or graphic residuals.

The required local vocabulary is:

```text
WORD_KIND_AMBIGUOUS
SOURCE_IDENTITY_REQUIRED
FORM_STATE_REQUIRED
ISM_PATH_AMBIGUOUS
FIIL_MASDAR_REQUIRED
FIIL_TEMPORAL_IMAGE_REQUIRED
HARF_OPERATOR_REQUIRED
REFERENCE_SOURCE_REQUIRED
PROPER_SELF_DESIGNATION_REQUIRED
MUSHTAQ_REQUIRES_MASDAR
MULTIPLE_LAFZI_CANDIDATES
LAFZI_SCOPE_REQUIRED
UNUSED_DAL_NO_LAFZI
LOAN_LAFZI_PATH_REQUIRED
FORBIDDEN_WADI_JUMP
FORBIDDEN_MUTABAQA_JUMP
FORBIDDEN_RELATION_JUMP
FORBIDDEN_HUKM_JUMP
```

Hard refusals map to existing global refusal names, including:

```text
GATE_REQUIRED
BOUNDARY_MISSING
TRACE_MISSING
SCOPE_MISSING
HIDDEN_RESIDUAL
BLOCKING_RESIDUAL_PRESENT
FORBIDDEN_STRAIGHT_LINE
OUTPUT_EXCEEDS_LAYER
```

No residual may be hidden to produce lafzi closure.

---

## §12 Lafzi closure states

A later `LafziMadlulState` must distinguish:

```text
CLOSED
DEFERRED
BLOCKED
```

`CLOSED` is licit only if all are present and non-blocking:

```text
DalAloneClosed
+ WordKindClosed
+ SourceIdentityClosed
+ FormStateClosed
+ InternalWordPathClosed
+ LafziScope
+ VisibleResiduals
```

`DEFERRED` is required when there are multiple candidates or missing but
non-blocking evidence, such as unvocalized `علم`.

`BLOCKED` is required when the path is unlicensed, such as:

```text
Harf -> Masdar
Fiil -> MamnuMinSarf
unused lafẓ -> LafziMadlulClosed
```

---

## §13 CorrespondenceNotClosureLaw

```text
CorrespondenceNotClosureLaw:
    DalAloneClosed opens a correspondence candidate set.
    It does not close lafzi madlul automatically.
```

The forbidden shortcut is:

```text
DalAloneClosed -> LafziMadlulClosed
```

The licensed chain is:

```text
DalAloneClosed
  -> LafziMadlulCandidateSet
  -> WordKindGate
  -> SourceIdentityGate
  -> FormStateGate
  -> InternalWordPathGate
  -> LafziScope
  -> LafziResidualAudit
  -> LafziMadlulClosed
```

---

## §14 LafziMadlul is not Wad'iMadlul

```text
LafziMadlul != Wad'iMadlul.
LafziMadlulClosed opens Wad'iMadlulGate only.
LafziMadlulClosed does not cross Wad'iMadlulGate.
```

Examples:

| word | lafzi madlul | wadʿī madlul |
| ---- | ------------ | ------------ |
| `رجل` | ism identity-carrier candidate | human male by lexical placement |
| `ضرب` | fiʿl/masdar path candidate according to vocalization | placed meaning of striking |
| `من` | harf relation-operator candidate | ibtidāʾ / tabʿīḍ / bayān by context |
| `عين` | ism identity-carrier candidate | water spring / eye / spy / sun-eye deferred |

The lafzi layer may answer "what bounded verbal-signified kind can this closed
lafẓ carry?" It must not answer "which wadʿī meaning is intended?"

---

## §15 Golden examples

### §15.1 `مِنْ`

```text
DalAloneClosed
  -> HARF
  -> RelationOperatorIdentity
  -> MABNI
  -> BuiltOperator
  -> LafziMadlulClosed
```

Forbidden output: `ActualRelation`.

### §15.2 `رَجُل`

```text
DalAloneClosed
  -> ISM
  -> EntityCarrier
  -> MURAB_POTENTIAL
  -> JAMID
  -> LafziMadlulClosed
```

Forbidden output: `ActualFa'il`.

### §15.3 `ضَرَبَ`

```text
DalAloneClosed
  -> FIIL
  -> Masdar(ضرب)
  -> PastForm
  -> TemporalImage
  -> LafziMadlulClosed
```

Forbidden output: external occurrence or `ActualSubject`.

### §15.4 `علم`

```text
DalAloneClosed
  -> MULTIPLE_LAFZI_CANDIDATES
  -> DEFERRED
```

Forbidden output: automatic closure.

### §15.5 `عين`

```text
DalAloneClosed
  -> ISM
  -> IdentityCarrier
  -> LafziMadlulClosed
  -> Wad'iMadlulGate opened only
```

Forbidden output: choosing which `عين` wadʿī meaning is intended.

---

## §16 Negative jump matrix

The following transitions must fail or remain forbidden until separately
licensed:

| forbidden transition | reason |
| -------------------- | ------ |
| `DalOnlyCandidate -> LafziMadlulCandidateSet` | dal is not atomically closed |
| `DalAloneClosed -> WordKind` without gate | gate bypass |
| `DalAloneClosed -> LafziMadlulClosed` | correspondence is not closure |
| `LafziMadlul -> Wad'iMadlul` | wadʿī gate not crossed |
| `LafziMadlul -> Mutabaqah` | dalālah relation jump |
| `LafziMadlul -> Tadammun` | dalālah relation jump |
| `LafziMadlul -> Iltizam` | dalālah relation jump |
| `LafziMadlul -> Relation` | composition/relation jump |
| `LafziMadlul -> Composition` | composition jump |
| `LafziMadlul -> Ifadah` | proposition jump |
| `LafziMadlul -> Hukm` | judgment jump |
| `Ism -> ActualFa'il` | syntactic role jump |
| `Fiil -> ActualSubject` | syntactic role jump |
| `Harf -> ActualRelation` | relation realization jump |

---

## §17 Runtime staging opened by this law

This law opens a later implementation sequence only after DAL-A8 is ratified:

```text
LAFZI-B1  carriers + local residual vocabulary
LAFZI-B2  WordKindCandidateGate
LAFZI-B3  SourceIdentityGate
LAFZI-B4  FormStateGate
LAFZI-B5  InternalWordPathGate
LAFZI-B6  LafziResidualAudit
LAFZI-B7  LafziMadlulClosed -> Wad'iMadlulGate integration
```

Each later step must be separately staged in docs/14 before code ships.
LAFZI-B0 itself ships no runtime code.

---

## §18 Legacy VerbalMadlulCandidate reconciliation

Existing `VerbalMadlulCandidate` is an earlier PR-16 surface that starts from
`DalOnlyCandidate`. This law does not silently rewrite that historical
contract.

A later corrective or integration PR must explicitly decide whether the legacy
surface becomes:

```text
historical upstream carrier
compatibility alias
consumer of LafziMadlulClosed
```

Until that reconciliation PR exists, `LafziMadlulCandidateSet` and
`LafziMadlulClosed` remain the new post-`DalAloneClosed` path, and no downstream
legacy consumer may be reinterpreted by implication.

---

## §19 Golden law

```text
DalAloneClosed opens LafziMadlulGate.
LafziMadlulGate produces LafziMadlulCandidateSet, not automatic closure.
NoAutomaticOneToOneMapping.
LafziMadlulClosed requires independent lafzi gates.
LafziMadlulClosed opens Wad'iMadlulGate only; it does not cross it.
No approved lafzi output may hide residuals or jump to meaning, relation,
ifādah, hukm, tanzīl, or reality.
```
