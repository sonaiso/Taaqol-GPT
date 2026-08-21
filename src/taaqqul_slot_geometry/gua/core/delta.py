"""Transition-delta carriers for general-core transitions."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class TransitionDelta:
    """Mandatory transition delta surface for every stage move."""

    preserved: tuple[str, ...]
    changed: tuple[str, ...]
    added: tuple[str, ...]
    lost: tuple[str, ...]
    unresolved: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_tuple(cls, "preserved", self.preserved)
        _require_tuple(cls, "changed", self.changed)
        _require_tuple(cls, "added", self.added)
        _require_tuple(cls, "lost", self.lost)
        _require_tuple(cls, "unresolved", self.unresolved)


def _require_tuple(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise GuaCoreSchemaError(f"{cls_name}.{field_name} entries must be non-empty strings")
