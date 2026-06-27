"""GPT-R7 — GPT Answer Reasonableness Verdict.

Binding:
- docs/54 §3.5 (GPTAnswerReasonablenessVerdict)
- docs/55 §8, §10, §11, §14 (origin binding, forbidden outputs, rank/trace)
- docs/14 chain row GPT-R7 (verdict only, no audit integration)

This module consumes the completed GPT-R6 ReasonablenessGateReport and
produces a bounded verdict-state surface. It does not mutate AnswerAudit,
does not produce certificate/authority semantics, and does not rerun gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.gpt.knowledge_origins import OriginResidual
from taaqqul_slot_geometry.gpt.reasonableness_gates import (
    ReasonablenessGateKind,
    ReasonablenessGateReport,
    ReasonablenessGateReportState,
)
from taaqqul_slot_geometry.x0r import TransitionContract


class ReasonablenessVerdictSchemaError(TypeError):
    """A GPT-R7 reasonableness verdict surface was constructed incorrectly."""


class ReasonablenessVerdictState(StrEnum):
    """Bounded GPT-R7 verdict states; never audit/certificate states."""

    REASONABLE = "REASONABLE"
    OFF_MAQAM = "OFF_MAQAM"
    UNSUPPORTED = "UNSUPPORTED"
    CONTRADICTORY = "CONTRADICTORY"
    FORBIDDEN_LEAP = "FORBIDDEN_LEAP"
    RESIDUAL_BLOCKED = "RESIDUAL_BLOCKED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


GPT_REASONABLENESS_VERDICT_TRANSITION_CONTRACT = TransitionContract(
    declared_transitions=frozenset(
        {
            (
                "ReasonablenessGateReport",
                "GPTAnswerReasonablenessVerdict",
                "prove_gpt_answer_reasonableness_verdict",
                "gpt_reasonableness",
            ),
        }
    )
)


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
    """Bounded GPT-R7 verdict; not an AnswerAudit and not a certificate."""

    state: ReasonablenessVerdictState
    source_gate_report_state: ReasonablenessGateReportState
    failure_code: FailureCode | None
    residuals: tuple[OriginResidual, ...]
    rank: Rank
    rank_ceiling: Rank
    source_gate_report_ref: str
    source_binding_ref: str
    trace_ref: str
    integration_status: str = "pre_audit_verdict"
    not_final_audit: bool = True
    requires_r8_audit_integration: bool = True
    certificate_allowed: bool = False

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.state, ReasonablenessVerdictState):
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.state must be a ReasonablenessVerdictState member"
            )
        if not isinstance(self.source_gate_report_state, ReasonablenessGateReportState):
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.source_gate_report_state must be a ReasonablenessGateReportState member"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.failure_code must be a FailureCode member or None"
            )
        _require_origin_residuals(self.residuals)
        if not isinstance(self.rank, Rank):
            raise ReasonablenessVerdictSchemaError(f"{cls}.rank must be a Rank member")
        if not isinstance(self.rank_ceiling, Rank):
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.rank_ceiling must be a Rank member"
            )
        if self.rank.name == "CERTIFICATE" or self.rank_ceiling.name == "CERTIFICATE":
            raise ReasonablenessVerdictSchemaError(
                f"{cls} must not carry certificate rank semantics"
            )
        if self.rank > self.rank_ceiling:
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.rank must not exceed rank_ceiling"
            )
        _require_trace_ref(cls, "source_gate_report_ref", self.source_gate_report_ref)
        _require_trace_ref(cls, "source_binding_ref", self.source_binding_ref)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if self.integration_status != "pre_audit_verdict":
            raise ReasonablenessVerdictSchemaError(
                f"{cls}.integration_status must remain 'pre_audit_verdict'"
            )
        if self.not_final_audit is not True:
            raise ReasonablenessVerdictSchemaError(f"{cls} is not a final AnswerAudit")
        if self.requires_r8_audit_integration is not True:
            raise ReasonablenessVerdictSchemaError(
                f"{cls} requires GPT-R8 audit integration"
            )
        if self.certificate_allowed is not False:
            raise ReasonablenessVerdictSchemaError(
                f"{cls} must not allow certificate emission"
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
    requested_rank: Rank | None = None,
) -> GPTAnswerReasonablenessVerdict:
    """Map a GPT-R6 gate report into a bounded GPT-R7 verdict."""

    _require_trace_ref("GPTAnswerReasonablenessVerdict", "trace_ref", trace_ref)
    if not isinstance(gate_report, ReasonablenessGateReport):
        return _verdict(
            ReasonablenessVerdictState.REFUSED,
            ReasonablenessGateReportState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=(),
            rank=Rank.TRACE,
            rank_ceiling=Rank.TRACE,
            source_gate_report_ref="trace://gpt-r7/missing-gate-report",
            source_binding_ref="trace://gpt-r7/missing-origin-binding",
            trace_ref=trace_ref,
        )

    rank_ceiling = _rank_ceiling_for(gate_report.state)
    rank = requested_rank if requested_rank is not None else rank_ceiling
    if not isinstance(rank, Rank):
        raise ReasonablenessVerdictSchemaError("requested_rank must be a Rank member or None")
    if rank > rank_ceiling:
        return _verdict(
            ReasonablenessVerdictState.REFUSED,
            gate_report.state,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            residuals=gate_report.residuals,
            rank=rank_ceiling,
            rank_ceiling=rank_ceiling,
            source_gate_report_ref=gate_report.trace_ref,
            source_binding_ref=gate_report.source_binding_ref,
            trace_ref=trace_ref,
        )

    state, failure_code = _map_report_state(gate_report)
    return _verdict(
        state,
        gate_report.state,
        failure_code=failure_code,
        residuals=gate_report.residuals,
        rank=rank,
        rank_ceiling=rank_ceiling,
        source_gate_report_ref=gate_report.trace_ref,
        source_binding_ref=gate_report.source_binding_ref,
        trace_ref=trace_ref,
    )


def _rank_ceiling_for(report_state: ReasonablenessGateReportState) -> Rank:
    if report_state is ReasonablenessGateReportState.LICENSED_FOR_VERDICT:
        return Rank.LICENSED
    if report_state in (
        ReasonablenessGateReportState.BLOCKED,
        ReasonablenessGateReportState.DEFERRED,
    ):
        return Rank.CANDIDATE
    return Rank.TRACE


def _map_report_state(
    gate_report: ReasonablenessGateReport,
) -> tuple[ReasonablenessVerdictState, FailureCode | None]:
    if gate_report.state is ReasonablenessGateReportState.LICENSED_FOR_VERDICT:
        return ReasonablenessVerdictState.REASONABLE, None
    if gate_report.state is ReasonablenessGateReportState.DEFERRED:
        return (
            _deferred_state_for(gate_report),
            gate_report.failure_code or FailureCode.REQUIRED_SLOT_EMPTY,
        )
    if gate_report.state is ReasonablenessGateReportState.BLOCKED:
        return (
            _blocked_state_for(gate_report),
            gate_report.failure_code or FailureCode.BLOCKING_RESIDUAL_PRESENT,
        )
    return ReasonablenessVerdictState.REFUSED, (
        gate_report.failure_code or FailureCode.GATE_REQUIRED
    )


def _blocked_state_for(gate_report: ReasonablenessGateReport) -> ReasonablenessVerdictState:
    blocked_gate = next(
        (
            gate
            for gate in gate_report.gates
            if gate.gate is ReasonablenessGateKind.CONTRADICTION_CHECK and gate.failure_code
        ),
        None,
    )
    if blocked_gate is None:
        blocked_gate = next((gate for gate in gate_report.gates if gate.failure_code), None)
    if blocked_gate is None:
        return ReasonablenessVerdictState.RESIDUAL_BLOCKED
    if blocked_gate.gate is ReasonablenessGateKind.MAQAM_FIT:
        return ReasonablenessVerdictState.OFF_MAQAM
    if blocked_gate.gate is ReasonablenessGateKind.CONTRADICTION_CHECK:
        return ReasonablenessVerdictState.CONTRADICTORY
    if blocked_gate.gate is ReasonablenessGateKind.FORBIDDEN_LEAP_CHECK:
        return ReasonablenessVerdictState.FORBIDDEN_LEAP
    if blocked_gate.gate is ReasonablenessGateKind.RANK_RESIDUAL_POLICY:
        return ReasonablenessVerdictState.RESIDUAL_BLOCKED
    return ReasonablenessVerdictState.UNSUPPORTED


def _deferred_state_for(gate_report: ReasonablenessGateReport) -> ReasonablenessVerdictState:
    deferred_gate = next((gate for gate in gate_report.gates if gate.failure_code), None)
    if deferred_gate is not None and deferred_gate.gate in (
        ReasonablenessGateKind.ORIGIN_BINDING,
        ReasonablenessGateKind.EVIDENCE_SUPPORT,
    ):
        return ReasonablenessVerdictState.UNSUPPORTED
    return ReasonablenessVerdictState.DEFERRED


def _verdict(
    state: ReasonablenessVerdictState,
    source_gate_report_state: ReasonablenessGateReportState,
    *,
    failure_code: FailureCode | None,
    residuals: tuple[OriginResidual, ...],
    rank: Rank,
    rank_ceiling: Rank,
    source_gate_report_ref: str,
    source_binding_ref: str,
    trace_ref: str,
) -> GPTAnswerReasonablenessVerdict:
    return GPTAnswerReasonablenessVerdict(
        state=state,
        source_gate_report_state=source_gate_report_state,
        failure_code=failure_code,
        residuals=residuals,
        rank=rank,
        rank_ceiling=rank_ceiling,
        source_gate_report_ref=source_gate_report_ref,
        source_binding_ref=source_binding_ref,
        trace_ref=trace_ref,
    )


__all__ = [
    "GPT_REASONABLENESS_VERDICT_TRANSITION_CONTRACT",
    "GPTAnswerReasonablenessVerdict",
    "ReasonablenessVerdictSchemaError",
    "ReasonablenessVerdictState",
    "prove_gpt_answer_reasonableness_verdict",
]
