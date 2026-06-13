# 37 — Maqām / Context Boundary Readiness Law

> PR-D1.2 binding.
> Origin: PR-D1 (Mufrad Semantic Slot Geometry) prerequisite +
> Amendment-11 (chain insertion).
> Ratified by: PR-D1.2.

---

## §1 Purpose

This law governs the Maqām/Context Boundary Readiness layer. The
layer establishes the constitutional boundary constraints that make
dalālah operations (mutābaqah/taḍammun/iltizām) *bounded* — domain of
usage, wadʿ scope constraint, discourse register, technical domain,
qarīnah readiness, blocker audit, and literal domain constraint —
without performing any dalālah operation.

Maqām/Context Boundary Readiness is **not dalālah**.

The governing principle:

```text
لا مطابقة قبل حدود المقام والسياق.
لا تضمن قبل كل مقيد بمجال.
لا التزام قبل علاقة لزوم مقيدة بسياق.
لا مجاز قبل محاولة حقيقة.
لا منقول قبل بوابة نقل.
لا قصد متكلم قبل إفادة ومنطوق.

No Mutābaqah before Maqām/ContextBoundary.
No Taḍammun before Maqām-bounded whole/part frame.
No Iltizām before Context-bounded NecessaryRelation.
No Majāz before HaqīqahAttempt.
No Manqūl before TransferGate.
No SpeakerIntent before Ifādah/Manṭūq layer.
```

---

## §2 Governing invariants

```text
MaqamContextBoundary ≠ Meaning.
MaqamContextBoundary ≠ Dalālah.
MaqamContextBoundary ≠ Ifādah.
MaqamContextBoundary ≠ SpeakerIntent.
MaqamContextBoundary ≠ Majāz.
MaqamContextBoundary ≠ Manqūl.
MaqamContextBoundary ≠ Hukm.
MaqamContextBoundary ≠ Tanzīl.
MaqamContextBoundary ≠ Mutābaqah.
MaqamContextBoundary ≠ Taḍammun.
MaqamContextBoundary ≠ Iltizām.
DiscourseDomainCandidate ≠ semantic content.
UsageRegisterCandidate ≠ meaning determination.
TechnicalDomainCandidate ≠ technical definition.
QarinaReadiness ≠ qarīnah application.
BlockerCandidateSet ≠ blocker verdict.
LiteralDomainConstraint ≠ ḥaqīqah verdict.
WadScopeConstraint ≠ wadʿ assignment.
```

---

## §3 Prerequisite

PR-D1.2 consumes:

1. `SemanticSlotFrame` from PR-D1 (proven semantic slot geometry).
2. `MufradSemanticSlotGeometryVerdict` with state PROVEN.
3. Rank / residual / trace governance from prior layers.

PR-D1.2 must not consume or produce meaning, dalālah operations
(mutābaqah/taḍammun/iltizām), ifādah, hukm, manṭūq, mafhūm, majāz
operation, manqūl operation, speaker intent, or any semantic content.
It produces only boundary readiness — the constraints that bound the
domain in which dalālah operations will later operate.

---

## §4 Euclidean proof of necessity

### §4.1 Mutābaqah requires Maqām

Correspondence (mutābaqah) is not:

```text
signifier ↔ meaning
```

It is:

```text
signifier within wadʿ domain
+ maqām of usage
+ context constraints
→ correspondence candidate
```

A word like "al-ṣalāh" cannot open a single correspondence without
maqām: linguistically it is "supplication"; legally it is "the
designated worship"; customarily it is "a known devotional act". To
open PR-D2 without maqām/context is to force either an arbitrary
choice or unbounded correspondence — both Euclidean violations.

### §4.2 Taḍammun requires bounded whole

Inclusion (taḍammun) decomposes a whole into parts. But parts differ
by domain: "insān" in a logical domain has genus + differentia; in a
customary domain has "living being + human attributes"; in a legal
domain opens capacity and responsibility slots. No part decomposition
without knowing which domain defines the whole.

### §4.3 Iltizām requires bounded necessity

Entailment (iltizām) establishes necessary relations. But necessity
is domain-relative: it may be linguistic, rational, customary, legal,
technical, or contextual. "al-amr" in a legal context may open
obligation; in a threat context it does not; in a guidance context
it opens recommendation only. Without maqām/context, iltizām becomes
"free inference" — constitutionally forbidden.

---

## §5 Maqām/Context Boundary structure

### §5.1 MaqamContextFrame

The constitutional frame for maqām/context boundary readiness.

Required fields:

| Field | Constraint |
|-------|-----------|
| semantic_slot_frame_ref | Non-empty — SemanticSlotFrame trace |
| discourse_domain | DiscourseDomainCandidate |
| usage_register | UsageRegisterCandidate |
| technical_domain | TechnicalDomainCandidate |
| speaker_position | str — non-empty, readiness only |
| addressee_position | str — non-empty, readiness only |
| textual_context_window | str — non-empty, readiness only |
| qarina_readiness | QarinaReadinessCarrier |
| blocker_candidate_set | BlockerCandidateSet |
| literal_domain_constraint | LiteralDomainConstraint |
| wad_scope_constraint | WadScopeConstraint |
| style_relevance_constraint | str — non-empty, readiness only |
| rank | Rank ≤ SEMANTIC_SLOT_GEOMETRY_RANK_CEILING |
| residuals | tuple[Residual, ...] — all visible, all EXPLANATORY |
| trace_ref | str — non-empty |

### §5.2 DiscourseDomainCandidate

Classifies the discourse domain without determining meaning.

| Field | Constraint |
|-------|-----------|
| domain_type | DiscourseDomainType |
| evidence_ref | str — non-empty |
| rank | Rank ≤ SEMANTIC_SLOT_GEOMETRY_RANK_CEILING |
| trace_ref | str — non-empty |

