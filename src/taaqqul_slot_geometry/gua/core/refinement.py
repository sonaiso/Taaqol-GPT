"""Refinement-relation carriers for typed entities."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError
from taaqqul_slot_geometry.gua.core.identity import TypedEntity


@dataclass(frozen=True, slots=True)
class RefinementRelation:
    """Directional refinement edge between two typed entities."""

    source: TypedEntity
    target: TypedEntity
    relation_kind: str
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.source, TypedEntity):
            raise GuaCoreSchemaError("RefinementRelation.source must be TypedEntity")
        if not isinstance(self.target, TypedEntity):
            raise GuaCoreSchemaError("RefinementRelation.target must be TypedEntity")
        _require_str(self.__class__.__name__, "relation_kind", self.relation_kind)
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")
