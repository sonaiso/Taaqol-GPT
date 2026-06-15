"""ManāṭCandidate — PR-21M.

PR-21M binding of ``docs/44_MANAT_BOUNDARY_LAW.md``.

This module proves that a PROVEN HukmVerdict, under a declared ManatMode
with explicit description, effective attribute, evidence, and domain,
carries a **manāṭ candidate** (locus-of-application candidate). It does
not verify reality, does not apply the judgment, and does not produce
tanzīl.

PR-21M consumes:
1. A PROVEN HukmVerdict (PR-21).
2. A ManatMode (TAKHRIJ_CANDIDATE | TANQIH_CANDIDATE | TAHQIQ_READINESS_ONLY).
3. manat_description (non-empty).
4. effective_attribute_candidate (non-empty).
5. conditions (tuple[str, ...]).
6. preventers (tuple[str, ...]).
7. manat_evidence (non-empty).
8. manat_domain (non-empty).
9. closure_scope (non-empty).

Constitutional invariants (docs/44 §9):

* ManatCandidate ≠ TanzilCandidate.
* ManatCandidate ≠ RealityVerification.
* ManatCandidate ≠ RealityApplication.
* ManatCandidate ≠ Execution.
* ManatCandidate ≠ FinalAuthority.
* ManatCandidate ≠ FinalMeaning.
* ManatCandidate ≠ Meaning.
* ManatCandidate ≠ PropositionTruthValue.
* ManatCandidate ≠ OntologicalClaim.
* ManatCandidate ≠ FreeReasoning.
* ManatCandidate ≠ Enforcement.
* ManatCandidate ≠ Fatwa.
* ManatCandidate ≠ Qada.
* ManatCandidate ≠ DivineAuthorityClaim.
* No manāṭ closure without a PROVEN HukmVerdict.
* No manāṭ closure without one of the minimal ManatMode members.
* No manāṭ closure without explicit manat_description and
  effective_attribute_candidate.
* No manāṭ closure without manat_evidence.
* No manāṭ closure without manat_domain.
* No manāṭ closure with hidden or blocking residuals.
* No rank promotion beyond MANAT_RANK_CEILING.
* All operations are pure: no I/O, no ledger, no network, no clock.
* TAHQIQ_READINESS_ONLY — never TAHQIQ_FINAL.

Deferred residuals (docs/44 §11):

* MANAT_NOT_TANZIL — ManatCandidate is locus identification, not presentation.
* TAHQIQ_FINAL_DEFERRED — Final tahqīq verification is deferred beyond PR-21M.
* TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW — awaits docs/45.
* REALITY_APPLICATION_DEFERRED — Reality application is not manāṭ.
* NO_PREVENTER_CHECK_DEFERRED — Conditions/preventers checked only at tahqīq time.
* EXTERNAL_EXECUTION_FORBIDDEN — No external action at the manāṭ boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.hukm_candidate import (
    HUKM_RANK_CEILING,
    HukmCandidate,
    HukmState,
    HukmVerdict,
)

__all__ = [
    "MANAT_RANK_CEILING",
    "ManatCandidate",
    "ManatMode",
    "ManatState",
    "ManatVerdict",
    "prove_manat_candidate",
]

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from hukm layer
# ---------------------------------------------------------------------------

MANAT_RANK_CEILING: Rank = HUKM_RANK_CEILING

# ---------------------------------------------------------------------------
# ManatMode — minimal set (docs/44 §6)
# ---------------------------------------------------------------------------


class ManatMode(StrEnum):
    """Minimal manāṭ mode set for PR-21M (docs/44 §6).

    Only TAKHRIJ_CANDIDATE, TANQIH_CANDIDATE, and TAHQIQ_READINESS_ONLY
    are licensed members. Extended modes are deferred residuals only —
    never enum members in PR-21M.

    TAHQIQ_READINESS_ONLY is readiness, never verification.
    """

    TAKHRIJ_CANDIDATE = "TAKHRIJ_CANDIDATE"
    TANQIH_CANDIDATE = "TANQIH_CANDIDATE"
    TAHQIQ_READINESS_ONLY = "TAHQIQ_READINESS_ONLY"


# ---------------------------------------------------------------------------
# ManatState — verdict outcome
# ---------------------------------------------------------------------------


class ManatState(StrEnum):
    """The outcome of a prove_manat_candidate() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# ManatCandidate — the manāṭ candidate carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ManatCandidate:
    """Manāṭ candidate carrier (docs/44 §1, §9).

    Proves that a PROVEN HukmCandidate has been given a candidate
    locus of application: an effective attribute, a description,
    evidence, and a domain.

    ManatCandidate ≠ TanzilCandidate.
    ManatCandidate ≠ RealityApplication.
    ManatCandidate ≠ Execution.
    """

    hukm_verdict_ref: str
    manat_mode: ManatMode
    manat_description: str
    effective_attribute_candidate: str
    conditions: tuple[str, ...]
    preventers: tuple[str, ...]
    manat_evidence: str
    manat_domain: str
    closure_scope: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if (
            not isinstance(self.hukm_verdict_ref, str)
            or not self.hukm_verdict_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "hukm_verdict_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.manat_mode, ManatMode):
            raise WeightCarrierSchemaError(
                f"manat_mode must be a ManatMode member, "
                f"got {type(self.manat_mode).__name__}",
                FailureCode.NO_MANAT_MODE,
            )
        if (
            not isinstance(self.manat_description, str)
            or not self.manat_description.strip()
        ):
            raise WeightCarrierSchemaError(
                "manat_description must be a non-empty string",
                FailureCode.NO_MANAT_DESCRIPTION,
            )
        if (
            not isinstance(self.effective_attribute_candidate, str)
            or not self.effective_attribute_candidate.strip()
        ):
            raise WeightCarrierSchemaError(
                "effective_attribute_candidate must be a non-empty string",
                FailureCode.NO_EFFECTIVE_ATTRIBUTE,
            )
        if not isinstance(self.conditions, tuple):
            raise WeightCarrierSchemaError(
                "conditions must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        for c in self.conditions:
            if not isinstance(c, str):
                raise WeightCarrierSchemaError(
                    f"each condition must be a str, got {type(c).__name__}",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        if not isinstance(self.preventers, tuple):
            raise WeightCarrierSchemaError(
                "preventers must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        for p in self.preventers:
            if not isinstance(p, str):
                raise WeightCarrierSchemaError(
                    f"each preventer must be a str, got {type(p).__name__}",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        if (
            not isinstance(self.manat_evidence, str)
            or not self.manat_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "manat_evidence must be a non-empty string",
                FailureCode.NO_MANAT_EVIDENCE,
            )
        if (
            not isinstance(self.manat_domain, str)
            or not self.manat_domain.strip()
        ):
            raise WeightCarrierSchemaError(
                "manat_domain must be a non-empty string",
                FailureCode.NO_MANAT_DOMAIN,
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
        if self.rank > MANAT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{MANAT_RANK_CEILING.name}",
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
# ManatVerdict — operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ManatVerdict:
    """Verdict from prove_manat_candidate() (docs/44 §7).

    PROVEN carries a ManatCandidate.
    REFUSED carries a FailureCode and no candidate.
    """

    candidate: ManatCandidate | None
    verdict_state: ManatState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# Deferred residuals builder (docs/44 §11)
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the 6 required deferred residuals for ManatCandidate."""
    names_and_notes = (
        (
            "MANAT_NOT_TANZIL",
            "ManatCandidate is locus identification, not presentation. "
            "Tanzil awaits docs/45 (PR-D9).",
        ),
        (
            "TAHQIQ_FINAL_DEFERRED",
            "Final tahqiq verification is deferred beyond PR-21M. "
            "TAHQIQ_READINESS_ONLY is readiness, never verification.",
        ),
        (
            "TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW",
            "Tanzil (application/presentation) awaits docs/45 (PR-D9). "
            "No application before its presentation boundary.",
        ),
        (
            "REALITY_APPLICATION_DEFERRED",
            "Reality application is not manat. "
            "ManatCandidate does not apply judgment to reality.",
        ),
        (
            "NO_PREVENTER_CHECK_DEFERRED",
            "Conditions/preventers are candidates only. "
            "Checking against reality is deferred to tahqiq time.",
        ),
        (
            "EXTERNAL_EXECUTION_FORBIDDEN",
            "No external action at the manat boundary. "
            "Execution is never a manat operation.",
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
# Forbidden overclaim keywords (docs/44 §6.2, §10)
# ---------------------------------------------------------------------------

_TAHQIQ_OVERCLAIM_KEYWORDS = frozenset({
    "verified", "confirmed", "reality_checked", "applied",
    "executed", "final_tahqiq", "tahqiq_final",
})


# ---------------------------------------------------------------------------
# prove_manat_candidate — the pure operation
# ---------------------------------------------------------------------------


def prove_manat_candidate(
    hukm_verdict: HukmVerdict,
    manat_mode: ManatMode,
    manat_description: str,
    effective_attribute_candidate: str,
    conditions: tuple[str, ...],
    preventers: tuple[str, ...],
    manat_evidence: str,
    manat_domain: str,
    closure_scope: str,
) -> ManatVerdict:
    """Prove manāṭ (locus-of-application) candidate.

    Parameters
    ----------
    hukm_verdict
        PROVEN HukmVerdict (PR-21).
    manat_mode
        ManatMode (TAKHRIJ_CANDIDATE | TANQIH_CANDIDATE | TAHQIQ_READINESS_ONLY).
    manat_description
        Non-empty description of the manāṭ (locus of application).
    effective_attribute_candidate
        Non-empty candidate effective attribute (al-waṣf al-muʾaththir).
    conditions
        Tuple of candidate condition strings.
    preventers
        Tuple of candidate preventer strings.
    manat_evidence
        Non-empty evidence string supporting the manāṭ identification.
    manat_domain
        Non-empty domain bounding the manāṭ.
    closure_scope
        Non-empty scope bounding the manāṭ candidate.

    Returns
    -------
    ManatVerdict
        PROVEN with a ManatCandidate on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "prove_manat_candidate"

    # --- 1. Input boundary: hukm_verdict type ---
    if not isinstance(hukm_verdict, HukmVerdict):
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.NO_HUKM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_verdict_invalid_type",
        )

    # --- 2. Input boundary: hukm must be PROVEN ---
    if hukm_verdict.verdict_state is not HukmState.PROVEN:
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.NO_HUKM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_not_proven",
        )

    # --- 3. Input boundary: hukm candidate present ---
    if not isinstance(hukm_verdict.candidate, HukmCandidate):
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.NO_HUKM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_candidate_missing",
        )

    # --- 4. Input boundary: manat_mode type ---
    if not isinstance(manat_mode, ManatMode):
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.NO_MANAT_MODE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/manat_mode_invalid_type",
        )

    # --- 5. Input boundary: manat_description ---
    if not isinstance(manat_description, str) or not manat_description.strip():
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.NO_MANAT_DESCRIPTION,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/manat_description_empty",
        )

    # --- 6. Input boundary: effective_attribute_candidate ---
    if (
        not isinstance(effective_attribute_candidate, str)
        or not effective_attribute_candidate.strip()
    ):
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.NO_EFFECTIVE_ATTRIBUTE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/effective_attribute_empty",
        )

    # --- 7. Input boundary: conditions type ---
    if not isinstance(conditions, tuple):
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/conditions_not_tuple",
        )
    for c in conditions:
        if not isinstance(c, str):
            return ManatVerdict(
                candidate=None,
                verdict_state=ManatState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref=f"{_trace_base}/refused/condition_not_str",
            )

    # --- 8. Input boundary: preventers type ---
    if not isinstance(preventers, tuple):
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/preventers_not_tuple",
        )
    for p in preventers:
        if not isinstance(p, str):
            return ManatVerdict(
                candidate=None,
                verdict_state=ManatState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref=f"{_trace_base}/refused/preventer_not_str",
            )

    # --- 9. Input boundary: manat_evidence ---
    if not isinstance(manat_evidence, str) or not manat_evidence.strip():
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.NO_MANAT_EVIDENCE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/manat_evidence_empty",
        )

    # --- 10. Input boundary: manat_domain ---
    if not isinstance(manat_domain, str) or not manat_domain.strip():
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.NO_MANAT_DOMAIN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/manat_domain_empty",
        )

    # --- 11. Input boundary: closure_scope ---
    if not isinstance(closure_scope, str) or not closure_scope.strip():
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/closure_scope_empty",
        )

    # --- 12. TAHQIQ_READINESS_ONLY overclaim check ---
    if manat_mode is ManatMode.TAHQIQ_READINESS_ONLY:
        lower_desc = manat_description.lower()
        lower_attr = effective_attribute_candidate.lower()
        for keyword in _TAHQIQ_OVERCLAIM_KEYWORDS:
            if keyword in lower_desc or keyword in lower_attr:
                return ManatVerdict(
                    candidate=None,
                    verdict_state=ManatState.REFUSED,
                    failure_code=FailureCode.TAHQIQ_OVERCLAIM,
                    verdict_rank=Rank.ZERO,
                    residuals=(),
                    trace_ref=f"{_trace_base}/refused/tahqiq_overclaim",
                )

    # --- 13. Compute rank (meet of hukm rank with ceiling) ---
    verdict_rank = RankLattice.meet(
        hukm_verdict.verdict_rank,
        MANAT_RANK_CEILING,
    )

    # --- 14. Check rank ceiling ---
    if verdict_rank > MANAT_RANK_CEILING:
        return ManatVerdict(
            candidate=None,
            verdict_state=ManatState.REFUSED,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/rank_exceeds_ceiling",
        )

    # --- 15. Build deferred residuals ---
    deferred_residuals = _build_deferred_residuals()

    # --- 16. Check deferred residual governance ---
    for r in deferred_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return ManatVerdict(
                candidate=None,
                verdict_state=ManatState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return ManatVerdict(
                candidate=None,
                verdict_state=ManatState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- 17. Check input verdict residuals for hidden/blocking ---
    for r in hukm_verdict.residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return ManatVerdict(
                candidate=None,
                verdict_state=ManatState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/input_hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return ManatVerdict(
                candidate=None,
                verdict_state=ManatState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/input_blocking_residual",
            )

    # --- Construct ManatCandidate ---
    candidate = ManatCandidate(
        hukm_verdict_ref=hukm_verdict.trace_ref,
        manat_mode=manat_mode,
        manat_description=manat_description,
        effective_attribute_candidate=effective_attribute_candidate,
        conditions=conditions,
        preventers=preventers,
        manat_evidence=manat_evidence,
        manat_domain=manat_domain,
        closure_scope=closure_scope,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )

    return ManatVerdict(
        candidate=candidate,
        verdict_state=ManatState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )
