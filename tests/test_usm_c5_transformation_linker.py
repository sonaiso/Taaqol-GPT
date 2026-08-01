"""USM-C5 bounded transformation linking tests."""

from __future__ import annotations

from dataclasses import asdict, replace

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    CapabilityEvaluationEnvironment,
    CapabilityEvaluationRef,
    CapabilityEvaluationRequest,
    CapabilityId,
    ContextId,
    EntityInstanceContract,
    EntityInstanceRef,
    EvaluationContextContract,
    RelationEvaluationEnvironment,
    RelationEvaluationRequest,
    RelationEvaluationState,
    RelationOperandBinding,
    RequestId,
    RoleId,
    RuleId,
    TraceRef,
    TransformationLinkEnvironment,
    TransformationLinkRequest,
    TransformationLinkState,
    TransformationTypeId,
    USMFailureCode,
    USMResidual,
    USMResidualKind,
    evaluate_capability,
    evaluate_relation,
    evaluate_transformation_link,
    load_reference_matrices_v1,
)
from taaqqul_slot_geometry.usm.transformation_contract import TransformationContract
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"USM-C5 ({branch_note})",
        constitutional_chain=("docs/14", "USM-C2.1", "USM-C3", "USM-C3.1", "USM-C4", "USM-C5"),
        chain_position="USM-C5 bounded transformation linking",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md",
        branch_of_origin="USM bounded relation/transformation branch",
        forbidden_shortcut_assertions=(
            "RelationEligible -> TransformationExecuted",
            "TransformationLinkEligible -> TransitionCertificate",
            "TransformationLinkEligible -> ClaimProven",
            "TransformationLinkEligible -> ExternalTruth",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "TransformationExecuted",
            "ApprovedTransitionContext",
            "TransitionCertificate",
            "ClaimVerdict",
            "JudgmentVerdict",
            "ExternalTruthCertificate",
            "BridgeExecutionVerdict",
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


def _make_case(matrix_index: int):
    matrix = load_reference_matrices_v1()[matrix_index]
    relation = matrix.relations[0]
    base_capability = matrix.capabilities[0]
    evidence_type = matrix.evidence[0].evidence_type_id

    capabilities = tuple(
        replace(
            base_capability,
            capability_id=CapabilityId(f"C5_CAP_{matrix_index}_{position}"),
            bearer_type=relation.operand_types[position],
            permitted_relation_roles=(relation.roles[position],),
            required_conditions=(RuleId(f"C5_CAP_REQ_{matrix_index}_{position}"),),
            blockers=(RuleId(f"C5_CAP_BLK_{matrix_index}_{position}"),),
            evidence_requirements=(evidence_type,),
            rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(
                f"{matrix.trace_ref.value}/capabilities/c5/{matrix_index}/{position}"
            ),
        )
        for position in range(relation.arity)
    )
    transformation = TransformationContract(
        transformation_type_id=TransformationTypeId(f"C5_TRANSFORM_{matrix_index}"),
        science_id=matrix.science_id,
        source_types=relation.operand_types,
        target_types=relation.operand_types,
        required_capabilities=tuple(item.capability_id for item in capabilities),
        preserved_invariants=(RuleId(f"C5_TRANSFORM_INV_{matrix_index}"),),
        declared_changes=(RuleId(f"C5_TRANSFORM_CHANGE_{matrix_index}"),),
        required_conditions=(RuleId(f"C5_TRANSFORM_REQ_{matrix_index}"),),
        blockers=(RuleId(f"C5_TRANSFORM_BLK_{matrix_index}"),),
        evidence_requirements=(evidence_type,),
        rank_ceiling=Rank.CANDIDATE,
        residual_policy_ref=RuleId(f"C5_RESIDUAL_POLICY_{matrix_index}"),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/transformations/c5/{matrix_index}"),
    )
    matrix = replace(
        matrix,
        capabilities=matrix.capabilities + capabilities,
        transformations=matrix.transformations + (transformation,),
    )

    entities = tuple(
        EntityInstanceContract(
            entity_instance_ref=EntityInstanceRef(f"entity://c5/{matrix_index}/{position}"),
            entity_type_id=relation.operand_types[position],
            science_id=matrix.science_id,
            matrix_id=matrix.matrix_id,
            state_rank=Rank.CANDIDATE,
            active_property_refs=(),
            residuals=(),
            trace_ref=TraceRef(f"{matrix.trace_ref.value}/entities/c5/{matrix_index}/{position}"),
        )
        for position in range(relation.arity)
    )
    context = EvaluationContextContract(
        context_id=ContextId(f"context://c5/{matrix_index}"),
        science_id=matrix.science_id,
        matrix_id=matrix.matrix_id,
        active_condition_refs=(
            tuple(
                RuleId(f"C5_CAP_REQ_{matrix_index}_{position}")
                for position in range(relation.arity)
            )
            + relation.compatibility_rules
            + (relation.saturation_rule, relation.scope_rule)
            + transformation.required_conditions
        ),
        active_blocker_refs=(),
        supplied_evidence_type_refs=(evidence_type,),
        residuals=(),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/contexts/c5/{matrix_index}"),
    )
    capability_env = CapabilityEvaluationEnvironment(entity_instances=entities, contexts=(context,))
    capability_results = tuple(
        evaluate_capability(
            matrix,
            capability_env,
            CapabilityEvaluationRequest(
                request_id=RequestId(f"c5-cap-req-{matrix_index}-{position}"),
                matrix_id=matrix.matrix_id,
                science_id=matrix.science_id,
                entity_type_id=entities[position].entity_type_id,
                entity_instance_ref=entities[position].entity_instance_ref,
                capability_id=capabilities[position].capability_id,
                context_id=context.context_id,
                supplied_condition_refs=(RuleId(f"C5_CAP_REQ_{matrix_index}_{position}"),),
                supplied_evidence_type_refs=(evidence_type,),
                active_blocker_refs=(),
                requested_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref=TraceRef(
                    f"{matrix.trace_ref.value}/requests/c5-cap-req-{matrix_index}-{position}"
                ),
            ),
        )
        for position in range(relation.arity)
    )
    relation_env = RelationEvaluationEnvironment(
        entity_instances=entities,
        contexts=(context,),
        capability_results=capability_results,
    )
    relation_request = RelationEvaluationRequest(
        request_id=RequestId(f"c5-rel-req-{matrix_index}"),
        matrix_id=matrix.matrix_id,
        science_id=matrix.science_id,
        relation_type_id=relation.relation_type_id,
        operand_bindings=tuple(
            RelationOperandBinding(
                role_id=RoleId(relation.roles[position].value),
                entity_instance_ref=entities[position].entity_instance_ref,
                capability_result_ref=CapabilityEvaluationRef(
                    capability_results[position].request_id.value
                ),
                position=position,
            )
            for position in range(relation.arity)
        ),
        context_id=context.context_id,
        requested_rank=Rank.CANDIDATE,
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/requests/c5-rel-req-{matrix_index}"),
    )
    relation_result = evaluate_relation(matrix, relation_env, relation_request)

    env = TransformationLinkEnvironment(
        entity_instances=entities,
        contexts=(context,),
        capability_results=capability_results,
        relation_requests=(relation_request,),
        relation_results=(relation_result,),
    )
    request = TransformationLinkRequest(
        request_id=RequestId(f"c5-link-req-{matrix_index}"),
        matrix_id=matrix.matrix_id,
        science_id=matrix.science_id,
        transformation_type_id=transformation.transformation_type_id,
        relation_request_id=relation_request.request_id,
        requested_rank=Rank.CANDIDATE,
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/requests/c5-link-req-{matrix_index}"),
    )
    return matrix, env, request


def test_transformation_type_must_resolve() -> None:
    _declare("transformation type must resolve")
    matrix, env, request = _make_case(1)
    result = evaluate_transformation_link(
        matrix, env, replace(request, transformation_type_id=TransformationTypeId("UNKNOWN"))
    )
    assert result.state is TransformationLinkState.INVALID
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_TYPE_UNRESOLVED,)


