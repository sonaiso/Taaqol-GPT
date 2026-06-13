"""VerbalMadlulCandidate Boundary — PR-16.

PR-16 binding of ``docs/27_VERBAL_MADLUL_CANDIDATE_BOUNDARY_LAW.md``.
This module introduces:

* :class:`MadlulBoundaryState` — the two verdict states.
* :class:`VerbalMadlulCandidate` — the verbal signified candidate carrier.
* :class:`VerbalMadlulBoundaryVerdict` — the verbal signified candidacy proof.
* :func:`prove_verbal_madlul` — the verbal signified boundary operation
  consuming only a
  :class:`~taaqqul_slot_geometry.weight.dal_only.DalOnlyCandidate`.

Constitutional invariants (docs/27):

* prove_verbal_madlul() accepts ONLY a DalOnlyCandidate as prior.
* prove_verbal_madlul() refuses all earlier-stage carriers.
* VerbalMadlulCandidate is a verbal signified candidacy proof, NOT
  meaning, reference, ifadah, hukm, or reality.
* No rank promotion beyond MADLUL_BOUNDARY_RANK_CEILING.
* Residual governance from PR-15 is respected.
* TraceRef remains a reference, not an audit ledger commit.
* No DalMadlulBindingCandidate, no meaning, no reference certainty.
* No extra-letter licensing, no ContractableUnitGeometry.
* correspondence_candidate is not final denotation.
* inclusion_candidate is not final concept.
* iltizam_condition is a condition, not a conclusion.
* No new FailureCode members; no new runtime dependencies.
* prove_verbal_madlul() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.dal_only import (
    DAL_BOUNDARY_RANK_CEILING,
    DalOnlyCandidate,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for PR-16 — same as DAL_BOUNDARY_RANK_CEILING.
#: No verbal madlul boundary verdict may emit a rank above this value (docs/27 §5).
MADLUL_BOUNDARY_RANK_CEILING: Rank = DAL_BOUNDARY_RANK_CEILING


# ---------------------------------------------------------------------------
# MadlulBoundaryState — the two verdict states
# ---------------------------------------------------------------------------


class MadlulBoundaryState(StrEnum):
    """The outcome of a prove_verbal_madlul() operation (docs/27 §4)."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# VerbalMadlulCandidate — the verbal signified candidate carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class VerbalMadlulCandidate:
    """The verbal signified boundary carrier (docs/27 §2).

    Proves the verbal signified (wadʿ/usage boundary, conceptual
    correspondence candidate, inclusion candidate, iltizām condition,
    existence/event/relation affordance candidates) stands independently
    before any meaning. It does NOT carry meaning, reference, ifadah,
    hukm, reality, binding, composition, extra-letter license,
    augmentation category, or ContractableUnitGeometry.

    Fields:
    * ``dal_only`` — the proven DalOnlyCandidate from PR-15.
    * ``wad_usage_boundary`` — the wadʿ/usage evidence boundary.
    * ``correspondence_candidate`` — conceptual correspondence as
      candidate, not as final denotation.
    * ``inclusion_candidate`` — inclusion as candidate, not as final
      concept.
    * ``iltizam_condition`` — iltizām as condition, not as conclusion.
    * ``existence_carrier_candidate`` — existence affordance as
      candidate, not as ontological claim.
    * ``event_carrier_candidate`` — event affordance as candidate,
      not as real event.
    * ``relation_affordance_candidate`` — relation affordance as
      candidate, not as RelationCandidate.
    * ``madlul_rank`` — the candidate rank, bounded to the ceiling.
    * ``residuals`` — residuals carried from prior layers.
    * ``trace_ref`` — reference, not ledger commit.
    """

    dal_only: DalOnlyCandidate
    wad_usage_boundary: str
    correspondence_candidate: str
    inclusion_candidate: str
    iltizam_condition: str
    existence_carrier_candidate: str
    event_carrier_candidate: str
    relation_affordance_candidate: str
    madlul_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.dal_only, DalOnlyCandidate):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.dal_only must be a DalOnlyCandidate "
                "— verbal signified candidacy without a proven signifier "
                f"is ungated ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.wad_usage_boundary, str) or not self.wad_usage_boundary.strip():
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.wad_usage_boundary must be a non-empty "
                f"string ({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.correspondence_candidate, str):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.correspondence_candidate must be a string "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.inclusion_candidate, str):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.inclusion_candidate must be a string "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.iltizam_condition, str):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.iltizam_condition must be a string "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.existence_carrier_candidate, str):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.existence_carrier_candidate must be a string "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.event_carrier_candidate, str):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.event_carrier_candidate must be a string "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.relation_affordance_candidate, str):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.relation_affordance_candidate must be a string "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.madlul_rank, Rank):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.madlul_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.madlul_rank > MADLUL_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.madlul_rank must not exceed "
                f"{MADLUL_BOUNDARY_RANK_CEILING.name} — no rank promotion "
                f"without a gate ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.residuals must be a tuple of Residual carriers "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "VerbalMadlulCandidate.residuals entries must be Residual carriers "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "VerbalMadlulCandidate.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )


