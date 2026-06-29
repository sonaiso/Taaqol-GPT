"""AQD L1 audit-only contracts.

The AQD surface is a proof-reference contract layer, not a parser,
interpreter, relation runtime, semantic runtime, or execution engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from taaqqul_slot_geometry.core.rank_lattice import Rank


class AqdAuditContractSchemaError(TypeError):
    """Raised when an AQD audit-only contract violates its schema."""


AQD_RANK_CEILING: Rank = Rank.CANDIDATE

AQD_FORBIDDEN_OUTPUTS: frozenset[str] = frozenset(
    {
        "RUNTIME_RESULT",
        "AUTHORITATIVE_DECISION",
        "FINAL_MEANING",
        "RELATION_RUNTIME",
        "IFADAH_RUNTIME",
        "HUKM",
        "TANZIL",
        "YAQIN",
        "KERNEL_DECISION",
    }
)

AQD_AUDIT_STATUSES: frozenset[str] = frozenset(
    {
        "AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
        "AUDIT_SHAPE_INVALID_RUNTIME_STILL_BLOCKED",
        "AUDIT_REVERSE_REQUIRED_RUNTIME_STILL_BLOCKED",
    }
)


@dataclass(frozen=True, slots=True)
class AqdUniversalContract:
    """Universal AQD contract identity; audit-only and never authoritative."""

    contract_ref: str
    domain_ref: str
    scope_ref: str
    trace_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    rank: Rank = AQD_RANK_CEILING
    authoritative: Literal[False] = False
    runtime_authorized: Literal[False] = False
    forbidden_outputs: frozenset[str] = AQD_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_ref, "AqdUniversalContract.contract_ref")
        _require_non_empty(self.domain_ref, "AqdUniversalContract.domain_ref")
        _require_non_empty(self.scope_ref, "AqdUniversalContract.scope_ref")
        _validate_aqd_contract_surface(self, "AqdUniversalContract")


@dataclass(frozen=True, slots=True)
class AqdPartialBranchContract:
    """AQD branch shape: origin, branch, relations, condition, sabab, preventer."""

    origin_ref: str
    branch_ref: str
    relation_with_prev_ref: str
    relation_with_next_ref: str
    relation_next_to_prev_ref: str
    condition_ref: str
    sabab_ref: str
    preventer_ref: str
    trace_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    rank: Rank = AQD_RANK_CEILING
    authoritative: Literal[False] = False
    runtime_authorized: Literal[False] = False
    forbidden_outputs: frozenset[str] = AQD_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        for field_name in (
            "origin_ref",
            "branch_ref",
            "relation_with_prev_ref",
            "relation_with_next_ref",
            "relation_next_to_prev_ref",
            "condition_ref",
            "sabab_ref",
            "preventer_ref",
        ):
            _require_non_empty(
                getattr(self, field_name),
                f"AqdPartialBranchContract.{field_name}",
            )
        _validate_aqd_contract_surface(self, "AqdPartialBranchContract")


@dataclass(frozen=True, slots=True)
class AqdAttributeContract:
    """AQD attribute shape; carries refs only and emits no final property."""

    carrier_ref: str
    attribute_ref: str
    operator_ref: str
    effect_candidate_ref: str
    trace_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    rank: Rank = AQD_RANK_CEILING
    authoritative: Literal[False] = False
    runtime_authorized: Literal[False] = False
    forbidden_outputs: frozenset[str] = AQD_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(self.carrier_ref, "AqdAttributeContract.carrier_ref")
        _require_non_empty(self.attribute_ref, "AqdAttributeContract.attribute_ref")
        _require_non_empty(self.operator_ref, "AqdAttributeContract.operator_ref")
        _require_non_empty(
            self.effect_candidate_ref,
            "AqdAttributeContract.effect_candidate_ref",
        )
        _validate_aqd_contract_surface(self, "AqdAttributeContract")


@dataclass(frozen=True, slots=True)
class AqdRelationTripletContract:
    """AQD relation triplet candidate; never opens final relation runtime."""

    previous_relation_ref: str
    next_relation_ref: str
    next_to_previous_relation_ref: str
    relation_function_candidate: str
    tool_surface_ref: str
    license_condition_ref: str
    trace_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    rank: Rank = AQD_RANK_CEILING
    authoritative: Literal[False] = False
    runtime_authorized: Literal[False] = False
    relation_authorized: Literal[False] = False
    relation_runtime_opened: Literal[False] = False
    forbidden_outputs: frozenset[str] = AQD_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        for field_name in (
            "previous_relation_ref",
            "next_relation_ref",
            "next_to_previous_relation_ref",
            "relation_function_candidate",
            "tool_surface_ref",
            "license_condition_ref",
        ):
            _require_non_empty(
                getattr(self, field_name),
                f"AqdRelationTripletContract.{field_name}",
            )
        _require_false(self.relation_authorized, "AqdRelationTripletContract.relation_authorized")
        _require_false(
            self.relation_runtime_opened,
            "AqdRelationTripletContract.relation_runtime_opened",
        )
        _validate_aqd_contract_surface(self, "AqdRelationTripletContract")


@dataclass(frozen=True, slots=True)
class AqdTemporalBindingContract:
    """AQD temporal binding shape; references time but never executes time."""

    temporal_scope_ref: str
    utterance_time_ref: str
    attribute_time_ref: str
    temporal_policy_ref: str
    trace_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    rank: Rank = AQD_RANK_CEILING
    authoritative: Literal[False] = False
    runtime_authorized: Literal[False] = False
    time_executed: Literal[False] = False
    forbidden_outputs: frozenset[str] = AQD_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.temporal_scope_ref,
            "AqdTemporalBindingContract.temporal_scope_ref",
        )
        _require_non_empty(
            self.utterance_time_ref,
            "AqdTemporalBindingContract.utterance_time_ref",
        )
        _require_non_empty(
            self.attribute_time_ref,
            "AqdTemporalBindingContract.attribute_time_ref",
        )
        _require_non_empty(
            self.temporal_policy_ref,
            "AqdTemporalBindingContract.temporal_policy_ref",
        )
        _require_false(self.time_executed, "AqdTemporalBindingContract.time_executed")
        _validate_aqd_contract_surface(self, "AqdTemporalBindingContract")


@dataclass(frozen=True, slots=True)
class AqdInflectionAuditContract:
    """AQD inflection audit shape; no final i'rab or meaning is emitted."""

    operator_ref: str
    carrier_ref: str
    utterance_time_ref: str
    attribute_time_ref: str
    temporal_policy_ref: str
    effect_candidate_ref: str
    trace_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    rank: Rank = AQD_RANK_CEILING
    authoritative: Literal[False] = False
    runtime_authorized: Literal[False] = False
    final_irab_emitted: Literal[False] = False
    final_meaning_emitted: Literal[False] = False
    forbidden_outputs: frozenset[str] = AQD_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        for field_name in (
            "operator_ref",
            "carrier_ref",
            "utterance_time_ref",
            "attribute_time_ref",
            "temporal_policy_ref",
            "effect_candidate_ref",
        ):
            _require_non_empty(
                getattr(self, field_name),
                f"AqdInflectionAuditContract.{field_name}",
            )
        _require_false(
            self.final_irab_emitted,
            "AqdInflectionAuditContract.final_irab_emitted",
        )
        _require_false(
            self.final_meaning_emitted,
            "AqdInflectionAuditContract.final_meaning_emitted",
        )
        _validate_aqd_contract_surface(self, "AqdInflectionAuditContract")


