"""Mufrad Semantic Slot Geometry — PR-D1.

PR-D1 binding of ``docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md``.

This module introduces the constitutional structure that makes
singular dalalah *possible*: identity continuity, wad' evidence,
per-unit formal profile closure, kulli/juz'i axis verdict,
origin/branch geometry, and inter-frame relation readiness — without
performing any dalalah operation.

PR-D1 consumes FormalStyleCandidate (from PR-F8),
DalOnlyCandidate (PR-15), VerbalMadlulCandidate (PR-16),
ContractableUnitGeometry (PR-18), and FormalShapeClosure.CLOSED.
It produces SemanticSlotFrame — a carrier that proves the geometry
of dalalah possibility without meaning, dalalah operations,
ifadah, hukm, mantuq, mafhum, majaz, or manqul.

Constitutional invariants:

* SemanticSlotFrame ≠ meaning.
* SemanticSlotFrame ≠ dalalah operation.
* SemanticSlotFrame ≠ Mutabaqah.
* SemanticSlotFrame ≠ Tadammun.
* SemanticSlotFrame ≠ Iltizam.
* SemanticSlotFrame ≠ ifadah.
* Wad'Evidence ≠ lexical meaning.
* Wad'Evidence ≠ dictionary definition.
* IdentityContinuityProof ≠ semantic assertion.
* PerUnitFormalProfileClosure ≠ semantic derivation.
* KulliJuz'iAxisVerdict ≠ ontological claim.
* BranchLinkCandidate ≠ qiyas result.
* BranchLinkCandidate ≠ free reasoning.
* NaqlReadiness ≠ Naql.
* MajazReadiness ≠ Majaz.
* JamidAnchorSlot ≠ lexical meaning.
* MasdarSlot ≠ event occurrence.
* MushtaqSlot ≠ real agent.
* HarfOperatorSlot ≠ semantic relation.
* ReferenceSlot ≠ resolved referent.
* Semantic slot geometry is not dalalah.
* No rank promotion beyond FORMAL_SHAPE_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* All operations are pure: no I/O, no ledger, no network.
* No new FailureCode members; no new runtime dependencies.

Deferred residuals (binding):

* SEMANTIC_SLOT_GEOMETRY_NOT_DALALAH — geometry, not operation.
* MUTABAQAH_DEFERRED_TO_PR_D2 — mutabaqah not licensed here.
* TADAMMUN_DEFERRED_TO_PR_D2 — tadammun not licensed here.
* ILTIZAM_DEFERRED_TO_PR_D2 — iltizam not licensed here.
* MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3 — closure not here.
* IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE — ifadah not here.
* MANTUQ_DEFERRED_UNTIL_IFADAH — mantuq not here.
* MAFHUM_DEFERRED_UNTIL_MANTUQ — mafhum not here.
* MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT — majaz not here.
* MANQUL_DEFERRED_UNTIL_TRANSFER_GATE — manqul not here.
* TAWATUI_READINESS — inter-frame relation readiness stub.
* TASHKIK_READINESS — inter-frame relation readiness stub.
* TABAYUN_READINESS — inter-frame relation readiness stub.
* TARADUF_READINESS — inter-frame relation readiness stub.
* ISHTIRAK_READINESS — inter-frame relation readiness stub.
* NAQL_READINESS — inter-frame relation readiness stub.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.formal_shape import (
    FORMAL_SHAPE_RANK_CEILING,
    FormalShapeClosureState,
)

# ---------------------------------------------------------------------------
# Rank ceiling — inherits from formal shape layer
# ---------------------------------------------------------------------------

SEMANTIC_SLOT_GEOMETRY_RANK_CEILING: Rank = FORMAL_SHAPE_RANK_CEILING


# ---------------------------------------------------------------------------
# SemanticCategory — the five semantic slot kinds
# ---------------------------------------------------------------------------


class SemanticCategory(StrEnum):
    """Semantic slot category — structural classification only.

    Each category is a readiness classification, never meaning:
    * JAMID — entity anchoring readiness (not lexical meaning).
    * MASDAR — abstract transformation potential (not event occurrence).
    * MUSHTAQ — formal role-shape distribution (not real agency/patiency).
    * HARF — relational operator readiness (not semantic relation).
    * REFERENCE — reference search space (not resolved referent).
    """

    JAMID = "JAMID"
    MASDAR = "MASDAR"
    MUSHTAQ = "MUSHTAQ"
    HARF = "HARF"
    REFERENCE = "REFERENCE"


#: All semantic categories as a tuple.
SEMANTIC_CATEGORIES: tuple[SemanticCategory, ...] = tuple(SemanticCategory)


# ---------------------------------------------------------------------------
# WadOriginDomain — origin domain of conventional assignment
# ---------------------------------------------------------------------------


class WadOriginDomain(StrEnum):
    """Origin domain of wad' (conventional assignment).

    Classifies the domain from which conventional assignment evidence
    originates. This is evidence classification, not meaning.
    """

    LUGHAWI = "LUGHAWI"
    URFI = "URFI"
    ISTILAHI = "ISTILAHI"
    NAQL_READY = "NAQL_READY"


# ---------------------------------------------------------------------------
# WadEvidenceType — type of wad' evidence
# ---------------------------------------------------------------------------


class WadEvidenceType(StrEnum):
    """Type of wad' (conventional assignment) evidence.

    Classifies the evidence source. This is evidence classification,
    not meaning derivation.
    """

    SAMA = "SAMA"
    CORPUS = "CORPUS"
    TECHNICAL_CONVENTION = "TECHNICAL_CONVENTION"
    TEXTUAL_AUTHORITY = "TEXTUAL_AUTHORITY"


# ---------------------------------------------------------------------------
# KulliJuziiAxis — kulli/juz'i as verdict axis
# ---------------------------------------------------------------------------


class KulliJuziiAxis(StrEnum):
    """Kulli/juz'i classification axis — a verdict, not a label.

    KULLI: the signified can be predicated of many.
    JUZII: the signified is particular.
    """

    KULLI = "KULLI"
    JUZII = "JUZII"


# ---------------------------------------------------------------------------
# ParticularitySource — source of juz'i particularity
# ---------------------------------------------------------------------------


class ParticularitySource(StrEnum):
    """Source of juz'i particularity — structural classification.

    NOT_APPLICABLE: kulli (no particularity).
    WAD: particularity from conventional assignment (e.g. proper names).
    REFERENCE: particularity from reference (e.g. pronouns, demonstratives).
    CONTEXT: particularity from context (deferred to later layer).
    """

    NOT_APPLICABLE = "NOT_APPLICABLE"
    WAD = "WAD"
    REFERENCE = "REFERENCE"
    CONTEXT = "CONTEXT"


# ---------------------------------------------------------------------------
# MufradSemanticState — verdict outcome
# ---------------------------------------------------------------------------


class MufradSemanticState(StrEnum):
    """The outcome of a prove_mufrad_semantic_slot_geometry() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# WadEvidenceCarrier — conventional assignment evidence
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WadEvidenceCarrier:
    """Evidence of conventional assignment (docs/36 §4.2).

    Proves that the signifier has wad' evidence without carrying
    lexical meaning or dictionary definition. This is evidence
    classification, not meaning extraction.

    WadEvidenceCarrier ≠ lexical meaning.
    WadEvidenceCarrier ≠ dictionary definition.
    """

    origin_domain: WadOriginDomain
    evidence_type: WadEvidenceType
    scope: str
    evidence_ref: str
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.origin_domain, WadOriginDomain):
            raise WeightCarrierSchemaError(
                f"origin_domain must be a WadOriginDomain member, "
                f"got {type(self.origin_domain).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.evidence_type, WadEvidenceType):
            raise WeightCarrierSchemaError(
                f"evidence_type must be a WadEvidenceType member, "
                f"got {type(self.evidence_type).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.scope, str) or not self.scope.strip():
            raise WeightCarrierSchemaError(
                "scope must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.evidence_ref, str)
            or not self.evidence_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > SEMANTIC_SLOT_GEOMETRY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{SEMANTIC_SLOT_GEOMETRY_RANK_CEILING.name}",
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


# ---------------------------------------------------------------------------
# PerUnitFormalProfileClosure — formal layers closure proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PerUnitFormalProfileClosure:
    """Proves all formal layers are closed for this unit (docs/36 §4.3).

    Links to the five formal layer closure proofs. This is closure
    evidence, not semantic derivation.

    PerUnitFormalProfileClosure ≠ semantic derivation.
    """

    word_class_closure_ref: str
    weight_pattern_closure_ref: str
    inflection_closure_ref: str
    contract_slot_readiness_ref: str
    composition_participation_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        for field_name in (
            "word_class_closure_ref",
            "weight_pattern_closure_ref",
            "inflection_closure_ref",
            "contract_slot_readiness_ref",
            "composition_participation_ref",
            "trace_ref",
        ):
            val = getattr(self, field_name)
            if not isinstance(val, str) or not val.strip():
                raise WeightCarrierSchemaError(
                    f"{field_name} must be a non-empty string",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )


# ---------------------------------------------------------------------------
# KulliJuziiAxisVerdict — kulli/juz'i as verdict
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class KulliJuziiAxisVerdict:
    """Kulli/juz'i axis verdict (docs/36 §4.4).

    A verdict, not a label. Classifies whether the signified can
    be predicated of many (kulli) or is particular (juz'i), and
    identifies the source of particularity.

    KulliJuziiAxisVerdict ≠ ontological claim.
    """

    axis: KulliJuziiAxis
    particularity_source: ParticularitySource
    predication_test_passed: bool
    reference_resolution_status: str
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.axis, KulliJuziiAxis):
            raise WeightCarrierSchemaError(
                f"axis must be a KulliJuziiAxis member, "
                f"got {type(self.axis).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.particularity_source, ParticularitySource):
            raise WeightCarrierSchemaError(
                f"particularity_source must be a ParticularitySource member, "
                f"got {type(self.particularity_source).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.predication_test_passed, bool):
            raise WeightCarrierSchemaError(
                "predication_test_passed must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if (
            not isinstance(self.reference_resolution_status, str)
            or not self.reference_resolution_status.strip()
        ):
            raise WeightCarrierSchemaError(
                "reference_resolution_status must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.trace_ref, str) or not self.trace_ref.strip():
            raise WeightCarrierSchemaError(
                "trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# BranchLinkCandidate — origin/branch geometry
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BranchLinkCandidate:
    """Origin/branch geometry with 'illa jamia and preventer audit
    (docs/36 §4.5).

    Proves origin/branch relation geometry with evidence and
    preventer audit. No branch without origin. No transition
    without 'illa jamia. No 'illa without evidence. No evidence
    without rank and residual. No transition before fariq qadih
    audit.

    BranchLinkCandidate ≠ qiyas result.
    BranchLinkCandidate ≠ free reasoning.
    """

    origin_ref: str
    branch_ref: str
    relation_type: str
    illa_jamia: str
    evidence_ref: str
    domain_compatibility: str
    no_preventer: bool
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        for field_name in (
            "origin_ref",
            "branch_ref",
            "relation_type",
            "illa_jamia",
            "evidence_ref",
            "domain_compatibility",
        ):
            val = getattr(self, field_name)
            if not isinstance(val, str) or not val.strip():
                raise WeightCarrierSchemaError(
                    f"{field_name} must be a non-empty string",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        if not isinstance(self.no_preventer, bool):
            raise WeightCarrierSchemaError(
                "no_preventer must be a bool",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > SEMANTIC_SLOT_GEOMETRY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{SEMANTIC_SLOT_GEOMETRY_RANK_CEILING.name}",
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


# ---------------------------------------------------------------------------
# SemanticSlotFrame — the constitutional frame
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SemanticSlotFrame:
    """The constitutional frame for mufrad dalalah possibility
    (docs/36 §4.1).

    Every SemanticSlotFrame proves that a signifier has the
    constitutional structure needed for dalalah — identity
    continuity from dal through madlul lafzi to formal shape,
    wad' evidence, per-unit formal profile closure, kulli/juz'i
    axis verdict, and origin/branch geometry.

    SemanticSlotFrame is geometry, never dalalah operation.
    SemanticSlotFrame ≠ meaning.
    SemanticSlotFrame ≠ Mutabaqah.
    SemanticSlotFrame ≠ Tadammun.
    SemanticSlotFrame ≠ Iltizam.
    SemanticSlotFrame opens PR-D2 readiness only.
    SemanticSlotFrame does not open Ifadah.
    """

    dal_identity_ref: str
    verbal_madlul_ref: str
    contractable_unit_ref: str
    formal_shape_ref: str
    formal_style_ref: str
    wad_evidence: WadEvidenceCarrier
    per_unit_profile: PerUnitFormalProfileClosure
    kulli_juzii_axis: KulliJuziiAxisVerdict
    branch_link: BranchLinkCandidate
    naql_readiness: str
    majaz_readiness: str
    semantic_category: SemanticCategory
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- Identity continuity references ---
        for field_name in (
            "dal_identity_ref",
            "verbal_madlul_ref",
            "contractable_unit_ref",
            "formal_shape_ref",
            "formal_style_ref",
            "naql_readiness",
            "majaz_readiness",
        ):
            val = getattr(self, field_name)
            if not isinstance(val, str) or not val.strip():
                raise WeightCarrierSchemaError(
                    f"{field_name} must be a non-empty string",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        # --- Sub-carrier types ---
        if not isinstance(self.wad_evidence, WadEvidenceCarrier):
            raise WeightCarrierSchemaError(
                f"wad_evidence must be a WadEvidenceCarrier, "
                f"got {type(self.wad_evidence).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.per_unit_profile, PerUnitFormalProfileClosure):
            raise WeightCarrierSchemaError(
                f"per_unit_profile must be a PerUnitFormalProfileClosure, "
                f"got {type(self.per_unit_profile).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.kulli_juzii_axis, KulliJuziiAxisVerdict):
            raise WeightCarrierSchemaError(
                f"kulli_juzii_axis must be a KulliJuziiAxisVerdict, "
                f"got {type(self.kulli_juzii_axis).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.branch_link, BranchLinkCandidate):
            raise WeightCarrierSchemaError(
                f"branch_link must be a BranchLinkCandidate, "
                f"got {type(self.branch_link).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- semantic_category ---
        if not isinstance(self.semantic_category, SemanticCategory):
            raise WeightCarrierSchemaError(
                f"semantic_category must be a SemanticCategory member, "
                f"got {type(self.semantic_category).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- rank ---
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > SEMANTIC_SLOT_GEOMETRY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
                f"{SEMANTIC_SLOT_GEOMETRY_RANK_CEILING.name}",
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
# MufradSemanticSlotGeometryVerdict — the proof output
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MufradSemanticSlotGeometryVerdict:
    """The output of :func:`prove_mufrad_semantic_slot_geometry`
    (docs/36).

    Carries a proven SemanticSlotFrame on success, or a named
    FailureCode on refusal. Does NOT carry meaning, dalalah
    operations, ifadah, hukm, or any semantic content.
    """

    candidate: SemanticSlotFrame | None
    verdict_state: MufradSemanticState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, MufradSemanticState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be MufradSemanticState, "
                f"got {type(self.verdict_state).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- verdict_rank type and ceiling ---
        if not isinstance(self.verdict_rank, Rank):
            raise WeightCarrierSchemaError(
                f"verdict_rank must be a Rank member, "
                f"got {type(self.verdict_rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.verdict_rank > SEMANTIC_SLOT_GEOMETRY_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"verdict_rank {self.verdict_rank.name} exceeds ceiling "
                f"{SEMANTIC_SLOT_GEOMETRY_RANK_CEILING.name}",
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
        # --- State invariants ---
        if self.verdict_state is MufradSemanticState.PROVEN:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "PROVEN verdict must have failure_code=None",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "PROVEN verdict must have a SemanticSlotFrame",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if not isinstance(self.candidate, SemanticSlotFrame):
                raise WeightCarrierSchemaError(
                    f"PROVEN candidate must be SemanticSlotFrame, "
                    f"got {type(self.candidate).__name__}",
                    FailureCode.GATE_REQUIRED,
                )
        elif self.verdict_state is MufradSemanticState.REFUSED:
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
    """Build the required deferred residuals for semantic slot geometry."""
    return (
        Residual(
            name="SEMANTIC_SLOT_GEOMETRY_NOT_DALALAH",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "SemanticSlotFrame is geometry for dalalah possibility, "
                "not dalalah operation — SLOT_GEOMETRY ≠ dalalah"
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
            name="MANTUQ_DEFERRED_UNTIL_IFADAH",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note="Mantuq is not licensed here — deferred until ifadah.",
        ),
        Residual(
            name="MAFHUM_DEFERRED_UNTIL_MANTUQ",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note="Mafhum is not licensed here — deferred until mantuq.",
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
        # --- Inter-frame relation readiness stubs ---
        Residual(
            name="TAWATUI_READINESS",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Tawatui (univocal) readiness stub — "
                "no tawatui without shared hadd."
            ),
        ),
        Residual(
            name="TASHKIK_READINESS",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Tashkik (equivocal gradation) readiness stub — "
                "no tashkik without shared hadd + licensed gradation."
            ),
        ),
        Residual(
            name="TABAYUN_READINESS",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Tabayun (distinction) readiness stub — "
                "no tabayun without blocker of shared hadd."
            ),
        ),
        Residual(
            name="TARADUF_READINESS",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Taraduf (synonymy) readiness stub — "
                "no taraduf without same mutabaqah frame in same domain."
            ),
        ),
        Residual(
            name="ISHTIRAK_READINESS",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Ishtirak (homonymy) readiness stub — no ishtirak "
                "without one signifier and multiple separated frames."
            ),
        ),
        Residual(
            name="NAQL_READINESS",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Naql (transfer) readiness stub — no naql without "
                "origin frame + target frame + transfer evidence."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# prove_mufrad_semantic_slot_geometry() — the geometry operation
# ---------------------------------------------------------------------------


def prove_mufrad_semantic_slot_geometry(
    formal_style_candidate: object,
    dal_only_candidate: object,
    verbal_madlul_candidate: object,
    contractable_unit: object,
    formal_closure_state: FormalShapeClosureState,
    semantic_category: SemanticCategory,
    wad_origin_domain: WadOriginDomain,
    wad_evidence_type: WadEvidenceType,
    wad_scope: str,
    wad_evidence_ref: str,
    word_class_closure_ref: str,
    weight_pattern_closure_ref: str,
    inflection_closure_ref: str,
    contract_slot_readiness_ref: str,
    composition_participation_ref: str,
    kulli_juzii_axis: KulliJuziiAxis,
    particularity_source: ParticularitySource,
    predication_test_passed: bool,
    reference_resolution_status: str,
    branch_origin_ref: str,
    branch_ref: str,
    branch_relation_type: str,
    branch_illa_jamia: str,
    branch_evidence_ref: str,
    branch_domain_compatibility: str,
    branch_no_preventer: bool,
    naql_readiness: str,
    majaz_readiness: str,
) -> MufradSemanticSlotGeometryVerdict:
    """Prove mufrad semantic slot geometry (docs/36).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    The function validates all inputs, constructs the constitutional
    sub-carriers, assembles the SemanticSlotFrame, and returns a
    verdict. It consumes prior-layer candidates for identity
    continuity: FormalStyleCandidate (PR-F8), DalOnlyCandidate
    (PR-15), VerbalMadlulCandidate (PR-16), and
    ContractableUnitGeometry (PR-18).

    Returns
    -------
    MufradSemanticSlotGeometryVerdict
        PROVEN with a SemanticSlotFrame on success; REFUSED with a
        named FailureCode on any violation.
    """
    # Deferred import to avoid circular dependency at module load time.
    from taaqqul_slot_geometry.weight.contractable_unit_geometry import (
        ContractableUnitGeometry,
    )
    from taaqqul_slot_geometry.weight.dal_only import DalOnlyCandidate
    from taaqqul_slot_geometry.weight.formal_style_candidate import (
        FormalStyleCandidate,
    )
    from taaqqul_slot_geometry.weight.verbal_madlul import (
        VerbalMadlulCandidate,
    )

    _trace_base = "prove_mufrad_semantic_slot_geometry"

    # --- Input boundary: formal_style_candidate ---
    if not isinstance(formal_style_candidate, FormalStyleCandidate):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/formal_style_invalid_type",
        )

    # --- Input boundary: dal_only_candidate ---
    if not isinstance(dal_only_candidate, DalOnlyCandidate):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/dal_only_invalid_type",
        )

    # --- Input boundary: verbal_madlul_candidate ---
    if not isinstance(verbal_madlul_candidate, VerbalMadlulCandidate):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/verbal_madlul_invalid_type",
        )

    # --- Input boundary: contractable_unit ---
    if not isinstance(contractable_unit, ContractableUnitGeometry):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/contractable_unit_invalid_type",
        )

    # --- Input boundary: formal_closure_state must be CLOSED ---
    if not isinstance(formal_closure_state, FormalShapeClosureState):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/closure_state_invalid_type",
        )
    if formal_closure_state is not FormalShapeClosureState.CLOSED:
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/closure_not_closed",
        )

    # --- Input boundary: semantic_category ---
    if not isinstance(semantic_category, SemanticCategory):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/semantic_category_invalid",
        )

    # --- Input boundary: wad' fields ---
    if not isinstance(wad_origin_domain, WadOriginDomain):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/wad_origin_invalid",
        )
    if not isinstance(wad_evidence_type, WadEvidenceType):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/wad_evidence_type_invalid",
        )

    # --- Input boundary: string fields (non-empty) ---
    _string_checks = {
        "wad_scope": wad_scope,
        "wad_evidence_ref": wad_evidence_ref,
        "word_class_closure_ref": word_class_closure_ref,
        "weight_pattern_closure_ref": weight_pattern_closure_ref,
        "inflection_closure_ref": inflection_closure_ref,
        "contract_slot_readiness_ref": contract_slot_readiness_ref,
        "composition_participation_ref": composition_participation_ref,
        "reference_resolution_status": reference_resolution_status,
        "branch_origin_ref": branch_origin_ref,
        "branch_ref": branch_ref,
        "branch_relation_type": branch_relation_type,
        "branch_illa_jamia": branch_illa_jamia,
        "branch_evidence_ref": branch_evidence_ref,
        "branch_domain_compatibility": branch_domain_compatibility,
        "naql_readiness": naql_readiness,
        "majaz_readiness": majaz_readiness,
    }
    for field_name, val in _string_checks.items():
        if not isinstance(val, str) or not val.strip():
            return MufradSemanticSlotGeometryVerdict(
                candidate=None,
                verdict_state=MufradSemanticState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref=f"{_trace_base}/refused/{field_name}_empty",
            )

    # --- Input boundary: kulli_juzii_axis ---
    if not isinstance(kulli_juzii_axis, KulliJuziiAxis):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/kulli_juzii_axis_invalid",
        )
    if not isinstance(particularity_source, ParticularitySource):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/particularity_source_invalid",
        )
    if not isinstance(predication_test_passed, bool):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/predication_test_invalid",
        )
    if not isinstance(branch_no_preventer, bool):
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/branch_no_preventer_invalid",
        )

    # --- Identity continuity: prove same-chain provenance ---
    # verbal_madlul_candidate must reference the same dal_only_candidate.
    if verbal_madlul_candidate.dal_only is not dal_only_candidate:
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/identity_broken/verbal_madlul_dal_mismatch",
        )

    # contractable_unit.binding_candidate.dal_candidate must be the same
    # DalOnlyCandidate instance.
    if contractable_unit.binding_candidate.dal_candidate is not dal_only_candidate:
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/identity_broken/contractable_dal_mismatch",
        )

    # contractable_unit.binding_candidate.madlul_candidate must be the
    # same VerbalMadlulCandidate instance.
    if contractable_unit.binding_candidate.madlul_candidate is not verbal_madlul_candidate:
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/identity_broken/contractable_madlul_mismatch",
        )

    # The madlul inside the binding must also reference the same dal.
    if contractable_unit.binding_candidate.madlul_candidate.dal_only is not dal_only_candidate:
        return MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.IDENTITY_BROKEN,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref=f"{_trace_base}/refused/identity_broken/binding_madlul_dal_mismatch",
        )

    # --- Rank bounding via lattice meet ---
    candidate_rank = RankLattice.meet(
        Rank.CANDIDATE,
        SEMANTIC_SLOT_GEOMETRY_RANK_CEILING,
    )

    # --- Build deferred residuals ---
    residuals = _build_deferred_residuals()

    # --- Check residuals for HIDDEN_FORBIDDEN or BLOCKING ---
    for r in residuals:
        if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
            return MufradSemanticSlotGeometryVerdict(
                candidate=None,
                verdict_state=MufradSemanticState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=residuals,
                trace_ref=f"{_trace_base}/refused/hidden_residual",
            )
        if r.kind is ResidualKind.BLOCKING:
            return MufradSemanticSlotGeometryVerdict(
                candidate=None,
                verdict_state=MufradSemanticState.REFUSED,
                failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
                verdict_rank=Rank.ZERO,
                residuals=residuals,
                trace_ref=f"{_trace_base}/refused/blocking_residual",
            )

    # --- Construct sub-carriers ---
    _trace_suffix = f"{semantic_category.value}"

    wad_evidence = WadEvidenceCarrier(
        origin_domain=wad_origin_domain,
        evidence_type=wad_evidence_type,
        scope=wad_scope,
        evidence_ref=wad_evidence_ref,
        rank=candidate_rank,
        residuals=(),
        trace_ref=f"{_trace_base}/wad_evidence/{_trace_suffix}",
    )

    per_unit_profile = PerUnitFormalProfileClosure(
        word_class_closure_ref=word_class_closure_ref,
        weight_pattern_closure_ref=weight_pattern_closure_ref,
        inflection_closure_ref=inflection_closure_ref,
        contract_slot_readiness_ref=contract_slot_readiness_ref,
        composition_participation_ref=composition_participation_ref,
        trace_ref=f"{_trace_base}/per_unit_profile/{_trace_suffix}",
    )

    kulli_axis_verdict = KulliJuziiAxisVerdict(
        axis=kulli_juzii_axis,
        particularity_source=particularity_source,
        predication_test_passed=predication_test_passed,
        reference_resolution_status=reference_resolution_status,
        trace_ref=f"{_trace_base}/kulli_juzii_axis/{_trace_suffix}",
    )

    branch_link = BranchLinkCandidate(
        origin_ref=branch_origin_ref,
        branch_ref=branch_ref,
        relation_type=branch_relation_type,
        illa_jamia=branch_illa_jamia,
        evidence_ref=branch_evidence_ref,
        domain_compatibility=branch_domain_compatibility,
        no_preventer=branch_no_preventer,
        rank=candidate_rank,
        residuals=(),
        trace_ref=f"{_trace_base}/branch_link/{_trace_suffix}",
    )

    # --- Construct SemanticSlotFrame ---
    frame = SemanticSlotFrame(
        dal_identity_ref=dal_only_candidate.trace_ref,
        verbal_madlul_ref=verbal_madlul_candidate.trace_ref,
        contractable_unit_ref=contractable_unit.trace_ref,
        formal_shape_ref=formal_style_candidate.formal_closure_ref,
        formal_style_ref=formal_style_candidate.trace_ref,
        wad_evidence=wad_evidence,
        per_unit_profile=per_unit_profile,
        kulli_juzii_axis=kulli_axis_verdict,
        branch_link=branch_link,
        naql_readiness=naql_readiness,
        majaz_readiness=majaz_readiness,
        semantic_category=semantic_category,
        rank=candidate_rank,
        residuals=residuals,
        trace_ref=f"{_trace_base}/proven/{_trace_suffix}",
    )

    return MufradSemanticSlotGeometryVerdict(
        candidate=frame,
        verdict_state=MufradSemanticState.PROVEN,
        failure_code=None,
        verdict_rank=candidate_rank,
        residuals=residuals,
        trace_ref=f"{_trace_base}/proven/{_trace_suffix}",
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "SEMANTIC_CATEGORIES",
    "SEMANTIC_SLOT_GEOMETRY_RANK_CEILING",
    "BranchLinkCandidate",
    "KulliJuziiAxis",
    "KulliJuziiAxisVerdict",
    "MufradSemanticSlotGeometryVerdict",
    "MufradSemanticState",
    "ParticularitySource",
    "PerUnitFormalProfileClosure",
    "SemanticCategory",
    "SemanticSlotFrame",
    "WadEvidenceCarrier",
    "WadEvidenceType",
    "WadOriginDomain",
    "prove_mufrad_semantic_slot_geometry",
]
