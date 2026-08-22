# SLGE-SDLC-E0 Lifecycle Execution Engine

Constitutional stage:
- Predecessor branch: `SLGE-SDLC-M0`
- Current branch: `SLGE-SDLC-E0`
- Next and only permitted successor: `SLGE-SDLC-P0`

`SLGE-SDLC-E0` opens runtime evaluation for **current/future** lifecycle transitions only.

It does not certify unknown legacy history.

## Core Invariants

- `CurrentRuntimeAdmission != HistoricalCertification`
- `ResidualConsumption != ResidualResolution`
- `RebuildCreatesNewLicensedLineage != RepairsUnknownPast`
- `historical_status != PROVEN -> historical_mclt_ref = null`

## Temporal Cut

E0 uses canonical cut `T_SLGE` anchored by ratified governance identity and immutable governance/dependency order, not wall-clock alone.

- `event < T_SLGE`: legacy-history domain; E0 cannot create historical certification.
- `event >= T_SLGE`: governed E0 domain; transition requires full licensed MCLT validation.

## Legacy Baseline Admission

`LegacyBaselineAdmission != HistoricalCertification`

- `KEEP`: may enter bounded present baseline with legacy residual visibility preserved.
- `RETYPE`: requires explicit identity semantics.
- `REORDER`: preserves `HistoricalOrder != DependencyOrder`.
- `QUARANTINE`: refuses ordinary progression.
- `REBUILD`: creates new licensed lineage only; old unknown lineage is not repaired.

## Runtime Surface

E0 input: typed `TransitionAttempt` (identity/origin/domain-scope proofs, evidence refs, residual refs, trace ref, backward proof, forward readiness, triangle coherence, optional baseline ref).

E0 output: typed `TransitionDecision` with:
- state: `APPROVED | REFUSED | DEFERRED | SUSPENDED`
- named failure codes
- authority/rank ceiling
- consumed/inherited/blocking residual refs
- trace ref
- next openings

`APPROVED` licenses only the current transition and does not imply closure, historical proof promotion, or global lifecycle state computation.

## Boundaries Preserved

E0 does not open:
- `SLGE-SDLC-P0` reducer runtime
- `SLGE-SDLC-G0` PR/runtime enforcement
- `SLGE-SDLC-C0` closure audit
- any `OBS-*` runtime
- any V1 closure override
