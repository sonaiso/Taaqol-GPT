"""WEIGHT-ONTOLOGY-BRIDGE-C1 contract surface (carrier-only).

Runtime contract binding for docs/90 §10 hardening statements:
* NoWeightedAnchor without ActiveOntologySchema.
* No bridge output from weight image alone.
* Typed compatibility is structural, not semantic generation.
* WeightedAnchorCandidate is never Meaning/Predication/Truth.

This module is C1 carrier-only surface:
* frozen dataclasses + schema guards,
* no gate execution,
* no bridge arbitration runtime,
* no meaning/predication/truth closure output.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight._schema_helpers import (
    require_non_empty as _shared_require_non_empty,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_rank as _shared_validate_rank,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError

WEIGHT_ONTOLOGY_BRIDGE_C1_RANK_CEILING: Rank = Rank.CANDIDATE
WEIGHT_ONTOLOGY_BRIDGE_C1_ALLOWED_OUTPUT: str = "WEIGHTED_ANCHOR_COMPATIBILITY_ASSESSMENT"
WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "MEANING",
    "PREDICATION",
    "TRUTH",
    "ACTUAL_THING",
    "ACTUAL_PROPERTY",
    "ACTUAL_ATTRIBUTE",
    "ACTUAL_TRANSFORMATION",
    "ACTUAL_EVENT",
    "ACTUAL_GENUS_MEMBERSHIP",
    "ACTUAL_SPECIES_MEMBERSHIP",
    "ACTUAL_AGENT",
    "ACTUAL_PATIENT",
    "ACTUAL_RELATION",
    "RESOLVED_REFERENCE",
    "EXTERNAL_TRUTH",
)

WEIGHT_ONTOLOGY_BRIDGE_C1_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "ACTIVE_ONTOLOGY_SCHEMA_REQUIRED",
    "DECLARED_WEIGHT_KIND_REQUIRED",
    "TYPED_COMPATIBILITY_RULE_REQUIRED",
    "LEXICAL_EVIDENCE_REQUIRED",
    "STRUCTURAL_COMPATIBILITY_ONLY",
    "COMPETING_BRIDGE_ALTERNATIVES",
    "HARF_OR_MABNI_PATH_BLOCKED",
    "RELATION_REFERENCE_PATH_UNLICENSED",
    "WEIGHT_COLLAPSE_REVOKES_DEPENDENTS",
    "SCHEMA_COLLAPSE_REOPENS_BRIDGE",
)


class WeightOntologyBridgeResidualKind(StrEnum):
    """Local residual vocabulary for WEIGHT-ONTOLOGY-BRIDGE-C1."""

    ACTIVE_ONTOLOGY_SCHEMA_REQUIRED = "ACTIVE_ONTOLOGY_SCHEMA_REQUIRED"
    DECLARED_WEIGHT_KIND_REQUIRED = "DECLARED_WEIGHT_KIND_REQUIRED"
    TYPED_COMPATIBILITY_RULE_REQUIRED = "TYPED_COMPATIBILITY_RULE_REQUIRED"
    LEXICAL_EVIDENCE_REQUIRED = "LEXICAL_EVIDENCE_REQUIRED"
    STRUCTURAL_COMPATIBILITY_ONLY = "STRUCTURAL_COMPATIBILITY_ONLY"
    COMPETING_BRIDGE_ALTERNATIVES = "COMPETING_BRIDGE_ALTERNATIVES"
    HARF_OR_MABNI_PATH_BLOCKED = "HARF_OR_MABNI_PATH_BLOCKED"
    RELATION_REFERENCE_PATH_UNLICENSED = "RELATION_REFERENCE_PATH_UNLICENSED"
    WEIGHT_COLLAPSE_REVOKES_DEPENDENTS = "WEIGHT_COLLAPSE_REVOKES_DEPENDENTS"
    SCHEMA_COLLAPSE_REOPENS_BRIDGE = "SCHEMA_COLLAPSE_REOPENS_BRIDGE"


class WeightKind(StrEnum):
    """Declared `weight_kind` constrained by docs/90 §10 hardening."""

    JAMID_STEM = "JAMID_STEM"
    SOURCE = "SOURCE"
    DERIVATIONAL_NOUN = "DERIVATIONAL_NOUN"
    VERB_FORM = "VERB_FORM"
    TRANSFORMATION_PATTERN = "TRANSFORMATION_PATTERN"
    PLURAL = "PLURAL"
    DIMINUTIVE = "DIMINUTIVE"
    NISBA = "NISBA"


class AnchorKind(StrEnum):
    """Admissible typed anchor-candidate kinds for bridge assessment."""

    WEIGHTED_ENTITY_ANCHOR = "WEIGHTED_ENTITY_ANCHOR"
    WEIGHTED_GENUS_ANCHOR = "WEIGHTED_GENUS_ANCHOR"
    WEIGHTED_SPECIES_ANCHOR = "WEIGHTED_SPECIES_ANCHOR"
    WEIGHTED_PROPERTY_ANCHOR = "WEIGHTED_PROPERTY_ANCHOR"
    WEIGHTED_SOURCE_ANCHOR = "WEIGHTED_SOURCE_ANCHOR"
    WEIGHTED_ATTRIBUTE_INTERFACE = "WEIGHTED_ATTRIBUTE_INTERFACE"
    WEIGHTED_EVENT_FRAME = "WEIGHTED_EVENT_FRAME"
    WEIGHTED_RELATION_INTERFACE = "WEIGHTED_RELATION_INTERFACE"
    WEIGHTED_REFERENCE_INTERFACE = "WEIGHTED_REFERENCE_INTERFACE"


class BridgePathFamily(StrEnum):
    """Input path families relevant to bridge admission discipline."""

    DERIVATIONAL_WEIGHT_PATH = "DERIVATIONAL_WEIGHT_PATH"
    HARF_PATH = "HARF_PATH"
    MABNI_PATH = "MABNI_PATH"
    OTHER_PATH = "OTHER_PATH"


class BridgeDecisionState(StrEnum):
    """BridgeAssessment decision state."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"
    SUSPENDED = "SUSPENDED"
    UNDERDETERMINED = "UNDERDETERMINED"


