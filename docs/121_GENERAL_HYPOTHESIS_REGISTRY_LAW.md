# 121 — General Hypothesis Registry Law (OBS-H0)

> Status: law-only constitutional boundary (no runtime, no carriers, no ORM implementation, no datasets).
> Scope: define the legal admission boundary for `GeneralHypothesis` after `GUA-OBS-ES0` and before `OBS-D0`.
> Snapshot date: 2026-08-22.

## §1 Constitutional role

`OBS-H0` opens the first licensed observatory entry point where a general
hypothesis may be registered as testable without being upgraded to law, truth,
or invariant.

Governing thesis:

```text
Registration =/= Validation =/= Evidence =/= Promotion
```

## §2 Placement and dependency

`OBS-H0` is licensed only after:

- `docs/119_GENERAL_ALGEBRA_OBSERVATORY_FOUNDATION_LAW.md` (`GUA-OBS-L0`)
- `docs/120_EPISTEMIC_SELF_STATE_DERIVATION_LAW.md` (`GUA-OBS-ES0`)

and must precede:

- `OBS-D0` (domain projection/evidence contracts)
- `OBS-LE0` (learning event/evidence contracts)
- `OBS-X0` (cross-domain comparison)
- `OBS-P0` (promotion/demotion governance)
- any `OBS-ORM-*` runtime realization.

## §3 General hypothesis legal identity

A registered general hypothesis is a bounded research object, not a
constitutional truth claim:

```text
GH = <
  Identity,
  Claim,
  Scope,
  Variables,
  ExpectedInvariant,
  Falsifiers,
  Origin,
  EpistemicStateRef,
  ResidualRefs,
  TraceRef
>
```

`Rank` is not an independent field authority inside `GH`.
Any rank-like posture must be derivable through:

```text
GeneralHypothesis -> EpistemicStateRef -> RankAssignment
```

under `docs/120` derivation discipline.

## §4 Origin is not evidence

`Origin` may be philosophical, textual, methodological, or empirical in source,
but source identity does not constitute evidence of truth.

```text
FoundationalText -> HypothesisOrigin
FoundationalText -/-> EvidenceOfHypothesisTruth
FoundationalText -/-> GeneralInvariant
```

## §5 Expected invariant separation

`ExpectedInvariant` is a predictive field, never an observed result:

```text
ExpectedInvariant = WhatHypothesisPredictsShouldRemain
ObservedInvariant = WhatControlledTestingShowsToRemain
```

Required separations:

```text
ExpectedInvariant =/= ObservedInvariant
ExpectedInvariant =/= CrossDomainInvariantCandidate
ExpectedInvariant =/= GeneralInvariant
```

No promotion is licensed from expected value alone.

## §6 Hypothesis admission gate

Every candidate must pass `HypothesisAdmissionGate` before registration:

```text
CandidateHypothesis -> HypothesisAdmissionGate -> AdmittedGeneralHypothesis
```

`Admitted` means "licensed for testing", not "accepted as true".

Minimum gate obligations:

- `Falsifiability`
- `ScopeBoundedness`
- `VariableDeclaration`
- `InvariantSeparation`
- `NonCircularity`
- `DomainNeutrality`
- `ResidualVisibility`
- `Traceability`

## §7 Non-circularity requirement

No hypothesis is admissible if its definition encodes its own desired outcome.

Forbidden example class:

```text
DefinitionByDesiredInvariant
```

where success is guaranteed by definition rather than testable structure.

## §8 Domain-neutrality requirement

`OBS-H0` permits only domain-neutral general structure at registry entry.
Domain-specific evidence vocabularies are deferred to `OBS-D0`.

Allowed posture example:

```text
Transformation -> TrackableOperandIdentity
```

Disallowed posture at `OBS-H0`:

```text
DomainSpecificEvidenceSchemaAsGeneralRequirement
```

## §9 Epistemic state anchoring

The registered hypothesis must carry `EpistemicStateRef` under
`CurrentEpistemicState = Reduce(EpistemicEvents)` discipline from `docs/120`.

No detached mutable authority is licensed:

```text
GeneralHypothesis.rank = "GENERAL_LAW"
GeneralHypothesis.truth = true
```

without event-derived provenance.

## §10 Minimum complete epistemic event alignment

`OBS-H0` assumes self-state/event alignment with the minimum event posture:

```text
MCEE = <
  Subject,
  Proposition,
  PreState,
  Evidence,
  GateDecision,
  Transition,
  PostState,
  RankAssignment,
  Residuals,
  Trace
>
```

`OBS-H0` does not implement this runtime; it binds registry legality to this
event-derived authority posture.

## §11 Constitutional acceptance criteria (law-only)

A PR claiming `OBS-H0` closure is constitutionally admissible only if it proves:

1. `GeneralHypothesis` is legally defined as hypothesis, not invariant/law/truth.
2. Registry admission is explicitly separated from validation/evidence/promotion.
3. `Origin` is explicitly separated from evidence authority.
4. `ExpectedInvariant` is explicitly separated from observed/cross-domain/general invariants.
5. `HypothesisAdmissionGate` obligations include falsifiability, non-circularity,
   domain-neutrality, residual visibility, and traceability.
6. `EpistemicStateRef` is bound to `docs/120` event-history derivation discipline.
7. No runtime carrier, evaluator, dataset, ORM table, or migration is added.

## §12 Forbidden shortcuts

```text
Registration -/-> Validation
Registration -/-> Evidence
Registration -/-> Promotion
Origin -/-> Evidence
ExpectedInvariant -/-> ObservedInvariant
ExpectedInvariant -/-> CrossDomainInvariantCandidate
ExpectedInvariant -/-> GeneralInvariant
HypothesisDefinition -/-> SelfProof
AdmittedHypothesis -/-> DomainEvidence
GeneralHypothesis -/-> GeneralInvariant
```

## §13 Boundary of this step

`OBS-H0` does not:

- introduce runtime code under `src/`,
- add observatory carriers/contracts implementations,
- add persistence models, ORM schemas, migrations, or adapters,
- open domain evidence execution,
- open learning/cross-domain/promotion execution.

These surfaces are deferred to `OBS-D0` and successor steps.
