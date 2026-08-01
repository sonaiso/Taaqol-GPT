"""USM-C3.1 capability provenance and trace hardening tests."""

from __future__ import annotations

from dataclasses import asdict, replace

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    CapabilityEvaluationEnvironment,
    CapabilityEvaluationRequest,
    CapabilityEvaluationResult,
    CapabilityEvaluationState,
    CapabilityEvaluationTrace,
    ContextId,
    EntityInstanceContract,
    EntityInstanceRef,
    EntityTypeId,
    EvaluationContextContract,
    EvidenceTypeId,
    RequestId,
    ScienceId,
    TraceRef,
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
        branch_name=f"USM-C3.1 ({branch_note})",
        constitutional_chain=("docs/14", "USM-C2.1", "USM-C3", "USM-C3.1"),
        chain_position="USM-C3.1 capability provenance and trace hardening",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md",
        branch_of_origin="USM capability hardening branch",
        forbidden_shortcut_assertions=(
            "CapabilityEligible -> RelationCandidate",
            "CapabilityEligible -> TransformationExecuted",
            "EvidenceTypePresent -> EvidenceValid",
            "EvidenceTypePresent -> ClaimProven",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RelationCandidate",
            "RelationEvaluationResult",
            "TransformationProposal",
            "ApprovedTransitionContext",
            "EvidenceVerdict",
            "ScientificTruthCertificate",
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
    request_id = RequestId("REQ-C31-001")
    return CapabilityEvaluationRequest(
        request_id=request_id,
        matrix_id=matrix.matrix_id,
        science_id=matrix.science_id,
        entity_type_id=capability.bearer_type,
        entity_instance_ref=EntityInstanceRef("entity://matrix/sample/1"),
        capability_id=capability.capability_id,
        context_id=ContextId("context://matrix/default"),
        supplied_condition_refs=capability.required_conditions,
        supplied_evidence_type_refs=capability.evidence_requirements,
        active_blocker_refs=(),
        requested_rank=Rank.CANDIDATE,
        residuals=(),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/requests/{request_id.value}"),
    )


def _environment_for(
    matrix: UniversalScienceMatrix,
    request: CapabilityEvaluationRequest,
    *,
    entity_rank: Rank = Rank.CANDIDATE,
) -> CapabilityEvaluationEnvironment:
    context = EvaluationContextContract(
        context_id=request.context_id,
        science_id=matrix.science_id,
        matrix_id=matrix.matrix_id,
        active_condition_refs=(),
        active_blocker_refs=(),
        supplied_evidence_type_refs=(),
        residuals=(),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/contexts/default"),
    )
    entity = EntityInstanceContract(
        entity_instance_ref=request.entity_instance_ref,
        entity_type_id=request.entity_type_id,
        science_id=matrix.science_id,
        matrix_id=matrix.matrix_id,
        state_rank=entity_rank,
        active_property_refs=(),
        residuals=(),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/entities/instance/1"),
    )
    return CapabilityEvaluationEnvironment(entity_instances=(entity,), contexts=(context,))


def _trace_for_result(
    request: CapabilityEvaluationRequest, state: CapabilityEvaluationState
) -> CapabilityEvaluationTrace:
    base = request.trace_ref.value
    return CapabilityEvaluationTrace(
        evaluation_trace_ref=TraceRef(f"{base}/decisions/{state.value.lower()}"),
        request_trace_ref=request.trace_ref,
        entity_trace_ref=TraceRef(f"{base}/entity"),
        context_trace_ref=TraceRef(f"{base}/context"),
        matrix_trace_ref=TraceRef(f"{base}/matrix"),
        capability_trace_ref=TraceRef(f"{base}/capability"),
        decision_stage=state.value.lower(),
    )


def test_entity_instance_must_resolve() -> None:
    _declare("entity instance must resolve")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    unresolved = replace(request, entity_instance_ref=EntityInstanceRef("entity://ghost/1"))
    result = evaluate_capability(matrix, env, unresolved)
    assert result.state is CapabilityEvaluationState.DEFERRED
    assert result.failure_codes == (USMFailureCode.CAPABILITY_ENTITY_INSTANCE_UNRESOLVED,)


def test_entity_instance_type_must_match_request() -> None:
    _declare("entity instance type must match request")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    wrong_entity_type = next(
        entity.entity_type_id
        for entity in matrix.entities
        if entity.entity_type_id != request.entity_type_id
    )
    entity = EntityInstanceContract(
        entity_instance_ref=request.entity_instance_ref,
        entity_type_id=wrong_entity_type,
        science_id=matrix.science_id,
        matrix_id=matrix.matrix_id,
        state_rank=Rank.CANDIDATE,
        active_property_refs=(),
        residuals=(),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/entities/instance/wrong"),
    )
    env = CapabilityEvaluationEnvironment(
        entity_instances=(entity,), contexts=_environment_for(matrix, request).contexts
    )
    result = evaluate_capability(matrix, env, request)
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert result.failure_codes == (USMFailureCode.CAPABILITY_ENTITY_INSTANCE_TYPE_MISMATCH,)


def test_entity_instance_science_must_match_matrix() -> None:
    _declare("entity instance science must match matrix")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    foreign = replace(
        env.entity_instances[0],
        science_id=ScienceId("FOREIGN"),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/entities/instance/foreign"),
    )
    result = evaluate_capability(matrix, replace(env, entity_instances=(foreign,)), request)
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert result.failure_codes == (USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE,)


def test_context_must_resolve() -> None:
    _declare("context must resolve")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    unresolved = replace(request, context_id=ContextId("context://ghost/default"))
    result = evaluate_capability(matrix, env, unresolved)
    assert result.state is CapabilityEvaluationState.DEFERRED
    assert result.failure_codes == (USMFailureCode.CAPABILITY_CONTEXT_UNRESOLVED,)


def test_context_science_must_match_matrix() -> None:
    _declare("context science must match matrix")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    foreign_context = replace(
        env.contexts[0],
        science_id=ScienceId("FOREIGN"),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/contexts/foreign"),
    )
    result = evaluate_capability(matrix, replace(env, contexts=(foreign_context,)), request)
    assert result.state is CapabilityEvaluationState.INVALID
    assert result.failure_codes == (USMFailureCode.CAPABILITY_CONTEXT_SCIENCE_MISMATCH,)


def test_context_matrix_must_match_request() -> None:
    _declare("context matrix must match request")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    wrong_context = replace(
        env.contexts[0],
        matrix_id=matrix.matrix_id.__class__("MATRIX-OTHER"),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/contexts/other-matrix"),
    )
    result = evaluate_capability(matrix, replace(env, contexts=(wrong_context,)), request)
    assert result.state is CapabilityEvaluationState.INVALID
    assert result.failure_codes == (USMFailureCode.CAPABILITY_CONTEXT_MATRIX_MISMATCH,)


def test_identifier_prefix_alone_does_not_establish_identity() -> None:
    _declare("identifier prefix alone does not establish identity")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    prefixed_only = replace(
        request,
        entity_instance_ref=EntityInstanceRef("entity://not-in-registry"),
        context_id=ContextId("context://not-in-registry"),
    )
    result = evaluate_capability(matrix, env, prefixed_only)
    assert result.failure_codes == (USMFailureCode.CAPABILITY_ENTITY_INSTANCE_UNRESOLVED,)


def test_evaluation_emits_new_trace_event() -> None:
    _declare("evaluation emits new trace event")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert result.trace_ref != request.trace_ref


def test_result_trace_links_request_entity_context_and_capability() -> None:
    _declare("trace links request/entity/context/capability")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    result = evaluate_capability(matrix, env, request)
    assert result.evaluation_trace.request_trace_ref == request.trace_ref
    assert result.evaluation_trace.entity_trace_ref == env.entity_instances[0].trace_ref
    assert result.evaluation_trace.context_trace_ref == env.contexts[0].trace_ref
    assert result.evaluation_trace.capability_trace_ref == matrix.capabilities[0].trace_ref
    assert result.evaluation_trace.matrix_trace_ref == matrix.trace_ref


def test_broken_trace_chain_is_invalid() -> None:
    _declare("broken trace chain invalid")
    matrix = load_reference_matrices_v1()[1]
    request = replace(_request_for(matrix), trace_ref=TraceRef("trace://foreign/root"))
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert result.state is CapabilityEvaluationState.INVALID
    assert result.failure_codes == (USMFailureCode.CAPABILITY_TRACE_CHAIN_BROKEN,)


def test_refusal_also_emits_trace() -> None:
    _declare("refusal emits trace")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(
        matrix,
        _environment_for(matrix, request),
        replace(request, entity_instance_ref=EntityInstanceRef("entity://ghost")),
    )
    assert result.state is CapabilityEvaluationState.DEFERRED
    assert result.trace_ref != request.trace_ref


def test_result_cannot_reuse_request_trace_as_if_no_decision_occurred() -> None:
    _declare("result cannot reuse request trace")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert result.evaluation_trace.evaluation_trace_ref != result.evaluation_trace.request_trace_ref


def test_evidence_type_presence_does_not_mean_validity() -> None:
    _declare("evidence type presence does not mean validity")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert not hasattr(result, "evidence_valid")


def test_evidence_type_presence_does_not_mean_sufficiency() -> None:
    _declare("evidence type presence does not mean sufficiency")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert not hasattr(result, "evidence_sufficient")


def test_evidence_type_presence_does_not_prove_claim() -> None:
    _declare("evidence type presence does not prove claim")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert not hasattr(result, "claim_proven")


def test_unresolved_evidence_type_is_distinct_from_missing_supplied_type() -> None:
    _declare("unresolved evidence distinct from missing supplied type")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    missing_result = evaluate_capability(
        matrix,
        env,
        replace(request, supplied_evidence_type_refs=()),
    )
    assert missing_result.failure_codes == (USMFailureCode.CAPABILITY_EVIDENCE_TYPE_NOT_SUPPLIED,)

    unknown_evidence = EvidenceTypeId("EVIDENCE-UNKNOWN")
    patched_capability = replace(matrix.capabilities[0], evidence_requirements=(unknown_evidence,))
    patched_matrix = replace(matrix, capabilities=(patched_capability,) + matrix.capabilities[1:])
    unresolved_result = evaluate_capability(
        patched_matrix,
        env,
        replace(request, supplied_evidence_type_refs=(unknown_evidence,)),
    )
    assert unresolved_result.failure_codes == (USMFailureCode.CAPABILITY_EVIDENCE_TYPE_UNRESOLVED,)


def test_entity_state_rank_bounds_capability_rank() -> None:
    _declare("entity state rank bounds capability rank")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(
        matrix, _environment_for(matrix, request, entity_rank=Rank.ZERO), request
    )
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert result.granted_rank is Rank.ZERO
    assert result.failure_codes == (USMFailureCode.CAPABILITY_ENTITY_RANK_CEILING_EXCEEDED,)


def test_capability_evaluator_never_promotes_entity_rank() -> None:
    _declare("never promotes entity rank")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request, entity_rank=Rank.CANDIDATE)
    result = evaluate_capability(matrix, env, request)
    assert result.granted_rank <= env.entity_instances[0].state_rank


