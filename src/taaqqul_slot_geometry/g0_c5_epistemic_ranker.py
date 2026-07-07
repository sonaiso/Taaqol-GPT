"""G0-C5 epistemic ranker (docs/77 §4).

Binding: docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md §4, §13.
Chain position: G0-C5 (epistemic ranking only after G0-C4 output).
Forbidden: anchor issuance, ḥukm/truth outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Literal

from taaqqul_slot_geometry.core import FailureCode, Rank
from taaqqul_slot_geometry.g0_c1_carriers import (
    BareJamidStemCandidate,
    EpistemicRank,
    OntologicalClass,
)
from taaqqul_slot_geometry.g0_c4_ontological_classifier import (
    G0OntologicalClassifierResult,
    G0OntologicalClassifierState,
)


class G0C5RankerSchemaError(TypeError):
    """Raised when the G0-C5 ranker surface is malformed."""


class G0EpistemicRankerState(StrEnum):
    """Bounded G0-C5 state vocabulary."""

    RANKED = "RANKED"
    DEFERRED = "DEFERRED"
    FORBIDDEN = "FORBIDDEN"


class G0EpistemicResidualKind(StrEnum):
    """Local visible residual vocabulary for G0-C5."""

    UPSTREAM_CLASSIFIER_CONDITIONAL = "UPSTREAM_CLASSIFIER_CONDITIONAL"
    UPSTREAM_CLASSIFIER_DEFERRED = "UPSTREAM_CLASSIFIER_DEFERRED"
    UPSTREAM_CLASSIFIER_FORBIDDEN = "UPSTREAM_CLASSIFIER_FORBIDDEN"
    NOMINATION_ONLY_E0 = "NOMINATION_ONLY_E0"
    REAL_MULTIPLICITY_UNDECIDED_E3 = "REAL_MULTIPLICITY_UNDECIDED_E3"
    INSUFFICIENT_WITNESS_E4 = "INSUFFICIENT_WITNESS_E4"
    CONTEXT_OR_TRANSFER_REQUIRED_E5 = "CONTEXT_OR_TRANSFER_REQUIRED_E5"


G0_C5_ALLOWED_OUTPUT: Final[str] = "G0_EPISTEMIC_RANKER_RESULT"
G0_C5_RANK_CEILING: Final[Rank] = Rank.ZERO
G0_C5_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "G0AnchorCertificateIssuance",
    "HukmVerdict",
    "TruthCertificate",
    "CertaintyCertificate",
    "RealityClaim",
)


def _require_trace_ref(owner: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise G0C5RankerSchemaError(
            f"{owner}.{field_name} must be a non-empty string ({FailureCode.TRACE_MISSING.value})"
        )
    if not value.startswith("trace://"):
        raise G0C5RankerSchemaError(
            f"{owner}.{field_name} must start with 'trace://' ({FailureCode.TRACE_MISSING.value})"
        )


def _validate_forbidden_outputs(owner: str, forbidden_outputs: tuple[str, ...]) -> None:
    if not isinstance(forbidden_outputs, tuple):
        raise G0C5RankerSchemaError(
            f"{owner}.forbidden_outputs must be tuple ({FailureCode.BOUNDARY_MISSING.value})"
        )
    for item in forbidden_outputs:
        if not isinstance(item, str) or not item.strip():
            raise G0C5RankerSchemaError(
                f"{owner}.forbidden_outputs must contain non-empty strings "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class G0EpistemicResidual:
    """Visible G0-C5 residual entry."""

    kind: G0EpistemicResidualKind
    trace_ref: str
    message: str
    blocking: bool

    def __post_init__(self) -> None:
        if not isinstance(self.kind, G0EpistemicResidualKind):
            raise G0C5RankerSchemaError(
                "G0EpistemicResidual.kind must be G0EpistemicResidualKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_trace_ref("G0EpistemicResidual", "trace_ref", self.trace_ref)
        if not isinstance(self.message, str) or not self.message.strip():
            raise G0C5RankerSchemaError(
                "G0EpistemicResidual.message must be a non-empty string "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise G0C5RankerSchemaError(
                "G0EpistemicResidual.blocking must be bool "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class G0EpistemicRankerResult:
    """Bounded G0-C5 output (ranker only; never anchor issuance)."""

    state: G0EpistemicRankerState
    candidate_ref: str
    upstream_classifier_state: G0OntologicalClassifierState
    ontological_class: OntologicalClass | None
    epistemic_rank: EpistemicRank | None
    residuals: tuple[G0EpistemicResidual, ...]
    failure_code: FailureCode | None
    rank: Rank
    trace_ref: str
    output: Literal["G0_EPISTEMIC_RANKER_RESULT"] = G0_C5_ALLOWED_OUTPUT
    forbidden_outputs: tuple[str, ...] = G0_C5_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, G0EpistemicRankerState):
            raise G0C5RankerSchemaError(
                "G0EpistemicRankerResult.state must be G0EpistemicRankerState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_trace_ref("G0EpistemicRankerResult", "candidate_ref", self.candidate_ref)
        if not isinstance(self.upstream_classifier_state, G0OntologicalClassifierState):
            raise G0C5RankerSchemaError(
                "G0EpistemicRankerResult.upstream_classifier_state must be "
                "G0OntologicalClassifierState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.ontological_class is not None and not isinstance(
            self.ontological_class, OntologicalClass
        ):
            raise G0C5RankerSchemaError(
                "G0EpistemicRankerResult.ontological_class must be OntologicalClass or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.epistemic_rank is not None and not isinstance(self.epistemic_rank, EpistemicRank):
            raise G0C5RankerSchemaError(
                "G0EpistemicRankerResult.epistemic_rank must be EpistemicRank or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise G0C5RankerSchemaError(
                "G0EpistemicRankerResult.residuals must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, G0EpistemicResidual):
                raise G0C5RankerSchemaError(
                    "G0EpistemicRankerResult.residuals must contain G0EpistemicResidual "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise G0C5RankerSchemaError(
                "G0EpistemicRankerResult.failure_code must be FailureCode or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.rank is not G0_C5_RANK_CEILING:
            raise G0C5RankerSchemaError(
                "G0EpistemicRankerResult.rank must stay at Rank.ZERO "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        _require_trace_ref("G0EpistemicRankerResult", "trace_ref", self.trace_ref)
        if self.output != G0_C5_ALLOWED_OUTPUT:
            raise G0C5RankerSchemaError(
                "G0EpistemicRankerResult.output must stay inside G0-C5 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs("G0EpistemicRankerResult", self.forbidden_outputs)

        has_blocking = any(residual.blocking for residual in self.residuals)
        has_non_blocking = any(not residual.blocking for residual in self.residuals)

        if self.state is G0EpistemicRankerState.RANKED:
            if self.upstream_classifier_state is not G0OntologicalClassifierState.CLASSIFIED:
                raise G0C5RankerSchemaError(
                    "RANKED state requires CLASSIFIED upstream classifier state "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if self.ontological_class is None:
                raise G0C5RankerSchemaError(
                    "RANKED state requires ontological_class "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
            if self.epistemic_rank not in {
                EpistemicRank.E1,
                EpistemicRank.E2,
                EpistemicRank.E3,
            }:
                raise G0C5RankerSchemaError(
                    "RANKED state requires epistemic_rank in {E1, E2, E3} "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if has_blocking:
                raise G0C5RankerSchemaError(
                    "RANKED state must not include blocking residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            if self.failure_code is not None:
                raise G0C5RankerSchemaError(
                    "RANKED state must not carry failure_code "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0EpistemicRankerState.DEFERRED:
            if self.upstream_classifier_state is G0OntologicalClassifierState.FORBIDDEN:
                raise G0C5RankerSchemaError(
                    "DEFERRED state is invalid for FORBIDDEN upstream classifier state "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if self.ontological_class is not None:
                raise G0C5RankerSchemaError(
                    "DEFERRED state must not emit ontological_class "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
            if self.epistemic_rank is not None:
                raise G0C5RankerSchemaError(
                    "DEFERRED state must not emit epistemic_rank "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
            if not self.residuals or has_blocking or not has_non_blocking:
                raise G0C5RankerSchemaError(
                    "DEFERRED state requires visible non-blocking residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            if self.failure_code is not FailureCode.GATE_REQUIRED:
                raise G0C5RankerSchemaError(
                    "DEFERRED state must name GATE_REQUIRED "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0EpistemicRankerState.FORBIDDEN:
            if self.ontological_class is not None:
                raise G0C5RankerSchemaError(
                    "FORBIDDEN state must not emit ontological_class "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
            if self.epistemic_rank is not None:
                raise G0C5RankerSchemaError(
                    "FORBIDDEN state must not emit epistemic_rank "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
            if not self.residuals or not has_blocking:
                raise G0C5RankerSchemaError(
                    "FORBIDDEN state requires visible blocking residuals "
                    f"({FailureCode.BLOCKING_RESIDUAL_PRESENT.value})"
                )
            if self.failure_code is not FailureCode.BLOCKING_RESIDUAL_PRESENT:
                raise G0C5RankerSchemaError(
                    "FORBIDDEN state must name BLOCKING_RESIDUAL_PRESENT "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )


def _residual(
    kind: G0EpistemicResidualKind,
    trace_ref: str,
    message: str,
    *,
    blocking: bool,
) -> G0EpistemicResidual:
    return G0EpistemicResidual(
        kind=kind,
        trace_ref=f"{trace_ref}/residual/{kind.value.lower()}",
        message=message,
        blocking=blocking,
    )


def rank_g0_epistemic_origin(
    candidate: BareJamidStemCandidate,
    *,
    ontological_classifier_verdict: G0OntologicalClassifierResult,
    trace_ref: str,
) -> G0EpistemicRankerResult:
    """Rank docs/77 §4 epistemic origin after a valid G0-C4 handoff."""

    if not isinstance(candidate, BareJamidStemCandidate):
        raise G0C5RankerSchemaError(
            "rank_g0_epistemic_origin requires BareJamidStemCandidate "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(ontological_classifier_verdict, G0OntologicalClassifierResult):
        raise G0C5RankerSchemaError(
            "rank_g0_epistemic_origin.ontological_classifier_verdict must be "
            f"G0OntologicalClassifierResult ({FailureCode.GATE_REQUIRED.value})"
        )
    _require_trace_ref("rank_g0_epistemic_origin", "trace_ref", trace_ref)
    if ontological_classifier_verdict.candidate_ref != candidate.trace_ref:
        raise G0C5RankerSchemaError(
            "rank_g0_epistemic_origin requires candidate and "
            f"ontological_classifier_verdict continuity ({FailureCode.IDENTITY_BROKEN.value})"
        )
    if (
        ontological_classifier_verdict.state is G0OntologicalClassifierState.CLASSIFIED
        and ontological_classifier_verdict.ontological_class != candidate.ontological_class
    ):
        raise G0C5RankerSchemaError(
            "rank_g0_epistemic_origin requires ontological class continuity "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )

    if ontological_classifier_verdict.state is G0OntologicalClassifierState.FORBIDDEN:
        return G0EpistemicRankerResult(
            state=G0EpistemicRankerState.FORBIDDEN,
            candidate_ref=candidate.trace_ref,
            upstream_classifier_state=ontological_classifier_verdict.state,
            ontological_class=None,
            epistemic_rank=None,
            residuals=(
                _residual(
                    G0EpistemicResidualKind.UPSTREAM_CLASSIFIER_FORBIDDEN,
                    trace_ref,
                    "upstream ontological classifier is forbidden; ranker remains closed",
                    blocking=True,
                ),
            ),
            failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
            rank=G0_C5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if ontological_classifier_verdict.state is G0OntologicalClassifierState.DEFERRED:
        return G0EpistemicRankerResult(
            state=G0EpistemicRankerState.DEFERRED,
            candidate_ref=candidate.trace_ref,
            upstream_classifier_state=ontological_classifier_verdict.state,
            ontological_class=None,
            epistemic_rank=None,
            residuals=(
                _residual(
                    G0EpistemicResidualKind.UPSTREAM_CLASSIFIER_DEFERRED,
                    trace_ref,
                    "upstream ontological classifier is deferred; ranker requires classifier closure",
                    blocking=False,
                ),
            ),
            failure_code=FailureCode.GATE_REQUIRED,
            rank=G0_C5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if candidate.epistemic_rank is EpistemicRank.E5:
        return G0EpistemicRankerResult(
            state=G0EpistemicRankerState.FORBIDDEN,
            candidate_ref=candidate.trace_ref,
            upstream_classifier_state=ontological_classifier_verdict.state,
            ontological_class=None,
            epistemic_rank=None,
            residuals=(
                _residual(
                    G0EpistemicResidualKind.CONTEXT_OR_TRANSFER_REQUIRED_E5,
                    trace_ref,
                    "E5 requires context/transfer and is forbidden at G0",
                    blocking=True,
                ),
            ),
            failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
            rank=G0_C5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if candidate.epistemic_rank in {EpistemicRank.E0, EpistemicRank.E4}:
        kind = (
            G0EpistemicResidualKind.NOMINATION_ONLY_E0
            if candidate.epistemic_rank is EpistemicRank.E0
            else G0EpistemicResidualKind.INSUFFICIENT_WITNESS_E4
        )
        message = (
            "E0 nominates only a genus and cannot produce a ranked verdict at G0"
            if candidate.epistemic_rank is EpistemicRank.E0
            else "E4 has insufficient witness and remains suspended at G0"
        )
        return G0EpistemicRankerResult(
            state=G0EpistemicRankerState.DEFERRED,
            candidate_ref=candidate.trace_ref,
            upstream_classifier_state=ontological_classifier_verdict.state,
            ontological_class=None,
            epistemic_rank=None,
            residuals=(_residual(kind, trace_ref, message, blocking=False),),
            failure_code=FailureCode.GATE_REQUIRED,
            rank=G0_C5_RANK_CEILING,
            trace_ref=trace_ref,
        )

    residuals: list[G0EpistemicResidual] = []
    if ontological_classifier_verdict.residuals:
        residuals.append(
            _residual(
                G0EpistemicResidualKind.UPSTREAM_CLASSIFIER_CONDITIONAL,
                trace_ref,
                "upstream classifier carries conditional residuals; preserved for visibility",
                blocking=False,
            )
        )
    if candidate.epistemic_rank is EpistemicRank.E3:
        residuals.append(
            _residual(
                G0EpistemicResidualKind.REAL_MULTIPLICITY_UNDECIDED_E3,
                trace_ref,
                "E3 records real multiplicity and remains undecided without context",
                blocking=False,
            )
        )
    return G0EpistemicRankerResult(
        state=G0EpistemicRankerState.RANKED,
        candidate_ref=candidate.trace_ref,
        upstream_classifier_state=ontological_classifier_verdict.state,
        ontological_class=candidate.ontological_class,
        epistemic_rank=candidate.epistemic_rank,
        residuals=tuple(residuals),
        failure_code=None,
        rank=G0_C5_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "G0_C5_ALLOWED_OUTPUT",
    "G0_C5_FORBIDDEN_OUTPUTS",
    "G0_C5_RANK_CEILING",
    "G0C5RankerSchemaError",
    "G0EpistemicRankerResult",
    "G0EpistemicRankerState",
    "G0EpistemicResidual",
    "G0EpistemicResidualKind",
    "rank_g0_epistemic_origin",
]
