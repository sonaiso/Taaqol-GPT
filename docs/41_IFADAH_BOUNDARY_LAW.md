# 41 — Ifādah Boundary Law

> **Status:** Constitutional law. Ratified by PR-D5 (law only — no
> code). Binds every later PR that constructs, processes, or consumes
> an `IfādahCandidate` — most directly PR-20 (IfādahCandidate code),
> and transitively PR-D7/PR-21 (Hukm), PR-D8/PR-21M (Manāṭ),
> PR-D9/PR-22 (Tanzīl), PR-22-AUDIT, and PR-D10 (Vertical Path
> Closure). It is load-bearing.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change. Any attempt to import an
> `IfādahCandidate`, an `IfadahVerdict`, an `IfadahState`, or a
> `prove_ifadah_candidate()` symbol before PR-20 (the code PR) is
> merged is a `FORBIDDEN_LEAP` regardless of CI status.

## §1 Governing principle (ما يحفظ — what it preserves)

```text
No IfādahCandidate without a PROVEN RelationClosureVerdict.
No IfādahCandidate without a PROVEN FormalStyleVerdict.
No IfādahCandidate without a licensed SpeechForceKind inside a maqam.
No IfādahCandidate without a single shared MaqamContextReadinessVerdict.
No IfādahCandidate that produces a hukm, a tanzīl, a mafhūm, a
   manṭūq, a majāz, a haqīqah claim, a final meaning, a reality
   application, or a speaker-intent verdict.
No IfādahCandidate is a proposition in the logical sense.
No IfādahCandidate is a certificate; it remains a candidate forever.
```

`IfādahCandidate` proves that a closed relation between two
mufrad-dalālah-closed units carries a **speech-level closure** (a
candidate proposition-shape) inside a single bounded maqām. It does
not determine truth, hukm, application, or meaning.

The constitutional middle terms preserved by this law:

```text
RelationClosure   (what the units form together — PR-D4)
FormalStyleClosure (what the form licenses — PR-F8 / docs/35)
SpeechForce        (what the speaker-shape declares — KHABAR | INSHĀ)
MaqamContextReadiness (where the discourse is bounded — PR-D1.2 / docs/37)
```

None of the four can substitute for any other. Ifādah is the
boundary at which all four must be simultaneously present and
mutually consistent.

## §2 What this law opens

```text
PR-20 — IfādahCandidate (code).
        Carriers: IfādahCandidate, IfadahVerdict, IfadahState,
                  SpeechForceKind (minimal: KHABAR, INSHĀ),
                  IFADAH_RANK_CEILING, prove_ifadah_candidate().
        Nothing else.
```

PR-20 is the **only** PR licensed by docs/41. It produces a
candidate carrier, never a hukm and never a meaning.

This law also licenses docs/42 (SpeechForce/FormalStyle Bridge Law,
PR-D6) as its *necessary companion* — PR-20 may not merge until
both docs/41 and docs/42 are ratified.

## §3 What this law forbids

```text
No HukmCandidate.
No ManatCandidate.
No TanzilCandidate.
No MafhumCandidate.
No MantuqClosure.
No MajazVerdict / MajazLicense.
No ManqulVerdict / ManqulLicense.
No HaqiqahAttemptVerdict.
No SpeakerIntentVerdict.
No FinalMeaning / Meaning.
No PropositionTruthValue.
No external execution / enforcement / tool action.
No legal, religious, or normative authority claim.
No Ω-style domain assignment beyond docs/20 scope.
No re-export, alias, or string representation that drops the
   "Candidate" suffix from any Ifādah-layer carrier.
No synthesis of a missing input verdict.
No silent reordering of input verdicts. Their semantic positions are
   fixed by the signature of prove_ifadah_candidate().
No coercion of a free-text maqām into a verdict object.
```

PR-20 ships none of these. Any future PR that ships any one of
them must declare its own origin law and its own chain position.

## §4 Domain (المجال — where this law applies)

```text
Speech-level closure at the boundary between RelationClosure (PR-D4)
and HukmCandidate (PR-D7 + PR-21). It binds:

  * PR-20 (IfādahCandidate code).
  * PR-D6 (docs/42, SpeechForce/FormalStyle Bridge Law).
  * PR-D7 / PR-21 (Hukm) — Hukm may consume an IfādahCandidate, but
    may never recompute one.
  * PR-22-AUDIT — AnswerAudit may surface an IfādahCandidate inside
    an AuditedAnswer only as a candidate, never as a proposition.

It does not bind:
  * Core kernel (core/) — Ifādah is not a SlotGraph property.
  * Adapter layer (audit/) — adapters never produce Ifādah.
  * Any horizontal branch (majāz, mantūq, mafhūm, naql, GPT-proposer,
    reference expansion, conditions DAG) — these are forbidden
    before docs/46 (PR-D10) closes the vertical path.
```

