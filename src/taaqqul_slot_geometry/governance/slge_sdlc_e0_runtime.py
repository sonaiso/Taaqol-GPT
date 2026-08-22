"""SLGE-SDLC-E0 lifecycle transition execution runtime (current/future only)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SLGEE0SchemaError(TypeError):
    """Raised when E0 runtime inputs or outputs violate schema contracts."""


class SLGEE0DecisionState(StrEnum):
    """Bounded E0 decision vocabulary."""

    APPROVED = "APPROVED"
    REFUSED = "REFUSED"
    DEFERRED = "DEFERRED"
    SUSPENDED = "SUSPENDED"


class SLGEE0FailureCode(StrEnum):
    """Named fail-closed E0 refusal and deferral reasons."""

    TEMPORAL_CUT_VIOLATION = "TEMPORAL_CUT_VIOLATION"
    HISTORICAL_CERTIFICATION_FORBIDDEN = "HISTORICAL_CERTIFICATION_FORBIDDEN"
    HISTORICAL_MCLT_FABRICATION_FORBIDDEN = "HISTORICAL_MCLT_FABRICATION_FORBIDDEN"
    LEGACY_BASELINE_REQUIRED = "LEGACY_BASELINE_REQUIRED"
    REBUILD_REQUIRES_NEW_LINEAGE = "REBUILD_REQUIRES_NEW_LINEAGE"
    QUARANTINED_SOURCE = "QUARANTINED_SOURCE"
    UNCERTAIN_LEGACY_SLOT = "UNCERTAIN_LEGACY_SLOT"
    TRANSITION_NOT_LICENSED = "TRANSITION_NOT_LICENSED"
    EVIDENCE_INSUFFICIENT = "EVIDENCE_INSUFFICIENT"
    GATE_NOT_APPROVED = "GATE_NOT_APPROVED"
    BLOCKING_RESIDUAL = "BLOCKING_RESIDUAL"
    RESIDUAL_RESOLUTION_NOT_AUTHORIZED = "RESIDUAL_RESOLUTION_NOT_AUTHORIZED"
    RANK_AUTHORITY_EXCEEDED = "RANK_AUTHORITY_EXCEEDED"
    TRACE_LOSS = "TRACE_LOSS"
    BACKWARD_PROOF_FAILED = "BACKWARD_PROOF_FAILED"
    FORWARD_READINESS_FAILED = "FORWARD_READINESS_FAILED"
    TRIANGLE_COHERENCE_FAILED = "TRIANGLE_COHERENCE_FAILED"


class LegacyRemapDecision(StrEnum):
    """M0 remap decisions consumed by E0."""

    KEEP = "KEEP"
    RETYPE = "RETYPE"
    REORDER = "REORDER"
    QUARANTINE = "QUARANTINE"
    REBUILD = "REBUILD"


class HistoricalTransitionStatus(StrEnum):
    """Historical transition statuses inherited from M0."""

    PROVEN = "PROVEN"
    PARTIAL = "PARTIAL"
    UNASSESSED = "UNASSESSED"
    UNKNOWN = "UNKNOWN"
    REFUSED = "REFUSED"


T_SLGE_CUT_ID = "T_SLGE"
T_SLGE_ANCHOR_EVENT_ID = "SLGE-SDLC-M0"
T_SLGE_MIN_ORDER = 1280
E0_ALLOWED_FROM_SLOT = "SLGE-SDLC-M0"
E0_ALLOWED_TO_SLOT = "SLGE-SDLC-E0"
E0_NEXT_OPENING = "SLGE-SDLC-P0"
E0_AUTHORITY_CEILING = "ProjectionRuntimeAuthority"
E0_RANK_CEILING = "E1"
E0_REQUIRED_MCLT_PREDICATES: tuple[str, ...] = (
    "IdentityPreserved",
    "OriginPreserved",
    "DomainScopeValid",
    "TemporalPolicyValid",
    "SourceStateAdmissible",
    "TransitionContractValid",
    "PreconditionsSatisfied",
    "EvidenceAdequate",
    "GateApproved",
    "RankAuthorityBounded",
    "ResidualPolicySatisfied",
    "TraceReconstructible",
    "BackwardProofValid",
    "ForwardReadinessValid",
    "TriangleCoherenceValid",
)


@dataclass(frozen=True, slots=True)
class LegacyBaselineAnchor:
    """Bounded E0 baseline admission over legacy artifacts without history rewriting."""

    baseline_id: str
    artifact_id: str
    lineage_ref: str
    remap_record_id: str
    remap_decision: LegacyRemapDecision
    historical_transition_status: HistoricalTransitionStatus
    historical_mclt_ref: str | None
    unresolved_residual_refs: tuple[str, ...]
    uncertain_legacy_slot_mapping: bool
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_non_empty_str(cls, "baseline_id", self.baseline_id)
        _require_non_empty_str(cls, "artifact_id", self.artifact_id)
        _require_non_empty_str(cls, "lineage_ref", self.lineage_ref)
        _require_non_empty_str(cls, "remap_record_id", self.remap_record_id)
        _require_enum(cls, "remap_decision", self.remap_decision, LegacyRemapDecision)
        _require_enum(
            cls,
            "historical_transition_status",
            self.historical_transition_status,
            HistoricalTransitionStatus,
        )
        if self.historical_mclt_ref is not None:
            _require_non_empty_str(cls, "historical_mclt_ref", self.historical_mclt_ref)
        _require_unique_non_empty_str_tuple(
            cls,
            "unresolved_residual_refs",
            self.unresolved_residual_refs,
            allow_empty=True,
        )
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class TransitionAttempt:
    """Typed E0 transition attempt (current/future lifecycle transitions only)."""

    attempt_id: str
    artifact_id: str
    lineage_ref: str
    transition_contract_ref: str
    from_slot_ref: str
    to_slot_ref: str
    temporal_epoch_ref: str
    governance_order: int
    dependency_order: int
    identity_proof_ref: str
    origin_proof_ref: str
    domain_scope_proof_ref: str
    evidence_refs: tuple[str, ...]
    residual_refs: tuple[str, ...]
    blocking_residual_refs: tuple[str, ...]
    trace_ref: str
    backward_proof_ref: str
    forward_readiness_ref: str
    triangle_coherence_ref: str
    legacy_baseline_ref: str | None = None
    new_lineage_ref: str | None = None
    source_is_legacy: bool = False
    request_historical_certification: bool = False
    residual_resolution_requested: bool = False
    residual_resolution_authorized: bool = False
    rank_promotion_requested: bool = False
    rank_promotion_authorized: bool = False
    forbidden_skip_detected: bool = False
    identity_preserved: bool = False
    origin_preserved: bool = False
    domain_scope_valid: bool = False
    temporal_policy_valid: bool = False
    source_state_admissible: bool = False
    transition_contract_valid: bool = False
    preconditions_satisfied: bool = False
    evidence_adequate: bool = False
    gate_approved: bool = False
    rank_authority_bounded: bool = False
    residual_policy_satisfied: bool = False
    trace_reconstructible: bool = False
    backward_proof_valid: bool = False
    forward_readiness_valid: bool = False
    triangle_coherence_valid: bool = False

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        for name in (
            "attempt_id",
            "artifact_id",
            "lineage_ref",
            "transition_contract_ref",
            "from_slot_ref",
            "to_slot_ref",
            "temporal_epoch_ref",
            "identity_proof_ref",
            "origin_proof_ref",
            "domain_scope_proof_ref",
            "backward_proof_ref",
            "forward_readiness_ref",
            "triangle_coherence_ref",
        ):
            _require_non_empty_str(cls, name, getattr(self, name))
        _require_int(cls, "governance_order", self.governance_order)
        _require_int(cls, "dependency_order", self.dependency_order)
        _require_unique_non_empty_str_tuple(cls, "evidence_refs", self.evidence_refs)
        _require_unique_non_empty_str_tuple(
            cls,
            "residual_refs",
            self.residual_refs,
            allow_empty=True,
        )
        _require_unique_non_empty_str_tuple(
            cls,
            "blocking_residual_refs",
            self.blocking_residual_refs,
            allow_empty=True,
        )
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if self.legacy_baseline_ref is not None:
            _require_non_empty_str(cls, "legacy_baseline_ref", self.legacy_baseline_ref)
        if self.new_lineage_ref is not None:
            _require_non_empty_str(cls, "new_lineage_ref", self.new_lineage_ref)


@dataclass(frozen=True, slots=True)
class TransitionDecision:
    """Typed E0 transition decision output."""

    attempt_id: str
    state: SLGEE0DecisionState
    failure_codes: tuple[SLGEE0FailureCode, ...]
    authority_ceiling: str
    rank_ceiling: str
    consumed_residual_refs: tuple[str, ...]
    inherited_residual_refs: tuple[str, ...]
    blocking_residual_refs: tuple[str, ...]
    trace_ref: str
    next_openings: tuple[str, ...]
    historical_status_preserved: bool
    rank_promotion_granted: bool

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_non_empty_str(cls, "attempt_id", self.attempt_id)
        _require_enum(cls, "state", self.state, SLGEE0DecisionState)
        _require_unique_enum_tuple(
            cls,
            "failure_codes",
            self.failure_codes,
            SLGEE0FailureCode,
            allow_empty=True,
        )
        _require_non_empty_str(cls, "authority_ceiling", self.authority_ceiling)
        _require_non_empty_str(cls, "rank_ceiling", self.rank_ceiling)
        _require_unique_non_empty_str_tuple(
            cls,
            "consumed_residual_refs",
            self.consumed_residual_refs,
            allow_empty=True,
        )
        _require_unique_non_empty_str_tuple(
            cls,
            "inherited_residual_refs",
            self.inherited_residual_refs,
            allow_empty=True,
        )
        _require_unique_non_empty_str_tuple(
            cls,
            "blocking_residual_refs",
            self.blocking_residual_refs,
            allow_empty=True,
        )
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        _require_unique_non_empty_str_tuple(
            cls,
            "next_openings",
            self.next_openings,
            allow_empty=True,
        )

        if self.state is SLGEE0DecisionState.APPROVED and self.failure_codes:
            raise SLGEE0SchemaError(f"{cls}.APPROVED cannot carry failure_codes")
        if self.state is not SLGEE0DecisionState.APPROVED and not self.failure_codes:
            raise SLGEE0SchemaError(f"{cls} non-APPROVED states require failure_codes")
        if self.rank_promotion_granted:
            raise SLGEE0SchemaError(
                f"{cls}.rank_promotion_granted must remain false in SLGE-SDLC-E0"
            )


def evaluate_transition_attempt(
    attempt: TransitionAttempt,
    *,
    legacy_baseline: LegacyBaselineAnchor | None = None,
) -> TransitionDecision:
    """Evaluate an E0 lifecycle transition attempt with fail-closed semantics."""

    if not isinstance(attempt, TransitionAttempt):
        raise SLGEE0SchemaError("evaluate_transition_attempt requires TransitionAttempt")
    if legacy_baseline is not None and not isinstance(legacy_baseline, LegacyBaselineAnchor):
        raise SLGEE0SchemaError(
            "evaluate_transition_attempt.legacy_baseline must be LegacyBaselineAnchor or None"
        )

    codes: list[SLGEE0FailureCode] = []

    if attempt.from_slot_ref != E0_ALLOWED_FROM_SLOT or attempt.to_slot_ref != E0_ALLOWED_TO_SLOT:
        codes.append(SLGEE0FailureCode.TRANSITION_NOT_LICENSED)

    if attempt.governance_order < T_SLGE_MIN_ORDER or attempt.dependency_order < T_SLGE_MIN_ORDER:
        codes.append(SLGEE0FailureCode.TEMPORAL_CUT_VIOLATION)
    if not attempt.temporal_epoch_ref.startswith(f"{T_SLGE_CUT_ID}::"):
        codes.append(SLGEE0FailureCode.TEMPORAL_CUT_VIOLATION)

    if attempt.source_is_legacy and legacy_baseline is None:
        codes.append(SLGEE0FailureCode.LEGACY_BASELINE_REQUIRED)

    if legacy_baseline is not None:
        if (
            legacy_baseline.historical_transition_status is not HistoricalTransitionStatus.PROVEN
            and legacy_baseline.historical_mclt_ref is not None
        ):
            codes.append(SLGEE0FailureCode.HISTORICAL_MCLT_FABRICATION_FORBIDDEN)
        if (
            attempt.request_historical_certification
            and legacy_baseline.historical_transition_status
            is not HistoricalTransitionStatus.PROVEN
        ):
            codes.append(SLGEE0FailureCode.HISTORICAL_CERTIFICATION_FORBIDDEN)
        if legacy_baseline.uncertain_legacy_slot_mapping:
            codes.append(SLGEE0FailureCode.UNCERTAIN_LEGACY_SLOT)
        if legacy_baseline.remap_decision is LegacyRemapDecision.QUARANTINE:
            codes.append(SLGEE0FailureCode.QUARANTINED_SOURCE)
        if (
            legacy_baseline.remap_decision is LegacyRemapDecision.REBUILD
            and not attempt.new_lineage_ref
        ):
            codes.append(SLGEE0FailureCode.REBUILD_REQUIRES_NEW_LINEAGE)

    if not attempt.evidence_refs or not attempt.evidence_adequate:
        codes.append(SLGEE0FailureCode.EVIDENCE_INSUFFICIENT)
    if not attempt.trace_reconstructible:
        codes.append(SLGEE0FailureCode.TRACE_LOSS)
    if not attempt.gate_approved:
        codes.append(SLGEE0FailureCode.GATE_NOT_APPROVED)
    if attempt.blocking_residual_refs:
        codes.append(SLGEE0FailureCode.BLOCKING_RESIDUAL)
    if attempt.residual_resolution_requested and not attempt.residual_resolution_authorized:
        codes.append(SLGEE0FailureCode.RESIDUAL_RESOLUTION_NOT_AUTHORIZED)
    if attempt.rank_promotion_requested and (
        not attempt.rank_promotion_authorized
        or not attempt.rank_authority_bounded
        or not attempt.gate_approved
        or not attempt.evidence_adequate
        or attempt.forbidden_skip_detected
    ):
        codes.append(SLGEE0FailureCode.RANK_AUTHORITY_EXCEEDED)
    if not attempt.backward_proof_valid:
        codes.append(SLGEE0FailureCode.BACKWARD_PROOF_FAILED)
    if not attempt.forward_readiness_valid:
        codes.append(SLGEE0FailureCode.FORWARD_READINESS_FAILED)
    if not attempt.triangle_coherence_valid:
        codes.append(SLGEE0FailureCode.TRIANGLE_COHERENCE_FAILED)

    required_flags = (
        attempt.identity_preserved,
        attempt.origin_preserved,
        attempt.domain_scope_valid,
        attempt.temporal_policy_valid,
        attempt.source_state_admissible,
        attempt.transition_contract_valid,
        attempt.preconditions_satisfied,
        attempt.evidence_adequate,
        attempt.gate_approved,
        attempt.rank_authority_bounded,
        attempt.residual_policy_satisfied,
        attempt.trace_reconstructible,
        attempt.backward_proof_valid,
        attempt.forward_readiness_valid,
        attempt.triangle_coherence_valid,
    )
    if not all(required_flags):
        if not attempt.gate_approved and SLGEE0FailureCode.GATE_NOT_APPROVED not in codes:
            codes.append(SLGEE0FailureCode.GATE_NOT_APPROVED)
        if not attempt.evidence_adequate and SLGEE0FailureCode.EVIDENCE_INSUFFICIENT not in codes:
            codes.append(SLGEE0FailureCode.EVIDENCE_INSUFFICIENT)
        if not attempt.trace_reconstructible and SLGEE0FailureCode.TRACE_LOSS not in codes:
            codes.append(SLGEE0FailureCode.TRACE_LOSS)

    ordered_codes = tuple(dict.fromkeys(codes))
    inherited_residuals = _sorted_tuple(attempt.residual_refs)
    consumed_residuals = _sorted_tuple(
        tuple(
            residual_ref
            for residual_ref in attempt.residual_refs
            if residual_ref not in set(attempt.blocking_residual_refs)
        )
    )
    blocking_residuals = _sorted_tuple(attempt.blocking_residual_refs)

    if not ordered_codes:
        return TransitionDecision(
            attempt_id=attempt.attempt_id,
            state=SLGEE0DecisionState.APPROVED,
            failure_codes=(),
            authority_ceiling=E0_AUTHORITY_CEILING,
            rank_ceiling=E0_RANK_CEILING,
            consumed_residual_refs=consumed_residuals,
            inherited_residual_refs=inherited_residuals,
            blocking_residual_refs=blocking_residuals,
            trace_ref=attempt.trace_ref,
            next_openings=(E0_NEXT_OPENING,),
            historical_status_preserved=True,
            rank_promotion_granted=False,
        )

    state = SLGEE0DecisionState.REFUSED
    if SLGEE0FailureCode.QUARANTINED_SOURCE in ordered_codes:
        state = SLGEE0DecisionState.SUSPENDED
    elif (
        SLGEE0FailureCode.UNCERTAIN_LEGACY_SLOT in ordered_codes
        or SLGEE0FailureCode.FORWARD_READINESS_FAILED in ordered_codes
    ):
        state = SLGEE0DecisionState.DEFERRED

    return TransitionDecision(
        attempt_id=attempt.attempt_id,
        state=state,
        failure_codes=ordered_codes,
        authority_ceiling=E0_AUTHORITY_CEILING,
        rank_ceiling=E0_RANK_CEILING,
        consumed_residual_refs=consumed_residuals,
        inherited_residual_refs=inherited_residuals,
        blocking_residual_refs=blocking_residuals,
        trace_ref=attempt.trace_ref,
        next_openings=(),
        historical_status_preserved=True,
        rank_promotion_granted=False,
    )


def _sorted_tuple(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _require_non_empty_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_trace_ref(cls_name: str, field_name: str, value: object) -> None:
    _require_non_empty_str(cls_name, field_name, value)


def _require_int(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, int):
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} must be int")


def _require_enum(
    cls_name: str,
    field_name: str,
    value: object,
    enum_type: type[StrEnum],
) -> None:
    if not isinstance(value, enum_type):
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} must be {enum_type.__name__}")


def _require_unique_non_empty_str_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise SLGEE0SchemaError(
                f"{cls_name}.{field_name} entries must be non-empty strings"
            )
    if len(set(value)) != len(value):
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} entries must be unique")


def _require_unique_enum_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    enum_type: type[StrEnum],
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, enum_type):
            raise SLGEE0SchemaError(
                f"{cls_name}.{field_name} entries must be {enum_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise SLGEE0SchemaError(f"{cls_name}.{field_name} entries must be unique")


__all__ = [
    "E0_ALLOWED_FROM_SLOT",
    "E0_ALLOWED_TO_SLOT",
    "E0_AUTHORITY_CEILING",
    "E0_NEXT_OPENING",
    "E0_RANK_CEILING",
    "E0_REQUIRED_MCLT_PREDICATES",
    "HistoricalTransitionStatus",
    "LegacyBaselineAnchor",
    "LegacyRemapDecision",
    "SLGEE0DecisionState",
    "SLGEE0FailureCode",
    "SLGEE0SchemaError",
    "T_SLGE_ANCHOR_EVENT_ID",
    "T_SLGE_CUT_ID",
    "T_SLGE_MIN_ORDER",
    "TransitionAttempt",
    "TransitionDecision",
    "evaluate_transition_attempt",
]
