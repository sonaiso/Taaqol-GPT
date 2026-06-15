# 45 — Tanzīl Presentation Boundary Law

> **Status:** Constitutional law. Ratified by PR-D9 (law only — no
> code). Binds every later PR that constructs, processes, or consumes
> a `TanzilCandidate` — most directly PR-22 (TanzīlCandidate code),
> and transitively PR-22-AUDIT (Vertical Chain AnswerAudit Bridge)
> and PR-D10 (Vertical Path Closure Law). It is load-bearing.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change. Any attempt to import a
> `TanzilCandidate`, a `TanzilVerdict`, a `TanzilState`, or a
> `prove_tanzil_candidate()` symbol before PR-22 (the code PR) is
> merged is a `FORBIDDEN_LEAP` regardless of CI status.

## §1 Governing principle (ما يحفظ — what it preserves)

```text
No TanzilCandidate without a PROVEN HukmVerdict.
No TanzilCandidate without a PROVEN ManatVerdict.
No TanzilCandidate without a presentation envelope.
No TanzilCandidate that constitutes execution.
No TanzilCandidate that constitutes fatwa.
No TanzilCandidate that constitutes qada.
No TanzilCandidate that constitutes final authority.
No TanzilCandidate without a NOT_EXECUTION_WARNING marker.
No presentation of TanzilCandidate without visible rank, residuals,
   and trace.
No serialization of TanzilCandidate that separates it from its
   presentation envelope.
TanzilCandidate is presentation-bound application readiness, not
   execution.
```

`TanzilCandidate` presents the point at which a `ManatCandidate`
(the candidate locus of application) meets a specific case
description and instance evidence — making the application of the
judgment *presentable*. It does **not** execute, enforce, certify,
or authorise. It produces a presentation-bound envelope that must
always carry an explicit warning: this is not execution, not fatwa,
not qada, not final authority.

The constitutional distinction preserved by this law:

```text
HukmCandidate     (what evaluation says about a closed ifādah
                   inside a bounded domain — PR-21)
ManatCandidate    (where the judgment-candidate would apply: the
                   effective attribute and the locus description — PR-21M)
TanzilCandidate   (how the judgment-candidate is presented for a
                   specific case — PR-22; always within an envelope)
```

None of the three can substitute for any other. Tanzīl is the
boundary at which a ManatCandidate acquires a specific-case
presentation, never the point at which the judgment is executed or
authority is exercised.

The governing sentence:

```text
التنزيل لا يُنفَّذ.
والتنزيل لا يُعرض بلا غلاف.
وكل عرض بلا تحذير هو تسرب تنفيذ.
```

## §2 What this law opens

```text
PR-22 — TanzilCandidate (code).
         Carriers: TanzilCandidate, TanzilVerdict, TanzilState,
                   TANZIL_RANK_CEILING, prove_tanzil_candidate().
         Each candidate must carry a presentation envelope per §6.
         Nothing else.
```

PR-22 is the **only** PR licensed by docs/45. It produces a
presentation-bound candidate carrier, never execution and never
authority.

The enum surface in PR-22 must use ASCII transliterations without
diacritics (`TanzilCandidate`, `TanzilVerdict`, `TanzilState`,
`TANZIL_RANK_CEILING`). Arabic prose may still write *تنزيل*;
the code identifier is `TanzilCandidate`.

## §3 What this law forbids

```text
No Execution.
No ExternalAction.
No Enforcement.
No Fatwa.
No Qada.
No FinalAuthority.
No DivineAuthorityClaim.
No VerifiedRealityClaim (tanzil does not verify — it presents).
No RealityApplication (tanzil does not apply — it presents).
No FinalMeaning / Meaning.
No OntologicalClaim.
No FreeReasoning.
No PropositionTruthValue.
No AuthorityClaim.
No NormativeJudgment.
No MafhumCandidate.
No MantuqClosure.
No MajazVerdict / MajazLicense.
No ManqulVerdict / ManqulLicense.
No HaqiqahAttemptVerdict.
No SpeakerIntentVerdict.
No bare TanzilCandidate serialization without presentation envelope.
No __repr__ that drops the warning.
No serialization that hides rank, residuals, or trace.
No horizontal branches (Majāz, Mantūq, Mafhūm, Naql, GPT-proposer,
   reference expansion, conditions DAG) before PR-D10.
```