# ---------------------------------------------------------------------------
# VerbalMadlulBoundaryVerdict — the verbal signified candidacy proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class VerbalMadlulBoundaryVerdict:
    """The output of :func:`prove_verbal_madlul` (docs/27 §4).

    Proves that a verbal signified can stand independently as a
    boundary-proven candidate. It does NOT carry meaning, reference,
    ifadah, hukm, reality, binding, or any post-signified content.

    Fields:
    * ``candidate`` — the VerbalMadlulCandidate that was proven (or None
      on refusal).
    * ``verdict_state`` — PROVEN or REFUSED.
    * ``failure_code`` — named FailureCode on refusal, None on success.
    * ``verdict_rank`` — the verdict rank, bounded to the ceiling.
    * ``residuals`` — residuals carried through.
    * ``trace_ref`` — reference, not ledger commit.
    """

    candidate: VerbalMadlulCandidate | None
    verdict_state: MadlulBoundaryState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.verdict_state, MadlulBoundaryState):
            raise WeightCarrierSchemaError(
                "VerbalMadlulBoundaryVerdict.verdict_state must be a "
                "MadlulBoundaryState member"
            )
        if not isinstance(self.verdict_rank, Rank):
            raise WeightCarrierSchemaError(
                "VerbalMadlulBoundaryVerdict.verdict_rank must be a Rank member"
            )
        if self.verdict_rank > MADLUL_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "VerbalMadlulBoundaryVerdict.verdict_rank must not exceed "
                f"MADLUL_BOUNDARY_RANK_CEILING ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "VerbalMadlulBoundaryVerdict.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "VerbalMadlulBoundaryVerdict.residuals entries must be "
                    "Residual carriers"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "VerbalMadlulBoundaryVerdict.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        # State invariants
        if self.verdict_state is MadlulBoundaryState.PROVEN:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a PROVEN VerbalMadlulBoundaryVerdict must not carry a "
                    "FailureCode (docs/27 §4)"
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "a PROVEN VerbalMadlulBoundaryVerdict must carry a "
                    "VerbalMadlulCandidate (docs/27 §4)"
                )
            if not isinstance(self.candidate, VerbalMadlulCandidate):
                raise WeightCarrierSchemaError(
                    "VerbalMadlulBoundaryVerdict.candidate must be a "
                    "VerbalMadlulCandidate (docs/27 §4)"
                )
        elif self.verdict_state is MadlulBoundaryState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED VerbalMadlulBoundaryVerdict must carry a named "
                    "FailureCode (docs/27 §4)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "VerbalMadlulBoundaryVerdict.failure_code must be a "
                    "FailureCode member"
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED VerbalMadlulBoundaryVerdict must not carry a "
                    "candidate (docs/27 §4)"
                )


