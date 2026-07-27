"""Matrix-to-weight wiring bridge for constitutional operations.

This module binds selected matrix operation IDs to the expected runtime
carrier types in ``taaqqul_slot_geometry.weight``.
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.weight import (
    HukmCandidate,
    IfadahCandidate,
    ManatCandidate,
    RelationCandidate,
    TanzilCandidate,
)


@dataclass(frozen=True, slots=True)
class MatrixWiringError(Exception):
    """Raised when matrix->weight carrier wiring cannot be resolved."""

    residuals: tuple[str, ...]
    failure_code: FailureCode


class MatrixWeightBridge:
    """Resolve matrix operation carriers from runtime transition inputs."""

    _OP_TO_CARRIERS: dict[str, tuple[type[object], ...]] = {
        "OP-35": (RelationCandidate,),
        "OP-36": (IfadahCandidate,),
        "OP-37": (HukmCandidate,),
        "OP-38": (HukmCandidate, ManatCandidate, TanzilCandidate),
    }

    def resolve_wired_carrier(
        self,
        operation_id: str,
        inputs: dict[str, object],
    ) -> object | tuple[object, ...] | None:
        expected = self._OP_TO_CARRIERS.get(operation_id)
        if expected is None:
            return None

        resolved: list[object] = []
        for carrier_type in expected:
            carrier = self._resolve_one(carrier_type, inputs)
            resolved.append(carrier)

        if len(resolved) == 1:
            return resolved[0]
        return tuple(resolved)

    def _resolve_one(self, carrier_type: type[object], inputs: dict[str, object]) -> object:
        key = carrier_type.__name__
        keyed_value = inputs.get(key)
        if keyed_value is not None:
            if isinstance(keyed_value, carrier_type):
                return keyed_value
            raise MatrixWiringError(
                residuals=(f"INVALID_WIRED_CARRIER_TYPE:{key}",),
                failure_code=FailureCode.GATE_REQUIRED,
            )

        for value in inputs.values():
            if isinstance(value, carrier_type):
                return value

        raise MatrixWiringError(
            residuals=(f"MISSING_WIRED_CARRIER:{key}",),
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        )


__all__ = ["MatrixWeightBridge", "MatrixWiringError"]