PR-22 ships none of these. Any future PR that ships any one of
them must declare its own origin law and its own chain position.

## §4 Domain (المجال — where this law applies)

```text
Presentation of the candidate application of a HukmCandidate
through a ManatCandidate to a specific case, at the boundary
between ManatCandidate (PR-21M) and the AnswerAudit surface
(PR-22-AUDIT).

It binds:

  * PR-22 (TanzilCandidate code).
  * PR-22-AUDIT — AnswerAudit surfaces a TanzilCandidate inside
    an AuditedAnswer only within the presentation envelope
    defined here.
  * PR-D10 (docs/46, Vertical Path Closure Law) — asserts trace
    continuity through the Tanzīl layer.

It does not bind:
  * Core kernel (core/) — Tanzīl is not a SlotGraph property.
  * Adapter layer (audit/) — adapters never produce Tanzīl.
  * Any horizontal branch (majāz, mantūq, mafhūm, naql,
    GPT-proposer, reference expansion, conditions DAG) — these
    are forbidden before docs/46 (PR-D10) closes the vertical path.
```

## §5 Evidence (الدليل — what justifies this boundary)

1. **docs/44 §1 (Manāṭ Boundary Law)**: ManatCandidate explicitly
   states "No ManatCandidate that produces tanzīl, reality
   application, enforcement, execution, or authority." The boundary
   between Manāṭ and Tanzīl must therefore be a law that governs
   how the next carrier is presented.
2. **docs/44 §11 deferred-residual table**: The residual
   `TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW` names this very document
   (docs/45) as its closing reference. PR-22 may consume that
   residual; no other PR may.
3. **docs/04 (Forbidden Straight-Line Transitions, PR-5)**
   forbids `Candidate → Certificate` and `Judgment → Application`.

   **docs/05 (Rank Lattice, PR-3)**
   bounds any downstream rank movement and prevents rank overclaim.

   Tanzīl sits on this boundary to prevent the leap from
   ManatCandidate to Execution / Authority; only an explicit
   presentation law can guard the transition.
4. **Amendment-12 vertical closure path**: No horizontal branch
   before PR-D10. Tanzīl is part of the vertical column and must be
   staged before the AnswerAudit bridge.
5. **The governing sentence**: التنزيل لا يُنفَّذ — a presentation
   candidate does not execute; it requires a presentation envelope
   that warns the consumer this is not execution, not fatwa, not
   qada, not final authority. Without this boundary, the leap
   ManatCandidate → Execution is constitutionally unguarded.

## §6 Presentation envelope (binding on PR-22)

Every `TanzilCandidate` emitted by `prove_tanzil_candidate()` must
carry a **presentation envelope** containing at minimum:

```text
NOT_EXECUTION_WARNING
    Explicit marker that the candidate is not execution.

NOT_FATWA
    Explicit marker that the candidate is not fatwa.

NOT_QADA
    Explicit marker that the candidate is not qada.

NOT_FINAL_AUTHORITY
    Explicit marker that the candidate is not final authority.

rank_visible
    The rank of the candidate must be visible in any output.

residuals_visible
    All residuals must be visible in any output (no hidden residuals).

trace_visible
    The trace reference chain must be visible in any output.

hukm_ref_visible
    The originating HukmCandidate reference must be visible.

manat_ref_visible
    The originating ManatCandidate reference must be visible.
```

### §6.1 Envelope discipline (binding on PR-22)

