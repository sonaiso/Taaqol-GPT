"""Closure state — carrier enum (PR-1A).

Names the six verdicts that ``Γ`` (gamma) returns. PR-1A shipped the
*enum* so that the constitutional documents and tests can reference
the verdict names exactly; the verdict *function* shipped in PR-2 as
``core.gamma`` alongside the executable ``SlotGraph``.

See ``docs/03_GAMMA_CLOSURE_CONTRACT.md`` and
``docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md``.
"""

from __future__ import annotations

from enum import StrEnum


class ClosureState(StrEnum):
    """The six constitutional closure verdicts.

    Do **not** add helper logic here. This module ships names only;
    the decision law lives in the documents and is bound by the
    ``core.gamma`` implementation (PR-2).
    """

    OPEN = "OPEN"
    MINIMALLY_CLOSED = "MINIMALLY_CLOSED"
    PERFORATED_CLOSED = "PERFORATED_CLOSED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"
    FORBIDDEN_LEAP = "FORBIDDEN_LEAP"


__all__ = ["ClosureState"]
