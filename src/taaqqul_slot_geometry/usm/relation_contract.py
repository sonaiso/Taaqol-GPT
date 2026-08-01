"""USM relation contract (USM-C1 carrier surface only)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.usm.enums import RelationDirection
from taaqqul_slot_geometry.usm.identifiers import (
    EntityTypeId,
    RelationTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class RelationContract:
    relation_type_id: RelationTypeId
    science_id: ScienceId
    arity: int
    operand_types: tuple[EntityTypeId, ...]
    roles: tuple[RuleId, ...]
    direction: RelationDirection
    compatibility_rules: tuple[RuleId, ...]
    saturation_rule: RuleId
    scope_rule: RuleId
    closure_rule: RuleId
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.relation_type_id, RelationTypeId):
            raise USMSchemaError("RelationContract.relation_type_id must be RelationTypeId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("RelationContract.science_id must be ScienceId")
        if not isinstance(self.arity, int) or self.arity <= 0:
            raise USMSchemaError("RelationContract.arity must be a positive int")
        require_tuple_of_type("RelationContract", "operand_types", self.operand_types, EntityTypeId)
        require_tuple_of_type("RelationContract", "roles", self.roles, RuleId)
        if len(self.roles) != self.arity:
            raise USMSchemaError("RelationContract.roles length must match arity")
        if len(self.operand_types) != self.arity:
            raise USMSchemaError("RelationContract.operand_types length must match arity")
        if not isinstance(self.direction, RelationDirection):
            raise USMSchemaError("RelationContract.direction must be RelationDirection")
        require_tuple_of_type(
            "RelationContract", "compatibility_rules", self.compatibility_rules, RuleId
        )
        if not isinstance(self.saturation_rule, RuleId):
            raise USMSchemaError("RelationContract.saturation_rule must be RuleId")
        if not isinstance(self.scope_rule, RuleId):
            raise USMSchemaError("RelationContract.scope_rule must be RuleId")
        if not isinstance(self.closure_rule, RuleId):
            raise USMSchemaError("RelationContract.closure_rule must be RuleId")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("RelationContract.trace_ref must be TraceRef")


__all__ = ["RelationContract"]