```text
* NOT_EXECUTION_WARNING must be structurally attached to the
  TanzilCandidate, not injected after the fact.
* NOT_FATWA, NOT_QADA, NOT_FINAL_AUTHORITY must be structurally
  attached, not injected after the fact.
* No serialization of TanzilCandidate may separate it from its
  envelope. A bare TanzilCandidate without envelope is a
  structural violation, not merely a missing field.
* No __repr__ of TanzilCandidate may omit the warning markers.
* The presentation envelope is not a cosmetic label. It is a
  constitutional boundary marker that prevents the consumer from
  reading the candidate as execution.
* PR-22-AUDIT must preserve the envelope inside AuditedAnswer;
  AnswerAudit may not drop any envelope field.
```

### §6.2 Forbidden presentation forms (binding on PR-22)

PR-22 **must not** produce, alias, import, or reference any of:

```text
EXECUTED
ENFORCED
APPLIED
CERTIFIED
FINAL
AUTHORITATIVE
BINDING
FATWA_ISSUED
QADA_ISSUED
REALITY_VERIFIED
```

A future PR that needs any such presentation state must declare its
own chain position and its own origin law. It cannot appear before
PR-D10 (Vertical Path Closure).

## §7 Failure surface (الفشل — named refusals for PR-22)

`prove_tanzil_candidate()` must refuse with one of these labels; no
silent `None`, no bare exception:

```text
NO_HUKM
    The hukm_verdict is missing, malformed, not a HukmVerdict,
    or not in state PROVEN.

NO_MANAT
    The manat_verdict is missing, malformed, not a ManatVerdict,
    or not in state PROVEN.

NO_REALITY_EVIDENCE
    The reality_evidence (instance-level evidence about the case)
    is missing or empty.

NO_INSTANCE_DESCRIPTOR
    The instance_descriptor (description of the specific case)
    is missing or empty.

NO_PRESENTATION_BOUNDARY
    The presentation envelope is missing or incomplete.

NO_TANZIL_SCOPE
    The tanzil_scope (scope of application presentation) is
    missing or empty.

PRESENTATION_WARNING_MISSING
    The NOT_EXECUTION_WARNING or any other mandatory envelope
    marker is missing from the TanzilCandidate.

EXECUTION_LEAK
    The candidate attempts to produce execution, enforcement,
    external action, or any form of authority exercise.

AUTHORITY_LEAK
    The candidate attempts to claim fatwa, qada, divine
    authority, or final legal/religious authority.

REALITY_APPLICATION_OVERCLAIM
    The candidate claims that reality has been verified or that
    the judgment has been applied to the real world. Tanzīl
    is presentation, not verification.

HIDDEN_RESIDUAL
    A residual carried by the input verdicts or produced by the
    tanzīl operation is hidden (visibility != EXPLANATORY) at
    the point of consumption or emission.

BLOCKING_RESIDUAL_PRESENT
    A residual carried by any input verdict is in a blocking state.

RANK_EXCEEDS_CEILING
    The meet of input rank against TANZIL_RANK_CEILING exceeds the
    ceiling.
```

### §7.1 FailureCode rule

PR-22 must either add dedicated `FailureCode` members for the labels
above, or map these refusals to existing `FailureCode` values with
exact `trace_ref` labels (e.g. `FailureCode.REQUIRED_SLOT_EMPTY` with
`trace_ref="no_instance_descriptor"`). Silent fallback — where a
refusal produces no named code and no trace label — is forbidden and
is itself a `FORBIDDEN_LEAP`.

## §8 Effect (الأثر — what changes when this law is ratified)

* PR-22 becomes reviewable. Without docs/45, PR-22 is a
  `FORBIDDEN_LEAP`.
* PR-22-AUDIT acquires a contract: a TanzilCandidate may flow into
  an `AuditedAnswer` only within the presentation envelope defined
  in §6.
* PR-D10 (docs/46, Vertical Path Closure Law) becomes able to assert
  trace continuity through the Tanzīl layer.
