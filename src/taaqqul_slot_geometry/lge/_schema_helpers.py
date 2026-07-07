"""Shared schema helpers for LGE runtime surfaces."""

from __future__ import annotations

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank


class LGESchemaError(TypeError):
    """Raised when an LGE runtime schema contract is malformed."""


def require_non_empty(value: object, owner: str, field_name: str, failure_code: FailureCode) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LGESchemaError(
            f"{owner}.{field_name} must be non-empty ({failure_code.value})"
        )
    if value != value.strip():
        raise LGESchemaError(
            f"{owner}.{field_name} must not have leading/trailing whitespace "
            f"({failure_code.value})"
        )
    return value


def require_trace_ref(value: object, owner: str, field_name: str) -> str:
    text = require_non_empty(value, owner, field_name, FailureCode.TRACE_MISSING)
    if not text.startswith("trace://"):
        raise LGESchemaError(
            f"{owner}.{field_name} must start with 'trace://' ({FailureCode.TRACE_MISSING.value})"
        )
    return text


def validate_residuals(value: object, owner: str, field_name: str = "residuals") -> tuple[str, ...]:
    if not isinstance(value, tuple):
        raise LGESchemaError(
            f"{owner}.{field_name} must be tuple ({FailureCode.HIDDEN_RESIDUAL.value})"
        )
    cleaned: list[str] = []
    for item in value:
        cleaned.append(require_non_empty(item, owner, field_name, FailureCode.HIDDEN_RESIDUAL))
    return tuple(cleaned)


def validate_forbidden_outputs(value: object, owner: str) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        raise LGESchemaError(
            f"{owner}.forbidden_outputs must be tuple ({FailureCode.BOUNDARY_MISSING.value})"
        )
    forbidden: list[str] = []
    for item in value:
        forbidden.append(
            require_non_empty(item, owner, "forbidden_outputs", FailureCode.BOUNDARY_MISSING)
        )
    return tuple(forbidden)


def validate_rank(value: object, owner: str, *, ceiling: Rank) -> Rank:
    if not isinstance(value, Rank):
        raise LGESchemaError(
            f"{owner}.rank must be Rank ({FailureCode.RANK_EXCEEDS_CEILING.value})"
        )
    if value > ceiling:
        raise LGESchemaError(
            f"{owner}.rank must not exceed {ceiling.value} ({FailureCode.RANK_EXCEEDS_CEILING.value})"
        )
    return value
