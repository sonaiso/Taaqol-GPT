"""Lexical / Samāʿ / Qiyās License Boundary — PR-14.

PR-14 binding of ``docs/25_LEXICAL_SAMAEE_QIYAS_LICENSE_BOUNDARY_LAW.md``.
This module introduces:

* :class:`LicenseBoundaryKind` — the three boundary kinds.
* :class:`BoundaryEvidence` — the evidence required by assess_license().
* :class:`LicensingBoundaryVerdict` — the boundary eligibility output.
* :class:`LicensingBoundaryState` — the three verdict states.
* :class:`LicensingBoundaryResult` — the value returned by assess_license().
* :func:`assess_license` — the boundary assessment consuming only a
  :class:`~taaqqul_slot_geometry.weight.weight_fit.WeightFitCandidate`.

Constitutional invariants (docs/25):

* assess_license() accepts ONLY a WeightFitCandidate.
* assess_license() refuses all earlier-stage carriers.
* LicensingBoundaryVerdict is a boundary eligibility assessment, NOT
  LicensedWeight, meaning, agency, hukm, reality, or generated form.
* No rank promotion beyond LICENSE_BOUNDARY_RANK_CEILING.
* Residual governance from PR-12 is respected.
* TraceRef remains a reference, not an audit ledger commit.
* No LexicalMadlulCandidate, no GeneratedQiyasForm.
* No extra-letter licensing, no ContractableUnitGeometry.
* Samāʿ licenses occurrence only, not generalization.
* Qiyās licenses eligibility only, not generation.
* No new FailureCode members; no new runtime dependencies.
* assess_license() is pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.mu_chain import (
    OmegaGovernanceState,
    ResidualGovernanceVerdict,
)
from taaqqul_slot_geometry.weight.weight_fit import (
    WEIGHT_FIT_RANK_CEILING,
    WeightFitCandidate,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for PR-14 — same as WEIGHT_FIT_RANK_CEILING.
#: No boundary verdict may emit a rank above this value (docs/25 §5).
LICENSE_BOUNDARY_RANK_CEILING: Rank = WEIGHT_FIT_RANK_CEILING


# ---------------------------------------------------------------------------
# LicenseBoundaryKind — the three boundary kinds
# ---------------------------------------------------------------------------


class LicenseBoundaryKind(StrEnum):
    """The three licensing boundary kinds (docs/25 §2)."""

    LEXICAL = "LEXICAL"
    SAMAA = "SAMAA"
    QIYAS = "QIYAS"


# ---------------------------------------------------------------------------
# BoundaryEvidence — required by assess_license()
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BoundaryEvidence:
    """Evidence required for a licensing boundary assessment (docs/25 §3.3).

    All boundary kinds require:
    * ``kind`` — which boundary is being assessed.
    * ``attestation`` — the evidence surface (non-empty).
    * ``evidence_rank`` — the rank of the evidence (bounded).
    * ``domain`` — the evidence domain.

    For QIYAS kind, additional fields are required:
    * ``preserved_root`` — the asl (non-empty for qiyās).
    * ``effective_description`` — the wasf (non-empty for qiyās).
    * ``no_disqualifying_difference`` — farq qādih absent (True for qiyās).
    """

    kind: LicenseBoundaryKind
    attestation: str
    evidence_rank: Rank
    domain: str
    # Qiyās-specific (optional for LEXICAL/SAMAA)
    preserved_root: str = ""
    effective_description: str = ""
    no_disqualifying_difference: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.kind, LicenseBoundaryKind):
            raise WeightCarrierSchemaError(
                "BoundaryEvidence.kind must be a LicenseBoundaryKind member "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.attestation, str) or not self.attestation.strip():
            raise WeightCarrierSchemaError(
                "BoundaryEvidence.attestation must be a non-empty string "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.evidence_rank, Rank):
            raise WeightCarrierSchemaError(
                "BoundaryEvidence.evidence_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.evidence_rank > LICENSE_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "BoundaryEvidence.evidence_rank must not exceed "
                f"{LICENSE_BOUNDARY_RANK_CEILING.name} "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.domain, str) or not self.domain.strip():
            raise WeightCarrierSchemaError(
                "BoundaryEvidence.domain must be a non-empty string "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )


# ---------------------------------------------------------------------------
# LicensingBoundaryVerdict — the boundary eligibility output
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LicensingBoundaryVerdict:
    """The output carrier of :func:`assess_license` — a boundary eligibility assessment.

    docs/25 §4: LicensingBoundaryVerdict carries the eligibility verdict for a
    WeightFitCandidate against a licensing boundary. It tells whether the form
    may approach that boundary — nothing more. It does NOT carry meaning,
    madlul, ifādah, agency, hukm, reality, generated forms, lexical entry
    content, weight family, weight discovery algorithm, extra-letter license,
    augmentation category, or ContractableUnitGeometry.

    Fields:
    * ``source`` — the WeightFitCandidate that was assessed.
    * ``boundary_kind`` — which boundary was assessed.
    * ``eligibility_verdict`` — the boundary assessment (non-empty).
    * ``eligibility_rank`` — the verdict rank, bounded to the ceiling.
    * ``evidence_summary`` — what evidence was evaluated.
    """

    source: WeightFitCandidate
    boundary_kind: LicenseBoundaryKind
    eligibility_verdict: str
    eligibility_rank: Rank
    evidence_summary: str

    def __post_init__(self) -> None:
        if not isinstance(self.source, WeightFitCandidate):
            raise WeightCarrierSchemaError(
                "LicensingBoundaryVerdict.source must be a WeightFitCandidate — "
                f"boundary assessment without a fit is ungated "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.boundary_kind, LicenseBoundaryKind):
            raise WeightCarrierSchemaError(
                "LicensingBoundaryVerdict.boundary_kind must be a "
                f"LicenseBoundaryKind member ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.eligibility_verdict, str) or not self.eligibility_verdict.strip():
            raise WeightCarrierSchemaError(
                "LicensingBoundaryVerdict.eligibility_verdict must be a non-empty "
                f"string ({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.eligibility_rank, Rank):
            raise WeightCarrierSchemaError(
                "LicensingBoundaryVerdict.eligibility_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.eligibility_rank > LICENSE_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "LicensingBoundaryVerdict.eligibility_rank must not exceed "
                f"{LICENSE_BOUNDARY_RANK_CEILING.name} — no rank promotion "
                f"without a gate ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.evidence_summary, str) or not self.evidence_summary.strip():
            raise WeightCarrierSchemaError(
                "LicensingBoundaryVerdict.evidence_summary must be a non-empty "
                f"string ({FailureCode.TRACE_MISSING.value})"
            )


# ---------------------------------------------------------------------------
# LicensingBoundaryResult — the value returned by assess_license()
# ---------------------------------------------------------------------------


class LicensingBoundaryState(StrEnum):
    """The outcome of an assess_license() operation (docs/25 §3.5)."""

    ELIGIBLE = "ELIGIBLE"
    REFUSED = "REFUSED"
    DEFERRED = "DEFERRED"


@dataclass(frozen=True, slots=True)
class LicensingBoundaryResult:
    """The bounded result or named refusal returned by :func:`assess_license`.

    Invariants (docs/25 §3.5):

    * ``state`` is ``ELIGIBLE`` **iff** ``failure_code`` is ``None`` and
      ``verdict`` is not ``None``.
    * A refusal carries a named FailureCode and no verdict.
    * A deferred result carries a named FailureCode and no verdict.
    * ``rank`` never exceeds LICENSE_BOUNDARY_RANK_CEILING.
    * ``residuals`` are always visible.
    * ``trace_ref`` is a reference, not an audit ledger commit.
    """

    state: LicensingBoundaryState
    failure_code: FailureCode | None
    verdict: LicensingBoundaryVerdict | None
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, LicensingBoundaryState):
            raise WeightCarrierSchemaError(
                "LicensingBoundaryResult.state must be a LicensingBoundaryState member"
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                "LicensingBoundaryResult.rank must be a Rank member"
            )
        if self.rank > LICENSE_BOUNDARY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "LicensingBoundaryResult.rank must not exceed "
                f"LICENSE_BOUNDARY_RANK_CEILING ({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "LicensingBoundaryResult.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "LicensingBoundaryResult.residuals entries must be Residual carriers"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "LicensingBoundaryResult.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        # State invariants
        if self.state is LicensingBoundaryState.ELIGIBLE:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "an ELIGIBLE LicensingBoundaryResult must not carry a FailureCode "
                    "(docs/25 §3.5)"
                )
            if self.verdict is None:
                raise WeightCarrierSchemaError(
                    "an ELIGIBLE LicensingBoundaryResult must carry a "
                    "LicensingBoundaryVerdict (docs/25 §3.5)"
                )
        elif self.state is LicensingBoundaryState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED LicensingBoundaryResult must carry a named FailureCode "
                    "(docs/25 §3.5)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "LicensingBoundaryResult.failure_code must be a FailureCode member"
                )
            if self.verdict is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED LicensingBoundaryResult must not carry a verdict "
                    "(docs/25 §3.5)"
                )
        elif self.state is LicensingBoundaryState.DEFERRED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a DEFERRED LicensingBoundaryResult must carry a named FailureCode "
                    "(docs/25 §3.5)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "LicensingBoundaryResult.failure_code must be a FailureCode member"
                )
            if self.verdict is not None:
                raise WeightCarrierSchemaError(
                    "a DEFERRED LicensingBoundaryResult must not carry a verdict "
                    "(docs/25 §3.5)"
                )


# ---------------------------------------------------------------------------
# assess_license() — the licensing boundary operation
# ---------------------------------------------------------------------------


def assess_license(
    candidate: WeightFitCandidate,
    evidence: BoundaryEvidence,
    governance: ResidualGovernanceVerdict,
) -> LicensingBoundaryResult:
    """Licensing boundary assessment — boundary eligibility verdict.

    A pure function: evaluates whether the form described by a
    :class:`WeightFitCandidate` is eligible to approach a licensing
    boundary, producing a :class:`LicensingBoundaryResult`.

    Input boundary (docs/25 §3.2):

    * Accepts ONLY a WeightFitCandidate.
    * Refuses all other input types with a named FailureCode.

    Evidence requirement (docs/25 §3.3):

    * Requires a valid BoundaryEvidence.

    Governance requirement (docs/25 §3.4):

    * Requires a GRANTED :class:`ResidualGovernanceVerdict`.
    * Non-GRANTED governance produces a named refusal or deferral.

    Output:

    * On success: ELIGIBLE with a LicensingBoundaryVerdict.
    * On refusal: REFUSED with a named FailureCode.
    * On deferral: DEFERRED with a named FailureCode.

    This function is pure: no I/O, no ledger writes, no network.
    """
    # --- Input boundary enforcement ---
    if not isinstance(candidate, WeightFitCandidate):
        return LicensingBoundaryResult(
            state=LicensingBoundaryState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="assess_license/refused/input_boundary",
        )

    if not isinstance(evidence, BoundaryEvidence):
        return LicensingBoundaryResult(
            state=LicensingBoundaryState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="assess_license/refused/evidence_missing",
        )

    if not isinstance(governance, ResidualGovernanceVerdict):
        return LicensingBoundaryResult(
            state=LicensingBoundaryState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="assess_license/refused/governance_missing",
        )

    # --- Governance enforcement (docs/25 §3.4, inherits PR-12 §5) ---
    if governance.state is OmegaGovernanceState.REJECTED:
        return LicensingBoundaryResult(
            state=LicensingBoundaryState.REFUSED,
            failure_code=governance.failure_code or FailureCode.HIDDEN_RESIDUAL,
            verdict=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="assess_license/refused/governance_rejected",
        )

    if governance.state is OmegaGovernanceState.BLOCKED:
        return LicensingBoundaryResult(
            state=LicensingBoundaryState.REFUSED,
            failure_code=governance.failure_code or FailureCode.BLOCKING_RESIDUAL_PRESENT,
            verdict=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="assess_license/refused/governance_blocked",
        )

    if governance.state is OmegaGovernanceState.DEFERRED:
        return LicensingBoundaryResult(
            state=LicensingBoundaryState.DEFERRED,
            failure_code=governance.failure_code or FailureCode.GATE_REQUIRED,
            verdict=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="assess_license/deferred/governance_deferred",
        )

    # --- GRANTED: proceed with boundary assessment ---

    # Bound the rank
    eligibility_rank = RankLattice.meet(
        governance.granted_rank, evidence.evidence_rank, LICENSE_BOUNDARY_RANK_CEILING
    )

    # --- Kind-specific assessment ---
    boundary_kind = evidence.kind

    if boundary_kind is LicenseBoundaryKind.QIYAS:
        # Qiyās requires three conditions (docs/25 §7.2)
        if not evidence.preserved_root.strip():
            return LicensingBoundaryResult(
                state=LicensingBoundaryState.REFUSED,
                failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
                verdict=None,
                rank=Rank.ZERO,
                residuals=governance.residuals,
                trace_ref="assess_license/refused/qiyas_no_preserved_root",
            )
        if not evidence.effective_description.strip():
            return LicensingBoundaryResult(
                state=LicensingBoundaryState.REFUSED,
                failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
                verdict=None,
                rank=Rank.ZERO,
                residuals=governance.residuals,
                trace_ref="assess_license/refused/qiyas_no_effective_description",
            )
        if not evidence.no_disqualifying_difference:
            return LicensingBoundaryResult(
                state=LicensingBoundaryState.REFUSED,
                failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
                verdict=None,
                rank=Rank.ZERO,
                residuals=governance.residuals,
                trace_ref="assess_license/refused/qiyas_disqualifying_difference",
            )

    if boundary_kind is LicenseBoundaryKind.SAMAA and not evidence.attestation.strip():
        # Defense-in-depth: BoundaryEvidence birth guard already refuses empty
        # attestation, so this branch is unreachable under normal construction.
        # Retained as a constitutional safety net against future refactoring.
        return LicensingBoundaryResult(
            state=LicensingBoundaryState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="assess_license/refused/samaa_no_attestation",
        )

    # --- Construct the boundary verdict ---
    verdict = LicensingBoundaryVerdict(
        source=candidate,
        boundary_kind=boundary_kind,
        eligibility_verdict=f"boundary_eligible:{boundary_kind.value}",
        eligibility_rank=eligibility_rank,
        evidence_summary=f"{boundary_kind.value}:{evidence.attestation}",
    )

    return LicensingBoundaryResult(
        state=LicensingBoundaryState.ELIGIBLE,
        failure_code=None,
        verdict=verdict,
        rank=eligibility_rank,
        residuals=governance.residuals,
        trace_ref=f"assess_license/eligible/{boundary_kind.value}/{candidate.identity}",
    )


__all__ = [
    "LICENSE_BOUNDARY_RANK_CEILING",
    "BoundaryEvidence",
    "LicenseBoundaryKind",
    "LicensingBoundaryResult",
    "LicensingBoundaryState",
    "LicensingBoundaryVerdict",
    "assess_license",
]
