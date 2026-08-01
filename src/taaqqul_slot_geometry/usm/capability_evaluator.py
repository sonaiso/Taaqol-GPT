"""USM-C3.1 bounded capability evaluator hardening (pure, deterministic, non-executive)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.usm.capability_contract import CapabilityContract
from taaqqul_slot_geometry.usm.entity_contract import EntityTypeContract
from taaqqul_slot_geometry.usm.identifiers import (
    CapabilityId,
    ContextId,
    EntityInstanceRef,
    EntityTypeId,
    EvidenceTypeId,
    MatrixId,
    RequestId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)
from taaqqul_slot_geometry.usm.matrix import UniversalScienceMatrix
from taaqqul_slot_geometry.usm.residuals import USMResidual
from taaqqul_slot_geometry.usm.validator import USMFailureCode


class CapabilityEvaluationState(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    ELIGIBLE_WITH_RESIDUALS = "ELIGIBLE_WITH_RESIDUALS"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class EntityInstanceContract:
    entity_instance_ref: EntityInstanceRef
    entity_type_id: EntityTypeId
    science_id: ScienceId
    matrix_id: MatrixId
    state_rank: Rank
    active_property_refs: tuple[RuleId, ...]
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.entity_instance_ref, EntityInstanceRef):
            raise USMSchemaError(
                "EntityInstanceContract.entity_instance_ref must be EntityInstanceRef"
            )
        if not isinstance(self.entity_type_id, EntityTypeId):
            raise USMSchemaError("EntityInstanceContract.entity_type_id must be EntityTypeId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("EntityInstanceContract.science_id must be ScienceId")
        if not isinstance(self.matrix_id, MatrixId):
            raise USMSchemaError("EntityInstanceContract.matrix_id must be MatrixId")
        if not isinstance(self.state_rank, Rank):
            raise USMSchemaError("EntityInstanceContract.state_rank must be Rank")
        require_tuple_of_type(
            "EntityInstanceContract",
            "active_property_refs",
            self.active_property_refs,
            RuleId,
        )
        require_tuple_of_type("EntityInstanceContract", "residuals", self.residuals, USMResidual)
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("EntityInstanceContract.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class EvaluationContextContract:
    context_id: ContextId
    science_id: ScienceId
    matrix_id: MatrixId
    active_condition_refs: tuple[RuleId, ...]
    active_blocker_refs: tuple[RuleId, ...]
    supplied_evidence_type_refs: tuple[EvidenceTypeId, ...]
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.context_id, ContextId):
            raise USMSchemaError("EvaluationContextContract.context_id must be ContextId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("EvaluationContextContract.science_id must be ScienceId")
        if not isinstance(self.matrix_id, MatrixId):
            raise USMSchemaError("EvaluationContextContract.matrix_id must be MatrixId")
        require_tuple_of_type(
            "EvaluationContextContract",
            "active_condition_refs",
            self.active_condition_refs,
            RuleId,
        )
        require_tuple_of_type(
            "EvaluationContextContract",
            "active_blocker_refs",
            self.active_blocker_refs,
            RuleId,
        )
        require_tuple_of_type(
            "EvaluationContextContract",
            "supplied_evidence_type_refs",
            self.supplied_evidence_type_refs,
            EvidenceTypeId,
        )
        require_tuple_of_type("EvaluationContextContract", "residuals", self.residuals, USMResidual)
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("EvaluationContextContract.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class CapabilityEvaluationEnvironment:
    entity_instances: tuple[EntityInstanceContract, ...]
    contexts: tuple[EvaluationContextContract, ...]

    def __post_init__(self) -> None:
        require_tuple_of_type(
            "CapabilityEvaluationEnvironment",
            "entity_instances",
            self.entity_instances,
            EntityInstanceContract,
        )
        require_tuple_of_type(
            "CapabilityEvaluationEnvironment",
            "contexts",
            self.contexts,
            EvaluationContextContract,
        )
        if len({item.entity_instance_ref for item in self.entity_instances}) != len(
            self.entity_instances
        ):
            raise USMSchemaError(
                "CapabilityEvaluationEnvironment.entity_instances has duplicate references"
            )
        if len({item.context_id for item in self.contexts}) != len(self.contexts):
            raise USMSchemaError(
                "CapabilityEvaluationEnvironment.contexts has duplicate references"
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


@dataclass(frozen=True, slots=True)
class CapabilityEvaluationTrace:
    evaluation_trace_ref: TraceRef
    request_trace_ref: TraceRef
    entity_trace_ref: TraceRef
    context_trace_ref: TraceRef
    matrix_trace_ref: TraceRef
    capability_trace_ref: TraceRef
    decision_stage: str

    def __post_init__(self) -> None:
        if not isinstance(self.evaluation_trace_ref, TraceRef):
            raise USMSchemaError("CapabilityEvaluationTrace.evaluation_trace_ref must be TraceRef")
        if not isinstance(self.request_trace_ref, TraceRef):
            raise USMSchemaError("CapabilityEvaluationTrace.request_trace_ref must be TraceRef")
        if not isinstance(self.entity_trace_ref, TraceRef):
            raise USMSchemaError("CapabilityEvaluationTrace.entity_trace_ref must be TraceRef")
        if not isinstance(self.context_trace_ref, TraceRef):
            raise USMSchemaError("CapabilityEvaluationTrace.context_trace_ref must be TraceRef")
        if not isinstance(self.matrix_trace_ref, TraceRef):
            raise USMSchemaError("CapabilityEvaluationTrace.matrix_trace_ref must be TraceRef")
        if not isinstance(self.capability_trace_ref, TraceRef):
            raise USMSchemaError("CapabilityEvaluationTrace.capability_trace_ref must be TraceRef")
        if not isinstance(self.decision_stage, str) or not self.decision_stage:
            raise USMSchemaError("CapabilityEvaluationTrace.decision_stage must be non-empty str")
        if self.evaluation_trace_ref == self.request_trace_ref:
            raise USMSchemaError("CapabilityEvaluationTrace must emit a new trace event")


@dataclass(frozen=True, slots=True)
class CapabilityEvaluationRequest:
    request_id: RequestId
    matrix_id: MatrixId
    science_id: ScienceId
    entity_type_id: EntityTypeId
    entity_instance_ref: EntityInstanceRef
    capability_id: CapabilityId
    context_id: ContextId
    supplied_condition_refs: tuple[RuleId, ...]
    supplied_evidence_type_refs: tuple[EvidenceTypeId, ...]
    active_blocker_refs: tuple[RuleId, ...]
    requested_rank: Rank
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, RequestId):
            raise USMSchemaError("CapabilityEvaluationRequest.request_id must be RequestId")
        if not isinstance(self.matrix_id, MatrixId):
            raise USMSchemaError("CapabilityEvaluationRequest.matrix_id must be MatrixId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("CapabilityEvaluationRequest.science_id must be ScienceId")
        if not isinstance(self.entity_type_id, EntityTypeId):
            raise USMSchemaError("CapabilityEvaluationRequest.entity_type_id must be EntityTypeId")
        if not isinstance(self.entity_instance_ref, EntityInstanceRef):
            raise USMSchemaError(
                "CapabilityEvaluationRequest.entity_instance_ref must be EntityInstanceRef"
            )
        if not isinstance(self.capability_id, CapabilityId):
            raise USMSchemaError("CapabilityEvaluationRequest.capability_id must be CapabilityId")
        if not isinstance(self.context_id, ContextId):
            raise USMSchemaError("CapabilityEvaluationRequest.context_id must be ContextId")
        require_tuple_of_type(
            "CapabilityEvaluationRequest",
            "supplied_condition_refs",
            self.supplied_condition_refs,
            RuleId,
        )
        require_tuple_of_type(
            "CapabilityEvaluationRequest",
            "supplied_evidence_type_refs",
            self.supplied_evidence_type_refs,
            EvidenceTypeId,
        )
        require_tuple_of_type(
            "CapabilityEvaluationRequest",
            "active_blocker_refs",
            self.active_blocker_refs,
            RuleId,
        )
        if not isinstance(self.requested_rank, Rank):
            raise USMSchemaError("CapabilityEvaluationRequest.requested_rank must be Rank")
        require_tuple_of_type(
            "CapabilityEvaluationRequest", "residuals", self.residuals, USMResidual
        )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("CapabilityEvaluationRequest.trace_ref must be TraceRef")


@dataclass(frozen=True, slots=True)
class CapabilityEvaluationResult:
    request_id: RequestId
    state: CapabilityEvaluationState
    capability_id: CapabilityId
    entity_type_id: EntityTypeId
    granted_rank: Rank
    satisfied_conditions: tuple[RuleId, ...]
    missing_conditions: tuple[RuleId, ...]
    active_blockers: tuple[RuleId, ...]
    recognized_evidence_type_refs: tuple[EvidenceTypeId, ...]
    failure_codes: tuple[USMFailureCode, ...]
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef
    evaluation_trace: CapabilityEvaluationTrace

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, RequestId):
            raise USMSchemaError("CapabilityEvaluationResult.request_id must be RequestId")
        if not isinstance(self.state, CapabilityEvaluationState):
            raise USMSchemaError(
                "CapabilityEvaluationResult.state must be CapabilityEvaluationState"
            )
        if not isinstance(self.capability_id, CapabilityId):
            raise USMSchemaError("CapabilityEvaluationResult.capability_id must be CapabilityId")
        if not isinstance(self.entity_type_id, EntityTypeId):
            raise USMSchemaError("CapabilityEvaluationResult.entity_type_id must be EntityTypeId")
        if not isinstance(self.granted_rank, Rank):
            raise USMSchemaError("CapabilityEvaluationResult.granted_rank must be Rank")
        require_tuple_of_type(
            "CapabilityEvaluationResult", "satisfied_conditions", self.satisfied_conditions, RuleId
        )
        require_tuple_of_type(
            "CapabilityEvaluationResult", "missing_conditions", self.missing_conditions, RuleId
        )
        require_tuple_of_type(
            "CapabilityEvaluationResult", "active_blockers", self.active_blockers, RuleId
        )
        require_tuple_of_type(
            "CapabilityEvaluationResult",
            "recognized_evidence_type_refs",
            self.recognized_evidence_type_refs,
            EvidenceTypeId,
        )
        require_tuple_of_type(
            "CapabilityEvaluationResult", "failure_codes", self.failure_codes, USMFailureCode
        )
        require_tuple_of_type(
            "CapabilityEvaluationResult", "residuals", self.residuals, USMResidual
        )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("CapabilityEvaluationResult.trace_ref must be TraceRef")
        if not isinstance(self.evaluation_trace, CapabilityEvaluationTrace):
            raise USMSchemaError(
                "CapabilityEvaluationResult.evaluation_trace must be CapabilityEvaluationTrace"
            )
        if self.trace_ref != self.evaluation_trace.evaluation_trace_ref:
            raise USMSchemaError(
                "CapabilityEvaluationResult.trace_ref must equal "
                "evaluation_trace.evaluation_trace_ref"
            )
        self._assert_invariants()

    def _assert_invariants(self) -> None:
        if self.state is CapabilityEvaluationState.ELIGIBLE:
            if self.failure_codes or self.missing_conditions or self.active_blockers:
                raise USMSchemaError("ELIGIBLE result cannot carry blockers or failure codes")
            if any(residual.blocking for residual in self.residuals):
                raise USMSchemaError("ELIGIBLE result cannot carry blocking residuals")
            if self.granted_rank is Rank.ZERO:
                raise USMSchemaError("ELIGIBLE result must grant non-zero rank")
            return

        if self.state is CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS:
            if self.failure_codes:
                raise USMSchemaError("ELIGIBLE_WITH_RESIDUALS result cannot carry failure codes")
            if not self.residuals:
                raise USMSchemaError(
                    "ELIGIBLE_WITH_RESIDUALS result requires visible non-blocking residuals"
                )
            if any(residual.blocking for residual in self.residuals):
                raise USMSchemaError(
                    "ELIGIBLE_WITH_RESIDUALS rejects blocking residuals by invariant"
                )
            if self.granted_rank is Rank.ZERO:
                raise USMSchemaError("ELIGIBLE_WITH_RESIDUALS result must grant non-zero rank")
            return

        if self.state is CapabilityEvaluationState.DEFERRED:
            if self.granted_rank is not Rank.ZERO:
                raise USMSchemaError("DEFERRED result must grant Rank.ZERO")
            if not self.failure_codes:
                raise USMSchemaError("DEFERRED result requires named deferred failure")
            if any(code in _BLOCKING_FAILURE_CODES for code in self.failure_codes):
                raise USMSchemaError("DEFERRED result cannot carry blocking failure codes")
            if self.active_blockers:
                raise USMSchemaError("DEFERRED result cannot carry active blockers")
            return

        if self.state is CapabilityEvaluationState.BLOCKED:
            if not self.failure_codes:
                raise USMSchemaError("BLOCKED result requires named blocking failure")
            if not any(code in _BLOCKING_FAILURE_CODES for code in self.failure_codes):
                raise USMSchemaError("BLOCKED result requires at least one blocking failure code")
            return

        if self.state is CapabilityEvaluationState.INVALID and self.granted_rank is not Rank.ZERO:
            raise USMSchemaError("INVALID result must grant Rank.ZERO")


_BLOCKING_FAILURE_CODES: frozenset[USMFailureCode] = frozenset(
    {
        USMFailureCode.CAPABILITY_BLOCKER_ACTIVE,
        USMFailureCode.CAPABILITY_BLOCKING_RESIDUAL,
        USMFailureCode.CAPABILITY_BEARER_TYPE_MISMATCH,
        USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE,
        USMFailureCode.CAPABILITY_ENTITY_INSTANCE_TYPE_MISMATCH,
        USMFailureCode.CAPABILITY_SCIENCE_MISMATCH,
        USMFailureCode.CAPABILITY_RANK_CEILING_EXCEEDED,
        USMFailureCode.CAPABILITY_ENTITY_RANK_CEILING_EXCEEDED,
    }
)

_INVALID_FAILURE_CODES: frozenset[USMFailureCode] = frozenset(
    {
        USMFailureCode.SCHEMA_INVALID,
        USMFailureCode.CAPABILITY_RESULT_INVARIANT_VIOLATION,
        USMFailureCode.CAPABILITY_TRACE_CHAIN_BROKEN,
        USMFailureCode.CAPABILITY_MATRIX_ID_MISMATCH,
        USMFailureCode.CAPABILITY_CONTEXT_MATRIX_MISMATCH,
        USMFailureCode.CAPABILITY_CONTEXT_SCIENCE_MISMATCH,
    }
)


def evaluate_capability(
    matrix: UniversalScienceMatrix,
    environment: CapabilityEvaluationEnvironment,
    request: CapabilityEvaluationRequest,
) -> CapabilityEvaluationResult:
    """Evaluate structural capability eligibility only; never relation or transformation."""

    if not isinstance(matrix, UniversalScienceMatrix):
        raise USMSchemaError("evaluate_capability requires UniversalScienceMatrix")
    if not isinstance(environment, CapabilityEvaluationEnvironment):
        raise USMSchemaError("evaluate_capability requires CapabilityEvaluationEnvironment")
    if not isinstance(request, CapabilityEvaluationRequest):
        raise USMSchemaError("evaluate_capability requires CapabilityEvaluationRequest")

    failure_code: USMFailureCode | None = None
    state = CapabilityEvaluationState.DEFERRED
    granted_rank = Rank.ZERO
    satisfied_conditions: tuple[RuleId, ...] = ()
    missing_conditions: tuple[RuleId, ...] = ()
    active_blockers: tuple[RuleId, ...] = ()
    recognized_evidence_type_refs: tuple[EvidenceTypeId, ...] = ()
    residuals = request.residuals

    matrix_evidence = {contract.evidence_type_id: contract for contract in matrix.evidence}
    matrix_capabilities = {contract.capability_id: contract for contract in matrix.capabilities}
    matrix_entities = {contract.entity_type_id: contract for contract in matrix.entities}

    entity_instance: EntityInstanceContract | None = None
    context: EvaluationContextContract | None = None
    capability_contract: CapabilityContract | None = None
    entity_contract: EntityTypeContract | None = None

    if request.matrix_id != matrix.matrix_id:
        failure_code = USMFailureCode.CAPABILITY_MATRIX_ID_MISMATCH
        state = CapabilityEvaluationState.INVALID
    elif request.science_id != matrix.science_id:
        failure_code = USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE
        state = CapabilityEvaluationState.BLOCKED
    else:
        entity_instance = environment.resolve_entity_instance(request.entity_instance_ref)
        if entity_instance is None:
            failure_code = USMFailureCode.CAPABILITY_ENTITY_INSTANCE_UNRESOLVED
            state = CapabilityEvaluationState.DEFERRED
        elif entity_instance.entity_type_id != request.entity_type_id:
            failure_code = USMFailureCode.CAPABILITY_ENTITY_INSTANCE_TYPE_MISMATCH
            state = CapabilityEvaluationState.BLOCKED
        elif entity_instance.science_id != matrix.science_id:
            failure_code = USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE
            state = CapabilityEvaluationState.BLOCKED
        elif entity_instance.matrix_id != matrix.matrix_id:
            failure_code = USMFailureCode.CAPABILITY_MATRIX_ID_MISMATCH
            state = CapabilityEvaluationState.INVALID
        else:
            entity_contract = matrix_entities.get(request.entity_type_id)
            if entity_contract is None:
                failure_code = USMFailureCode.ENTITY_TYPE_UNRESOLVED
                state = CapabilityEvaluationState.INVALID
            else:
                context = environment.resolve_context(request.context_id)
                if context is None:
                    failure_code = USMFailureCode.CAPABILITY_CONTEXT_UNRESOLVED
                    state = CapabilityEvaluationState.DEFERRED
                elif context.science_id != matrix.science_id:
                    failure_code = USMFailureCode.CAPABILITY_CONTEXT_SCIENCE_MISMATCH
                    state = CapabilityEvaluationState.INVALID
                elif context.matrix_id != matrix.matrix_id:
                    failure_code = USMFailureCode.CAPABILITY_CONTEXT_MATRIX_MISMATCH
                    state = CapabilityEvaluationState.INVALID
                else:
                    capability_contract = matrix_capabilities.get(request.capability_id)
                    if capability_contract is None:
                        failure_code = USMFailureCode.CAPABILITY_ID_UNRESOLVED
                        state = CapabilityEvaluationState.INVALID
                    elif capability_contract.science_id != matrix.science_id:
                        failure_code = USMFailureCode.CAPABILITY_SCIENCE_MISMATCH
                        state = CapabilityEvaluationState.BLOCKED
                    elif capability_contract.bearer_type != request.entity_type_id:
                        failure_code = USMFailureCode.CAPABILITY_BEARER_TYPE_MISMATCH
                        state = CapabilityEvaluationState.BLOCKED
                    else:
                        supplied_conditions = {
                            *request.supplied_condition_refs,
                            *context.active_condition_refs,
                        }
                        missing_conditions = tuple(
                            condition
                            for condition in capability_contract.required_conditions
                            if condition not in supplied_conditions
                        )
                        satisfied_conditions = tuple(
                            condition
                            for condition in capability_contract.required_conditions
                            if condition in supplied_conditions
                        )
                        if missing_conditions:
                            failure_code = USMFailureCode.CAPABILITY_CONDITION_MISSING
                            state = CapabilityEvaluationState.DEFERRED
                        else:
                            active_requested_blockers = {
                                *request.active_blocker_refs,
                                *context.active_blocker_refs,
                            }
                            active_blockers = tuple(
                                blocker
                                for blocker in capability_contract.blockers
                                if blocker in active_requested_blockers
                            )
                            if active_blockers:
                                failure_code = USMFailureCode.CAPABILITY_BLOCKER_ACTIVE
                                state = CapabilityEvaluationState.BLOCKED
                            else:
                                unresolved_evidence = tuple(
                                    evidence
                                    for evidence in capability_contract.evidence_requirements
                                    if evidence not in matrix_evidence
                                )
                                if unresolved_evidence:
                                    failure_code = (
                                        USMFailureCode.CAPABILITY_EVIDENCE_TYPE_UNRESOLVED
                                    )
                                    state = CapabilityEvaluationState.DEFERRED
                                else:
                                    supplied_evidence = {
                                        *request.supplied_evidence_type_refs,
                                        *context.supplied_evidence_type_refs,
                                    }
                                    missing_evidence = tuple(
                                        evidence
                                        for evidence in capability_contract.evidence_requirements
                                        if evidence not in supplied_evidence
                                    )
                                    if missing_evidence:
                                        failure_code = (
                                            USMFailureCode.CAPABILITY_EVIDENCE_TYPE_NOT_SUPPLIED
                                        )
                                        state = CapabilityEvaluationState.DEFERRED
                                    else:
                                        recognized_evidence_type_refs = tuple(
                                            evidence
                                            for evidence in (
                                                capability_contract.evidence_requirements
                                            )
                                            if evidence in matrix_evidence
                                        )
                                        evidence_ceiling = min(
                                            (
                                                matrix_evidence[evidence].global_rank_ceiling
                                                for evidence in recognized_evidence_type_refs
                                            ),
                                            default=max(Rank),
                                        )
                                        granted_rank = min(
                                            request.requested_rank,
                                            entity_instance.state_rank,
                                            capability_contract.rank_ceiling,
                                            evidence_ceiling,
                                        )
                                        if request.requested_rank > entity_instance.state_rank:
                                            failure_code = (
                                                USMFailureCode.CAPABILITY_ENTITY_RANK_CEILING_EXCEEDED
                                            )
                                            state = CapabilityEvaluationState.BLOCKED
                                        elif request.requested_rank > granted_rank:
                                            failure_code = (
                                                USMFailureCode.CAPABILITY_RANK_CEILING_EXCEEDED
                                            )
                                            state = CapabilityEvaluationState.BLOCKED
                                        else:
                                            residuals = (
                                                request.residuals
                                                + matrix.residuals
                                                + entity_instance.residuals
                                                + context.residuals
                                            )
                                            blocking_residuals = tuple(
                                                residual
                                                for residual in residuals
                                                if residual.blocking
                                            )
                                            if blocking_residuals:
                                                failure_code = (
                                                    USMFailureCode.CAPABILITY_BLOCKING_RESIDUAL
                                                )
                                                state = CapabilityEvaluationState.BLOCKED
                                            else:
                                                state = (
                                                    CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS
                                                    if residuals
                                                    else CapabilityEvaluationState.ELIGIBLE
                                                )

    trace_code = _trace_chain_failure(
        matrix=matrix,
        request=request,
        capability_contract=capability_contract,
        entity_instance=entity_instance,
        context=context,
    )
    if trace_code is not None and state is not CapabilityEvaluationState.INVALID:
        state = CapabilityEvaluationState.INVALID
        granted_rank = Rank.ZERO
        failure_code = trace_code

    failure_codes = () if failure_code is None else (failure_code,)
    result = _build_result(
        matrix=matrix,
        request=request,
        state=state,
        granted_rank=granted_rank,
        satisfied_conditions=satisfied_conditions,
        missing_conditions=missing_conditions,
        active_blockers=active_blockers,
        recognized_evidence_type_refs=recognized_evidence_type_refs,
        failure_codes=failure_codes,
        residuals=residuals,
        capability_contract=capability_contract,
        entity_instance=entity_instance,
        context=context,
    )
    return result


def _trace_chain_failure(
    *,
    matrix: UniversalScienceMatrix,
    request: CapabilityEvaluationRequest,
    capability_contract: CapabilityContract | None,
    entity_instance: EntityInstanceContract | None,
    context: EvaluationContextContract | None,
) -> USMFailureCode | None:
    expected_prefix = f"{matrix.trace_ref.value}/requests/{request.request_id.value}"
    if not request.trace_ref.value.startswith(expected_prefix):
        return USMFailureCode.CAPABILITY_TRACE_CHAIN_BROKEN

    traces = [matrix.trace_ref]
    if capability_contract is not None:
        traces.append(capability_contract.trace_ref)
    if entity_instance is not None:
        traces.append(entity_instance.trace_ref)
    if context is not None:
        traces.append(context.trace_ref)

    for trace in traces:
        if not (
            trace.value == matrix.trace_ref.value
            or trace.value.startswith(f"{matrix.trace_ref.value}/")
        ):
            return USMFailureCode.CAPABILITY_TRACE_CHAIN_BROKEN
    return None


def _build_result(
    *,
    matrix: UniversalScienceMatrix,
    request: CapabilityEvaluationRequest,
    state: CapabilityEvaluationState,
    granted_rank: Rank,
    satisfied_conditions: tuple[RuleId, ...],
    missing_conditions: tuple[RuleId, ...],
    active_blockers: tuple[RuleId, ...],
    recognized_evidence_type_refs: tuple[EvidenceTypeId, ...],
    failure_codes: tuple[USMFailureCode, ...],
    residuals: tuple[USMResidual, ...],
    capability_contract: CapabilityContract | None,
    entity_instance: EntityInstanceContract | None,
    context: EvaluationContextContract | None,
) -> CapabilityEvaluationResult:
    effective_rank = (
        Rank.ZERO
        if state in {CapabilityEvaluationState.INVALID, CapabilityEvaluationState.DEFERRED}
        else granted_rank
    )
    if state is CapabilityEvaluationState.INVALID:
        failure_codes = (
            failure_codes
            if failure_codes
            else (USMFailureCode.CAPABILITY_RESULT_INVARIANT_VIOLATION,)
        )

    trace = _emit_trace(
        matrix=matrix,
        request=request,
        capability_contract=capability_contract,
        entity_instance=entity_instance,
        context=context,
        state=state,
    )

    try:
        return CapabilityEvaluationResult(
            request_id=request.request_id,
            state=state,
            capability_id=request.capability_id,
            entity_type_id=request.entity_type_id,
            granted_rank=effective_rank,
            satisfied_conditions=satisfied_conditions,
            missing_conditions=missing_conditions,
            active_blockers=active_blockers,
            recognized_evidence_type_refs=recognized_evidence_type_refs,
            failure_codes=failure_codes,
            residuals=residuals,
            trace_ref=trace.evaluation_trace_ref,
            evaluation_trace=trace,
        )
    except USMSchemaError:
        fallback_trace = _emit_trace(
            matrix=matrix,
            request=request,
            capability_contract=capability_contract,
            entity_instance=entity_instance,
            context=context,
            state=CapabilityEvaluationState.INVALID,
        )
        return CapabilityEvaluationResult(
            request_id=request.request_id,
            state=CapabilityEvaluationState.INVALID,
            capability_id=request.capability_id,
            entity_type_id=request.entity_type_id,
            granted_rank=Rank.ZERO,
            satisfied_conditions=(),
            missing_conditions=(),
            active_blockers=(),
            recognized_evidence_type_refs=(),
            failure_codes=(USMFailureCode.CAPABILITY_RESULT_INVARIANT_VIOLATION,),
            residuals=residuals,
            trace_ref=fallback_trace.evaluation_trace_ref,
            evaluation_trace=fallback_trace,
        )


def _emit_trace(
    *,
    matrix: UniversalScienceMatrix,
    request: CapabilityEvaluationRequest,
    capability_contract: CapabilityContract | None,
    entity_instance: EntityInstanceContract | None,
    context: EvaluationContextContract | None,
    state: CapabilityEvaluationState,
) -> CapabilityEvaluationTrace:
    base = (
        request.trace_ref.value
        if request.trace_ref.value.startswith("trace://")
        else f"{matrix.trace_ref.value}/requests/{request.request_id.value}"
    )
    decision_stage = f"capability-evaluation/{state.value.lower()}"
    evaluation_trace_ref = TraceRef(
        f"{base}/decisions/{request.request_id.value}/{request.capability_id.value}/{decision_stage}"
    )
    return CapabilityEvaluationTrace(
        evaluation_trace_ref=evaluation_trace_ref,
        request_trace_ref=request.trace_ref,
        entity_trace_ref=(
            entity_instance.trace_ref
            if entity_instance is not None
            else TraceRef(
                f"{matrix.trace_ref.value}/unresolved/entity/{request.entity_instance_ref.value}"
            )
        ),
        context_trace_ref=(
            context.trace_ref
            if context is not None
            else TraceRef(f"{matrix.trace_ref.value}/unresolved/context/{request.context_id.value}")
        ),
        matrix_trace_ref=matrix.trace_ref,
        capability_trace_ref=(
            capability_contract.trace_ref
            if capability_contract is not None
            else TraceRef(
                f"{matrix.trace_ref.value}/unresolved/capability/{request.capability_id.value}"
            )
        ),
        decision_stage=decision_stage,
    )


__all__ = [
    "CapabilityEvaluationEnvironment",
    "CapabilityEvaluationRequest",
    "CapabilityEvaluationResult",
    "CapabilityEvaluationState",
    "CapabilityEvaluationTrace",
    "EntityInstanceContract",
    "EvaluationContextContract",
    "evaluate_capability",
]
