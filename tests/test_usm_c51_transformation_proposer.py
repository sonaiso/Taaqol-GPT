"""USM-C5.1 bounded transformation proposal construction tests."""

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
    RelationOperandBinding,
    RequestId,
    RoleId,
    RuleId,
    TraceRef,
    TransformationLinkEnvironment,
    TransformationLinkRequest,
    TransformationLinkState,
    TransformationProposalEnvironment,
    TransformationProposalRequest,
    TransformationProposalState,
    TransformationTypeId,
    USMFailureCode,
    construct_transformation_proposal,
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
        branch_name=f"USM-C5.1 ({branch_note})",
        constitutional_chain=(
            "docs/14",
            "USM-C2.1",
            "USM-C3",
            "USM-C3.1",
            "USM-C4",
            "USM-C5",
            "USM-C5.1",
        ),
        chain_position="USM-C5.1 bounded transformation proposal construction",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md",
        branch_of_origin="USM bounded relation/transformation branch",
        forbidden_shortcut_assertions=(
            "TransformationLinkEligible -> TransformationExecuted",
            "ProposalConstructed -> TransformationExecuted",
            "ProposalConstructed -> TransitionCertificate",
            "ProposalConstructed -> ClaimProven",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "TransformationExecuted",
            "ExecutionResultCandidate",
            "TransitionCertificate",
            "ClaimVerdict",
            "JudgmentVerdict",
            "ExternalTruthCertificate",
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
            capability_id=CapabilityId(f"C51_CAP_{matrix_index}_{position}"),
            bearer_type=relation.operand_types[position],
            permitted_relation_roles=(relation.roles[position],),
            required_conditions=(RuleId(f"C51_CAP_REQ_{matrix_index}_{position}"),),
            blockers=(RuleId(f"C51_CAP_BLK_{matrix_index}_{position}"),),
            evidence_requirements=(evidence_type,),
            rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(
                f"{matrix.trace_ref.value}/capabilities/c51/{matrix_index}/{position}"
            ),
        )
        for position in range(relation.arity)
    )
    transformation = TransformationContract(
        transformation_type_id=TransformationTypeId(f"C51_TRANSFORM_{matrix_index}"),
        science_id=matrix.science_id,
        source_types=relation.operand_types,
        target_types=relation.operand_types,
        required_capabilities=tuple(item.capability_id for item in capabilities),
        preserved_invariants=(RuleId(f"C51_TRANSFORM_INV_{matrix_index}"),),
        declared_changes=(RuleId(f"C51_TRANSFORM_CHANGE_{matrix_index}"),),
        required_conditions=(RuleId(f"C51_TRANSFORM_REQ_{matrix_index}"),),
        blockers=(RuleId(f"C51_TRANSFORM_BLK_{matrix_index}"),),
        evidence_requirements=(evidence_type,),
        rank_ceiling=Rank.CANDIDATE,
        residual_policy_ref=RuleId(f"C51_RESIDUAL_POLICY_{matrix_index}"),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/transformations/c51/{matrix_index}"),
    )
    matrix = replace(
        matrix,
        capabilities=matrix.capabilities + capabilities,
        transformations=matrix.transformations + (transformation,),
    )

    entities = tuple(
        EntityInstanceContract(
            entity_instance_ref=EntityInstanceRef(f"entity://c51/{matrix_index}/{position}"),
            entity_type_id=relation.operand_types[position],
            science_id=matrix.science_id,
            matrix_id=matrix.matrix_id,
            state_rank=Rank.CANDIDATE,
            active_property_refs=(),
            residuals=(),
            trace_ref=TraceRef(f"{matrix.trace_ref.value}/entities/c51/{matrix_index}/{position}"),
        )
        for position in range(relation.arity)
    )
    context = EvaluationContextContract(
        context_id=ContextId(f"context://c51/{matrix_index}"),
        science_id=matrix.science_id,
        matrix_id=matrix.matrix_id,
        active_condition_refs=(
            tuple(
                RuleId(f"C51_CAP_REQ_{matrix_index}_{position}")
                for position in range(relation.arity)
            )
            + relation.compatibility_rules
            + (relation.saturation_rule, relation.scope_rule)
            + transformation.required_conditions
        ),
        active_blocker_refs=(),
        supplied_evidence_type_refs=(evidence_type,),
        residuals=(),
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/contexts/c51/{matrix_index}"),
    )
    capability_env = CapabilityEvaluationEnvironment(entity_instances=entities, contexts=(context,))
    capability_results = tuple(
        evaluate_capability(
            matrix,
            capability_env,
            CapabilityEvaluationRequest(
                request_id=RequestId(f"c51-cap-req-{matrix_index}-{position}"),
                matrix_id=matrix.matrix_id,
                science_id=matrix.science_id,
                entity_type_id=entities[position].entity_type_id,
                entity_instance_ref=entities[position].entity_instance_ref,
                capability_id=capabilities[position].capability_id,
                context_id=context.context_id,
                supplied_condition_refs=(RuleId(f"C51_CAP_REQ_{matrix_index}_{position}"),),
                supplied_evidence_type_refs=(evidence_type,),
                active_blocker_refs=(),
                requested_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref=TraceRef(
                    f"{matrix.trace_ref.value}/requests/c51-cap-req-{matrix_index}-{position}"
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
        request_id=RequestId(f"c51-rel-req-{matrix_index}"),
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
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/requests/c51-rel-req-{matrix_index}"),
    )
    relation_result = evaluate_relation(matrix, relation_env, relation_request)
    link_env = TransformationLinkEnvironment(
        entity_instances=entities,
        contexts=(context,),
        capability_results=capability_results,
        relation_requests=(relation_request,),
        relation_results=(relation_result,),
    )
    link_request = TransformationLinkRequest(
        request_id=RequestId(f"c51-link-req-{matrix_index}"),
        matrix_id=matrix.matrix_id,
        science_id=matrix.science_id,
        transformation_type_id=transformation.transformation_type_id,
        relation_request_id=relation_request.request_id,
        requested_rank=Rank.CANDIDATE,
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/requests/c51-link-req-{matrix_index}"),
    )
    link_result = evaluate_transformation_link(matrix, link_env, link_request)

    proposal_env = TransformationProposalEnvironment(
        entity_instances=entities,
        contexts=(context,),
        capability_results=capability_results,
        relation_requests=(relation_request,),
        relation_results=(relation_result,),
        link_results=(link_result,),
    )
    proposal_request = TransformationProposalRequest(
        request_id=RequestId(f"c51-proposal-req-{matrix_index}"),
        matrix_id=matrix.matrix_id,
        science_id=matrix.science_id,
        transformation_type_id=transformation.transformation_type_id,
        relation_request_id=relation_request.request_id,
        link_request_id=link_request.request_id,
        identity_policy_ref=RuleId(f"C51_IDENTITY_POLICY_{matrix_index}"),
        rollback_requirements=(RuleId(f"C51_ROLLBACK_{matrix_index}"),),
        requested_rank=Rank.CANDIDATE,
        trace_ref=TraceRef(f"{matrix.trace_ref.value}/requests/c51-proposal-req-{matrix_index}"),
    )
    return matrix, proposal_env, proposal_request


def test_link_result_must_resolve() -> None:
    _declare("link result must resolve")
    matrix, env, request = _make_case(1)
    result = construct_transformation_proposal(
        matrix, env, replace(request, link_request_id=RequestId("missing-link-result"))
    )
    assert result.state is TransformationProposalState.DEFERRED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_LINK_RESULT_UNRESOLVED,)


def test_link_result_must_be_eligible() -> None:
    _declare("link result must be eligible")
    matrix, env, request = _make_case(1)
    blocked_link = replace(
        env.link_results[0],
        state=TransformationLinkState.BLOCKED,
        granted_rank=Rank.ZERO,
        failure_codes=(USMFailureCode.TRANSFORMATION_BLOCKER_ACTIVE,),
    )
    blocked_env = replace(env, link_results=(blocked_link,))
    result = construct_transformation_proposal(matrix, blocked_env, request)
    assert result.state is TransformationProposalState.BLOCKED
    assert result.failure_codes == (USMFailureCode.TRANSFORMATION_LINK_NOT_ELIGIBLE,)


def test_proposal_construction_is_bounded_not_executive() -> None:
    _declare("proposal construction only")
    matrix, env, request = _make_case(1)
    result = construct_transformation_proposal(matrix, env, request)
    assert result.state in {
        TransformationProposalState.CONSTRUCTED,
        TransformationProposalState.CONSTRUCTED_WITH_RESIDUALS,
    }
    assert result.proposal is not None
    assert result.proposal.transformation_type_id == request.transformation_type_id
    assert result.proposal.identity_policy_ref == request.identity_policy_ref
    assert result.proposal.rollback_requirements == request.rollback_requirements
    assert not hasattr(result, "transformation_executed")
    assert "CERTIFICATE" not in repr(result).upper()


def test_trace_chain_break_is_invalid() -> None:
    _declare("trace chain break invalid")
    matrix, env, request = _make_case(1)
    result = construct_transformation_proposal(
        matrix, env, replace(request, trace_ref=TraceRef("trace://foreign/root"))
    )
    assert result.state is TransformationProposalState.INVALID
    assert result.failure_codes == (
        USMFailureCode.TRANSFORMATION_PROPOSAL_TRACE_CHAIN_BROKEN,
    )


def test_refusal_also_emits_trace() -> None:
    _declare("refusal emits trace")
    matrix, env, request = _make_case(1)
    result = construct_transformation_proposal(
        matrix,
        env,
        replace(request, transformation_type_id=TransformationTypeId("UNKNOWN")),
    )
    assert result.state is TransformationProposalState.INVALID
    assert result.trace_ref != request.trace_ref


def test_proposal_constructor_is_pure_and_deterministic() -> None:
    _declare("pure and deterministic")
    matrix, env, request = _make_case(1)
    matrix_before = asdict(matrix)
    env_before = asdict(env)
    request_before = asdict(request)
    result_one = construct_transformation_proposal(matrix, env, request)
    result_two = construct_transformation_proposal(matrix, env, request)
    assert matrix_before == asdict(matrix)
    assert env_before == asdict(env)
    assert request_before == asdict(request)
    assert result_one == result_two
