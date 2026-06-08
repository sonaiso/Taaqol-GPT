"""Rank lattice — *carrier only* in PR-1.

This module ships the ``Rank`` enum so that ``SlotGraph`` and downstream
callers can declare a rank field. The lattice's ``meet`` operation, the
non-promotion law, and the evidence-driven ceiling computation all land
in PR-2. Do not add policy here.

See ``docs/05_RANK_LATTICE.md``.
"""

from __future__ import annotations

from enum import IntEnum


class Rank(IntEnum):
    """Bounded ordered carrier for evidential strength.

    ``IntEnum`` gives total ordering for free; PR-1 uses only the
    ordering. No ``meet``, no promotion logic, no policy.
    """

    ZERO = 0
    TRACE = 1
    CANDIDATE = 2
    HYPOTHESIS = 3
    LICENSED = 4
    STRONG = 5
    CERTIFICATE = 6


__all__ = ["Rank"]
