"""Shared schema-validation helpers for ``weight/`` carrier surfaces.

This module is an internal convenience layer that deduplicates the
truly-identical schema-validation primitives previously copy-pasted across
``wadi_madlul.py``, ``wadi_c8_integration.py``, and ``coupled_dalalah.py``.

Constitutional scope (corrective; no new layer):

* This module introduces **no new constitutional surface**: no carrier,
  no verdict, no gate, no closure, no `FailureCode`, no `ResidualKind`.
* It only re-exposes the existing per-file primitives behind a single
  authoritative definition so that future tightening (error wording,
  ceiling enforcement, residual-kind checks) happens in one place
  instead of being silently divergent across modules.
* Class-specific variants that are not byte-for-byte identical (e.g.
  ``_validate_forbidden_outputs`` with an `expected` equality check in
  ``coupled_dalalah.py``, ``_append_residual_once`` over different
  residual record shapes, ``_validate_coupled_residuals`` with
  visibility enforcement) are intentionally **not** unified here.
"""

from __future__ import annotations

from typing import TypeVar

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError

ResidualT = TypeVar("ResidualT")


def require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    """Raise ``WeightCarrierSchemaError`` when ``value`` is not a non-empty string."""

    if not isinstance(value, str) or not value.strip():
        raise WeightCarrierSchemaError(
            f"{field_name} must be a non-empty string ({failure_code.value})"
        )


def validate_rank(rank: Rank, owner: str, *, ceiling: Rank) -> None:
    """Validate ``rank`` is a ``Rank`` member and does not exceed ``ceiling``.

    The ceiling label is fixed as ``CANDIDATE`` because every callsite that
    used the duplicate helpers carried that ceiling. New layers that need a
    different ceiling label should not reuse this helper.
    """

    if not isinstance(rank, Rank):
        raise WeightCarrierSchemaError(
            f"{owner}.rank must be a Rank member "
            f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
        )
    if rank > ceiling:
        raise WeightCarrierSchemaError(
            f"{owner}.rank must not exceed CANDIDATE ({FailureCode.RANK_EXCEEDS_CEILING.value})"
        )


def validate_residual_tuple(
    residuals: tuple[ResidualT, ...],
    owner: str,
    *,
    expected_type: type,
) -> None:
    """Validate ``residuals`` is a tuple of ``expected_type`` entries.

    Mirrors the simple ``_validate_residuals(self.residuals, "Owner")``
    convention (helper appends ``.residuals`` to ``owner`` in messages).
    Variants that pre-format the owner (e.g. ``coupled_dalalah``'s
    ``_validate_wadi_residuals`` called as ``_validate_wadi_residuals(
    self.wadi_residuals, "Owner.wadi_residuals")``) are intentionally
    not routed here.
    """

    if not isinstance(residuals, tuple):
        raise WeightCarrierSchemaError(
            f"{owner}.residuals must be a tuple ({FailureCode.HIDDEN_RESIDUAL.value})"
        )
    for residual in residuals:
        if not isinstance(residual, expected_type):
            raise WeightCarrierSchemaError(
                f"{owner}.residuals entries must be {expected_type.__name__} "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


def validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    """Validate ``forbidden_outputs`` is a tuple of non-empty strings.

    This is the *simple* form used in ``wadi_madlul.py`` and
    ``wadi_c8_integration.py``. The ``coupled_dalalah.py`` variant adds an
    exact-equality check against a declared forbidden surface and stays
    local to that module.
    """

    if not isinstance(forbidden_outputs, tuple):
        raise WeightCarrierSchemaError(
            f"{owner}.forbidden_outputs must be a tuple "
            f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
        )
    for output in forbidden_outputs:
        require_non_empty(
            output,
            f"{owner}.forbidden_outputs entry",
            FailureCode.OUTPUT_EXCEEDS_LAYER,
        )


def merge_residuals(
    *residual_groups: tuple[ResidualT, ...],
) -> tuple[ResidualT, ...]:
    """Concatenate residual groups, preserving order and dropping duplicates."""

    merged: list[ResidualT] = []
    seen: set[ResidualT] = set()
    for residual_group in residual_groups:
        for residual in residual_group:
            if residual not in seen:
                seen.add(residual)
                merged.append(residual)
    return tuple(merged)


__all__ = [
    "merge_residuals",
    "require_non_empty",
    "validate_forbidden_outputs",
    "validate_rank",
    "validate_residual_tuple",
]
