"""Acceptance tests for GPT-R6 Reasonableness Gates.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law) + docs/55
Branch         : GPT-R6 (Reasonableness Gates)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.gpt import (
    GPT_REASONABLENESS_GATES_TRANSITION_CONTRACT,
    BindingVerdict,
    OriginBinding,
    OriginBindingGateResult,
    OriginBindingGateState,
    OriginResidual,
    OriginResidualKind,
    ReasonablenessGateKind,
    ReasonablenessGateReportState,
    ReasonablenessGateSchemaError,
    ReasonablenessGateState,
    run_reasonableness_gates,
)
from taaqqul_slot_geometry.x0r import JumpTestInput


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
            trace_ref="trace://gpt-r5/binding/entity/1",
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
        trace_ref="trace://gpt-r5/gate-result/entity/1",
    )


def test_all_gates_pass_only_licenses_next_step() -> None:
    report = run_reasonableness_gates(
        _binding_result(),
        maqam_fit=True,
        evidence_supported=True,
        forbidden_leap_detected=False,
        rank_within_evidence=True,
        residuals_visible=True,
        trace_ref="trace://gpt-r6/report/passed/1",
    )

    assert report.state is ReasonablenessGateReportState.LICENSED_FOR_VERDICT
    assert report.failure_code is None
    assert len(report.gates) == 6
    assert all(gate.state is ReasonablenessGateState.PASSED for gate in report.gates)
    assert not hasattr(report, "reasonableness_verdict")
    assert not hasattr(report, "certificate")


def test_maqam_mismatch_blocks_without_final_verdict() -> None:
    report = run_reasonableness_gates(
        _binding_result(),
        maqam_fit=False,
        evidence_supported=True,
        forbidden_leap_detected=False,
        rank_within_evidence=True,
        residuals_visible=True,
        trace_ref="trace://gpt-r6/report/maqam-blocked/1",
    )

    maqam_gate = next(
        gate for gate in report.gates if gate.gate is ReasonablenessGateKind.MAQAM_FIT
    )
    assert report.state is ReasonablenessGateReportState.BLOCKED
    assert maqam_gate.state is ReasonablenessGateState.BLOCKED
    assert maqam_gate.failure_code is FailureCode.MAQAM_DIVERGENCE


def test_deferred_origin_binding_deferred_report() -> None:
    report = run_reasonableness_gates(
        _binding_result(state=OriginBindingGateState.DEFERRED),
        maqam_fit=True,
        evidence_supported=True,
        forbidden_leap_detected=False,
        rank_within_evidence=True,
        residuals_visible=True,
        trace_ref="trace://gpt-r6/report/origin-deferred/1",
    )

    origin_gate = next(
        gate for gate in report.gates if gate.gate is ReasonablenessGateKind.ORIGIN_BINDING
    )
    assert report.state is ReasonablenessGateReportState.DEFERRED
    assert origin_gate.state is ReasonablenessGateState.DEFERRED
    assert origin_gate.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


def test_contradicted_binding_blocks_contradiction_gate() -> None:
    contradicted_residual = OriginResidual(
        kind=OriginResidualKind.EVIDENCE_CONTRADICTED,
        description="Origin evidence contradicts the claim.",
        claim_ref="claim/entity/1",
    )
    report = run_reasonableness_gates(
        _binding_result(
            state=OriginBindingGateState.BLOCKED,
            verdict=BindingVerdict.CONTRADICTED,
            residuals=(contradicted_residual,),
        ),
        maqam_fit=True,
        evidence_supported=True,
        forbidden_leap_detected=False,
        rank_within_evidence=True,
        residuals_visible=True,
        trace_ref="trace://gpt-r6/report/contradicted/1",
    )

    contradiction_gate = next(
        gate for gate in report.gates if gate.gate is ReasonablenessGateKind.CONTRADICTION_CHECK
    )
    assert report.state is ReasonablenessGateReportState.BLOCKED
    assert contradiction_gate.state is ReasonablenessGateState.BLOCKED
    assert contradiction_gate.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


def test_forbidden_leap_blocks_gate_report() -> None:
    report = run_reasonableness_gates(
        _binding_result(),
        maqam_fit=True,
        evidence_supported=True,
        forbidden_leap_detected=True,
        rank_within_evidence=True,
        residuals_visible=True,
        trace_ref="trace://gpt-r6/report/forbidden-leap/1",
    )

    leap_gate = next(
        gate
        for gate in report.gates
        if gate.gate is ReasonablenessGateKind.FORBIDDEN_LEAP_CHECK
    )
    assert report.state is ReasonablenessGateReportState.BLOCKED
    assert leap_gate.state is ReasonablenessGateState.BLOCKED
    assert leap_gate.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_hidden_residual_refuses_rank_residual_policy_gate() -> None:
    visible_residual = OriginResidual(
        kind=OriginResidualKind.BINDING_AMBIGUOUS,
        description="A visible residual exists and must not be hidden.",
        claim_ref="claim/entity/1",
    )
    report = run_reasonableness_gates(
        _binding_result(residuals=(visible_residual,)),
        maqam_fit=True,
        evidence_supported=True,
        forbidden_leap_detected=False,
        rank_within_evidence=True,
        residuals_visible=False,
        trace_ref="trace://gpt-r6/report/hidden-residual/1",
    )

    policy_gate = next(
        gate for gate in report.gates if gate.gate is ReasonablenessGateKind.RANK_RESIDUAL_POLICY
    )
    assert report.state is ReasonablenessGateReportState.REFUSED
    assert policy_gate.state is ReasonablenessGateState.REFUSED
    assert policy_gate.failure_code is FailureCode.HIDDEN_RESIDUAL


def test_missing_binding_refuses_gate_sequence() -> None:
    report = run_reasonableness_gates(
        None,
        maqam_fit=True,
        evidence_supported=True,
        forbidden_leap_detected=False,
        rank_within_evidence=True,
        residuals_visible=True,
        trace_ref="trace://gpt-r6/report/missing-binding/1",
    )

    assert report.state is ReasonablenessGateReportState.REFUSED
    assert report.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
    assert len(report.gates) == 1
    assert report.gates[0].gate is ReasonablenessGateKind.ORIGIN_BINDING


def test_transition_contract_refuses_missing_trace() -> None:
    result = GPT_REASONABLENESS_GATES_TRANSITION_CONTRACT.evaluate(
        JumpTestInput(
            source_level="OriginBindingGateResult",
            target_level="MaqamFitGate",
            transition_name="check_maqam_fit",
            domain="gpt_reasonableness",
            trace_ref="",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(),
        )
    )

    assert result.allowed is False
    assert result.failure_code is FailureCode.TRACE_MISSING


def test_report_requires_nonempty_gate_tuple() -> None:
    with pytest.raises(ReasonablenessGateSchemaError):
        from taaqqul_slot_geometry.gpt.reasonableness_gates import ReasonablenessGateReport

        ReasonablenessGateReport(
            state=ReasonablenessGateReportState.REFUSED,
            gates=(),
            failure_code=FailureCode.GATE_REQUIRED,
            residuals=(),
            source_binding_ref="trace://gpt-r6/binding/invalid",
            trace_ref="trace://gpt-r6/report/invalid",
        )
