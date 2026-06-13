"""Constitutional tests for PR-F3: Built and Reference Formal Definitions.

Origin law: docs/34_FORMAL_SHAPE_REGISTRY_LAW.md §6 (BUILT_REFERENCE).

This test module proves:
1. PERSONAL_PRONOUN, DEMONSTRATIVE, RELATIVE_PRONOUN, INTERROGATIVE,
   CONDITIONAL canonical definitions satisfy all constitutional
   requirements (13 fields, rank ceiling, residual governance, trace).
2. define_built_reference_shape() produces DEFINED verdicts for valid
   inputs and REFUSED verdicts with named FailureCodes for invalid inputs.
3. build_built_reference_registry() produces CLOSED state when all five
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
    FORMAL_SHAPE_RANK_CEILING,
    FormalShapeClosureState,
    FormalShapeDefinition,
    FormalShapeDomain,
    FormalShapeFamily,
)
from taaqqul_slot_geometry.weight.formal_shape_built_reference import (
    BUILT_REFERENCE_FAMILIES,
    CONDITIONAL_DEFINITION,
    CONDITIONAL_FAMILY,
    DEMONSTRATIVE_DEFINITION,
    DEMONSTRATIVE_FAMILY,
    INTERROGATIVE_DEFINITION,
    INTERROGATIVE_FAMILY,
    PERSONAL_PRONOUN_DEFINITION,
    PERSONAL_PRONOUN_FAMILY,
    RELATIVE_PRONOUN_DEFINITION,
    RELATIVE_PRONOUN_FAMILY,
    BuiltReferenceDefinitionState,
    BuiltReferenceDefinitionVerdict,
    build_built_reference_registry,
    define_built_reference_shape,
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
    """All 5 BUILT_REFERENCE canonical definitions are constitutionally valid."""

    def test_personal_pronoun_definition_is_valid(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="PERSONAL_PRONOUN canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        d = PERSONAL_PRONOUN_DEFINITION
        assert d.shape_id == "BUILT_REFERENCE.PERSONAL_PRONOUN"
        assert d.domain is FormalShapeDomain.BUILT_REFERENCE
        assert d.family is PERSONAL_PRONOUN_FAMILY
        assert d.canonical_name == "damir"
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

    def test_demonstrative_definition_is_valid(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="DEMONSTRATIVE canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        d = DEMONSTRATIVE_DEFINITION
        assert d.shape_id == "BUILT_REFERENCE.DEMONSTRATIVE"
        assert d.domain is FormalShapeDomain.BUILT_REFERENCE
        assert d.family is DEMONSTRATIVE_FAMILY
        assert d.canonical_name == "ism isharah"
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

    def test_relative_pronoun_definition_is_valid(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="RELATIVE_PRONOUN canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        d = RELATIVE_PRONOUN_DEFINITION
        assert d.shape_id == "BUILT_REFERENCE.RELATIVE_PRONOUN"
        assert d.domain is FormalShapeDomain.BUILT_REFERENCE
        assert d.family is RELATIVE_PRONOUN_FAMILY
        assert d.canonical_name == "ism mawsul"
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

    def test_interrogative_definition_is_valid(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="INTERROGATIVE canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        d = INTERROGATIVE_DEFINITION
        assert d.shape_id == "BUILT_REFERENCE.INTERROGATIVE"
        assert d.domain is FormalShapeDomain.BUILT_REFERENCE
        assert d.family is INTERROGATIVE_FAMILY
        assert d.canonical_name == "ism istifham"
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

    def test_conditional_definition_is_valid(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="CONDITIONAL canonical definition satisfies all fields",
            constitutional_chain=("FormalShapeDefinition", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        d = CONDITIONAL_DEFINITION
        assert d.shape_id == "BUILT_REFERENCE.CONDITIONAL"
        assert d.domain is FormalShapeDomain.BUILT_REFERENCE
        assert d.family is CONDITIONAL_FAMILY
        assert d.canonical_name == "adah shart"
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

    def test_all_definitions_mutually_distinct(self) -> None:
        """All 5 definitions have distinct shape_ids and evidence."""
        defs = (
            PERSONAL_PRONOUN_DEFINITION,
            DEMONSTRATIVE_DEFINITION,
            RELATIVE_PRONOUN_DEFINITION,
            INTERROGATIVE_DEFINITION,
            CONDITIONAL_DEFINITION,
        )
        shape_ids = [d.shape_id for d in defs]
        assert len(set(shape_ids)) == 5
        evidences = [d.distinguishing_evidence for d in defs]
        assert len(set(evidences)) == 5


# ===========================================================================
# §2 — define_built_reference_shape() produces correct verdicts
# ===========================================================================


class TestDefineBuiltReferenceShape:
    """define_built_reference_shape() pure function tests."""

    def test_valid_definition_produces_defined_verdict(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST_PRONOUN",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir_test",
            definition_text="Test formal definition for pronoun",
            distinguishing_evidence="Fixed pattern with pronominal substitution",
            boundary_conditions=("Morphologically built (mabni)",),
            exclusion_conditions=("Does not accept al-",),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.DEFINED
        assert verdict.failure_code is None
        assert verdict.definition is not None
        assert verdict.definition.shape_id == "TEST_PRONOUN"
        assert verdict.definition.domain is FormalShapeDomain.BUILT_REFERENCE
        assert verdict.verdict_rank <= FORMAL_SHAPE_RANK_CEILING
        assert verdict.trace_ref

    def test_empty_shape_id_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir",
            definition_text="Test",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert verdict.definition is None

    def test_wrong_domain_family_refused(self) -> None:
        word_class_family = FormalShapeFamily(
            domain=FormalShapeDomain.WORD_CLASS,
            family_id="ISM",
            description="Wrong domain family",
        )
        verdict = define_built_reference_shape(
            shape_id="WRONG_DOMAIN",
            family=word_class_family,
            canonical_name="test",
            definition_text="Test definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.DOMAIN_MISSING
        assert verdict.definition is None

    def test_empty_canonical_name_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="",
            definition_text="Test",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_empty_definition_text_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir",
            definition_text="",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_empty_distinguishing_evidence_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir",
            definition_text="Test definition",
            distinguishing_evidence="",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_empty_boundary_conditions_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir",
            definition_text="Test definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=(),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_non_tuple_boundary_conditions_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir",
            definition_text="Test definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=["cond"],  # type: ignore[arg-type]
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_non_family_type_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family="not_a_family",  # type: ignore[arg-type]
            canonical_name="damir",
            definition_text="Test definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_invalid_boundary_condition_item_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir",
            definition_text="Test definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("valid", ""),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_invalid_exclusion_condition_item_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir",
            definition_text="Test definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=("valid", "  "),
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_non_tuple_exclusion_conditions_refused(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="TEST",
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="damir",
            definition_text="Test definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=["exc"],  # type: ignore[arg-type]
        )
        assert verdict.verdict_state is BuiltReferenceDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# §3 — build_built_reference_registry() produces correct closure states
# ===========================================================================


class TestBuildBuiltReferenceRegistry:
    """build_built_reference_registry() pure function tests."""

    def test_default_registry_is_closed(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="BUILT_REFERENCE registry closure with all 5 families",
            constitutional_chain=(
                "FormalShapeDefinition",
                "FormalShapeRegistry",
                "ClosureState",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        registry = build_built_reference_registry()
        assert registry.domain is FormalShapeDomain.BUILT_REFERENCE
        assert registry.closure_state is FormalShapeClosureState.CLOSED
        assert len(registry.families) == 5
        assert len(registry.definitions) == 5
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

    def test_partial_registry_missing_family(self) -> None:
        partial_defs = (
            PERSONAL_PRONOUN_DEFINITION,
            DEMONSTRATIVE_DEFINITION,
            RELATIVE_PRONOUN_DEFINITION,
        )
        registry = build_built_reference_registry(definitions=partial_defs)
        assert registry.closure_state is FormalShapeClosureState.PARTIAL
        assert len(registry.definitions) == 3

    def test_empty_definitions_produce_empty_state(self) -> None:
        registry = build_built_reference_registry(definitions=())
        assert registry.closure_state is FormalShapeClosureState.EMPTY
        assert len(registry.definitions) == 0

    def test_wrong_domain_definition_refused(self) -> None:
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
        registry = build_built_reference_registry(definitions=(wrong_domain_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED

    def test_hidden_forbidden_residual_refused(self) -> None:
        bad_def = FormalShapeDefinition(
            shape_id="BUILT_REFERENCE.BAD",
            domain=FormalShapeDomain.BUILT_REFERENCE,
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="bad",
            definition_text="Definition with hidden residual",
            distinguishing_evidence="Bad evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
            weight_constraint=None,
            path_constraint=None,
            rank=Rank.CANDIDATE,
            residuals=(
                Residual(
                    name="hidden",
                    kind=ResidualKind.HIDDEN_FORBIDDEN,
                    visible=False,
                    note="Hidden forbidden",
                ),
            ),
            trace_ref="test/bad",
        )
        registry = build_built_reference_registry(definitions=(bad_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED

    def test_blocking_residual_refused(self) -> None:
        bad_def = FormalShapeDefinition(
            shape_id="BUILT_REFERENCE.BLOCKED",
            domain=FormalShapeDomain.BUILT_REFERENCE,
            family=PERSONAL_PRONOUN_FAMILY,
            canonical_name="blocked",
            definition_text="Definition with blocking residual",
            distinguishing_evidence="Blocked evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
            weight_constraint=None,
            path_constraint=None,
            rank=Rank.CANDIDATE,
            residuals=(
                Residual(
                    name="blocking",
                    kind=ResidualKind.BLOCKING,
                    visible=True,
                    note="Blocking",
                ),
            ),
            trace_ref="test/blocked",
        )
        registry = build_built_reference_registry(definitions=(bad_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED


# ===========================================================================
# §4 — Forbidden outputs proven absent
# ===========================================================================


class TestForbiddenOutputs:
    """No meaning, ifadah, hukm, or semantic content in any definition."""

    MEANING_KEYWORDS = ("denotes a meaning", "carries meaning", "has meaning")

    def test_no_positive_meaning_language_in_definitions(self) -> None:
        """No definition_text contains positive meaning language."""
        for d in (
            PERSONAL_PRONOUN_DEFINITION,
            DEMONSTRATIVE_DEFINITION,
            RELATIVE_PRONOUN_DEFINITION,
            INTERROGATIVE_DEFINITION,
            CONDITIONAL_DEFINITION,
        ):
            text_lower = d.definition_text.lower()
            for kw in self.MEANING_KEYWORDS:
                assert kw not in text_lower, (
                    f"{d.shape_id} contains forbidden meaning language: {kw!r}"
                )

    def test_residuals_are_explanatory_not_hidden(self) -> None:
        """All canonical residuals are EXPLANATORY and visible."""
        for d in (
            PERSONAL_PRONOUN_DEFINITION,
            DEMONSTRATIVE_DEFINITION,
            RELATIVE_PRONOUN_DEFINITION,
            INTERROGATIVE_DEFINITION,
            CONDITIONAL_DEFINITION,
        ):
            for r in d.residuals:
                assert r.kind is ResidualKind.EXPLANATORY
                assert r.visible is True

    def test_all_exclusion_conditions_contain_negation(self) -> None:
        """Exclusion conditions express what the form is NOT."""
        for d in (
            PERSONAL_PRONOUN_DEFINITION,
            DEMONSTRATIVE_DEFINITION,
            RELATIVE_PRONOUN_DEFINITION,
            INTERROGATIVE_DEFINITION,
            CONDITIONAL_DEFINITION,
        ):
            for exc in d.exclusion_conditions:
                lower = exc.lower()
                assert "not" in lower or "≠" in lower or "does not" in lower, (
                    f"{d.shape_id} exclusion missing negation: {exc!r}"
                )


# ===========================================================================
# §5 — Schema guards refuse malformed carriers
# ===========================================================================


class TestSchemaGuards:
    """Schema validation at carrier birth."""

    def test_verdict_with_defined_but_no_definition_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            BuiltReferenceDefinitionVerdict(
                definition=None,
                verdict_state=BuiltReferenceDefinitionState.DEFINED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/bad",
            )

    def test_verdict_with_refused_but_no_failure_code_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            BuiltReferenceDefinitionVerdict(
                definition=None,
                verdict_state=BuiltReferenceDefinitionState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/bad",
            )

    def test_verdict_rank_exceeds_ceiling_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            BuiltReferenceDefinitionVerdict(
                definition=None,
                verdict_state=BuiltReferenceDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.HYPOTHESIS,
                residuals=(),
                trace_ref="test/bad",
            )

    def test_verdict_empty_trace_ref_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            BuiltReferenceDefinitionVerdict(
                definition=None,
                verdict_state=BuiltReferenceDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# §6 — Rank and residual governance
# ===========================================================================


class TestRankAndResidualGovernance:
    """Rank never exceeds ceiling; no forbidden residuals pass."""

    def test_all_definitions_respect_rank_ceiling(self) -> None:
        for d in (
            PERSONAL_PRONOUN_DEFINITION,
            DEMONSTRATIVE_DEFINITION,
            RELATIVE_PRONOUN_DEFINITION,
            INTERROGATIVE_DEFINITION,
            CONDITIONAL_DEFINITION,
        ):
            assert d.rank <= FORMAL_SHAPE_RANK_CEILING

    def test_define_function_respects_rank_ceiling(self) -> None:
        verdict = define_built_reference_shape(
            shape_id="RANK_TEST",
            family=DEMONSTRATIVE_FAMILY,
            canonical_name="test",
            definition_text="Test formal definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_rank <= FORMAL_SHAPE_RANK_CEILING

    def test_registry_rank_ceiling_matches(self) -> None:
        registry = build_built_reference_registry()
        assert registry.rank_ceiling == FORMAL_SHAPE_RANK_CEILING


# ===========================================================================
# §7 — Family completeness and domain integrity
# ===========================================================================


class TestFamilyIntegrity:
    """BUILT_REFERENCE families are complete and correctly scoped."""

    def test_five_families_in_built_reference(self) -> None:
        assert len(BUILT_REFERENCE_FAMILIES) == 5

    def test_all_families_have_built_reference_domain(self) -> None:
        for f in BUILT_REFERENCE_FAMILIES:
            assert f.domain is FormalShapeDomain.BUILT_REFERENCE

    def test_family_ids_are_unique(self) -> None:
        ids = [f.family_id for f in BUILT_REFERENCE_FAMILIES]
        assert len(set(ids)) == 5

    def test_expected_family_ids_present(self) -> None:
        ids = {f.family_id for f in BUILT_REFERENCE_FAMILIES}
        assert ids == {
            "PERSONAL_PRONOUN",
            "DEMONSTRATIVE",
            "RELATIVE_PRONOUN",
            "INTERROGATIVE",
            "CONDITIONAL",
        }
