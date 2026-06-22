"""GPT-R3 — MantuqGPT explicit-claim boundary.

Binding:
- docs/54 §3.2 (MantuqGPT)
- docs/14 chain row GPT-R3 (explicit-claim extraction with trace)

This module preserves only what GPT explicitly stated. It does not derive
implications, open MafhumGPT, bind origins, run gates, or produce a final
reasonableness verdict.
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gpt.maqam_boundary import MaqamGPT


class MantuqGPTSchemaError(TypeError):
    """A GPT-R3 mantuq carrier was constructed with malformed fields."""


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise MantuqGPTSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _require_tuple_of_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise MantuqGPTSchemaError(f"{cls_name}.{field} must be a tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise MantuqGPTSchemaError(
                f"{cls_name}.{field} must contain only non-empty strings"
            )


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise MantuqGPTSchemaError(f"{cls_name}.{field} must start with 'trace://'")


@dataclass(frozen=True, slots=True)
class ExplicitClaim:
    """A single explicit GPT claim, preserving only what appears in the answer."""

    claim_id: str
    subject: str
    predicate: str
    qualifiers: tuple[str, ...]
    modality: str
    domain: str
    span_trace: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "claim_id", self.claim_id)
        _require_nonempty_str(cls, "subject", self.subject)
        _require_nonempty_str(cls, "predicate", self.predicate)
        _require_tuple_of_nonempty_str(cls, "qualifiers", self.qualifiers)
        _require_nonempty_str(cls, "modality", self.modality)
        _require_nonempty_str(cls, "domain", self.domain)
        _require_trace_ref(cls, "span_trace", self.span_trace)


@dataclass(frozen=True, slots=True)
class ClaimBoundary:
    """Trace-bound boundary around an explicit claim."""

    claim: ExplicitClaim
    source_maqam_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.claim, ExplicitClaim):
            raise MantuqGPTSchemaError(f"{cls}.claim must be an ExplicitClaim")
        _require_trace_ref(cls, "source_maqam_ref", self.source_maqam_ref)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class MantuqGPT:
    """Explicit GPT claim boundary for reasonableness processing.

    MantuqGPT is the preserved explicit surface of the GPT answer. It is not
    MafhumGPT, not origin binding, and not a reasonableness verdict.
    """

    source_maqam_ref: str
    answer_ref: str
    explicit_claims: tuple[ClaimBoundary, ...]
    domain: str
    span_traces: tuple[str, ...]
    residuals: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_trace_ref(cls, "source_maqam_ref", self.source_maqam_ref)
        _require_nonempty_str(cls, "answer_ref", self.answer_ref)
        if not isinstance(self.explicit_claims, tuple):
            raise MantuqGPTSchemaError(f"{cls}.explicit_claims must be a tuple")
        if not self.explicit_claims:
            raise MantuqGPTSchemaError(f"{cls}.explicit_claims must not be empty")
        for boundary in self.explicit_claims:
            if not isinstance(boundary, ClaimBoundary):
                raise MantuqGPTSchemaError(
                    f"{cls}.explicit_claims entries must be ClaimBoundary instances"
                )
            if boundary.source_maqam_ref != self.source_maqam_ref:
                raise MantuqGPTSchemaError(
                    f"{cls}.explicit_claims must preserve source_maqam_ref"
                )
        _require_nonempty_str(cls, "domain", self.domain)
        _require_tuple_of_nonempty_str(cls, "span_traces", self.span_traces)
        for span_trace in self.span_traces:
            _require_trace_ref(cls, "span_traces entry", span_trace)
        _require_tuple_of_nonempty_str(cls, "residuals", self.residuals)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


def build_mantuq_gpt(
    maqam: MaqamGPT,
    *,
    answer_ref: str,
    explicit_claims: tuple[ClaimBoundary, ...],
    span_traces: tuple[str, ...],
    residuals: tuple[str, ...],
    trace_ref: str,
) -> MantuqGPT:
    """Build a GPT-R3 MantuqGPT carrier from a preserved MaqamGPT boundary."""

    if not isinstance(maqam, MaqamGPT):
        raise MantuqGPTSchemaError("maqam must be a MaqamGPT")
    return MantuqGPT(
        source_maqam_ref=maqam.trace_ref,
        answer_ref=answer_ref,
        explicit_claims=explicit_claims,
        domain=maqam.domain,
        span_traces=span_traces,
        residuals=residuals,
        trace_ref=trace_ref,
    )


__all__ = [
    "ClaimBoundary",
    "ExplicitClaim",
    "MantuqGPT",
    "MantuqGPTSchemaError",
    "build_mantuq_gpt",
]
