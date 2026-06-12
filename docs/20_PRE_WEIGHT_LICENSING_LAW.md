# 20 — Pre-Weight Licensing Law

> **Status:** Constitutional law. Ratified in PR-9A; chain position
> ratified by Amendment-3
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). PR-9A is
> law only: no Arabic code, no carrier, no path gate, no μ
> operation, no `src/` change, no `tests/` change ships with this
> document. The pre-weight carriers land in PR-10, the path gate in
> PR-11, the chain operations in PR-12, and `weigh()` in PR-13, all
> bound by this document and by
> [`19_ARABIC_WEIGHT_BOUNDARY_LAW.md`](19_ARABIC_WEIGHT_BOUNDARY_LAW.md);
> no later PR may relax it.

This document closes, **before** any Arabic code exists, the
loophole [`docs/19`](19_ARABIC_WEIGHT_BOUNDARY_LAW.md) deliberately
left to this law:

```text
An Arabic weight module can accept any string — a raw word, a
surface, a syllable run, a bare root — and align it with a
pattern, as if the scale could reach into unlicensed text and
weigh it. The fit would look like harmless morphology and pass
a local test — while the input itself had never earned the
right to stand on the scale.
```

docs/19 fixed the **output** side of the Mīzān: wherever weighing
lands, it lands in PatternSpace and nowhere else. This law fixes
the **input** side: what may be weighed at all, and the licensing
chain that produces a weighable candidate.

The governing statement:

```text
لا شيء يدخل الميزان حتى يثبت كـ WeightReadinessCandidate.

Nothing enters the Mīzān until it stands as a
WeightReadinessCandidate.

No Mīzān input without Pre-Weight Licensing.
No weighing before WeightReadinessCandidate.
No extra/original split before PathGate.
No PathGate before WordCarrier.
No WordCarrier before WordBoundary.
No WordBoundary before SyllableSequence.
No SyllableSequence before licensed SyllableCandidate.
```

The licensing chain this law fixes:

```text
Syllable
  → SyllableSequence
  → WordBoundary
  → WordCarrier
  → PathGate
  → RootStem / non-root path
  → OriginalExtra
  → OperationTrace
  → WeightReadiness
```

---

## 1. The input boundary of the Mīzān

The Mīzān has exactly two constitutional boundaries, and each is
owned by exactly one law:

```text
docs/19:  Output boundary of weight.
          Weight lands only in PatternSpace.

docs/20:  Input boundary of weight.
          Nothing may be weighed before
          WeightReadinessCandidate.
```

PR-9 closed one question; PR-9A closes the other:

```text
PR-9  closed:  where does weight land?
               PatternSpace only.

PR-9A closes:  what may enter the weight?
               WeightReadinessCandidate only.
```

Until the chain below is implemented (PR-10 through PR-13), and
afterwards for every input that has not traversed it, the
following calls are refused, not computed:

```text
weigh(raw_word)    — refused.
weigh(surface)     — refused.
weigh(syllable)    — refused.
weigh(root)        — refused.

weigh(WeightReadinessCandidate)
                   — the only licensed form (PR-13).
```

In the sense of
[`09_ARABIC_APPLICATION_BOUNDARY.md`](09_ARABIC_APPLICATION_BOUNDARY.md),
this law extends the docs/19 declarations to the input side:

```text
Gates implemented            : none. PR-9A is law only. The path
                               gate opens in PR-11 and the chain
                               operations in PR-12, all behind
                               TransitionGates.

Transitions not shortcut     : Pronunciation → Syllable,
                               Syllable → Word,
                               HarakaMark → CaseFunction,
                               Unicode → ArabicLetter,
                               Grapheme → FunctionalLetter,
                               plus every docs/19 §1 row this law
                               inherits (the §12 table maps every
                               pre-weight leap onto these
                               registered rows).

Evidence sources consulted   : none. The pre-weight chain
                               consults no lexicon, no samāʿ
                               corpus, and no qiyās rule before
                               the PR-14 licensing boundary;
                               model confidence is never evidence
                               (docs/01).
```

## 2. The discriminating identities

In the same sense as docs/15 §2 and docs/19 §3, each station of
the pre-weight chain is what it is, and is not its neighbour up
the ladder:

```text
ḥarf       — an established letter identity. Not a code point,
             not a grapheme (docs/04: Unicode → ArabicLetter,
             Grapheme → FunctionalLetter).

ḥaraka     — an established vowel identity. Not a case function
             (docs/04: HarakaMark → CaseFunction), not a
             meaning.

unit       — a letter bound to its ḥaraka under a binding
             license. Not yet a syllable.

Syllable   — a licensed prosodic unit. Not a word, not a
             meaning (docs/04: Syllable → Word).

SyllableSequence
           — an ordered, licensed run of syllables. Not a
             bounded surface.

WordBoundary
           — a delimitation of the surface. Not a lexical
             identity.

WordCarrier
           — a form-level carrier of the bounded surface. Not a
             lexicon entry (docs/04: LexiconEntry → Candidate),
             not a meaning.

Path       — a candidate path emitted by the path gate. Not a
             verdict, not a meaning.

RootStem   — a derivational locus (docs/19: Root ≠ Reality).
             Not a reality, not a lexical meaning.

OriginalExtra
           — a structural split of original (aṣlī) and extra
             (zāʾid) letters. Not semantics.

OperationTrace
           — the preserved path of transformation. Not evidence
             of meaning.

WeightReadiness
           — a license to be weighed. Not a weight fit, not a
             certificate, not knowledge.
```

## 3. The stage license

Every stage transition in §§4–11 is licensed as a **branch of
origin**, never as a resemblance or a convenience. A stage license
has six elements:

```text
condition (sharṭ)        : what must already stand before the
                           stage may open.
cause (sabab)            : the licensed ground that makes the
                           stage's move follow.
no preventer (lā māniʿ)  : no named preventer stands; a
                           discovered preventer is a named,
                           visible residual — never silent.
jāmiʿ ʿilla              : the unifying ground that joins the
                           stage's input to its output — the
                           move travels on it, not on surface
                           resemblance.
effective attribute      : the attribute that actually carries
(waṣf muʾaththir)          the license — named, not assumed.
no defeating difference  : no effective difference (farq
                           muʾaththir) defeats the move.
```

These six names are uṣūlī terms used here as the **names of
structural license elements**, in the licensed-naming sense of
[`10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md`](10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md)
and docs/09: no fiqh content travels with them, and no samāʿ
corpus or qiyās rule is consulted before PR-14. Any stage whose
license would require samāʿ evidence leaves a `DEFERRED` residual
that closes only at the PR-14 boundary.

Every stage, in addition, preserves four invariants:

```text
preserved trace    : the stage records its move; an erased
                     underlying form is TRACE_MISSING.
visible residuals  : nothing pending is hidden; pass-with-
                     residual is closure with visible residuals,
                     never a new verdict kind.
bounded rank       : no stage promotes rank; promotion moves
                     only via the gate's bounded meet (docs/08).
named refusal      : every refusal returns a named FailureCode;
                     deferral and blockage are named verdicts
                     (DEFERRED / BLOCKED), never silent None.
```

This law adds **no new FailureCode members and no new
forbidden-line registry rows**: every stage refusal maps onto the
codes ratified in PR-1A and the rows bound in PR-5.

## 4. Stage 1 — the licensed syllable enters the sequence (μ_seq)

```text
No SyllableSequence before licensed SyllableCandidate.
```

The chain has no raw entry. A `SyllableCandidate` is licensed at
birth, below the sequence:

```text
The letter does not generate a syllable until it stands as a
letter. The ḥaraka does not operate until it stands as a
ḥaraka. Letter and ḥaraka do not become a unit until the
binding license stands. The unit does not enter the sequence
until the ordering license stands.
```

The origin is bound: the syllable stands only over the declared
text entry (`ArabicVocalizedText` — docs/15, docs/04 pre-text
table). `Pronunciation → Syllable` opens only as the
`SyllableStructureGate` bridge (PR-12), as the prosodic
structuring of the vocalized surface; the voice/audio pre-text
chain stays out of execution (Amendment-3, docs/14 §2).

```text
License : letter stands as letter; ḥaraka stands as ḥaraka;
          binding license joins them; ordering license admits
          units into the run.
Births  : SyllableSequenceCandidate, from licensed
          SyllableCandidates only.
Refuses : IDENTITY_BROKEN (letter or ḥaraka not established);
          UNLICENSED_OPENING (binding or ordering license
          missing); FORBIDDEN_STRAIGHT_LINE (raw text → syllable,
          pronunciation → syllable direct); TRACE_MISSING.
Never   : a word, a meaning, a case role.
```

## 5. Stage 2 — the sequence takes its boundaries (μ_boundary)

```text
No WordBoundary before SyllableSequence.
The sequence does not become a surface until its boundaries
stand.
```

```text
License : a licensed SyllableSequenceCandidate with declared
          domain and scope.
Births  : WordBoundaryCandidate — a delimitation, not an
          identity.
Refuses : BOUNDARY_MISSING; DOMAIN_MISSING; SCOPE_MISSING;
          GATE_REQUIRED (a surface assumed without the
          boundary stage).
Never   : a lexical identity, a meaning.
```

## 6. Stage 3 — the bounded surface takes a carrier (μ_word_carrier)

```text
No WordCarrier before WordBoundary.
```

`Syllable → Word` opens here **only** as a bridge to a form-level
carrier — never to a lexical identity. The `WordCarrierCandidate`
carries the bounded surface as a morphological word-form; it
consults no lexicon, and whatever part of word identity requires
samāʿ stays a `DEFERRED` residual until the PR-14 boundary.

```text
License : a WordBoundaryCandidate whose delimitation stands.
Births  : WordCarrierCandidate — a carrier, not a lexicon
          entry.
Refuses : BOUNDARY_MISSING; GATE_REQUIRED;
          FORBIDDEN_STRAIGHT_LINE (syllable → word direct,
          carrier → meaning).
Never   : a lexicon entry, a meaning, a hukm.
```

## 7. Stage 4 — the path gate precedes the root (μ_path_gate)

```text
No PathGate before WordCarrier.
No extra/original split before PathGate.
No weighing before the path stands.
```

The path gate is the constitutional fork of the chain. It emits
**candidate paths only**:

```text
Root (mushtaqq) / Jamid / Mabni / Operator / ProperName /
Borrowed / Residual
```

Each path sits behind a `TransitionGate` with named refusals. No
path is a verdict; no path is a meaning. A stronger competing
path is a named preventer (māniʿ), never a silent override — a
silent override is a `HIDDEN_RESIDUAL`. The path decides what the
Ω judgment (§11) can reach: functional paths head toward
`FunctionalClosure`, derivational paths may open the weight, and
unresolved paths stay `Residual`.

```text
License : a WordCarrierCandidate; the competing paths
          enumerated; the preventers named.
Births  : a PathCandidate (one of the family above).
Refuses : GATE_REQUIRED (a path assumed without the gate);
          HIDDEN_RESIDUAL (a silent override);
          BLOCKING_RESIDUAL_PRESENT.
Never   : a verdict, a meaning, a final lexicon.
```

## 8. Stage 5 — the root/stem and the non-root paths (μ_root_stem)

```text
The root is reached only through its path.
```

Root/stem extraction operates only on a Root-path candidate. The
`RootStemCandidate` is a derivational locus and nothing more:
never a reality, never a lexical meaning
(docs/04: `Root → LexicalMeaning`; docs/19: Root ≠ Reality). The
non-root paths (Jamid, Mabni, Operator, ProperName, Borrowed)
continue without extraction; functional paths continue toward
functional closure, not toward the scale.

```text
License : a PathCandidate from §7; extraction only on the
          Root path.
Births  : RootStemCandidate (Root path), or the non-root
          continuation of the carrier.
Refuses : GATE_REQUIRED (extraction without a path);
          FORBIDDEN_STRAIGHT_LINE (root → lexical meaning,
          root → reality).
Never   : a meaning, a referent, a truth claim.
```