## §5 Evidence (الدليل — what justifies this boundary)

1. **PR-F7.1 chain-correction law**: No Ifādah before mufrad
   dalālah closure. Closure of dalālah (PR-D3) and closure of
   relation (PR-D4) are necessary but not sufficient; the speech
   surface remains open.
2. **PR-D4 forbidden-surface clause** (docs/40 §9): RelationClosure
   explicitly forbids exporting `IfadahCandidate`. The boundary
   must therefore be erected outside PR-D4.
3. **PR-F8 (docs/35)**: FormalStyleCandidate proves the formal
   readiness for a speech style (e.g. khabar/inshāʾ surface), but
   formal readiness alone never determines speech force inside a
   maqām. The bridge is constitutive, not derivative.
4. **PR-D1.2 (docs/37)**: MaqamContextBoundary establishes a single
   discourse domain at the readiness level. Two units cannot relate
   across diverging maqāms without breaking identity continuity;
   speech-level closure inherits this constraint and tightens it
   (a single shared verdict, not two equivalent ones).
5. **Forbidden Straight-Line Registry (docs/05, PR-5)**: The lines
   `Candidate → Certificate`, `Evidence → Certainty`, and
   `Signifier → Meaning` are constitutionally forbidden. Ifādah
   sits on exactly those forbidden lines; only an explicit boundary
   law can prevent the leap.

## §6 Failure surface (الفشل — named refusals)

`prove_ifadah_candidate()` must refuse with one of these
`FailureCode` values; no silent `None`, no bare exception:

```text
NO_RELATION_CLOSURE
    The relation_closure_verdict is missing, malformed, not a
    RelationClosureVerdict, or not in state PROVEN.

NO_FORMAL_STYLE
    The formal_style_verdict is missing, malformed, not a
    FormalStyleVerdict, or not in state PROVEN.

NO_SPEECH_FORCE
    The speech_force is missing, not a member of SpeechForceKind,
    or is a forbidden member outside the minimal set
    (anything beyond KHABAR | INSHĀ in PR-20).

NO_IFADAH_MAQAM
    The ifadah_maqam_verdict is missing, malformed, not a
    MaqamContextReadinessVerdict, or not in state READY.

MAQAM_DIVERGENCE
    The ifadah_maqam_verdict does not equal the
    MaqamContextReadinessVerdict that the relation_closure_verdict
    (and both underlying MufradDalalahClosureVerdicts) were
    produced under. A single shared maqam verdict is required.

FORMAL_STYLE_CONFLICT
    The formal_style_verdict and speech_force are incompatible
    under the bridge law (see docs/42, PR-D6).

NO_IFADAH_EVIDENCE
    ifadah_evidence is empty or whitespace-only.

NO_IFADAH_SCOPE
    closure_scope is empty or whitespace-only.

IDENTITY_BROKEN
    The first/second dal_identity_ref carried by the relation
    closure no longer match the identities under which the
    formal_style_verdict was proven; the three input verdicts are
    not co-referent.

HIDDEN_RESIDUAL
    A residual carried by any input verdict is hidden
    (visibility != EXPLANATORY) at the point of consumption.

BLOCKING_RESIDUAL
    A residual carried by any input verdict is in a blocking state.

RANK_EXCEEDS_CEILING
    The meet of input ranks against IFADAH_RANK_CEILING exceeds the
    ceiling.

GATE_REQUIRED
    Any input verdict crossed a layer without a TransitionGate
    proof attached.

REQUIRED_SLOT_EMPTY
    Any structurally required field on the IfādahCandidate carrier
    is empty.
```

The taxonomy is closed for PR-20. Any new failure code must come
with a new chain-step PR and its own origin law.

## §7 Effect (الأثر — what changes when this law is ratified)

* PR-20 becomes reviewable. Without docs/41 + docs/42, PR-20 is a
  `FORBIDDEN_LEAP`.
* PR-D7 / PR-21 (Hukm) acquire a single legal input shape
  (`IfadahVerdict` of state `PROVEN`).
* PR-22-AUDIT acquires a contract: an IfādahCandidate may flow into
  an `AuditedAnswer` only as a candidate, bounded by the
  presentation boundary that docs/45 (PR-D9) will erect.
* PR-D10 (docs/46, Vertical Path Closure Law) becomes able to assert
  trace continuity through the Ifādah layer.
* Any existing residual named `IFADAH_DEFERRED_UNTIL_SPEECH_FORCE`
  (docs/40 §7) is re-anchored to this law as its closing reference.
  PR-20 may consume that residual; no other PR may.

## §8 Constitutional invariants (binding on PR-20 code)

