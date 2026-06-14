"""Mufrad Dalalah Closure — PR-D3.

PR-D3 binding of ``docs/39_MUFRAD_DALALAH_CLOSURE_LAW.md``.

This module proves that the minimum complete singular dalalah is
formally closed as a **candidate** — sufficient for later
HaqiqahAttempt, Majaz, Naql, and composition gates, but never
producing meaning itself.

PR-D3 consumes **all three** proven verdicts:
1. MufradSemanticSlotGeometryVerdict (PROVEN) — SemanticSlotFrame.
2. MaqamContextBoundaryVerdict (PROVEN) — MaqamContextFrame.
3. DalalahCandidateVerdict (PROVEN) — Mutabaqah + Tadammun + Iltizam.

Constitutional invariants:

* MufradDalalahClosureCandidate ≠ Meaning.
* MufradDalalahClosureCandidate ≠ FinalMeaning.
* MufradDalalahClosureCandidate ≠ Ifadah.
* MufradDalalahClosureCandidate ≠ Hukm.
* MufradDalalahClosureCandidate ≠ Tanzil.
* MufradDalalahClosureCandidate ≠ MafhumCandidate.
* MufradDalalahClosureCandidate ≠ MantuqClosure.
* MufradDalalahClosureCandidate ≠ MajazVerdict.
* MufradDalalahClosureCandidate ≠ MajazLicense.
* MufradDalalahClosureCandidate ≠ ManqulVerdict.
* MufradDalalahClosureCandidate ≠ ManqulLicense.
* MufradDalalahClosureCandidate ≠ HaqiqahAttemptVerdict.
* MufradDalalahClosureCandidate ≠ SpeakerIntentVerdict.
* MufradDalalahClosureCandidate ≠ OntologicalClaim.
* MufradDalalahClosureCandidate ≠ FreeReasoning.
* MufradDalalahClosureCandidate ≠ QiyasResult.
* No closure without Mutabaqah + Tadammun + Iltizam.
* No closure without SemanticSlotFrame proven.
* No closure without MaqamContextFrame proven.
* No closure without identity continuity across all layers.
* No closure with hidden or blocking residuals.
* No rank promotion beyond DALALAH_CANDIDATE_RANK_CEILING.
* All operations are pure: no I/O, no ledger, no network.

Deferred residuals (binding):

* MUFRAD_DALALAH_CLOSURE_NOT_MEANING — closure, not meaning.
* HAQIQAH_ATTEMPT_DEFERRED_TO_POST_CLOSURE — haqiqah later.
* MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT — majaz later.
* MANQUL_DEFERRED_UNTIL_TRANSFER_GATE — manqul later.
* IFADAH_DEFERRED_UNTIL_RELATION_CLOSURE — ifadah needs PR-D4.
* HUKM_DEFERRED_UNTIL_IFADAH — hukm later.
* MAFHUM_DEFERRED_UNTIL_MANTUQ — mafhum later.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.dalalah_candidates import (
    DALALAH_CANDIDATE_RANK_CEILING,
    DalalahCandidateState,
    DalalahCandidateVerdict,
    IltizamCandidate,
    MutabaqahCandidate,
    TadammunCandidate,
)
from taaqqul_slot_geometry.weight.maqam_context_boundary import (
    MaqamContextBoundaryVerdict,
    MaqamContextFrame,
    MaqamContextState,
)
from taaqqul_slot_geometry.weight.mufrad_semantic_slot_geometry import (
    MufradSemanticSlotGeometryVerdict,
    MufradSemanticState,
    SemanticSlotFrame,
)

__all__ = [
    "MUFRAD_DALALAH_CLOSURE_RANK_CEILING",
    "MufradDalalahClosureCandidate",
    "MufradDalalahClosureState",
    "MufradDalalahClosureVerdict",
    "prove_mufrad_dalalah_closure",
]

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from dalalah candidate layer
# ---------------------------------------------------------------------------

MUFRAD_DALALAH_CLOSURE_RANK_CEILING: Rank = DALALAH_CANDIDATE_RANK_CEILING

# ---------------------------------------------------------------------------
# MufradDalalahClosureState — verdict outcome
# ---------------------------------------------------------------------------


class MufradDalalahClosureState(StrEnum):
    """The outcome of a prove_mufrad_dalalah_closure() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# MufradDalalahClosureCandidate — minimum complete closure carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MufradDalalahClosureCandidate:
    """Minimum complete mufrad dalalah closure (docs/39 §4.1).

    Proves that a singular Arabic unit has the minimum complete
    dalalah needed for later HaqiqahAttempt and Majaz/Naql gates.

    MufradDalalahClosureCandidate ≠ Meaning.
    MufradDalalahClosureCandidate ≠ Ifadah.
    MufradDalalahClosureCandidate ≠ Hukm.
    """

    semantic_slot_frame_ref: str
    maqam_context_frame_ref: str
    mutabaqah_ref: str
    tadammun_ref: str
    iltizam_ref: str
    dal_identity_ref: str
    closure_scope: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if (
            not isinstance(self.semantic_slot_frame_ref, str)
            or not self.semantic_slot_frame_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "semantic_slot_frame_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.maqam_context_frame_ref, str)
            or not self.maqam_context_frame_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "maqam_context_frame_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.mutabaqah_ref, str) or not self.mutabaqah_ref.strip():
            raise WeightCarrierSchemaError(
                "mutabaqah_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.tadammun_ref, str) or not self.tadammun_ref.strip():
            raise WeightCarrierSchemaError(
                "tadammun_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.iltizam_ref, str) or not self.iltizam_ref.strip():
            raise WeightCarrierSchemaError(
                "iltizam_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.dal_identity_ref, str)
            or not self.dal_identity_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "dal_identity_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.closure_scope, str) or not self.closure_scope.strip():
            raise WeightCarrierSchemaError(
                "closure_scope must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > MUFRAD_DALALAH_CLOSURE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{MUFRAD_DALALAH_CLOSURE_RANK_CEILING.name}",
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
# MufradDalalahClosureVerdict — operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MufradDalalahClosureVerdict:
    """Verdict from prove_mufrad_dalalah_closure() (docs/39 §4.3).

    PROVEN carries a MufradDalalahClosureCandidate.
    REFUSED carries a FailureCode and no candidate.
    """

    candidate: MufradDalalahClosureCandidate | None
    verdict_state: MufradDalalahClosureState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# Deferred residuals builder
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the 7 required deferred residuals (docs/39 §7)."""
    names_and_notes = (
        (
            "MUFRAD_DALALAH_CLOSURE_NOT_MEANING",
            "Closure proves minimum completeness of mufrad dalalah. "
            "It does not determine meaning, ifadah, hukm, or majaz.",
        ),
        (
            "HAQIQAH_ATTEMPT_DEFERRED_TO_POST_CLOSURE",
            "Haqiqah/majaz determination is a post-closure gate "
            "(requires MufradDalalahClosure as input).",
        ),
        (
            "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
            "Majaz license is not issued here. It requires "
            "HaqiqahAttempt gate (post-closure).",
        ),
        (
            "MANQUL_DEFERRED_UNTIL_TRANSFER_GATE",
            "Manqul (transfer) is not issued here. It requires "
            "a dedicated transfer gate (post-closure).",
        ),
        (
            "IFADAH_DEFERRED_UNTIL_RELATION_CLOSURE",
            "Ifadah (proposition) requires RelationClosure (PR-D4) "
            "after MufradDalalahClosure (PR-D3).",
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
# prove_mufrad_dalalah_closure — the pure operation
# ---------------------------------------------------------------------------


def prove_mufrad_dalalah_closure(
    semantic_slot_verdict: MufradSemanticSlotGeometryVerdict,
    maqam_context_verdict: MaqamContextBoundaryVerdict,
    dalalah_candidate_verdict: DalalahCandidateVerdict,
    closure_scope: str,
) -> MufradDalalahClosureVerdict:
    """Prove minimum complete mufrad dalalah closure (docs/39 §5).

    Parameters
    ----------
    semantic_slot_verdict
        PROVEN MufradSemanticSlotGeometryVerdict carrying a SemanticSlotFrame.
    maqam_context_verdict
        PROVEN MaqamContextBoundaryVerdict carrying a MaqamContextFrame.
    dalalah_candidate_verdict
        PROVEN DalalahCandidateVerdict carrying all three candidates.
    closure_scope
        Non-empty scope bounding the closure.

    Returns
    -------
    MufradDalalahClosureVerdict
        PROVEN with a MufradDalalahClosureCandidate on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "prove_mufrad_dalalah_closure"

    # --- Input boundary: semantic_slot_verdict type ---
    if not isinstance(semantic_slot_verdict, MufradSemanticSlotGeometryVerdict):
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_verdict_invalid_type",
        )

    # --- Input boundary: semantic verdict must be PROVEN ---
    if semantic_slot_verdict.verdict_state is not MufradSemanticState.PROVEN:
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_verdict_not_proven",
        )

    # --- Input boundary: semantic candidate must be SemanticSlotFrame ---
    if not isinstance(semantic_slot_verdict.candidate, SemanticSlotFrame):
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_frame_invalid_type",
        )

    # --- Input boundary: maqam_context_verdict type ---
    if not isinstance(maqam_context_verdict, MaqamContextBoundaryVerdict):
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_verdict_invalid_type",
        )

    # --- Input boundary: maqam verdict must be PROVEN ---
    if maqam_context_verdict.verdict_state is not MaqamContextState.PROVEN:
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_verdict_not_proven",
        )

    # --- Input boundary: maqam candidate must be MaqamContextFrame ---
    if not isinstance(maqam_context_verdict.candidate, MaqamContextFrame):
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_frame_invalid_type",
        )

    # --- Input boundary: dalalah_candidate_verdict type ---
    if not isinstance(dalalah_candidate_verdict, DalalahCandidateVerdict):
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/dalalah_verdict_invalid_type",
        )

    # --- Input boundary: dalalah verdict must be PROVEN ---
    if dalalah_candidate_verdict.verdict_state is not DalalahCandidateState.PROVEN:
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/dalalah_verdict_not_proven",
        )

    # --- Input boundary: dalalah verdict has all three candidates ---
    if not isinstance(dalalah_candidate_verdict.mutabaqah, MutabaqahCandidate):
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/mutabaqah_missing",
        )
    if not isinstance(dalalah_candidate_verdict.tadammun, TadammunCandidate):
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/tadammun_missing",
        )
    if not isinstance(dalalah_candidate_verdict.iltizam, IltizamCandidate):
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/iltizam_missing",
        )

    # --- Input boundary: closure_scope ---
    if not isinstance(closure_scope, str) or not closure_scope.strip():
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/closure_scope_empty",
        )

    # --- Extract frame references ---
    slot_frame: SemanticSlotFrame = semantic_slot_verdict.candidate
    maqam_frame: MaqamContextFrame = maqam_context_verdict.candidate
    mutabaqah: MutabaqahCandidate = dalalah_candidate_verdict.mutabaqah
    tadammun: TadammunCandidate = dalalah_candidate_verdict.tadammun
    iltizam: IltizamCandidate = dalalah_candidate_verdict.iltizam

    # --- Identity-continuity: maqam → semantic slot ---
    if maqam_frame.semantic_slot_frame_ref != slot_frame.trace_ref:
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=(
                f"{_trace_base}/refused/"
                "identity_broken/maqam_semantic_frame_mismatch"
            ),
        )

    # --- Identity-continuity: mutabaqah → semantic slot ---
    if mutabaqah.semantic_slot_frame_ref != slot_frame.trace_ref:
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=(
                f"{_trace_base}/refused/"
                "identity_broken/mutabaqah_semantic_frame_mismatch"
            ),
        )

    # --- Identity-continuity: mutabaqah → maqam context ---
    if mutabaqah.maqam_context_frame_ref != maqam_frame.trace_ref:
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=(
                f"{_trace_base}/refused/"
                "identity_broken/mutabaqah_maqam_frame_mismatch"
            ),
        )

    # --- Structural integrity: tadammun → mutabaqah ---
    if tadammun.mutabaqah_ref != mutabaqah.trace_ref:
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=(
                f"{_trace_base}/refused/"
                "identity_broken/tadammun_mutabaqah_mismatch"
            ),
        )

    # --- Structural integrity: iltizam → mutabaqah ---
    if iltizam.mutabaqah_ref != mutabaqah.trace_ref:
        return MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=(
                f"{_trace_base}/refused/"
                "identity_broken/iltizam_mutabaqah_mismatch"
            ),
        )

    # --- Compute rank (meet of CANDIDATE with ceiling) ---
    verdict_rank = RankLattice.meet(
        Rank.CANDIDATE, MUFRAD_DALALAH_CLOSURE_RANK_CEILING
    )

    # --- Build deferred residuals ---
    deferred_residuals = _build_deferred_residuals()

    # --- Check residual governance ---
    for r in deferred_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return MufradDalalahClosureVerdict(
                candidate=None,
                verdict_state=MufradDalalahClosureState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return MufradDalalahClosureVerdict(
                candidate=None,
                verdict_state=MufradDalalahClosureState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- Construct MufradDalalahClosureCandidate ---
    candidate = MufradDalalahClosureCandidate(
        semantic_slot_frame_ref=slot_frame.trace_ref,
        maqam_context_frame_ref=maqam_frame.trace_ref,
        mutabaqah_ref=mutabaqah.trace_ref,
        tadammun_ref=tadammun.trace_ref,
        iltizam_ref=iltizam.trace_ref,
        dal_identity_ref=slot_frame.dal_identity_ref,
        closure_scope=closure_scope,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )

    return MufradDalalahClosureVerdict(
        candidate=candidate,
        verdict_state=MufradDalalahClosureState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )
