"""Trace ledger — PR-1 surface.

PR-1 ships two things:

* ``TraceEntryCandidate`` — the immutable shape ``gamma`` puts inside
  every ``GammaResult``.
* ``TraceLedger`` — a minimal in-memory append-only container. It
  exists so callers and tests have something concrete to assert
  against. **``gamma.py`` must not import ``TraceLedger``**; a static
  guard in ``tests/test_gamma_purity.py`` enforces this.

See ``docs/07_TRACE_LEDGER.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode


@dataclass(frozen=True, slots=True)
class TraceEntryCandidate:
    """An immutable trace event proposed by a pure verdict function.

    The candidate is appended to a ``TraceLedger`` by an outer caller,
    never by the function that produced it.
    """

    stage: str
    input_ref: str
    verdict: str
    failure_code: FailureCode | None = None
    residuals_seen: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


class TraceLedger:
    """Minimal in-memory append-only ledger.

    Not imported by ``gamma``. Provided so callers (and the purity
    test) have a concrete container to assert against.
    """

    __slots__ = ("_entries",)

    def __init__(self) -> None:
        self._entries: list[TraceEntryCandidate] = []

    def append(self, entry: TraceEntryCandidate) -> None:
        if not isinstance(entry, TraceEntryCandidate):
            raise TypeError("TraceLedger only accepts TraceEntryCandidate entries")
        self._entries.append(entry)

    @property
    def entries(self) -> tuple[TraceEntryCandidate, ...]:
        return tuple(self._entries)

    def __len__(self) -> int:
        return len(self._entries)


__all__ = ["TraceEntryCandidate", "TraceLedger"]
