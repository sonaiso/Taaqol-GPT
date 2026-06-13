# 36 — Mufrad Semantic Slot Geometry Law

> PR-D1 binding.
> Origin: FormalShapeClosure.CLOSED + PR-F8 (FormalStyleCandidate) prerequisite.
> Ratified by: PR-D1.

---

## §1 Purpose

This law governs the mufrad semantic slot geometry layer. Mufrad
semantic slot geometry establishes the constitutional structure that
makes singular dalālah *possible* — identity continuity, wadʿ
evidence, per-unit formal profile closure, kulli/juzʾi axis verdict,
origin/branch geometry, and inter-frame relation readiness — without
performing any dalālah operation.

Mufrad semantic slot geometry is **not dalālah**.

The governing principle:

```text
خانات إمكان الدلالة، لا الدلالة.
Slots for the possibility of dalālah, not dalālah itself.
```

The semantic transition must be Euclidean and organically linked to
DalOnlyCandidate (the signifier alone) and VerbalMadlulCandidate
(the verbal signified), because those are its preconditions — the
origin of the verbal signified and the origin of the signifier alone.

---

## §2 Governing invariants

```text
SemanticSlotFrame ≠ meaning.
SemanticSlotFrame ≠ dalālah operation.
SemanticSlotFrame ≠ Mutābaqah.
SemanticSlotFrame ≠ Taḍammun.
SemanticSlotFrame ≠ Iltizām.
SemanticSlotFrame ≠ ifādah.
WadʿEvidence ≠ lexical meaning.
WadʿEvidence ≠ dictionary definition.
IdentityContinuityProof ≠ semantic assertion.
PerUnitFormalProfileClosure ≠ semantic derivation.
KulliJuzʾiAxisVerdict ≠ ontological claim.
BranchLinkCandidate ≠ qiyās result.
BranchLinkCandidate ≠ free reasoning.
NaqlReadiness ≠ Naql.
MajazReadiness ≠ Majaz.
JāmidAnchorSlot ≠ lexical meaning.
JāmidAnchorSlot = entity anchoring readiness.
MasdarSlot ≠ event occurrence.
MasdarSlot ≠ tense.
MasdarSlot = abstract transformation potential.
MushtaqSlot ≠ real agent.
MushtaqSlot ≠ real patient.
HarfOperatorSlot ≠ semantic relation.
HarfOperatorSlot = licensed relational operator readiness.
ReferenceSlot ≠ resolved referent.
```

---

## §3 Prerequisite

PR-D1 consumes:

1. `FormalStyleCandidate` from PR-F8 (proven formal style classification).
2. `DalOnlyCandidate` from PR-15 (proven signifier standing).
3. `VerbalMadlulCandidate` from PR-16 (proven verbal signified standing).
4. `ContractableUnitGeometry` from PR-18 (proven contractability).
5. `FormalShapeClosure.CLOSED` from the formal shape registry.
6. Rank / residual / trace governance.

PR-D1 must not consume or produce meaning, dalālah operations
(mutābaqah/taḍammun/iltizām), ifādah, hukm, manṭūq, mafhūm, majāz,
manqūl, or any semantic content. It produces only geometry — the
slots that make dalālah possible.

---

## §4 Semantic slot geometry structure

### §4.1 SemanticSlotFrame

The constitutional frame for mufrad dalālah possibility. Every
SemanticSlotFrame must carry an identity center (not synthesised):

```text
identity_claim:
    This signifier (dal), with this verbal signified (madlul lafzi),
    with this closed formal shape, is a candidate for opening
    semantic dalālah slots — never for final meaning.
```

Required fields:

| Field | Constraint |
|-------|-----------|
| dal_identity_ref | Non-empty — DalOnlyCandidate trace |
| verbal_madlul_ref | Non-empty — VerbalMadlulCandidate trace |
| contractable_unit_ref | Non-empty — ContractableUnitGeometry trace |
| formal_shape_ref | Non-empty — FormalShapeClosure trace |
| formal_style_ref | Non-empty — FormalStyleCandidate trace |
| wad_evidence | WadʿEvidenceCarrier |
| per_unit_profile | PerUnitFormalProfileClosure |
| kulli_juzʾi_axis | KulliJuzʾiAxisVerdict |
| branch_link | BranchLinkCandidate |
| naql_readiness | str — readiness carrier, never naql itself |
| majaz_readiness | str — readiness carrier, never majaz itself |
| semantic_category | SemanticCategory — jāmid/maṣdar/mushtaq/ḥarf/reference |
| rank | Rank ≤ FORMAL_SHAPE_RANK_CEILING |
| residuals | tuple[Residual, ...] — all visible, all EXPLANATORY |
| trace_ref | str — non-empty |

### §4.2 WadʿEvidenceCarrier

Evidence of conventional assignment (wadʿ) — not lexical meaning.

| Field | Constraint |
|-------|-----------|
| origin_domain | WadʿOriginDomain |
| evidence_type | WadʿEvidenceType |
| scope | str — non-empty |
| evidence_ref | str — non-empty |
| rank | Rank ≤ FORMAL_SHAPE_RANK_CEILING |
| residuals | tuple[Residual, ...] |
| trace_ref | str — non-empty |

### §4.3 PerUnitFormalProfileClosure

Proves that all formal layers are closed for this unit.

| Field | Constraint |
|-------|-----------|
| word_class_closure_ref | str — non-empty |
| weight_pattern_closure_ref | str — non-empty |
| inflection_closure_ref | str — non-empty |
| contract_slot_readiness_ref | str — non-empty |
| composition_participation_ref | str — non-empty |
| trace_ref | str — non-empty |

### §4.4 KulliJuzʾiAxisVerdict

