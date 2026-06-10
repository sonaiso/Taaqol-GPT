"""Trace ledger carriers — PR-2 minimal binding.

This module ships:

* :class:`TraceEntryCandidate` — the immutable value that ``Γ``
  packages inside its :class:`GammaResult`. The candidate is a *pure
  value*; appending it to the ledger is the caller's responsibility
  (docs/07 — *the purity rule*).

* :class:`TraceLedger` — a minimal in-memory append-only container.
  PR-2 stays in-memory; persistence is out of scope through PR-6
  (docs/07 — *The ledger itself is in-memory in PR-2 and stays
  in-memory through PR-6*).

The module deliberately does **not** import
:mod:`taaqqul_slot_geometry.core.gamma`. ``gamma.py``, in turn, must
not import :class:`TraceLedger` from this module — only
:class:`TraceEntryCandidate`. The static guard for this rule lives
in the PR-2 test suite (docs/07 — *PR-2 binding*).
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core.closure_state import ClosureState
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank


@dataclass(frozen=True, slots=True)
class TraceEntryCandidate:
    """An opaque, immutable trace event proposed by ``Γ``.

    Fields mirror the :class:`~docs/07_TRACE_LEDGER` ``TraceEntry``
    schema with the minimum needed for PR-2:

    * ``parent_anchor`` — the opaque trace anchor copied from the
      graph's :class:`~taaqqul_slot_geometry.core.slot_graph.Center`.
      Core never inspects its contents.
    * ``stage`` — the named verdict stage (``"gamma"`` since PR-2,
      ``"gate"`` since PR-4; ``"audit"`` lands in PR-6).
    * ``snapshot_state`` / ``snapshot_failure`` / ``snapshot_rank`` —
      a minimum snapshot of the verdict for the ledger to record.

    The candidate is a *value*. It does not write itself anywhere.
    """

    parent_anchor: str
    stage: str
    snapshot_state: ClosureState
    snapshot_failure: FailureCode | None
    snapshot_rank: Rank


class TraceLedger:
    """Minimal append-only in-memory ledger.

    The ledger lives **outside** the pure core verdict functions.
    ``gamma(graph)`` never touches it: a caller (test harness, future
    audit wrapper, future gate runner) decides when to call
    :meth:`append`.
    """

    __slots__ = ("_entries",)

    def __init__(self) -> None:
        self._entries: list[TraceEntryCandidate] = []

    def append(self, entry: TraceEntryCandidate) -> None:
        if not isinstance(entry, TraceEntryCandidate):
            raise TypeError(
                "TraceLedger.append requires a TraceEntryCandidate value"
            )
        self._entries.append(entry)

    @property
    def entries(self) -> tuple[TraceEntryCandidate, ...]:
        """Read-only view of every entry appended so far."""

        return tuple(self._entries)

    def __len__(self) -> int:
        return len(self._entries)


__all__ = ["TraceEntryCandidate", "TraceLedger"]