def test_relation_request_must_resolve() -> None:
    _declare("relation request must resolve")
    matrix, env, request = _make_case(1)
    result = evaluate_transformation_link(
        matrix, env, replace(request, relation_request_id=RequestId("missing-rel"))
    )
    assert result.state is TransformationLinkState.DEFERRED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_RELATION_REQUEST_UNRESOLVED,)


def test_relation_result_must_be_eligible() -> None:
    _declare("relation result must be eligible")
    matrix, env, request = _make_case(1)
    blocked_relation = replace(
        env.relation_results[0],
        state=RelationEvaluationState.BLOCKED,
        granted_rank=Rank.ZERO,
        failure_codes=(USMFailureCode.RELATION_BLOCKER_ACTIVE,),
    )
    blocked_env = replace(env, relation_results=(blocked_relation,))
    result = evaluate_transformation_link(matrix, blocked_env, request)
    assert result.state is TransformationLinkState.BLOCKED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_RELATION_NOT_ELIGIBLE,)


def test_source_arity_must_match_transformation_contract() -> None:
    _declare("source arity must match")
    matrix, env, request = _make_case(1)
    shortened = replace(
        matrix.transformations[-1],
        source_types=matrix.transformations[-1].source_types[:-1],
    )
    bad_matrix = replace(matrix, transformations=matrix.transformations[:-1] + (shortened,))
    result = evaluate_transformation_link(bad_matrix, env, request)
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_SOURCE_ARITY_MISMATCH,)


def test_source_entity_type_must_match_contract() -> None:
    _declare("source type must match")
    matrix, env, request = _make_case(2)
    swapped = replace(
        env.entity_instances[0],
        entity_type_id=env.entity_instances[1].entity_type_id,
    )
    bad_env = replace(env, entity_instances=(swapped,) + env.entity_instances[1:])
    result = evaluate_transformation_link(matrix, bad_env, request)
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_SOURCE_TYPE_MISMATCH,)