* The deferred residual `TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW`
  (declared in docs/44 §11) is re-anchored to this law as its closing
  reference. PR-22 may consume that residual; no other PR may.

## §9 Constitutional invariants (binding on PR-22 code)

* `TanzilCandidate` ≠ Execution.
* `TanzilCandidate` ≠ ExternalAction.
* `TanzilCandidate` ≠ Enforcement.
* `TanzilCandidate` ≠ Fatwa.
* `TanzilCandidate` ≠ Qada.
* `TanzilCandidate` ≠ FinalAuthority.
* `TanzilCandidate` ≠ DivineAuthorityClaim.
* `TanzilCandidate` ≠ RealityVerification.
* `TanzilCandidate` ≠ RealityApplication.
* `TanzilCandidate` ≠ FinalMeaning.
* `TanzilCandidate` ≠ Meaning.
* `TanzilCandidate` ≠ PropositionTruthValue.
* `TanzilCandidate` ≠ OntologicalClaim.
* `TanzilCandidate` ≠ FreeReasoning.
* `TanzilCandidate` ≠ AuthorityClaim.
* `TanzilCandidate` ≠ NormativeJudgment.
* `TanzilCandidate` ≠ Certificate.
* No tanzīl closure without a PROVEN HukmVerdict.
* No tanzīl closure without a PROVEN ManatVerdict.
* No tanzīl closure without the ManatCandidate referencing the same
  HukmCandidate.
* No tanzīl closure without reality_evidence.
* No tanzīl closure without instance_descriptor.
* No tanzīl closure without tanzil_scope.
* No tanzīl closure without presentation_warning.
* No tanzīl closure without not_execution_marker.
* No tanzīl closure with hidden or blocking residuals.
* No rank promotion beyond `TANZIL_RANK_CEILING`.
* All operations are pure: no I/O, no ledger, no network, no
  filesystem, no clock.
* Every TanzilCandidate carries its presentation envelope at birth.
* No TanzilCandidate leaves the weight layer without envelope.

## §10 Forbidden surface (mirror of §3, declared explicitly)

PR-22 (code) **must not** export, define, instantiate, alias, or
reference:

* `Execution`, `ExternalAction`, `Enforcement`
* `Fatwa`, `Qada`, `FinalAuthority`, `DivineAuthorityClaim`
* `RealityApplication`, `RealityVerification`, `VerifiedRealityClaim`
* `MafhumCandidate`, `MantuqClosure`
* `MajazVerdict`, `MajazLicense`, `ManqulVerdict`, `ManqulLicense`
* `HaqiqahAttemptVerdict`, `SpeakerIntentVerdict`
* `FinalMeaning`, `Meaning`, `OntologicalClaim`
* `PropositionTruthValue`, `FreeReasoning`
* `AuthorityClaim`, `NormativeJudgment`
* `EXECUTED`, `ENFORCED`, `APPLIED`, `CERTIFIED`, `FINAL`,
  `AUTHORITATIVE`, `BINDING`, `FATWA_ISSUED`, `QADA_ISSUED`,
  `REALITY_VERIFIED`
* Any serialization or `__repr__` that omits the presentation envelope.

A future PR that needs any of these must declare its own chain
position and origin law.

## §11 Residuals (carried explicitly by PR-22)

| Name                                              | Note                                                        |
|---------------------------------------------------|-------------------------------------------------------------|
| `TANZIL_NOT_EXECUTION`                            | TanzilCandidate is presentation, never execution.           |
| `PRESENTATION_BOUNDARY_REQUIRED`                  | Envelope is mandatory; no bare tanzīl.                       |
| `EXTERNAL_EXECUTION_FORBIDDEN`                    | No external action at the tanzīl boundary.                  |
| `FATWA_FORBIDDEN`                                 | Fatwa is not licensed; not deferred, forbidden.             |
| `QADA_FORBIDDEN`                                  | Qada is not licensed; not deferred, forbidden.              |
| `ANSWER_AUDIT_BRIDGE_DEFERRED`                    | Awaits PR-22-AUDIT to surface inside AuditedAnswer.          |
| `VERTICAL_CLOSURE_DEFERRED`                       | Awaits docs/46 / PR-D10 Vertical Path Closure Law.          |

