"""Acceptance tests for GPT-R2 MaqamGPT boundary surface.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law)
Branch         : GPT-R2 (MaqamGPT Boundary)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses

import pytest

from taaqqul_slot_geometry.gpt import (
    GPTAnswerInput,
    InputEvidenceNeed,
    InputRiskLevel,
    InputTimeSensitivity,
    MaqamCommunicationMode,
    MaqamGPT,
    MaqamGPTSchemaError,
    build_maqam_gpt,
    classify_maqam_communication_mode,
)


def _make_input() -> GPTAnswerInput:
    return GPTAnswerInput(
        request_id="req-r2-001",
        user_question="هل هذه الدعوى مدعومة بدليل ظاهر؟",
        gpt_answer="الدعوى تحتاج إلى توثيق إضافي.",
        question_type_hint="factual",
        domain_hint="reasonableness-audit",
        constraints=("no-overclaim", "show-residuals"),
        evidence_need=InputEvidenceNeed.HIGH,
        risk_level=InputRiskLevel.HIGH,
        time_sensitivity=InputTimeSensitivity.TIME_BOUND,
        forbidden_answer_forms=("truth-declaration", "certificate-language"),
        trace_ref="trace://gpt-r1/input/r2-001",
    )


def test_build_maqam_gpt_preserves_input_context_only() -> None:
    maqam = build_maqam_gpt(_make_input(), trace_ref="trace://gpt-r2/maqam/001")

    assert maqam == MaqamGPT(
        request_id="req-r2-001",
        user_question="هل هذه الدعوى مدعومة بدليل ظاهر؟",
        question_type="factual",
        communication_mode=MaqamCommunicationMode.IKHBAR,
        domain="reasonableness-audit",
        constraints=("no-overclaim", "show-residuals"),
        evidence_need=InputEvidenceNeed.HIGH,
        risk_level=InputRiskLevel.HIGH,
        time_sensitivity=InputTimeSensitivity.TIME_BOUND,
        forbidden_answer_forms=("truth-declaration", "certificate-language"),
        source_trace_ref="trace://gpt-r1/input/r2-001",
        trace_ref="trace://gpt-r2/maqam/001",
    )
    assert not hasattr(maqam, "gpt_answer")


def test_maqam_gpt_is_frozen() -> None:
    maqam = build_maqam_gpt(_make_input(), trace_ref="trace://gpt-r2/maqam/002")

    with pytest.raises(dataclasses.FrozenInstanceError):
        maqam.domain = "modified"  # type: ignore[misc]


def test_build_maqam_gpt_requires_gpt_answer_input() -> None:
    with pytest.raises(MaqamGPTSchemaError):
        build_maqam_gpt("not-input", trace_ref="trace://gpt-r2/maqam/003")  # type: ignore[arg-type]


def test_maqam_trace_ref_must_use_trace_scheme() -> None:
    with pytest.raises(MaqamGPTSchemaError):
        build_maqam_gpt(_make_input(), trace_ref="bad://gpt-r2/maqam/004")


def test_maqam_constraints_must_be_tuple_of_nonempty_strings() -> None:
    with pytest.raises(MaqamGPTSchemaError):
        MaqamGPT(
            request_id="req-r2-005",
            user_question="q",
            question_type="factual",
            communication_mode=MaqamCommunicationMode.IKHBAR,
            domain="general",
            constraints=("ok", ""),
            evidence_need=InputEvidenceNeed.LOW,
            risk_level=InputRiskLevel.LOW,
            time_sensitivity=InputTimeSensitivity.STATIC,
            forbidden_answer_forms=(),
            source_trace_ref="trace://gpt-r1/input/r2-005",
            trace_ref="trace://gpt-r2/maqam/005",
        )


def test_question_type_hint_classifies_ikhbar_maqam() -> None:
    maqam = build_maqam_gpt(_make_input(), trace_ref="trace://gpt-r2/maqam/006")

    assert maqam.communication_mode is MaqamCommunicationMode.IKHBAR
    assert classify_maqam_communication_mode("إخبار") is MaqamCommunicationMode.IKHBAR


def test_question_type_hint_classifies_insha_maqam() -> None:
    answer_input = GPTAnswerInput(
        request_id="req-r2-007",
        user_question="اكتب صياغة موجزة لهذه الفكرة.",
        gpt_answer="صياغة مقترحة.",
        question_type_hint="creative",
        domain_hint="reasonableness-audit",
        constraints=("preserve-residuals",),
        evidence_need=InputEvidenceNeed.LOW,
        risk_level=InputRiskLevel.LOW,
        time_sensitivity=InputTimeSensitivity.STATIC,
        forbidden_answer_forms=("truth-declaration",),
        trace_ref="trace://gpt-r1/input/r2-007",
    )

    maqam = build_maqam_gpt(answer_input, trace_ref="trace://gpt-r2/maqam/007")

    assert maqam.communication_mode is MaqamCommunicationMode.INSHA
    assert classify_maqam_communication_mode("إنشاء") is MaqamCommunicationMode.INSHA


def test_question_type_hint_must_classify_as_ikhbar_or_insha() -> None:
    answer_input = GPTAnswerInput(
        request_id="req-r2-008",
        user_question="q",
        gpt_answer="a",
        question_type_hint="unlicensed-mode",
        domain_hint="reasonableness-audit",
        constraints=("show-residuals",),
        evidence_need=InputEvidenceNeed.LOW,
        risk_level=InputRiskLevel.LOW,
        time_sensitivity=InputTimeSensitivity.STATIC,
        forbidden_answer_forms=("truth-declaration",),
        trace_ref="trace://gpt-r1/input/r2-008",
    )

    with pytest.raises(MaqamGPTSchemaError):
        build_maqam_gpt(answer_input, trace_ref="trace://gpt-r2/maqam/008")


def test_communication_mode_must_match_question_type() -> None:
    with pytest.raises(MaqamGPTSchemaError):
        MaqamGPT(
            request_id="req-r2-009",
            user_question="q",
            question_type="factual",
            communication_mode=MaqamCommunicationMode.INSHA,
            domain="general",
            constraints=("ok",),
            evidence_need=InputEvidenceNeed.LOW,
            risk_level=InputRiskLevel.LOW,
            time_sensitivity=InputTimeSensitivity.STATIC,
            forbidden_answer_forms=("truth-declaration",),
            source_trace_ref="trace://gpt-r1/input/r2-009",
            trace_ref="trace://gpt-r2/maqam/009",
        )


def test_forbidden_future_symbols_still_absent_in_gpt_surface() -> None:
    import taaqqul_slot_geometry.gpt as gpt_module

    for forbidden in (
        "ReasonablenessVerdict",
        "NeedGate",
        "OriginBindingGate",
        "Pipeline",
        "SpeechForceKind",
    ):
        assert not hasattr(gpt_module, forbidden)
