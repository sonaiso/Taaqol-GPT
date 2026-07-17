# 94 — AUX-ESA-0 Enriched Simulation Agent Boundary Law

> Status: constitutional boundary law document (law-only).
> Scope: constitutional quarantine boundary for `enriched_simulation_agent/` auxiliary kernel.
> Snapshot date: 2026-07-17.

Constitutional origin: `docs/13`, `docs/14`, and `docs/93`.

---

## §1 Constitutional identity

`AUX-ESA-0` is a bounded auxiliary kernel law.

It is admitted as:

```text
AUXILIARY_KERNEL_ONLY
QUARANTINED_FROM_CONSTITUTIONAL_CHAIN_RUNTIME
```

It is not admitted as:

```text
CHAIN_ADVANCING_LAYER
BRIDGE_PROOF_LAYER
```

## §2 Governing boundary equation

```text
AUX_ESA_0_BOUNDARY_EQUATION :=
  MERGED_AUXILIARY_KERNEL
  AND LAW_ONLY
  AND ROADMAP_UNLOCK = FORBIDDEN_AND_NOT_PRESENT
  AND CORE_RUNTIME_MUTATION = FORBIDDEN_AND_NOT_PRESENT
  AND LINGUISTIC_TO_KNOWLEDGE_BRIDGE = FORBIDDEN_AND_NOT_PRESENT
  AND WORDCAPABILITY_TO_RELATION_IFADAH_HUKM = FORBIDDEN_AND_NOT_PRESENT
  AND CONSTITUTIONAL_HARNESS_ADMISSION = NOT_PRESENT
```

Any claim violating one or more terms in this equation is an `UNLICENSED_OPENING`.

## §3 Auxiliary-local allowance surface

`AUX-ESA-0` may provide local simulation governance checks within
`enriched_simulation_agent/` only, including:

- transition verdicting (`ACCEPT`/`DEFER`/`BLOCK`),
- local preservation/refutation checks,
- local validation traces and residual checks.

This allowance does not grant constitutional chain admission.

## §4 Forbidden transitions and outputs

The following are forbidden in `AUX-ESA-0`:

```text
FORBIDDEN_TRANSITIONS = {
  AUX_ESA_0 -> docs/14_chain_unlock,
  AUX_ESA_0 -> core_runtime_mutation,
  AUX_ESA_0 -> linguistic_to_knowledge_bridge_proof,
  AUX_ESA_0 -> WordCapability_to_Relation,
  AUX_ESA_0 -> WordCapability_to_Ifadah,
  AUX_ESA_0 -> WordCapability_to_Hukm
}
```

```text
FORBIDDEN_OUTPUTS = {
  ConstitutionalAdmissionCertificate,
  RoadmapAdvanceClaim,
  BridgeLicensedClaim,
  RelationUnlockedByAux,
  IfadahUnlockedByAux,
  HukmUnlockedByAux,
  GlobalConstitutionalVerdict
}
```

## §5 Rank and residual discipline

```text
MAX_RANK_FOR_AUX_LAW_STEP = ZERO
RESIDUAL_VISIBILITY = REQUIRED
HIDDEN_RESIDUALS_ON_APPROVAL = FORBIDDEN
DEFAULT_FAILURE_CODE_ON_BOUNDARY_BREACH = UNLICENSED_OPENING
```

AUX law checks may succeed locally while constitutional admission remains unopened.

## §6 Runtime embargo in this step

```text
RUNTIME_NOT_OPENED = {
  src/taaqqul_slot_geometry/**,
  tests/support/constitutional_case.py admission path,
  docs/14 chain mutation,
  bridge runtime from linguistic subsystem to knowledge subsystem,
  relation/ifadah/hukm constitutional unlock path
}
```

`AUX-ESA-0` boundary law introduces no runtime code in core chain modules and no
constitutional chain-state mutation.

## §7 Deferred admission obligations

Before any future constitutional admission of auxiliary simulation claims,
a dedicated follow-up path is required:

1. explicit admission record in authoritative chain governance,
2. constitutional harness migration rule,
3. staged closure of simulation-law obligations:
   - `IdentitySimulationLaw`,
   - `CompositionSimulationLaw`,
   - `OperationHomomorphismLaw`,
   - `ResidualReflectionLaw`,
   - `CoverageContractLaw`,
   - `NonTrivialityStrengtheningLaw`.

Until all are satisfied, `AUX-ESA-0` remains quarantined.

## §8 Test obligations

Acceptance tests for this law must prove:

1. this document exists and declares law-only boundary status,
2. boundary equation terms are explicitly present,
3. roadmap/core/bridge/relation-ifadah-hukm unlocks remain forbidden,
4. rank-zero and residual-visibility constraints are explicit,
5. deferred simulation-law obligations are explicitly listed.

## §9 Trace

Trace path:

`docs/13` -> `docs/14` -> `docs/93` -> `docs/94`.

`docs/94` is a boundary law for auxiliary quarantine discipline.
It is not constitutional admission and not a bridge proof.
