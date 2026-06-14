"""Mutabaqah / Tadammun / Iltizam Candidate — PR-D2.

PR-D2 binding of ``docs/38_MUTABAQAH_TADAMMUN_ILTIZAM_CANDIDATE_LAW.md``.

This module establishes the three dalalah relation candidates —
correspondence (mutabaqah), inclusion (tadammun), and entailment
(iltizam) — built on the proven semantic slot geometry (PR-D1) and
bounded by maqam/context readiness (PR-D1.2). These are *candidates
only*, never final meaning.

PR-D2 consumes **both**:
1. MufradSemanticSlotGeometryVerdict (PROVEN) — SemanticSlotFrame.
2. MaqamContextBoundaryVerdict (PROVEN) — MaqamContextFrame.

Constitutional invariants:

* MutabaqahCandidate ≠ Meaning.
* MutabaqahCandidate ≠ Ifadah.
* MutabaqahCandidate ≠ Hukm.
* MutabaqahCandidate ≠ Majaz verdict.
* MutabaqahCandidate ≠ Manqul verdict.
* TadammunCandidate ≠ arbitrary part decomposition.
* TadammunCandidate ≠ Meaning.
* TadammunCandidate ≠ ontological claim.
* IltizamCandidate ≠ free reasoning.
* IltizamCandidate ≠ Mafhum.
* IltizamCandidate ≠ Hukm.
* IltizamCandidate ≠ Qiyas result.
* IltizamCandidate ≠ Majaz license.
* IltizamCandidate ≠ Manqul license.
* BLOCKED_BY_QARINA ≠ HaqiqahAttempt failure.
* BLOCKED_BY_QARINA ≠ Majaz license.
* No Tadammun without Mutabaqah.
* No part without whole.
* No part outside identity_anchor.
* No Iltizam without LicensedNecessaryRelation.
* No rank promotion beyond MAQAM_CONTEXT_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* All operations are pure: no I/O, no ledger, no network.

Deferred residuals (binding):

* DALALAH_CANDIDATES_NOT_MEANING — candidates, not meaning.
* MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3 — closure not here.
* IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE — ifadah not here.
* HUKM_DEFERRED_UNTIL_IFADAH — hukm not here.
* MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT — majaz not here.
* MANQUL_DEFERRED_UNTIL_TRANSFER_GATE — manqul not here.
* MAFHUM_DEFERRED_UNTIL_MANTUQ — mafhum not here.
* BLOCKED_BY_QARINA_IS_CONSTRAINT_NOT_VERDICT — constraint only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.maqam_context_boundary import (
    MAQAM_CONTEXT_RANK_CEILING,
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
    "DALALAH_CANDIDATE_RANK_CEILING",
    "DalalahCandidateState",
    "DalalahCandidateVerdict",
    "IltizamCandidate",
    "MutabaqahCandidate",
    "NecessaryRelationType",
    "TadammunCandidate",
    "prove_dalalah_candidates",
]

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from maqam context boundary layer
# ---------------------------------------------------------------------------

DALALAH_CANDIDATE_RANK_CEILING: Rank = MAQAM_CONTEXT_RANK_CEILING

# ---------------------------------------------------------------------------
# NecessaryRelationType — licensed necessary relation types
# ---------------------------------------------------------------------------


class NecessaryRelationType(StrEnum):
    """Licensed necessary relation types for iltizam (docs/38 §4.4).

    Only these licensed types are permitted. Free reasoning,
    mafhum, hukm, and qiyas result are excluded.

    * SHART — Condition (shart).
    * SABAB — Cause (sabab).
    * MANI — Preventer (mani').
    * ILLA — Effective cause ('illa).
    * ATHAR_LAZIM — Necessary effect (athar lazim).
    * QARINA_LAZIMA — Necessary indicator (qarinah lazima).
    """

    SHART = "SHART"
    SABAB = "SABAB"
    MANI = "MANI"
    ILLA = "ILLA"
    ATHAR_LAZIM = "ATHAR_LAZIM"
    QARINA_LAZIMA = "QARINA_LAZIMA"


# ---------------------------------------------------------------------------
# DalalahCandidateState — verdict outcome
# ---------------------------------------------------------------------------


class DalalahCandidateState(StrEnum):
    """The outcome of a prove_dalalah_candidates() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# MutabaqahCandidate — correspondence candidate
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MutabaqahCandidate:
    """Correspondence candidate (docs/38 §4.1).

    Full-extension dalalah candidate: the signified corresponds to the
    full extension of the signifier's wad'. Built on SemanticSlotFrame
    + MaqamContextFrame.

    MutabaqahCandidate ≠ Meaning.
    MutabaqahCandidate ≠ Ifadah.
    MutabaqahCandidate ≠ Hukm.
    """

    semantic_slot_frame_ref: str
    maqam_context_frame_ref: str
    wad_evidence_ref: str
    kulli_juzii_axis: str
    formal_profile_ref: str
    correspondence_domain: str
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
        if not isinstance(self.wad_evidence_ref, str) or not self.wad_evidence_ref.strip():
            raise WeightCarrierSchemaError(
                "wad_evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.kulli_juzii_axis, str) or not self.kulli_juzii_axis.strip():
            raise WeightCarrierSchemaError(
                "kulli_juzii_axis must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.formal_profile_ref, str) or not self.formal_profile_ref.strip():
            raise WeightCarrierSchemaError(
                "formal_profile_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.correspondence_domain, str)
            or not self.correspondence_domain.strip()
        ):
            raise WeightCarrierSchemaError(
                "correspondence_domain must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > DALALAH_CANDIDATE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{DALALAH_CANDIDATE_RANK_CEILING.name}",
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
# TadammunCandidate — inclusion candidate
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TadammunCandidate:
    """Inclusion candidate (docs/38 §4.2).

    Part-of-whole dalalah candidate: the signified corresponds to a
    part of the full extension. No part without whole. No part
    outside identity_anchor.

    TadammunCandidate ≠ arbitrary part decomposition.
    TadammunCandidate ≠ Meaning.
    TadammunCandidate ≠ ontological claim.
    """

    mutabaqah_ref: str
    whole_identity_anchor: str
    part_designation: str
    inclusion_evidence: str
    domain_bounded: bool
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.mutabaqah_ref, str) or not self.mutabaqah_ref.strip():
            raise WeightCarrierSchemaError(
                "mutabaqah_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.whole_identity_anchor, str)
            or not self.whole_identity_anchor.strip()
        ):
            raise WeightCarrierSchemaError(
                "whole_identity_anchor must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.part_designation, str) or not self.part_designation.strip():
            raise WeightCarrierSchemaError(
                "part_designation must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.inclusion_evidence, str) or not self.inclusion_evidence.strip():
            raise WeightCarrierSchemaError(
                "inclusion_evidence must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.domain_bounded, bool):
            raise WeightCarrierSchemaError(
                "domain_bounded must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > DALALAH_CANDIDATE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{DALALAH_CANDIDATE_RANK_CEILING.name}",
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
# IltizamCandidate — entailment candidate
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class IltizamCandidate:
    """Entailment candidate (docs/38 §4.3).

    Necessary-relation dalalah candidate: the signified entails a
    necessary concomitant through a licensed relation type only.

    IltizamCandidate ≠ free reasoning.
    IltizamCandidate ≠ Mafhum.
    IltizamCandidate ≠ Hukm.
    IltizamCandidate ≠ Qiyas result.
    IltizamCandidate ≠ Majaz license.
    IltizamCandidate ≠ Manqul license.
    """

    mutabaqah_ref: str
    necessary_relation_type: NecessaryRelationType
    relation_evidence: str
    context_bounded: bool
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.mutabaqah_ref, str) or not self.mutabaqah_ref.strip():
            raise WeightCarrierSchemaError(
                "mutabaqah_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.necessary_relation_type, NecessaryRelationType):
            raise WeightCarrierSchemaError(
                f"necessary_relation_type must be a NecessaryRelationType member, "
                f"got {type(self.necessary_relation_type).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.relation_evidence, str) or not self.relation_evidence.strip():
            raise WeightCarrierSchemaError(
                "relation_evidence must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.context_bounded, bool):
            raise WeightCarrierSchemaError(
                "context_bounded must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > DALALAH_CANDIDATE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{DALALAH_CANDIDATE_RANK_CEILING.name}",
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
# DalalahCandidateVerdict — verdict containing all three candidates
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DalalahCandidateVerdict:
    """Output of prove_dalalah_candidates() (docs/38 §5).

    Contains all three dalalah relation candidates when PROVEN,
    or a named FailureCode when REFUSED.
    """

    mutabaqah: MutabaqahCandidate | None
    tadammun: TadammunCandidate | None
    iltizam: IltizamCandidate | None
    verdict_state: DalalahCandidateState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str


# ---------------------------------------------------------------------------
# Required deferred residuals (docs/38 §6)
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the 8 required deferred residuals for PR-D2."""
    return (
        Residual(
            name="DALALAH_CANDIDATES_NOT_MEANING",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Dalalah candidates (mutabaqah/tadammun/iltizam) are "
                "candidates only — never final meaning."
            ),
        ),
        Residual(
            name="MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Mufrad dalalah closure is not licensed here — "
                "deferred to PR-D3."
            ),
        ),
        Residual(
            name="IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Ifadah is not licensed here — deferred until "
                "mufrad dalalah closure (PR-D3 + PR-D4)."
            ),
        ),
        Residual(
            name="HUKM_DEFERRED_UNTIL_IFADAH",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Hukm is not licensed here — deferred until "
                "ifadah layer."
            ),
        ),
        Residual(
            name="MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Majaz is not licensed here — deferred until "
                "haqiqah attempt."
            ),
        ),
        Residual(
            name="MANQUL_DEFERRED_UNTIL_TRANSFER_GATE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Manqul is not licensed here — deferred until "
                "transfer gate."
            ),
        ),
        Residual(
            name="MAFHUM_DEFERRED_UNTIL_MANTUQ",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Mafhum is not licensed here — deferred until "
                "mantuq layer."
            ),
        ),
        Residual(
            name="BLOCKED_BY_QARINA_IS_CONSTRAINT_NOT_VERDICT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "BLOCKED_BY_QARINA from PR-D1.2 is a literal domain "
                "constraint candidate only — not a haqiqah attempt "
                "failure, not a majaz license."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# prove_dalalah_candidates() — the candidate operation
# ---------------------------------------------------------------------------


def prove_dalalah_candidates(
    semantic_slot_verdict: MufradSemanticSlotGeometryVerdict,
    maqam_context_verdict: MaqamContextBoundaryVerdict,
    correspondence_domain: str,
    part_designation: str,
    inclusion_evidence: str,
    necessary_relation_type: NecessaryRelationType,
    relation_evidence: str,
) -> DalalahCandidateVerdict:
    """Prove dalalah candidates (docs/38).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    The function validates both input verdicts, constructs all three
    dalalah relation candidates, and returns a verdict.

    Parameters
    ----------
    semantic_slot_verdict : MufradSemanticSlotGeometryVerdict
        Must be PROVEN with a SemanticSlotFrame.
    maqam_context_verdict : MaqamContextBoundaryVerdict
        Must be PROVEN with a MaqamContextFrame.
    correspondence_domain : str
        Bounded correspondence domain for mutabaqah.
    part_designation : str
        Part designation for tadammun.
    inclusion_evidence : str
        Evidence of inclusion relation for tadammun.
    necessary_relation_type : NecessaryRelationType
        Licensed necessary relation type for iltizam.
    relation_evidence : str
        Evidence of necessary relation for iltizam.

    Returns
    -------
    DalalahCandidateVerdict
        PROVEN with all three candidates on success; REFUSED with a
        named FailureCode on any violation.
    """
    _trace_base = "prove_dalalah_candidates"

    # --- Input boundary: semantic_slot_verdict type ---
    if not isinstance(semantic_slot_verdict, MufradSemanticSlotGeometryVerdict):
        return DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_verdict_invalid_type",
        )

    # --- Input boundary: semantic verdict must be PROVEN ---
    if semantic_slot_verdict.verdict_state is not MufradSemanticState.PROVEN:
        return DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_verdict_not_proven",
        )

    # --- Input boundary: semantic candidate must be a SemanticSlotFrame ---
    if not isinstance(semantic_slot_verdict.candidate, SemanticSlotFrame):
        return DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_frame_invalid_type",
        )

    # --- Input boundary: maqam_context_verdict type ---
    if not isinstance(maqam_context_verdict, MaqamContextBoundaryVerdict):
        return DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_verdict_invalid_type",
        )

    # --- Input boundary: maqam verdict must be PROVEN ---
    if maqam_context_verdict.verdict_state is not MaqamContextState.PROVEN:
        return DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_verdict_not_proven",
        )

    # --- Input boundary: maqam candidate must be a MaqamContextFrame ---
    if not isinstance(maqam_context_verdict.candidate, MaqamContextFrame):
        return DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/maqam_frame_invalid_type",
        )

    # --- Input boundary: string fields ---
    _string_checks = {
        "correspondence_domain": correspondence_domain,
        "part_designation": part_designation,
        "inclusion_evidence": inclusion_evidence,
        "relation_evidence": relation_evidence,
    }
    for field_name, field_value in _string_checks.items():
        if not isinstance(field_value, str) or not field_value.strip():
            return DalalahCandidateVerdict(
                mutabaqah=None,
                tadammun=None,
                iltizam=None,
                verdict_state=DalalahCandidateState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref=f"{_trace_base}/refused/{field_name}_empty",
            )

    # --- Input boundary: necessary_relation_type enum ---
    if not isinstance(necessary_relation_type, NecessaryRelationType):
        return DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/necessary_relation_type_invalid",
        )

    # --- Extract frame references ---
    slot_frame: SemanticSlotFrame = semantic_slot_verdict.candidate
    maqam_frame: MaqamContextFrame = maqam_context_verdict.candidate

    # --- Identity-continuity check (PR-D2.1) ---
    if maqam_frame.semantic_slot_frame_ref != slot_frame.trace_ref:
        return DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=(
                f"{_trace_base}/refused/"
                "identity_broken/semantic_maqam_frame_mismatch"
            ),
        )

    # --- Compute rank (meet of CANDIDATE with ceiling) ---
    verdict_rank = RankLattice.meet(Rank.CANDIDATE, DALALAH_CANDIDATE_RANK_CEILING)

    # --- Build deferred residuals ---
    deferred_residuals = _build_deferred_residuals()

    # --- Check residual governance ---
    for r in deferred_residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return DalalahCandidateVerdict(
                mutabaqah=None,
                tadammun=None,
                iltizam=None,
                verdict_state=DalalahCandidateState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return DalalahCandidateVerdict(
                mutabaqah=None,
                tadammun=None,
                iltizam=None,
                verdict_state=DalalahCandidateState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=deferred_residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- Construct MutabaqahCandidate ---
    mutabaqah = MutabaqahCandidate(
        semantic_slot_frame_ref=slot_frame.trace_ref,
        maqam_context_frame_ref=maqam_frame.trace_ref,
        wad_evidence_ref=slot_frame.wad_evidence.evidence_ref,
        kulli_juzii_axis=slot_frame.kulli_juzii_axis.axis.value,
        formal_profile_ref=slot_frame.per_unit_profile.trace_ref,
        correspondence_domain=correspondence_domain,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven/mutabaqah",
    )

    # --- Construct TadammunCandidate (no part without whole) ---
    tadammun = TadammunCandidate(
        mutabaqah_ref=mutabaqah.trace_ref,
        whole_identity_anchor=slot_frame.dal_identity_ref,
        part_designation=part_designation,
        inclusion_evidence=inclusion_evidence,
        domain_bounded=True,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven/tadammun",
    )

    # --- Construct IltizamCandidate (licensed relation only) ---
    iltizam = IltizamCandidate(
        mutabaqah_ref=mutabaqah.trace_ref,
        necessary_relation_type=necessary_relation_type,
        relation_evidence=relation_evidence,
        context_bounded=True,
        rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven/iltizam",
    )

    return DalalahCandidateVerdict(
        mutabaqah=mutabaqah,
        tadammun=tadammun,
        iltizam=iltizam,
        verdict_state=DalalahCandidateState.PROVEN,
        failure_code=None,
        verdict_rank=verdict_rank,
        residuals=deferred_residuals,
        trace_ref=f"{_trace_base}/proven",
    )
