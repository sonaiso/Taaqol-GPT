# 60 — Wad'i Madlul Condition Law

> **Status:** Constitutional law document. Ratified in LAFZI-C0.
> Constitutional origin: docs/59 (Lafzi Madlul Correspondence Law), docs/58
> (DalAlone Atomic Closure Law), docs/47 (Post-Vertical Roadmap), docs/51
> (Maʿqūl Branch Discipline Law), docs/52 (Constitutional Test Origin
> Covenant), and docs/14 (PR Chain Roadmap).
>
> This document defines the **Wad'iMadlul condition boundary**. It is
> law-only: it introduces no runtime code, no carriers, no enums, no
> operations, no adapter change, no audit change, and no global `FailureCode`
> expansion.
>
> Numbering note: docs/56 and docs/57 remain reserved for GPT reasonableness
> boundary documents, docs/58 is the DalAlone Atomic Closure Law, docs/59 is
> the Lafzi Madlul Correspondence Law, so this law uses docs/60.

---

## §1 Governing principle

```text
No Wad'iMadlul without LafziMadlulClosed.
No Wad'iMadlulClosed from LafziMadlulClosed alone.
No wadʿī meaning without WadKind.
No WadKind without WadAuthority.
No WadAuthority without UsageScope.
No UsageScope without MeaningIdentity.
No Manqul without OriginalWad' and licensed transfer.
No Majaz without OriginalHaqiqah, Relation, Qarinah, and Preventer.
No Mutabaqah before Wad'iMadlulClosed and CoupledDalalah.
No Tadammun before Mutabaqah.
No Iltizam before Tadammun.
```

`LafziMadlulClosed` proves only that the bounded verbal-signified layer has
closed. It opens the next wadʿī condition boundary, but it does not decide the
placed meaning.

The only lawful first transition is:

```text
LafziMadlulClosed
  -> Wad'iMadlulGate
  -> Wad'iMadlulContract
```

The following shortcut is forbidden:

```text
LafziMadlulClosed -> Wad'iMadlulClosed
```

---

## §2 Licensed chain

The chain licensed by this law is:

```text
DalAloneClosed
  -> LafziMadlulClosed
  -> Wad'iMadlulClosed
  -> CoupledDalalah
  -> Mutabaqah
  -> Tadammun
  -> Iltizam
```

The following transitions remain forbidden until separately licensed by later
law and gate implementations:

```text
LafziMadlul -> Mutabaqah
LafziMadlul -> Tadammun
LafziMadlul -> Iltizam
LafziMadlulClosed -> Wad'iMadlulClosed without Wad'iMadlulGate proof
Wad'iMadlulClosed -> Mutabaqah without CoupledDalalah
Mutabaqah -> Iltizam without Tadammun
```

---

## §3 Domain and non-domain

### §3.1 Domain

`Wad'iMadlulGate` may inspect only the licensed post-lafzi condition surface:

```text
LafziMadlulClosedRef
WadKind
WadAuthority
UsageScope
MeaningIdentity
TransferOrMajazStatus
Wad'iResidualAudit
```

The domain is wadʿī: it concerns whether a closed lafzi candidate has a placed
meaning within a licensed language, customary, technical, transferred, or
figurative scope. It is not mutābaqah, taḍammun, iltizām, ifādah, hukm,
tanzīl, or reality.

### §3.2 Non-domain

`Wad'iMadlulGate` and `Wad'iMadlulContract` must not emit or infer:

```text
MutabaqahCandidate
TadammunCandidate
IltizamCandidate
CoupledDalalahVerdict
RelationCandidate
CompositionCandidate
IfadahCandidate
HukmCandidate
TanzilCandidate
ActualRelation
Reality
Ontology
TruthValue
```

A successful condition proof opens only wadʿī candidacy. It does not perform a
dalālah relation operation.

---

## §4 Wad'iMadlulContract

The later `Wad'iMadlulContract` carrier must carry at least:

```text
Wad'iMadlulContract =
    lafzi_madlul_closed_ref
    wad_kind
    wad_authority
    usage_scope
    meaning_identity
    transfer_or_majaz_status
    residuals
    rank
    trace_ref
```

It must not carry:

```text
mutabaqah
tadammun
iltizam
ifadah
hukm
tanzil
reality
```

`Wad'iMadlulContract` is a condition contract. It is not a final semantic
meaning, not a relation candidate, and not a judgment.

---

## §5 Gate sequence W0–W7

The wadʿī condition gate sequence is:

```text
W0  LafziMadlulClosedGate
W1  WadKindGate
W2  WadAuthorityGate
W3  UsageScopeGate
W4  MeaningIdentityGate
W5  TransferMajazGate
W6  WadiResidualAudit
W7  WadiStopGate
```

### §5.1 W0 — LafziMadlulClosedGate

```text
NoLafziMadlulClosed => NoWad'iMadlul
```

Unclosed or ambiguous lafzi surfaces, such as unvocalized `علم`, cannot open a
single wadʿī madlūl.

### §5.2 W1 — WadKindGate

```text
WadKind =
    LUGHAWI
  | URFI
  | ISTILAHI
  | MANQUL
  | MAJAZI
  | DEFERRED
```

