"""ContractableUnitGeometry Boundary — PR-18.

PR-18 binding of ``docs/32_CONTRACTABLE_UNIT_GEOMETRY_LAW.md``.
This module introduces:

* :class:`ContractableUnitState` — the two verdict states.
* :class:`ContractabilityProfile` — the affordance profile carrier.
* :class:`ContractableUnitGeometry` — the objecthood carrier.
* :class:`ContractableUnitVerdict` — the objecthood proof.
* :func:`prove_contractable_unit` — the objecthood operation consuming
  only a
  :class:`~taaqqul_slot_geometry.weight.dal_madlul_binding.DalMadlulBindingCandidate`.

Constitutional invariants (docs/32):

* prove_contractable_unit() accepts ONLY a DalMadlulBindingCandidate.
* prove_contractable_unit() refuses all earlier-stage carriers.
* ContractableUnitGeometry is a structural objecthood proof, NOT
  meaning, ifadah, hukm, or reality.
* ContractableUnitGeometry is NOT RelationCandidate.
* ContractabilityProfile is affordance, NOT SyntaxRole.
* No rank promotion beyond CONTRACTABLE_UNIT_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* TraceRef remains a reference, not an audit ledger commit.
* No meaning, no composition, no relation, no extra-letter license.
* No new FailureCode members; no new runtime dependencies.
* prove_contractable_unit() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.dal_madlul_binding import (
    BINDING_RANK_CEILING,
    DalMadlulBindingCandidate,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for PR-18 — same as BINDING_RANK_CEILING.
#: No contractable unit verdict may emit a rank above this value (docs/32 §4).
CONTRACTABLE_UNIT_RANK_CEILING: Rank = BINDING_RANK_CEILING


# ---------------------------------------------------------------------------
# ContractableUnitState — the two verdict states
# ---------------------------------------------------------------------------


class ContractableUnitState(StrEnum):
    """The outcome of a prove_contractable_unit() operation (docs/32 §5)."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# ContractabilityProfile — the affordance profile carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ContractabilityProfile:
    """The contractability profile (docs/32 §2).

    An affordance/profile carrier — it describes what roles the unit
    CAN and CANNOT fill, along with word-class, inflection, and
    derivational affordances. It is NOT a syntactic role assignment.
    It is NOT meaning. It is NOT a grammatical judgment.

    Fields:
    * ``admissible_roles`` — roles the unit can fill (affordance).
    * ``blocked_roles`` — roles the unit cannot fill (constraint).
    * ``path_profile`` — weight-path summary.
    * ``word_class_affordance`` — word-class affordance tag.
    * ``inflection_affordance`` — inflection affordance tag.
    * ``derivational_affordance`` — derivational affordance tag.
    """

    admissible_roles: tuple[str, ...]
    blocked_roles: tuple[str, ...]
    path_profile: str
    word_class_affordance: str
    inflection_affordance: str
    derivational_affordance: str

    def __post_init__(self) -> None:
        if not isinstance(self.admissible_roles, tuple) or not self.admissible_roles:
            raise WeightCarrierSchemaError(
                "ContractabilityProfile.admissible_roles must be a non-empty "
                f"tuple of strings ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        for role in self.admissible_roles:
            if not isinstance(role, str) or not role.strip():
                raise WeightCarrierSchemaError(
                    "ContractabilityProfile.admissible_roles entries must be "
                    f"non-empty strings ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
                )
        if not isinstance(self.blocked_roles, tuple):
            raise WeightCarrierSchemaError(
                "ContractabilityProfile.blocked_roles must be a tuple "
                f"of strings ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        for role in self.blocked_roles:
            if not isinstance(role, str) or not role.strip():
                raise WeightCarrierSchemaError(
                    "ContractabilityProfile.blocked_roles entries must be "
                    f"non-empty strings ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
                )
        if not isinstance(self.path_profile, str) or not self.path_profile.strip():
            raise WeightCarrierSchemaError(
                "ContractabilityProfile.path_profile must be a non-empty "
                f"string ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if (
            not isinstance(self.word_class_affordance, str)
            or not self.word_class_affordance.strip()
        ):
            raise WeightCarrierSchemaError(
                "ContractabilityProfile.word_class_affordance must be a "
                f"non-empty string ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if (
            not isinstance(self.inflection_affordance, str)
            or not self.inflection_affordance.strip()
        ):
            raise WeightCarrierSchemaError(
                "ContractabilityProfile.inflection_affordance must be a "
                f"non-empty string ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if (
            not isinstance(self.derivational_affordance, str)
            or not self.derivational_affordance.strip()
        ):
            raise WeightCarrierSchemaError(
                "ContractabilityProfile.derivational_affordance must be a "
                f"non-empty string ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )


# ---------------------------------------------------------------------------
# ContractableUnitGeometry — the objecthood carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ContractableUnitGeometry:
    """The contractable unit geometry carrier (docs/32 §3).

    Proves that a bound dal-madlul pair (DalMadlulBindingCandidate) can
    stand as a contractable object before any composition. The geometry
    carries NO semantic content: it is a structural proof of objecthood,
    never meaning, ifadah, hukm, or reality.

    Fields:
    * ``binding_candidate`` — the proven DalMadlulBindingCandidate from PR-17.
    * ``unit_identity`` — identity of the contractable unit.
    * ``contractability_profile`` — affordance profile (not syntax role).
    * ``objecthood_rank`` — the objecthood rank, bounded to the ceiling.
    * ``residuals`` — residuals carried from the binding.
    * ``trace_ref`` — reference, not ledger commit.
    """

    binding_candidate: DalMadlulBindingCandidate
    unit_identity: str
    contractability_profile: ContractabilityProfile
    objecthood_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.binding_candidate, DalMadlulBindingCandidate):
            raise WeightCarrierSchemaError(
                "ContractableUnitGeometry.binding_candidate must be a "
                "DalMadlulBindingCandidate — objecthood without a proven "
                f"binding is ungated ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.unit_identity, str) or not self.unit_identity.strip():
            raise WeightCarrierSchemaError(
                "ContractableUnitGeometry.unit_identity must be a non-empty "
                f"string ({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.contractability_profile, ContractabilityProfile):
            raise WeightCarrierSchemaError(
                "ContractableUnitGeometry.contractability_profile must be a "
                f"ContractabilityProfile ({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        if not isinstance(self.objecthood_rank, Rank):
            raise WeightCarrierSchemaError(
                "ContractableUnitGeometry.objecthood_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.objecthood_rank > CONTRACTABLE_UNIT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "ContractableUnitGeometry.objecthood_rank must not exceed "
                f"{CONTRACTABLE_UNIT_RANK_CEILING.name} — no rank promotion "
                f"without a gate ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "ContractableUnitGeometry.residuals must be a tuple of "
                f"Residual carriers ({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "ContractableUnitGeometry.residuals entries must be "
                    f"Residual carriers ({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "ContractableUnitGeometry.trace_ref must be a non-empty "
                f"string ({FailureCode.TRACE_MISSING.value})"
            )


# ---------------------------------------------------------------------------
# ContractableUnitVerdict — the objecthood proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ContractableUnitVerdict:
    """The output of :func:`prove_contractable_unit` (docs/32 §5).

    Proves that a bound dal-madlul pair can stand as a contractable
    object before any composition. It does NOT carry meaning,
    reference, ifadah, hukm, reality, or any post-objecthood content.

    Fields:
    * ``candidate`` — the ContractableUnitGeometry (or None on refusal).
    * ``verdict_state`` — PROVEN or REFUSED.
    * ``failure_code`` — named FailureCode on refusal, None on success.
    * ``verdict_rank`` — the verdict rank, bounded to the ceiling.
    * ``residuals`` — residuals carried through.
    * ``trace_ref`` — reference, not ledger commit.
    """

    candidate: ContractableUnitGeometry | None
    verdict_state: ContractableUnitState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.verdict_state, ContractableUnitState):
            raise WeightCarrierSchemaError(
                "ContractableUnitVerdict.verdict_state must be a "
                "ContractableUnitState member"
            )
        if not isinstance(self.verdict_rank, Rank):
            raise WeightCarrierSchemaError(
                "ContractableUnitVerdict.verdict_rank must be a Rank member"
            )
        if self.verdict_rank > CONTRACTABLE_UNIT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "ContractableUnitVerdict.verdict_rank must not exceed "
                f"CONTRACTABLE_UNIT_RANK_CEILING ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "ContractableUnitVerdict.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "ContractableUnitVerdict.residuals entries must be "
                    "Residual carriers"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "ContractableUnitVerdict.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        # State invariants
        if self.verdict_state is ContractableUnitState.PROVEN:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a PROVEN ContractableUnitVerdict must not carry a "
                    "FailureCode (docs/32 §5)"
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "a PROVEN ContractableUnitVerdict must carry a "
                    "ContractableUnitGeometry (docs/32 §5)"
                )
            if not isinstance(self.candidate, ContractableUnitGeometry):
                raise WeightCarrierSchemaError(
                    "ContractableUnitVerdict.candidate must be a "
                    "ContractableUnitGeometry (docs/32 §5)"
                )
        elif self.verdict_state is ContractableUnitState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED ContractableUnitVerdict must carry a named "
                    "FailureCode (docs/32 §5)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "ContractableUnitVerdict.failure_code must be a "
                    "FailureCode member"
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED ContractableUnitVerdict must not carry a "
                    "candidate (docs/32 §5)"
                )


# ---------------------------------------------------------------------------
# prove_contractable_unit() — the objecthood operation
# ---------------------------------------------------------------------------


def prove_contractable_unit(
    binding_candidate: DalMadlulBindingCandidate,
    admissible_roles: tuple[str, ...],
    blocked_roles: tuple[str, ...],
    path_profile: str,
    word_class_affordance: str,
    inflection_affordance: str,
    derivational_affordance: str,
) -> ContractableUnitVerdict:
    """Contractable unit objecthood proof — objecthood candidacy (docs/32).

    A pure function: evaluates whether a DalMadlulBindingCandidate can
    stand as a contractable object, producing a
    :class:`ContractableUnitVerdict`.

    Input boundary (docs/32 §4):

    * Accepts ONLY a DalMadlulBindingCandidate.
    * Requires non-empty admissible_roles, path_profile,
      word_class_affordance, inflection_affordance,
      derivational_affordance.
    * Refuses all invalid input combinations with a named FailureCode.

    Output:

    * On success: PROVEN with a ContractableUnitGeometry.
    * On refusal: REFUSED with a named FailureCode.

    This function is pure: no I/O, no ledger writes, no network.
    """
    # --- Input boundary enforcement: binding_candidate ---
    if not isinstance(binding_candidate, DalMadlulBindingCandidate):
        return ContractableUnitVerdict(
            candidate=None,
            verdict_state=ContractableUnitState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_contractable_unit/refused/binding_candidate_invalid",
        )

    # --- Input boundary enforcement: admissible_roles ---
    if not isinstance(admissible_roles, tuple) or not admissible_roles:
        return ContractableUnitVerdict(
            candidate=None,
            verdict_state=ContractableUnitState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_contractable_unit/refused/admissible_roles_empty",
        )
    for role in admissible_roles:
        if not isinstance(role, str) or not role.strip():
            return ContractableUnitVerdict(
                candidate=None,
                verdict_state=ContractableUnitState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="prove_contractable_unit/refused/admissible_role_invalid",
            )

    # --- Input boundary enforcement: blocked_roles ---
    if not isinstance(blocked_roles, tuple):
        return ContractableUnitVerdict(
            candidate=None,
            verdict_state=ContractableUnitState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_contractable_unit/refused/blocked_roles_invalid",
        )
    for role in blocked_roles:
        if not isinstance(role, str) or not role.strip():
            return ContractableUnitVerdict(
                candidate=None,
                verdict_state=ContractableUnitState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref=(
                    "prove_contractable_unit/refused/"
                    "blocked_role_invalid"
                ),
            )

    # --- Input boundary enforcement: path_profile ---
    if not isinstance(path_profile, str) or not path_profile.strip():
        return ContractableUnitVerdict(
            candidate=None,
            verdict_state=ContractableUnitState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_contractable_unit/refused/path_profile_empty",
        )

    # --- Input boundary enforcement: word_class_affordance ---
    if not isinstance(word_class_affordance, str) or not word_class_affordance.strip():
        return ContractableUnitVerdict(
            candidate=None,
            verdict_state=ContractableUnitState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_contractable_unit/refused/word_class_affordance_empty",
        )

    # --- Input boundary enforcement: inflection_affordance ---
    if not isinstance(inflection_affordance, str) or not inflection_affordance.strip():
        return ContractableUnitVerdict(
            candidate=None,
            verdict_state=ContractableUnitState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_contractable_unit/refused/inflection_affordance_empty",
        )

    # --- Input boundary enforcement: derivational_affordance ---
    if not isinstance(derivational_affordance, str) or not derivational_affordance.strip():
        return ContractableUnitVerdict(
            candidate=None,
            verdict_state=ContractableUnitState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_contractable_unit/refused/derivational_affordance_empty",
        )

    # --- Carry residuals from binding candidate ---
    carried_residuals = binding_candidate.residuals

    # --- Residual governance ---
    for r in carried_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return ContractableUnitVerdict(
                candidate=None,
                verdict_state=ContractableUnitState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=carried_residuals,
                trace_ref="prove_contractable_unit/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return ContractableUnitVerdict(
                candidate=None,
                verdict_state=ContractableUnitState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=carried_residuals,
                trace_ref="prove_contractable_unit/refused/blocking_residual",
            )

    # --- Bound the rank ---
    objecthood_rank = RankLattice.meet(
        binding_candidate.binding_rank, CONTRACTABLE_UNIT_RANK_CEILING
    )

    # --- Construct the ContractabilityProfile ---
    profile = ContractabilityProfile(
        admissible_roles=admissible_roles,
        blocked_roles=blocked_roles,
        path_profile=path_profile,
        word_class_affordance=word_class_affordance,
        inflection_affordance=inflection_affordance,
        derivational_affordance=derivational_affordance,
    )

    # --- Construct the ContractableUnitGeometry ---
    unit_identity = binding_candidate.dal_candidate.signifier_identity
    candidate = ContractableUnitGeometry(
        binding_candidate=binding_candidate,
        unit_identity=unit_identity,
        contractability_profile=profile,
        objecthood_rank=objecthood_rank,
        residuals=carried_residuals,
        trace_ref=f"prove_contractable_unit/proven/{unit_identity}",
    )

    return ContractableUnitVerdict(
        candidate=candidate,
        verdict_state=ContractableUnitState.PROVEN,
        failure_code=None,
        verdict_rank=objecthood_rank,
        residuals=carried_residuals,
        trace_ref=f"prove_contractable_unit/proven/{unit_identity}",
    )


__all__ = [
    "CONTRACTABLE_UNIT_RANK_CEILING",
    "ContractabilityProfile",
    "ContractableUnitGeometry",
    "ContractableUnitState",
    "ContractableUnitVerdict",
    "prove_contractable_unit",
]
