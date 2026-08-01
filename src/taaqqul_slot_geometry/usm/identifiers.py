"""USM identifier carriers (USM-C1: schema/carrier-only)."""

from __future__ import annotations

from dataclasses import dataclass


class USMSchemaError(TypeError):
    """Raised when a USM carrier violates schema constraints."""


def _require_id_string(owner: str, value: object) -> str:
    if not isinstance(value, str):
        raise USMSchemaError(f"{owner}.value must be a string")
    if not value:
        raise USMSchemaError(f"{owner}.value must be non-empty")
    if value != value.strip():
        raise USMSchemaError(f"{owner}.value must not contain surrounding whitespace")
    return value


@dataclass(frozen=True, slots=True)
class _BaseId:
    value: str

    def __post_init__(self) -> None:
        _require_id_string(self.__class__.__name__, self.value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ScienceId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class MatrixId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class DomainId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class EntityTypeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class CapabilityId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class RelationTypeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class TransformationTypeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class EvidenceTypeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class ClaimTypeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class JudgmentTypeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class KnowledgeObjectTypeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class ApplicationTypeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class CriterionId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class BridgeId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class RuleId(_BaseId):
    pass


@dataclass(frozen=True, slots=True)
class TraceRef(_BaseId):
    def __post_init__(self) -> None:
        _BaseId.__post_init__(self)
        if not self.value.startswith("trace://"):
            raise USMSchemaError("TraceRef.value must start with 'trace://'")


def require_tuple(owner: str, field_name: str, value: object) -> tuple[object, ...]:
    if not isinstance(value, tuple):
        raise USMSchemaError(f"{owner}.{field_name} must be tuple")
    return value


def require_non_empty_text(owner: str, field_name: str, value: object) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise USMSchemaError(
            f"{owner}.{field_name} must be a non-empty string without surrounding whitespace"
        )
    return value


def require_tuple_of_type(
    owner: str, field_name: str, value: object, expected_type: type
) -> tuple[object, ...]:
    entries = require_tuple(owner, field_name, value)
    for entry in entries:
        if not isinstance(entry, expected_type):
            raise USMSchemaError(
                f"{owner}.{field_name} entries must be {expected_type.__name__}"
            )
    return entries


__all__ = [
    "ApplicationTypeId",
    "BridgeId",
    "CapabilityId",
    "ClaimTypeId",
    "CriterionId",
    "DomainId",
    "EntityTypeId",
    "EvidenceTypeId",
    "JudgmentTypeId",
    "KnowledgeObjectTypeId",
    "MatrixId",
    "RelationTypeId",
    "RuleId",
    "ScienceId",
    "TraceRef",
    "TransformationTypeId",
    "USMSchemaError",
    "require_non_empty_text",
    "require_tuple",
    "require_tuple_of_type",
]
