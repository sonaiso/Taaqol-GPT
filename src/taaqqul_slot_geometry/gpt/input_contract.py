"""GPT-R1 — GPT Answer Input Contract carriers.

Binding:
- docs/54 §6 (GPT-R1 = GPT Answer Input Contract)
- docs/14 chain row GPT-R1 (input boundary before extraction)

This module ships carrier-only contract surfaces for GPT input envelopes.
No MaqamGPT verdict, no extraction, no gate, and no reasonableness verdict
lives here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class InputContractSchemaError(TypeError):
    """A GPT-R1 input carrier was constructed with malformed fields."""


class InputRiskLevel(StrEnum):
    """Risk hint attached to the input envelope (pre-Maqam boundary)."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class InputTimeSensitivity(StrEnum):
    """Time sensitivity hint attached to the input envelope."""

    STATIC = "STATIC"
    TIME_BOUND = "TIME_BOUND"
    REAL_TIME = "REAL_TIME"


class InputEvidenceNeed(StrEnum):
    """Evidence need hint attached to the input envelope."""

    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise InputContractSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _require_tuple_of_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise InputContractSchemaError(f"{cls_name}.{field} must be a tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise InputContractSchemaError(
                f"{cls_name}.{field} must contain only non-empty strings"
            )


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise InputContractSchemaError(f"{cls_name}.{field} must start with 'trace://'")


@dataclass(frozen=True, slots=True)
class GPTAnswerInput:
    """Input envelope for GPT reasonableness processing (GPT-R1).

    This is a boundary carrier, not a verdict. It preserves user question,
    model answer, and contract hints needed by the next staged boundaries.
    """

    request_id: str
    user_question: str
    gpt_answer: str
    question_type_hint: str
    domain_hint: str
    constraints: tuple[str, ...]
    evidence_need: InputEvidenceNeed
    risk_level: InputRiskLevel
    time_sensitivity: InputTimeSensitivity
    forbidden_answer_forms: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "request_id", self.request_id)
        _require_nonempty_str(cls, "user_question", self.user_question)
        _require_nonempty_str(cls, "gpt_answer", self.gpt_answer)
        _require_nonempty_str(cls, "question_type_hint", self.question_type_hint)
        _require_nonempty_str(cls, "domain_hint", self.domain_hint)
        _require_tuple_of_nonempty_str(cls, "constraints", self.constraints)
        if not isinstance(self.evidence_need, InputEvidenceNeed):
            raise InputContractSchemaError(
                f"{cls}.evidence_need must be an InputEvidenceNeed member"
            )
        if not isinstance(self.risk_level, InputRiskLevel):
            raise InputContractSchemaError(f"{cls}.risk_level must be an InputRiskLevel member")
        if not isinstance(self.time_sensitivity, InputTimeSensitivity):
            raise InputContractSchemaError(
                f"{cls}.time_sensitivity must be an InputTimeSensitivity member"
            )
        _require_tuple_of_nonempty_str(
            cls,
            "forbidden_answer_forms",
            self.forbidden_answer_forms,
        )
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


__all__ = [
    "GPTAnswerInput",
    "InputContractSchemaError",
    "InputEvidenceNeed",
    "InputRiskLevel",
    "InputTimeSensitivity",
]