@dataclass(frozen=True, slots=True)
class AqdMorphologicalBranchContract:
    """AQD morphological branch shape; surface weight never opens derivation."""

    surface_weight_ref: str
    path_card_ref: str
    masdar_open_ref: str
    denominal_branch_license_ref: str
    residual_policy_ref: str
    trace_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    rank: Rank = AQD_RANK_CEILING
    authoritative: Literal[False] = False
    runtime_authorized: Literal[False] = False
    derivation_runtime_opened: Literal[False] = False
    forbidden_outputs: frozenset[str] = AQD_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        for field_name in (
            "surface_weight_ref",
            "path_card_ref",
            "masdar_open_ref",
            "denominal_branch_license_ref",
            "residual_policy_ref",
        ):
            _require_non_empty(
                getattr(self, field_name),
                f"AqdMorphologicalBranchContract.{field_name}",
            )
        _require_false(
            self.derivation_runtime_opened,
            "AqdMorphologicalBranchContract.derivation_runtime_opened",
        )
        _validate_aqd_contract_surface(self, "AqdMorphologicalBranchContract")


@dataclass(frozen=True, slots=True)
class AqdReverseAuditContract:
    """AQD reverse audit requirement; source/target refs only, no reverse runtime."""

    source_stage_ref: str
    target_stage_ref: str
    reverse_policy_ref: str
    trace_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    rank: Rank = AQD_RANK_CEILING
    authoritative: Literal[False] = False
    runtime_authorized: Literal[False] = False
    reverse_runtime_opened: Literal[False] = False
    forbidden_outputs: frozenset[str] = AQD_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(self.source_stage_ref, "AqdReverseAuditContract.source_stage_ref")
        _require_non_empty(self.target_stage_ref, "AqdReverseAuditContract.target_stage_ref")
        _require_non_empty(self.reverse_policy_ref, "AqdReverseAuditContract.reverse_policy_ref")
        _require_false(
            self.reverse_runtime_opened,
            "AqdReverseAuditContract.reverse_runtime_opened",
        )
        _validate_aqd_contract_surface(self, "AqdReverseAuditContract")


