"""Transition state — the five gate verdicts of docs/08.

Relocated from :mod:`taaqqul_slot_geometry.core.transition_gate` in
PR-6 so that the trace split (docs/07 — *PR-6 binding*) can type the
``gate_transition_state`` field of ``TraceEntryCandidate`` without a
circular import: this module is a *leaf* — it imports nothing from
the rest of the kernel, so both ``trace_ledger`` and
``transition_gate`` may depend on it.
"""

from __future__ import annotations

from enum import StrEnum


class TransitionState(StrEnum):
    """The five gate verdicts of docs/08.

    ``TransitionState`` is deliberately distinct from
    ``ClosureState``: a gate verdict speaks about a *move*, a
    closure verdict speaks about a *graph*. The two never coerce
    into each other silently — ``TransitionVerdict`` carries the
    consulted ``gamma_state`` alongside the gate ``state`` so both
    judgements stay visible, and since PR-6 the trace candidate
    records them in two distinct fields (``consulted_gamma_state``
    / ``gate_transition_state``).
    """

    APPROVED = "APPROVED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"
    FORBIDDEN_LEAP = "FORBIDDEN_LEAP"


__all__ = ["TransitionState"]
