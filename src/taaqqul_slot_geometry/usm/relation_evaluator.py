"""USM-C4 bounded relation evaluator (pure, deterministic, non-executive)."""

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
from taaqqul_slot_geometry.usm.enums import RelationDirection
from taaqqul_slot_geometry.usm.identifiers import (
    CapabilityEvaluationRef,
    ContextId,
    EntityInstanceRef,
    MatrixId,
    RelationTypeId,
    RequestId,
    RoleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)
from taaqqul_slot_geometry.usm.matrix import UniversalScienceMatrix
from taaqqul_slot_geometry.usm.residuals import USMResidual
from taaqqul_slot_geometry.usm.validator import USMFailureCode


class RelationEvaluationState(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    ELIGIBLE_WITH_RESIDUALS = "ELIGIBLE_WITH_RESIDUALS"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class RelationOperandBinding:
    role_id: RoleId
    entity_instance_ref: EntityInstanceRef
    capability_result_ref: CapabilityEvaluationRef
    position: int

    def __post_init__(self) -> None:
        if not isinstance(self.role_id, RoleId):
            raise USMSchemaError("RelationOperandBinding.role_id must be RoleId")
        if not isinstance(self.entity_instance_ref, EntityInstanceRef):
            raise USMSchemaError(
                "RelationOperandBinding.entity_instance_ref must be EntityInstanceRef"
            )
        if not isinstance(self.capability_result_ref, CapabilityEvaluationRef):
            raise USMSchemaError(
                "RelationOperandBinding.capability_result_ref must be CapabilityEvaluationRef"
            )
        if not isinstance(self.position, int) or self.position < 0:
            raise USMSchemaError("RelationOperandBinding.position must be non-negative int")


@dataclass(frozen=True, slots=True)
class RelationEvaluationRequest:
    request_id: RequestId
    matrix_id: MatrixId
    science_id: ScienceId
    relation_type_id: RelationTypeId
    operand_bindings: tuple[RelationOperandBinding, ...]
    context_id: ContextId
    requested_rank: Rank
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, RequestId):
            raise USMSchemaError("RelationEvaluationRequest.request_id must be RequestId")
        if not isinstance(self.matrix_id, MatrixId):
            raise USMSchemaError("RelationEvaluationRequest.matrix_id must be MatrixId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("RelationEvaluationRequest.science_id must be ScienceId")
        if not isinstance(self.relation_type_id, RelationTypeId):
            raise USMSchemaError(
                "RelationEvaluationRequest.relation_type_id must be RelationTypeId"
            )
        require_tuple_of_type(
            "RelationEvaluationRequest",
            "operand_bindings",
            self.operand_bindings,
            RelationOperandBinding,
        )
        if not isinstance(self.context_id, ContextId):
            raise USMSchemaError("RelationEvaluationRequest.context_id must be ContextId")
        if not isinstance(self.requested_rank, Rank):
            raise USMSchemaError("RelationEvaluationRequest.requested_rank must be Rank")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("RelationEvaluationRequest.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class RelationEvaluationEnvironment:
    entity_instances: tuple[EntityInstanceContract, ...]
    contexts: tuple[EvaluationContextContract, ...]
    capability_results: tuple[CapabilityEvaluationResult, ...]

    def __post_init__(self) -> None:
        require_tuple_of_type(
            "RelationEvaluationEnvironment",
            "entity_instances",
            self.entity_instances,
            EntityInstanceContract,
        )
        require_tuple_of_type(
            "RelationEvaluationEnvironment",
            "contexts",
            self.contexts,
            EvaluationContextContract,
        )
        require_tuple_of_type(
            "RelationEvaluationEnvironment",
            "capability_results",
            self.capability_results,
            CapabilityEvaluationResult,
        )
        if len({item.entity_instance_ref for item in self.entity_instances}) != len(
            self.entity_instances
        ):
            raise USMSchemaError(
                "RelationEvaluationEnvironment.entity_instances has duplicate references"
            )
        if len({item.context_id for item in self.contexts}) != len(self.contexts):
            raise USMSchemaError("RelationEvaluationEnvironment.contexts has duplicate references")
        if len({item.request_id for item in self.capability_results}) != len(
            self.capability_results
        ):
            raise USMSchemaError(
                "RelationEvaluationEnvironment.capability_results has duplicate references"
            )

        traces = {item.trace_ref for item in self.entity_instances}
        for result in self.capability_results:
            if result.evaluation_trace.entity_trace_ref not in traces:
                raise USMSchemaError(
                    "RelationEvaluationEnvironment capability result does not resolve to entity"
                )
            entity = next(
                item
                for item in self.entity_instances
                if item.trace_ref == result.evaluation_trace.entity_trace_ref
            )
            if result.granted_rank > entity.state_rank:
                raise USMSchemaError(
                    "RelationEvaluationEnvironment capability result rank cannot exceed entity rank"
                )

    def resolve_entity_instance(
        self, entity_instance_ref: EntityInstanceRef
    ) -> EntityInstanceContract | None:
        return next(
            (
                item
                for item in self.entity_instances
                if item.entity_instance_ref == entity_instance_ref
            ),
            None,
        )

    def resolve_context(self, context_id: ContextId) -> EvaluationContextContract | None:
        return next((item for item in self.contexts if item.context_id == context_id), None)

    def resolve_capability_result(
        self, capability_result_ref: CapabilityEvaluationRef
    ) -> CapabilityEvaluationResult | None:
        return next(
            (
                item
                for item in self.capability_results
                if item.request_id.value == capability_result_ref.value
            ),
            None,
        )


@dataclass(frozen=True, slots=True)
class RelationEvaluationTrace:
    evaluation_trace_ref: TraceRef
    request_trace_ref: TraceRef
    context_trace_ref: TraceRef
    matrix_trace_ref: TraceRef
    relation_trace_ref: TraceRef
    entity_trace_refs: tuple[TraceRef, ...]
    capability_trace_refs: tuple[TraceRef, ...]
    decision_stage: str

    def __post_init__(self) -> None:
        if not isinstance(self.evaluation_trace_ref, TraceRef):
            raise USMSchemaError("RelationEvaluationTrace.evaluation_trace_ref must be TraceRef")
        if not isinstance(self.request_trace_ref, TraceRef):
            raise USMSchemaError("RelationEvaluationTrace.request_trace_ref must be TraceRef")
        if not isinstance(self.context_trace_ref, TraceRef):
            raise USMSchemaError("RelationEvaluationTrace.context_trace_ref must be TraceRef")
        if not isinstance(self.matrix_trace_ref, TraceRef):
            raise USMSchemaError("RelationEvaluationTrace.matrix_trace_ref must be TraceRef")
        if not isinstance(self.relation_trace_ref, TraceRef):
            raise USMSchemaError("RelationEvaluationTrace.relation_trace_ref must be TraceRef")
        require_tuple_of_type(
            "RelationEvaluationTrace", "entity_trace_refs", self.entity_trace_refs, TraceRef
        )
        require_tuple_of_type(
            "RelationEvaluationTrace",
            "capability_trace_refs",
            self.capability_trace_refs,
            TraceRef,
        )
        if not isinstance(self.decision_stage, str) or not self.decision_stage:
            raise USMSchemaError("RelationEvaluationTrace.decision_stage must be non-empty str")
        if self.evaluation_trace_ref == self.request_trace_ref:
            raise USMSchemaError("RelationEvaluationTrace must emit a new trace event")


@dataclass(frozen=True, slots=True)
class RelationEvaluationResult:
    request_id: RequestId
    state: RelationEvaluationState
    relation_type_id: RelationTypeId
    granted_rank: Rank
    failure_codes: tuple[USMFailureCode, ...]
    structural_saturation: bool
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef
    evaluation_trace: RelationEvaluationTrace

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, RequestId):
            raise USMSchemaError("RelationEvaluationResult.request_id must be RequestId")
        if not isinstance(self.state, RelationEvaluationState):
            raise USMSchemaError("RelationEvaluationResult.state must be RelationEvaluationState")
        if not isinstance(self.relation_type_id, RelationTypeId):
            raise USMSchemaError("RelationEvaluationResult.relation_type_id must be RelationTypeId")
        if not isinstance(self.granted_rank, Rank):
            raise USMSchemaError("RelationEvaluationResult.granted_rank must be Rank")
        require_tuple_of_type(
            "RelationEvaluationResult", "failure_codes", self.failure_codes, USMFailureCode
        )
        if not isinstance(self.structural_saturation, bool):
            raise USMSchemaError("RelationEvaluationResult.structural_saturation must be bool")
        require_tuple_of_type("RelationEvaluationResult", "residuals", self.residuals, USMResidual)
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("RelationEvaluationResult.trace_ref must be TraceRef")
        if not isinstance(self.evaluation_trace, RelationEvaluationTrace):
            raise USMSchemaError(
                "RelationEvaluationResult.evaluation_trace must be RelationEvaluationTrace"
            )
        if self.trace_ref != self.evaluation_trace.evaluation_trace_ref:
            raise USMSchemaError(
                "RelationEvaluationResult.trace_ref must equal "
                "evaluation_trace.evaluation_trace_ref"
            )
        self._assert_invariants()

    def _assert_invariants(self) -> None:
        if self.state is RelationEvaluationState.ELIGIBLE:
            if self.failure_codes:
                raise USMSchemaError("ELIGIBLE result cannot carry failure codes")
            if any(residual.blocking for residual in self.residuals):
                raise USMSchemaError("ELIGIBLE result cannot carry blocking residuals")
            if self.granted_rank is Rank.ZERO:
                raise USMSchemaError("ELIGIBLE result must grant non-zero rank")
            return
        if self.state is RelationEvaluationState.ELIGIBLE_WITH_RESIDUALS:
            if self.failure_codes:
                raise USMSchemaError("ELIGIBLE_WITH_RESIDUALS result cannot carry failure codes")
            if not self.residuals:
                raise USMSchemaError("ELIGIBLE_WITH_RESIDUALS requires visible residuals")
            if any(residual.blocking for residual in self.residuals):
                raise USMSchemaError(
                    "ELIGIBLE_WITH_RESIDUALS cannot carry blocking residuals"
                )
            if self.granted_rank is Rank.ZERO:
                raise USMSchemaError("ELIGIBLE_WITH_RESIDUALS result must grant non-zero rank")
            return
        if self.state is RelationEvaluationState.DEFERRED:
            if self.granted_rank is not Rank.ZERO:
                raise USMSchemaError("DEFERRED result must grant Rank.ZERO")
            if not self.failure_codes:
                raise USMSchemaError("DEFERRED result requires named deferred failure")
            return
        if self.state is RelationEvaluationState.BLOCKED:
            if self.granted_rank is not Rank.ZERO:
                raise USMSchemaError("BLOCKED result must grant Rank.ZERO")
            if not self.failure_codes:
                raise USMSchemaError("BLOCKED result requires named blocking failure")
            return
        if self.state is RelationEvaluationState.INVALID and self.granted_rank is not Rank.ZERO:
            raise USMSchemaError("INVALID result must grant Rank.ZERO")


_ELIGIBLE_CAPABILITY_STATES = frozenset(
    {CapabilityEvaluationState.ELIGIBLE, CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS}
)
_BLOCKING_FAILURE_CODES = frozenset(
    {
        USMFailureCode.RELATION_BLOCKER_ACTIVE,
        USMFailureCode.RELATION_BLOCKING_RESIDUAL,
        USMFailureCode.RELATION_OPERAND_TYPE_MISMATCH,
        USMFailureCode.RELATION_DIRECTION_MISMATCH,
        USMFailureCode.RELATION_CAPABILITY_NOT_ELIGIBLE,
        USMFailureCode.RELATION_RANK_CEILING_EXCEEDED,
    }
)
_DEFERRED_FAILURE_CODES = frozenset(
    {
        USMFailureCode.RELATION_OPERAND_UNRESOLVED,
        USMFailureCode.RELATION_REQUIRED_CAPABILITY_MISSING,
        USMFailureCode.RELATION_CAPABILITY_RESULT_UNRESOLVED,
        USMFailureCode.RELATION_REQUIRED_CONDITION_MISSING,
        USMFailureCode.RELATION_STRUCTURAL_SATURATION_INCOMPLETE,
    }
)


def evaluate_relation(
    matrix: UniversalScienceMatrix,
    environment: RelationEvaluationEnvironment,
    request: RelationEvaluationRequest,
) -> RelationEvaluationResult:
    """Evaluate relation eligibility only; never establish truth or execute transformations."""

    if not isinstance(matrix, UniversalScienceMatrix):
        raise USMSchemaError("evaluate_relation requires UniversalScienceMatrix")
    if not isinstance(environment, RelationEvaluationEnvironment):
        raise USMSchemaError("evaluate_relation requires RelationEvaluationEnvironment")
    if not isinstance(request, RelationEvaluationRequest):
        raise USMSchemaError("evaluate_relation requires RelationEvaluationRequest")

    failure_code: USMFailureCode | None = None
    state = RelationEvaluationState.DEFERRED
    granted_rank = Rank.ZERO
    structural_saturation = False
    residuals: tuple[USMResidual, ...] = matrix.residuals
    context: EvaluationContextContract | None = None
    relation = None
    resolved_entities: list[EntityInstanceContract] = []
    resolved_capability_results: list[CapabilityEvaluationResult] = []

    if request.matrix_id != matrix.matrix_id:
        failure_code = USMFailureCode.RELATION_MATRIX_MISMATCH
        state = RelationEvaluationState.INVALID
    elif request.science_id != matrix.science_id:
        failure_code = USMFailureCode.RELATION_SCIENCE_MISMATCH
        state = RelationEvaluationState.BLOCKED
    else:
        context = environment.resolve_context(request.context_id)
        if context is None:
            failure_code = USMFailureCode.RELATION_REQUIRED_CONDITION_MISSING
            state = RelationEvaluationState.DEFERRED
        elif context.science_id != matrix.science_id:
            failure_code = USMFailureCode.RELATION_SCIENCE_MISMATCH
            state = RelationEvaluationState.BLOCKED
        elif context.matrix_id != matrix.matrix_id:
            failure_code = USMFailureCode.RELATION_MATRIX_MISMATCH
            state = RelationEvaluationState.INVALID
        else:
            relation = next(
                (
                    item
                    for item in matrix.relations
                    if item.relation_type_id == request.relation_type_id
                ),
                None,
            )
            if relation is None:
                failure_code = USMFailureCode.RELATION_TYPE_UNRESOLVED
                state = RelationEvaluationState.INVALID
            elif relation.science_id != matrix.science_id:
                failure_code = USMFailureCode.RELATION_SCIENCE_MISMATCH
                state = RelationEvaluationState.BLOCKED
            elif len(request.operand_bindings) != relation.arity:
                failure_code = USMFailureCode.RELATION_ARITY_MISMATCH
                state = RelationEvaluationState.BLOCKED
            elif len({binding.position for binding in request.operand_bindings}) != len(
                request.operand_bindings
            ):
                failure_code = USMFailureCode.RELATION_POSITION_DUPLICATED
                state = RelationEvaluationState.BLOCKED
            elif len({binding.role_id for binding in request.operand_bindings}) != len(
                request.operand_bindings
            ):
                failure_code = USMFailureCode.RELATION_ROLE_DUPLICATED
                state = RelationEvaluationState.BLOCKED
            elif tuple(sorted(binding.position for binding in request.operand_bindings)) != tuple(
                range(relation.arity)
            ):
                failure_code = USMFailureCode.RELATION_STRUCTURAL_SATURATION_INCOMPLETE
                state = RelationEvaluationState.DEFERRED
            else:
                ordered_bindings = tuple(
                    sorted(request.operand_bindings, key=lambda item: item.position)
                )
                relation_role_values = tuple(item.value for item in relation.roles)
                binding_role_values = tuple(item.role_id.value for item in ordered_bindings)
                if any(value not in relation_role_values for value in binding_role_values):
                    failure_code = USMFailureCode.RELATION_ROLE_UNRESOLVED
                    state = RelationEvaluationState.BLOCKED
                elif relation.direction is RelationDirection.DIRECTED and (
                    binding_role_values != relation_role_values
                ):
                    failure_code = USMFailureCode.RELATION_DIRECTION_MISMATCH
                    state = RelationEvaluationState.BLOCKED
                else:
                    for index, binding in enumerate(ordered_bindings):
                        entity = environment.resolve_entity_instance(binding.entity_instance_ref)
                        if entity is None:
                            failure_code = USMFailureCode.RELATION_OPERAND_UNRESOLVED
                            state = RelationEvaluationState.DEFERRED
                            break
                        if entity.science_id != matrix.science_id:
                            failure_code = USMFailureCode.RELATION_SCIENCE_MISMATCH
                            state = RelationEvaluationState.BLOCKED
                            break
                        if entity.matrix_id != matrix.matrix_id:
                            failure_code = USMFailureCode.RELATION_MATRIX_MISMATCH
                            state = RelationEvaluationState.INVALID
                            break
                        if entity.entity_type_id != relation.operand_types[index]:
                            failure_code = USMFailureCode.RELATION_OPERAND_TYPE_MISMATCH
                            state = RelationEvaluationState.BLOCKED
                            break
                        capability_result = environment.resolve_capability_result(
                            binding.capability_result_ref
                        )
                        if capability_result is None:
                            failure_code = USMFailureCode.RELATION_CAPABILITY_RESULT_UNRESOLVED
                            state = RelationEvaluationState.DEFERRED
                            break
                        if capability_result.state not in _ELIGIBLE_CAPABILITY_STATES:
                            failure_code = USMFailureCode.RELATION_CAPABILITY_NOT_ELIGIBLE
                            state = RelationEvaluationState.BLOCKED
                            break
                        if capability_result.entity_type_id != entity.entity_type_id:
                            failure_code = USMFailureCode.RELATION_CAPABILITY_PROVENANCE_MISMATCH
                            state = RelationEvaluationState.BLOCKED
                            break
                        if (
                            capability_result.evaluation_trace.entity_trace_ref != entity.trace_ref
                            or capability_result.evaluation_trace.context_trace_ref
                            != context.trace_ref
                            or capability_result.evaluation_trace.matrix_trace_ref
                            != matrix.trace_ref
                        ):
                            failure_code = USMFailureCode.RELATION_CAPABILITY_PROVENANCE_MISMATCH
                            state = RelationEvaluationState.BLOCKED
                            break
                        if capability_result.granted_rank > entity.state_rank:
                            failure_code = USMFailureCode.RELATION_CAPABILITY_PROVENANCE_MISMATCH
                            state = RelationEvaluationState.BLOCKED
                            break

                        capability_contract = next(
                            (
                                item
                                for item in matrix.capabilities
                                if item.capability_id == capability_result.capability_id
                            ),
                            None,
                        )
                        if capability_contract is None:
                            failure_code = USMFailureCode.RELATION_REQUIRED_CAPABILITY_MISSING
                            state = RelationEvaluationState.DEFERRED
                            break
                        if capability_contract.bearer_type != entity.entity_type_id:
                            failure_code = USMFailureCode.RELATION_CAPABILITY_PROVENANCE_MISMATCH
                            state = RelationEvaluationState.BLOCKED
                            break
                        if (
                            relation.roles[index]
                            not in capability_contract.permitted_relation_roles
                        ):
                            failure_code = USMFailureCode.RELATION_REQUIRED_CAPABILITY_MISSING
                            state = RelationEvaluationState.DEFERRED
                            break
                        resolved_entities.append(entity)
                        resolved_capability_results.append(capability_result)

                    if failure_code is None:
                        required_conditions = relation.compatibility_rules + (
                            relation.saturation_rule,
                            relation.scope_rule,
                        )
                        missing_conditions = tuple(
                            condition
                            for condition in required_conditions
                            if condition not in context.active_condition_refs
                        )
                        if missing_conditions:
                            failure_code = USMFailureCode.RELATION_REQUIRED_CONDITION_MISSING
                            state = RelationEvaluationState.DEFERRED
                        else:
                            active_blockers = tuple(
                                blocker
                                for blocker in context.active_blocker_refs
                                if blocker in required_conditions
                            )
                            if active_blockers:
                                failure_code = USMFailureCode.RELATION_BLOCKER_ACTIVE
                                state = RelationEvaluationState.BLOCKED
                            else:
                                residuals = (
                                    matrix.residuals
                                    + context.residuals
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
                                    failure_code = USMFailureCode.RELATION_BLOCKING_RESIDUAL
                                    state = RelationEvaluationState.BLOCKED
                                else:
                                    evidence_contracts = {
                                        contract.evidence_type_id: contract
                                        for contract in matrix.evidence
                                    }
                                    evidence_rank_ceiling = min(
                                        (
                                            evidence_contracts[evidence].global_rank_ceiling
                                            for result in resolved_capability_results
                                            for evidence in result.recognized_evidence_type_refs
                                            if evidence in evidence_contracts
                                        ),
                                        default=max(Rank),
                                    )
                                    granted_rank = min(
                                        request.requested_rank,
                                        relation.rank_ceiling,
                                        min(entity.state_rank for entity in resolved_entities),
                                        min(
                                            result.granted_rank
                                            for result in resolved_capability_results
                                        ),
                                        evidence_rank_ceiling,
                                    )
                                    if granted_rank < request.requested_rank:
                                        failure_code = USMFailureCode.RELATION_RANK_CEILING_EXCEEDED
                                        state = RelationEvaluationState.BLOCKED
                                        granted_rank = Rank.ZERO
                                    else:
                                        structural_saturation = True
                                        state = (
                                            RelationEvaluationState.ELIGIBLE_WITH_RESIDUALS
                                            if residuals
                                            else RelationEvaluationState.ELIGIBLE
                                        )

    trace_failure = _trace_chain_failure(
        matrix=matrix,
        request=request,
        relation_trace_ref=relation.trace_ref if relation is not None else None,
        context=context,
        entities=tuple(resolved_entities),
        capability_results=tuple(resolved_capability_results),
    )
    if trace_failure is not None:
        failure_code = trace_failure
        state = RelationEvaluationState.INVALID
        granted_rank = Rank.ZERO

    failure_codes = () if failure_code is None else (failure_code,)
    if state is RelationEvaluationState.INVALID and not failure_codes:
        failure_codes = (USMFailureCode.SCHEMA_INVALID,)
    if state is RelationEvaluationState.BLOCKED and failure_codes and (
        failure_codes[0] not in _BLOCKING_FAILURE_CODES
    ):
        state = RelationEvaluationState.INVALID
        granted_rank = Rank.ZERO
    if state is RelationEvaluationState.DEFERRED and failure_codes and (
        failure_codes[0] not in _DEFERRED_FAILURE_CODES
    ):
        state = RelationEvaluationState.INVALID
        granted_rank = Rank.ZERO

    trace = _emit_trace(
        matrix=matrix,
        request=request,
        state=state,
        relation_trace_ref=(
            relation.trace_ref
            if relation is not None
            else TraceRef(
                f"{matrix.trace_ref.value}/unresolved/relation/"
                f"{request.relation_type_id.value}"
            )
        ),
        context_trace_ref=(
            context.trace_ref
            if context is not None
            else TraceRef(f"{matrix.trace_ref.value}/unresolved/context/{request.context_id.value}")
        ),
        entity_trace_refs=tuple(entity.trace_ref for entity in resolved_entities),
        capability_trace_refs=tuple(
            result.evaluation_trace.evaluation_trace_ref for result in resolved_capability_results
        ),
    )
    return RelationEvaluationResult(
        request_id=request.request_id,
        state=state,
        relation_type_id=request.relation_type_id,
        granted_rank=granted_rank if state in _ELIGIBLE_STATES else Rank.ZERO,
        failure_codes=failure_codes,
        structural_saturation=structural_saturation,
        residuals=residuals,
        trace_ref=trace.evaluation_trace_ref,
        evaluation_trace=trace,
    )


_ELIGIBLE_STATES = frozenset(
    {RelationEvaluationState.ELIGIBLE, RelationEvaluationState.ELIGIBLE_WITH_RESIDUALS}
)


def _trace_chain_failure(
    *,
    matrix: UniversalScienceMatrix,
    request: RelationEvaluationRequest,
    relation_trace_ref: TraceRef | None,
    context: EvaluationContextContract | None,
    entities: tuple[EntityInstanceContract, ...],
    capability_results: tuple[CapabilityEvaluationResult, ...],
) -> USMFailureCode | None:
    expected_prefix = f"{matrix.trace_ref.value}/requests/{request.request_id.value}"
    if not request.trace_ref.value.startswith(expected_prefix):
        return USMFailureCode.RELATION_TRACE_CHAIN_BROKEN

    traces: list[TraceRef] = [matrix.trace_ref, request.trace_ref]
    if relation_trace_ref is not None:
        traces.append(relation_trace_ref)
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
            return USMFailureCode.RELATION_TRACE_CHAIN_BROKEN
    return None


def _emit_trace(
    *,
    matrix: UniversalScienceMatrix,
    request: RelationEvaluationRequest,
    state: RelationEvaluationState,
    relation_trace_ref: TraceRef,
    context_trace_ref: TraceRef,
    entity_trace_refs: tuple[TraceRef, ...],
    capability_trace_refs: tuple[TraceRef, ...],
) -> RelationEvaluationTrace:
    base = (
        request.trace_ref.value
        if request.trace_ref.value.startswith("trace://")
        else f"{matrix.trace_ref.value}/requests/{request.request_id.value}"
    )
    decision_stage = f"relation-evaluation/{state.value.lower()}"
    evaluation_trace_ref = TraceRef(
        f"{base}/decisions/{request.request_id.value}/{request.relation_type_id.value}/{decision_stage}"
    )
    return RelationEvaluationTrace(
        evaluation_trace_ref=evaluation_trace_ref,
        request_trace_ref=request.trace_ref,
        context_trace_ref=context_trace_ref,
        matrix_trace_ref=matrix.trace_ref,
        relation_trace_ref=relation_trace_ref,
        entity_trace_refs=entity_trace_refs,
        capability_trace_refs=capability_trace_refs,
        decision_stage=decision_stage,
    )


__all__ = [
    "RelationEvaluationEnvironment",
    "RelationEvaluationRequest",
    "RelationEvaluationResult",
    "RelationEvaluationState",
    "RelationEvaluationTrace",
    "RelationOperandBinding",
    "evaluate_relation",
]
