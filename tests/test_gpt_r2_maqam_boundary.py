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
    MaqamGPT,
    MaqamGPTSchemaError,
    build_maqam_gpt,
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
            domain="general",
            constraints=("ok", ""),
            evidence_need=InputEvidenceNeed.LOW,
            risk_level=InputRiskLevel.LOW,
            time_sensitivity=InputTimeSensitivity.STATIC,
            forbidden_answer_forms=(),
            source_trace_ref="trace://gpt-r1/input/r2-005",
            trace_ref="trace://gpt-r2/maqam/005",
        )


def test_forbidden_future_symbols_still_absent_in_gpt_surface() -> None:
    import taaqqul_slot_geometry.gpt as gpt_module

    for forbidden in (
        "MantuqGPT",
        "MafhumGPT",
        "GPTAnswerReasonablenessVerdict",
        "ReasonablenessVerdict",
        "NeedGate",
        "OriginBindingGate",
        "Pipeline",
    ):
        assert not hasattr(gpt_module, forbidden)
