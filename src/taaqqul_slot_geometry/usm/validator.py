"""USM structural validator (USM-C2/C2.1 bounded validation surface only)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.usm.bridge_contract import (
    BridgeDirection,
    ScienceBridgeContract,
    TypedUSMReference,
    USMReferenceSlot,
)
from taaqqul_slot_geometry.usm.identifiers import ClaimTypeId, ScienceId, TraceRef, USMSchemaError
from taaqqul_slot_geometry.usm.matrix import UniversalScienceMatrix
from taaqqul_slot_geometry.usm.residuals import USMResidual, USMResidualKind


class USMFailureCode(StrEnum):
    SCHEMA_INVALID = "SCHEMA_INVALID"
    DUPLICATE_IDENTIFIER = "DUPLICATE_IDENTIFIER"
    UNKNOWN_CAPABILITY_BEARER = "UNKNOWN_CAPABILITY_BEARER"
    UNKNOWN_RELATION_OPERAND = "UNKNOWN_RELATION_OPERAND"
    UNKNOWN_TRANSFORMATION_REFERENCE = "UNKNOWN_TRANSFORMATION_REFERENCE"
    UNKNOWN_EVIDENCE_CLAIM_TYPE = "UNKNOWN_EVIDENCE_CLAIM_TYPE"
    UNKNOWN_JUDGMENT_EVIDENCE_TYPE = "UNKNOWN_JUDGMENT_EVIDENCE_TYPE"
    UNKNOWN_KNOWLEDGE_OBJECT_REFERENCE = "UNKNOWN_KNOWLEDGE_OBJECT_REFERENCE"
    UNKNOWN_APPLICATION_REFERENCE = "UNKNOWN_APPLICATION_REFERENCE"
    CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE = "CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE"
    HIDDEN_RESIDUAL = "HIDDEN_RESIDUAL"
    CLAIM_TYPE_ID_MISSING = "CLAIM_TYPE_ID_MISSING"
    CLAIM_TYPE_REFERENCE_UNRESOLVED = "CLAIM_TYPE_REFERENCE_UNRESOLVED"
    CLAIM_TYPE_RULE_ID_CONFUSION = "CLAIM_TYPE_RULE_ID_CONFUSION"
    EVIDENCE_CLAIM_TYPE_MISMATCH = "EVIDENCE_CLAIM_TYPE_MISMATCH"
    BRIDGE_DIRECTION_MISSING = "BRIDGE_DIRECTION_MISSING"
    BRIDGE_SOURCE_REFERENCE_UNRESOLVED = "BRIDGE_SOURCE_REFERENCE_UNRESOLVED"
    BRIDGE_TARGET_REFERENCE_UNRESOLVED = "BRIDGE_TARGET_REFERENCE_UNRESOLVED"
    BRIDGE_IMPLICIT_EVIDENCE_TRANSFER = "BRIDGE_IMPLICIT_EVIDENCE_TRANSFER"
    BRIDGE_RANK_CEILING_VIOLATION = "BRIDGE_RANK_CEILING_VIOLATION"
    REFERENCE_MATRIX_EXPECTED_STATE_MISMATCH = "REFERENCE_MATRIX_EXPECTED_STATE_MISMATCH"
    REFERENCE_MATRIX_EMPTY_ENTITIES_SLOT = "REFERENCE_MATRIX_EMPTY_ENTITIES_SLOT"
    REFERENCE_MATRIX_EMPTY_CAPABILITIES_SLOT = "REFERENCE_MATRIX_EMPTY_CAPABILITIES_SLOT"
    REFERENCE_MATRIX_EMPTY_RELATIONS_SLOT = "REFERENCE_MATRIX_EMPTY_RELATIONS_SLOT"
    REFERENCE_MATRIX_EMPTY_TRANSFORMATIONS_SLOT = "REFERENCE_MATRIX_EMPTY_TRANSFORMATIONS_SLOT"
    REFERENCE_MATRIX_EMPTY_EVIDENCE_SLOT = "REFERENCE_MATRIX_EMPTY_EVIDENCE_SLOT"
    REFERENCE_MATRIX_EMPTY_JUDGMENTS_SLOT = "REFERENCE_MATRIX_EMPTY_JUDGMENTS_SLOT"
    REFERENCE_MATRIX_EMPTY_KNOWLEDGE_OBJECTS_SLOT = "REFERENCE_MATRIX_EMPTY_KNOWLEDGE_OBJECTS_SLOT"
    REFERENCE_MATRIX_EMPTY_APPLICATIONS_SLOT = "REFERENCE_MATRIX_EMPTY_APPLICATIONS_SLOT"
    REFERENCE_MATRIX_FOREIGN_SCIENCE_ID = "REFERENCE_MATRIX_FOREIGN_SCIENCE_ID"
    REFERENCE_MATRIX_DUPLICATE_IDENTIFIER = "REFERENCE_MATRIX_DUPLICATE_IDENTIFIER"
    REFERENCE_MATRIX_UNRESOLVED_REFERENCE = "REFERENCE_MATRIX_UNRESOLVED_REFERENCE"
    CAPABILITY_ID_UNRESOLVED = "CAPABILITY_ID_UNRESOLVED"
    ENTITY_TYPE_UNRESOLVED = "ENTITY_TYPE_UNRESOLVED"
    CAPABILITY_SCIENCE_MISMATCH = "CAPABILITY_SCIENCE_MISMATCH"
    CAPABILITY_BEARER_TYPE_MISMATCH = "CAPABILITY_BEARER_TYPE_MISMATCH"
    CAPABILITY_CONDITION_MISSING = "CAPABILITY_CONDITION_MISSING"
    CAPABILITY_BLOCKER_ACTIVE = "CAPABILITY_BLOCKER_ACTIVE"
    CAPABILITY_EVIDENCE_TYPE_MISSING = "CAPABILITY_EVIDENCE_TYPE_MISSING"
    CAPABILITY_RANK_CEILING_EXCEEDED = "CAPABILITY_RANK_CEILING_EXCEEDED"
    CAPABILITY_BLOCKING_RESIDUAL = "CAPABILITY_BLOCKING_RESIDUAL"
    CAPABILITY_CROSS_SCIENCE_REFERENCE = "CAPABILITY_CROSS_SCIENCE_REFERENCE"
    CAPABILITY_CONTEXT_UNRESOLVED = "CAPABILITY_CONTEXT_UNRESOLVED"
    CAPABILITY_TRACE_MISSING = "CAPABILITY_TRACE_MISSING"
    CAPABILITY_ENTITY_INSTANCE_UNRESOLVED = "CAPABILITY_ENTITY_INSTANCE_UNRESOLVED"
    CAPABILITY_ENTITY_INSTANCE_TYPE_MISMATCH = "CAPABILITY_ENTITY_INSTANCE_TYPE_MISMATCH"
    CAPABILITY_CONTEXT_SCIENCE_MISMATCH = "CAPABILITY_CONTEXT_SCIENCE_MISMATCH"
    CAPABILITY_CONTEXT_MATRIX_MISMATCH = "CAPABILITY_CONTEXT_MATRIX_MISMATCH"
    CAPABILITY_TRACE_CHAIN_BROKEN = "CAPABILITY_TRACE_CHAIN_BROKEN"
    CAPABILITY_ENTITY_RANK_CEILING_EXCEEDED = "CAPABILITY_ENTITY_RANK_CEILING_EXCEEDED"
    CAPABILITY_EVIDENCE_TYPE_UNRESOLVED = "CAPABILITY_EVIDENCE_TYPE_UNRESOLVED"
    CAPABILITY_EVIDENCE_TYPE_NOT_SUPPLIED = "CAPABILITY_EVIDENCE_TYPE_NOT_SUPPLIED"
    CAPABILITY_RESULT_INVARIANT_VIOLATION = "CAPABILITY_RESULT_INVARIANT_VIOLATION"
    CAPABILITY_MATRIX_ID_MISMATCH = "CAPABILITY_MATRIX_ID_MISMATCH"
    RELATION_TYPE_UNRESOLVED = "RELATION_TYPE_UNRESOLVED"
    RELATION_SCIENCE_MISMATCH = "RELATION_SCIENCE_MISMATCH"
    RELATION_MATRIX_MISMATCH = "RELATION_MATRIX_MISMATCH"
    RELATION_ARITY_MISMATCH = "RELATION_ARITY_MISMATCH"
    RELATION_ROLE_UNRESOLVED = "RELATION_ROLE_UNRESOLVED"
    RELATION_ROLE_DUPLICATED = "RELATION_ROLE_DUPLICATED"
    RELATION_POSITION_DUPLICATED = "RELATION_POSITION_DUPLICATED"
    RELATION_OPERAND_UNRESOLVED = "RELATION_OPERAND_UNRESOLVED"
    RELATION_OPERAND_TYPE_MISMATCH = "RELATION_OPERAND_TYPE_MISMATCH"
    RELATION_DIRECTION_MISMATCH = "RELATION_DIRECTION_MISMATCH"
    RELATION_REQUIRED_CAPABILITY_MISSING = "RELATION_REQUIRED_CAPABILITY_MISSING"
    RELATION_CAPABILITY_RESULT_UNRESOLVED = "RELATION_CAPABILITY_RESULT_UNRESOLVED"
    RELATION_CAPABILITY_PROVENANCE_MISMATCH = "RELATION_CAPABILITY_PROVENANCE_MISMATCH"
    RELATION_CAPABILITY_NOT_ELIGIBLE = "RELATION_CAPABILITY_NOT_ELIGIBLE"
    RELATION_REQUIRED_CONDITION_MISSING = "RELATION_REQUIRED_CONDITION_MISSING"
    RELATION_BLOCKER_ACTIVE = "RELATION_BLOCKER_ACTIVE"
    RELATION_STRUCTURAL_SATURATION_INCOMPLETE = "RELATION_STRUCTURAL_SATURATION_INCOMPLETE"
    RELATION_BLOCKING_RESIDUAL = "RELATION_BLOCKING_RESIDUAL"
    RELATION_TRACE_CHAIN_BROKEN = "RELATION_TRACE_CHAIN_BROKEN"
    RELATION_RANK_CEILING_EXCEEDED = "RELATION_RANK_CEILING_EXCEEDED"
    TRANSFORMATION_TYPE_UNRESOLVED = "TRANSFORMATION_TYPE_UNRESOLVED"
    TRANSFORMATION_SCIENCE_MISMATCH = "TRANSFORMATION_SCIENCE_MISMATCH"
    TRANSFORMATION_MATRIX_MISMATCH = "TRANSFORMATION_MATRIX_MISMATCH"
    TRANSFORMATION_RELATION_REQUEST_UNRESOLVED = "TRANSFORMATION_RELATION_REQUEST_UNRESOLVED"
    TRANSFORMATION_RELATION_RESULT_UNRESOLVED = "TRANSFORMATION_RELATION_RESULT_UNRESOLVED"
    TRANSFORMATION_RELATION_NOT_ELIGIBLE = "TRANSFORMATION_RELATION_NOT_ELIGIBLE"
    TRANSFORMATION_RELATION_PROVENANCE_MISMATCH = "TRANSFORMATION_RELATION_PROVENANCE_MISMATCH"
    TRANSFORMATION_SOURCE_ARITY_MISMATCH = "TRANSFORMATION_SOURCE_ARITY_MISMATCH"
    TRANSFORMATION_SOURCE_ENTITY_UNRESOLVED = "TRANSFORMATION_SOURCE_ENTITY_UNRESOLVED"
    TRANSFORMATION_SOURCE_TYPE_MISMATCH = "TRANSFORMATION_SOURCE_TYPE_MISMATCH"
    TRANSFORMATION_CAPABILITY_RESULT_UNRESOLVED = "TRANSFORMATION_CAPABILITY_RESULT_UNRESOLVED"
    TRANSFORMATION_CAPABILITY_NOT_ELIGIBLE = "TRANSFORMATION_CAPABILITY_NOT_ELIGIBLE"
    TRANSFORMATION_REQUIRED_CAPABILITY_MISSING = "TRANSFORMATION_REQUIRED_CAPABILITY_MISSING"
    TRANSFORMATION_REQUIRED_CONDITION_MISSING = "TRANSFORMATION_REQUIRED_CONDITION_MISSING"
    TRANSFORMATION_BLOCKER_ACTIVE = "TRANSFORMATION_BLOCKER_ACTIVE"
    TRANSFORMATION_EVIDENCE_REQUIREMENT_MISSING = "TRANSFORMATION_EVIDENCE_REQUIREMENT_MISSING"
    TRANSFORMATION_BLOCKING_RESIDUAL = "TRANSFORMATION_BLOCKING_RESIDUAL"
    TRANSFORMATION_TRACE_CHAIN_BROKEN = "TRANSFORMATION_TRACE_CHAIN_BROKEN"
    TRANSFORMATION_RANK_CEILING_EXCEEDED = "TRANSFORMATION_RANK_CEILING_EXCEEDED"
    TRANSFORMATION_LINK_RESULT_UNRESOLVED = "TRANSFORMATION_LINK_RESULT_UNRESOLVED"
    TRANSFORMATION_LINK_NOT_ELIGIBLE = "TRANSFORMATION_LINK_NOT_ELIGIBLE"
    TRANSFORMATION_PROPOSAL_TRACE_CHAIN_BROKEN = "TRANSFORMATION_PROPOSAL_TRACE_CHAIN_BROKEN"


class USMValidationState(StrEnum):
    VALID = "VALID"
    VALID_WITH_RESIDUALS = "VALID_WITH_RESIDUALS"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class USMValidationResult:
    state: USMValidationState
    failure_codes: tuple[USMFailureCode, ...]
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.state, USMValidationState):
            raise USMSchemaError("USMValidationResult.state must be USMValidationState")
        if not isinstance(self.failure_codes, tuple) or not all(
            isinstance(code, USMFailureCode) for code in self.failure_codes
        ):
            raise USMSchemaError("USMValidationResult.failure_codes must be tuple[USMFailureCode]")
        if not isinstance(self.residuals, tuple) or not all(
            isinstance(residual, USMResidual) for residual in self.residuals
        ):
            raise USMSchemaError("USMValidationResult.residuals must be tuple[USMResidual]")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("USMValidationResult.trace_ref must be TraceRef")


_BLOCKING_FAILURES: frozenset[USMFailureCode] = frozenset(
    {
        USMFailureCode.UNKNOWN_CAPABILITY_BEARER,
        USMFailureCode.UNKNOWN_RELATION_OPERAND,
        USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE,
        USMFailureCode.UNKNOWN_JUDGMENT_EVIDENCE_TYPE,
        USMFailureCode.UNKNOWN_APPLICATION_REFERENCE,
        USMFailureCode.CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE,
        USMFailureCode.HIDDEN_RESIDUAL,
        USMFailureCode.CLAIM_TYPE_ID_MISSING,
        USMFailureCode.CLAIM_TYPE_REFERENCE_UNRESOLVED,
        USMFailureCode.EVIDENCE_CLAIM_TYPE_MISMATCH,
        USMFailureCode.BRIDGE_DIRECTION_MISSING,
        USMFailureCode.BRIDGE_SOURCE_REFERENCE_UNRESOLVED,
        USMFailureCode.BRIDGE_TARGET_REFERENCE_UNRESOLVED,
        USMFailureCode.BRIDGE_IMPLICIT_EVIDENCE_TRANSFER,
        USMFailureCode.BRIDGE_RANK_CEILING_VIOLATION,
        USMFailureCode.REFERENCE_MATRIX_FOREIGN_SCIENCE_ID,
        USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE,
        USMFailureCode.REFERENCE_MATRIX_EMPTY_ENTITIES_SLOT,
        USMFailureCode.REFERENCE_MATRIX_EMPTY_CAPABILITIES_SLOT,
        USMFailureCode.REFERENCE_MATRIX_EMPTY_RELATIONS_SLOT,
        USMFailureCode.REFERENCE_MATRIX_EMPTY_TRANSFORMATIONS_SLOT,
        USMFailureCode.REFERENCE_MATRIX_EMPTY_EVIDENCE_SLOT,
        USMFailureCode.REFERENCE_MATRIX_EMPTY_JUDGMENTS_SLOT,
        USMFailureCode.REFERENCE_MATRIX_EMPTY_KNOWLEDGE_OBJECTS_SLOT,
        USMFailureCode.REFERENCE_MATRIX_EMPTY_APPLICATIONS_SLOT,
    }
)


def validate_usm_matrix(
    matrix: UniversalScienceMatrix,
    *,
    expected_state: USMValidationState | None = None,
) -> USMValidationResult:
    if not isinstance(matrix, UniversalScienceMatrix):
        raise USMSchemaError("validate_usm_matrix requires UniversalScienceMatrix")

    failure_codes: list[USMFailureCode] = []
    residuals = list(matrix.residuals)

    if _has_duplicates(matrix):
        failure_codes.append(USMFailureCode.DUPLICATE_IDENTIFIER)
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_DUPLICATE_IDENTIFIER)

    if any(not residual.visible for residual in matrix.residuals):
        failure_codes.append(USMFailureCode.HIDDEN_RESIDUAL)

    _check_required_slot_presence(matrix, failure_codes)

    entity_ids = {contract.entity_type_id for contract in matrix.entities}
    capability_ids = {contract.capability_id for contract in matrix.capabilities}
    relation_ids = {contract.relation_type_id for contract in matrix.relations}
    evidence_ids = {contract.evidence_type_id for contract in matrix.evidence}
    claim_type_ids = {contract.claim_type_id for contract in matrix.claim_types}
    judgment_ids = {contract.judgment_type_id for contract in matrix.judgments}
    knowledge_object_ids = {
        contract.knowledge_object_type_id for contract in matrix.knowledge_objects
    }

    for contract in (
        matrix.entities
        + matrix.capabilities
        + matrix.relations
        + matrix.transformations
        + matrix.evidence
        + matrix.claim_types
        + matrix.judgments
        + matrix.knowledge_objects
        + matrix.applications
    ):
        if contract.science_id != matrix.science_id:
            if not _bridge_exists(matrix, contract.science_id):
                failure_codes.append(USMFailureCode.CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_FOREIGN_SCIENCE_ID)

    for capability in matrix.capabilities:
        if capability.bearer_type not in entity_ids:
            failure_codes.append(USMFailureCode.UNKNOWN_CAPABILITY_BEARER)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)

    for relation in matrix.relations:
        if any(operand not in entity_ids for operand in relation.operand_types):
            failure_codes.append(USMFailureCode.UNKNOWN_RELATION_OPERAND)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)

    for transformation in matrix.transformations:
        if any(source not in entity_ids for source in transformation.source_types):
            failure_codes.append(USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(target not in entity_ids for target in transformation.target_types):
            failure_codes.append(USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(
            capability_id not in capability_ids
            for capability_id in transformation.required_capabilities
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(
            evidence_id not in evidence_ids for evidence_id in transformation.evidence_requirements
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)

    if not matrix.claim_types:
        failure_codes.append(USMFailureCode.CLAIM_TYPE_ID_MISSING)

    for claim_type in matrix.claim_types:
        if any(subject not in entity_ids for subject in claim_type.subject_type_refs):
            failure_codes.append(USMFailureCode.CLAIM_TYPE_REFERENCE_UNRESOLVED)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(
            predicate not in entity_ids for predicate in claim_type.predicate_or_result_type_refs
        ):
            failure_codes.append(USMFailureCode.CLAIM_TYPE_REFERENCE_UNRESOLVED)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(relation not in relation_ids for relation in claim_type.relation_type_refs):
            failure_codes.append(USMFailureCode.CLAIM_TYPE_REFERENCE_UNRESOLVED)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(
            evidence_id not in evidence_ids
            for evidence_id in claim_type.admissible_evidence_type_refs
        ):
            failure_codes.append(USMFailureCode.CLAIM_TYPE_REFERENCE_UNRESOLVED)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)

    for evidence_contract in matrix.evidence:
        if any(
            not isinstance(claim_type, ClaimTypeId)
            for claim_type in evidence_contract.supported_claim_types
        ):
            failure_codes.append(USMFailureCode.CLAIM_TYPE_RULE_ID_CONFUSION)
        if any(
            claim_type not in claim_type_ids
            for claim_type in evidence_contract.supported_claim_types
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_EVIDENCE_CLAIM_TYPE)
            failure_codes.append(USMFailureCode.EVIDENCE_CLAIM_TYPE_MISMATCH)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)

    for judgment in matrix.judgments:
        if any(
            not isinstance(claim_type, ClaimTypeId) for claim_type in judgment.supported_claim_types
        ):
            failure_codes.append(USMFailureCode.CLAIM_TYPE_RULE_ID_CONFUSION)
        if any(claim_type not in claim_type_ids for claim_type in judgment.supported_claim_types):
            failure_codes.append(USMFailureCode.CLAIM_TYPE_REFERENCE_UNRESOLVED)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(
            evidence_type not in evidence_ids for evidence_type in judgment.required_evidence_types
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_JUDGMENT_EVIDENCE_TYPE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)

    for knowledge_object in matrix.knowledge_objects:
        if any(subject not in entity_ids for subject in knowledge_object.subject_types):
            failure_codes.append(USMFailureCode.UNKNOWN_KNOWLEDGE_OBJECT_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(relation not in relation_ids for relation in knowledge_object.relation_types):
            failure_codes.append(USMFailureCode.UNKNOWN_KNOWLEDGE_OBJECT_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(judgment not in judgment_ids for judgment in knowledge_object.required_judgments):
            failure_codes.append(USMFailureCode.UNKNOWN_KNOWLEDGE_OBJECT_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)

    for application in matrix.applications:
        if any(
            knowledge_object not in knowledge_object_ids
            for knowledge_object in application.knowledge_object_types
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_APPLICATION_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)
        if any(case_type not in entity_ids for case_type in application.case_entity_types):
            failure_codes.append(USMFailureCode.UNKNOWN_APPLICATION_REFERENCE)
            failure_codes.append(USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE)

    for bridge in matrix.bridges:
        _validate_bridge_contract(
            matrix=matrix,
            bridge=bridge,
            failure_codes=failure_codes,
        )

    failure_codes = sorted(set(failure_codes), key=lambda item: item.value)
    state = _resolve_state(tuple(failure_codes), tuple(residuals))
    if expected_state is not None and state is not expected_state:
        failure_codes = sorted(
            set(failure_codes + [USMFailureCode.REFERENCE_MATRIX_EXPECTED_STATE_MISMATCH]),
            key=lambda item: item.value,
        )
        state = USMValidationState.INVALID
    return USMValidationResult(
        state=state,
        failure_codes=tuple(failure_codes),
        residuals=tuple(residuals),
        trace_ref=matrix.trace_ref,
    )


def _check_required_slot_presence(
    matrix: UniversalScienceMatrix, failure_codes: list[USMFailureCode]
) -> None:
    if len(matrix.entities) == 0:
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_EMPTY_ENTITIES_SLOT)
    if len(matrix.capabilities) == 0:
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_EMPTY_CAPABILITIES_SLOT)
    if len(matrix.relations) == 0:
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_EMPTY_RELATIONS_SLOT)
    if len(matrix.transformations) == 0:
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_EMPTY_TRANSFORMATIONS_SLOT)
    if len(matrix.evidence) == 0:
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_EMPTY_EVIDENCE_SLOT)
    if len(matrix.judgments) == 0:
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_EMPTY_JUDGMENTS_SLOT)
    if len(matrix.knowledge_objects) == 0:
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_EMPTY_KNOWLEDGE_OBJECTS_SLOT)
    if len(matrix.applications) == 0:
        failure_codes.append(USMFailureCode.REFERENCE_MATRIX_EMPTY_APPLICATIONS_SLOT)


def _reference_exists(matrix: UniversalScienceMatrix, reference: TypedUSMReference) -> bool:
    if reference.science_id != matrix.science_id:
        return False
    resolved_by_slot: dict[USMReferenceSlot, set[str]] = {
        USMReferenceSlot.ENTITY: {entry.entity_type_id.value for entry in matrix.entities},
        USMReferenceSlot.CAPABILITY: {entry.capability_id.value for entry in matrix.capabilities},
        USMReferenceSlot.RELATION: {entry.relation_type_id.value for entry in matrix.relations},
        USMReferenceSlot.TRANSFORMATION: {
            entry.transformation_type_id.value for entry in matrix.transformations
        },
        USMReferenceSlot.EVIDENCE: {entry.evidence_type_id.value for entry in matrix.evidence},
        USMReferenceSlot.CLAIM_TYPE: {entry.claim_type_id.value for entry in matrix.claim_types},
        USMReferenceSlot.JUDGMENT: {entry.judgment_type_id.value for entry in matrix.judgments},
        USMReferenceSlot.KNOWLEDGE_OBJECT: {
            entry.knowledge_object_type_id.value for entry in matrix.knowledge_objects
        },
        USMReferenceSlot.APPLICATION: {
            entry.application_type_id.value for entry in matrix.applications
        },
    }
    return reference.local_identifier in resolved_by_slot[reference.slot]


def _validate_bridge_contract(
    *,
    matrix: UniversalScienceMatrix,
    bridge: ScienceBridgeContract,
    failure_codes: list[USMFailureCode],
) -> None:
    if not isinstance(bridge.direction, BridgeDirection):
        failure_codes.append(USMFailureCode.BRIDGE_DIRECTION_MISSING)
    if bridge.source_science_id == bridge.target_science_id:
        failure_codes.append(USMFailureCode.CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE)

    if not _reference_exists(matrix, bridge.source_type_ref):
        failure_codes.append(USMFailureCode.BRIDGE_SOURCE_REFERENCE_UNRESOLVED)

    if not _reference_exists(matrix, bridge.target_type_ref):
        failure_codes.append(USMFailureCode.BRIDGE_TARGET_REFERENCE_UNRESOLVED)

    source_rank_ceiling = _max_rank_for_science(matrix)
    if bridge.rank_ceiling > source_rank_ceiling:
        failure_codes.append(USMFailureCode.BRIDGE_RANK_CEILING_VIOLATION)

    local_evidence_ids = {item.evidence_type_id for item in matrix.evidence}
    if any(
        evidence_type not in local_evidence_ids for evidence_type in bridge.required_evidence_types
    ):
        failure_codes.append(USMFailureCode.BRIDGE_IMPLICIT_EVIDENCE_TRANSFER)


def _max_rank_for_science(matrix: UniversalScienceMatrix) -> int:
    local_rank_values = (
        [contract.rank_ceiling for contract in matrix.capabilities]
        + [contract.rank_ceiling for contract in matrix.transformations]
        + [contract.local_rank_ceiling for contract in matrix.claim_types]
        + [contract.global_rank_ceiling for contract in matrix.evidence]
        + [contract.global_rank_ceiling for contract in matrix.judgments]
    )
    if not local_rank_values:
        return 0
    return max(local_rank_values)


def _has_duplicates(matrix: UniversalScienceMatrix) -> bool:
    slots = (
        tuple(contract.entity_type_id.value for contract in matrix.entities),
        tuple(contract.capability_id.value for contract in matrix.capabilities),
        tuple(contract.relation_type_id.value for contract in matrix.relations),
        tuple(contract.transformation_type_id.value for contract in matrix.transformations),
        tuple(contract.evidence_type_id.value for contract in matrix.evidence),
        tuple(contract.claim_type_id.value for contract in matrix.claim_types),
        tuple(contract.judgment_type_id.value for contract in matrix.judgments),
        tuple(contract.knowledge_object_type_id.value for contract in matrix.knowledge_objects),
        tuple(contract.application_type_id.value for contract in matrix.applications),
        tuple(contract.bridge_id.value for contract in matrix.bridges),
    )
    return any(len(slot) != len(set(slot)) for slot in slots)


def _bridge_exists(matrix: UniversalScienceMatrix, foreign_science_id: ScienceId) -> bool:
    for bridge in matrix.bridges:
        inbound_source_to_target = (
            bridge.direction is BridgeDirection.SOURCE_TO_TARGET
            and bridge.source_science_id == foreign_science_id
            and bridge.target_science_id == matrix.science_id
        )
        inbound_target_to_source = (
            bridge.direction is BridgeDirection.TARGET_TO_SOURCE
            and bridge.source_science_id == matrix.science_id
            and bridge.target_science_id == foreign_science_id
        )
        if inbound_source_to_target or inbound_target_to_source:
            return True
    return False


def _resolve_state(
    failure_codes: tuple[USMFailureCode, ...], residuals: tuple[USMResidual, ...]
) -> USMValidationState:
    if failure_codes:
        if any(code in _BLOCKING_FAILURES for code in failure_codes):
            return USMValidationState.BLOCKED
        return USMValidationState.INVALID
    if not residuals:
        return USMValidationState.VALID
    if any(residual.blocking for residual in residuals):
        return USMValidationState.BLOCKED
    if any(residual.kind is USMResidualKind.KNOWLEDGE_REVISION_DEFERRED for residual in residuals):
        return USMValidationState.DEFERRED
    return USMValidationState.VALID_WITH_RESIDUALS


_IRREDUCIBILITY_LOSS_MAP: dict[str, str] = {
    "entities": "no subject identity",
    "capabilities": "possible and forbidden operations become indistinguishable",
    "relations": "entities cannot form structured claims",
    "transformations": "no licensed change or derivation",
    "evidence": "supported and unsupported claims collapse",
    "judgments": "no epistemic rank assignment",
    "knowledge_objects": "no organized reusable knowledge",
    "applications": "no transfer to new cases or feedback",
}


def initial_functional_irreducibility_evidence(
    matrix: UniversalScienceMatrix,
) -> dict[str, str]:
    report: dict[str, str] = {}
    for slot_name, loss_message in _IRREDUCIBILITY_LOSS_MAP.items():
        slot_value = getattr(matrix, slot_name)
        if len(slot_value) == 0:
            report[slot_name] = loss_message
    return report


__all__ = [
    "USMFailureCode",
    "USMValidationResult",
    "USMValidationState",
    "initial_functional_irreducibility_evidence",
    "validate_usm_matrix",
]