## 9. Stage 6 — the original/extra split (μ_original_extra)

```text
No extra/original split before PathGate.
```

The split assigns each letter of the carried form its structural
standing — original (aṣlī) or extra (zāʾid) — as an
`OriginalExtraMap`. The split is structural, never semantic, and
it never erases the underlying form: the form before the split
stays readable through the trace.

```text
License : a §8 output whose path licenses a split.
Births  : OriginalExtraMap.
Refuses : TRACE_MISSING (the underlying form erased);
          IDENTITY_BROKEN (a letter's standing reassigned
          without license).
Never   : semantics from the split.
```

## 10. Stage 7 — the operation trace (μ_ops)

```text
Operations preserve the path of transformation.
```

Every transformation applied to the form on its way to the scale
is recorded, in order, as an `OperationTraceCandidate`. An
operation that cannot show its step is not an operation but an
erasure; an erased step is `TRACE_MISSING`.

```text
License : an OriginalExtraMap; each operation named and
          ordered.
Births  : OperationTraceCandidate.
Refuses : TRACE_MISSING (a step erased or unordered);
          IDENTITY_BROKEN (the form's identity lost across an
          operation).
Never   : an operation as evidence of meaning.
```

## 11. Stage 8 — weight readiness and the Ω judgment (μ_weight_readiness)

The chain's last stage assembles the **pre-weight surface**
(`PreWeightSurface`): the bounded carrier with its path, its
original/extra map, and its operation trace. Over that surface,
and only over it, the pre-weight licensing judgment Ω is
pronounced:

```text
Ω : PreWeightSurface → { FunctionalClosure
                       | WeightOpening
                       | Residual }

WeightAllowed ⇔ Ω = WeightOpening.
```

The three outcomes are exhaustive, and each is constitutional:

```text
FunctionalClosure — a licit completion without weighing. A
                    functional surface closes; it is never a
                    failure, and it is never weighed.

WeightOpening     — the only outcome that births a
                    WeightReadinessCandidate.

Residual          — a visible remainder: DEFERRED or BLOCKED,
                    named, never silently weighed, never
                    silently dropped.
```

`weigh()` (PR-13) consumes a `WeightReadinessCandidate` and
nothing else; its output side is owned entirely by docs/19 —
the fit lands in PatternSpace and means nothing.

```text
License : a completed PreWeightSurface — no stage skipped, no
          residual hidden.
Births  : WeightReadinessCandidate (Ω = WeightOpening only).
Refuses : BLOCKING_RESIDUAL_PRESENT; HIDDEN_RESIDUAL;
          RANK_PROMOTION_WITHOUT_GATE (readiness asserted
          above its rank).
Never   : a weight fit, a meaning, a certificate, knowledge.
```

## 12. The registered straight lines this law binds

