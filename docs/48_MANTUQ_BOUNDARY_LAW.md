# 48 — Manṭūq Boundary Law

> **Status:** Constitutional law. Ratified by PV-A1 (law only — no
> code). Binds every later PR that constructs, processes, or consumes
> a `MantuqClosureCandidate` — most directly PV-A2 (ManṭūqClosure
> code). It is load-bearing.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change. Any attempt to import a
> `MantuqClosureCandidate`, a `MantuqVerdict`, a `MantuqState`, or a
> `prove_mantuq_closure()` symbol before PV-A2 (the code PR) is
> merged is a `FORBIDDEN_LEAP` regardless of CI status.

## §1 Governing principle (ما يحفظ — what it preserves)

```text
No MantuqClosureCandidate without a PROVEN IfadahVerdict.
No MantuqClosureCandidate without a preserved speech-origin boundary.
No exit from the speech boundary without a gate.
No MafhumCandidate without a closed MantuqClosureCandidate.
No hukm from Mafhum before its own proof.
No MantuqClosureCandidate that produces a mafhum, a majaz, a haqiqah
   claim, a naql claim, a GPT proposition, or any horizontal branch
   output.
No MantuqClosureCandidate is a certificate; it remains a candidate
   forever.
```

`MantuqClosureCandidate` proves that a closed `IfadahCandidate` has a
**preserved spoken/textual origin** — the explicit indication that
stands before any implied meaning (mafhum), any figurative transfer
(majaz), or any terminological transfer (naql). It does not determine
mafhum, majaz, or reality.

The constitutional position preserved by this law:

```text
لا مفهوم بلا منطوق محفوظ.
ولا فرع بلا أصل.
ولا خروج عن حد النطق بلا بوابة.
ولا حكم من مفهوم قبل حفظ الأصل.
```

Translation:

```text
No mafhum without a preserved mantuq.
No branch without an origin.
No exit from the speech boundary without a gate.
No hukm from mafhum before preserving the origin.
```

## §2 Constitutional middle terms

The middle terms that connect Manṭūq to its predecessors and
successors:

```text
IfadahCandidate        (what speech-level closure the vertical path
                        produced — PR-20; the input to Manṭūq)
TanzilCandidate        (how the vertical path presents the chain —
                        PR-22; the presentation envelope that Manṭūq
                        inherits via AuditedTanzilBridge)
MantuqClosureCandidate (what this law defines: the preserved explicit
                        indication; the origin that Mafhūm may branch
                        from — PV-A2)
MafhumCandidate        (what this law forbids until ManṭūqClosure is
                        complete — PV-A4; never before PV-A2)
```

## §3 What this law opens

```text
PV-A2 — ManṭūqClosure (code).
        Carriers: MantuqClosureCandidate, MantuqVerdict, MantuqState,
                  MANTUQ_RANK_CEILING, prove_mantuq_closure().
        Nothing else.
```

PV-A2 is the **only** PR licensed by docs/48. It produces a
candidate carrier, never a mafhum and never a meaning.

## §4 What this law forbids

```text
No MafhumCandidate.
No MafhumVerdict.
No MafhumState.
No MajazVerdict / MajazLicense.
No ManqulVerdict / ManqulLicense.
No HaqiqahAttempt.
No ReferenceExpansion.
No GPTProposer.
No GovernmentServiceEngine.
No ArabicConditionsDAG.
No horizontal branch output of any kind.
```

None of the above may exist in any module before PV-A2 completes its
code and PV-A3 (Mafhūm Boundary Law) is ratified.

## §5 Rank and residual discipline

```text
MANTUQ_RANK_CEILING ≤ TANZIL_RANK_CEILING
```

ManṭūqClosure may not promote rank above the vertical path ceiling.
The rank at which ManṭūqClosure operates is bounded by the meet of
the IfadahCandidate rank and the existing vertical ceiling:

```text
rank(MantuqClosureCandidate) ≤ meet(rank(IfadahCandidate), TANZIL_RANK_CEILING)
```

### Residual policy

ManṭūqClosure declares the following residual:

```text
MAFHUM_NOT_YET_OPENED — this residual records that Mafhūm has not
   been derived and is constitutionally deferred until PV-A3/PV-A4.
```

This residual must be visible in the trace. It may not be hidden.

## §6 Trace discipline

ManṭūqClosure must produce a trace entry that records:

```text
- input: IfadahVerdict (PROVEN)
- operation: prove_mantuq_closure
- output: MantuqVerdict (PROVEN | REFUSED)
- residuals: [MAFHUM_NOT_YET_OPENED]
- rank: ≤ MANTUQ_RANK_CEILING
- failure_code: named FailureCode if REFUSED
```

The trace must be continuous with the vertical path trace. No gap
between the last vertical-path trace entry and the ManṭūqClosure
entry.

## §7 Boundary integrity

