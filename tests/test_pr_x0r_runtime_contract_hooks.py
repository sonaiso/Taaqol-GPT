"""Constitutional tests for PR-X0R runtime contract hooks.

Origin law          : docs/14 Amendment-32 (PR-X0R)
Branch name         : PR-X0R Runtime Contract Hooks
Constitutional chain: docs/14 -> Amendment-32 -> Runtime contract hooks
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re
from typing import Literal

import pytest

from taaqqul_slot_geometry.core import FailureCode
from taaqqul_slot_geometry.x0r import (
    BranchProof,
    DifferentiatingFeatureProof,
    EuclideanGateDecision,
    EuclideanGateStage,
    EuclideanTransitionContract,
    JumpTestContractError,
    JumpTestInput,
    JumpTestResult,
    MinimalCompleteRequirement,
    OriginBranchLinkProof,
    OriginProof,
    QadihCheckStatus,
    RankForceCeiling,
    ResidualKind,
    TransitionContract,
    TransitionReadinessState,
)

ORIGIN_LAW = "docs/14 Amendment-32 (PR-X0R — Runtime Contract Hooks)"
BRANCH_NAME = "PR-X0R Runtime Contract Hooks"
CONSTITUTIONAL_CHAIN = ("docs/14", "Amendment-32", "Runtime contract hooks")
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"
_BASE_STAGE_RANK = 3
_BASE_RANK_CEILING = 5


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


def _valid_jump(**kwargs: object) -> JumpTestInput:
    defaults: dict[str, object] = {
        "source_level": "CellSequence",
        "target_level": "BuiltPath",
        "transition_name": "CELL_TO_BUILT_PATH",
        "domain": "text_understanding",
        "trace_ref": "trace://x0r/001",
        "origin": "asl://cell-sequence",
        "branch": "far://built-path",
        "handoff": "handoff://x0r/jump/1",
        "rank": 3,
        "rank_ceiling": 5,
        "sufficiency": True,
        "necessity": True,
        "preserved_trace": True,
        "residual_visible": True,
        "differentiating_feature_verified": True,
        "qadih_status": QadihCheckStatus.CLEAR,
        "residual_kinds": (ResidualKind.NON_BLOCKING,),
        "blocking_residuals": (),
    }
    defaults.update(kwargs)
    return JumpTestInput(**defaults)


def test_declares_identity_fields_for_pr_x0r_surface() -> None:
    assert ORIGIN_LAW
    assert BRANCH_NAME
    assert CONSTITUTIONAL_CHAIN


def test_default_unsupported_transition_is_forbidden_straight_line() -> None:
    verdict = _contract().evaluate(
        _valid_jump(
            source_level="Silence",
            target_level="Motion",
            transition_name="UNDECLARED_DIRECT_MOVE",
            trace_ref="trace://x0r/002",
        )
    )
    assert verdict.allowed is False
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert verdict.failed_stage is EuclideanGateStage.ORIGIN


def test_blocking_or_contradictory_residuals_block_transition() -> None:
    contract = _contract()

    blocking = contract.evaluate(
        _valid_jump(
            trace_ref="trace://x0r/003",
            residual_kinds=(ResidualKind.BLOCKING,),
        )
    )
    contradictory = contract.evaluate(
        _valid_jump(
            trace_ref="trace://x0r/004",
            residual_kinds=(ResidualKind.CONTRADICTORY,),
        )
    )

    assert blocking.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert blocking.readiness_state is TransitionReadinessState.BLOCKED
    assert contradictory.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert contradictory.readiness_state is TransitionReadinessState.BLOCKED


def test_domain_and_trace_are_not_optional() -> None:
    contract = _contract()
    missing_domain = contract.evaluate(_valid_jump(domain="", trace_ref="trace://x0r/006"))
    missing_trace = contract.evaluate(_valid_jump(trace_ref=""))
    assert missing_domain.failure_code is FailureCode.DOMAIN_MISSING
    assert missing_domain.failed_stage is EuclideanGateStage.DOMAIN
    assert missing_trace.failure_code is FailureCode.TRACE_MISSING
    assert missing_trace.failed_stage is EuclideanGateStage.TRACE


def test_path_matrix_allows_multiple_declared_paths_after_cellsequence() -> None:
    contract = _contract()
    built_path = contract.evaluate(_valid_jump())
    root_weight_path = contract.evaluate(
        _valid_jump(
            target_level="RootWeightPath",
            transition_name="CELL_TO_ROOT_WEIGHT_PATH",
            trace_ref="trace://x0r/007",
            branch="far://root-weight-path",
        )
    )
    assert built_path.allowed is True
    assert built_path.readiness_state is TransitionReadinessState.LINK_READY
    assert root_weight_path.allowed is True


def test_jump_qadih_truth_table_is_explicit() -> None:
    contract = _contract()

    unchecked = contract.evaluate(
        _valid_jump(
            trace_ref="trace://x0r/qadih/unchecked",
            qadih_status=QadihCheckStatus.UNCHECKED,
        )
    )
    blocking = contract.evaluate(
        _valid_jump(trace_ref="trace://x0r/qadih/blocking", qadih_status=QadihCheckStatus.BLOCKING)
    )
    clear = contract.evaluate(
        _valid_jump(trace_ref="trace://x0r/qadih/clear", qadih_status=QadihCheckStatus.CLEAR)
    )
    residual = contract.evaluate(
        _valid_jump(trace_ref="trace://x0r/qadih/residual", qadih_status=QadihCheckStatus.RESIDUAL)
    )

    assert unchecked.readiness_state is TransitionReadinessState.DEFERRED
    assert unchecked.failure_code is FailureCode.QADIH_DIFFERENCE_UNCHECKED
    assert blocking.readiness_state is TransitionReadinessState.BLOCKED
    assert blocking.failure_code is FailureCode.QADIH_DIFFERENCE_BLOCKING
    assert clear.allowed is True
    assert residual.readiness_state is TransitionReadinessState.DEFERRED
    assert residual.failure_code is FailureCode.GATE_REQUIRED


def test_jump_differentiating_feature_is_runtime_stage() -> None:
    result = _contract().evaluate(
        _valid_jump(
            trace_ref="trace://x0r/diff/1",
            differentiating_feature_verified=False,
        )
    )
    assert result.allowed is False
    assert result.readiness_state is TransitionReadinessState.DEFERRED
    assert result.failed_stage is EuclideanGateStage.DIFFERENTIATING_FEATURE


def test_jump_result_surface_has_no_silent_success_or_failure() -> None:
    contract = _contract()
    approved = contract.evaluate(_valid_jump())
    refused = contract.evaluate(
        _valid_jump(
            trace_ref="trace://x0r/008",
            blocking_residuals=("incomplete evidence",),
        )
    )
    assert approved.trace_ref.startswith("trace://")
    assert approved.residual_kinds
    assert approved.failure_code is None

    assert refused.trace_ref.startswith("trace://")
    assert refused.failure_code is not None
    assert refused.blocking_residuals


def test_jump_result_rejects_contradictory_public_surface() -> None:
    contract = _contract()

    with pytest.raises(JumpTestContractError):
        JumpTestResult(
            allowed=True,
            readiness_state=TransitionReadinessState.LINK_READY,
            failure_code=FailureCode.GATE_REQUIRED,
            failed_stage=None,
            domain="text_understanding",
            trace_ref="trace://x0r/jump/invariant/1",
            transition_name="CELL_TO_BUILT_PATH",
            source_level="CellSequence",
            target_level="BuiltPath",
            residual_policy=contract.residual_policy,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )

    with pytest.raises(JumpTestContractError):
        JumpTestResult(
            allowed=True,
            readiness_state=TransitionReadinessState.LINK_READY,
            failure_code=None,
            failed_stage=EuclideanGateStage.QADIH,
            domain="text_understanding",
            trace_ref="trace://x0r/jump/invariant/2",
            transition_name="CELL_TO_BUILT_PATH",
            source_level="CellSequence",
            target_level="BuiltPath",
            residual_policy=contract.residual_policy,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )

    with pytest.raises(JumpTestContractError):
        JumpTestResult(
            allowed=False,
            readiness_state=TransitionReadinessState.LINK_READY,
            failure_code=FailureCode.GATE_REQUIRED,
            failed_stage=EuclideanGateStage.QADIH,
            domain="text_understanding",
            trace_ref="trace://x0r/jump/invariant/3",
            transition_name="CELL_TO_BUILT_PATH",
            source_level="CellSequence",
            target_level="BuiltPath",
            residual_policy=contract.residual_policy,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )

    with pytest.raises(JumpTestContractError):
        JumpTestResult(
            allowed=False,
            readiness_state=TransitionReadinessState.BLOCKED,
            failure_code=FailureCode.GATE_REQUIRED,
            failed_stage=None,
            domain="text_understanding",
            trace_ref="trace://x0r/jump/invariant/4",
            transition_name="CELL_TO_BUILT_PATH",
            source_level="CellSequence",
            target_level="BuiltPath",
            residual_policy=contract.residual_policy,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )

    with pytest.raises(JumpTestContractError):
        JumpTestResult(
            allowed=False,
            readiness_state=TransitionReadinessState.BLOCKED,
            failure_code=None,
            failed_stage=EuclideanGateStage.QADIH,
            domain="text_understanding",
            trace_ref="trace://x0r/jump/invariant/5",
            transition_name="CELL_TO_BUILT_PATH",
            source_level="CellSequence",
            target_level="BuiltPath",
            residual_policy=contract.residual_policy,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )


def test_euclidean_gate_decision_rejects_contradictory_public_surface() -> None:
    with pytest.raises(JumpTestContractError):
        EuclideanGateDecision(
            transition_allowed=True,
            readiness_state=TransitionReadinessState.LINK_READY,
            failed_stage=EuclideanGateStage.QADIH,
            failure_code=None,
            rank=3,
            residuals=("visible:deferred",),
            handoff="handoff://x0r/decision/invariant/1",
        )

    with pytest.raises(JumpTestContractError):
        EuclideanGateDecision(
            transition_allowed=True,
            readiness_state=TransitionReadinessState.LINK_READY,
            failed_stage=None,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=3,
            residuals=("visible:deferred",),
            handoff="handoff://x0r/decision/invariant/2",
        )

    with pytest.raises(JumpTestContractError):
        EuclideanGateDecision(
            transition_allowed=False,
            readiness_state=TransitionReadinessState.LINK_READY,
            failed_stage=EuclideanGateStage.QADIH,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=3,
            residuals=("visible:deferred",),
            handoff="handoff://x0r/decision/invariant/3",
        )

    with pytest.raises(JumpTestContractError):
        EuclideanGateDecision(
            transition_allowed=False,
            readiness_state=TransitionReadinessState.BLOCKED,
            failed_stage=None,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=3,
            residuals=("visible:deferred",),
            handoff="handoff://x0r/decision/invariant/4",
        )

    with pytest.raises(JumpTestContractError):
        EuclideanGateDecision(
            transition_allowed=False,
            readiness_state=TransitionReadinessState.BLOCKED,
            failed_stage=EuclideanGateStage.QADIH,
            failure_code=None,
            rank=3,
            residuals=("visible:deferred",),
            handoff="handoff://x0r/decision/invariant/5",
        )


def test_surface_stays_generic_without_linguistic_runtime_functions() -> None:
    module_dict = __import__(
        "taaqqul_slot_geometry.x0r.transition_contract", fromlist=["dummy"]
    ).__dict__
    for forbidden_name in (
        "parse_arabic",
        "detect_root",
        "detect_weight",
        "infer_meaning",
        "classify_particle",
    ):
        assert forbidden_name not in module_dict


def test_pr_x0r_is_marked_done_in_chain_table_and_claude_staging() -> None:
    doc_14 = _DOC_14.read_text(encoding="utf-8")
    claude_md = _CLAUDE_MD.read_text(encoding="utf-8")

    done_pattern = re.compile(r"PR-X0R\s+Runtime Contract Hooks\s+✓ done")

    assert done_pattern.search(doc_14) is not None
    assert done_pattern.search(claude_md) is not None


def _minimal_complete(
    *,
    current_stage_rank: int = _BASE_STAGE_RANK,
    max_required_stage_rank: int = _BASE_STAGE_RANK,
    requested_state: Literal["candidate", "deferred", "licensed"] = "candidate",
    candidate_or_deferred_sufficient: bool = True,
    missing_requirements: tuple[str, ...] = (),
    rank_ceiling: int | None = _BASE_RANK_CEILING,
) -> MinimalCompleteRequirement:
    return MinimalCompleteRequirement(
        current_stage_rank=current_stage_rank,
        max_required_stage_rank=max_required_stage_rank,
        requested_state=requested_state,
        candidate_or_deferred_sufficient=candidate_or_deferred_sufficient,
        missing_requirements=missing_requirements,
        rank_ceiling=rank_ceiling,
    )


def _euclidean_contract(**kwargs: object) -> EuclideanTransitionContract:
    defaults: dict[str, object] = {
        "domain": "text_understanding",
        "trace_ref": "trace://x0r/euclidean/1",
        "origin_proof": OriginProof(
            origin_ref="asl/base_rule",
            preserved_identity=True,
            domain="text_understanding",
            trace_ref="trace://x0r/euclidean/1",
            rank=3,
        ),
        "branch_proof": BranchProof(
            branch_ref="far/derived_case",
            domain="text_understanding",
            trace_ref="trace://x0r/euclidean/1",
            rank=3,
        ),
        "linking_proof": OriginBranchLinkProof(
            origin_ref="asl/base_rule",
            branch_ref="far/derived_case",
            origin_to_branch_linked=True,
            branch_to_origin_linked=True,
            reversible_to_origin=True,
        ),
        "differentiating_feature": DifferentiatingFeatureProof(
            feature_ref="feature://distinguishing",
            verified=True,
        ),
        "common_illah": "shared causal bridge",
        "effective_description": "effective operational descriptor",
        "qadih_status": QadihCheckStatus.CLEAR,
        "condition": True,
        "sabab": True,
        "preventer": False,
        "evidence_refs": ("evidence://x0r/1",),
        "residuals": ("visible:deferred",),
        "rank": 3,
        "minimal_complete_requirement": _minimal_complete(),
        "rank_force_ceiling": RankForceCeiling(
            evidence_rank=5,
            identity_rank=5,
            gate_rank=5,
            closure_rank=5,
            residual_rank_ceiling=5,
            explicit_rank_ceiling=5,
        ),
        "handoff": "handoff://x0r/euclidean",
    }
    defaults.update(kwargs)
    return EuclideanTransitionContract(**defaults)


def _assert_branch_test_metadata(branch_case: str) -> None:
    assert ORIGIN_LAW
    assert branch_case
    assert CONSTITUTIONAL_CHAIN


def test_euclidean_complete_contract_passes() -> None:
    _assert_branch_test_metadata("euclidean complete contract pass")
    contract = _euclidean_contract()
    decision = contract.evaluate_gate()
    assert decision.transition_allowed is True
    assert decision.readiness_state is TransitionReadinessState.LINK_READY


def test_euclidean_stage_order_stops_at_first_failure() -> None:
    _assert_branch_test_metadata("euclidean stage order")
    contract = _euclidean_contract(domain="", condition=False, sabab=False)
    decision = contract.evaluate_gate()
    assert decision.transition_allowed is False
    assert decision.failed_stage is EuclideanGateStage.DOMAIN
    assert decision.failure_code is FailureCode.DOMAIN_MISSING


def test_euclidean_condition_sabab_mani_map_to_distinct_stages() -> None:
    _assert_branch_test_metadata("euclidean condition sabab mani")
    condition = _euclidean_contract(condition=False).evaluate_gate()
    sabab = _euclidean_contract(sabab=False).evaluate_gate()
    mani = _euclidean_contract(preventer=True).evaluate_gate()

    assert condition.failed_stage is EuclideanGateStage.CONDITION
    assert condition.readiness_state is TransitionReadinessState.DEFERRED
    assert sabab.failed_stage is EuclideanGateStage.SABAB
    assert sabab.readiness_state is TransitionReadinessState.DEFERRED
    assert mani.failed_stage is EuclideanGateStage.MANI
    assert mani.readiness_state is TransitionReadinessState.BLOCKED


def test_euclidean_qadih_truth_table_is_explicit() -> None:
    _assert_branch_test_metadata("euclidean qadih truth table")
    unchecked = _euclidean_contract(qadih_status=QadihCheckStatus.UNCHECKED).evaluate_gate()
    blocking = _euclidean_contract(qadih_status=QadihCheckStatus.BLOCKING).evaluate_gate()
    clear = _euclidean_contract(qadih_status=QadihCheckStatus.CLEAR).evaluate_gate()
    residual = _euclidean_contract(qadih_status=QadihCheckStatus.RESIDUAL).evaluate_gate()

    assert unchecked.failed_stage is EuclideanGateStage.QADIH
    assert unchecked.readiness_state is TransitionReadinessState.DEFERRED
    assert unchecked.failure_code is FailureCode.QADIH_DIFFERENCE_UNCHECKED

    assert blocking.failed_stage is EuclideanGateStage.QADIH
    assert blocking.readiness_state is TransitionReadinessState.BLOCKED
    assert blocking.failure_code is FailureCode.QADIH_DIFFERENCE_BLOCKING

    assert clear.transition_allowed is True

    assert residual.failed_stage is EuclideanGateStage.QADIH
    assert residual.readiness_state is TransitionReadinessState.DEFERRED


def test_euclidean_origin_vs_prior_info_mismatch_refuses() -> None:
    _assert_branch_test_metadata("euclidean origin mismatch")
    contract = _euclidean_contract(
        origin_proof=OriginProof(
            origin_ref="asl/base_rule",
            preserved_identity=True,
            domain="other_domain",
            trace_ref="trace://x0r/euclidean/1",
            rank=3,
        )
    )
    decision = contract.evaluate_gate()
    assert decision.transition_allowed is False
    assert decision.failed_stage is EuclideanGateStage.ORIGIN
    assert decision.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_euclidean_minimal_complete_requirement_failure_deferred() -> None:
    _assert_branch_test_metadata("euclidean minimal complete failure")
    contract = _euclidean_contract(
        minimal_complete_requirement=_minimal_complete(
            current_stage_rank=2,
            max_required_stage_rank=3,
        )
    )
    decision = contract.evaluate_gate()
    assert decision.transition_allowed is False
    assert decision.failed_stage is EuclideanGateStage.MINIMUM_COMPLETE
    assert decision.readiness_state is TransitionReadinessState.DEFERRED


def test_euclidean_rank_ceiling_is_meet_preserving() -> None:
    _assert_branch_test_metadata("euclidean rank ceiling meet")
    contract = _euclidean_contract(
        rank=4,
        minimal_complete_requirement=_minimal_complete(
            current_stage_rank=5,
            max_required_stage_rank=3,
            rank_ceiling=5,
        ),
        rank_force_ceiling=RankForceCeiling(
            evidence_rank=6,
            identity_rank=4,
            gate_rank=7,
            closure_rank=5,
            residual_rank_ceiling=3,
            explicit_rank_ceiling=8,
        ),
    )
    decision = contract.evaluate_gate()
    assert contract.force_rank_ceiling() == 3
    assert decision.transition_allowed is False
    assert decision.failed_stage is EuclideanGateStage.RANK_CEILING
    assert decision.failure_code is FailureCode.RANK_EXCEEDS_CEILING


def test_predict_branch_ranked_returns_readiness_state() -> None:
    _assert_branch_test_metadata("euclidean ranked branch prediction")
    prediction = _euclidean_contract().predict_branch_ranked()
    assert prediction.predicted_branch == "far/derived_case"
    assert prediction.predicted_rank == 3
    assert prediction.residuals == ("visible:deferred",)
    assert prediction.decision.readiness_state is TransitionReadinessState.LINK_READY
    assert prediction.is_final_judgment is False
    assert prediction.predicts_next_token is False


def test_to_failure_record_contains_stage_and_named_failure() -> None:
    _assert_branch_test_metadata("euclidean failure record surface")
    contract = _euclidean_contract(
        condition=False,
        preventer=True,
        residuals=("blocking:governor",),
        minimal_complete_requirement=_minimal_complete(missing_requirements=("evidence",)),
        handoff="handoff://x0r/required",
    )
    failure = contract.to_failure_record()

    assert failure.failed_transition is True
    assert failure.readiness_state is TransitionReadinessState.DEFERRED
    assert failure.failed_stage is EuclideanGateStage.MINIMUM_COMPLETE
    assert "condition" in failure.missing_condition
    assert "preventer_absence" in failure.missing_condition
    assert "minimal_complete_requirement" in failure.missing_condition
    assert failure.active_preventer is True
    assert failure.blocking_residual == ("blocking:governor",)
    assert failure.closest_valid_stage == 3
    assert failure.required_handoff == "handoff://x0r/required"
    assert failure.failure_code is FailureCode.RANK_PROMOTION_WITHOUT_GATE
    assert "blocking residuals" in failure.repair_suggestion.lower()