A verdict, not a label. Asks: can this signified be predicated of
many? Is the particularity from wadʿ, reference, or context?

| Field | Constraint |
|-------|-----------|
| axis | KulliJuzʾiAxis (KULLI or JUZʾI) |
| particularity_source | ParticularitySource |
| predication_test_passed | bool |
| reference_resolution_status | str — non-empty |
| trace_ref | str — non-empty |

### §4.5 BranchLinkCandidate

Origin/branch geometry with ʿilla jāmiʿa and preventer audit.

| Field | Constraint |
|-------|-----------|
| origin_ref | str — non-empty |
| branch_ref | str — non-empty |
| relation_type | str — non-empty |
| illa_jamia | str — non-empty (ʿilla jāmiʿa evidence) |
| evidence_ref | str — non-empty |
| domain_compatibility | str — non-empty |
| no_preventer | bool — fāriq qādiḥ audit passed |
| rank | Rank ≤ FORMAL_SHAPE_RANK_CEILING |
| residuals | tuple[Residual, ...] |
| trace_ref | str — non-empty |

### §4.6 Semantic category

```text
JAMID      — entity anchoring readiness (not lexical meaning)
MASDAR     — abstract transformation potential (not event occurrence)
MUSHTAQ    — formal role-shape distribution (not real agency/patiency)
HARF       — relational operator readiness (not semantic relation)
REFERENCE  — reference search space (not resolved referent)
```

---

## §5 Inter-frame relation geometry stubs

The following are readiness stubs only — no content:

```text
TAWATUI_READINESS     — no tawāṭuʾ without shared ḥadd
TASHKIK_READINESS     — no tashkīk without shared ḥadd + licensed gradation
TABAYUN_READINESS     — no tabāyun without blocker of shared ḥadd
TARADUF_READINESS     — no tarāduf without same mutābaqah frame in same domain
ISHTIRAK_READINESS    — no ishtirāk without one signifier and multiple separated frames
NAQL_READINESS        — no naql without origin frame + target frame + transfer evidence
```

All are EXPLANATORY residuals.

---

## §6 prove_mufrad_semantic_slot_geometry() operation

A **pure function** that:

1. Validates all inputs (FormalStyleCandidate type and proven state,
   DalOnlyCandidate type, VerbalMadlulCandidate type,
   ContractableUnitGeometry type, FormalShapeClosureState.CLOSED).
2. Validates identity continuity (dal_identity, verbal_madlul_ref,
   formal references all non-empty).
3. Bounds rank via `RankLattice.meet(Rank.CANDIDATE, FORMAL_SHAPE_RANK_CEILING)`.
4. Builds deferred residuals (§7).
5. Refuses if any residual is HIDDEN_FORBIDDEN or BLOCKING.
6. Constructs all sub-carriers (WadʿEvidenceCarrier,
   PerUnitFormalProfileClosure, KulliJuzʾiAxisVerdict,
   BranchLinkCandidate).
7. Constructs SemanticSlotFrame.
8. Returns MufradSemanticSlotGeometryVerdict (PROVEN or REFUSED).

---

## §7 Required deferred residuals

Every SemanticSlotFrame must carry:

```text
SEMANTIC_SLOT_GEOMETRY_NOT_DALALAH
MUTABAQAH_DEFERRED_TO_PR_D2
TADAMMUN_DEFERRED_TO_PR_D2
ILTIZAM_DEFERRED_TO_PR_D2
MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3
IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE
MANTUQ_DEFERRED_UNTIL_IFADAH
MAFHUM_DEFERRED_UNTIL_MANTUQ
MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT
MANQUL_DEFERRED_UNTIL_TRANSFER_GATE
TAWATUI_READINESS
TASHKIK_READINESS
TABAYUN_READINESS
TARADUF_READINESS
ISHTIRAK_READINESS
NAQL_READINESS
```

All must be EXPLANATORY and visible.

---

## §8 Forbidden outputs

PR-D1 must not produce, export, or instantiate:

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
- Lexical semantic content
- Dictionary definition

---

## §9 Constitutional transition law

```text
No branch without origin.
No branch transition without ʿilla jāmiʿa.
No ʿilla jāmiʿa without evidence.
No evidence without rank and residual.
No transition before fāriq qādiḥ audit.
No SemanticSlotFrame without identity continuity from dal to frame.
No SemanticSlotFrame without WadʿEvidence.
No WadʿEvidence → Meaning.
No SemanticSlotFrame without all formal layers closed.
```

---

## §10 Chain position

```text
Previous required: PR-F8 (FormalStyleCandidate).
Current step: PR-D1.
Next permitted: PR-D1.2 — Maqām/Context Boundary Readiness.
PR-D1.2 is forbidden before PR-D1.
PR-D2 is forbidden before PR-D1.2.
PR-D3 is forbidden before PR-D2.
PR-20 is forbidden before PR-D3 + PR-D4.
```

SemanticSlotFrame opens PR-D1.2 readiness only.
SemanticSlotFrame does not open dalālah operations.
SemanticSlotFrame does not open Ifādah.

---

## §11 Governing chain law

```text
دلالة المفرد ليست قاموسًا.
هي تركيب إقليدي من: هوية الدال، المدلول اللفظي،
الشكل المغلق، الوضع، الأصل والفرع، الكل والجزء،
والعلة والمانع.

الإقليدية ليست ترتيب المصطلحات.
الإقليدية هي منع كل فرع من أن يولد إلا من أصل محفوظ،
بعلة جامعة، ومانع مفحوص، ورتبة، وبقايا، وأثر.

Mufrad dalālah is not a dictionary.
It is a Euclidean composition of: signifier identity,
verbal signified, closed formal shape, wadʿ, origin
and branch, whole and part, and ʿilla and preventer.
```
