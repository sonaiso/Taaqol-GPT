"""Domain specification carriers for the GUA general core."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class DomainSpec:
    """Bounded domain identity used by typed slots and transitions."""

    domain_id: str
    scope: str
    boundaries: tuple[str, ...]
    invariants: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "domain_id", self.domain_id)
        _require_str(cls, "scope", self.scope)
        _require_tuple_of_str(cls, "boundaries", self.boundaries)
        _require_tuple_of_str(cls, "invariants", self.invariants)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_tuple_of_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple) or not value:
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise GuaCoreSchemaError(f"{cls_name}.{field_name} entries must be non-empty strings")