def test_evidence_type_ceiling_does_not_raise_entity_rank() -> None:
    _declare("evidence ceiling does not raise entity rank")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request, entity_rank=Rank.ZERO)
    result = evaluate_capability(matrix, env, request)
    assert result.granted_rank <= env.entity_instances[0].state_rank


def test_zero_rank_entity_cannot_receive_candidate_eligibility_rank() -> None:
    _declare("zero-rank entity cannot receive candidate eligibility rank")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(
        matrix, _environment_for(matrix, request, entity_rank=Rank.ZERO), request
    )
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert result.granted_rank is Rank.ZERO


def test_eligible_result_cannot_carry_failure_code() -> None:
    _declare("eligible cannot carry failure")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    with pytest.raises(USMSchemaError):
        CapabilityEvaluationResult(
            request_id=request.request_id,
            state=CapabilityEvaluationState.ELIGIBLE,
            capability_id=request.capability_id,
            entity_type_id=request.entity_type_id,
            granted_rank=Rank.CANDIDATE,
            satisfied_conditions=(),
            missing_conditions=(),
            active_blockers=(),
            recognized_evidence_type_refs=(),
            failure_codes=(USMFailureCode.CAPABILITY_BLOCKER_ACTIVE,),
            residuals=(),
            trace_ref=TraceRef(f"{request.trace_ref.value}/bad"),
            evaluation_trace=_trace_for_result(request, CapabilityEvaluationState.ELIGIBLE),
        )


