"""TanzīlCandidate — PR-22.

PR-22 binding of ``docs/45_TANZIL_PRESENTATION_BOUNDARY_LAW.md``.

This module proves that a PROVEN HukmVerdict and a PROVEN ManatVerdict,
combined with instance-level evidence and a presentation envelope, carry
a **tanzīl candidate** (presentation-bound application readiness). It does
not execute, does not issue fatwa, does not issue qada, and does not claim
final authority.

PR-22 consumes:
1. A PROVEN HukmVerdict (PR-21).
2. A PROVEN ManatVerdict (PR-21M) referencing the same HukmCandidate.
3. reality_evidence (non-empty).
4. instance_descriptor (non-empty).
5. tanzil_scope (non-empty).
6. presentation_warning (non-empty NOT_EXECUTION_WARNING).
7. not_execution_marker (must be True).

Constitutional invariants (docs/45 §9):

* TanzilCandidate ≠ Execution.
* TanzilCandidate ≠ ExternalAction.
* TanzilCandidate ≠ Enforcement.
* TanzilCandidate ≠ Fatwa.
* TanzilCandidate ≠ Qada.
* TanzilCandidate ≠ FinalAuthority.
* TanzilCandidate ≠ DivineAuthorityClaim.
* TanzilCandidate ≠ RealityVerification.
* TanzilCandidate ≠ RealityApplication.
* TanzilCandidate ≠ FinalMeaning.
* TanzilCandidate ≠ Meaning.
* TanzilCandidate ≠ PropositionTruthValue.
* TanzilCandidate ≠ OntologicalClaim.
* TanzilCandidate ≠ FreeReasoning.
* TanzilCandidate ≠ AuthorityClaim.
* TanzilCandidate ≠ NormativeJudgment.
* TanzilCandidate ≠ Certificate.
* No tanzil closure without a PROVEN HukmVerdict.
* No tanzil closure without a PROVEN ManatVerdict.
* No tanzil closure without the ManatCandidate referencing the same
  HukmCandidate.
* No tanzil closure without presentation_warning.
* No tanzil closure without not_execution_marker.
* No tanzil closure with hidden or blocking residuals.
* No rank promotion beyond TANZIL_RANK_CEILING.
* All operations are pure: no I/O, no ledger, no network, no clock.
* Every TanzilCandidate carries its presentation envelope at birth.

Deferred residuals (docs/45 §11):

* TANZIL_NOT_EXECUTION — TanzilCandidate is presentation, never execution.
* PRESENTATION_BOUNDARY_REQUIRED — Envelope is mandatory; no bare tanzil.
* EXTERNAL_EXECUTION_FORBIDDEN — No external action at the tanzil boundary.
* FATWA_FORBIDDEN — Fatwa is not licensed; not deferred, forbidden.
* QADA_FORBIDDEN — Qada is not licensed; not deferred, forbidden.
* ANSWER_AUDIT_BRIDGE_DEFERRED — Awaits PR-22-AUDIT.
* VERTICAL_CLOSURE_DEFERRED — Awaits docs/46 / PR-D10.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.hukm_candidate import (
    HukmCandidate,
    HukmState,
    HukmVerdict,
)
from taaqqul_slot_geometry.weight.manat_candidate import (
    MANAT_RANK_CEILING,
    ManatCandidate,
    ManatState,
    ManatVerdict,
)

__all__ = [
    "TANZIL_RANK_CEILING",
    "TanzilCandidate",
    "TanzilPresentationEnvelope",
    "TanzilState",
    "TanzilVerdict",
    "prove_tanzil_candidate",
]

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from manat layer
# ---------------------------------------------------------------------------

TANZIL_RANK_CEILING: Rank = MANAT_RANK_CEILING

# ---------------------------------------------------------------------------
# TanzilState — verdict outcome
# ---------------------------------------------------------------------------


class TanzilState(StrEnum):
    """The outcome of a prove_tanzil_candidate() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# TanzilPresentationEnvelope — mandatory presentation boundary (docs/45 §6)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TanzilPresentationEnvelope:
    """Presentation envelope for TanzilCandidate (docs/45 §6).

    Every TanzilCandidate must carry this envelope at birth.
    No serialization may separate a TanzilCandidate from its envelope.
    No __repr__ may omit the warning markers.
    """

    not_execution_warning: str
    not_fatwa: bool
    not_qada: bool
    not_final_authority: bool
    rank_visible: bool
    residuals_visible: bool
    trace_visible: bool
    hukm_ref_visible: bool
    manat_ref_visible: bool

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if (
            not isinstance(self.not_execution_warning, str)
            or not self.not_execution_warning.strip()
        ):
            raise WeightCarrierSchemaError(
                "not_execution_warning must be a non-empty string",
                FailureCode.PRESENTATION_WARNING_MISSING,
            )
        if self.not_fatwa is not True:
            raise WeightCarrierSchemaError(
                "not_fatwa must be True",
                FailureCode.AUTHORITY_LEAK,
            )
        if self.not_qada is not True:
            raise WeightCarrierSchemaError(
                "not_qada must be True",
                FailureCode.AUTHORITY_LEAK,
            )
        if self.not_final_authority is not True:
            raise WeightCarrierSchemaError(
                "not_final_authority must be True",
                FailureCode.AUTHORITY_LEAK,
            )
        if self.rank_visible is not True:
            raise WeightCarrierSchemaError(
                "rank_visible must be True",
                FailureCode.NO_PRESENTATION_BOUNDARY,
            )
        if self.residuals_visible is not True:
            raise WeightCarrierSchemaError(
                "residuals_visible must be True",
                FailureCode.NO_PRESENTATION_BOUNDARY,
            )
        if self.trace_visible is not True:
            raise WeightCarrierSchemaError(
                "trace_visible must be True",
                FailureCode.NO_PRESENTATION_BOUNDARY,
            )
        if self.hukm_ref_visible is not True:
            raise WeightCarrierSchemaError(
                "hukm_ref_visible must be True",
                FailureCode.NO_PRESENTATION_BOUNDARY,
            )
        if self.manat_ref_visible is not True:
            raise WeightCarrierSchemaError(
                "manat_ref_visible must be True",
                FailureCode.NO_PRESENTATION_BOUNDARY,
            )


