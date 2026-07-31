"""USM entity type contract (USM-C1 carrier surface only)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.usm.identifiers import (
    CriterionId,
    DomainId,
    EntityTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class EntityTypeContract:
    entity_type_id: EntityTypeId
    science_id: ScienceId
    domain_id: DomainId
    identity_criterion: CriterionId
    membership_criterion: CriterionId
    boundary_rule: RuleId
    parent_types: tuple[EntityTypeId, ...]
    forbidden_confusions: tuple[RuleId, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.entity_type_id, EntityTypeId):
            raise USMSchemaError("EntityTypeContract.entity_type_id must be EntityTypeId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("EntityTypeContract.science_id must be ScienceId")
        if not isinstance(self.domain_id, DomainId):
            raise USMSchemaError("EntityTypeContract.domain_id must be DomainId")
        if not isinstance(self.identity_criterion, CriterionId):
            raise USMSchemaError("EntityTypeContract.identity_criterion must be CriterionId")
        if not isinstance(self.membership_criterion, CriterionId):
            raise USMSchemaError("EntityTypeContract.membership_criterion must be CriterionId")
        if not isinstance(self.boundary_rule, RuleId):
            raise USMSchemaError("EntityTypeContract.boundary_rule must be RuleId")
        require_tuple_of_type(
            "EntityTypeContract", "parent_types", self.parent_types, EntityTypeId
        )
        require_tuple_of_type(
            "EntityTypeContract", "forbidden_confusions", self.forbidden_confusions, RuleId
        )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("EntityTypeContract.trace_ref must be TraceRef")


__all__ = ["EntityTypeContract"]
