"""GPT-R6 — Reasonableness Gates.

Binding:
- docs/54 §3.5 (Reasonableness conditions)
- docs/55 §8, §10, §11 (origin binding, forbidden outputs, rank/residual policy)
- docs/14 chain row GPT-R6 (gates only, no final verdict)

This module evaluates the bounded GPT-R6 gate sequence after GPT-R5 origin
binding. It does not produce GPTAnswerReasonablenessVerdict, does not mutate
AnswerAudit, and does not open a full pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.gpt.knowledge_origins import BindingVerdict, OriginResidual
from taaqqul_slot_geometry.gpt.origin_binding_gate import (
    OriginBindingGateResult,
    OriginBindingGateState,
)
from taaqqul_slot_geometry.x0r import TransitionContract


class ReasonablenessGateSchemaError(TypeError):
    """A GPT-R6 reasonableness gate surface was constructed incorrectly."""


class ReasonablenessGateKind(StrEnum):
    """Licensed GPT-R6 gates (no final verdict at this stage)."""

    MAQAM_FIT = "MAQAM_FIT"
    ORIGIN_BINDING = "ORIGIN_BINDING"
    EVIDENCE_SUPPORT = "EVIDENCE_SUPPORT"
    CONTRADICTION_CHECK = "CONTRADICTION_CHECK"
    FORBIDDEN_LEAP_CHECK = "FORBIDDEN_LEAP_CHECK"
    RANK_RESIDUAL_POLICY = "RANK_RESIDUAL_POLICY"


class ReasonablenessGateState(StrEnum):
    """Per-gate state for GPT-R6."""

    PASSED = "PASSED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


class ReasonablenessGateReportState(StrEnum):
    """Aggregate GPT-R6 report state; still pre-verdict."""

    LICENSED_FOR_VERDICT = "LICENSED_FOR_VERDICT"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


GPT_REASONABLENESS_GATES_TRANSITION_CONTRACT = TransitionContract(
    declared_transitions=frozenset(
        {
            (
                "OriginBindingGateResult",
                "MaqamFitGate",
                "check_maqam_fit",
                "gpt_reasonableness",
            ),
            (
                "MaqamFitGate",
                "OriginBindingGate",
                "check_origin_binding",
                "gpt_reasonableness",
            ),
            (
                "OriginBindingGate",
                "EvidenceSupportGate",
                "check_evidence_support",
                "gpt_reasonableness",
            ),
            (
                "EvidenceSupportGate",
                "ContradictionGate",
                "check_contradiction",
                "gpt_reasonableness",
            ),
            (
                "ContradictionGate",
                "ForbiddenLeapGate",
                "check_forbidden_leap",
                "gpt_reasonableness",
            ),
            (
                "ForbiddenLeapGate",
                "RankResidualPolicyGate",
                "check_rank_and_residual_policy",
                "gpt_reasonableness",
            ),
            (
                "RankResidualPolicyGate",
                "ReasonablenessGateReport",
                "surface_reasonableness_gates",
                "gpt_reasonableness",
            ),
        }
    )
)


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ReasonablenessGateSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise ReasonablenessGateSchemaError(f"{cls_name}.{field} must start with 'trace://'")


def _require_origin_residuals(value: object) -> None:
    if not isinstance(value, tuple):
        raise ReasonablenessGateSchemaError(
            "residuals must be a tuple of OriginResidual carriers"
        )
    for residual in value:
        if not isinstance(residual, OriginResidual):
            raise ReasonablenessGateSchemaError(
                "residuals entries must be OriginResidual carriers"
            )


@dataclass(frozen=True, slots=True)
class ReasonablenessGateDecision:
    """One GPT-R6 gate decision (never the final reasonableness verdict)."""

    gate: ReasonablenessGateKind
    state: ReasonablenessGateState
    failure_code: FailureCode | None
    residuals: tuple[OriginResidual, ...]
    source_claim_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.gate, ReasonablenessGateKind):
            raise ReasonablenessGateSchemaError(
                f"{cls}.gate must be a ReasonablenessGateKind member"
            )
        if not isinstance(self.state, ReasonablenessGateState):
            raise ReasonablenessGateSchemaError(
                f"{cls}.state must be a ReasonablenessGateState member"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise ReasonablenessGateSchemaError(
                f"{cls}.failure_code must be a FailureCode member or None"
            )
        _require_origin_residuals(self.residuals)
        _require_nonempty_str(cls, "source_claim_ref", self.source_claim_ref)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if self.state is ReasonablenessGateState.PASSED and self.failure_code is not None:
            raise ReasonablenessGateSchemaError(f"{cls}.PASSED must not carry failure_code")
        if self.state is not ReasonablenessGateState.PASSED and self.failure_code is None:
            raise ReasonablenessGateSchemaError(
                f"{cls}.{self.state.value} requires a named failure_code"
            )


@dataclass(frozen=True, slots=True)
class ReasonablenessGateReport:
    """Aggregate GPT-R6 gate report; bounded handoff to GPT-R7 only."""

    state: ReasonablenessGateReportState
    gates: tuple[ReasonablenessGateDecision, ...]
    failure_code: FailureCode | None
    residuals: tuple[OriginResidual, ...]
    source_binding_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.state, ReasonablenessGateReportState):
            raise ReasonablenessGateSchemaError(
                f"{cls}.state must be a ReasonablenessGateReportState member"
            )
        if not isinstance(self.gates, tuple):
            raise ReasonablenessGateSchemaError(f"{cls}.gates must be a tuple")
        if not self.gates:
            raise ReasonablenessGateSchemaError(f"{cls}.gates must not be empty")
        for decision in self.gates:
            if not isinstance(decision, ReasonablenessGateDecision):
                raise ReasonablenessGateSchemaError(
                    f"{cls}.gates entries must be ReasonablenessGateDecision carriers"
                )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise ReasonablenessGateSchemaError(
                f"{cls}.failure_code must be a FailureCode member or None"
            )
        _require_origin_residuals(self.residuals)
        _require_trace_ref(cls, "source_binding_ref", self.source_binding_ref)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if (
            self.state is ReasonablenessGateReportState.LICENSED_FOR_VERDICT
            and self.failure_code is not None
        ):
            raise ReasonablenessGateSchemaError(
                f"{cls}.LICENSED_FOR_VERDICT must not carry failure_code"
            )
        if (
            self.state is not ReasonablenessGateReportState.LICENSED_FOR_VERDICT
            and self.failure_code is None
        ):
            raise ReasonablenessGateSchemaError(
                f"{cls}.{self.state.value} requires a named failure_code"
            )


def run_reasonableness_gates(
    binding_result: OriginBindingGateResult | None,
    *,
    maqam_fit: bool,
    evidence_supported: bool,
    forbidden_leap_detected: bool,
    rank_within_evidence: bool,
    residuals_visible: bool,
    trace_ref: str,
) -> ReasonablenessGateReport:
    """Evaluate the six GPT-R6 reasonableness gates over GPT-R5 output."""

    _require_trace_ref("ReasonablenessGateReport", "trace_ref", trace_ref)

    if not isinstance(binding_result, OriginBindingGateResult):
        gates = (
            _gate_decision(
                ReasonablenessGateKind.ORIGIN_BINDING,
                state=ReasonablenessGateState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                residuals=(),
                source_claim_ref="missing-claim",
                trace_ref=trace_ref,
            ),
        )
        return _report(
            ReasonablenessGateReportState.REFUSED,
            gates,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=(),
            source_binding_ref="trace://gpt-r6/missing-origin-binding",
            trace_ref=trace_ref,
        )

    source_claim_ref = binding_result.source_claim_ref
    residuals = binding_result.residuals
    gates = (
        _maqam_gate(maqam_fit=maqam_fit, source_claim_ref=source_claim_ref, trace_ref=trace_ref),
        _origin_binding_gate(binding_result, trace_ref=trace_ref),
        _evidence_gate(
            evidence_supported=evidence_supported,
            source_claim_ref=source_claim_ref,
            trace_ref=trace_ref,
        ),
        _contradiction_gate(binding_result, trace_ref=trace_ref),
        _forbidden_leap_gate(
            forbidden_leap_detected=forbidden_leap_detected,
            source_claim_ref=source_claim_ref,
            trace_ref=trace_ref,
        ),
        _rank_residual_policy_gate(
            rank_within_evidence=rank_within_evidence,
            residuals_visible=residuals_visible,
            source_claim_ref=source_claim_ref,
            residuals=residuals,
            trace_ref=trace_ref,
        ),
    )
    state, failure_code = _derive_report_state(gates)
    return _report(
        state,
        gates,
        failure_code=failure_code,
        residuals=residuals,
        source_binding_ref=binding_result.trace_ref,
        trace_ref=trace_ref,
    )


def _maqam_gate(
    *,
    maqam_fit: bool,
    source_claim_ref: str,
    trace_ref: str,
) -> ReasonablenessGateDecision:
    if maqam_fit:
        return _gate_decision(
            ReasonablenessGateKind.MAQAM_FIT,
            state=ReasonablenessGateState.PASSED,
            failure_code=None,
            residuals=(),
            source_claim_ref=source_claim_ref,
            trace_ref=trace_ref,
        )
    return _gate_decision(
        ReasonablenessGateKind.MAQAM_FIT,
        state=ReasonablenessGateState.BLOCKED,
        failure_code=FailureCode.MAQAM_DIVERGENCE,
        residuals=(),
        source_claim_ref=source_claim_ref,
        trace_ref=trace_ref,
    )


def _origin_binding_gate(
    binding_result: OriginBindingGateResult,
    *,
    trace_ref: str,
) -> ReasonablenessGateDecision:
    if binding_result.state is OriginBindingGateState.BOUND:
        return _gate_decision(
            ReasonablenessGateKind.ORIGIN_BINDING,
            state=ReasonablenessGateState.PASSED,
            failure_code=None,
            residuals=binding_result.residuals,
            source_claim_ref=binding_result.source_claim_ref,
            trace_ref=trace_ref,
        )
    if binding_result.state is OriginBindingGateState.BLOCKED:
        failure = binding_result.failure_code or FailureCode.BLOCKING_RESIDUAL_PRESENT
        state = ReasonablenessGateState.BLOCKED
    elif binding_result.state is OriginBindingGateState.DEFERRED:
        failure = binding_result.failure_code or FailureCode.REQUIRED_SLOT_EMPTY
        state = ReasonablenessGateState.DEFERRED
    else:
        failure = binding_result.failure_code or FailureCode.GATE_REQUIRED
        state = ReasonablenessGateState.REFUSED
    return _gate_decision(
        ReasonablenessGateKind.ORIGIN_BINDING,
        state=state,
        failure_code=failure,
        residuals=binding_result.residuals,
        source_claim_ref=binding_result.source_claim_ref,
        trace_ref=trace_ref,
    )


def _evidence_gate(
    *,
    evidence_supported: bool,
    source_claim_ref: str,
    trace_ref: str,
) -> ReasonablenessGateDecision:
    if evidence_supported:
        return _gate_decision(
            ReasonablenessGateKind.EVIDENCE_SUPPORT,
            state=ReasonablenessGateState.PASSED,
            failure_code=None,
            residuals=(),
            source_claim_ref=source_claim_ref,
            trace_ref=trace_ref,
        )
    return _gate_decision(
        ReasonablenessGateKind.EVIDENCE_SUPPORT,
        state=ReasonablenessGateState.DEFERRED,
        failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        residuals=(),
        source_claim_ref=source_claim_ref,
        trace_ref=trace_ref,
    )


def _contradiction_gate(
    binding_result: OriginBindingGateResult,
    *,
    trace_ref: str,
) -> ReasonablenessGateDecision:
    verdict = binding_result.binding.verdict if binding_result.binding is not None else None
    if verdict is BindingVerdict.CONTRADICTED:
        return _gate_decision(
            ReasonablenessGateKind.CONTRADICTION_CHECK,
            state=ReasonablenessGateState.BLOCKED,
            failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
            residuals=binding_result.residuals,
            source_claim_ref=binding_result.source_claim_ref,
            trace_ref=trace_ref,
        )
    return _gate_decision(
        ReasonablenessGateKind.CONTRADICTION_CHECK,
        state=ReasonablenessGateState.PASSED,
        failure_code=None,
        residuals=(),
        source_claim_ref=binding_result.source_claim_ref,
        trace_ref=trace_ref,
    )


def _forbidden_leap_gate(
    *,
    forbidden_leap_detected: bool,
    source_claim_ref: str,
    trace_ref: str,
) -> ReasonablenessGateDecision:
    if forbidden_leap_detected:
        return _gate_decision(
            ReasonablenessGateKind.FORBIDDEN_LEAP_CHECK,
            state=ReasonablenessGateState.BLOCKED,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
            residuals=(),
            source_claim_ref=source_claim_ref,
            trace_ref=trace_ref,
        )
    return _gate_decision(
        ReasonablenessGateKind.FORBIDDEN_LEAP_CHECK,
        state=ReasonablenessGateState.PASSED,
        failure_code=None,
        residuals=(),
        source_claim_ref=source_claim_ref,
        trace_ref=trace_ref,
    )


def _rank_residual_policy_gate(
    *,
    rank_within_evidence: bool,
    residuals_visible: bool,
    source_claim_ref: str,
    residuals: tuple[OriginResidual, ...],
    trace_ref: str,
) -> ReasonablenessGateDecision:
    if not residuals_visible:
        return _gate_decision(
            ReasonablenessGateKind.RANK_RESIDUAL_POLICY,
            state=ReasonablenessGateState.REFUSED,
            failure_code=FailureCode.HIDDEN_RESIDUAL,
            residuals=residuals,
            source_claim_ref=source_claim_ref,
            trace_ref=trace_ref,
        )
    if not rank_within_evidence:
        return _gate_decision(
            ReasonablenessGateKind.RANK_RESIDUAL_POLICY,
            state=ReasonablenessGateState.BLOCKED,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            residuals=residuals,
            source_claim_ref=source_claim_ref,
            trace_ref=trace_ref,
        )
    return _gate_decision(
        ReasonablenessGateKind.RANK_RESIDUAL_POLICY,
        state=ReasonablenessGateState.PASSED,
        failure_code=None,
        residuals=residuals,
        source_claim_ref=source_claim_ref,
        trace_ref=trace_ref,
    )


def _gate_decision(
    gate: ReasonablenessGateKind,
    *,
    state: ReasonablenessGateState,
    failure_code: FailureCode | None,
    residuals: tuple[OriginResidual, ...],
    source_claim_ref: str,
    trace_ref: str,
) -> ReasonablenessGateDecision:
    return ReasonablenessGateDecision(
        gate=gate,
        state=state,
        failure_code=failure_code,
        residuals=residuals,
        source_claim_ref=source_claim_ref,
        trace_ref=trace_ref,
    )


def _derive_report_state(
    gates: tuple[ReasonablenessGateDecision, ...],
) -> tuple[ReasonablenessGateReportState, FailureCode | None]:
    for state in (
        ReasonablenessGateState.REFUSED,
        ReasonablenessGateState.BLOCKED,
        ReasonablenessGateState.DEFERRED,
    ):
        for gate in gates:
            if gate.state is state:
                report_state = {
                    ReasonablenessGateState.REFUSED: ReasonablenessGateReportState.REFUSED,
                    ReasonablenessGateState.BLOCKED: ReasonablenessGateReportState.BLOCKED,
                    ReasonablenessGateState.DEFERRED: ReasonablenessGateReportState.DEFERRED,
                }[state]
                return report_state, gate.failure_code
    return ReasonablenessGateReportState.LICENSED_FOR_VERDICT, None


def _report(
    state: ReasonablenessGateReportState,
    gates: tuple[ReasonablenessGateDecision, ...],
    *,
    failure_code: FailureCode | None,
    residuals: tuple[OriginResidual, ...],
    source_binding_ref: str,
    trace_ref: str,
) -> ReasonablenessGateReport:
    return ReasonablenessGateReport(
        state=state,
        gates=gates,
        failure_code=failure_code,
        residuals=residuals,
        source_binding_ref=source_binding_ref,
        trace_ref=trace_ref,
    )


__all__ = [
    "GPT_REASONABLENESS_GATES_TRANSITION_CONTRACT",
    "ReasonablenessGateDecision",
    "ReasonablenessGateKind",
    "ReasonablenessGateReport",
    "ReasonablenessGateReportState",
    "ReasonablenessGateSchemaError",
    "ReasonablenessGateState",
    "run_reasonableness_gates",
]
