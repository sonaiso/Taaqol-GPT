"""Acceptance tests for GPT-R3 MantuqGPT explicit-claim boundary.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law)
Branch         : GPT-R3 (MantuqGPT Claim Extraction)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses

import pytest

from taaqqul_slot_geometry.gpt import (
    ClaimBoundary,
    ExplicitClaim,
    GPTAnswerInput,
    InputEvidenceNeed,
    InputRiskLevel,
    InputTimeSensitivity,
    MantuqGPT,
    MantuqGPTSchemaError,
    build_mantuq_gpt,
    build_maqam_gpt,
)


def _make_maqam():
    answer_input = GPTAnswerInput(
        request_id="req-r3-001",
        user_question="هل جواب GPT معقول؟",
        gpt_answer="إن نجح زيد فأكرمه.",
        question_type_hint="factual",
        domain_hint="reasonableness-audit",
        constraints=("show-residuals",),
        evidence_need=InputEvidenceNeed.MEDIUM,
        risk_level=InputRiskLevel.MEDIUM,
        time_sensitivity=InputTimeSensitivity.STATIC,
        forbidden_answer_forms=("truth-declaration",),
        trace_ref="trace://gpt-r1/input/r3-001",
    )
    return build_maqam_gpt(answer_input, trace_ref="trace://gpt-r2/maqam/r3-001")


def _make_claim_boundary(source_maqam_ref: str) -> ClaimBoundary:
    claim = ExplicitClaim(
        claim_id="claim/condition/1",
        subject="زيد",
        predicate="إكرامه عند النجاح",
        qualifiers=("إن نجح",),
        modality="asserted",
        domain="reasonableness-audit",
        span_trace="trace://gpt-r3/span/condition/1",
    )
    return ClaimBoundary(
        claim=claim,
        source_maqam_ref=source_maqam_ref,
        trace_ref="trace://gpt-r3/claim-boundary/condition/1",
    )


def test_build_mantuq_gpt_preserves_explicit_claims_only() -> None:
    maqam = _make_maqam()
    boundary = _make_claim_boundary(maqam.trace_ref)

    mantuq = build_mantuq_gpt(
        maqam,
        answer_ref="answer://gpt/r3/001",
        explicit_claims=(boundary,),
        span_traces=("trace://gpt-r3/span/condition/1",),
        residuals=("MafhumGPT not opened at GPT-R3.",),
        trace_ref="trace://gpt-r3/mantuq/001",
    )

    assert mantuq == MantuqGPT(
        source_maqam_ref=maqam.trace_ref,
        answer_ref="answer://gpt/r3/001",
        explicit_claims=(boundary,),
        domain="reasonableness-audit",
        span_traces=("trace://gpt-r3/span/condition/1",),
        residuals=("MafhumGPT not opened at GPT-R3.",),
        trace_ref="trace://gpt-r3/mantuq/001",
    )
    assert not hasattr(mantuq, "implication")
    assert not hasattr(mantuq, "origin_binding")


def test_mantuq_gpt_is_frozen() -> None:
    maqam = _make_maqam()
    mantuq = build_mantuq_gpt(
        maqam,
        answer_ref="answer://gpt/r3/002",
        explicit_claims=(_make_claim_boundary(maqam.trace_ref),),
        span_traces=("trace://gpt-r3/span/condition/2",),
        residuals=("MafhumGPT not opened at GPT-R3.",),
        trace_ref="trace://gpt-r3/mantuq/002",
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        mantuq.domain = "modified"  # type: ignore[misc]


def test_mantuq_gpt_refuses_missing_explicit_claims() -> None:
    maqam = _make_maqam()

    with pytest.raises(MantuqGPTSchemaError):
        build_mantuq_gpt(
            maqam,
            answer_ref="answer://gpt/r3/003",
            explicit_claims=(),
            span_traces=("trace://gpt-r3/span/condition/3",),
            residuals=("No explicit claim was extracted.",),
            trace_ref="trace://gpt-r3/mantuq/003",
        )


def test_claim_boundary_must_preserve_maqam_trace() -> None:
    maqam = _make_maqam()
    bad_boundary = _make_claim_boundary("trace://gpt-r2/maqam/other")

    with pytest.raises(MantuqGPTSchemaError):
        build_mantuq_gpt(
            maqam,
            answer_ref="answer://gpt/r3/004",
            explicit_claims=(bad_boundary,),
            span_traces=("trace://gpt-r3/span/condition/4",),
            residuals=("Trace mismatch is forbidden.",),
            trace_ref="trace://gpt-r3/mantuq/004",
        )


def test_forbidden_later_symbols_still_absent_after_gpt_r3() -> None:
    import taaqqul_slot_geometry.gpt as gpt_module

    for forbidden in (
        "GPTAnswerReasonablenessVerdict",
        "ReasonablenessVerdict",
        "OriginBindingGate",
        "Pipeline",
        "NeedGate",
    ):
        assert not hasattr(gpt_module, forbidden)
