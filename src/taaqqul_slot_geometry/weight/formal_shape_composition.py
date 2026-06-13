"""Composition Pattern Formal Definitions — PR-F7.

PR-F7 binding of ``docs/34_FORMAL_SHAPE_REGISTRY_LAW.md`` §10
(COMPOSITION_PATTERN).

This module introduces the COMPOSITION_PATTERN domain families and their
canonical formal definitions. Composition patterns are formal structural
arrangements — they describe HOW slots compose into sentence or phrase
patterns, not WHAT those patterns mean or assert.

Constitutional invariants (docs/34 §10):

* COMPOSITION_PATTERN ≠ Meaning.
* COMPOSITION_PATTERN ≠ Proposition.
* NOMINAL_SENTENCE_PATTERN ≠ proposition.
* VERBAL_SENTENCE_PATTERN ≠ event assertion.
* IDAFA_PATTERN ≠ ownership.
* SIFA_MAWSUF_PATTERN ≠ attribute judgment.
* ATIF_PATTERN ≠ semantic equality / coordination in meaning.
* BADAL_PATTERN ≠ semantic substitution.
* FormalShapeDefinition ≠ Meaning.
* FormalShapeDefinition ≠ SemanticEntry.
* FormalShapeDefinition ≠ WadʿiSignified.
* FormalShapeDefinition ≠ Dalālah.
* FormalShapeDefinition ≠ SyntaxRole.
* FormalShapeRegistry ≠ SemanticLexicon.
* Composition pattern is formal structure, not meaning.
* No rank promotion beyond FORMAL_SHAPE_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* All operations are pure: no I/O, no ledger, no network.
* No new FailureCode members; no new runtime dependencies.
* No positive 'meaning' language in definition_text.

Deferred residuals (binding):

* IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE — whether composition
  produces ifadah (proposition completion) is not licensed here.
  No ifādah before mufrad dalālah closure (PR-F7.1 correction).
* SEMANTIC_DALALAH_DEFERRED_TO_POST_FORMAL_CLOSURE — what the
  composition MEANS is not licensed here.
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
# CompositionPatternDefinitionState — verdict outcome
# ---------------------------------------------------------------------------


class CompositionPatternDefinitionState(StrEnum):
    """The outcome of a define_composition_pattern_shape() operation."""

    DEFINED = "DEFINED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# CompositionPatternDefinitionVerdict — the definition proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CompositionPatternDefinitionVerdict:
    """The output of :func:`define_composition_pattern_shape` (docs/34 §10).

    Proves that a composition pattern formal shape definition satisfies all
    constitutional requirements. It does NOT carry meaning, ifadah,
    hukm, reality, proposition content, or any semantic content.
    """

    definition: FormalShapeDefinition | None
    verdict_state: CompositionPatternDefinitionState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, CompositionPatternDefinitionState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be CompositionPatternDefinitionState, "
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
        if self.verdict_state is CompositionPatternDefinitionState.DEFINED:
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
        elif self.verdict_state is CompositionPatternDefinitionState.REFUSED:
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
# COMPOSITION_PATTERN Families (docs/34 §10)
# ---------------------------------------------------------------------------

#: NOMINAL_SENTENCE — formal nominal sentence pattern (jumlah ismiyyah).
NOMINAL_SENTENCE_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family_id="NOMINAL_SENTENCE",
    description=(
        "Formal nominal sentence pattern — a structural arrangement "
        "of topic (mubtada') + predicate (khabar) slots, without "
        "asserting proposition or truth"
    ),
)

#: VERBAL_SENTENCE — formal verbal sentence pattern (jumlah fi'liyyah).
VERBAL_SENTENCE_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family_id="VERBAL_SENTENCE",
    description=(
        "Formal verbal sentence pattern — a structural arrangement "
        "of verb (fi'l) + subject (fa'il) slots, without asserting "
        "event occurrence or action"
    ),
)

#: IDAFA — formal annexation pattern (idafah).
IDAFA_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family_id="IDAFA",
    description=(
        "Formal annexation pattern — a structural arrangement of "
        "mudaf + mudaf ilayh slots producing genitive governance, "
        "without asserting ownership or possession"
    ),
)

#: SIFA_MAWSUF — formal qualification pattern (sifah + mawsuf).
SIFA_MAWSUF_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family_id="SIFA_MAWSUF",
    description=(
        "Formal qualification pattern — a structural arrangement of "
        "head noun (mawsuf) + qualifier (sifah) with four-way "
        "agreement, without asserting attribute judgment"
    ),
)

#: ATIF — formal coordination pattern ('atf).
ATIF_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family_id="ATIF",
    description=(
        "Formal coordination pattern — a structural arrangement of "
        "conjunct + conjunction + conjunct with case agreement, "
        "without asserting semantic coordination or equality"
    ),
)

#: BADAL — formal apposition pattern (badal).
BADAL_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family_id="BADAL",
    description=(
        "Formal apposition pattern — a structural arrangement of "
        "head (mubdal minhu) + appositive (badal) with case "
        "agreement, without asserting semantic substitution"
    ),
)

#: All COMPOSITION_PATTERN families.
COMPOSITION_PATTERN_FAMILIES: tuple[FormalShapeFamily, ...] = (
    NOMINAL_SENTENCE_FAMILY,
    VERBAL_SENTENCE_FAMILY,
    IDAFA_FAMILY,
    SIFA_MAWSUF_FAMILY,
    ATIF_FAMILY,
    BADAL_FAMILY,
)


# ---------------------------------------------------------------------------
# define_composition_pattern_shape() — the definition operation
# ---------------------------------------------------------------------------


def define_composition_pattern_shape(
    shape_id: str,
    family: FormalShapeFamily,
    canonical_name: str,
    definition_text: str,
    distinguishing_evidence: str,
    boundary_conditions: tuple[str, ...],
    exclusion_conditions: tuple[str, ...],
    weight_constraint: str | None = None,
    path_constraint: str | None = None,
) -> CompositionPatternDefinitionVerdict:
    """Prove a composition pattern formal shape definition (docs/34 §10).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    Parameters
    ----------
    shape_id : str
        Globally unique identifier for this formal shape.
    family : FormalShapeFamily
        Must belong to the COMPOSITION_PATTERN domain.
    canonical_name : str
        The Arabic grammatical term (e.g., "jumlah ismiyyah").
    definition_text : str
        Formal textual definition proving the shape.
    distinguishing_evidence : str
        What proves this shape vs. other composition pattern families.
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
    CompositionPatternDefinitionVerdict
        DEFINED with a FormalShapeDefinition on success; REFUSED with a
        named FailureCode on any violation.
    """
    # --- Input boundary: shape_id ---
    if not isinstance(shape_id, str) or not shape_id.strip():
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/shape_id_empty",
        )

    # --- Input boundary: family type and domain ---
    if not isinstance(family, FormalShapeFamily):
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/family_not_formal_shape_family",
        )
    if family.domain is not FormalShapeDomain.COMPOSITION_PATTERN:
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.DOMAIN_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/family_domain_not_composition",
        )

    # --- Input boundary: canonical_name ---
    if not isinstance(canonical_name, str) or not canonical_name.strip():
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/canonical_name_empty",
        )

    # --- Input boundary: definition_text ---
    if not isinstance(definition_text, str) or not definition_text.strip():
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/definition_text_empty",
        )

    # --- Input boundary: distinguishing_evidence ---
    if not isinstance(distinguishing_evidence, str) or not distinguishing_evidence.strip():
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/distinguishing_evidence_empty",
        )

    # --- Input boundary: boundary_conditions ---
    if not isinstance(boundary_conditions, tuple):
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/boundary_conditions_not_tuple",
        )
    if not boundary_conditions:
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/boundary_conditions_empty",
        )
    for bc in boundary_conditions:
        if not isinstance(bc, str) or not bc.strip():
            return CompositionPatternDefinitionVerdict(
                definition=None,
                verdict_state=CompositionPatternDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_composition_pattern_shape/refused/boundary_condition_invalid",
            )

    # --- Input boundary: exclusion_conditions ---
    if not isinstance(exclusion_conditions, tuple):
        return CompositionPatternDefinitionVerdict(
            definition=None,
            verdict_state=CompositionPatternDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_composition_pattern_shape/refused/exclusion_conditions_not_tuple",
        )
    for ec in exclusion_conditions:
        if not isinstance(ec, str) or not ec.strip():
            return CompositionPatternDefinitionVerdict(
                definition=None,
                verdict_state=CompositionPatternDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_composition_pattern_shape/refused/exclusion_condition_invalid",
            )

    # --- Rank bounding via lattice meet ---
    definition_rank = RankLattice.meet(
        Rank.CANDIDATE,
        FORMAL_SHAPE_RANK_CEILING,
    )

    # --- Residuals: open residual noting composition pattern ≠ meaning ---
    open_residuals: tuple[Residual, ...] = (
        Residual(
            name=f"composition_pattern_not_meaning/{shape_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"FormalShapeDefinition({shape_id}) is formal composition "
                f"pattern, not meaning — COMPOSITION_PATTERN ≠ "
                f"proposition, COMPOSITION_PATTERN ≠ event"
            ),
        ),
    )

    # --- Construct the FormalShapeDefinition ---
    definition = FormalShapeDefinition(
        shape_id=shape_id,
        domain=FormalShapeDomain.COMPOSITION_PATTERN,
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
        trace_ref=f"define_composition_pattern_shape/defined/{shape_id}",
    )

    return CompositionPatternDefinitionVerdict(
        definition=definition,
        verdict_state=CompositionPatternDefinitionState.DEFINED,
        failure_code=None,
        verdict_rank=definition_rank,
        residuals=open_residuals,
        trace_ref=f"define_composition_pattern_shape/defined/{shape_id}",
    )


# ---------------------------------------------------------------------------
# Canonical COMPOSITION_PATTERN definitions (docs/34 §10)
# ---------------------------------------------------------------------------

#: NOMINAL_SENTENCE formal definition.
NOMINAL_SENTENCE_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="COMPOSITION_PATTERN.NOMINAL_SENTENCE",
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family=NOMINAL_SENTENCE_FAMILY,
    canonical_name="jumlah ismiyyah",
    definition_text=(
        "A formal composition pattern in which a topic slot "
        "(mubtada') occupies the initial position and a predicate "
        "slot (khabar) completes the structural dependency. Proved "
        "by: (1) topic slot in clause-initial position with raf' "
        "by ibtida', (2) predicate slot structurally dependent on "
        "the topic. This is a structural arrangement of formal "
        "slots, not a proposition or truth-bearing assertion."
    ),
    distinguishing_evidence=(
        "Topic-initial structure with raf' by ibtida' (no preceding "
        "verbal governor) — distinguishing from verbal sentence "
        "(verb-initial) and from subordinate clause patterns."
    ),
    boundary_conditions=(
        "Topic slot (mubtada') present in initial position",
        "Predicate slot (khabar) present and structurally dependent on topic",
        "No verbal governor precedes the topic in clause scope",
    ),
    exclusion_conditions=(
        "NOMINAL_SENTENCE does not assert proposition (ifadah)",
        "NOMINAL_SENTENCE does not assert truth value",
        "NOMINAL_SENTENCE does not assert that something is predicated of something",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="composition_pattern_not_meaning/COMPOSITION_PATTERN.NOMINAL_SENTENCE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(COMPOSITION_PATTERN.NOMINAL_SENTENCE) is "
                "formal composition pattern, not meaning — "
                "NOMINAL_SENTENCE ≠ proposition"
            ),
        ),
        Residual(
            name="IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE/COMPOSITION_PATTERN.NOMINAL_SENTENCE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Whether nominal sentence composition produces ifadah "
                "(proposition completion) is not licensed here — "
                "deferred until mufrad dalalah closure (PR-F7.1 correction)."
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/COMPOSITION_PATTERN.NOMINAL_SENTENCE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What the nominal sentence asserts or communicates is "
                "not licensed here — deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/COMPOSITION_PATTERN.NOMINAL_SENTENCE",
)

#: VERBAL_SENTENCE formal definition.
VERBAL_SENTENCE_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="COMPOSITION_PATTERN.VERBAL_SENTENCE",
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family=VERBAL_SENTENCE_FAMILY,
    canonical_name="jumlah fi'liyyah",
    definition_text=(
        "A formal composition pattern in which a verbal governor "
        "(fi'l) occupies the initial position and a subject slot "
        "(fa'il) receives raf' governance from it. Proved by: "
        "(1) verbal element in clause-initial position, (2) subject "
        "slot carrying raf' governed by the verb. This is a "
        "structural arrangement of formal slots, not an event "
        "occurrence or action assertion."
    ),
    distinguishing_evidence=(
        "Verb-initial structure with subject governed in raf' by "
        "the verb — distinguishing from nominal sentence "
        "(topic-initial with raf' by ibtida') and from embedded "
        "clausal complements."
    ),
    boundary_conditions=(
        "Verbal governor (fi'l) present in initial position",
        "Subject slot (fa'il) present and carrying raf' from the verb",
        "Verb precedes the subject in clause scope",
    ),
    exclusion_conditions=(
        "VERBAL_SENTENCE does not assert event occurrence",
        "VERBAL_SENTENCE does not assert action performance",
        "VERBAL_SENTENCE does not assert temporal anchoring of events",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="composition_pattern_not_meaning/COMPOSITION_PATTERN.VERBAL_SENTENCE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(COMPOSITION_PATTERN.VERBAL_SENTENCE) is "
                "formal composition pattern, not meaning — "
                "VERBAL_SENTENCE ≠ event assertion"
            ),
        ),
        Residual(
            name="IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE/COMPOSITION_PATTERN.VERBAL_SENTENCE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "Whether verbal sentence composition produces ifadah "
                "(proposition completion) is not licensed here — "
                "deferred until mufrad dalalah closure (PR-F7.1 correction)."
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/COMPOSITION_PATTERN.VERBAL_SENTENCE",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What event or action the verbal sentence describes is "
                "not licensed here — deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/COMPOSITION_PATTERN.VERBAL_SENTENCE",
)

#: IDAFA formal definition.
IDAFA_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="COMPOSITION_PATTERN.IDAFA",
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family=IDAFA_FAMILY,
    canonical_name="idafah",
    definition_text=(
        "A formal composition pattern in which a head noun (mudaf) "
        "governs a complement (mudaf ilayh) in the genitive case "
        "(jarr). Proved by: (1) mudaf loses its tanwin and direct "
        "definiteness marker, (2) mudaf ilayh carries jarr governed "
        "by the annexation. This is a structural governance "
        "arrangement, not an assertion of possession or ownership."
    ),
    distinguishing_evidence=(
        "Genitive governance by annexation (mudaf governs mudaf "
        "ilayh in jarr without a preposition) — distinguishing from "
        "prepositional jarr (governed by harf jarr) and from "
        "qualifier agreement (tabi' follows head)."
    ),
    boundary_conditions=(
        "Head noun (mudaf) present and loses tanwin/direct al-",
        "Complement (mudaf ilayh) present and carries jarr mark",
        "Jarr is by annexation governance, not by preposition",
    ),
    exclusion_conditions=(
        "IDAFA does not assert ownership or possession",
        "IDAFA does not assert the relation type between mudaf and mudaf ilayh",
        "IDAFA does not resolve which of the 20+ idafah types applies",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="composition_pattern_not_meaning/COMPOSITION_PATTERN.IDAFA",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(COMPOSITION_PATTERN.IDAFA) is "
                "formal composition pattern, not meaning — "
                "IDAFA ≠ ownership"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/COMPOSITION_PATTERN.IDAFA",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What the idafah relation expresses (ownership, "
                "specification, partitive, etc.) is not licensed here — "
                "deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/COMPOSITION_PATTERN.IDAFA",
)

#: SIFA_MAWSUF formal definition.
SIFA_MAWSUF_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="COMPOSITION_PATTERN.SIFA_MAWSUF",
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family=SIFA_MAWSUF_FAMILY,
    canonical_name="sifah wa-mawsuf",
    definition_text=(
        "A formal composition pattern in which a qualifier (sifah) "
        "follows its head noun (mawsuf) with four-way agreement in "
        "case, definiteness, gender, and number. Proved by: "
        "(1) qualifier in immediate post-head position, (2) case "
        "agreement, (3) definiteness agreement, (4) gender/number "
        "agreement. This is a structural agreement arrangement, "
        "not an attribute judgment or quality assertion."
    ),
    distinguishing_evidence=(
        "Four-way agreement (case, definiteness, gender, number) "
        "with a preceding head noun in post-head position — "
        "distinguishing from coordination (connected by conjunction), "
        "apposition (same referent, no agreement requirement beyond "
        "case), and emphasis (identical repetition)."
    ),
    boundary_conditions=(
        "Qualifier (sifah) follows head noun (mawsuf) directly",
        "Case agreement between qualifier and head",
        "Definiteness agreement between qualifier and head",
        "Gender and number agreement between qualifier and head",
    ),
    exclusion_conditions=(
        "SIFA_MAWSUF does not assert attribute or quality",
        "SIFA_MAWSUF does not assert judgment about the head noun",
        "SIFA_MAWSUF does not evaluate the described property",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="composition_pattern_not_meaning/COMPOSITION_PATTERN.SIFA_MAWSUF",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(COMPOSITION_PATTERN.SIFA_MAWSUF) is "
                "formal composition pattern, not meaning — "
                "SIFA_MAWSUF ≠ attribute judgment"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/COMPOSITION_PATTERN.SIFA_MAWSUF",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What quality or attribute the qualifier asserts about "
                "the head is not licensed here — deferred to "
                "post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/COMPOSITION_PATTERN.SIFA_MAWSUF",
)

#: ATIF formal definition.
ATIF_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="COMPOSITION_PATTERN.ATIF",
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family=ATIF_FAMILY,
    canonical_name="'atf",
    definition_text=(
        "A formal composition pattern in which a conjunction (harf "
        "'atf) connects two elements (ma'tuf 'alayh and ma'tuf) "
        "with case agreement between the conjuncts. Proved by: "
        "(1) conjunction particle present between elements, "
        "(2) case agreement between the two conjuncts. This is a "
        "structural coordination arrangement, not an assertion of "
        "equivalence or shared properties."
    ),
    distinguishing_evidence=(
        "Conjunction particle connecting two elements with case "
        "agreement — distinguishing from apposition (no conjunction), "
        "qualifier (four-way agreement beyond case), and emphasis "
        "(identical repetition without conjunction)."
    ),
    boundary_conditions=(
        "Conjunction particle (harf 'atf) present between elements",
        "Case agreement between the two conjuncts",
        "Both conjuncts occupy comparable structural positions",
    ),
    exclusion_conditions=(
        "ATIF does not assert semantic equivalence between conjuncts",
        "ATIF does not assert shared properties or attributes",
        "ATIF does not resolve conjunction type (wa/fa/thumma/aw) to temporal or logical relation",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="composition_pattern_not_meaning/COMPOSITION_PATTERN.ATIF",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(COMPOSITION_PATTERN.ATIF) is "
                "formal composition pattern, not meaning — "
                "ATIF ≠ semantic coordination"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/COMPOSITION_PATTERN.ATIF",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What semantic relation the conjunction establishes "
                "(temporal sequence, addition, alternation) is not "
                "licensed here — deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/COMPOSITION_PATTERN.ATIF",
)

#: BADAL formal definition.
BADAL_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="COMPOSITION_PATTERN.BADAL",
    domain=FormalShapeDomain.COMPOSITION_PATTERN,
    family=BADAL_FAMILY,
    canonical_name="badal",
    definition_text=(
        "A formal composition pattern in which an appositive "
        "(badal) follows its head (mubdal minhu) with case "
        "agreement, where the appositive structurally replaces the "
        "head in governance terms. Proved by: (1) appositive in "
        "post-head position, (2) case agreement with the head, "
        "(3) no conjunction connecting them, (4) structural "
        "replaceability. This is a structural apposition "
        "arrangement, not a claim about referential identity."
    ),
    distinguishing_evidence=(
        "Post-head position with case agreement but no conjunction "
        "and structural replaceability — distinguishing from "
        "coordination (requires conjunction), qualifier (four-way "
        "agreement), and emphasis (identical repetition)."
    ),
    boundary_conditions=(
        "Appositive (badal) follows head (mubdal minhu) directly",
        "Case agreement between appositive and head",
        "No conjunction particle connects them",
    ),
    exclusion_conditions=(
        "BADAL does not assert referential identity",
        "BADAL does not assert semantic substitution",
        "BADAL does not resolve which badal type (kull/ba'd/ishtimal/ghalat)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="composition_pattern_not_meaning/COMPOSITION_PATTERN.BADAL",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(COMPOSITION_PATTERN.BADAL) is "
                "formal composition pattern, not meaning — "
                "BADAL ≠ semantic substitution"
            ),
        ),
        Residual(
            name="SEMANTIC_DALALAH_DEFERRED/COMPOSITION_PATTERN.BADAL",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "What referential relation the apposition establishes "
                "is not licensed here — deferred to post-formal-closure."
            ),
        ),
    ),
    trace_ref="canonical/COMPOSITION_PATTERN.BADAL",
)


# ---------------------------------------------------------------------------
# build_composition_pattern_registry() — assemble COMPOSITION_PATTERN registry
# ---------------------------------------------------------------------------


def build_composition_pattern_registry(
    definitions: tuple[FormalShapeDefinition, ...] | None = None,
) -> FormalShapeRegistry:
    """Assemble the COMPOSITION_PATTERN domain registry (docs/34 §10).

    This is a **pure function**: it accepts values and returns a value.
    If no definitions are provided, uses all 6 canonical definitions.

    The registry is CLOSED when all 6 required families have at least
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
            NOMINAL_SENTENCE_DEFINITION,
            VERBAL_SENTENCE_DEFINITION,
            IDAFA_DEFINITION,
            SIFA_MAWSUF_DEFINITION,
            ATIF_DEFINITION,
            BADAL_DEFINITION,
        )

    # Validate all definitions belong to COMPOSITION_PATTERN
    for defn in definitions:
        if defn.domain is not FormalShapeDomain.COMPOSITION_PATTERN:
            return FormalShapeRegistry(
                domain=FormalShapeDomain.COMPOSITION_PATTERN,
                families=COMPOSITION_PATTERN_FAMILIES,
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
                    domain=FormalShapeDomain.COMPOSITION_PATTERN,
                    families=COMPOSITION_PATTERN_FAMILIES,
                    definitions=definitions,
                    rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                    closure_state=FormalShapeClosureState.REFUSED,
                )

    # Compute closure state
    if not definitions:
        closure_state = FormalShapeClosureState.EMPTY
    else:
        required_family_ids = {f.family_id for f in COMPOSITION_PATTERN_FAMILIES}
        covered_family_ids = {d.family.family_id for d in definitions}
        if required_family_ids <= covered_family_ids:
            closure_state = FormalShapeClosureState.CLOSED
        else:
            closure_state = FormalShapeClosureState.PARTIAL

    return FormalShapeRegistry(
        domain=FormalShapeDomain.COMPOSITION_PATTERN,
        families=COMPOSITION_PATTERN_FAMILIES,
        definitions=definitions,
        rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
        closure_state=closure_state,
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "ATIF_DEFINITION",
    "ATIF_FAMILY",
    "BADAL_DEFINITION",
    "BADAL_FAMILY",
    "COMPOSITION_PATTERN_FAMILIES",
    "CompositionPatternDefinitionState",
    "CompositionPatternDefinitionVerdict",
    "IDAFA_DEFINITION",
    "IDAFA_FAMILY",
    "NOMINAL_SENTENCE_DEFINITION",
    "NOMINAL_SENTENCE_FAMILY",
    "SIFA_MAWSUF_DEFINITION",
    "SIFA_MAWSUF_FAMILY",
    "VERBAL_SENTENCE_DEFINITION",
    "VERBAL_SENTENCE_FAMILY",
    "build_composition_pattern_registry",
    "define_composition_pattern_shape",
]
