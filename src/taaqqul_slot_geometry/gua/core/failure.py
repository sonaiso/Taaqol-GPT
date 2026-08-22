"""General-core failure carriers for GUA refoundation."""

from __future__ import annotations

from dataclasses import dataclass


class GuaCoreSchemaError(TypeError):
    """Raised when GUA core carriers are malformed."""


@dataclass(frozen=True, slots=True)
class TypedFailure:
    """Typed failure carrier with explicit trace surface."""

    code: str
    message: str
    trace_ref: str
    blocking: bool = True

    def __post_init__(self) -> None:
        _require_str(self.__class__.__name__, "code", self.code)
        _require_str(self.__class__.__name__, "message", self.message)
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)
        _require_bool(self.__class__.__name__, "blocking", self.blocking)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_bool(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, bool):
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be bool")
