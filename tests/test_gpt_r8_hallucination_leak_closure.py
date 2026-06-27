"""Acceptance tests for GPT-R8 hallucination leak closure.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law) + docs/55
Branch         : GPT-R8-HALLUCINATION-LEAK-CLOSURE
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.gpt import (
    BindingEvidenceType,
    BindingVerdict,
    DomainBridgeCard,
    DomainBridgeResult,
    EllipsisEstimate,
    EllipsisQarinahType,
    GPTAnswerReasonablenessVerdict,
    HallucinationLeakGateState,
    OriginBinding,
    OriginBindingGateResult,
    OriginBindingGateState,
    OriginCarrierSchemaError,
    OriginRank,
    OriginResidual,
    OriginResidualKind,
    ReasonablenessGateReportState,
    ReasonablenessVerdictState,
    ReferenceBindingEvidence,
    ResolutionType,
    evaluate_domain_bridge,
    evaluate_reference_binding,
    license_ellipsis_estimate,
    refuse_r7_as_final_audit,
)


def _reference_evidence(
    *,
    binding_evidence_type: BindingEvidenceType = BindingEvidenceType.EXPLICIT_PRIOR_TEXT,
    competing_referents: tuple[str, ...] = (),
) -> ReferenceBindingEvidence:
    return ReferenceBindingEvidence(
        reference_id="ref/pronoun/huwa",
        reference_surface="هو",
        reference_trace_ref="trace://gpt-r8/reference/huwa",
        candidate_referent="زيد",
        referent_trace_ref="trace://gpt-r8/referent/zayd",
        binding_evidence_type=binding_evidence_type,
        binding_evidence_trace_ref="trace://gpt-r8/reference/evidence/zayd",
        resolution_type=ResolutionType.ANAPHORIC,
        resolution_rank=OriginRank.HIGH,
        competing_referents=competing_referents,
        blocking_residuals=(),
    )


def _ellipsis(
    *,
    qarinah_type: EllipsisQarinahType = EllipsisQarinahType.PREVIOUS_QUESTION,
    alternatives: tuple[str, ...] = (),
) -> EllipsisEstimate:
    return EllipsisEstimate(
        ellipsis_id="ellipsis/zayd-answer",
        missing_slot="predicate",
        proposed_fill="حضر زيد",
        opening_trigger="fragment answer after question",
        qarinah_type=qarinah_type,
        qarinah_trace_ref="trace://gpt-r8/qarinah/previous-question",
        license_reason="previous question supplies the missing predicate slot",
        alternatives=alternatives,
        closure_effect="maqami_complete",
        residuals=(),
        rank=OriginRank.HIGH,
    )


def _domain_bridge(*, qadih_difference_check: bool = True) -> DomainBridgeCard:
    return DomainBridgeCard(
        source_domain="linguistic-generality",
        target_domain="legal-certainty",
        source_claim="اللفظ عام",
        target_claim="الحكم الشرعي قطعي",
        preserved_manat="licensed general wording under preserved scope",
        common_illah="generality is relevant only under scoped evidence",
        effective_description="domain transfer is bounded by preserved manāṭ",
        qadih_difference_check=qadih_difference_check,
        bridge_evidence_trace_ref="trace://gpt-r8/domain-bridge/evidence",
        rank_ceiling=Rank.CANDIDATE,
        residual_transfer_policy="residuals stay visible across bridge",
        result=DomainBridgeResult.BRIDGED,
    )


def _r7_verdict() -> GPTAnswerReasonablenessVerdict:
    return GPTAnswerReasonablenessVerdict(
        state=ReasonablenessVerdictState.REASONABLE,
        source_gate_report_state=ReasonablenessGateReportState.LICENSED_FOR_VERDICT,
        failure_code=None,
        residuals=(),
        rank=Rank.LICENSED,
        rank_ceiling=Rank.LICENSED,
        source_gate_report_ref="trace://gpt-r6/report/r8",
        source_binding_ref="trace://gpt-r5/binding/r8",
        trace_ref="trace://gpt-r7/verdict/r8",
    )


def test_reference_origin_requires_internal_trace() -> None:
    with pytest.raises(OriginCarrierSchemaError, match="reference_trace_ref"):
        ReferenceBindingEvidence(
            reference_id="ref/pronoun/huwa",
            reference_surface="هو",
            reference_trace_ref="",
            candidate_referent="زيد",
            referent_trace_ref="trace://gpt-r8/referent/zayd",
            binding_evidence_type=BindingEvidenceType.EXPLICIT_PRIOR_TEXT,
            binding_evidence_trace_ref="trace://gpt-r8/reference/evidence/zayd",
            resolution_type=ResolutionType.ANAPHORIC,
            resolution_rank=OriginRank.HIGH,
            competing_referents=(),
            blocking_residuals=(),
        )

    result = evaluate_reference_binding(None, trace_ref="trace://gpt-r8/reference/missing")

    assert result.state is HallucinationLeakGateState.DEFERRED
    assert result.failure_code is FailureCode.REFERENCE_WITHOUT_TRACE
    assert result.residuals[0].kind is OriginResidualKind.REFERENCE_WITHOUT_TRACE


def test_reference_probability_only_is_not_license() -> None:
    result = evaluate_reference_binding(
        _reference_evidence(binding_evidence_type=BindingEvidenceType.PROBABILITY_ONLY),
        trace_ref="trace://gpt-r8/reference/probability-only",
    )

    assert result.state is HallucinationLeakGateState.BLOCKED
    assert result.failure_code is FailureCode.REFERENCE_RESOLVED_BY_PROBABILITY_ONLY
    assert result.residuals[0].kind is OriginResidualKind.REFERENCE_RESOLVED_BY_PROBABILITY_ONLY


def test_reference_binding_with_competitor_is_blocked() -> None:
    result = evaluate_reference_binding(
        _reference_evidence(competing_referents=("عمرو",)),
        trace_ref="trace://gpt-r8/reference/competitor",
    )

    assert result.state is HallucinationLeakGateState.BLOCKED
    assert result.failure_code is FailureCode.REFERENCE_BINDING_COMPETITOR_UNHANDLED


def test_unlicensed_ellipsis_is_rejected() -> None:
    result = license_ellipsis_estimate(None, trace_ref="trace://gpt-r8/ellipsis/no-qarinah")

    assert result.state is HallucinationLeakGateState.DEFERRED
    assert result.failure_code is FailureCode.MISSING_QARINAH_FOR_DELETION
    assert result.residuals[0].kind is OriginResidualKind.MISSING_QARINAH_FOR_DELETION


def test_question_licenses_ellipsis_fill() -> None:
    result = license_ellipsis_estimate(
        _ellipsis(),
        trace_ref="trace://gpt-r8/ellipsis/previous-question",
    )

    assert result.state is HallucinationLeakGateState.PASSED
    assert result.failure_code is None


def test_probability_only_ellipsis_is_rejected() -> None:
    result = license_ellipsis_estimate(
        _ellipsis(qarinah_type=EllipsisQarinahType.STATISTICAL_LIKELIHOOD),
        trace_ref="trace://gpt-r8/ellipsis/probability-only",
    )

    assert result.state is HallucinationLeakGateState.BLOCKED
    assert result.failure_code is FailureCode.ELLIPSIS_FILLED_BY_PROBABILITY_ONLY


def test_domain_transfer_without_manat_is_rejected() -> None:
    result = evaluate_domain_bridge(None, trace_ref="trace://gpt-r8/domain/missing-manat")

    assert result.state is HallucinationLeakGateState.BLOCKED
    assert result.failure_code is FailureCode.DOMAIN_TRANSFER_WITHOUT_MANAT
    assert result.residuals[0].kind is OriginResidualKind.DOMAIN_TRANSFER_WITHOUT_MANAT


def test_qadih_difference_blocks_domain_bridge() -> None:
    result = evaluate_domain_bridge(
        _domain_bridge(qadih_difference_check=False),
        trace_ref="trace://gpt-r8/domain/qadih-unchecked",
    )

    assert result.state is HallucinationLeakGateState.BLOCKED
    assert result.failure_code is FailureCode.QADIH_DIFFERENCE_UNCHECKED


def test_closed_domain_bridge_passes_without_truth_or_certificate() -> None:
    result = evaluate_domain_bridge(
        _domain_bridge(),
        trace_ref="trace://gpt-r8/domain/bridged",
    )

    assert result.state is HallucinationLeakGateState.PASSED
    assert result.failure_code is None
    assert not hasattr(result, "truth")
    assert not hasattr(result, "certificate")


def test_r7_verdict_cannot_be_consumed_as_answer_audit() -> None:
    verdict = _r7_verdict()
    result = refuse_r7_as_final_audit(verdict, trace_ref="trace://gpt-r8/r7/not-audit")

    assert verdict.integration_status == "pre_audit_verdict"
    assert verdict.not_final_audit is True
    assert verdict.requires_r8_audit_integration is True
    assert verdict.certificate_allowed is False
    assert result.state is HallucinationLeakGateState.BLOCKED
    assert result.failure_code is FailureCode.PREMATURE_R7_AUDIT_CONSUMPTION
    assert result.residuals[0].kind is OriginResidualKind.PREMATURE_R7_AUDIT_CONSUMPTION


def test_origin_binding_can_surface_new_leak_residuals() -> None:
    residual = OriginResidual(
        kind=OriginResidualKind.REFERENCE_WITHOUT_TRACE,
        description="Reference binding has no internal trace.",
        claim_ref="claim/reference/huwa",
    )
    binding = OriginBinding(
        claim_ref="claim/reference/huwa",
        origin_type="ReferenceOrigin",
        origin_id="ref/pronoun/huwa",
        verdict=BindingVerdict.UNSUPPORTED,
        residuals=(residual,),
        trace_ref="trace://gpt-r5/binding/reference-without-trace",
    )
    result = OriginBindingGateResult(
        state=OriginBindingGateState.DEFERRED,
        binding=binding,
        failure_code=FailureCode.REFERENCE_WITHOUT_TRACE,
        residuals=(residual,),
        source_claim_ref="claim/reference/huwa",
        trace_ref="trace://gpt-r5/gate/reference-without-trace",
    )

    assert result.failure_code is FailureCode.REFERENCE_WITHOUT_TRACE
    assert result.residuals == (residual,)
