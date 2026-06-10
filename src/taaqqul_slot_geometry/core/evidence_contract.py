"""Evidence contract — PR-3 carriers for docs/05 + docs/08 + docs/11 §8.

The transition gate (PR-4) refuses to run without evidence: its
preconditions (docs/08) require a non-empty evidence surface carrying
an ``evidence_rank`` that enters the non-promotion ``meet`` of
docs/11 §8. PR-3 ships exactly the carriers that make that
precondition speakable:

* :class:`EvidenceSource` — one named, traced piece of evidence with
  a declared rank.
* :class:`EvidenceContract` — the immutable pool of sources whose
  aggregate :attr:`~EvidenceContract.evidence_rank` the gate consumes.

The contract is a carrier, not a judge: it never approves an output,
never issues a certificate, and never licenses a transition. The
single law it *does* bind is the canonical anti-straight-line of
docs/11 §8 — **a single evidence source may never license
``CERTIFICATE``** (``Evidence → Certainty`` is the forbidden line of
docs/04; the carrier caps it at :data:`SINGLE_SOURCE_EVIDENCE_CEILING`
before any gate ever sees it).

The per-*kind* evidence ceiling table named by docs/05 remains a
declared residual of this PR: no canonical kind list exists yet (the
lexicon surface is forbidden until far later PRs), so ``kind`` stays
an opaque non-empty string and imposes no rank semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.slot_graph import SlotGraphSchemaError, TraceRef

# docs/11 §8: "A single evidence source may never license CERTIFICATE."
# The cap is the rank immediately below the lattice top.
SINGLE_SOURCE_EVIDENCE_CEILING: Rank = Rank.STRONG


@dataclass(frozen=True, slots=True)
class EvidenceSource:
    """One named, traced piece of evidence with a declared rank.

    Mandatory fields (missing means refuse — docs/11 §12):

    * ``name`` — the identity of the source; an empty name is a
      broken identity (:attr:`FailureCode.IDENTITY_BROKEN`).
    * ``kind`` — the declared domain the evidence comes from; opaque
      to core in PR-3, but it must be declared
      (:attr:`FailureCode.DOMAIN_MISSING`).
    * ``rank`` — the evidential strength the source itself carries.
      The carrier never raises it; aggregation can only ``meet`` /
      ``join`` it.
    * ``trace_ref`` — every piece of evidence names where it came
      from; evidence without a trace is not evidence
      (:attr:`FailureCode.TRACE_MISSING`).
    """

    name: str
    kind: str
    rank: Rank
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise SlotGraphSchemaError(
                "EvidenceSource.name must be a non-empty string "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise SlotGraphSchemaError(
                "EvidenceSource.kind must be a non-empty string "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )
        if not isinstance(self.rank, Rank):
            raise SlotGraphSchemaError(
                f"EvidenceSource.rank must be a Rank member, got {self.rank!r}"
            )
        if not isinstance(self.trace_ref, TraceRef):
            raise SlotGraphSchemaError(
                "EvidenceSource.trace_ref must be a TraceRef "
                f"({FailureCode.TRACE_MISSING.value})"
            )


@dataclass(frozen=True, slots=True)
class EvidenceContract:
    """Immutable pool of evidence sources consumed by the gate (PR-4).

    An empty contract is legal as a *carrier*: it states, loudly and
    inspectably, that no evidence exists, and its
    :attr:`evidence_rank` is the lattice bottom (``ZERO``). The gate
    precondition that refuses to run on empty evidence (docs/08)
    belongs to the gate, not to this carrier — PR-3 must not license
    or refuse transitions.
    """

    sources: tuple[EvidenceSource, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.sources, tuple):
            raise SlotGraphSchemaError(
                "EvidenceContract.sources must be a tuple of EvidenceSource"
            )
        for source in self.sources:
            if not isinstance(source, EvidenceSource):
                raise SlotGraphSchemaError(
                    "EvidenceContract.sources accepts only EvidenceSource "
                    f"members, got {source!r}"
                )

    @property
    def evidence_rank(self) -> Rank:
        """The aggregate rank this evidence pool can enter into a meet.

        * No source — the lattice bottom (``ZERO``): absent evidence
          licenses nothing.
        * One source — the source's own rank capped at
          :data:`SINGLE_SOURCE_EVIDENCE_CEILING` (docs/11 §8: a single
          source never licenses ``CERTIFICATE``).
        * Several sources — the lattice ``join``: a pool is as strong
          as its strongest member, never stronger. No corroboration
          bonus is synthesised; only a gate (PR-4) may weigh sources
          against each other, and only bounded by the §8 meet.
        """

        if not self.sources:
            return RankLattice.BOTTOM
        if len(self.sources) == 1:
            return RankLattice.meet(
                self.sources[0].rank, SINGLE_SOURCE_EVIDENCE_CEILING
            )
        return RankLattice.join(*(source.rank for source in self.sources))


__all__ = [
    "SINGLE_SOURCE_EVIDENCE_CEILING",
    "EvidenceContract",
    "EvidenceSource",
]
