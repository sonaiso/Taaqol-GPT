"""Acceptance tests for GPT-R7 GPTAnswerReasonablenessVerdict.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law) + docs/55
Branch         : GPT-R7 (bounded reasonableness verdict)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.gpt import (
    BindingVerdict,
    GPTAnswerReasonablenessVerdict,
    OriginBinding,
    OriginBindingGateResult,
    OriginBindingGateState,
    OriginResidual,
    OriginResidualKind,
    ReasonablenessGateKind,
    ReasonablenessGateReportState,
    ReasonablenessGateState,
    ReasonablenessVerdictSchemaError,
    ReasonablenessVerdictState,
    prove_gpt_answer_reasonableness_verdict,
    run_reasonableness_gates,
)


def _binding_result(
    *,
    state: OriginBindingGateState = OriginBindingGateState.BOUND,
    verdict: BindingVerdict = BindingVerdict.COMPATIBLE,
    residuals: tuple[OriginResidual, ...] = (),
) -> OriginBindingGateResult:
    binding = (
        OriginBinding(
            claim_ref="claim/entity/r7",
            origin_type="EntityGenusOrigin",
            origin_id="entity/zayd",
            verdict=verdict,
            residuals=residuals,
            trace_ref="trace://gpt-r5/binding/r7/entity",
        )
        if state is not OriginBindingGateState.REFUSED
        else None
    )
    failure_code = None
    if state is OriginBindingGateState.BLOCKED:
        failure_code = FailureCode.BLOCKING_RESIDUAL_PRESENT
    elif state is OriginBindingGateState.DEFERRED:
        failure_code = FailureCode.REQUIRED_SLOT_EMPTY
    elif state is OriginBindingGateState.REFUSED:
        failure_code = FailureCode.GATE_REQUIRED
    return OriginBindingGateResult(
        state=state,
        binding=binding,
        failure_code=failure_code,
        residuals=residuals,
        source_claim_ref="claim/entity/r7",
        trace_ref="trace://gpt-r5/gate-result/r7/entity",
    )


def _r6_report(
    *,
    binding_result: OriginBindingGateResult | None = None,
    maqam_fit: bool = True,
    evidence_supported: bool = True,
    forbidden_leap_detected: bool = False,
    rank_within_evidence: bool = True,
    residuals_visible: bool = True,
    trace_ref: str = "trace://gpt-r6/report/r7/default",
):
    return run_reasonableness_gates(
        binding_result if binding_result is not None else _binding_result(),
        maqam_fit=maqam_fit,
        evidence_supported=evidence_supported,
        forbidden_leap_detected=forbidden_leap_detected,
        rank_within_evidence=rank_within_evidence,
        residuals_visible=residuals_visible,
        trace_ref=trace_ref,
    )


def test_all_passed_r6_report_produces_bounded_positive_verdict() -> None:
    report = _r6_report(trace_ref="trace://gpt-r6/report/r7/passed")

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/passed",
    )

    assert verdict.state is ReasonablenessVerdictState.REASONABLE
    assert verdict.source_report_state is ReasonablenessGateReportState.LICENSED_FOR_VERDICT
    assert verdict.failure_code is None
    assert verdict.source_gate_report_ref == report.trace_ref
    assert verdict.source_binding_ref == report.source_binding_ref
    assert not hasattr(verdict, "answer_audit")
    assert not hasattr(verdict, "certificate")
    assert not hasattr(verdict, "authority_approved")


def test_blocked_r6_report_maps_to_unreasonable_verdict() -> None:
    report = _r6_report(
        maqam_fit=False,
        trace_ref="trace://gpt-r6/report/r7/maqam-blocked",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/maqam-blocked",
    )

    assert report.state is ReasonablenessGateReportState.BLOCKED
    assert verdict.state is ReasonablenessVerdictState.UNREASONABLE
    assert verdict.failure_code is FailureCode.MAQAM_DIVERGENCE


def test_deferred_r6_report_maps_to_deferred_verdict() -> None:
    report = _r6_report(
        binding_result=_binding_result(state=OriginBindingGateState.DEFERRED),
        trace_ref="trace://gpt-r6/report/r7/deferred",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/deferred",
    )

    assert report.state is ReasonablenessGateReportState.DEFERRED
    assert verdict.state is ReasonablenessVerdictState.DEFERRED
    assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


def test_visible_residuals_and_trace_are_preserved() -> None:
    residual = OriginResidual(
        kind=OriginResidualKind.BINDING_AMBIGUOUS,
        description="Visible ambiguity remains after origin binding.",
        claim_ref="claim/entity/r7",
    )
    report = _r6_report(
        binding_result=_binding_result(residuals=(residual,)),
        trace_ref="trace://gpt-r6/report/r7/visible-residual",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/visible-residual",
    )

    assert verdict.residuals == (residual,)
    assert verdict.source_gate_report_ref == "trace://gpt-r6/report/r7/visible-residual"
    assert verdict.trace_ref == "trace://gpt-r7/verdict/visible-residual"
    assert verdict.rank_ceiling is report.state


def test_missing_r6_report_refuses_verdict() -> None:
    verdict = prove_gpt_answer_reasonableness_verdict(
        None,
        trace_ref="trace://gpt-r7/verdict/missing-report",
    )

    assert verdict.state is ReasonablenessVerdictState.REFUSED
    assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
    assert verdict.source_report_state is ReasonablenessGateReportState.REFUSED


def test_missing_trace_is_schema_refused() -> None:
    with pytest.raises(ReasonablenessVerdictSchemaError):
        prove_gpt_answer_reasonableness_verdict(_r6_report(), trace_ref="")


def test_hidden_residual_refuses_verdict() -> None:
    residual = OriginResidual(
        kind=OriginResidualKind.BINDING_AMBIGUOUS,
        description="Visible residual must not be hidden.",
        claim_ref="claim/entity/r7",
    )
    report = _r6_report(
        binding_result=_binding_result(residuals=(residual,)),
        residuals_visible=False,
        trace_ref="trace://gpt-r6/report/r7/hidden-residual",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/hidden-residual",
    )

    assert report.state is ReasonablenessGateReportState.REFUSED
    assert verdict.state is ReasonablenessVerdictState.REFUSED
    assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL
    assert verdict.residuals == (residual,)


def test_forbidden_leap_cannot_become_positive_verdict() -> None:
    report = _r6_report(
        forbidden_leap_detected=True,
        trace_ref="trace://gpt-r6/report/r7/forbidden-leap",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/forbidden-leap",
    )

    assert report.state is ReasonablenessGateReportState.BLOCKED
    assert verdict.state is not ReasonablenessVerdictState.REASONABLE
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_failed_evidence_support_cannot_become_positive_verdict() -> None:
    report = _r6_report(
        evidence_supported=False,
        trace_ref="trace://gpt-r6/report/r7/evidence-deferred",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/evidence-deferred",
    )

    evidence_gate = next(
        gate for gate in report.gates if gate.gate is ReasonablenessGateKind.EVIDENCE_SUPPORT
    )
    assert evidence_gate.state is ReasonablenessGateState.DEFERRED
    assert verdict.state is ReasonablenessVerdictState.DEFERRED
    assert verdict.state is not ReasonablenessVerdictState.REASONABLE


def test_rank_promotion_above_gate_report_is_refused() -> None:
    report = _r6_report(
        maqam_fit=False,
        trace_ref="trace://gpt-r6/report/r7/rank-promotion",
    )

    with pytest.raises(ReasonablenessVerdictSchemaError):
        GPTAnswerReasonablenessVerdict(
            state=ReasonablenessVerdictState.REASONABLE,
            source_report_state=report.state,
            source_gate_report_ref=report.trace_ref,
            source_binding_ref=report.source_binding_ref,
            failure_code=None,
            residuals=report.residuals,
            rank_ceiling=report.state,
            trace_ref="trace://gpt-r7/verdict/rank-promotion",
        )


def test_answer_audit_certificate_authority_and_truth_semantics_absent() -> None:
    import taaqqul_slot_geometry.gpt as gpt_module

    forbidden_symbols = {
        "AnswerAudit",
        "Certificate",
        "AuthorityApproved",
        "TruthVerdict",
        "RealityVerdict",
        "ExecutionOrder",
    }
    assert forbidden_symbols.isdisjoint(set(gpt_module.__all__))