# ---------------------------------------------------------------------------
# TanzilCandidate — the tanzil candidate carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TanzilCandidate:
    """Tanzil candidate carrier (docs/45 §1, §9).

    Proves that a PROVEN HukmCandidate, applied through a PROVEN
    ManatCandidate, is presentable for a specific case — within a
    presentation envelope that prevents the consumer from reading
    the candidate as execution.

    TanzilCandidate ≠ Execution.
    TanzilCandidate ≠ Fatwa.
    TanzilCandidate ≠ Qada.
    TanzilCandidate ≠ FinalAuthority.
    """

    hukm_verdict_ref: str
    manat_verdict_ref: str
    ifadah_ref: str
    reality_evidence: str
    instance_descriptor: str
    tanzil_scope: str
    presentation_envelope: TanzilPresentationEnvelope
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
        if (
            not isinstance(self.manat_verdict_ref, str)
            or not self.manat_verdict_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "manat_verdict_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.ifadah_ref, str) or not self.ifadah_ref.strip():
            raise WeightCarrierSchemaError(
                "ifadah_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.reality_evidence, str)
            or not self.reality_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "reality_evidence must be a non-empty string",
                FailureCode.NO_REALITY_EVIDENCE,
            )
        if (
            not isinstance(self.instance_descriptor, str)
            or not self.instance_descriptor.strip()
        ):
            raise WeightCarrierSchemaError(
                "instance_descriptor must be a non-empty string",
                FailureCode.NO_INSTANCE_DESCRIPTOR,
            )
        if (
            not isinstance(self.tanzil_scope, str)
            or not self.tanzil_scope.strip()
        ):
            raise WeightCarrierSchemaError(
                "tanzil_scope must be a non-empty string",
                FailureCode.NO_TANZIL_SCOPE,
            )
        if not isinstance(self.presentation_envelope, TanzilPresentationEnvelope):
            raise WeightCarrierSchemaError(
                "presentation_envelope must be a TanzilPresentationEnvelope",
                FailureCode.NO_PRESENTATION_BOUNDARY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > TANZIL_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{TANZIL_RANK_CEILING.name}",
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
# TanzilVerdict — operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TanzilVerdict:
    """Verdict from prove_tanzil_candidate() (docs/45 §7).

    PROVEN carries a TanzilCandidate.
    REFUSED carries a FailureCode and no candidate.
    """

    candidate: TanzilCandidate | None
    verdict_state: TanzilState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# Deferred residuals builder (docs/45 §11)
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the 7 required deferred residuals for TanzilCandidate."""
    names_and_notes = (
        (
            "TANZIL_NOT_EXECUTION",
            "TanzilCandidate is presentation, never execution. "
            "No external action, enforcement, or authority exercise.",
        ),
        (
            "PRESENTATION_BOUNDARY_REQUIRED",
            "Envelope is mandatory; no bare tanzil. "
            "No serialization may separate candidate from envelope.",
        ),
        (
            "EXTERNAL_EXECUTION_FORBIDDEN",
            "No external action at the tanzil boundary. "
            "Execution is never a tanzil operation.",
        ),
        (
            "FATWA_FORBIDDEN",
            "Fatwa is not licensed at the tanzil boundary. "
            "Not deferred, forbidden.",
        ),
        (
            "QADA_FORBIDDEN",
            "Qada is not licensed at the tanzil boundary. "
            "Not deferred, forbidden.",
        ),
        (
            "ANSWER_AUDIT_BRIDGE_DEFERRED",
            "Awaits PR-22-AUDIT to surface TanzilCandidate "
            "inside AuditedAnswer.",
        ),
        (
            "VERTICAL_CLOSURE_DEFERRED",
            "Awaits docs/46 / PR-D10 Vertical Path Closure Law. "
            "No vertical closure certificate before PR-D10.",
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
# prove_tanzil_candidate — the pure operation
# ---------------------------------------------------------------------------


def prove_tanzil_candidate(
    hukm_verdict: HukmVerdict,
    manat_verdict: ManatVerdict,
    reality_evidence: str,
    instance_descriptor: str,
    tanzil_scope: str,
    presentation_warning: str,
    not_execution_marker: bool,
) -> TanzilVerdict:
    """Prove tanzil (presentation-bound application readiness) candidate.

    Parameters
    ----------
    hukm_verdict
        PROVEN HukmVerdict (PR-21).
    manat_verdict
        PROVEN ManatVerdict (PR-21M) referencing the same HukmCandidate.
    reality_evidence
        Non-empty instance-level evidence about the specific case.
    instance_descriptor
        Non-empty description of the specific case.
    tanzil_scope
        Non-empty scope of the presentation.
    presentation_warning
        Non-empty NOT_EXECUTION_WARNING string.
    not_execution_marker
        Must be True — the candidate is not execution.

    Returns
    -------
    TanzilVerdict
        PROVEN with a TanzilCandidate on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "prove_tanzil_candidate"

    # --- 1. Input boundary: hukm_verdict type ---
    if not isinstance(hukm_verdict, HukmVerdict):
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_HUKM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_verdict_invalid_type",
        )

    # --- 2. Input boundary: hukm must be PROVEN ---
    if hukm_verdict.verdict_state is not HukmState.PROVEN:
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_HUKM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_not_proven",
        )

    # --- 3. Input boundary: hukm candidate present ---
    if not isinstance(hukm_verdict.candidate, HukmCandidate):
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_HUKM,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/hukm_candidate_missing",
        )

    # --- 4. Input boundary: manat_verdict type ---
    if not isinstance(manat_verdict, ManatVerdict):
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_MANAT,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/manat_verdict_invalid_type",
        )

    # --- 5. Input boundary: manat must be PROVEN ---
    if manat_verdict.verdict_state is not ManatState.PROVEN:
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_MANAT,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/manat_not_proven",
        )

    # --- 6. Input boundary: manat candidate present ---
    if not isinstance(manat_verdict.candidate, ManatCandidate):
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_MANAT,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/manat_candidate_missing",
        )

    # --- 7. Identity continuity: manat references same hukm ---
    if manat_verdict.candidate.hukm_verdict_ref != hukm_verdict.trace_ref:
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_MANAT,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/manat_hukm_ref_mismatch",
        )

    # --- 8. Input boundary: reality_evidence ---
    if not isinstance(reality_evidence, str) or not reality_evidence.strip():
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_REALITY_EVIDENCE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/reality_evidence_empty",
        )

    # --- 9. Input boundary: instance_descriptor ---
    if not isinstance(instance_descriptor, str) or not instance_descriptor.strip():
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_INSTANCE_DESCRIPTOR,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/instance_descriptor_empty",
        )

    # --- 10. Input boundary: tanzil_scope ---
    if not isinstance(tanzil_scope, str) or not tanzil_scope.strip():
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_TANZIL_SCOPE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/tanzil_scope_empty",
        )

    # --- 11. Input boundary: presentation_warning ---
    if not isinstance(presentation_warning, str) or not presentation_warning.strip():
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.PRESENTATION_WARNING_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/presentation_warning_empty",
        )

    # --- 12. Input boundary: not_execution_marker ---
    if not_execution_marker is not True:
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.EXECUTION_LEAK,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/not_execution_marker_false",
        )

    # --- 13. Compute rank (meet of hukm rank, manat rank, ceiling) ---
    verdict_rank = RankLattice.meet(
        hukm_verdict.verdict_rank,
        manat_verdict.verdict_rank,
        TANZIL_RANK_CEILING,
    )

    # --- 14. Check rank ceiling ---
    if verdict_rank > TANZIL_RANK_CEILING:
        return TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
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
            return TanzilVerdict(
                candidate=None,
                verdict_state=TanzilState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return TanzilVerdict(
                candidate=None,
                verdict_state=TanzilState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- 17. Check input hukm verdict residuals ---
    for r in hukm_verdict.residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return TanzilVerdict(
                candidate=None,
                verdict_state=TanzilState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hukm_hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return TanzilVerdict(
                candidate=None,
                verdict_state=TanzilState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hukm_blocking_residual",
            )

    # --- 18. Check input manat verdict residuals ---
    for r in manat_verdict.residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return TanzilVerdict(
                candidate=None,
                verdict_state=TanzilState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/manat_hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return TanzilVerdict(
                candidate=None,
                verdict_state=TanzilState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/manat_blocking_residual",
            )

    # --- 19. Build presentation envelope ---
    envelope = TanzilPresentationEnvelope(
        not_execution_warning=presentation_warning,
        not_fatwa=True,
        not_qada=True,
        not_final_authority=True,
        rank_visible=True,
        residuals_visible=True,
        trace_visible=True,
        hukm_ref_visible=True,
        manat_ref_visible=True,
    )

    # --- 20. Construct TanzilCandidate ---
    candidate = TanzilCandidate(
        hukm_verdict_ref=hukm_verdict.trace_ref,
        manat_verdict_ref=manat_verdict.trace_ref,
        ifadah_ref=hukm_verdict.candidate.ifadah_verdict_ref,
        reality_evidence=reality_evidence,
        instance_descriptor=instance_descriptor,
        tanzil_scope=tanzil_scope,
        presentation_envelope=envelope,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )

    return TanzilVerdict(
        candidate=candidate,
        verdict_state=TanzilState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )
