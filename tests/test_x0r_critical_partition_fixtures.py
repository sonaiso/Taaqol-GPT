"""Fixture validation for LAW-E1R critical partition runtime cases.

Origin law          : docs/70_CRITICAL_LINGUISTIC_SYSTEM_PARTITION_LAWS.md
Branch name         : LAW-E1R critical partition fixtures
Constitutional chain: docs/70 -> LAW-E1R -> fixture-backed runtime refusals
Category            : Category 4 — Support / fixture tests (docs/52 §4)
"""

from __future__ import annotations

import json
import pathlib

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.core import FailureCode
from taaqqul_slot_geometry.x0r import (
    CriticalPartitionRuntimeContract,
    CriticalPartitionStage,
    IdentityPropertyConservationProof,
    NecessityTier,
    NecessityTierProof,
    PartitionBridgeProof,
    PartitionDeclaration,
    PartitionKind,
    PartitionReadinessState,
    TriadicIdentityContinuityProof,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_FIXTURES = _REPO_ROOT / "data" / "x0r_critical_partition_fixtures.json"
_SCHEMA_KEYS = frozenset({"fixture_id", "input", "expected"})


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/70_CRITICAL_LINGUISTIC_SYSTEM_PARTITION_LAWS.md",
        branch_name=branch_name,
        constitutional_chain=("docs/70", "LAW-E1R", "FixtureValidation"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("ParserRuntime", "SemanticClosureClaim"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _load_fixtures() -> list[dict[str, object]]:
    return json.loads(_FIXTURES.read_text(encoding="utf-8"))


def _contract() -> CriticalPartitionRuntimeContract:
    return CriticalPartitionRuntimeContract(
        declared_partitions=frozenset(
            {
                (PartitionKind.PHONETIC, "text_understanding", "critical_partition"),
                (PartitionKind.STRUCTURAL, "text_understanding", "critical_partition"),
            }
        ),
        declared_bridges=frozenset(
            {
                (
                    PartitionKind.PHONETIC,
                    PartitionKind.STRUCTURAL,
                    "text_understanding",
                    "critical_partition",
                    "PHONETIC_TO_STRUCTURAL",
                ),
                (
                    PartitionKind.STRUCTURAL,
                    PartitionKind.SYSTEMIC,
                    "text_understanding",
                    "critical_partition",
                    "STRUCTURAL_TO_SYSTEMIC",
                ),
            }
        ),
    )


def _build_declaration(payload: dict[str, object]) -> PartitionDeclaration:
    return PartitionDeclaration(
        partition_kind=PartitionKind[str(payload["partition_kind"])],
        domain=str(payload["domain"]),
        scope=str(payload["scope"]),
        trace_ref=str(payload["trace_ref"]),
        residual_visible=bool(payload["residual_visible"]),
    )


def _build_bridge(payload: dict[str, object]) -> PartitionBridgeProof:
    return PartitionBridgeProof(
        source_partition=PartitionKind[str(payload["source_partition"])],
        target_partition=PartitionKind[str(payload["target_partition"])],
        domain=str(payload["domain"]),
        scope=str(payload["scope"]),
        trace_ref=str(payload["trace_ref"]),
        residual_visible=bool(payload["residual_visible"]),
        bridge_name=str(payload["bridge_name"]),
    )


def _build_identity(payload: dict[str, object]) -> IdentityPropertyConservationProof:
    return IdentityPropertyConservationProof(
        identity_anchor=str(payload["identity_anchor"]),
        preserved_properties=tuple(str(v) for v in payload["preserved_properties"]),
        licensed_variants=tuple(str(v) for v in payload["licensed_variants"]),
        broken_properties=tuple(str(v) for v in payload["broken_properties"]),
        trace_ref=str(payload["trace_ref"]),
    )


def _build_triadic(payload: dict[str, object]) -> TriadicIdentityContinuityProof:
    return TriadicIdentityContinuityProof(
        previous_identity_ref=str(payload["previous_identity_ref"]),
        current_identity_ref=str(payload["current_identity_ref"]),
        next_identity_ref=str(payload["next_identity_ref"]),
        previous_current_link=str(payload["previous_current_link"]),
        current_next_link=str(payload["current_next_link"]),
        bridge_coherent=bool(payload["bridge_coherent"]),
        residual_visible=bool(payload["residual_visible"]),
    )


def _build_tier(payload: dict[str, object]) -> NecessityTierProof:
    return NecessityTierProof(
        tier=NecessityTier[str(payload["tier"])],
        declared_cause=str(payload["declared_cause"]),
        evidence_ref=str(payload["evidence_ref"]),
        transition_ref=str(payload["transition_ref"]),
        residual_visible=bool(payload["residual_visible"]),
    )


def test_fixture_pack_exists_and_uses_expected_schema() -> None:
    _declare("LAW-E1R fixture schema")
    assert _FIXTURES.exists(), "LAW-E1R fixture pack must exist"
    fixtures = _load_fixtures()
    assert isinstance(fixtures, list) and fixtures
    for entry in fixtures:
        assert frozenset(entry.keys()) == _SCHEMA_KEYS
        assert isinstance(entry["fixture_id"], str) and entry["fixture_id"].strip()
        assert isinstance(entry["input"], dict)
        assert isinstance(entry["expected"], dict)


def test_fixture_pack_ids_are_unique() -> None:
    _declare("LAW-E1R fixture ids unique")
    fixture_ids = [str(entry["fixture_id"]) for entry in _load_fixtures()]
    assert len(fixture_ids) == len(set(fixture_ids))


def test_fixture_cases_match_runtime_contract_surface() -> None:
    _declare("LAW-E1R fixture runtime alignment")
    contract = _contract()

    for entry in _load_fixtures():
        fixture_id = str(entry["fixture_id"])
        payload = entry["input"]
        expected = entry["expected"]

        verdict = contract.evaluate(
            declaration=_build_declaration(payload["declaration"]),
            bridge_proof=_build_bridge(payload["bridge"]),
            identity_proof=_build_identity(payload["identity"]),
            triadic_proof=_build_triadic(payload["triadic"]),
            tier_proof=_build_tier(payload["tier"]),
            handoff=str(payload["handoff"]),
            residuals=tuple(str(v) for v in payload["residuals"]),
        )

        assert verdict.partition_allowed is expected["partition_allowed"], fixture_id
        assert (
            verdict.readiness_state
            is PartitionReadinessState[str(expected["readiness_state"])]
        ), fixture_id

        if expected["failed_stage"] is None:
            assert verdict.failed_stage is None, fixture_id
        else:
            assert (
                verdict.failed_stage is CriticalPartitionStage[str(expected["failed_stage"])]
            ), fixture_id

        assert verdict.local_failure_name == expected["local_failure_name"], fixture_id

        if expected["failure_code"] is None:
            assert verdict.failure_code is None, fixture_id
        else:
            assert verdict.failure_code is FailureCode[str(expected["failure_code"])], fixture_id