All residuals MUST carry `visibility = EXPLANATORY` when
emitted on a `TanzilCandidate`; emitting any of them with hidden
or blocking visibility is `HIDDEN_RESIDUAL` / `BLOCKING_RESIDUAL_PRESENT`.

## §12 Required input boundary for PR-22 (مدخلات)

```text
1.  hukm_verdict: HukmVerdict — must be in state PROVEN.
2.  manat_verdict: ManatVerdict — must be in state PROVEN.
3.  manat_candidate must reference the same HukmCandidate as the
    hukm_verdict (identity continuity).
4.  reality_evidence: str — non-empty, non-whitespace (instance-level
    evidence about the specific case).
5.  instance_descriptor: str — non-empty, non-whitespace (description
    of the specific case to which the judgment is being presented).
6.  tanzil_scope: str — non-empty, non-whitespace (scope of the
    presentation).
7.  presentation_warning: str — non-empty (structurally attached
    NOT_EXECUTION_WARNING).
8.  not_execution_marker: bool — must be True.
9.  No hidden or blocking residuals on any input.
10. Rank must not exceed TANZIL_RANK_CEILING.
```

## §13 Derivation prohibition (ممنوعات الاشتقاق)

```text
TanzilCandidate must NOT be derived from:
  * HukmVerdict directly (must go through ManatVerdict).
  * IfadahVerdict directly (must go through HukmVerdict + ManatVerdict).
  * RelationClosureVerdict directly (must go through the full chain).
  * MufradDalalahClosureVerdict directly (must go through the full chain).
  * FormalStyleVerdict directly (must go through the full chain).
  * Any pre-hukm carrier directly.
  * ManatCandidate alone without ManatVerdict PROVEN.

The only legal derivation path:
  HukmVerdict (PROVEN) → ManatVerdict (PROVEN) → prove_tanzil_candidate()
  → TanzilCandidate (with envelope)
```

Any shortcut that bypasses the ManatCandidate layer, or that omits
the presentation envelope, is a `FORBIDDEN_LEAP` regardless of CI
status.

## §14 Presentation versus execution (العرض مقابل التنفيذ)

This section makes explicit the core distinction this law guards:

```text
Presentation (tanzīl):
    "This judgment-candidate, applied through this manāṭ-candidate,
     would — if all conditions are verified and no preventers apply —
     produce this result for this specific case. This is a candidate
     presentation. It is not execution."

Execution (forbidden):
    "This judgment is hereby applied. This is binding. This is final.
     Act on it."
```

The distance between these two is not a matter of confidence or
probability. It is a structural constitutional boundary. No amount
of evidence, no high rank, no zero residuals can collapse
presentation into execution. Only a future law — beyond the current
chain — could license execution, and it would need its own
constitutional boundary, its own chain position, and its own
origin law.

## §15 Reviewer law (binding on PR review)

```text
PR-D9 is law-only.
It licenses PR-22 only.
It does not create TanzilCandidate in runtime.
It does not bridge AnswerAudit.
It does not execute anything.
No PR-22 may start until PR-D9 is merged.
```

A reviewer who finds any of the following in a PR-D9 submission must
reject:

* Any file under `src/`
* Any file under `tests/` (other than pre-existing test modifications
  that adjust chain expectations)
* Any change to `pyproject.toml`
* Any CI workflow change
* Any runtime symbol (`TanzilCandidate`, `TanzilVerdict`,
  `TanzilState`, `prove_tanzil_candidate()`)
* Any adapter or audit code change
* Any external execution, enforcement, or authority claim
* Any horizontal branch (majāz, mantūq, mafhūm, naql, GPT-proposer,
  reference expansion, conditions DAG)
