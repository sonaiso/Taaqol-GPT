# 39 — Mufrad Dalālah Closure Law

> PR-D3 binding.
> Origin: PR-D2 (Mutābaqah/Taḍammun/Iltizām Candidate) prerequisite.
> Ratified by: PR-D3.

---

## §1 Purpose

This law governs the Mufrad Dalālah Closure layer. The layer proves
that the minimum complete singular dalālah is formally closed as a
**candidate** — sufficient for later HaqīqahAttempt, Majāz, Naql,
and composition gates, but never producing meaning itself.

The governing principle:

```text
لا حقيقة ولا مجاز ولا مفهوم ولا إفادة ولا حكم قبل دلالة مفردة مكتملة بالحد الأدنى.
والحد الأدنى للدلالة المفردة هو مطابقة تحفظ الكل، وتضمن يحفظ الداخل، والتزام يحفظ اللازم، ومقام يحد العلاقة، وهوية محفوظة بين الجميع.

No Haqīqah, no Majāz, no Mafhūm, no Ifādah, no Hukm before minimum
complete mufrad dalālah.
The minimum for mufrad dalālah is: Mutābaqah preserving the whole,
Taḍammun preserving the interior, Iltizām preserving the necessary,
Maqām bounding the relation, and identity preserved across all.
```

---

## §2 Governing invariants

```text
MufradDalālahClosureCandidate ≠ Meaning.
MufradDalālahClosureCandidate ≠ FinalMeaning.
MufradDalālahClosureCandidate ≠ Ifādah.
MufradDalālahClosureCandidate ≠ Hukm.
MufradDalālahClosureCandidate ≠ Tanzīl.
MufradDalālahClosureCandidate ≠ MafhūmCandidate.
MufradDalālahClosureCandidate ≠ ManṭūqClosure.
MufradDalālahClosureCandidate ≠ MajāzVerdict.
MufradDalālahClosureCandidate ≠ MajāzLicense.
MufradDalālahClosureCandidate ≠ ManqūlVerdict.
MufradDalālahClosureCandidate ≠ ManqūlLicense.
MufradDalālahClosureCandidate ≠ HaqīqahAttemptVerdict.
MufradDalālahClosureCandidate ≠ SpeakerIntentVerdict.
MufradDalālahClosureCandidate ≠ OntologicalClaim.
MufradDalālahClosureCandidate ≠ FreeReasoning.
MufradDalālahClosureCandidate ≠ QiyāsResult.
No closure without Mutābaqah + Taḍammun + Iltizām.
No closure without SemanticSlotFrame proven.
No closure without MaqamContextFrame proven.
No closure without identity continuity across all layers.
No closure with hidden or blocking residuals.
No rank promotion beyond DALALAH_CANDIDATE_RANK_CEILING.
```

---

## §3 Prerequisites

PR-D3 consumes **all three** proven verdicts:

1. `MufradSemanticSlotGeometryVerdict` (PROVEN) — SemanticSlotFrame.
2. `MaqamContextBoundaryVerdict` (PROVEN) — MaqamContextFrame.
3. `DalalahCandidateVerdict` (PROVEN) — MutabaqahCandidate +
   TadammunCandidate + IltizamCandidate.

PR-D3 must not consume or produce:
- Final meaning
- Ifādah (proposition)
- Hukm (judgment)
- Tanzīl (application)
- Mafhūm (concept extraction)
- Majāz verdict or license
- Manqūl verdict or license
- HaqīqahAttempt verdict
- SpeakerIntent verdict
- Ontological claim
- Free reasoning
- Qiyās result

---

## §4 Structure

### §4.1 MufradDalālahClosureCandidate

The output carrier proving minimum complete mufrad dalālah:

| Field | Type | Invariant |
|-------|------|-----------|
| semantic_slot_frame_ref | str | references SemanticSlotFrame.trace_ref |
| maqam_context_frame_ref | str | references MaqamContextFrame.trace_ref |
| mutabaqah_ref | str | references MutabaqahCandidate.trace_ref |
| tadammun_ref | str | references TadammunCandidate.trace_ref |
| iltizam_ref | str | references IltizamCandidate.trace_ref |
| dal_identity_ref | str | preserved dal identity (from SemanticSlotFrame) |
| closure_scope | str | non-empty scope bounding the closure |
| rank | Rank | ≤ DALALAH_CANDIDATE_RANK_CEILING |
| residuals | tuple[Residual, ...] | all visible, no HIDDEN_FORBIDDEN/BLOCKING |
| trace_ref | str | non-empty trace reference |

### §4.2 MufradDalalahClosureState

```text
PROVEN  — minimum complete closure proven.
REFUSED — closure refused with named FailureCode.
```

### §4.3 MufradDalalahClosureVerdict

| Field | Type |
|-------|------|
| candidate | MufradDalālahClosureCandidate or None |
| verdict_state | MufradDalalahClosureState |
| failure_code | FailureCode or None |
| verdict_rank | Rank |
| residuals | tuple[Residual, ...] |
| trace_ref | str |

---

## §5 Required checks

The `prove_mufrad_dalalah_closure()` operation must verify:

1. semantic_slot_verdict is PROVEN.
2. maqam_context_verdict is PROVEN.
3. dalalah_candidate_verdict is PROVEN.
4. semantic_slot_verdict.candidate is SemanticSlotFrame.
5. maqam_context_verdict.candidate is MaqamContextFrame.
6. dalalah_candidate_verdict has mutabaqah, tadammun, and iltizam.
7. maqam_context_verdict.candidate.semantic_slot_frame_ref ==
   semantic_slot_verdict.candidate.trace_ref (identity continuity).
8. dalalah_candidate_verdict.mutabaqah.semantic_slot_frame_ref ==
   semantic_slot_verdict.candidate.trace_ref (identity continuity).
9. dalalah_candidate_verdict.mutabaqah.maqam_context_frame_ref ==
   maqam_context_verdict.candidate.trace_ref (identity continuity).
10. dalalah_candidate_verdict.tadammun.mutabaqah_ref ==
    dalalah_candidate_verdict.mutabaqah.trace_ref (structural integrity).
11. dalalah_candidate_verdict.iltizam.mutabaqah_ref ==
    dalalah_candidate_verdict.mutabaqah.trace_ref (structural integrity).
12. closure_scope is non-empty.
13. No HIDDEN_FORBIDDEN residual.
14. No BLOCKING residual.
15. Rank never exceeds DALALAH_CANDIDATE_RANK_CEILING.

---

## §6 Failure taxonomy

| Condition | FailureCode |
|-----------|-------------|
| Any identity link fails | IDENTITY_BROKEN |
| Any required proven verdict missing / wrong type | GATE_REQUIRED |
| closure_scope empty | REQUIRED_SLOT_EMPTY |
| Hidden residual appears | HIDDEN_RESIDUAL |
| Blocking residual appears | BLOCKING_RESIDUAL_PRESENT |
| Rank exceeds ceiling | RANK_EXCEEDS_CEILING |

---

## §7 Deferred residuals

```text
MUFRAD_DALALAH_CLOSURE_NOT_MEANING
    — closure proves completeness, not meaning.
HAQIQAH_ATTEMPT_DEFERRED_TO_POST_CLOSURE
    — haqiqah attempt is a later gate.
MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT
    — majaz is a later gate.
MANQUL_DEFERRED_UNTIL_TRANSFER_GATE
    — manqul is a later gate.
IFADAH_DEFERRED_UNTIL_RELATION_CLOSURE
    — ifadah requires relation closure (PR-D4) first.
HUKM_DEFERRED_UNTIL_IFADAH
    — hukm requires ifadah first.
MAFHUM_DEFERRED_UNTIL_MANTUQ
    — mafhum requires mantuq first.
```

All deferred residuals are `EXPLANATORY`, `visible=True`.

---

## §8 Forbidden outputs

PR-D3 must never export, instantiate, or return:

```text
Meaning, FinalMeaning, IfadahCandidate, HukmCandidate,
TanzilCandidate, MantuqClosure, MafhumCandidate, MajazVerdict,
MajazLicense, ManqulVerdict, ManqulLicense, SpeakerIntentVerdict,
HaqiqahAttemptVerdict, OntologicalClaim, FreeReasoning, QiyasResult.
```

---

## §9 Rank ceiling

```text
MUFRAD_DALALAH_CLOSURE_RANK_CEILING = DALALAH_CANDIDATE_RANK_CEILING
```

The closure layer inherits its ceiling from the dalalah candidate
layer. No rank promotion occurs within the closure operation.

---

## §10 Constitutional transition

```text
PR-D3 output (MufradDalālahClosureCandidate) is the prerequisite for:
- PR-D4 (RelationClosure)
- PR-20 (IfādahCandidate) — only after both PR-D3 and PR-D4 close.

PR-D3 does not open:
- HaqīqahAttempt
- Majāz
- Naql
- Composition closure
- Ifādah
- Hukm
```

---

## §11 Chain position

```text
PR-D3
    Origin   : PR-D2 prerequisite.
    Output   : MufradDalālahClosure — proves that singular
               dalālah candidates are formally closed as
               candidates. Does not produce meaning.
    Forbidden: ifādah; hukm; reality; tanzil; ontology;
               adapter or audit changes; new runtime dependencies.
    Binding  : No IfādahCandidate before this closes.
    Law      : MufradDalālahClosure ≠ Meaning.
               MufradDalālahClosure ≠ Ifādah.
```
