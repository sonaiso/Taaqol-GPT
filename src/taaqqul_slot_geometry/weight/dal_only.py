"""DalOnlyCandidate Boundary — PR-15.

PR-15 binding of ``docs/26_DAL_ONLY_CANDIDATE_BOUNDARY_LAW.md``.
This module introduces:

* :class:`DalBoundaryState` — the two verdict states.
* :class:`DalOnlyCandidate` — the signifier-alone carrier.
* :class:`DalBoundaryVerdict` — the signifier candidacy proof.
* :func:`prove_dal` — the signifier boundary operation consuming only a
  :class:`~taaqqul_slot_geometry.weight.licensing_boundary.LicensingBoundaryVerdict`.

Constitutional invariants (docs/26):

* prove_dal() accepts ONLY a LicensingBoundaryVerdict as prior.
* prove_dal() refuses all earlier-stage carriers.
* DalOnlyCandidate is a signifier identity proof, NOT
  VerbalMadlulCandidate, meaning, ifadah, hukm, or reality.
* No rank promotion beyond DAL_BOUNDARY_RANK_CEILING.
* Residual governance from PR-14 is respected.
* TraceRef remains a reference, not an audit ledger commit.
* No VerbalMadlulCandidate, no DalMadlulBindingCandidate.
* No LexicalMadlul, no meaning, no composition.
* No extra-letter licensing, no ContractableUnitGeometry.
* No new FailureCode members; no new runtime dependencies.
* prove_dal() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.licensing_boundary import (
    LICENSE_BOUNDARY_RANK_CEILING,
    LicensingBoundaryVerdict,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for PR-15 — same as LICENSE_BOUNDARY_RANK_CEILING.
#: No dal boundary verdict may emit a rank above this value (docs/26 §5).
DAL_BOUNDARY_RANK_CEILING: Rank = LICENSE_BOUNDARY_RANK_CEILING


# ---------------------------------------------------------------------------
# DalBoundaryState — the two verdict states
# ---------------------------------------------------------------------------


class DalBoundaryState(StrEnum):
    """The outcome of a prove_dal() operation (docs/26 §4)."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# DalOnlyCandidate — the signifier-alone carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DalOnlyCandidate:
    """The signifier-alone boundary carrier (docs/26 §2).

    Proves the signifier surface (identity, phonetic trace, graphic
    trace, prior licensing boundary verdict) stands independently
    before any signified. It does NOT carry meaning, madlul, ifadah,
    hukm, reality, binding, composition, extra-letter license,
    augmentation category, or ContractableUnitGeometry.

    Fields:
    * ``signifier_identity`` — the signifier surface identity.
    * ``phonetic_trace_ref`` — reference to phonetic trace.
    * ``graphic_trace_ref`` — reference to graphic trace (may be empty
      for oral-only forms).
    * ``prior_licensing_verdict`` — the LicensingBoundaryVerdict from PR-14.
    * ``dal_rank`` — the candidate rank, bounded to the ceiling.
    * ``residuals`` — residuals carried from prior layers.
    * ``trace_ref`` — reference, not ledger commit.
    """

    signifier_identity: str
    phonetic_trace_ref: str
    graphic_trace_ref: str
    prior_licensing_verdict: LicensingBoundaryVerdict
    dal_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.signifier_identity, str) or not self.signifier_identity.strip():
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.signifier_identity must be a non-empty string "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.phonetic_trace_ref, str) or not self.phonetic_trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.phonetic_trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.graphic_trace_ref, str):
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.graphic_trace_ref must be a string "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.prior_licensing_verdict, LicensingBoundaryVerdict):
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.prior_licensing_verdict must be a "
                "LicensingBoundaryVerdict — signifier candidacy without a "
                f"prior licensing verdict is ungated ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.dal_rank, Rank):
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.dal_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.dal_rank > DAL_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.dal_rank must not exceed "
                f"{DAL_BOUNDARY_RANK_CEILING.name} — no rank promotion "
                f"without a gate ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.residuals must be a tuple of Residual carriers "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "DalOnlyCandidate.residuals entries must be Residual carriers "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalOnlyCandidate.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )


# ---------------------------------------------------------------------------
# DalBoundaryVerdict — the signifier candidacy proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DalBoundaryVerdict:
    """The output of :func:`prove_dal` — a signifier candidacy proof (docs/26 §4).

    Proves that a signifier surface can stand independently as a
    boundary-proven candidate. It does NOT carry meaning, madlul,
    ifadah, hukm, reality, binding, or any post-signifier content.

    Fields:
    * ``candidate`` — the DalOnlyCandidate that was proven (or None on refusal).
    * ``verdict_state`` — PROVEN or REFUSED.
    * ``failure_code`` — named FailureCode on refusal, None on success.
    * ``verdict_rank`` — the verdict rank, bounded to the ceiling.
    * ``residuals`` — residuals carried through.
    * ``trace_ref`` — reference, not ledger commit.
    """

    candidate: DalOnlyCandidate | None
    verdict_state: DalBoundaryState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.verdict_state, DalBoundaryState):
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.verdict_state must be a DalBoundaryState member"
            )
        if not isinstance(self.verdict_rank, Rank):
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.verdict_rank must be a Rank member"
            )
        if self.verdict_rank > DAL_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.verdict_rank must not exceed "
                f"DAL_BOUNDARY_RANK_CEILING ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "DalBoundaryVerdict.residuals entries must be Residual carriers"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalBoundaryVerdict.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        # State invariants
        if self.verdict_state is DalBoundaryState.PROVEN:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a PROVEN DalBoundaryVerdict must not carry a FailureCode "
                    "(docs/26 §4)"
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "a PROVEN DalBoundaryVerdict must carry a DalOnlyCandidate "
                    "(docs/26 §4)"
                )
            if not isinstance(self.candidate, DalOnlyCandidate):
                raise WeightCarrierSchemaError(
                    "DalBoundaryVerdict.candidate must be a DalOnlyCandidate "
                    "(docs/26 §4)"
                )
        elif self.verdict_state is DalBoundaryState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED DalBoundaryVerdict must carry a named FailureCode "
                    "(docs/26 §4)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "DalBoundaryVerdict.failure_code must be a FailureCode member"
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED DalBoundaryVerdict must not carry a candidate "
                    "(docs/26 §4)"
                )


# ---------------------------------------------------------------------------
# prove_dal() — the signifier boundary operation
# ---------------------------------------------------------------------------


def prove_dal(
    prior_verdict: LicensingBoundaryVerdict,
    signifier_identity: str,
    phonetic_trace_ref: str,
    graphic_trace_ref: str = "",
) -> DalBoundaryVerdict:
    """Signifier boundary proof — signifier candidacy (docs/26).

    A pure function: evaluates whether the signifier surface described
    by a prior :class:`LicensingBoundaryVerdict` can stand independently
    as a DalOnlyCandidate, producing a :class:`DalBoundaryVerdict`.

    Input boundary (docs/26 §3):

    * Accepts ONLY a LicensingBoundaryVerdict as prior.
    * Refuses all other input types with a named FailureCode.

    Output:

    * On success: PROVEN with a DalOnlyCandidate.
    * On refusal: REFUSED with a named FailureCode.

    This function is pure: no I/O, no ledger writes, no network.
    """
    # --- Input boundary enforcement ---
    if not isinstance(prior_verdict, LicensingBoundaryVerdict):
        return DalBoundaryVerdict(
            candidate=None,
            verdict_state=DalBoundaryState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_dal/refused/input_boundary",
        )

    # --- Signifier identity validation ---
    if not isinstance(signifier_identity, str) or not signifier_identity.strip():
        return DalBoundaryVerdict(
            candidate=None,
            verdict_state=DalBoundaryState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_dal/refused/signifier_identity_missing",
        )

    # --- Phonetic trace validation ---
    if not isinstance(phonetic_trace_ref, str) or not phonetic_trace_ref.strip():
        return DalBoundaryVerdict(
            candidate=None,
            verdict_state=DalBoundaryState.REFUSED,
            failure_code=FailureCode.TRACE_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_dal/refused/phonetic_trace_missing",
        )

    # --- Graphic trace ref validation (must be str, may be empty) ---
    if not isinstance(graphic_trace_ref, str):
        return DalBoundaryVerdict(
            candidate=None,
            verdict_state=DalBoundaryState.REFUSED,
            failure_code=FailureCode.TRACE_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_dal/refused/graphic_trace_invalid",
        )

    # --- Residual governance from the prior verdict ---
    # Inherit residuals from the prior verdict's source (the WeightFitCandidate)
    inherited_residuals = prior_verdict.source.residuals

    # Check for hidden-forbidden residuals
    for r in inherited_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return DalBoundaryVerdict(
                candidate=None,
                verdict_state=DalBoundaryState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=inherited_residuals,
                trace_ref="prove_dal/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return DalBoundaryVerdict(
                candidate=None,
                verdict_state=DalBoundaryState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=inherited_residuals,
                trace_ref="prove_dal/refused/blocking_residual",
            )

    # --- Bound the rank ---
    dal_rank = RankLattice.meet(
        prior_verdict.eligibility_rank, DAL_BOUNDARY_RANK_CEILING
    )

    # --- Construct the DalOnlyCandidate ---
    candidate = DalOnlyCandidate(
        signifier_identity=signifier_identity,
        phonetic_trace_ref=phonetic_trace_ref,
        graphic_trace_ref=graphic_trace_ref,
        prior_licensing_verdict=prior_verdict,
        dal_rank=dal_rank,
        residuals=inherited_residuals,
        trace_ref=f"prove_dal/proven/{signifier_identity}",
    )

    return DalBoundaryVerdict(
        candidate=candidate,
        verdict_state=DalBoundaryState.PROVEN,
        failure_code=None,
        verdict_rank=dal_rank,
        residuals=inherited_residuals,
        trace_ref=f"prove_dal/proven/{signifier_identity}",
    )


__all__ = [
    "DAL_BOUNDARY_RANK_CEILING",
    "DalBoundaryState",
    "DalBoundaryVerdict",
    "DalOnlyCandidate",
    "prove_dal",
]
