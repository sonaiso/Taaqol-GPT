# 123 — Repository State, Authority, and Topology Law (REPO-ORG-L0)

> Status: law-only constitutional governance boundary (no runtime mutation, no branch opening, no ORM opening).
> Scope: repository-organization refoundation that separates historical authority from projected current state.
> Snapshot date: 2026-08-22.

## §1 Constitutional role

`REPO-ORG-L0` governs the repository itself as a bounded audited object.
It separates law authority, runtime state, evidence state, historical record,
and current-state projection.

Governing thesis:

```text
NoRepositoryStateWithoutDerivedEvidence.
RepositoryCurrentState = Projection(History, Dependencies, Runtime, Tests, Evidence, Residuals).
```

## §2 Historical order vs dependency order

Repository governance must preserve both:

```text
HistoricalOrder != DependencyOrder
```

A historical amendment order may differ from semantic dependency order.
Both must be represented explicitly and must not be collapsed into one field.

## §3 Five authority roles

Repository governance is split into five authority roles:

1. `LawAuthority`
2. `RuntimeAuthority`
3. `EvidenceAuthority`
4. `HistoricalAuthority`
5. `ProjectionAuthority`

No single narrative file is allowed to act as all five simultaneously.
No role assignment grants epistemic truth by itself.

## §4 Multi-axis status model

Single-axis `status = done` is forbidden for governance truth.
Every governed artifact/branch must admit multi-axis state at minimum:

```text
ConstitutionalStatus in {PROPOSED, RATIFIED, SUPERSEDED}
RuntimeStatus in {ABSENT, CARRIER_ONLY, EXECUTABLE, QUARANTINED}
EvidenceStatus in {UNEVIDENCED, PARTIAL, PROVEN, REFUSED, DEFERRED}
ReleaseStatus in {EXPERIMENTAL, ALPHA, STABLE, FROZEN}
```

## §5 Source-of-truth discipline

`docs/14_PR_CHAIN_ROADMAP.md` remains authoritative for chain history and
chain-stage law boundaries. It is not a stand-alone current-state projection
engine.

`README.md`, `docs/README.md`, and `CLAUDE.md` are governed views and must not
assert state that contradicts the machine-readable governance projection.

## §6 Registry and projection contract

Repository state projection must be derived from machine-readable governance
records:

```text
governance/history/amendments.jsonl
governance/registry/artifacts.json
governance/registry/branches.json
governance/registry/dependencies.json
governance/registry/runtime_map.json
governance/registry/evidence_map.json
governance/registry/residuals.json
-> governance/projections/current_state.json
```

## §7 V1 closure and observatory separation

`V1` closure evidence and observatory progression must remain explicitly
non-equivalent unless proven otherwise.

Licensed posture:

```text
OBSERVATORY_PROGRAM.scope = POST_V1_RESEARCH
OBSERVATORY_PROGRAM.does_not_imply = V1_CLOSED
OBSERVATORY_PROGRAM.authority_impact = NONE_ON_V1_CLOSURE
```

## §8 Logical reorganization before physical reorganization

No large path migration is required at this step.

This law permits logical classification (metadata taxonomy and projection)
without renaming existing document IDs or moving existing runtime/data paths.

## §9 Public API boundary posture

Root package API must be stable-kernel-first.
Compatibility re-exports are allowed, but historical PR narration must not be
the primary contract of `src/taaqqul_slot_geometry/__init__.py`.

## §10 Technical residual visibility

At the `REPO-ORG-L0` step the following technical residuals are visible:

1. `GUA_CORE_FREEZE_CANONICAL_SERIALIZATION_NOT_YET_RATIFIED`
2. `GUA_LEGACY_CORE_INTEGRITY_WITNESS_STATIC_TOKEN`
3. `DECLARED_PROJECTION_NOT_YET_COMPUTED`

No claim of final GUA closure is licensed while these residuals remain open.
No claim of computed projection is licensed while
`DECLARED_PROJECTION_NOT_YET_COMPUTED` remains open.

Post-L0 trace note:
`REPO-ORG-P0` is the licensed closure branch for residual (3). Its runtime
closure evidence and residual disposition are governed by machine-readable
records under `governance/registry/` and `governance/projections/`.

## §11 Boundary of this step

`REPO-ORG-L0` does not:

- change constitutional chain position in `docs/14`,
- open observatory runtime (`OBS-D0` and successors),
- add runtime dependencies,
- add ORM schemas/migrations,
- move existing files physically.

## §12 Successor sequencing boundary

This law-only step opens only the following immediate sequence:

```text
REPO-ORG-L0 -> REPO-ORG-R0 -> REPO-ORG-P0
```

`REPO-ORG-L0` does not license direct opening of `SLGE-SDLC-L0`.
