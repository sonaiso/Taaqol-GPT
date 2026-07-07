"""G0-C6 anchor-certificate issuance and downstream consumption gate (docs/77 §10, §13).

Binding: docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md §10, §13.
Chain position: G0-C6 (anchor issuance + downstream consumption after G0-C5 output).
Forbidden: semantic/hukm/truth/certainty outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Literal

from taaqqul_slot_geometry.core import FailureCode, Rank
from taaqqul_slot_geometry.g0_c1_carriers import AnchorCertificate, BareJamidStemCandidate
from taaqqul_slot_geometry.g0_c5_epistemic_ranker import (
    G0EpistemicRankerResult,
    G0EpistemicRankerState,
)


class G0C6AnchorSchemaError(TypeError):
    """Raised when the G0-C6 anchor surface is malformed."""


class G0AnchorGateState(StrEnum):
    """Bounded G0-C6 state vocabulary."""

    ISSUED = "ISSUED"
    DEFERRED = "DEFERRED"
    FORBIDDEN = "FORBIDDEN"


class G0AnchorResidualKind(StrEnum):
    """Local visible residual vocabulary for G0-C6."""

    UPSTREAM_RANKER_RESIDUALS_VISIBLE = "UPSTREAM_RANKER_RESIDUALS_VISIBLE"
    UPSTREAM_RANKER_DEFERRED = "UPSTREAM_RANKER_DEFERRED"
    UPSTREAM_RANKER_FORBIDDEN = "UPSTREAM_RANKER_FORBIDDEN"
    DOWNSTREAM_CONSUMPTION_DEFERRED = "DOWNSTREAM_CONSUMPTION_DEFERRED"
    DOWNSTREAM_CONSUMPTION_FORBIDDEN = "DOWNSTREAM_CONSUMPTION_FORBIDDEN"


G0_C6_ISSUANCE_OUTPUT: Final[str] = "G0_ANCHOR_CERTIFICATE_ISSUANCE_RESULT"
G0_C6_CONSUMPTION_OUTPUT: Final[str] = "G0_DOWNSTREAM_CONSUMPTION_GATE_RESULT"
G0_C6_RANK_CEILING: Final[Rank] = Rank.ZERO
G0_C6_FORBIDDEN_OUTPUTS: Final[tuple[str, ...]] = (
    "HukmVerdict",
    "TruthCertificate",
    "CertaintyCertificate",
    "RealityClaim",
)


def _require_trace_ref(owner: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise G0C6AnchorSchemaError(
            f"{owner}.{field_name} must be a non-empty string ({FailureCode.TRACE_MISSING.value})"
        )
    if not value.startswith("trace://"):
        raise G0C6AnchorSchemaError(
            f"{owner}.{field_name} must start with 'trace://' ({FailureCode.TRACE_MISSING.value})"
        )


def _validate_forbidden_outputs(owner: str, forbidden_outputs: tuple[str, ...]) -> None:
    if not isinstance(forbidden_outputs, tuple):
        raise G0C6AnchorSchemaError(
            f"{owner}.forbidden_outputs must be tuple ({FailureCode.BOUNDARY_MISSING.value})"
        )
    for item in forbidden_outputs:
        if not isinstance(item, str) or not item.strip():
            raise G0C6AnchorSchemaError(
                f"{owner}.forbidden_outputs must contain non-empty strings "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class G0AnchorResidual:
    """Visible G0-C6 residual entry."""

    kind: G0AnchorResidualKind
    trace_ref: str
    message: str
    blocking: bool

    def __post_init__(self) -> None:
        if not isinstance(self.kind, G0AnchorResidualKind):
            raise G0C6AnchorSchemaError(
                "G0AnchorResidual.kind must be G0AnchorResidualKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_trace_ref("G0AnchorResidual", "trace_ref", self.trace_ref)
        if not isinstance(self.message, str) or not self.message.strip():
            raise G0C6AnchorSchemaError(
                "G0AnchorResidual.message must be a non-empty string "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise G0C6AnchorSchemaError(
                "G0AnchorResidual.blocking must be bool "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class G0AnchorIssuanceResult:
    """Bounded G0-C6 output for anchor-certificate issuance."""

    state: G0AnchorGateState
    candidate_ref: str
    upstream_ranker_state: G0EpistemicRankerState
    anchor_certificate: AnchorCertificate | None
    residuals: tuple[G0AnchorResidual, ...]
    failure_code: FailureCode | None
    rank: Rank
    trace_ref: str
    output: Literal["G0_ANCHOR_CERTIFICATE_ISSUANCE_RESULT"] = G0_C6_ISSUANCE_OUTPUT
    forbidden_outputs: tuple[str, ...] = G0_C6_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, G0AnchorGateState):
            raise G0C6AnchorSchemaError(
                "G0AnchorIssuanceResult.state must be G0AnchorGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_trace_ref("G0AnchorIssuanceResult", "candidate_ref", self.candidate_ref)
        if not isinstance(self.upstream_ranker_state, G0EpistemicRankerState):
            raise G0C6AnchorSchemaError(
                "G0AnchorIssuanceResult.upstream_ranker_state must be G0EpistemicRankerState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.anchor_certificate is not None and not isinstance(
            self.anchor_certificate, AnchorCertificate
        ):
            raise G0C6AnchorSchemaError(
                "G0AnchorIssuanceResult.anchor_certificate must be AnchorCertificate or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise G0C6AnchorSchemaError(
                "G0AnchorIssuanceResult.residuals must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, G0AnchorResidual):
                raise G0C6AnchorSchemaError(
                    "G0AnchorIssuanceResult.residuals must contain G0AnchorResidual "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise G0C6AnchorSchemaError(
                "G0AnchorIssuanceResult.failure_code must be FailureCode or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.rank is not G0_C6_RANK_CEILING:
            raise G0C6AnchorSchemaError(
                "G0AnchorIssuanceResult.rank must stay at Rank.ZERO "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        _require_trace_ref("G0AnchorIssuanceResult", "trace_ref", self.trace_ref)
        if self.output != G0_C6_ISSUANCE_OUTPUT:
            raise G0C6AnchorSchemaError(
                "G0AnchorIssuanceResult.output must stay inside G0-C6 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs("G0AnchorIssuanceResult", self.forbidden_outputs)

        has_blocking = any(residual.blocking for residual in self.residuals)
        has_non_blocking = any(not residual.blocking for residual in self.residuals)

        if self.state is G0AnchorGateState.ISSUED:
            if self.upstream_ranker_state is not G0EpistemicRankerState.RANKED:
                raise G0C6AnchorSchemaError(
                    "ISSUED state requires RANKED upstream ranker state "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if self.anchor_certificate is None:
                raise G0C6AnchorSchemaError(
                    "ISSUED state requires anchor_certificate "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
            if self.anchor_certificate.source_trace_ref != self.candidate_ref:
                raise G0C6AnchorSchemaError(
                    "ISSUED anchor_certificate must preserve candidate_ref continuity "
                    f"({FailureCode.IDENTITY_BROKEN.value})"
                )
            if has_blocking:
                raise G0C6AnchorSchemaError(
                    "ISSUED state must not include blocking residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            if self.failure_code is not None:
                raise G0C6AnchorSchemaError(
                    "ISSUED state must not carry failure_code "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0AnchorGateState.DEFERRED:
            if self.upstream_ranker_state is G0EpistemicRankerState.FORBIDDEN:
                raise G0C6AnchorSchemaError(
                    "DEFERRED state is invalid for FORBIDDEN upstream ranker state "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )
            if self.anchor_certificate is not None:
                raise G0C6AnchorSchemaError(
                    "DEFERRED state must not emit anchor_certificate "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
            if not self.residuals or has_blocking or not has_non_blocking:
                raise G0C6AnchorSchemaError(
                    "DEFERRED state requires visible non-blocking residuals "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
            if self.failure_code is not FailureCode.GATE_REQUIRED:
                raise G0C6AnchorSchemaError(
                    "DEFERRED state must name GATE_REQUIRED "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )

        if self.state is G0AnchorGateState.FORBIDDEN:
            if self.anchor_certificate is not None:
                raise G0C6AnchorSchemaError(
                    "FORBIDDEN state must not emit anchor_certificate "
                    f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
                )
            if not self.residuals or not has_blocking:
                raise G0C6AnchorSchemaError(
                    "FORBIDDEN state requires visible blocking residuals "
                    f"({FailureCode.BLOCKING_RESIDUAL_PRESENT.value})"
                )
            if self.failure_code is not FailureCode.BLOCKING_RESIDUAL_PRESENT:
                raise G0C6AnchorSchemaError(
                    "FORBIDDEN state must name BLOCKING_RESIDUAL_PRESENT "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )


@dataclass(frozen=True, slots=True)
class G0DownstreamConsumptionGateResult:
    """Bounded G0-C6 output for downstream opening only through a G0 anchor."""

    state: G0AnchorGateState
    candidate_ref: str
    downstream_stage: str
    anchor_certificate_id: str
    residuals: tuple[G0AnchorResidual, ...]
    failure_code: FailureCode | None
    rank: Rank
    trace_ref: str
    output: Literal["G0_DOWNSTREAM_CONSUMPTION_GATE_RESULT"] = G0_C6_CONSUMPTION_OUTPUT
    forbidden_outputs: tuple[str, ...] = G0_C6_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, G0AnchorGateState):
            raise G0C6AnchorSchemaError(
                "G0DownstreamConsumptionGateResult.state must be G0AnchorGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_trace_ref("G0DownstreamConsumptionGateResult", "candidate_ref", self.candidate_ref)
        if not isinstance(self.downstream_stage, str) or not self.downstream_stage.strip():
            raise G0C6AnchorSchemaError(
                "G0DownstreamConsumptionGateResult.downstream_stage must be a non-empty string "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.anchor_certificate_id, str):
            raise G0C6AnchorSchemaError(
                "G0DownstreamConsumptionGateResult.anchor_certificate_id must be string "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.state is G0AnchorGateState.ISSUED and not self.anchor_certificate_id.strip():
            raise G0C6AnchorSchemaError(
                "ISSUED downstream gate requires anchor_certificate_id "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.state is not G0AnchorGateState.ISSUED and self.anchor_certificate_id.strip():
            raise G0C6AnchorSchemaError(
                "Non-ISSUED downstream gate must not carry anchor_certificate_id "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise G0C6AnchorSchemaError(
                "G0DownstreamConsumptionGateResult.residuals must be tuple "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, G0AnchorResidual):
                raise G0C6AnchorSchemaError(
                    "G0DownstreamConsumptionGateResult.residuals must contain G0AnchorResidual "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise G0C6AnchorSchemaError(
                "G0DownstreamConsumptionGateResult.failure_code must be FailureCode or None "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if self.rank is not G0_C6_RANK_CEILING:
            raise G0C6AnchorSchemaError(
                "G0DownstreamConsumptionGateResult.rank must stay at Rank.ZERO "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        _require_trace_ref("G0DownstreamConsumptionGateResult", "trace_ref", self.trace_ref)
        if self.output != G0_C6_CONSUMPTION_OUTPUT:
            raise G0C6AnchorSchemaError(
                "G0DownstreamConsumptionGateResult.output must stay inside G0-C6 boundary "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs("G0DownstreamConsumptionGateResult", self.forbidden_outputs)


def _residual(
    kind: G0AnchorResidualKind,
    trace_ref: str,
    message: str,
    *,
    blocking: bool,
) -> G0AnchorResidual:
    return G0AnchorResidual(
        kind=kind,
        trace_ref=f"{trace_ref}/residual/{kind.value.lower()}",
        message=message,
        blocking=blocking,
    )


def issue_g0_anchor_certificate(
    candidate: BareJamidStemCandidate,
    *,
    epistemic_ranker_verdict: G0EpistemicRankerResult,
    trace_ref: str,
) -> G0AnchorIssuanceResult:
    """Issue a bounded G0 anchor certificate after a valid G0-C5 handoff."""

    if not isinstance(candidate, BareJamidStemCandidate):
        raise G0C6AnchorSchemaError(
            "issue_g0_anchor_certificate requires BareJamidStemCandidate "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(epistemic_ranker_verdict, G0EpistemicRankerResult):
        raise G0C6AnchorSchemaError(
            "issue_g0_anchor_certificate.epistemic_ranker_verdict must be "
            f"G0EpistemicRankerResult ({FailureCode.GATE_REQUIRED.value})"
        )
    _require_trace_ref("issue_g0_anchor_certificate", "trace_ref", trace_ref)
    if epistemic_ranker_verdict.candidate_ref != candidate.trace_ref:
        raise G0C6AnchorSchemaError(
            "issue_g0_anchor_certificate requires candidate and "
            "epistemic_ranker_verdict continuity "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )

    if epistemic_ranker_verdict.state is G0EpistemicRankerState.FORBIDDEN:
        return G0AnchorIssuanceResult(
            state=G0AnchorGateState.FORBIDDEN,
            candidate_ref=candidate.trace_ref,
            upstream_ranker_state=epistemic_ranker_verdict.state,
            anchor_certificate=None,
            residuals=(
                _residual(
                    G0AnchorResidualKind.UPSTREAM_RANKER_FORBIDDEN,
                    trace_ref,
                    "upstream ranker is forbidden; anchor issuance remains closed",
                    blocking=True,
                ),
            ),
            failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
            rank=G0_C6_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if epistemic_ranker_verdict.state is G0EpistemicRankerState.DEFERRED:
        return G0AnchorIssuanceResult(
            state=G0AnchorGateState.DEFERRED,
            candidate_ref=candidate.trace_ref,
            upstream_ranker_state=epistemic_ranker_verdict.state,
            anchor_certificate=None,
            residuals=(
                _residual(
                    G0AnchorResidualKind.UPSTREAM_RANKER_DEFERRED,
                    trace_ref,
                    "upstream ranker is deferred; anchor issuance requires ranker closure",
                    blocking=False,
                ),
            ),
            failure_code=FailureCode.GATE_REQUIRED,
            rank=G0_C6_RANK_CEILING,
            trace_ref=trace_ref,
        )

    certificate = AnchorCertificate(
        certificate_id=f"anchor://{candidate.trace_ref.removeprefix('trace://')}",
        stem_key=candidate.stem,
        ontological_class=candidate.ontological_class,
        epistemic_rank=candidate.epistemic_rank,
        entity_rank=candidate.entity_rank,
        source_trace_ref=candidate.trace_ref,
        residuals=tuple(
            f"RANKER::{residual.kind.value}" for residual in epistemic_ranker_verdict.residuals
        ),
    )
    residuals = ()
    if epistemic_ranker_verdict.residuals:
        residuals = (
            _residual(
                G0AnchorResidualKind.UPSTREAM_RANKER_RESIDUALS_VISIBLE,
                trace_ref,
                "upstream ranker residuals remain visible on anchor issuance",
                blocking=False,
            ),
        )
    return G0AnchorIssuanceResult(
        state=G0AnchorGateState.ISSUED,
        candidate_ref=candidate.trace_ref,
        upstream_ranker_state=epistemic_ranker_verdict.state,
        anchor_certificate=certificate,
        residuals=residuals,
        failure_code=None,
        rank=G0_C6_RANK_CEILING,
        trace_ref=trace_ref,
    )


def enforce_g0_anchor_consumption(
    issuance_result: G0AnchorIssuanceResult,
    *,
    downstream_stage: str,
    trace_ref: str,
) -> G0DownstreamConsumptionGateResult:
    """Open downstream stage only through a valid G0 anchor certificate."""

    if not isinstance(issuance_result, G0AnchorIssuanceResult):
        raise G0C6AnchorSchemaError(
            "enforce_g0_anchor_consumption requires G0AnchorIssuanceResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(downstream_stage, str) or not downstream_stage.strip():
        raise G0C6AnchorSchemaError(
            "enforce_g0_anchor_consumption.downstream_stage must be a non-empty string "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_trace_ref("enforce_g0_anchor_consumption", "trace_ref", trace_ref)

    if issuance_result.state is G0AnchorGateState.ISSUED:
        anchor = issuance_result.anchor_certificate
        if anchor is None:
            raise G0C6AnchorSchemaError(
                "ISSUED issuance_result must carry anchor_certificate "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        return G0DownstreamConsumptionGateResult(
            state=G0AnchorGateState.ISSUED,
            candidate_ref=issuance_result.candidate_ref,
            downstream_stage=downstream_stage,
            anchor_certificate_id=anchor.certificate_id,
            residuals=issuance_result.residuals,
            failure_code=None,
            rank=G0_C6_RANK_CEILING,
            trace_ref=trace_ref,
        )

    if issuance_result.state is G0AnchorGateState.DEFERRED:
        return G0DownstreamConsumptionGateResult(
            state=G0AnchorGateState.DEFERRED,
            candidate_ref=issuance_result.candidate_ref,
            downstream_stage=downstream_stage,
            anchor_certificate_id="",
            residuals=(
                _residual(
                    G0AnchorResidualKind.DOWNSTREAM_CONSUMPTION_DEFERRED,
                    trace_ref,
                    "downstream opening is deferred until anchor issuance closes",
                    blocking=False,
                ),
            ),
            failure_code=FailureCode.GATE_REQUIRED,
            rank=G0_C6_RANK_CEILING,
            trace_ref=trace_ref,
        )

    return G0DownstreamConsumptionGateResult(
        state=G0AnchorGateState.FORBIDDEN,
        candidate_ref=issuance_result.candidate_ref,
        downstream_stage=downstream_stage,
        anchor_certificate_id="",
        residuals=(
            _residual(
                G0AnchorResidualKind.DOWNSTREAM_CONSUMPTION_FORBIDDEN,
                trace_ref,
                "downstream opening is forbidden because anchor issuance is forbidden",
                blocking=True,
            ),
        ),
        failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
        rank=G0_C6_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "G0_C6_CONSUMPTION_OUTPUT",
    "G0_C6_FORBIDDEN_OUTPUTS",
    "G0_C6_ISSUANCE_OUTPUT",
    "G0_C6_RANK_CEILING",
    "G0DownstreamConsumptionGateResult",
    "G0AnchorGateState",
    "G0AnchorIssuanceResult",
    "G0AnchorResidual",
    "G0AnchorResidualKind",
    "G0C6AnchorSchemaError",
    "enforce_g0_anchor_consumption",
    "issue_g0_anchor_certificate",
]
