"""Maqam / Context Boundary Readiness — PR-D1.2.

PR-D1.2 binding of ``docs/37_MAQAM_CONTEXT_BOUNDARY_READINESS_LAW.md``.

This module establishes the constitutional boundary constraints that make
dalalah operations (mutabaqah/tadammun/iltizam) *bounded* — domain of
usage, wad' scope constraint, discourse register, technical domain,
qarinah readiness, blocker audit, and literal domain constraint — without
performing any dalalah operation.

PR-D1.2 consumes SemanticSlotFrame (from PR-D1) and produces
MaqamContextFrame — a carrier that proves the boundary constraints
without meaning, dalalah operations, ifadah, hukm, or speaker intent.

Constitutional invariants:

* MaqamContextBoundary ≠ Meaning.
* MaqamContextBoundary ≠ Dalalah.
* MaqamContextBoundary ≠ Ifadah.
* MaqamContextBoundary ≠ SpeakerIntent.
* MaqamContextBoundary ≠ Majaz.
* MaqamContextBoundary ≠ Manqul.
* MaqamContextBoundary ≠ Hukm.
* MaqamContextBoundary ≠ Tanzil.
* MaqamContextBoundary ≠ Mutabaqah.
* MaqamContextBoundary ≠ Tadammun.
* MaqamContextBoundary ≠ Iltizam.
* DiscourseDomainCandidate ≠ semantic content.
* UsageRegisterCandidate ≠ meaning determination.
* TechnicalDomainCandidate ≠ technical definition.
* QarinaReadiness ≠ qarinah application.
* BlockerCandidateSet ≠ blocker verdict.
* LiteralDomainConstraint ≠ haqiqah verdict.
* WadScopeConstraint ≠ wad' assignment.
* No rank promotion beyond SEMANTIC_SLOT_GEOMETRY_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* All operations are pure: no I/O, no ledger, no network.

Deferred residuals (binding):

* MAQAM_CONTEXT_BOUNDARY_NOT_DALALAH — boundary, not operation.
* MUTABAQAH_DEFERRED_TO_PR_D2 — mutabaqah not licensed here.
* TADAMMUN_DEFERRED_TO_PR_D2 — tadammun not licensed here.
* ILTIZAM_DEFERRED_TO_PR_D2 — iltizam not licensed here.
* MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3 — closure not here.
* IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE — ifadah not here.
* MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT — majaz not here.
* MANQUL_DEFERRED_UNTIL_TRANSFER_GATE — manqul not here.
* SPEAKER_INTENT_DEFERRED_UNTIL_IFADAH — speaker intent not here.
* QARINA_APPLICATION_DEFERRED — qarinah application not here.
* BLOCKER_VERDICT_DEFERRED — blocker verdict not here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.mufrad_semantic_slot_geometry import (
    SEMANTIC_SLOT_GEOMETRY_RANK_CEILING,
    MufradSemanticSlotGeometryVerdict,
    MufradSemanticState,
    SemanticSlotFrame,
)

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from semantic slot geometry layer
# ---------------------------------------------------------------------------

MAQAM_CONTEXT_RANK_CEILING: Rank = SEMANTIC_SLOT_GEOMETRY_RANK_CEILING


# ---------------------------------------------------------------------------
# DiscourseDomainType — domain classification
# ---------------------------------------------------------------------------


class DiscourseDomainType(StrEnum):
    """Discourse domain type — structural classification only.

    Classifies the domain of discourse without determining meaning.
    * LUGHAWI — linguistic domain (language-internal).
    * URFI — customary/conventional domain.
    * ISTILAHI — technical/terminological domain.
    * SHARI — legal/normative domain.
    * AQLI — rational/intellectual domain.
    """

    LUGHAWI = "LUGHAWI"
    URFI = "URFI"
    ISTILAHI = "ISTILAHI"
    SHARI = "SHARI"
    AQLI = "AQLI"


# ---------------------------------------------------------------------------
# UsageRegisterType — register classification
# ---------------------------------------------------------------------------


class UsageRegisterType(StrEnum):
    """Usage register type — structural classification only.

    Classifies the register of usage without meaning determination.
    * HAQIQI — literal usage register.
    * MAJAZI_READY — figurative usage readiness (not majaz itself).
    * KINAI_READY — metonymic usage readiness (not kinayah itself).
    * TECHNICAL — technical register.
    """

    HAQIQI = "HAQIQI"
    MAJAZI_READY = "MAJAZI_READY"
    KINAI_READY = "KINAI_READY"
    TECHNICAL = "TECHNICAL"


# ---------------------------------------------------------------------------
# LiteralConstraintType — literal domain constraint type
# ---------------------------------------------------------------------------


class LiteralConstraintType(StrEnum):
    """Literal domain constraint type.

    Classifies constraints on the literal (haqiqah) domain.
    * UNCONSTRAINED — no constraint on literal domain.
    * NARROWED_BY_CONTEXT — context narrows literal domain.
    * BLOCKED_BY_QARINA — qarinah blocks literal domain.
    * TECHNICAL_OVERRIDE — technical convention overrides.
    """

    UNCONSTRAINED = "UNCONSTRAINED"
    NARROWED_BY_CONTEXT = "NARROWED_BY_CONTEXT"
    BLOCKED_BY_QARINA = "BLOCKED_BY_QARINA"
    TECHNICAL_OVERRIDE = "TECHNICAL_OVERRIDE"


# ---------------------------------------------------------------------------
# WadScopeType — wad' scope constraint type
# ---------------------------------------------------------------------------


class WadScopeType(StrEnum):
    """Wad' scope constraint type.

    Classifies the scope narrowing applied to wad' (conventional
    assignment) evidence. This is scope classification, not meaning.
    * ORIGINAL — original wad' scope, no narrowing.
    * NARROWED_URFI — narrowed by customary usage.
    * NARROWED_ISTILAHI — narrowed by technical convention.
    * NARROWED_SHARI — narrowed by legal usage.
    * TRANSFERRED — scope transferred (naql-ready, not naql itself).
    """

    ORIGINAL = "ORIGINAL"
    NARROWED_URFI = "NARROWED_URFI"
    NARROWED_ISTILAHI = "NARROWED_ISTILAHI"
    NARROWED_SHARI = "NARROWED_SHARI"
    TRANSFERRED = "TRANSFERRED"


# ---------------------------------------------------------------------------
# MaqamContextState — verdict outcome
# ---------------------------------------------------------------------------


class MaqamContextState(StrEnum):
    """The outcome of a prove_maqam_context_boundary() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# DiscourseDomainCandidate — discourse domain classification
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DiscourseDomainCandidate:
    """Discourse domain classification (docs/37 §5.2).

    Classifies the discourse domain without determining meaning.

    DiscourseDomainCandidate ≠ semantic content.
    """

    domain_type: DiscourseDomainType
    evidence_ref: str
    rank: Rank
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.domain_type, DiscourseDomainType):
            raise WeightCarrierSchemaError(
                f"domain_type must be a DiscourseDomainType member, "
                f"got {type(self.domain_type).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise WeightCarrierSchemaError(
                "evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > MAQAM_CONTEXT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{MAQAM_CONTEXT_RANK_CEILING.name}",
                FailureCode.RANK_EXCEEDS_CEILING,
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# UsageRegisterCandidate — register classification
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class UsageRegisterCandidate:
    """Usage register classification (docs/37 §5.3).

    Classifies the register of usage without meaning determination.

    UsageRegisterCandidate ≠ meaning determination.
    """

    register_type: UsageRegisterType
    evidence_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.register_type, UsageRegisterType):
            raise WeightCarrierSchemaError(
                f"register_type must be a UsageRegisterType member, "
                f"got {type(self.register_type).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise WeightCarrierSchemaError(
                "evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# TechnicalDomainCandidate — technical domain marker
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TechnicalDomainCandidate:
    """Technical domain marker (docs/37 §5.4).

    Marks whether the unit belongs to a technical domain.

    TechnicalDomainCandidate ≠ technical definition.
    """

    domain_name: str
    is_technical: bool
    evidence_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.domain_name, str) or not self.domain_name.strip():
            raise WeightCarrierSchemaError(
                "domain_name must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.is_technical, bool):
            raise WeightCarrierSchemaError(
                "is_technical must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise WeightCarrierSchemaError(
                "evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# QarinaReadinessCarrier — qarinah readiness
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class QarinaReadinessCarrier:
    """Qarinah readiness carrier (docs/37 §5.5).

    Readiness for qarinah (contextual indicator) — not the qarinah
    itself and not its application.

    QarinaReadinessCarrier ≠ qarinah application.
    """

    has_potential_qarina: bool
    qarina_type_readiness: str
    blocks_literal: bool
    evidence_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.has_potential_qarina, bool):
            raise WeightCarrierSchemaError(
                "has_potential_qarina must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.qarina_type_readiness, str)
            or not self.qarina_type_readiness.strip()
        ):
            raise WeightCarrierSchemaError(
                "qarina_type_readiness must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.blocks_literal, bool):
            raise WeightCarrierSchemaError(
                "blocks_literal must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise WeightCarrierSchemaError(
                "evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# BlockerCandidateSet — blocker candidate set
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BlockerCandidateSet:
    """Blocker candidate set (docs/37 §5.6).

    Candidate set of potential blockers (mawani') — not verdicts.

    BlockerCandidateSet ≠ blocker verdict.
    """

    blocker_count: int
    blocker_types: tuple[str, ...]
    all_audited: bool
    evidence_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.blocker_count, int) or self.blocker_count < 0:
            raise WeightCarrierSchemaError(
                "blocker_count must be a non-negative int",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.blocker_types, tuple):
            raise WeightCarrierSchemaError(
                "blocker_types must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        for bt in self.blocker_types:
            if not isinstance(bt, str) or not bt.strip():
                raise WeightCarrierSchemaError(
                    "Each blocker_type must be a non-empty string",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        if not isinstance(self.all_audited, bool):
            raise WeightCarrierSchemaError(
                "all_audited must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise WeightCarrierSchemaError(
                "evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# LiteralDomainConstraint — literal domain constraint
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LiteralDomainConstraint:
    """Literal domain constraint (docs/37 §5.7).

    Constraint on literal (haqiqah) domain — not a verdict.

    LiteralDomainConstraint ≠ haqiqah verdict.
    """

    constraint_type: LiteralConstraintType
    domain_ref: str
    evidence_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.constraint_type, LiteralConstraintType):
            raise WeightCarrierSchemaError(
                f"constraint_type must be a LiteralConstraintType member, "
                f"got {type(self.constraint_type).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.domain_ref, str) or not self.domain_ref.strip():
            raise WeightCarrierSchemaError(
                "domain_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise WeightCarrierSchemaError(
                "evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# WadScopeConstraint — wad' scope constraint
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WadScopeConstraint:
    """Wad' scope constraint (docs/37 §5.8).

    Constraint on wad' scope — narrower than origin domain.

    WadScopeConstraint ≠ wad' assignment.
    """

    scope_type: WadScopeType
    narrowing_evidence: str
    evidence_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.scope_type, WadScopeType):
            raise WeightCarrierSchemaError(
                f"scope_type must be a WadScopeType member, "
                f"got {type(self.scope_type).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.narrowing_evidence, str)
            or not self.narrowing_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "narrowing_evidence must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise WeightCarrierSchemaError(
                "evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# MaqamContextFrame — the constitutional frame
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MaqamContextFrame:
    """The constitutional frame for maqam/context boundary readiness
    (docs/37 §5.1).

    Every MaqamContextFrame proves that a semantic slot has the
    constitutional boundary constraints needed for dalalah operations —
    discourse domain, usage register, technical domain, qarinah
    readiness, blocker audit, literal domain constraint, and wad'
    scope constraint.

    MaqamContextFrame is boundary, never dalalah operation.
    MaqamContextFrame ≠ meaning.
    MaqamContextFrame ≠ Mutabaqah.
    MaqamContextFrame ≠ Tadammun.
    MaqamContextFrame ≠ Iltizam.
    MaqamContextFrame opens PR-D2 readiness only.
    MaqamContextFrame does not open Ifadah.
    """

    semantic_slot_frame_ref: str
    discourse_domain: DiscourseDomainCandidate
    usage_register: UsageRegisterCandidate
    technical_domain: TechnicalDomainCandidate
    speaker_position: str
    addressee_position: str
    textual_context_window: str
    qarina_readiness: QarinaReadinessCarrier
    blocker_candidate_set: BlockerCandidateSet
    literal_domain_constraint: LiteralDomainConstraint
    wad_scope_constraint: WadScopeConstraint
    style_relevance_constraint: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- String ref fields ---
        for field_name in (
            "semantic_slot_frame_ref",
            "speaker_position",
            "addressee_position",
            "textual_context_window",
            "style_relevance_constraint",
        ):
            val = getattr(self, field_name)
            if not isinstance(val, str) or not val.strip():
                raise WeightCarrierSchemaError(
                    f"{field_name} must be a non-empty string",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        # --- Sub-carrier types ---
        if not isinstance(self.discourse_domain, DiscourseDomainCandidate):
            raise WeightCarrierSchemaError(
                f"discourse_domain must be a DiscourseDomainCandidate, "
                f"got {type(self.discourse_domain).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.usage_register, UsageRegisterCandidate):
            raise WeightCarrierSchemaError(
                f"usage_register must be a UsageRegisterCandidate, "
                f"got {type(self.usage_register).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.technical_domain, TechnicalDomainCandidate):
            raise WeightCarrierSchemaError(
                f"technical_domain must be a TechnicalDomainCandidate, "
                f"got {type(self.technical_domain).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.qarina_readiness, QarinaReadinessCarrier):
            raise WeightCarrierSchemaError(
                f"qarina_readiness must be a QarinaReadinessCarrier, "
                f"got {type(self.qarina_readiness).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.blocker_candidate_set, BlockerCandidateSet):
            raise WeightCarrierSchemaError(
                f"blocker_candidate_set must be a BlockerCandidateSet, "
                f"got {type(self.blocker_candidate_set).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.literal_domain_constraint, LiteralDomainConstraint):
            raise WeightCarrierSchemaError(
                f"literal_domain_constraint must be a LiteralDomainConstraint, "
                f"got {type(self.literal_domain_constraint).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.wad_scope_constraint, WadScopeConstraint):
            raise WeightCarrierSchemaError(
                f"wad_scope_constraint must be a WadScopeConstraint, "
                f"got {type(self.wad_scope_constraint).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- rank ---
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > MAQAM_CONTEXT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{MAQAM_CONTEXT_RANK_CEILING.name}",
                FailureCode.RANK_EXCEEDS_CEILING,
            )
        # --- residuals ---
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "residuals must be a tuple",
                FailureCode.HIDDEN_RESIDUAL,
            )
        for r in self.residuals:
            if not isinstance(r, Residual):
                raise WeightCarrierSchemaError(
                    f"Each residual must be a Residual instance, "
                    f"got {type(r).__name__}",
                    FailureCode.HIDDEN_RESIDUAL,
                )
        # --- trace_ref ---
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# MaqamContextBoundaryVerdict — the proof output
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MaqamContextBoundaryVerdict:
    """The output of :func:`prove_maqam_context_boundary` (docs/37).

    Carries a proven MaqamContextFrame on success, or a named
    FailureCode on refusal. Does NOT carry meaning, dalalah
    operations, ifadah, hukm, or any semantic content.
    """

    candidate: MaqamContextFrame | None
    verdict_state: MaqamContextState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.verdict_state, MaqamContextState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be MaqamContextState, "
                f"got {type(self.verdict_state).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.verdict_rank, Rank):
            raise WeightCarrierSchemaError(
                f"verdict_rank must be a Rank member, "
                f"got {type(self.verdict_rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.verdict_rank > MAQAM_CONTEXT_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"verdict_rank {self.verdict_rank.name} exceeds ceiling "
                f"{MAQAM_CONTEXT_RANK_CEILING.name}",
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
                    f"Each residual must be a Residual instance, "
                    f"got {type(r).__name__}",
                    FailureCode.HIDDEN_RESIDUAL,
                )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )
        # --- State invariants ---
        if self.verdict_state is MaqamContextState.PROVEN:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "PROVEN verdict must have failure_code=None",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "PROVEN verdict must have a MaqamContextFrame",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if not isinstance(self.candidate, MaqamContextFrame):
                raise WeightCarrierSchemaError(
                    f"PROVEN candidate must be MaqamContextFrame, "
                    f"got {type(self.candidate).__name__}",
                    FailureCode.GATE_REQUIRED,
                )
        elif self.verdict_state is MaqamContextState.REFUSED:
            if self.failure_code is None:
                raise WeightCarrierSchemaError(
                    "REFUSED verdict must have a named FailureCode",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if not isinstance(self.failure_code, FailureCode):
                raise WeightCarrierSchemaError(
                    f"failure_code must be a FailureCode member, "
                    f"got {type(self.failure_code).__name__}",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if self.candidate is not None:
                raise WeightCarrierSchemaError(
                    "REFUSED verdict must have candidate=None",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )


# ---------------------------------------------------------------------------
# Required deferred residuals (constitutional binding)
# ---------------------------------------------------------------------------


def _build_deferred_residuals() -> tuple[Residual, ...]:
    """Build the required deferred residuals for maqam/context boundary."""
    return (
        Residual(
            name="MAQAM_CONTEXT_BOUNDARY_NOT_DALALAH",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "MaqamContextFrame is boundary for dalalah possibility, "
                "not dalalah operation — BOUNDARY ≠ dalalah"
            ),
        ),
        Residual(
            name="MUTABAQAH_DEFERRED_TO_PR_D2",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Mutabaqah (correspondence) is not licensed here — "
                "deferred to PR-D2 (Mutabaqah/Tadammun/Iltizam Candidate)."
            ),
        ),
        Residual(
            name="TADAMMUN_DEFERRED_TO_PR_D2",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Tadammun (inclusion) is not licensed here — "
                "deferred to PR-D2."
            ),
        ),
        Residual(
            name="ILTIZAM_DEFERRED_TO_PR_D2",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Iltizam (entailment) is not licensed here — "
                "deferred to PR-D2."
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
            name="SPEAKER_INTENT_DEFERRED_UNTIL_IFADAH",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Speaker intent is not licensed here — deferred "
                "until ifadah/mantuq layer."
            ),
        ),
        Residual(
            name="QARINA_APPLICATION_DEFERRED",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Qarinah application is not licensed here — "
                "readiness only, not application."
            ),
        ),
        Residual(
            name="BLOCKER_VERDICT_DEFERRED",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Blocker verdict is not licensed here — "
                "candidate audit only, not verdict."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# prove_maqam_context_boundary() — the boundary operation
# ---------------------------------------------------------------------------


def prove_maqam_context_boundary(
    semantic_slot_verdict: MufradSemanticSlotGeometryVerdict,
    discourse_domain_type: DiscourseDomainType,
    discourse_evidence_ref: str,
    usage_register_type: UsageRegisterType,
    usage_evidence_ref: str,
    technical_domain_name: str,
    is_technical: bool,
    technical_evidence_ref: str,
    speaker_position: str,
    addressee_position: str,
    textual_context_window: str,
    has_potential_qarina: bool,
    qarina_type_readiness: str,
    qarina_blocks_literal: bool,
    qarina_evidence_ref: str,
    blocker_count: int,
    blocker_types: tuple[str, ...],
    all_blockers_audited: bool,
    blocker_evidence_ref: str,
    literal_constraint_type: LiteralConstraintType,
    literal_domain_ref: str,
    literal_evidence_ref: str,
    wad_scope_type: WadScopeType,
    wad_narrowing_evidence: str,
    wad_scope_evidence_ref: str,
    style_relevance_constraint: str,
) -> MaqamContextBoundaryVerdict:
    """Prove maqam/context boundary readiness (docs/37).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    The function validates the SemanticSlotFrame verdict, constructs
    sub-carriers, assembles the MaqamContextFrame, and returns a
    verdict.

    Returns
    -------
    MaqamContextBoundaryVerdict
        PROVEN with a MaqamContextFrame on success; REFUSED with a
        named FailureCode on any violation.
    """
    _trace_base = "prove_maqam_context_boundary"

    # --- Input boundary: semantic_slot_verdict type ---
    if not isinstance(semantic_slot_verdict, MufradSemanticSlotGeometryVerdict):
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_verdict_invalid_type",
        )

    # --- Input boundary: verdict must be PROVEN ---
    if semantic_slot_verdict.verdict_state is not MufradSemanticState.PROVEN:
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_verdict_not_proven",
        )

    # --- Input boundary: candidate must be a SemanticSlotFrame ---
    if not isinstance(semantic_slot_verdict.candidate, SemanticSlotFrame):
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/slot_frame_invalid_type",
        )

    # --- Input boundary: enum types ---
    if not isinstance(discourse_domain_type, DiscourseDomainType):
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/discourse_domain_type_invalid",
        )
    if not isinstance(usage_register_type, UsageRegisterType):
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/usage_register_type_invalid",
        )
    if not isinstance(literal_constraint_type, LiteralConstraintType):
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/literal_constraint_type_invalid",
        )
    if not isinstance(wad_scope_type, WadScopeType):
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/wad_scope_type_invalid",
        )

    # --- Input boundary: string fields (non-empty) ---
    _string_checks = {
        "discourse_evidence_ref": discourse_evidence_ref,
        "usage_evidence_ref": usage_evidence_ref,
        "technical_domain_name": technical_domain_name,
        "technical_evidence_ref": technical_evidence_ref,
        "speaker_position": speaker_position,
        "addressee_position": addressee_position,
        "textual_context_window": textual_context_window,
        "qarina_type_readiness": qarina_type_readiness,
        "qarina_evidence_ref": qarina_evidence_ref,
        "blocker_evidence_ref": blocker_evidence_ref,
        "literal_domain_ref": literal_domain_ref,
        "literal_evidence_ref": literal_evidence_ref,
        "wad_narrowing_evidence": wad_narrowing_evidence,
        "wad_scope_evidence_ref": wad_scope_evidence_ref,
        "style_relevance_constraint": style_relevance_constraint,
    }
    for field_name, val in _string_checks.items():
        if not isinstance(val, str) or not val.strip():
            return MaqamContextBoundaryVerdict(
                candidate=None,
                verdict_state=MaqamContextState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref=f"{_trace_base}/refused/{field_name}_empty",
            )

    # --- Input boundary: bool fields ---
    for bool_name, bool_val in (
        ("is_technical", is_technical),
        ("has_potential_qarina", has_potential_qarina),
        ("qarina_blocks_literal", qarina_blocks_literal),
        ("all_blockers_audited", all_blockers_audited),
    ):
        if not isinstance(bool_val, bool):
            return MaqamContextBoundaryVerdict(
                candidate=None,
                verdict_state=MaqamContextState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref=f"{_trace_base}/refused/{bool_name}_invalid",
            )

    # --- Input boundary: blocker_count ---
    if not isinstance(blocker_count, int) or blocker_count < 0:
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/blocker_count_invalid",
        )

    # --- Input boundary: blocker_types ---
    if not isinstance(blocker_types, tuple):
        return MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/blocker_types_invalid",
        )

    # --- Rank bounding via lattice meet ---
    candidate_rank = RankLattice.meet(Rank.CANDIDATE, MAQAM_CONTEXT_RANK_CEILING)

    # --- Build deferred residuals ---
    residuals = _build_deferred_residuals()

    # --- Check residuals for HIDDEN_FORBIDDEN or BLOCKING ---
    for r in residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return MaqamContextBoundaryVerdict(
                candidate=None,
                verdict_state=MaqamContextState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return MaqamContextBoundaryVerdict(
                candidate=None,
                verdict_state=MaqamContextState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- Construct sub-carriers ---
    _trace_suffix = semantic_slot_verdict.candidate.semantic_category.value

    discourse_domain = DiscourseDomainCandidate(
        domain_type=discourse_domain_type,
        evidence_ref=discourse_evidence_ref,
        rank=candidate_rank,
        trace_ref=f"{_trace_base}/discourse_domain/{_trace_suffix}",
    )

    usage_register = UsageRegisterCandidate(
        register_type=usage_register_type,
        evidence_ref=usage_evidence_ref,
        trace_ref=f"{_trace_base}/usage_register/{_trace_suffix}",
    )

    technical_domain = TechnicalDomainCandidate(
        domain_name=technical_domain_name,
        is_technical=is_technical,
        evidence_ref=technical_evidence_ref,
        trace_ref=f"{_trace_base}/technical_domain/{_trace_suffix}",
    )

    qarina_readiness = QarinaReadinessCarrier(
        has_potential_qarina=has_potential_qarina,
        qarina_type_readiness=qarina_type_readiness,
        blocks_literal=qarina_blocks_literal,
        evidence_ref=qarina_evidence_ref,
        trace_ref=f"{_trace_base}/qarina_readiness/{_trace_suffix}",
    )

    blocker_set = BlockerCandidateSet(
        blocker_count=blocker_count,
        blocker_types=blocker_types,
        all_audited=all_blockers_audited,
        evidence_ref=blocker_evidence_ref,
        trace_ref=f"{_trace_base}/blocker_set/{_trace_suffix}",
    )

    literal_constraint = LiteralDomainConstraint(
        constraint_type=literal_constraint_type,
        domain_ref=literal_domain_ref,
        evidence_ref=literal_evidence_ref,
        trace_ref=f"{_trace_base}/literal_constraint/{_trace_suffix}",
    )

    wad_scope = WadScopeConstraint(
        scope_type=wad_scope_type,
        narrowing_evidence=wad_narrowing_evidence,
        evidence_ref=wad_scope_evidence_ref,
        trace_ref=f"{_trace_base}/wad_scope/{_trace_suffix}",
    )

    # --- Construct MaqamContextFrame ---
    frame = MaqamContextFrame(
        semantic_slot_frame_ref=semantic_slot_verdict.candidate.trace_ref,
        discourse_domain=discourse_domain,
        usage_register=usage_register,
        technical_domain=technical_domain,
        speaker_position=speaker_position,
        addressee_position=addressee_position,
        textual_context_window=textual_context_window,
        qarina_readiness=qarina_readiness,
        blocker_candidate_set=blocker_set,
        literal_domain_constraint=literal_constraint,
        wad_scope_constraint=wad_scope,
        style_relevance_constraint=style_relevance_constraint,
        rank=candidate_rank,
        residuals=residuals,
        trace_ref=f"{_trace_base}/proven/{_trace_suffix}",
    )

    return MaqamContextBoundaryVerdict(
        candidate=frame,
        verdict_state=MaqamContextState.PROVEN,
        failure_code=None,
        verdict_rank=candidate_rank,
        residuals=residuals,
        trace_ref=f"{_trace_base}/proven/{_trace_suffix}",
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "MAQAM_CONTEXT_RANK_CEILING",
    "BlockerCandidateSet",
    "DiscourseDomainCandidate",
    "DiscourseDomainType",
    "LiteralConstraintType",
    "LiteralDomainConstraint",
    "MaqamContextBoundaryVerdict",
    "MaqamContextFrame",
    "MaqamContextState",
    "QarinaReadinessCarrier",
    "TechnicalDomainCandidate",
    "UsageRegisterCandidate",
    "UsageRegisterType",
    "WadScopeConstraint",
    "WadScopeType",
    "prove_maqam_context_boundary",
]
