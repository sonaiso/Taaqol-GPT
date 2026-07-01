"""Fixture validation for foundational X0R transition cases.

Origin law          : docs/68_FOUNDATIONAL_EUCLIDEAN_LICENSING_LAWS.md
Branch name         : X0R foundational fixtures
Constitutional chain: docs/68 -> docs/69 -> X0R fixture validation
Category            : Category 4 — Support / fixture tests (docs/52 §4)
"""

from __future__ import annotations

import json
import pathlib

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.core import FailureCode
from taaqqul_slot_geometry.x0r import (
    EuclideanGateStage,
    JumpTestInput,
    QadihCheckStatus,
    ResidualKind,
    TransitionContract,
    TransitionReadinessState,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_FIXTURES = _REPO_ROOT / "data" / "x0r_foundational_transition_fixtures.json"

_SCHEMA_KEYS = frozenset({"fixture_id", "input", "expected"})


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/68_FOUNDATIONAL_EUCLIDEAN_LICENSING_LAWS.md",
        branch_name=branch_name,
        constitutional_chain=("docs/68", "docs/69", "X0RFixtureValidation"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("PromotionWithoutGate", "HiddenResidualApproval"),
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


def _contract() -> TransitionContract:
    return TransitionContract(
        declared_transitions=frozenset(
            {
                ("CellSequence", "BuiltPath", "CELL_TO_BUILT_PATH", "text_understanding"),
                (
                    "CellSequence",
                    "RootWeightPath",
                    "CELL_TO_ROOT_WEIGHT_PATH",
                    "text_understanding",
                ),
            }
        )
    )


def _build_jump(payload: dict[str, object]) -> JumpTestInput:
    return JumpTestInput(
        source_level=str(payload["source_level"]),
        target_level=str(payload["target_level"]),
        transition_name=str(payload["transition_name"]),
        domain=str(payload["domain"]),
        trace_ref=str(payload["trace_ref"]),
        origin=str(payload["origin"]),
        branch=str(payload["branch"]),
        handoff=str(payload["handoff"]),
        rank=int(payload["rank"]),
        rank_ceiling=int(payload["rank_ceiling"]) if payload["rank_ceiling"] is not None else None,
        sufficiency=bool(payload["sufficiency"]),
        necessity=bool(payload["necessity"]),
        preserved_trace=bool(payload["preserved_trace"]),
        residual_visible=bool(payload["residual_visible"]),
        differentiating_feature_verified=bool(payload["differentiating_feature_verified"]),
        qadih_status=QadihCheckStatus[str(payload["qadih_status"])],
        residual_kinds=tuple(ResidualKind[name] for name in payload["residual_kinds"]),
        blocking_residuals=tuple(str(name) for name in payload["blocking_residuals"]),
    )


def test_fixture_pack_exists_and_uses_expected_schema() -> None:
    _declare("x0r fixture schema")
    assert _FIXTURES.exists(), "x0r foundational fixture pack must exist"
    fixtures = _load_fixtures()
    assert isinstance(fixtures, list) and fixtures
    for entry in fixtures:
        assert frozenset(entry.keys()) == _SCHEMA_KEYS
        assert isinstance(entry["fixture_id"], str) and entry["fixture_id"].strip()
        assert isinstance(entry["input"], dict)
        assert isinstance(entry["expected"], dict)


def test_fixture_pack_ids_are_unique() -> None:
    _declare("x0r fixture ids unique")
    ids = [str(entry["fixture_id"]) for entry in _load_fixtures()]
    assert len(ids) == len(set(ids))


def test_fixture_cases_match_runtime_contract_verdict_surface() -> None:
    _declare("x0r fixture runtime alignment")
    contract = _contract()

    for entry in _load_fixtures():
        fixture_id = str(entry["fixture_id"])
        expected = entry["expected"]
        jump = _build_jump(entry["input"])
        verdict = contract.evaluate(jump)

        assert verdict.allowed is expected["allowed"], fixture_id
        assert verdict.readiness_state is TransitionReadinessState[str(expected["readiness_state"])], (
            fixture_id
        )
        if expected["failed_stage"] is None:
            assert verdict.failed_stage is None, fixture_id
        else:
            assert verdict.failed_stage is EuclideanGateStage[str(expected["failed_stage"])], fixture_id
        if expected["failure_code"] is None:
            assert verdict.failure_code is None, fixture_id
        else:
            assert verdict.failure_code is FailureCode[str(expected["failure_code"])], fixture_id
