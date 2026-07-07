"""G0-C2 hard-blocker gates (docs/77 §7).

Binding: docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md §7, §13.
Chain position: G0-C2 (hard-blocker gates only).
Forbidden: distance computation (G0-C3+), ontological/rank decisions, ḥukm/truth outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Literal

from taaqqul_slot_geometry.core import FailureCode, Rank
from taaqqul_slot_geometry.g0_c1_carriers import BareJamidStemCandidate


class G0C2GateSchemaError(TypeError):
    """Raised when the G0-C2 gate surface is malformed."""


class G0HardBlocker(StrEnum):
    """Hard blockers from docs/77 §7."""

    DUAL_PRESENT = "DUAL_PRESENT"
    PLURAL_PRESENT = "PLURAL_PRESENT"
    NISBAH_PRESENT = "NISBAH_PRESENT"
    SINAI_MASDAR_PRESENT = "SINAI_MASDAR_PRESENT"
    VERBAL_FORM_OR_TENSE_PRESENT = "VERBAL_FORM_OR_TENSE_PRESENT"
    EVENT_MASDAR_PRESENT = "EVENT_MASDAR_PRESENT"
    DERIVATION_PRESENT = "DERIVATION_PRESENT"
    MAJAZ_REQUIRED = "MAJAZ_REQUIRED"
    TERMINOLOGICAL_NAQL_REQUIRED = "TERMINOLOGICAL_NAQL_REQUIRED"
    CONTEXT_POLYSEMY_REQUIRED = "CONTEXT_POLYSEMY_REQUIRED"


class G0HardBlockerGateState(StrEnum):
    """Bounded G0-C2 gate state vocabulary."""

    PASSED = "PASSED"
    FORBIDDEN = "FORBIDDEN"
    DEFERRED = "DEFERRED"


class G0HardBlockerResidualKind(StrEnum):
    """Local visible residual vocabulary for G0-C2."""

    HARD_BLOCKER_PRESENT = "HARD_BLOCKER_PRESENT"
    CONTEXT_POLYSEMY_DEFERRED = "CONTEXT_POLYSEMY_DEFERRED"


G0_C2_ALLOWED_OUTPUT: Final[str] = "G0_HARD_BLOCKER_GATE_RESULT"
G0_C2_RANK_CEILING: Final[Rank] = Rank.ZERO
G0_C2_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "G0BoundedDistanceComputation",
    "G0OntologicalClassifier",
    "G0EpistemicRanker",
    "G0AnchorCertificateIssuance",
    "HukmVerdict",
    "TruthCertificate",
    "CertaintyCertificate",
    "RealityClaim",
)


def _require_trace_ref(owner: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise G0C2GateSchemaError(
            f"{owner}.{field_name} must be a non-empty string ({FailureCode.TRACE_MISSING.value})"
        )
    if not value.startswith("trace://"):
        raise G0C2GateSchemaError(
            f"{owner}.{field_name} must start with 'trace://' ({FailureCode.TRACE_MISSING.value})"
        )


def _validate_forbidden_outputs(owner: str, forbidden_outputs: tuple[str, ...]) -> None:
    if not isinstance(forbidden_outputs, tuple):
        raise G0C2GateSchemaError(
            f"{owner}.forbidden_outputs must be tuple ({FailureCode.BOUNDARY_MISSING.value})"
        )
    for item in forbidden_outputs:
        if not isinstance(item, str) or not item.strip():
            raise G0C2GateSchemaError(
                f"{owner}.forbidden_outputs must contain non-empty strings "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class G0HardBlockerResidual:
    """Visible G0-C2 residual entry."""

    kind: G0HardBlockerResidualKind
    blocker: G0HardBlocker
    trace_ref: str
    message: str
    blocking: bool

    def __post_init__(self) -> None:
        if not isinstance(self.kind, G0HardBlockerResidualKind):
            raise G0C2GateSchemaError(
                "G0HardBlockerResidual.kind must be G0HardBlockerResidualKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.blocker, G0HardBlocker):
            raise G0C2GateSchemaError(
                "G0HardBlockerResidual.blocker must be G0HardBlocker "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_trace_ref("G0HardBlockerResidual", "trace_ref", self.trace_ref)
        if not isinstance(self.message, str) or not self.message.strip():
            raise G0C2GateSchemaError(
                "G0HardBlockerResidual.message must be a non-empty string "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise G0C2GateSchemaError(
                "G0HardBlockerResidual.blocking must be bool "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class G0HardBlockerGateResult:
    """Bounded G0-C2 gate output (never distance/ranker/certificate issuance)."""

    state: G0HardBlockerGateState
    candidate_ref: str
    detected_blockers: tuple[G0HardBlocker, ...]
    residuals: tuple[G0HardBlockerResidual, ...]
    failure_code: FailureCode | None
    rank: Rank
    trace_ref: str
    output: Literal["G0_HARD_BLOCKER_GATE_RESULT"] = G0_C2_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = G0_C2_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, G0HardBlockerGateState):
            raise G0C2GateSchemaError(
                "G0HardBlockerGateResult.state must be G0HardBlockerGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_trace_ref("G0HardBlockerGateResult", "candidate_ref", self.candidate_ref)
        if not isinstance(self.detected_blockers, tuple):
            raise G0C2GateSchemaError(
                "G0HardBlockerGateResult.detected_blockers must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for blocker in self.detected_blockers:
            if not isinstance(blocker, G0HardBlocker):
                raise G0C2GateSchemaError(
                    "G0HardBlockerGateResult.detected_blockers must contain G0HardBlocker "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        if len(self.detected_blockers) != len(set(self.detected_blockers)):
            raise G0C2GateSchemaError(
                "G0HardBlockerGateResult.detected_blockers must not contain duplicates "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise G0C2GateSchemaError(
                "G0HardBlockerGateResult.residuals must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, G0HardBlockerResidual):
                raise G0C2GateSchemaError(
                    "G0HardBlockerGateResult.residuals must contain G0HardBlockerResidual "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise G0C2GateSchemaError(
                "G0HardBlockerGateResult.failure_code must be FailureCode or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.rank is not G0_C2_RANK_CEILING:
            raise G0C2GateSchemaError(
                "G0HardBlockerGateResult.rank must stay at Rank.ZERO "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        _require_trace_ref("G0HardBlockerGateResult", "trace_ref", self.trace_ref)
        if self.output != G0_C2_ALLOWED_OUTPUT:
            raise G0C2GateSchemaError(
                "G0HardBlockerGateResult.output must stay inside G0-C2 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs("G0HardBlockerGateResult", self.forbidden_outputs)

        has_blocking = any(residual.blocking for residual in self.residuals)
        has_non_blocking = any(not residual.blocking for residual in self.residuals)
        has_context_only = (
            bool(self.detected_blockers)
            and set(self.detected_blockers) == {G0HardBlocker.CONTEXT_POLYSEMY_REQUIRED}
        )

        if self.state is G0HardBlockerGateState.PASSED:
            if self.detected_blockers:
                raise G0C2GateSchemaError(
                    "PASSED state must not carry blockers "
                    f"({FailureCode.BLOCKING_RESIDUAL_PRESENT.value})"
                )
            if self.residuals or self.failure_code is not None:
                raise G0C2GateSchemaError(
                    "PASSED state must not carry residuals/failure_code "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )

        if self.state is G0HardBlockerGateState.FORBIDDEN:
            if has_context_only:
                raise G0C2GateSchemaError(
                    "FORBIDDEN state is invalid for context-only blocker "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if not self.detected_blockers or not has_blocking:
                raise G0C2GateSchemaError(
                    "FORBIDDEN state requires blockers with visible blocking residuals "
                    f"({FailureCode.BLOCKING_RESIDUAL_PRESENT.value})"
                )
            if self.failure_code is not FailureCode.BLOCKING_RESIDUAL_PRESENT:
                raise G0C2GateSchemaError(
                    "FORBIDDEN state must name BLOCKING_RESIDUAL_PRESENT "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0HardBlockerGateState.DEFERRED:
            if not has_context_only or not has_non_blocking or has_blocking:
                raise G0C2GateSchemaError(
                    "DEFERRED state requires context-only blocker and visible non-blocking residual "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if self.failure_code is not FailureCode.GATE_REQUIRED:
                raise G0C2GateSchemaError(
                    "DEFERRED state must name GATE_REQUIRED "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )


def _build_residual(
    *,
    blocker: G0HardBlocker,
    trace_ref: str,
) -> G0HardBlockerResidual:
    is_context = blocker is G0HardBlocker.CONTEXT_POLYSEMY_REQUIRED
    return G0HardBlockerResidual(
        kind=(
            G0HardBlockerResidualKind.CONTEXT_POLYSEMY_DEFERRED
            if is_context
            else G0HardBlockerResidualKind.HARD_BLOCKER_PRESENT
        ),
        blocker=blocker,
        trace_ref=f"{trace_ref}/residual/{blocker.value.lower()}",
        message=(
            "context required for polysemy resolution; defer to upper layers"
            if is_context
            else "hard blocker present before distance; forbid G0 licensing"
        ),
        blocking=not is_context,
    )


def prove_g0_hard_blocker_gates(
    candidate: BareJamidStemCandidate,
    *,
    detected_blockers: tuple[G0HardBlocker, ...],
    trace_ref: str,
) -> G0HardBlockerGateResult:
    """Run docs/77 §7 hard-blocker gate before distance/ranking steps."""

    if not isinstance(candidate, BareJamidStemCandidate):
        raise G0C2GateSchemaError(
            "prove_g0_hard_blocker_gates requires BareJamidStemCandidate "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(detected_blockers, tuple):
        raise G0C2GateSchemaError(
            "prove_g0_hard_blocker_gates.detected_blockers must be tuple "
            f"({FailureCode.BOUNDARY_MISSING.value})"
        )
    for blocker in detected_blockers:
        if not isinstance(blocker, G0HardBlocker):
            raise G0C2GateSchemaError(
                "prove_g0_hard_blocker_gates.detected_blockers entries must be G0HardBlocker "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
    if len(detected_blockers) != len(set(detected_blockers)):
        raise G0C2GateSchemaError(
            "prove_g0_hard_blocker_gates.detected_blockers must not contain duplicates "
            f"({FailureCode.BOUNDARY_MISSING.value})"
        )
    _require_trace_ref("prove_g0_hard_blocker_gates", "trace_ref", trace_ref)

    if not detected_blockers:
        return G0HardBlockerGateResult(
            state=G0HardBlockerGateState.PASSED,
            candidate_ref=candidate.trace_ref,
            detected_blockers=(),
            residuals=(),
            failure_code=None,
            rank=G0_C2_RANK_CEILING,
            trace_ref=trace_ref,
        )

    has_forbidden = any(
        blocker is not G0HardBlocker.CONTEXT_POLYSEMY_REQUIRED for blocker in detected_blockers
    )
    residuals = tuple(_build_residual(blocker=blocker, trace_ref=trace_ref) for blocker in detected_blockers)

    if has_forbidden:
        return G0HardBlockerGateResult(
            state=G0HardBlockerGateState.FORBIDDEN,
            candidate_ref=candidate.trace_ref,
            detected_blockers=detected_blockers,
            residuals=residuals,
            failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
            rank=G0_C2_RANK_CEILING,
            trace_ref=trace_ref,
        )

    return G0HardBlockerGateResult(
        state=G0HardBlockerGateState.DEFERRED,
        candidate_ref=candidate.trace_ref,
        detected_blockers=detected_blockers,
        residuals=residuals,
        failure_code=FailureCode.GATE_REQUIRED,
        rank=G0_C2_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "G0C2GateSchemaError",
    "G0HardBlocker",
    "G0HardBlockerGateResult",
    "G0HardBlockerGateState",
    "G0HardBlockerResidual",
    "G0HardBlockerResidualKind",
    "G0_C2_ALLOWED_OUTPUT",
    "G0_C2_FORBIDDEN_OUTPUTS",
    "G0_C2_RANK_CEILING",
    "prove_g0_hard_blocker_gates",
]
