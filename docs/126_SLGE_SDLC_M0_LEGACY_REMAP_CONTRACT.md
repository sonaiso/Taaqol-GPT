# SLGE-SDLC-M0 Legacy Repository Lifecycle Remap Contract

## Origin

- Origin law: `docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md`
- Predecessor branch: `SLGE-SDLC-R0`
- Current branch: `SLGE-SDLC-M0`
- Next and only permitted successor: `SLGE-SDLC-E0`

## Purpose

`SLGE-SDLC-M0` classifies existing repository artifacts into the ratified lifecycle ontology without fabricating historical lifecycle approvals.

- `LegacyExistence != HistoricallyLicensedTransition`
- `CurrentArtifactPresence != ProofOfHistoricalMCLT`
- `Remap != RetroactiveRatification`
- `Classification != HistoricalProof`

M0 is an evidence-backed legacy classification layer, not a lifecycle runtime execution layer.

## Machine Contract Surfaces

- `governance/registry/slge_sdlc_m0_legacy_remap.json`
- `schemas/governance/slge_sdlc_m0_legacy_remap.schema.json`
- `tests/test_slge_sdlc_m0_legacy_remap.py`

These surfaces define:

- deterministic eligible-artifact enumeration,
- full coverage ledger,
- typed remap decisions (`KEEP`, `RETYPE`, `REORDER`, `QUARANTINE`, `REBUILD`),
- historical-transition status posture,
- remap evidence records,
- fixture-vs-authoritative separation,
- rank-mapping boundary posture,
- authority supporting-vs-executing distinction,
- residual visibility for unproven history.

## Fixture vs Authoritative Boundary

The contract enforces a structural split:

- `ContractFixture` is schema/test/example material only.
- `AuthoritativeLegacyRemap` is governance classification authority.

Therefore:

- `ContractFixture != GovernanceAuthority`
- `ContractFixture != HistoricalProof`
- `ContractFixture != AuthoritativeLegacyRemap`

## Historical Proof Boundary

M0 requires explicit historical-transition status per remap record and forbids synthetic historical certification.

- `CurrentArtifactClassification != HistoricalTransitionProof`
- `UnknownHistory -> ResidualVisibility`
- `NoSyntheticHistoricalMCLT`

## Coverage Law

Coverage is deterministic and exhaustive over the eligible legacy artifact set:

- Every eligible artifact appears exactly once in the coverage ledger.
- Every covered artifact has exactly one primary decision.
- Out-of-scope entries require explicit reasons.
- Silent omission is forbidden.

## Rank and Authority Boundary

M0 keeps rank ontologies and authority surfaces non-conflated.

- `SameLabel != SameRankSemantics`
- `SupportingSurface != ExecutingSurface`
- `DefinesProjectionLaw != ExecutesProjection`

Unlicensed mappings remain explicit residuals.

## Quarantine and Rebuild Semantics

- `QUARANTINE` preserves historical visibility but refuses current lifecycle execution authority.
- `REBUILD` records insufficiency and required reconstruction conditions without performing runtime rebuild.

Therefore:

- `Quarantine != Deletion`
- `RebuildDecision != RebuiltArtifact`

## Non-Runtime Boundary

M0 does not open:

- lifecycle transition execution runtime,
- lifecycle state reducer runtime,
- lifecycle PR enforcement runtime,
- lifecycle closure audit runtime,
- OBS-D0,
- ORM/database/persistence.

`REPO-ORG-P0` remains the repository current-state projection runtime authority.

## Residual Policy

M0 resolves the R0 handoff residual for legacy remap staging and preserves unresolved historical uncertainty as explicit visible residuals targeted to successor branches.

## Successor Boundary

After M0 completion, only `SLGE-SDLC-E0` is licensed as immediate successor.
No E0 runtime is implemented by M0.
