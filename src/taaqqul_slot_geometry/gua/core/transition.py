"""Transition contracts for the GUA general core."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class TransitionContract:
    """Typed transition declaration independent of realization branch names."""

    transition_id: str
    source_state: str
    target_state: str
    required_evidence: tuple[str, ...]
    rank_ceiling: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "transition_id", self.transition_id)
        _require_str(cls, "source_state", self.source_state)
        _require_str(cls, "target_state", self.target_state)
        _require_tuple_of_str(cls, "required_evidence", self.required_evidence)
        _require_str(cls, "rank_ceiling", self.rank_ceiling)
        _require_str(cls, "trace_ref", self.trace_ref)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_tuple_of_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple) or not value:
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise GuaCoreSchemaError(f"{cls_name}.{field_name} entries must be non-empty strings")
