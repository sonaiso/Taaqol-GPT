"""USM judgment contract (USM-C1 carrier surface only)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.usm.identifiers import (
    EvidenceTypeId,
    JudgmentTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_non_empty_text,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class JudgmentContract:
    judgment_type_id: JudgmentTypeId
    science_id: ScienceId
    supported_claim_types: tuple[RuleId, ...]
    required_evidence_types: tuple[EvidenceTypeId, ...]
    local_rank_name: str
    global_rank_ceiling: Rank
    conditions: tuple[RuleId, ...]
    blockers: tuple[RuleId, ...]
    downgrade_rules: tuple[RuleId, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.judgment_type_id, JudgmentTypeId):
            raise USMSchemaError("JudgmentContract.judgment_type_id must be JudgmentTypeId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("JudgmentContract.science_id must be ScienceId")
        require_tuple_of_type(
            "JudgmentContract", "supported_claim_types", self.supported_claim_types, RuleId
        )
        require_tuple_of_type(
            "JudgmentContract",
            "required_evidence_types",
            self.required_evidence_types,
            EvidenceTypeId,
        )
        if len(self.required_evidence_types) == 0:
            raise USMSchemaError("JudgmentContract.required_evidence_types must not be empty")
        require_non_empty_text("JudgmentContract", "local_rank_name", self.local_rank_name)
        if not isinstance(self.global_rank_ceiling, Rank):
            raise USMSchemaError("JudgmentContract.global_rank_ceiling must be Rank")
        require_tuple_of_type("JudgmentContract", "conditions", self.conditions, RuleId)
        require_tuple_of_type("JudgmentContract", "blockers", self.blockers, RuleId)
        require_tuple_of_type("JudgmentContract", "downgrade_rules", self.downgrade_rules, RuleId)
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("JudgmentContract.trace_ref must be TraceRef")


__all__ = ["JudgmentContract"]
