# SLGE-SDLC-P0 Deterministic Lifecycle Current-State Projection

Constitutional stage:
- Predecessor branch: `SLGE-SDLC-E0`
- Current branch: `SLGE-SDLC-P0`
- Next and only permitted successor: `SLGE-SDLC-G0`

`SLGE-SDLC-P0` computes lifecycle current state as a deterministic projection from authoritative lifecycle records.

## Core Invariants

- `HistoryIsAuthority`
- `CurrentStateIsProjection`
- `TransitionApproval != StateMutation`
- `Decision != Event`
- `Event != Projection`
- `Merge != Closure`
- `GreenCI != Closure`

Canonical equation:

```text
CurrentLifecycleState_t = Reduce(LegacyBaseline + AppliedLicensedLifecycleEvents<=t)
```

## Authority Boundary

P0 state mutation is licensed only by authoritative **applied lifecycle events**.

- Approved decisions without an applied event remain non-mutating.
- README, PR prose, filenames, CI results, and hand-edited projection files are non-authoritative.

## Legacy Boundary

`CurrentRuntimeAdmission != HistoricalCertification` remains binding.

For pre-`T_SLGE` records:
- bounded legacy baseline is admitted,
- historical uncertainty remains visible,
- no synthetic historical MCLT is allowed.

For post-`T_SLGE` records:
- only licensed applied lifecycle events may advance state.

## Runtime Surface

P0 runtime:
- input registry: `governance/registry/slge_sdlc_p0_lifecycle_events.json`
- reducer runtime: `src/taaqqul_slot_geometry/governance/slge_sdlc_p0_projection.py`
- projection output: `governance/projections/slge_sdlc_current_lifecycle_state.json`

Operational modes:
- `--check`: fail closed on drift (`LIFECYCLE_PROJECTION_DRIFT`)
- `--write`: canonical projection materialization

## Boundaries Preserved

P0 does not open:
- `SLGE-SDLC-G0` enforcement runtime,
- `SLGE-SDLC-C0` closure audit runtime,
- any `OBS-*` runtime,
- any V1 closure override.
