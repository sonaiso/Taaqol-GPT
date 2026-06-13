"""Constitutional tests for PR-F6: Contract Slot Formal Definitions.

Origin law: docs/34_FORMAL_SHAPE_REGISTRY_LAW.md §9 (CONTRACT_SLOT).

This test module proves:
1. All 8 CONTRACT_SLOT canonical definitions satisfy constitutional
   requirements (13 fields, rank ceiling, residual governance, trace).
2. define_contract_slot_shape() produces DEFINED/REFUSED verdicts.
3. build_contract_slot_registry() produces CLOSED/PARTIAL/EMPTY states.
4. Forbidden outputs proven absent: no meaning, no ifadah, no hukm,
   no reality, no semantic content, no real agency/patienthood.
5. Constitutional invariants hold: FORMAL_SUBJECT ≠ real agent, etc.
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
from taaqqul_slot_geometry.weight.formal_shape_contract_slot import (
    CONTRACT_SLOT_FAMILIES,
    FORMAL_GENITIVE_SLOT_DEFINITION,
    FORMAL_GENITIVE_SLOT_FAMILY,
    FORMAL_OBJECT_SLOT_DEFINITION,
    FORMAL_OBJECT_SLOT_FAMILY,
    FORMAL_PREDICATE_SLOT_DEFINITION,
    FORMAL_PREDICATE_SLOT_FAMILY,
    FORMAL_QUALIFIER_SLOT_DEFINITION,
    FORMAL_QUALIFIER_SLOT_FAMILY,
    FORMAL_SPECIFICATION_SLOT_DEFINITION,
    FORMAL_SPECIFICATION_SLOT_FAMILY,
    FORMAL_STATE_SLOT_DEFINITION,
    FORMAL_STATE_SLOT_FAMILY,
    FORMAL_SUBJECT_SLOT_DEFINITION,
    FORMAL_SUBJECT_SLOT_FAMILY,
    FORMAL_TOPIC_SLOT_DEFINITION,
    FORMAL_TOPIC_SLOT_FAMILY,
    ContractSlotDefinitionState,
    ContractSlotDefinitionVerdict,
    build_contract_slot_registry,
    define_contract_slot_shape,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

# All 8 canonical definitions for parametrized tests.
ALL_CANONICAL_DEFINITIONS = (
    FORMAL_SUBJECT_SLOT_DEFINITION,
    FORMAL_TOPIC_SLOT_DEFINITION,
    FORMAL_PREDICATE_SLOT_DEFINITION,
    FORMAL_OBJECT_SLOT_DEFINITION,
    FORMAL_GENITIVE_SLOT_DEFINITION,
    FORMAL_QUALIFIER_SLOT_DEFINITION,
    FORMAL_STATE_SLOT_DEFINITION,
    FORMAL_SPECIFICATION_SLOT_DEFINITION,
)

# All 8 families.
ALL_FAMILIES = (
    FORMAL_SUBJECT_SLOT_FAMILY,
    FORMAL_TOPIC_SLOT_FAMILY,
    FORMAL_PREDICATE_SLOT_FAMILY,
    FORMAL_OBJECT_SLOT_FAMILY,
    FORMAL_GENITIVE_SLOT_FAMILY,
    FORMAL_QUALIFIER_SLOT_FAMILY,
    FORMAL_STATE_SLOT_FAMILY,
    FORMAL_SPECIFICATION_SLOT_FAMILY,
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
# Test 1: All 8 canonical definitions are valid
# ===========================================================================


class TestAllCanonicalContractSlotDefinitionsValid:
    """All 8 CONTRACT_SLOT canonical definitions satisfy constitutional fields."""

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
        assert defn.domain is FormalShapeDomain.CONTRACT_SLOT
        assert isinstance(defn.family, FormalShapeFamily)
        assert defn.family.domain is FormalShapeDomain.CONTRACT_SLOT
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
# Test 2: define_contract_slot_shape() produces correct verdicts
# ===========================================================================


class TestDefineContractSlotShape:
    """define_contract_slot_shape() produces DEFINED/REFUSED verdicts."""

    def test_valid_definition_returns_defined(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="define_contract_slot_shape returns DEFINED for valid input",
            constitutional_chain=("define_contract_slot_shape", "Verdict", "Rank", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        verdict = define_contract_slot_shape(
            shape_id="CONTRACT_SLOT.TEST_SUBJECT",
            family=FORMAL_SUBJECT_SLOT_FAMILY,
            canonical_name="fa'il test",
            definition_text=(
                "A test formal structural position proved by raf' "
                "governance. This is governance-position shape."
            ),
            distinguishing_evidence="Raf' governed by verbal element.",
            boundary_conditions=("Carries raf' mark",),
            exclusion_conditions=("Does not assert real agency",),
        )
        assert verdict.verdict_state is ContractSlotDefinitionState.DEFINED
        assert verdict.failure_code is None
        assert verdict.definition is not None
        assert verdict.definition.domain is FormalShapeDomain.CONTRACT_SLOT
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
            branch_name="define_contract_slot_shape refuses empty shape_id",
            constitutional_chain=("define_contract_slot_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_contract_slot_shape(
            shape_id="",
            family=FORMAL_SUBJECT_SLOT_FAMILY,
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is ContractSlotDefinitionState.REFUSED
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
            branch_name="define_contract_slot_shape refuses wrong-domain family",
            constitutional_chain=("define_contract_slot_shape", "Refusal"),
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
        verdict = define_contract_slot_shape(
            shape_id="CONTRACT_SLOT.WRONG",
            family=wrong_family,
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is ContractSlotDefinitionState.REFUSED
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
            branch_name="define_contract_slot_shape refuses non-FormalShapeFamily",
            constitutional_chain=("define_contract_slot_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_contract_slot_shape(
            shape_id="CONTRACT_SLOT.BAD",
            family="not a family",  # type: ignore[arg-type]
            canonical_name="test",
            definition_text="test",
            distinguishing_evidence="test",
            boundary_conditions=("test",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is ContractSlotDefinitionState.REFUSED
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
            branch_name="define_contract_slot_shape refuses empty boundary_conditions",
            constitutional_chain=("define_contract_slot_shape", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = define_contract_slot_shape(
            shape_id="CONTRACT_SLOT.EMPTY_BC",
            family=FORMAL_SUBJECT_SLOT_FAMILY,
            canonical_name="test",
            definition_text="test text",
            distinguishing_evidence="test evidence",
            boundary_conditions=(),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is ContractSlotDefinitionState.REFUSED
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
# Test 3: build_contract_slot_registry() produces correct closure states
# ===========================================================================


class TestBuildContractSlotRegistry:
    """build_contract_slot_registry() produces CLOSED/PARTIAL/EMPTY/REFUSED."""

    def test_all_canonical_gives_closed(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="build_contract_slot_registry CLOSED with all 8 canonical",
            constitutional_chain=("build_contract_slot_registry", "Closure", "Rank"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        registry = build_contract_slot_registry()
        assert registry.domain is FormalShapeDomain.CONTRACT_SLOT
        assert registry.closure_state is FormalShapeClosureState.CLOSED
        assert len(registry.definitions) == 8
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
        registry = build_contract_slot_registry(
            definitions=(FORMAL_SUBJECT_SLOT_DEFINITION, FORMAL_OBJECT_SLOT_DEFINITION)
        )
        assert registry.closure_state is FormalShapeClosureState.PARTIAL
        assert len(registry.definitions) == 2

    def test_empty_definitions_gives_empty(self) -> None:
        """Empty when no definitions provided."""
        registry = build_contract_slot_registry(definitions=())
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
        registry = build_contract_slot_registry(definitions=(wrong_domain_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED

    def test_hidden_forbidden_residual_gives_refused(self) -> None:
        """Refused on HIDDEN_FORBIDDEN residual."""
        bad_defn = FormalShapeDefinition(
            shape_id="CONTRACT_SLOT.BAD",
            domain=FormalShapeDomain.CONTRACT_SLOT,
            family=FORMAL_SUBJECT_SLOT_FAMILY,
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
        registry = build_contract_slot_registry(definitions=(bad_defn,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED


# ===========================================================================
# Test 4: Constitutional invariants — contract slot ≠ semantic role
# ===========================================================================


class TestContractSlotConstitutionalInvariants:
    """Proves forbidden outputs are absent from all definitions."""

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_definition_does_not_assert_real_role(
        self, defn: FormalShapeDefinition
    ) -> None:
        """No definition_text asserts a real semantic role."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} does not assert real semantic role",
            constitutional_chain=("FormalShapeDefinition", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "RealAgent", "RealPatient"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        text = defn.definition_text.lower()
        # Must not positively assert real roles
        assert "is a real agent" not in text
        assert "is a real patient" not in text
        assert "is a real subject" not in text
        assert "performs the action" not in text
        assert "receives the action" not in text
        assert "is the doer" not in text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_formal_subject_not_real_agent(self) -> None:
        """FORMAL_SUBJECT_SLOT ≠ real agent."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="FORMAL_SUBJECT_SLOT does not assert real agency",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("RealAgent",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_SUBJECT_SLOT_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "real agency" in exclusions or "fa'il haqiqi" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_formal_object_not_real_patient(self) -> None:
        """FORMAL_OBJECT_SLOT ≠ real patient."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="FORMAL_OBJECT_SLOT does not assert real patienthood",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("RealPatient",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_OBJECT_SLOT_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "real patienthood" in exclusions or "maf'ul haqiqi" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_formal_topic_not_proposition_subject(self) -> None:
        """FORMAL_TOPIC_SLOT ≠ proposition subject in meaning."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="FORMAL_TOPIC_SLOT does not assert proposition subject",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_TOPIC_SLOT_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "proposition subject" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_formal_predicate_not_ifadah(self) -> None:
        """FORMAL_PREDICATE_SLOT ≠ ifadah."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="FORMAL_PREDICATE_SLOT does not assert ifadah",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Ifadah",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_PREDICATE_SLOT_DEFINITION
        exclusions = " ".join(defn.exclusion_conditions).lower()
        assert "proposition completion" in exclusions or "ifadah" in exclusions
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=defn.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_formal_genitive_not_possession(self) -> None:
        """FORMAL_GENITIVE_SLOT ≠ ownership/possession meaning."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="FORMAL_GENITIVE_SLOT does not assert possession meaning",
            constitutional_chain=("FormalShapeDefinition", "Invariant", "Exclusion"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_GENITIVE_SLOT_DEFINITION
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
    def test_composition_pattern_deferred_residual_present(
        self, defn: FormalShapeDefinition
    ) -> None:
        """All definitions must have COMPOSITION_PATTERN_DEFERRED_TO_PR_F7."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name=f"{defn.shape_id} has COMPOSITION_PATTERN_DEFERRED residual",
            constitutional_chain=("FormalShapeDefinition", "Residual", "Deferred"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("CompositionPattern",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        residual_names = [r.name for r in defn.residuals]
        has_deferred = any(
            "COMPOSITION_PATTERN_DEFERRED_TO_PR_F7" in name for name in residual_names
        )
        assert has_deferred, (
            f"{defn.shape_id} must have a COMPOSITION_PATTERN_DEFERRED_TO_PR_F7 residual"
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


class TestContractSlotVerdictSchemaGuard:
    """ContractSlotDefinitionVerdict refuses malformed carriers at birth."""

    def test_wrong_verdict_state_type_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            ContractSlotDefinitionVerdict(
                definition=None,
                verdict_state="DEFINED",  # type: ignore[arg-type]
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_rank_exceeds_ceiling_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            ContractSlotDefinitionVerdict(
                definition=None,
                verdict_state=ContractSlotDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.LICENSED,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_defined_without_definition_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            ContractSlotDefinitionVerdict(
                definition=None,
                verdict_state=ContractSlotDefinitionState.DEFINED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_refused_without_failure_code_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            ContractSlotDefinitionVerdict(
                definition=None,
                verdict_state=ContractSlotDefinitionState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/guard",
            )

    def test_empty_trace_ref_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            ContractSlotDefinitionVerdict(
                definition=None,
                verdict_state=ContractSlotDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# Test 8: CONTRACT_SLOT_FAMILIES completeness
# ===========================================================================


class TestContractSlotFamiliesCompleteness:
    """CONTRACT_SLOT_FAMILIES has exactly 8 families."""

    def test_exactly_8_families(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="CONTRACT_SLOT_FAMILIES has exactly 8 families",
            constitutional_chain=("CONTRACT_SLOT_FAMILIES", "Completeness"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(),
            max_rank=Rank.CANDIDATE,
            required_trace=False,
            required_residual_visibility=False,
        )
        assert len(CONTRACT_SLOT_FAMILIES) == 8
        # All must belong to CONTRACT_SLOT domain
        for f in CONTRACT_SLOT_FAMILIES:
            assert f.domain is FormalShapeDomain.CONTRACT_SLOT
        # All must have unique family_ids
        ids = [f.family_id for f in CONTRACT_SLOT_FAMILIES]
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
            branch_name="Each CONTRACT_SLOT family has one canonical definition",
            constitutional_chain=("CONTRACT_SLOT_FAMILIES", "Definition", "Coverage"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(),
            max_rank=Rank.CANDIDATE,
            required_trace=False,
            required_residual_visibility=False,
        )
        family_ids_from_families = {f.family_id for f in CONTRACT_SLOT_FAMILIES}
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
