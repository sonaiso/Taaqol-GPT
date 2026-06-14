# 42 — SpeechForce / FormalStyle Bridge Law

> **Status:** Constitutional law. Ratified by PR-D6 (law only — no
> code). Binds every later PR that constructs, processes, or consumes
> a `SpeechForceKind` or an `IfādahCandidate` — most directly PR-20
> (IfādahCandidate code), and transitively PR-D7/PR-21 (Hukm),
> PR-D8/PR-21M (Manāṭ), PR-D9/PR-22 (Tanzīl), PR-22-AUDIT, and
> PR-D10 (Vertical Path Closure). It is load-bearing.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change. Any attempt to import a
> `SpeechForceKind`, a `SpeechForceVerdict`, a
> `prove_formal_style_speech_force_compatibility()` symbol, or any
> "bridge" carrier before PR-20 (the code PR) is merged is a
> `FORBIDDEN_LEAP` regardless of CI status.
>
> This law presupposes docs/41 (PR-D5) as ratified by PR-D5.1 and
> PR-D5.2 (identifier-surface finalization). It does not redefine
> docs/41; it states the bridge that docs/41 §2 declares as its
> "necessary companion" and that docs/41 §6 defers to under the
> `FORMAL_STYLE_CONFLICT` refusal label.

## §1 Governing principle (ما يحفظ — what it preserves)

```text
FormalStyleVerdict ≠ SpeechForceKind.
SpeechForceKind   ≠ IfādahCandidate.
FormalStyleVerdict ≠ IfādahCandidate.
Ifādah            ≠ Hukm.

FormalStyleVerdict is form-only readiness, proven by docs/35 / PR-F8.
SpeechForceKind   is a maqām-licensed communicative-force readiness
                  label, supplied by the caller of
                  prove_ifadah_candidate() and validated, never
                  derived, by the bridge.
IfādahCandidate   is the speech-level closure carrier produced only
                  by PR-20 from three PROVEN input verdicts plus a
                  licensed SpeechForceKind plus a single shared
                  maqām verdict (docs/41 §1, §8).
```

`FormalStyleVerdict` (carrying `FormalStyleCandidate`, ratified by
docs/35 / PR-F8) proves *formal* readiness for a khabar-shaped or
inshāʾ-shaped surface. `SpeechForceKind` is a *maqām-licensed*
communicative-force readiness label. Neither implies the other; the
bridge in §6 below states the only licit pairings.

The constitutional middle terms preserved by this law:

```text
FormalStyleVerdict          (docs/35 / PR-F8 — form-only readiness;
                             carries FormalStyleCandidate)
SpeechForceKind             (this law / PR-20 — KHABAR | INSHA,
                             minimal set; never derived from form
                             or maqām alone)
MaqamContextBoundaryVerdict (docs/37 / PR-D1.2 — boundary verdict,
                             not a force)
RelationClosureVerdict      (docs/40 / PR-D4 — relational substrate;
                             docs/40 §9 forbids it from exporting
                             formal_style or speech_force)
```

None of the four can substitute for any other. The bridge is the
layer at which a `FormalStyleVerdict` and a `SpeechForceKind` are
checked for *compatibility* under a shared
`MaqamContextBoundaryVerdict`, before either may be presented to
`prove_ifadah_candidate()`.

## §2 What this law opens

```text
PR-20 — IfādahCandidate (code).
        Carrier surface as declared by docs/41 §2:
        IfādahCandidate, IfadahVerdict, IfadahState,
        SpeechForceKind (minimal: KHABAR, INSHA),
        IFADAH_RANK_CEILING, prove_ifadah_candidate().
        Nothing else.
```

PR-20 is the **only** PR licensed by docs/42. It is co-licensed by
docs/41 (PR-D5); neither law alone licenses PR-20. PR-20 may not
merge until **both** docs/41 and docs/42 are ratified.