### §5.3 UsageRegisterCandidate

Classifies the register of usage without determining meaning.

| Field | Constraint |
|-------|-----------|
| register_type | UsageRegisterType |
| evidence_ref | str — non-empty |
| trace_ref | str — non-empty |

### §5.4 TechnicalDomainCandidate

Marks whether the unit belongs to a technical domain.

| Field | Constraint |
|-------|-----------|
| domain_name | str — non-empty (domain name or "NONE") |
| is_technical | bool |
| evidence_ref | str — non-empty |
| trace_ref | str — non-empty |

### §5.5 QarinaReadinessCarrier

Readiness for qarīnah (contextual indicator) — not the qarīnah itself.

| Field | Constraint |
|-------|-----------|
| has_potential_qarina | bool |
| qarina_type_readiness | str — non-empty |
| blocks_literal | bool |
| evidence_ref | str — non-empty |
| trace_ref | str — non-empty |

### §5.6 BlockerCandidateSet

Candidate set of potential blockers (mawāniʿ) — not verdicts.

| Field | Constraint |
|-------|-----------|
| blocker_count | int ≥ 0 |
| blocker_types | tuple[str, ...] — type names |
| all_audited | bool |
| evidence_ref | str — non-empty |
| trace_ref | str — non-empty |

### §5.7 LiteralDomainConstraint

Constraint on literal (ḥaqīqah) domain — not a verdict.

| Field | Constraint |
|-------|-----------|
| constraint_type | LiteralConstraintType |
| domain_ref | str — non-empty |
| evidence_ref | str — non-empty |
| trace_ref | str — non-empty |

### §5.8 WadScopeConstraint

Constraint on wadʿ scope — narrower than origin domain.

| Field | Constraint |
|-------|-----------|
| scope_type | WadScopeType |
| narrowing_evidence | str — non-empty |
| evidence_ref | str — non-empty |
| trace_ref | str — non-empty |

---

## §6 prove_maqam_context_boundary() operation

A **pure function** that:

1. Validates SemanticSlotFrame input (type, PROVEN state).
2. Validates all sub-carrier inputs.
3. Bounds rank via `RankLattice.meet(Rank.CANDIDATE, SEMANTIC_SLOT_GEOMETRY_RANK_CEILING)`.
4. Builds deferred residuals (§7).
5. Refuses if any residual is HIDDEN_FORBIDDEN or BLOCKING.
6. Constructs all sub-carriers.
7. Constructs MaqamContextFrame.
8. Returns MaqamContextBoundaryVerdict (PROVEN or REFUSED).

---

## §7 Required deferred residuals

Every MaqamContextFrame must carry:

```text
MAQAM_CONTEXT_BOUNDARY_NOT_DALALAH
MUTABAQAH_DEFERRED_TO_PR_D2
TADAMMUN_DEFERRED_TO_PR_D2
ILTIZAM_DEFERRED_TO_PR_D2
MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3
IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE
MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT
MANQUL_DEFERRED_UNTIL_TRANSFER_GATE
SPEAKER_INTENT_DEFERRED_UNTIL_IFADAH
QARINA_APPLICATION_DEFERRED
BLOCKER_VERDICT_DEFERRED
```

All must be EXPLANATORY and visible.

---

## §8 Forbidden outputs

PR-D1.2 must not produce, export, or instantiate:

- MutābaqahCandidate
- TaḍammunCandidate
- IltizāmCandidate
- IfādahCandidate
- HukmCandidate
- Meaning
- Dalālah (as operation)
- ManṭūqClosure
- MafhūmCandidate
- Majāz (as operation)
- Manqūl (as operation)
- Truth value
- Semantic assertion
- Reality / Tanzil
- Speaker intent determination
- Qarīnah application / verdict
- Blocker verdict
- Lexical semantic content
- Dictionary definition

---

## §9 Constitutional transition law

```text
No Mutābaqah without MaqamContextBoundary.
No Taḍammun without Maqām-bounded whole.
No Iltizām without Context-bounded NecessaryRelation.
No MaqamContextFrame without SemanticSlotFrame.
No MaqamContextFrame without discourse domain.
No MaqamContextFrame without usage register.
No MaqamContextFrame without blocker audit.
No MaqamContextFrame without literal domain constraint.
No MaqamContextFrame without wadʿ scope constraint.
No qarīnah application without qarīnah readiness.
No blocker verdict without blocker audit.
```

---

## §10 Chain position

```text
Previous required: PR-D1 (Mufrad Semantic Slot Geometry) + PR-D1.1.
Current step: PR-D1.2.
Next permitted: PR-D2 — Mutābaqah/Taḍammun/Iltizām Candidate.
PR-D2 is forbidden before PR-D1.2.
PR-D3 is forbidden before PR-D2.
PR-20 is forbidden before PR-D3 + PR-D4.
```

MaqamContextFrame opens PR-D2 readiness only.
MaqamContextFrame does not open dalālah operations.
MaqamContextFrame does not open Ifādah.

---

## §11 Governing chain law

```text
لا مطابقة قبل خانات.
ولا خانات قبل استمرار هوية.
ولا تشغيل للخانات قبل حدود مقام وسياق.
ولا دلالة قبل مقام مضبوط.

No Mutābaqah before slots.
No slots before identity continuity.
No slot activation before maqām/context boundaries.
No dalālah before bounded maqām.

المطابقة تحتاج خانات.
الخانات تحتاج استمرار هوية.
واستمرار الهوية يحتاج مقامًا وسياقًا حتى لا تتحول الخانات إلى معنى
مطلق بلا مجال.
```
