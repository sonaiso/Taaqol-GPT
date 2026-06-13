"""Formal Style Candidate — PR-F8.

PR-F8 binding of ``docs/35_FORMAL_STYLE_CANDIDATE_LAW.md``.

This module introduces the formal style classification layer that
operates on closed formal composition patterns. Formal style
classifies HOW a composition pattern is used (khabar/inshāʾ and
sub-families) without interpreting WHY or WHAT it communicates.

PR-F8 consumes only FormalShapeClosure.CLOSED and formal composition
evidence. It produces FormalStyleCandidate — a carrier that proves
formal style classification without meaning, dalālah, ifādah, hukm,
manṭūq, mafhūm, majāz, or manqūl.

Constitutional invariants:

* FORMAL_STYLE ≠ meaning.
* FORMAL_STYLE ≠ dalālah.
* FORMAL_STYLE ≠ ifādah.
* KHABAR_STYLE_FORM ≠ truth.
* KHABAR_STYLE_FORM ≠ assertion.
* KHABAR_STYLE_FORM ≠ proposition.
* INSHA_STYLE_FORM ≠ speaker intent.
* COMMAND_STYLE_FORM ≠ obligation.
* PROHIBITION_STYLE_FORM ≠ prohibition reality.
* INTERROGATIVE_STYLE_FORM ≠ request for answer.
* VOCATIVE_STYLE_FORM ≠ real addressee.
* WISH_STYLE_FORM ≠ psychological wish.
* HOPE_STYLE_FORM ≠ expectation.
* OATH_STYLE_FORM ≠ truth guarantee.
* CONDITION_STYLE_FORM ≠ conditional truth.
* EXCLAMATION_STYLE_FORM ≠ real emotion.
* Formal style is not meaning.
* Khabar/inshāʾ are formal sentence-style candidates only.
* No rank promotion beyond FORMAL_SHAPE_RANK_CEILING.
* Residual governance: HIDDEN_FORBIDDEN and BLOCKING refuse.
* All operations are pure: no I/O, no ledger, no network.
* No new FailureCode members; no new runtime dependencies.
* No positive 'meaning' language in definition_text.

Deferred residuals (binding):

* DALALAH_DEFERRED_TO_PR_D1 — dalālah not licensed here.
* MUFRAD_SEMANTIC_SLOT_GEOMETRY_DEFERRED_TO_PR_D1 — semantic slot
  geometry not licensed here.
* IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE — ifādah not here.
* MANTUQ_DEFERRED_UNTIL_IFADAH — manṭūq not here.
* MAFHUM_DEFERRED_UNTIL_MANTUQ — mafhūm not here.
* MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT — majāz not here.
* MANQUL_DEFERRED_UNTIL_TRANSFER_GATE — manqūl not here.
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
# FormalStyleFamily — the style classification families
# ---------------------------------------------------------------------------


class FormalStyleFamily(StrEnum):
    """Formal style families — the closed set of sentence-type forms.

    Each family is a formal classification of composition pattern
    usage style. These are structural classifications only: they do
    NOT carry meaning, truth value, speaker intent, or any semantic
    content.
    """

    DECLARATIVE_STYLE_FORM = "DECLARATIVE_STYLE_FORM"
    COMMAND_STYLE_FORM = "COMMAND_STYLE_FORM"
    PROHIBITION_STYLE_FORM = "PROHIBITION_STYLE_FORM"
    INTERROGATIVE_STYLE_FORM = "INTERROGATIVE_STYLE_FORM"
    VOCATIVE_STYLE_FORM = "VOCATIVE_STYLE_FORM"
    WISH_STYLE_FORM = "WISH_STYLE_FORM"
    HOPE_STYLE_FORM = "HOPE_STYLE_FORM"
    OATH_STYLE_FORM = "OATH_STYLE_FORM"
    CONDITION_STYLE_FORM = "CONDITION_STYLE_FORM"
    EXCLAMATION_STYLE_FORM = "EXCLAMATION_STYLE_FORM"


#: All formal style families as a tuple.
FORMAL_STYLE_FAMILIES: tuple[FormalStyleFamily, ...] = tuple(FormalStyleFamily)


# ---------------------------------------------------------------------------
# FormalStyleState — verdict outcome
# ---------------------------------------------------------------------------


class FormalStyleState(StrEnum):
    """The outcome of a prove_formal_style_candidate() operation."""

    PROVEN = "PROVEN"
    REFUSED = "REFUSED"


# ---------------------------------------------------------------------------
# FormalStyleCandidate — the proven formal style carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FormalStyleCandidate:
    """A proven formal style classification (docs/35).

    Proves that a composition pattern has a formal style classification.
    This is a structural classification only — it does NOT carry meaning,
    truth value, speaker intent, dalālah, ifādah, or any semantic content.

    FormalStyleCandidate opens PR-D1 readiness only.
    FormalStyleCandidate does not open Ifādah.
    """

    style_family: FormalStyleFamily
    composition_evidence_ref: str
    formal_closure_ref: str
    definition_text: str
    distinguishing_evidence: str
    boundary_conditions: tuple[str, ...]
    exclusion_conditions: tuple[str, ...]
    rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- style_family type ---
        if not isinstance(self.style_family, FormalStyleFamily):
            raise WeightCarrierSchemaError(
                f"style_family must be a FormalStyleFamily member, "
                f"got {type(self.style_family).__name__}",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- composition_evidence_ref ---
        if (
            not isinstance(self.composition_evidence_ref, str)
            or not self.composition_evidence_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "composition_evidence_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- formal_closure_ref ---
        if (
            not isinstance(self.formal_closure_ref, str)
            or not self.formal_closure_ref.strip()
        ):
            raise WeightCarrierSchemaError(
                "formal_closure_ref must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- definition_text ---
        if (
            not isinstance(self.definition_text, str)
            or not self.definition_text.strip()
        ):
            raise WeightCarrierSchemaError(
                "definition_text must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- distinguishing_evidence ---
        if (
            not isinstance(self.distinguishing_evidence, str)
            or not self.distinguishing_evidence.strip()
        ):
            raise WeightCarrierSchemaError(
                "distinguishing_evidence must be a non-empty string",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        # --- boundary_conditions ---
        if not isinstance(self.boundary_conditions, tuple):
            raise WeightCarrierSchemaError(
                "boundary_conditions must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        if not self.boundary_conditions:
            raise WeightCarrierSchemaError(
                "boundary_conditions must be non-empty",
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
                "exclusion_conditions must be a tuple",
                FailureCode.REQUIRED_SLOT_EMPTY,
            )
        for ec in self.exclusion_conditions:
            if not isinstance(ec, str) or not ec.strip():
                raise WeightCarrierSchemaError(
                    "Each exclusion_condition must be a non-empty string",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
        # --- rank ---
        if not isinstance(self.rank, Rank):
            raise WeightCarrierSchemaError(
                f"rank must be a Rank member, got {type(self.rank).__name__}",
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            )
        if self.rank > FORMAL_SHAPE_RANK_CEILING:
            raise WeightCarrierSchemaError(
                f"rank {self.rank.name} exceeds ceiling "
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


# ---------------------------------------------------------------------------
# FormalStyleVerdict — the proof output
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FormalStyleVerdict:
    """The output of :func:`prove_formal_style_candidate` (docs/35).

    Carries a proven FormalStyleCandidate on success, or a named
    FailureCode on refusal. Does NOT carry meaning, dalālah, ifādah,
    hukm, or any semantic content.
    """

    candidate: FormalStyleCandidate | None
    verdict_state: FormalStyleState
    failure_code: FailureCode | None
    verdict_rank: Rank
    residuals: tuple[Residual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        from taaqqul_slot_geometry.weight.carrier_core import (
            WeightCarrierSchemaError,
        )

        # --- verdict_state type ---
        if not isinstance(self.verdict_state, FormalStyleState):
            raise WeightCarrierSchemaError(
                f"verdict_state must be FormalStyleState, "
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
        if self.verdict_state is FormalStyleState.PROVEN:
            if self.failure_code is not None:
                raise WeightCarrierSchemaError(
                    "PROVEN verdict must have failure_code=None",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if self.candidate is None:
                raise WeightCarrierSchemaError(
                    "PROVEN verdict must have a FormalStyleCandidate",
                    FailureCode.REQUIRED_SLOT_EMPTY,
                )
            if not isinstance(self.candidate, FormalStyleCandidate):
                raise WeightCarrierSchemaError(
                    f"PROVEN candidate must be FormalStyleCandidate, "
                    f"got {type(self.candidate).__name__}",
                    FailureCode.GATE_REQUIRED,
                )
        elif self.verdict_state is FormalStyleState.REFUSED:
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
# Canonical style definitions — formal classification descriptions
# ---------------------------------------------------------------------------

#: Canonical formal style definitions. Each maps a FormalStyleFamily
#: to its formal structural description. These describe WHAT the form
#: IS structurally, never what it MEANS or intends.
FORMAL_STYLE_DEFINITIONS: dict[FormalStyleFamily, dict[str, object]] = {
    FormalStyleFamily.DECLARATIVE_STYLE_FORM: {
        "canonical_name": "khabar",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally admits truth-predication "
            "markers (tashkil al-khabar). Proved by: presence of "
            "compositional slots that formally support a predication "
            "structure. This is a formal structural classification, "
            "not a truth-bearing assertion or proposition."
        ),
        "distinguishing_evidence": (
            "Structural admittance of truth-predication markers — "
            "distinguishing from insha' forms which lack these markers."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Pattern structurally admits predication markers",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "DECLARATIVE_STYLE_FORM does not assert truth",
            "DECLARATIVE_STYLE_FORM does not assert proposition",
            "DECLARATIVE_STYLE_FORM does not carry semantic assertion",
            "DECLARATIVE_STYLE_FORM is not information transfer",
        ),
    },
    FormalStyleFamily.COMMAND_STYLE_FORM: {
        "canonical_name": "amr",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries a command-form "
            "marker (sighah amriyyah). Proved by: verbal element in "
            "imperative morphological pattern (fi'l amr or lam "
            "al-amr). This is a formal structural classification, "
            "not an obligation or real command."
        ),
        "distinguishing_evidence": (
            "Imperative morphological pattern (fi'l amr or lam al-amr) "
            "— distinguishing from declarative (predication markers) "
            "and from prohibition (la al-nahiyah)."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Verbal element in imperative morphological pattern",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "COMMAND_STYLE_FORM does not assert obligation",
            "COMMAND_STYLE_FORM does not create duty",
            "COMMAND_STYLE_FORM is not a real command to obey",
        ),
    },
    FormalStyleFamily.PROHIBITION_STYLE_FORM: {
        "canonical_name": "nahy",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries a prohibition-form "
            "marker (la al-nahiyah + fi'l mudari' majzum). Proved by: "
            "la al-nahiyah governing a jussive verb form. This is a "
            "formal structural classification, not a real forbiddance."
        ),
        "distinguishing_evidence": (
            "La al-nahiyah with jussive verb — distinguishing from "
            "command (imperative verb) and from negation (la al-nafiyah)."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "La al-nahiyah governs a jussive verb form",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "PROHIBITION_STYLE_FORM does not assert real prohibition",
            "PROHIBITION_STYLE_FORM does not create legal forbiddance",
            "PROHIBITION_STYLE_FORM is not a binding prohibition",
        ),
    },
    FormalStyleFamily.INTERROGATIVE_STYLE_FORM: {
        "canonical_name": "istifham",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries an interrogative "
            "marker (adah istifham). Proved by: presence of an "
            "interrogative particle (hal, hamzah, ma, man, etc.) or "
            "interrogative noun in pattern-initial position. This is "
            "a formal structural classification, not a request for "
            "an answer."
        ),
        "distinguishing_evidence": (
            "Interrogative particle or noun in pattern-initial "
            "position — distinguishing from declarative (no "
            "interrogative marker) and from exclamation (different "
            "structural marker)."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Interrogative marker present in initial position",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "INTERROGATIVE_STYLE_FORM does not request an answer",
            "INTERROGATIVE_STYLE_FORM does not express doubt",
            "INTERROGATIVE_STYLE_FORM is not a rhetorical question",
        ),
    },
    FormalStyleFamily.VOCATIVE_STYLE_FORM: {
        "canonical_name": "nida'",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries a vocative "
            "marker (harf nida'). Proved by: presence of a vocative "
            "particle (ya, ay, ayya, etc.) governing a called noun "
            "(munada). This is a formal structural classification, "
            "not a real call to a real addressee."
        ),
        "distinguishing_evidence": (
            "Vocative particle governing a called noun (munada) — "
            "distinguishing from other forms by the vocative "
            "governance relationship."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Vocative particle governs a called noun",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "VOCATIVE_STYLE_FORM does not address a real person",
            "VOCATIVE_STYLE_FORM does not establish communication",
            "VOCATIVE_STYLE_FORM is not a real call",
        ),
    },
    FormalStyleFamily.WISH_STYLE_FORM: {
        "canonical_name": "tamanni",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries a wish-form "
            "marker (adah tamanni — layta or hal). Proved by: "
            "presence of a wish particle (layta, or hal/law in "
            "wish context) governing its complement. This is a "
            "formal structural classification, not a psychological "
            "wish or desire."
        ),
        "distinguishing_evidence": (
            "Wish particle (layta or hal/law in wish context) with "
            "governed complement — distinguishing from hope "
            "(la'alla) and from declarative (no wish marker)."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Wish particle present and governing complement",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "WISH_STYLE_FORM does not assert psychological wish",
            "WISH_STYLE_FORM does not express desire",
            "WISH_STYLE_FORM is not a real want",
        ),
    },
    FormalStyleFamily.HOPE_STYLE_FORM: {
        "canonical_name": "taraji",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries a hope-form "
            "marker (adah taraji — la'alla). Proved by: presence "
            "of la'alla (or 'asa) governing its complement. This "
            "is a formal structural classification, not a real "
            "expectation or anticipation."
        ),
        "distinguishing_evidence": (
            "Hope particle (la'alla or 'asa) governing complement "
            "— distinguishing from wish (layta, for impossible/ "
            "difficult) and from declarative (no hope marker)."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Hope particle present and governing complement",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "HOPE_STYLE_FORM does not assert expectation",
            "HOPE_STYLE_FORM does not express anticipation",
            "HOPE_STYLE_FORM is not a real hope",
        ),
    },
    FormalStyleFamily.OATH_STYLE_FORM: {
        "canonical_name": "qasam",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries an oath-form "
            "marker (harf qasam — wa, ba, ta al-qasam). Proved by: "
            "presence of an oath particle governing a sworn-upon "
            "noun (muqsam bihi) with a response clause (jawab "
            "al-qasam). This is a formal structural classification, "
            "not a truth guarantee or binding oath."
        ),
        "distinguishing_evidence": (
            "Oath particle with sworn-upon noun and response clause "
            "— distinguishing from declarative (no oath governance) "
            "and from condition (no conditional particle)."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Oath particle governs sworn-upon noun",
            "Response clause (jawab al-qasam) present",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "OATH_STYLE_FORM does not guarantee truth",
            "OATH_STYLE_FORM does not create binding commitment",
            "OATH_STYLE_FORM is not a real oath",
        ),
    },
    FormalStyleFamily.CONDITION_STYLE_FORM: {
        "canonical_name": "shart",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries a conditional-form "
            "marker (adah shart — in, idha, law, etc.). Proved by: "
            "presence of a conditional particle governing a protasis "
            "(fi'l al-shart) and apodosis (jawab al-shart). This is "
            "a formal structural classification, not a conditional "
            "truth or causal relation."
        ),
        "distinguishing_evidence": (
            "Conditional particle with protasis-apodosis governance "
            "structure — distinguishing from declarative (no "
            "conditional governance) and from oath (different "
            "particle class)."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Conditional particle governs protasis and apodosis",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "CONDITION_STYLE_FORM does not assert conditional truth",
            "CONDITION_STYLE_FORM does not establish causation",
            "CONDITION_STYLE_FORM is not a real if-then",
        ),
    },
    FormalStyleFamily.EXCLAMATION_STYLE_FORM: {
        "canonical_name": "ta'ajjub",
        "definition_text": (
            "A formal sentence-style classification in which the "
            "composition pattern structurally carries an exclamation-form "
            "marker (sighah ta'ajjub — ma af'alahu or af'il bihi). "
            "Proved by: presence of an exclamatory pattern (ma + "
            "af'ala form, or af'il + bi- form). This is a formal "
            "structural classification, not a real emotion or "
            "psychological state."
        ),
        "distinguishing_evidence": (
            "Exclamatory structural pattern (ma af'alahu or af'il "
            "bihi) — distinguishing from declarative (no exclamatory "
            "pattern) and from interrogative (different particle "
            "class, despite shared 'ma')."
        ),
        "boundary_conditions": (
            "Composition pattern is formally closed",
            "Exclamatory morphological pattern present",
            "FormalShapeClosure.CLOSED prerequisite satisfied",
        ),
        "exclusion_conditions": (
            "EXCLAMATION_STYLE_FORM does not assert real emotion",
            "EXCLAMATION_STYLE_FORM does not express psychological state",
            "EXCLAMATION_STYLE_FORM is not real amazement",
        ),
    },
}


# ---------------------------------------------------------------------------
# Required deferred residuals (constitutional binding)
# ---------------------------------------------------------------------------


def _build_deferred_residuals(style_family: FormalStyleFamily) -> tuple[Residual, ...]:
    """Build the required deferred residuals for a formal style candidate."""
    style_id = style_family.value
    return (
        Residual(
            name=f"formal_style_not_meaning/{style_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"FormalStyleCandidate({style_id}) is formal style "
                f"classification, not meaning — FORMAL_STYLE ≠ meaning"
            ),
        ),
        Residual(
            name=f"DALALAH_DEFERRED_TO_PR_D1/{style_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"Dalālah for {style_id} is not licensed here — "
                f"deferred to PR-D1 (Mufrad Semantic Slot Geometry)."
            ),
        ),
        Residual(
            name=f"MUFRAD_SEMANTIC_SLOT_GEOMETRY_DEFERRED_TO_PR_D1/{style_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"Semantic slot geometry for {style_id} is not licensed "
                f"here — deferred to PR-D1."
            ),
        ),
        Residual(
            name=f"IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE/{style_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"Whether {style_id} produces ifadah is not licensed "
                f"here — deferred until mufrad dalalah closure."
            ),
        ),
        Residual(
            name=f"MANTUQ_DEFERRED_UNTIL_IFADAH/{style_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"Mantuq for {style_id} is not licensed here — "
                f"deferred until ifadah."
            ),
        ),
        Residual(
            name=f"MAFHUM_DEFERRED_UNTIL_MANTUQ/{style_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"Mafhum for {style_id} is not licensed here — "
                f"deferred until mantuq."
            ),
        ),
        Residual(
            name=f"MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT/{style_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"Majaz for {style_id} is not licensed here — "
                f"deferred until haqiqah attempt."
            ),
        ),
        Residual(
            name=f"MANQUL_DEFERRED_UNTIL_TRANSFER_GATE/{style_id}",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=(
                f"Manqul for {style_id} is not licensed here — "
                f"deferred until transfer gate."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# prove_formal_style_candidate() — the classification operation
# ---------------------------------------------------------------------------


def prove_formal_style_candidate(
    style_family: FormalStyleFamily,
    composition_evidence_ref: str,
    formal_closure_state: FormalShapeClosureState,
    formal_closure_ref: str,
) -> FormalStyleVerdict:
    """Prove a formal style candidate classification (docs/35).

    This is a **pure function**: it accepts values and returns a value.
    It does not write to a ledger, does not perform I/O, and does not
    call external services.

    Parameters
    ----------
    style_family : FormalStyleFamily
        The formal style family to classify.
    composition_evidence_ref : str
        Reference to the composition pattern evidence that supports
        this classification.
    formal_closure_state : FormalShapeClosureState
        Must be CLOSED — PR-F8 requires FormalShapeClosure.CLOSED.
    formal_closure_ref : str
        Reference to the formal shape closure proof.

    Returns
    -------
    FormalStyleVerdict
        PROVEN with a FormalStyleCandidate on success; REFUSED with a
        named FailureCode on any violation.
    """
    # --- Input boundary: style_family ---
    if not isinstance(style_family, FormalStyleFamily):
        return FormalStyleVerdict(
            candidate=None,
            verdict_state=FormalStyleState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_formal_style_candidate/refused/style_family_invalid",
        )

    # --- Input boundary: composition_evidence_ref ---
    if (
        not isinstance(composition_evidence_ref, str)
        or not composition_evidence_ref.strip()
    ):
        return FormalStyleVerdict(
            candidate=None,
            verdict_state=FormalStyleState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_formal_style_candidate/refused/composition_evidence_ref_empty",
        )

    # --- Input boundary: formal_closure_state must be CLOSED ---
    if not isinstance(formal_closure_state, FormalShapeClosureState):
        return FormalStyleVerdict(
            candidate=None,
            verdict_state=FormalStyleState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_formal_style_candidate/refused/closure_state_invalid_type",
        )
    if formal_closure_state is not FormalShapeClosureState.CLOSED:
        return FormalStyleVerdict(
            candidate=None,
            verdict_state=FormalStyleState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_formal_style_candidate/refused/closure_not_closed",
        )

    # --- Input boundary: formal_closure_ref ---
    if (
        not isinstance(formal_closure_ref, str)
        or not formal_closure_ref.strip()
    ):
        return FormalStyleVerdict(
            candidate=None,
            verdict_state=FormalStyleState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_formal_style_candidate/refused/formal_closure_ref_empty",
        )

    # --- Rank bounding via lattice meet ---
    candidate_rank = RankLattice.meet(
        Rank.CANDIDATE,
        FORMAL_SHAPE_RANK_CEILING,
    )

    # --- Build deferred residuals ---
    residuals = _build_deferred_residuals(style_family)

    # --- Check residuals for HIDDEN_FORBIDDEN or BLOCKING ---
    _refused_kinds = (ResidualKind.HIDDEN_FORBIDDEN, ResidualKind.BLOCKING)
    for r in residuals:
        if r.kind in _refused_kinds:
            return FormalStyleVerdict(
                candidate=None,
                verdict_state=FormalStyleState.REFUSED,
                failure_code=FailureCode.HIDDEN_RESIDUAL,
                verdict_rank=Rank.ZERO,
                residuals=residuals,
                trace_ref="prove_formal_style_candidate/refused/blocking_residual",
            )

    # --- Look up canonical style definition ---
    style_def = FORMAL_STYLE_DEFINITIONS[style_family]

    # --- Construct the FormalStyleCandidate ---
    candidate = FormalStyleCandidate(
        style_family=style_family,
        composition_evidence_ref=composition_evidence_ref,
        formal_closure_ref=formal_closure_ref,
        definition_text=str(style_def["definition_text"]),
        distinguishing_evidence=str(style_def["distinguishing_evidence"]),
        boundary_conditions=tuple(str(bc) for bc in style_def["boundary_conditions"]),  # type: ignore[union-attr]
        exclusion_conditions=tuple(str(ec) for ec in style_def["exclusion_conditions"]),  # type: ignore[union-attr]
        rank=candidate_rank,
        residuals=residuals,
        trace_ref=(
            f"prove_formal_style_candidate/proven/{style_family.value}"
        ),
    )

    return FormalStyleVerdict(
        candidate=candidate,
        verdict_state=FormalStyleState.PROVEN,
        failure_code=None,
        verdict_rank=candidate_rank,
        residuals=residuals,
        trace_ref=(
            f"prove_formal_style_candidate/proven/{style_family.value}"
        ),
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------

__all__ = [
    "FORMAL_STYLE_DEFINITIONS",
    "FORMAL_STYLE_FAMILIES",
    "FormalStyleCandidate",
    "FormalStyleFamily",
    "FormalStyleState",
    "FormalStyleVerdict",
    "prove_formal_style_candidate",
]
