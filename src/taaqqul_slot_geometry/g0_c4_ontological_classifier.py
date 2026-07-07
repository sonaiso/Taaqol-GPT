"""G0-C4 ontological classifier (docs/77 §3, §13).

Binding: docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md §3, §13.
Chain position: G0-C4 (ontological classifier only after G0-C3 output).
Forbidden: epistemic ranker decisions, anchor issuance, ḥukm/truth outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Literal

from taaqqul_slot_geometry.core import FailureCode, Rank
from taaqqul_slot_geometry.g0_c1_carriers import BareJamidStemCandidate, OntologicalClass
from taaqqul_slot_geometry.g0_c3_bounded_epistemic_distance import (
    G0BoundedDistanceResult,
    G0DistanceBand,
)


class G0C4ClassifierSchemaError(TypeError):
    """Raised when the G0-C4 classifier surface is malformed."""


class G0OntologicalClassifierState(StrEnum):
    """Bounded G0-C4 state vocabulary."""

    CLASSIFIED = "CLASSIFIED"
    DEFERRED = "DEFERRED"
    FORBIDDEN = "FORBIDDEN"


class G0OntologicalResidualKind(StrEnum):
    """Local visible residual vocabulary for G0-C4."""

    CONDITIONAL_DISTANCE_WITNESS_REQUIRED = "CONDITIONAL_DISTANCE_WITNESS_REQUIRED"
    UPSTREAM_DISTANCE_SUSPENDED = "UPSTREAM_DISTANCE_SUSPENDED"
    UPSTREAM_DISTANCE_INSUFFICIENT = "UPSTREAM_DISTANCE_INSUFFICIENT"


G0_C4_ALLOWED_OUTPUT: Final[str] = "G0_ONTOLOGICAL_CLASSIFIER_RESULT"
G0_C4_RANK_CEILING: Final[Rank] = Rank.ZERO
G0_C4_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "G0EpistemicRanker",
    "G0AnchorCertificateIssuance",
    "HukmVerdict",
    "TruthCertificate",
    "CertaintyCertificate",
    "RealityClaim",
)


def _require_trace_ref(owner: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise G0C4ClassifierSchemaError(
            f"{owner}.{field_name} must be a non-empty string ({FailureCode.TRACE_MISSING.value})"
        )
    if not value.startswith("trace://"):
        raise G0C4ClassifierSchemaError(
            f"{owner}.{field_name} must start with 'trace://' ({FailureCode.TRACE_MISSING.value})"
        )


def _validate_forbidden_outputs(owner: str, forbidden_outputs: tuple[str, ...]) -> None:
    if not isinstance(forbidden_outputs, tuple):
        raise G0C4ClassifierSchemaError(
            f"{owner}.forbidden_outputs must be tuple ({FailureCode.BOUNDARY_MISSING.value})"
        )
    for item in forbidden_outputs:
        if not isinstance(item, str) or not item.strip():
            raise G0C4ClassifierSchemaError(
                f"{owner}.forbidden_outputs must contain non-empty strings "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class G0OntologicalResidual:
    """Visible G0-C4 residual entry."""

    kind: G0OntologicalResidualKind
    trace_ref: str
    message: str
    blocking: bool

    def __post_init__(self) -> None:
        if not isinstance(self.kind, G0OntologicalResidualKind):
            raise G0C4ClassifierSchemaError(
                "G0OntologicalResidual.kind must be G0OntologicalResidualKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_trace_ref("G0OntologicalResidual", "trace_ref", self.trace_ref)
        if not isinstance(self.message, str) or not self.message.strip():
            raise G0C4ClassifierSchemaError(
                "G0OntologicalResidual.message must be a non-empty string "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise G0C4ClassifierSchemaError(
                "G0OntologicalResidual.blocking must be bool ({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class G0OntologicalClassifierResult:
    """Bounded G0-C4 output (classifier only; never ranker/certification)."""

    state: G0OntologicalClassifierState
    candidate_ref: str
    upstream_distance_state: G0DistanceBand
    ontological_class: OntologicalClass | None
    residuals: tuple[G0OntologicalResidual, ...]
    failure_code: FailureCode | None
    rank: Rank
    trace_ref: str
    output: Literal["G0_ONTOLOGICAL_CLASSIFIER_RESULT"] = G0_C4_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = G0_C4_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, G0OntologicalClassifierState):
            raise G0C4ClassifierSchemaError(
                "G0OntologicalClassifierResult.state must be G0OntologicalClassifierState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_trace_ref("G0OntologicalClassifierResult", "candidate_ref", self.candidate_ref)
        if not isinstance(self.upstream_distance_state, G0DistanceBand):
            raise G0C4ClassifierSchemaError(
                "G0OntologicalClassifierResult.upstream_distance_state must be G0DistanceBand "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.ontological_class is not None and not isinstance(
            self.ontological_class, OntologicalClass
        ):
            raise G0C4ClassifierSchemaError(
                "G0OntologicalClassifierResult.ontological_class must be OntologicalClass or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise G0C4ClassifierSchemaError(
                "G0OntologicalClassifierResult.residuals must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, G0OntologicalResidual):
                raise G0C4ClassifierSchemaError(
                    "G0OntologicalClassifierResult.residuals must contain G0OntologicalResidual "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise G0C4ClassifierSchemaError(
                "G0OntologicalClassifierResult.failure_code must be FailureCode or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.rank is not G0_C4_RANK_CEILING:
            raise G0C4ClassifierSchemaError(
                "G0OntologicalClassifierResult.rank must stay at Rank.ZERO "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        _require_trace_ref("G0OntologicalClassifierResult", "trace_ref", self.trace_ref)
        if self.output != G0_C4_ALLOWED_OUTPUT:
            raise G0C4ClassifierSchemaError(
                "G0OntologicalClassifierResult.output must stay inside G0-C4 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs("G0OntologicalClassifierResult", self.forbidden_outputs)

        has_blocking = any(residual.blocking for residual in self.residuals)
        has_non_blocking = any(not residual.blocking for residual in self.residuals)

        if self.state is G0OntologicalClassifierState.CLASSIFIED:
            if self.upstream_distance_state in {
                G0DistanceBand.SUSPENDED,
                G0DistanceBand.INSUFFICIENT,
            }:
                raise G0C4ClassifierSchemaError(
                    "CLASSIFIED state is invalid for suspended/insufficient upstream distance "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if self.ontological_class is None:
                raise G0C4ClassifierSchemaError(
                    "CLASSIFIED state requires ontological_class "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
            if self.upstream_distance_state is G0DistanceBand.LICENSED_CONDITIONAL_VISIBLE_RESIDUAL:
                if not self.residuals or has_blocking:
                    raise G0C4ClassifierSchemaError(
                        "Conditional upstream distance requires visible non-blocking residuals "
                        f"({FailureCode.HIDDEN_RESIDUAL.value})"
                    )
            elif self.residuals:
                raise G0C4ClassifierSchemaError(
                    "Non-conditional classified states must not carry residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            if self.failure_code is not None:
                raise G0C4ClassifierSchemaError(
                    "CLASSIFIED state must not carry failure_code "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0OntologicalClassifierState.DEFERRED:
            if self.upstream_distance_state is not G0DistanceBand.SUSPENDED:
                raise G0C4ClassifierSchemaError(
                    "DEFERRED state requires suspended upstream distance "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if self.ontological_class is not None:
                raise G0C4ClassifierSchemaError(
                    "DEFERRED state must not emit ontological_class "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
            if not self.residuals or has_blocking or not has_non_blocking:
                raise G0C4ClassifierSchemaError(
                    "DEFERRED state requires visible non-blocking residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            if self.failure_code is not FailureCode.GATE_REQUIRED:
                raise G0C4ClassifierSchemaError(
                    "DEFERRED state must name GATE_REQUIRED "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0OntologicalClassifierState.FORBIDDEN:
            if self.upstream_distance_state is not G0DistanceBand.INSUFFICIENT:
                raise G0C4ClassifierSchemaError(
                    "FORBIDDEN state requires insufficient upstream distance "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if self.ontological_class is not None:
                raise G0C4ClassifierSchemaError(
                    "FORBIDDEN state must not emit ontological_class "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
            if not self.residuals or not has_blocking:
                raise G0C4ClassifierSchemaError(
                    "FORBIDDEN state requires visible blocking residuals "
                    f"({FailureCode.BLOCKING_RESIDUAL_PRESENT.value})"
                )
            if self.failure_code is not FailureCode.BLOCKING_RESIDUAL_PRESENT:
                raise G0C4ClassifierSchemaError(
                    "FORBIDDEN state must name BLOCKING_RESIDUAL_PRESENT "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )


def _residual(
    kind: G0OntologicalResidualKind,
    trace_ref: str,
    message: str,
    *,
    blocking: bool,
) -> G0OntologicalResidual:
    return G0OntologicalResidual(
        kind=kind,
        trace_ref=f"{trace_ref}/residual/{kind.value.lower()}",
        message=message,
        blocking=blocking,
    )


def classify_g0_ontological_origin(
    candidate: BareJamidStemCandidate,
    *,
    bounded_distance_verdict: G0BoundedDistanceResult,
    trace_ref: str,
) -> G0OntologicalClassifierResult:
    """Classify docs/77 §3 ontological origin after a valid G0-C3 handoff."""

    if not isinstance(candidate, BareJamidStemCandidate):
        raise G0C4ClassifierSchemaError(
            "classify_g0_ontological_origin requires BareJamidStemCandidate "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(bounded_distance_verdict, G0BoundedDistanceResult):
        raise G0C4ClassifierSchemaError(
            "classify_g0_ontological_origin.bounded_distance_verdict must be "
            f"G0BoundedDistanceResult ({FailureCode.GATE_REQUIRED.value})"
        )
    _require_trace_ref("classify_g0_ontological_origin", "trace_ref", trace_ref)
    if bounded_distance_verdict.candidate_ref != candidate.trace_ref:
        raise G0C4ClassifierSchemaError(
            "classify_g0_ontological_origin requires candidate and "
            f"bounded_distance_verdict continuity ({FailureCode.IDENTITY_BROKEN.value})"
        )

    if bounded_distance_verdict.state in {
        G0DistanceBand.FULL_REAL_ORIGIN,
        G0DistanceBand.LICENSED_SILENT_RESIDUAL,
    }:
        return G0OntologicalClassifierResult(
            state=G0OntologicalClassifierState.CLASSIFIED,
            candidate_ref=candidate.trace_ref,
            upstream_distance_state=bounded_distance_verdict.state,
            ontological_class=candidate.ontological_class,
            residuals=(),
            failure_code=None,
            rank=G0_C4_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if bounded_distance_verdict.state is G0DistanceBand.LICENSED_CONDITIONAL_VISIBLE_RESIDUAL:
        return G0OntologicalClassifierResult(
            state=G0OntologicalClassifierState.CLASSIFIED,
            candidate_ref=candidate.trace_ref,
            upstream_distance_state=bounded_distance_verdict.state,
            ontological_class=candidate.ontological_class,
            residuals=(
                _residual(
                    G0OntologicalResidualKind.CONDITIONAL_DISTANCE_WITNESS_REQUIRED,
                    trace_ref,
                    "ontological classification emitted with conditional distance residual; "
                    "stronger witness still required before ranker/anchor stages",
                    blocking=False,
                ),
            ),
            failure_code=None,
            rank=G0_C4_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if bounded_distance_verdict.state is G0DistanceBand.SUSPENDED:
        return G0OntologicalClassifierResult(
            state=G0OntologicalClassifierState.DEFERRED,
            candidate_ref=candidate.trace_ref,
            upstream_distance_state=bounded_distance_verdict.state,
            ontological_class=None,
            residuals=(
                _residual(
                    G0OntologicalResidualKind.UPSTREAM_DISTANCE_SUSPENDED,
                    trace_ref,
                    "upstream distance is suspended; defer ontological classification finalization",
                    blocking=False,
                ),
            ),
            failure_code=FailureCode.GATE_REQUIRED,
            rank=G0_C4_RANK_CEILING,
            trace_ref=trace_ref,
        )

    return G0OntologicalClassifierResult(
        state=G0OntologicalClassifierState.FORBIDDEN,
        candidate_ref=candidate.trace_ref,
        upstream_distance_state=bounded_distance_verdict.state,
        ontological_class=None,
        residuals=(
            _residual(
                G0OntologicalResidualKind.UPSTREAM_DISTANCE_INSUFFICIENT,
                trace_ref,
                "upstream distance is insufficient; refuse progression "
                "to ranker/certificate stages",
                blocking=True,
            ),
        ),
        failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
        rank=G0_C4_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "G0_C4_ALLOWED_OUTPUT",
    "G0_C4_FORBIDDEN_OUTPUTS",
    "G0_C4_RANK_CEILING",
    "G0C4ClassifierSchemaError",
    "G0OntologicalClassifierResult",
    "G0OntologicalClassifierState",
    "G0OntologicalResidual",
    "G0OntologicalResidualKind",
    "classify_g0_ontological_origin",
]
