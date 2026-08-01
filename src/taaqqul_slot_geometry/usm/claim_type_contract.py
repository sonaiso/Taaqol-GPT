"""USM claim-type contract registry (USM-C2.1 carrier-only surface)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.usm.identifiers import (
    ClaimTypeId,
    DomainId,
    EntityTypeId,
    EvidenceTypeId,
    RelationTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_tuple_of_type,
)


@dataclass(frozen=True, slots=True)
class ClaimTypeContract:
    claim_type_id: ClaimTypeId
    science_id: ScienceId
    domain_scope: DomainId
    subject_type_refs: tuple[EntityTypeId, ...]
    predicate_or_result_type_refs: tuple[EntityTypeId, ...]
    relation_type_refs: tuple[RelationTypeId, ...]
    matching_criterion_ref: RuleId
    admissible_evidence_type_refs: tuple[EvidenceTypeId, ...]
    local_rank_ceiling: Rank
    forbidden_overclaims: tuple[RuleId, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.claim_type_id, ClaimTypeId):
            raise USMSchemaError("ClaimTypeContract.claim_type_id must be ClaimTypeId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("ClaimTypeContract.science_id must be ScienceId")
        if not isinstance(self.domain_scope, DomainId):
            raise USMSchemaError("ClaimTypeContract.domain_scope must be DomainId")
        require_tuple_of_type(
            "ClaimTypeContract", "subject_type_refs", self.subject_type_refs, EntityTypeId
        )
        require_tuple_of_type(
            "ClaimTypeContract",
            "predicate_or_result_type_refs",
            self.predicate_or_result_type_refs,
            EntityTypeId,
        )
        require_tuple_of_type(
            "ClaimTypeContract", "relation_type_refs", self.relation_type_refs, RelationTypeId
        )
        if not isinstance(self.matching_criterion_ref, RuleId):
            raise USMSchemaError("ClaimTypeContract.matching_criterion_ref must be RuleId")
        require_tuple_of_type(
            "ClaimTypeContract",
            "admissible_evidence_type_refs",
            self.admissible_evidence_type_refs,
            EvidenceTypeId,
        )
        if len(self.admissible_evidence_type_refs) == 0:
            raise USMSchemaError(
                "ClaimTypeContract.admissible_evidence_type_refs must not be empty"
            )
        if not isinstance(self.local_rank_ceiling, Rank):
            raise USMSchemaError("ClaimTypeContract.local_rank_ceiling must be Rank")
        require_tuple_of_type(
            "ClaimTypeContract", "forbidden_overclaims", self.forbidden_overclaims, RuleId
        )
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("ClaimTypeContract.trace_ref must be TraceRef")


__all__ = ["ClaimTypeContract"]
