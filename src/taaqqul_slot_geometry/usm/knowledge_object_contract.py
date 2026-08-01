"""USM knowledge object contract (USM-C1 carrier surface only)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.usm.identifiers import (
    EntityTypeId,
    JudgmentTypeId,
    KnowledgeObjectTypeId,
    RelationTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class KnowledgeObjectContract:
    knowledge_object_type_id: KnowledgeObjectTypeId
    science_id: ScienceId
    subject_types: tuple[EntityTypeId, ...]
    relation_types: tuple[RelationTypeId, ...]
    required_judgments: tuple[JudgmentTypeId, ...]
    scope_rule: RuleId
    exception_policy: RuleId
    conflict_policy: RuleId
    revision_policy: RuleId
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.knowledge_object_type_id, KnowledgeObjectTypeId):
            raise USMSchemaError(
                "KnowledgeObjectContract.knowledge_object_type_id must be KnowledgeObjectTypeId"
            )
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("KnowledgeObjectContract.science_id must be ScienceId")
        require_tuple_of_type(
            "KnowledgeObjectContract", "subject_types", self.subject_types, EntityTypeId
        )
        require_tuple_of_type(
            "KnowledgeObjectContract", "relation_types", self.relation_types, RelationTypeId
        )
        require_tuple_of_type(
            "KnowledgeObjectContract",
            "required_judgments",
            self.required_judgments,
            JudgmentTypeId,
        )
        if not isinstance(self.scope_rule, RuleId):
            raise USMSchemaError("KnowledgeObjectContract.scope_rule must be RuleId")
        if not isinstance(self.exception_policy, RuleId):
            raise USMSchemaError("KnowledgeObjectContract.exception_policy must be RuleId")
        if not isinstance(self.conflict_policy, RuleId):
            raise USMSchemaError("KnowledgeObjectContract.conflict_policy must be RuleId")
        if not isinstance(self.revision_policy, RuleId):
            raise USMSchemaError("KnowledgeObjectContract.revision_policy must be RuleId")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("KnowledgeObjectContract.trace_ref must be TraceRef")


__all__ = ["KnowledgeObjectContract"]