Every leap the pre-weight chain could be tempted to take is
already a registered forbidden straight line
([`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md),
bound as data in PR-5):

```text
| Pre-weight leap                       | Registered line (docs/04)    |
| raw text → syllable (no letter or     | Unicode → ArabicLetter,      |
|   ḥaraka license)                     | Grapheme → FunctionalLetter  |
| pronunciation → syllable, unprosodied | Pronunciation → Syllable     |
| ḥaraka pressed into a case role       | HarakaMark → CaseFunction    |
| syllable → word without boundary and  | Syllable → Word              |
|   carrier                             |                              |
| carrier / surface → meaning           | WordForm → Meaning           |
| root/stem → lexical meaning / reality | Root → LexicalMeaning        |
| lexicon entry smuggled in as input    | LexiconEntry → Candidate     |
| readiness → certificate               | Candidate → Certificate      |
| readiness / fit → knowledge           | Tool/Number/LCNV → Knowledge |
```

This law adds **no new registry rows and no new FailureCode
members**. A pre-weight implementation that takes any of these
leaps directly is refused with the registered
`FORBIDDEN_STRAIGHT_LINE`; an implementation shipped out of chain
position is a `FORBIDDEN_LEAP`. Both verdicts exist since PR-1A.

## 13. Forbidden pre-weight forms

The following are constitutional refusals at the boundary level.
None of them may be added by any PR, including future PRs, without
an Amendment PR that opens them under a named gate.

```text
forbidden: weigh(raw_word), weigh(surface), weigh(syllable),
           weigh(root) — weighing any input that is not a
           WeightReadinessCandidate (binds PR-13).
forbidden: pre-weight carriers before PR-10; the path gate
           before PR-11; μ operations or Ω before PR-12;
           weigh() before PR-13.
forbidden: a meaning, agency, hukm, or reality field on any
           pre-weight carrier (binds PR-10, with docs/19).
forbidden: skipping, merging, or re-ordering a stage of
           §§4–11; synthesising a missing stage output —
           missing means refuse.
forbidden: a path emitted as a verdict, or a competing path
           silently overridden — the preventer must be named.
forbidden: weighing a FunctionalClosure or a Residual surface;
           any fourth Ω outcome.
forbidden: lexicons, root tables, pattern tables, or any
           samāʿ/qiyās material before the PR-14 license.
forbidden: pre-weight code inside the adapter or audit layers,
           or any kernel, gate, or schema change made for the
           pre-weight branch.
forbidden: new FailureCode members, new forbidden-line
           registry rows, new runtime dependencies.
```

## 14. Purity and totality

The future μ operations and the Ω judgment are bound by the same
discipline as `Γ` and the construction surface (docs/11 §7,
docs/17 §5, docs/19 §7):

```text
purity:        μ operations and Ω are pure functions — no I/O,
               no ledger writes, no time reads, no network.
totality:      every stage either licenses or refuses with a
               named FailureCode; deferral and blockage are
               named verdicts. No bare exception for an
               expected verdict; no silent None.
no synthesis:  no stage fabricates a missing carrier, boundary,
               center, license, or trace. Missing means refuse.
no promotion:  no stage promotes rank; promotion moves only via
               the gate's bounded meet (docs/08).
```

## 15. Anti-collapse rules

```text
no-raw-entry:     nothing enters the chain except over the
                  declared text entry (docs/15).
no-skip:          no stage is skipped, merged, or re-ordered.
no-case-role:     the ḥaraka never operates as a case function
                  inside this chain.
no-word-leap:     syllables never become a word without
                  boundary and carrier.
no-lexicon:       no stage consults a lexicon before the PR-14
                  license.
no-meaning:       no stage emits meaning; the chain ends at
                  readiness, and weight ends in PatternSpace
                  (docs/19).
gate-owned:       every stage transition is gate-owned; paths
                  come only from the path gate.
preventer-named:  a stronger competing path or a discovered
                  māniʿ is named, never silent.
closure-licit:    FunctionalClosure is a licit completion, not
                  a failure — and never weighed.
residual-visible: a Residual surface stays visible — DEFERRED
                  or BLOCKED, never silently weighed.
readiness-only:   weigh() consumes only a
                  WeightReadinessCandidate.
law-first:        no pre-weight code before this law.
named-refusal:    every refusal returns a named FailureCode.
```

## 16. Reserved names

`SyllableCandidate`, `SyllableSequenceCandidate`,
`WordBoundaryCandidate`, `WordCarrierCandidate`, the
`PathCandidate` family, `RootStemCandidate`, `OriginalExtraMap`,
`OperationTraceCandidate`, `WeightReadinessCandidate`, and
`PreWeightSurface` are reserved names under the reserved-name rule
in `CLAUDE.md`. They land in PR-10 **only**, as frozen carriers
that depict structure. `μ_path_gate` lands in PR-11 **only**.
`μ_seq`, `μ_boundary`, `μ_word_carrier`, `μ_root_stem`,
`μ_original_extra`, `μ_ops`, `μ_weight_readiness`, and the Ω
judgment land in PR-12 **only**. `weigh()` and
`WeightFitCandidate` stay PR-13 names under docs/19 §9. Binding
any of these names to a free container, or shipping any of them
before its chain position, is a `FORBIDDEN_LEAP` regardless of CI
status.

## 17. Short constitutional summary

```text
الحرف لا يولد مقطعًا حتى يثبت كحرف.
والحركة لا تعمل حتى تثبت كحركة.
والحرف والحركة لا يصيران وحدة حتى تثبت رخصة الربط.
والوحدة لا تدخل السلسلة حتى تثبت رخصة الترتيب.
والسلسلة لا تصير سطحًا حتى تثبت حدودها.
والسطح لا يدخل الوزن حتى تثبت بوابة المسار.
والوزن لا يعطي مدلولًا، بل صورة في PatternSpace فقط.
```

In English:

```text
The letter does not generate a syllable until it stands as a
letter.
The ḥaraka does not operate until it stands as a ḥaraka.
Letter and ḥaraka do not become a unit until the binding
license stands.
The unit does not enter the sequence until the ordering
license stands.
The sequence does not become a surface until its boundaries
stand.
The surface does not enter the weight until the path gate
stands.
And the weight yields no signified — only an image in
PatternSpace.
```

---

## Cross-references

- The output boundary this law pairs with (weight lands only in
  PatternSpace):
  [`19_ARABIC_WEIGHT_BOUNDARY_LAW.md`](19_ARABIC_WEIGHT_BOUNDARY_LAW.md).
- The door both weight laws answer to:
  [`09_ARABIC_APPLICATION_BOUNDARY.md`](09_ARABIC_APPLICATION_BOUNDARY.md).
- The registered straight-line surface every §12 row maps onto:
  [`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md)
  and the PR-5 registry in
  [`src/taaqqul_slot_geometry/core/forbidden_lines.py`](../src/taaqqul_slot_geometry/core/forbidden_lines.py).
- The terminology discipline licensing the §3 uṣūlī names:
  [`10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md`](10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md).
- The declared text entry the chain stands over:
  [`15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md`](15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md).
- The entity-level licensing discipline this chain mirrors:
  [`16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md`](16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md).
- The only rank authority, which no stage bypasses:
  [`08_TRANSITION_GATE.md`](08_TRANSITION_GATE.md).
- The carrier discipline that binds the PR-10 surface:
  [`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md).
- The generation law binding any future SlotGraph that carries
  pre-weight content:
  [`17_SLOTGRAPH_GENERATION_LAW.md`](17_SLOTGRAPH_GENERATION_LAW.md).
- The black-box boundary (model confidence is never evidence):
  [`01_BLACK_BOX_BOUNDARY.md`](01_BLACK_BOX_BOUNDARY.md).
- The chain position of this document and of the code it licenses:
  [`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) — PR-9A,
  PR-10 through PR-14, and the §2 Amendment-3 record.

---

## PR-10 through PR-14 binding

PR-9A writes no code. This document binds what the later
weight-branch PRs must do, jointly with docs/19:

```text
1. PR-10 ships the pre-weight carriers named in §16 beside the
   docs/19 carriers — frozen, with no operation, no fit
   computation, and no meaning field — and adds the docs/19 and
   docs/20 presence guards beside its constitutional tests, in
   the shape of the existing docs-presence guards.
2. PR-11 opens the §7 path gate only — candidate paths behind a
   TransitionGate, named refusals, no final lexicon, no
   extraction, no split, no weighing.
3. PR-12 opens the §§4–11 chain operations — μ_seq through
   μ_weight_readiness and the Ω judgment — pure, gated, total;
   Pronunciation → Syllable and Syllable → Word open here as
   licensed bridges, never as shortcuts; samāʿ-grounded
   preventers stay DEFERRED residuals until PR-14.
4. PR-13 ships weigh(WeightReadinessCandidate, ...) →
   WeightFitCandidate or a named Refusal — and may accept no
   other input, under the docs/19 output boundary.
5. PR-14 places the lexical / samāʿ / qiyās licenses before any
   semantics; the DEFERRED residuals left by PR-11 and PR-12
   close there.
```

A weight-branch PR that does not honor this law is a
`FORBIDDEN_LEAP` regardless of CI status.