@dataclass(frozen=True, slots=True)
class AqdAuditResult:
    """Audit-only AQD shape status; valid shape still leaves runtime blocked."""

    shape_valid: bool
    status: str
    residuals: frozenset[str]
    trace_ref: str
    runtime_authorized: Literal[False] = False
    authoritative: Literal[False] = False
    rank: Rank = AQD_RANK_CEILING

    def __post_init__(self) -> None:
        if not isinstance(self.shape_valid, bool):
            raise AqdAuditContractSchemaError("AqdAuditResult.shape_valid must be bool")
        if self.status not in AQD_AUDIT_STATUSES:
            raise AqdAuditContractSchemaError(
                "AqdAuditResult.status must be an AQD audit-only status"
            )
        _validate_residuals(self.residuals, "AqdAuditResult.residuals")
        _require_non_empty(self.trace_ref, "AqdAuditResult.trace_ref")
        _require_false(self.runtime_authorized, "AqdAuditResult.runtime_authorized")
        _require_false(self.authoritative, "AqdAuditResult.authoritative")
        _validate_rank(self.rank, "AqdAuditResult.rank")


def _validate_aqd_contract_surface(contract: object, owner: str) -> None:
    _validate_rank(getattr(contract, "rank"), f"{owner}.rank")
    _require_false(getattr(contract, "authoritative"), f"{owner}.authoritative")
    _require_false(
        getattr(contract, "runtime_authorized"),
        f"{owner}.runtime_authorized",
    )
    _require_non_empty(getattr(contract, "trace_ref"), f"{owner}.trace_ref")
    _require_proof_ref(
        getattr(contract, "proof_object_ref"),
        getattr(contract, "proof_trace_ref"),
        owner,
    )
    _validate_forbidden_outputs(getattr(contract, "forbidden_outputs"), owner)


def _validate_rank(rank: object, field_name: str) -> None:
    if not isinstance(rank, Rank):
        raise AqdAuditContractSchemaError(f"{field_name} must be a Rank member")
    if rank > AQD_RANK_CEILING:
        raise AqdAuditContractSchemaError(f"{field_name} must not exceed CANDIDATE")


def _require_false(value: object, field_name: str) -> None:
    if value is not False:
        raise AqdAuditContractSchemaError(f"{field_name} must remain False")


def _require_non_empty(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise AqdAuditContractSchemaError(f"{field_name} must be a non-empty string")


def _require_proof_ref(proof_object_ref: object, proof_trace_ref: object, owner: str) -> None:
    if proof_object_ref != "":
        _require_non_empty(proof_object_ref, f"{owner}.proof_object_ref")
    if proof_trace_ref != "":
        _require_non_empty(proof_trace_ref, f"{owner}.proof_trace_ref")
    if not (
        isinstance(proof_object_ref, str)
        and proof_object_ref.strip()
        or isinstance(proof_trace_ref, str)
        and proof_trace_ref.strip()
    ):
        raise AqdAuditContractSchemaError(
            f"{owner} requires proof_object_ref or proof_trace_ref"
        )


def _validate_forbidden_outputs(forbidden_outputs: object, owner: str) -> None:
    if not isinstance(forbidden_outputs, frozenset):
        raise AqdAuditContractSchemaError(f"{owner}.forbidden_outputs must be a frozenset")
    if not forbidden_outputs:
        raise AqdAuditContractSchemaError(f"{owner}.forbidden_outputs must be non-empty")
    for output in forbidden_outputs:
        _require_non_empty(output, f"{owner}.forbidden_outputs entry")
    missing = AQD_FORBIDDEN_OUTPUTS - forbidden_outputs
    if missing:
        raise AqdAuditContractSchemaError(
            f"{owner}.forbidden_outputs is missing required blockers: {sorted(missing)}"
        )


def _validate_residuals(residuals: object, field_name: str) -> None:
    if not isinstance(residuals, frozenset):
        raise AqdAuditContractSchemaError(f"{field_name} must be a frozenset")
    for residual in residuals:
        _require_non_empty(residual, f"{field_name} entry")


__all__ = [
    "AQD_AUDIT_STATUSES",
    "AQD_FORBIDDEN_OUTPUTS",
    "AQD_RANK_CEILING",
    "AqdAttributeContract",
    "AqdAuditContractSchemaError",
    "AqdAuditResult",
    "AqdInflectionAuditContract",
    "AqdMorphologicalBranchContract",
    "AqdPartialBranchContract",
    "AqdRelationTripletContract",
    "AqdReverseAuditContract",
    "AqdTemporalBindingContract",
    "AqdUniversalContract",
]
