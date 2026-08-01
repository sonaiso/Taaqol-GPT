"""USM-C3 bounded capability evaluator runtime (pure, deterministic, non-executive)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core import Rank
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
            raise USMSchemaError(
                "CapabilityEvaluationRequest.entity_type_id must be EntityTypeId"
            )
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
    evidence_type_refs: tuple[EvidenceTypeId, ...]
    failure_codes: tuple[USMFailureCode, ...]
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef

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
            "evidence_type_refs",
            self.evidence_type_refs,
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


def evaluate_capability(
    matrix: UniversalScienceMatrix,
    request: CapabilityEvaluationRequest,
) -> CapabilityEvaluationResult:
    """Evaluate only structural capability eligibility; never executes relation/transform."""

    if request.trace_ref.value != request.trace_ref.value.strip():
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.INVALID,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_TRACE_MISSING,),
        )

    if not request.context_id.value.startswith("context://"):
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.DEFERRED,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_CONTEXT_UNRESOLVED,),
        )

    if not request.entity_instance_ref.value.startswith("entity://"):
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.DEFERRED,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_CONTEXT_UNRESOLVED,),
        )

    if request.matrix_id != matrix.matrix_id:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.INVALID,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_ID_UNRESOLVED,),
        )

    if request.science_id != matrix.science_id:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.BLOCKED,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE,),
        )

    entity_contract = next(
        (entity for entity in matrix.entities if entity.entity_type_id == request.entity_type_id),
        None,
    )
    if entity_contract is None:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.INVALID,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.ENTITY_TYPE_UNRESOLVED,),
        )

    capability_contract = next(
        (
            capability
            for capability in matrix.capabilities
            if capability.capability_id == request.capability_id
        ),
        None,
    )
    if capability_contract is None:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.INVALID,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_ID_UNRESOLVED,),
        )

    if capability_contract.science_id != matrix.science_id:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.BLOCKED,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_SCIENCE_MISMATCH,),
        )

    if capability_contract.bearer_type != request.entity_type_id:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.BLOCKED,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_BEARER_TYPE_MISMATCH,),
        )

    if entity_contract.science_id != capability_contract.science_id:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.BLOCKED,
            granted_rank=Rank.ZERO,
            failure_codes=(USMFailureCode.CAPABILITY_CROSS_SCIENCE_REFERENCE,),
        )

    supplied_conditions = set(request.supplied_condition_refs)
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
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.DEFERRED,
            granted_rank=Rank.ZERO,
            satisfied_conditions=satisfied_conditions,
            missing_conditions=missing_conditions,
            failure_codes=(USMFailureCode.CAPABILITY_CONDITION_MISSING,),
        )

    active_requested_blockers = set(request.active_blocker_refs)
    active_blockers = tuple(
        blocker for blocker in capability_contract.blockers if blocker in active_requested_blockers
    )
    if active_blockers:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.BLOCKED,
            granted_rank=Rank.ZERO,
            satisfied_conditions=satisfied_conditions,
            active_blockers=active_blockers,
            failure_codes=(USMFailureCode.CAPABILITY_BLOCKER_ACTIVE,),
        )

    supplied_evidence = set(request.supplied_evidence_type_refs)
    matrix_evidence = {contract.evidence_type_id: contract for contract in matrix.evidence}
    missing_evidence = tuple(
        evidence
        for evidence in capability_contract.evidence_requirements
        if evidence not in supplied_evidence
    )
    unresolved_evidence = tuple(
        evidence
        for evidence in capability_contract.evidence_requirements
        if evidence not in matrix_evidence
    )
    if missing_evidence or unresolved_evidence:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.DEFERRED,
            granted_rank=Rank.ZERO,
            satisfied_conditions=satisfied_conditions,
            evidence_type_refs=request.supplied_evidence_type_refs,
            failure_codes=(USMFailureCode.CAPABILITY_EVIDENCE_TYPE_MISSING,),
        )

    evidence_ceiling = min(
        (
            matrix_evidence[evidence].global_rank_ceiling
            for evidence in capability_contract.evidence_requirements
        ),
        default=Rank.CERTIFICATE,
    )
    entity_state_ceiling = Rank.CANDIDATE
    granted_rank = min(
        request.requested_rank,
        capability_contract.rank_ceiling,
        evidence_ceiling,
        entity_state_ceiling,
    )
    if request.requested_rank > granted_rank:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.BLOCKED,
            granted_rank=granted_rank,
            satisfied_conditions=satisfied_conditions,
            evidence_type_refs=request.supplied_evidence_type_refs,
            failure_codes=(USMFailureCode.CAPABILITY_RANK_CEILING_EXCEEDED,),
        )

    combined_residuals = request.residuals + matrix.residuals
    blocking_residuals = tuple(residual for residual in combined_residuals if residual.blocking)
    if blocking_residuals:
        return _finalize(
            request=request,
            state=CapabilityEvaluationState.BLOCKED,
            granted_rank=granted_rank,
            satisfied_conditions=satisfied_conditions,
            evidence_type_refs=request.supplied_evidence_type_refs,
            failure_codes=(USMFailureCode.CAPABILITY_BLOCKING_RESIDUAL,),
            residuals=combined_residuals,
        )

    state = (
        CapabilityEvaluationState.ELIGIBLE_WITH_RESIDUALS
        if combined_residuals
        else CapabilityEvaluationState.ELIGIBLE
    )
    return _finalize(
        request=request,
        state=state,
        granted_rank=granted_rank,
        satisfied_conditions=satisfied_conditions,
        evidence_type_refs=request.supplied_evidence_type_refs,
        residuals=combined_residuals,
    )


def _finalize(
    *,
    request: CapabilityEvaluationRequest,
    state: CapabilityEvaluationState,
    granted_rank: Rank,
    satisfied_conditions: tuple[RuleId, ...] = (),
    missing_conditions: tuple[RuleId, ...] = (),
    active_blockers: tuple[RuleId, ...] = (),
    evidence_type_refs: tuple[EvidenceTypeId, ...] = (),
    failure_codes: tuple[USMFailureCode, ...] = (),
    residuals: tuple[USMResidual, ...] | None = None,
) -> CapabilityEvaluationResult:
    return CapabilityEvaluationResult(
        request_id=request.request_id,
        state=state,
        capability_id=request.capability_id,
        entity_type_id=request.entity_type_id,
        granted_rank=granted_rank,
        satisfied_conditions=satisfied_conditions,
        missing_conditions=missing_conditions,
        active_blockers=active_blockers,
        evidence_type_refs=evidence_type_refs,
        failure_codes=failure_codes,
        residuals=request.residuals if residuals is None else residuals,
        trace_ref=request.trace_ref,
    )


__all__ = [
    "CapabilityEvaluationRequest",
    "CapabilityEvaluationResult",
    "CapabilityEvaluationState",
    "evaluate_capability",
]
