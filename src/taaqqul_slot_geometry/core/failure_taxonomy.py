"""Named failure codes carried by ``GammaResult``.

PR-1 emits only the codes below. Failures are *values*, never
exceptions. Every refusal verdict from ``gamma`` carries one of these.
"""

from __future__ import annotations

from enum import StrEnum


class FailureCode(StrEnum):
    """Named failure codes for PR-1 verdicts.

    String-valued so they serialise cleanly into trace entries.
    """

    REQUIRED_SLOT_EMPTY = "REQUIRED_SLOT_EMPTY"
    IDENTITY_BROKEN = "IDENTITY_BROKEN"
    HIDDEN_RESIDUAL = "HIDDEN_RESIDUAL"
    BLOCKING_RESIDUAL_PRESENT = "BLOCKING_RESIDUAL_PRESENT"
    OUTPUT_EXCEEDS_LAYER = "OUTPUT_EXCEEDS_LAYER"


__all__ = ["FailureCode"]
