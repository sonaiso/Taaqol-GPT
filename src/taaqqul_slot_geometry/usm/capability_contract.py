"""USM capability contract (USM-C1 carrier surface only)."""

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
    USMSchemaError,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class CapabilityContract:
    capability_id: CapabilityId
    science_id: ScienceId
    bearer_type: EntityTypeId
    permitted_operations: tuple[RuleId, ...]
    permitted_relation_roles: tuple[RuleId, ...]
    required_conditions: tuple[RuleId, ...]
    blockers: tuple[RuleId, ...]
    evidence_requirements: tuple[EvidenceTypeId, ...]
    rank_ceiling: Rank
    residual_policy_ref: RuleId
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.capability_id, CapabilityId):
            raise USMSchemaError("CapabilityContract.capability_id must be CapabilityId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("CapabilityContract.science_id must be ScienceId")
        if not isinstance(self.bearer_type, EntityTypeId):
            raise USMSchemaError("CapabilityContract.bearer_type must be EntityTypeId")
        require_tuple_of_type(
            "CapabilityContract", "permitted_operations", self.permitted_operations, RuleId
        )
        require_tuple_of_type(
            "CapabilityContract",
            "permitted_relation_roles",
            self.permitted_relation_roles,
            RuleId,
        )
        require_tuple_of_type(
            "CapabilityContract", "required_conditions", self.required_conditions, RuleId
        )
        require_tuple_of_type("CapabilityContract", "blockers", self.blockers, RuleId)
        require_tuple_of_type(
            "CapabilityContract",
            "evidence_requirements",
            self.evidence_requirements,
            EvidenceTypeId,
        )
        if not isinstance(self.rank_ceiling, Rank):
            raise USMSchemaError("CapabilityContract.rank_ceiling must be Rank")
        if not isinstance(self.residual_policy_ref, RuleId):
            raise USMSchemaError("CapabilityContract.residual_policy_ref must be RuleId")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("CapabilityContract.trace_ref must be TraceRef")


__all__ = ["CapabilityContract"]
