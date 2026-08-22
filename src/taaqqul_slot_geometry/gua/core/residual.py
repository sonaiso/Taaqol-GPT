"""Residual carriers for GUA gate visibility discipline."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


class ResidualKind(StrEnum):
    """Local residual categories for GUA core gating."""

    BLOCKING = "BLOCKING"
    DEFERRED = "DEFERRED"
    INFORMATIONAL = "INFORMATIONAL"


@dataclass(frozen=True, slots=True)
class Residual:
    """Single residual item with visibility guarantee."""

    kind: ResidualKind
    detail: str
    visible: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.kind, ResidualKind):
            raise GuaCoreSchemaError("Residual.kind must be ResidualKind")
        _require_str(self.__class__.__name__, "detail", self.detail)
        if not isinstance(self.visible, bool):
            raise GuaCoreSchemaError("Residual.visible must be bool")


@dataclass(frozen=True, slots=True)
class ResidualSet:
    """Immutable residual set used by gate and suite outputs."""

    items: tuple[Residual, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.items, tuple):
            raise GuaCoreSchemaError("ResidualSet.items must be tuple")
        for item in self.items:
            if not isinstance(item, Residual):
                raise GuaCoreSchemaError("ResidualSet.items entries must be Residual")

    @property
    def has_blocking(self) -> bool:
        """Return True if at least one blocking residual is visible."""

        return any(item.kind is ResidualKind.BLOCKING and item.visible for item in self.items)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")
