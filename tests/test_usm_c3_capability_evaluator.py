"""USM-C3 bounded capability evaluator tests."""

from __future__ import annotations

from dataclasses import asdict, replace

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    CapabilityEvaluationRequest,
    CapabilityEvaluationState,
    ContextId,
    EntityInstanceRef,
    EntityTypeId,
    RequestId,
    RuleId,
    ScienceId,
    UniversalScienceMatrix,
    USMFailureCode,
    USMResidual,
    USMResidualKind,
    USMSchemaError,
    evaluate_capability,
    load_reference_matrices_v1,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"USM-C3 ({branch_note})",
        constitutional_chain=("docs/14", "USM-C2.1", "USM-C3"),
        chain_position="USM-C3 bounded capability evaluator runtime",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md",
        branch_of_origin="USM bounded capability-evaluation branch",
        forbidden_shortcut_assertions=(
            "CapabilityEligible -> RelationCandidate",
            "CapabilityEligible -> TransformationExecuted",
            "CapabilityEligible -> ScientificTruth",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RelationCandidate",
            "TransformationProposal",
            "ApprovedTransitionContext",
        ),
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


def _request_for(matrix: UniversalScienceMatrix) -> CapabilityEvaluationRequest:
    capability = matrix.capabilities[0]
    return CapabilityEvaluationRequest(
        request_id=RequestId("REQ-C3-001"),
        matrix_id=matrix.matrix_id,
        science_id=matrix.science_id,
        entity_type_id=capability.bearer_type,
        entity_instance_ref=EntityInstanceRef("entity://example/1"),
        capability_id=capability.capability_id,
        context_id=ContextId("context://example/default"),
        supplied_condition_refs=capability.required_conditions,
        supplied_evidence_type_refs=capability.evidence_requirements,
        active_blocker_refs=(),
        requested_rank=Rank.CANDIDATE,
        residuals=(),
        trace_ref=matrix.trace_ref,
    )


def _other_entity_type(matrix: UniversalScienceMatrix, current: EntityTypeId) -> EntityTypeId:
    for entity in matrix.entities:
        if entity.entity_type_id != current:
            return entity.entity_type_id
    raise AssertionError("matrix must contain more than one entity type")


def test_capability_evaluator_is_pure() -> None:
    _declare("pure evaluator")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    before = asdict(matrix)
    _ = evaluate_capability(matrix, request)
    after = asdict(matrix)
    assert before == after


def test_capability_evaluation_does_not_create_relation() -> None:
    _declare("no relation creation")
    matrix = load_reference_matrices_v1()[1]
    result = evaluate_capability(matrix, _request_for(matrix))
    assert not hasattr(result, "relation_candidate")


def test_capability_evaluation_does_not_execute_transformation() -> None:
    _declare("no transformation execution")
    matrix = load_reference_matrices_v1()[1]
    result = evaluate_capability(matrix, _request_for(matrix))
    assert not hasattr(result, "transformation_executed")


def test_capability_evaluation_does_not_issue_transition_certificate() -> None:
    _declare("no transition certificate issuance")
    matrix = load_reference_matrices_v1()[1]
    result = evaluate_capability(matrix, _request_for(matrix))
    assert "CERTIFICATE" not in repr(result).upper()


def test_capability_evaluation_does_not_promote_rank() -> None:
    _declare("no rank promotion")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, request)
    assert result.granted_rank <= request.requested_rank


def test_capability_evaluation_preserves_residuals() -> None:
    _declare("residual preservation")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    residual = USMResidual(
        residual_id="capability-nonblocking-residual",
        kind=USMResidualKind.COVERAGE_GAP,
        detail="non-blocking residual stays visible",
        blocking=False,
        visible=True,
        repair_hint="extend bounded capability checks",
    )
    result = evaluate_capability(matrix, replace(request, residuals=(residual,)))
    assert residual in result.residuals
    assert result.state is CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS


def test_capability_evaluation_requires_matching_entity_type() -> None:
    _declare("matching entity type")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    wrong_entity = _other_entity_type(matrix, request.entity_type_id)
    result = evaluate_capability(matrix, replace(request, entity_type_id=wrong_entity))
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert USMFailureCode.CAPABILITY_BEARER_TYPE_MISMATCH in result.failure_codes


def test_capability_evaluation_requires_local_science_identity() -> None:
    _declare("local science identity")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, replace(request, science_id=ScienceId("FOREIGN")))
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE in result.failure_codes


def test_capability_evaluation_defers_missing_condition() -> None:
    _declare("missing condition deferred")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, replace(request, supplied_condition_refs=()))
    assert result.state is CapabilityEvaluationState.DEFERRED
    assert USMFailureCode.CAPABILITY_CONDITION_MISSING in result.failure_codes


def test_capability_evaluation_blocks_active_blocker() -> None:
    _declare("active blocker blocked")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    blocker = matrix.capabilities[0].blockers[0]
    result = evaluate_capability(matrix, replace(request, active_blocker_refs=(blocker,)))
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert USMFailureCode.CAPABILITY_BLOCKER_ACTIVE in result.failure_codes


def test_capability_evaluation_rejects_rank_above_ceiling() -> None:
    _declare("rank ceiling rejection")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, replace(request, requested_rank=max(Rank)))
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert USMFailureCode.CAPABILITY_RANK_CEILING_EXCEEDED in result.failure_codes


def test_capability_evaluation_rejects_cross_science_reference() -> None:
    _declare("cross science reference rejection")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, replace(request, science_id=ScienceId("OTHER_SCIENCE")))
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE in result.failure_codes


def test_same_evaluator_shape_runs_on_all_three_reference_matrices() -> None:
    _declare("same evaluator shape")
    for matrix in load_reference_matrices_v1():
        request = _request_for(matrix)
        result = evaluate_capability(matrix, request)
        assert isinstance(result.state, CapabilityEvaluationState)
        assert result.state in {
            CapabilityEvaluationState.ELIGIBLE,
            CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS,
        }
        assert result.capability_id == request.capability_id


def test_capability_eligible_does_not_imply_relation_candidate() -> None:
    _declare("no eligible-to-relation jump")
    matrix = load_reference_matrices_v1()[1]
    result = evaluate_capability(matrix, _request_for(matrix))
    assert not hasattr(result, "relation_type_id")


def test_capability_eligible_does_not_imply_transformation_executed() -> None:
    _declare("no eligible-to-transformation jump")
    matrix = load_reference_matrices_v1()[1]
    result = evaluate_capability(matrix, _request_for(matrix))
    assert not hasattr(result, "transformation_type_id")


def test_capability_eligible_does_not_imply_claim_proven_or_scientific_truth() -> None:
    _declare("no eligible-to-truth jump")
    matrix = load_reference_matrices_v1()[1]
    result = evaluate_capability(matrix, _request_for(matrix))
    assert not hasattr(result, "claim_verdict")
    assert not hasattr(result, "scientific_truth")


def test_capability_eligible_does_not_imply_cross_science_transfer() -> None:
    _declare("no eligible-to-cross-science-transfer jump")
    matrix = load_reference_matrices_v1()[1]
    result = evaluate_capability(matrix, _request_for(matrix))
    assert "BRIDGE" not in repr(result).upper()


def test_capability_eligible_does_not_imply_rank_promotion() -> None:
    _declare("no eligible-to-rank-promotion jump")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, request)
    assert result.granted_rank <= request.requested_rank


def test_bounded_capability_evaluator_minimality_evidence() -> None:
    _declare("bounded capability-evaluator minimality evidence")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    params = asdict(request)
    required_fields = (
        "entity_instance_ref",
        "entity_type_id",
        "capability_id",
        "context_id",
        "supplied_condition_refs",
        "active_blocker_refs",
        "requested_rank",
        "residuals",
        "trace_ref",
    )
    for field in required_fields:
        bad = dict(params)
        bad.pop(field)
        with pytest.raises(TypeError):
            CapabilityEvaluationRequest(**bad)


def test_capability_evaluation_defers_when_context_unresolved() -> None:
    _declare("context unresolved")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, replace(request, context_id=ContextId("ctx-unresolved")))
    assert result.state is CapabilityEvaluationState.DEFERRED
    assert USMFailureCode.CAPABILITY_CONTEXT_UNRESOLVED in result.failure_codes


def test_capability_request_types_are_strict() -> None:
    _declare("typed request fields")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    with pytest.raises(USMSchemaError):
        CapabilityEvaluationRequest(
            request_id=request.request_id,
            matrix_id=request.matrix_id,
            science_id=request.science_id,
            entity_type_id=request.entity_type_id,
            entity_instance_ref=request.entity_instance_ref,
            capability_id=request.capability_id,
            context_id=request.context_id,
            supplied_condition_refs=(RuleId("X"),),
            supplied_evidence_type_refs=request.supplied_evidence_type_refs,
            active_blocker_refs=("NOT_RULE_ID",),  # type: ignore[arg-type]
            requested_rank=request.requested_rank,
            residuals=request.residuals,
            trace_ref=request.trace_ref,
        )
