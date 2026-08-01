"""USM-C5.1 bounded transformation proposal construction (pure, deterministic, non-executive)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.usm.capability_evaluator import (
    CapabilityEvaluationResult,
    CapabilityEvaluationState,
    EntityInstanceContract,
    EvaluationContextContract,
)
from taaqqul_slot_geometry.usm.identifiers import (
    ContextId,
    EntityInstanceRef,
    EntityTypeId,
    MatrixId,
    RequestId,
    RuleId,
    ScienceId,
    TraceRef,
    TransformationTypeId,
    USMSchemaError,
    require_tuple_of_type,
)
from taaqqul_slot_geometry.usm.matrix import UniversalScienceMatrix
from taaqqul_slot_geometry.usm.relation_evaluator import (
    RelationEvaluationRequest,
    RelationEvaluationResult,
    RelationEvaluationState,
)
from taaqqul_slot_geometry.usm.residuals import USMResidual
from taaqqul_slot_geometry.usm.transformation_linker import (
    TransformationLinkResult,
    TransformationLinkState,
)
from taaqqul_slot_geometry.usm.validator import USMFailureCode


class TransformationProposalState(StrEnum):
    CONSTRUCTED = "CONSTRUCTED"
    CONSTRUCTED_WITH_RESIDUALS = "CONSTRUCTED_WITH_RESIDUALS"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class TransformationProposalRequest:
    request_id: RequestId
    matrix_id: MatrixId
    science_id: ScienceId
    transformation_type_id: TransformationTypeId
    relation_request_id: RequestId
    link_request_id: RequestId
    identity_policy_ref: RuleId
    rollback_requirements: tuple[RuleId, ...]
    requested_rank: Rank
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, RequestId):
            raise USMSchemaError("TransformationProposalRequest.request_id must be RequestId")
        if not isinstance(self.matrix_id, MatrixId):
            raise USMSchemaError("TransformationProposalRequest.matrix_id must be MatrixId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("TransformationProposalRequest.science_id must be ScienceId")
        if not isinstance(self.transformation_type_id, TransformationTypeId):
            raise USMSchemaError(
                "TransformationProposalRequest.transformation_type_id must be TransformationTypeId"
            )
        if not isinstance(self.relation_request_id, RequestId):
            raise USMSchemaError(
                "TransformationProposalRequest.relation_request_id must be RequestId"
            )
        if not isinstance(self.link_request_id, RequestId):
            raise USMSchemaError("TransformationProposalRequest.link_request_id must be RequestId")
        if not isinstance(self.identity_policy_ref, RuleId):
            raise USMSchemaError(
                "TransformationProposalRequest.identity_policy_ref must be RuleId"
            )
        require_tuple_of_type(
            "TransformationProposalRequest",
            "rollback_requirements",
            self.rollback_requirements,
            RuleId,
        )
        if not isinstance(self.requested_rank, Rank):
            raise USMSchemaError("TransformationProposalRequest.requested_rank must be Rank")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("TransformationProposalRequest.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class TransformationProposalEnvironment:
    entity_instances: tuple[EntityInstanceContract, ...]
    contexts: tuple[EvaluationContextContract, ...]
    capability_results: tuple[CapabilityEvaluationResult, ...]
    relation_requests: tuple[RelationEvaluationRequest, ...]
    relation_results: tuple[RelationEvaluationResult, ...]
    link_results: tuple[TransformationLinkResult, ...]

    def __post_init__(self) -> None:
        require_tuple_of_type(
            "TransformationProposalEnvironment",
            "entity_instances",
            self.entity_instances,
            EntityInstanceContract,
        )
        require_tuple_of_type(
            "TransformationProposalEnvironment",
            "contexts",
            self.contexts,
            EvaluationContextContract,
        )
        require_tuple_of_type(
            "TransformationProposalEnvironment",
            "capability_results",
            self.capability_results,
            CapabilityEvaluationResult,
        )
        require_tuple_of_type(
            "TransformationProposalEnvironment",
            "relation_requests",
            self.relation_requests,
            RelationEvaluationRequest,
        )
        require_tuple_of_type(
            "TransformationProposalEnvironment",
            "relation_results",
            self.relation_results,
            RelationEvaluationResult,
        )
        require_tuple_of_type(
            "TransformationProposalEnvironment",
            "link_results",
            self.link_results,
            TransformationLinkResult,
        )
        if len({item.entity_instance_ref for item in self.entity_instances}) != len(
            self.entity_instances
        ):
            raise USMSchemaError(
                "TransformationProposalEnvironment.entity_instances has duplicate references"
            )
        if len({item.context_id for item in self.contexts}) != len(self.contexts):
            raise USMSchemaError(
                "TransformationProposalEnvironment.contexts has duplicate references"
            )
        if len({item.request_id for item in self.capability_results}) != len(
            self.capability_results
        ):
            raise USMSchemaError(
                "TransformationProposalEnvironment.capability_results has duplicate references"
            )
        if len({item.request_id for item in self.relation_requests}) != len(
            self.relation_requests
        ):
            raise USMSchemaError(
                "TransformationProposalEnvironment.relation_requests has duplicate references"
            )
        if len({item.request_id for item in self.relation_results}) != len(
            self.relation_results
        ):
            raise USMSchemaError(
                "TransformationProposalEnvironment.relation_results has duplicate references"
            )
        if len({item.request_id for item in self.link_results}) != len(self.link_results):
            raise USMSchemaError(
                "TransformationProposalEnvironment.link_results has duplicate references"
            )

    def resolve_context(self, context_id: ContextId) -> EvaluationContextContract | None:
        return next((item for item in self.contexts if item.context_id == context_id), None)

    def resolve_entity(self, entity_ref: object) -> EntityInstanceContract | None:
        return next(
            (
                item
                for item in self.entity_instances
                if item.entity_instance_ref == entity_ref
            ),
            None,
        )

    def resolve_capability_result(
        self, capability_result_ref: object
    ) -> CapabilityEvaluationResult | None:
        return next(
            (
                item
                for item in self.capability_results
                if item.request_id.value == capability_result_ref.value
            ),
            None,
        )

    def resolve_relation_request(self, request_id: RequestId) -> RelationEvaluationRequest | None:
        return next(
            (item for item in self.relation_requests if item.request_id == request_id),
            None,
        )

    def resolve_relation_result(self, request_id: RequestId) -> RelationEvaluationResult | None:
        return next(
            (item for item in self.relation_results if item.request_id == request_id),
            None,
        )

    def resolve_link_result(self, request_id: RequestId) -> TransformationLinkResult | None:
        return next((item for item in self.link_results if item.request_id == request_id), None)


@dataclass(frozen=True, slots=True)
class TransformationProposalTrace:
    evaluation_trace_ref: TraceRef
    request_trace_ref: TraceRef
    link_trace_ref: TraceRef
    relation_trace_ref: TraceRef
    transformation_trace_ref: TraceRef
    context_trace_ref: TraceRef
    matrix_trace_ref: TraceRef
    source_entity_trace_refs: tuple[TraceRef, ...]
    capability_trace_refs: tuple[TraceRef, ...]
    decision_stage: str

    def __post_init__(self) -> None:
        if not isinstance(self.evaluation_trace_ref, TraceRef):
            raise USMSchemaError(
                "TransformationProposalTrace.evaluation_trace_ref must be TraceRef"
            )
        if not isinstance(self.request_trace_ref, TraceRef):
            raise USMSchemaError("TransformationProposalTrace.request_trace_ref must be TraceRef")
        if not isinstance(self.link_trace_ref, TraceRef):
            raise USMSchemaError("TransformationProposalTrace.link_trace_ref must be TraceRef")
        if not isinstance(self.relation_trace_ref, TraceRef):
            raise USMSchemaError("TransformationProposalTrace.relation_trace_ref must be TraceRef")
        if not isinstance(self.transformation_trace_ref, TraceRef):
            raise USMSchemaError(
                "TransformationProposalTrace.transformation_trace_ref must be TraceRef"
            )
        if not isinstance(self.context_trace_ref, TraceRef):
            raise USMSchemaError("TransformationProposalTrace.context_trace_ref must be TraceRef")
        if not isinstance(self.matrix_trace_ref, TraceRef):
            raise USMSchemaError("TransformationProposalTrace.matrix_trace_ref must be TraceRef")
        require_tuple_of_type(
            "TransformationProposalTrace",
            "source_entity_trace_refs",
            self.source_entity_trace_refs,
            TraceRef,
        )
        require_tuple_of_type(
            "TransformationProposalTrace",
            "capability_trace_refs",
            self.capability_trace_refs,
            TraceRef,
        )
        if not isinstance(self.decision_stage, str) or not self.decision_stage:
            raise USMSchemaError(
                "TransformationProposalTrace.decision_stage must be non-empty str"
            )
        if self.evaluation_trace_ref == self.request_trace_ref:
            raise USMSchemaError("TransformationProposalTrace must emit a new trace event")


@dataclass(frozen=True, slots=True)
class TransformationProposal:
    proposal_id: RequestId
    matrix_id: MatrixId
    science_id: ScienceId
    relation_request_id: RequestId
    link_request_id: RequestId
    source_state_refs: tuple[EntityInstanceRef, ...]
    transformation_type_id: TransformationTypeId
    target_type_ids: tuple[EntityTypeId, ...]
    identity_policy_ref: RuleId
    preserved_invariants: tuple[RuleId, ...]
    declared_changes: tuple[RuleId, ...]
    required_conditions: tuple[RuleId, ...]
    active_blockers: tuple[RuleId, ...]
    expected_effects: tuple[RuleId, ...]
    rank_ceiling: Rank
    residual_policy_ref: RuleId
    rollback_requirements: tuple[RuleId, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.proposal_id, RequestId):
            raise USMSchemaError("TransformationProposal.proposal_id must be RequestId")
        if not isinstance(self.matrix_id, MatrixId):
            raise USMSchemaError("TransformationProposal.matrix_id must be MatrixId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("TransformationProposal.science_id must be ScienceId")
        if not isinstance(self.relation_request_id, RequestId):
            raise USMSchemaError(
                "TransformationProposal.relation_request_id must be RequestId"
            )
        if not isinstance(self.link_request_id, RequestId):
            raise USMSchemaError("TransformationProposal.link_request_id must be RequestId")
        require_tuple_of_type(
            "TransformationProposal",
            "source_state_refs",
            self.source_state_refs,
            EntityInstanceRef,
        )
        if not isinstance(self.transformation_type_id, TransformationTypeId):
            raise USMSchemaError(
                "TransformationProposal.transformation_type_id must be TransformationTypeId"
            )
        require_tuple_of_type(
            "TransformationProposal",
            "target_type_ids",
            self.target_type_ids,
            EntityTypeId,
        )
        if not isinstance(self.identity_policy_ref, RuleId):
            raise USMSchemaError("TransformationProposal.identity_policy_ref must be RuleId")
        require_tuple_of_type(
            "TransformationProposal",
            "preserved_invariants",
            self.preserved_invariants,
            RuleId,
        )
        require_tuple_of_type(
            "TransformationProposal",
            "declared_changes",
            self.declared_changes,
            RuleId,
        )
        require_tuple_of_type(
            "TransformationProposal",
            "required_conditions",
            self.required_conditions,
            RuleId,
        )
        require_tuple_of_type(
            "TransformationProposal", "active_blockers", self.active_blockers, RuleId
        )
        require_tuple_of_type(
            "TransformationProposal", "expected_effects", self.expected_effects, RuleId
        )
        if not isinstance(self.rank_ceiling, Rank):
            raise USMSchemaError("TransformationProposal.rank_ceiling must be Rank")
        if not isinstance(self.residual_policy_ref, RuleId):
            raise USMSchemaError("TransformationProposal.residual_policy_ref must be RuleId")
        require_tuple_of_type(
            "TransformationProposal",
            "rollback_requirements",
            self.rollback_requirements,
            RuleId,
        )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("TransformationProposal.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class TransformationProposalResult:
    request_id: RequestId
    state: TransformationProposalState
    transformation_type_id: TransformationTypeId
    relation_request_id: RequestId
    link_request_id: RequestId
    granted_rank: Rank
    proposal: TransformationProposal | None
    failure_codes: tuple[USMFailureCode, ...]
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef
    evaluation_trace: TransformationProposalTrace

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, RequestId):
            raise USMSchemaError("TransformationProposalResult.request_id must be RequestId")
        if not isinstance(self.state, TransformationProposalState):
            raise USMSchemaError(
                "TransformationProposalResult.state must be TransformationProposalState"
            )
        if not isinstance(self.transformation_type_id, TransformationTypeId):
            raise USMSchemaError(
                "TransformationProposalResult.transformation_type_id must be TransformationTypeId"
            )
        if not isinstance(self.relation_request_id, RequestId):
            raise USMSchemaError(
                "TransformationProposalResult.relation_request_id must be RequestId"
            )
        if not isinstance(self.link_request_id, RequestId):
            raise USMSchemaError(
                "TransformationProposalResult.link_request_id must be RequestId"
            )
        if not isinstance(self.granted_rank, Rank):
            raise USMSchemaError("TransformationProposalResult.granted_rank must be Rank")
        if self.proposal is not None and not isinstance(self.proposal, TransformationProposal):
            raise USMSchemaError(
                "TransformationProposalResult.proposal must be TransformationProposal | None"
            )
        require_tuple_of_type(
            "TransformationProposalResult", "failure_codes", self.failure_codes, USMFailureCode
        )
        require_tuple_of_type(
            "TransformationProposalResult", "residuals", self.residuals, USMResidual
        )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("TransformationProposalResult.trace_ref must be TraceRef")
        if not isinstance(self.evaluation_trace, TransformationProposalTrace):
            raise USMSchemaError(
                "TransformationProposalResult.evaluation_trace must be TransformationProposalTrace"
            )
        if self.trace_ref != self.evaluation_trace.evaluation_trace_ref:
            raise USMSchemaError(
                "TransformationProposalResult.trace_ref must equal "
                "evaluation_trace.evaluation_trace_ref"
            )
        self._assert_invariants()

    def _assert_invariants(self) -> None:
        if self.state is TransformationProposalState.CONSTRUCTED:
            if self.failure_codes:
                raise USMSchemaError("CONSTRUCTED proposal cannot carry failure codes")
            if self.proposal is None:
                raise USMSchemaError("CONSTRUCTED proposal requires TransformationProposal")
            if any(residual.blocking for residual in self.residuals):
                raise USMSchemaError("CONSTRUCTED proposal cannot carry blocking residuals")
            if self.residuals:
                raise USMSchemaError("CONSTRUCTED proposal cannot carry residuals")
            if self.granted_rank is Rank.ZERO:
                raise USMSchemaError("CONSTRUCTED proposal must grant non-zero rank")
            return
        if self.state is TransformationProposalState.CONSTRUCTED_WITH_RESIDUALS:
            if self.failure_codes:
                raise USMSchemaError(
                    "CONSTRUCTED_WITH_RESIDUALS proposal cannot carry failure codes"
                )
            if self.proposal is None:
                raise USMSchemaError(
                    "CONSTRUCTED_WITH_RESIDUALS proposal requires TransformationProposal"
                )
            if not self.residuals:
                raise USMSchemaError(
                    "CONSTRUCTED_WITH_RESIDUALS proposal requires visible residuals"
                )
            if any(residual.blocking for residual in self.residuals):
                raise USMSchemaError(
                    "CONSTRUCTED_WITH_RESIDUALS proposal cannot carry blocking residuals"
                )
            if self.granted_rank is Rank.ZERO:
                raise USMSchemaError(
                    "CONSTRUCTED_WITH_RESIDUALS proposal must grant non-zero rank"
                )
            return
        if self.proposal is not None:
            raise USMSchemaError("Non-constructed proposal results must not carry proposal payload")
        if self.granted_rank is not Rank.ZERO:
            raise USMSchemaError("Non-constructed proposal results must grant Rank.ZERO")


_ELIGIBLE_CAPABILITY_STATES = frozenset(
    {CapabilityEvaluationState.ELIGIBLE, CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS}
)
_ELIGIBLE_RELATION_STATES = frozenset(
    {RelationEvaluationState.ELIGIBLE, RelationEvaluationState.ELIGIBLE_WITH_RESIDUALS}
)
_ELIGIBLE_LINK_STATES = frozenset(
    {TransformationLinkState.ELIGIBLE, TransformationLinkState.ELIGIBLE_WITH_RESIDUALS}
)
_CONSTRUCTED_STATES = frozenset(
    {
        TransformationProposalState.CONSTRUCTED,
        TransformationProposalState.CONSTRUCTED_WITH_RESIDUALS,
    }
)
_BLOCKING_FAILURE_CODES = frozenset(
    {
        USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH,
        USMFailureCode.TRANSFORMATION_RELATION_NOT_ELIGIBLE,
        USMFailureCode.TRANSFORMATION_LINK_NOT_ELIGIBLE,
        USMFailureCode.TRANSFORMATION_RELATION_PROVENANCE_MISMATCH,
        USMFailureCode.TRANSFORMATION_SOURCE_TYPE_MISMATCH,
        USMFailureCode.TRANSFORMATION_CAPABILITY_NOT_ELIGIBLE,
        USMFailureCode.TRANSFORMATION_BLOCKER_ACTIVE,
        USMFailureCode.TRANSFORMATION_BLOCKING_RESIDUAL,
        USMFailureCode.TRANSFORMATION_RANK_CEILING_EXCEEDED,
    }
)
_DEFERRED_FAILURE_CODES = frozenset(
    {
        USMFailureCode.TRANSFORMATION_LINK_RESULT_UNRESOLVED,
        USMFailureCode.TRANSFORMATION_RELATION_REQUEST_UNRESOLVED,
        USMFailureCode.TRANSFORMATION_RELATION_RESULT_UNRESOLVED,
        USMFailureCode.TRANSFORMATION_SOURCE_ENTITY_UNRESOLVED,
        USMFailureCode.TRANSFORMATION_CAPABILITY_RESULT_UNRESOLVED,
    }
)


def construct_transformation_proposal(
    matrix: UniversalScienceMatrix,
    environment: TransformationProposalEnvironment,
    request: TransformationProposalRequest,
) -> TransformationProposalResult:
    """Construct a bounded transformation proposal from an eligible C5 link only."""

    if not isinstance(matrix, UniversalScienceMatrix):
        raise USMSchemaError("construct_transformation_proposal requires UniversalScienceMatrix")
    if not isinstance(environment, TransformationProposalEnvironment):
        raise USMSchemaError(
            "construct_transformation_proposal requires TransformationProposalEnvironment"
        )
    if not isinstance(request, TransformationProposalRequest):
        raise USMSchemaError(
            "construct_transformation_proposal requires TransformationProposalRequest"
        )

    failure_code: USMFailureCode | None = None
    state = TransformationProposalState.DEFERRED
    granted_rank = Rank.ZERO
    residuals: tuple[USMResidual, ...] = matrix.residuals
    proposal: TransformationProposal | None = None

    transformation = None
    link_result = None
    relation_request = None
    relation_result = None
    context = None
    resolved_entities: list[EntityInstanceContract] = []
    resolved_capability_results: list[CapabilityEvaluationResult] = []

    if request.matrix_id != matrix.matrix_id:
        failure_code = USMFailureCode.TRANSFORMATION_MATRIX_MISMATCH
        state = TransformationProposalState.INVALID
    elif request.science_id != matrix.science_id:
        failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
        state = TransformationProposalState.BLOCKED
    else:
        transformation = next(
            (
                item
                for item in matrix.transformations
                if item.transformation_type_id == request.transformation_type_id
            ),
            None,
        )
        if transformation is None:
            failure_code = USMFailureCode.TRANSFORMATION_TYPE_UNRESOLVED
            state = TransformationProposalState.INVALID
        elif transformation.science_id != matrix.science_id:
            failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
            state = TransformationProposalState.BLOCKED
        else:
            link_result = environment.resolve_link_result(request.link_request_id)
            if link_result is None:
                failure_code = USMFailureCode.TRANSFORMATION_LINK_RESULT_UNRESOLVED
                state = TransformationProposalState.DEFERRED
            elif (
                link_result.transformation_type_id != request.transformation_type_id
                or link_result.relation_request_id != request.relation_request_id
            ):
                failure_code = USMFailureCode.TRANSFORMATION_RELATION_PROVENANCE_MISMATCH
                state = TransformationProposalState.BLOCKED
            elif link_result.state not in _ELIGIBLE_LINK_STATES:
                failure_code = USMFailureCode.TRANSFORMATION_LINK_NOT_ELIGIBLE
                state = TransformationProposalState.BLOCKED
            else:
                relation_request = environment.resolve_relation_request(request.relation_request_id)
                if relation_request is None:
                    failure_code = USMFailureCode.TRANSFORMATION_RELATION_REQUEST_UNRESOLVED
                    state = TransformationProposalState.DEFERRED
                else:
                    relation_result = environment.resolve_relation_result(
                        request.relation_request_id
                    )
                    if relation_result is None:
                        failure_code = USMFailureCode.TRANSFORMATION_RELATION_RESULT_UNRESOLVED
                        state = TransformationProposalState.DEFERRED
                    elif relation_result.state not in _ELIGIBLE_RELATION_STATES:
                        failure_code = USMFailureCode.TRANSFORMATION_RELATION_NOT_ELIGIBLE
                        state = TransformationProposalState.BLOCKED
                    elif relation_request.science_id != matrix.science_id:
                        failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
                        state = TransformationProposalState.BLOCKED
                    elif relation_request.matrix_id != matrix.matrix_id:
                        failure_code = USMFailureCode.TRANSFORMATION_MATRIX_MISMATCH
                        state = TransformationProposalState.INVALID
                    elif relation_result.relation_type_id != relation_request.relation_type_id:
                        failure_code = USMFailureCode.TRANSFORMATION_RELATION_PROVENANCE_MISMATCH
                        state = TransformationProposalState.BLOCKED
                    elif len(relation_request.operand_bindings) != len(
                        transformation.source_types
                    ):
                        failure_code = USMFailureCode.TRANSFORMATION_SOURCE_ARITY_MISMATCH
                        state = TransformationProposalState.BLOCKED
                    else:
                        context = environment.resolve_context(relation_request.context_id)
                        if context is None:
                            failure_code = (
                                USMFailureCode.TRANSFORMATION_REQUIRED_CONDITION_MISSING
                            )
                            state = TransformationProposalState.DEFERRED
                        elif context.science_id != matrix.science_id:
                            failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
                            state = TransformationProposalState.BLOCKED
                        elif context.matrix_id != matrix.matrix_id:
                            failure_code = USMFailureCode.TRANSFORMATION_MATRIX_MISMATCH
                            state = TransformationProposalState.INVALID
                        else:
                            ordered_bindings = tuple(
                                sorted(
                                    relation_request.operand_bindings,
                                    key=lambda item: item.position,
                                )
                            )
                            for position, binding in enumerate(ordered_bindings):
                                entity = environment.resolve_entity(binding.entity_instance_ref)
                                if entity is None:
                                    failure_code = (
                                        USMFailureCode.TRANSFORMATION_SOURCE_ENTITY_UNRESOLVED
                                    )
                                    state = TransformationProposalState.DEFERRED
                                    break
                                if entity.science_id != matrix.science_id:
                                    failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
                                    state = TransformationProposalState.BLOCKED
                                    break
                                if entity.matrix_id != matrix.matrix_id:
                                    failure_code = USMFailureCode.TRANSFORMATION_MATRIX_MISMATCH
                                    state = TransformationProposalState.INVALID
                                    break
                                if entity.entity_type_id != transformation.source_types[position]:
                                    failure_code = (
                                        USMFailureCode.TRANSFORMATION_SOURCE_TYPE_MISMATCH
                                    )
                                    state = TransformationProposalState.BLOCKED
                                    break
                                capability_result = environment.resolve_capability_result(
                                    binding.capability_result_ref
                                )
                                if capability_result is None:
                                    failure_code = (
                                        USMFailureCode.TRANSFORMATION_CAPABILITY_RESULT_UNRESOLVED
                                    )
                                    state = TransformationProposalState.DEFERRED
                                    break
                                if capability_result.state not in _ELIGIBLE_CAPABILITY_STATES:
                                    failure_code = (
                                        USMFailureCode.TRANSFORMATION_CAPABILITY_NOT_ELIGIBLE
                                    )
                                    state = TransformationProposalState.BLOCKED
                                    break
                                resolved_entities.append(entity)
                                resolved_capability_results.append(capability_result)
                            if failure_code is None:
                                active_blockers = tuple(
                                    blocker
                                    for blocker in transformation.blockers
                                    if blocker in context.active_blocker_refs
                                )
                                if active_blockers:
                                    failure_code = USMFailureCode.TRANSFORMATION_BLOCKER_ACTIVE
                                    state = TransformationProposalState.BLOCKED
                                else:
                                    residuals = (
                                        matrix.residuals
                                        + context.residuals
                                        + relation_result.residuals
                                        + link_result.residuals
                                        + tuple(
                                            residual
                                            for entity in resolved_entities
                                            for residual in entity.residuals
                                        )
                                        + tuple(
                                            residual
                                            for result in resolved_capability_results
                                            for residual in result.residuals
                                        )
                                    )
                                    if any(residual.blocking for residual in residuals):
                                        failure_code = (
                                            USMFailureCode.TRANSFORMATION_BLOCKING_RESIDUAL
                                        )
                                        state = TransformationProposalState.BLOCKED
                                    else:
                                        granted_rank = min(
                                            request.requested_rank,
                                            transformation.rank_ceiling,
                                            link_result.granted_rank,
                                            relation_result.granted_rank,
                                            min(
                                                entity.state_rank for entity in resolved_entities
                                            ),
                                            min(
                                                result.granted_rank
                                                for result in resolved_capability_results
                                            ),
                                        )
                                        if granted_rank < request.requested_rank:
                                            failure_code = (
                                                USMFailureCode.TRANSFORMATION_RANK_CEILING_EXCEEDED
                                            )
                                            state = TransformationProposalState.BLOCKED
                                            granted_rank = Rank.ZERO
                                        else:
                                            proposal = TransformationProposal(
                                                proposal_id=request.request_id,
                                                matrix_id=matrix.matrix_id,
                                                science_id=matrix.science_id,
                                                relation_request_id=request.relation_request_id,
                                                link_request_id=request.link_request_id,
                                                source_state_refs=tuple(
                                                    entity.entity_instance_ref
                                                    for entity in resolved_entities
                                                ),
                                                transformation_type_id=(
                                                    request.transformation_type_id
                                                ),
                                                target_type_ids=transformation.target_types,
                                                identity_policy_ref=request.identity_policy_ref,
                                                preserved_invariants=(
                                                    transformation.preserved_invariants
                                                ),
                                                declared_changes=transformation.declared_changes,
                                                required_conditions=(
                                                    transformation.required_conditions
                                                ),
                                                active_blockers=active_blockers,
                                                expected_effects=(
                                                    transformation.declared_changes
                                                ),
                                                rank_ceiling=transformation.rank_ceiling,
                                                residual_policy_ref=(
                                                    transformation.residual_policy_ref
                                                ),
                                                rollback_requirements=(
                                                    request.rollback_requirements
                                                ),
                                                trace_ref=TraceRef(
                                                    f"{request.trace_ref.value}/proposal/"
                                                    f"{request.transformation_type_id.value}"
                                                ),
                                            )
                                            state = (
                                                TransformationProposalState.CONSTRUCTED_WITH_RESIDUALS
                                                if residuals
                                                else TransformationProposalState.CONSTRUCTED
                                            )

    trace_failure = _trace_chain_failure(
        matrix=matrix,
        request=request,
        transformation_trace_ref=transformation.trace_ref if transformation is not None else None,
        link_result=link_result,
        relation_result=relation_result,
        context=context,
        entities=tuple(resolved_entities),
        capability_results=tuple(resolved_capability_results),
    )
    if trace_failure is not None:
        failure_code = trace_failure
        state = TransformationProposalState.INVALID
        granted_rank = Rank.ZERO
        proposal = None

    failure_codes = () if failure_code is None else (failure_code,)
    if state is TransformationProposalState.INVALID and not failure_codes:
        failure_codes = (USMFailureCode.SCHEMA_INVALID,)
    if state is TransformationProposalState.BLOCKED and failure_codes and (
        failure_codes[0] not in _BLOCKING_FAILURE_CODES
    ):
        state = TransformationProposalState.INVALID
        granted_rank = Rank.ZERO
        proposal = None
    if state is TransformationProposalState.DEFERRED and failure_codes and (
        failure_codes[0] not in _DEFERRED_FAILURE_CODES
    ):
        state = TransformationProposalState.INVALID
        granted_rank = Rank.ZERO
        proposal = None

    trace = _emit_trace(
        matrix=matrix,
        request=request,
        state=state,
        link_trace_ref=(
            link_result.trace_ref
            if link_result is not None
            else TraceRef(
                f"{matrix.trace_ref.value}/unresolved/link/{request.link_request_id.value}"
            )
        ),
        relation_trace_ref=(
            relation_result.trace_ref
            if relation_result is not None
            else TraceRef(
                f"{matrix.trace_ref.value}/unresolved/relation/{request.relation_request_id.value}"
            )
        ),
        transformation_trace_ref=(
            transformation.trace_ref
            if transformation is not None
            else TraceRef(
                f"{matrix.trace_ref.value}/unresolved/transformation/"
                f"{request.transformation_type_id.value}"
            )
        ),
        context_trace_ref=(
            context.trace_ref
            if context is not None
            else TraceRef(f"{matrix.trace_ref.value}/unresolved/context")
        ),
        source_entity_trace_refs=tuple(entity.trace_ref for entity in resolved_entities),
        capability_trace_refs=tuple(
            result.evaluation_trace.evaluation_trace_ref for result in resolved_capability_results
        ),
    )

    return TransformationProposalResult(
        request_id=request.request_id,
        state=state,
        transformation_type_id=request.transformation_type_id,
        relation_request_id=request.relation_request_id,
        link_request_id=request.link_request_id,
        granted_rank=granted_rank if state in _CONSTRUCTED_STATES else Rank.ZERO,
        proposal=proposal if state in _CONSTRUCTED_STATES else None,
        failure_codes=failure_codes,
        residuals=residuals,
        trace_ref=trace.evaluation_trace_ref,
        evaluation_trace=trace,
    )


def _trace_chain_failure(
    *,
    matrix: UniversalScienceMatrix,
    request: TransformationProposalRequest,
    transformation_trace_ref: TraceRef | None,
    link_result: TransformationLinkResult | None,
    relation_result: RelationEvaluationResult | None,
    context: EvaluationContextContract | None,
    entities: tuple[EntityInstanceContract, ...],
    capability_results: tuple[CapabilityEvaluationResult, ...],
) -> USMFailureCode | None:
    expected_prefix = f"{matrix.trace_ref.value}/requests/{request.request_id.value}"
    if not request.trace_ref.value.startswith(expected_prefix):
        return USMFailureCode.TRANSFORMATION_PROPOSAL_TRACE_CHAIN_BROKEN

    traces: list[TraceRef] = [matrix.trace_ref, request.trace_ref]
    if transformation_trace_ref is not None:
        traces.append(transformation_trace_ref)
    if link_result is not None:
        traces.append(link_result.trace_ref)
        traces.append(link_result.evaluation_trace.request_trace_ref)
        traces.append(link_result.evaluation_trace.relation_trace_ref)
    if relation_result is not None:
        traces.append(relation_result.trace_ref)
        traces.append(relation_result.evaluation_trace.request_trace_ref)
    if context is not None:
        traces.append(context.trace_ref)
    traces.extend(entity.trace_ref for entity in entities)
    traces.extend(result.evaluation_trace.evaluation_trace_ref for result in capability_results)
    traces.extend(result.evaluation_trace.request_trace_ref for result in capability_results)

    for trace in traces:
        if not (
            trace.value == matrix.trace_ref.value
            or trace.value.startswith(f"{matrix.trace_ref.value}/")
        ):
            return USMFailureCode.TRANSFORMATION_PROPOSAL_TRACE_CHAIN_BROKEN
    return None


def _emit_trace(
    *,
    matrix: UniversalScienceMatrix,
    request: TransformationProposalRequest,
    state: TransformationProposalState,
    link_trace_ref: TraceRef,
    relation_trace_ref: TraceRef,
    transformation_trace_ref: TraceRef,
    context_trace_ref: TraceRef,
    source_entity_trace_refs: tuple[TraceRef, ...],
    capability_trace_refs: tuple[TraceRef, ...],
) -> TransformationProposalTrace:
    base = (
        request.trace_ref.value
        if request.trace_ref.value.startswith("trace://")
        else f"{matrix.trace_ref.value}/requests/{request.request_id.value}"
    )
    decision_stage = f"transformation-proposal/{state.value.lower()}"
    evaluation_trace_ref = TraceRef(
        f"{base}/decisions/{request.request_id.value}/"
        f"{request.transformation_type_id.value}/{decision_stage}"
    )
    return TransformationProposalTrace(
        evaluation_trace_ref=evaluation_trace_ref,
        request_trace_ref=request.trace_ref,
        link_trace_ref=link_trace_ref,
        relation_trace_ref=relation_trace_ref,
        transformation_trace_ref=transformation_trace_ref,
        context_trace_ref=context_trace_ref,
        matrix_trace_ref=matrix.trace_ref,
        source_entity_trace_refs=source_entity_trace_refs,
        capability_trace_refs=capability_trace_refs,
        decision_stage=decision_stage,
    )


__all__ = [
    "TransformationProposal",
    "TransformationProposalEnvironment",
    "TransformationProposalRequest",
    "TransformationProposalResult",
    "TransformationProposalState",
    "TransformationProposalTrace",
    "construct_transformation_proposal",
]
