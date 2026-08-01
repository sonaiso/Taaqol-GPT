"""USM-C5 bounded transformation linking (pure, deterministic, non-executive)."""

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
    MatrixId,
    RequestId,
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
from taaqqul_slot_geometry.usm.validator import USMFailureCode


class TransformationLinkState(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    ELIGIBLE_WITH_RESIDUALS = "ELIGIBLE_WITH_RESIDUALS"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class TransformationLinkRequest:
    request_id: RequestId
    matrix_id: MatrixId
    science_id: ScienceId
    transformation_type_id: TransformationTypeId
    relation_request_id: RequestId
    requested_rank: Rank
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, RequestId):
            raise USMSchemaError("TransformationLinkRequest.request_id must be RequestId")
        if not isinstance(self.matrix_id, MatrixId):
            raise USMSchemaError("TransformationLinkRequest.matrix_id must be MatrixId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("TransformationLinkRequest.science_id must be ScienceId")
        if not isinstance(self.transformation_type_id, TransformationTypeId):
            raise USMSchemaError(
                "TransformationLinkRequest.transformation_type_id must be TransformationTypeId"
            )
        if not isinstance(self.relation_request_id, RequestId):
            raise USMSchemaError(
                "TransformationLinkRequest.relation_request_id must be RequestId"
            )
        if not isinstance(self.requested_rank, Rank):
            raise USMSchemaError("TransformationLinkRequest.requested_rank must be Rank")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("TransformationLinkRequest.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class TransformationLinkEnvironment:
    entity_instances: tuple[EntityInstanceContract, ...]
    contexts: tuple[EvaluationContextContract, ...]
    capability_results: tuple[CapabilityEvaluationResult, ...]
    relation_requests: tuple[RelationEvaluationRequest, ...]
    relation_results: tuple[RelationEvaluationResult, ...]

    def __post_init__(self) -> None:
        require_tuple_of_type(
            "TransformationLinkEnvironment",
            "entity_instances",
            self.entity_instances,
            EntityInstanceContract,
        )
        require_tuple_of_type(
            "TransformationLinkEnvironment",
            "contexts",
            self.contexts,
            EvaluationContextContract,
        )
        require_tuple_of_type(
            "TransformationLinkEnvironment",
            "capability_results",
            self.capability_results,
            CapabilityEvaluationResult,
        )
        require_tuple_of_type(
            "TransformationLinkEnvironment",
            "relation_requests",
            self.relation_requests,
            RelationEvaluationRequest,
        )
        require_tuple_of_type(
            "TransformationLinkEnvironment",
            "relation_results",
            self.relation_results,
            RelationEvaluationResult,
        )
        if len({item.entity_instance_ref for item in self.entity_instances}) != len(
            self.entity_instances
        ):
            raise USMSchemaError(
                "TransformationLinkEnvironment.entity_instances has duplicate references"
            )
        if len({item.context_id for item in self.contexts}) != len(self.contexts):
            raise USMSchemaError(
                "TransformationLinkEnvironment.contexts has duplicate references"
            )
        if len({item.request_id for item in self.capability_results}) != len(
            self.capability_results
        ):
            raise USMSchemaError(
                "TransformationLinkEnvironment.capability_results has duplicate references"
            )
        if len({item.request_id for item in self.relation_requests}) != len(
            self.relation_requests
        ):
            raise USMSchemaError(
                "TransformationLinkEnvironment.relation_requests has duplicate references"
            )
        if len({item.request_id for item in self.relation_results}) != len(
            self.relation_results
        ):
            raise USMSchemaError(
                "TransformationLinkEnvironment.relation_results has duplicate references"
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


@dataclass(frozen=True, slots=True)
class TransformationLinkTrace:
    evaluation_trace_ref: TraceRef
    request_trace_ref: TraceRef
    relation_trace_ref: TraceRef
    transformation_trace_ref: TraceRef
    context_trace_ref: TraceRef
    matrix_trace_ref: TraceRef
    capability_trace_refs: tuple[TraceRef, ...]
    entity_trace_refs: tuple[TraceRef, ...]
    decision_stage: str

    def __post_init__(self) -> None:
        if not isinstance(self.evaluation_trace_ref, TraceRef):
            raise USMSchemaError("TransformationLinkTrace.evaluation_trace_ref must be TraceRef")
        if not isinstance(self.request_trace_ref, TraceRef):
            raise USMSchemaError("TransformationLinkTrace.request_trace_ref must be TraceRef")
        if not isinstance(self.relation_trace_ref, TraceRef):
            raise USMSchemaError("TransformationLinkTrace.relation_trace_ref must be TraceRef")
        if not isinstance(self.transformation_trace_ref, TraceRef):
            raise USMSchemaError(
                "TransformationLinkTrace.transformation_trace_ref must be TraceRef"
            )
        if not isinstance(self.context_trace_ref, TraceRef):
            raise USMSchemaError("TransformationLinkTrace.context_trace_ref must be TraceRef")
        if not isinstance(self.matrix_trace_ref, TraceRef):
            raise USMSchemaError("TransformationLinkTrace.matrix_trace_ref must be TraceRef")
        require_tuple_of_type(
            "TransformationLinkTrace", "capability_trace_refs", self.capability_trace_refs, TraceRef
        )
        require_tuple_of_type(
            "TransformationLinkTrace", "entity_trace_refs", self.entity_trace_refs, TraceRef
        )
        if not isinstance(self.decision_stage, str) or not self.decision_stage:
            raise USMSchemaError("TransformationLinkTrace.decision_stage must be non-empty str")
        if self.evaluation_trace_ref == self.request_trace_ref:
            raise USMSchemaError("TransformationLinkTrace must emit a new trace event")


@dataclass(frozen=True, slots=True)
class TransformationLinkResult:
    request_id: RequestId
    state: TransformationLinkState
    transformation_type_id: TransformationTypeId
    relation_request_id: RequestId
    granted_rank: Rank
    failure_codes: tuple[USMFailureCode, ...]
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef
    evaluation_trace: TransformationLinkTrace

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, RequestId):
            raise USMSchemaError("TransformationLinkResult.request_id must be RequestId")
        if not isinstance(self.state, TransformationLinkState):
            raise USMSchemaError("TransformationLinkResult.state must be TransformationLinkState")
        if not isinstance(self.transformation_type_id, TransformationTypeId):
            raise USMSchemaError(
                "TransformationLinkResult.transformation_type_id must be TransformationTypeId"
            )
        if not isinstance(self.relation_request_id, RequestId):
            raise USMSchemaError(
                "TransformationLinkResult.relation_request_id must be RequestId"
            )
        if not isinstance(self.granted_rank, Rank):
            raise USMSchemaError("TransformationLinkResult.granted_rank must be Rank")
        require_tuple_of_type(
            "TransformationLinkResult", "failure_codes", self.failure_codes, USMFailureCode
        )
        require_tuple_of_type(
            "TransformationLinkResult", "residuals", self.residuals, USMResidual
        )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("TransformationLinkResult.trace_ref must be TraceRef")
        if not isinstance(self.evaluation_trace, TransformationLinkTrace):
            raise USMSchemaError(
                "TransformationLinkResult.evaluation_trace must be TransformationLinkTrace"
            )
        if self.trace_ref != self.evaluation_trace.evaluation_trace_ref:
            raise USMSchemaError(
                "TransformationLinkResult.trace_ref must equal "
                "evaluation_trace.evaluation_trace_ref"
            )
        self._assert_invariants()

    def _assert_invariants(self) -> None:
        if self.state is TransformationLinkState.ELIGIBLE:
            if self.failure_codes:
                raise USMSchemaError("ELIGIBLE transformation link cannot carry failure codes")
            if any(residual.blocking for residual in self.residuals):
                raise USMSchemaError("ELIGIBLE transformation link cannot carry blocking residuals")
            if self.granted_rank is Rank.ZERO:
                raise USMSchemaError("ELIGIBLE transformation link must grant non-zero rank")
            return
        if self.state is TransformationLinkState.ELIGIBLE_WITH_RESIDUALS:
            if self.failure_codes:
                raise USMSchemaError(
                    "ELIGIBLE_WITH_RESIDUALS transformation link cannot carry failure codes"
                )
            if not self.residuals:
                raise USMSchemaError(
                    "ELIGIBLE_WITH_RESIDUALS transformation link requires visible residuals"
                )
            if any(residual.blocking for residual in self.residuals):
                raise USMSchemaError(
                    "ELIGIBLE_WITH_RESIDUALS transformation link cannot carry blocking residuals"
                )
            if self.granted_rank is Rank.ZERO:
                raise USMSchemaError(
                    "ELIGIBLE_WITH_RESIDUALS transformation link must grant non-zero rank"
                )
            return
        if self.granted_rank is not Rank.ZERO:
            raise USMSchemaError("Non-eligible transformation link results must grant Rank.ZERO")


_ELIGIBLE_CAPABILITY_STATES = frozenset(
    {CapabilityEvaluationState.ELIGIBLE, CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS}
)
_ELIGIBLE_RELATION_STATES = frozenset(
    {RelationEvaluationState.ELIGIBLE, RelationEvaluationState.ELIGIBLE_WITH_RESIDUALS}
)
_ELIGIBLE_STATES = frozenset(
    {TransformationLinkState.ELIGIBLE, TransformationLinkState.ELIGIBLE_WITH_RESIDUALS}
)
_BLOCKING_FAILURE_CODES = frozenset(
    {
        USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH,
        USMFailureCode.TRANSFORMATION_RELATION_NOT_ELIGIBLE,
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
        USMFailureCode.TRANSFORMATION_RELATION_REQUEST_UNRESOLVED,
        USMFailureCode.TRANSFORMATION_RELATION_RESULT_UNRESOLVED,
        USMFailureCode.TRANSFORMATION_SOURCE_ENTITY_UNRESOLVED,
        USMFailureCode.TRANSFORMATION_CAPABILITY_RESULT_UNRESOLVED,
        USMFailureCode.TRANSFORMATION_REQUIRED_CAPABILITY_MISSING,
        USMFailureCode.TRANSFORMATION_REQUIRED_CONDITION_MISSING,
        USMFailureCode.TRANSFORMATION_EVIDENCE_REQUIREMENT_MISSING,
    }
)


def evaluate_transformation_link(
    matrix: UniversalScienceMatrix,
    environment: TransformationLinkEnvironment,
    request: TransformationLinkRequest,
) -> TransformationLinkResult:
    """Link relation eligibility to transformation proposal boundaries only."""

    if not isinstance(matrix, UniversalScienceMatrix):
        raise USMSchemaError("evaluate_transformation_link requires UniversalScienceMatrix")
    if not isinstance(environment, TransformationLinkEnvironment):
        raise USMSchemaError(
            "evaluate_transformation_link requires TransformationLinkEnvironment"
        )
    if not isinstance(request, TransformationLinkRequest):
        raise USMSchemaError("evaluate_transformation_link requires TransformationLinkRequest")

    failure_code: USMFailureCode | None = None
    state = TransformationLinkState.DEFERRED
    granted_rank = Rank.ZERO
    residuals: tuple[USMResidual, ...] = matrix.residuals

    transformation = None
    relation_request = None
    relation_result = None
    context = None
    resolved_entities: list[EntityInstanceContract] = []
    resolved_capability_results: list[CapabilityEvaluationResult] = []

    if request.matrix_id != matrix.matrix_id:
        failure_code = USMFailureCode.TRANSFORMATION_MATRIX_MISMATCH
        state = TransformationLinkState.INVALID
    elif request.science_id != matrix.science_id:
        failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
        state = TransformationLinkState.BLOCKED
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
            state = TransformationLinkState.INVALID
        elif transformation.science_id != matrix.science_id:
            failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
            state = TransformationLinkState.BLOCKED
        else:
            relation_request = environment.resolve_relation_request(request.relation_request_id)
            if relation_request is None:
                failure_code = USMFailureCode.TRANSFORMATION_RELATION_REQUEST_UNRESOLVED
                state = TransformationLinkState.DEFERRED
            else:
                relation_result = environment.resolve_relation_result(request.relation_request_id)
                if relation_result is None:
                    failure_code = USMFailureCode.TRANSFORMATION_RELATION_RESULT_UNRESOLVED
                    state = TransformationLinkState.DEFERRED
                elif relation_result.state not in _ELIGIBLE_RELATION_STATES:
                    failure_code = USMFailureCode.TRANSFORMATION_RELATION_NOT_ELIGIBLE
                    state = TransformationLinkState.BLOCKED
                elif relation_request.science_id != matrix.science_id:
                    failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
                    state = TransformationLinkState.BLOCKED
                elif relation_request.matrix_id != matrix.matrix_id:
                    failure_code = USMFailureCode.TRANSFORMATION_MATRIX_MISMATCH
                    state = TransformationLinkState.INVALID
                elif relation_result.relation_type_id != relation_request.relation_type_id:
                    failure_code = USMFailureCode.TRANSFORMATION_RELATION_PROVENANCE_MISMATCH
                    state = TransformationLinkState.BLOCKED
                elif len(relation_request.operand_bindings) != len(transformation.source_types):
                    failure_code = USMFailureCode.TRANSFORMATION_SOURCE_ARITY_MISMATCH
                    state = TransformationLinkState.BLOCKED
                else:
                    context = environment.resolve_context(relation_request.context_id)
                    if context is None:
                        failure_code = USMFailureCode.TRANSFORMATION_REQUIRED_CONDITION_MISSING
                        state = TransformationLinkState.DEFERRED
                    elif context.science_id != matrix.science_id:
                        failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
                        state = TransformationLinkState.BLOCKED
                    elif context.matrix_id != matrix.matrix_id:
                        failure_code = USMFailureCode.TRANSFORMATION_MATRIX_MISMATCH
                        state = TransformationLinkState.INVALID
                    else:
                        ordered_bindings = tuple(
                            sorted(
                                relation_request.operand_bindings, key=lambda item: item.position
                            )
                        )
                        for position, binding in enumerate(ordered_bindings):
                            entity = environment.resolve_entity(binding.entity_instance_ref)
                            if entity is None:
                                failure_code = (
                                    USMFailureCode.TRANSFORMATION_SOURCE_ENTITY_UNRESOLVED
                                )
                                state = TransformationLinkState.DEFERRED
                                break
                            if entity.science_id != matrix.science_id:
                                failure_code = USMFailureCode.TRANSFORMATION_SCIENCE_MISMATCH
                                state = TransformationLinkState.BLOCKED
                                break
                            if entity.matrix_id != matrix.matrix_id:
                                failure_code = USMFailureCode.TRANSFORMATION_MATRIX_MISMATCH
                                state = TransformationLinkState.INVALID
                                break
                            if entity.entity_type_id != transformation.source_types[position]:
                                failure_code = USMFailureCode.TRANSFORMATION_SOURCE_TYPE_MISMATCH
                                state = TransformationLinkState.BLOCKED
                                break

                            capability_result = environment.resolve_capability_result(
                                binding.capability_result_ref
                            )
                            if capability_result is None:
                                failure_code = (
                                    USMFailureCode.TRANSFORMATION_CAPABILITY_RESULT_UNRESOLVED
                                )
                                state = TransformationLinkState.DEFERRED
                                break
                            if capability_result.state not in _ELIGIBLE_CAPABILITY_STATES:
                                failure_code = USMFailureCode.TRANSFORMATION_CAPABILITY_NOT_ELIGIBLE
                                state = TransformationLinkState.BLOCKED
                                break
                            if capability_result.entity_type_id != entity.entity_type_id:
                                failure_code = (
                                    USMFailureCode.TRANSFORMATION_RELATION_PROVENANCE_MISMATCH
                                )
                                state = TransformationLinkState.BLOCKED
                                break
                            if (
                                capability_result.evaluation_trace.entity_trace_ref
                                != entity.trace_ref
                                or capability_result.evaluation_trace.context_trace_ref
                                != context.trace_ref
                                or capability_result.evaluation_trace.matrix_trace_ref
                                != matrix.trace_ref
                            ):
                                failure_code = (
                                    USMFailureCode.TRANSFORMATION_RELATION_PROVENANCE_MISMATCH
                                )
                                state = TransformationLinkState.BLOCKED
                                break
                            resolved_entities.append(entity)
                            resolved_capability_results.append(capability_result)

                        if failure_code is None:
                            provided_capabilities = {
                                result.capability_id for result in resolved_capability_results
                            }
                            if any(
                                capability not in provided_capabilities
                                for capability in transformation.required_capabilities
                            ):
                                failure_code = (
                                    USMFailureCode.TRANSFORMATION_REQUIRED_CAPABILITY_MISSING
                                )
                                state = TransformationLinkState.DEFERRED
                            else:
                                missing_conditions = tuple(
                                    condition
                                    for condition in transformation.required_conditions
                                    if condition not in context.active_condition_refs
                                )
                                if missing_conditions:
                                    failure_code = (
                                        USMFailureCode.TRANSFORMATION_REQUIRED_CONDITION_MISSING
                                    )
                                    state = TransformationLinkState.DEFERRED
                                else:
                                    active_blockers = tuple(
                                        blocker
                                        for blocker in transformation.blockers
                                        if blocker in context.active_blocker_refs
                                    )
                                    if active_blockers:
                                        failure_code = USMFailureCode.TRANSFORMATION_BLOCKER_ACTIVE
                                        state = TransformationLinkState.BLOCKED
                                    else:
                                        provided_evidence = {
                                            evidence
                                            for result in resolved_capability_results
                                            for evidence in result.recognized_evidence_type_refs
                                        } | set(context.supplied_evidence_type_refs)
                                        if any(
                                            evidence not in provided_evidence
                                            for evidence in transformation.evidence_requirements
                                        ):
                                            failure_code = (
                                                USMFailureCode.TRANSFORMATION_EVIDENCE_REQUIREMENT_MISSING
                                            )
                                            state = TransformationLinkState.DEFERRED
                                        else:
                                            residuals = (
                                                matrix.residuals
                                                + context.residuals
                                                + relation_result.residuals
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
                                                state = TransformationLinkState.BLOCKED
                                            else:
                                                evidence_contracts = {
                                                    contract.evidence_type_id: contract
                                                    for contract in matrix.evidence
                                                }
                                                evidence_rank_ceiling = min(
                                                    (
                                                        evidence_contracts[evidence].global_rank_ceiling
                                                        for evidence in (
                                                            transformation.evidence_requirements
                                                        )
                                                        if evidence in evidence_contracts
                                                    ),
                                                    default=max(Rank),
                                                )
                                                granted_rank = min(
                                                    request.requested_rank,
                                                    transformation.rank_ceiling,
                                                    relation_result.granted_rank,
                                                    min(
                                                        entity.state_rank
                                                        for entity in resolved_entities
                                                    ),
                                                    min(
                                                        result.granted_rank
                                                        for result in resolved_capability_results
                                                    ),
                                                    evidence_rank_ceiling,
                                                )
                                                if granted_rank < request.requested_rank:
                                                    failure_code = (
                                                        USMFailureCode.TRANSFORMATION_RANK_CEILING_EXCEEDED
                                                    )
                                                    state = TransformationLinkState.BLOCKED
                                                    granted_rank = Rank.ZERO
                                                else:
                                                    state = (
                                                        TransformationLinkState.ELIGIBLE_WITH_RESIDUALS
                                                        if residuals
                                                        else TransformationLinkState.ELIGIBLE
                                                    )

    trace_failure = _trace_chain_failure(
        matrix=matrix,
        request=request,
        transformation_trace_ref=transformation.trace_ref if transformation is not None else None,
        relation_result=relation_result,
        context=context,
        entities=tuple(resolved_entities),
        capability_results=tuple(resolved_capability_results),
    )
    if trace_failure is not None:
        failure_code = trace_failure
        state = TransformationLinkState.INVALID
        granted_rank = Rank.ZERO

    failure_codes = () if failure_code is None else (failure_code,)
    if state is TransformationLinkState.INVALID and not failure_codes:
        failure_codes = (USMFailureCode.SCHEMA_INVALID,)
    if state is TransformationLinkState.BLOCKED and failure_codes and (
        failure_codes[0] not in _BLOCKING_FAILURE_CODES
    ):
        state = TransformationLinkState.INVALID
        granted_rank = Rank.ZERO
    if state is TransformationLinkState.DEFERRED and failure_codes and (
        failure_codes[0] not in _DEFERRED_FAILURE_CODES
    ):
        state = TransformationLinkState.INVALID
        granted_rank = Rank.ZERO

    trace = _emit_trace(
        matrix=matrix,
        request=request,
        state=state,
        transformation_trace_ref=(
            transformation.trace_ref
            if transformation is not None
            else TraceRef(
                f"{matrix.trace_ref.value}/unresolved/transformation/"
                f"{request.transformation_type_id.value}"
            )
        ),
        relation_trace_ref=(
            relation_result.trace_ref
            if relation_result is not None
            else TraceRef(
                f"{matrix.trace_ref.value}/unresolved/relation/{request.relation_request_id.value}"
            )
        ),
        context_trace_ref=(
            context.trace_ref
            if context is not None
            else TraceRef(f"{matrix.trace_ref.value}/unresolved/context")
        ),
        entity_trace_refs=tuple(entity.trace_ref for entity in resolved_entities),
        capability_trace_refs=tuple(
            result.evaluation_trace.evaluation_trace_ref for result in resolved_capability_results
        ),
    )
    return TransformationLinkResult(
        request_id=request.request_id,
        state=state,
        transformation_type_id=request.transformation_type_id,
        relation_request_id=request.relation_request_id,
        granted_rank=granted_rank if state in _ELIGIBLE_STATES else Rank.ZERO,
        failure_codes=failure_codes,
        residuals=residuals,
        trace_ref=trace.evaluation_trace_ref,
        evaluation_trace=trace,
    )


def _trace_chain_failure(
    *,
    matrix: UniversalScienceMatrix,
    request: TransformationLinkRequest,
    transformation_trace_ref: TraceRef | None,
    relation_result: RelationEvaluationResult | None,
    context: EvaluationContextContract | None,
    entities: tuple[EntityInstanceContract, ...],
    capability_results: tuple[CapabilityEvaluationResult, ...],
) -> USMFailureCode | None:
    expected_prefix = f"{matrix.trace_ref.value}/requests/{request.request_id.value}"
    if not request.trace_ref.value.startswith(expected_prefix):
        return USMFailureCode.TRANSFORMATION_TRACE_CHAIN_BROKEN

    traces: list[TraceRef] = [matrix.trace_ref, request.trace_ref]
    if transformation_trace_ref is not None:
        traces.append(transformation_trace_ref)
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
            return USMFailureCode.TRANSFORMATION_TRACE_CHAIN_BROKEN
    return None


def _emit_trace(
    *,
    matrix: UniversalScienceMatrix,
    request: TransformationLinkRequest,
    state: TransformationLinkState,
    transformation_trace_ref: TraceRef,
    relation_trace_ref: TraceRef,
    context_trace_ref: TraceRef,
    entity_trace_refs: tuple[TraceRef, ...],
    capability_trace_refs: tuple[TraceRef, ...],
) -> TransformationLinkTrace:
    base = (
        request.trace_ref.value
        if request.trace_ref.value.startswith("trace://")
        else f"{matrix.trace_ref.value}/requests/{request.request_id.value}"
    )
    decision_stage = f"transformation-link/{state.value.lower()}"
    evaluation_trace_ref = TraceRef(
        f"{base}/decisions/{request.request_id.value}/"
        f"{request.transformation_type_id.value}/{decision_stage}"
    )
    return TransformationLinkTrace(
        evaluation_trace_ref=evaluation_trace_ref,
        request_trace_ref=request.trace_ref,
        relation_trace_ref=relation_trace_ref,
        transformation_trace_ref=transformation_trace_ref,
        context_trace_ref=context_trace_ref,
        matrix_trace_ref=matrix.trace_ref,
        capability_trace_refs=capability_trace_refs,
        entity_trace_refs=entity_trace_refs,
        decision_stage=decision_stage,
    )


__all__ = [
    "TransformationLinkEnvironment",
    "TransformationLinkRequest",
    "TransformationLinkResult",
    "TransformationLinkState",
    "TransformationLinkTrace",
    "evaluate_transformation_link",
]
