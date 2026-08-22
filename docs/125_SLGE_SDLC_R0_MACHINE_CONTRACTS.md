# SLGE-SDLC-R0 Machine Contracts Boundary

## Origin

- Origin law: `docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md`
- Chain position: `SLGE-SDLC-L0 -> SLGE-SDLC-R0 -> SLGE-SDLC-M0`

## Purpose

`SLGE-SDLC-R0` introduces machine-readable lifecycle contracts only.

- `LawExists != MachineContractExists`
- `MachineContractExists != LifecycleEngineExists`
- `SchemaValidity != TransitionApproval`

This step defines lifecycle ontology and contract surfaces without opening transition execution runtime.

## Contract Surfaces

`governance/registry/slge_sdlc_r0_contracts.json` and
`schemas/governance/slge_sdlc_r0_contracts.schema.json` define:

- `ProjectArtifactRecord`
- `LifecycleSlotRecord`
- `LifecycleTransitionContractRecord`
- `EvidenceRequirementRecord`
- `LifecycleEventRecord` (structural only)
- `GateReference` / gate-decision shape reference
- `ResidualRecord` / residual-delta references
- `TraceRecord`
- `MCLT` contract shape

## Typed Evidence Boundary

Evidence is modeled by domain/kind/target rather than a single overloaded status.

The registry keeps constitutional and empirical tracks distinct:

- `ConstitutionalRatificationEvidence` for law ratification posture
- `EpistemicClaimEvidence` for empirical truth posture

Therefore:

- `ConstitutionalRatificationEvidence != EmpiricalTruthEvidence`

## Authority Separation

R0 preserves authority role separation:

- `LawAuthority`
- `ProjectionContractAuthority`
- `ProjectionRuntimeAuthority`
- `CurrentStateProjectionAuthority`
- `EvidenceAuthority`
- `HistoricalAuthority`
- `RuntimeAuthority`

Critical constraint:

- `DefinesProjectionLaw != ExecutesProjection`
- `RatifiedLaw != ProjectionRuntimeAuthority`

`REPO-ORG-P0` remains the runtime holder for deterministic current-state projection.

## Maturity Axes

R0 keeps lifecycle and maturity dimensions independent:

- `LifecycleSlot`
- `EpistemicRank`
- `ConstitutionalMaturity`
- `RuntimeMaturity`
- `ReleaseMaturity`
- `GeneralityScope`

No truth claim is inferred from enum order.

## Non-Runtime Boundary

R0 forbids:

- lifecycle transition execution
- lifecycle state reducer execution
- PR enforcement execution
- closure-ledger execution
- historical certificate fabrication for legacy artifacts

These remain deferred by visible residuals to:

- `SLGE-SDLC-M0`
- `SLGE-SDLC-E0`
- `SLGE-SDLC-P0`
- `SLGE-SDLC-G0`
- `SLGE-SDLC-C0`