* `IfādahCandidate` ≠ Meaning.
* `IfādahCandidate` ≠ FinalMeaning.
* `IfādahCandidate` ≠ Hukm.
* `IfādahCandidate` ≠ Manāṭ.
* `IfādahCandidate` ≠ Tanzīl.
* `IfādahCandidate` ≠ PropositionTruthValue.
* `IfādahCandidate` ≠ SpeakerIntentVerdict.
* `IfādahCandidate` ≠ MafhumCandidate / MantuqClosure.
* `IfādahCandidate` ≠ MajazVerdict / HaqiqahAttemptVerdict.
* `IfādahCandidate` ≠ OntologicalClaim.
* `IfādahCandidate` ≠ FreeReasoning.
* No ifādah closure without three PROVEN input verdicts
  (RelationClosure, FormalStyle, MaqamContextReadiness).
* No ifādah closure without a licensed SpeechForceKind inside the
  minimal set declared by PR-20.
* No ifādah closure without a single shared maqām verdict across
  every prior layer the inputs depend on.
* No ifādah closure with hidden or blocking residuals.
* No rank promotion beyond `IFADAH_RANK_CEILING`.
* All operations are pure: no I/O, no ledger, no network, no
  filesystem, no clock.

## §9 Forbidden surface (mirror of §3, declared explicitly)

PR-20 (code) **must not** export, define, instantiate, alias, or
reference:

* `HukmCandidate`, `HukmVerdict`, `HukmState`
* `ManatCandidate`, `ManatVerdict`, `ManatState`, `ManatMode`
* `TanzilCandidate`, `TanzilVerdict`, `TanzilState`
* `MafhumCandidate`, `MantuqClosure`
* `MajazVerdict`, `MajazLicense`, `ManqulVerdict`, `ManqulLicense`
* `HaqiqahAttemptVerdict`
* `SpeakerIntentVerdict`
* `FinalMeaning`, `Meaning`, `OntologicalClaim`
* `PropositionTruthValue`, `ProofObligation`
* `NormativeJudgment`, `NORMATIVE` (use only `NORMATIVE_CANDIDATE`
  once docs/43 / PR-D7 is ratified — never inside PR-20)
* Any `SpeechForceKind` member outside the minimal set
  (`KHABAR`, `INSHĀ`). The members `AMR`, `NAHY`, `ISTIFHAM`,
  `NIDA`, `DUʿĀʾ`, `TAMANNI`, `TARAJJI`, `TAHDID`, `TAʿAJJUB` are
  deferred residuals only; PR-20 must carry them as explanatory
  residuals, never as enum members.

A future PR that needs any of these must declare its own chain
position and origin law.

## §10 Deferred residuals (carried explicitly by PR-20)

| Name                                          | Note                                                |
|-----------------------------------------------|-----------------------------------------------------|
| `IFADAH_NOT_PROPOSITION`                      | Ifādah is candidate-shape, not truth-valued.        |
| `HUKM_DEFERRED_UNTIL_HUKM_DOMAIN_LAW`         | Awaits docs/43 (PR-D7).                             |
| `MANAT_DEFERRED_UNTIL_MANAT_LAW`              | Awaits docs/44 (PR-D8).                             |
| `TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW`      | Awaits docs/45 (PR-D9).                             |
| `MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL`        | Awaits docs/46 (PR-D10) horizontal-branch licence.  |
| `MAJAZ_HAQIQAH_DEFERRED_POST_VERTICAL`        | Awaits docs/46 (PR-D10) horizontal-branch licence.  |
| `EXTRA_SPEECH_FORCE_DEFERRED`                 | AMR / NAHY / ISTIFHAM / etc. — never in PR-20.      |
| `SPEAKER_INTENT_DEFERRED`                     | Speaker intent is not Ifādah.                       |
| `AUDIT_INTEGRATION_DEFERRED_UNTIL_PR_22_AUDIT`| AnswerAudit bridge ships in PR-22-AUDIT.            |

All deferred residuals MUST carry `visibility = EXPLANATORY` when
emitted on an `IfādahCandidate`; emitting any of them with hidden
or blocking visibility is `HIDDEN_RESIDUAL` / `BLOCKING_RESIDUAL`.

## §11 Reading order for reviewers of PR-20

```text
1. docs/13 — Constitutional PR Geometry
2. docs/14 — PR Chain Roadmap (this PR appears in Amendment-12)
3. docs/35 — Formal Style Candidate Law
4. docs/37 — Maqām/Context Boundary Readiness Law
5. docs/40 — Relation Closure Law
6. docs/41 — this document
7. docs/42 — SpeechForce/FormalStyle Bridge Law (PR-D6)
8. The PR-20 PR description, checked against (1)–(7).
```

A reviewer who skips (5), (6), or (7) cannot tell whether PR-20 is
a constitutional branch or a leap. CI cannot tell either.
