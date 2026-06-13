"""Constitutional tests for PR-F7: Composition Pattern Formal Definitions.

Origin law: docs/34_FORMAL_SHAPE_REGISTRY_LAW.md §10 (COMPOSITION_PATTERN).

This test module proves:
1. All 6 COMPOSITION_PATTERN canonical definitions satisfy constitutional
   requirements (13 fields, rank ceiling, residual governance, trace).
2. define_composition_pattern_shape() produces DEFINED/REFUSED verdicts.
3. build_composition_pattern_registry() produces CLOSED/PARTIAL/EMPTY states.
4. Forbidden outputs proven absent: no meaning, no ifadah, no hukm,
   no reality, no proposition, no event assertion.
5. Constitutional invariants hold: NOMINAL_SENTENCE ≠ proposition, etc.
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
from taaqqul_slot_geometry.weight.formal_shape_composition import (
    ATIF_DEFINITION,
    ATIF_FAMILY,
    BADAL_DEFINITION,
    BADAL_FAMILY,
    COMPOSITION_PATTERN_FAMILIES,
    IDAFA_DEFINITION,
    IDAFA_FAMILY,
    NOMINAL_SENTENCE_DEFINITION,
    NOMINAL_SENTENCE_FAMILY,
    SIFA_MAWSUF_DEFINITION,
    SIFA_MAWSUF_FAMILY,
    VERBAL_SENTENCE_DEFINITION,
    VERBAL_SENTENCE_FAMILY,
    CompositionPatternDefinitionState,
    CompositionPatternDefinitionVerdict,
    build_composition_pattern_registry,
    define_composition_pattern_shape,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

# All 6 canonical definitions for parametrized tests.
ALL_CANONICAL_DEFINITIONS = (
    NOMINAL_SENTENCE_DEFINITION,
    VERBAL_SENTENCE_DEFINITION,
    IDAFA_DEFINITION,
    SIFA_MAWSUF_DEFINITION,
    ATIF_DEFINITION,
    BADAL_DEFINITION,
)

# All 6 families.
ALL_FAMILIES = (
    NOMINAL_SENTENCE_FAMILY,
    VERBAL_SENTENCE_FAMILY,
    IDAFA_FAMILY,
    SIFA_MAWSUF_FAMILY,
    ATIF_FAMILY,
    BADAL_FAMILY,
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
# Test 1: All 6 canonical definitions are valid
# ===========================================================================


class TestAllCanonicalCompositionPatternDefinitionsValid:
    """All 6 COMPOSITION_PATTERN canonical definitions satisfy constitutional fields."""

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
        assert defn.domain is FormalShapeDomain.COMPOSITION_PATTERN
        assert isinstance(defn.family, FormalShapeFamily)
        assert defn.family.domain is FormalShapeDomain.COMPOSITION_PATTERN
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
# Test 2: define_composition_pattern_shape() produces correct verdicts
# ===========================================================================


class TestDefineCompositionPatternShape:
    """define_composition_pattern_shape() produces DEFINED/REFUSED verdicts."""

    def test_valid_definition_returns_defined(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="define_composition_pattern_shape returns DEFINED for valid input",
            constitutional_chain=(
                "define_composition_pattern_shape", "Verdict", "Rank", "Trace",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        verdict = define_composition_pattern_shape(
            shape_id="COMPOSITION_PATTERN.TEST_NOMINAL",
            family=NOMINAL_SENTENCE_FAMILY,
            canonical_name="jumlah ismiyyah test",
            definition_text=(
                "A test formal composition pattern with topic + predicate "
                "slots arranged structurally."
            ),
            distinguishing_evidence="Topic-initial structure with raf' by ibtida'.",
            boundary_conditions=("Topic slot present in initial position",),
            exclusion_conditions=("Does not assert proposition",),
        )
        assert verdict.verdict_state is CompositionPatternDefinitionState.DEFINED
        assert verdict.failure_code is None
        assert verdict.definition is not None
        assert verdict.definition.domain is FormalShapeDomain.COMPOSITION_PATTERN
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
            branch_name="define_composition_pattern_shape refuses empty shape_id",
            constitutional_chain=("define_composition_pattern_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_composition_pattern_shape(
            shape_id="",
            family=NOMINAL_SENTENCE_FAMILY,
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is CompositionPatternDefinitionState.REFUSED
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
            branch_name="define_composition_pattern_shape refuses wrong-domain family",
            constitutional_chain=("define_composition_pattern_shape", "Refusal"),
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
        verdict = define_composition_pattern_shape(
            shape_id="COMPOSITION_PATTERN.WRONG",
            family=wrong_family,
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is CompositionPatternDefinitionState.REFUSED
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
            branch_name="define_composition_pattern_shape refuses non-FormalShapeFamily",
            constitutional_chain=("define_composition_pattern_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_composition_pattern_shape(
            shape_id="COMPOSITION_PATTERN.BAD",
            family="not a family",  # type: ignore[arg-type]
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is CompositionPatternDefinitionState.REFUSED
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
            branch_name="define_composition_pattern_shape refuses empty boundary_conditions",
            constitutional_chain=("define_composition_pattern_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_composition_pattern_shape(
            shape_id="COMPOSITION_PATTERN.EMPTY_BC",
            family=NOMINAL_SENTENCE_FAMILY,
            canonical_name="test",
            definition_text="test text",
            distinguishing_evidence="test evidence",
            boundary_conditions=(),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is CompositionPatternDefinitionState.REFUSED
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
# Test 3: build_composition_pattern_registry() produces correct closure states
# ===========================================================================


class TestBuildCompositionPatternRegistry:
    """build_composition_pattern_registry() produces CLOSED/PARTIAL/EMPTY/REFUSED."""

    def test_all_canonical_gives_closed(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="build_composition_pattern_registry CLOSED with all 6 canonical",
            constitutional_chain=("build_composition_pattern_registry", "Closure", "Rank"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        registry = build_composition_pattern_registry()
        assert registry.domain is FormalShapeDomain.COMPOSITION_PATTERN
        assert registry.closure_state is FormalShapeClosureState.CLOSED
        assert len(registry.definitions) == 6
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
        registry = build_composition_pattern_registry(
            definitions=(NOMINAL_SENTENCE_DEFINITION, VERBAL_SENTENCE_DEFINITION)
        )
        assert registry.closure_state is FormalShapeClosureState.PARTIAL
        assert len(registry.definitions) == 2

    def test_empty_definitions_gives_empty(self) -> None:
        """Empty when no definitions provided."""
        registry = build_composition_pattern_registry(definitions=())
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
            definition_text="Wrong domain definition text here",
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
        registry = build_composition_pattern_registry(definitions=(wrong_domain_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED

    def test_hidden_forbidden_residual_gives_refused(self) -> None:
        """Refused on HIDDEN_FORBIDDEN residual."""
        bad_defn = FormalShapeDefinition(
            shape_id="COMPOSITION_PATTERN.BAD",
            domain=FormalShapeDomain.COMPOSITION_PATTERN,
            family=NOMINAL_SENTENCE_FAMILY,
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
        registry = build_composition_pattern_registry(definitions=(bad_defn,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED


# ===========================================================================
# Test 4: Constitutional invariants — composition pattern ≠ meaning
# ===========================================================================


class TestCompositionPatternConstitutionalInvariants:
    """Proves forbidden outputs are absent from all definitions."""

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_definition_does_not_assert_proposition(
        self, defn: FormalShapeDefinition
    ) -> None:
        """No definition_text asserts a proposition or truth value."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} does not assert proposition or truth",
            constitutional_chain=("FormalShapeDefinition", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Proposition", "TruthValue"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        text = defn.definition_text.lower()
        # Must not positively assert propositions or truth
        assert "is a proposition" not in text
        assert "asserts truth" not in text
        assert "is true" not in text
        assert "is false" not in text
        assert "produces ifadah" not in text
        assert "completes a proposition" not in text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_nominal_sentence_not_proposition(self) -> None:
        """NOMINAL_SENTENCE ≠ proposition."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="NOMINAL_SENTENCE does not assert proposition",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Proposition",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = NOMINAL_SENTENCE_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "proposition" in exclusions or "ifadah" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_verbal_sentence_not_event(self) -> None:
        """VERBAL_SENTENCE ≠ event assertion."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="VERBAL_SENTENCE does not assert event occurrence",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("EventAssertion",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = VERBAL_SENTENCE_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "event occurrence" in exclusions or "event" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_idafa_not_ownership(self) -> None:
        """IDAFA ≠ ownership."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="IDAFA does not assert ownership",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = IDAFA_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "ownership" in exclusions or "possession" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_sifa_mawsuf_not_attribute_judgment(self) -> None:
        """SIFA_MAWSUF ≠ attribute judgment."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="SIFA_MAWSUF does not assert attribute judgment",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = SIFA_MAWSUF_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "attribute" in exclusions or "quality" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_atif_not_semantic_coordination(self) -> None:
        """ATIF ≠ semantic coordination."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="ATIF does not assert semantic coordination",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = ATIF_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "equivalence" in exclusions or "shared properties" in exclusions
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
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_semantic_dalalah_deferred_residual_present(
        self, defn: FormalShapeDefinition
    ) -> None:
        """All definitions must have SEMANTIC_DALALAH_DEFERRED."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} has SEMANTIC_DALALAH_DEFERRED residual",
            constitutional_chain=("FormalShapeDefinition", "Residual", "Deferred"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("SemanticDalalah",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        residual_names = [r.name for r in defn.residuals]
        has_deferred = any(
            "SEMANTIC_DALALAH_DEFERRED" in name for name in residual_names
        )
        assert has_deferred, (
            f"{defn.shape_id} must have a SEMANTIC_DALALAH_DEFERRED residual"
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

    def test_nominal_sentence_has_ifadah_deferred(self) -> None:
        """NOMINAL_SENTENCE must have IFADAH_DEFERRED_TO_PR_20."""
        defn = NOMINAL_SENTENCE_DEFINITION
        residual_names = [r.name for r in defn.residuals]
        has_ifadah = any("IFADAH_DEFERRED_TO_PR_20" in name for name in residual_names)
        assert has_ifadah

    def test_verbal_sentence_has_ifadah_deferred(self) -> None:
        """VERBAL_SENTENCE must have IFADAH_DEFERRED_TO_PR_20."""
        defn = VERBAL_SENTENCE_DEFINITION
        residual_names = [r.name for r in defn.residuals]
        has_ifadah = any("IFADAH_DEFERRED_TO_PR_20" in name for name in residual_names)
        assert has_ifadah


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


class TestCompositionPatternVerdictSchemaGuard:
    """CompositionPatternDefinitionVerdict refuses malformed carriers at birth."""

    def test_wrong_verdict_state_type_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            CompositionPatternDefinitionVerdict(
                definition=None,
                verdict_state="DEFINED",  # type: ignore[arg-type]
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_rank_exceeds_ceiling_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            CompositionPatternDefinitionVerdict(
                definition=None,
                verdict_state=CompositionPatternDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.LICENSED,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_defined_without_definition_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            CompositionPatternDefinitionVerdict(
                definition=None,
                verdict_state=CompositionPatternDefinitionState.DEFINED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_refused_without_failure_code_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            CompositionPatternDefinitionVerdict(
                definition=None,
                verdict_state=CompositionPatternDefinitionState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_empty_trace_ref_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            CompositionPatternDefinitionVerdict(
                definition=None,
                verdict_state=CompositionPatternDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# Test 8: COMPOSITION_PATTERN_FAMILIES completeness
# ===========================================================================


class TestCompositionPatternFamiliesCompleteness:
    """COMPOSITION_PATTERN_FAMILIES has exactly 6 families."""

    def test_exactly_6_families(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="COMPOSITION_PATTERN_FAMILIES has exactly 6 families",
            constitutional_chain=("COMPOSITION_PATTERN_FAMILIES", "Completeness"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(),
            max_rank=Rank.CANDIDATE,
            required_trace=False,
            required_residual_visibility=False,
        )
        assert len(COMPOSITION_PATTERN_FAMILIES) == 6
        # All must belong to COMPOSITION_PATTERN domain
        for f in COMPOSITION_PATTERN_FAMILIES:
            assert f.domain is FormalShapeDomain.COMPOSITION_PATTERN
        # All must have unique family_ids
        ids = [f.family_id for f in COMPOSITION_PATTERN_FAMILIES]
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
            branch_name="Each COMPOSITION_PATTERN family has one canonical definition",
            constitutional_chain=("COMPOSITION_PATTERN_FAMILIES", "Definition", "Coverage"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(),
            max_rank=Rank.CANDIDATE,
            required_trace=False,
            required_residual_visibility=False,
        )
        family_ids_from_families = {f.family_id for f in COMPOSITION_PATTERN_FAMILIES}
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
