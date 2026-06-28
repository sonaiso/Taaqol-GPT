"""Trace ledger carriers — PR-2 minimal binding, PR-6 trace split.

This module ships:

* :class:`TraceEntryCandidate` — the immutable value that ``Γ``
  packages inside its :class:`GammaResult`. The candidate is a *pure
  value*; appending it to the ledger is the caller's responsibility
  (docs/07 — *the purity rule*).

* :class:`TraceLedger` — a minimal in-memory append-only container.
  PR-2 stays in-memory; persistence is out of scope through PR-6
  (docs/07 — *The ledger itself is in-memory in PR-2 and stays
  in-memory through PR-6*).

PR-6 splits the former single ``snapshot_state`` field into
``consulted_gamma_state`` (always a :class:`ClosureState` — what
``Γ`` said about the *graph*) and ``gate_transition_state`` (a
:class:`TransitionState` for ``"gate"`` / ``"audit"`` entries —
what the gate said about the *move*; ``None`` for ``"gamma"``
entries). The two judgements never share one field again, so a
ledger reader can no longer mistake a closure verdict for a gate
verdict (docs/07 — *PR-6 binding*).

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
from taaqqul_slot_geometry.core.transition_state import TransitionState

# The named verdict stages a candidate may snapshot: "gamma" since
# PR-2, "gate" since PR-4, "audit" since PR-6, "audit.reasonableness"
# since GPT-R8 (docs/07; docs/56 §2 B6 — the reasonableness verdict's
# trace_ref appends in constitutional order, after the "audit" entry,
# never replacing it).
_KNOWN_STAGES: tuple[str, ...] = ("gamma", "gate", "audit", "audit.reasonableness")


@dataclass(frozen=True, slots=True)
class TraceEntryCandidate:
    """An opaque, immutable trace event proposed by ``Γ``.

    Fields mirror the :class:`~docs/07_TRACE_LEDGER` ``TraceEntry``
    schema with the minimum needed for the kernel:

    * ``parent_anchor`` — the opaque trace anchor copied from the
      graph's :class:`~taaqqul_slot_geometry.core.slot_graph.Center`.
      Core never inspects its contents.
    * ``stage`` — the named verdict stage (``"gamma"`` since PR-2,
      ``"gate"`` since PR-4, ``"audit"`` since PR-6,
      ``"audit.reasonableness"`` since GPT-R8 — docs/56 §2 B6).
    * ``consulted_gamma_state`` — the :class:`ClosureState` ``Γ``
      returned for the graph under examination. Every stage carries
      it: the gate and the audit wrapper are bound to consult ``Γ``
      first (docs/11 §11) and the trace records what it said.
    * ``gate_transition_state`` — the :class:`TransitionState` the
      gate returned for the *move*. Mandatory for ``"gate"`` and
      ``"audit"`` entries; ``None`` for ``"gamma"`` entries, which
      precede any gate (docs/07 — *PR-6 binding*: the split keeps a
      graph verdict and a move verdict in two distinct fields).
    * ``snapshot_failure`` / ``snapshot_rank`` — the named refusal
      (``None`` for closure / approval) and the rank snapshot.

    The candidate is a *value*. It does not write itself anywhere.
    A malformed candidate is a programmer mistake refused loudly at
    birth with ``TypeError`` (mirroring :meth:`TraceLedger.append`),
    never a constitutional verdict.
    """

    parent_anchor: str
    stage: str
    consulted_gamma_state: ClosureState
    gate_transition_state: TransitionState | None
    snapshot_failure: FailureCode | None
    snapshot_rank: Rank

    def __post_init__(self) -> None:
        if not isinstance(self.parent_anchor, str):
            raise TypeError("TraceEntryCandidate.parent_anchor must be a string")
        if self.stage not in _KNOWN_STAGES:
            raise TypeError(
                "TraceEntryCandidate.stage must be one of 'gamma', 'gate', "
                "'audit', 'audit.reasonableness' (docs/07; docs/56 §2 B6)"
            )
        if not isinstance(self.consulted_gamma_state, ClosureState):
            raise TypeError(
                "TraceEntryCandidate.consulted_gamma_state must be a "
                "ClosureState member"
            )
        if self.stage == "gamma":
            if self.gate_transition_state is not None:
                raise TypeError(
                    "a stage='gamma' TraceEntryCandidate precedes any gate "
                    "and must carry gate_transition_state=None (docs/07 — "
                    "PR-6 binding)"
                )
        elif not isinstance(self.gate_transition_state, TransitionState):
            raise TypeError(
                f"a stage={self.stage!r} TraceEntryCandidate must carry a "
                "TransitionState gate_transition_state (docs/07 — PR-6 "
                "binding)"
            )
        if self.snapshot_failure is not None and not isinstance(
            self.snapshot_failure, FailureCode
        ):
            raise TypeError(
                "TraceEntryCandidate.snapshot_failure must be a FailureCode "
                "or None"
            )
        if not isinstance(self.snapshot_rank, Rank):
            raise TypeError("TraceEntryCandidate.snapshot_rank must be a Rank member")


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
