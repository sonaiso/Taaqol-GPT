"""Word-Class Formal Definitions — PR-F2.

PR-F2 binding of ``docs/34_FORMAL_SHAPE_REGISTRY_LAW.md`` §5 (WORD_CLASS).
This module introduces:

* :class:`FormalShapeDomain` — the top-level domain classification.
* :class:`FormalShapeFamily` — the sub-classification within a domain.
* :class:`FormalShapeDefinition` — the proven formal type (frozen carrier).
* :class:`FormalShapeClosureState` — the registry closure states.
* :class:`FormalShapeRegistry` — the classified collection for one domain.
* :class:`WordClassDefinitionVerdict` — the verdict of a definition attempt.
* :class:`WordClassDefinitionState` — two-state verdict outcome.
* :func:`define_word_class_shape` — pure function proving a word-class
  formal shape from constitutional evidence.
* :func:`build_word_class_registry` — pure function assembling the
  WORD_CLASS domain registry from proven definitions.
* Constants: ``ISM_DEFINITION``, ``FIL_DEFINITION``, ``HARF_DEFINITION``
  — the three canonical proven definitions.

Constitutional invariants (docs/34):

* FormalShapeDefinition ≠ Meaning.
* FormalShapeDefinition ≠ SemanticEntry.
* FormalShapeDefinition ≠ WadʿiSignified.
* FormalShapeDefinition ≠ Dalālah.
* FormalShapeDefinition ≠ SyntaxRole.
* FormalShapeRegistry ≠ SemanticLexicon.
* Word-class is formal category, not meaning.
* ISM ≠ meaning; FI'L ≠ event; HARF ≠ semantic relation.
* No rank promotion beyond FORMAL_SHAPE_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* All operations are pure: no I/O, no ledger, no network.
* No new FailureCode members; no new runtime dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The rank ceiling for formal shape definitions (docs/34 §3.1 point 11).
#: Same as BIRTH_RANK_CEILING — no gate promotes formal shapes in PR-F2.
FORMAL_SHAPE_RANK_CEILING: Rank = Rank.CANDIDATE


# ---------------------------------------------------------------------------
# FormalShapeDomain — the top-level classification
# ---------------------------------------------------------------------------


class FormalShapeDomain(StrEnum):
    """Top-level domain classification (docs/34 §1).

    Each domain is a bounded classification space. Domains do not overlap:
    a formal shape belongs to exactly one domain.
    """

    WORD_CLASS = "WORD_CLASS"
    BUILT_REFERENCE = "BUILT_REFERENCE"
    WEIGHT_PATTERN = "WEIGHT_PATTERN"
    INFLECTION = "INFLECTION"
    CONTRACT_SLOT = "CONTRACT_SLOT"
    COMPOSITION_PATTERN = "COMPOSITION_PATTERN"


# ---------------------------------------------------------------------------
# FormalShapeFamily — the sub-classification within a domain
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FormalShapeFamily:
    """A family within a domain (docs/34 §2).

    Families group related formal shapes within a domain. For example,
    within WORD_CLASS: ISM, FI'L, HARF are families.
    """

    domain: FormalShapeDomain
    family_id: str
    description: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        if not isinstance(self.domain, FormalShapeDomain):
            raise WeightCarrierSchemaError(
                f"FormalShapeFamily.domain must be a FormalShapeDomain, "
                f"got {type(self.domain).__name__}",
                FailureCode.DOMAIN_MISSING,
            )
        if not isinstance(self.family_id, str) or not self.family_id.strip():
            raise WeightCarrierSchemaError(
                "FormalShapeFamily.family_id must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not isinstance(self.description, str) or not self.description.strip():
            raise WeightCarrierSchemaError(
                "FormalShapeFamily.description must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )


# ---------------------------------------------------------------------------
# FormalShapeDefinition — the proven formal type
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FormalShapeDefinition:
    """A proven formal shape definition (docs/34 §3).

    This is the constitutional middle term between the signifier surface
    (proved by the pre-semantic chain PR-10..PR-19) and the semantic
    lexicon (not yet licensed). It describes the STRUCTURAL FORM of a
    grammatical category — its shape, conditions, and evidence — never
    its semantic content.

    FormalShapeDefinition is structure, not meaning:
    - FormalShapeDefinition ≠ Meaning
    - FormalShapeDefinition ≠ SemanticEntry
    - FormalShapeDefinition ≠ WadʿiSignified
    - FormalShapeDefinition ≠ Dalālah
    - FormalShapeDefinition ≠ SyntaxRole
    """

    shape_id: str
    domain: FormalShapeDomain
    family: FormalShapeFamily
    canonical_name: str
    definition_text: str
    distinguishing_evidence: str
    boundary_conditions: tuple[str, ...]
    exclusion_conditions: tuple[str, ...]
    weight_constraint: str | None
    path_constraint: str | None
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- shape_id ---
        if not isinstance(self.shape_id, str) or not self.shape_id.strip():
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.shape_id must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- domain ---
        if not isinstance(self.domain, FormalShapeDomain):
            raise WeightCarrierSchemaError(
                f"FormalShapeDefinition.domain must be a FormalShapeDomain, "
                f"got {type(self.domain).__name__}",
                FailureCode.DOMAIN_MISSING,
            )
        # --- family ---
        if not isinstance(self.family, FormalShapeFamily):
            raise WeightCarrierSchemaError(
                f"FormalShapeDefinition.family must be a FormalShapeFamily, "
                f"got {type(self.family).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if self.family.domain is not self.domain:
            raise WeightCarrierSchemaError(
                f"FormalShapeDefinition.family.domain ({self.family.domain.value}) "
                f"must match FormalShapeDefinition.domain ({self.domain.value})",
                FailureCode.DOMAIN_MISSING,
            )
        # --- canonical_name ---
        if not isinstance(self.canonical_name, str) or not self.canonical_name.strip():
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.canonical_name must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- definition_text ---
        if not isinstance(self.definition_text, str) or not self.definition_text.strip():
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.definition_text must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- distinguishing_evidence ---
        if (
            not isinstance(self.distinguishing_evidence, str)
            or not self.distinguishing_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.distinguishing_evidence must be a "
                "non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- boundary_conditions ---
        if not isinstance(self.boundary_conditions, tuple):
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.boundary_conditions must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not self.boundary_conditions:
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.boundary_conditions must be non-empty",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        for bc in self.boundary_conditions:
            if not isinstance(bc, str) or not bc.strip():
                raise WeightCarrierSchemaError(
                    "Each boundary_condition must be a non-empty string",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        # --- exclusion_conditions ---
        if not isinstance(self.exclusion_conditions, tuple):
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.exclusion_conditions must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        for ec in self.exclusion_conditions:
            if not isinstance(ec, str) or not ec.strip():
                raise WeightCarrierSchemaError(
                    "Each exclusion_condition must be a non-empty string",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        # --- weight_constraint ---
        if (
            self.weight_constraint is not None
            and (not isinstance(self.weight_constraint, str) or not self.weight_constraint.strip())
        ):
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.weight_constraint, if present, must be "
                "a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- path_constraint ---
        if (
            self.path_constraint is not None
            and (not isinstance(self.path_constraint, str) or not self.path_constraint.strip())
        ):
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.path_constraint, if present, must be "
                "a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- rank ---
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"FormalShapeDefinition.rank must be a Rank member, "
                f"got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > FORMAL_SHAPE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"FormalShapeDefinition.rank {self.rank.name} exceeds ceiling "
                f"{FORMAL_SHAPE_RANK_CEILING.name}",
                FailureCode.RANK_EXCEEDS_CEILING,
            )
        # --- residuals ---
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "FormalShapeDefinition.residuals must be a tuple",
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
                "FormalShapeDefinition.trace_ref must be a non-empty string",
                FailureCode.TRACE_MISSING,
            )


# ---------------------------------------------------------------------------
# FormalShapeClosureState — registry closure states
# ---------------------------------------------------------------------------


class FormalShapeClosureState(StrEnum):
    """Closure state of a FormalShapeRegistry (docs/34 §4.1)."""

    CLOSED = "CLOSED"
    PARTIAL = "PARTIAL"
    EMPTY = "EMPTY"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# FormalShapeRegistry — the classified collection for one domain
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FormalShapeRegistry:
    """A domain-level registry of formal shape definitions (docs/34 §4).

    The registry holds all definitions for a single domain. A registry
    with no definitions is EMPTY. A registry with definitions but
    incomplete families is PARTIAL. A registry with all required families
    proven is CLOSED.

    FormalShapeRegistry ≠ SemanticLexicon — the registry is a
    structural catalogue, not a meaning dictionary.
    """

    domain: FormalShapeDomain
    families: tuple[FormalShapeFamily, ...]
    definitions: tuple[FormalShapeDefinition, ...]
    rank_ceiling: Rank
    closure_state: FormalShapeClosureState

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- domain ---
        if not isinstance(self.domain, FormalShapeDomain):
            raise WeightCarrierSchemaError(
                f"FormalShapeRegistry.domain must be a FormalShapeDomain, "
                f"got {type(self.domain).__name__}",
                FailureCode.DOMAIN_MISSING,
            )
        # --- families ---
        if not isinstance(self.families, tuple):
            raise WeightCarrierSchemaError(
                "FormalShapeRegistry.families must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        for f in self.families:
            if not isinstance(f, FormalShapeFamily):
                raise WeightCarrierSchemaError(
                    f"Each family must be a FormalShapeFamily, "
                    f"got {type(f).__name__}",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if f.domain is not self.domain:
                raise WeightCarrierSchemaError(
                    f"Family domain ({f.domain.value}) must match registry "
                    f"domain ({self.domain.value})",
                    FailureCode.DOMAIN_MISSING,
                )
        # --- definitions ---
        if not isinstance(self.definitions, tuple):
            raise WeightCarrierSchemaError(
                "FormalShapeRegistry.definitions must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        for d in self.definitions:
            if not isinstance(d, FormalShapeDefinition):
                raise WeightCarrierSchemaError(
                    f"Each definition must be a FormalShapeDefinition, "
                    f"got {type(d).__name__}",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if d.domain is not self.domain:
                raise WeightCarrierSchemaError(
                    f"Definition domain ({d.domain.value}) must match "
                    f"registry domain ({self.domain.value})",
                    FailureCode.DOMAIN_MISSING,
                )
        # --- rank_ceiling ---
        if not isinstance(self.rank_ceiling, Rank):
            raise WeightCarrierSchemaError(
                f"FormalShapeRegistry.rank_ceiling must be a Rank, "
                f"got {type(self.rank_ceiling).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        # --- closure_state ---
        if not isinstance(self.closure_state, FormalShapeClosureState):
            raise WeightCarrierSchemaError(
                f"FormalShapeRegistry.closure_state must be a "
                f"FormalShapeClosureState, "
                f"got {type(self.closure_state).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )


# ---------------------------------------------------------------------------
# WordClassDefinitionState — verdict outcome
# ---------------------------------------------------------------------------


class WordClassDefinitionState(StrEnum):
    """The outcome of a define_word_class_shape() operation."""

    DEFINED = "DEFINED"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# WordClassDefinitionVerdict — the definition proof
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WordClassDefinitionVerdict:
    """The output of :func:`define_word_class_shape` (docs/34 §5).

    Proves that a word-class formal shape definition satisfies all
    constitutional requirements. It does NOT carry meaning, ifadah,
    hukm, reality, or any semantic content.
    """

    definition: FormalShapeDefinition | None
    verdict_state: WordClassDefinitionState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, WordClassDefinitionState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be WordClassDefinitionState, "
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
        if self.verdict_state is WordClassDefinitionState.DEFINED:
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
        elif self.verdict_state is WordClassDefinitionState.REFUSED:
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
# WORD_CLASS Families (docs/34 §5)
# ---------------------------------------------------------------------------

#: ISM (noun/name) family.
ISM_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WORD_CLASS,
    family_id="ISM",
    description="Noun/name — accepts al- (definite article), tanwin, or jarr",
)

#: FI'L (verb) family.
FIL_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WORD_CLASS,
    family_id="FIL",
    description="Verb — accepts ta' al-fa'il, qad, sawfa, or sin",
)

#: HARF (particle) family.
HARF_FAMILY = FormalShapeFamily(
    domain=FormalShapeDomain.WORD_CLASS,
    family_id="HARF",
    description="Particle — does not accept noun-markers or verb-markers",
)

#: All WORD_CLASS families.
WORD_CLASS_FAMILIES: tuple[FormalShapeFamily, ...] = (
    ISM_FAMILY,
    FIL_FAMILY,
    HARF_FAMILY,
)


# ---------------------------------------------------------------------------
# define_word_class_shape() — the definition operation
# ---------------------------------------------------------------------------


def define_word_class_shape(
    shape_id: str,
    family: FormalShapeFamily,
    canonical_name: str,
    definition_text: str,
    distinguishing_evidence: str,
    boundary_conditions: tuple[str, ...],
    exclusion_conditions: tuple[str, ...],
    weight_constraint: str | None = None,
    path_constraint: str | None = None,
) -> WordClassDefinitionVerdict:
    """Prove a word-class formal shape definition (docs/34 §5).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    Parameters
    ----------
    shape_id : str
        Globally unique identifier for this formal shape.
    family : FormalShapeFamily
        Must belong to the WORD_CLASS domain (ISM, FI'L, or HARF).
    canonical_name : str
        The Arabic grammatical term (e.g., "ism", "fi'l", "harf").
    definition_text : str
        Formal textual definition proving the shape.
    distinguishing_evidence : str
        What proves this shape vs. the other two word classes.
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
    WordClassDefinitionVerdict
        DEFINED with a FormalShapeDefinition on success; REFUSED with a
        named FailureCode on any violation.
    """
    # --- Input boundary: shape_id ---
    if not isinstance(shape_id, str) or not shape_id.strip():
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/shape_id_empty",
        )

    # --- Input boundary: family type and domain ---
    if not isinstance(family, FormalShapeFamily):
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/family_not_formal_shape_family",
        )
    if family.domain is not FormalShapeDomain.WORD_CLASS:
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.DOMAIN_MISSING,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/family_domain_not_word_class",
        )

    # --- Input boundary: canonical_name ---
    if not isinstance(canonical_name, str) or not canonical_name.strip():
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/canonical_name_empty",
        )

    # --- Input boundary: definition_text ---
    if not isinstance(definition_text, str) or not definition_text.strip():
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/definition_text_empty",
        )

    # --- Input boundary: distinguishing_evidence ---
    if not isinstance(distinguishing_evidence, str) or not distinguishing_evidence.strip():
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/distinguishing_evidence_empty",
        )

    # --- Input boundary: boundary_conditions ---
    if not isinstance(boundary_conditions, tuple):
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/boundary_conditions_not_tuple",
        )
    if not boundary_conditions:
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/boundary_conditions_empty",
        )
    for bc in boundary_conditions:
        if not isinstance(bc, str) or not bc.strip():
            return WordClassDefinitionVerdict(
                definition=None,
                verdict_state=WordClassDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_word_class_shape/refused/boundary_condition_invalid",
            )

    # --- Input boundary: exclusion_conditions ---
    if not isinstance(exclusion_conditions, tuple):
        return WordClassDefinitionVerdict(
            definition=None,
            verdict_state=WordClassDefinitionState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="define_word_class_shape/refused/exclusion_conditions_not_tuple",
        )
    for ec in exclusion_conditions:
        if not isinstance(ec, str) or not ec.strip():
            return WordClassDefinitionVerdict(
                definition=None,
                verdict_state=WordClassDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="define_word_class_shape/refused/exclusion_condition_invalid",
            )

    # --- Rank bounding via lattice meet ---
    definition_rank = RankLattice.meet(
        Rank.CANDIDATE,
        FORMAL_SHAPE_RANK_CEILING,
    )

    # --- Residuals: open residual noting formal shape does not carry meaning ---
    open_residuals: tuple[Residual, ...] = (
        Residual(
            name=f"formal_category_not_meaning/{shape_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"FormalShapeDefinition({shape_id}) is formal category, "
                f"not meaning — ISM ≠ meaning, FI'L ≠ event, HARF ≠ "
                f"semantic relation"
            ),
        ),
    )

    # --- Construct the FormalShapeDefinition ---
    definition = FormalShapeDefinition(
        shape_id=shape_id,
        domain=FormalShapeDomain.WORD_CLASS,
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
        trace_ref=f"define_word_class_shape/defined/{shape_id}",
    )

    return WordClassDefinitionVerdict(
        definition=definition,
        verdict_state=WordClassDefinitionState.DEFINED,
        failure_code=None,
        verdict_rank=definition_rank,
        residuals=open_residuals,
        trace_ref=f"define_word_class_shape/defined/{shape_id}",
    )


# ---------------------------------------------------------------------------
# Canonical WORD_CLASS definitions (docs/34 §5)
# ---------------------------------------------------------------------------

#: ISM (noun/name) formal definition.
ISM_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WORD_CLASS.ISM",
    domain=FormalShapeDomain.WORD_CLASS,
    family=ISM_FAMILY,
    canonical_name="ism",
    definition_text=(
        "A word that denotes a meaning in itself without being bound to "
        "a time reference. Proved formally by acceptance of al- (the "
        "definite article), tanwin (nunation), or jarr (genitive "
        "preposition governance)."
    ),
    distinguishing_evidence=(
        "Accepts al- (definite article), tanwin, or jarr (genitive "
        "governance) — markers that neither fi'l nor harf accept."
    ),
    boundary_conditions=(
        "Accepts al- (definite article)",
        "Accepts tanwin (nunation)",
        "Accepts jarr (genitive governance)",
    ),
    exclusion_conditions=(
        "Does not accept ta' al-fa'il (subject-ta')",
        "Does not accept qad",
        "Does not accept sawfa or sin (futurity markers)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="formal_category_not_meaning/WORD_CLASS.ISM",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WORD_CLASS.ISM) is formal category, "
                "not meaning — ISM ≠ meaning"
            ),
        ),
    ),
    trace_ref="canonical/WORD_CLASS.ISM",
)

#: FI'L (verb) formal definition.
FIL_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WORD_CLASS.FIL",
    domain=FormalShapeDomain.WORD_CLASS,
    family=FIL_FAMILY,
    canonical_name="fi'l",
    definition_text=(
        "A word that denotes a meaning in itself and is bound to a time "
        "reference. Proved formally by acceptance of ta' al-fa'il "
        "(subject-ta'), qad, sawfa, or sin."
    ),
    distinguishing_evidence=(
        "Accepts ta' al-fa'il (subject-ta'), qad, sawfa, or sin — "
        "markers that neither ism nor harf accept."
    ),
    boundary_conditions=(
        "Accepts ta' al-fa'il (subject-ta')",
        "Accepts qad (emphasis/completion particle)",
        "Accepts sawfa or sin (futurity markers)",
    ),
    exclusion_conditions=(
        "Does not accept al- (definite article)",
        "Does not accept tanwin (nunation)",
        "Does not accept jarr (genitive governance)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="formal_category_not_meaning/WORD_CLASS.FIL",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WORD_CLASS.FIL) is formal category, "
                "not meaning — FI'L ≠ event"
            ),
        ),
    ),
    trace_ref="canonical/WORD_CLASS.FIL",
)

#: HARF (particle) formal definition.
HARF_DEFINITION: FormalShapeDefinition = FormalShapeDefinition(
    shape_id="WORD_CLASS.HARF",
    domain=FormalShapeDomain.WORD_CLASS,
    family=HARF_FAMILY,
    canonical_name="harf",
    definition_text=(
        "A word that denotes a meaning only in combination with another "
        "word (ism or fi'l), not independently. Proved formally by the "
        "rejection of both noun-markers and verb-markers."
    ),
    distinguishing_evidence=(
        "Does not accept noun-markers (al-, tanwin, jarr) and does not "
        "accept verb-markers (ta' al-fa'il, qad, sawfa, sin) — the "
        "negative criterion that distinguishes harf from both ism and fi'l."
    ),
    boundary_conditions=(
        "Does not accept al- (definite article)",
        "Does not accept tanwin (nunation)",
        "Does not accept jarr (genitive governance)",
        "Does not accept ta' al-fa'il (subject-ta')",
        "Does not accept qad",
        "Does not accept sawfa or sin (futurity markers)",
    ),
    exclusion_conditions=(
        "Accepts al- (would make it ism)",
        "Accepts tanwin (would make it ism)",
        "Accepts ta' al-fa'il (would make it fi'l)",
        "Accepts qad (would make it fi'l)",
    ),
    weight_constraint=None,
    path_constraint=None,
    rank=Rank.CANDIDATE,
    residuals=(
        Residual(
            name="formal_category_not_meaning/WORD_CLASS.HARF",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                "FormalShapeDefinition(WORD_CLASS.HARF) is formal category, "
                "not meaning — HARF ≠ semantic relation"
            ),
        ),
    ),
    trace_ref="canonical/WORD_CLASS.HARF",
)


# ---------------------------------------------------------------------------
# build_word_class_registry() — assemble WORD_CLASS registry
# ---------------------------------------------------------------------------


def build_word_class_registry(
    definitions: tuple[FormalShapeDefinition, ...] | None = None,
) -> FormalShapeRegistry:
    """Assemble the WORD_CLASS domain registry (docs/34 §4).

    This is a **pure function**: it accepts values and returns a value.
    If no definitions are provided, uses the three canonical definitions
    (ISM, FI'L, HARF).

    The registry is CLOSED when all three required families (ISM, FI'L,
    HARF) have at least one proven definition each. Otherwise PARTIAL
    or EMPTY.

    Parameters
    ----------
    definitions : tuple[FormalShapeDefinition, ...] | None
        Definitions to register. If None, uses the canonical three.

    Returns
    -------
    FormalShapeRegistry
        The assembled registry with its computed closure_state.
    """
    if definitions is None:
        definitions = (ISM_DEFINITION, FIL_DEFINITION, HARF_DEFINITION)

    # Validate all definitions belong to WORD_CLASS
    for defn in definitions:
        if defn.domain is not FormalShapeDomain.WORD_CLASS:
            # Return REFUSED registry — wrong domain
            return FormalShapeRegistry(
                domain=FormalShapeDomain.WORD_CLASS,
                families=WORD_CLASS_FAMILIES,
                definitions=(),
                rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                closure_state=FormalShapeClosureState.REFUSED,
            )

    # Check residuals for HIDDEN_FORBIDDEN or BLOCKING
    for defn in definitions:
        for r in defn.residuals:
            if r.kind is ResidualKind.HIDDEN_FORBIDDEN:
                return FormalShapeRegistry(
                    domain=FormalShapeDomain.WORD_CLASS,
                    families=WORD_CLASS_FAMILIES,
                    definitions=definitions,
                    rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                    closure_state=FormalShapeClosureState.REFUSED,
                )
            if r.kind is ResidualKind.BLOCKING:
                return FormalShapeRegistry(
                    domain=FormalShapeDomain.WORD_CLASS,
                    families=WORD_CLASS_FAMILIES,
                    definitions=definitions,
                    rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                    closure_state=FormalShapeClosureState.REFUSED,
                )

    # Compute closure state
    if not definitions:
        closure_state = FormalShapeClosureState.EMPTY
    else:
        # Check all required families have at least one definition
        required_family_ids = {f.family_id for f in WORD_CLASS_FAMILIES}
        covered_family_ids = {d.family.family_id for d in definitions}
        if required_family_ids <= covered_family_ids:
            closure_state = FormalShapeClosureState.CLOSED
        else:
            closure_state = FormalShapeClosureState.PARTIAL

    return FormalShapeRegistry(
        domain=FormalShapeDomain.WORD_CLASS,
        families=WORD_CLASS_FAMILIES,
        definitions=definitions,
        rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
        closure_state=closure_state,
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "FIL_DEFINITION",
    "FIL_FAMILY",
    "FORMAL_SHAPE_RANK_CEILING",
    "FormalShapeClosureState",
    "FormalShapeDefinition",
    "FormalShapeDomain",
    "FormalShapeFamily",
    "FormalShapeRegistry",
    "HARF_DEFINITION",
    "HARF_FAMILY",
    "ISM_DEFINITION",
    "ISM_FAMILY",
    "WORD_CLASS_FAMILIES",
    "WordClassDefinitionState",
    "WordClassDefinitionVerdict",
    "build_word_class_registry",
    "define_word_class_shape",
]