# ---------------------------------------------------------------------------
# prove_verbal_madlul() — the verbal signified boundary operation
# ---------------------------------------------------------------------------


def prove_verbal_madlul(
    prior_dal: DalOnlyCandidate,
    wad_usage_boundary: str,
    correspondence_candidate: str = "",
    inclusion_candidate: str = "",
    iltizam_condition: str = "",
    existence_carrier_candidate: str = "",
    event_carrier_candidate: str = "",
    relation_affordance_candidate: str = "",
) -> VerbalMadlulBoundaryVerdict:
    """Verbal signified boundary proof — verbal signified candidacy (docs/27).

    A pure function: evaluates whether a verbal signified described
    by a prior :class:`DalOnlyCandidate` can stand independently as a
    VerbalMadlulCandidate, producing a :class:`VerbalMadlulBoundaryVerdict`.

    Input boundary (docs/27 §3):

    * Accepts ONLY a DalOnlyCandidate as prior.
    * Refuses all other input types with a named FailureCode.

    Output:

    * On success: PROVEN with a VerbalMadlulCandidate.
    * On refusal: REFUSED with a named FailureCode.

    This function is pure: no I/O, no ledger writes, no network.
    """
    # --- Input boundary enforcement ---
    if not isinstance(prior_dal, DalOnlyCandidate):
        return VerbalMadlulBoundaryVerdict(
            candidate=None,
            verdict_state=MadlulBoundaryState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_verbal_madlul/refused/input_boundary",
        )

    # --- Wadʿ/usage boundary validation ---
    if not isinstance(wad_usage_boundary, str) or not wad_usage_boundary.strip():
        return VerbalMadlulBoundaryVerdict(
            candidate=None,
            verdict_state=MadlulBoundaryState.REFUSED,
            failure_code=FailureCode.BOUNDARY_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_verbal_madlul/refused/wad_usage_boundary_missing",
        )

    # --- Residual governance from the prior dal candidate ---
    inherited_residuals = prior_dal.residuals

    # Check for hidden-forbidden residuals
    for r in inherited_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return VerbalMadlulBoundaryVerdict(
                candidate=None,
                verdict_state=MadlulBoundaryState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=inherited_residuals,
                trace_ref="prove_verbal_madlul/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return VerbalMadlulBoundaryVerdict(
                candidate=None,
                verdict_state=MadlulBoundaryState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=inherited_residuals,
                trace_ref="prove_verbal_madlul/refused/blocking_residual",
            )

    # --- Bound the rank ---
    madlul_rank = RankLattice.meet(
        prior_dal.dal_rank, MADLUL_BOUNDARY_RANK_CEILING
    )

    # --- Construct the VerbalMadlulCandidate ---
    candidate = VerbalMadlulCandidate(
        dal_only=prior_dal,
        wad_usage_boundary=wad_usage_boundary,
        correspondence_candidate=correspondence_candidate,
        inclusion_candidate=inclusion_candidate,
        iltizam_condition=iltizam_condition,
        existence_carrier_candidate=existence_carrier_candidate,
        event_carrier_candidate=event_carrier_candidate,
        relation_affordance_candidate=relation_affordance_candidate,
        madlul_rank=madlul_rank,
        residuals=inherited_residuals,
        trace_ref=f"prove_verbal_madlul/proven/{prior_dal.signifier_identity}",
    )

    return VerbalMadlulBoundaryVerdict(
        candidate=candidate,
        verdict_state=MadlulBoundaryState.PROVEN,
        failure_code=None,
        verdict_rank=madlul_rank,
        residuals=inherited_residuals,
        trace_ref=f"prove_verbal_madlul/proven/{prior_dal.signifier_identity}",
    )


__all__ = [
    "MADLUL_BOUNDARY_RANK_CEILING",
    "MadlulBoundaryState",
    "VerbalMadlulBoundaryVerdict",
    "VerbalMadlulCandidate",
    "prove_verbal_madlul",
]
