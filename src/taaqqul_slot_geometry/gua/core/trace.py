"""Trace carriers for GUA general-core operations."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class Trace:
    """Minimal trace surface that every GUA stage must expose."""

    trace_ref: str
    stage: str
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_str(cls, "stage", self.stage)
        _require_tuple_of_str(cls, "notes", self.notes, allow_empty=True)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_tuple_of_str(
    cls_name: str, field_name: str, value: object, *, allow_empty: bool = False
) -> None:
    if not isinstance(value, tuple):
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a tuple")
    if not allow_empty and not value:
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise GuaCoreSchemaError(f"{cls_name}.{field_name} entries must be non-empty strings")
