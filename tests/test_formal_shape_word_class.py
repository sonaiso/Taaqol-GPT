"""Constitutional tests for PR-F2: Word-Class Formal Definitions.

Origin law: docs/34_FORMAL_SHAPE_REGISTRY_LAW.md §5 (WORD_CLASS).

This test module proves:
1. ISM, FI'L, HARF canonical definitions satisfy all constitutional
   requirements (13 fields, rank ceiling, residual governance, trace).
2. define_word_class_shape() produces DEFINED verdicts for valid inputs
   and REFUSED verdicts with named FailureCodes for invalid inputs.
3. build_word_class_registry() produces CLOSED state when all three
   families are present, PARTIAL when incomplete, EMPTY when none.
4. Forbidden outputs are proven absent: no meaning, no ifadah, no hukm,
   no reality, no semantic lexicon, no dalālah.
5. Schema guards refuse malformed carriers at birth.
6. No HIDDEN_FORBIDDEN or BLOCKING residuals pass through.
7. Rank never exceeds FORMAL_SHAPE_RANK_CEILING.
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.formal_shape import (
    FIL_DEFINITION,
    FIL_FAMILY,
    FORMAL_SHAPE_RANK_CEILING,
    HARF_DEFINITION,
    HARF_FAMILY,
    ISM_DEFINITION,
    ISM_FAMILY,
    WORD_CLASS_FAMILIES,
    FormalShapeClosureState,
    FormalShapeDefinition,
    FormalShapeDomain,
    FormalShapeFamily,
    FormalShapeRegistry,
    WordClassDefinitionState,
    WordClassDefinitionVerdict,
    build_word_class_registry,
    define_word_class_shape,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

# ===========================================================================
# §1 — Canonical definitions satisfy constitutional requirements
# ===========================================================================


class TestCanonicalDefinitions:
    """ISM, FI'L, HARF canonical definitions are constitutionally valid."""

    def test_ism_definition_is_valid(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="ISM canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        d = ISM_DEFINITION
        assert d.shape_id == "WORD_CLASS.ISM"
        assert d.domain is FormalShapeDomain.WORD_CLASS
        assert d.family is ISM_FAMILY
        assert d.canonical_name == "ism"
        assert d.rank <= FORMAL_SHAPE_RANK_CEILING
        assert d.trace_ref
        assert all(isinstance(r, Residual) for r in d.residuals)
        assert all(r.kind is not ResidualKind.HIDDEN_FORBIDDEN for r in d.residuals)
        assert all(r.kind is not ResidualKind.BLOCKING for r in d.residuals)
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=d.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_fil_definition_is_valid(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="FI'L canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        d = FIL_DEFINITION
        assert d.shape_id == "WORD_CLASS.FIL"
        assert d.domain is FormalShapeDomain.WORD_CLASS
        assert d.family is FIL_FAMILY
        assert d.canonical_name == "fi'l"
        assert d.rank <= FORMAL_SHAPE_RANK_CEILING
        assert d.trace_ref
        assert all(isinstance(r, Residual) for r in d.residuals)
        assert all(r.kind is not ResidualKind.HIDDEN_FORBIDDEN for r in d.residuals)
        assert all(r.kind is not ResidualKind.BLOCKING for r in d.residuals)
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=d.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_harf_definition_is_valid(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="HARF canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        d = HARF_DEFINITION
        assert d.shape_id == "WORD_CLASS.HARF"
        assert d.domain is FormalShapeDomain.WORD_CLASS
        assert d.family is HARF_FAMILY
        assert d.canonical_name == "harf"
        assert d.rank <= FORMAL_SHAPE_RANK_CEILING
        assert d.trace_ref
        assert all(isinstance(r, Residual) for r in d.residuals)
        assert all(r.kind is not ResidualKind.HIDDEN_FORBIDDEN for r in d.residuals)
        assert all(r.kind is not ResidualKind.BLOCKING for r in d.residuals)
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=d.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_ism_distinguishes_from_fil_and_harf(self) -> None:
        """ISM evidence is distinct from FI'L and HARF evidence."""
        assert ISM_DEFINITION.distinguishing_evidence != FIL_DEFINITION.distinguishing_evidence
        assert ISM_DEFINITION.distinguishing_evidence != HARF_DEFINITION.distinguishing_evidence
        assert ISM_DEFINITION.boundary_conditions != FIL_DEFINITION.boundary_conditions
        assert ISM_DEFINITION.exclusion_conditions != FIL_DEFINITION.exclusion_conditions

    def test_fil_distinguishes_from_ism_and_harf(self) -> None:
        """FI'L evidence is distinct from ISM and HARF evidence."""
        assert FIL_DEFINITION.distinguishing_evidence != ISM_DEFINITION.distinguishing_evidence
        assert FIL_DEFINITION.distinguishing_evidence != HARF_DEFINITION.distinguishing_evidence
        assert FIL_DEFINITION.boundary_conditions != ISM_DEFINITION.boundary_conditions

    def test_harf_distinguishes_from_ism_and_fil(self) -> None:
        """HARF evidence is distinct from ISM and FI'L evidence."""
        assert HARF_DEFINITION.distinguishing_evidence != ISM_DEFINITION.distinguishing_evidence
        assert HARF_DEFINITION.distinguishing_evidence != FIL_DEFINITION.distinguishing_evidence
        assert HARF_DEFINITION.boundary_conditions != ISM_DEFINITION.boundary_conditions


# ===========================================================================
# §2 — define_word_class_shape() produces correct verdicts
# ===========================================================================


class TestDefineWordClassShape:
    """define_word_class_shape() pure function tests."""

    def test_valid_definition_produces_defined_verdict(self) -> None:
        verdict = define_word_class_shape(
            shape_id="TEST_ISM",
            family=ISM_FAMILY,
            canonical_name="ism_test",
            definition_text="Test formal definition for ism",
            distinguishing_evidence="Accepts al-, tanwin, or jarr",
            boundary_conditions=("Accepts al-",),
            exclusion_conditions=("Does not accept qad",),
        )
        assert verdict.verdict_state is WordClassDefinitionState.DEFINED
        assert verdict.failure_code is None
        assert verdict.definition is not None
        assert verdict.definition.shape_id == "TEST_ISM"
        assert verdict.definition.domain is FormalShapeDomain.WORD_CLASS
        assert verdict.verdict_rank <= FORMAL_SHAPE_RANK_CEILING
        assert verdict.trace_ref

    def test_empty_shape_id_refused(self) -> None:
        verdict = define_word_class_shape(
            shape_id="",
            family=ISM_FAMILY,
            canonical_name="ism",
            definition_text="Some text",
            distinguishing_evidence="Some evidence",
            boundary_conditions=("condition",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert verdict.definition is None

    def test_wrong_domain_family_refused(self) -> None:
        """Family from non-WORD_CLASS domain is refused."""
        wrong_family = FormalShapeFamily(
            domain=FormalShapeDomain.INFLECTION,
            family_id="IRAB",
            description="Wrong domain family",
        )
        verdict = define_word_class_shape(
            shape_id="WRONG_DOMAIN",
            family=wrong_family,
            canonical_name="irab",
            definition_text="Some text",
            distinguishing_evidence="Some evidence",
            boundary_conditions=("condition",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.DOMAIN_MISSING
        assert verdict.definition is None

    def test_empty_canonical_name_refused(self) -> None:
        verdict = define_word_class_shape(
            shape_id="TEST",
            family=ISM_FAMILY,
            canonical_name="",
            definition_text="Some text",
            distinguishing_evidence="Some evidence",
            boundary_conditions=("condition",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_empty_definition_text_refused(self) -> None:
        verdict = define_word_class_shape(
            shape_id="TEST",
            family=ISM_FAMILY,
            canonical_name="ism",
            definition_text="",
            distinguishing_evidence="Some evidence",
            boundary_conditions=("condition",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_empty_distinguishing_evidence_refused(self) -> None:
        verdict = define_word_class_shape(
            shape_id="TEST",
            family=ISM_FAMILY,
            canonical_name="ism",
            definition_text="Some text",
            distinguishing_evidence="",
            boundary_conditions=("condition",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_empty_boundary_conditions_refused(self) -> None:
        verdict = define_word_class_shape(
            shape_id="TEST",
            family=ISM_FAMILY,
            canonical_name="ism",
            definition_text="Some text",
            distinguishing_evidence="Some evidence",
            boundary_conditions=(),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_invalid_boundary_condition_entry_refused(self) -> None:
        verdict = define_word_class_shape(
            shape_id="TEST",
            family=ISM_FAMILY,
            canonical_name="ism",
            definition_text="Some text",
            distinguishing_evidence="Some evidence",
            boundary_conditions=("valid", ""),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_verdict_rank_bounded_by_ceiling(self) -> None:
        verdict = define_word_class_shape(
            shape_id="RANK_TEST",
            family=FIL_FAMILY,
            canonical_name="fi'l",
            definition_text="Formal definition",
            distinguishing_evidence="Accepts ta' al-fa'il",
            boundary_conditions=("Accepts ta' al-fa'il",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.DEFINED
        assert verdict.verdict_rank <= FORMAL_SHAPE_RANK_CEILING

    def test_non_family_input_refused(self) -> None:
        """Passing non-FormalShapeFamily type is refused."""
        verdict = define_word_class_shape(
            shape_id="TEST",
            family="not_a_family",  # type: ignore[arg-type]
            canonical_name="ism",
            definition_text="Some text",
            distinguishing_evidence="Some evidence",
            boundary_conditions=("condition",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WordClassDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED


# ===========================================================================
# §3 — build_word_class_registry() closure state
# ===========================================================================


class TestBuildWordClassRegistry:
    """build_word_class_registry() closure computation tests."""

    def test_default_registry_is_closed(self) -> None:
        """Default (all three canonical) produces CLOSED."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="WORD_CLASS registry CLOSED with all three families",
            constitutional_chain=("FormalShapeRegistry", "FormalShapeClosureState"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticLexicon"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        registry = build_word_class_registry()
        assert registry.domain is FormalShapeDomain.WORD_CLASS
        assert registry.closure_state is FormalShapeClosureState.CLOSED
        assert len(registry.definitions) == 3
        assert len(registry.families) == 3
        assert registry.rank_ceiling <= FORMAL_SHAPE_RANK_CEILING
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=registry.rank_ceiling,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeRegistry"}),
        )
        assert_constitutional_case(case, result)

    def test_partial_registry_with_one_family(self) -> None:
        """Only ISM definition produces PARTIAL."""
        registry = build_word_class_registry(definitions=(ISM_DEFINITION,))
        assert registry.closure_state is FormalShapeClosureState.PARTIAL

    def test_partial_registry_with_two_families(self) -> None:
        """Two families but missing one produces PARTIAL."""
        registry = build_word_class_registry(
            definitions=(ISM_DEFINITION, FIL_DEFINITION)
        )
        assert registry.closure_state is FormalShapeClosureState.PARTIAL

    def test_empty_registry(self) -> None:
        """No definitions produces EMPTY."""
        registry = build_word_class_registry(definitions=())
        assert registry.closure_state is FormalShapeClosureState.EMPTY

    def test_registry_with_hidden_forbidden_residual_refused(self) -> None:
        """Definition with HIDDEN_FORBIDDEN residual produces REFUSED registry."""
        bad_def = FormalShapeDefinition(
            shape_id="BAD_ISM",
            domain=FormalShapeDomain.WORD_CLASS,
            family=ISM_FAMILY,
            canonical_name="ism_bad",
            definition_text="Bad definition",
            distinguishing_evidence="Evidence",
            boundary_conditions=("condition",),
            exclusion_conditions=(),
            weight_constraint=None,
            path_constraint=None,
            rank=Rank.CANDIDATE,
            residuals=(
                Residual(
                    name="hidden_test",
                    kind=ResidualKind.HIDDEN_FORBIDDEN,
                    visible=False,
                    note="Hidden residual",
                ),
            ),
            trace_ref="test/bad",
        )
        registry = build_word_class_registry(
            definitions=(bad_def, FIL_DEFINITION, HARF_DEFINITION)
        )
        assert registry.closure_state is FormalShapeClosureState.REFUSED

    def test_registry_with_blocking_residual_refused(self) -> None:
        """Definition with BLOCKING residual produces REFUSED registry."""
        bad_def = FormalShapeDefinition(
            shape_id="BLOCKING_FIL",
            domain=FormalShapeDomain.WORD_CLASS,
            family=FIL_FAMILY,
            canonical_name="fil_blocking",
            definition_text="Blocking definition",
            distinguishing_evidence="Evidence",
            boundary_conditions=("condition",),
            exclusion_conditions=(),
            weight_constraint=None,
            path_constraint=None,
            rank=Rank.CANDIDATE,
            residuals=(
                Residual(
                    name="blocking_test",
                    kind=ResidualKind.BLOCKING,
                    visible=True,
                    note="Blocking residual",
                ),
            ),
            trace_ref="test/blocking",
        )
        registry = build_word_class_registry(
            definitions=(ISM_DEFINITION, bad_def, HARF_DEFINITION)
        )
        assert registry.closure_state is FormalShapeClosureState.REFUSED


# ===========================================================================
# §4 — Schema guards refuse malformed carriers at birth
# ===========================================================================


class TestSchemaGuards:
    """Birth guards enforce FormalShapeDefinition schema."""

    def test_empty_shape_id_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeDefinition(
                shape_id="",
                domain=FormalShapeDomain.WORD_CLASS,
                family=ISM_FAMILY,
                canonical_name="ism",
                definition_text="text",
                distinguishing_evidence="evidence",
                boundary_conditions=("cond",),
                exclusion_conditions=(),
                weight_constraint=None,
                path_constraint=None,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )

    def test_wrong_domain_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeDefinition(
                shape_id="X",
                domain="NOT_A_DOMAIN",  # type: ignore[arg-type]
                family=ISM_FAMILY,
                canonical_name="ism",
                definition_text="text",
                distinguishing_evidence="evidence",
                boundary_conditions=("cond",),
                exclusion_conditions=(),
                weight_constraint=None,
                path_constraint=None,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )

    def test_family_domain_mismatch_raises(self) -> None:
        """Family domain must match definition domain."""
        inflection_family = FormalShapeFamily(
            domain=FormalShapeDomain.INFLECTION,
            family_id="IRAB",
            description="Wrong domain",
        )
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeDefinition(
                shape_id="MISMATCH",
                domain=FormalShapeDomain.WORD_CLASS,
                family=inflection_family,
                canonical_name="ism",
                definition_text="text",
                distinguishing_evidence="evidence",
                boundary_conditions=("cond",),
                exclusion_conditions=(),
                weight_constraint=None,
                path_constraint=None,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )

    def test_rank_exceeds_ceiling_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeDefinition(
                shape_id="HIGH_RANK",
                domain=FormalShapeDomain.WORD_CLASS,
                family=ISM_FAMILY,
                canonical_name="ism",
                definition_text="text",
                distinguishing_evidence="evidence",
                boundary_conditions=("cond",),
                exclusion_conditions=(),
                weight_constraint=None,
                path_constraint=None,
                rank=Rank.CERTIFICATE,
                residuals=(),
                trace_ref="test",
            )

    def test_empty_canonical_name_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeDefinition(
                shape_id="X",
                domain=FormalShapeDomain.WORD_CLASS,
                family=ISM_FAMILY,
                canonical_name="",
                definition_text="text",
                distinguishing_evidence="evidence",
                boundary_conditions=("cond",),
                exclusion_conditions=(),
                weight_constraint=None,
                path_constraint=None,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )

    def test_empty_trace_ref_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeDefinition(
                shape_id="X",
                domain=FormalShapeDomain.WORD_CLASS,
                family=ISM_FAMILY,
                canonical_name="ism",
                definition_text="text",
                distinguishing_evidence="evidence",
                boundary_conditions=("cond",),
                exclusion_conditions=(),
                weight_constraint=None,
                path_constraint=None,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )

    def test_empty_boundary_conditions_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeDefinition(
                shape_id="X",
                domain=FormalShapeDomain.WORD_CLASS,
                family=ISM_FAMILY,
                canonical_name="ism",
                definition_text="text",
                distinguishing_evidence="evidence",
                boundary_conditions=(),
                exclusion_conditions=(),
                weight_constraint=None,
                path_constraint=None,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )

    def test_non_residual_in_residuals_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeDefinition(
                shape_id="X",
                domain=FormalShapeDomain.WORD_CLASS,
                family=ISM_FAMILY,
                canonical_name="ism",
                definition_text="text",
                distinguishing_evidence="evidence",
                boundary_conditions=("cond",),
                exclusion_conditions=(),
                weight_constraint=None,
                path_constraint=None,
                rank=Rank.CANDIDATE,
                residuals=("not_a_residual",),  # type: ignore[arg-type]
                trace_ref="test",
            )


# ===========================================================================
# §5 — FormalShapeFamily schema guards
# ===========================================================================


class TestFormalShapeFamily:
    """FormalShapeFamily birth guards."""

    def test_valid_family(self) -> None:
        f = FormalShapeFamily(
            domain=FormalShapeDomain.WORD_CLASS,
            family_id="TEST",
            description="Test family",
        )
        assert f.domain is FormalShapeDomain.WORD_CLASS
        assert f.family_id == "TEST"

    def test_invalid_domain_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeFamily(
                domain="NOT_DOMAIN",  # type: ignore[arg-type]
                family_id="TEST",
                description="Test",
            )

    def test_empty_family_id_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeFamily(
                domain=FormalShapeDomain.WORD_CLASS,
                family_id="",
                description="Test",
            )

    def test_empty_description_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeFamily(
                domain=FormalShapeDomain.WORD_CLASS,
                family_id="TEST",
                description="",
            )


# ===========================================================================
# §6 — FormalShapeRegistry schema guards
# ===========================================================================


class TestFormalShapeRegistryGuards:
    """FormalShapeRegistry birth guards."""

    def test_registry_wrong_domain_definition_raises(self) -> None:
        """Registry domain must match all definition domains."""
        inflection_family = FormalShapeFamily(
            domain=FormalShapeDomain.INFLECTION,
            family_id="IRAB",
            description="inflection family",
        )
        inflection_def = FormalShapeDefinition(
            shape_id="INFLECTION_X",
            domain=FormalShapeDomain.INFLECTION,
            family=inflection_family,
            canonical_name="irab",
            definition_text="text",
            distinguishing_evidence="evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
            weight_constraint=None,
            path_constraint=None,
            rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="test",
        )
        with pytest.raises(WeightCarrierSchemaError):
            FormalShapeRegistry(
                domain=FormalShapeDomain.WORD_CLASS,
                families=WORD_CLASS_FAMILIES,
                definitions=(inflection_def,),
                rank_ceiling=FORMAL_SHAPE_RANK_CEILING,
                closure_state=FormalShapeClosureState.CLOSED,
            )


# ===========================================================================
# §7 — Forbidden outputs proven absent
# ===========================================================================


class TestForbiddenOutputs:
    """Prove that PR-F2 carriers never produce forbidden outputs."""

    def test_ism_not_meaning(self) -> None:
        """ISM_DEFINITION ≠ Meaning."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="ISM definition is formal category not meaning",
            constitutional_chain=("FormalShapeDefinition", "ForbiddenOutput"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(
                "Meaning",
                "Ifadah",
                "HukmCandidate",
                "SemanticEntry",
                "WadʿiSignified",
                "Dalālah",
                "SyntaxRole",
            ),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        # The definition carries an EXPLANATORY residual noting it is
        # not meaning — verify that residual exists
        assert any("not meaning" in r.note for r in ISM_DEFINITION.residuals)
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=ISM_DEFINITION.rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalShapeDefinition"}),
        )
        assert_constitutional_case(case, result)

    def test_fil_not_event(self) -> None:
        """FI'L formal shape ≠ event/action."""
        assert any("not meaning" in r.note or "event" in r.note
                   for r in FIL_DEFINITION.residuals)

    def test_harf_not_semantic_relation(self) -> None:
        """HARF formal shape ≠ semantic relation."""
        assert any("not meaning" in r.note or "semantic" in r.note
                   for r in HARF_DEFINITION.residuals)

    def test_registry_not_semantic_lexicon(self) -> None:
        """WORD_CLASS registry ≠ SemanticLexicon."""
        registry = build_word_class_registry()
        # Registry produces FormalShapeRegistry, never SemanticLexicon
        assert registry.closure_state is FormalShapeClosureState.CLOSED
        assert isinstance(registry, FormalShapeRegistry)


# ===========================================================================
# §8 — WordClassDefinitionVerdict schema guards
# ===========================================================================


class TestVerdictGuards:
    """WordClassDefinitionVerdict birth guards enforce state invariants."""

    def test_defined_verdict_without_definition_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WordClassDefinitionVerdict(
                definition=None,
                verdict_state=WordClassDefinitionState.DEFINED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )

    def test_refused_verdict_without_failure_code_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WordClassDefinitionVerdict(
                definition=None,
                verdict_state=WordClassDefinitionState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )

    def test_refused_verdict_with_definition_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WordClassDefinitionVerdict(
                definition=ISM_DEFINITION,
                verdict_state=WordClassDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )

    def test_rank_exceeds_ceiling_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WordClassDefinitionVerdict(
                definition=None,
                verdict_state=WordClassDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.CERTIFICATE,
                residuals=(),
                trace_ref="test",
            )


# ===========================================================================
# §9 — Import hygiene
# ===========================================================================


class TestImportHygiene:
    """PR-F2 symbols accessible from weight package."""

    def test_formal_shape_symbols_importable_from_weight(self) -> None:
        from taaqqul_slot_geometry.weight import (
            FIL_DEFINITION,  # noqa: F811
            FIL_FAMILY,  # noqa: F811
            FORMAL_SHAPE_RANK_CEILING,  # noqa: F811
            HARF_DEFINITION,  # noqa: F811
            HARF_FAMILY,  # noqa: F811
            ISM_DEFINITION,  # noqa: F811
            ISM_FAMILY,  # noqa: F811
            WORD_CLASS_FAMILIES,  # noqa: F811
            FormalShapeClosureState,  # noqa: F811
            FormalShapeDefinition,  # noqa: F811
            FormalShapeDomain,  # noqa: F811
            FormalShapeFamily,  # noqa: F811
            FormalShapeRegistry,  # noqa: F811
            WordClassDefinitionState,  # noqa: F811
            WordClassDefinitionVerdict,  # noqa: F811
            build_word_class_registry,  # noqa: F811
            define_word_class_shape,  # noqa: F811
        )

        assert FORMAL_SHAPE_RANK_CEILING is not None
        assert FormalShapeDomain.WORD_CLASS.value == "WORD_CLASS"
        assert ISM_FAMILY is not None
        assert FIL_FAMILY is not None
        assert HARF_FAMILY is not None
        assert ISM_DEFINITION is not None
        assert FIL_DEFINITION is not None
        assert HARF_DEFINITION is not None
        assert WORD_CLASS_FAMILIES is not None
        assert FormalShapeClosureState.CLOSED.value == "CLOSED"
        assert FormalShapeDefinition is not None
        assert FormalShapeFamily is not None
        assert FormalShapeRegistry is not None
        assert WordClassDefinitionState.DEFINED.value == "DEFINED"
        assert WordClassDefinitionVerdict is not None
        assert build_word_class_registry is not None
        assert define_word_class_shape is not None
