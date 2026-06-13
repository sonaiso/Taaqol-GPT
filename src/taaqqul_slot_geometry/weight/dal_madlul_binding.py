"""DalMadlulBindingCandidate Boundary — PR-17.

PR-17 binding of ``docs/31_DAL_MADLUL_BINDING_LAW.md``.
This module introduces:

* :class:`BindingState` — the two verdict states.
* :class:`DalMadlulBindingCandidate` — the binding carrier.
* :class:`DalMadlulBindingVerdict` — the binding proof.
* :func:`bind_dal_madlul` — the binding operation consuming a
  :class:`~taaqqul_slot_geometry.weight.dal_only.DalOnlyCandidate`
  and a
  :class:`~taaqqul_slot_geometry.weight.verbal_madlul.VerbalMadlulCandidate`
  with registry evidence.

Constitutional invariants (docs/31):

* bind_dal_madlul() accepts ONLY a DalOnlyCandidate +
  VerbalMadlulCandidate + two RegistryLookupResult instances.
* bind_dal_madlul() refuses all invalid input combinations.
* DalMadlulBindingCandidate is a pre-semantic binding proof, NOT
  meaning, ifadah, hukm, or reality.
* DalMadlulBindingCandidate is NOT ContractableUnitGeometry.
* No rank promotion beyond BINDING_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* TraceRef remains a reference, not an audit ledger commit.
* No meaning, no composition, no relation, no extra-letter license.
* No new FailureCode members; no new runtime dependencies.
* bind_dal_madlul() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.dal_only import DalOnlyCandidate
from taaqqul_slot_geometry.weight.registry_contract import (
    RegistryLookupResult,
    RegistryLookupState,
)
from taaqqul_slot_geometry.weight.verbal_madlul import (
    MADLUL_BOUNDARY_RANK_CEILING,
    VerbalMadlulCandidate,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for PR-17 — same as MADLUL_BOUNDARY_RANK_CEILING.
#: No binding verdict may emit a rank above this value (docs/31 §3).
BINDING_RANK_CEILING: Rank = MADLUL_BOUNDARY_RANK_CEILING


# ---------------------------------------------------------------------------
# BindingState — the two verdict states
# ---------------------------------------------------------------------------


class BindingState(StrEnum):
    """The outcome of a bind_dal_madlul() operation (docs/31 §4)."""

    BOUND = "BOUND"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# DalMadlulBindingCandidate — the binding carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DalMadlulBindingCandidate:
    """The dal-madlul binding carrier (docs/31 §2).

    Proves that a signifier (DalOnlyCandidate) and a verbal signified
    (VerbalMadlulCandidate) can be formally bound under constitutional
    governance. The binding carries NO semantic content: it is a
    structural proof, never meaning, ifadah, hukm, or reality.

    Fields:
    * ``dal_candidate`` — the proven DalOnlyCandidate from PR-15.
    * ``madlul_candidate`` — the proven VerbalMadlulCandidate from PR-16.
    * ``dal_registry_proof`` — FOUND RegistryLookupResult for DAL_ONLY.
    * ``madlul_registry_proof`` — FOUND RegistryLookupResult for
      VERBAL_MADLUL.
    * ``binding_rank`` — the binding rank, bounded to the ceiling.
    * ``residuals`` — merged residuals from both candidates.
    * ``trace_ref`` — reference, not ledger commit.
    """

    dal_candidate: DalOnlyCandidate
    madlul_candidate: VerbalMadlulCandidate
    dal_registry_proof: RegistryLookupResult
    madlul_registry_proof: RegistryLookupResult
    binding_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.dal_candidate, DalOnlyCandidate):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.dal_candidate must be a "
                "DalOnlyCandidate — binding without a proven signifier "
                f"is ungated ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.madlul_candidate, VerbalMadlulCandidate):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.madlul_candidate must be a "
                "VerbalMadlulCandidate — binding without a proven verbal "
                f"signified is ungated ({FailureCode.GATE_REQUIRED.value})"
            )
        if self.madlul_candidate.dal_only is not self.dal_candidate:
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.madlul_candidate.dal_only must be "
                "the SAME DalOnlyCandidate instance as dal_candidate — "
                f"binding identity mismatch ({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.dal_registry_proof, RegistryLookupResult):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.dal_registry_proof must be a "
                f"RegistryLookupResult ({FailureCode.GATE_REQUIRED.value})"
            )
        if self.dal_registry_proof.state is not RegistryLookupState.FOUND:
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.dal_registry_proof must have "
                f"state FOUND ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if not isinstance(self.madlul_registry_proof, RegistryLookupResult):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.madlul_registry_proof must be a "
                f"RegistryLookupResult ({FailureCode.GATE_REQUIRED.value})"
            )
        if self.madlul_registry_proof.state is not RegistryLookupState.FOUND:
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.madlul_registry_proof must have "
                f"state FOUND ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if not isinstance(self.binding_rank, Rank):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.binding_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.binding_rank > BINDING_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.binding_rank must not exceed "
                f"{BINDING_RANK_CEILING.name} — no rank promotion "
                f"without a gate ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.residuals must be a tuple of "
                f"Residual carriers ({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "DalMadlulBindingCandidate.residuals entries must be "
                    f"Residual carriers ({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalMadlulBindingCandidate.trace_ref must be a non-empty "
                f"string ({FailureCode.TRACE_MISSING.value})"
            )


# ---------------------------------------------------------------------------
# DalMadlulBindingVerdict — the binding proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DalMadlulBindingVerdict:
    """The output of :func:`bind_dal_madlul` (docs/31 §4).

    Proves that a signifier and verbal signified can be formally bound
    under constitutional governance. It does NOT carry meaning,
    reference, ifadah, hukm, reality, or any post-binding content.

    Fields:
    * ``candidate`` — the DalMadlulBindingCandidate (or None on refusal).
    * ``verdict_state`` — BOUND or REFUSED.
    * ``failure_code`` — named FailureCode on refusal, None on success.
    * ``verdict_rank`` — the verdict rank, bounded to the ceiling.
    * ``residuals`` — residuals carried through.
    * ``trace_ref`` — reference, not ledger commit.
    """

    candidate: DalMadlulBindingCandidate | None
    verdict_state: BindingState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.verdict_state, BindingState):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingVerdict.verdict_state must be a "
                "BindingState member"
            )
        if not isinstance(self.verdict_rank, Rank):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingVerdict.verdict_rank must be a Rank member"
            )
        if self.verdict_rank > BINDING_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "DalMadlulBindingVerdict.verdict_rank must not exceed "
                f"BINDING_RANK_CEILING ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalMadlulBindingVerdict.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "DalMadlulBindingVerdict.residuals entries must be "
                    "Residual carriers"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "DalMadlulBindingVerdict.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        # State invariants
        if self.verdict_state is BindingState.BOUND:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a BOUND DalMadlulBindingVerdict must not carry a "
                    "FailureCode (docs/31 §4)"
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "a BOUND DalMadlulBindingVerdict must carry a "
                    "DalMadlulBindingCandidate (docs/31 §4)"
                )
            if not isinstance(self.candidate, DalMadlulBindingCandidate):
                raise WeightCarrierSchemaError(
                    "DalMadlulBindingVerdict.candidate must be a "
                    "DalMadlulBindingCandidate (docs/31 §4)"
                )
        elif self.verdict_state is BindingState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED DalMadlulBindingVerdict must carry a named "
                    "FailureCode (docs/31 §4)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "DalMadlulBindingVerdict.failure_code must be a "
                    "FailureCode member"
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED DalMadlulBindingVerdict must not carry a "
                    "candidate (docs/31 §4)"
                )


# ---------------------------------------------------------------------------
# bind_dal_madlul() — the binding operation
# ---------------------------------------------------------------------------


def bind_dal_madlul(
    dal_candidate: DalOnlyCandidate,
    madlul_candidate: VerbalMadlulCandidate,
    dal_registry: RegistryLookupResult,
    madlul_registry: RegistryLookupResult,
) -> DalMadlulBindingVerdict:
    """Dal-Madlul binding proof — binding candidacy (docs/31).

    A pure function: evaluates whether a DalOnlyCandidate and a
    VerbalMadlulCandidate can be bound, producing a
    :class:`DalMadlulBindingVerdict`.

    Input boundary (docs/31 §3):

    * Accepts ONLY a DalOnlyCandidate and VerbalMadlulCandidate.
    * Requires both RegistryLookupResult instances to have state FOUND.
    * madlul_candidate.dal_only must be the same instance as dal_candidate.
    * Refuses all invalid input combinations with a named FailureCode.

    Output:

    * On success: BOUND with a DalMadlulBindingCandidate.
    * On refusal: REFUSED with a named FailureCode.

    This function is pure: no I/O, no ledger writes, no network.
    """
    # --- Input boundary enforcement: dal_candidate ---
    if not isinstance(dal_candidate, DalOnlyCandidate):
        return DalMadlulBindingVerdict(
            candidate=None,
            verdict_state=BindingState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="bind_dal_madlul/refused/dal_candidate_invalid",
        )

    # --- Input boundary enforcement: madlul_candidate ---
    if not isinstance(madlul_candidate, VerbalMadlulCandidate):
        return DalMadlulBindingVerdict(
            candidate=None,
            verdict_state=BindingState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="bind_dal_madlul/refused/madlul_candidate_invalid",
        )

    # --- Identity match enforcement ---
    if madlul_candidate.dal_only is not dal_candidate:
        return DalMadlulBindingVerdict(
            candidate=None,
            verdict_state=BindingState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="bind_dal_madlul/refused/identity_mismatch",
        )

    # --- Input boundary enforcement: dal_registry ---
    if not isinstance(dal_registry, RegistryLookupResult):
        return DalMadlulBindingVerdict(
            candidate=None,
            verdict_state=BindingState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="bind_dal_madlul/refused/dal_registry_invalid",
        )

    if dal_registry.state is not RegistryLookupState.FOUND:
        return DalMadlulBindingVerdict(
            candidate=None,
            verdict_state=BindingState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="bind_dal_madlul/refused/dal_registry_not_found",
        )

    # --- Input boundary enforcement: madlul_registry ---
    if not isinstance(madlul_registry, RegistryLookupResult):
        return DalMadlulBindingVerdict(
            candidate=None,
            verdict_state=BindingState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="bind_dal_madlul/refused/madlul_registry_invalid",
        )

    if madlul_registry.state is not RegistryLookupState.FOUND:
        return DalMadlulBindingVerdict(
            candidate=None,
            verdict_state=BindingState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="bind_dal_madlul/refused/madlul_registry_not_found",
        )

    # --- Merge residuals from both candidates ---
    merged_residuals = dal_candidate.residuals + madlul_candidate.residuals

    # --- Residual governance ---
    for r in merged_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return DalMadlulBindingVerdict(
                candidate=None,
                verdict_state=BindingState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=merged_residuals,
                trace_ref="bind_dal_madlul/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return DalMadlulBindingVerdict(
                candidate=None,
                verdict_state=BindingState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=merged_residuals,
                trace_ref="bind_dal_madlul/refused/blocking_residual",
            )

    # --- Bound the rank ---
    binding_rank = RankLattice.meet(
        dal_candidate.dal_rank, madlul_candidate.madlul_rank
    )
    binding_rank = RankLattice.meet(binding_rank, BINDING_RANK_CEILING)

    # --- Construct the DalMadlulBindingCandidate ---
    candidate = DalMadlulBindingCandidate(
        dal_candidate=dal_candidate,
        madlul_candidate=madlul_candidate,
        dal_registry_proof=dal_registry,
        madlul_registry_proof=madlul_registry,
        binding_rank=binding_rank,
        residuals=merged_residuals,
        trace_ref=f"bind_dal_madlul/bound/{dal_candidate.signifier_identity}",
    )

    return DalMadlulBindingVerdict(
        candidate=candidate,
        verdict_state=BindingState.BOUND,
        failure_code=None,
        verdict_rank=binding_rank,
        residuals=merged_residuals,
        trace_ref=f"bind_dal_madlul/bound/{dal_candidate.signifier_identity}",
    )


__all__ = [
    "BINDING_RANK_CEILING",
    "BindingState",
    "DalMadlulBindingCandidate",
    "DalMadlulBindingVerdict",
    "bind_dal_madlul",
]
