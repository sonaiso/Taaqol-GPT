"""USM application contract (USM-C1 carrier surface only)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.usm.identifiers import (
    ApplicationTypeId,
    CriterionId,
    EntityTypeId,
    KnowledgeObjectTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class ApplicationContract:
    application_type_id: ApplicationTypeId
    science_id: ScienceId
    knowledge_object_types: tuple[KnowledgeObjectTypeId, ...]
    case_entity_types: tuple[EntityTypeId, ...]
    membership_criterion: CriterionId
    required_conditions: tuple[RuleId, ...]
    blockers: tuple[RuleId, ...]
    invalidating_differences: tuple[RuleId, ...]
    feedback_policy: RuleId
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.application_type_id, ApplicationTypeId):
            raise USMSchemaError(
                "ApplicationContract.application_type_id must be ApplicationTypeId"
            )
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("ApplicationContract.science_id must be ScienceId")
        require_tuple_of_type(
            "ApplicationContract",
            "knowledge_object_types",
            self.knowledge_object_types,
            KnowledgeObjectTypeId,
        )
        require_tuple_of_type(
            "ApplicationContract", "case_entity_types", self.case_entity_types, EntityTypeId
        )
        if not isinstance(self.membership_criterion, CriterionId):
            raise USMSchemaError("ApplicationContract.membership_criterion must be CriterionId")
        require_tuple_of_type(
            "ApplicationContract", "required_conditions", self.required_conditions, RuleId
        )
        require_tuple_of_type("ApplicationContract", "blockers", self.blockers, RuleId)
        require_tuple_of_type(
            "ApplicationContract", "invalidating_differences", self.invalidating_differences, RuleId
        )
        if not isinstance(self.feedback_policy, RuleId):
            raise USMSchemaError("ApplicationContract.feedback_policy must be RuleId")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("ApplicationContract.trace_ref must be TraceRef")


__all__ = ["ApplicationContract"]
