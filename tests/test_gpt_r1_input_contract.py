"""Acceptance tests for GPT-R1 input contract surface.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law)
Branch         : GPT-R1 (GPT Answer Input Contract)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses

import pytest

from taaqqul_slot_geometry.gpt import (
    GPTAnswerInput,
    InputContractSchemaError,
    InputEvidenceNeed,
    InputRiskLevel,
    InputTimeSensitivity,
)


def _make_input() -> GPTAnswerInput:
    return GPTAnswerInput(
        request_id="req-001",
        user_question="هل هذه الدعوى مدعومة بدليل؟",
        gpt_answer="الدعوى تحتاج إلى توثيق إضافي.",
        question_type_hint="factual",
        domain_hint="reasonableness-audit",
        constraints=("no-overclaim", "show-residuals"),
        evidence_need=InputEvidenceNeed.HIGH,
        risk_level=InputRiskLevel.HIGH,
        time_sensitivity=InputTimeSensitivity.TIME_BOUND,
        forbidden_answer_forms=("truth-declaration", "certificate-language"),
        trace_ref="trace://gpt-r1/input/001",
    )


def test_input_contract_constructs() -> None:
    carrier = _make_input()
    assert carrier.request_id == "req-001"
    assert carrier.evidence_need is InputEvidenceNeed.HIGH


def test_input_contract_is_frozen() -> None:
    carrier = _make_input()
    with pytest.raises(dataclasses.FrozenInstanceError):
        carrier.user_question = "modified"  # type: ignore[misc]


def test_trace_ref_must_use_trace_scheme() -> None:
    with pytest.raises(InputContractSchemaError):
        GPTAnswerInput(
            request_id="req-002",
            user_question="q",
            gpt_answer="a",
            question_type_hint="factual",
            domain_hint="general",
            constraints=(),
            evidence_need=InputEvidenceNeed.LOW,
            risk_level=InputRiskLevel.LOW,
            time_sensitivity=InputTimeSensitivity.STATIC,
            forbidden_answer_forms=(),
            trace_ref="bad://trace",
        )


def test_constraints_must_be_tuple_of_nonempty_strings() -> None:
    with pytest.raises(InputContractSchemaError):
        GPTAnswerInput(
            request_id="req-003",
            user_question="q",
            gpt_answer="a",
            question_type_hint="factual",
            domain_hint="general",
            constraints=("ok", ""),
            evidence_need=InputEvidenceNeed.LOW,
            risk_level=InputRiskLevel.LOW,
            time_sensitivity=InputTimeSensitivity.STATIC,
            forbidden_answer_forms=(),
            trace_ref="trace://gpt-r1/input/003",
        )


def test_forbidden_symbols_still_absent_in_gpt_surface() -> None:
    import taaqqul_slot_geometry.gpt as gpt_module

    for forbidden in (
        "GPTAnswerReasonablenessVerdict",
        "NeedGate",
        "Pipeline",
    ):
        assert not hasattr(gpt_module, forbidden)
