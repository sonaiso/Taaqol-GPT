"""Minimal WeightFit operation — PR-13 binding of docs/24.

PR-13 binding of ``docs/24_MINIMAL_WEIGHT_FIT_LAW.md``. This module
introduces:

* :class:`WeightFitState` — the three fit verdict states.
* :class:`WeightFitCandidate` — the bounded fit assessment output.
* :class:`WeightFitResult` — the value returned by :func:`weigh`.
* :func:`weigh` — the minimal weighing operation consuming only a
  :class:`~taaqqul_slot_geometry.weight.pre_weight.WeightReadinessCandidate`.

Constitutional invariants (docs/24):

* weigh() accepts ONLY a WeightReadinessCandidate.
* weigh() refuses PathKind, PathGateVerdict, raw carriers, and
  incomplete μ outputs.
* WeightFitCandidate is a pattern-space fit assessment, NOT
  LicensedWeight, meaning, agency, hukm, or reality.
* No rank promotion beyond WEIGHT_FIT_RANK_CEILING.
* Residual governance from PR-12 is respected.
* TraceRef remains a reference, not an audit ledger commit.
* No DiscoverWeightAlgorithm, no WeightFamilyCandidate.
* No lexical / samāʿ / qiyās licensing.
* No extra-letter licensing.
* No new FailureCode members; no new runtime dependencies.
* weigh() and WeightFitCandidate are pure: no I/O, no ledger, no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual
from taaqqul_slot_geometry.weight.carrier_core import (
    WeightCarrierBase,
    WeightCarrierSchemaError,
)
from taaqqul_slot_geometry.weight.mu_chain import (
    MU_CHAIN_RANK_CEILING,
    OmegaGovernanceState,
    ResidualGovernanceVerdict,
)
from taaqqul_slot_geometry.weight.pre_weight import WeightReadinessCandidate

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for the weigh() operation — same as MU_CHAIN_RANK_CEILING.
#: No fit result may emit a rank above this value (docs/24 §4).
WEIGHT_FIT_RANK_CEILING: Rank = MU_CHAIN_RANK_CEILING


# ---------------------------------------------------------------------------
# WeightFitCandidate — the bounded fit assessment
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WeightFitCandidate(WeightCarrierBase):
    """The output carrier of :func:`weigh` — a pattern-space fit assessment.

    docs/24 §3: WeightFitCandidate carries the fit verdict for a form
    against a pattern shape. It tells whether the form fits — nothing
    more. It does NOT carry meaning, agency, hukm, reality, lexical
    entry, samāʿ attestation, qiyās derivation, weight family, weight
    discovery algorithm, extra-letter license, or augmentation category.

    Fields beyond the 9 mandatory WeightCarrierBase fields:

    * ``source`` — the WeightReadinessCandidate that was weighed.
    * ``fit_verdict`` — the pattern-space fit assessment (non-empty).
    * ``fit_rank`` — the fit quality rank, bounded to the ceiling.
    """

    source: WeightReadinessCandidate
    fit_verdict: str
    fit_rank: Rank

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.source, WeightReadinessCandidate):
            raise WeightCarrierSchemaError(
                "WeightFitCandidate.source must be a WeightReadinessCandidate — "
                f"weighing without the pre-weight chain is ungated "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.fit_verdict, str) or not self.fit_verdict.strip():
            raise WeightCarrierSchemaError(
                "WeightFitCandidate.fit_verdict must be a non-empty string — "
                f"an erased fit verdict loses its trace "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.fit_rank, Rank):
            raise WeightCarrierSchemaError(
                "WeightFitCandidate.fit_rank must be a Rank member "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.fit_rank > WEIGHT_FIT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "WeightFitCandidate.fit_rank must not exceed "
                f"{WEIGHT_FIT_RANK_CEILING.name} — no rank promotion without a gate "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )


# ---------------------------------------------------------------------------
# WeightFitResult — the value returned by weigh()
# ---------------------------------------------------------------------------


class WeightFitState(StrEnum):
    """The outcome of a weigh() operation (docs/24 §2.4)."""

    FITTED = "FITTED"
    REFUSED = "REFUSED"
    DEFERRED = "DEFERRED"


@dataclass(frozen=True, slots=True)
class WeightFitResult:
    """The bounded fit result or named refusal returned by :func:`weigh`.

    Invariants (docs/24 §2.4):

    * ``state`` is ``FITTED`` **iff** ``failure_code`` is ``None`` and
      ``candidate`` is not ``None``.
    * A refusal carries a named FailureCode and no candidate.
    * A deferred result carries a named FailureCode and may not carry
      a candidate.
    * ``rank`` never exceeds WEIGHT_FIT_RANK_CEILING.
    * ``residuals`` are always visible.
    * ``trace_ref`` is a reference, not an audit ledger commit.
    """

    state: WeightFitState
    failure_code: FailureCode | None
    candidate: WeightFitCandidate | None
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, WeightFitState):
            raise WeightCarrierSchemaError(
                "WeightFitResult.state must be a WeightFitState member"
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                "WeightFitResult.rank must be a Rank member"
            )
        if self.rank > WEIGHT_FIT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                "WeightFitResult.rank must not exceed WEIGHT_FIT_RANK_CEILING "
                f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "WeightFitResult.residuals must be a tuple"
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    "WeightFitResult.residuals entries must be Residual carriers"
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "WeightFitResult.trace_ref must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )

        # State invariants
        if self.state is WeightFitState.FITTED:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "a FITTED WeightFitResult must not carry a FailureCode "
                    "(docs/24 §2.4)"
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "a FITTED WeightFitResult must carry a WeightFitCandidate "
                    "(docs/24 §2.4)"
                )
        elif self.state is WeightFitState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a REFUSED WeightFitResult must carry a named FailureCode "
                    "(docs/24 §2.4)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "WeightFitResult.failure_code must be a FailureCode member"
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "a REFUSED WeightFitResult must not carry a candidate "
                    "(docs/24 §2.4)"
                )
        elif self.state is WeightFitState.DEFERRED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "a DEFERRED WeightFitResult must carry a named FailureCode "
                    "(docs/24 §2.4)"
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    "WeightFitResult.failure_code must be a FailureCode member"
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "a DEFERRED WeightFitResult must not carry a candidate "
                    "(docs/24 §2.4)"
                )


# ---------------------------------------------------------------------------
# weigh() — the minimal weighing operation
# ---------------------------------------------------------------------------


def weigh(
    candidate: WeightReadinessCandidate,
    governance: ResidualGovernanceVerdict,
) -> WeightFitResult:
    """Minimal WeightFit operation — pattern-space fit assessment.

    A pure function: evaluates whether the form described by a
    :class:`WeightReadinessCandidate` fits its pattern shape,
    producing a :class:`WeightFitResult`.

    Input boundary (docs/24 §2.2):

    * Accepts ONLY a WeightReadinessCandidate.
    * Refuses all other input types with a named FailureCode.

    Governance requirement (docs/24 §2.3):

    * Requires a GRANTED :class:`ResidualGovernanceVerdict`.
    * Non-GRANTED governance produces a named refusal or deferral.

    Output:

    * On success: FITTED with a WeightFitCandidate.
    * On refusal: REFUSED with a named FailureCode.
    * On deferral: DEFERRED with a named FailureCode.

    This function is pure: no I/O, no ledger writes, no network.
    """
    # --- Input boundary enforcement ---
    if not isinstance(candidate, WeightReadinessCandidate):
        return WeightFitResult(
            state=WeightFitState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            candidate=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="weigh/refused/input_boundary",
        )

    if not isinstance(governance, ResidualGovernanceVerdict):
        return WeightFitResult(
            state=WeightFitState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            candidate=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="weigh/refused/governance_missing",
        )

    # --- Governance enforcement (docs/24 §2.3, inherits PR-12 §5) ---
    if governance.state is OmegaGovernanceState.REJECTED:
        return WeightFitResult(
            state=WeightFitState.REFUSED,
            failure_code=governance.failure_code or FailureCode.HIDDEN_RESIDUAL,
            candidate=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="weigh/refused/governance_rejected",
        )

    if governance.state is OmegaGovernanceState.BLOCKED:
        return WeightFitResult(
            state=WeightFitState.REFUSED,
            failure_code=governance.failure_code or FailureCode.BLOCKING_RESIDUAL_PRESENT,
            candidate=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="weigh/refused/governance_blocked",
        )

    if governance.state is OmegaGovernanceState.DEFERRED:
        return WeightFitResult(
            state=WeightFitState.DEFERRED,
            failure_code=governance.failure_code or FailureCode.GATE_REQUIRED,
            candidate=None,
            rank=Rank.ZERO,
            residuals=governance.residuals,
            trace_ref="weigh/deferred/governance_deferred",
        )

    # --- GRANTED: proceed with fit operation ---
    # Bound the rank: meet of (governance granted_rank, WEIGHT_FIT_RANK_CEILING)
    fit_rank = RankLattice.meet(governance.granted_rank, WEIGHT_FIT_RANK_CEILING)

    # Construct the fit candidate — the pattern-space fit assessment
    fit_candidate = WeightFitCandidate(
        value=candidate.value,
        type="weight_fit",
        origin="weigh_operation",
        identity=f"fit:{candidate.identity}",
        domain=candidate.domain,
        scope=candidate.scope,
        rank=candidate.rank,
        residuals=governance.residuals,
        trace=candidate.trace,
        source=candidate,
        fit_verdict="pattern_fit_assessed",
        fit_rank=fit_rank,
    )

    return WeightFitResult(
        state=WeightFitState.FITTED,
        failure_code=None,
        candidate=fit_candidate,
        rank=fit_rank,
        residuals=governance.residuals,
        trace_ref=f"weigh/fitted/{candidate.identity}",
    )


__all__ = [
    "WEIGHT_FIT_RANK_CEILING",
    "WeightFitCandidate",
    "WeightFitResult",
    "WeightFitState",
    "weigh",
]
