"""Contract Slot Formal Definitions — PR-F6.

PR-F6 binding of ``docs/34_FORMAL_SHAPE_REGISTRY_LAW.md`` §9
(CONTRACT_SLOT).

This module introduces the CONTRACT_SLOT domain families and their
canonical formal definitions. Contract slot forms are formal
structural positions — they describe WHERE a word sits in the
governance structure, not WHAT it means or WHO it is.

Constitutional invariants (docs/34 §9):

* CONTRACT_SLOT ≠ SyntaxRoleFinal.
* CONTRACT_SLOT ≠ meaning.
* FORMAL_SUBJECT_SLOT ≠ real agent (fa'il haqiqi).
* FORMAL_TOPIC_SLOT ≠ proposition subject in meaning.
* FORMAL_PREDICATE_SLOT ≠ ifadah (proposition completion).
* FORMAL_OBJECT_SLOT ≠ real patient (maf'ul haqiqi).
* FORMAL_GENITIVE_SLOT ≠ ownership/possession meaning.
* FORMAL_QUALIFIER_SLOT ≠ attribute judgment.
* FORMAL_STATE_SLOT ≠ real state assertion.
* FORMAL_SPECIFICATION_SLOT ≠ semantic clarification.
* FormalShapeDefinition ≠ Meaning.
* FormalShapeDefinition ≠ SemanticEntry.
* FormalShapeDefinition ≠ WadʿiSignified.
* FormalShapeDefinition ≠ Dalālah.
* FormalShapeDefinition ≠ SyntaxRole.
* FormalShapeRegistry ≠ SemanticLexicon.
* Contract slot is formal position, not meaning.
* No rank promotion beyond FORMAL_SHAPE_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* All operations are pure: no I/O, no ledger, no network.
* No new FailureCode members; no new runtime dependencies.
* No positive 'meaning' language in definition_text.

Deferred residuals (binding):

* COMPOSITION_PATTERN_DEFERRED_TO_PR_F7 — how slots compose into
  sentence patterns is not licensed here.
* SEMANTIC_DALALAH_DEFERRED_TO_POST_FORMAL_CLOSURE — what the
  slot MEANS is not licensed here.
* IFADAH_DEFERRED_TO_PR_20 — proposition completion is not
  licensed here.
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
# ContractSlotDefinitionState — verdict outcome
# ---------------------------------------------------------------------------


class ContractSlotDefinitionState(StrEnum):
    """The outcome of a define_contract_slot_shape() operation."""

    DEFINED = "DEFINED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# ContractSlotDefinitionVerdict — the definition proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ContractSlotDefinitionVerdict:
    """The output of :func:`define_contract_slot_shape` (docs/34 §9).

    Proves that a contract slot formal shape definition satisfies all
    constitutional requirements. It does NOT carry meaning, ifadah,
    hukm, reality, syntactic role assignment, or any semantic content.
    """

    definition: FormalShapeDefinition | None
    verdict_state: ContractSlotDefinitionState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, ContractSlotDefinitionState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be ContractSlotDefinitionState, "
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
        if self.verdict_state is ContractSlotDefinitionState.DEFINED:
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
        elif self.verdict_state is ContractSlotDefinitionState.REFUSED:
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
# CONTRACT_SLOT Families (docs/34 §9)
# ---------------------------------------------------------------------------

#: FORMAL_SUBJECT_SLOT — formal subject position (fa'il / na'ib al-fa'il).
FORMAL_SUBJECT_SLOT_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family_id="FORMAL_SUBJECT_SLOT",
    description=(
        "Formal subject position — a structural slot proved by "
        "raf' governance from a verbal governor, without asserting "
        "real agency or real subjecthood"
    ),
)

#: FORMAL_TOPIC_SLOT — formal topic position (mubtada').
FORMAL_TOPIC_SLOT_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family_id="FORMAL_TOPIC_SLOT",
    description=(
        "Formal topic position — a structural slot proved by "
        "initial nominative standing (ibtida'), without asserting "
        "proposition subject in meaning"
    ),
)

#: FORMAL_PREDICATE_SLOT — formal predicate position (khabar).
FORMAL_PREDICATE_SLOT_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family_id="FORMAL_PREDICATE_SLOT",
    description=(
        "Formal predicate position — a structural slot proved by "
        "dependency on a topic or subject, without asserting "
        "proposition completion (ifadah)"
    ),
)

#: FORMAL_OBJECT_SLOT — formal object position (maf'ul bih).
FORMAL_OBJECT_SLOT_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family_id="FORMAL_OBJECT_SLOT",
    description=(
        "Formal object position — a structural slot proved by "
        "nasb governance from a transitive governor, without "
        "asserting real patienthood or real objecthood"
    ),
)

#: FORMAL_GENITIVE_SLOT — formal genitive position (mudaf ilayh).
FORMAL_GENITIVE_SLOT_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family_id="FORMAL_GENITIVE_SLOT",
    description=(
        "Formal genitive position — a structural slot proved by "
        "jarr governance from idafah or a preposition, without "
        "asserting ownership or possession meaning"
    ),
)

#: FORMAL_QUALIFIER_SLOT — formal qualifier position (sifah / na't).
FORMAL_QUALIFIER_SLOT_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family_id="FORMAL_QUALIFIER_SLOT",
    description=(
        "Formal qualifier position — a structural slot proved by "
        "tabi' (follower) agreement in case, definiteness, gender, "
        "and number, without asserting attribute judgment"
    ),
)

#: FORMAL_STATE_SLOT — formal state position (hal).
FORMAL_STATE_SLOT_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family_id="FORMAL_STATE_SLOT",
    description=(
        "Formal state position — a structural slot proved by "
        "indefinite nasb (accusative) with a definite referent "
        "(sahib al-hal), without asserting real state"
    ),
)

#: FORMAL_SPECIFICATION_SLOT — formal specification position (tamyiz).
FORMAL_SPECIFICATION_SLOT_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family_id="FORMAL_SPECIFICATION_SLOT",
    description=(
        "Formal specification position — a structural slot proved "
        "by indefinite nasb (accusative) resolving a preceding "
        "ambiguity in number/measure/kind, without asserting "
        "semantic clarification"
    ),
)

#: All CONTRACT_SLOT families.
CONTRACT_SLOT_FAMILIES: tuple[FormalShapeFamily, ...] = (
    FORMAL_SUBJECT_SLOT_FAMILY,
    FORMAL_TOPIC_SLOT_FAMILY,
    FORMAL_PREDICATE_SLOT_FAMILY,
    FORMAL_OBJECT_SLOT_FAMILY,
    FORMAL_GENITIVE_SLOT_FAMILY,
    FORMAL_QUALIFIER_SLOT_FAMILY,
    FORMAL_STATE_SLOT_FAMILY,
    FORMAL_SPECIFICATION_SLOT_FAMILY,
)


# ---------------------------------------------------------------------------
# define_contract_slot_shape() — the definition operation
# ---------------------------------------------------------------------------


def define_contract_slot_shape(
    shape_id: str,
    family: FormalShapeFamily,
    canonical_name: str,
    definition_text: str,
    distinguishing_evidence: str,
    boundary_conditions: tuple[str, ...],
    exclusion_conditions: tuple[str, ...],
    weight_constraint: str | None = None,
    path_constraint: str | None = None,
) -> ContractSlotDefinitionVerdict:
    """Prove a contract slot formal shape definition (docs/34 §9).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    Parameters
    ----------
    shape_id : str
        Globally unique identifier for this formal shape.
    family : FormalShapeFamily
        Must belong to the CONTRACT_SLOT domain.
    canonical_name : str
        The Arabic grammatical term (e.g., "fa'il", "maf'ul bih").
    definition_text : str
        Formal textual definition proving the shape.
    distinguishing_evidence : str
        What proves this shape vs. other contract slot families.
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
    ContractSlotDefinitionVerdict
        DEFINED with a FormalShapeDefinition on success; REFUSED with a
        named FailureCode on any violation.
    """
    # --- Input boundary: shape_id ---
    if not isinstance(shape_id, str) or not shape_id.strip():
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/shape_id_empty",
        )

    # --- Input boundary: family type and domain ---
    if not isinstance(family, FormalShapeFamily):
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/family_not_formal_shape_family",
        )
    if family.domain is not FormalShapeDomain.CONTRACT_SLOT:
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.DOMAIN_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/family_domain_not_contract_slot",
        )

    # --- Input boundary: canonical_name ---
    if not isinstance(canonical_name, str) or not canonical_name.strip():
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/canonical_name_empty",
        )

    # --- Input boundary: definition_text ---
    if not isinstance(definition_text, str) or not definition_text.strip():
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/definition_text_empty",
        )

    # --- Input boundary: distinguishing_evidence ---
    if not isinstance(distinguishing_evidence, str) or not distinguishing_evidence.strip():
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/distinguishing_evidence_empty",
        )

    # --- Input boundary: boundary_conditions ---
    if not isinstance(boundary_conditions, tuple):
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/boundary_conditions_not_tuple",
        )
    if not boundary_conditions:
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/boundary_conditions_empty",
        )
    for bc in boundary_conditions:
        if not isinstance(bc, str) or not bc.strip():
            return ContractSlotDefinitionVerdict(
                definition=None,
                verdict_state=ContractSlotDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_contract_slot_shape/refused/boundary_condition_invalid",
            )

    # --- Input boundary: exclusion_conditions ---
    if not isinstance(exclusion_conditions, tuple):
        return ContractSlotDefinitionVerdict(
            definition=None,
            verdict_state=ContractSlotDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_contract_slot_shape/refused/exclusion_conditions_not_tuple",
        )
    for ec in exclusion_conditions:
        if not isinstance(ec, str) or not ec.strip():
            return ContractSlotDefinitionVerdict(
                definition=None,
                verdict_state=ContractSlotDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_contract_slot_shape/refused/exclusion_condition_invalid",
            )

    # --- Rank bounding via lattice meet ---
    definition_rank = RankLattice.meet(
        Rank.CANDIDATE,
        FORMAL_SHAPE_RANK_CEILING,
    )

    # --- Residuals: open residual noting contract slot ≠ meaning ---
    open_residuals: tuple[Residual, ...] = (
        Residual(
            name=f"contract_slot_not_meaning/{shape_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"FormalShapeDefinition({shape_id}) is formal contract "
                f"slot position, not meaning — CONTRACT_SLOT ≠ "
                f"SyntaxRoleFinal, CONTRACT_SLOT ≠ meaning"
            ),
        ),
    )

    # --- Construct the FormalShapeDefinition ---
    definition = FormalShapeDefinition(
        shape_id=shape_id,
        domain=FormalShapeDomain.CONTRACT_SLOT,
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
        trace_ref=f"define_contract_slot_shape/defined/{shape_id}",
    )

    return ContractSlotDefinitionVerdict(
        definition=definition,
        verdict_state=ContractSlotDefinitionState.DEFINED,
        failure_code=None,
        verdict_rank=definition_rank,
        residuals=open_residuals,
        trace_ref=f"define_contract_slot_shape/defined/{shape_id}",
    )


# ---------------------------------------------------------------------------
# Canonical CONTRACT_SLOT definitions (docs/34 §9)
# ---------------------------------------------------------------------------

#: FORMAL_SUBJECT_SLOT formal definition.
FORMAL_SUBJECT_SLOT_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="CONTRACT_SLOT.FORMAL_SUBJECT_SLOT",
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family=FORMAL_SUBJECT_SLOT_FAMILY,
    canonical_name="fa'il / na'ib al-fa'il",
    definition_text=(
        "A formal structural position occupied by the word that "
        "receives raf' (nominative) governance from a verbal "
        "governor. Proved by: (1) raf' mark on the occupant, "
        "(2) presence of a verbal governor requiring a subject "
        "slot. This is a governance-position shape, not agency "
        "or real subjecthood."
    ),
    distinguishing_evidence=(
        "Raf' mark governed by a verbal element — distinguishing "
        "from formal topic (raf' by ibtida') and from formal "
        "predicate (dependent on topic/subject)."
    ),
    boundary_conditions=(
        "Occupant carries raf' mark (nominative/indicative)",
        "Raf' is governed by a verbal governor (fi'l or operator)",
        "Position is the primary nominative slot of the verbal clause",
    ),
    exclusion_conditions=(
        "FORMAL_SUBJECT_SLOT does not assert real agency (fa'il haqiqi)",
        "FORMAL_SUBJECT_SLOT does not assert the occupant performed an action",
        "FORMAL_SUBJECT_SLOT does not resolve governor identity to a lexical verb",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="contract_slot_not_meaning/CONTRACT_SLOT.FORMAL_SUBJECT_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(CONTRACT_SLOT.FORMAL_SUBJECT_SLOT) is "
                "formal contract slot position, not meaning — "
                "FORMAL_SUBJECT_SLOT ≠ real agent"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/CONTRACT_SLOT.FORMAL_SUBJECT_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How subject slot composes into sentence patterns not "
                "licensed here — deferred to PR-F7 (Composition Pattern "
                "Formal Definitions)."
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/CONTRACT_SLOT.FORMAL_SUBJECT_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What the subject slot occupant does (agency, experience, "
                "etc.) is not licensed here — deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/CONTRACT_SLOT.FORMAL_SUBJECT_SLOT",
)

#: FORMAL_TOPIC_SLOT formal definition.
FORMAL_TOPIC_SLOT_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="CONTRACT_SLOT.FORMAL_TOPIC_SLOT",
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family=FORMAL_TOPIC_SLOT_FAMILY,
    canonical_name="mubtada'",
    definition_text=(
        "A formal structural position occupied by the word that "
        "carries raf' (nominative) by virtue of initiality "
        "(ibtida') — standing at the beginning of a nominal "
        "clause without a preceding verbal governor. Proved by: "
        "(1) raf' mark on the occupant, (2) absence of a verbal "
        "governor, (3) clause-initial position. This is a "
        "governance-position shape, not proposition subject."
    ),
    distinguishing_evidence=(
        "Raf' by ibtida' (no verbal governor) in clause-initial "
        "position — distinguishing from formal subject (raf' by "
        "verbal governor) and from formal predicate (dependent "
        "on topic)."
    ),
    boundary_conditions=(
        "Occupant carries raf' mark (nominative)",
        "No verbal governor precedes (raf' is by ibtida')",
        "Occupant stands in clause-initial position",
    ),
    exclusion_conditions=(
        "FORMAL_TOPIC_SLOT does not assert proposition subject in meaning",
        "FORMAL_TOPIC_SLOT does not assert that the occupant is 'what the "
        "sentence is about' semantically",
        "FORMAL_TOPIC_SLOT does not resolve to a referent",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="contract_slot_not_meaning/CONTRACT_SLOT.FORMAL_TOPIC_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(CONTRACT_SLOT.FORMAL_TOPIC_SLOT) is "
                "formal contract slot position, not meaning — "
                "FORMAL_TOPIC_SLOT ≠ proposition subject in meaning"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/CONTRACT_SLOT.FORMAL_TOPIC_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How topic slot composes into sentence patterns not "
                "licensed here — deferred to PR-F7 (Composition Pattern "
                "Formal Definitions)."
            ),
        ),
        Residual(
            name="IFADAH_DEFERRED_TO_PR_20/CONTRACT_SLOT.FORMAL_TOPIC_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Whether topic + predicate produce ifadah (proposition "
                "completion) is not licensed here — deferred to PR-20."
            ),
        ),
    ),
    trace_ref="canonical/CONTRACT_SLOT.FORMAL_TOPIC_SLOT",
)

#: FORMAL_PREDICATE_SLOT formal definition.
FORMAL_PREDICATE_SLOT_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="CONTRACT_SLOT.FORMAL_PREDICATE_SLOT",
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family=FORMAL_PREDICATE_SLOT_FAMILY,
    canonical_name="khabar",
    definition_text=(
        "A formal structural position occupied by the word (or "
        "phrase) that completes the formal clause dependency "
        "started by a topic (mubtada'). Proved by: (1) structural "
        "dependency on a preceding topic, (2) raf' agreement with "
        "the topic (in nominal clauses) or verbal form completing "
        "the clause. This is a governance-position shape, not "
        "proposition completion or assertion."
    ),
    distinguishing_evidence=(
        "Structural dependency on a topic (mubtada') or subject — "
        "distinguishing from formal subject (governed by verb), "
        "formal topic (independent/initial), and formal object "
        "(governed in nasb)."
    ),
    boundary_conditions=(
        "Occupant is structurally dependent on a topic/subject",
        "Completes the formal clause dependency (paired with musnad ilayh)",
        "Carries appropriate case for its clause type (raf' in nominal)",
    ),
    exclusion_conditions=(
        "FORMAL_PREDICATE_SLOT does not assert proposition completion (ifadah)",
        "FORMAL_PREDICATE_SLOT does not assert truth value",
        "FORMAL_PREDICATE_SLOT does not assert that 'something is said about something'",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="contract_slot_not_meaning/CONTRACT_SLOT.FORMAL_PREDICATE_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(CONTRACT_SLOT.FORMAL_PREDICATE_SLOT) is "
                "formal contract slot position, not meaning — "
                "FORMAL_PREDICATE_SLOT ≠ ifadah"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/CONTRACT_SLOT.FORMAL_PREDICATE_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How predicate slot composes into sentence patterns not "
                "licensed here — deferred to PR-F7 (Composition Pattern "
                "Formal Definitions)."
            ),
        ),
        Residual(
            name="IFADAH_DEFERRED_TO_PR_20/CONTRACT_SLOT.FORMAL_PREDICATE_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Whether predicate completes a proposition (ifadah) is "
                "not licensed here — deferred to PR-20."
            ),
        ),
    ),
    trace_ref="canonical/CONTRACT_SLOT.FORMAL_PREDICATE_SLOT",
)

#: FORMAL_OBJECT_SLOT formal definition.
FORMAL_OBJECT_SLOT_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="CONTRACT_SLOT.FORMAL_OBJECT_SLOT",
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family=FORMAL_OBJECT_SLOT_FAMILY,
    canonical_name="maf'ul bih",
    definition_text=(
        "A formal structural position occupied by the word that "
        "receives nasb (accusative) governance from a transitive "
        "verbal governor. Proved by: (1) nasb mark on the "
        "occupant, (2) presence of a transitive verbal governor "
        "requiring an object slot. This is a governance-position "
        "shape, not real patienthood or real objecthood."
    ),
    distinguishing_evidence=(
        "Nasb mark governed by a transitive verb — distinguishing "
        "from formal state (nasb with indefinite + definite "
        "referent), formal specification (nasb resolving "
        "ambiguity), and adverbials (nasb with different evidence)."
    ),
    boundary_conditions=(
        "Occupant carries nasb mark (accusative)",
        "Nasb is governed by a transitive verbal governor",
        "Position is the direct complement slot of the verb",
    ),
    exclusion_conditions=(
        "FORMAL_OBJECT_SLOT does not assert real patienthood",
        "FORMAL_OBJECT_SLOT does not assert the occupant received an action",
        "FORMAL_OBJECT_SLOT does not resolve governor identity to a lexical verb",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="contract_slot_not_meaning/CONTRACT_SLOT.FORMAL_OBJECT_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(CONTRACT_SLOT.FORMAL_OBJECT_SLOT) is "
                "formal contract slot position, not meaning — "
                "FORMAL_OBJECT_SLOT ≠ real patient"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/CONTRACT_SLOT.FORMAL_OBJECT_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How object slot composes into sentence patterns not "
                "licensed here — deferred to PR-F7 (Composition Pattern "
                "Formal Definitions)."
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/CONTRACT_SLOT.FORMAL_OBJECT_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What the object slot occupant undergoes (patienthood, "
                "etc.) is not licensed here — deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/CONTRACT_SLOT.FORMAL_OBJECT_SLOT",
)

#: FORMAL_GENITIVE_SLOT formal definition.
FORMAL_GENITIVE_SLOT_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="CONTRACT_SLOT.FORMAL_GENITIVE_SLOT",
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family=FORMAL_GENITIVE_SLOT_FAMILY,
    canonical_name="mudaf ilayh / majrur",
    definition_text=(
        "A formal structural position occupied by the word that "
        "receives jarr (genitive) governance from an idafah "
        "construct (mudaf) or a preposition (harf jarr). Proved "
        "by: (1) jarr mark on the occupant, (2) presence of a "
        "governing mudaf or preposition. This is a "
        "governance-position shape, not ownership or possession."
    ),
    distinguishing_evidence=(
        "Jarr mark governed by mudaf or preposition — "
        "distinguishing from other jarr contexts (tawabi' in "
        "jarr follow their head, not independent governance)."
    ),
    boundary_conditions=(
        "Occupant carries jarr mark (genitive)",
        "Jarr is governed by an idafah construct or a preposition",
        "Position is the complement slot of the governance source",
    ),
    exclusion_conditions=(
        "FORMAL_GENITIVE_SLOT does not assert ownership meaning",
        "FORMAL_GENITIVE_SLOT does not assert possession",
        "FORMAL_GENITIVE_SLOT does not resolve the idafah relation semantically",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="contract_slot_not_meaning/CONTRACT_SLOT.FORMAL_GENITIVE_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(CONTRACT_SLOT.FORMAL_GENITIVE_SLOT) is "
                "formal contract slot position, not meaning — "
                "FORMAL_GENITIVE_SLOT ≠ ownership/possession meaning"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/CONTRACT_SLOT.FORMAL_GENITIVE_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How genitive slot composes into idafah patterns not "
                "licensed here — deferred to PR-F7 (Composition Pattern "
                "Formal Definitions)."
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/CONTRACT_SLOT.FORMAL_GENITIVE_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What the idafah relation expresses (ownership, "
                "specification, etc.) is not licensed here — deferred to "
                "post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/CONTRACT_SLOT.FORMAL_GENITIVE_SLOT",
)

#: FORMAL_QUALIFIER_SLOT formal definition.
FORMAL_QUALIFIER_SLOT_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="CONTRACT_SLOT.FORMAL_QUALIFIER_SLOT",
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family=FORMAL_QUALIFIER_SLOT_FAMILY,
    canonical_name="sifah / na't",
    definition_text=(
        "A formal structural position occupied by a word that "
        "follows (tabi') its head (mawsuf) in case, definiteness, "
        "gender, and number. Proved by: (1) case agreement with "
        "the head, (2) definiteness agreement, (3) gender/number "
        "agreement, (4) immediate post-head position. This is a "
        "structural agreement shape, not attribute judgment."
    ),
    distinguishing_evidence=(
        "Four-way agreement (case, definiteness, gender, number) "
        "with a preceding head noun — distinguishing from other "
        "tawabi' (conjunction, apposition, emphasis) which have "
        "different agreement patterns or connectors."
    ),
    boundary_conditions=(
        "Occupant agrees in case with the preceding head noun",
        "Occupant agrees in definiteness with the head noun",
        "Occupant agrees in gender and number with the head noun",
    ),
    exclusion_conditions=(
        "FORMAL_QUALIFIER_SLOT does not assert attribute judgment",
        "FORMAL_QUALIFIER_SLOT does not assert quality attribution",
        "FORMAL_QUALIFIER_SLOT does not evaluate the described property",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="contract_slot_not_meaning/CONTRACT_SLOT.FORMAL_QUALIFIER_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(CONTRACT_SLOT.FORMAL_QUALIFIER_SLOT) is "
                "formal contract slot position, not meaning — "
                "FORMAL_QUALIFIER_SLOT ≠ attribute judgment"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/CONTRACT_SLOT.FORMAL_QUALIFIER_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How qualifier slot composes into na't patterns not "
                "licensed here — deferred to PR-F7 (Composition Pattern "
                "Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/CONTRACT_SLOT.FORMAL_QUALIFIER_SLOT",
)

#: FORMAL_STATE_SLOT formal definition.
FORMAL_STATE_SLOT_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="CONTRACT_SLOT.FORMAL_STATE_SLOT",
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family=FORMAL_STATE_SLOT_FAMILY,
    canonical_name="hal",
    definition_text=(
        "A formal structural position occupied by a word in "
        "indefinite nasb (accusative) that structurally relates "
        "to a definite noun (sahib al-hal) in the clause. Proved "
        "by: (1) nasb mark on the occupant, (2) indefiniteness "
        "of the occupant, (3) presence of a definite referent "
        "(sahib al-hal). This is a governance-position shape, "
        "not real state assertion."
    ),
    distinguishing_evidence=(
        "Indefinite nasb with a definite referent (sahib al-hal) — "
        "distinguishing from formal object (nasb by transitive "
        "verb without indefiniteness/definiteness constraint) and "
        "formal specification (nasb resolving quantity/kind "
        "ambiguity)."
    ),
    boundary_conditions=(
        "Occupant carries nasb mark (accusative)",
        "Occupant is indefinite (nakirah)",
        "A definite referent (sahib al-hal) is present in the clause",
    ),
    exclusion_conditions=(
        "FORMAL_STATE_SLOT does not assert real state of the referent",
        "FORMAL_STATE_SLOT does not assert temporal or modal condition",
        "FORMAL_STATE_SLOT does not evaluate the described state",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="contract_slot_not_meaning/CONTRACT_SLOT.FORMAL_STATE_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(CONTRACT_SLOT.FORMAL_STATE_SLOT) is "
                "formal contract slot position, not meaning — "
                "FORMAL_STATE_SLOT ≠ real state"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/CONTRACT_SLOT.FORMAL_STATE_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How state slot composes into sentence patterns not "
                "licensed here — deferred to PR-F7 (Composition Pattern "
                "Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/CONTRACT_SLOT.FORMAL_STATE_SLOT",
)

#: FORMAL_SPECIFICATION_SLOT formal definition.
FORMAL_SPECIFICATION_SLOT_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="CONTRACT_SLOT.FORMAL_SPECIFICATION_SLOT",
    domain=FormalShapeDomain.CONTRACT_SLOT,
    family=FORMAL_SPECIFICATION_SLOT_FAMILY,
    canonical_name="tamyiz",
    definition_text=(
        "A formal structural position occupied by a word in "
        "indefinite nasb (accusative) that formally resolves a "
        "preceding structural ambiguity in number, measure, or "
        "kind. Proved by: (1) nasb mark on the occupant, "
        "(2) indefiniteness, (3) preceding element with formal "
        "ambiguity (number/measure/kind). This is a "
        "governance-position shape, not external clarification."
    ),
    distinguishing_evidence=(
        "Indefinite nasb resolving a preceding structural "
        "ambiguity — distinguishing from formal state (nasb with "
        "definite referent) and formal object (nasb by transitive "
        "governance without ambiguity resolution)."
    ),
    boundary_conditions=(
        "Occupant carries nasb mark (accusative)",
        "Occupant is indefinite (nakirah)",
        "Preceding element has formal ambiguity (number/measure/kind)",
    ),
    exclusion_conditions=(
        "FORMAL_SPECIFICATION_SLOT does not assert semantic clarification",
        "FORMAL_SPECIFICATION_SLOT does not resolve what the number/measure means",
        "FORMAL_SPECIFICATION_SLOT does not evaluate the specification content",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="contract_slot_not_meaning/CONTRACT_SLOT.FORMAL_SPECIFICATION_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(CONTRACT_SLOT.FORMAL_SPECIFICATION_SLOT) "
                "is formal contract slot position, not meaning — "
                "FORMAL_SPECIFICATION_SLOT ≠ semantic clarification"
            ),
        ),
        Residual(
            name="COMPOSITION_PATTERN_DEFERRED_TO_PR_F7/CONTRACT_SLOT.FORMAL_SPECIFICATION_SLOT",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "How specification slot composes into sentence patterns "
                "not licensed here — deferred to PR-F7 (Composition "
                "Pattern Formal Definitions)."
            ),
        ),
    ),
    trace_ref="canonical/CONTRACT_SLOT.FORMAL_SPECIFICATION_SLOT",
)


# ---------------------------------------------------------------------------
# build_contract_slot_registry() — assemble CONTRACT_SLOT registry
# ---------------------------------------------------------------------------


def build_contract_slot_registry(
    definitions: tuple[FormalShapeDefinition, ...] | None = None,
) -> FormalShapeRegistry:
    """Assemble the CONTRACT_SLOT domain registry (docs/34 §9).

    This is a **pure function**: it accepts values and returns a value.
    If no definitions are provided, uses all 8 canonical definitions.

    The registry is CLOSED when all 8 required families have at least
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
            FORMAL_SUBJECT_SLOT_DEFINITION,
            FORMAL_TOPIC_SLOT_DEFINITION,
            FORMAL_PREDICATE_SLOT_DEFINITION,
            FORMAL_OBJECT_SLOT_DEFINITION,
            FORMAL_GENITIVE_SLOT_DEFINITION,
            FORMAL_QUALIFIER_SLOT_DEFINITION,
            FORMAL_STATE_SLOT_DEFINITION,
            FORMAL_SPECIFICATION_SLOT_DEFINITION,
        )

    # Validate all definitions belong to CONTRACT_SLOT
    for defn in definitions:
        if defn.domain is not FormalShapeDomain.CONTRACT_SLOT:
            return FormalShapeRegistry(
                domain=FormalShapeDomain.CONTRACT_SLOT,
                families=CONTRACT_SLOT_FAMILIES,
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
                    domain=FormalShapeDomain.CONTRACT_SLOT,
                    families=CONTRACT_SLOT_FAMILIES,
                    definitions=definitions,
                    rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                    closure_state=FormalShapeClosureState.REFUSED,
                )

    # Compute closure state
    if not definitions:
        closure_state = FormalShapeClosureState.EMPTY
    else:
        required_family_ids = {f.family_id for f in CONTRACT_SLOT_FAMILIES}
        covered_family_ids = {d.family.family_id for d in definitions}
        if required_family_ids <= covered_family_ids:
            closure_state = FormalShapeClosureState.CLOSED
        else:
            closure_state = FormalShapeClosureState.PARTIAL

    return FormalShapeRegistry(
        domain=FormalShapeDomain.CONTRACT_SLOT,
        families=CONTRACT_SLOT_FAMILIES,
        definitions=definitions,
        rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
        closure_state=closure_state,
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "CONTRACT_SLOT_FAMILIES",
    "ContractSlotDefinitionState",
    "ContractSlotDefinitionVerdict",
    "FORMAL_GENITIVE_SLOT_DEFINITION",
    "FORMAL_GENITIVE_SLOT_FAMILY",
    "FORMAL_OBJECT_SLOT_DEFINITION",
    "FORMAL_OBJECT_SLOT_FAMILY",
    "FORMAL_PREDICATE_SLOT_DEFINITION",
    "FORMAL_PREDICATE_SLOT_FAMILY",
    "FORMAL_QUALIFIER_SLOT_DEFINITION",
    "FORMAL_QUALIFIER_SLOT_FAMILY",
    "FORMAL_SPECIFICATION_SLOT_DEFINITION",
    "FORMAL_SPECIFICATION_SLOT_FAMILY",
    "FORMAL_STATE_SLOT_DEFINITION",
    "FORMAL_STATE_SLOT_FAMILY",
    "FORMAL_SUBJECT_SLOT_DEFINITION",
    "FORMAL_SUBJECT_SLOT_FAMILY",
    "FORMAL_TOPIC_SLOT_DEFINITION",
    "FORMAL_TOPIC_SLOT_FAMILY",
    "build_contract_slot_registry",
    "define_contract_slot_shape",
]
