"""Tests for the ConstitutionalMatrixEngine runtime surface."""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.transition_state import TransitionState
from taaqqul_slot_geometry.x0r.constitutional_matrix_engine import (
    ClosureVerdict,
    ConstitutionalMatrixEngine,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_MATRIX_JSON = _REPO_ROOT / "data" / "constitutional_matrix_38.json"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/52_CONSTITUTIONAL_TEST_ORIGIN_COVENANT.md",
        branch_name=f"PR-132-CONSTITUTIONAL-MATRIX-ENGINE ({branch_note})",
        constitutional_chain=("docs/52", "docs/13", "docs/14"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ChainMutationClaim",
            "LawAmendmentClaim",
            "UnboundedRuntimeInference",
        ),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _engine() -> ConstitutionalMatrixEngine:
    return ConstitutionalMatrixEngine.from_json_file(_MATRIX_JSON)


def test_matrix_loads_and_verifies() -> None:
    _declare("matrix verification")
    engine = _engine()
    assert len(engine.matrix.operations) == 38

    verification = engine.verify()
    assert verification.all_origins_defined is True
    assert verification.acyclic_dag is True
    assert verification.no_orphans is True
    assert verification.euclidean_gradient is True
    assert verification.residual_vocabulary_count == 115


def test_transition_success_from_predication_to_ifadah() -> None:
    _declare("predication to ifadah handoff")
    engine = _engine()

    result = engine.evaluate_transition(
        current_operation_id="OP-35",
        inputs={
            "RelationCandidate": object(),
            "SpeechForce": "KHABAR",
            "ContextualSufficiency": True,
        },
        evidence={"visible": True, "evidence_id": "ev-1"},
    )

    assert result.next_operation_id == "OP-36"
    assert result.closure_verdict is ClosureVerdict.CLOSED
    assert result.failure_code is None
    assert result.trace_entry.gate_transition_state is TransitionState.APPROVED


def test_transition_deferred_on_missing_inputs() -> None:
    _declare("deferred on missing inputs")
    engine = _engine()

    result = engine.evaluate_transition(
        current_operation_id="OP-35",
        inputs={"RelationCandidate": object()},
        evidence={"visible": True},
    )

    assert result.next_operation_id is None
    assert result.closure_verdict is ClosureVerdict.DEFERRED
    assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
    assert any(item.startswith("MISSING_INPUT:") for item in result.residuals)


def test_transition_refused_on_unknown_operation() -> None:
    _declare("refused on unknown operation")
    engine = _engine()

    result = engine.evaluate_transition(
        current_operation_id="OP-99",
        inputs={},
        evidence={"visible": True},
    )

    assert result.next_operation_id is None
    assert result.closure_verdict is ClosureVerdict.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED
    assert result.trace_entry.gate_transition_state is TransitionState.REJECTED


def test_terminal_operation_returns_closed_without_successor() -> None:
    _declare("terminal closure without successor")
    engine = _engine()

    result = engine.evaluate_transition(
        current_operation_id="OP-38",
        inputs={
            "HukmCandidate": object(),
            "ManatCandidate": object(),
            "TanzilCandidate": object(),
        },
        evidence={"visible": True},
    )

    assert result.next_operation_id is None
    assert result.closure_verdict is ClosureVerdict.CLOSED
    assert result.failure_code is None
