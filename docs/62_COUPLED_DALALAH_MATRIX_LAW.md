# 62 — Coupled Dalālah Matrix Law

> **Status:** Constitutional law document. Planned as LAFZI-D0.
> Constitutional origin: docs/60 (Wad'i Madlul Condition Law), docs/59
> (Lafzi Madlul Correspondence Law), docs/58 (DalAlone Atomic Closure Law),
> docs/51 (Maʿqūl Branch Discipline Law), docs/52 (Constitutional Test Origin
> Covenant), and docs/14 (PR Chain Roadmap).
>
> This document defines the **Coupled Dalālah Matrix** boundary. It is
> law-only: it introduces no runtime code, no carriers, no enums, no operations,
> no adapter change, no audit change, and no global `FailureCode` expansion.

---

## §1 Governing principle

```text
No Mutabaqah without Wad'iMadlulClosed.
No Mutabaqah without CoupledDalalah.
No Tadammun without Mutabaqah.
No Iltizam without Tadammun.
No Iltizam without licensed LuzumEvidence.
No dalalah matrix output may become Ifadah, Mafhum, Hukm, Tanzil, Reality.
```

Mutābaqah, taḍammun, and iltizām are not operations on the dal alone and are
not judgments about reality. They are gates inside the bounded relation between
a preserved lafẓ and its limited wadʿī madlūl after wadʿ/samāʿ and before
word capability, relation, sentence, ifādah, mafhūm, and hukm.

Thus:

```text
MutabaqahDalalah != HukmCorrespondence
```

The first is correspondence of a lafẓ to the whole bounded placed madlūl. The
second is correspondence of a judgment to reality or evidence, and remains
outside this law.

---

## §2 Licensed placement

The corrected placement is:

```text
DalAloneClosed
 -> LafziMadlulClosed
 -> Wad'iMadlulClosed
 -> CoupledDalalah
 -> DalalahMatrix
 -> WordCapability
 -> Relation
 -> Sentence
 -> Ifadah
 -> Mantuq
 -> Mafhum
 -> Hukm
```

The following shortcuts are forbidden:

```text
DalAloneClosed -> Mutabaqah
LafziMadlulClosed -> Mutabaqah
Wad'iMadlulClosed -> Mutabaqah without CoupledDalalah
CoupledDalalah -> Tadammun without Mutabaqah
Mutabaqah -> Iltizam without Tadammun
Iltizam -> Ifadah
Iltizam -> Mafhum
Iltizam -> Hukm
Iltizam -> Reality
```

---

## §3 Domain and non-domain

### §3.1 Domain

The Coupled Dalālah Matrix may inspect only:

```text
Wad'iMadlulClosedRef
LafziMadlulClosedRef
MadlulBoundary
IncludedSurface
ExcludedSurface
DomainRef
ScopeRef
PriorKnowledgeRefs
VisibleResiduals
Rank
TraceRef
```

It asks:

1. whether the lafẓ indicates the whole bounded madlūl;
2. whether a claimed part is internal to that bounded madlūl;
3. whether a claimed lāzim is external to the madlūl but necessarily linked by
   licensed evidence.

### §3.2 Non-domain

The Coupled Dalālah Matrix must not emit or infer:

```text
IfadahCandidate
MafhumCandidate
HukmCandidate
TanzilCandidate
Reality
TruthValue
Ontology
FinalMeaning
```

---

## §4 Gate matrix

| Gate | License question | Output | Blocker | Inverse test |
| ---- | ---------------- | ------ | ------- | ------------ |
| CoupledDalalah | Is closed lafẓ coupled to closed wadʿī madlūl? | coupling candidate | missing Wad'iMadlulClosed | does the candidate preserve both refs? |
| MutabaqahGate | Does lafẓ indicate the whole bounded madlūl? | MutabaqahGateResult | missing madlūl boundary | does the result return to the whole placed meaning? |
| TadammunGate | Is the claimed part internal? | TadammunGateResult | part outside boundary | is the part inside the bounded definition? |
| IltizamGate | Is the claimed lāzim external and necessary? | IltizamGateResult | mere association | is it outside the definition and linked by evidence? |
| ResidualAudit | Are all residuals visible? | closed/deferred/blocked matrix | hidden residual | are blockers still visible? |

---

## §5 Conditions of possibility

```text
No Mutabaqah without a whole madlul boundary.
No Tadammun without an internal part licensed inside that boundary.
No Iltizam without an external lazim and visible LuzumEvidence.
No LuzumEvidence without a bounded domain and scope.
No threefold dalalah without organized prior knowledge.
```

Mutābaqah requires a full boundary. Taḍammun requires an internal structure of
the already bounded whole. Iltizām requires an external candidate and licensed
luzūm evidence; association, habit, suggestion, and free reasoning are not
luzūm.

---

## §6 Local residual vocabulary

Later runtime steps must begin with local residual names, not global
`FailureCode` expansion:

```text
MADLUL_BOUNDARY_REQUIRED
WAD_AUTHORITY_REQUIRED
USAGE_SCOPE_REQUIRED
MUTABAQAH_REQUIRED
INTERNAL_PART_REQUIRED
PART_OUTSIDE_MADLUL
LAZIM_OUTSIDE_REQUIRED
LUZUM_EVIDENCE_REQUIRED
MERE_ASSOCIATION_NOT_LUZUM
DOMAIN_MISMATCH
ISHTIRAK_REQUIRES_QARINAH
NAQL_SCOPE_REQUIRED
MAJAZ_LICENSE_REQUIRED
HIDDEN_DALALAH_MATRIX_RESIDUAL
FORBIDDEN_IFADAH_JUMP
FORBIDDEN_HUKM_JUMP
```

All residuals must remain visible. Hidden residuals refuse closure.

---

## §7 Legacy surface reconciliation

Existing historical surfaces — `MutabaqahCandidate`, `TadammunCandidate`, and
`IltizamCandidate` in `dalalah_candidates.py` — are not silently
reinterpreted by this law.

A later corrective or integration PR must explicitly decide whether each legacy
surface becomes:

```text
historical upstream surface
compatibility alias
consumer of Wad'iMadlulClosed / CoupledDalalah
```

Until that reconciliation exists, no downstream consumer may treat this law as
an implicit migration.

---

## §8 Staged implementation opened by this law

```text
LAFZI-D0  Coupled Dalalah Matrix Law
LAFZI-D1  CoupledDalalah carrier surface
LAFZI-D2  MutabaqahGate
LAFZI-D3  TadammunGate
LAFZI-D4  IltizamGate
LAFZI-D5  DalalahMatrixResidualAudit
LAFZI-D6  DalalahMatrixClosed -> WordCapability
```

This law does not implement any of those runtime steps. LAFZI-D runtime work may
open only after the LAFZI-C wadʿī sequence reaches its declared closure through
LAFZI-C8, unless the roadmap is amended explicitly.