No `Wad'iMadlulClosed` may be emitted when `WadKind` is unknown.

### §5.3 W2 — WadAuthorityGate

No wadʿ exists without a visible usage authority:

```text
NoWadAuthority => DeferredWadiMadlul
```

Permitted authority families include:

```text
LUGHAWI    -> lexicon / samāʿ / Arabic usage evidence
URFI       -> bounded usage community
ISTILAHI   -> named technical discipline
MANQUL     -> transferring custom or technical convention
MAJAZI     -> qarinah + relation preventing literal closure
```

### §5.4 W3 — UsageScopeGate

No placed meaning works without scope. `UsageScope` must bind the candidate to a
language, customary, technical, transferred, or figurative domain.

Example: `جذر` may belong to botanical, morphological, mathematical, or project
identity-origin scope. An open scope forces `DEFERRED`.

### §5.5 W4 — MeaningIdentityGate

`MeaningIdentity` must declare:

```text
identity_kind
boundary
included_surface
excluded_surface
residuals
```

Permitted identity kinds are structural only:

```text
ENTITY
TRANSFORMATION
ATTRIBUTE
RELATION_OPERATOR
REFERENCE_SPACE
DEFERRED
```

`MeaningIdentity` is a bounded identity for the placed meaning. It is not
mutābaqah and not final truth.

### §5.6 W5 — TransferMajazGate

For `MANQUL`, closure requires:

```text
OriginalWad'
TransferCause
NewUsageScope
PreservedTrace
QadihDifference
```

For `MAJAZI`, closure requires:

```text
OriginalHaqiqah
Relation
Qarinah
PreventerOfLiteralMeaning
Residuals
```

Thus:

```text
No Manqul without OriginalWad'.
No Majaz without OriginalHaqiqah, Relation, Qarinah, and Preventer.
```

Missing transfer or figurative components must surface through the local
residual vocabulary:

```text
Missing OriginalWad' => TRANSFER_ORIGIN_REQUIRED
Missing TransferCause => TRANSFER_CAUSE_REQUIRED
Missing OriginalHaqiqah => MAJAZ_HAQIQAH_REQUIRED
Missing Relation => MAJAZ_RELATION_REQUIRED
Missing Qarinah => MAJAZ_QARINAH_REQUIRED
Missing PreventerOfLiteralMeaning => MAJAZ_LITERAL_PREVENTER_REQUIRED
```

### §5.7 W6 — WadiResidualAudit

All residuals must remain visible. Hidden residuals refuse closure.

### §5.8 W7 — WadiStopGate

The only permitted outputs of the condition sequence are:

```text
Wad'iMadlulClosed
DeferredWadiMadlul
BlockedWadiMadlul
```

`WadiStopGate` must not emit `Mutabaqah`, `Tadammun`, `Iltizam`, `Ifadah`,
`Hukm`, `Tanzil`, or `Reality`.

---

## §6 Local wadʿī residual vocabulary

The required local vocabulary is:

```text
LAFZI_MADLUL_CLOSED_REQUIRED
WAD_KIND_REQUIRED
WAD_AUTHORITY_REQUIRED
USAGE_SCOPE_REQUIRED
MEANING_IDENTITY_REQUIRED
TRANSFER_ORIGIN_REQUIRED
TRANSFER_CAUSE_REQUIRED
MAJAZ_HAQIQAH_REQUIRED
MAJAZ_RELATION_REQUIRED
MAJAZ_QARINAH_REQUIRED
MAJAZ_LITERAL_PREVENTER_REQUIRED
MULTIPLE_WADI_CANDIDATES
HIDDEN_WADI_RESIDUAL
FORBIDDEN_WADI_CLOSURE_JUMP
FORBIDDEN_COUPLED_DALALAH_JUMP
FORBIDDEN_MUTABAQA_JUMP
FORBIDDEN_TADAMMUN_JUMP
FORBIDDEN_ILTIZAM_JUMP
FORBIDDEN_IFADAH_JUMP
FORBIDDEN_HUKM_JUMP
```

Hard refusals map to existing global refusal names, including:

```text
GATE_REQUIRED
BOUNDARY_MISSING
TRACE_MISSING
SCOPE_MISSING
HIDDEN_RESIDUAL
BLOCKING_RESIDUAL_PRESENT
FORBIDDEN_STRAIGHT_LINE
OUTPUT_EXCEEDS_LAYER
```

No residual may be hidden to produce wadʿī closure.

---

## §7 Closure states

A later `WadiMadlulState` must distinguish:

```text
CLOSED
DEFERRED
BLOCKED
```

`CLOSED` is licit only if all are present and non-blocking:

```text
LafziMadlulClosed
+ WadKind
+ WadAuthority
+ UsageScope
+ MeaningIdentity
+ TransferOrMajazStatus
+ VisibleResiduals
```

`DEFERRED` is required when there are multiple placed meanings or missing but
non-blocking evidence.

`BLOCKED` is required when the path is unlicensed or tries to jump to a later
relation layer.

---

## §8 Legacy surface reconciliation

