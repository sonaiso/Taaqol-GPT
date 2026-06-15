"""MafhūmClosure — PV-A4.

PV-A4 binding of ``docs/50_MAFHUM_BOUNDARY_LAW.md``.

This module proves that a CLOSED MantuqClosureCandidate, combined with a
declared outside boundary, a branch relation, a source domain declaration,
and visible residuals, carries a **mafhum closure candidate** — proof that
the mafhum (implied meaning outside the explicit indication) satisfies
the eight admission conditions from docs/50 §4.

MafhumClosureCandidate ≠ HukmCandidate.
MafhumClosureCandidate ≠ TanzilCandidate.
MafhumClosureCandidate ≠ RealityClaim.
MafhumClosureCandidate ≠ MajazVerdict.
MafhumClosureCandidate ≠ NaqlVerdict.
MafhumClosureCandidate ≠ Certificate.

PV-A4 consumes:
1. A PROVEN MantuqClosureVerdict with a MantuqClosureCandidate.
2. outside_boundary (non-empty: what the mafhum asserts outside mantuq).
3. branch_type (muwafaqah or mukhalafah).
4. branch_subtype (optional: specific mukhalafah type e.g. sifah/shart/etc).
5. qayd (non-empty: the constraint licensing the branch).
6. source_domain (non-empty: meta-term domain per docs/49).
7. mantuq_blocks (bool: whether the mantuq explicitly blocks this mafhum).
8. residuals (tuple of Residual).

Constitutional invariants (docs/50 §1, §4, §13):

* No mafhum without a closed mantuq (Law 1).
* No outside without a defined inside (Law 2).
* No branch without a declared source domain (Law 3).
* No branch without a branch relation (Law 4).
* No unlicensed cross-domain transfer (Law 5).
* No mafhum with blocking mantuq constraint (Law 6).
* No mafhum with hidden residuals (Law 7).
* No hukm or tanzil from mafhum in this law (Law 8).
* Rank ceiling: CANDIDATE (docs/50 §10).
* All operations are pure: no I/O, no ledger, no network, no clock.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.mantuq_closure import (
    MantuqClosureCandidate,
    MantuqClosureState,
    MantuqClosureVerdict,
)

__all__ = [
    "MAFHUM_RANK_CEILING",
    "MafhumBranchType",
    "MafhumClosureCandidate",
    "MafhumClosureState",
    "MafhumClosureVerdict",
    "prove_mafhum_closure",
]

# ---------------------------------------------------------------------------
# Rank ceiling — docs/50 §10: CANDIDATE only, never beyond.
# ---------------------------------------------------------------------------

MAFHUM_RANK_CEILING: Rank = Rank.CANDIDATE

# ---------------------------------------------------------------------------
# MafhumBranchType — muwafaqah vs mukhalafah
# ---------------------------------------------------------------------------


class MafhumBranchType(StrEnum):
    """The two primary mafhum branch types (docs/50 §9)."""

    MUWAFAQAH = "MUWAFAQAH"
    MUKHALAFAH = "MUKHALAFAH"


# ---------------------------------------------------------------------------
# MafhumClosureState — verdict outcome
# ---------------------------------------------------------------------------


class MafhumClosureState(StrEnum):
    """The outcome of a prove_mafhum_closure() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# MafhumClosureCandidate — the mafhum closure carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MafhumClosureCandidate:
    """Mafhum closure candidate carrier (docs/50 §1, §13).

    Proves that an implied meaning (mafhum) branching from a closed
    mantuq satisfies all eight admission conditions. The candidate
    never reaches beyond MAFHUM_RANK_CEILING (CANDIDATE). It does not
    produce hukm, tanzil, or reality.

    MafhumClosureCandidate ≠ HukmCandidate.
    MafhumClosureCandidate ≠ TanzilCandidate.
    MafhumClosureCandidate ≠ Certificate.
    """

    mantuq_closure_ref: str
    outside_boundary: str
    branch_type: MafhumBranchType
    branch_subtype: str
    qayd: str
    source_domain: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if (
            not isinstance(self.mantuq_closure_ref, str)
            or not self.mantuq_closure_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "mantuq_closure_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.outside_boundary, str)
            or not self.outside_boundary.strip()
        ):
            raise WeightCarrierSchemaError(
                "outside_boundary must be a non-empty string",
                FailureCode.NO_MAFHUM_WITHOUT_OUTSIDE_BOUNDARY,
            )
        if not isinstance(self.branch_type, MafhumBranchType):
            raise WeightCarrierSchemaError(
                f"branch_type must be a MafhumBranchType member, "
                f"got {type(self.branch_type).__name__}",
                FailureCode.NO_MAFHUM_WITHOUT_BRANCH_RELATION,
            )
        if not isinstance(self.branch_subtype, str):
            raise WeightCarrierSchemaError(
                "branch_subtype must be a string",
                FailureCode.NO_MAFHUM_WITHOUT_BRANCH_RELATION,
            )
        if not isinstance(self.qayd, str) or not self.qayd.strip():
            raise WeightCarrierSchemaError(
                "qayd must be a non-empty string",
                FailureCode.NO_MAFHUM_WITHOUT_BRANCH_RELATION,
            )
        if (
            not isinstance(self.source_domain, str)
            or not self.source_domain.strip()
        ):
            raise WeightCarrierSchemaError(
                "source_domain must be a non-empty string",
                FailureCode.NO_MAFHUM_WITHOUT_SOURCE_DOMAIN,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > MAFHUM_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{MAFHUM_RANK_CEILING.name}",
                FailureCode.RANK_EXCEEDS_CEILING,
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "residuals must be a tuple",
                FailureCode.MAFHUM_HIDDEN_RESIDUAL,
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    f"each residual must be a Residual instance, "
                    f"got {type(r).__name__}",
                    FailureCode.MAFHUM_HIDDEN_RESIDUAL,
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# MafhumClosureVerdict — operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MafhumClosureVerdict:
    """Verdict from prove_mafhum_closure() (docs/50 §4).

    PROVEN carries a MafhumClosureCandidate.
    REFUSED carries a FailureCode and no candidate.
    """

    candidate: MafhumClosureCandidate | None
    verdict_state: MafhumClosureState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# prove_mafhum_closure — the pure operation
# ---------------------------------------------------------------------------


def prove_mafhum_closure(
    mantuq_verdict: MantuqClosureVerdict,
    outside_boundary: str,
    branch_type: MafhumBranchType,
    branch_subtype: str,
    qayd: str,
    source_domain: str,
    cross_domain_transfer: str,
    mantuq_blocks: bool,
    residuals: tuple[Residual, ...],
) -> MafhumClosureVerdict:
    """Prove mafhum closure candidate (docs/50 §4, §13).

    Parameters
    ----------
    mantuq_verdict
        PROVEN MantuqClosureVerdict (PV-A2).
    outside_boundary
        Non-empty description of the outside boundary (what
        the mafhum asserts beyond the mantuq).
    branch_type
        MUWAFAQAH or MUKHALAFAH.
    branch_subtype
        Specific subtype (e.g. "sifah", "shart", "ghayah",
        "adad", "laqab") or empty string for muwafaqah.
    qayd
        Non-empty: the constraint that separates inside from outside.
    source_domain
        Non-empty: the meta-language domain per docs/49 (e.g. "nahw",
        "sarf", "dalalah", "usul").
    cross_domain_transfer
        Empty string if no cross-domain transfer; non-empty if the
        mafhum references a term at a different domain level. If non-empty,
        this is treated as an unlicensed transfer (Law 5 refusal).
    mantuq_blocks
        If True, the mantuq carries a constraint that blocks this mafhum
        (Law 6 refusal).
    residuals
        Tuple of Residual instances to attach to the candidate.

    Returns
    -------
    MafhumClosureVerdict
        PROVEN with a MafhumClosureCandidate on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "prove_mafhum_closure"

    # --- Law 1: No mafhum before closed mantuq ---
    if not isinstance(mantuq_verdict, MantuqClosureVerdict):
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.NO_MAFHUM_BEFORE_MANTUQ_CLOSURE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/mantuq_verdict_invalid_type",
        )

    if mantuq_verdict.verdict_state is not MantuqClosureState.PROVEN:
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.NO_MAFHUM_BEFORE_MANTUQ_CLOSURE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/mantuq_not_proven",
        )

    if not isinstance(mantuq_verdict.candidate, MantuqClosureCandidate):
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.NO_MAFHUM_BEFORE_MANTUQ_CLOSURE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/mantuq_candidate_missing",
        )

    # --- Law 2: No outside without defined inside boundary ---
    if not isinstance(outside_boundary, str) or not outside_boundary.strip():
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.NO_MAFHUM_WITHOUT_OUTSIDE_BOUNDARY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/outside_boundary_empty",
        )

    # --- Law 3: No mafhum without declared source domain ---
    if not isinstance(source_domain, str) or not source_domain.strip():
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.NO_MAFHUM_WITHOUT_SOURCE_DOMAIN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/source_domain_empty",
        )

    # --- Law 4: No mafhum without branch relation ---
    if not isinstance(branch_type, MafhumBranchType):
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.NO_MAFHUM_WITHOUT_BRANCH_RELATION,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/branch_type_invalid",
        )

    if not isinstance(qayd, str) or not qayd.strip():
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.NO_MAFHUM_WITHOUT_BRANCH_RELATION,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/qayd_empty",
        )

    # --- Law 5: No unlicensed cross-domain transfer ---
    if isinstance(cross_domain_transfer, str) and cross_domain_transfer.strip():
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.NO_MAFHUM_CROSS_DOMAIN_LEAP,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/cross_domain_transfer",
        )

    # --- Law 6: No mafhum with blocking mantuq constraint ---
    if mantuq_blocks:
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.MANTUQ_BLOCKS_MAFHUM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/mantuq_blocks_mafhum",
        )

    # --- Law 7: No mafhum with hidden residuals ---
    if not isinstance(residuals, tuple):
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.MAFHUM_HIDDEN_RESIDUAL,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/residuals_not_tuple",
        )

    for r in residuals:
        if not isinstance(r, Residual):
            return MafhumClosureVerdict(
                candidate=None,
                verdict_state=MafhumClosureState.REFUSED,
                failure_code=FailureCode.MAFHUM_HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref=f"{_trace_base}/refused/residual_invalid_type",
            )
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return MafhumClosureVerdict(
                candidate=None,
                verdict_state=MafhumClosureState.REFUSED,
                failure_code=FailureCode.MAFHUM_HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return MafhumClosureVerdict(
                candidate=None,
                verdict_state=MafhumClosureState.REFUSED,
                failure_code=FailureCode.MAFHUM_HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- Compute rank (meet of mantuq rank and mafhum ceiling) ---
    verdict_rank = RankLattice.meet(
        mantuq_verdict.verdict_rank,
        MAFHUM_RANK_CEILING,
    )

    # --- Rank ceiling enforcement (defensive: meet guarantees this,
    #     but guards against future RankLattice changes) ---
    if verdict_rank > MAFHUM_RANK_CEILING:
        return MafhumClosureVerdict(
            candidate=None,
            verdict_state=MafhumClosureState.REFUSED,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/rank_exceeds_ceiling",
        )

    # --- Construct MafhumClosureCandidate ---
    candidate = MafhumClosureCandidate(
        mantuq_closure_ref=mantuq_verdict.trace_ref,
        outside_boundary=outside_boundary,
        branch_type=branch_type,
        branch_subtype=branch_subtype if isinstance(branch_subtype, str) else "",
        qayd=qayd,
        source_domain=source_domain,
        rank=verdict_rank,
        residuals=residuals,
        trace_ref=f"{_trace_base}/proven",
    )

    return MafhumClosureVerdict(
        candidate=candidate,
        verdict_state=MafhumClosureState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=residuals,
        trace_ref=f"{_trace_base}/proven",
    )