def test_eligible_with_residuals_rejects_blocking_residual() -> None:
    _declare("eligible with residuals rejects blocking residual")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    blocking = USMResidual(
        residual_id="blocking",
        kind=USMResidualKind.COVERAGE_GAP,
        detail="blocking residual not allowed for eligible-with-residuals",
        blocking=True,
        visible=True,
        repair_hint="resolve blocker",
    )
    with pytest.raises(USMSchemaError):
        CapabilityEvaluationResult(
            request_id=request.request_id,
            state=CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS,
            capability_id=request.capability_id,
            entity_type_id=request.entity_type_id,
            granted_rank=Rank.CANDIDATE,
            satisfied_conditions=(),
            missing_conditions=(),
            active_blockers=(),
            recognized_evidence_type_refs=(),
            failure_codes=(),
            residuals=(blocking,),
            trace_ref=TraceRef(f"{request.trace_ref.value}/bad"),
            evaluation_trace=_trace_for_result(
                request, CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS
            ),
        )


def test_deferred_result_requires_named_deferred_failure() -> None:
    _declare("deferred requires named deferred failure")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    with pytest.raises(USMSchemaError):
        CapabilityEvaluationResult(
            request_id=request.request_id,
            state=CapabilityEvaluationState.DEFERRED,
            capability_id=request.capability_id,
            entity_type_id=request.entity_type_id,
            granted_rank=Rank.ZERO,
            satisfied_conditions=(),
            missing_conditions=(),
            active_blockers=(),
            recognized_evidence_type_refs=(),
            failure_codes=(),
            residuals=(),
            trace_ref=TraceRef(f"{request.trace_ref.value}/bad"),
            evaluation_trace=_trace_for_result(request, CapabilityEvaluationState.DEFERRED),
        )


