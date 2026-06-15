# 44 — Manāṭ Boundary Law

> **Status:** Constitutional law. Ratified by PR-D8 (law only — no
> code). Binds every later PR that constructs, processes, or consumes
> a `ManatCandidate` — most directly PR-21M (ManāṭCandidate code),
> and transitively PR-D9/PR-22 (Tanzīl), PR-22-AUDIT, and PR-D10
> (Vertical Path Closure). It is load-bearing.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change. Any attempt to import a
> `ManatCandidate`, a `ManatVerdict`, a `ManatState`, a `ManatMode`,
> or a `prove_manat_candidate()` symbol before PR-21M (the code PR)
> is merged is a `FORBIDDEN_LEAP` regardless of CI status.

## §1 Governing principle (ما يحفظ — what it preserves)

```text
No ManatCandidate without a PROVEN HukmVerdict.
No ManatCandidate without a declared ManatMode.
No ManatCandidate without a manat_description.
No ManatCandidate without an effective_attribute_candidate.
No ManatCandidate without manat_evidence.
No ManatCandidate without a manat_domain.
No ManatCandidate that produces tanzīl, reality application,
   enforcement, execution, or authority.
No ManatCandidate that verifies reality.
No ManatCandidate that collapses takhrīj, tanqīḥ, and taḥqīq into
   one undifferentiated mode.
No ManatCandidate is a certificate; it remains a candidate forever.
TAHQIQ_READINESS_ONLY is readiness, never verification.
```

`ManatCandidate` identifies the candidate locus of application for a
proven `HukmCandidate`. It determines **where** a judgment-candidate
might apply — the effective attribute (al-waṣf al-muʾaththir), the
description, and the domain — without verifying that the world
satisfies the conditions. It does not apply the judgment and does not
claim that reality has been checked.

The constitutional distinction preserved by this law:

```text
HukmCandidate    (what evaluation says about a closed ifādah
                  inside a bounded domain — PR-21)
ManatCandidate   (where the judgment-candidate would apply: the
                  effective attribute and the locus description — PR-21M)
TanzilCandidate  (how the judgment is presented once the manat is
                  established — PR-22)
```

None of the three can substitute for any other. Manāṭ is the boundary
at which a HukmCandidate acquires a candidate locus of application,
never the point at which reality is verified or authority is exercised.

The governing sentence:

```text
الحكم لا ينزل بذاته.
والمناط لا يثبت الواقع.
وتحقيق المناط في هذه المرحلة جاهزية لا تطبيق.
```

## §2 What this law opens

```text
PR-21M — ManatCandidate (code).
         Carriers: ManatCandidate, ManatVerdict, ManatState,
                   ManatMode (minimal:
                   TAKHRIJ_CANDIDATE | TANQIH_CANDIDATE |
                   TAHQIQ_READINESS_ONLY),
                   MANAT_RANK_CEILING, prove_manat_candidate().
         Nothing else.
```

PR-21M is the **only** PR licensed by docs/44. It produces a
candidate carrier, never reality verification and never tanzīl.

The enum surface in PR-21M must use ASCII transliterations without
diacritics (`TAKHRIJ_CANDIDATE`, `TANQIH_CANDIDATE`,
`TAHQIQ_READINESS_ONLY`). Arabic prose may still write *مناط*;
the code identifier is `ManatCandidate`.

## §3 What this law forbids

```text
No TanzilCandidate.
No TanzilVerdict / TanzilState.
No RealityApplication.
No Execution.
No Fatwa.
No Qada.
No ExternalAction.
No FinalAuthority.
No VerifiedRealityClaim.
No DivineAuthorityClaim.
No MafhumCandidate.
No MantuqClosure.
No MajazVerdict / MajazLicense.
No ManqulVerdict / ManqulLicense.
No HaqiqahAttemptVerdict.
No SpeakerIntentVerdict.
No OntologicalClaim.
No FreeReasoning.
No PropositionTruthValue.
No AuthorityClaim.
No NormativeJudgment.
No FinalMeaning / Meaning.
No TAHQIQ_FINAL / REALITY_VERIFIED / APPLIED_MANAT / EXECUTED_MANAT.
No FINAL_ILLA / FINAL_QIYAS_RESULT.
No horizontal branches (Majāz, Mantūq, Mafhūm, Naql, GPT-proposer,
   reference expansion, conditions DAG) before PR-D10.
```

