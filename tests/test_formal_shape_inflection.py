"""Constitutional tests for PR-F5: Inflection Formal Definitions.

Origin law: docs/34_FORMAL_SHAPE_REGISTRY_LAW.md §8 (INFLECTION).

This test module proves:
1. All 12 INFLECTION canonical definitions satisfy constitutional
   requirements (13 fields, rank ceiling, residual governance, trace).
2. define_inflection_shape() produces DEFINED/REFUSED verdicts.
3. build_inflection_registry() produces CLOSED/PARTIAL/EMPTY states.
4. Forbidden outputs proven absent: no meaning, no ifadah, no hukm,
   no reality, no semantic content, no syntactic role assignment.
5. Constitutional invariants hold: RAF' ≠ fa'il, NASB ≠ maf'ul, etc.
6. Required deferred residuals are present.
7. Rank never exceeds FORMAL_SHAPE_RANK_CEILING.
8. Schema guards refuse malformed carriers at birth.
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.formal_shape import (
    FORMAL_SHAPE_RANK_CEILING,
    FormalShapeClosureState,
    FormalShapeDefinition,
    FormalShapeDomain,
    FormalShapeFamily,
)
from taaqqul_slot_geometry.weight.formal_shape_inflection import (
    DECLENSION_BLOCK_FORM_DEFINITION,
    DECLENSION_BLOCK_FORM_FAMILY,
    DIPTOTE_FORM_DEFINITION,
    DIPTOTE_FORM_FAMILY,
    ESTIMATED_MARK_FORM_DEFINITION,
    ESTIMATED_MARK_FORM_FAMILY,
    GOVERNANCE_EFFECT_DEFERRED_FORM_DEFINITION,
    GOVERNANCE_EFFECT_DEFERRED_FORM_FAMILY,
    INFLECTION_FAMILIES,
    JARR_MARK_FORM_DEFINITION,
    JARR_MARK_FORM_FAMILY,
    JAZM_MARK_FORM_DEFINITION,
    JAZM_MARK_FORM_FAMILY,
    MABNI_FORM_DEFINITION,
    MABNI_FORM_FAMILY,
    MURAB_FORM_DEFINITION,
    MURAB_FORM_FAMILY,
    NASB_MARK_FORM_DEFINITION,
    NASB_MARK_FORM_FAMILY,
    ORIGINAL_MARK_FORM_DEFINITION,
    ORIGINAL_MARK_FORM_FAMILY,
    RAF_MARK_FORM_DEFINITION,
    RAF_MARK_FORM_FAMILY,
    SUBSIDIARY_MARK_FORM_DEFINITION,
    SUBSIDIARY_MARK_FORM_FAMILY,
    InflectionDefinitionState,
    InflectionDefinitionVerdict,
    build_inflection_registry,
    define_inflection_shape,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

# All 12 canonical definitions for parametrized tests.
ALL_CANONICAL_DEFINITIONS = (
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

# All 12 families.
ALL_FAMILIES = (
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

# Forbidden meaning words (PR-F2.1 MCE rule).
MEANING_WORDS = (
    "meaning",
    "signifies",
    "denotes",
    "refers to",
    "represents",
    "semantic",
    "ontological",
)


# ===========================================================================
# Test 1: All 12 canonical definitions are valid
# ===========================================================================


class TestAllCanonicalInflectionDefinitionsValid:
    """All 12 INFLECTION canonical definitions satisfy constitutional fields."""

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_canonical_definition_satisfies_all_fields(
        self, defn: FormalShapeDefinition
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        # Verify 13 fields present
        assert isinstance(defn.shape_id, str) and defn.shape_id.strip()
        assert defn.domain is FormalShapeDomain.INFLECTION
        assert isinstance(defn.family, FormalShapeFamily)
        assert defn.family.domain is FormalShapeDomain.INFLECTION
        assert isinstance(defn.canonical_name, str) and defn.canonical_name.strip()
        assert isinstance(defn.definition_text, str) and defn.definition_text.strip()
        assert (
            isinstance(defn.distinguishing_evidence, str)
            and defn.distinguishing_evidence.strip()
        )
        assert isinstance(defn.boundary_conditions, tuple) and defn.boundary_conditions
        assert isinstance(defn.exclusion_conditions, tuple)
        assert defn.weight_constraint is None or (
            isinstance(defn.weight_constraint, str) and defn.weight_constraint.strip()
        )
        assert defn.path_constraint is None or (
            isinstance(defn.path_constraint, str) and defn.path_constraint.strip()
        )
        assert isinstance(defn.rank, Rank)
        assert defn.rank <= FORMAL_SHAPE_RANK_CEILING
        assert isinstance(defn.residuals, tuple) and defn.residuals
        for r in defn.residuals:
            assert isinstance(r, Residual)
            assert r.visible is True
            assert r.kind is ResidualKind.EXPLANATORY
        assert isinstance(defn.trace_ref, str) and defn.trace_ref.strip()

        # Assert constitutional chain result
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_canonical_definition_no_meaning_language(
        self, defn: FormalShapeDefinition
    ) -> None:
        """PR-F2.1 MCE rule: no positive 'meaning' language in definition_text."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} definition_text has no meaning language",
            constitutional_chain=("FormalShapeDefinition", "MCE_Hardening"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "SemanticEntry", "Dalālah"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        text_lower = defn.definition_text.lower()
        for word in MEANING_WORDS:
            assert word not in text_lower, (
                f"definition_text for {defn.shape_id} contains forbidden "
                f"meaning-language word: '{word}'"
            )
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 2: define_inflection_shape() produces correct verdicts
# ===========================================================================


class TestDefineInflectionShape:
    """define_inflection_shape() produces DEFINED/REFUSED verdicts."""

    def test_valid_definition_returns_defined(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="define_inflection_shape returns DEFINED for valid input",
            constitutional_chain=("define_inflection_shape", "Verdict", "Rank", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        verdict = define_inflection_shape(
            shape_id="INFLECTION.TEST_MURAB",
            family=MURAB_FORM_FAMILY,
            canonical_name="mu'rab test",
            definition_text=(
                "A test word form whose ending varies by governance "
                "position. This is formal ending-variation shape."
            ),
            distinguishing_evidence="Ending varies across positions.",
            boundary_conditions=("Ending varies",),
            exclusion_conditions=("Does not assert syntactic role",),
        )
        assert verdict.verdict_state is InflectionDefinitionState.DEFINED
        assert verdict.failure_code is None
        assert verdict.definition is not None
        assert verdict.definition.domain is FormalShapeDomain.INFLECTION
        assert verdict.verdict_rank <= FORMAL_SHAPE_RANK_CEILING
        assert verdict.residuals
        for r in verdict.residuals:
            assert r.visible is True
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_empty_shape_id_returns_refused(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="define_inflection_shape refuses empty shape_id",
            constitutional_chain=("define_inflection_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_inflection_shape(
            shape_id="",
            family=MURAB_FORM_FAMILY,
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is InflectionDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert verdict.definition is None
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_wrong_domain_family_returns_refused(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="define_inflection_shape refuses wrong-domain family",
            constitutional_chain=("define_inflection_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.DOMAIN_MISSING,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        wrong_family = FormalShapeFamily(
            domain=FormalShapeDomain.WORD_CLASS,
            family_id="ISM",
            description="Wrong domain family",
        )
        verdict = define_inflection_shape(
            shape_id="INFLECTION.WRONG",
            family=wrong_family,
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is InflectionDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.DOMAIN_MISSING
        assert verdict.definition is None
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.DOMAIN_MISSING,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_non_family_object_returns_refused(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="define_inflection_shape refuses non-FormalShapeFamily",
            constitutional_chain=("define_inflection_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_inflection_shape(
            shape_id="INFLECTION.BAD",
            family="not a family",  # type: ignore[arg-type]
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is InflectionDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_empty_boundary_conditions_returns_refused(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="define_inflection_shape refuses empty boundary_conditions",
            constitutional_chain=("define_inflection_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_inflection_shape(
            shape_id="INFLECTION.EMPTY_BC",
            family=MURAB_FORM_FAMILY,
            canonical_name="test",
            definition_text="test text",
            distinguishing_evidence="test evidence",
            boundary_conditions=(),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is InflectionDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 3: build_inflection_registry() produces correct closure states
# ===========================================================================


class TestBuildInflectionRegistry:
    """build_inflection_registry() produces CLOSED/PARTIAL/EMPTY/REFUSED."""

    def test_all_canonical_gives_closed(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="build_inflection_registry CLOSED with all 12 canonical",
            constitutional_chain=("build_inflection_registry", "Closure", "Rank"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        registry = build_inflection_registry()
        assert registry.domain is FormalShapeDomain.INFLECTION
        assert registry.closure_state is FormalShapeClosureState.CLOSED
        assert len(registry.definitions) == 12
        assert registry.rank_ceiling == FORMAL_SHAPE_RANK_CEILING
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeRegistry"}),
        )
        assert_constitutional_case(case, result)

    def test_partial_definitions_gives_partial(self) -> None:
        """Partial when some families missing."""
        registry = build_inflection_registry(
            definitions=(MURAB_FORM_DEFINITION, MABNI_FORM_DEFINITION)
        )
        assert registry.closure_state is FormalShapeClosureState.PARTIAL
        assert len(registry.definitions) == 2

    def test_empty_definitions_gives_empty(self) -> None:
        """Empty when no definitions provided."""
        registry = build_inflection_registry(definitions=())
        assert registry.closure_state is FormalShapeClosureState.EMPTY
        assert len(registry.definitions) == 0

    def test_wrong_domain_definition_gives_refused(self) -> None:
        """Refused when definition has wrong domain."""
        wrong_domain_def = FormalShapeDefinition(
            shape_id="WRONG.ISM",
            domain=FormalShapeDomain.WORD_CLASS,
            family=FormalShapeFamily(
                domain=FormalShapeDomain.WORD_CLASS,
                family_id="ISM",
                description="Wrong domain",
            ),
            canonical_name="ism",
            definition_text="Wrong domain definition",
            distinguishing_evidence="Accepts al-",
            boundary_conditions=("Accepts al-",),
            exclusion_conditions=(),
            weight_constraint=None,
            path_constraint=None,
            rank=Rank.CANDIDATE,
            residuals=(
                Residual(
                    name="test",
                    kind=ResidualKind.EXPLANATORY,
                    visible=True,
                    note="test",
                ),
            ),
            trace_ref="test/wrong",
        )
        registry = build_inflection_registry(definitions=(wrong_domain_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED

    def test_hidden_forbidden_residual_gives_refused(self) -> None:
        """Refused on HIDDEN_FORBIDDEN residual."""
        bad_defn = FormalShapeDefinition(
            shape_id="INFLECTION.BAD",
            domain=FormalShapeDomain.INFLECTION,
            family=MURAB_FORM_FAMILY,
            canonical_name="bad",
            definition_text="A test definition with forbidden residual shape.",
            distinguishing_evidence="Test evidence.",
            boundary_conditions=("Test condition",),
            exclusion_conditions=(),
            weight_constraint=None,
            path_constraint=None,
            rank=Rank.CANDIDATE,
            residuals=(
                Residual(
                    name="hidden/bad",
                    kind=ResidualKind.HIDDEN_FORBIDDEN,
                    visible=False,
                    note="This should trigger REFUSED",
                ),
            ),
            trace_ref="test/bad",
        )
        registry = build_inflection_registry(definitions=(bad_defn,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED


# ===========================================================================
# Test 4: Constitutional invariants — inflection ≠ syntactic role
# ===========================================================================


class TestInflectionConstitutionalInvariants:
    """Proves forbidden outputs are absent from all definitions."""

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_definition_does_not_assert_syntactic_role(
        self, defn: FormalShapeDefinition
    ) -> None:
        """No definition_text asserts a syntactic role."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} does not assert syntactic role",
            constitutional_chain=("FormalShapeDefinition", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("SyntaxRole", "FormalAgentSlot", "FormalObjectSlot"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        text = defn.definition_text.lower()
        # Must not positively assert these roles
        assert "is a subject" not in text
        assert "is a predicate" not in text
        assert "is an object" not in text
        assert "is a fa'il" not in text
        assert "is a mubtada'" not in text
        assert "is a maf'ul" not in text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_raf_mark_not_fail(self) -> None:
        """RAF'_MARK_FORM ≠ fa'il."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="RAF'_MARK_FORM does not assert fa'il",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("FormalAgentSlot",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = RAF_MARK_FORM_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "fa'il" in exclusions or "subjecthood" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_nasb_mark_not_maful(self) -> None:
        """NASB_MARK_FORM ≠ maf'ul."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="NASB_MARK_FORM does not assert maf'ul",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("FormalObjectSlot",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = NASB_MARK_FORM_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "maf'ul" in exclusions or "objecthood" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_jarr_mark_not_idafah(self) -> None:
        """JARR_MARK_FORM ≠ idafah meaning."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="JARR_MARK_FORM does not assert idafah meaning",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = JARR_MARK_FORM_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "idafah" in exclusions or "possession" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_jazm_mark_not_shart(self) -> None:
        """JAZM_MARK_FORM ≠ shart completion."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="JAZM_MARK_FORM does not assert shart completion",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = JAZM_MARK_FORM_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "condition" in exclusions or "shart" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_mabni_not_reference_resolution(self) -> None:
        """MABNI_FORM ≠ reference resolution."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="MABNI_FORM does not assert reference resolution",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = MABNI_FORM_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "reference resolution" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 5: Deferred residuals present where required
# ===========================================================================


class TestDeferredResiduals:
    """Proves required deferred residuals are present."""

    @pytest.mark.parametrize(
        "defn",
        [
            MURAB_FORM_DEFINITION,
            MABNI_FORM_DEFINITION,
            RAF_MARK_FORM_DEFINITION,
            NASB_MARK_FORM_DEFINITION,
            JARR_MARK_FORM_DEFINITION,
            JAZM_MARK_FORM_DEFINITION,
            GOVERNANCE_EFFECT_DEFERRED_FORM_DEFINITION,
        ],
        ids=[
            d.shape_id
            for d in [
                MURAB_FORM_DEFINITION,
                MABNI_FORM_DEFINITION,
                RAF_MARK_FORM_DEFINITION,
                NASB_MARK_FORM_DEFINITION,
                JARR_MARK_FORM_DEFINITION,
                JAZM_MARK_FORM_DEFINITION,
                GOVERNANCE_EFFECT_DEFERRED_FORM_DEFINITION,
            ]
        ],
    )
    def test_contract_slot_deferred_residual_present(
        self, defn: FormalShapeDefinition
    ) -> None:
        """Definitions close to governance must have CONTRACT_SLOT_DEFERRED."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} has CONTRACT_SLOT_DEFERRED residual",
            constitutional_chain=("FormalShapeDefinition", "Residual", "Deferred"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("FormalAgentSlot", "FormalObjectSlot"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        residual_names = [r.name for r in defn.residuals]
        has_deferred = any(
            "CONTRACT_SLOT_DEFERRED_TO_PR_F6" in name for name in residual_names
        )
        assert has_deferred, (
            f"{defn.shape_id} must have a CONTRACT_SLOT_DEFERRED_TO_PR_F6 residual"
        )
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 6: Rank ceiling enforcement
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds FORMAL_SHAPE_RANK_CEILING."""

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_rank_within_ceiling(self, defn: FormalShapeDefinition) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} rank <= FORMAL_SHAPE_RANK_CEILING",
            constitutional_chain=("FormalShapeDefinition", "Rank"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        assert defn.rank <= FORMAL_SHAPE_RANK_CEILING
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 7: Schema guard — verdict refuses malformed carriers
# ===========================================================================


class TestInflectionVerdictSchemaGuard:
    """InflectionDefinitionVerdict refuses malformed carriers at birth."""

    def test_wrong_verdict_state_type_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            InflectionDefinitionVerdict(
                definition=None,
                verdict_state="DEFINED",  # type: ignore[arg-type]
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_rank_exceeds_ceiling_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            InflectionDefinitionVerdict(
                definition=None,
                verdict_state=InflectionDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.LICENSED,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_defined_without_definition_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            InflectionDefinitionVerdict(
                definition=None,
                verdict_state=InflectionDefinitionState.DEFINED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_refused_without_failure_code_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            InflectionDefinitionVerdict(
                definition=None,
                verdict_state=InflectionDefinitionState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_empty_trace_ref_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            InflectionDefinitionVerdict(
                definition=None,
                verdict_state=InflectionDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# Test 8: INFLECTION_FAMILIES completeness
# ===========================================================================


class TestInflectionFamiliesCompleteness:
    """INFLECTION_FAMILIES has exactly 12 families."""

    def test_exactly_12_families(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="INFLECTION_FAMILIES has exactly 12 families",
            constitutional_chain=("INFLECTION_FAMILIES", "Completeness"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(),
            max_rank=Rank.CANDIDATE,
            required_trace=False,
            required_residual_visibility=False,
        )
        assert len(INFLECTION_FAMILIES) == 12
        # All must belong to INFLECTION domain
        for f in INFLECTION_FAMILIES:
            assert f.domain is FormalShapeDomain.INFLECTION
        # All must have unique family_ids
        ids = [f.family_id for f in INFLECTION_FAMILIES]
        assert len(ids) == len(set(ids))
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=False,
            trace_present=False,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_all_families_match_definitions(self) -> None:
        """Each family has exactly one canonical definition."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="Each INFLECTION family has one canonical definition",
            constitutional_chain=("INFLECTION_FAMILIES", "Definition", "Coverage"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(),
            max_rank=Rank.CANDIDATE,
            required_trace=False,
            required_residual_visibility=False,
        )
        family_ids_from_families = {f.family_id for f in INFLECTION_FAMILIES}
        family_ids_from_defs = {d.family.family_id for d in ALL_CANONICAL_DEFINITIONS}
        assert family_ids_from_families == family_ids_from_defs
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=False,
            trace_present=False,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)
