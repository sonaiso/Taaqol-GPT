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
| Phonetic partition | ✅ docs/70 §2 | ❌ law-only (runtime deferred) | ❌ | ❌ | ✅ docs/70 §5 | ✅ docs/70 acceptance | ❌ | ◐ law-only |
| Structural partition | ✅ docs/70 §2 | ❌ law-only (runtime deferred) | ❌ | ❌ | ✅ docs/70 §5 | ✅ docs/70 acceptance | ❌ | ◐ law-only |
| System partition | ✅ docs/70 §2 | ❌ law-only (runtime deferred) | ❌ | ❌ | ✅ docs/70 §5 | ✅ docs/70 acceptance | ❌ | ◐ law-only |
| Identity property law | ✅ docs/70 §3 | ❌ law-only (runtime deferred) | ❌ | ❌ | ✅ docs/70 §5 | ✅ docs/70 acceptance | ❌ | ◐ law-only |
| Triadic identity continuity | ✅ docs/70 §3 | ❌ law-only (runtime deferred) | ❌ | ❌ | ✅ docs/70 §5 | ✅ docs/70 acceptance | ❌ | ◐ law-only |
| Necessity-tier law (ḍarūrī/ḥājī/taḥsīnī) | ✅ docs/70 §4 | ❌ law-only (runtime deferred) | ❌ | ❌ | ✅ docs/70 §5 | ✅ docs/70 acceptance | ❌ | ◐ law-only |

## Notes

- `◐ partial` means stage-bound mapping exists in runtime, while broad family-wide expansion remains deferred.
- `◐ law-only` means the boundary is ratified as definitions and failure mapping only; runtime carriers/gates remain deferred.
- Unopened rows are intentionally blocked pending dedicated law/contract steps.
