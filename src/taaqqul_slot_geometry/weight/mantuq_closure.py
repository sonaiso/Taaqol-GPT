"""ManṭūqClosure — PV-A2.

PV-A2 binding of ``docs/48_MANTUQ_BOUNDARY_LAW.md``.

This module proves that a PROVEN IfadahVerdict, combined with a PROVEN
MaqamContextBoundaryVerdict and a preserved speech-origin boundary,
carries a **mantuq closure candidate** — proof that the explicit
spoken/textual origin has been preserved. It does not determine mafhum,
does not determine majaz, does not determine haqiqah, and does not
determine naql.

PV-A2 consumes:
1. A PROVEN IfadahVerdict (PR-20).
2. A PROVEN MaqamContextBoundaryVerdict (PR-D1.2).
3. mantuq_scope (non-empty).
4. spoken_surface_ref (non-empty).
5. mantuq_evidence (non-empty).
6. closure_scope (non-empty).

Constitutional invariants (docs/48 §1, §4):

* MantuqClosureCandidate ≠ MafhumCandidate.
* MantuqClosureCandidate ≠ MajazVerdict.
* MantuqClosureCandidate ≠ MajazLicense.
* MantuqClosureCandidate ≠ ManqulVerdict.
* MantuqClosureCandidate ≠ HaqiqahAttempt.
* MantuqClosureCandidate ≠ ReferenceExpansion.
* MantuqClosureCandidate ≠ GPTProposer.
* MantuqClosureCandidate ≠ GovernmentServiceEngine.
* MantuqClosureCandidate ≠ ArabicConditionsDAG.
* MantuqClosureCandidate ≠ Certificate.
* No mantuq closure without a PROVEN IfadahVerdict.
* No mantuq closure without a PROVEN MaqamContextBoundaryVerdict.
* No mantuq closure with hidden or blocking residuals.
* No rank promotion beyond MANTUQ_RANK_CEILING.
* All operations are pure: no I/O, no ledger, no network, no clock.

Deferred residuals (docs/48 §5):

* MAFHUM_NOT_YET_OPENED — Mafhum deferred until PV-A3/PV-A4.
* MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT — Majaz deferred.
* HAQIQAH_ATTEMPT_DEFERRED — Haqiqah attempt deferred.
* NAQL_DEFERRED_UNTIL_TRANSFER_GATE — Naql deferred.
* MANTUQ_NOT_MAFHUM — Mantuq is the origin, not the branch.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.ifadah_candidate import (
    IfadahCandidate,
    IfadahState,
    IfadahVerdict,
)
from taaqqul_slot_geometry.weight.maqam_context_boundary import (
    MaqamContextBoundaryVerdict,
    MaqamContextState,
)
from taaqqul_slot_geometry.weight.tanzil_candidate import TANZIL_RANK_CEILING

__all__ = [
    "MANTUQ_RANK_CEILING",
    "MantuqClosureCandidate",
    "MantuqClosureState",
    "MantuqClosureVerdict",
    "prove_mantuq_closure",
]

# ---------------------------------------------------------------------------
# Rank ceiling — bounded by the vertical path ceiling (docs/48 §5)
# ---------------------------------------------------------------------------

MANTUQ_RANK_CEILING: Rank = TANZIL_RANK_CEILING

# ---------------------------------------------------------------------------
# MantuqClosureState — verdict outcome
# ---------------------------------------------------------------------------


class MantuqClosureState(StrEnum):
    """The outcome of a prove_mantuq_closure() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# MantuqClosureCandidate — the mantuq closure carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MantuqClosureCandidate:
    """Mantuq closure candidate carrier (docs/48 §1, §7).

    Proves that a PROVEN IfadahCandidate has a preserved spoken/textual
    origin — the explicit indication that stands before any implied
    meaning (mafhum), any figurative transfer (majaz), or any
    terminological transfer (naql).

    MantuqClosureCandidate ≠ MafhumCandidate.
    MantuqClosureCandidate ≠ MajazVerdict.
    MantuqClosureCandidate ≠ HaqiqahAttempt.
    MantuqClosureCandidate ≠ Certificate.
    """

    ifadah_verdict_ref: str
    maqam_verdict_ref: str
    mantuq_scope: str
    spoken_surface_ref: str
    mantuq_evidence: str
    closure_scope: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if (
            not isinstance(self.ifadah_verdict_ref, str)
            or not self.ifadah_verdict_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "ifadah_verdict_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.maqam_verdict_ref, str)
            or not self.maqam_verdict_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "maqam_verdict_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.mantuq_scope, str)
            or not self.mantuq_scope.strip()
        ):
            raise WeightCarrierSchemaError(
                "mantuq_scope must be a non-empty string",
                FailureCode.NO_MANTUQ_SCOPE,
            )
        if (
            not isinstance(self.spoken_surface_ref, str)
            or not self.spoken_surface_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "spoken_surface_ref must be a non-empty string",
                FailureCode.NO_SPOKEN_SURFACE,
            )
        if (
            not isinstance(self.mantuq_evidence, str)
            or not self.mantuq_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "mantuq_evidence must be a non-empty string",
                FailureCode.NO_MANTUQ_EVIDENCE,
            )
        if (
            not isinstance(self.closure_scope, str)
            or not self.closure_scope.strip()
        ):
            raise WeightCarrierSchemaError(
                "closure_scope must be a non-empty string",
                FailureCode.NO_MANTUQ_CLOSURE_SCOPE,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > MANTUQ_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{MANTUQ_RANK_CEILING.name}",
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
# MantuqClosureVerdict — operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MantuqClosureVerdict:
    """Verdict from prove_mantuq_closure() (docs/48 §6).

    PROVEN carries a MantuqClosureCandidate.
    REFUSED carries a FailureCode and no candidate.
    """

    candidate: MantuqClosureCandidate | None
    verdict_state: MantuqClosureState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# Deferred residuals builder (docs/48 §5)
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the 5 required deferred residuals for MantuqClosureCandidate."""
    names_and_notes = (
        (
            "MAFHUM_NOT_YET_OPENED",
            "Mafhum has not been derived and is constitutionally deferred "
            "until PV-A3 (Mafhum Boundary Law) and PV-A4 (MafhumClosure).",
        ),
        (
            "MANTUQ_NOT_MAFHUM",
            "MantuqClosureCandidate is the preserved explicit origin, "
            "not the implied branch. Mafhum is a branch of Mantuq.",
        ),
        (
            "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
            "Majaz (figurative transfer) is deferred until HaqiqahAttempt "
            "boundary is established. No figurative determination here.",
        ),
        (
            "HAQIQAH_ATTEMPT_DEFERRED",
            "HaqiqahAttempt (literal/figurative determination) is deferred. "
            "MantuqClosure preserves the origin without determining "
            "haqiqah vs majaz.",
        ),
        (
            "NAQL_DEFERRED_UNTIL_TRANSFER_GATE",
            "Naql (terminological transfer) is deferred until a transfer "
            "gate is licensed. No terminological transfer at this boundary.",
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
# prove_mantuq_closure — the pure operation
# ---------------------------------------------------------------------------


def prove_mantuq_closure(
    ifadah_verdict: IfadahVerdict,
    maqam_verdict: MaqamContextBoundaryVerdict,
    mantuq_scope: str,
    spoken_surface_ref: str,
    mantuq_evidence: str,
    closure_scope: str,
) -> MantuqClosureVerdict:
    """Prove mantuq closure (preserved spoken/textual origin) candidate.

    Parameters
    ----------
    ifadah_verdict
        PROVEN IfadahVerdict (PR-20).
    maqam_verdict
        PROVEN MaqamContextBoundaryVerdict (PR-D1.2).
    mantuq_scope
        Non-empty scope of the mantuq boundary.
    spoken_surface_ref
        Non-empty reference to the spoken/textual surface being preserved.
    mantuq_evidence
        Non-empty evidence supporting the mantuq preservation.
    closure_scope
        Non-empty scope of the closure operation.

    Returns
    -------
    MantuqClosureVerdict
        PROVEN with a MantuqClosureCandidate on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "prove_mantuq_closure"

    # --- 1. Input boundary: ifadah_verdict type ---
    if not isinstance(ifadah_verdict, IfadahVerdict):
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_IFADAH,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_verdict_invalid_type",
        )

    # --- 2. Input boundary: ifadah must be PROVEN ---
    if ifadah_verdict.verdict_state is not IfadahState.PROVEN:
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_IFADAH,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_not_proven",
        )

    # --- 3. Input boundary: ifadah candidate present ---
    if not isinstance(ifadah_verdict.candidate, IfadahCandidate):
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_IFADAH,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_candidate_missing",
        )

    # --- 4. Input boundary: maqam_verdict type ---
    if not isinstance(maqam_verdict, MaqamContextBoundaryVerdict):
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_IFADAH_MAQAM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_verdict_invalid_type",
        )

    # --- 5. Input boundary: maqam must be PROVEN ---
    if maqam_verdict.verdict_state is not MaqamContextState.PROVEN:
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_IFADAH_MAQAM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_not_proven",
        )

    # --- 6. Input boundary: maqam concordance ---
    # The maqam verdict ref must match the ifadah candidate's maqam ref
    if (
        maqam_verdict.trace_ref
        != ifadah_verdict.candidate.maqam_verdict_ref
    ):
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.MANTUQ_MAQAM_DIVERGENCE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_divergence",
        )

    # --- 7. Input boundary: mantuq_scope ---
    if not isinstance(mantuq_scope, str) or not mantuq_scope.strip():
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_MANTUQ_SCOPE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/mantuq_scope_empty",
        )

    # --- 8. Input boundary: spoken_surface_ref ---
    if not isinstance(spoken_surface_ref, str) or not spoken_surface_ref.strip():
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_SPOKEN_SURFACE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/spoken_surface_ref_empty",
        )

    # --- 9. Input boundary: mantuq_evidence ---
    if not isinstance(mantuq_evidence, str) or not mantuq_evidence.strip():
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_MANTUQ_EVIDENCE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/mantuq_evidence_empty",
        )

    # --- 10. Input boundary: closure_scope ---
    if not isinstance(closure_scope, str) or not closure_scope.strip():
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_MANTUQ_CLOSURE_SCOPE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/closure_scope_empty",
        )

    # --- 11. Compute rank (meet of ifadah rank and ceiling) ---
    verdict_rank = RankLattice.meet(
        ifadah_verdict.verdict_rank,
        MANTUQ_RANK_CEILING,
    )

    # --- 12. Check rank ceiling ---
    if verdict_rank > MANTUQ_RANK_CEILING:
        return MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/rank_exceeds_ceiling",
        )

    # --- 13. Build deferred residuals ---
    deferred_residuals = _build_deferred_residuals()

    # --- 14. Check deferred residual governance ---
    for r in deferred_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return MantuqClosureVerdict(
                candidate=None,
                verdict_state=MantuqClosureState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return MantuqClosureVerdict(
                candidate=None,
                verdict_state=MantuqClosureState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- 15. Check input ifadah verdict residuals ---
    for r in ifadah_verdict.residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return MantuqClosureVerdict(
                candidate=None,
                verdict_state=MantuqClosureState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/ifadah_hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return MantuqClosureVerdict(
                candidate=None,
                verdict_state=MantuqClosureState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/ifadah_blocking_residual",
            )

    # --- 16. Construct MantuqClosureCandidate ---
    candidate = MantuqClosureCandidate(
        ifadah_verdict_ref=ifadah_verdict.trace_ref,
        maqam_verdict_ref=maqam_verdict.trace_ref,
        mantuq_scope=mantuq_scope,
        spoken_surface_ref=spoken_surface_ref,
        mantuq_evidence=mantuq_evidence,
        closure_scope=closure_scope,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )

    return MantuqClosureVerdict(
        candidate=candidate,
        verdict_state=MantuqClosureState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )
