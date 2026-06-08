# 15 — Textual Communication Entry Law

> **Status:** Constitutional law. Ratified in PR-1C. Every later PR
> that constructs, validates, or consumes a textual entry is bound by
> this document; no later PR may relax it.

This document closes a loophole that the
[Mathematical Slot Geometry Laws](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md)
§13 (the Declared Entry Boundary Law) names but does not fully
operationalise:

```text
A vocalised, well-formed text can look like a beginning,
and be silently treated as an origin, a sound, or a meaning.
```

That collapse is the textual mirror of agent hallucination: a string
arrives at the engine and is granted ontological status it does not
have. The repository refuses that move. The well-formed vocalised
text is a **communicative representational entry point**, not an
origin, not a sound, and not a meaning.

The governing statement is:

```text
النص المشكول المنضبط يدخل النظام لا بوصفه صوتًا،
ولا أصلًا وجوديًا أول،
ولا معنى،
بل بوصفه تمثيلًا تواصليًا لما قبله،
ونقطة تشغيل مرخصة بمعلوم سابق أدنى،
تفتح SlotGraph للأصول والفروع،
ولا تنتج معنى أو حكمًا إلا بسلسلة لاحقة مرخصة.
```

In English:

```text
A well-formed vocalised text enters the engine
not as sound,
not as ontological origin,
not as meaning,
but as a communicative representation of what precedes it,
a licensed operational entry point licensed by a lower prior known,
opening a SlotGraph over origins and branches,
producing no meaning or verdict except through a later licensed chain.
```

---

## 1. Why a textual entry must not be promoted at the door

A piece of code that does the following is **not** a constitutional
entry:

```text
receive text  →  treat it as letter identities
receive text  →  treat it as phonemes
receive text  →  treat it as meaning
receive text  →  treat it as a judgment
```

Even when the text is fully vocalised and orthographically clean, no
local property of the string licenses any of these moves. Each move
requires a downstream licensed transition that this PR does not yet
implement.

The repository rule:

```text
TextEntry is a TextTraceCandidate,
not a Letter, not a Sound, not a Meaning, not a Judgment.
```

## 2. The discriminating chain

The Textual Communication Entry Law fixes the following identities as
constitutional refusals. They are not stylistic preferences; each
non-identity must be enforceable by a named refusal in `Γ` or by a
named forbidden transition in the registry that lands in PR-5.

```text
TextEntry           ≠ OntologicalOrigin.
TextEntry           ≠ Sound.
Unicode             ≠ ArabicLetter.
BinaryText          ≠ Unicode.
VocalizedText       ≠ ValidAnalysis.
TextTraceCandidate  ≠ Meaning.
```

Each line above is a *named refusal*: when an implementation observes
the left-hand side and is asked to deliver the right-hand side, it
must refuse with a named `FailureCode` rather than coerce the value.

Mapping to existing carriers (`docs/02..11`):

```text
TextEntry ≠ OntologicalOrigin
    Refusal carrier (PR-2+): FORBIDDEN_STRAIGHT_LINE.
    Registry row (PR-5):     TextEntry → OntologicalOrigin.

TextEntry ≠ Sound
    Refusal carrier:         FORBIDDEN_STRAIGHT_LINE.
    Registry row:             TextEntry → Sound.

Unicode ≠ ArabicLetter
    Already declared in:     docs/04 + docs/11 §13.3.
    Refusal carrier:         FORBIDDEN_STRAIGHT_LINE.

BinaryText ≠ Unicode
    Already declared in:     docs/04 + docs/11 §13.3.
    Refusal carrier:         FORBIDDEN_STRAIGHT_LINE.

VocalizedText ≠ ValidAnalysis
    Already declared in:     docs/04 + docs/11 §13.3.
    Refusal carrier:         FORBIDDEN_STRAIGHT_LINE.

TextTraceCandidate ≠ Meaning
    New row, added by this PR.
    Refusal carrier:         FORBIDDEN_STRAIGHT_LINE.
    Registry row (PR-5):     TextEntry → Meaning.
```

PR-1C only **names** these failures. The typed registry that binds
them as data lands in PR-5 (see `docs/04_FORBIDDEN_STRAIGHT_LINES.md`).

## 3. The new forbidden straight line added by this PR

The single new entry that this law contributes to the forbidden
straight-line surface, to be merged into the registry in PR-5:

```text
| Forbidden transition  | Why                                       | Required bridge                 |
| TextEntry → Meaning   | A textual entry is a representational     | Full pre-text + signification   |
|                       | candidate; meaning requires the full       | chain (TextEntryValidation →    |
|                       | downstream licensed chain.                 | Lexical → Morphological →       |
|                       |                                            | Syntactic → Semantic → Gate).    |
```

No other registry rows are introduced here.

## 4. Prior trace is preserved, not executed

The pre-text chain — voice, audio bytes, raw byte text, Unicode
encoding, code points, graphemes — is acknowledged as **prior trace**.
It is never silently collapsed into the textual entry, and it is
never erased.

```text
ما قبل النص محفوظ كأثر سابق،
لكنه لا يُنفّذ تفصيليًا إلا إذا فُتح له مسار لاحق.
```

Equivalently:

```text
Pre-text layers are preserved as prior trace
and are out of current execution until a future PR
explicitly opens a bridge gate for them.
```

This restates `docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md` §13.4
in the entry-side direction. It does not introduce ASR, audio
decoders, encoding pipelines, normalisation, or phoneme extractors.

## 5. Boundary obligations on every textual entry

When PR-2 lands `SlotGraph`, every textual entry must arrive with the
boundary already declared. Until PR-2 ships, this document **names**
the boundary; it does not yet implement it.

A textual entry's `entry_boundary` must declare:

```text
entry_boundary:
  declared_entry_kind: ARABIC_VOCALIZED_TEXT
  representation_status: REPRESENTATIONAL_OF_PRIOR
  ontological_status:    NOT_AN_ORIGIN
  sound_status:          NOT_A_SOUND
  meaning_status:        NOT_A_MEANING
  prior_trace_status:    OUT_OF_CURRENT_EXECUTION
  produces_only:         TEXT_TRACE_CANDIDATE
```

A `SlotGraph` whose textual entry omits any of these fields is to be
refused at construction time. The matching refusal carriers already
exist (`docs/11` §13.2, `core/failure_taxonomy.py`):

```text
DOMAIN_MISSING, SCOPE_MISSING, BOUNDARY_MISSING, TRACE_MISSING,
UNLICENSED_OPENING, FORBIDDEN_STRAIGHT_LINE.
```

## 6. What this PR does **not** introduce

PR-1C ratifies the Textual Communication Entry Law as constitutional
text only. It does **not** introduce:

```text
ASR
audio decoders
binary-text decoders
Unicode normalisation
phoneme extractors
encoding pipelines
lexicons
Arabic linguistic code
SlotGraph construction code
gamma() or any closure behavior
```

The matching pre-text refusals are already enumerated in
`docs/04_FORBIDDEN_STRAIGHT_LINES.md` under *Pre-text declared-entry
transitions*. This PR adds the single new row `TextEntry → Meaning`
to the surface those refusals govern.

## 7. Short constitutional summary

```text
النص ليس الصوت.
النص ليس الأصل.
النص ليس المعنى.
النص نقطة دخول تواصلية تمثيلية،
تفتح خانات، ولا تُغلق حكمًا.
```

In English:

```text
Text is not sound.
Text is not origin.
Text is not meaning.
Text is a communicative representational entry point
that opens slots and never closes a judgment.
```

---

## Cross-references

- The mathematical statement and the Declared Entry Boundary Law:
  [`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md) §13.
- The pre-text forbidden transitions table:
  [`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md) §
  *Pre-text declared-entry transitions*.
- The Arabic application boundary:
  [`09_ARABIC_APPLICATION_BOUNDARY.md`](09_ARABIC_APPLICATION_BOUNDARY.md).
- The technical terminology non-confusion law:
  [`10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md`](10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md).
- The identity-to-truth licensing chain that consumes this entry:
  [`16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md`](16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md).
- The `SlotGraph` generation law that constrains what a textual entry
  may produce:
  [`17_SLOTGRAPH_GENERATION_LAW.md`](17_SLOTGRAPH_GENERATION_LAW.md).
- The PR-chain position of this document:
  [`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) — PR-1C.
