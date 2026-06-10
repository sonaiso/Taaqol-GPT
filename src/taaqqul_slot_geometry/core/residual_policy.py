"""Residual policy — PR-3 binding of docs/06 + docs/11 §9.

PR-1A shipped the ``ResidualKind`` enum and the immutable
``Residual`` dataclass as carriers. PR-3 binds the policy engine the
constitution names:

* the per-kind **rank caps** (docs/06 — *Residual kinds*);
* the **residual ceiling** ``ResidualCeiling(G) = meet over δ of
  rank-cap(δ.kind)`` (docs/11 §9) consumed by ``Γ`` step 9;
* the **visibility law** ``ResidualHidden → ApprovedOutput is
  forbidden`` surfaced through :meth:`ResidualPolicy.evaluate`.

The policy is pure: it accepts residual tuples and returns values.
It never mutates a graph, never suppresses a residual, and never
promotes a rank — a ceiling can only keep or lower what the lattice
``meet`` already bounds.

See ``docs/06_RESIDUAL_POLICY.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice


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

    The PR-3 engine reads the carrier and never rewrites it
    (visibility is declared at birth, not edited). PR-3-FIX hardens
    the birth itself: :meth:`ResidualPolicy.ceiling` and ``Γ`` step 9
    consume the carrier as-is, so every field is guarded at
    construction time (docs/11 §12 — missing means refuse). A
    malformed residual is refused loudly with ``TypeError`` — a
    programmer mistake, not a constitutional verdict, mirroring the
    :meth:`ResidualPolicy.rank_cap` and ``RankLattice`` domain
    guards — and therefore can never reach the policy engine or
    ``Γ``.
    """

    name: str
    kind: ResidualKind
    visible: bool
    note: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise TypeError("Residual.name must be a non-empty string")
        if not isinstance(self.kind, ResidualKind):
            raise TypeError("Residual.kind must be a ResidualKind")
        if not isinstance(self.visible, bool):
            raise TypeError("Residual.visible must be a bool")
        if not isinstance(self.note, str):
            raise TypeError("Residual.note must be a string")


# Residual kinds that, when visible, license a perforated closure
# (docs/11 §6). HIDDEN_FORBIDDEN is *never* in this set; BLOCKING is
# refused at ``Γ`` step 7 before perforation is consulted. This is the
# canonical home of the set — ``Γ`` step 10 imports it from here.
PERFORATING_KINDS: frozenset[ResidualKind] = frozenset(
    {
        ResidualKind.NON_BLOCKING,
        ResidualKind.DEFERRABLE,
        ResidualKind.EXPLANATORY,
    }
)


# Per-kind rank caps (docs/06 — *Residual kinds*; docs/11 §9):
#
# * ``BLOCKING`` prevents closure entirely — nothing above ``ZERO``
#   may travel while one is present.
# * ``HIDDEN_FORBIDDEN`` is a fatal contract violation — same floor.
# * ``DEFERRABLE`` does not block closure but caps the output rank at
#   ``HYPOTHESIS``.
# * ``NON_BLOCKING`` / ``EXPLANATORY`` do not affect rank — their cap
#   is the lattice top (no constraint), not a promotion.
_RANK_CAPS: dict[ResidualKind, Rank] = {
    ResidualKind.BLOCKING: Rank.ZERO,
    ResidualKind.HIDDEN_FORBIDDEN: Rank.ZERO,
    ResidualKind.DEFERRABLE: Rank.HYPOTHESIS,
    ResidualKind.NON_BLOCKING: RankLattice.TOP,
    ResidualKind.EXPLANATORY: RankLattice.TOP,
}


@dataclass(frozen=True, slots=True)
class ResidualEvaluation:
    """Pure value returned by :meth:`ResidualPolicy.evaluate`.

    Properties:

    * ``failure_code`` — ``None`` when the residual surface is
      admissible; :attr:`FailureCode.HIDDEN_RESIDUAL` when any
      residual is hidden or invisible (docs/11 §9 — fatal);
      :attr:`FailureCode.BLOCKING_RESIDUAL_PRESENT` when a visible
      blocking residual remains. Hidden wins over blocking, mirroring
      the ordered law (``Γ`` step 6 before step 7).
    * ``ceiling`` — ``ResidualCeiling`` per docs/11 §9: the lattice
      ``meet`` of every per-kind cap. The empty surface yields the
      lattice top — *vacuously* no residual constraint, **not** a
      licence (the §8 meet with evidence / identity / gate ranks
      still binds at the gate).
    * ``all_visible`` — the visibility conjunction (every residual is
      visible and not ``HIDDEN_FORBIDDEN``); vacuously true when no
      residual exists.
    * ``perforating`` — whether any visible residual licenses a
      perforated closure (kind in :data:`PERFORATING_KINDS`).
    """

    failure_code: FailureCode | None
    ceiling: Rank
    all_visible: bool
    perforating: bool


class ResidualPolicy:
    """The residual engine named by docs/06 and consumed by ``Γ`` / Gate.

    Every method is a pure static function over the immutable
    :class:`Residual` carriers. The policy never edits, suppresses,
    or reclassifies a residual; it only *reads* the declared surface
    and reports caps and named refusals.
    """

    @staticmethod
    def rank_cap(kind: ResidualKind) -> Rank:
        """Per-kind output-rank cap (docs/06 — *Residual kinds*)."""

        if not isinstance(kind, ResidualKind):
            raise TypeError(
                f"ResidualPolicy.rank_cap() accepts only ResidualKind members, "
                f"got {kind!r}"
            )
        return _RANK_CAPS[kind]

    @staticmethod
    def ceiling(residuals: tuple[Residual, ...]) -> Rank:
        """``ResidualCeiling(G)`` — meet of per-kind caps (docs/11 §9).

        The meet over the empty residual surface is the lattice top:
        no residual imposes a constraint. That is the standard
        lattice convention, stated here explicitly so it can never be
        mistaken for a promotion — the value only ever *enters* a
        ``meet``, it is never an output rank by itself.
        """

        caps = tuple(ResidualPolicy.rank_cap(residual.kind) for residual in residuals)
        if not caps:
            return RankLattice.TOP
        return RankLattice.meet(*caps)

    @staticmethod
    def evaluate(residuals: tuple[Residual, ...]) -> ResidualEvaluation:
        """Evaluate a residual surface into a :class:`ResidualEvaluation`.

        The refusal order mirrors the ordered closure law (docs/03,
        docs/11 §7): a hidden residual (``Γ`` step 6) is named before
        a blocking residual (``Γ`` step 7). Every refusal is a named
        :class:`FailureCode` value — never an exception, never a
        silent ``None``.
        """

        all_visible = all(
            residual.visible and residual.kind is not ResidualKind.HIDDEN_FORBIDDEN
            for residual in residuals
        )
        perforating = any(
            residual.visible and residual.kind in PERFORATING_KINDS
            for residual in residuals
        )
        ceiling = ResidualPolicy.ceiling(residuals)

        failure_code: FailureCode | None = None
        if not all_visible:
            failure_code = FailureCode.HIDDEN_RESIDUAL
        elif any(residual.kind is ResidualKind.BLOCKING for residual in residuals):
            failure_code = FailureCode.BLOCKING_RESIDUAL_PRESENT

        return ResidualEvaluation(
            failure_code=failure_code,
            ceiling=ceiling,
            all_visible=all_visible,
            perforating=perforating,
        )


__all__ = [
    "PERFORATING_KINDS",
    "Residual",
    "ResidualEvaluation",
    "ResidualKind",
    "ResidualPolicy",
]