def test_required_capability_must_be_present() -> None:
    _declare("required capability must be present")
    matrix, env, request = _make_case(1)
    transformed = replace(
        matrix.transformations[-1],
        required_capabilities=matrix.transformations[-1].required_capabilities
        + (CapabilityId("MISSING_CAP"),),
    )
    bad_matrix = replace(matrix, transformations=matrix.transformations[:-1] + (transformed,))
    result = evaluate_transformation_link(bad_matrix, env, request)
    assert result.state is TransformationLinkState.DEFERRED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_REQUIRED_CAPABILITY_MISSING,)


def test_required_condition_must_be_active() -> None:
    _declare("required condition must be active")
    matrix, env, request = _make_case(1)
    empty_context = replace(env.contexts[0], active_condition_refs=())
    result = evaluate_transformation_link(matrix, replace(env, contexts=(empty_context,)), request)
    assert result.state is TransformationLinkState.DEFERRED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_REQUIRED_CONDITION_MISSING,)


def test_active_blocker_blocks_linking() -> None:
    _declare("active blocker blocks linking")
    matrix, env, request = _make_case(1)
    blocker_context = replace(
        env.contexts[0],
        active_blocker_refs=(matrix.transformations[-1].blockers[0],),
    )
    result = evaluate_transformation_link(
        matrix,
        replace(env, contexts=(blocker_context,)),
        request,
    )
    assert result.state is TransformationLinkState.BLOCKED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_BLOCKER_ACTIVE,)


def test_evidence_requirements_must_be_present() -> None:
    _declare("evidence requirements must be present")
    matrix, env, request = _make_case(1)
    transformed = replace(
        matrix.transformations[-1],
        evidence_requirements=matrix.transformations[-1].evidence_requirements
        + (type(matrix.evidence[0].evidence_type_id)("MISSING_EVIDENCE"),),
    )
    bad_matrix = replace(matrix, transformations=matrix.transformations[:-1] + (transformed,))
    result = evaluate_transformation_link(bad_matrix, env, request)
    assert result.state is TransformationLinkState.DEFERRED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_EVIDENCE_REQUIREMENT_MISSING,)


def test_blocking_residual_blocks_link() -> None:
    _declare("blocking residual blocks link")
    matrix, env, request = _make_case(1)
    blocking = USMResidual(
        residual_id="c5-blocking",
        kind=USMResidualKind.COVERAGE_GAP,
        detail="blocking residual",
        blocking=True,
        visible=True,
        repair_hint="resolve",
    )
    blocked_entity = replace(env.entity_instances[0], residuals=(blocking,))
    bad_env = replace(env, entity_instances=(blocked_entity,) + env.entity_instances[1:])
    result = evaluate_transformation_link(matrix, bad_env, request)
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_BLOCKING_RESIDUAL,)


def test_rank_ceiling_is_enforced() -> None:
    _declare("rank ceiling enforced")
    matrix, env, request = _make_case(1)
    result = evaluate_transformation_link(
        matrix,
        env,
        replace(request, requested_rank=Rank.HYPOTHESIS),
    )
    assert result.state is TransformationLinkState.BLOCKED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_RANK_CEILING_EXCEEDED,)


def test_trace_chain_break_is_invalid() -> None:
    _declare("trace chain break invalid")
    matrix, env, request = _make_case(1)
    result = evaluate_transformation_link(
        matrix, env, replace(request, trace_ref=TraceRef("trace://foreign/root"))
    )
    assert result.state is TransformationLinkState.INVALID
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_TRACE_CHAIN_BROKEN,)


def test_success_links_without_executing_transformation() -> None:
    _declare("success links only")
    matrix, env, request = _make_case(1)
    result = evaluate_transformation_link(matrix, env, request)
    assert result.state in {
        TransformationLinkState.ELIGIBLE,
        TransformationLinkState.ELIGIBLE_WITH_RESIDUALS,
    }
    assert not hasattr(result, "transformation_executed")
    assert "CERTIFICATE" not in repr(result).upper()


def test_refusal_also_emits_trace() -> None:
    _declare("refusal emits trace")
    matrix, env, request = _make_case(1)
    result = evaluate_transformation_link(
        matrix, env, replace(request, transformation_type_id=TransformationTypeId("UNKNOWN"))
    )
    assert result.trace_ref != request.trace_ref


def test_linking_is_pure_and_deterministic() -> None:
    _declare("pure and deterministic")
    matrix, env, request = _make_case(1)
    matrix_before = asdict(matrix)
    env_before = asdict(env)
    request_before = asdict(request)
    result_one = evaluate_transformation_link(matrix, env, request)
    result_two = evaluate_transformation_link(matrix, env, request)
    assert matrix_before == asdict(matrix)
    assert env_before == asdict(env)
    assert request_before == asdict(request)
    assert result_one == result_two