PR-21M ships none of these. Any future PR that ships any one of
them must declare its own origin law and its own chain position.

## §4 Domain (المجال — where this law applies)

```text
Identification of the candidate locus of application for a
HukmCandidate, at the boundary between HukmCandidate (PR-21)
and TanzīlCandidate (PR-D9 + PR-22).
It binds:

  * PR-21M (ManatCandidate code).
  * PR-D9 / PR-22 (Tanzīl) — Tanzīl consumes ManatCandidate as
    its prior origin, never produces a new one.
  * PR-22-AUDIT — AnswerAudit may surface a ManatCandidate inside
    an AuditedAnswer only as a candidate, never as verification.
  * PR-D10 (docs/46, Vertical Path Closure Law) — asserts trace
    continuity through the Manāṭ layer.

It does not bind:
  * Core kernel (core/) — Manāṭ is not a SlotGraph property.
  * Adapter layer (audit/) — adapters never produce Manāṭ.
  * Any horizontal branch (majāz, mantūq, mafhūm, naql, GPT-proposer,
    reference expansion, conditions DAG) — these are forbidden
    before docs/46 (PR-D10) closes the vertical path.
```

## §5 Evidence (الدليل — what justifies this boundary)

1. **docs/43 §1 (Hukm Domain Boundary Law)**: HukmCandidate explicitly
   states "No HukmCandidate that produces a tanzīl, a manāṭ verdict,
   a reality application." The boundary must therefore be erected
   *outside* PR-21.
2. **docs/43 §11 deferred-residual table**: The residual
   `MANAT_DEFERRED_UNTIL_MANAT_LAW` names this very document
   (docs/44) as its closing reference. PR-21M may consume that
   residual; no other PR may.
3. **docs/04 (Forbidden Straight-Line Transitions, PR-5)**
   forbids `Candidate → Certificate` and `Judgment → Application`.

   **docs/05 (Rank Lattice, PR-3)**
   bounds any downstream rank movement and prevents rank overclaim.

   Manāṭ sits on this boundary to prevent the leap from HukmCandidate
   to Application / RealityApplication; only an explicit boundary law
   can guard the transition.
4. **Amendment-12 vertical closure path**: No horizontal branch
   before PR-D10. Manāṭ is part of the vertical column and must be
   staged before Tanzīl.
5. **The governing sentence**: الحكم لا ينزل بذاته — a judgment
   candidate does not apply itself; it requires a locus-of-application
   (manāṭ), an effective attribute, and evidence. Without this
   boundary, the leap HukmCandidate → RealityApplication is
   constitutionally unguarded.

## §6 Minimal ManatMode (binding on PR-21M)

PR-21M must declare `ManatMode` with **exactly** the following
minimal members:

```text
TAKHRIJ_CANDIDATE
    Candidate extraction of the effective attribute (al-waṣf
    al-muʾaththir) from the HukmCandidate or its source chain.
    The waṣf is a candidate — never a final ʿillah (cause) and
    never a verified reality fact.

TANQIH_CANDIDATE
    Candidate refinement: removal of non-effective attributes from
    a takhrīj result. The purified waṣf remains a candidate — never
    a final determination of relevance and never a reality claim.

TAHQIQ_READINESS_ONLY
    Readiness to verify the manāṭ in a specific case. This mode
    declares that the manāṭ is structurally ready to be tested
    against the world — but does NOT execute the test, does NOT
    claim reality is verified, and does NOT produce a tahqīq
    verdict. The verification itself is deferred.
```

### §6.1 Mode discipline (binding on PR-21M)

```text
* TAKHRIJ_CANDIDATE ≠ final ʿillah.
* TANQIH_CANDIDATE ≠ reality verification.
* TAHQIQ_READINESS_ONLY ≠ TAHQIQ.
* No mode may collapse into another.
* Each mode must be independently provable.
* The three modes cannot be merged into a single undifferentiated
  ManatMode. PR-21M must reject any attempt to construct a
  ManatCandidate without declaring which specific mode applies.
```

### §6.2 Forbidden ManatMode names (binding on PR-21M)

PR-21M **must not** define, alias, import, or reference any of:

```text
TAHQIQ_FINAL
REALITY_VERIFIED
APPLIED_MANAT
EXECUTED_MANAT
FINAL_ILLA
FINAL_QIYAS_RESULT
VERIFIED_CONDITION
VERIFIED_PREVENTER
EXTERNAL_APPLICATION
```

