"""Residual policy — *carrier only* in PR-1.

This module ships the ``ResidualKind`` enum and the immutable
``Residual`` dataclass. The classification engine and the rank-ceiling
computation land in PR-2. Do not add policy here.

See ``docs/06_RESIDUAL_POLICY.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ResidualKind(StrEnum):
    """Residual kinds as declared in the constitution."""

    BLOCKING = "BLOCKING"
    DEFERRABLE = "DEFERRABLE"
    NON_BLOCKING = "NON_BLOCKING"
    EXPLANATORY = "EXPLANATORY"
    HIDDEN_FORBIDDEN = "HIDDEN_FORBIDDEN"


@dataclass(frozen=True, slots=True)
class Residual:
    """A declared residual attached to a ``SlotGraph``.

    PR-1 only carries this value through to ``gamma``. The full residual
    engine (rank-ceiling, suppression rules) lands in PR-2.
    """

    name: str
    kind: ResidualKind
    visible: bool
    note: str = ""


__all__ = ["Residual", "ResidualKind"]
