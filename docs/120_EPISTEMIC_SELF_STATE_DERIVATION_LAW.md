# 120 — Epistemic Self-State Derivation Law (GUA-OBS-ES0)

> Status: law-only constitutional boundary (no runtime, no ORM implementation, no persistence implementation).
> Scope: define how a system's self-epistemic state is licensed and derived before `OBS-H0`.
> Snapshot date: 2026-08-22.

## §1 Constitutional role

`GUA-OBS-ES0` is positioned between `GUA-OBS-L0` and `OBS-H0`.
It binds self-epistemic claims to licensed epistemic history.

Governing thesis:

```text
No epistemic self-claim without trace-derived authority.
```

## §2 Core derivation law

Self-state at time `t` is derived from licensed history:

```text
SelfEpistemicState_t = Projection(LicensedEpistemicHistory_<=t)
```

and never from free self-declaration:

```text
SelfEpistemicState_t =/= SelfDeclaration_t
```

## §3 Boundary of meaning

This law does not assert phenomenal consciousness.
It governs only auditable epistemic self-modeling.

```text
EpistemicSelfModel = AuditableModelOfOwnLicensedKnowledgeState
```

## §4 Permissibility rule

```text
PermissibleSelfClaim ⊆ DerivableSelfState
```

A system may not claim certainty, ignorance, revision, or suspension beyond what
its licensed record derivably supports.

## §5 No state without provenance

```text
NoSelfEpistemicStateWithoutProvenance
```

Every self-state must be traceable through:

```text
SelfState -> RankAssignment -> GateDecision -> Evidence -> Claim -> Origin
```

If this chain is missing, the self-state claim is unlicensed.

## §6 State is not boolean

Knowledge-state is structured, not `true/false`:

```text
KnowledgeState(p,t) = <Status, Rank, Scope, Evidence, Residuals, Trace>
```

`State` and `Rank` are separate surfaces.

## §7 Subject-proposition-time binding

Self-state must be bound to:

```text
Subject + Proposition + Domain + Scope + Time
```

No global "system knows domain X" claim is licensed without bounded proposition-level derivation.

## §8 Ignorance-state distinctions

"I do not know" is not a single state. At minimum:

- `UNASSESSED`
- `OUT_OF_SCOPE`
- `UNDERDETERMINED`
- `CONFLICTED`
- `UNKNOWN_WITH_RESIDUALS`
- `SUSPENDED`

Absence of record alone does not license `UNKNOWN`; it licenses `UNASSESSED`.

## §9 Event-history over mutable current-state

Current state is a projection:

```text
CurrentEpistemicState = Reduce(EpistemicEvents)
```

No constitutional authority for detached mutable assignment:

```text
SET current_state = CERTAIN
```

without corresponding licensed transition history.

## §10 No erasure across revisions

State change must preserve prior state and transition cause:

```text
State_t + Transition + Evidence + State_t+1
```

No revision/correction/retraction/demotion claim is licensed without preserved
pre-state, trigger, and post-state lineage.

## §11 Residuals are part of self-state

Self-knowledge representation must include unresolved boundaries:

```text
SelfKnowledge = Known + Unknown + KnownUnknowns + BlockingResiduals
```

Residual closure may produce new transitions; it must not erase prior residual history.

## §12 Confidence-rank separation

```text
ModelConfidence =/= EpistemicRank
```

Epistemic rank is derived from licensed evidence/gate/policy/residual history,
not directly from model probability outputs unless domain policy explicitly
licenses such signals as evidence.

## §13 Forbidden shortcuts

```text
SelfDeclaration -/-> SelfEpistemicState
AnswerConfidence -/-> EpistemicRank
NoRecord -/-> KnownIgnorance
CorrectAnswer -/-> Knowledge
ChangedAnswer -/-> JustifiedRevision
NewEvidence -/-> RankPromotion
ResidualResolved -/-> ResidualDeletion
CurrentState -/-> HistoricalTruth
ModelProbability -/-> EpistemicProbability
```

## §14 Minimal record contract posture (law-only)

Before any ORM runtime step, the law binds the following minimum event-level
surfaces as constitutional obligations:

- `EpistemicSubject`
- `Proposition`
- `EvidenceRecord`
- `GateDecision`
- `RankAssignment`
- `ResidualRecord`
- `EpistemicStateTransition`
- `TraceEvent`

`CurrentSelfEpistemicState` is a derived projection, not an independent source
of authority.

## §15 Sequencing obligation

`GUA-OBS-ES0` is a prerequisite before:

- `OBS-H0` (General Hypothesis Registry Law),
- `OBS-D0` (Domain projection/evidence contracts),
- `OBS-L0/LE0` (Learning event/evidence law),
- `OBS-X0` (Cross-domain comparison law),
- `OBS-P0` (Invariant promotion/demotion law),
- any `OBS-ORM-*` runtime implementation.

## §16 Boundary of this step

`GUA-OBS-ES0` does not:

- add runtime code,
- add persistence/ORM runtime implementation,
- add schema migrations,
- add dataset ingestion,
- add consciousness claims,
- mutate `src/taaqqul_slot_geometry/gua/` runtime semantics.
