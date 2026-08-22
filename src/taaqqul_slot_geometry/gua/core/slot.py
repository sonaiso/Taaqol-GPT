"""Typed-slot carriers for the GUA general core."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class TypedSlot:
    """General slot geometry carrier without branch-specific semantics."""

    slot_type: str
    domain_id: str
    coordinates: tuple[str, ...]
    boundary: tuple[str, ...]
    invariants: tuple[str, ...]
    prior_requirements: tuple[str, ...]
    admissible_states: tuple[str, ...]
    residual_region: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "slot_type", self.slot_type)
        _require_str(cls, "domain_id", self.domain_id)
        _require_tuple_of_str(cls, "coordinates", self.coordinates)
        _require_tuple_of_str(cls, "boundary", self.boundary)
        _require_tuple_of_str(cls, "invariants", self.invariants)
        _require_tuple_of_str(cls, "prior_requirements", self.prior_requirements)
        _require_tuple_of_str(cls, "admissible_states", self.admissible_states)
        _require_tuple_of_str(cls, "residual_region", self.residual_region)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_tuple_of_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple) or not value:
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise GuaCoreSchemaError(f"{cls_name}.{field_name} entries must be non-empty strings")