def test_blocked_result_requires_named_blocking_failure() -> None:
    _declare("blocked requires named blocking failure")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    with pytest.raises(USMSchemaError):
        CapabilityEvaluationResult(
            request_id=request.request_id,
            state=CapabilityEvaluationState.BLOCKED,
            capability_id=request.capability_id,
            entity_type_id=request.entity_type_id,
            granted_rank=Rank.ZERO,
            satisfied_conditions=(),
            missing_conditions=(),
            active_blockers=(),
            recognized_evidence_type_refs=(),
            failure_codes=(USMFailureCode.CAPABILITY_CONDITION_MISSING,),
            residuals=(),
            trace_ref=TraceRef(f"{request.trace_ref.value}/bad"),
            evaluation_trace=_trace_for_result(request, CapabilityEvaluationState.BLOCKED),
        )


def test_invalid_result_grants_zero_rank() -> None:
    _declare("invalid grants zero rank")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    with pytest.raises(USMSchemaError):
        CapabilityEvaluationResult(
            request_id=request.request_id,
            state=CapabilityEvaluationState.INVALID,
            capability_id=request.capability_id,
            entity_type_id=request.entity_type_id,
            granted_rank=Rank.CANDIDATE,
            satisfied_conditions=(),
            missing_conditions=(),
            active_blockers=(),
            recognized_evidence_type_refs=(),
            failure_codes=(USMFailureCode.CAPABILITY_TRACE_CHAIN_BROKEN,),
            residuals=(),
            trace_ref=TraceRef(f"{request.trace_ref.value}/bad"),
            evaluation_trace=_trace_for_result(request, CapabilityEvaluationState.INVALID),
        )