A future PR that needs any such mode must declare its own chain
position and its own origin law. It cannot appear before PR-D10
(Vertical Path Closure).

## §7 Failure surface (الفشل — named refusals for PR-21M)

`prove_manat_candidate()` must refuse with one of these labels; no
silent `None`, no bare exception:

```text
NO_HUKM
    The hukm_verdict is missing, malformed, not a HukmVerdict,
    or not in state PROVEN.

NO_MANAT_MODE
    The manat_mode is missing or not a member of ManatMode.

NO_MANAT_DESCRIPTION
    manat_description is empty or whitespace-only.

NO_EFFECTIVE_ATTRIBUTE
    effective_attribute_candidate is empty or whitespace-only.

NO_MANAT_EVIDENCE
    manat_evidence is empty or whitespace-only.

NO_MANAT_DOMAIN
    manat_domain is missing or empty.

MANAT_MODE_COLLAPSE
    The candidate attempts to operate in multiple modes
    simultaneously or claims undifferentiated mode. Each
    ManatCandidate must declare exactly one mode.

TAHQIQ_OVERCLAIM
    The candidate claims reality verification, produces a tahqīq
    verdict, or asserts that conditions/preventers have been
    checked in the real world. Only TAHQIQ_READINESS_ONLY is
    permitted; any overclaim is a refusal.

REALITY_APPLICATION_FORBIDDEN
    The candidate attempts to produce a reality application,
    enforcement, execution, or authority claim. This is a
    structural boundary violation, not merely a missing field.

HIDDEN_RESIDUAL
    A residual carried by the input HukmVerdict or produced by the
    manāṭ operation is hidden (visibility != EXPLANATORY) at the
    point of consumption or emission.

BLOCKING_RESIDUAL_PRESENT
    A residual carried by any input verdict is in a blocking state.

RANK_EXCEEDS_CEILING
    The meet of input rank against MANAT_RANK_CEILING exceeds the
    ceiling.
```

### §7.1 FailureCode rule

PR-21M must either add dedicated `FailureCode` members for the labels
above, or map these refusals to existing `FailureCode` values with
exact `trace_ref` labels (e.g. `FailureCode.REQUIRED_SLOT_EMPTY` with
`trace_ref="no_manat_description"`). Silent fallback — where a refusal
produces no named code and no trace label — is forbidden and is itself
a `FORBIDDEN_LEAP`.

## §8 Effect (الأثر — what changes when this law is ratified)

* PR-21M becomes reviewable. Without docs/44, PR-21M is a
  `FORBIDDEN_LEAP`.
* PR-D9 / PR-22 (Tanzīl) acquire a single legal input shape
  (`ManatVerdict` of state `PROVEN`).
* PR-22-AUDIT acquires a contract: a ManatCandidate may flow into
  an `AuditedAnswer` only as a candidate, bounded by the
  presentation boundary that docs/45 (PR-D9) will erect.
* PR-D10 (docs/46, Vertical Path Closure Law) becomes able to assert
  trace continuity through the Manāṭ layer.
* The deferred residual `MANAT_DEFERRED_UNTIL_MANAT_LAW`
  (declared in docs/43 §11) is re-anchored to this law as its closing
  reference. PR-21M may consume that residual; no other PR may.

## §9 Constitutional invariants (binding on PR-21M code)

* `ManatCandidate` ≠ TanzīlCandidate.
* `ManatCandidate` ≠ RealityVerification.
* `ManatCandidate` ≠ RealityApplication.
* `ManatCandidate` ≠ Execution.
* `ManatCandidate` ≠ FinalAuthority.
* `ManatCandidate` ≠ FinalMeaning.
* `ManatCandidate` ≠ Meaning.
* `ManatCandidate` ≠ PropositionTruthValue.
* `ManatCandidate` ≠ OntologicalClaim.
* `ManatCandidate` ≠ FreeReasoning.
* `ManatCandidate` ≠ Enforcement.
* `ManatCandidate` ≠ Fatwa.
* `ManatCandidate` ≠ Qada.
* `ManatCandidate` ≠ DivineAuthorityClaim.
* No manāṭ closure without a PROVEN HukmVerdict.
* No manāṭ closure without one of the minimal ManatMode members.
* No manāṭ closure without explicit manat_description and
  effective_attribute_candidate.
