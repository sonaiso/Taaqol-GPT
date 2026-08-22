"""Realization contracts layered above the frozen general core."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError
from taaqqul_slot_geometry.gua.core.slot import TypedSlot
from taaqqul_slot_geometry.gua.core.transition import TransitionContract


@dataclass(frozen=True, slots=True)
class RealizationContract:
    """Bounded realization contract consuming a frozen general core."""

    domain: str
    frozen_core_hash: str
    slots: tuple[TypedSlot, ...]
    transitions: tuple[TransitionContract, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        _require_str(self.__class__.__name__, "domain", self.domain)
        _require_str(self.__class__.__name__, "frozen_core_hash", self.frozen_core_hash)
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)
        if not isinstance(self.slots, tuple) or not self.slots:
            raise GuaCoreSchemaError("RealizationContract.slots must be a non-empty tuple")
        for slot in self.slots:
            if not isinstance(slot, TypedSlot):
                raise GuaCoreSchemaError("RealizationContract.slots entries must be TypedSlot")
        if not isinstance(self.transitions, tuple) or not self.transitions:
            raise GuaCoreSchemaError("RealizationContract.transitions must be a non-empty tuple")
        for transition in self.transitions:
            if not isinstance(transition, TransitionContract):
                raise GuaCoreSchemaError(
                    "RealizationContract.transitions entries must be TransitionContract"
                )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")
