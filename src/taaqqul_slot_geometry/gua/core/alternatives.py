"""Alternative-set carriers for branching possibilities."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class AlternativeSet:
    """Bounded alternatives surface used by refinement operations."""

    alternatives: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        _require_tuple_of_str(self.__class__.__name__, "alternatives", self.alternatives)
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_tuple_of_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple) or not value:
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise GuaCoreSchemaError(f"{cls_name}.{field_name} entries must be non-empty strings")