ManṭūqClosure operates **after** the vertical path is complete. It
does not modify, replace, or bypass any vertical-path layer:

```text
MufradDalalahClosure → RelationClosure → IfadahCandidate →
HukmCandidate → ManatCandidate → TanzilCandidate →
AuditedTanzilBridge
```

ManṭūqClosure receives `IfadahCandidate` as its input (the
speech-level closure) and produces `MantuqClosureCandidate` as proof
that the explicit spoken/textual origin has been preserved. It is the
first horizontal extension of the vertical path.

## §8 Relationship to Mafhūm

Mafhūm (implied meaning) is constitutionally dependent on Manṭūq:

```text
Manṭūq is the root.
Mafhūm is the branch.
No branch without preserving the root.
No implied meaning without preserving the explicit.
```

The specific types of Mafhūm that depend on ManṭūqClosure:

```text
Mafhūm al-Muwāfaqah (a fortiori implication — stronger or equal)
Mafhūm al-Mukhālafah (contrary implication — opposite case)
```

Neither may be opened before ManṭūqClosure proves the explicit
origin is preserved. This ordering is constitutional, not stylistic.

## §9 Governing sentences

```text
المنطوق هو الأصل المحفوظ.
والمفهوم فرع لا يصح بلا أصله.
والخروج عن حد النطق يحتاج بوابة.
والحكم من مفهوم لا يسبق حفظ المنطوق.

Manṭūq is the preserved origin.
Mafhūm is a branch that is invalid without its origin.
Exit from the speech boundary requires a gate.
Hukm from mafhūm does not precede preserving the manṭūq.
```

## §10 Reviewer law

```text
PV-A1 is law-only.
It opens only PV-A2 (ManṭūqClosure code).
It does not create ManṭūqClosure runtime.
No Mafhūm PR may start before ManṭūqClosure is complete.
No Majāz PR may start before Mafhūm Boundary Law is ratified.
No horizontal branch may open concurrently (WIP rule from docs/47 §5).
```

## §10.1 Lexical-origin continuity (PV-A1.1 clarification)

> **Status:** Law-only corrective. Ratified by PV-A1.1. Clarifies
> that ManṭūqClosure consumes existing MufradDalālahClosure through
> IfadahVerdict, not a new LexicalMeaningClosure layer. No new
> carrier, no new enum, no new layer.

### Governing principle

```text
لا منطوق بلا دلالة مفردة مغلقة.
ولا دلالة مفردة باسم جديد إذا كان أصلها محفوظًا.
ولا طبقة جديدة حيث يكفي trace إلى طبقة قائمة.

No mantuq without a closed mufrad dalalah.
No mufrad dalalah under a new name when its origin is already preserved.
No new layer where a trace to an existing layer suffices.
```

### Rules

```text
1. ManṭūqClosure does not create lexical meaning.
2. ManṭūqClosure does not create a new LexicalMeaningClosure carrier.
3. ManṭūqClosure consumes IfadahVerdict PROVEN.
4. The IfadahVerdict must trace back through:
   RelationClosureVerdict → MufradDalālahClosureVerdict.
5. If ManṭūqClosure accepts any lexical unit not covered by the
   Ifadah upstream chain, that unit must have a PROVEN
   MufradDalālahClosureVerdict or a justified residual.
6. If any required lexical unit lacks PROVEN MufradDalālahClosure,
   PV-A2 must refuse with MUFRAD_DALALAH_NOT_CLOSED or record
   a trace_ref containing "mufrad_dalalah_not_closed".
```

### Constitutional chain guarantee

The upstream chain that ManṭūqClosure inherits through IfadahVerdict:

```text
DalOnlyCandidate
→ VerbalMadlulCandidate
→ DalalahCandidates (Mutābaqah / Taḍammun / Iltizām)
→ MufradDalālahClosure
→ RelationClosure
→ IfadahCandidate
→ ManṭūqClosure (this law)
```

This chain proves that ManṭūqClosure always has a closed mufrad
dalālah upstream. No separate LexicalMeaningClosure layer is needed.

### Forbidden names

```text
No LexicalMeaningClosure.
No LexicalMeaningClosureCandidate.
No LexicalMeaning.
No FinalLexicalMeaning.
No MeaningClosure (ambiguous — "meaning" is loaded in this repository).
```

These names are forbidden because they either duplicate
MufradDalālahClosure or imply a final meaning before maqam,
which is constitutionally invalid.

### Reviewer law for §10.1

```text
PV-A1.1 is law-only corrective.
It does not open a new layer.
It does not implement ManṭūqClosure.
It clarifies that PV-A2 consumes MufradDalālahClosure through
  the existing IfadahVerdict chain, not a new carrier.
No PV-A2 code change is required if it already consumes
  IfadahVerdict PROVEN (which traces through MufradDalālahClosure).
```
