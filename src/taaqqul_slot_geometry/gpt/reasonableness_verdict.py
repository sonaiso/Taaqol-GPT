"""GPT-R7 — GPT answer reasonableness verdict.

Binding:
- docs/54 §3.5, §6 (ReasonablenessVerdict)
- docs/55 §10, §11 (forbidden outputs, rank/residual discipline)
- docs/14 chain row GPT-R7 (bounded verdict only, no audit integration)

This module consumes the completed GPT-R6 ReasonablenessGateReport and maps it
to a bounded GPTAnswerReasonablenessVerdict. It does not re-run GPT-R6 gates,
does not mutate AnswerAudit, and does not produce certificate, authority,
truth, reality, execution, or model-internal semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.gpt.knowledge_origins import OriginResidual
from taaqqul_slot_geometry.gpt.reasonableness_gates import (
    ReasonablenessGateReport,
    ReasonablenessGateReportState,
)


class ReasonablenessVerdictSchemaError(TypeError):
    """A GPT-R7 reasonableness verdict surface was constructed incorrectly."""


class ReasonablenessVerdictState(StrEnum):
    """Bounded GPT-R7 verdict states; never audit, certificate, or truth."""

    REASONABLE = "REASONABLE"
    UNREASONABLE = "UNREASONABLE"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


_REPORT_TO_VERDICT_STATE = {
    ReasonablenessGateReportState.LICENSED_FOR_VERDICT: ReasonablenessVerdictState.REASONABLE,
    ReasonablenessGateReportState.BLOCKED: ReasonablenessVerdictState.UNREASONABLE,
    ReasonablenessGateReportState.DEFERRED: ReasonablenessVerdictState.DEFERRED,
    ReasonablenessGateReportState.REFUSED: ReasonablenessVerdictState.REFUSED,
}


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ReasonablenessVerdictSchemaError(
            f"{cls_name}.{field} must be a non-empty string"
        )


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise ReasonablenessVerdictSchemaError(
            f"{cls_name}.{field} must start with 'trace://'"
        )


def _require_origin_residuals(value: object) -> None:
    if not isinstance(value, tuple):
        raise ReasonablenessVerdictSchemaError(
            "residuals must be a tuple of OriginResidual carriers"
        )
    for residual in value:
        if not isinstance(residual, OriginResidual):
            raise ReasonablenessVerdictSchemaError(
                "residuals entries must be OriginResidual carriers"
            )


@dataclass(frozen=True, slots=True)
class GPTAnswerReasonablenessVerdict:
    """Bounded GPT-R7 verdict mapped from GPT-R6 gate report ancestry."""

    state: ReasonablenessVerdictState
    source_report_state: ReasonablenessGateReportState
    source_gate_report_ref: str
    source_binding_ref: str
    failure_code: FailureCode | None
    residuals: tuple[OriginResidual, ...]
    rank_ceiling: ReasonablenessGateReportState
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.state, ReasonablenessVerdictState):
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.state must be a ReasonablenessVerdictState member"
            )
        if not isinstance(self.source_report_state, ReasonablenessGateReportState):
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.source_report_state must be a ReasonablenessGateReportState member"
            )
        if not isinstance(self.rank_ceiling, ReasonablenessGateReportState):
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.rank_ceiling must be a ReasonablenessGateReportState member"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.failure_code must be a FailureCode member or None"
            )
        _require_trace_ref(cls, "source_gate_report_ref", self.source_gate_report_ref)
        _require_trace_ref(cls, "source_binding_ref", self.source_binding_ref)
        _require_origin_residuals(self.residuals)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)

        expected_state = _REPORT_TO_VERDICT_STATE[self.source_report_state]
        if self.state is not expected_state:
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.state cannot exceed source_report_state "
                f"{self.source_report_state.value}"
            )
        if self.rank_ceiling is not self.source_report_state:
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.rank_ceiling must preserve source_report_state"
            )
        if self.state is ReasonablenessVerdictState.REASONABLE and self.failure_code is not None:
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.REASONABLE must not carry failure_code"
            )
        if self.state is not ReasonablenessVerdictState.REASONABLE and self.failure_code is None:
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.{self.state.value} requires a named failure_code"
            )


def prove_gpt_answer_reasonableness_verdict(
    gate_report: ReasonablenessGateReport | None,
    *,
    trace_ref: str,
) -> GPTAnswerReasonablenessVerdict:
    """Map one GPT-R6 gate report to the bounded GPT-R7 verdict surface."""

    _require_trace_ref("GPTAnswerReasonablenessVerdict", "trace_ref", trace_ref)

    if not isinstance(gate_report, ReasonablenessGateReport):
        return GPTAnswerReasonablenessVerdict(
            state=ReasonablenessVerdictState.REFUSED,
            source_report_state=ReasonablenessGateReportState.REFUSED,
            source_gate_report_ref="trace://gpt-r7/missing-gate-report",
            source_binding_ref="trace://gpt-r7/missing-origin-binding",
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=(),
            rank_ceiling=ReasonablenessGateReportState.REFUSED,
            trace_ref=trace_ref,
        )

    verdict_state = _REPORT_TO_VERDICT_STATE[gate_report.state]
    return GPTAnswerReasonablenessVerdict(
        state=verdict_state,
        source_report_state=gate_report.state,
        source_gate_report_ref=gate_report.trace_ref,
        source_binding_ref=gate_report.source_binding_ref,
        failure_code=gate_report.failure_code,
        residuals=gate_report.residuals,
        rank_ceiling=gate_report.state,
        trace_ref=trace_ref,
    )


__all__ = [
    "GPTAnswerReasonablenessVerdict",
    "ReasonablenessVerdictSchemaError",
    "ReasonablenessVerdictState",
    "prove_gpt_answer_reasonableness_verdict",
]