This law does not expand the PR-20 carrier surface declared by
docs/41 §2. It does not add a new carrier, a new enum, or a new
operation symbol. The enum surface in PR-20 must continue to use
ASCII transliterations without diacritics (`KHABAR`, `INSHA`).

## §3 What this law forbids

```text
No derivation of SpeechForceKind from RelationClosureVerdict alone.
No derivation of SpeechForceKind from FormalStyleVerdict alone.
No derivation of SpeechForceKind from MaqamContextBoundaryVerdict
   alone.
No derivation of SpeechForceKind from any pairwise combination of
   the above without the third also being PROVEN under the same
   maqām verdict.
No treating FormalStyleVerdict as Ifādah.
No treating SpeechForceKind as Ifādah.
No treating Ifādah as Hukm. (The forbidding law remains docs/41 §3
   and the future docs/43; this is restated here because the
   bridge is the layer at which the reader is most tempted to
   leap.)
No SpeechForceKind enum member in PR-20 outside the minimal set
   {KHABAR, INSHA}. The members AMR, NAHY, ISTIFHAM, NIDA, DUA,
   TAMANNI, TARAJJI, TAHDID, TAAJJUB, QASAM remain explanatory
   residuals only (docs/41 §10; this law §9).
No introduction of `formal_style` (or `speech_force`) as a
   *derived* attribute of any pre-Ifādah carrier — including
   RelationClosureCandidate, MufradDalalahClosureCandidate, and
   FormalStyleCandidate. `FormalStyleVerdict` and `SpeechForceKind`
   must be passed as independent, structurally separate arguments
   to `prove_ifadah_candidate()`.
No implementation of the bridge in PR-20 as a *silent* dispatch
   table. The compatibility rule of §6 must be explicit in PR-20
   code (named branches, named refusals) and visible in the trace.
No silent fallback for FORMAL_STYLE_CONFLICT (see §7).
No "auto-promotion" from a deferred SpeechForceKind residual
   (AMR / NAHY / ISTIFHAM / etc.) into the enum surface inside
   PR-20.
No re-export, alias, or string representation that drops the
   "Candidate" suffix from any Ifādah-layer carrier.
```

PR-20 ships none of these. Any future PR that ships any one of them
must declare its own origin law and its own chain position.

## §4 Domain (المجال — where this law applies)

```text
Bridge layer between FormalStyleVerdict (docs/35 / PR-F8) and the
SpeechForce input slot of prove_ifadah_candidate() (docs/41 / PR-20),
checked under a single shared MaqamContextBoundaryVerdict
(docs/37 / PR-D1.2). It binds:

  * PR-20 (IfādahCandidate code) — must implement §6 explicitly
    and must observe §7 for FORMAL_STYLE_CONFLICT.
  * PR-D7 / PR-21 (Hukm) — may consume an IfādahCandidate that
    has passed this bridge, but may never recompute or re-bridge
    it.
  * PR-22-AUDIT — AnswerAudit may surface an IfādahCandidate as a
    candidate; the bridge result is internal to the candidate and
    is never re-exported as a standalone "force" object.

It does not bind:
  * Core kernel (core/) — SpeechForce is not a SlotGraph property.
  * Adapter layer (audit/) — adapters never derive or assert
    SpeechForce.
  * Weight branch (docs/19, docs/20, docs/22–docs/25) — weight
    layers never produce a SpeechForce.
  * Any horizontal branch (majāz, mantūq, mafhūm, naql,
    GPT-proposer, reference expansion, conditions DAG) — these
    are forbidden before docs/46 (PR-D10) closes the vertical
    path.
```

## §5 Evidence (الدليل — what justifies this bridge)

1. **docs/35 / PR-F8** (Formal Style Candidate Law): `FormalStyleCandidate`
   is *form-only* readiness. The §4 family list (DECLARATIVE_STYLE_FORM,
   COMMAND_STYLE_FORM, …) is a structural classification only and
   carries the explicit non-equivalences `KHABAR_STYLE_FORM ≠
   truth / assertion / proposition` and `INSHA_STYLE_FORM ≠
   speaker intent`. Form alone never determines communicative force.
