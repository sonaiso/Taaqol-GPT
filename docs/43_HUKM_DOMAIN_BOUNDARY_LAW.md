# 43 — Hukm Domain Boundary Law

> **Status:** Constitutional law. Ratified by PR-D7 (law only — no
> code). Binds every later PR that constructs, processes, or consumes
> a `HukmCandidate` — most directly PR-21 (HukmCandidate code),
> and transitively PR-D8/PR-21M (Manāṭ), PR-D9/PR-22 (Tanzīl),
> PR-22-AUDIT, and PR-D10 (Vertical Path Closure). It is load-bearing.
>
> This document is **law only**. It ships no carrier, no operation,
> no enum, no test, and no runtime change. Any attempt to import a
> `HukmCandidate`, a `HukmVerdict`, a `HukmState`, an
> `EvaluationDomain`, or a `prove_hukm_candidate()` symbol before
> PR-21 (the code PR) is merged is a `FORBIDDEN_LEAP` regardless of
> CI status.

## §1 Governing principle (ما يحفظ — what it preserves)

```text
No HukmCandidate without a PROVEN IfadahVerdict.
No HukmCandidate without a declared EvaluationDomain.
No HukmCandidate without a hukm_claim.
No HukmCandidate without hukm_evidence.
No HukmCandidate without a maqām (hukm_maqam or proven maqām verdict).
No HukmCandidate that produces authority, enforcement, or execution.
No HukmCandidate that produces a tanzīl, a manāṭ verdict, a reality
   application, a legal binding, or a fatwa.
No HukmCandidate is a certificate; it remains a candidate forever.
NORMATIVE must appear only as NORMATIVE_CANDIDATE.
Dropping _CANDIDATE is AUTHORITY_LEAK.
```

`HukmCandidate` proves that a closed ifādah (speech-level closure) has
been **evaluated** inside a single declared domain with explicit evidence.
It does not determine final authority, reality, enforcement, or meaning.

The constitutional distinction preserved by this law:

```text
IfādahCandidate  (what the closed relation declares — PR-20)
HukmCandidate    (what evaluation says about that declaration
                  inside a bounded domain — PR-21)
ManāṭCandidate   (where reality meets the judgment — PR-21M)
TanzīlCandidate  (how the judgment is presented/applied — PR-22)
```

None of the four can substitute for any other. Hukm is the boundary
at which an IfādahCandidate is evaluated, never the point at which
authority is exercised or reality is verified.

## §2 What this law opens

```text
PR-21 — HukmCandidate (code).
        Carriers: HukmCandidate, HukmVerdict, HukmState,
                  EvaluationDomain (minimal:
                  LINGUISTIC | LOGICAL | NORMATIVE_CANDIDATE),
                  HUKM_RANK_CEILING, prove_hukm_candidate().
        An AST-level guard test asserting no module under
        taaqqul_slot_geometry defines the bare name `NORMATIVE`
        (alias-drop guard).
        Nothing else.
```

PR-21 is the **only** PR licensed by docs/43. It produces a
candidate carrier, never authority and never reality.

The enum surface in PR-21 must use ASCII transliterations without
diacritics (`LINGUISTIC`, `LOGICAL`, `NORMATIVE_CANDIDATE`). Arabic
prose may still write *حكم*; the code identifier is `HukmCandidate`.

## §3 What this law forbids

```text
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
No OntologicalClaim.
No AuthorityClaim.
No NormativeJudgment / NORMATIVE (without _CANDIDATE suffix).
No external execution / enforcement / tool action.
No legal, religious, or normative authority claim.
No SHARI_FINAL.
No LEGAL_AUTHORITY.
No FATWA.
No QADA.
No EXECUTION.
No DIVINE_AUTHORITY_CLAIM.
No REALITY_APPLICATION.
No re-export, alias, or string representation that drops the
   "Candidate" suffix from any Hukm-layer carrier.
No re-export, alias, or string representation that drops the
   "_CANDIDATE" suffix from NORMATIVE_CANDIDATE.
No synthesis of a missing IfadahVerdict.
No coercion of a free-text evaluation domain into a domain object.
No silent fallback for any refusal.
```

PR-21 ships none of these. Any future PR that ships any one of
them must declare its own origin law and its own chain position.

## §4 Domain (المجال — where this law applies)

