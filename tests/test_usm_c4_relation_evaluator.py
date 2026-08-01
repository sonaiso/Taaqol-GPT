"""USM-C4 bounded relation evaluation tests."""

from __future__ import annotations

from dataclasses import asdict, replace

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    CapabilityEvaluationEnvironment,
    CapabilityEvaluationRef,
    CapabilityEvaluationRequest,
    CapabilityEvaluationState,
    CapabilityId,
    ContextId,
    EntityInstanceContract,
    EntityInstanceRef,
    EvaluationContextContract,
    MatrixId,
    RelationEvaluationEnvironment,
    RelationEvaluationRequest,
    RelationEvaluationState,
    RelationOperandBinding,
    RelationTypeId,
    RequestId,
    RoleId,
    RuleId,
    ScienceId,
    TraceRef,
    USMFailureCode,
    USMResidual,
    USMResidualKind,
    evaluate_capability,
    evaluate_relation,
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
        branch_name=f"USM-C4 ({branch_note})",
        constitutional_chain=("docs/14", "USM-C2.1", "USM-C3", "USM-C3.1", "USM-C4"),
        chain_position="USM-C4 bounded relation evaluation",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md",
        branch_of_origin="USM bounded relation branch",
        forbidden_shortcut_assertions=(
            "CapabilityEligible -> RelationEstablished",
            "RelationEligible -> TransformationExecuted",
            "RelationEligible -> ClaimProven",
            "RelationEligible -> ExternalTruth",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "TransformationProposal",
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
    added_capabilities = tuple(
        replace(
            base_capability,
            capability_id=CapabilityId(f"C4_CAP_{matrix_index}_{position}"),
            bearer_type=relation.operand_types[position],
            permitted_relation_roles=(relation.roles[position],),
            required_conditions=(RuleId(f"C4_CAP_REQ_{matrix_index}_{position}"),),
            blockers=(RuleId(f"C4_CAP_BLK_{matrix_index}_{position}"),),
            evidence_requirements=(evidence_type,),
            rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(
                f"{matrix.trace_ref.value}/capabilities/c4/{matrix_index}/{position}"
            ),
        )
        for position in range(relation.arity)
    )
    matrix = replace(matrix, capabilities=matrix.capabilities + added_capabilities)

    entities = tuple(
        EntityInstanceContract(
            entity_instance_ref=EntityInstanceRef(f"entity://c4/{matrix_index}/{position}"),
            entity_type_id=relation.operand_types[position],
            science_id=matrix.science_id,
            matrix_id=matrix.matrix_id,
            state_rank=Rank.CANDIDATE,
            active_property_refs=(),
            residuals=(),
            trace_ref=TraceRef(f"{matrix.trace_ref.value}/entities/c4/{matrix_index}/{position}"),
        )
        for position in range(relation.arity)
    )
    context = EvaluationContextContract(
        context_id=ContextId(f"context://c4/{matrix_index}"),
        science_id=matrix.science_id,
        matrix_id=matrix.matrix_id,
        active_condition_refs=(
            tuple(
                RuleId(f"C4_CAP_REQ_{matrix_index}_{position}")
                for position in range(relation.arity)
            )
            + relation.compatibility_rules
            + (relation.saturation_rule, relation.scope_rule)
        ),
        active_blocker_refs=(),
        supplied_evidence_type_refs=(evidence_type,),
        residuals=(),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/contexts/c4/{matrix_index}"),
    )
    capability_env = CapabilityEvaluationEnvironment(entity_instances=entities, contexts=(context,))
    capability_results = tuple(
        evaluate_capability(
            matrix,
            capability_env,
            CapabilityEvaluationRequest(
                request_id=RequestId(f"cap-req-{matrix_index}-{position}"),
                matrix_id=matrix.matrix_id,
                science_id=matrix.science_id,
                entity_type_id=entities[position].entity_type_id,
                entity_instance_ref=entities[position].entity_instance_ref,
                capability_id=added_capabilities[position].capability_id,
                context_id=context.context_id,
                supplied_condition_refs=(RuleId(f"C4_CAP_REQ_{matrix_index}_{position}"),),
                supplied_evidence_type_refs=(evidence_type,),
                active_blocker_refs=(),
                requested_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref=TraceRef(
                    f"{matrix.trace_ref.value}/requests/cap-req-{matrix_index}-{position}"
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
        request_id=RequestId(f"rel-req-{matrix_index}"),
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
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/requests/rel-req-{matrix_index}"),
    )
    return matrix, relation_env, relation_request


def test_relation_type_must_resolve() -> None:
    _declare("relation type must resolve")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(
        matrix,
        env,
        replace(request, relation_type_id=RelationTypeId("UNKNOWN")),
    )
    assert result.state is RelationEvaluationState.INVALID
    assert result.failure_codes == (USMFailureCode.RELATION_TYPE_UNRESOLVED,)


def test_relation_science_must_match_matrix() -> None:
    _declare("science must match matrix")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, replace(request, science_id=ScienceId("FOREIGN")))
    assert result.failure_codes == (USMFailureCode.RELATION_SCIENCE_MISMATCH,)


def test_relation_matrix_must_match_request() -> None:
    _declare("matrix must match request")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(
        matrix, env, replace(request, matrix_id=MatrixId("OtherReferenceMatrixV1"))
    )
    assert result.state is RelationEvaluationState.INVALID
    assert result.failure_codes == (USMFailureCode.RELATION_MATRIX_MISMATCH,)


def test_all_operands_must_resolve() -> None:
    _declare("all operands must resolve")
    matrix, env, request = _make_case(1)
    bad = replace(
        request.operand_bindings[0],
        entity_instance_ref=EntityInstanceRef("entity://c4/ghost"),
    )
    result = evaluate_relation(
        matrix,
        env,
        replace(request, operand_bindings=(bad,) + request.operand_bindings[1:]),
    )
    assert result.state is RelationEvaluationState.DEFERRED
    assert result.failure_codes == (USMFailureCode.RELATION_OPERAND_UNRESOLVED,)


def test_arity_must_match_contract() -> None:
    _declare("arity must match")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(
        matrix,
        env,
        replace(request, operand_bindings=request.operand_bindings[:-1]),
    )
    assert result.failure_codes == (USMFailureCode.RELATION_ARITY_MISMATCH,)


def test_roles_must_be_unique_when_required() -> None:
    _declare("roles unique")
    matrix, env, request = _make_case(1)
    dup = replace(request.operand_bindings[1], role_id=request.operand_bindings[0].role_id)
    result = evaluate_relation(
        matrix,
        env,
        replace(request, operand_bindings=(request.operand_bindings[0], dup)),
    )
    assert result.failure_codes == (USMFailureCode.RELATION_ROLE_DUPLICATED,)


def test_operand_type_must_match_role_signature() -> None:
    _declare("operand type must match")
    matrix, env, request = _make_case(2)
    swapped_entity = replace(
        env.entity_instances[0], entity_type_id=env.entity_instances[1].entity_type_id
    )
    bad_env = replace(env, entity_instances=(swapped_entity,) + env.entity_instances[1:])
    result = evaluate_relation(matrix, bad_env, request)
    assert result.failure_codes == (USMFailureCode.RELATION_OPERAND_TYPE_MISMATCH,)


def test_directed_relation_rejects_reversed_roles() -> None:
    _declare("directed relation rejects reversed roles")
    matrix, env, request = _make_case(0)
    reversed_bindings = (
        replace(request.operand_bindings[0], role_id=request.operand_bindings[1].role_id),
        replace(request.operand_bindings[1], role_id=request.operand_bindings[0].role_id),
    )
    result = evaluate_relation(matrix, env, replace(request, operand_bindings=reversed_bindings))
    assert result.failure_codes == (USMFailureCode.RELATION_DIRECTION_MISMATCH,)


def test_capability_result_must_resolve() -> None:
    _declare("capability result must resolve")
    matrix, env, request = _make_case(1)
    bad = replace(
        request.operand_bindings[0],
        capability_result_ref=CapabilityEvaluationRef("cap-req-missing"),
    )
    result = evaluate_relation(
        matrix,
        env,
        replace(request, operand_bindings=(bad,) + request.operand_bindings[1:]),
    )
    assert result.failure_codes == (USMFailureCode.RELATION_CAPABILITY_RESULT_UNRESOLVED,)


def test_capability_result_must_belong_to_operand() -> None:
    _declare("capability result must belong to operand")
    matrix, env, request = _make_case(2)
    swapped = (
        replace(
            request.operand_bindings[0],
            capability_result_ref=request.operand_bindings[1].capability_result_ref,
        ),
        request.operand_bindings[1],
    )
    result = evaluate_relation(matrix, env, replace(request, operand_bindings=swapped))
    assert result.failure_codes == (USMFailureCode.RELATION_CAPABILITY_PROVENANCE_MISMATCH,)


def test_blocked_capability_cannot_open_relation() -> None:
    _declare("blocked capability blocks relation")
    matrix, env, request = _make_case(1)
    blocked = replace(
        env.capability_results[0],
        state=CapabilityEvaluationState.BLOCKED,
        granted_rank=Rank.ZERO,
        failure_codes=(USMFailureCode.CAPABILITY_BLOCKER_ACTIVE,),
    )
    bad_env = replace(env, capability_results=(blocked,) + env.capability_results[1:])
    result = evaluate_relation(matrix, bad_env, request)
    assert result.failure_codes == (USMFailureCode.RELATION_CAPABILITY_NOT_ELIGIBLE,)


def test_invalid_capability_cannot_open_relation() -> None:
    _declare("invalid capability blocks relation")
    matrix, env, request = _make_case(1)
    invalid = replace(
        env.capability_results[0],
        state=CapabilityEvaluationState.INVALID,
        granted_rank=Rank.ZERO,
        failure_codes=(USMFailureCode.CAPABILITY_TRACE_CHAIN_BROKEN,),
    )
    bad_env = replace(env, capability_results=(invalid,) + env.capability_results[1:])
    result = evaluate_relation(matrix, bad_env, request)
    assert result.failure_codes == (USMFailureCode.RELATION_CAPABILITY_NOT_ELIGIBLE,)


def test_missing_condition_is_deferred() -> None:
    _declare("missing condition deferred")
    matrix, env, request = _make_case(1)
    empty_context = replace(env.contexts[0], active_condition_refs=())
    result = evaluate_relation(matrix, replace(env, contexts=(empty_context,)), request)
    assert result.state is RelationEvaluationState.DEFERRED
    assert result.failure_codes == (USMFailureCode.RELATION_REQUIRED_CONDITION_MISSING,)


def test_active_blocker_is_blocked() -> None:
    _declare("active blocker blocked")
    matrix, env, request = _make_case(1)
    blocker_context = replace(
        env.contexts[0],
        active_blocker_refs=(RuleId(matrix.relations[0].saturation_rule.value),),
    )
    result = evaluate_relation(matrix, replace(env, contexts=(blocker_context,)), request)
    assert result.state is RelationEvaluationState.BLOCKED
    assert result.failure_codes == (USMFailureCode.RELATION_BLOCKER_ACTIVE,)


def test_blocking_residual_prevents_eligible_with_residuals() -> None:
    _declare("blocking residual prevents eligible")
    matrix, env, request = _make_case(1)
    blocking = USMResidual(
        residual_id="relation-blocking",
        kind=USMResidualKind.COVERAGE_GAP,
        detail="blocking residual",
        blocking=True,
        visible=True,
        repair_hint="resolve",
    )
    blocked_entity = replace(env.entity_instances[0], residuals=(blocking,))
    result = evaluate_relation(
        matrix,
        replace(
            env, entity_instances=(blocked_entity,) + env.entity_instances[1:]
        ),
        request,
    )
    assert result.failure_codes == (USMFailureCode.RELATION_BLOCKING_RESIDUAL,)


def test_entity_rank_bounds_relation_rank() -> None:
    _declare("entity rank bounds relation rank")
    matrix, env, request = _make_case(1)
    low = replace(env.entity_instances[0], state_rank=Rank.TRACE)
    low_cap = replace(env.capability_results[0], granted_rank=Rank.TRACE)
    bad_env = replace(
        env,
        entity_instances=(low,) + env.entity_instances[1:],
        capability_results=(low_cap,) + env.capability_results[1:],
    )
    result = evaluate_relation(matrix, bad_env, request)
    assert result.failure_codes == (USMFailureCode.RELATION_RANK_CEILING_EXCEEDED,)


def test_capability_rank_bounds_relation_rank() -> None:
    _declare("capability rank bounds relation rank")
    matrix, env, request = _make_case(1)
    low_cap = replace(env.capability_results[0], granted_rank=Rank.TRACE)
    result = evaluate_relation(
        matrix,
        replace(env, capability_results=(low_cap,) + env.capability_results[1:]),
        request,
    )
    assert result.failure_codes == (USMFailureCode.RELATION_RANK_CEILING_EXCEEDED,)


def test_relation_evaluator_never_promotes_operand_rank() -> None:
    _declare("never promotes operand rank")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert result.granted_rank <= min(entity.state_rank for entity in env.entity_instances)


def test_relation_evaluation_emits_new_trace() -> None:
    _declare("emits new trace")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert result.trace_ref != request.trace_ref


def test_broken_relation_trace_chain_is_invalid() -> None:
    _declare("broken relation trace invalid")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, replace(request, trace_ref=TraceRef("trace://foreign/root")))
    assert result.state is RelationEvaluationState.INVALID
    assert result.failure_codes == (USMFailureCode.RELATION_TRACE_CHAIN_BROKEN,)


def test_refusal_also_emits_trace() -> None:
    _declare("refusal emits trace")
    matrix, env, request = _make_case(1)
    bad = replace(
        request.operand_bindings[0],
        entity_instance_ref=EntityInstanceRef("entity://ghost"),
    )
    result = evaluate_relation(
        matrix,
        env,
        replace(request, operand_bindings=(bad,) + request.operand_bindings[1:]),
    )
    assert result.trace_ref != request.trace_ref


def test_structural_saturation_does_not_claim_semantic_closure() -> None:
    _declare("structural saturation not semantic closure")
    matrix, env, request = _make_case(0)
    result = evaluate_relation(matrix, env, request)
    assert result.structural_saturation is True
    assert not hasattr(result, "semantic_saturation")


def test_structural_saturation_does_not_claim_ifadah() -> None:
    _declare("structural saturation not ifadah")
    matrix, env, request = _make_case(0)
    result = evaluate_relation(matrix, env, request)
    assert not hasattr(result, "ifadah")


def test_relation_eligibility_does_not_establish_external_relation() -> None:
    _declare("eligibility not external relation truth")
    matrix, env, request = _make_case(0)
    result = evaluate_relation(matrix, env, request)
    assert not hasattr(result, "relation_true")


def test_relation_result_does_not_execute_transformation() -> None:
    _declare("no transformation execution")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert not hasattr(result, "transformation_executed")


def test_relation_result_does_not_issue_transition_certificate() -> None:
    _declare("no transition certificate")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert "CERTIFICATE" not in repr(result).upper()


def test_relation_result_does_not_create_approved_transition_context() -> None:
    _declare("no approved transition context")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert not hasattr(result, "approved_transition_context")


def test_relation_result_does_not_prove_claim() -> None:
    _declare("no claim proof")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert not hasattr(result, "claim_proven")


def test_relation_result_does_not_claim_truth() -> None:
    _declare("no truth claim")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert not hasattr(result, "external_truth")


def test_relation_result_does_not_execute_bridge() -> None:
    _declare("no bridge execution")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert "BRIDGE_EXECUTED" not in repr(result).upper()


def test_success_arabic_structural_relation_only() -> None:
    _declare("arabic positive bounded eligibility")
    matrix, env, request = _make_case(0)
    result = evaluate_relation(matrix, env, request)
    assert result.state in {
        RelationEvaluationState.ELIGIBLE,
        RelationEvaluationState.ELIGIBLE_WITH_RESIDUALS,
    }
    assert result.structural_saturation is True


def test_success_math_membership_or_order_relation_only() -> None:
    _declare("math positive bounded eligibility")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, request)
    assert result.state in {
        RelationEvaluationState.ELIGIBLE,
        RelationEvaluationState.ELIGIBLE_WITH_RESIDUALS,
    }
    assert result.granted_rank <= Rank.CANDIDATE


def test_success_mechanics_structural_effect_relation_only() -> None:
    _declare("mechanics positive bounded eligibility")
    matrix, env, request = _make_case(2)
    result = evaluate_relation(matrix, env, request)
    assert result.state in {
        RelationEvaluationState.ELIGIBLE,
        RelationEvaluationState.ELIGIBLE_WITH_RESIDUALS,
    }
    assert result.structural_saturation is True


def test_science_mismatch_is_prioritized_over_missing_condition() -> None:
    _declare("science mismatch priority")
    matrix, env, request = _make_case(1)
    context = replace(env.contexts[0], active_condition_refs=())
    result = evaluate_relation(
        matrix,
        replace(env, contexts=(context,)),
        replace(request, science_id=ScienceId("FOREIGN")),
    )
    assert result.failure_codes == (USMFailureCode.RELATION_SCIENCE_MISMATCH,)


def test_unknown_operand_is_not_reported_as_type_mismatch() -> None:
    _declare("unknown operand priority")
    matrix, env, request = _make_case(2)
    bad = replace(
        request.operand_bindings[0],
        entity_instance_ref=EntityInstanceRef("entity://unknown"),
    )
    result = evaluate_relation(
        matrix,
        env,
        replace(request, operand_bindings=(bad,) + request.operand_bindings[1:]),
    )
    assert result.failure_codes == (USMFailureCode.RELATION_OPERAND_UNRESOLVED,)


def test_capability_result_unresolved_is_not_ineligible_failure() -> None:
    _declare("capability unresolved priority")
    matrix, env, request = _make_case(1)
    bad = replace(
        request.operand_bindings[0],
        capability_result_ref=CapabilityEvaluationRef("missing-ref"),
    )
    result = evaluate_relation(
        matrix,
        env,
        replace(request, operand_bindings=(bad,) + request.operand_bindings[1:]),
    )
    assert result.failure_codes == (USMFailureCode.RELATION_CAPABILITY_RESULT_UNRESOLVED,)


def test_trace_break_is_invalid_not_blocked() -> None:
    _declare("trace break invalid")
    matrix, env, request = _make_case(1)
    result = evaluate_relation(matrix, env, replace(request, trace_ref=TraceRef("trace://outside")))
    assert result.state is RelationEvaluationState.INVALID


def test_evaluator_is_pure_and_deterministic() -> None:
    _declare("evaluator purity and determinism")
    matrix, env, request = _make_case(1)
    matrix_before = asdict(matrix)
    env_before = asdict(env)
    request_before = asdict(request)
    result_one = evaluate_relation(matrix, env, request)
    result_two = evaluate_relation(matrix, env, request)
    assert matrix_before == asdict(matrix)
    assert env_before == asdict(env)
    assert request_before == asdict(request)
    assert result_one == result_two