2. **docs/37 / PR-D1.2** (Maqām/Context Boundary Readiness Law):
   `MaqamContextBoundaryVerdict` is a *boundary* verdict that
   licenses readiness inside a discourse domain. It is not a force,
   and it does not by itself license any `SpeechForceKind`.
3. **docs/40 / PR-D4** (Relation Closure Law) §9: `RelationClosure`
   explicitly forbids exporting `IfadahCandidate`,
   `FormalStyleVerdict`-equivalents, or any speech-force-shaped
   surface. The relational substrate is necessary but not
   sufficient.
4. **docs/41 / PR-D5** (Ifādah Boundary Law) §2 declares this
   document as its necessary companion. §5.3 establishes that
   "formal readiness alone never determines speech force inside a
   maqām. The bridge is constitutive, not derivative." §6 names
   `FORMAL_STYLE_CONFLICT` and explicitly defers its semantics
   ("incompatible under the bridge law (see docs/42, PR-D6)") to
   this document.
5. **docs/04 / docs/05** (Forbidden Straight-Line Registry):
   the lines `Form → Force`, `Force → Proposition`, `Form →
   Meaning`, and `Context → Force` are constitutionally forbidden
   straight lines. The bridge in §6 is precisely what prevents
   them from being collapsed.

## §6 Compatibility rule (the bridge content)

Inside a single PROVEN `MaqamContextBoundaryVerdict`, the only
licit pairings of a PROVEN `FormalStyleVerdict` (carrying a
`FormalStyleCandidate` from the docs/35 §4 family) with a
`SpeechForceKind` member are:

```text
FormalStyleCandidate of DECLARATIVE_STYLE_FORM
    + maqām support
    + SpeechForceKind = KHABAR
        => COMPATIBLE

FormalStyleCandidate whose family is one of
    { COMMAND_STYLE_FORM, PROHIBITION_STYLE_FORM,
      INTERROGATIVE_STYLE_FORM, VOCATIVE_STYLE_FORM,
      WISH_STYLE_FORM, HOPE_STYLE_FORM, OATH_STYLE_FORM,
      CONDITION_STYLE_FORM, EXCLAMATION_STYLE_FORM }
    + maqām support
    + SpeechForceKind = INSHA
        => COMPATIBLE
```

Any other pair — e.g. a declarative-shape form claimed as `INSHA`,
or an inshāʾ-shape family claimed as `KHABAR`, or any pair under a
divergent maqām verdict — is `FORMAL_STYLE_CONFLICT` (see §7).

The rule is stated as **compatibility**, not **derivation**.
`SpeechForceKind` is *supplied* by the caller of
`prove_ifadah_candidate()`. The bridge only validates the pairing
against the form family and the shared maqām verdict.

Neither side is sufficient alone:

- **Form alone** never licenses `SpeechForceKind` — that would be
  the forbidden line `Form → Force` (docs/05).
- **Maqām alone** never licenses `SpeechForceKind` — that would be
  the forbidden line `Context → Force` (docs/05).
- **Relation alone** never licenses `SpeechForceKind` — that would
  re-introduce the export forbidden by docs/40 §9.

The compatibility rule does not name any sub-shape discriminator
beyond the existing docs/35 §4 family list. PR-20 must read the
family from the existing `FormalStyleCandidate` surface; it must
not introduce a new `FormalStyleShape` enum or a new sub-typing
layer.

The bridge does not promote, narrow, or otherwise modify the input
`FormalStyleVerdict`. A successful bridge check yields only the
internal fact that the pair is compatible under the shared maqām;
PR-20 may carry this as an internal predicate of the
`IfādahCandidate` it builds, never as a free-standing verdict.

## §7 Failure surface (mapping, not new FailureCode)

