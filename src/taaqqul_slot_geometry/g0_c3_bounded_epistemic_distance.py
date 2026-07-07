"""G0-C3 bounded epistemic distance computation (docs/77 §6).

Binding: docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md §6, §13.
Chain position: G0-C3 (distance computation only after G0-C2 PASSED).
Forbidden: ontological classifier/ranker decisions, anchor issuance, ḥukm/truth outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import sqrt
from typing import Final, Literal

from taaqqul_slot_geometry.core import FailureCode, Rank
from taaqqul_slot_geometry.g0_c1_carriers import (
    BareJamidStemCandidate,
    EpistemicRank,
    LexicalTruthStatus,
    StemGender,
)
from taaqqul_slot_geometry.g0_c2_hard_blocker_gates import (
    G0HardBlockerGateResult,
    G0HardBlockerGateState,
)


class G0C3DistanceSchemaError(TypeError):
    """Raised when the G0-C3 distance surface is malformed."""


class G0DistanceBand(StrEnum):
    """Bounded G0-C3 distance verdict bands from docs/77 §6."""

    FULL_REAL_ORIGIN = "FULL_REAL_ORIGIN"
    LICENSED_SILENT_RESIDUAL = "LICENSED_SILENT_RESIDUAL"
    LICENSED_CONDITIONAL_VISIBLE_RESIDUAL = "LICENSED_CONDITIONAL_VISIBLE_RESIDUAL"
    SUSPENDED = "SUSPENDED"
    INSUFFICIENT = "INSUFFICIENT"


class G0DistanceResidualKind(StrEnum):
    """Local visible residual vocabulary for G0-C3."""

    CONDITIONAL_WITNESS_REQUIRED = "CONDITIONAL_WITNESS_REQUIRED"
    DISTANCE_SUSPENDED = "DISTANCE_SUSPENDED"
    DISTANCE_INSUFFICIENT = "DISTANCE_INSUFFICIENT"


G0_C3_ALLOWED_OUTPUT: Final[str] = "G0_BOUNDED_DISTANCE_RESULT"
G0_C3_RANK_CEILING: Final[Rank] = Rank.ZERO
G0_C3_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "G0OntologicalClassifier",
    "G0EpistemicRanker",
    "G0AnchorCertificateIssuance",
    "HukmVerdict",
    "TruthCertificate",
    "CertaintyCertificate",
    "RealityClaim",
)

_ALPHA_STEM_PURITY: Final[float] = 2.0
_BETA_JAMIDIYYAH: Final[float] = 2.0
_GAMMA_REAL_ASSIGNMENT: Final[float] = 3.0
_DELTA_ANCHOR_ATTESTATION: Final[float] = 2.0
_EPSILON_ONTOLOGY_MATCH: Final[float] = 2.0
_ZETA_GENDER_STEM_PROPERTY: Final[float] = 1.0
_ETA_EPISTEMIC_EVIDENCE: Final[float] = 2.0
_TOTAL_WEIGHT: Final[float] = (
    _ALPHA_STEM_PURITY
    + _BETA_JAMIDIYYAH
    + _GAMMA_REAL_ASSIGNMENT
    + _DELTA_ANCHOR_ATTESTATION
    + _EPSILON_ONTOLOGY_MATCH
    + _ZETA_GENDER_STEM_PROPERTY
    + _ETA_EPISTEMIC_EVIDENCE
)


def _require_trace_ref(owner: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise G0C3DistanceSchemaError(
            f"{owner}.{field_name} must be a non-empty string ({FailureCode.TRACE_MISSING.value})"
        )
    if not value.startswith("trace://"):
        raise G0C3DistanceSchemaError(
            f"{owner}.{field_name} must start with 'trace://' ({FailureCode.TRACE_MISSING.value})"
        )


def _validate_forbidden_outputs(owner: str, forbidden_outputs: tuple[str, ...]) -> None:
    if not isinstance(forbidden_outputs, tuple):
        raise G0C3DistanceSchemaError(
            f"{owner}.forbidden_outputs must be tuple ({FailureCode.BOUNDARY_MISSING.value})"
        )
    for item in forbidden_outputs:
        if not isinstance(item, str) or not item.strip():
            raise G0C3DistanceSchemaError(
                f"{owner}.forbidden_outputs must contain non-empty strings "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )


def _require_unit_interval(owner: str, field_name: str, value: float) -> None:
    if not isinstance(value, float) or not (0.0 <= value <= 1.0):
        raise G0C3DistanceSchemaError(
            f"{owner}.{field_name} must be a float in [0.0, 1.0] "
            f"({FailureCode.BOUNDARY_MISSING.value})"
        )


def _dimension_real_assignment(status: LexicalTruthStatus) -> float:
    if status is LexicalTruthStatus.ATTESTED:
        return 1.0
    if status is LexicalTruthStatus.CANDIDATE:
        return 0.5
    return 0.0


def _dimension_gender_stem_property(gender: StemGender) -> float:
    return 0.5 if gender is StemGender.COMMON else 1.0


def _dimension_epistemic_evidence(rank: EpistemicRank) -> float:
    mapping = {
        EpistemicRank.E0: 0.0,
        EpistemicRank.E1: 0.2,
        EpistemicRank.E2: 0.4,
        EpistemicRank.E3: 0.6,
        EpistemicRank.E4: 0.8,
        EpistemicRank.E5: 1.0,
    }
    return mapping[rank]


@dataclass(frozen=True, slots=True)
class G0DistanceResidual:
    """Visible G0-C3 residual entry."""

    kind: G0DistanceResidualKind
    trace_ref: str
    message: str
    blocking: bool

    def __post_init__(self) -> None:
        if not isinstance(self.kind, G0DistanceResidualKind):
            raise G0C3DistanceSchemaError(
                "G0DistanceResidual.kind must be G0DistanceResidualKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_trace_ref("G0DistanceResidual", "trace_ref", self.trace_ref)
        if not isinstance(self.message, str) or not self.message.strip():
            raise G0C3DistanceSchemaError(
                "G0DistanceResidual.message must be a non-empty string "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise G0C3DistanceSchemaError(
                "G0DistanceResidual.blocking must be bool ({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class G0BoundedDistanceResult:
    """Bounded G0-C3 output (distance only; never classifier/ranker/certification)."""

    state: G0DistanceBand
    candidate_ref: str
    upstream_gate_state: G0HardBlockerGateState
    distance: float
    residuals: tuple[G0DistanceResidual, ...]
    failure_code: FailureCode | None
    rank: Rank
    trace_ref: str
    output: Literal["G0_BOUNDED_DISTANCE_RESULT"] = G0_C3_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = G0_C3_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, G0DistanceBand):
            raise G0C3DistanceSchemaError(
                "G0BoundedDistanceResult.state must be G0DistanceBand "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_trace_ref("G0BoundedDistanceResult", "candidate_ref", self.candidate_ref)
        if self.upstream_gate_state is not G0HardBlockerGateState.PASSED:
            raise G0C3DistanceSchemaError(
                "G0BoundedDistanceResult.upstream_gate_state must be PASSED "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_unit_interval("G0BoundedDistanceResult", "distance", self.distance)
        if not isinstance(self.residuals, tuple):
            raise G0C3DistanceSchemaError(
                "G0BoundedDistanceResult.residuals must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, G0DistanceResidual):
                raise G0C3DistanceSchemaError(
                    "G0BoundedDistanceResult.residuals must contain G0DistanceResidual "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise G0C3DistanceSchemaError(
                "G0BoundedDistanceResult.failure_code must be FailureCode or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.rank is not G0_C3_RANK_CEILING:
            raise G0C3DistanceSchemaError(
                "G0BoundedDistanceResult.rank must stay at Rank.ZERO "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        _require_trace_ref("G0BoundedDistanceResult", "trace_ref", self.trace_ref)
        if self.output != G0_C3_ALLOWED_OUTPUT:
            raise G0C3DistanceSchemaError(
                "G0BoundedDistanceResult.output must stay inside G0-C3 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs("G0BoundedDistanceResult", self.forbidden_outputs)

        has_blocking = any(residual.blocking for residual in self.residuals)
        has_non_blocking = any(not residual.blocking for residual in self.residuals)

        if (
            self.state
            in {
                G0DistanceBand.FULL_REAL_ORIGIN,
                G0DistanceBand.LICENSED_SILENT_RESIDUAL,
            }
            and (self.residuals or self.failure_code is not None)
        ):
            raise G0C3DistanceSchemaError(
                "Full/silent licensed bands must not carry residuals/failure_code "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )

        if self.state is G0DistanceBand.LICENSED_CONDITIONAL_VISIBLE_RESIDUAL:
            if not self.residuals or has_blocking:
                raise G0C3DistanceSchemaError(
                    "Conditional band requires visible non-blocking residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            if self.failure_code is not None:
                raise G0C3DistanceSchemaError(
                    "Conditional band must not carry failure_code "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0DistanceBand.SUSPENDED:
            if not self.residuals or has_blocking or not has_non_blocking:
                raise G0C3DistanceSchemaError(
                    "Suspended band requires visible non-blocking residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            if self.failure_code is not FailureCode.GATE_REQUIRED:
                raise G0C3DistanceSchemaError(
                    "Suspended band must name GATE_REQUIRED "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0DistanceBand.INSUFFICIENT:
            if not self.residuals or not has_blocking:
                raise G0C3DistanceSchemaError(
                    "Insufficient band requires visible blocking residuals "
                    f"({FailureCode.BLOCKING_RESIDUAL_PRESENT.value})"
                )
            if self.failure_code is not FailureCode.BLOCKING_RESIDUAL_PRESENT:
                raise G0C3DistanceSchemaError(
                    "Insufficient band must name BLOCKING_RESIDUAL_PRESENT "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )


def _compute_distance(candidate: BareJamidStemCandidate) -> float:
    stem_purity = 1.0 - candidate.d_form
    jamidiyyah = 1.0 if candidate.jamid else 0.0
    real_assignment = _dimension_real_assignment(candidate.lexical_truth_status)
    anchor_attestation = 1.0 - candidate.d_wad
    ontology_match = 1.0 - candidate.d_onto
    gender_stem_property = _dimension_gender_stem_property(candidate.gender)
    epistemic_evidence = _dimension_epistemic_evidence(candidate.epistemic_rank)

    return sqrt(
        (
            _ALPHA_STEM_PURITY * (1.0 - stem_purity) ** 2
            + _BETA_JAMIDIYYAH * (1.0 - jamidiyyah) ** 2
            + _GAMMA_REAL_ASSIGNMENT * (1.0 - real_assignment) ** 2
            + _DELTA_ANCHOR_ATTESTATION * (1.0 - anchor_attestation) ** 2
            + _EPSILON_ONTOLOGY_MATCH * (1.0 - ontology_match) ** 2
            + _ZETA_GENDER_STEM_PROPERTY * (1.0 - gender_stem_property) ** 2
            + _ETA_EPISTEMIC_EVIDENCE * (1.0 - epistemic_evidence) ** 2
        )
        / _TOTAL_WEIGHT
    )


def _residual(
    kind: G0DistanceResidualKind,
    trace_ref: str,
    message: str,
    *,
    blocking: bool,
) -> G0DistanceResidual:
    return G0DistanceResidual(
        kind=kind,
        trace_ref=f"{trace_ref}/residual/{kind.value.lower()}",
        message=message,
        blocking=blocking,
    )


def compute_g0_bounded_epistemic_distance(
    candidate: BareJamidStemCandidate,
    *,
    hard_blocker_verdict: G0HardBlockerGateResult,
    trace_ref: str,
) -> G0BoundedDistanceResult:
    """Compute docs/77 §6 bounded distance after a PASSED G0-C2 gate."""

    if not isinstance(candidate, BareJamidStemCandidate):
        raise G0C3DistanceSchemaError(
            "compute_g0_bounded_epistemic_distance requires BareJamidStemCandidate "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(hard_blocker_verdict, G0HardBlockerGateResult):
        raise G0C3DistanceSchemaError(
            "compute_g0_bounded_epistemic_distance.hard_blocker_verdict must be "
            f"G0HardBlockerGateResult ({FailureCode.GATE_REQUIRED.value})"
        )
    _require_trace_ref("compute_g0_bounded_epistemic_distance", "trace_ref", trace_ref)
    if hard_blocker_verdict.state is not G0HardBlockerGateState.PASSED:
        raise G0C3DistanceSchemaError(
            "compute_g0_bounded_epistemic_distance requires PASSED hard_blocker_verdict "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    distance = _compute_distance(candidate)

    if distance <= 0.10:
        return G0BoundedDistanceResult(
            state=G0DistanceBand.FULL_REAL_ORIGIN,
            candidate_ref=candidate.trace_ref,
            upstream_gate_state=hard_blocker_verdict.state,
            distance=distance,
            residuals=(),
            failure_code=None,
            rank=G0_C3_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if distance <= 0.25:
        return G0BoundedDistanceResult(
            state=G0DistanceBand.LICENSED_SILENT_RESIDUAL,
            candidate_ref=candidate.trace_ref,
            upstream_gate_state=hard_blocker_verdict.state,
            distance=distance,
            residuals=(),
            failure_code=None,
            rank=G0_C3_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if distance <= 0.40:
        return G0BoundedDistanceResult(
            state=G0DistanceBand.LICENSED_CONDITIONAL_VISIBLE_RESIDUAL,
            candidate_ref=candidate.trace_ref,
            upstream_gate_state=hard_blocker_verdict.state,
            distance=distance,
            residuals=(
                _residual(
                    G0DistanceResidualKind.CONDITIONAL_WITNESS_REQUIRED,
                    trace_ref,
                    "distance in conditional band; stronger witness required "
                    "before anchor issuance",
                    blocking=False,
                ),
            ),
            failure_code=None,
            rank=G0_C3_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if distance <= 0.60:
        return G0BoundedDistanceResult(
            state=G0DistanceBand.SUSPENDED,
            candidate_ref=candidate.trace_ref,
            upstream_gate_state=hard_blocker_verdict.state,
            distance=distance,
            residuals=(
                _residual(
                    G0DistanceResidualKind.DISTANCE_SUSPENDED,
                    trace_ref,
                    "distance in suspended band; assignment proof must be strengthened",
                    blocking=False,
                ),
            ),
            failure_code=FailureCode.GATE_REQUIRED,
            rank=G0_C3_RANK_CEILING,
            trace_ref=trace_ref,
        )

    return G0BoundedDistanceResult(
        state=G0DistanceBand.INSUFFICIENT,
        candidate_ref=candidate.trace_ref,
        upstream_gate_state=hard_blocker_verdict.state,
        distance=distance,
        residuals=(
            _residual(
                G0DistanceResidualKind.DISTANCE_INSUFFICIENT,
                trace_ref,
                "distance exceeds licensed bound; refuse progression to classifier/ranker stages",
                blocking=True,
            ),
        ),
        failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
        rank=G0_C3_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "G0BoundedDistanceResult",
    "G0C3DistanceSchemaError",
    "G0DistanceBand",
    "G0DistanceResidual",
    "G0DistanceResidualKind",
    "G0_C3_ALLOWED_OUTPUT",
    "G0_C3_FORBIDDEN_OUTPUTS",
    "G0_C3_RANK_CEILING",
    "compute_g0_bounded_epistemic_distance",
]
