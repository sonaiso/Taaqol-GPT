# 38 — Mutābaqah / Taḍammun / Iltizām Candidate Law

> PR-D2 binding.
> Origin: PR-D1.2 (Maqām/Context Boundary Readiness) prerequisite.
> Ratified by: PR-D2.

---

## §1 Purpose

This law governs the Mutābaqah/Taḍammun/Iltizām Candidate layer. The
layer establishes the three dalālah relation candidates — correspondence,
inclusion, and entailment — built on the proven semantic slot geometry
(PR-D1) and bounded by maqām/context readiness (PR-D1.2). These are
**candidates only**, never final meaning.

The governing principle:

```text
لا مطابقة بلا خانات دلالية ولا حدود مقام.
لا تضمن بلا كل مقيد بمجال.
لا التزام بلا علاقة لزوم مقيدة بسياق.
المطابقة مرشح لا معنى نهائي.
التضمن جزء مقيّد بهوية الكل، لا تفكيك حر.
الالتزام علاقة لزوم مرخصة، لا استدلال حر ولا مفهوم ولا حكم.

No Mutābaqah without SemanticSlotFrame and MaqamContextBoundary.
No Taḍammun without Maqām-bounded whole/part frame.
No Iltizām without Context-bounded LicensedNecessaryRelation.
MutābaqahCandidate ≠ final meaning.
TaḍammunCandidate ≠ free part decomposition.
IltizāmCandidate ≠ free reasoning / Mafhūm / Hukm / Qiyās result.
```

---

## §2 Governing invariants

```text
MutābaqahCandidate ≠ Meaning.
MutābaqahCandidate ≠ Ifādah.
MutābaqahCandidate ≠ Hukm.
MutābaqahCandidate ≠ Majāz verdict.
MutābaqahCandidate ≠ Manqūl verdict.
TaḍammunCandidate ≠ arbitrary part decomposition.
TaḍammunCandidate ≠ Meaning.
TaḍammunCandidate ≠ ontological claim.
IltizāmCandidate ≠ free reasoning.
IltizāmCandidate ≠ Mafhūm.
IltizāmCandidate ≠ Hukm.
IltizāmCandidate ≠ Qiyās result.
IltizāmCandidate ≠ Majāz license.
IltizāmCandidate ≠ Manqūl license.
BLOCKED_BY_QARINA ≠ HaqīqahAttempt failure.
BLOCKED_BY_QARINA ≠ Majāz license.
No Taḍammun without Mutābaqah.
No part without whole.
No part outside identity_anchor.
No Iltizām without LicensedNecessaryRelation.
```

---

## §3 Prerequisites

PR-D2 consumes **both**:

1. `MufradSemanticSlotGeometryVerdict` with state PROVEN — provides
   the SemanticSlotFrame (identity continuity, wadʿ evidence, formal
   profile, kulli/juzʾi axis, branch-link geometry).
2. `MaqamContextBoundaryVerdict` with state PROVEN — provides the
   MaqamContextFrame (discourse domain, usage register, technical
   domain, qarīnah readiness, blocker audit, literal domain
   constraint, wadʿ scope constraint).

PR-D2 must not consume or produce:
- Final meaning
- Ifādah (proposition)
- Hukm (judgment)
- Tanzīl (application)
- Majāz operation (figurative transfer)
- Manqūl operation (terminological transfer)
- Mafhūm (derived understanding)
- Speaker intent
- Ontological claims
- Free reasoning

---

## §4 Candidate structure

### §4.1 MutābaqahCandidate

Correspondence candidate — the candidate for full-extension dalālah:

- `semantic_slot_frame_ref: str` — Reference to proven SemanticSlotFrame.
- `maqam_context_frame_ref: str` — Reference to proven MaqamContextFrame.
- `wad_evidence_ref: str` — Wadʿ evidence reference.
- `kulli_juzii_axis: KulliJuziiAxis` — Whole/part classification.
- `formal_profile_ref: str` — Per-unit formal profile closure reference.
- `correspondence_domain: str` — Bounded correspondence domain.
- `rank: Rank` — Bounded by DALALAH_CANDIDATE_RANK_CEILING.
- `residuals: tuple[Residual, ...]` — Visible deferred residuals.
- `trace_ref: str` — Trace reference.

### §4.2 TaḍammunCandidate

Inclusion candidate — the candidate for part-of-whole dalālah:

- `mutabaqah_ref: str` — Reference to a proven MutābaqahCandidate.
- `whole_identity_anchor: str` — Identity anchor of the whole.
- `part_designation: str` — Designation of the included part.
- `inclusion_evidence: str` — Evidence of the inclusion relation.
- `domain_bounded: bool` — Whether part is bounded by discourse domain.
- `rank: Rank` — Bounded by DALALAH_CANDIDATE_RANK_CEILING.
- `residuals: tuple[Residual, ...]` — Visible deferred residuals.
- `trace_ref: str` — Trace reference.

### §4.3 IltizāmCandidate

Entailment candidate — the candidate for necessary-relation dalālah:

- `mutabaqah_ref: str` — Reference to a proven MutābaqahCandidate.
- `necessary_relation_type: NecessaryRelationType` — Type of luzūm.
- `relation_evidence: str` — Evidence of the necessary relation.
- `context_bounded: bool` — Whether relation is bounded by context.
- `rank: Rank` — Bounded by DALALAH_CANDIDATE_RANK_CEILING.
- `residuals: tuple[Residual, ...]` — Visible deferred residuals.
- `trace_ref: str` — Trace reference.

### §4.4 NecessaryRelationType

Licensed necessary relation types (never free reasoning):

- `SHART` — Condition (shart).
- `SABAB` — Cause (sabab).
- `MANI` — Preventer (māniʿ).
- `ILLA` — Effective cause (ʿilla).
- `ATHAR_LAZIM` — Necessary effect (athar lāzim).
- `QARINA_LAZIMA` — Necessary indicator (qarīna lāzima).

---

## §5 Operation: `prove_dalalah_candidates()`

```text
prove_dalalah_candidates(
    semantic_slot_verdict: MufradSemanticSlotGeometryVerdict,
    maqam_context_verdict: MaqamContextBoundaryVerdict,
    correspondence_domain: str,
    part_designation: str,
    inclusion_evidence: str,
    necessary_relation_type: NecessaryRelationType,
    relation_evidence: str,
) → DalalahCandidateVerdict
```

The function:

1. Validates both input verdicts are PROVEN.
2. Validates SemanticSlotFrame and MaqamContextFrame are present.
3. Validates LiteralConstraintType.BLOCKED_BY_QARINA is treated as
   constraint only — not as HaqīqahAttempt failure, not as Majāz
   license.
4. Constructs MutābaqahCandidate from SemanticSlotFrame + MaqamContextFrame.
5. Constructs TaḍammunCandidate only if MutābaqahCandidate exists
   (no part without whole).
6. Constructs IltizāmCandidate only if MutābaqahCandidate exists
   and NecessaryRelationType is licensed.
7. Returns DalalahCandidateVerdict with all three candidates.

---

## §6 Required deferred residuals

```text
DALALAH_CANDIDATES_NOT_MEANING
MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3
IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE
HUKM_DEFERRED_UNTIL_IFADAH
MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT
MANQUL_DEFERRED_UNTIL_TRANSFER_GATE
MAFHUM_DEFERRED_UNTIL_MANTUQ
BLOCKED_BY_QARINA_IS_CONSTRAINT_NOT_VERDICT
```

All residuals are EXPLANATORY and visible.

---

## §7 Forbidden outputs

PR-D2 must NOT export or instantiate:

- `Meaning` / `FinalMeaning`
- `IfādahCandidate`
- `HukmCandidate`
- `TanzīlCandidate`
- `ManṭūqClosure`
- `MafhūmCandidate`
- `MajāzVerdict` / `MajāzLicense`
- `ManqūlVerdict` / `ManqūlLicense`
- `SpeakerIntentVerdict`
- `HaqīqahAttemptVerdict`
- `OntologicalClaim`
- `FreeReasoning`
- `QiyāsResult`

---

## §8 Rank governance

```text
DALALAH_CANDIDATE_RANK_CEILING = MAQAM_CONTEXT_RANK_CEILING
```

No rank promotion beyond the inherited ceiling.

---

## §9 Critical constraint: BLOCKED_BY_QARINA

```text
BLOCKED_BY_QARINA is a literal domain constraint candidate.
BLOCKED_BY_QARINA ≠ HaqīqahAttempt failure.
BLOCKED_BY_QARINA ≠ Majāz license.
```

PR-D2 must treat `LiteralConstraintType.BLOCKED_BY_QARINA` from
PR-D1.2 as a constraint type only. It does not open the door to
majāz. It does not declare haqīqah impossible. It merely records
that a qarīnah *constrains* the literal domain — the actual
haqīqah/majāz determination is deferred to a later layer.
