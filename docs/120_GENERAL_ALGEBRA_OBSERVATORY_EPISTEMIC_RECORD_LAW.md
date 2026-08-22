# 120 — General Algebra Observatory Epistemic Record Law (GUA-OBS-R0)

> Status: law-only constitutional boundary (no runtime, no ORM implementation, no datasets).
> Scope: define epistemic-record meaning before `OBS-H0` registry law and before any observatory relational runtime.
> Snapshot date: 2026-08-22.

## §1 Constitutional role

`GUA-OBS-R0` is the observatory record boundary.
It defines what is being recorded before defining how it is stored.

The governing posture:

```text
The database records licensed epistemic history;
it does not declare reality.
```

## §2 Core separations

```text
Reality != KnowledgeClaim != ORMRecord
```

- Reality is not produced by persistence.
- Knowledge claim is not equivalent to its storage row.
- ORM record is a bounded historical projection, not a truth primitive.

## §3 Minimum complete epistemic event

Every admissible observatory record must trace back to one
minimum-complete epistemic event (`MCEE`):

```text
MCEE =
< Identity,
  Domain,
  StateBefore,
  RelationOrOperation,
  StateAfter,
  Evidence,
  Gate,
  Rank,
  Residuals,
  Trace >
```

No `MCEE` element may be silently synthesized.

## §4 Loss discipline

If any `MCEE` element is absent, the epistemic record is constitutionally
incomplete:

- no `Identity` -> changed object cannot be tracked,
- no `Domain` -> operation legality cannot be judged,
- no `StateBefore`/`StateAfter` -> transition cannot be reconstructed,
- no `RelationOrOperation` -> transformation type is unknown,
- no `Evidence` -> transition is unjustified,
- no `Gate` -> licensing path is unknown,
- no `Rank` -> evidential force is unknown,
- no `Residuals` -> closure gaps are hidden,
- no `Trace` -> replay/audit path is broken.

## §5 Structural vs epistemic relations

`StructuralFK` is not `EpistemicRelation`.

Structural linkage (for storage normalization) does not by itself assert:

- support,
- contradiction,
- causation,
- prerequisite,
- evidence-for.

Every epistemic relation must be explicit and auditable as:

```text
EpistemicRelationAssertion =
< Subject, Predicate, Object, Domain, Evidence, Rank, Residuals, Trace >
```

## §6 Event-history over mutable snapshots

Current state is a projection of event history:

```text
CurrentState = Projection(EventHistory)
```

It is not a truth source by itself.

Rank and residual transitions must be historical events, not detached mutable
fields:

```text
Rank_1 -> PromotionDecision -> Rank_2
ResidualOpen -> ResolutionEvent -> ResidualResolved
```

## §7 Derived verdict discipline

Whenever constitutionally possible:

```text
Verdict = DerivedView(Evidence, Gate, Transition, Residuals)
```

and not an independently mutable label detached from provenance.

No stored verdict is constitutional without derivation lineage.

## §8 Macro-chain and operational chain

The conceptual observatory chain remains:

```text
GeneralHypothesis -> DomainEvidence -> LearningEvidence -> CrossDomainInvariantCandidate
```

Operational execution must use a non-skipping measurement chain:

```text
GeneralHypothesis
-> DomainProjection
-> DomainEvidenceRecord
-> LearningOperationalization
-> LearningEvent
-> LearningEvidenceRecord
-> CrossDomainComparison
-> CrossDomainInvariantCandidate
-> PromotionDecision
-> GeneralInvariant
```

No observatory runtime/schema step may collapse this chain into shortcut links.

## §9 Forbidden shortcuts

The following are forbidden:

```text
ORMRowExistence -/-> TruthOfClaim
StructuralFK -/-> EpistemicRelationProof
CurrentState -/-> FullEpistemicHistory
ManualVerdictField -/-> DerivedClosureAuthority
DomainEvidence -/-> LearningEvidence (without operationalization/event)
LearningEvidenceSet -/-> Invariant (without controlled comparison)
```

## §10 Boundary of this step

`GUA-OBS-R0` does not:

- add runtime tables/migrations/models,
- define ORM framework implementation details,
- open dataset ingestion,
- open curriculum execution runtime,
- mutate existing `GUA-1` runtime code.

## §11 Sequencing obligation

`GUA-OBS-R0` is a prerequisite boundary before:

- `OBS-H0` (General Hypothesis Registry),
- `OBS-D0` (Domain Projection/Evidence contracts),
- `OBS-L0` (Learning operationalization/events),
- `OBS-X0` (cross-domain comparison/promotion),
- and any `OBS-ORM-*` runtime implementation step.

