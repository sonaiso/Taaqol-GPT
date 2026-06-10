"""Rank lattice — PR-3 binding of docs/05 + docs/11 §8.

PR-1A shipped the ``Rank`` enum as a carrier. PR-3 binds the lattice
operations the constitution names:

* ``RankLattice.meet`` — the bounded greatest-lower-bound used by the
  non-promotion law ``OutputRank ≤ meet(EvidenceRank, IdentityRank,
  GateRank, ResidualCeiling)`` (docs/11 §8).
* ``RankLattice.join`` — the bounded least-upper-bound used by the
  evidence aggregation rule (docs/05; see
  ``core/evidence_contract.py``).

The lattice is *pure algebra*: no promotion decision lives here. Only
a ``TransitionGate`` (PR-4) may promote a rank, and only bounded by
``meet`` — this module merely makes that bound computable.

See ``docs/05_RANK_LATTICE.md``.
"""

from __future__ import annotations

from enum import IntEnum


class Rank(IntEnum):
    """Bounded ordered carrier for evidential strength.

    ``IntEnum`` gives total ordering for free. The order is the
    constitutional chain ``ZERO < TRACE < CANDIDATE < HYPOTHESIS <
    LICENSED < STRONG < CERTIFICATE`` (docs/05, docs/11 §8).
    """

    ZERO = 0
    TRACE = 1
    CANDIDATE = 2
    HYPOTHESIS = 3
    LICENSED = 4
    STRONG = 5
    CERTIFICATE = 6


def _require_ranks(operation: str, ranks: tuple[Rank, ...]) -> None:
    """Schema guard shared by :meth:`RankLattice.meet` / ``join``.

    An empty or ill-typed call is a *programmer mistake*, not a
    constitutional verdict (mirrors ``gamma``'s domain guard), so it
    refuses loudly with :class:`TypeError` instead of silently
    synthesising a bound (docs/11 §12 — *no synthesis*).
    """

    if not ranks:
        raise TypeError(
            f"RankLattice.{operation}() requires at least one Rank; "
            "an empty meet/join would silently synthesise a bound"
        )
    for rank in ranks:
        if not isinstance(rank, Rank):
            raise TypeError(
                f"RankLattice.{operation}() accepts only Rank members, "
                f"got {rank!r}"
            )


class RankLattice:
    """Bounded lattice operations over :class:`Rank` (docs/11 §8).

    The lattice is the total order on :class:`Rank`, bounded by
    :attr:`BOTTOM` (``ZERO``) and :attr:`TOP` (``CERTIFICATE``).
    Because the order is total, ``meet`` is ``min`` and ``join`` is
    ``max`` — but callers must speak lattice language: the
    constitution states the non-promotion law in terms of ``meet``,
    and the transition gate (PR-4) is bound to call exactly this
    surface.

    ``RankLattice`` carries **no policy**: it never decides *which*
    ranks enter the meet. The rank ceiling imposed by residuals comes
    from :class:`~taaqqul_slot_geometry.core.residual_policy.ResidualPolicy`;
    the evidence rank comes from
    :class:`~taaqqul_slot_geometry.core.evidence_contract.EvidenceContract`;
    identity and gate ranks join the meet when the gate lands (PR-4).
    """

    BOTTOM: Rank = Rank.ZERO
    TOP: Rank = Rank.CERTIFICATE

    @staticmethod
    def meet(*ranks: Rank) -> Rank:
        """Greatest lower bound of ``ranks``.

        The non-promotion law (docs/11 §8): no code path may produce
        a rank above the ``meet`` of its licensing components. The
        result is always one of the inputs — ``meet`` can only keep
        or lower, never raise.
        """

        _require_ranks("meet", ranks)
        return min(ranks)

    @staticmethod
    def join(*ranks: Rank) -> Rank:
        """Least upper bound of ``ranks``.

        Used by evidence aggregation (docs/05): a pool of sources is
        as strong as its strongest member, never stronger — ``join``
        never invents a rank above every input.
        """

        _require_ranks("join", ranks)
        return max(ranks)


__all__ = ["Rank", "RankLattice"]
