"""Inflection Formal Definitions — PR-F5.

PR-F5 binding of ``docs/34_FORMAL_SHAPE_REGISTRY_LAW.md`` §8
(INFLECTION).

This module introduces the INFLECTION domain families and their
canonical formal definitions. Inflection forms are formal marking
systems — they describe case/mood marks and declension classes,
not syntactic roles or meaning.

Constitutional invariants (docs/34 §8):

* INFLECTION_FORM ≠ meaning.
* INFLECTION_FORM ≠ syntactic judgment.
* MUʿRAB_FORM ≠ syntactic role.
* MABNI_FORM ≠ reference resolution.
* MABNI_FORM ≠ immutability assertion.
* RAFʿ_MARK_FORM ≠ fāʿil (subject).
* RAFʿ_MARK_FORM ≠ mubtadaʾ (topic).
* NAṢB_MARK_FORM ≠ mafʿūl (object).
* JARR_MARK_FORM ≠ iḍāfah meaning.
* JARR_MARK_FORM ≠ genitive meaning.
* JAZM_MARK_FORM ≠ shart completion.
* JAZM_MARK_FORM ≠ prohibition/condition completion.
* ORIGINAL_MARK_FORM ≠ priority judgment.
* SUBSIDIARY_MARK_FORM ≠ deficiency judgment.
* ESTIMATED_MARK_FORM ≠ hidden meaning.
* DIPTOTE_FORM ≠ lexical category meaning.
* DECLENSION_BLOCK_FORM ≠ syntax assignment.
* GOVERNANCE_EFFECT_DEFERRED_FORM ≠ governor identity.
* FormalShapeDefinition ≠ Meaning.
* FormalShapeDefinition ≠ SemanticEntry.
* FormalShapeDefinition ≠ WadʿiSignified.
* FormalShapeDefinition ≠ Dalālah.
* FormalShapeDefinition ≠ SyntaxRole.
* FormalShapeRegistry ≠ SemanticLexicon.
* Inflection form is formal marking, not meaning.
* No rank promotion beyond FORMAL_SHAPE_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* All operations are pure: no I/O, no ledger, no network.
* No new FailureCode members; no new runtime dependencies.
* No positive 'meaning' language in definition_text.
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
    FormalShapeDefinition,
    FormalShapeDomain,
    FormalShapeFamily,
    FormalShapeRegistry,
)

# ---------------------------------------------------------------------------
# InflectionDefinitionState — verdict outcome
# ---------------------------------------------------------------------------


class InflectionDefinitionState(StrEnum):
    """The outcome of a define_inflection_shape() operation."""

    DEFINED = "DEFINED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# InflectionDefinitionVerdict — the definition proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class InflectionDefinitionVerdict:
    """The output of :func:`define_inflection_shape` (docs/34 §8).

    Proves that an inflection formal shape definition satisfies all
    constitutional requirements. It does NOT carry meaning, ifadah,
    hukm, reality, syntactic role, or any semantic content.
    """

    definition: FormalShapeDefinition | None
    verdict_state: InflectionDefinitionState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, InflectionDefinitionState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be InflectionDefinitionState, "
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
        if self.verdict_rank > FORMAL_SHAPE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"verdict_rank {self.verdict_rank.name} exceeds ceiling "
                f"{FORMAL_SHAPE_RANK_CEILING.name}",
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
        if self.verdict_state is InflectionDefinitionState.DEFINED:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "DEFINED verdict must have failure_code=None",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if self.definition is None:
                raise WeightCarrierSchemaError(
                    "DEFINED verdict must have a FormalShapeDefinition",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if not isinstance(self.definition, FormalShapeDefinition):
                raise WeightCarrierSchemaError(
                    f"DEFINED definition must be FormalShapeDefinition, "
                    f"got {type(self.definition).__name__}",
                    FailureCode.GATE_REQUIRED,
                )
        elif self.verdict_state is InflectionDefinitionState.REFUSED:
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
            if self.definition is not None:
                raise WeightCarrierSchemaError(
                    "REFUSED verdict must have definition=None",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )


# ---------------------------------------------------------------------------
# INFLECTION Families (docs/34 §8)
# ---------------------------------------------------------------------------

#: MUʿRAB_FORM — declinable word (accepts case/mood variation).
MURAB_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="MURAB_FORM",
    description=(
        "Declinable (mu'rab) word form — a word whose ending varies "
        "according to governance without asserting what governs it"
    ),
)

#: MABNI_FORM — indeclinable word (fixed ending).
MABNI_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="MABNI_FORM",
    description=(
        "Indeclinable (mabni) word form — a word whose ending is "
        "fixed regardless of structural position, without asserting "
        "reference resolution or immutability"
    ),
)

#: RAFʿ_MARK_FORM — nominative/indicative marking.
RAF_MARK_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="RAF_MARK_FORM",
    description=(
        "Nominative/indicative mark (raf') — formal ending shape for "
        "the raf' position without asserting subjecthood (fa'il) or "
        "topichood (mubtada')"
    ),
)

#: NAṢB_MARK_FORM — accusative/subjunctive marking.
NASB_MARK_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="NASB_MARK_FORM",
    description=(
        "Accusative/subjunctive mark (nasb) — formal ending shape for "
        "the nasb position without asserting objecthood (maf'ul) or "
        "any semantic patient role"
    ),
)

#: JARR_MARK_FORM — genitive marking.
JARR_MARK_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="JARR_MARK_FORM",
    description=(
        "Genitive mark (jarr) — formal ending shape for the jarr "
        "position without asserting idafah meaning or genitive "
        "semantic content"
    ),
)

#: JAZM_MARK_FORM — jussive marking.
JAZM_MARK_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="JAZM_MARK_FORM",
    description=(
        "Jussive mark (jazm) — formal ending shape for the jazm "
        "position without asserting condition completion, prohibition, "
        "or any modal meaning"
    ),
)

#: ORIGINAL_MARK_FORM — original (asli) inflection marker.
ORIGINAL_MARK_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="ORIGINAL_MARK_FORM",
    description=(
        "Original (asli) inflection marker — the default vowel mark "
        "(dammah/fathah/kasrah/sukun) that appears in the standard "
        "paradigm without asserting priority or superiority"
    ),
)

#: SUBSIDIARY_MARK_FORM — subsidiary (far'i) inflection marker.
SUBSIDIARY_MARK_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="SUBSIDIARY_MARK_FORM",
    description=(
        "Subsidiary (far'i) inflection marker — an alternative mark "
        "(alif/waw/ya'/nun-deletion/etc.) replacing the original in "
        "specific paradigms without asserting deficiency"
    ),
)

#: ESTIMATED_MARK_FORM — estimated (muqaddar) inflection marker.
ESTIMATED_MARK_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="ESTIMATED_MARK_FORM",
    description=(
        "Estimated (muqaddar) inflection marker — a mark that is "
        "formally present but phonologically suppressed (due to "
        "heaviness/impossibility), without asserting hidden meaning"
    ),
)

#: DIPTOTE_FORM — restricted declension (mamnu' min al-sarf).
DIPTOTE_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="DIPTOTE_FORM",
    description=(
        "Restricted declension (mamnu' min al-sarf) form — a word "
        "that does not take tanwin and takes fathah instead of "
        "kasrah in jarr, without asserting lexical category meaning"
    ),
)

#: DECLENSION_BLOCK_FORM — the formal declension paradigm block.
DECLENSION_BLOCK_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="DECLENSION_BLOCK_FORM",
    description=(
        "Declension block form — a formal paradigm block (triptote, "
        "diptote, indeclinable, five-nouns, five-verbs, etc.) "
        "classifying the inflection pattern without syntax assignment"
    ),
)

#: GOVERNANCE_EFFECT_DEFERRED_FORM — formal governance effect placeholder.
GOVERNANCE_EFFECT_DEFERRED_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.INFLECTION,
    family_id="GOVERNANCE_EFFECT_DEFERRED_FORM",
    description=(
        "Governance effect deferred form — a formal mark shape that "
        "records that a governance effect is visible but the governor "
        "identity is deferred to PR-F6 (contract slot definitions)"
    ),
)

#: All INFLECTION families.
INFLECTION_FAMILIES: tuple[FormalShapeFamily, ...] = (
    MURAB_FORM_FAMILY,
    MABNI_FORM_FAMILY,
    RAF_MARK_FORM_FAMILY,
    NASB_MARK_FORM_FAMILY,
    JARR_MARK_FORM_FAMILY,
    JAZM_MARK_FORM_FAMILY,
    ORIGINAL_MARK_FORM_FAMILY,
    SUBSIDIARY_MARK_FORM_FAMILY,
    ESTIMATED_MARK_FORM_FAMILY,
    DIPTOTE_FORM_FAMILY,
    DECLENSION_BLOCK_FORM_FAMILY,
    GOVERNANCE_EFFECT_DEFERRED_FORM_FAMILY,
)


# ---------------------------------------------------------------------------
# define_inflection_shape() — the definition operation
# ---------------------------------------------------------------------------


def define_inflection_shape(
    shape_id: str,
    family: FormalShapeFamily,
    canonical_name: str,
    definition_text: str,
    distinguishing_evidence: str,
    boundary_conditions: tuple[str, ...],
    exclusion_conditions: tuple[str, ...],
    weight_constraint: str | None = None,
    path_constraint: str | None = None,
) -> InflectionDefinitionVerdict:
    """Prove an inflection formal shape definition (docs/34 §8).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    Parameters
    ----------
    shape_id : str
        Globally unique identifier for this formal shape.
    family : FormalShapeFamily
        Must belong to the INFLECTION domain.
    canonical_name : str
        The Arabic grammatical term (e.g., "mu'rab", "mabni").
    definition_text : str
        Formal textual definition proving the shape.
    distinguishing_evidence : str
        What proves this shape vs. other inflection families.
    boundary_conditions : tuple[str, ...]
        When this shape applies (non-empty).
    exclusion_conditions : tuple[str, ...]
        When this shape does NOT apply.
    weight_constraint : str | None
        Weight pattern requirement, if any.
    path_constraint : str | None
        PathKind constraint, if any.

    Returns
    -------
    InflectionDefinitionVerdict
        DEFINED with a FormalShapeDefinition on success; REFUSED with a
        named FailureCode on any violation.
    """
    # --- Input boundary: shape_id ---
    if not isinstance(shape_id, str) or not shape_id.strip():
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/shape_id_empty",
        )

    # --- Input boundary: family type and domain ---
    if not isinstance(family, FormalShapeFamily):
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/family_not_formal_shape_family",
        )
    if family.domain is not FormalShapeDomain.INFLECTION:
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.DOMAIN_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/family_domain_not_inflection",
        )

    # --- Input boundary: canonical_name ---
    if not isinstance(canonical_name, str) or not canonical_name.strip():
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/canonical_name_empty",
        )

    # --- Input boundary: definition_text ---
    if not isinstance(definition_text, str) or not definition_text.strip():
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/definition_text_empty",
        )

    # --- Input boundary: distinguishing_evidence ---
    if not isinstance(distinguishing_evidence, str) or not distinguishing_evidence.strip():
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/distinguishing_evidence_empty",
        )

    # --- Input boundary: boundary_conditions ---
    if not isinstance(boundary_conditions, tuple):
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/boundary_conditions_not_tuple",
        )
    if not boundary_conditions:
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/boundary_conditions_empty",
        )
    for bc in boundary_conditions:
        if not isinstance(bc, str) or not bc.strip():
            return InflectionDefinitionVerdict(
                definition=None,
                verdict_state=InflectionDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_inflection_shape/refused/boundary_condition_invalid",
            )

    # --- Input boundary: exclusion_conditions ---
    if not isinstance(exclusion_conditions, tuple):
        return InflectionDefinitionVerdict(
            definition=None,
            verdict_state=InflectionDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_inflection_shape/refused/exclusion_conditions_not_tuple",
        )
    for ec in exclusion_conditions:
        if not isinstance(ec, str) or not ec.strip():
            return InflectionDefinitionVerdict(
                definition=None,
                verdict_state=InflectionDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_inflection_shape/refused/exclusion_condition_invalid",
            )

    # --- Rank bounding via lattice meet ---
    definition_rank = RankLattice.meet(
        Rank.CANDIDATE,
        FORMAL_SHAPE_RANK_CEILING,
    )

    # --- Residuals: open residual noting inflection form ≠ meaning ---
    open_residuals: tuple[Residual, ...] = (
        Residual(
            name=f"inflection_not_meaning/{shape_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"FormalShapeDefinition({shape_id}) is inflection form, "
                f"not meaning — INFLECTION ≠ syntactic judgment, "
                f"INFLECTION ≠ meaning"
            ),
        ),
    )

    # --- Construct the FormalShapeDefinition ---
    definition = FormalShapeDefinition(
        shape_id=shape_id,
        domain=FormalShapeDomain.INFLECTION,
        family=family,
        canonical_name=canonical_name,
        definition_text=definition_text,
        distinguishing_evidence=distinguishing_evidence,
        boundary_conditions=boundary_conditions,
        exclusion_conditions=exclusion_conditions,
        weight_constraint=weight_constraint,
        path_constraint=path_constraint,
        rank=definition_rank,
        residuals=open_residuals,
        trace_ref=f"define_inflection_shape/defined/{shape_id}",
    )

    return InflectionDefinitionVerdict(
        definition=definition,
        verdict_state=InflectionDefinitionState.DEFINED,
        failure_code=None,
        verdict_rank=definition_rank,
        residuals=open_residuals,
        trace_ref=f"define_inflection_shape/defined/{shape_id}",
    )


# ---------------------------------------------------------------------------
# Canonical INFLECTION definitions (docs/34 §8)
# ---------------------------------------------------------------------------

#: MUʿRAB_FORM formal definition.
MURAB_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.MURAB_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=MURAB_FORM_FAMILY,
    canonical_name="mu'rab",
    definition_text=(
        "A word whose ending varies formally according to differing "
        "governance positions. Proved by observable variation of the "
        "final vowel/letter across positions (raf', nasb, jarr/jazm). "
        "This is ending-variation shape, not syntactic role."
    ),
    distinguishing_evidence=(
        "Final vowel/letter changes across governance positions — "
        "dammah in raf', fathah in nasb, kasrah in jarr (or sukun "
        "in jazm for verbs) — distinguishing from mabni forms whose "
        "endings remain fixed."
    ),
    boundary_conditions=(
        "Final ending varies across governance positions",
        "Observable alternation of vowel marks (dammah/fathah/kasrah/sukun)",
        "Variation is systematic (not free variation)",
    ),
    exclusion_conditions=(
        "MU'RAB_FORM does not assert what governs the word",
        "MU'RAB_FORM does not assign a syntactic role",
        "MU'RAB_FORM does not resolve governance identity",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.MURAB_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.MURAB_FORM) is inflection "
                "form, not meaning — MU'RAB ≠ syntactic role"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/INFLECTION.MURAB_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Governor identity and contract slot assignment not licensed "
                "here — deferred to PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.MURAB_FORM",
)

#: MABNI_FORM formal definition.
MABNI_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.MABNI_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=MABNI_FORM_FAMILY,
    canonical_name="mabni",
    definition_text=(
        "A word whose ending is formally fixed regardless of "
        "governance position. Proved by non-variation of the final "
        "vowel/letter across all structural positions. This is "
        "ending-fixity shape, not reference resolution or "
        "immutability assertion."
    ),
    distinguishing_evidence=(
        "Final ending remains constant regardless of structural "
        "position — same vowel/letter in all contexts — distinguishing "
        "from mu'rab forms whose endings vary."
    ),
    boundary_conditions=(
        "Final ending does not vary across governance positions",
        "Fixed ending (fathah, dammah, kasrah, or sukun)",
        "Fixity is structural (not accidental homophony)",
    ),
    exclusion_conditions=(
        "MABNI_FORM does not assert reference resolution",
        "MABNI_FORM does not assert immutability of referent",
        "MABNI_FORM does not resolve pronoun binding",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.MABNI_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.MABNI_FORM) is inflection "
                "form, not meaning — MABNI ≠ reference resolution"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/INFLECTION.MABNI_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Structural position assignment for mabni words not licensed "
                "here — deferred to PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.MABNI_FORM",
)

#: RAFʿ_MARK_FORM formal definition.
RAF_MARK_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.RAF_MARK_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=RAF_MARK_FORM_FAMILY,
    canonical_name="'alamat al-raf'",
    definition_text=(
        "A formal ending mark indicating the raf' (nominative/ "
        "indicative) position. Proved by presence of dammah, waw, "
        "alif, or nun (depending on paradigm). This is a position "
        "mark, not subjecthood or agency."
    ),
    distinguishing_evidence=(
        "Dammah (or waw/alif/nun in subsidiary paradigms) as the "
        "formal mark in raf' position — distinguishing from nasb "
        "(fathah), jarr (kasrah), and jazm (sukun) marks."
    ),
    boundary_conditions=(
        "Mark appears in the raf' governance position",
        "Original form: dammah; subsidiary forms: waw/alif/nun",
        "Applies to mu'rab words only",
    ),
    exclusion_conditions=(
        "RAF'_MARK_FORM does not assert subjecthood (fa'il)",
        "RAF'_MARK_FORM does not assert topichood (mubtada')",
        "RAF'_MARK_FORM does not identify the governor",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.RAF_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.RAF_MARK_FORM) is "
                "inflection form, not meaning — RAF' ≠ fa'il, "
                "RAF' ≠ mubtada'"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/INFLECTION.RAF_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Subject/topic slot licensing not available here — "
                "deferred to PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.RAF_MARK_FORM",
)

#: NAṢB_MARK_FORM formal definition.
NASB_MARK_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.NASB_MARK_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=NASB_MARK_FORM_FAMILY,
    canonical_name="'alamat al-nasb",
    definition_text=(
        "A formal ending mark indicating the nasb (accusative/ "
        "subjunctive) position. Proved by presence of fathah, alif, "
        "kasrah, or nun-deletion (depending on paradigm). This is "
        "a position mark, not objecthood or patienthood."
    ),
    distinguishing_evidence=(
        "Fathah (or alif/kasrah/nun-deletion in subsidiary paradigms) "
        "as the formal mark in nasb position — distinguishing from "
        "raf' (dammah), jarr (kasrah in standard), and jazm (sukun)."
    ),
    boundary_conditions=(
        "Mark appears in the nasb governance position",
        "Original form: fathah; subsidiary forms: alif/kasrah/nun-deletion",
        "Applies to mu'rab words only",
    ),
    exclusion_conditions=(
        "NASB_MARK_FORM does not assert objecthood (maf'ul)",
        "NASB_MARK_FORM does not assert patienthood",
        "NASB_MARK_FORM does not identify the governor",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.NASB_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.NASB_MARK_FORM) is "
                "inflection form, not meaning — NASB ≠ maf'ul, "
                "NASB ≠ patienthood"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/INFLECTION.NASB_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Object slot licensing not available here — deferred to "
                "PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.NASB_MARK_FORM",
)

#: JARR_MARK_FORM formal definition.
JARR_MARK_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.JARR_MARK_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=JARR_MARK_FORM_FAMILY,
    canonical_name="'alamat al-jarr",
    definition_text=(
        "A formal ending mark indicating the jarr (genitive) "
        "position. Proved by presence of kasrah, ya', or fathah "
        "(in diptote). This is a position mark, not possession "
        "or idafah relation."
    ),
    distinguishing_evidence=(
        "Kasrah (or ya'/fathah in subsidiary paradigms) as the "
        "formal mark in jarr position — distinguishing from raf' "
        "(dammah), nasb (fathah in standard), and jazm (sukun)."
    ),
    boundary_conditions=(
        "Mark appears in the jarr governance position",
        "Original form: kasrah; subsidiary forms: ya'/fathah (diptote)",
        "Applies to mu'rab nouns only (verbs do not take jarr)",
    ),
    exclusion_conditions=(
        "JARR_MARK_FORM does not assert idafah meaning",
        "JARR_MARK_FORM does not assert possession",
        "JARR_MARK_FORM does not identify the governing preposition",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.JARR_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.JARR_MARK_FORM) is "
                "inflection form, not meaning — JARR ≠ idafah meaning, "
                "JARR ≠ possession"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/INFLECTION.JARR_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Genitive complement slot licensing not available here — "
                "deferred to PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.JARR_MARK_FORM",
)

#: JAZM_MARK_FORM formal definition.
JAZM_MARK_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.JAZM_MARK_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=JAZM_MARK_FORM_FAMILY,
    canonical_name="'alamat al-jazm",
    definition_text=(
        "A formal ending mark indicating the jazm (jussive) "
        "position. Proved by presence of sukun or nun-deletion "
        "(in five-verbs). This is a position mark, not condition "
        "completion or prohibition."
    ),
    distinguishing_evidence=(
        "Sukun (or nun-deletion in five-verb paradigm) as the "
        "formal mark in jazm position — distinguishing from raf' "
        "(dammah/nun), nasb (fathah/nun-deletion), and jarr (kasrah)."
    ),
    boundary_conditions=(
        "Mark appears in the jazm governance position",
        "Original form: sukun; subsidiary form: nun-deletion (five-verbs)",
        "Applies to mu'rab mudari' verbs only (nouns do not take jazm)",
    ),
    exclusion_conditions=(
        "JAZM_MARK_FORM does not assert condition completion (shart)",
        "JAZM_MARK_FORM does not assert prohibition",
        "JAZM_MARK_FORM does not identify the governing jazm particle",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.JAZM_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.JAZM_MARK_FORM) is "
                "inflection form, not meaning — JAZM ≠ shart completion, "
                "JAZM ≠ prohibition"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/INFLECTION.JAZM_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Jazm governor identity not licensed here — deferred to "
                "PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.JAZM_MARK_FORM",
)

#: ORIGINAL_MARK_FORM formal definition.
ORIGINAL_MARK_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.ORIGINAL_MARK_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=ORIGINAL_MARK_FORM_FAMILY,
    canonical_name="'alamah asliyyah",
    definition_text=(
        "A formal inflection mark that is the default (asli) sign in "
        "the standard paradigm: dammah for raf', fathah for nasb, "
        "kasrah for jarr, sukun for jazm. Proved by appearing in "
        "the regular (salim) singular noun/verb paradigm. This is "
        "mark-type classification, not priority assertion."
    ),
    distinguishing_evidence=(
        "Appears as the standard vowel mark in the regular (salim) "
        "paradigm — dammah/fathah/kasrah/sukun — distinguishing from "
        "subsidiary marks (waw/alif/ya'/nun-deletion) that replace "
        "the original in non-standard paradigms."
    ),
    boundary_conditions=(
        "Mark is the default sign for its governance position",
        "Appears in the regular (salim) singular paradigm",
        "Is a short vowel (dammah/fathah/kasrah) or sukun",
    ),
    exclusion_conditions=(
        "ORIGINAL_MARK_FORM does not assert priority over subsidiary marks",
        "ORIGINAL_MARK_FORM does not assert correctness judgment",
        "Does not appear in dual/sound plural/five-noun paradigms as mark",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.ORIGINAL_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.ORIGINAL_MARK_FORM) is "
                "inflection form, not meaning — ORIGINAL_MARK ≠ priority "
                "judgment"
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.ORIGINAL_MARK_FORM",
)

#: SUBSIDIARY_MARK_FORM formal definition.
SUBSIDIARY_MARK_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.SUBSIDIARY_MARK_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=SUBSIDIARY_MARK_FORM_FAMILY,
    canonical_name="'alamah far'iyyah",
    definition_text=(
        "A formal inflection mark that replaces the original (asli) "
        "in specific paradigms: waw/alif/ya' for five-nouns, "
        "alif/waw/ya' for dual and sound plurals, nun-deletion for "
        "five-verbs. Proved by appearing in non-standard paradigms "
        "where the original mark is absent. This is mark-type "
        "classification, not deficiency assertion."
    ),
    distinguishing_evidence=(
        "Appears as replacement mark in non-standard paradigms — "
        "waw/alif/ya'/nun-deletion — distinguishing from original "
        "marks (dammah/fathah/kasrah/sukun) by paradigm membership."
    ),
    boundary_conditions=(
        "Mark replaces the original sign in a specific paradigm",
        "Appears in dual, sound plural, five-noun, or five-verb forms",
        "Is a letter (waw/alif/ya') or absence (nun-deletion)",
    ),
    exclusion_conditions=(
        "SUBSIDIARY_MARK_FORM does not assert deficiency",
        "SUBSIDIARY_MARK_FORM does not assert irregularity judgment",
        "Does not appear in the regular (salim) singular paradigm as mark",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.SUBSIDIARY_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.SUBSIDIARY_MARK_FORM) is "
                "inflection form, not meaning — SUBSIDIARY_MARK ≠ deficiency "
                "judgment"
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.SUBSIDIARY_MARK_FORM",
)

#: ESTIMATED_MARK_FORM formal definition.
ESTIMATED_MARK_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.ESTIMATED_MARK_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=ESTIMATED_MARK_FORM_FAMILY,
    canonical_name="'alamah muqaddarah",
    definition_text=(
        "A formal inflection mark that is structurally present but "
        "phonologically suppressed due to heaviness (thiqal) or "
        "impossibility (ta'adhdhur). Proved by the inability to "
        "pronounce the expected vowel on the final letter (e.g., "
        "alif maqsurah, ya' before ya' al-mutakallim). This is "
        "suppression-type classification, not hidden content."
    ),
    distinguishing_evidence=(
        "Mark is formally posited but not pronounced — due to "
        "heaviness on ya' or impossibility on alif — distinguishing "
        "from original marks (pronounced) and subsidiary marks "
        "(visible letters)."
    ),
    boundary_conditions=(
        "Expected vowel mark cannot be pronounced on final letter",
        "Suppression cause: heaviness (thiqal) or impossibility (ta'adhdhur)",
        "Mark is formally present for governance purposes",
    ),
    exclusion_conditions=(
        "ESTIMATED_MARK_FORM does not assert hidden meaning",
        "ESTIMATED_MARK_FORM does not assert semantic suppression",
        "Does not apply when mark is actually pronounced (would be original/subsidiary)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.ESTIMATED_MARK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.ESTIMATED_MARK_FORM) is "
                "inflection form, not meaning — ESTIMATED_MARK ≠ hidden "
                "meaning"
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.ESTIMATED_MARK_FORM",
)

#: DIPTOTE_FORM formal definition.
DIPTOTE_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.DIPTOTE_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=DIPTOTE_FORM_FAMILY,
    canonical_name="mamnu' min al-sarf",
    definition_text=(
        "A word with restricted declension that does not take tanwin "
        "and takes fathah instead of kasrah in the jarr position. "
        "Proved by absence of tanwin and fathah-in-jarr. This is "
        "declension-restriction shape, not lexical category content."
    ),
    distinguishing_evidence=(
        "Does not take tanwin and takes fathah instead of kasrah in "
        "jarr — distinguishing from triptote (munṣarif) forms which "
        "take tanwin and kasrah in jarr."
    ),
    boundary_conditions=(
        "Does not accept tanwin (nunation)",
        "Takes fathah instead of kasrah in jarr position",
        "Carries one or more diptote-triggering formal properties",
    ),
    exclusion_conditions=(
        "DIPTOTE_FORM does not assert lexical category meaning",
        "DIPTOTE_FORM does not assert deficiency of the word",
        "Does not apply when tanwin is present (would be triptote)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.DIPTOTE_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.DIPTOTE_FORM) is "
                "inflection form, not meaning — DIPTOTE ≠ lexical "
                "category meaning"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/INFLECTION.DIPTOTE_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Why a word is diptote (semantic reason) is not licensed "
                "here — deferred to post-formal-closure semantics."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.DIPTOTE_FORM",
)

#: DECLENSION_BLOCK_FORM formal definition.
DECLENSION_BLOCK_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.DECLENSION_BLOCK_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=DECLENSION_BLOCK_FORM_FAMILY,
    canonical_name="namat al-tasrif",
    definition_text=(
        "A formal paradigm block classifying the complete inflection "
        "pattern of a word: triptote, diptote, indeclinable, "
        "five-nouns, five-verbs, dual, sound masculine plural, sound "
        "feminine plural, etc. Proved by the set of marks the word "
        "accepts across all governance positions. This is paradigm "
        "classification, not syntax assignment."
    ),
    distinguishing_evidence=(
        "Complete set of marks across all governance positions forms "
        "a paradigm block — distinguishing individual mark types "
        "(raf'/nasb/jarr/jazm) from the holistic paradigm pattern."
    ),
    boundary_conditions=(
        "Word has a classifiable paradigm of mark alternations",
        "Paradigm is identified by the full set of marks accepted",
        "Classification covers all four governance positions where applicable",
    ),
    exclusion_conditions=(
        "DECLENSION_BLOCK_FORM does not assign syntactic roles",
        "DECLENSION_BLOCK_FORM does not assert meaning of paradigm membership",
        "Does not identify the governor (would be contract slot, PR-F6)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.DECLENSION_BLOCK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.DECLENSION_BLOCK_FORM) is "
                "inflection form, not meaning — DECLENSION_BLOCK ≠ syntax "
                "assignment"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/INFLECTION.DECLENSION_BLOCK_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How paradigm blocks interact in composition not licensed "
                "here — deferred to PR-F7 (Composition Pattern Formal "
                "Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.DECLENSION_BLOCK_FORM",
)

#: GOVERNANCE_EFFECT_DEFERRED_FORM formal definition.
GOVERNANCE_EFFECT_DEFERRED_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="INFLECTION.GOVERNANCE_EFFECT_DEFERRED_FORM",
    domain=FormalShapeDomain.INFLECTION,
    family=GOVERNANCE_EFFECT_DEFERRED_FORM_FAMILY,
    canonical_name="athar al-'amal mu'ajjal",
    definition_text=(
        "A formal shape recording that a governance effect (athar "
        "al-'amal) is visible on the word ending, but the identity "
        "of the governor ('amil) is not licensed at this layer. "
        "Proved by presence of an inflection mark without identifying "
        "what caused it. This is effect-visibility shape, not "
        "governor identity."
    ),
    distinguishing_evidence=(
        "Records presence of a governance effect (visible mark "
        "change) without identifying the governing element — "
        "distinguishing from contract slots (PR-F6) which identify "
        "the governor-governed relationship."
    ),
    boundary_conditions=(
        "A governance effect is visible (ending has changed)",
        "Governor identity is not licensed at this layer",
        "Effect is recorded as formal shape only",
    ),
    exclusion_conditions=(
        "GOVERNANCE_EFFECT_DEFERRED_FORM does not identify the governor",
        "GOVERNANCE_EFFECT_DEFERRED_FORM does not assert governor-governed binding",
        "GOVERNANCE_EFFECT_DEFERRED_FORM does not assign syntactic relationship",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="inflection_not_meaning/INFLECTION.GOVERNANCE_EFFECT_DEFERRED_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(INFLECTION.GOVERNANCE_EFFECT_DEFERRED_FORM) "
                "is inflection form, not meaning — GOVERNANCE_EFFECT_DEFERRED "
                "≠ governor identity"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/INFLECTION.GOVERNANCE_EFFECT_DEFERRED_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Governor identity and 'amil-ma'mul binding not licensed "
                "here — deferred to PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/INFLECTION.GOVERNANCE_EFFECT_DEFERRED_FORM",
)


# ---------------------------------------------------------------------------
# build_inflection_registry() — assemble INFLECTION registry
# ---------------------------------------------------------------------------


def build_inflection_registry(
    definitions: tuple[FormalShapeDefinition, ...] | None = None,
) -> FormalShapeRegistry:
    """Assemble the INFLECTION domain registry (docs/34 §8).

    This is a **pure function**: it accepts values and returns a value.
    If no definitions are provided, uses all 12 canonical definitions.

    The registry is CLOSED when all 12 required families have at least
    one proven definition each. Otherwise PARTIAL or EMPTY.

    Parameters
    ----------
    definitions : tuple[FormalShapeDefinition, ...] | None
        Definitions to register. If None, uses all canonical definitions.

    Returns
    -------
    FormalShapeRegistry
        The assembled registry with its computed closure_state.
    """
    if definitions is None:
        definitions = (
            MURAB_FORM_DEFINITION,
            MABNI_FORM_DEFINITION,
            RAF_MARK_FORM_DEFINITION,
            NASB_MARK_FORM_DEFINITION,
            JARR_MARK_FORM_DEFINITION,
            JAZM_MARK_FORM_DEFINITION,
            ORIGINAL_MARK_FORM_DEFINITION,
            SUBSIDIARY_MARK_FORM_DEFINITION,
            ESTIMATED_MARK_FORM_DEFINITION,
            DIPTOTE_FORM_DEFINITION,
            DECLENSION_BLOCK_FORM_DEFINITION,
            GOVERNANCE_EFFECT_DEFERRED_FORM_DEFINITION,
        )

    # Validate all definitions belong to INFLECTION
    for defn in definitions:
        if defn.domain is not FormalShapeDomain.INFLECTION:
            return FormalShapeRegistry(
                domain=FormalShapeDomain.INFLECTION,
                families=INFLECTION_FAMILIES,
                definitions=(),
                rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                closure_state=FormalShapeClosureState.REFUSED,
            )

    # Check residuals for HIDDEN_FORBIDDEN or BLOCKING
    _refused_kinds = (ResidualKind.HIDDEN_FORBIDDEN, ResidualKind.BLOCKING)
    for defn in definitions:
        for r in defn.residuals:
            if r.kind in _refused_kinds:
                return FormalShapeRegistry(
                    domain=FormalShapeDomain.INFLECTION,
                    families=INFLECTION_FAMILIES,
                    definitions=definitions,
                    rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                    closure_state=FormalShapeClosureState.REFUSED,
                )

    # Compute closure state
    if not definitions:
        closure_state = FormalShapeClosureState.EMPTY
    else:
        required_family_ids = {f.family_id for f in INFLECTION_FAMILIES}
        covered_family_ids = {d.family.family_id for d in definitions}
        if required_family_ids <= covered_family_ids:
            closure_state = FormalShapeClosureState.CLOSED
        else:
            closure_state = FormalShapeClosureState.PARTIAL

    return FormalShapeRegistry(
        domain=FormalShapeDomain.INFLECTION,
        families=INFLECTION_FAMILIES,
        definitions=definitions,
        rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
        closure_state=closure_state,
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "DECLENSION_BLOCK_FORM_DEFINITION",
    "DECLENSION_BLOCK_FORM_FAMILY",
    "DIPTOTE_FORM_DEFINITION",
    "DIPTOTE_FORM_FAMILY",
    "ESTIMATED_MARK_FORM_DEFINITION",
    "ESTIMATED_MARK_FORM_FAMILY",
    "GOVERNANCE_EFFECT_DEFERRED_FORM_DEFINITION",
    "GOVERNANCE_EFFECT_DEFERRED_FORM_FAMILY",
    "INFLECTION_FAMILIES",
    "InflectionDefinitionState",
    "InflectionDefinitionVerdict",
    "JARR_MARK_FORM_DEFINITION",
    "JARR_MARK_FORM_FAMILY",
    "JAZM_MARK_FORM_DEFINITION",
    "JAZM_MARK_FORM_FAMILY",
    "MABNI_FORM_DEFINITION",
    "MABNI_FORM_FAMILY",
    "MURAB_FORM_DEFINITION",
    "MURAB_FORM_FAMILY",
    "NASB_MARK_FORM_DEFINITION",
    "NASB_MARK_FORM_FAMILY",
    "ORIGINAL_MARK_FORM_DEFINITION",
    "ORIGINAL_MARK_FORM_FAMILY",
    "RAF_MARK_FORM_DEFINITION",
    "RAF_MARK_FORM_FAMILY",
    "SUBSIDIARY_MARK_FORM_DEFINITION",
    "SUBSIDIARY_MARK_FORM_FAMILY",
    "build_inflection_registry",
    "define_inflection_shape",
]
