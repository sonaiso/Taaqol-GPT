from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class SlotState(str, Enum):
    OPEN = "OPEN"
    FILLED = "FILLED"


class Rank(str, Enum):
    ZERO = "ZERO"
    TRACE = "TRACE"
    CANDIDATE = "CANDIDATE"
    HYPOTHESIS = "HYPOTHESIS"
    LICENSED = "LICENSED"
    STRONG = "STRONG"
    CERTIFICATE = "CERTIFICATE"


class ResidualKind(str, Enum):
    BLOCKING = "BLOCKING"
    DEFERRABLE = "DEFERRABLE"
    NON_BLOCKING = "NON_BLOCKING"
    EXPLANATORY = "EXPLANATORY"
    HIDDEN_FORBIDDEN = "HIDDEN_FORBIDDEN"


@dataclass(frozen=True)
class TraceRef:
    trace_id: str
    input_ref: str | None = None


@dataclass(frozen=True)
class SlotBoundary:
    layer: int
    max_output_layer: int | None = None

    def allows(self, requested_output_layer: int) -> bool:
        ceiling = self.layer if self.max_output_layer is None else self.max_output_layer
        return requested_output_layer <= ceiling


@dataclass(frozen=True)
class Residual:
    code: str
    kind: ResidualKind
    message: str
    visible: bool = True


@dataclass(frozen=True)
class Slot:
    name: str
    state: SlotState = SlotState.OPEN
    required: bool = False
    value: Any = None
    boundary: SlotBoundary | None = None

    def is_filled(self) -> bool:
        return self.state == SlotState.FILLED


@dataclass(frozen=True)
class SlotGraph:
    center: str
    layer: int
    trace: TraceRef
    slots: tuple[Slot, ...]
    residuals: tuple[Residual, ...] = ()
    identity_ok: bool = True

    def missing_required_slots(self) -> tuple[str, ...]:
        return tuple(slot.name for slot in self.slots if slot.required and not slot.is_filled())

    def allows_output_layer(self, requested_output_layer: int) -> bool:
        if requested_output_layer > self.layer:
            return False

        for slot in self.slots:
            boundary = slot.boundary or SlotBoundary(layer=self.layer)
            if slot.is_filled() and not boundary.allows(requested_output_layer):
                return False

        return True
