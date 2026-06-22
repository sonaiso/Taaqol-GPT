"""GPT-R2 — MaqamGPT Boundary.

Binding:
- docs/54 §3.1 (MaqamGPT)
- docs/14 chain row GPT-R2 (context-preservation boundary)

This module preserves the user's question context and the input-envelope
constraints from GPT-R1. It does not extract claims, infer implications,
consult origins, run gates, or produce a reasonableness verdict.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.gpt.input_contract import (
    GPTAnswerInput,
    InputEvidenceNeed,
    InputRiskLevel,
    InputTimeSensitivity,
)


class MaqamGPTSchemaError(TypeError):
    """A GPT-R2 maqam carrier was constructed with malformed fields."""


class MaqamCommunicationMode(StrEnum):
    """Question-context mode at the GPT-R2 maqām boundary.

    This is a structural question-context label only. It is not
    ``SpeechForceKind``, not Ifādah, not a claim verdict, and not a truth
    judgment.
    """

    IKHBAR = "IKHBAR"
    INSHA = "INSHA"


_IKHBAR_QUESTION_TYPE_HINTS: frozenset[str] = frozenset({
    "audit",
    "evaluative",
    "explanation",
    "explanatory",
    "fact",
    "factual",
    "ikhbar",
    "informational",
    "khabar",
    "procedural",
    "qa",
    "question",
    "verification",
    "إخبار",
    "اخبار",
    "خبر",
})

_INSHA_QUESTION_TYPE_HINTS: frozenset[str] = frozenset({
    "compose",
    "composition",
    "creative",
    "draft",
    "generation",
    "generative",
    "insha",
    "rewrite",
    "إنشاء",
    "انشاء",
})


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise MaqamGPTSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _require_tuple_of_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise MaqamGPTSchemaError(f"{cls_name}.{field} must be a tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise MaqamGPTSchemaError(
                f"{cls_name}.{field} must contain only non-empty strings"
            )


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise MaqamGPTSchemaError(f"{cls_name}.{field} must start with 'trace://'")


def _canonical_question_type(question_type: str) -> str:
    return " ".join(question_type.strip().casefold().replace("_", " ").split())


def classify_maqam_communication_mode(question_type: str) -> MaqamCommunicationMode:
    """Classify the GPT-R2 maqām as ikhbar or insha from the declared hint."""

    _require_nonempty_str("MaqamGPT", "question_type", question_type)
    canonical = _canonical_question_type(question_type)
    if canonical in _IKHBAR_QUESTION_TYPE_HINTS:
        return MaqamCommunicationMode.IKHBAR
    if canonical in _INSHA_QUESTION_TYPE_HINTS:
        return MaqamCommunicationMode.INSHA
    raise MaqamGPTSchemaError(
        "MaqamGPT.question_type must classify as IKHBAR or INSHA at GPT-R2"
    )


@dataclass(frozen=True, slots=True)
class MaqamGPT:
    """Preserved context of the user's question for GPT reasonableness.

    MaqamGPT is a boundary carrier for what was asked, in which domain, with
    which constraints and risk/evidence hints. It is not MantuqGPT, MafhumGPT,
    NeedGate, an origin-binding gate, or a final verdict.
    """

    request_id: str
    user_question: str
    question_type: str
    communication_mode: MaqamCommunicationMode
    domain: str
    constraints: tuple[str, ...]
    evidence_need: InputEvidenceNeed
    risk_level: InputRiskLevel
    time_sensitivity: InputTimeSensitivity
    forbidden_answer_forms: tuple[str, ...]
    source_trace_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "request_id", self.request_id)
        _require_nonempty_str(cls, "user_question", self.user_question)
        _require_nonempty_str(cls, "question_type", self.question_type)
        if not isinstance(self.communication_mode, MaqamCommunicationMode):
            raise MaqamGPTSchemaError(
                f"{cls}.communication_mode must be a MaqamCommunicationMode member"
            )
        expected_mode = classify_maqam_communication_mode(self.question_type)
        if self.communication_mode is not expected_mode:
            raise MaqamGPTSchemaError(
                f"{cls}.communication_mode must match question_type classification"
            )
        _require_nonempty_str(cls, "domain", self.domain)
        _require_tuple_of_nonempty_str(cls, "constraints", self.constraints)
        if not isinstance(self.evidence_need, InputEvidenceNeed):
            raise MaqamGPTSchemaError(
                f"{cls}.evidence_need must be an InputEvidenceNeed member"
            )
        if not isinstance(self.risk_level, InputRiskLevel):
            raise MaqamGPTSchemaError(f"{cls}.risk_level must be an InputRiskLevel member")
        if not isinstance(self.time_sensitivity, InputTimeSensitivity):
            raise MaqamGPTSchemaError(
                f"{cls}.time_sensitivity must be an InputTimeSensitivity member"
            )
        _require_tuple_of_nonempty_str(
            cls,
            "forbidden_answer_forms",
            self.forbidden_answer_forms,
        )
        _require_trace_ref(cls, "source_trace_ref", self.source_trace_ref)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


def build_maqam_gpt(answer_input: GPTAnswerInput, *, trace_ref: str) -> MaqamGPT:
    """Preserve GPT-R1 input context as a GPT-R2 MaqamGPT boundary carrier."""

    if not isinstance(answer_input, GPTAnswerInput):
        raise MaqamGPTSchemaError("answer_input must be a GPTAnswerInput")
    return MaqamGPT(
        request_id=answer_input.request_id,
        user_question=answer_input.user_question,
        question_type=answer_input.question_type_hint,
        communication_mode=classify_maqam_communication_mode(
            answer_input.question_type_hint
        ),
        domain=answer_input.domain_hint,
        constraints=answer_input.constraints,
        evidence_need=answer_input.evidence_need,
        risk_level=answer_input.risk_level,
        time_sensitivity=answer_input.time_sensitivity,
        forbidden_answer_forms=answer_input.forbidden_answer_forms,
        source_trace_ref=answer_input.trace_ref,
        trace_ref=trace_ref,
    )


__all__ = [
    "MaqamCommunicationMode",
    "MaqamGPT",
    "MaqamGPTSchemaError",
    "build_maqam_gpt",
    "classify_maqam_communication_mode",
]