class BridgeConflictState(StrEnum):
    """BridgeAssessment conflict channel (distinct from residuals)."""

    NONE = "NONE"
    BLOCKER_PRESENT = "BLOCKER_PRESENT"
    COMPETING_ALTERNATIVES = "COMPETING_ALTERNATIVES"
    DEFEATING_DIFFERENCE = "DEFEATING_DIFFERENCE"


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=WEIGHT_ONTOLOGY_BRIDGE_C1_RANK_CEILING)


def _validate_string_tuple(
    value: tuple[str, ...],
    owner: str,
    *,
    failure_code: FailureCode,
    must_be_non_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise WeightCarrierSchemaError(
            f"{owner} must be a tuple ({failure_code.value})"
        )
    if must_be_non_empty and not value:
        raise WeightCarrierSchemaError(
            f"{owner} must not be empty ({failure_code.value})"
        )
    for item in value:
        _require_non_empty(item, f"{owner} entry", failure_code)


def _validate_forbidden_outputs(outputs: tuple[str, ...], owner: str) -> None:
    _validate_string_tuple(
        outputs,
        f"{owner}.forbidden_outputs",
        failure_code=FailureCode.OUTPUT_EXCEEDS_LAYER,
    )
    if outputs != WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS:
        raise WeightCarrierSchemaError(
            f"{owner}.forbidden_outputs must exactly match "
            "WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS "
            f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
        )


@dataclass(frozen=True, slots=True)
class WeightOntologyBridgeResidual:
    """Visible local residual for bridge C1 contracts."""

    kind: WeightOntologyBridgeResidualKind
    trace_ref: str
    visibility: Literal["VISIBLE"] = "VISIBLE"
    blocking: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.kind, WeightOntologyBridgeResidualKind):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeResidual.kind must be "
                "WeightOntologyBridgeResidualKind "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        _require_non_empty(
            self.trace_ref,
            "WeightOntologyBridgeResidual.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.visibility != "VISIBLE":
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeResidual.visibility must be VISIBLE "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeResidual.blocking must be bool "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class OntologySchemaRef:
    """Active ontology-schema reference used by bridge C1 contracts."""

    schema_id: str
    schema_kind: str
    domain: str
    admissible_properties: tuple[str, ...]
    invariant_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    trace_ref: str
    schema_status: Literal["ACTIVE"] = "ACTIVE"

    def __post_init__(self) -> None:
        _require_non_empty(
            self.schema_id,
            "OntologySchemaRef.schema_id",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.schema_kind, "OntologySchemaRef.schema_kind", FailureCode.BOUNDARY_MISSING
        )
        _require_non_empty(self.domain, "OntologySchemaRef.domain", FailureCode.DOMAIN_MISSING)
        _validate_string_tuple(
            self.admissible_properties,
            "OntologySchemaRef.admissible_properties",
            failure_code=FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.invariant_refs,
            "OntologySchemaRef.invariant_refs",
            failure_code=FailureCode.BOUNDARY_MISSING,
            must_be_non_empty=True,
        )
        _validate_string_tuple(
            self.evidence_refs,
            "OntologySchemaRef.evidence_refs",
            failure_code=FailureCode.BOUNDARY_MISSING,
            must_be_non_empty=True,
        )
        _require_non_empty(self.trace_ref, "OntologySchemaRef.trace_ref", FailureCode.TRACE_MISSING)
        if self.schema_status != "ACTIVE":
            raise WeightCarrierSchemaError(
                "OntologySchemaRef.schema_status must be ACTIVE "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class WeightOntologyBridgeRequest:
    """C1 request contract: typed compatibility inputs only."""

    request_id: str
    formal_weight_id: str
    ontology_schema_ref: OntologySchemaRef
    weight_kind: WeightKind
    requested_anchor_kind: AnchorKind
    path_family: BridgePathFamily
    compatibility_rule_ids: tuple[str, ...]
    lexical_evidence_refs: tuple[str, ...]
    residuals: tuple[WeightOntologyBridgeResidual, ...]
    rank: Rank
    trace_ref: str
    forbidden_outputs: tuple[str, ...] = WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.request_id,
            "WeightOntologyBridgeRequest.request_id",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.formal_weight_id,
            "WeightOntologyBridgeRequest.formal_weight_id",
            FailureCode.BOUNDARY_MISSING,
        )
        if not isinstance(self.ontology_schema_ref, OntologySchemaRef):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeRequest.ontology_schema_ref must be OntologySchemaRef "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.weight_kind, WeightKind):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeRequest.weight_kind must be WeightKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.requested_anchor_kind, AnchorKind):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeRequest.requested_anchor_kind must be AnchorKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.path_family, BridgePathFamily):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeRequest.path_family must be BridgePathFamily "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.path_family in {BridgePathFamily.HARF_PATH, BridgePathFamily.MABNI_PATH}:
            raise WeightCarrierSchemaError(
                "HARF/MABNI paths do not open WEIGHT-ONTOLOGY-BRIDGE-C1 by default "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )
        if self.requested_anchor_kind in {
            AnchorKind.WEIGHTED_RELATION_INTERFACE,
            AnchorKind.WEIGHTED_REFERENCE_INTERFACE,
        } and self.path_family is not BridgePathFamily.DERIVATIONAL_WEIGHT_PATH:
            raise WeightCarrierSchemaError(
                "Relation/reference weighted interfaces require DERIVATIONAL_WEIGHT_PATH "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )
        _validate_string_tuple(
            self.compatibility_rule_ids,
            "WeightOntologyBridgeRequest.compatibility_rule_ids",
            failure_code=FailureCode.BOUNDARY_MISSING,
            must_be_non_empty=True,
        )
        _validate_string_tuple(
            self.lexical_evidence_refs,
            "WeightOntologyBridgeRequest.lexical_evidence_refs",
            failure_code=FailureCode.BOUNDARY_MISSING,
            must_be_non_empty=True,
        )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeRequest.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, WeightOntologyBridgeResidual):
                raise WeightCarrierSchemaError(
                    "WeightOntologyBridgeRequest.residuals entries must be "
                    "WeightOntologyBridgeResidual "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        _validate_rank(self.rank, "WeightOntologyBridgeRequest")
        _require_non_empty(
            self.trace_ref,
            "WeightOntologyBridgeRequest.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _validate_forbidden_outputs(self.forbidden_outputs, "WeightOntologyBridgeRequest")


@dataclass(frozen=True, slots=True)
class WeightOntologyBridgeAssessment:
    """C1 assessment contract: decision/rank/conflict/residuals/allowed anchors."""

    request_id: str
    allowed_anchor_kinds: tuple[AnchorKind, ...]
    competing_bridge_ids: tuple[str, ...]
    defeating_difference_refs: tuple[str, ...]
    blocker_refs: tuple[str, ...]
    decision: BridgeDecisionState
    rank: Rank
    conflict: BridgeConflictState
    residuals: tuple[WeightOntologyBridgeResidual, ...]
    trace_ref: str
    forbidden_outputs: tuple[str, ...] = WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.request_id,
            "WeightOntologyBridgeAssessment.request_id",
            FailureCode.IDENTITY_BROKEN,
        )
        if not isinstance(self.allowed_anchor_kinds, tuple):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeAssessment.allowed_anchor_kinds must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for anchor_kind in self.allowed_anchor_kinds:
            if not isinstance(anchor_kind, AnchorKind):
                raise WeightCarrierSchemaError(
                    "WeightOntologyBridgeAssessment.allowed_anchor_kinds entries must be "
                    "AnchorKind "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        _validate_string_tuple(
            self.competing_bridge_ids,
            "WeightOntologyBridgeAssessment.competing_bridge_ids",
            failure_code=FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.defeating_difference_refs,
            "WeightOntologyBridgeAssessment.defeating_difference_refs",
            failure_code=FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.blocker_refs,
            "WeightOntologyBridgeAssessment.blocker_refs",
            failure_code=FailureCode.BOUNDARY_MISSING,
        )
        if not isinstance(self.decision, BridgeDecisionState):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeAssessment.decision must be BridgeDecisionState "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_rank(self.rank, "WeightOntologyBridgeAssessment")
        if not isinstance(self.conflict, BridgeConflictState):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeAssessment.conflict must be BridgeConflictState "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "WeightOntologyBridgeAssessment.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, WeightOntologyBridgeResidual):
                raise WeightCarrierSchemaError(
                    "WeightOntologyBridgeAssessment.residuals entries must be "
                    "WeightOntologyBridgeResidual "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        _require_non_empty(
            self.trace_ref,
            "WeightOntologyBridgeAssessment.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.decision is BridgeDecisionState.PROVEN and not self.allowed_anchor_kinds:
            raise WeightCarrierSchemaError(
                "PROVEN assessment requires at least one allowed anchor kind "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if len(self.allowed_anchor_kinds) > 1 and self.decision is BridgeDecisionState.PROVEN:
            raise WeightCarrierSchemaError(
                "Multiple admissible anchors cannot be forced into PROVEN single-winner output "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )
        if len(self.allowed_anchor_kinds) > 1 and self.decision not in {
            BridgeDecisionState.UNDERDETERMINED,
            BridgeDecisionState.SUSPENDED,
        }:
            raise WeightCarrierSchemaError(
                "Multiple admissible anchors require UNDERDETERMINED or SUSPENDED decision "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "WeightOntologyBridgeAssessment")


__all__ = [
    "AnchorKind",
    "BridgeConflictState",
    "BridgeDecisionState",
    "BridgePathFamily",
    "OntologySchemaRef",
    "WEIGHT_ONTOLOGY_BRIDGE_C1_ALLOWED_OUTPUT",
    "WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS",
    "WEIGHT_ONTOLOGY_BRIDGE_C1_RANK_CEILING",
    "WEIGHT_ONTOLOGY_BRIDGE_C1_RESIDUAL_VOCABULARY",
    "WeightKind",
    "WeightOntologyBridgeAssessment",
    "WeightOntologyBridgeRequest",
    "WeightOntologyBridgeResidual",
    "WeightOntologyBridgeResidualKind",
]