The closed taxonomy for PR-20 remains the one declared by docs/41
§6. This law adds no new `FailureCode` member. It specifies, for
the refusal label `FORMAL_STYLE_CONFLICT` named in docs/41 §6,
exactly one of two licit implementations PR-20 may choose, mirroring
docs/41 §6's either-or rule for `MAQAM_DIVERGENCE`:

1. add `FailureCode.FORMAL_STYLE_CONFLICT` as a new `FailureCode`
   member, justified by this law (docs/42 §6 + §7); or
2. use an existing `FailureCode` member with a `trace_ref` whose
   token includes the literal `"formal_style_conflict"`.
   `FailureCode.REQUIRED_SLOT_EMPTY` is **not** an acceptable
   existing fallback (the slots are present; the pair is
   incompatible). If option (2) is chosen, the existing member must
   be one that does not misrepresent the failure as a missing input
   (e.g. `FailureCode.IDENTITY_BROKEN` with the
   `"formal_style_conflict"` token is acceptable; PR-20's review
   must justify the choice).

Silent fallback (no code, no trace label) is forbidden and is itself
a `FORBIDDEN_LEAP`.

This law does **not** restate the other refusals named in docs/41
§6 (`NO_RELATION_CLOSURE`, `NO_FORMAL_STYLE`, `NO_SPEECH_FORCE`,
`NO_IFADAH_MAQAM`, `MAQAM_DIVERGENCE`, `NO_IFADAH_EVIDENCE`,
`NO_IFADAH_SCOPE`, `IDENTITY_BROKEN`, `HIDDEN_RESIDUAL`,
`BLOCKING_RESIDUAL`, `RANK_EXCEEDS_CEILING`, `GATE_REQUIRED`,
`REQUIRED_SLOT_EMPTY`). Their semantics belong to docs/41 and are
unchanged by this bridge.

## §8 Constitutional invariants (binding on PR-20 code)

* `FormalStyleVerdict.state == PROVEN` is a *precondition* of the
  bridge, not a derivation. A non-PROVEN `FormalStyleVerdict` is
  refused under docs/41 §6 `NO_FORMAL_STYLE`, before §6 of this
  law is ever reached.
* `SpeechForceKind ∈ {KHABAR, INSHA}` is a *precondition* of the
  bridge, not a derivation. A `SpeechForceKind` outside the minimal
  set is refused under docs/41 §6 `NO_SPEECH_FORCE`, before §6 of
  this law is ever reached.
* `MaqamContextBoundaryVerdict.state == PROVEN` and a single shared
  maqām verdict across all input verdicts is a *precondition* of
  the bridge. A missing or divergent maqām is refused under
  docs/41 §6 (`NO_IFADAH_MAQAM` / `MAQAM_DIVERGENCE`), before §6
  of this law is ever reached.
* The bridge step in PR-20 (whatever symbol PR-20 names it; this
  law does not name a symbol) must be **pure**: it takes the two
  verdicts plus the shared `MaqamContextBoundaryVerdict` and
  returns either an explicit "compatible" predicate (internal to
  the `IfādahCandidate` being built) or a named refusal per §7.
* The bridge must not write to the ledger, perform I/O, query a
  clock, or call out to any successor layer (Hukm, Manāṭ, Tanzīl,
  AnswerAudit).
* The bridge must not introduce a new top-level carrier exported
  from PR-20. The bridge result is an internal predicate of
  `IfādahCandidate`; it does not become `SpeechForceVerdict`,
  `BridgeVerdict`, or any other free-standing object.

## §9 Deferred residuals (carried explicitly by PR-20)

All residuals named here MUST carry `visibility = EXPLANATORY` when
emitted on an `IfādahCandidate`; emitting any of them with hidden
or blocking visibility is `HIDDEN_RESIDUAL` / `BLOCKING_RESIDUAL`
under docs/41 §6.