```text
Evaluation of speech-level closure at the boundary between
IfādahCandidate (PR-20) and ManāṭCandidate (PR-D8 + PR-21M).
It binds:

  * PR-21 (HukmCandidate code).
  * PR-D8 / PR-21M (Manāṭ) — Manāṭ consumes a HukmCandidate, but
    may never recompute one.
  * PR-22 (Tanzīl) — Tanzīl consumes the full chain including
    HukmCandidate, never produces a new one.
  * PR-22-AUDIT — AnswerAudit may surface a HukmCandidate inside
    an AuditedAnswer only as a candidate, never as authority.

It does not bind:
  * Core kernel (core/) — Hukm is not a SlotGraph property.
  * Adapter layer (audit/) — adapters never produce Hukm.
  * Any horizontal branch (majāz, mantūq, mafhūm, naql, GPT-proposer,
    reference expansion, conditions DAG) — these are forbidden
    before docs/46 (PR-D10) closes the vertical path.
```

## §5 Evidence (الدليل — what justifies this boundary)

1. **docs/41 §1 (Ifādah Boundary Law)**: IfādahCandidate explicitly
   states "No IfādahCandidate that produces a hukm." The boundary
   must therefore be erected *outside* PR-20.
2. **docs/41 §10 deferred-residual table**: The residual
   `HUKM_DEFERRED_UNTIL_HUKM_DOMAIN_LAW` names this very document
   (docs/43) as its closing reference. PR-21 may consume that
   residual; no other PR may.
3. **Forbidden Straight-Line Registry (docs/05, PR-5)**: The lines
   `Candidate → Certificate`, `Evidence → Certainty`, and
   `Judgment → Authority` are constitutionally forbidden. Hukm
   sits on exactly those forbidden lines; only an explicit boundary
   law can prevent the leap from candidate judgment to final
   authority.
4. **PR-D4 and PR-20 forbidden surfaces**: Both explicitly forbid
   exporting `HukmCandidate`. The boundary must be erected before
   any code attempts to produce one.
5. **The governing sentence**: الإفادة لا تحكم بذاتها — speech-level
   closure does not judge by itself; it requires an evaluation
   domain and evidence. Without this boundary, the leap
   Ifādah → Authority is constitutionally unguarded.

## §6 Minimal EvaluationDomain (binding on PR-21)

PR-21 must declare `EvaluationDomain` with **exactly** the following
minimal members:

```text
LINGUISTIC
    The hukm evaluates the ifādah qua linguistic structure
    (e.g. grammatical correctness, stylistic appropriateness,
    lexical precision). Domain evidence is linguistic.

LOGICAL
    The hukm evaluates the ifādah qua logical form
    (e.g. internal consistency, inferential validity,
    contradictions). Domain evidence is logical.

NORMATIVE_CANDIDATE
    The hukm evaluates the ifādah qua normative bearing
    (e.g. ḥalāl/ḥarām candidacy, obligation/prohibition
    candidacy, recommended/reprehensible candidacy). The
    result is always a candidate — never a binding ruling,
    fatwa, qaḍāʾ, or authority claim.
```

### §6.1 Forbidden domain names

PR-21 **must not** define, alias, import, or reference any of:

```text
NORMATIVE           (bare — without _CANDIDATE)
SHARI_FINAL
LEGAL_AUTHORITY
FATWA
QADA
EXECUTION
DIVINE_AUTHORITY_CLAIM
REALITY_APPLICATION
ONTOLOGICAL
METAPHYSICAL_TRUTH
```

A future PR that needs a domain from this list must declare its own
chain position, its own origin law, and must not appear before PR-D10
(Vertical Path Closure).

### §6.2 AST alias-drop guard (binding on PR-21)

PR-21 must ship an AST-level test that:

1. Scans every `.py` file under `src/taaqqul_slot_geometry/`.
2. Asserts that no public symbol (class, function, constant, enum
   member) uses the bare name `NORMATIVE` — only
   `NORMATIVE_CANDIDATE` is permitted.
3. Fails with an explicit message if a bare `NORMATIVE` is found.

This guard is constitutional; it is not merely a lint preference.
Removing or weakening it is a `FORBIDDEN_LEAP`.

## §7 Failure surface (الفشل — named refusals)

`prove_hukm_candidate()` must refuse with one of these labels; no
silent `None`, no bare exception:

```text
NO_IFADAH
    The ifadah_verdict is missing, malformed, not an
    IfadahVerdict, or not in state PROVEN.

NO_EVALUATION_DOMAIN
    The evaluation_domain is missing, not a member of
    EvaluationDomain, or is a forbidden domain name (§6.1).

NO_HUKM_CLAIM
    hukm_claim is empty or whitespace-only.

NO_HUKM_EVIDENCE
    hukm_evidence is empty or whitespace-only.

NO_HUKM_MAQAM
    hukm_maqam is missing and no proven maqām verdict is carried.
    (PR-21 may either accept a separate hukm_maqam string-argument
    or reuse the maqām verdict surface from the input IfadahVerdict;
    but absence of both is a refusal.)

AUTHORITY_LEAK
    Any public symbol, enum member, carrier field, or output surface
    drops the _CANDIDATE suffix from NORMATIVE_CANDIDATE, or claims
    final authority in any form.

DOMAIN_LEAP
    The evaluation_domain is not one of the minimal permitted members
    (LINGUISTIC | LOGICAL | NORMATIVE_CANDIDATE). A leap beyond the
    declared domain surface is a DOMAIN_LEAP, not a silent promotion.

HIDDEN_RESIDUAL
    A residual carried by the input IfadahVerdict or produced by the
    hukm operation is hidden (visibility != EXPLANATORY) at the point
    of consumption or emission.

BLOCKING_RESIDUAL_PRESENT
    A residual carried by any input verdict is in a blocking state.

RANK_EXCEEDS_CEILING
    The meet of input rank against HUKM_RANK_CEILING exceeds the
    ceiling.
```

### §7.1 FailureCode rule

PR-21 must either add dedicated `FailureCode` members for the labels
above, or map these refusals to existing `FailureCode` values with
exact `trace_ref` labels (e.g. `FailureCode.REQUIRED_SLOT_EMPTY` with
`trace_ref="no_hukm_claim"`). Silent fallback — where a refusal
produces no named code and no trace label — is forbidden and is itself
a `FORBIDDEN_LEAP`.

## §8 Effect (الأثر — what changes when this law is ratified)

* PR-21 becomes reviewable. Without docs/43, PR-21 is a
  `FORBIDDEN_LEAP`.
* PR-D8 / PR-21M (Manāṭ) acquire a single legal input shape
  (`HukmVerdict` of state `PROVEN`).
* PR-22-AUDIT acquires a contract: a HukmCandidate may flow into
  an `AuditedAnswer` only as a candidate, bounded by the
  presentation boundary that docs/45 (PR-D9) will erect.
* PR-D10 (docs/46, Vertical Path Closure Law) becomes able to assert
  trace continuity through the Hukm layer.
* The deferred residual `HUKM_DEFERRED_UNTIL_HUKM_DOMAIN_LAW`
  (declared in docs/41 §10) is re-anchored to this law as its closing
  reference. PR-21 may consume that residual; no other PR may.

## §9 Constitutional invariants (binding on PR-21 code)

* `HukmCandidate` ≠ Authority.
* `HukmCandidate` ≠ NormativeJudgment.
* `HukmCandidate` ≠ FinalMeaning.
* `HukmCandidate` ≠ Meaning.
* `HukmCandidate` ≠ Reality.
* `HukmCandidate` ≠ ManāṭCandidate.
* `HukmCandidate` ≠ TanzīlCandidate.
* `HukmCandidate` ≠ PropositionTruthValue.
* `HukmCandidate` ≠ OntologicalClaim.
* `HukmCandidate` ≠ FreeReasoning.
* `HukmCandidate` ≠ Enforcement.
* `HukmCandidate` ≠ Execution.
* No hukm closure without a PROVEN IfadahVerdict.
* No hukm closure without one of the minimal EvaluationDomain members.
* No hukm closure without explicit hukm_claim and hukm_evidence.
* No hukm closure without a maqām (explicit or carried).
* No hukm closure with hidden or blocking residuals.
* No rank promotion beyond `HUKM_RANK_CEILING`.
* All operations are pure: no I/O, no ledger, no network, no
  filesystem, no clock.
* `NORMATIVE_CANDIDATE` only — never bare `NORMATIVE`.

## §10 Forbidden surface (mirror of §3, declared explicitly)

PR-21 (code) **must not** export, define, instantiate, alias, or
reference:

* `ManatCandidate`, `ManatVerdict`, `ManatState`, `ManatMode`
* `TanzilCandidate`, `TanzilVerdict`, `TanzilState`
* `MafhumCandidate`, `MantuqClosure`
* `MajazVerdict`, `MajazLicense`, `ManqulVerdict`, `ManqulLicense`
* `HaqiqahAttemptVerdict`
* `SpeakerIntentVerdict`
* `FinalMeaning`, `Meaning`, `OntologicalClaim`
* `PropositionTruthValue`, `ProofObligation`
* `AuthorityClaim`, `NormativeJudgment`
* `NORMATIVE` (bare — must always be `NORMATIVE_CANDIDATE`)
* `SHARI_FINAL`, `LEGAL_AUTHORITY`, `FATWA`, `QADA`
* `EXECUTION`, `DIVINE_AUTHORITY_CLAIM`, `REALITY_APPLICATION`
* Any `EvaluationDomain` member outside the minimal set
  (`LINGUISTIC`, `LOGICAL`, `NORMATIVE_CANDIDATE`). Extended domains
  are deferred residuals only; PR-21 must carry them as explanatory
  residuals, never as enum members.

A future PR that needs any of these must declare its own chain
position and origin law.

## §11 Deferred residuals (carried explicitly by PR-21)

| Name                                             | Note                                                     |
|--------------------------------------------------|----------------------------------------------------------|
| `HUKM_NOT_AUTHORITY`                             | HukmCandidate is evaluation, not binding authority.      |
| `MANAT_DEFERRED_UNTIL_MANAT_LAW`                 | Awaits docs/44 (PR-D8).                                  |
| `TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW`         | Awaits docs/45 (PR-D9).                                  |
| `MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL`           | Awaits docs/46 (PR-D10) horizontal-branch licence.       |
| `EXTENDED_DOMAIN_DEFERRED`                       | Domains beyond the minimal set — never in PR-21.         |
| `REALITY_VERIFICATION_DEFERRED`                  | Reality check is manāṭ, not hukm.                        |
| `AUDIT_INTEGRATION_DEFERRED_UNTIL_PR_22_AUDIT`   | AnswerAudit bridge ships in PR-22-AUDIT.                 |

All deferred residuals MUST carry `visibility = EXPLANATORY` when
emitted on a `HukmCandidate`; emitting any of them with hidden
or blocking visibility is `HIDDEN_RESIDUAL` / `BLOCKING_RESIDUAL_PRESENT`.

## §12 Required input boundary for PR-21 (مدخلات)

```text
1. ifadah_verdict: IfadahVerdict — must be in state PROVEN.
2. evaluation_domain: EvaluationDomain — must be one of
   LINGUISTIC | LOGICAL | NORMATIVE_CANDIDATE.
3. hukm_claim: str — non-empty, non-whitespace.
4. hukm_evidence: str — non-empty, non-whitespace.
5. hukm_maqam: str — non-empty, OR carried by a proven maqām
   verdict if PR-21 reuses the maqām surface.
6. closure_scope: str — non-empty, non-whitespace.
7. No hidden or blocking residuals on any input.
8. Rank must not exceed HUKM_RANK_CEILING.
```

## §13 Derivation prohibition (ممنوعات الاشتقاق)

```text
HukmCandidate must NOT be derived from:
  * RelationClosureVerdict directly (must go through IfadahVerdict).
  * MufradDalalahClosureVerdict directly (must go through IfadahVerdict).
  * FormalStyleVerdict directly (must go through IfadahVerdict).
  * Any pre-ifādah carrier directly.

The only legal derivation path:
  IfadahVerdict (PROVEN) → prove_hukm_candidate() → HukmCandidate
```

Any shortcut that bypasses the IfādahCandidate layer is a
`FORBIDDEN_LEAP` regardless of CI status.

## §14 Reading order for reviewers of PR-21

```text
1. docs/13 — Constitutional PR Geometry
2. docs/14 — PR Chain Roadmap (PR-D7 and PR-21 appear in Amendment-12)
3. docs/41 — Ifādah Boundary Law (PR-D5)
4. docs/42 — SpeechForce/FormalStyle Bridge Law (PR-D6)
5. docs/43 — this document
6. The PR-21 PR description, checked against (1)–(5).
```

A reviewer who skips (3), (4), or (5) cannot tell whether PR-21 is
a constitutional branch or a leap. CI cannot tell either.

## §15 Governing sentence (الجملة الحاكمة)

```text
الإفادة لا تحكم بذاتها.
والحكم المرشح لا يملك سلطة.
وكل NORMATIVE بلا CANDIDATE هو تسرب سلطة.
```

---

*Ratified by PR-D7 (law only — no code, no carriers, no tests).*
