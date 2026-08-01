"""USM transformation contract (USM-C1 carrier surface only)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.usm.identifiers import (
    CapabilityId,
    EntityTypeId,
    EvidenceTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    TransformationTypeId,
    USMSchemaError,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class TransformationContract:
    transformation_type_id: TransformationTypeId
    science_id: ScienceId
    source_types: tuple[EntityTypeId, ...]
    target_types: tuple[EntityTypeId, ...]
    required_capabilities: tuple[CapabilityId, ...]
    preserved_invariants: tuple[RuleId, ...]
    declared_changes: tuple[RuleId, ...]
    required_conditions: tuple[RuleId, ...]
    blockers: tuple[RuleId, ...]
    evidence_requirements: tuple[EvidenceTypeId, ...]
    rank_ceiling: Rank
    residual_policy_ref: RuleId
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.transformation_type_id, TransformationTypeId):
            raise USMSchemaError(
                "TransformationContract.transformation_type_id must be TransformationTypeId"
            )
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("TransformationContract.science_id must be ScienceId")
        require_tuple_of_type(
            "TransformationContract", "source_types", self.source_types, EntityTypeId
        )
        require_tuple_of_type(
            "TransformationContract", "target_types", self.target_types, EntityTypeId
        )
        require_tuple_of_type(
            "TransformationContract",
            "required_capabilities",
            self.required_capabilities,
            CapabilityId,
        )
        require_tuple_of_type(
            "TransformationContract",
            "preserved_invariants",
            self.preserved_invariants,
            RuleId,
        )
        require_tuple_of_type(
            "TransformationContract", "declared_changes", self.declared_changes, RuleId
        )
        require_tuple_of_type(
            "TransformationContract", "required_conditions", self.required_conditions, RuleId
        )
        require_tuple_of_type("TransformationContract", "blockers", self.blockers, RuleId)
        require_tuple_of_type(
            "TransformationContract",
            "evidence_requirements",
            self.evidence_requirements,
            EvidenceTypeId,
        )
        if not isinstance(self.rank_ceiling, Rank):
            raise USMSchemaError("TransformationContract.rank_ceiling must be Rank")
        if not isinstance(self.residual_policy_ref, RuleId):
            raise USMSchemaError("TransformationContract.residual_policy_ref must be RuleId")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("TransformationContract.trace_ref must be TraceRef")


__all__ = ["TransformationContract"]
