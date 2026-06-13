"""Built and Reference Formal Definitions — PR-F3.

PR-F3 binding of ``docs/34_FORMAL_SHAPE_REGISTRY_LAW.md`` §6
(BUILT_REFERENCE).

This module introduces the BUILT_REFERENCE domain families and their
canonical formal definitions. Built forms are morphologically "built"
(mabnī) on fixed patterns and reference forms.

Constitutional invariants (docs/34 §6):

* PERSONAL_PRONOUN_FORM ≠ resolved reference.
* DEMONSTRATIVE_FORM ≠ pointed real object.
* RELATIVE_PRONOUN_FORM ≠ completed ṣilah meaning.
* INTERROGATIVE_FORM ≠ question intent.
* CONDITIONAL_FORM ≠ conditional truth.
* FormalShapeDefinition ≠ Meaning.
* FormalShapeDefinition ≠ SemanticEntry.
* FormalShapeDefinition ≠ WadʿiSignified.
* FormalShapeDefinition ≠ Dalālah.
* FormalShapeDefinition ≠ SyntaxRole.
* FormalShapeRegistry ≠ SemanticLexicon.
* Built/reference form is formal shape, not meaning.
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
# BuiltReferenceDefinitionState — verdict outcome
# ---------------------------------------------------------------------------


class BuiltReferenceDefinitionState(StrEnum):
    """The outcome of a define_built_reference_shape() operation."""

    DEFINED = "DEFINED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# BuiltReferenceDefinitionVerdict — the definition proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BuiltReferenceDefinitionVerdict:
    """The output of :func:`define_built_reference_shape` (docs/34 §6).

    Proves that a built-reference formal shape definition satisfies all
    constitutional requirements. It does NOT carry meaning, ifadah,
    hukm, reality, or any semantic content.
    """

    definition: FormalShapeDefinition | None
    verdict_state: BuiltReferenceDefinitionState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, BuiltReferenceDefinitionState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be BuiltReferenceDefinitionState, "
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
        if self.verdict_state is BuiltReferenceDefinitionState.DEFINED:
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
        elif self.verdict_state is BuiltReferenceDefinitionState.REFUSED:
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
# BUILT_REFERENCE Families (docs/34 §6)
# ---------------------------------------------------------------------------

#: PERSONAL_PRONOUN (ḍamīr) family.
PERSONAL_PRONOUN_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family_id="PERSONAL_PRONOUN",
    description=(
        "Personal pronoun (damir) — morphologically built form that "
        "occupies a noun position without accepting standard ism markers"
    ),
)

#: DEMONSTRATIVE (ism ishārah) family.
DEMONSTRATIVE_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family_id="DEMONSTRATIVE",
    description=(
        "Demonstrative (ism isharah) — built form indicating proximity "
        "or distance without resolving to a pointed object"
    ),
)

#: RELATIVE_PRONOUN (ism mawṣūl) family.
RELATIVE_PRONOUN_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family_id="RELATIVE_PRONOUN",
    description=(
        "Relative pronoun (ism mawsul) — built form opening a dependent "
        "clause attachment without completing the silah"
    ),
)

#: INTERROGATIVE (ism istifhām) family.
INTERROGATIVE_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family_id="INTERROGATIVE",
    description=(
        "Interrogative (ism istifham) — built form opening an inquiry "
        "structure without asserting question intent"
    ),
)

#: CONDITIONAL (adawāt al-sharṭ) family.
CONDITIONAL_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family_id="CONDITIONAL",
    description=(
        "Conditional (adawat al-shart) — built form opening a "
        "protasis-apodosis structure without asserting conditional truth"
    ),
)

#: All BUILT_REFERENCE families.
BUILT_REFERENCE_FAMILIES: tuple[FormalShapeFamily, ...] = (
    PERSONAL_PRONOUN_FAMILY,
    DEMONSTRATIVE_FAMILY,
    RELATIVE_PRONOUN_FAMILY,
    INTERROGATIVE_FAMILY,
    CONDITIONAL_FAMILY,
)


# ---------------------------------------------------------------------------
# define_built_reference_shape() — the definition operation
# ---------------------------------------------------------------------------


def define_built_reference_shape(
    shape_id: str,
    family: FormalShapeFamily,
    canonical_name: str,
    definition_text: str,
    distinguishing_evidence: str,
    boundary_conditions: tuple[str, ...],
    exclusion_conditions: tuple[str, ...],
    weight_constraint: str | None = None,
    path_constraint: str | None = None,
) -> BuiltReferenceDefinitionVerdict:
    """Prove a built-reference formal shape definition (docs/34 §6).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    Parameters
    ----------
    shape_id : str
        Globally unique identifier for this formal shape.
    family : FormalShapeFamily
        Must belong to the BUILT_REFERENCE domain.
    canonical_name : str
        The Arabic grammatical term (e.g., "damir", "ism isharah").
    definition_text : str
        Formal textual definition proving the shape.
    distinguishing_evidence : str
        What proves this shape vs. other built-reference families.
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
    BuiltReferenceDefinitionVerdict
        DEFINED with a FormalShapeDefinition on success; REFUSED with a
        named FailureCode on any violation.
    """
    # --- Input boundary: shape_id ---
    if not isinstance(shape_id, str) or not shape_id.strip():
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/shape_id_empty",
        )

    # --- Input boundary: family type and domain ---
    if not isinstance(family, FormalShapeFamily):
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/family_not_formal_shape_family",
        )
    if family.domain is not FormalShapeDomain.BUILT_REFERENCE:
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.DOMAIN_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/family_domain_not_built_reference",
        )

    # --- Input boundary: canonical_name ---
    if not isinstance(canonical_name, str) or not canonical_name.strip():
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/canonical_name_empty",
        )

    # --- Input boundary: definition_text ---
    if not isinstance(definition_text, str) or not definition_text.strip():
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/definition_text_empty",
        )

    # --- Input boundary: distinguishing_evidence ---
    if not isinstance(distinguishing_evidence, str) or not distinguishing_evidence.strip():
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/distinguishing_evidence_empty",
        )

    # --- Input boundary: boundary_conditions ---
    if not isinstance(boundary_conditions, tuple):
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/boundary_conditions_not_tuple",
        )
    if not boundary_conditions:
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/boundary_conditions_empty",
        )
    for bc in boundary_conditions:
        if not isinstance(bc, str) or not bc.strip():
            return BuiltReferenceDefinitionVerdict(
                definition=None,
                verdict_state=BuiltReferenceDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_built_reference_shape/refused/boundary_condition_invalid",
            )

    # --- Input boundary: exclusion_conditions ---
    if not isinstance(exclusion_conditions, tuple):
        return BuiltReferenceDefinitionVerdict(
            definition=None,
            verdict_state=BuiltReferenceDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_built_reference_shape/refused/exclusion_conditions_not_tuple",
        )
    for ec in exclusion_conditions:
        if not isinstance(ec, str) or not ec.strip():
            return BuiltReferenceDefinitionVerdict(
                definition=None,
                verdict_state=BuiltReferenceDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_built_reference_shape/refused/exclusion_condition_invalid",
            )

    # --- Rank bounding via lattice meet ---
    definition_rank = RankLattice.meet(
        Rank.CANDIDATE,
        FORMAL_SHAPE_RANK_CEILING,
    )

    # --- Residuals: open residual noting built form does not carry meaning ---
    open_residuals: tuple[Residual, ...] = (
        Residual(
            name=f"built_reference_not_meaning/{shape_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"FormalShapeDefinition({shape_id}) is built/reference form, "
                f"not meaning — PRONOUN ≠ referent, DEMONSTRATIVE ≠ object, "
                f"RELATIVE ≠ silah meaning"
            ),
        ),
    )

    # --- Construct the FormalShapeDefinition ---
    definition = FormalShapeDefinition(
        shape_id=shape_id,
        domain=FormalShapeDomain.BUILT_REFERENCE,
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
        trace_ref=f"define_built_reference_shape/defined/{shape_id}",
    )

    return BuiltReferenceDefinitionVerdict(
        definition=definition,
        verdict_state=BuiltReferenceDefinitionState.DEFINED,
        failure_code=None,
        verdict_rank=definition_rank,
        residuals=open_residuals,
        trace_ref=f"define_built_reference_shape/defined/{shape_id}",
    )


# ---------------------------------------------------------------------------
# Canonical BUILT_REFERENCE definitions (docs/34 §6)
# ---------------------------------------------------------------------------

#: PERSONAL_PRONOUN formal definition.
PERSONAL_PRONOUN_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="BUILT_REFERENCE.PERSONAL_PRONOUN",
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family=PERSONAL_PRONOUN_FAMILY,
    canonical_name="damir",
    definition_text=(
        "A morphologically built form that occupies a noun-like formal "
        "slot without accepting the standard ism markers (al-, tanwin, "
        "jarr preposition directly). Proved formally by fixed vowel "
        "pattern (bina') and pronominal substitution capacity. "
        "Specific contract slots deferred to PR-F6."
    ),
    distinguishing_evidence=(
        "Fixed morphological pattern (mabni) with pronominal substitution "
        "capacity — occupies noun-like formal slots without "
        "al-/tanwin/direct jarr acceptance, distinguishing from "
        "mu'rab ism forms."
    ),
    boundary_conditions=(
        "Morphologically built (mabni) — fixed vowel ending",
        "Occupies a noun-like formal slot (contract-slot detail deferred to PR-F6)",
        "Pronominal substitution capacity (stands for a noun)",
        "Subcategories: munfasil (separate), muttasil (attached), mustatir (hidden)",
    ),
    exclusion_conditions=(
        "Does not accept al- (definite article) directly",
        "Does not accept tanwin (nunation)",
        "Does not resolve to a referent (PERSONAL_PRONOUN ≠ resolved reference)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="built_reference_not_meaning/BUILT_REFERENCE.PERSONAL_PRONOUN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(BUILT_REFERENCE.PERSONAL_PRONOUN) is "
                "built form, not meaning — PERSONAL_PRONOUN ≠ resolved reference"
            ),
        ),
        Residual(
            name="CONTRACT_SLOT_DEFERRED_TO_PR_F6/BUILT_REFERENCE.PERSONAL_PRONOUN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Contract-slot labels (fa'il, maf'ul, mubtada') are not "
                "licensed here — deferred to PR-F6 (Contract Slot Formal "
                "Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/BUILT_REFERENCE.PERSONAL_PRONOUN",
)

#: DEMONSTRATIVE formal definition.
DEMONSTRATIVE_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="BUILT_REFERENCE.DEMONSTRATIVE",
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family=DEMONSTRATIVE_FAMILY,
    canonical_name="ism isharah",
    definition_text=(
        "A morphologically built form that opens a proximity/distance "
        "indication slot without resolving to a pointed real object. "
        "Proved formally by fixed pattern (bina'), gender/number "
        "inflection on a closed set, and deictic position marking."
    ),
    distinguishing_evidence=(
        "Fixed morphological set with gender/number variants (hadha, "
        "hadhihi, dhalika, tilka, etc.) carrying deictic position "
        "marking — distinguishing from personal pronouns which lack "
        "proximity/distance indication."
    ),
    boundary_conditions=(
        "Morphologically built (mabni) — fixed pattern",
        "Carries gender/number formal variants (closed set)",
        "Opens proximity/distance indication slot",
        "Deictic position marking (near: hadha/hadhihi, far: dhalika/tilka)",
    ),
    exclusion_conditions=(
        "Does not accept tanwin (nunation)",
        "Does not point to a real object (DEMONSTRATIVE ≠ pointed real object)",
        "Does not substitute for a noun (would be pronoun)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="built_reference_not_meaning/BUILT_REFERENCE.DEMONSTRATIVE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(BUILT_REFERENCE.DEMONSTRATIVE) is "
                "built form, not meaning — DEMONSTRATIVE ≠ pointed real object"
            ),
        ),
    ),
    trace_ref="canonical/BUILT_REFERENCE.DEMONSTRATIVE",
)

#: RELATIVE_PRONOUN formal definition.
RELATIVE_PRONOUN_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="BUILT_REFERENCE.RELATIVE_PRONOUN",
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family=RELATIVE_PRONOUN_FAMILY,
    canonical_name="ism mawsul",
    definition_text=(
        "A morphologically built form that opens a dependent-clause "
        "attachment slot (silah al-mawsul) without completing the "
        "clause or asserting its content. Proved formally by fixed "
        "pattern, requirement of a following silah clause, and "
        "return pronoun (a'id) linkage."
    ),
    distinguishing_evidence=(
        "Requires a following silah clause with a return pronoun "
        "(a'id) — specific (alladhi, allati, alladhina) or generic "
        "(man, ma) — distinguishing from demonstratives which do "
        "not open a clause attachment."
    ),
    boundary_conditions=(
        "Morphologically built (mabni) — fixed pattern",
        "Opens a silah clause attachment slot",
        "Requires a return pronoun (a'id) in the silah",
        "Two subcategories: specific (alladhi-set) and generic (man, ma)",
    ),
    exclusion_conditions=(
        "Does not accept tanwin (nunation)",
        "Does not complete silah meaning (RELATIVE_PRONOUN ≠ completed silah meaning)",
        "Does not carry proximity/distance marking (would be demonstrative)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="built_reference_not_meaning/BUILT_REFERENCE.RELATIVE_PRONOUN",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(BUILT_REFERENCE.RELATIVE_PRONOUN) is "
                "built form, not meaning — RELATIVE_PRONOUN ≠ completed "
                "silah meaning"
            ),
        ),
    ),
    trace_ref="canonical/BUILT_REFERENCE.RELATIVE_PRONOUN",
)

#: INTERROGATIVE formal definition.
INTERROGATIVE_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="BUILT_REFERENCE.INTERROGATIVE",
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family=INTERROGATIVE_FAMILY,
    canonical_name="ism istifham",
    definition_text=(
        "A morphologically built form that opens an inquiry structure "
        "slot without asserting question intent or expecting an answer. "
        "Proved formally by fixed pattern and sentence-initial position "
        "requirement. Governance detail deferred to PR-F5/PR-F7."
    ),
    distinguishing_evidence=(
        "Opens formal inquiry structure from sentence-initial position "
        "(man, ma, ayyu, mata, ayna, kayfa, kam, etc.) — distinguishing "
        "from relative pronouns which open dependent clause attachment "
        "rather than inquiry."
    ),
    boundary_conditions=(
        "Morphologically built (mabni) — fixed pattern (most members)",
        "Sentence-initial formal position (sadarah)",
        "Opens inquiry formal structure (governance detail deferred to PR-F5/PR-F7)",
        "Closed set: man, ma, ayyu, mata, ayna, kayfa, kam, etc.",
    ),
    exclusion_conditions=(
        "Does not assert question intent (INTERROGATIVE ≠ question intent)",
        "Does not open silah attachment (would be relative pronoun)",
        "Does not carry proximity/distance marking (would be demonstrative)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="built_reference_not_meaning/BUILT_REFERENCE.INTERROGATIVE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(BUILT_REFERENCE.INTERROGATIVE) is "
                "built form, not meaning — INTERROGATIVE ≠ question intent"
            ),
        ),
        Residual(
            name="INFLECTION_GOVERNANCE_DEFERRED_TO_PR_F5/BUILT_REFERENCE.INTERROGATIVE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Interrogative governance detail (i'rab effects) not "
                "licensed here — deferred to PR-F5 (Inflection Formal "
                "Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/BUILT_REFERENCE.INTERROGATIVE",
)

#: CONDITIONAL formal definition.
CONDITIONAL_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="BUILT_REFERENCE.CONDITIONAL",
    domain=FormalShapeDomain.BUILT_REFERENCE,
    family=CONDITIONAL_FAMILY,
    canonical_name="adah shart",
    definition_text=(
        "A morphologically built form that opens a condition-consequence "
        "formal structure (shart-jawab al-shart) without asserting "
        "conditional truth or causal connection. Proved formally by "
        "fixed pattern and conditional structure requirement. "
        "Inflection/governance closure deferred to PR-F5/PR-F7."
    ),
    distinguishing_evidence=(
        "Opens condition-consequence formal structure — conditional "
        "tools (in, idha, man, ma, mata, ayna, etc.) — distinguishing "
        "from interrogatives which open inquiry rather than "
        "condition-consequence structure."
    ),
    boundary_conditions=(
        "Morphologically built (mabni) — fixed pattern",
        "Opens condition-consequence formal structure (shart + jawab)",
        "Inflection/governance detail deferred to PR-F5/PR-F7",
        "Closed set: in, idha, man, ma, mata, ayna, mahma, etc.",
    ),
    exclusion_conditions=(
        "Does not assert conditional truth (CONDITIONAL ≠ conditional truth)",
        "Does not open inquiry (would be interrogative)",
        "Does not open silah attachment (would be relative pronoun)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="built_reference_not_meaning/BUILT_REFERENCE.CONDITIONAL",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(BUILT_REFERENCE.CONDITIONAL) is "
                "built form, not meaning — CONDITIONAL ≠ conditional truth"
            ),
        ),
        Residual(
            name="INFLECTION_GOVERNANCE_DEFERRED_TO_PR_F5/BUILT_REFERENCE.CONDITIONAL",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Jazm governance on condition/consequence verbs not "
                "licensed here — deferred to PR-F5 (Inflection Formal "
                "Definitions)."
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/BUILT_REFERENCE.CONDITIONAL",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Full shart-jawab composition pattern not licensed here — "
                "deferred to PR-F7 (Composition Pattern Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/BUILT_REFERENCE.CONDITIONAL",
)


# ---------------------------------------------------------------------------
# build_built_reference_registry() — assemble BUILT_REFERENCE registry
# ---------------------------------------------------------------------------


def build_built_reference_registry(
    definitions: tuple[FormalShapeDefinition, ...] | None = None,
) -> FormalShapeRegistry:
    """Assemble the BUILT_REFERENCE domain registry (docs/34 §6).

    This is a **pure function**: it accepts values and returns a value.
    If no definitions are provided, uses all 5 canonical definitions.

    The registry is CLOSED when all 5 required families have at least
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
            PERSONAL_PRONOUN_DEFINITION,
            DEMONSTRATIVE_DEFINITION,
            RELATIVE_PRONOUN_DEFINITION,
            INTERROGATIVE_DEFINITION,
            CONDITIONAL_DEFINITION,
        )

    # Validate all definitions belong to BUILT_REFERENCE
    for defn in definitions:
        if defn.domain is not FormalShapeDomain.BUILT_REFERENCE:
            return FormalShapeRegistry(
                domain=FormalShapeDomain.BUILT_REFERENCE,
                families=BUILT_REFERENCE_FAMILIES,
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
                    domain=FormalShapeDomain.BUILT_REFERENCE,
                    families=BUILT_REFERENCE_FAMILIES,
                    definitions=definitions,
                    rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                    closure_state=FormalShapeClosureState.REFUSED,
                )

    # Compute closure state
    if not definitions:
        closure_state = FormalShapeClosureState.EMPTY
    else:
        required_family_ids = {f.family_id for f in BUILT_REFERENCE_FAMILIES}
        covered_family_ids = {d.family.family_id for d in definitions}
        if required_family_ids <= covered_family_ids:
            closure_state = FormalShapeClosureState.CLOSED
        else:
            closure_state = FormalShapeClosureState.PARTIAL

    return FormalShapeRegistry(
        domain=FormalShapeDomain.BUILT_REFERENCE,
        families=BUILT_REFERENCE_FAMILIES,
        definitions=definitions,
        rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
        closure_state=closure_state,
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "BUILT_REFERENCE_FAMILIES",
    "BuiltReferenceDefinitionState",
    "BuiltReferenceDefinitionVerdict",
    "CONDITIONAL_DEFINITION",
    "CONDITIONAL_FAMILY",
    "DEMONSTRATIVE_DEFINITION",
    "DEMONSTRATIVE_FAMILY",
    "INTERROGATIVE_DEFINITION",
    "INTERROGATIVE_FAMILY",
    "PERSONAL_PRONOUN_DEFINITION",
    "PERSONAL_PRONOUN_FAMILY",
    "RELATIVE_PRONOUN_DEFINITION",
    "RELATIVE_PRONOUN_FAMILY",
    "build_built_reference_registry",
    "define_built_reference_shape",
]
