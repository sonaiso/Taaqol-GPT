"""HukmCandidate — PR-21.

PR-21 binding of ``docs/43_HUKM_DOMAIN_BOUNDARY_LAW.md``.

This module proves that a PROVEN IfadahVerdict, under a declared
EvaluationDomain with explicit evidence and maqam, carries a
**judgment candidate** (hukm candidate). It does not determine
authority, enforcement, execution, reality, or meaning.

PR-21 consumes:
1. A PROVEN IfadahVerdict (PR-20).
2. An EvaluationDomain (LINGUISTIC | LOGICAL | NORMATIVE_CANDIDATE).
3. hukm_claim (non-empty).
4. hukm_evidence (non-empty).
5. hukm_maqam (non-empty).
6. closure_scope (non-empty).

Constitutional invariants (docs/43 §9):

* HukmCandidate ≠ Authority.
* HukmCandidate ≠ NormativeJudgment.
* HukmCandidate ≠ FinalMeaning.
* HukmCandidate ≠ Meaning.
* HukmCandidate ≠ Reality.
* HukmCandidate ≠ ManatCandidate.
* HukmCandidate ≠ TanzilCandidate.
* HukmCandidate ≠ PropositionTruthValue.
* HukmCandidate ≠ OntologicalClaim.
* HukmCandidate ≠ FreeReasoning.
* HukmCandidate ≠ Enforcement.
* HukmCandidate ≠ Execution.
* No hukm closure without a PROVEN IfadahVerdict.
* No hukm closure without one of the minimal EvaluationDomain members.
* No hukm closure without explicit hukm_claim and hukm_evidence.
* No hukm closure without a maqam (explicit or carried).
* No hukm closure with hidden or blocking residuals.
* No rank promotion beyond HUKM_RANK_CEILING.
* All operations are pure: no I/O, no ledger, no network, no clock.
* NORMATIVE_CANDIDATE only — never bare NORMATIVE.

Deferred residuals (docs/43 §11):

* HUKM_NOT_AUTHORITY — HukmCandidate is evaluation, not binding authority.
* MANAT_DEFERRED_UNTIL_MANAT_LAW — awaits docs/44.
* TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW — awaits docs/45.
* MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL — awaits docs/46.
* EXTENDED_DOMAIN_DEFERRED — domains beyond the minimal set.
* REALITY_VERIFICATION_DEFERRED — reality check is manat, not hukm.
* AUDIT_INTEGRATION_DEFERRED_UNTIL_PR_22_AUDIT — awaits PR-22-AUDIT.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.ifadah_candidate import (
    IFADAH_RANK_CEILING,
    IfadahCandidate,
    IfadahState,
    IfadahVerdict,
)

__all__ = [
    "EvaluationDomain",
    "HUKM_RANK_CEILING",
    "HukmCandidate",
    "HukmState",
    "HukmVerdict",
    "prove_hukm_candidate",
]

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from ifadah layer
# ---------------------------------------------------------------------------

HUKM_RANK_CEILING: Rank = IFADAH_RANK_CEILING

# ---------------------------------------------------------------------------
# EvaluationDomain — minimal set (docs/43 §6)
# ---------------------------------------------------------------------------


class EvaluationDomain(StrEnum):
    """Minimal evaluation domain set for PR-21 (docs/43 §6).

    Only LINGUISTIC, LOGICAL, and NORMATIVE_CANDIDATE are licensed members.
    Extended domains (beyond this set) are deferred residuals only — never
    enum members in PR-21.

    NORMATIVE_CANDIDATE evaluates ifadah qua normative bearing (always
    candidate, never binding ruling, fatwa, qada, or authority claim).
    """

    LINGUISTIC = "LINGUISTIC"
    LOGICAL = "LOGICAL"
    NORMATIVE_CANDIDATE = "NORMATIVE_CANDIDATE"


# ---------------------------------------------------------------------------
# HukmState — verdict outcome
# ---------------------------------------------------------------------------


class HukmState(StrEnum):
    """The outcome of a prove_hukm_candidate() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# HukmCandidate — the judgment candidate carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class HukmCandidate:
    """Judgment candidate carrier (docs/43 §1, §9).

    Proves that a closed ifadah (speech-level closure) has been evaluated
    inside a single declared domain with explicit evidence.

    HukmCandidate ≠ Authority.
    HukmCandidate ≠ NormativeJudgment.
    HukmCandidate ≠ FinalMeaning.
    """

    ifadah_verdict_ref: str
    evaluation_domain: EvaluationDomain
    hukm_claim: str
    hukm_evidence: str
    hukm_maqam: str
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
        if not isinstance(self.evaluation_domain, EvaluationDomain):
            raise WeightCarrierSchemaError(
                f"evaluation_domain must be an EvaluationDomain member, "
                f"got {type(self.evaluation_domain).__name__}",
                FailureCode.NO_EVALUATION_DOMAIN,
            )
        if (
            not isinstance(self.hukm_claim, str)
            or not self.hukm_claim.strip()
        ):
            raise WeightCarrierSchemaError(
                "hukm_claim must be a non-empty string",
                FailureCode.NO_HUKM_CLAIM,
            )
        if (
            not isinstance(self.hukm_evidence, str)
            or not self.hukm_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "hukm_evidence must be a non-empty string",
                FailureCode.NO_HUKM_EVIDENCE,
            )
        if (
            not isinstance(self.hukm_maqam, str)
            or not self.hukm_maqam.strip()
        ):
            raise WeightCarrierSchemaError(
                "hukm_maqam must be a non-empty string",
                FailureCode.NO_HUKM_MAQAM,
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
        if self.rank > HUKM_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{HUKM_RANK_CEILING.name}",
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
# HukmVerdict — operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class HukmVerdict:
    """Verdict from prove_hukm_candidate() (docs/43 §7).

    PROVEN carries a HukmCandidate.
    REFUSED carries a FailureCode and no candidate.
    """

    candidate: HukmCandidate | None
    verdict_state: HukmState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# Deferred residuals builder (docs/43 §11)
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the 7 required deferred residuals for HukmCandidate."""
    names_and_notes = (
        (
            "HUKM_NOT_AUTHORITY",
            "HukmCandidate is evaluation, not binding authority. "
            "It does not determine final authority, enforcement, or meaning.",
        ),
        (
            "MANAT_DEFERRED_UNTIL_MANAT_LAW",
            "Manat (effective cause identification) awaits docs/44 (PR-D8). "
            "No manat before its boundary law.",
        ),
        (
            "TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW",
            "Tanzil (application/presentation) awaits docs/45 (PR-D9). "
            "No application before its presentation boundary.",
        ),
        (
            "MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL",
            "Mafhum/mantuq operations await docs/46 (PR-D10) "
            "horizontal-branch licence. Forbidden before vertical closure.",
        ),
        (
            "EXTENDED_DOMAIN_DEFERRED",
            "Domains beyond the minimal set (LINGUISTIC, LOGICAL, "
            "NORMATIVE_CANDIDATE) are deferred. Never enum members in PR-21.",
        ),
        (
            "REALITY_VERIFICATION_DEFERRED",
            "Reality verification is manat (PR-21M), not hukm. "
            "HukmCandidate does not verify reality or application.",
        ),
        (
            "AUDIT_INTEGRATION_DEFERRED_UNTIL_PR_22_AUDIT",
            "AnswerAudit bridge ships in PR-22-AUDIT. "
            "HukmCandidate does not directly enter AnswerAudit yet.",
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
# prove_hukm_candidate — the pure operation
# ---------------------------------------------------------------------------


def prove_hukm_candidate(
    ifadah_verdict: IfadahVerdict,
    evaluation_domain: EvaluationDomain,
    hukm_claim: str,
    hukm_evidence: str,
    hukm_maqam: str,
    closure_scope: str,
) -> HukmVerdict:
    """Prove hukm (judgment) candidate.

    Parameters
    ----------
    ifadah_verdict
        PROVEN IfadahVerdict (PR-20).
    evaluation_domain
        EvaluationDomain (LINGUISTIC | LOGICAL | NORMATIVE_CANDIDATE).
    hukm_claim
        Non-empty claim string specifying the judgment.
    hukm_evidence
        Non-empty evidence string supporting the judgment.
    hukm_maqam
        Non-empty maqam string (context of evaluation).
    closure_scope
        Non-empty scope bounding the judgment.

    Returns
    -------
    HukmVerdict
        PROVEN with a HukmCandidate on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "prove_hukm_candidate"

    # --- Input boundary: ifadah_verdict type ---
    if not isinstance(ifadah_verdict, IfadahVerdict):
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.NO_IFADAH,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_verdict_invalid_type",
        )

    # --- Input boundary: ifadah must be PROVEN ---
    if ifadah_verdict.verdict_state is not IfadahState.PROVEN:
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.NO_IFADAH,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_not_proven",
        )

    # --- Input boundary: ifadah candidate present ---
    if not isinstance(ifadah_verdict.candidate, IfadahCandidate):
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.NO_IFADAH,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/ifadah_candidate_missing",
        )

    # --- Input boundary: evaluation_domain type ---
    if not isinstance(evaluation_domain, EvaluationDomain):
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.NO_EVALUATION_DOMAIN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/evaluation_domain_invalid_type",
        )

    # --- Domain leap check: must be in the minimal set ---
    # NOTE: This branch is defensively unreachable by enum design (the
    # isinstance check above ensures evaluation_domain is one of the 3
    # members, none of which has value "NORMATIVE"). It exists as a
    # constitutional requirement of docs/43 §6.2 and is tested by the
    # AST alias-drop guard in test_hukm_candidate.py.
    if evaluation_domain.value == "NORMATIVE":
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.AUTHORITY_LEAK,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/bare_normative_authority_leak",
        )

    # --- Input boundary: hukm_claim ---
    if not isinstance(hukm_claim, str) or not hukm_claim.strip():
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.NO_HUKM_CLAIM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_claim_empty",
        )

    # --- Input boundary: hukm_evidence ---
    if not isinstance(hukm_evidence, str) or not hukm_evidence.strip():
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.NO_HUKM_EVIDENCE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_evidence_empty",
        )

    # --- Input boundary: hukm_maqam ---
    if not isinstance(hukm_maqam, str) or not hukm_maqam.strip():
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.NO_HUKM_MAQAM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_maqam_empty",
        )

    # --- Input boundary: closure_scope ---
    if not isinstance(closure_scope, str) or not closure_scope.strip():
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/closure_scope_empty",
        )

    # --- Compute rank (meet of ifadah rank with ceiling) ---
    verdict_rank = RankLattice.meet(
        ifadah_verdict.verdict_rank,
        HUKM_RANK_CEILING,
    )

    # --- Check rank ceiling ---
    if verdict_rank > HUKM_RANK_CEILING:
        return HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/rank_exceeds_ceiling",
        )

    # --- Build deferred residuals ---
    deferred_residuals = _build_deferred_residuals()

    # --- Check deferred residual governance ---
    for r in deferred_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return HukmVerdict(
                candidate=None,
                verdict_state=HukmState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return HukmVerdict(
                candidate=None,
                verdict_state=HukmState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- Check input verdict residuals for hidden/blocking ---
    for r in ifadah_verdict.residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return HukmVerdict(
                candidate=None,
                verdict_state=HukmState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/input_hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return HukmVerdict(
                candidate=None,
                verdict_state=HukmState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/input_blocking_residual",
            )

    # --- Construct HukmCandidate ---
    candidate = HukmCandidate(
        ifadah_verdict_ref=ifadah_verdict.trace_ref,
        evaluation_domain=evaluation_domain,
        hukm_claim=hukm_claim,
        hukm_evidence=hukm_evidence,
        hukm_maqam=hukm_maqam,
        closure_scope=closure_scope,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )

    return HukmVerdict(
        candidate=candidate,
        verdict_state=HukmState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )
