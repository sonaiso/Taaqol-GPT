"""Identity carriers for GUA general-core entities."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class TypedEntity:
    """Typed entity with domain-local identity."""

    entity_id: str
    entity_type: str
    domain_id: str

    def __post_init__(self) -> None:
        _require_str(self.__class__.__name__, "entity_id", self.entity_id)
        _require_str(self.__class__.__name__, "entity_type", self.entity_type)
        _require_str(self.__class__.__name__, "domain_id", self.domain_id)


@dataclass(frozen=True, slots=True)
class IdentityContract:
    """Identity continuity declaration for a typed entity."""

    anchor_id: str
    entity: TypedEntity
    preserved_traits: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_str(self.__class__.__name__, "anchor_id", self.anchor_id)
        if not isinstance(self.entity, TypedEntity):
            raise GuaCoreSchemaError("IdentityContract.entity must be TypedEntity")
        _require_tuple_of_str(self.__class__.__name__, "preserved_traits", self.preserved_traits)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_tuple_of_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple) or not value:
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise GuaCoreSchemaError(f"{cls_name}.{field_name} entries must be non-empty strings")