def test_evaluator_does_not_mutate_matrix_environment_or_request() -> None:
    _declare("evaluator purity")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    matrix_before = asdict(matrix)
    env_before = asdict(env)
    request_before = asdict(request)
    _ = evaluate_capability(matrix, env, request)
    assert matrix_before == asdict(matrix)
    assert env_before == asdict(env)
    assert request_before == asdict(request)


def test_capability_result_does_not_create_relation() -> None:
    _declare("no relation creation")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert not hasattr(result, "relation_candidate")


def test_capability_result_does_not_execute_transformation() -> None:
    _declare("no transformation execution")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert not hasattr(result, "transformation_executed")


def test_capability_result_does_not_issue_transition_certificate() -> None:
    _declare("no transition certificate")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert "CERTIFICATE" not in repr(result).upper()


def test_capability_result_does_not_execute_bridge() -> None:
    _declare("no bridge execution")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert "BRIDGE_EXECUTED" not in repr(result).upper()


def test_capability_result_does_not_claim_truth() -> None:
    _declare("no truth claim")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert not hasattr(result, "scientific_truth")


def test_science_mismatch_is_prioritized_over_missing_condition() -> None:
    _declare("science mismatch priority")
    matrix = load_reference_matrices_v1()[1]
    request = replace(
        _request_for(matrix), science_id=ScienceId("FOREIGN"), supplied_condition_refs=()
    )
    result = evaluate_capability(matrix, _environment_for(matrix, request), request)
    assert result.failure_codes == (USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE,)


def test_unknown_entity_is_not_reported_as_bearer_mismatch() -> None:
    _declare("unknown entity priority")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    env = _environment_for(matrix, request)
    result = evaluate_capability(
        matrix,
        env,
        replace(
            request,
            entity_instance_ref=EntityInstanceRef("entity://unknown"),
            entity_type_id=EntityTypeId("X"),
        ),
    )
    assert result.failure_codes == (USMFailureCode.CAPABILITY_ENTITY_INSTANCE_UNRESOLVED,)


def test_active_blocker_is_not_deferred() -> None:
    _declare("active blocker is blocked")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    blocker = matrix.capabilities[0].blockers[0]
    result = evaluate_capability(
        matrix,
        _environment_for(matrix, request),
        replace(request, active_blocker_refs=(blocker,)),
    )
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert result.failure_codes == (USMFailureCode.CAPABILITY_BLOCKER_ACTIVE,)


def test_blocking_residual_is_not_eligible_with_residuals() -> None:
    _declare("blocking residual blocks")
    matrix = load_reference_matrices_v1()[1]
    request = _request_for(matrix)
    blocking = USMResidual(
        residual_id="block-me",
        kind=USMResidualKind.COVERAGE_GAP,
        detail="blocking residual",
        blocking=True,
        visible=True,
        repair_hint="resolve",
    )
    result = evaluate_capability(
        matrix,
        _environment_for(matrix, request),
        replace(request, residuals=(blocking,)),
    )
    assert result.state is CapabilityEvaluationState.BLOCKED
    assert result.failure_codes == (USMFailureCode.CAPABILITY_BLOCKING_RESIDUAL,)
