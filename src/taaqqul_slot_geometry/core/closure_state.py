"""Closure state — carrier enum only (PR-1).

Names the six verdicts that ``Γ`` (gamma) will eventually return. PR-1
ships the *enum* so that the constitutional documents and tests can
reference the verdict names exactly; the verdict *function* lands in
PR-2 alongside the executable ``SlotGraph``.

See ``docs/03_GAMMA_CLOSURE_CONTRACT.md`` and
``docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md``.
"""

from __future__ import annotations

from enum import StrEnum


class ClosureState(StrEnum):
    """The six constitutional closure verdicts.

    Do **not** add helper logic here. PR-1 ships names only; the
    decision law lives in the documents and is bound by the PR-2
    ``gamma`` implementation.
    """

    OPEN = "OPEN"
    MINIMALLY_CLOSED = "MINIMALLY_CLOSED"
    PERFORATED_CLOSED = "PERFORATED_CLOSED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"
    FORBIDDEN_LEAP = "FORBIDDEN_LEAP"


__all__ = ["ClosureState"]
