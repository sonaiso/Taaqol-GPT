"""Relation Closure — PR-D4.

PR-D4 binding of ``docs/40_RELATION_CLOSURE_LAW.md``.

This module proves that a relation between two units whose singular
dalalah is formally closed (MufradDalalahClosure) can itself be
closed as a **candidate** — sufficient for later IfadahCandidate
(PR-20) gates, but never producing meaning itself.

PR-D4 consumes:
1. Two MufradDalalahClosureVerdict instances (both PROVEN).
2. A RelationType identifying the minimal relation.
3. A relation_maqam bounding the relation contextually.
4. A relation_evidence string (non-empty evidence basis).

Constitutional invariants:

* RelationClosureCandidate ≠ Meaning.
* RelationClosureCandidate ≠ FinalMeaning.
* RelationClosureCandidate ≠ Ifadah.
* RelationClosureCandidate ≠ Hukm.
* RelationClosureCandidate ≠ Tanzil.
* RelationClosureCandidate ≠ MafhumCandidate.
* RelationClosureCandidate ≠ MantuqClosure.
* RelationClosureCandidate ≠ MajazVerdict.
* RelationClosureCandidate ≠ HaqiqahAttemptVerdict.
* RelationClosureCandidate ≠ OntologicalClaim.
* RelationClosureCandidate ≠ FreeReasoning.
* No relation closure without two PROVEN MufradDalalahClosureVerdicts.
* No relation closure without RelationType.
* No relation closure without relation_maqam.
* No relation closure with hidden or blocking residuals.
* No rank promotion beyond RELATION_CLOSURE_RANK_CEILING.
* All operations are pure: no I/O, no ledger, no network.

Deferred residuals (binding):

* RELATION_CLOSURE_NOT_MEANING — closure, not meaning.
* IFADAH_DEFERRED_UNTIL_SPEECH_FORCE — ifadah needs speech force.
* HUKM_DEFERRED_UNTIL_IFADAH — hukm needs ifadah.
* MAFHUM_DEFERRED_UNTIL_MANTUQ — mafhum needs mantuq.
* HAQIQAH_MAJAZ_DEFERRED_TO_POST_RELATION — haqiqah/majaz later.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.mufrad_dalalah_closure import (
    MUFRAD_DALALAH_CLOSURE_RANK_CEILING,
    MufradDalalahClosureCandidate,
    MufradDalalahClosureState,
    MufradDalalahClosureVerdict,
)

__all__ = [
    "RELATION_CLOSURE_RANK_CEILING",
    "RelationClosureCandidate",
    "RelationClosureState",
    "RelationClosureVerdict",
    "RelationType",
    "prove_relation_closure",
]

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from mufrad dalalah closure layer
# ---------------------------------------------------------------------------

RELATION_CLOSURE_RANK_CEILING: Rank = MUFRAD_DALALAH_CLOSURE_RANK_CEILING

# ---------------------------------------------------------------------------
# RelationType — minimal relation kinds (docs/40 §2)
# ---------------------------------------------------------------------------


class RelationType(StrEnum):
    """Minimal relation types for PR-D4 (docs/40 §2).

    Only the minimum set needed to close a relation between
    two mufrad dalalah units. Extended in later PRs.
    """

    PREDICATIVE = "PREDICATIVE"
    RESTRICTIVE = "RESTRICTIVE"
    INCLUSION = "INCLUSION"
    REFERENCE = "REFERENCE"
    OPERATOR = "OPERATOR"


# ---------------------------------------------------------------------------
# RelationClosureState — verdict outcome
# ---------------------------------------------------------------------------


class RelationClosureState(StrEnum):
    """The outcome of a prove_relation_closure() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# RelationClosureCandidate — the relation closure carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RelationClosureCandidate:
    """Relation closure carrier (docs/40 §4).

    Proves that a relation between two mufrad-dalalah-closed units
    is formally closed. The candidate carries NO semantic content:
    it is a structural proof of relation closure, never meaning,
    ifadah, hukm, or reality.

    RelationClosureCandidate ≠ Meaning.
    RelationClosureCandidate ≠ Ifadah.
    RelationClosureCandidate ≠ Hukm.
    """

    first_closure_ref: str
    second_closure_ref: str
    first_dal_identity_ref: str
    second_dal_identity_ref: str
    relation_type: RelationType
    relation_maqam: str
    relation_evidence: str
    closure_scope: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if (
            not isinstance(self.first_closure_ref, str)
            or not self.first_closure_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "first_closure_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.second_closure_ref, str)
            or not self.second_closure_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "second_closure_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.first_dal_identity_ref, str)
            or not self.first_dal_identity_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "first_dal_identity_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.second_dal_identity_ref, str)
            or not self.second_dal_identity_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "second_dal_identity_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.relation_type, RelationType):
            raise WeightCarrierSchemaError(
                f"relation_type must be a RelationType member, got "
                f"{type(self.relation_type).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.relation_maqam, str)
            or not self.relation_maqam.strip()
        ):
            raise WeightCarrierSchemaError(
                "relation_maqam must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.relation_evidence, str)
            or not self.relation_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "relation_evidence must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.closure_scope, str)
            or not self.closure_scope.strip()
        ):
            raise WeightCarrierSchemaError(
                "closure_scope must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > RELATION_CLOSURE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{RELATION_CLOSURE_RANK_CEILING.name}",
                FailureCode.RANK_EXCEEDS_CEILING,
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "residuals must be a tuple",
                FailureCode.HIDDEN_RESIDUAL,
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    f"each residual must be a Residual instance, "
                    f"got {type(r).__name__}",
                    FailureCode.HIDDEN_RESIDUAL,
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# RelationClosureVerdict — operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RelationClosureVerdict:
    """Verdict from prove_relation_closure() (docs/40 §5).

    PROVEN carries a RelationClosureCandidate.
    REFUSED carries a FailureCode and no candidate.
    """

    candidate: RelationClosureCandidate | None
    verdict_state: RelationClosureState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# Deferred residuals builder
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the 5 required deferred residuals (docs/40 §7)."""
    names_and_notes = (
        (
            "RELATION_CLOSURE_NOT_MEANING",
            "Relation closure proves formal closure of a relation "
            "between two mufrad dalalah units. It does not determine "
            "meaning, ifadah, hukm, or reality.",
        ),
        (
            "IFADAH_DEFERRED_UNTIL_SPEECH_FORCE",
            "Ifadah (proposition) requires SpeechForce boundary "
            "after RelationClosure (PR-D4). No ifadah here.",
        ),
        (
            "HUKM_DEFERRED_UNTIL_IFADAH",
            "Hukm (judgment) requires Ifadah first. "
            "No hukm before proposition.",
        ),
        (
            "MAFHUM_DEFERRED_UNTIL_MANTUQ",
            "Mafhum (concept extraction) requires Mantuq first. "
            "No mafhum before explicit meaning.",
        ),
        (
            "HAQIQAH_MAJAZ_DEFERRED_TO_POST_RELATION",
            "Haqiqah/majaz determination is a post-relation gate "
            "(may apply to individual units or the relation as a whole).",
        ),
    )
    return tuple(
        Residual(
            name=name,
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=note,
        )
        for name, note in names_and_notes
    )


# ---------------------------------------------------------------------------
# prove_relation_closure — the pure operation
# ---------------------------------------------------------------------------


def prove_relation_closure(
    first_verdict: MufradDalalahClosureVerdict,
    second_verdict: MufradDalalahClosureVerdict,
    relation_type: RelationType,
    relation_maqam: str,
    relation_evidence: str,
    closure_scope: str,
) -> RelationClosureVerdict:
    """Prove relation closure between two mufrad-dalalah-closed units.

    Parameters
    ----------
    first_verdict
        PROVEN MufradDalalahClosureVerdict for the first unit.
    second_verdict
        PROVEN MufradDalalahClosureVerdict for the second unit.
    relation_type
        The minimal relation type binding the two units.
    relation_maqam
        Non-empty maqam bounding the relation context.
    relation_evidence
        Non-empty evidence string supporting the relation.
    closure_scope
        Non-empty scope bounding the closure.

    Returns
    -------
    RelationClosureVerdict
        PROVEN with a RelationClosureCandidate on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "prove_relation_closure"

    # --- Input boundary: first_verdict type ---
    if not isinstance(first_verdict, MufradDalalahClosureVerdict):
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/first_verdict_invalid_type",
        )

    # --- Input boundary: first verdict must be PROVEN ---
    if first_verdict.verdict_state is not MufradDalalahClosureState.PROVEN:
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/first_verdict_not_proven",
        )

    # --- Input boundary: first candidate must be present ---
    if not isinstance(first_verdict.candidate, MufradDalalahClosureCandidate):
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/first_candidate_invalid",
        )

    # --- Input boundary: second_verdict type ---
    if not isinstance(second_verdict, MufradDalalahClosureVerdict):
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/second_verdict_invalid_type",
        )

    # --- Input boundary: second verdict must be PROVEN ---
    if second_verdict.verdict_state is not MufradDalalahClosureState.PROVEN:
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/second_verdict_not_proven",
        )

    # --- Input boundary: second candidate must be present ---
    if not isinstance(second_verdict.candidate, MufradDalalahClosureCandidate):
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/second_candidate_invalid",
        )

    # --- Input boundary: relation_type ---
    if not isinstance(relation_type, RelationType):
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/relation_type_invalid",
        )

    # --- Input boundary: relation_maqam ---
    if not isinstance(relation_maqam, str) or not relation_maqam.strip():
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/relation_maqam_empty",
        )

    # --- Input boundary: relation_evidence ---
    if not isinstance(relation_evidence, str) or not relation_evidence.strip():
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/relation_evidence_empty",
        )

    # --- Input boundary: closure_scope ---
    if not isinstance(closure_scope, str) or not closure_scope.strip():
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/closure_scope_empty",
        )

    # --- Identity distinctness: two different units ---
    first_candidate: MufradDalalahClosureCandidate = first_verdict.candidate
    second_candidate: MufradDalalahClosureCandidate = second_verdict.candidate

    if first_candidate.dal_identity_ref == second_candidate.dal_identity_ref:
        return RelationClosureVerdict(
            candidate=None,
            verdict_state=RelationClosureState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/same_dal_identity",
        )

    # --- Compute rank (meet of both candidate ranks with ceiling) ---
    verdict_rank = RankLattice.meet(
        first_candidate.rank,
        second_candidate.rank,
        RELATION_CLOSURE_RANK_CEILING,
    )

    # --- Build deferred residuals ---
    deferred_residuals = _build_deferred_residuals()

    # --- Check residual governance ---
    for r in deferred_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return RelationClosureVerdict(
                candidate=None,
                verdict_state=RelationClosureState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return RelationClosureVerdict(
                candidate=None,
                verdict_state=RelationClosureState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- Construct RelationClosureCandidate ---
    candidate = RelationClosureCandidate(
        first_closure_ref=first_candidate.trace_ref,
        second_closure_ref=second_candidate.trace_ref,
        first_dal_identity_ref=first_candidate.dal_identity_ref,
        second_dal_identity_ref=second_candidate.dal_identity_ref,
        relation_type=relation_type,
        relation_maqam=relation_maqam,
        relation_evidence=relation_evidence,
        closure_scope=closure_scope,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )

    return RelationClosureVerdict(
        candidate=candidate,
        verdict_state=RelationClosureState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )
