# 69 — Foundational Euclidean Coverage Matrix

> Status: coverage matrix for foundational Euclidean licensing package.
> This matrix tracks closure state across:
> Definition → Contract → Carrier → Gate → Failure Mapping → Tests → Fixtures → Coverage.

| Law / Capability | Definition | Contract | Carrier | Gate | Failure Mapping | Tests | Fixtures | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Origin | ✅ docs/68 §2 | ✅ X0R | ✅ OriginProof | ✅ staged order | ◐ partial | ✅ | ✅ | ✅ |
| Branch | ✅ docs/68 §2 | ✅ X0R | ✅ BranchProof | ✅ staged order | ◐ partial | ✅ | ✅ | ✅ |
| Origin/Branch Link | ✅ docs/68 §2 | ✅ X0R | ✅ OriginBranchLinkProof | ✅ staged order | ◐ partial | ✅ | ✅ | ✅ |
| Differentiating Feature | ✅ docs/68 §2 | ✅ X0R | ✅ DifferentiatingFeatureProof | ✅ | ◐ partial | ✅ | ✅ | ✅ |
| Qadih Difference | ✅ docs/68 §2 | ✅ X0R | ✅ QadihCheckStatus | ✅ | ◐ partial | ✅ | ✅ | ✅ |
| Condition/Sabab/Mani separation | ✅ docs/68 §2 | ✅ X0R | ✅ booleans + checks | ✅ distinct stages | ◐ partial | ✅ | ✅ | ✅ |
| Rank Force Ceiling | ✅ docs/68 §2 | ✅ X0R/X0L | ✅ RankForceCeiling | ✅ | ✅ RANK_EXCEEDS_CEILING | ✅ | ✅ | ✅ |
| Residual visibility and blocking residuals | ✅ docs/68 §2 | ✅ X0R/X0L | ✅ residual carriers | ✅ | ✅ HIDDEN_RESIDUAL/BLOCKING_RESIDUAL_PRESENT | ✅ | ✅ | ✅ |
| Named handoff | ✅ docs/68 §2 | ✅ X0R/X0L | ✅ handoff field | ✅ | ◐ GATE_REQUIRED stage-linked | ✅ | ✅ | ✅ |
| Public carrier invariants (`JumpTestResult`) | ✅ docs/68 §4 | ✅ X0R | ✅ validated dataclass | n/a | ✅ contract error mapping | ✅ negative tests | ✅ | ✅ |
| Public carrier invariants (`EuclideanGateDecision`) | ✅ docs/68 §4 | ✅ X0R | ✅ validated dataclass | n/a | ✅ contract error mapping | ✅ negative tests | ✅ | ✅ |
| Phonetic partition | ✅ docs/70 §2 | ✅ LAW-E1R runtime (`CriticalPartitionRuntimeContract`) | ✅ `PartitionDeclaration` + `PartitionBridgeProof` | ✅ `CriticalPartitionRuntimeContract.evaluate()` | ✅ stage-local + `_LOCAL_FAILURE_MAP` | ✅ `tests/test_law_e1r_critical_partition_contract.py` | ✅ `data/x0r_critical_partition_fixtures.json` | ◐ runtime boundary (no semantic/hukm) |
| Structural partition | ✅ docs/70 §2 | ✅ LAW-E1R runtime (`CriticalPartitionRuntimeContract`) | ✅ `PartitionDeclaration` + `PartitionBridgeProof` | ✅ `CriticalPartitionRuntimeContract.evaluate()` | ✅ stage-local + `_LOCAL_FAILURE_MAP` | ✅ `tests/test_law_e1r_critical_partition_contract.py` | ✅ `data/x0r_critical_partition_fixtures.json` | ◐ runtime boundary (no semantic/hukm) |
| System partition | ✅ docs/70 §2 | ✅ LAW-E1R runtime (`CriticalPartitionRuntimeContract`) | ✅ `PartitionDeclaration` + `PartitionBridgeProof` | ✅ `CriticalPartitionRuntimeContract.evaluate()` | ✅ stage-local + `_LOCAL_FAILURE_MAP` | ✅ `tests/test_law_e1r_critical_partition_contract.py` | ✅ `data/x0r_critical_partition_fixtures.json` | ◐ runtime boundary (no semantic/hukm) |
| Identity property law | ✅ docs/70 §3 | ✅ LAW-E1R runtime (`CriticalPartitionRuntimeContract`) | ✅ `IdentityPropertyConservationProof` | ✅ identity-stage refusal in `evaluate()` | ✅ `IDENTITY_PROPERTY_BROKEN` → `IDENTITY_BROKEN` | ✅ `tests/test_law_e1r_critical_partition_contract.py` | ✅ `data/x0r_critical_partition_fixtures.json` | ◐ runtime boundary (no semantic/hukm) |
| Triadic identity continuity | ✅ docs/70 §3 | ✅ LAW-E1R runtime (`CriticalPartitionRuntimeContract`) | ✅ `TriadicIdentityContinuityProof` | ✅ triadic-stage refusal in `evaluate()` | ✅ `TRIADIC_*` local names → global `FailureCode` | ✅ `tests/test_law_e1r_critical_partition_contract.py` | ✅ `data/x0r_critical_partition_fixtures.json` | ◐ runtime boundary (no semantic/hukm) |
| Necessity-tier law (ḍarūrī/ḥājī/taḥsīnī) | ✅ docs/70 §4 | ✅ LAW-E1R runtime (`CriticalPartitionRuntimeContract`) | ✅ `NecessityTierProof` | ✅ tier-stage checks in `evaluate()` | ✅ tier local names → `GATE_REQUIRED` / `FORBIDDEN_STRAIGHT_LINE` | ✅ `tests/test_law_e1r_critical_partition_contract.py` | ✅ `data/x0r_critical_partition_fixtures.json` | ◐ runtime boundary (no semantic/hukm) |

## Notes

- `◐ partial` means stage-bound mapping exists in runtime, while broad family-wide expansion remains deferred.
- `◐ law-only` means the boundary is ratified as definitions and failure mapping only; runtime carriers/gates remain deferred.
- `◐ runtime boundary` means bounded runtime contract/carrier/gate/test/fixture coverage exists for refusal/transition discipline only; parser, morphology, syntax, semantic, ifādah, mafhūm, hukm, truth, certainty, and reality runtime outputs remain forbidden.
- Unopened rows are intentionally blocked pending dedicated law/contract steps.
- PR #161 (`LAW-E1R-A`) hardened runtime behavior with unconditional identity-break refusal and forbidden handoff token normalization across case/separators/punctuation (including Arabic forms).
