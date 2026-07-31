"""USM local evidence contract (USM-C1 carrier surface only)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.usm.identifiers import (
    DomainId,
    EvidenceTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class ScienceEvidenceContract:
    evidence_type_id: EvidenceTypeId
    science_id: ScienceId
    supported_claim_types: tuple[RuleId, ...]
    domain_scope: DomainId
    relevance_rule: RuleId
    coverage_rule: RuleId
    independence_rule: RuleId
    counterevidence_rule: RuleId
    global_rank_ceiling: Rank
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_type_id, EvidenceTypeId):
            raise USMSchemaError("ScienceEvidenceContract.evidence_type_id must be EvidenceTypeId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("ScienceEvidenceContract.science_id must be ScienceId")
        require_tuple_of_type(
            "ScienceEvidenceContract", "supported_claim_types", self.supported_claim_types, RuleId
        )
        if len(self.supported_claim_types) == 0:
            raise USMSchemaError(
                "ScienceEvidenceContract.supported_claim_types must not be empty"
            )
        if not isinstance(self.domain_scope, DomainId):
            raise USMSchemaError("ScienceEvidenceContract.domain_scope must be DomainId")
        if not isinstance(self.relevance_rule, RuleId):
            raise USMSchemaError("ScienceEvidenceContract.relevance_rule must be RuleId")
        if not isinstance(self.coverage_rule, RuleId):
            raise USMSchemaError("ScienceEvidenceContract.coverage_rule must be RuleId")
        if not isinstance(self.independence_rule, RuleId):
            raise USMSchemaError("ScienceEvidenceContract.independence_rule must be RuleId")
        if not isinstance(self.counterevidence_rule, RuleId):
            raise USMSchemaError("ScienceEvidenceContract.counterevidence_rule must be RuleId")
        if not isinstance(self.global_rank_ceiling, Rank):
            raise USMSchemaError("ScienceEvidenceContract.global_rank_ceiling must be Rank")
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("ScienceEvidenceContract.trace_ref must be TraceRef")


__all__ = ["ScienceEvidenceContract"]