Existing historical surfaces — `VerbalMadlulCandidate`, `SemanticSlotFrame`, and
`MutabaqahCandidate` — are not silently reinterpreted by this law.

A later corrective or integration PR must explicitly decide whether each legacy
surface becomes:

```text
historical upstream carrier
compatibility alias
consumer of LafziMadlulClosed / Wad'iMadlulClosed
```

Until that reconciliation exists, no downstream legacy consumer may treat this
law as an implicit migration.

---

## §9 Matrix required for wadʿī condition closure

| Gate | Unit | Condition | Blocker | Output | Not output |
| ---- | ---- | --------- | ------- | ------ | ---------- |
| W0 | LafziMadlulClosed | closed lafzi madlul | blocking lafzi residuals | wadʿī eligibility | mutabaqah |
| W1 | WadKind | lughawi / urfi / istilahi / manqul / majazi | no kind | wadʿ kind | hukm |
| W2 | WadAuthority | usage authority | undocumented usage | wadʿ license | tadammun |
| W3 | UsageScope | bounded scope | open scope | meaning within domain | generalization |
| W4 | MeaningIdentity | identity boundary | vague meaning | wadʿī candidate | automatic mutabaqah |
| W5 | Transfer/Majaz | origin + transfer or qarinah | forbidden leap | licensed transfer/majaz | hukm |
| W6 | ResidualAudit | visible residuals | hidden residuals | closed or deferred | relation |
| W7 | StopGate | wadʿī closure | jump | ready for coupling | direct mutabaqah |

---

## §10 Runtime staging opened by this law

This law opens a later implementation sequence only after `LAFZI-B7` is
ratified:

```text
LAFZI-C1  Wad'i carrier surface + local residual vocabulary
LAFZI-C2  WadKindGate
LAFZI-C3  WadAuthorityGate
LAFZI-C4  UsageScopeGate
LAFZI-C5  MeaningIdentityGate
LAFZI-C6  TransferMajazGate
LAFZI-C7  Wad'iResidualAudit
LAFZI-C8  Wad'iMadlulClosed -> CoupledDalalahGate integration
```

Each later step must be separately staged in docs/14 before code ships.
`LAFZI-C0` itself ships no runtime code.

---

## §11 Golden examples

### §11.1 `رَجُل`

```text
LafziMadlulClosed
  -> W1 LUGHAWI
  -> W2 Arabic usage authority
  -> W3 general Arabic scope
  -> W4 human male identity boundary
  -> W7 Wad'iMadlulClosed
```

Forbidden output: `MutabaqahCandidate`.

### §11.2 `جذر`

```text
LafziMadlulClosed
  -> multiple UsageScope candidates
  -> DEFERRED
```

Forbidden output: unscoped generalization.

### §11.3 manqūl usage

```text
LafziMadlulClosed
  -> MANQUL
  -> OriginalWad'
  -> TransferCause
  -> NewUsageScope
  -> PreservedTrace
  -> QadihDifference
  -> Wad'iMadlulClosed or DEFERRED
```

Forbidden output: no transferred meaning without origin.

### §11.4 majāz usage

```text
LafziMadlulClosed
  -> MAJAZI
  -> OriginalHaqiqah
  -> Relation
  -> Qarinah
  -> PreventerOfLiteralMeaning
  -> Wad'iMadlulClosed or DEFERRED
```

Forbidden output: no figurative meaning without truth-origin, relation, and
qarīnah.

---

## §12 Negative jump matrix

| forbidden transition | reason |
| -------------------- | ------ |
| `LafziMadlul -> Mutabaqah` | dalālah relation jump |
| `LafziMadlul -> Tadammun` | inclusion jump |
| `LafziMadlul -> Iltizam` | entailment jump |
| `LafziMadlulClosed -> Wad'iMadlulClosed` | wadʿī gate bypass |
| `WadKind -> Wad'iMadlulClosed` | authority / scope / identity missing |
| `WadAuthority -> MeaningIdentity` without scope | scope bypass |
| `MeaningIdentity -> Mutabaqah` | coupled dalālah missing |
| `Wad'iMadlulClosed -> Mutabaqah` | CoupledDalalah missing |
| `Wad'iMadlulClosed -> Tadammun` | Mutabaqah missing |
| `Wad'iMadlulClosed -> Iltizam` | Tadammun missing |
| `Wad'iMadlulClosed -> Ifadah` | proposition jump |
| `Wad'iMadlulClosed -> Hukm` | judgment jump |
| `Wad'iMadlulClosed -> Reality` | ontology/reality jump |

---

## §13 Golden law

```text
LafziMadlulClosed opens Wad'iMadlulGate only.
Wad'iMadlulGate proves conditions; it does not emit relation closure.
Wad'iMadlulClosed requires WadKind, WadAuthority, UsageScope,
MeaningIdentity, TransferOrMajazStatus, visible residuals, rank, and trace.
No Mutabaqah before CoupledDalalah.
No Tadammun before Mutabaqah.
No Iltizam before Tadammun.
No approved wadʿī output may hide residuals or jump to ifādah, hukm,
tanzīl, or reality.
```