* No manāṭ closure without manat_evidence.
* No manāṭ closure without manat_domain.
* No manāṭ closure with hidden or blocking residuals.
* No rank promotion beyond `MANAT_RANK_CEILING`.
* All operations are pure: no I/O, no ledger, no network, no
  filesystem, no clock.
* `TAHQIQ_READINESS_ONLY` — never `TAHQIQ_FINAL`.

## §10 Forbidden surface (mirror of §3, declared explicitly)

PR-21M (code) **must not** export, define, instantiate, alias, or
reference:

* `TanzilCandidate`, `TanzilVerdict`, `TanzilState`
* `RealityApplication`, `RealityVerification`, `VerifiedRealityClaim`
* `Execution`, `ExternalAction`, `Enforcement`
* `Fatwa`, `Qada`, `FinalAuthority`, `DivineAuthorityClaim`
* `MafhumCandidate`, `MantuqClosure`
* `MajazVerdict`, `MajazLicense`, `ManqulVerdict`, `ManqulLicense`
* `HaqiqahAttemptVerdict`, `SpeakerIntentVerdict`
* `FinalMeaning`, `Meaning`, `OntologicalClaim`
* `PropositionTruthValue`, `FreeReasoning`
* `AuthorityClaim`, `NormativeJudgment`
* `TAHQIQ_FINAL`, `REALITY_VERIFIED`, `APPLIED_MANAT`, `EXECUTED_MANAT`
* `FINAL_ILLA`, `FINAL_QIYAS_RESULT`
* `VERIFIED_CONDITION`, `VERIFIED_PREVENTER`, `EXTERNAL_APPLICATION`
* Any `ManatMode` member outside the minimal set
  (`TAKHRIJ_CANDIDATE`, `TANQIH_CANDIDATE`, `TAHQIQ_READINESS_ONLY`).
  Extended modes are deferred residuals only; PR-21M must carry them
  as explanatory residuals, never as enum members.

A future PR that needs any of these must declare its own chain
position and origin law.

## §11 Deferred residuals (carried explicitly by PR-21M)

| Name                                              | Note                                                      |
|---------------------------------------------------|-----------------------------------------------------------|
| `MANAT_NOT_TANZIL`                                | ManatCandidate is locus identification, not presentation. |
| `TAHQIQ_FINAL_DEFERRED`                           | Final tahqīq verification is deferred beyond PR-21M.      |
| `TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW`          | Awaits docs/45 / PR-D9 Tanzīl Presentation Boundary Law.  |
| `REALITY_APPLICATION_DEFERRED`                    | Reality application is not manāṭ.                         |
| `NO_PREVENTER_CHECK_DEFERRED`                     | Conditions/preventers checked only at tahqīq time.        |
| `EXTERNAL_EXECUTION_FORBIDDEN`                    | No external action at the manāṭ boundary.                 |

All deferred residuals MUST carry `visibility = EXPLANATORY` when
emitted on a `ManatCandidate`; emitting any of them with hidden
or blocking visibility is `HIDDEN_RESIDUAL` / `BLOCKING_RESIDUAL_PRESENT`.

## §12 Required input boundary for PR-21M (مدخلات)

```text
1. hukm_verdict: HukmVerdict — must be in state PROVEN.
2. manat_mode: ManatMode — must be one of
   TAKHRIJ_CANDIDATE | TANQIH_CANDIDATE | TAHQIQ_READINESS_ONLY.
3. manat_description: str — non-empty, non-whitespace.
4. effective_attribute_candidate: str — non-empty, non-whitespace.
5. manat_evidence: str — non-empty, non-whitespace.
6. manat_domain: str — non-empty, non-whitespace.
7. closure_scope: str — non-empty, non-whitespace.
8. No hidden or blocking residuals on any input.
9. Rank must not exceed MANAT_RANK_CEILING.
```

## §13 Derivation prohibition (ممنوعات الاشتقاق)

```text
ManatCandidate must NOT be derived from:
  * IfadahVerdict directly (must go through HukmVerdict).
  * RelationClosureVerdict directly (must go through HukmVerdict).
  * MufradDalalahClosureVerdict directly (must go through HukmVerdict).
  * FormalStyleVerdict directly (must go through HukmVerdict).
  * Any pre-hukm carrier directly.

The only legal derivation path:
  HukmVerdict (PROVEN) → prove_manat_candidate() → ManatCandidate
```

Any shortcut that bypasses the HukmCandidate layer is a
`FORBIDDEN_LEAP` regardless of CI status.
