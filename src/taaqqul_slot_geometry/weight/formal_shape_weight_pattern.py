"""Weight Formal Definitions — PR-F4.

PR-F4 binding of ``docs/34_FORMAL_SHAPE_REGISTRY_LAW.md`` §7
(WEIGHT_PATTERN).

This module introduces the WEIGHT_PATTERN domain families and their
canonical formal definitions. Weight patterns are formal morphological
templates — they describe shape, not meaning.

Constitutional invariants (docs/34 §7):

* WEIGHT_PATTERN_FORM ≠ meaning.
* VERBAL_PATTERN_FORM ≠ event occurrence.
* VERBAL_MUJARRAD_PATTERN ≠ actual action.
* VERBAL_MAZID_PATTERN ≠ semantic transformation.
* MASDAR_FORM ≠ event occurrence.
* MASDAR_FORM ≠ time/place.
* FAʿIL_FORM ≠ real agent.
* FAʿIL_FORM ≠ formal agent slot.
* MAFʿUL_FORM ≠ real patient.
* MAFʿUL_FORM ≠ formal object slot.
* SIFAH_MUSHABBAHA_FORM ≠ attribute judgment.
* INSTRUMENT_FORM ≠ actual instrument.
* TIME_PLACE_FORM ≠ real time/place.
* GENDERED_WEIGHT_FORM ≠ real sex/gender judgment.
* MUSHTAQ_FORM ≠ semantic derivation.
* FormalShapeDefinition ≠ Meaning.
* FormalShapeDefinition ≠ SemanticEntry.
* FormalShapeDefinition ≠ WadʿiSignified.
* FormalShapeDefinition ≠ Dalālah.
* FormalShapeDefinition ≠ SyntaxRole.
* FormalShapeRegistry ≠ SemanticLexicon.
* Weight pattern form is formal shape, not meaning.
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
# WeightPatternDefinitionState — verdict outcome
# ---------------------------------------------------------------------------


class WeightPatternDefinitionState(StrEnum):
    """The outcome of a define_weight_pattern_shape() operation."""

    DEFINED = "DEFINED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# WeightPatternDefinitionVerdict — the definition proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WeightPatternDefinitionVerdict:
    """The output of :func:`define_weight_pattern_shape` (docs/34 §7).

    Proves that a weight-pattern formal shape definition satisfies all
    constitutional requirements. It does NOT carry meaning, ifadah,
    hukm, reality, or any semantic content.
    """

    definition: FormalShapeDefinition | None
    verdict_state: WeightPatternDefinitionState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, WeightPatternDefinitionState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be WeightPatternDefinitionState, "
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
        if self.verdict_state is WeightPatternDefinitionState.DEFINED:
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
        elif self.verdict_state is WeightPatternDefinitionState.REFUSED:
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
# WEIGHT_PATTERN Families (docs/34 §7)
# ---------------------------------------------------------------------------

#: VERBAL_MUJARRAD_PATTERN (base trilateral/quadrilateral verb pattern).
VERBAL_MUJARRAD_PATTERN_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="VERBAL_MUJARRAD_PATTERN",
    description=(
        "Base (mujarrad) verbal weight pattern — trilateral or "
        "quadrilateral root on a formal verbal template without "
        "augmentation"
    ),
)

#: VERBAL_MAZID_PATTERN (augmented verb pattern).
VERBAL_MAZID_PATTERN_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="VERBAL_MAZID_PATTERN",
    description=(
        "Augmented (mazid) verbal weight pattern — base verbal "
        "template with one or more formal augmentation letters "
        "without asserting semantic transformation"
    ),
)

#: MASDAR_MUJARRAD_PATTERN (base verbal noun pattern).
MASDAR_MUJARRAD_PATTERN_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="MASDAR_MUJARRAD_PATTERN",
    description=(
        "Base (mujarrad) masdar pattern — formal nominal template "
        "for the event-name shape without asserting event occurrence "
        "or temporal reality"
    ),
)

#: MASDAR_MAZID_PATTERN (augmented verbal noun pattern).
MASDAR_MAZID_PATTERN_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="MASDAR_MAZID_PATTERN",
    description=(
        "Augmented (mazid) masdar pattern — formal nominal template "
        "for augmented event-name shape without asserting event "
        "occurrence or semantic transformation"
    ),
)

#: NOMINAL_DERIVED_PATTERN (general derived nominal pattern).
NOMINAL_DERIVED_PATTERN_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="NOMINAL_DERIVED_PATTERN",
    description=(
        "Derived nominal weight pattern — formal template for "
        "nominals derived from verbal roots (general category) "
        "without asserting semantic derivation"
    ),
)

#: FAʿIL_FORM (active participle pattern).
FAIL_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="FAIL_FORM",
    description=(
        "Active participle (fa'il) weight pattern — formal nominal "
        "template carrying agency-direction affordance only, without "
        "licensing a formal agent slot or asserting a real agent"
    ),
)

#: MAFʿUL_FORM (passive participle pattern).
MAFUL_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="MAFUL_FORM",
    description=(
        "Passive participle (maf'ul) weight pattern — formal nominal "
        "template carrying patient-direction affordance only, without "
        "licensing a formal object slot or asserting a real patient"
    ),
)

#: SIFAH_MUSHABBAHA_FORM (resembling adjective pattern).
SIFAH_MUSHABBAHA_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="SIFAH_MUSHABBAHA_FORM",
    description=(
        "Resembling adjective (sifah mushabbahah) weight pattern — "
        "formal nominal template for stable-attribute shape without "
        "asserting an attribute judgment"
    ),
)

#: INSTRUMENT_FORM (instrument noun pattern).
INSTRUMENT_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="INSTRUMENT_FORM",
    description=(
        "Instrument noun (ism alah) weight pattern — formal nominal "
        "template for instrument-shape affordance without asserting "
        "an actual instrument"
    ),
)

#: TIME_PLACE_FORM (time/place noun pattern).
TIME_PLACE_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="TIME_PLACE_FORM",
    description=(
        "Time/place noun (ism zaman/makan) weight pattern — formal "
        "nominal template for time/place-shape affordance without "
        "asserting real time or real place"
    ),
)

#: JAMID_WEIGHT_FORM (non-derived nominal weight).
JAMID_WEIGHT_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="JAMID_WEIGHT_FORM",
    description=(
        "Non-derived (jamid) nominal weight pattern — formal template "
        "for nominals with fixed root-pattern shape not derived from "
        "a verbal root"
    ),
)

#: GENDERED_WEIGHT_FORM (gendered pattern marking).
GENDERED_WEIGHT_FORM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family_id="GENDERED_WEIGHT_FORM",
    description=(
        "Gendered weight pattern — formal template marking "
        "masculine/feminine pattern shape only, without asserting "
        "real sex or gender judgment"
    ),
)

#: All WEIGHT_PATTERN families.
WEIGHT_PATTERN_FAMILIES: tuple[FormalShapeFamily, ...] = (
    VERBAL_MUJARRAD_PATTERN_FAMILY,
    VERBAL_MAZID_PATTERN_FAMILY,
    MASDAR_MUJARRAD_PATTERN_FAMILY,
    MASDAR_MAZID_PATTERN_FAMILY,
    NOMINAL_DERIVED_PATTERN_FAMILY,
    FAIL_FORM_FAMILY,
    MAFUL_FORM_FAMILY,
    SIFAH_MUSHABBAHA_FORM_FAMILY,
    INSTRUMENT_FORM_FAMILY,
    TIME_PLACE_FORM_FAMILY,
    JAMID_WEIGHT_FORM_FAMILY,
    GENDERED_WEIGHT_FORM_FAMILY,
)


# ---------------------------------------------------------------------------
# define_weight_pattern_shape() — the definition operation
# ---------------------------------------------------------------------------


def define_weight_pattern_shape(
    shape_id: str,
    family: FormalShapeFamily,
    canonical_name: str,
    definition_text: str,
    distinguishing_evidence: str,
    boundary_conditions: tuple[str, ...],
    exclusion_conditions: tuple[str, ...],
    weight_constraint: str | None = None,
    path_constraint: str | None = None,
) -> WeightPatternDefinitionVerdict:
    """Prove a weight-pattern formal shape definition (docs/34 §7).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    Parameters
    ----------
    shape_id : str
        Globally unique identifier for this formal shape.
    family : FormalShapeFamily
        Must belong to the WEIGHT_PATTERN domain.
    canonical_name : str
        The Arabic grammatical term (e.g., "fa'il", "maf'ul").
    definition_text : str
        Formal textual definition proving the shape.
    distinguishing_evidence : str
        What proves this shape vs. other weight-pattern families.
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
    WeightPatternDefinitionVerdict
        DEFINED with a FormalShapeDefinition on success; REFUSED with a
        named FailureCode on any violation.
    """
    # --- Input boundary: shape_id ---
    if not isinstance(shape_id, str) or not shape_id.strip():
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/shape_id_empty",
        )

    # --- Input boundary: family type and domain ---
    if not isinstance(family, FormalShapeFamily):
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/family_not_formal_shape_family",
        )
    if family.domain is not FormalShapeDomain.WEIGHT_PATTERN:
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.DOMAIN_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/family_domain_not_weight_pattern",
        )

    # --- Input boundary: canonical_name ---
    if not isinstance(canonical_name, str) or not canonical_name.strip():
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/canonical_name_empty",
        )

    # --- Input boundary: definition_text ---
    if not isinstance(definition_text, str) or not definition_text.strip():
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/definition_text_empty",
        )

    # --- Input boundary: distinguishing_evidence ---
    if not isinstance(distinguishing_evidence, str) or not distinguishing_evidence.strip():
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/distinguishing_evidence_empty",
        )

    # --- Input boundary: boundary_conditions ---
    if not isinstance(boundary_conditions, tuple):
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/boundary_conditions_not_tuple",
        )
    if not boundary_conditions:
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/boundary_conditions_empty",
        )
    for bc in boundary_conditions:
        if not isinstance(bc, str) or not bc.strip():
            return WeightPatternDefinitionVerdict(
                definition=None,
                verdict_state=WeightPatternDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_weight_pattern_shape/refused/boundary_condition_invalid",
            )

    # --- Input boundary: exclusion_conditions ---
    if not isinstance(exclusion_conditions, tuple):
        return WeightPatternDefinitionVerdict(
            definition=None,
            verdict_state=WeightPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_weight_pattern_shape/refused/exclusion_conditions_not_tuple",
        )
    for ec in exclusion_conditions:
        if not isinstance(ec, str) or not ec.strip():
            return WeightPatternDefinitionVerdict(
                definition=None,
                verdict_state=WeightPatternDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_weight_pattern_shape/refused/exclusion_condition_invalid",
            )

    # --- Rank bounding via lattice meet ---
    definition_rank = RankLattice.meet(
        Rank.CANDIDATE,
        FORMAL_SHAPE_RANK_CEILING,
    )

    # --- Residuals: open residual noting weight form does not carry meaning ---
    open_residuals: tuple[Residual, ...] = (
        Residual(
            name=f"weight_pattern_not_meaning/{shape_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"FormalShapeDefinition({shape_id}) is weight pattern form, "
                f"not meaning — WEIGHT_PATTERN ≠ meaning, "
                f"WEIGHT_PATTERN ≠ event occurrence"
            ),
        ),
    )

    # --- Construct the FormalShapeDefinition ---
    definition = FormalShapeDefinition(
        shape_id=shape_id,
        domain=FormalShapeDomain.WEIGHT_PATTERN,
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
        trace_ref=f"define_weight_pattern_shape/defined/{shape_id}",
    )

    return WeightPatternDefinitionVerdict(
        definition=definition,
        verdict_state=WeightPatternDefinitionState.DEFINED,
        failure_code=None,
        verdict_rank=definition_rank,
        residuals=open_residuals,
        trace_ref=f"define_weight_pattern_shape/defined/{shape_id}",
    )


# ---------------------------------------------------------------------------
# Canonical WEIGHT_PATTERN definitions (docs/34 §7)
# ---------------------------------------------------------------------------

#: VERBAL_MUJARRAD_PATTERN formal definition.
VERBAL_MUJARRAD_PATTERN_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.VERBAL_MUJARRAD_PATTERN",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=VERBAL_MUJARRAD_PATTERN_FAMILY,
    canonical_name="fi'l mujarrad",
    definition_text=(
        "A formal verbal weight template built on a trilateral or "
        "quadrilateral root without augmentation letters. Proved by "
        "root-letter correspondence to the base pattern (fa'ala, "
        "fa'ila, fa'ula for trilateral; fa'lala for quadrilateral). "
        "This is a pattern shape, not an event or action."
    ),
    distinguishing_evidence=(
        "Root letters correspond exactly to template positions "
        "without augmentation — trilateral (fa'ala/fa'ila/fa'ula) or "
        "quadrilateral (fa'lala) — distinguishing from mazid patterns "
        "which carry additional formal letters."
    ),
    boundary_conditions=(
        "Root letters fill all template positions without remainder",
        "No augmentation letter present (no extra beyond root)",
        "Template is verbal (carries tense-form marking, detail deferred to PR-F5)",
        "Trilateral or quadrilateral root structure",
    ),
    exclusion_conditions=(
        "VERBAL_MUJARRAD_PATTERN ≠ actual action or event occurrence",
        "Does not assert tense reality (tense-form is formal pattern only)",
        "Does not carry augmentation letters (would be mazid)",
        "Does not assert agency or patienthood",
    ),
    weight_constraint="Root letters only — no augmentation",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.VERBAL_MUJARRAD_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.VERBAL_MUJARRAD_PATTERN) "
                "is formal pattern, not meaning — VERBAL_PATTERN_FORM "
                "≠ event occurrence"
            ),
        ),
        Residual(
            name="INFLECTION_DEFERRED_TO_PR_F5/WEIGHT_PATTERN.VERBAL_MUJARRAD_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Tense/mood inflection effects not licensed here — "
                "deferred to PR-F5 (Inflection Formal Definitions)."
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/WEIGHT_PATTERN.VERBAL_MUJARRAD_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Subject/object contract-slot licensing not available here — "
                "deferred to PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.VERBAL_MUJARRAD_PATTERN",
)

#: VERBAL_MAZID_PATTERN formal definition.
VERBAL_MAZID_PATTERN_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.VERBAL_MAZID_PATTERN",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=VERBAL_MAZID_PATTERN_FAMILY,
    canonical_name="fi'l mazid",
    definition_text=(
        "A formal verbal weight template carrying one or more "
        "augmentation letters beyond the base root. Proved by "
        "identification of extra letters (hamzah, ta', nun, etc.) "
        "on known augmentation patterns (if'ala, tafa''ala, "
        "infa'ala, ifta'ala, etc.). This is a pattern shape, not "
        "a semantic transformation."
    ),
    distinguishing_evidence=(
        "Template carries identifiable augmentation letters beyond "
        "root positions — (if'ala, fa''ala, fa'ala, tafa''ala, "
        "infa'ala, ifta'ala, if'alla, istaf'ala, etc.) — "
        "distinguishing from mujarrad patterns which carry no "
        "augmentation."
    ),
    boundary_conditions=(
        "One or more augmentation letters beyond root letters",
        "Augmentation follows known formal patterns (abwab)",
        "Template is verbal (carries tense-form marking, detail deferred to PR-F5)",
        "Augmentation is formal addition, not semantic assertion",
    ),
    exclusion_conditions=(
        "VERBAL_MAZID_PATTERN ≠ semantic transformation",
        "Does not assert causation, reflexivity, or mutual action as reality",
        "Does not assert tense reality (tense-form is formal pattern only)",
        "Does not carry agency or patienthood assertions",
    ),
    weight_constraint="Root letters plus identifiable augmentation letters",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.VERBAL_MAZID_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.VERBAL_MAZID_PATTERN) "
                "is formal pattern, not meaning — VERBAL_MAZID_PATTERN "
                "≠ semantic transformation"
            ),
        ),
        Residual(
            name="INFLECTION_DEFERRED_TO_PR_F5/WEIGHT_PATTERN.VERBAL_MAZID_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Tense/mood inflection effects not licensed here — "
                "deferred to PR-F5 (Inflection Formal Definitions)."
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/WEIGHT_PATTERN.VERBAL_MAZID_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Subject/object contract-slot licensing not available here — "
                "deferred to PR-F6 (Contract Slot Formal Definitions)."
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.VERBAL_MAZID_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah (what augmentation 'means') not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.VERBAL_MAZID_PATTERN",
)

#: MASDAR_MUJARRAD_PATTERN formal definition.
MASDAR_MUJARRAD_PATTERN_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.MASDAR_MUJARRAD_PATTERN",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=MASDAR_MUJARRAD_PATTERN_FAMILY,
    canonical_name="masdar mujarrad",
    definition_text=(
        "A formal nominal weight template for the event-name shape "
        "derived from a base (mujarrad) verbal root. Proved by "
        "correspondence to known masdar patterns (fa'l, fu'ul, "
        "fi'alah, fu'lah, etc.) without asserting event occurrence, "
        "time, place, or reality."
    ),
    distinguishing_evidence=(
        "Nominal template corresponding to base verbal root with "
        "known masdar weight patterns (fa'l, fu'ul, fi'alah, etc.) — "
        "distinguishing from mazid masdar which requires augmentation "
        "and from verbal patterns which carry tense-form."
    ),
    boundary_conditions=(
        "Nominal template (not verbal — no tense-form marking)",
        "Derived from mujarrad (base) verbal root",
        "Matches known masdar weight patterns",
        "Event-name shape abstraction only",
    ),
    exclusion_conditions=(
        "MASDAR_MUJARRAD_PATTERN ≠ event occurrence",
        "MASDAR_FORM ≠ time/place",
        "Does not assert temporal reality",
        "Does not carry tense-form marking (would be verbal pattern)",
    ),
    weight_constraint="Masdar of mujarrad — no augmentation in source verb",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.MASDAR_MUJARRAD_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.MASDAR_MUJARRAD_PATTERN) "
                "is formal pattern, not meaning — MASDAR_FORM ≠ event occurrence"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.MASDAR_MUJARRAD_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah of masdar not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.MASDAR_MUJARRAD_PATTERN",
)

#: MASDAR_MAZID_PATTERN formal definition.
MASDAR_MAZID_PATTERN_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.MASDAR_MAZID_PATTERN",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=MASDAR_MAZID_PATTERN_FAMILY,
    canonical_name="masdar mazid",
    definition_text=(
        "A formal nominal weight template for the event-name shape "
        "derived from an augmented (mazid) verbal root. Proved by "
        "correspondence to known augmented masdar patterns (if'al, "
        "taf'il, tafa''ul, infi'al, ifti'al, istif'al, etc.) "
        "without asserting event occurrence or semantic transformation."
    ),
    distinguishing_evidence=(
        "Nominal template corresponding to augmented verbal root "
        "with known mazid masdar patterns (if'al, taf'il, etc.) — "
        "distinguishing from mujarrad masdar which has no augmentation "
        "and from verbal mazid which carries tense-form."
    ),
    boundary_conditions=(
        "Nominal template (not verbal — no tense-form marking)",
        "Derived from mazid (augmented) verbal root",
        "Matches known augmented masdar weight patterns",
        "Event-name shape abstraction only",
    ),
    exclusion_conditions=(
        "MASDAR_MAZID_PATTERN ≠ event occurrence",
        "MASDAR_FORM ≠ time/place",
        "Does not assert semantic transformation as reality",
        "Does not carry tense-form marking (would be verbal pattern)",
    ),
    weight_constraint="Masdar of mazid — augmentation in source verb",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.MASDAR_MAZID_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.MASDAR_MAZID_PATTERN) "
                "is formal pattern, not meaning — MASDAR_FORM ≠ event occurrence"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.MASDAR_MAZID_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah of augmented masdar not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.MASDAR_MAZID_PATTERN",
)

#: NOMINAL_DERIVED_PATTERN formal definition.
NOMINAL_DERIVED_PATTERN_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.NOMINAL_DERIVED_PATTERN",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=NOMINAL_DERIVED_PATTERN_FAMILY,
    canonical_name="ism mushtaq (general)",
    definition_text=(
        "A formal nominal weight template for general derived shapes "
        "not covered by the specialized fa'il, maf'ul, sifah, "
        "instrument, or time/place families. Proved by root-pattern "
        "correspondence showing derivation from a verbal root "
        "without asserting dalalah or meaning production."
    ),
    distinguishing_evidence=(
        "Nominal template with verbal-root derivation pattern not "
        "matching fa'il, maf'ul, sifah mushabbahah, instrument, "
        "or time/place specialized patterns — general derived "
        "nominal category."
    ),
    boundary_conditions=(
        "Nominal template derived from verbal root",
        "Does not match specialized families (fa'il, maf'ul, etc.)",
        "Root-pattern correspondence provable",
        "General derived nominal shape",
    ),
    exclusion_conditions=(
        "NOMINAL_DERIVED_PATTERN ≠ semantic derivation",
        "Does not assert what the derivation 'produces' semantically",
        "Does not match fa'il/maf'ul/sifah/instrument/time-place patterns",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.NOMINAL_DERIVED_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.NOMINAL_DERIVED_PATTERN) "
                "is formal pattern, not meaning — MUSHTAQ_FORM "
                "≠ semantic derivation"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.NOMINAL_DERIVED_PATTERN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah of derived nominal not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.NOMINAL_DERIVED_PATTERN",
)

#: FAʿIL_FORM formal definition.
FAIL_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.FAIL_FORM",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=FAIL_FORM_FAMILY,
    canonical_name="ism fa'il",
    definition_text=(
        "A formal nominal weight template on the pattern fa'il "
        "(trilateral) or equivalent augmented active-participle "
        "patterns. Carries agency-direction affordance as formal "
        "shape only. Does not license a formal agent slot and does "
        "not assert agency in the world."
    ),
    distinguishing_evidence=(
        "Nominal template on fa'il pattern (or muf'il, mutafa''il, "
        "munfa'il, mufta'il, mustaf'il for augmented forms) — "
        "carries agency-direction formal affordance — distinguishing "
        "from maf'ul which carries patient-direction."
    ),
    boundary_conditions=(
        "Nominal template on active-participle weight pattern",
        "Agency-direction affordance (formal shape only)",
        "Root-pattern correspondence to verbal source provable",
        "Pattern: fa'il (mujarrad) or muf'il/mutafa''il/etc. (mazid)",
    ),
    exclusion_conditions=(
        "FAʿIL_FORM ≠ real agent",
        "FAʿIL_FORM ≠ FORMAL_AGENT_SLOT (deferred to PR-F6)",
        "Does not assert actual agency or action occurrence",
        "Does not license subject/agent contract slot",
    ),
    weight_constraint="Active-participle pattern (fa'il or augmented equivalent)",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.FAIL_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.FAIL_FORM) is formal "
                "pattern, not meaning — FAʿIL_FORM ≠ real agent"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/WEIGHT_PATTERN.FAIL_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FAʿIL_FORM opens formal agency-direction affordance but "
                "does NOT license FORMAL_AGENT_SLOT — deferred to PR-F6 "
                "(Contract Slot Formal Definitions)."
            ),
        ),
        Residual(
            name="INFLECTION_DEFERRED_TO_PR_F5/WEIGHT_PATTERN.FAIL_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Inflection effects (i'rab) on fa'il form not licensed "
                "here — deferred to PR-F5 (Inflection Formal Definitions)."
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.FAIL_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah of agency-direction not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.FAIL_FORM",
)

#: MAFʿUL_FORM formal definition.
MAFUL_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.MAFUL_FORM",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=MAFUL_FORM_FAMILY,
    canonical_name="ism maf'ul",
    definition_text=(
        "A formal nominal weight template on the pattern maf'ul "
        "(trilateral) or equivalent augmented passive-participle "
        "patterns. Carries patient-direction affordance as formal "
        "shape only. Does not license a formal object slot and does "
        "not assert patient-hood in the world."
    ),
    distinguishing_evidence=(
        "Nominal template on maf'ul pattern (or muf'al, mutafa''al, "
        "munfa'al, mufta'al, mustaf'al for augmented forms) — "
        "carries patient-direction formal affordance — distinguishing "
        "from fa'il which carries agency-direction."
    ),
    boundary_conditions=(
        "Nominal template on passive-participle weight pattern",
        "Patient-direction affordance (formal shape only)",
        "Root-pattern correspondence to verbal source provable",
        "Pattern: maf'ul (mujarrad) or muf'al/mutafa''al/etc. (mazid)",
    ),
    exclusion_conditions=(
        "MAFʿUL_FORM ≠ real patient",
        "MAFʿUL_FORM ≠ FORMAL_OBJECT_SLOT (deferred to PR-F6)",
        "Does not assert actual patienthood or being-acted-upon",
        "Does not license object contract slot",
    ),
    weight_constraint="Passive-participle pattern (maf'ul or augmented equivalent)",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.MAFUL_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.MAFUL_FORM) is formal "
                "pattern, not meaning — MAFʿUL_FORM ≠ real patient"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/WEIGHT_PATTERN.MAFUL_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "MAFʿUL_FORM opens formal patient-direction affordance but "
                "does NOT license FORMAL_OBJECT_SLOT — deferred to PR-F6 "
                "(Contract Slot Formal Definitions)."
            ),
        ),
        Residual(
            name="INFLECTION_DEFERRED_TO_PR_F5/WEIGHT_PATTERN.MAFUL_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Inflection effects (i'rab) on maf'ul form not licensed "
                "here — deferred to PR-F5 (Inflection Formal Definitions)."
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.MAFUL_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah of patient-direction not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.MAFUL_FORM",
)

#: SIFAH_MUSHABBAHA_FORM formal definition.
SIFAH_MUSHABBAHA_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.SIFAH_MUSHABBAHA_FORM",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=SIFAH_MUSHABBAHA_FORM_FAMILY,
    canonical_name="sifah mushabbahah",
    definition_text=(
        "A formal nominal weight template for the resembling-adjective "
        "pattern (fa'il, fa'al, fa'lan, af'al, etc. when denoting "
        "stable attribute shape). Carries stable-attribute shape "
        "affordance only without asserting an attribute judgment."
    ),
    distinguishing_evidence=(
        "Nominal template on known sifah mushabbahah patterns "
        "(fa'il/fa'al/fa'lan/af'al with stable-attribute reading) — "
        "distinguishing from active participle fa'il by stability "
        "and from maf'ul by direction."
    ),
    boundary_conditions=(
        "Nominal template on resembling-adjective weight pattern",
        "Stable-attribute shape affordance (not transient action)",
        "Known sifah mushabbahah patterns",
        "Typically from intransitive verbs (formal pattern only)",
    ),
    exclusion_conditions=(
        "SIFAH_MUSHABBAHA_FORM ≠ attribute judgment",
        "Does not assert that the subject 'is' the attribute in reality",
        "Does not carry agency-direction (would be fa'il pattern)",
        "Does not carry patient-direction (would be maf'ul pattern)",
    ),
    weight_constraint="Sifah mushabbahah patterns",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.SIFAH_MUSHABBAHA_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.SIFAH_MUSHABBAHA_FORM) "
                "is formal pattern, not meaning — SIFAH_MUSHABBAHA_FORM "
                "≠ attribute judgment"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.SIFAH_MUSHABBAHA_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah of stable-attribute not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.SIFAH_MUSHABBAHA_FORM",
)

#: INSTRUMENT_FORM formal definition.
INSTRUMENT_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.INSTRUMENT_FORM",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=INSTRUMENT_FORM_FAMILY,
    canonical_name="ism alah",
    definition_text=(
        "A formal nominal weight template for the instrument-noun "
        "pattern (mif'al, mif'alah, mi'fal, fa''alah, etc.). "
        "Carries instrument-shape affordance only without asserting "
        "instrumentality in the world."
    ),
    distinguishing_evidence=(
        "Nominal template on known instrument-noun patterns "
        "(mif'al, mif'alah, mi'fal, fa''alah) — distinguishing from "
        "time/place patterns (maf'al, maf'il) and from fa'il/maf'ul."
    ),
    boundary_conditions=(
        "Nominal template on instrument-noun weight pattern",
        "Instrument-shape affordance (formal pattern only)",
        "Known ism alah patterns (mif'al, mif'alah, mi'fal, fa''alah)",
        "Root-pattern correspondence provable",
    ),
    exclusion_conditions=(
        "INSTRUMENT_FORM ≠ actual instrument",
        "Does not assert that something 'is' a tool in reality",
        "Does not match time/place patterns (would be TIME_PLACE_FORM)",
        "Does not carry agency/patient direction",
    ),
    weight_constraint="Instrument-noun patterns (mif'al, mif'alah, mi'fal, fa''alah)",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.INSTRUMENT_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.INSTRUMENT_FORM) "
                "is formal pattern, not meaning — INSTRUMENT_FORM "
                "≠ actual instrument"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.INSTRUMENT_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah of instrument-shape not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.INSTRUMENT_FORM",
)

#: TIME_PLACE_FORM formal definition.
TIME_PLACE_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.TIME_PLACE_FORM",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=TIME_PLACE_FORM_FAMILY,
    canonical_name="ism zaman wa-makan",
    definition_text=(
        "A formal nominal weight template for the time/place-noun "
        "pattern (maf'al, maf'il, maf'alah). Carries time/place "
        "shape affordance only without asserting temporal or spatial "
        "reference."
    ),
    distinguishing_evidence=(
        "Nominal template on known time/place patterns "
        "(maf'al, maf'il, maf'alah) — distinguishing from instrument "
        "patterns (mif'al, mif'alah) by vowel pattern and from "
        "maf'ul by template structure."
    ),
    boundary_conditions=(
        "Nominal template on time/place-noun weight pattern",
        "Time/place-shape affordance (formal pattern only)",
        "Known ism zaman/makan patterns (maf'al, maf'il, maf'alah)",
        "Root-pattern correspondence provable",
    ),
    exclusion_conditions=(
        "TIME_PLACE_FORM ≠ real time/place",
        "Does not assert temporal or spatial reality",
        "Does not match instrument patterns (would be INSTRUMENT_FORM)",
        "Does not carry agency/patient direction",
    ),
    weight_constraint="Time/place-noun patterns (maf'al, maf'il, maf'alah)",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.TIME_PLACE_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.TIME_PLACE_FORM) "
                "is formal pattern, not meaning — TIME_PLACE_FORM "
                "≠ real time/place"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/WEIGHT_PATTERN.TIME_PLACE_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Semantic dalalah of time/place-shape not licensed — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.TIME_PLACE_FORM",
)

#: JAMID_WEIGHT_FORM formal definition.
JAMID_WEIGHT_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.JAMID_WEIGHT_FORM",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=JAMID_WEIGHT_FORM_FAMILY,
    canonical_name="ism jamid (wazn)",
    definition_text=(
        "A formal nominal weight template for non-derived (jamid) "
        "nominals — words whose pattern is fixed and not derived "
        "from a verbal root. Proved by absence of verbal-root "
        "derivation path. This is a weight-pattern classification, "
        "not a semantic assertion."
    ),
    distinguishing_evidence=(
        "Nominal template without provable verbal-root derivation — "
        "pattern is primary/fixed rather than derived — distinguishing "
        "from all mushtaq (derived) families which require a verbal "
        "source."
    ),
    boundary_conditions=(
        "Nominal template with fixed (non-derived) pattern",
        "No provable verbal-root derivation path",
        "Weight pattern classifiable (e.g. fa'l, fu'l, fi'l, fu'al)",
        "Jamid status is pattern classification only",
    ),
    exclusion_conditions=(
        "JAMID_WEIGHT_FORM does not assert essence or substance",
        "Does not assert that the word 'is' its referent",
        "Does not have a verbal derivation path (would be mushtaq)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.JAMID_WEIGHT_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.JAMID_WEIGHT_FORM) "
                "is formal pattern, not meaning — weight classification "
                "≠ semantic content"
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.JAMID_WEIGHT_FORM",
)

#: GENDERED_WEIGHT_FORM formal definition.
GENDERED_WEIGHT_FORM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WEIGHT_PATTERN.GENDERED_WEIGHT_FORM",
    domain=FormalShapeDomain.WEIGHT_PATTERN,
    family=GENDERED_WEIGHT_FORM_FAMILY,
    canonical_name="wazn mudhakkar/mu'annath",
    definition_text=(
        "A formal weight-pattern template carrying masculine or "
        "feminine gender marking as morphological shape only. Proved "
        "by presence of ta' marbuta, alif maqsurah, alif mamdudah, "
        "or known gendered patterns. Does not assert real sex or "
        "gender judgment."
    ),
    distinguishing_evidence=(
        "Weight pattern carrying gender-marking morphemes (ta' "
        "marbuta, alif ta'nith maqsurah/mamdudah) or known gendered "
        "patterns (fa'lah, fu'la, fA'ilah, etc.) — distinguishing "
        "from ungendered forms by presence of gender-shape markers."
    ),
    boundary_conditions=(
        "Weight pattern with gender-marking morphological shape",
        "Gender marker is formal pattern feature only",
        "Known gender-marking patterns or suffixes present",
        "Applies to both inherently and formally gendered nominals",
    ),
    exclusion_conditions=(
        "GENDERED_WEIGHT_FORM ≠ real sex/gender judgment",
        "Does not assert biological sex or social gender",
        "Gender marking is morphological pattern, not reality assertion",
    ),
    weight_constraint="Gendered patterns or gender-marking morphemes",
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="weight_pattern_not_meaning/WEIGHT_PATTERN.GENDERED_WEIGHT_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WEIGHT_PATTERN.GENDERED_WEIGHT_FORM) "
                "is formal pattern, not meaning — GENDERED_WEIGHT_FORM "
                "≠ real sex/gender judgment"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/WEIGHT_PATTERN.GENDERED_WEIGHT_FORM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Gender agreement composition patterns not licensed here — "
                "deferred to PR-F7 (Composition Pattern Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/WEIGHT_PATTERN.GENDERED_WEIGHT_FORM",
)


# ---------------------------------------------------------------------------
# build_weight_pattern_registry() — assemble WEIGHT_PATTERN registry
# ---------------------------------------------------------------------------


def build_weight_pattern_registry(
    definitions: tuple[FormalShapeDefinition, ...] | None = None,
) -> FormalShapeRegistry:
    """Assemble the WEIGHT_PATTERN domain registry (docs/34 §7).

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
            VERBAL_MUJARRAD_PATTERN_DEFINITION,
            VERBAL_MAZID_PATTERN_DEFINITION,
            MASDAR_MUJARRAD_PATTERN_DEFINITION,
            MASDAR_MAZID_PATTERN_DEFINITION,
            NOMINAL_DERIVED_PATTERN_DEFINITION,
            FAIL_FORM_DEFINITION,
            MAFUL_FORM_DEFINITION,
            SIFAH_MUSHABBAHA_FORM_DEFINITION,
            INSTRUMENT_FORM_DEFINITION,
            TIME_PLACE_FORM_DEFINITION,
            JAMID_WEIGHT_FORM_DEFINITION,
            GENDERED_WEIGHT_FORM_DEFINITION,
        )

    # Validate all definitions belong to WEIGHT_PATTERN
    for defn in definitions:
        if defn.domain is not FormalShapeDomain.WEIGHT_PATTERN:
            return FormalShapeRegistry(
                domain=FormalShapeDomain.WEIGHT_PATTERN,
                families=WEIGHT_PATTERN_FAMILIES,
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
                    domain=FormalShapeDomain.WEIGHT_PATTERN,
                    families=WEIGHT_PATTERN_FAMILIES,
                    definitions=definitions,
                    rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                    closure_state=FormalShapeClosureState.REFUSED,
                )

    # Compute closure state
    if not definitions:
        closure_state = FormalShapeClosureState.EMPTY
    else:
        required_family_ids = {f.family_id for f in WEIGHT_PATTERN_FAMILIES}
        covered_family_ids = {d.family.family_id for d in definitions}
        if required_family_ids <= covered_family_ids:
            closure_state = FormalShapeClosureState.CLOSED
        else:
            closure_state = FormalShapeClosureState.PARTIAL

    return FormalShapeRegistry(
        domain=FormalShapeDomain.WEIGHT_PATTERN,
        families=WEIGHT_PATTERN_FAMILIES,
        definitions=definitions,
        rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
        closure_state=closure_state,
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "FAIL_FORM_DEFINITION",
    "FAIL_FORM_FAMILY",
    "GENDERED_WEIGHT_FORM_DEFINITION",
    "GENDERED_WEIGHT_FORM_FAMILY",
    "INSTRUMENT_FORM_DEFINITION",
    "INSTRUMENT_FORM_FAMILY",
    "JAMID_WEIGHT_FORM_DEFINITION",
    "JAMID_WEIGHT_FORM_FAMILY",
    "MAFUL_FORM_DEFINITION",
    "MAFUL_FORM_FAMILY",
    "MASDAR_MAZID_PATTERN_DEFINITION",
    "MASDAR_MAZID_PATTERN_FAMILY",
    "MASDAR_MUJARRAD_PATTERN_DEFINITION",
    "MASDAR_MUJARRAD_PATTERN_FAMILY",
    "NOMINAL_DERIVED_PATTERN_DEFINITION",
    "NOMINAL_DERIVED_PATTERN_FAMILY",
    "SIFAH_MUSHABBAHA_FORM_DEFINITION",
    "SIFAH_MUSHABBAHA_FORM_FAMILY",
    "TIME_PLACE_FORM_DEFINITION",
    "TIME_PLACE_FORM_FAMILY",
    "VERBAL_MAZID_PATTERN_DEFINITION",
    "VERBAL_MAZID_PATTERN_FAMILY",
    "VERBAL_MUJARRAD_PATTERN_DEFINITION",
    "VERBAL_MUJARRAD_PATTERN_FAMILY",
    "WEIGHT_PATTERN_FAMILIES",
    "WeightPatternDefinitionState",
    "WeightPatternDefinitionVerdict",
    "build_weight_pattern_registry",
    "define_weight_pattern_shape",
]
