"""Unified Pre-Semantic Chain Report — PR-16B.

PR-16B binding of ``docs/28_PRE_SEMANTIC_CHAIN_REPORT_LAW.md``.
This module introduces:

* :class:`ChainReportState` — the two report states.
* :class:`PreSemanticChainReport` — the integration carrier.
* :func:`assemble_chain_report` — the pure read-only integration
  operation consuming only a
  :class:`~taaqqul_slot_geometry.weight.verbal_madlul.VerbalMadlulCandidate`.

Constitutional invariants (docs/28):

* assemble_chain_report() accepts ONLY a VerbalMadlulCandidate.
* assemble_chain_report() refuses all other input types.
* PreSemanticChainReport adds NO new linguistic claim.
* PreSemanticChainReport does NOT promote rank.
* PreSemanticChainReport does NOT hide residuals.
* PreSemanticChainReport does NOT assert meaning.
* Rank monotonicity is verified across all layers.
* Residual continuity is verified.
* Forbidden output absence is attested.
* No new FailureCode members; no new runtime dependencies.
* assemble_chain_report() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.verbal_madlul import (
    MADLUL_BOUNDARY_RANK_CEILING,
    VerbalMadlulCandidate,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for the chain report — same as MADLUL_BOUNDARY_RANK_CEILING.
#: The report does not promote rank (docs/28 §7).
CHAIN_REPORT_RANK_CEILING: Rank = MADLUL_BOUNDARY_RANK_CEILING


# ---------------------------------------------------------------------------
# ChainReportState — the two report states
# ---------------------------------------------------------------------------


class ChainReportState(StrEnum):
    """The outcome of an assemble_chain_report() operation (docs/28 §3)."""

    ASSEMBLED = "ASSEMBLED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# PreSemanticChainReport — the integration carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PreSemanticChainReport:
    """The unified pre-semantic chain report (docs/28 §2).

    A read-only integration carrier that proves the pre-semantic chain
    (PR-10 through PR-16) produces a single vertical slice from syllable
    to verbal signified candidacy.

    This carrier adds NO linguistic claim. It aggregates existing outputs
    without promoting rank, hiding residuals, or asserting meaning.
    """

    # --- Source identity ---
    source_surface_identity: str

    # --- Weight readiness layer (PR-10/12) ---
    weight_readiness_ref: str

    # --- Weight fit layer (PR-13) ---
    weight_fit_ref: str
    weight_fit_rank: Rank

    # --- Licensing boundary layer (PR-14) ---
    licensing_boundary_ref: str
    licensing_boundary_kind: str
    licensing_eligibility_rank: Rank

    # --- Signifier layer (PR-15) ---
    dal_ref: str
    signifier_identity: str
    dal_rank: Rank

    # --- Verbal signified layer (PR-16) ---
    verbal_madlul_ref: str
    wad_usage_boundary: str
    correspondence_candidate: str
    inclusion_candidate: str
    iltizam_condition: str
    madlul_rank: Rank

    # --- Governance summary ---
    chain_rank_ceiling: Rank
    residuals: tuple[Residual, ...]
    named_refusals: tuple[str, ...]
    trace_refs: tuple[str, ...]

    # --- Forbidden output attestation ---
    forbidden_outputs_absent: bool

    def __post_init__(self) -> None:
        if not isinstance(self.source_surface_identity, str) or not self.source_surface_identity:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.source_surface_identity must be "
                f"a non-empty string ({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.weight_readiness_ref, str) or not self.weight_readiness_ref:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.weight_readiness_ref must be "
                f"a non-empty string ({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.weight_fit_ref, str) or not self.weight_fit_ref:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.weight_fit_ref must be "
                f"a non-empty string ({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.weight_fit_rank, Rank):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.weight_fit_rank must be a Rank "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if not isinstance(self.licensing_boundary_ref, str) or not self.licensing_boundary_ref:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.licensing_boundary_ref must be "
                f"a non-empty string ({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.licensing_boundary_kind, str) or not self.licensing_boundary_kind:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.licensing_boundary_kind must be "
                f"a non-empty string ({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.licensing_eligibility_rank, Rank):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.licensing_eligibility_rank must be "
                f"a Rank ({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if not isinstance(self.dal_ref, str) or not self.dal_ref:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.dal_ref must be "
                f"a non-empty string ({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.signifier_identity, str) or not self.signifier_identity:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.signifier_identity must be "
                f"a non-empty string ({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.dal_rank, Rank):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.dal_rank must be a Rank "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if not isinstance(self.verbal_madlul_ref, str) or not self.verbal_madlul_ref:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.verbal_madlul_ref must be "
                f"a non-empty string ({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.wad_usage_boundary, str) or not self.wad_usage_boundary:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.wad_usage_boundary must be "
                f"a non-empty string ({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.madlul_rank, Rank):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.madlul_rank must be a Rank "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if not isinstance(self.chain_rank_ceiling, Rank):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.chain_rank_ceiling must be a Rank "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.chain_rank_ceiling > CHAIN_REPORT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.chain_rank_ceiling must not exceed "
                f"{CHAIN_REPORT_RANK_CEILING.name} "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.residuals must be a tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "PreSemanticChainReport.residuals entries must be "
                    f"Residual carriers ({FailureCode.HIDDEN_RESIDUAL.value})"
                )
        if not isinstance(self.named_refusals, tuple):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.named_refusals must be a tuple"
            )
        if not isinstance(self.trace_refs, tuple):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.trace_refs must be a tuple "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        for t in self.trace_refs:
            if not isinstance(t, str) or not t:
                raise WeightCarrierSchemaError(
                    "PreSemanticChainReport.trace_refs entries must be "
                    f"non-empty strings ({FailureCode.TRACE_MISSING.value})"
                )
        if not isinstance(self.forbidden_outputs_absent, bool):
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.forbidden_outputs_absent must be bool"
            )
        if not self.forbidden_outputs_absent:
            raise WeightCarrierSchemaError(
                "PreSemanticChainReport.forbidden_outputs_absent must be True — "
                "a report with forbidden outputs is invalid "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )


# ---------------------------------------------------------------------------
# ChainReportResult — the value returned by assemble_chain_report()
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ChainReportResult:
    """The output of :func:`assemble_chain_report` (docs/28 §3).

    Fields:
    * ``report`` — the PreSemanticChainReport (or None on refusal).
    * ``state`` — ASSEMBLED or REFUSED.
    * ``failure_code`` — named FailureCode on refusal, None on success.
    """

    report: PreSemanticChainReport | None
    state: ChainReportState
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.state, ChainReportState):
            raise WeightCarrierSchemaError(
                "ChainReportResult.state must be a ChainReportState member"
            )
        if self.state is ChainReportState.ASSEMBLED:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "an ASSEMBLED ChainReportResult must not carry a FailureCode"
                )
            if self.report is None:
                raise WeightCarrierSchemaError(
                    "an ASSEMBLED ChainReportResult must carry a PreSemanticChainReport"
                )
            if not isinstance(self.report, PreSemanticChainReport):
                raise WeightCarrierSchemaError(
                    "ChainReportResult.report must be a PreSemanticChainReport"
                )
        elif self.state is ChainReportState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED ChainReportResult must carry a named FailureCode"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "ChainReportResult.failure_code must be a FailureCode member"
                )
            if self.report is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED ChainReportResult must not carry a report"
                )


# ---------------------------------------------------------------------------
# assemble_chain_report() — the pure read-only integration operation
# ---------------------------------------------------------------------------


def assemble_chain_report(
    terminal: VerbalMadlulCandidate,
) -> ChainReportResult:
    """Assemble the unified pre-semantic chain report (docs/28).

    A pure, read-only function: traverses the embedded chain in a
    VerbalMadlulCandidate and aggregates existing outputs into a
    PreSemanticChainReport.

    Input boundary (docs/28 §3):

    * Accepts ONLY a VerbalMadlulCandidate as input.
    * Refuses all other input types with FailureCode.GATE_REQUIRED.

    Output:

    * On success: ASSEMBLED with a PreSemanticChainReport.
    * On refusal: REFUSED with a named FailureCode.

    This function is pure: no I/O, no ledger writes, no network.
    It does NOT promote rank, hide residuals, or assert meaning.
    """
    # --- Input boundary enforcement ---
    if not isinstance(terminal, VerbalMadlulCandidate):
        return ChainReportResult(
            report=None,
            state=ChainReportState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
        )

    # --- Traverse the embedded chain (read-only) ---
    dal_only = terminal.dal_only
    licensing_verdict = dal_only.prior_licensing_verdict
    weight_fit = licensing_verdict.source
    weight_readiness = weight_fit.source

    # --- Extract trace references ---
    weight_readiness_ref = weight_readiness.trace.anchor if weight_readiness.trace else ""
    weight_fit_ref = weight_fit.trace.anchor if weight_fit.trace else ""
    dal_ref = dal_only.trace_ref
    verbal_madlul_ref = terminal.trace_ref

    # --- Validate trace coverage ---
    if not weight_readiness_ref:
        return ChainReportResult(
            report=None,
            state=ChainReportState.REFUSED,
            failure_code=FailureCode.TRACE_MISSING,
        )
    if not weight_fit_ref:
        return ChainReportResult(
            report=None,
            state=ChainReportState.REFUSED,
            failure_code=FailureCode.TRACE_MISSING,
        )

    # --- Extract ranks ---
    fit_rank = weight_fit.fit_rank
    eligibility_rank = licensing_verdict.eligibility_rank
    d_rank = dal_only.dal_rank
    m_rank = terminal.madlul_rank

    # --- Verify rank monotonicity (docs/28 §4) ---
    ranks_in_order = [fit_rank, eligibility_rank, d_rank, m_rank]
    for i in range(len(ranks_in_order) - 1):
        if ranks_in_order[i + 1] > ranks_in_order[i]:
            return ChainReportResult(
                report=None,
                state=ChainReportState.REFUSED,
                failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            )

    # --- Verify no hidden-forbidden residuals (docs/28 §5) ---
    for r in terminal.residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return ChainReportResult(
                report=None,
                state=ChainReportState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
            )

    # --- Compute chain rank ceiling ---
    chain_ceiling = RankLattice.meet(m_rank, CHAIN_REPORT_RANK_CEILING)

    # --- Assemble trace refs ---
    trace_refs = (
        weight_readiness_ref,
        weight_fit_ref,
        f"licensing/{licensing_verdict.boundary_kind.value}",
        dal_ref,
        verbal_madlul_ref,
    )

    # --- Construct the report ---
    report = PreSemanticChainReport(
        source_surface_identity=dal_only.signifier_identity,
        weight_readiness_ref=weight_readiness_ref,
        weight_fit_ref=weight_fit_ref,
        weight_fit_rank=fit_rank,
        licensing_boundary_ref=f"licensing/{licensing_verdict.boundary_kind.value}",
        licensing_boundary_kind=licensing_verdict.boundary_kind.value,
        licensing_eligibility_rank=eligibility_rank,
        dal_ref=dal_ref,
        signifier_identity=dal_only.signifier_identity,
        dal_rank=d_rank,
        verbal_madlul_ref=verbal_madlul_ref,
        wad_usage_boundary=terminal.wad_usage_boundary,
        correspondence_candidate=terminal.correspondence_candidate,
        inclusion_candidate=terminal.inclusion_candidate,
        iltizam_condition=terminal.iltizam_condition,
        madlul_rank=m_rank,
        chain_rank_ceiling=chain_ceiling,
        residuals=terminal.residuals,
        named_refusals=(),
        trace_refs=trace_refs,
        forbidden_outputs_absent=True,
    )

    return ChainReportResult(
        report=report,
        state=ChainReportState.ASSEMBLED,
        failure_code=None,
    )


__all__ = [
    "CHAIN_REPORT_RANK_CEILING",
    "ChainReportResult",
    "ChainReportState",
    "PreSemanticChainReport",
    "assemble_chain_report",
]
