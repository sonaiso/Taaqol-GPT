"""PR-22-AUDIT: Vertical Chain AnswerAudit Bridge.

Surfaces a PROVEN TanzilVerdict inside the audit layer as an
``AuditedTanzilBridge`` — a frozen, presentation-bound record that
preserves the full TanzilPresentationEnvelope and never executes,
never converts the candidate to a certificate, never calls a model
or adapter, and never drops the NOT_EXECUTION / NOT_FATWA / NOT_QADA /
NOT_FINAL_AUTHORITY markers.

Constitutional origin:
- PR-22 TanzilCandidate (docs/45 §1–§11)
- docs/45 Tanzil Presentation Boundary Law
- Amendment-12 vertical closure path

Governing sentences:
  No value in tanzil that does not reach the audit surface.
  No safety in an audit surface that drops the tanzil envelope.

This module is **pure**: it never writes to a TraceLedger, never
calls ModelClient, never invokes an adapter, never performs I/O.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.tanzil_candidate import (
    TANZIL_RANK_CEILING,
    TanzilCandidate,
    TanzilPresentationEnvelope,
    TanzilState,
    TanzilVerdict,
)

__all__ = [
    "AuditBridgeState",
    "AuditedTanzilBridge",
    "AuditedTanzilBridgeVerdict",
    "bridge_tanzil_to_audit",
]


# ---------------------------------------------------------------------------
# AuditBridgeState — verdict outcome
# ---------------------------------------------------------------------------


class AuditBridgeState(StrEnum):
    """Outcome of bridge_tanzil_to_audit()."""

    SURFACED = "SURFACED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# AuditedTanzilBridge — the audit-facing representation
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AuditedTanzilBridge:
    """Audit-facing representation of a TanzilCandidate.

    This is NOT a certificate. It is NOT execution. It carries the
    candidate inside its presentation envelope with all constitutional
    markers visible.

    Birth invariants (enforced; ValueError):
    * tanzil_candidate must be a TanzilCandidate instance.
    * presentation_envelope must be the candidate's own envelope.
    * rank must equal the candidate's rank (never re-ranked).
    * residuals must be the candidate's residuals (never stripped).
    * trace_ref must be the candidate's trace_ref (never truncated).
    * not_execution must be True.
    * not_fatwa must be True.
    * not_qada must be True.
    * not_final_authority must be True.
    """

    tanzil_candidate: TanzilCandidate
    presentation_envelope: TanzilPresentationEnvelope
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str
    not_execution: bool
    not_fatwa: bool
    not_qada: bool
    not_final_authority: bool

    def __post_init__(self) -> None:
        if not isinstance(self.tanzil_candidate, TanzilCandidate):
            raise ValueError(
                "AuditedTanzilBridge.tanzil_candidate must be a "
                "TanzilCandidate instance"
            )
        if not isinstance(self.presentation_envelope, TanzilPresentationEnvelope):
            raise ValueError(
                "AuditedTanzilBridge.presentation_envelope must be a "
                "TanzilPresentationEnvelope"
            )
        if self.presentation_envelope is not self.tanzil_candidate.presentation_envelope:
            raise ValueError(
                "AuditedTanzilBridge.presentation_envelope must be the "
                "candidate's own envelope (identity, not copy)"
            )
        if not isinstance(self.rank, Rank):
            raise ValueError("AuditedTanzilBridge.rank must be a Rank member")
        if self.rank is not self.tanzil_candidate.rank:
            raise ValueError(
                "AuditedTanzilBridge.rank must equal tanzil_candidate.rank "
                "(the audit bridge never re-ranks)"
            )
        if not isinstance(self.residuals, tuple):
            raise ValueError("AuditedTanzilBridge.residuals must be a tuple")
        if self.residuals is not self.tanzil_candidate.residuals:
            raise ValueError(
                "AuditedTanzilBridge.residuals must be the candidate's own "
                "residuals (never stripped)"
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise ValueError(
                "AuditedTanzilBridge.trace_ref must be a non-empty string"
            )
        if self.trace_ref != self.tanzil_candidate.trace_ref:
            raise ValueError(
                "AuditedTanzilBridge.trace_ref must equal "
                "tanzil_candidate.trace_ref"
            )
        if self.not_execution is not True:
            raise ValueError(
                "AuditedTanzilBridge.not_execution must be True "
                "(AUDIT_EXECUTION_LEAK)"
            )
        if self.not_fatwa is not True:
            raise ValueError(
                "AuditedTanzilBridge.not_fatwa must be True "
                "(AUDIT_AUTHORITY_LEAK)"
            )
        if self.not_qada is not True:
            raise ValueError(
                "AuditedTanzilBridge.not_qada must be True "
                "(AUDIT_AUTHORITY_LEAK)"
            )
        if self.not_final_authority is not True:
            raise ValueError(
                "AuditedTanzilBridge.not_final_authority must be True "
                "(AUDIT_AUTHORITY_LEAK)"
            )


# ---------------------------------------------------------------------------
# AuditedTanzilBridgeVerdict — the operation result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AuditedTanzilBridgeVerdict:
    """Verdict from bridge_tanzil_to_audit().

    SURFACED carries an AuditedTanzilBridge.
    REFUSED carries a FailureCode and no bridge.
    """

    bridge: AuditedTanzilBridge | None
    state: AuditBridgeState
    failure_code: FailureCode | None
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# bridge_tanzil_to_audit — the pure bridge operation
# ---------------------------------------------------------------------------


def bridge_tanzil_to_audit(
    tanzil_verdict: TanzilVerdict,
) -> AuditedTanzilBridgeVerdict:
    """Bridge a TanzilVerdict to the audit surface.

    This is pure: no I/O, no ledger, no model call, no adapter call.
    It does not execute the tanzil candidate. It does not convert it
    to a certificate. It surfaces it inside the audit layer with its
    full presentation envelope preserved.

    Parameters
    ----------
    tanzil_verdict
        A TanzilVerdict (from prove_tanzil_candidate).

    Returns
    -------
    AuditedTanzilBridgeVerdict
        SURFACED with an AuditedTanzilBridge on success;
        REFUSED with a named FailureCode on any violation.
    """
    _trace_base = "bridge_tanzil_to_audit"

    # --- 1. Input type check ---
    if not isinstance(tanzil_verdict, TanzilVerdict):
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.NO_TANZIL_VERDICT,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/invalid_verdict_type",
        )

    # --- 2. Verdict must be PROVEN ---
    if tanzil_verdict.verdict_state is not TanzilState.PROVEN:
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.NO_TANZIL_VERDICT,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/verdict_not_proven",
        )

    # --- 3. Candidate must exist ---
    if not isinstance(tanzil_verdict.candidate, TanzilCandidate):
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.NO_TANZIL_VERDICT,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/candidate_missing",
        )

    candidate = tanzil_verdict.candidate

    # --- 4. Presentation envelope must exist ---
    if not isinstance(candidate.presentation_envelope, TanzilPresentationEnvelope):
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.AUDIT_PRESENTATION_ENVELOPE_MISSING,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/envelope_missing",
        )

    envelope = candidate.presentation_envelope

    # --- 5. NOT_EXECUTION warning must be present ---
    if (
        not isinstance(envelope.not_execution_warning, str)
        or not envelope.not_execution_warning.strip()
    ):
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.AUDIT_PRESENTATION_WARNING_MISSING,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/warning_missing",
        )

    # --- 6. NOT_FATWA marker ---
    if envelope.not_fatwa is not True:
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.AUDIT_AUTHORITY_LEAK,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/not_fatwa_missing",
        )

    # --- 7. NOT_QADA marker ---
    if envelope.not_qada is not True:
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.AUDIT_AUTHORITY_LEAK,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/not_qada_missing",
        )

    # --- 8. NOT_FINAL_AUTHORITY marker ---
    if envelope.not_final_authority is not True:
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.AUDIT_AUTHORITY_LEAK,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/not_final_authority_missing",
        )

    # --- 9. Rank must be visible ---
    if envelope.rank_visible is not True:
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.AUDIT_RANK_NOT_VISIBLE,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/rank_not_visible",
        )

    # --- 10. Residuals must be visible ---
    if envelope.residuals_visible is not True:
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.AUDIT_RESIDUALS_NOT_VISIBLE,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/residuals_not_visible",
        )

    # --- 11. Trace must be visible ---
    if envelope.trace_visible is not True:
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.AUDIT_TRACE_NOT_VISIBLE,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/trace_not_visible",
        )

    # --- 12. Rank ceiling check ---
    if candidate.rank > TANZIL_RANK_CEILING:
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            rank=Rank.ZERO,
            residuals=tanzil_verdict.residuals,
            trace_ref=f"{_trace_base}/refused/rank_exceeds_ceiling",
        )

    # --- 13. Residual governance: no hidden residuals ---
    for r in candidate.residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return AuditedTanzilBridgeVerdict(
                bridge=None,
                state=AuditBridgeState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                rank=Rank.ZERO,
                residuals=candidate.residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )

    # --- 14. Residual governance: no blocking residuals ---
    for r in candidate.residuals:
        if r.kind is ResidualKind.BLOCKING:
            return AuditedTanzilBridgeVerdict(
                bridge=None,
                state=AuditBridgeState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                rank=Rank.ZERO,
                residuals=candidate.residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- 15. Trace ref must be present ---
    if not isinstance(candidate.trace_ref, str) or not candidate.trace_ref.strip():
        return AuditedTanzilBridgeVerdict(
            bridge=None,
            state=AuditBridgeState.REFUSED,
            failure_code=FailureCode.TRACE_MISSING,
            rank=Rank.ZERO,
            residuals=candidate.residuals,
            trace_ref=f"{_trace_base}/refused/trace_missing",
        )

    # --- 16. Construct bridge ---
    bridge = AuditedTanzilBridge(
        tanzil_candidate=candidate,
        presentation_envelope=candidate.presentation_envelope,
        rank=candidate.rank,
        residuals=candidate.residuals,
        trace_ref=candidate.trace_ref,
        not_execution=True,
        not_fatwa=True,
        not_qada=True,
        not_final_authority=True,
    )

    return AuditedTanzilBridgeVerdict(
        bridge=bridge,
        state=AuditBridgeState.SURFACED,
        failure_code=None,
        rank=candidate.rank,
        residuals=candidate.residuals,
        trace_ref=f"{_trace_base}/surfaced",
    )
