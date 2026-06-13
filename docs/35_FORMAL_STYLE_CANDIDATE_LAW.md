# 35 — Formal Style Candidate Law

> PR-F8 binding.
> Origin: docs/34 (FormalShapeClosure.CLOSED prerequisite).
> Ratified by: PR-F8.

---

## §1 Purpose

This law governs the formal style classification layer. Formal style
classifies **how** a closed composition pattern is structurally used
(khabar/inshāʾ and sub-families) without interpreting **why** or
**what** it communicates.

Formal style is **not meaning**.

---

## §2 Governing invariants

```text
FORMAL_STYLE ≠ meaning.
FORMAL_STYLE ≠ dalālah.
FORMAL_STYLE ≠ ifādah.
KHABAR_STYLE_FORM ≠ truth.
KHABAR_STYLE_FORM ≠ assertion.
KHABAR_STYLE_FORM ≠ proposition.
INSHA_STYLE_FORM ≠ speaker intent.
COMMAND_STYLE_FORM ≠ obligation.
PROHIBITION_STYLE_FORM ≠ prohibition reality.
INTERROGATIVE_STYLE_FORM ≠ request for answer.
VOCATIVE_STYLE_FORM ≠ real addressee.
WISH_STYLE_FORM ≠ psychological wish.
HOPE_STYLE_FORM ≠ expectation.
OATH_STYLE_FORM ≠ truth guarantee.
CONDITION_STYLE_FORM ≠ conditional truth.
EXCLAMATION_STYLE_FORM ≠ real emotion.
```

---

## §3 Prerequisite

PR-F8 consumes only:

1. `FormalShapeClosure.CLOSED` (the closed formal shape profile).
2. Composition pattern evidence (a reference to a proved composition).
3. Rank / residual / trace governance.

PR-F8 must not consume or produce meaning, dalālah, ifādah, hukm,
manṭūq, mafhūm, majāz, manqūl, or any semantic content.

---

## §4 Formal style families (closed set)

```text
1.  DECLARATIVE_STYLE_FORM   (khabar)
2.  COMMAND_STYLE_FORM        (amr)
3.  PROHIBITION_STYLE_FORM    (nahy)
4.  INTERROGATIVE_STYLE_FORM  (istifham)
5.  VOCATIVE_STYLE_FORM       (nida')
6.  WISH_STYLE_FORM           (tamanni)
7.  HOPE_STYLE_FORM           (taraji)
8.  OATH_STYLE_FORM           (qasam)
9.  CONDITION_STYLE_FORM      (shart)
10. EXCLAMATION_STYLE_FORM    (ta'ajjub)
```

Each family is a formal structural classification only.

---

## §5 FormalStyleCandidate carrier

The `FormalStyleCandidate` is a frozen, immutable carrier that proves:

- A composition pattern has been formally classified by style.
- The classification is structural only.
- No meaning, truth, intent, or semantic content is carried.

Required fields:

| Field | Type | Constraint |
|-------|------|-----------|
| style_family | FormalStyleFamily | Must be a valid member |
| composition_evidence_ref | str | Non-empty |
| formal_closure_ref | str | Non-empty |
| definition_text | str | Non-empty, no meaning language |
| distinguishing_evidence | str | Non-empty |
| boundary_conditions | tuple[str, ...] | Non-empty |
| exclusion_conditions | tuple[str, ...] | May be empty tuple |
| rank | Rank | ≤ FORMAL_SHAPE_RANK_CEILING |
| residuals | tuple[Residual, ...] | All visible, all EXPLANATORY |
| trace_ref | str | Non-empty |

---

## §6 prove_formal_style_candidate() operation

A **pure function** that:

1. Validates all inputs.
2. Requires `FormalShapeClosure.CLOSED`.
3. Bounds rank via `RankLattice.meet(Rank.CANDIDATE, FORMAL_SHAPE_RANK_CEILING)`.
4. Builds deferred residuals (§7).
5. Refuses if any residual is HIDDEN_FORBIDDEN or BLOCKING.
6. Constructs `FormalStyleCandidate` on success.
7. Returns `FormalStyleVerdict` (PROVEN or REFUSED).

---

## §7 Required deferred residuals

Every `FormalStyleCandidate` must carry:

```text
DALALAH_DEFERRED_TO_PR_D1
MUFRAD_SEMANTIC_SLOT_GEOMETRY_DEFERRED_TO_PR_D1
IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE
MANTUQ_DEFERRED_UNTIL_IFADAH
MAFHUM_DEFERRED_UNTIL_MANTUQ
MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT
MANQUL_DEFERRED_UNTIL_TRANSFER_GATE
```

All must be EXPLANATORY and visible.

---

## §8 Forbidden outputs

PR-F8 must not produce, export, or instantiate:

- Meaning
- Dalālah
- IfādahCandidate
- HukmCandidate
- ManṭūqClosure
- MafhūmCandidate
- Majāz
- Manqūl
- Truth value
- Speaker intent
- Semantic assertion
- Reality / Tanzil
- Lexical semantic content

---

## §9 Chain position

```text
Previous required: PR-F7.1 / Amendment-10.
Current step: PR-F8.
Next permitted: PR-D1 — Mufrad Semantic Slot Geometry.
PR-20 is forbidden before PR-D1, PR-D2, PR-D3, and PR-D4.
```

FormalStyleCandidate opens PR-D1 readiness only.
FormalStyleCandidate does not open Ifādah.

---

## §10 Important distinction

PR-F8 classifies the formal style of a closed composition pattern.
It does **not** interpret why that style is used. Therefore:

- Interrogative form is not rhetorical question.
- Command form is not obligation.
- Prohibition form is not legal forbiddance.
- Khabar form is not truth.
- Inshāʾ form is not speaker intent.

---

## §11 Governing chain law

```text
لا دلالة قبل الشكل.
ولا مطابقة قبل خانات المدلول المفرد.
ولا تضمن قبل المطابقة.
ولا التزام قبل علاقة لازمة مرخصة.
ولا إفادة قبل إغلاق دلالة المفرد والعلاقة.
```

No dalālah before formal shape.
No correspondence before mufrad dalālah slots.
No inclusion before correspondence.
No entailment before licensed necessary relation.
No ifādah before mufrad dalālah closure and relation closure.