| Name                                          | Note                                                |
|-----------------------------------------------|-----------------------------------------------------|
| `EXTRA_SPEECH_FORCE_DEFERRED`                 | `AMR`, `NAHY`, `ISTIFHAM`, `NIDA`, `DUA`, `TAMANNI`, `TARAJJI`, `TAHDID`, `TAAJJUB`, `QASAM` — never enum members in PR-20. |
| `SPEAKER_INTENT_DEFERRED`                     | Re-anchored from docs/41 §10. The bridge is the layer at which the reader is most tempted to leap from formal/force compatibility to speaker intent; that leap is forbidden. |
| `HUKM_DEFERRED_UNTIL_DOCS_43`                 | Pointer; semantics remain in docs/41 §10 and the future docs/43 (PR-D7). |
| `MANAT_DEFERRED_UNTIL_DOCS_44`                | Pointer; semantics remain in docs/41 §10 and the future docs/44 (PR-D8). |
| `TANZIL_DEFERRED_UNTIL_DOCS_45`               | Pointer; semantics remain in docs/41 §10 and the future docs/45 (PR-D9). |
| `MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL`        | Pointer; awaits docs/46 (PR-D10) horizontal-branch licence. |
| `MAJAZ_HAQIQAH_DEFERRED_POST_VERTICAL`        | Pointer; awaits docs/46 (PR-D10) horizontal-branch licence. |

The deferred-residual identifiers listed above are ASCII
transliterations only; Arabic prose may write *أمر*, *نهي*,
*استفهام*, etc.

## §10 Forbidden surface (mirror of §3, declared explicitly)

PR-20 (code) **must not** export, define, instantiate, alias, or
reference any of the following identifiers under licence of this
law. Identifiers are ASCII transliterations without diacritics, per
the repository convention.

* `SpeechForceVerdict`, `SpeechForceState`, `SpeechForceCandidate`
* `BridgeVerdict`, `BridgeCandidate`, `BridgeState`
* `FormalStyleShape` (a new sub-shape enum is not licensed by this
  law; use the docs/35 §4 family list)
* `FormalForceFusion`, `FormForceMap`, `FormForceAlignment`
* Any `SpeechForceKind` member outside the minimal set
  `{KHABAR, INSHA}`. The members `AMR`, `NAHY`, `ISTIFHAM`,
  `NIDA`, `DUA`, `TAMANNI`, `TARAJJI`, `TAHDID`, `TAAJJUB`,
  `QASAM` are deferred residuals only (§9); PR-20 must carry them
  as explanatory residuals, never as enum members.
* `HukmCandidate`, `HukmVerdict`, `HukmState`
* `ManatCandidate`, `ManatVerdict`, `ManatState`, `ManatMode`
* `TanzilCandidate`, `TanzilVerdict`, `TanzilState`
* `MafhumCandidate`, `MantuqClosure`
* `MajazVerdict`, `MajazLicense`, `ManqulVerdict`, `ManqulLicense`
* `HaqiqahAttemptVerdict`
* `SpeakerIntentVerdict`
* `FinalMeaning`, `Meaning`, `OntologicalClaim`
* `PropositionTruthValue`, `ProofObligation`
* `NormativeJudgment`, `NORMATIVE`

A future PR that needs any of these must declare its own chain
position and origin law.

## §11 Reading order for reviewers of PR-20

```text
1. docs/13 — Constitutional PR Geometry
2. docs/14 — PR Chain Roadmap (Amendment-12 and Amendment-12.x)
3. docs/35 — Formal Style Candidate Law
4. docs/37 — Maqām/Context Boundary Readiness Law
5. docs/40 — Relation Closure Law
6. docs/41 — Ifādah Boundary Law
7. docs/42 — this document
8. The PR-20 PR description, checked against (1)–(7).
```

A reviewer who skips (5), (6), or (7) cannot tell whether PR-20 is
a constitutional branch or a leap. CI cannot tell either.

---

*Ratified by PR-D6 (law only — no code, no carrier, no enum). This
document is the SpeechForce/FormalStyle bridge declared as a
necessary companion by docs/41 §2 and deferred to by docs/41 §6
under the `FORMAL_STYLE_CONFLICT` refusal label.*
