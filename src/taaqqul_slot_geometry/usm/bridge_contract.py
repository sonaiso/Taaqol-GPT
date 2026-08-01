"""USM bridge contract carriers (USM-C2.1 structural-only, non-executable)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.usm.identifiers import (
    BridgeId,
    DomainId,
    EvidenceTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_non_empty_text,
    require_tuple_of_type,
)


class BridgeDirection(StrEnum):
    SOURCE_TO_TARGET = "SOURCE_TO_TARGET"
    TARGET_TO_SOURCE = "TARGET_TO_SOURCE"


class BridgeKind(StrEnum):
    TERMINOLOGY_MAPPING = "TERMINOLOGY_MAPPING"
    UNIT_CONVERSION = "UNIT_CONVERSION"
    REPRESENTATION_LOWERING = "REPRESENTATION_LOWERING"
    MODEL_CORRESPONDENCE = "MODEL_CORRESPONDENCE"
    EVIDENCE_IMPORT_PROPOSAL = "EVIDENCE_IMPORT_PROPOSAL"


class USMReferenceSlot(StrEnum):
    ENTITY = "ENTITY"
    CAPABILITY = "CAPABILITY"
    RELATION = "RELATION"
    TRANSFORMATION = "TRANSFORMATION"
    EVIDENCE = "EVIDENCE"
    CLAIM_TYPE = "CLAIM_TYPE"
    JUDGMENT = "JUDGMENT"
    KNOWLEDGE_OBJECT = "KNOWLEDGE_OBJECT"
    APPLICATION = "APPLICATION"


@dataclass(frozen=True, slots=True)
class TypedUSMReference:
    science_id: ScienceId
    slot: USMReferenceSlot
    local_identifier: str

    def __post_init__(self) -> None:
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("TypedUSMReference.science_id must be ScienceId")
        if not isinstance(self.slot, USMReferenceSlot):
            raise USMSchemaError("TypedUSMReference.slot must be USMReferenceSlot")
        require_non_empty_text("TypedUSMReference", "local_identifier", self.local_identifier)


@dataclass(frozen=True, slots=True)
class ScienceBridgeContract:
    bridge_id: BridgeId
    source_science_id: ScienceId
    target_science_id: ScienceId
    source_domain_id: DomainId
    target_domain_id: DomainId
    source_type_ref: TypedUSMReference
    target_type_ref: TypedUSMReference
    bridge_kind: BridgeKind
    direction: BridgeDirection
    preserved_invariants: tuple[RuleId, ...]
    declared_translation: tuple[RuleId, ...]
    required_evidence_types: tuple[EvidenceTypeId, ...]
    blockers: tuple[RuleId, ...]
    rank_ceiling: Rank
    residual_policy_ref: RuleId
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.bridge_id, BridgeId):
            raise USMSchemaError("ScienceBridgeContract.bridge_id must be BridgeId")
        if not isinstance(self.source_science_id, ScienceId):
            raise USMSchemaError("ScienceBridgeContract.source_science_id must be ScienceId")
        if not isinstance(self.target_science_id, ScienceId):
            raise USMSchemaError("ScienceBridgeContract.target_science_id must be ScienceId")
        if not isinstance(self.source_domain_id, DomainId):
            raise USMSchemaError("ScienceBridgeContract.source_domain_id must be DomainId")
        if not isinstance(self.target_domain_id, DomainId):
            raise USMSchemaError("ScienceBridgeContract.target_domain_id must be DomainId")
        if not isinstance(self.source_type_ref, TypedUSMReference):
            raise USMSchemaError("ScienceBridgeContract.source_type_ref must be TypedUSMReference")
        if not isinstance(self.target_type_ref, TypedUSMReference):
            raise USMSchemaError("ScienceBridgeContract.target_type_ref must be TypedUSMReference")
        if not isinstance(self.bridge_kind, BridgeKind):
            raise USMSchemaError("ScienceBridgeContract.bridge_kind must be BridgeKind")
        if not isinstance(self.direction, BridgeDirection):
            raise USMSchemaError("ScienceBridgeContract.direction must be BridgeDirection")
        if self.source_type_ref.science_id != self.source_science_id:
            raise USMSchemaError(
                "ScienceBridgeContract.source_type_ref.science_id must match source_science_id"
            )
        if self.target_type_ref.science_id != self.target_science_id:
            raise USMSchemaError(
                "ScienceBridgeContract.target_type_ref.science_id must match target_science_id"
            )
        require_tuple_of_type(
            "ScienceBridgeContract", "preserved_invariants", self.preserved_invariants, RuleId
        )
        require_tuple_of_type(
            "ScienceBridgeContract", "declared_translation", self.declared_translation, RuleId
        )
        require_tuple_of_type(
            "ScienceBridgeContract",
            "required_evidence_types",
            self.required_evidence_types,
            EvidenceTypeId,
        )
        require_tuple_of_type("ScienceBridgeContract", "blockers", self.blockers, RuleId)
        if not isinstance(self.rank_ceiling, Rank):
            raise USMSchemaError("ScienceBridgeContract.rank_ceiling must be Rank")
        if not isinstance(self.residual_policy_ref, RuleId):
            raise USMSchemaError("ScienceBridgeContract.residual_policy_ref must be RuleId")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("ScienceBridgeContract.trace_ref must be TraceRef")


__all__ = [
    "BridgeDirection",
    "BridgeKind",
    "ScienceBridgeContract",
    "TypedUSMReference",
    "USMReferenceSlot",
]
