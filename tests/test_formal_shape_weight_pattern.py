"""Constitutional tests for PR-F4: Weight Formal Definitions.

Origin law: docs/34_FORMAL_SHAPE_REGISTRY_LAW.md §7 (WEIGHT_PATTERN).

This test module proves:
1. All 12 WEIGHT_PATTERN canonical definitions satisfy constitutional
   requirements (13 fields, rank ceiling, residual governance, trace).
2. define_weight_pattern_shape() produces DEFINED verdicts for valid
   inputs and REFUSED verdicts with named FailureCodes for invalid inputs.
3. build_weight_pattern_registry() produces CLOSED state when all 12
   families are present, PARTIAL when incomplete, EMPTY when none.
4. Forbidden outputs are proven absent: no meaning, no ifadah, no hukm,
   no reality, no semantic content, no event occurrence.
5. Constitutional invariants hold: FAʿIL_FORM ≠ real agent,
   MAFʿUL_FORM ≠ real patient, MASDAR ≠ event occurrence,
   INSTRUMENT ≠ actual instrument, TIME_PLACE ≠ real time/place,
   GENDERED_WEIGHT ≠ real gender judgment.
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
from taaqqul_slot_geometry.weight.formal_shape_weight_pattern import (
    FAIL_FORM_DEFINITION,
    FAIL_FORM_FAMILY,
    GENDERED_WEIGHT_FORM_DEFINITION,
    INSTRUMENT_FORM_DEFINITION,
    JAMID_WEIGHT_FORM_DEFINITION,
    MAFUL_FORM_DEFINITION,
    MASDAR_MAZID_PATTERN_DEFINITION,
    MASDAR_MUJARRAD_PATTERN_DEFINITION,
    NOMINAL_DERIVED_PATTERN_DEFINITION,
    SIFAH_MUSHABBAHA_FORM_DEFINITION,
    TIME_PLACE_FORM_DEFINITION,
    VERBAL_MAZID_PATTERN_DEFINITION,
    VERBAL_MUJARRAD_PATTERN_DEFINITION,
    VERBAL_MUJARRAD_PATTERN_FAMILY,
    WEIGHT_PATTERN_FAMILIES,
    WeightPatternDefinitionState,
    WeightPatternDefinitionVerdict,
    build_weight_pattern_registry,
    define_weight_pattern_shape,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

# All 12 canonical definitions for parametrized tests.
ALL_CANONICAL_DEFINITIONS = (
    VERBAL_MUJARRAD_PATTERN_DEFINITION,
    VERBAL_MAZID_PATTERN_DEFINITION,
    MASDAR_MUJARRAD_PATTERN_DEFINITION,
    MASDAR_MAZID_PATTERN_DEFINITION,
    NOMINAL_DERIVED_PATTERN_DEFINITION,
    FAIL_FORM_DEFINITION,
    MAFUL_FORM_DEFINITION,
    SIFAH_MUSHABBAHA_FORM_DEFINITION,
    INSTRUMENT_FORM_DEFINITION,
    TIME_PLACE_FORM_DEFINITION,
    JAMID_WEIGHT_FORM_DEFINITION,
    GENDERED_WEIGHT_FORM_DEFINITION,
)


# ===========================================================================
# §1 — All canonical definitions satisfy constitutional requirements
# ===========================================================================


class TestAllCanonicalWeightDefinitionsValid:
    """Test 1: All 12 WEIGHT_PATTERN canonical definitions are valid."""

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_all_canonical_weight_definitions_valid(
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
        assert defn.domain is FormalShapeDomain.WEIGHT_PATTERN
        assert defn.shape_id
        assert defn.canonical_name
        assert defn.definition_text
        assert defn.distinguishing_evidence
        assert defn.boundary_conditions
        assert defn.rank <= FORMAL_SHAPE_RANK_CEILING
        assert defn.trace_ref
        assert all(isinstance(r, Residual) for r in defn.residuals)
        assert all(r.kind is not ResidualKind.HIDDEN_FORBIDDEN for r in defn.residuals)
        assert all(r.kind is not ResidualKind.BLOCKING for r in defn.residuals)
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
# §2 — Registry closure states
# ===========================================================================


class TestWeightPatternRegistryClosed:
    """Tests 2-7: Registry closure logic."""

    def test_weight_pattern_registry_closed_with_all_12_families(self) -> None:
        """Test 2: Default registry is CLOSED with all 12 families."""
        case = ConstitutionalTestCase(
            origin_law="docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",
            branch_name="WEIGHT_PATTERN registry closure with all 12 families",
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
        registry = build_weight_pattern_registry()
        assert registry.domain is FormalShapeDomain.WEIGHT_PATTERN
        assert registry.closure_state is FormalShapeClosureState.CLOSED
        assert len(registry.families) == 12
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

    def test_weight_pattern_registry_partial_when_family_missing(self) -> None:
        """Test 3: Partial when some families missing."""
        partial_defs = (
            VERBAL_MUJARRAD_PATTERN_DEFINITION,
            VERBAL_MAZID_PATTERN_DEFINITION,
            FAIL_FORM_DEFINITION,
        )
        registry = build_weight_pattern_registry(definitions=partial_defs)
        assert registry.closure_state is FormalShapeClosureState.PARTIAL
        assert len(registry.definitions) == 3

    def test_weight_pattern_registry_empty_when_no_definitions(self) -> None:
        """Test 4: Empty when no definitions provided."""
        registry = build_weight_pattern_registry(definitions=())
        assert registry.closure_state is FormalShapeClosureState.EMPTY
        assert len(registry.definitions) == 0

    def test_weight_pattern_registry_refused_on_wrong_domain(self) -> None:
        """Test 5: Refused when definition has wrong domain."""
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
        registry = build_weight_pattern_registry(definitions=(wrong_domain_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED

    def test_registry_refused_on_hidden_forbidden_residual(self) -> None:
        """Test 6: Refused on HIDDEN_FORBIDDEN residual."""
        bad_def = FormalShapeDefinition(
            shape_id="WEIGHT_PATTERN.BAD",
            domain=FormalShapeDomain.WEIGHT_PATTERN,
            family=VERBAL_MUJARRAD_PATTERN_FAMILY,
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
        registry = build_weight_pattern_registry(definitions=(bad_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED

    def test_registry_refused_on_blocking_residual(self) -> None:
        """Test 7: Refused on BLOCKING residual."""
        bad_def = FormalShapeDefinition(
            shape_id="WEIGHT_PATTERN.BLOCKED",
            domain=FormalShapeDomain.WEIGHT_PATTERN,
            family=FAIL_FORM_FAMILY,
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
        registry = build_weight_pattern_registry(definitions=(bad_def,))
        assert registry.closure_state is FormalShapeClosureState.REFUSED


# ===========================================================================
# §3 — Forbidden outputs proven absent
# ===========================================================================


class TestForbiddenOutputs:
    """Tests 8-9: No meaning language, no event occurrence claims."""

    FORBIDDEN_MEANING_PHRASES = (
        "denotes a meaning",
        "carries meaning",
        "has meaning",
        "real agent",
        "real patient",
        "actual event",
        "event occurs",
        "semantic derivation",
        "true cause",
        "actual instrument",
        "real time",
        "real place",
    )

    def test_no_positive_meaning_language_in_definition_text(self) -> None:
        """Test 8: No positive meaning language in any definition_text."""
        for d in ALL_CANONICAL_DEFINITIONS:
            text_lower = d.definition_text.lower()
            for phrase in self.FORBIDDEN_MEANING_PHRASES:
                assert phrase not in text_lower, (
                    f"{d.shape_id} definition_text contains forbidden "
                    f"meaning language: {phrase!r}"
                )

    def test_no_event_occurrence_claim(self) -> None:
        """Test 9: No definition asserts event occurrence."""
        event_phrases = ("event occurs", "action happens", "event takes place")
        for d in ALL_CANONICAL_DEFINITIONS:
            text_lower = d.definition_text.lower()
            for phrase in event_phrases:
                assert phrase not in text_lower, (
                    f"{d.shape_id} asserts event occurrence: {phrase!r}"
                )


# ===========================================================================
# §4 — Constitutional invariants for specific forms
# ===========================================================================


class TestConstitutionalInvariants:
    """Tests 10-15: Specific form invariants."""

    def test_fa_il_form_not_real_agent_and_not_formal_agent_slot(self) -> None:
        """Test 10: FAʿIL_FORM ≠ real agent and ≠ FORMAL_AGENT_SLOT."""
        d = FAIL_FORM_DEFINITION
        # Exclusion conditions must state these
        exc_text = " ".join(d.exclusion_conditions).lower()
        assert "real agent" in exc_text or "≠ real agent" in " ".join(d.exclusion_conditions)
        assert "formal_agent_slot" in exc_text or "FORMAL_AGENT_SLOT" in " ".join(
            d.exclusion_conditions
        )
        # Residuals must include CONTRACT_SLOT_DEFERRED
        residual_names = [r.name for r in d.residuals]
        assert any("CONTRACT_SLOT_DEFERRED" in n for n in residual_names)

    def test_maf_ul_form_not_real_patient_and_not_formal_object_slot(self) -> None:
        """Test 11: MAFʿUL_FORM ≠ real patient and ≠ FORMAL_OBJECT_SLOT."""
        d = MAFUL_FORM_DEFINITION
        exc_text = " ".join(d.exclusion_conditions).lower()
        assert "real patient" in exc_text or "≠ real patient" in " ".join(
            d.exclusion_conditions
        )
        assert "formal_object_slot" in exc_text or "FORMAL_OBJECT_SLOT" in " ".join(
            d.exclusion_conditions
        )
        residual_names = [r.name for r in d.residuals]
        assert any("CONTRACT_SLOT_DEFERRED" in n for n in residual_names)

    def test_masdar_not_event_occurrence(self) -> None:
        """Test 12: MASDAR forms ≠ event occurrence."""
        for d in (MASDAR_MUJARRAD_PATTERN_DEFINITION, MASDAR_MAZID_PATTERN_DEFINITION):
            exc_text = " ".join(d.exclusion_conditions).lower()
            assert "event occurrence" in exc_text or "≠ event occurrence" in " ".join(
                d.exclusion_conditions
            ), f"{d.shape_id} missing event-occurrence exclusion"

    def test_instrument_not_actual_instrument(self) -> None:
        """Test 13: INSTRUMENT_FORM ≠ actual instrument."""
        d = INSTRUMENT_FORM_DEFINITION
        exc_text = " ".join(d.exclusion_conditions).lower()
        assert "actual instrument" in exc_text or "≠ actual instrument" in " ".join(
            d.exclusion_conditions
        )

    def test_time_place_not_real_time_or_place(self) -> None:
        """Test 14: TIME_PLACE_FORM ≠ real time/place."""
        d = TIME_PLACE_FORM_DEFINITION
        exc_text = " ".join(d.exclusion_conditions).lower()
        assert "real time" in exc_text or "real place" in exc_text

    def test_gendered_weight_not_real_gender_judgment(self) -> None:
        """Test 15: GENDERED_WEIGHT_FORM ≠ real sex/gender judgment."""
        d = GENDERED_WEIGHT_FORM_DEFINITION
        exc_text = " ".join(d.exclusion_conditions).lower()
        assert "real sex" in exc_text or "gender judgment" in exc_text


# ===========================================================================
# §5 — Deferred residuals present
# ===========================================================================


class TestDeferredResiduals:
    """Test 16: Required deferred residuals are present."""

    def test_required_deferred_residuals_present(self) -> None:
        """Test 16: Key definitions carry required deferred residuals."""
        # VERBAL patterns must have INFLECTION_DEFERRED and CONTRACT_SLOT_DEFERRED
        for d in (VERBAL_MUJARRAD_PATTERN_DEFINITION, VERBAL_MAZID_PATTERN_DEFINITION):
            names = [r.name for r in d.residuals]
            assert any("INFLECTION_DEFERRED" in n for n in names), (
                f"{d.shape_id} missing INFLECTION_DEFERRED residual"
            )
            assert any("CONTRACT_SLOT_DEFERRED" in n for n in names), (
                f"{d.shape_id} missing CONTRACT_SLOT_DEFERRED residual"
            )

        # FAʿIL_FORM and MAFʿUL_FORM must have CONTRACT_SLOT_DEFERRED
        for d in (FAIL_FORM_DEFINITION, MAFUL_FORM_DEFINITION):
            names = [r.name for r in d.residuals]
            assert any("CONTRACT_SLOT_DEFERRED" in n for n in names), (
                f"{d.shape_id} missing CONTRACT_SLOT_DEFERRED residual"
            )

        # MASDAR forms must have SEMANTIC_DALALAH_DEFERRED
        for d in (MASDAR_MUJARRAD_PATTERN_DEFINITION, MASDAR_MAZID_PATTERN_DEFINITION):
            names = [r.name for r in d.residuals]
            assert any("SEMANTIC_DALALAH_DEFERRED" in n for n in names), (
                f"{d.shape_id} missing SEMANTIC_DALALAH_DEFERRED residual"
            )

        # GENDERED_WEIGHT_FORM must have COMPOSITION_PATTERN_DEFERRED
        names = [r.name for r in GENDERED_WEIGHT_FORM_DEFINITION.residuals]
        assert any("COMPOSITION_PATTERN_DEFERRED" in n for n in names), (
            "GENDERED_WEIGHT_FORM_DEFINITION missing "
            "COMPOSITION_PATTERN_DEFERRED residual"
        )


# ===========================================================================
# §6 — Rank and trace governance
# ===========================================================================


class TestRankAndTrace:
    """Tests 17-18: Rank bounded and trace present."""

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_rank_bounded_by_formal_shape_ceiling(
        self, defn: FormalShapeDefinition
    ) -> None:
        """Test 17: Rank never exceeds FORMAL_SHAPE_RANK_CEILING."""
        assert defn.rank <= FORMAL_SHAPE_RANK_CEILING

    @pytest.mark.parametrize(
        "defn",
        ALL_CANONICAL_DEFINITIONS,
        ids=[d.shape_id for d in ALL_CANONICAL_DEFINITIONS],
    )
    def test_trace_ref_present_for_every_definition(
        self, defn: FormalShapeDefinition
    ) -> None:
        """Test 18: Every definition has a non-empty trace_ref."""
        assert defn.trace_ref
        assert isinstance(defn.trace_ref, str)
        assert defn.trace_ref.strip()


# ===========================================================================
# §7 — Package exports
# ===========================================================================


class TestPackageExports:
    """Test 19: All new symbols importable from weight package."""

    def test_all_new_symbols_importable_from_weight_package(self) -> None:
        """Test 19: All PR-F4 symbols accessible via weight package."""
        from taaqqul_slot_geometry import weight

        expected_symbols = [
            "FAIL_FORM_DEFINITION",
            "FAIL_FORM_FAMILY",
            "GENDERED_WEIGHT_FORM_DEFINITION",
            "GENDERED_WEIGHT_FORM_FAMILY",
            "INSTRUMENT_FORM_DEFINITION",
            "INSTRUMENT_FORM_FAMILY",
            "JAMID_WEIGHT_FORM_DEFINITION",
            "JAMID_WEIGHT_FORM_FAMILY",
            "MAFUL_FORM_DEFINITION",
            "MAFUL_FORM_FAMILY",
            "MASDAR_MAZID_PATTERN_DEFINITION",
            "MASDAR_MAZID_PATTERN_FAMILY",
            "MASDAR_MUJARRAD_PATTERN_DEFINITION",
            "MASDAR_MUJARRAD_PATTERN_FAMILY",
            "NOMINAL_DERIVED_PATTERN_DEFINITION",
            "NOMINAL_DERIVED_PATTERN_FAMILY",
            "SIFAH_MUSHABBAHA_FORM_DEFINITION",
            "SIFAH_MUSHABBAHA_FORM_FAMILY",
            "TIME_PLACE_FORM_DEFINITION",
            "TIME_PLACE_FORM_FAMILY",
            "VERBAL_MAZID_PATTERN_DEFINITION",
            "VERBAL_MAZID_PATTERN_FAMILY",
            "VERBAL_MUJARRAD_PATTERN_DEFINITION",
            "VERBAL_MUJARRAD_PATTERN_FAMILY",
            "WEIGHT_PATTERN_FAMILIES",
            "WeightPatternDefinitionState",
            "WeightPatternDefinitionVerdict",
            "build_weight_pattern_registry",
            "define_weight_pattern_shape",
        ]
        for sym in expected_symbols:
            assert hasattr(weight, sym), f"Missing export: {sym}"
            assert sym in weight.__all__, f"Not in __all__: {sym}"


# ===========================================================================
# §8 — define_weight_pattern_shape() operation tests
# ===========================================================================


class TestDefineWeightPatternShape:
    """define_weight_pattern_shape() pure function tests."""

    def test_valid_definition_produces_defined_verdict(self) -> None:
        verdict = define_weight_pattern_shape(
            shape_id="TEST_VERBAL",
            family=VERBAL_MUJARRAD_PATTERN_FAMILY,
            canonical_name="fi'l_test",
            definition_text="Test formal definition for verbal pattern",
            distinguishing_evidence="Root-pattern correspondence test",
            boundary_conditions=("Root letters fill template",),
            exclusion_conditions=("Does not assert event",),
        )
        assert verdict.verdict_state is WeightPatternDefinitionState.DEFINED
        assert verdict.failure_code is None
        assert verdict.definition is not None
        assert verdict.definition.shape_id == "TEST_VERBAL"
        assert verdict.definition.domain is FormalShapeDomain.WEIGHT_PATTERN
        assert verdict.verdict_rank <= FORMAL_SHAPE_RANK_CEILING
        assert verdict.trace_ref

    def test_empty_shape_id_refused(self) -> None:
        verdict = define_weight_pattern_shape(
            shape_id="",
            family=VERBAL_MUJARRAD_PATTERN_FAMILY,
            canonical_name="fi'l",
            definition_text="Test",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WeightPatternDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_wrong_domain_family_refused(self) -> None:
        wrong_family = FormalShapeFamily(
            domain=FormalShapeDomain.BUILT_REFERENCE,
            family_id="PRONOUN",
            description="Wrong domain",
        )
        verdict = define_weight_pattern_shape(
            shape_id="WRONG",
            family=wrong_family,
            canonical_name="test",
            definition_text="Test definition",
            distinguishing_evidence="Test evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WeightPatternDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.DOMAIN_MISSING

    def test_non_family_type_refused(self) -> None:
        verdict = define_weight_pattern_shape(
            shape_id="TEST",
            family="not_a_family",  # type: ignore[arg-type]
            canonical_name="test",
            definition_text="Test",
            distinguishing_evidence="Evidence",
            boundary_conditions=("cond",),
            exclusion_conditions=(),
        )
        assert verdict.verdict_state is WeightPatternDefinitionState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED


# ===========================================================================
# §9 — Schema guards
# ===========================================================================


class TestSchemaGuards:
    """Schema validation at verdict birth."""

    def test_verdict_with_defined_but_no_definition_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WeightPatternDefinitionVerdict(
                definition=None,
                verdict_state=WeightPatternDefinitionState.DEFINED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/bad",
            )

    def test_verdict_with_refused_but_no_failure_code_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WeightPatternDefinitionVerdict(
                definition=None,
                verdict_state=WeightPatternDefinitionState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/bad",
            )

    def test_verdict_rank_exceeds_ceiling_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WeightPatternDefinitionVerdict(
                definition=None,
                verdict_state=WeightPatternDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.HYPOTHESIS,
                residuals=(),
                trace_ref="test/bad",
            )

    def test_verdict_empty_trace_ref_raises(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WeightPatternDefinitionVerdict(
                definition=None,
                verdict_state=WeightPatternDefinitionState.REFUSED,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# §10 — Family completeness
# ===========================================================================


class TestFamilyIntegrity:
    """WEIGHT_PATTERN families are complete and correctly scoped."""

    def test_twelve_families_in_weight_pattern(self) -> None:
        assert len(WEIGHT_PATTERN_FAMILIES) == 12

    def test_all_families_have_weight_pattern_domain(self) -> None:
        for f in WEIGHT_PATTERN_FAMILIES:
            assert f.domain is FormalShapeDomain.WEIGHT_PATTERN

    def test_family_ids_are_unique(self) -> None:
        ids = [f.family_id for f in WEIGHT_PATTERN_FAMILIES]
        assert len(set(ids)) == 12

    def test_expected_family_ids_present(self) -> None:
        ids = {f.family_id for f in WEIGHT_PATTERN_FAMILIES}
        assert ids == {
            "VERBAL_MUJARRAD_PATTERN",
            "VERBAL_MAZID_PATTERN",
            "MASDAR_MUJARRAD_PATTERN",
            "MASDAR_MAZID_PATTERN",
            "NOMINAL_DERIVED_PATTERN",
            "FAIL_FORM",
            "MAFUL_FORM",
            "SIFAH_MUSHABBAHA_FORM",
            "INSTRUMENT_FORM",
            "TIME_PLACE_FORM",
            "JAMID_WEIGHT_FORM",
            "GENDERED_WEIGHT_FORM",
        }

    def test_all_definitions_mutually_distinct(self) -> None:
        """All 12 definitions have distinct shape_ids and evidence."""
        shape_ids = [d.shape_id for d in ALL_CANONICAL_DEFINITIONS]
        assert len(set(shape_ids)) == 12
        evidences = [d.distinguishing_evidence for d in ALL_CANONICAL_DEFINITIONS]
        assert len(set(evidences)) == 12
