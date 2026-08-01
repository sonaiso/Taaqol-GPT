"""USM structural validator (USM-C2 bounded validation surface only)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.usm.identifiers import (
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)
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
        require_tuple_of_type(
            "USMValidationResult", "failure_codes", self.failure_codes, USMFailureCode
        )
        require_tuple_of_type("USMValidationResult", "residuals", self.residuals, USMResidual)
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
    }
)


def validate_usm_matrix(
    matrix: UniversalScienceMatrix,
    *,
    declared_bridges: tuple[tuple[ScienceId, ScienceId], ...] = (),
) -> USMValidationResult:
    failure_codes: list[USMFailureCode] = []
    residuals = list(matrix.residuals)

    if not isinstance(matrix, UniversalScienceMatrix):
        raise USMSchemaError("validate_usm_matrix requires UniversalScienceMatrix")
    require_tuple_of_type("validate_usm_matrix", "declared_bridges", declared_bridges, tuple)
    for bridge in declared_bridges:
        if len(bridge) != 2:
            raise USMSchemaError("each declared bridge must be pair[ScienceId, ScienceId]")
        if not isinstance(bridge[0], ScienceId) or not isinstance(bridge[1], ScienceId):
            raise USMSchemaError("bridge entries must be ScienceId")

    if _has_duplicates(matrix):
        failure_codes.append(USMFailureCode.DUPLICATE_IDENTIFIER)

    if any(not residual.visible for residual in matrix.residuals):
        failure_codes.append(USMFailureCode.HIDDEN_RESIDUAL)

    entity_ids = {contract.entity_type_id for contract in matrix.entities}
    capability_ids = {contract.capability_id for contract in matrix.capabilities}
    relation_ids = {contract.relation_type_id for contract in matrix.relations}
    evidence_ids = {contract.evidence_type_id for contract in matrix.evidence}
    judgment_ids = {contract.judgment_type_id for contract in matrix.judgments}
    knowledge_object_ids = {
        contract.knowledge_object_type_id for contract in matrix.knowledge_objects
    }
    declared_claim_types = {
        claim
        for evidence_contract in matrix.evidence
        for claim in evidence_contract.supported_claim_types
    } | {
        claim
        for judgment_contract in matrix.judgments
        for claim in judgment_contract.supported_claim_types
    }

    for capability in matrix.capabilities:
        if capability.bearer_type not in entity_ids:
            failure_codes.append(USMFailureCode.UNKNOWN_CAPABILITY_BEARER)

    for relation in matrix.relations:
        if any(operand not in entity_ids for operand in relation.operand_types):
            failure_codes.append(USMFailureCode.UNKNOWN_RELATION_OPERAND)

    for transformation in matrix.transformations:
        if any(source not in entity_ids for source in transformation.source_types):
            failure_codes.append(USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE)
        if any(target not in entity_ids for target in transformation.target_types):
            failure_codes.append(USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE)
        if any(
            capability_id not in capability_ids
            for capability_id in transformation.required_capabilities
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE)

    for evidence_contract in matrix.evidence:
        if any(
            claim_type not in declared_claim_types
            for claim_type in evidence_contract.supported_claim_types
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_EVIDENCE_CLAIM_TYPE)

    for judgment in matrix.judgments:
        if any(
            evidence_type not in evidence_ids
            for evidence_type in judgment.required_evidence_types
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_JUDGMENT_EVIDENCE_TYPE)

    for knowledge_object in matrix.knowledge_objects:
        if any(subject not in entity_ids for subject in knowledge_object.subject_types):
            failure_codes.append(USMFailureCode.UNKNOWN_KNOWLEDGE_OBJECT_REFERENCE)
        if any(relation not in relation_ids for relation in knowledge_object.relation_types):
            failure_codes.append(USMFailureCode.UNKNOWN_KNOWLEDGE_OBJECT_REFERENCE)
        if any(judgment not in judgment_ids for judgment in knowledge_object.required_judgments):
            failure_codes.append(USMFailureCode.UNKNOWN_KNOWLEDGE_OBJECT_REFERENCE)

    for application in matrix.applications:
        if any(
            knowledge_object not in knowledge_object_ids
            for knowledge_object in application.knowledge_object_types
        ):
            failure_codes.append(USMFailureCode.UNKNOWN_APPLICATION_REFERENCE)
        if any(case_type not in entity_ids for case_type in application.case_entity_types):
            failure_codes.append(USMFailureCode.UNKNOWN_APPLICATION_REFERENCE)

    all_contracts = (
        matrix.entities
        + matrix.capabilities
        + matrix.relations
        + matrix.transformations
        + matrix.evidence
        + matrix.judgments
        + matrix.knowledge_objects
        + matrix.applications
    )
    for contract in all_contracts:
        if contract.science_id != matrix.science_id and not _bridge_exists(
            matrix.science_id, contract.science_id, declared_bridges
        ):
            failure_codes.append(USMFailureCode.CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE)

    failure_codes = sorted(set(failure_codes), key=lambda item: item.value)
    state = _resolve_state(failure_codes, tuple(residuals))
    return USMValidationResult(
        state=state,
        failure_codes=tuple(failure_codes),
        residuals=tuple(residuals),
        trace_ref=matrix.trace_ref,
    )


def _has_duplicates(matrix: UniversalScienceMatrix) -> bool:
    slots = (
        tuple(contract.entity_type_id.value for contract in matrix.entities),
        tuple(contract.capability_id.value for contract in matrix.capabilities),
        tuple(contract.relation_type_id.value for contract in matrix.relations),
        tuple(contract.transformation_type_id.value for contract in matrix.transformations),
        tuple(contract.evidence_type_id.value for contract in matrix.evidence),
        tuple(contract.judgment_type_id.value for contract in matrix.judgments),
        tuple(contract.knowledge_object_type_id.value for contract in matrix.knowledge_objects),
        tuple(contract.application_type_id.value for contract in matrix.applications),
    )
    return any(len(slot) != len(set(slot)) for slot in slots)


def _bridge_exists(
    left: ScienceId, right: ScienceId, bridges: tuple[tuple[ScienceId, ScienceId], ...]
) -> bool:
    return any(
        (left == source and right == target) or (left == target and right == source)
        for source, target in bridges
    )


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
    if any(
        residual.kind
        in {
            USMResidualKind.COVERAGE_GAP,
            USMResidualKind.IRREDUCIBILITY_UNPROVEN,
            USMResidualKind.KNOWLEDGE_REVISION_DEFERRED,
            USMResidualKind.APPLICATION_SCOPE_UNRESOLVED,
        }
        for residual in residuals
    ):
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
