"""Acceptance tests for GPT-R7 GPTAnswerReasonablenessVerdict.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law) + docs/55
Branch         : GPT-R7 (GPTAnswerReasonablenessVerdict)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.gpt import (
    GPT_REASONABLENESS_VERDICT_TRANSITION_CONTRACT,
    BindingVerdict,
    GPTAnswerReasonablenessVerdict,
    OriginBinding,
    OriginBindingGateResult,
    OriginBindingGateState,
    OriginResidual,
    OriginResidualKind,
    ReasonablenessGateReportState,
    ReasonablenessVerdictSchemaError,
    ReasonablenessVerdictState,
    run_reasonableness_gates,
)
from taaqqul_slot_geometry.gpt.reasonableness_verdict import (
    prove_gpt_answer_reasonableness_verdict,
)
from taaqqul_slot_geometry.x0r import JumpTestInput, QadihCheckStatus


def _binding_result(
    *,
    state: OriginBindingGateState = OriginBindingGateState.BOUND,
    verdict: BindingVerdict = BindingVerdict.COMPATIBLE,
    residuals: tuple[OriginResidual, ...] = (),
) -> OriginBindingGateResult:
    binding = (
        OriginBinding(
            claim_ref="claim/entity/1",
            origin_type="EntityGenusOrigin",
            origin_id="entity/zayd",
            verdict=verdict,
            residuals=residuals,
            trace_ref="trace://gpt-r5/binding/r7/entity/1",
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
        source_claim_ref="claim/entity/1",
        trace_ref="trace://gpt-r5/gate-result/r7/entity/1",
    )


def _report(
    *,
    maqam_fit: bool = True,
    evidence_supported: bool = True,
    forbidden_leap_detected: bool = False,
    rank_within_evidence: bool = True,
    residuals_visible: bool = True,
    binding_result: OriginBindingGateResult | None = None,
    trace_ref: str = "trace://gpt-r6/report/r7/1",
):
    return run_reasonableness_gates(
        _binding_result() if binding_result is None else binding_result,
        maqam_fit=maqam_fit,
        evidence_supported=evidence_supported,
        forbidden_leap_detected=forbidden_leap_detected,
        rank_within_evidence=rank_within_evidence,
        residuals_visible=residuals_visible,
        trace_ref=trace_ref,
    )


def test_minimal_accepted_r6_report_maps_to_reasonable_verdict() -> None:
    report = _report(trace_ref="trace://gpt-r6/report/r7/passed")

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/passed",
    )

    assert isinstance(verdict, GPTAnswerReasonablenessVerdict)
    assert verdict.state is ReasonablenessVerdictState.REASONABLE
    assert verdict.source_gate_report_state is ReasonablenessGateReportState.LICENSED_FOR_VERDICT
    assert verdict.failure_code is None
    assert verdict.rank is Rank.LICENSED
    assert verdict.rank_ceiling is Rank.LICENSED
    assert verdict.source_gate_report_ref == report.trace_ref
    assert verdict.source_binding_ref == report.source_binding_ref
    assert verdict.trace_ref == "trace://gpt-r7/verdict/passed"
    assert not hasattr(verdict, "answer_audit")
    assert not hasattr(verdict, "certificate")
    assert not hasattr(verdict, "authority_approved")


def test_blocked_r6_report_maps_to_blocked_verdict_not_reasonable() -> None:
    report = _report(maqam_fit=False, trace_ref="trace://gpt-r6/report/r7/off-maqam")

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/off-maqam",
    )

    assert verdict.state is ReasonablenessVerdictState.OFF_MAQAM
    assert verdict.failure_code is FailureCode.MAQAM_DIVERGENCE
    assert verdict.rank is Rank.CANDIDATE
    assert verdict.rank_ceiling is Rank.CANDIDATE


def test_deferred_r6_report_maps_to_deferred_or_unsupported_verdict() -> None:
    report = _report(
        evidence_supported=False,
        trace_ref="trace://gpt-r6/report/r7/evidence-deferred",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/evidence-deferred",
    )

    assert verdict.state is ReasonablenessVerdictState.UNSUPPORTED
    assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
    assert verdict.source_gate_report_state is ReasonablenessGateReportState.DEFERRED


def test_visible_residuals_are_preserved_from_r6_report() -> None:
    residual = OriginResidual(
        kind=OriginResidualKind.BINDING_AMBIGUOUS,
        description="Compatible binding still leaves a visible ambiguity.",
        claim_ref="claim/entity/1",
    )
    report = _report(
        binding_result=_binding_result(residuals=(residual,)),
        trace_ref="trace://gpt-r6/report/r7/visible-residual",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/visible-residual",
    )

    assert verdict.state is ReasonablenessVerdictState.REASONABLE
    assert verdict.residuals == (residual,)


def test_missing_r6_report_refuses_verdict() -> None:
    verdict = prove_gpt_answer_reasonableness_verdict(
        None,
        trace_ref="trace://gpt-r7/verdict/missing-report",
    )

    assert verdict.state is ReasonablenessVerdictState.REFUSED
    assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
    assert verdict.source_gate_report_state is ReasonablenessGateReportState.REFUSED


def test_missing_trace_refuses_jump_contract() -> None:
    result = GPT_REASONABLENESS_VERDICT_TRANSITION_CONTRACT.evaluate(
        JumpTestInput(
            source_level="ReasonablenessGateReport",
            target_level="GPTAnswerReasonablenessVerdict",
            transition_name="prove_gpt_answer_reasonableness_verdict",
            domain="gpt_reasonableness",
            trace_ref="",
            origin="asl://gpt-r7/gates",
            branch="far://gpt-r7/verdict",
            handoff="handoff://gpt-r7/verdict",
            rank=3,
            rank_ceiling=5,
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            residual_visible=True,
            differentiating_feature_verified=True,
            qadih_status=QadihCheckStatus.CLEAR,
            residual_kinds=(),
        )
    )

    assert result.allowed is False
    assert result.failure_code is FailureCode.TRACE_MISSING


def test_hidden_residual_refusal_remains_refused_verdict() -> None:
    residual = OriginResidual(
        kind=OriginResidualKind.BINDING_AMBIGUOUS,
        description="Hidden residual attempt must refuse R6 and R7.",
        claim_ref="claim/entity/1",
    )
    report = _report(
        binding_result=_binding_result(residuals=(residual,)),
        residuals_visible=False,
        trace_ref="trace://gpt-r6/report/r7/hidden-residual",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/hidden-residual",
    )

    assert verdict.state is ReasonablenessVerdictState.REFUSED
    assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL
    assert verdict.residuals == (residual,)


def test_forbidden_leap_cannot_become_positive_verdict() -> None:
    report = _report(
        forbidden_leap_detected=True,
        trace_ref="trace://gpt-r6/report/r7/forbidden-leap",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/forbidden-leap",
    )

    assert verdict.state is ReasonablenessVerdictState.FORBIDDEN_LEAP
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_contradicted_origin_cannot_become_positive_verdict() -> None:
    residual = OriginResidual(
        kind=OriginResidualKind.EVIDENCE_CONTRADICTED,
        description="Origin evidence contradicts the claim.",
        claim_ref="claim/entity/1",
    )
    report = _report(
        binding_result=_binding_result(
            state=OriginBindingGateState.BLOCKED,
            verdict=BindingVerdict.CONTRADICTED,
            residuals=(residual,),
        ),
        trace_ref="trace://gpt-r6/report/r7/contradicted",
    )

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/contradicted",
    )

    assert verdict.state is ReasonablenessVerdictState.CONTRADICTORY
    assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


def test_rank_promotion_above_r6_ceiling_is_refused() -> None:
    report = _report(trace_ref="trace://gpt-r6/report/r7/rank-promotion")

    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/rank-promotion",
        requested_rank=Rank.STRONG,
    )

    assert verdict.state is ReasonablenessVerdictState.REFUSED
    assert verdict.failure_code is FailureCode.RANK_EXCEEDS_CEILING
    assert verdict.rank is Rank.LICENSED
    assert verdict.rank_ceiling is Rank.LICENSED


def test_certificate_rank_is_rejected_at_schema_boundary() -> None:
    certificate_rank = getattr(Rank, "CERTIFICATE")
    with pytest.raises(ReasonablenessVerdictSchemaError):
        GPTAnswerReasonablenessVerdict(
            state=ReasonablenessVerdictState.REASONABLE,
            source_gate_report_state=ReasonablenessGateReportState.LICENSED_FOR_VERDICT,
            failure_code=None,
            residuals=(),
            rank=certificate_rank,
            rank_ceiling=certificate_rank,
            source_gate_report_ref="trace://gpt-r6/report/certificate",
            source_binding_ref="trace://gpt-r5/binding/certificate",
            trace_ref="trace://gpt-r7/verdict/certificate",
        )


def test_answer_audit_and_certificate_surfaces_remain_unproduced() -> None:
    import taaqqul_slot_geometry.gpt as gpt_module

    report = _report(trace_ref="trace://gpt-r6/report/r7/no-audit")
    verdict = prove_gpt_answer_reasonableness_verdict(
        report,
        trace_ref="trace://gpt-r7/verdict/no-audit",
    )

    assert not hasattr(verdict, "audit")
    assert not hasattr(verdict, "answer_audit")
    assert not hasattr(verdict, "certificate")
    for forbidden in (
        "AnswerAudit",
        "AuditIntegration",
        "Certificate",
        "AuthorityApproved",
        "ReasonablenessPipeline",
    ):
        assert not hasattr(gpt_module, forbidden)
