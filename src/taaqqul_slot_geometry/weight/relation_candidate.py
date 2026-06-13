"""RelationCandidate Boundary — PR-19.

PR-19 binding of ``docs/33_RELATION_CANDIDATE_BOUNDARY_LAW.md``.
This module introduces:

* :class:`RelationState` — the two verdict states.
* :class:`RelationCandidate` — the composition/relation affordance carrier.
* :class:`RelationVerdict` — the composition proof.
* :func:`prove_relation_candidate` — the composition operation consuming
  only :class:`~taaqqul_slot_geometry.weight.contractable_unit_geometry.ContractableUnitGeometry`
  instances.

Constitutional invariants (docs/33):

* prove_relation_candidate() accepts ONLY ContractableUnitGeometry inputs.
* prove_relation_candidate() refuses all earlier-stage carriers.
* RelationCandidate is relation affordance as candidate, NOT meaning,
  ifadah, hukm, or reality.
* RelationCandidate ≠ IfadahCandidate.
* ContractabilityProfile strings are affordance labels only —
  RelationCandidate must re-gate admissible_roles.
* No rank promotion beyond RELATION_CANDIDATE_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* TraceRef remains a reference, not an audit ledger commit.
* No meaning, no dalālah, no ifadah, no hukm, no reality.
* No new FailureCode members; no new runtime dependencies.
* prove_relation_candidate() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.contractable_unit_geometry import (
    CONTRACTABLE_UNIT_RANK_CEILING,
    ContractableUnitGeometry,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for PR-19 — same as CONTRACTABLE_UNIT_RANK_CEILING.
#: No relation verdict may emit a rank above this value (docs/33 §4).
RELATION_CANDIDATE_RANK_CEILING: Rank = CONTRACTABLE_UNIT_RANK_CEILING


# ---------------------------------------------------------------------------
# RelationState — the two verdict states
# ---------------------------------------------------------------------------


class RelationState(StrEnum):
    """The outcome of a prove_relation_candidate() operation (docs/33 §5)."""

    COMPOSED = "COMPOSED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# RelationCandidate — the composition/relation affordance carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RelationCandidate:
    """The relation candidate carrier (docs/33 §3).

    Proves that two contractable units (ContractableUnitGeometry) can
    stand in a governed relation — that is, they possess the geometric
    standing to compose. The relation candidate carries NO semantic
    content: it is a structural proof of relation affordance, never
    meaning, ifadah, hukm, or reality.

    The governor_role and dependent_role fields are RE-GATED at relation
    time. They are affordance labels from ContractabilityProfile, NOT
    final syntax role assignments. RelationCandidate does not promote
    them to SyntaxRole status.
    """

    governor: ContractableUnitGeometry
    dependent: ContractableUnitGeometry
    relation_basis: str
    governor_role: str
    dependent_role: str
    relation_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- governor ---
        if not isinstance(self.governor, ContractableUnitGeometry):
            raise WeightCarrierSchemaError(
                f"governor must be ContractableUnitGeometry, got "
                f"{type(self.governor).__name__}",
                FailureCode.GATE_REQUIRED,
            )
        # --- dependent ---
        if not isinstance(self.dependent, ContractableUnitGeometry):
            raise WeightCarrierSchemaError(
                f"dependent must be ContractableUnitGeometry, got "
                f"{type(self.dependent).__name__}",
                FailureCode.GATE_REQUIRED,
            )
        # --- relation_basis ---
        if not isinstance(self.relation_basis, str) or not self.relation_basis.strip():
            raise WeightCarrierSchemaError(
                "relation_basis must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- governor_role ---
        if not isinstance(self.governor_role, str) or not self.governor_role.strip():
            raise WeightCarrierSchemaError(
                "governor_role must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- dependent_role ---
        if not isinstance(self.dependent_role, str) or not self.dependent_role.strip():
            raise WeightCarrierSchemaError(
                "dependent_role must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- relation_rank ---
        if not isinstance(self.relation_rank, Rank):
            raise WeightCarrierSchemaError(
                f"relation_rank must be a Rank member, got "
                f"{type(self.relation_rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.relation_rank > RELATION_CANDIDATE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"relation_rank {self.relation_rank.name} exceeds ceiling "
                f"{RELATION_CANDIDATE_RANK_CEILING.name}",
                FailureCode.RANK_EXCEEDS_CEILING,
            )
        # --- residuals ---
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "residuals must be a tuple",
                FailureCode.HIDDEN_RESIDUAL,
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    f"each residual must be a Residual instance, got "
                    f"{type(r).__name__}",
                    FailureCode.HIDDEN_RESIDUAL,
                )
        # --- trace_ref ---
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# RelationVerdict — the composition proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RelationVerdict:
    """The output of :func:`prove_relation_candidate` (docs/33 §5).

    Proves that two contractable units can stand in a governed relation.
    It does NOT carry meaning, ifadah, hukm, reality, or any
    post-relation content.
    """

    candidate: RelationCandidate | None
    verdict_state: RelationState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, RelationState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be RelationState, got "
                f"{type(self.verdict_state).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- verdict_rank type and ceiling ---
        if not isinstance(self.verdict_rank, Rank):
            raise WeightCarrierSchemaError(
                f"verdict_rank must be a Rank member, got "
                f"{type(self.verdict_rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.verdict_rank > RELATION_CANDIDATE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"verdict_rank {self.verdict_rank.name} exceeds ceiling "
                f"{RELATION_CANDIDATE_RANK_CEILING.name}",
                FailureCode.RANK_EXCEEDS_CEILING,
            )
        # --- residuals ---
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "residuals must be a tuple",
                FailureCode.HIDDEN_RESIDUAL,
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    f"each residual must be a Residual instance, got "
                    f"{type(r).__name__}",
                    FailureCode.HIDDEN_RESIDUAL,
                )
        # --- trace_ref ---
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )
        # --- State invariants ---
        if self.verdict_state is RelationState.COMPOSED:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "COMPOSED verdict must have failure_code=None",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "COMPOSED verdict must have a RelationCandidate",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if not isinstance(self.candidate, RelationCandidate):
                raise WeightCarrierSchemaError(
                    f"COMPOSED candidate must be RelationCandidate, got "
                    f"{type(self.candidate).__name__}",
                    FailureCode.GATE_REQUIRED,
                )
        elif self.verdict_state is RelationState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "REFUSED verdict must have a named FailureCode",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    f"failure_code must be a FailureCode member, got "
                    f"{type(self.failure_code).__name__}",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "REFUSED verdict must have candidate=None",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )


# ---------------------------------------------------------------------------
# prove_relation_candidate() — the composition operation
# ---------------------------------------------------------------------------


def prove_relation_candidate(
    governor: ContractableUnitGeometry,
    dependent: ContractableUnitGeometry,
    relation_basis: str,
    governor_role_claim: str,
    dependent_role_claim: str,
) -> RelationVerdict:
    """Prove relation candidacy from two contractable units (docs/33 §4).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    Parameters
    ----------
    governor : ContractableUnitGeometry
        The governing unit (proven objecthood from PR-18).
    dependent : ContractableUnitGeometry
        The governed unit (proven objecthood from PR-18).
    relation_basis : str
        Non-empty string describing the compositional basis/evidence.
    governor_role_claim : str
        The role claimed for the governor; must be admissible and not blocked.
    dependent_role_claim : str
        The role claimed for the dependent; must be admissible and not blocked.

    Returns
    -------
    RelationVerdict
        COMPOSED with a RelationCandidate on success; REFUSED with a
        named FailureCode on any violation.
    """
    # --- Input boundary: governor type ---
    if not isinstance(governor, ContractableUnitGeometry):
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/governor_not_geometry",
        )

    # --- Input boundary: dependent type ---
    if not isinstance(dependent, ContractableUnitGeometry):
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/dependent_not_geometry",
        )

    # --- Input boundary: relation_basis ---
    if not isinstance(relation_basis, str) or not relation_basis.strip():
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/relation_basis_empty",
        )

    # --- Input boundary: governor_role_claim ---
    if not isinstance(governor_role_claim, str) or not governor_role_claim.strip():
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/governor_role_claim_empty",
        )

    # --- Input boundary: dependent_role_claim ---
    if not isinstance(dependent_role_claim, str) or not dependent_role_claim.strip():
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/dependent_role_claim_empty",
        )

    # --- Role re-gating: governor_role_claim admissibility ---
    gov_profile = governor.contractability_profile
    if governor_role_claim not in gov_profile.admissible_roles:
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/governor_role_not_admissible",
        )
    if governor_role_claim in gov_profile.blocked_roles:
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/governor_role_blocked",
        )

    # --- Role re-gating: dependent_role_claim admissibility ---
    dep_profile = dependent.contractability_profile
    if dependent_role_claim not in dep_profile.admissible_roles:
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/dependent_role_not_admissible",
        )
    if dependent_role_claim in dep_profile.blocked_roles:
        return RelationVerdict(
            candidate=None,
            verdict_state=RelationState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_relation_candidate/refused/dependent_role_blocked",
        )

    # --- Residual governance: merge from both units ---
    merged_residuals = governor.residuals + dependent.residuals

    for r in merged_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return RelationVerdict(
                candidate=None,
                verdict_state=RelationState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=merged_residuals,
                trace_ref="prove_relation_candidate/refused/hidden_forbidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return RelationVerdict(
                candidate=None,
                verdict_state=RelationState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=merged_residuals,
                trace_ref="prove_relation_candidate/refused/blocking_residual",
            )

    # --- Rank bounding via lattice meet ---
    relation_rank = RankLattice.meet(
        governor.objecthood_rank,
        dependent.objecthood_rank,
        RELATION_CANDIDATE_RANK_CEILING,
    )

    # --- Construct the RelationCandidate ---
    gov_id = governor.unit_identity
    dep_id = dependent.unit_identity

    candidate = RelationCandidate(
        governor=governor,
        dependent=dependent,
        relation_basis=relation_basis,
        governor_role=governor_role_claim,
        dependent_role=dependent_role_claim,
        relation_rank=relation_rank,
        residuals=merged_residuals,
        trace_ref=f"prove_relation_candidate/composed/{gov_id}+{dep_id}",
    )

    return RelationVerdict(
        candidate=candidate,
        verdict_state=RelationState.COMPOSED,
        failure_code=None,
        verdict_rank=relation_rank,
        residuals=merged_residuals,
        trace_ref=f"prove_relation_candidate/composed/{gov_id}+{dep_id}",
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "RELATION_CANDIDATE_RANK_CEILING",
    "RelationCandidate",
    "RelationState",
    "RelationVerdict",
    "prove_relation_candidate",
]
