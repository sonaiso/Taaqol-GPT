"""Gate carriers for typed GUA transitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.gua.core.delta import TransitionDelta
from taaqqul_slot_geometry.gua.core.evidence import EvidenceContract
from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError, TypedFailure
from taaqqul_slot_geometry.gua.core.residual import ResidualSet
from taaqqul_slot_geometry.gua.core.trace import Trace
from taaqqul_slot_geometry.gua.core.transition import TransitionContract


class GateDecision(StrEnum):
    """Gate-level decision vocabulary."""

    APPROVED = "APPROVED"
    REFUSED = "REFUSED"
    DEFERRED = "DEFERRED"


@dataclass(frozen=True, slots=True)
class Gate:
    """Typed gate record linking evidence, transition, delta, and trace."""

    gate_id: str
    transition: TransitionContract
    evidence: EvidenceContract
    delta: TransitionDelta
    decision: GateDecision
    residuals: ResidualSet
    trace: Trace
    failure: TypedFailure | None = None

    def __post_init__(self) -> None:
        _require_str(self.__class__.__name__, "gate_id", self.gate_id)
        if not isinstance(self.transition, TransitionContract):
            raise GuaCoreSchemaError("Gate.transition must be TransitionContract")
        if not isinstance(self.evidence, EvidenceContract):
            raise GuaCoreSchemaError("Gate.evidence must be EvidenceContract")
        if not isinstance(self.delta, TransitionDelta):
            raise GuaCoreSchemaError("Gate.delta must be TransitionDelta")
        if not isinstance(self.decision, GateDecision):
            raise GuaCoreSchemaError("Gate.decision must be GateDecision")
        if not isinstance(self.residuals, ResidualSet):
            raise GuaCoreSchemaError("Gate.residuals must be ResidualSet")
        if not isinstance(self.trace, Trace):
            raise GuaCoreSchemaError("Gate.trace must be Trace")
        if self.failure is not None and not isinstance(self.failure, TypedFailure):
            raise GuaCoreSchemaError("Gate.failure must be TypedFailure or None")

        if self.decision is GateDecision.APPROVED:
            if self.failure is not None:
                raise GuaCoreSchemaError("Gate.failure must be None when decision is APPROVED")
            if self.residuals.has_blocking:
                raise GuaCoreSchemaError(
                    "Gate.residuals must not contain visible blocking residuals for APPROVED"
                )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")
