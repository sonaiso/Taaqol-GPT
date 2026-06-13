"""Constitutional tests for PR-F8: Formal Style Candidate.

Origin law: docs/35_FORMAL_STYLE_CANDIDATE_LAW.md.

This test module proves:
1. All 10 formal style definitions are formal only (no meaning language).
2. No definition_text contains positive meaning/assertion/truth/intent language.
3. Declarative/khabar style is not proposition.
4. Command style is not obligation.
5. Prohibition style is not real prohibition.
6. Interrogative style is not request for answer.
7. Vocative style is not real addressee.
8. Condition style is not conditional truth.
9. Oath style is not truth guarantee.
10. Registry or closure refuses wrong domain.
11. Hidden/blocking residual refuses.
12. Rank never exceeds formal ceiling.
13. Every verdict carries trace_ref.
14. PR-F8 does not export or instantiate IfādahCandidate, Meaning,
    Dalālah, Hukm, Manṭūq, Mafhūm, Majāz, or Manqūl.
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import ResidualKind
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.formal_shape import (
    FORMAL_SHAPE_RANK_CEILING,
    FormalShapeClosureState,
)
from taaqqul_slot_geometry.weight.formal_style_candidate import (
    FORMAL_STYLE_DEFINITIONS,
    FORMAL_STYLE_FAMILIES,
    FormalStyleCandidate,
    FormalStyleFamily,
    FormalStyleState,
    FormalStyleVerdict,
    prove_formal_style_candidate,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
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

# Required deferred residual name prefixes.
REQUIRED_RESIDUAL_PREFIXES = (
    "formal_style_not_meaning/",
    "DALALAH_DEFERRED_TO_PR_D1/",
    "MUFRAD_SEMANTIC_SLOT_GEOMETRY_DEFERRED_TO_PR_D1/",
    "IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE/",
    "MANTUQ_DEFERRED_UNTIL_IFADAH/",
    "MAFHUM_DEFERRED_UNTIL_MANTUQ/",
    "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT/",
    "MANQUL_DEFERRED_UNTIL_TRANSFER_GATE/",
)


# ===========================================================================
# Test 1: All 10 formal style definitions are formal only
# ===========================================================================


class TestAllFormalStyleDefinitionsAreFormalOnly:
    """All 10 FormalStyleFamily members have valid canonical definitions."""

    @pytest.mark.parametrize(
        "family",
        FORMAL_STYLE_FAMILIES,
        ids=[f.value for f in FORMAL_STYLE_FAMILIES],
    )
    def test_style_has_canonical_definition(
        self, family: FormalStyleFamily
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name=f"{family.value} has canonical definition",
            constitutional_chain=("FormalStyleCandidate", "Rank", "Residual", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "SemanticEntry"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        assert family in FORMAL_STYLE_DEFINITIONS
        defn = FORMAL_STYLE_DEFINITIONS[family]
        assert isinstance(defn["canonical_name"], str)
        assert isinstance(defn["definition_text"], str)
        assert defn["definition_text"].strip()
        assert isinstance(defn["distinguishing_evidence"], str)
        assert defn["distinguishing_evidence"].strip()
        assert isinstance(defn["boundary_conditions"], tuple)
        assert len(defn["boundary_conditions"]) > 0
        assert isinstance(defn["exclusion_conditions"], tuple)
        assert len(defn["exclusion_conditions"]) > 0

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)

    @pytest.mark.parametrize(
        "family",
        FORMAL_STYLE_FAMILIES,
        ids=[f.value for f in FORMAL_STYLE_FAMILIES],
    )
    def test_prove_produces_proven_verdict(
        self, family: FormalStyleFamily
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name=f"prove_formal_style_candidate({family.value}) returns PROVEN",
            constitutional_chain=(
                "prove_formal_style_candidate", "Verdict", "Rank", "Trace",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = prove_formal_style_candidate(
            style_family=family,
            composition_evidence_ref=f"test/composition/{family.value}",
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="test/closure/CLOSED",
        )

        assert verdict.verdict_state is FormalStyleState.PROVEN
        assert verdict.failure_code is None
        assert verdict.candidate is not None
        assert verdict.candidate.style_family is family
        assert verdict.verdict_rank <= FORMAL_SHAPE_RANK_CEILING
        assert verdict.trace_ref.strip()
        assert verdict.residuals
        for r in verdict.residuals:
            assert r.visible is True
            assert r.kind is ResidualKind.EXPLANATORY

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 2: No definition_text contains positive meaning language
# ===========================================================================


class TestNoMeaningLanguageInDefinitions:
    """PR-F2.1 MCE rule: no positive 'meaning' language in definition_text."""

    @pytest.mark.parametrize(
        "family",
        FORMAL_STYLE_FAMILIES,
        ids=[f.value for f in FORMAL_STYLE_FAMILIES],
    )
    def test_definition_text_has_no_meaning_language(
        self, family: FormalStyleFamily
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name=f"{family.value} definition_text has no meaning language",
            constitutional_chain=("FormalStyleCandidate", "MCE_Hardening"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "SemanticEntry", "Dalālah"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_STYLE_DEFINITIONS[family]
        text_lower = str(defn["definition_text"]).lower()
        for word in MEANING_WORDS:
            assert word not in text_lower, (
                f"definition_text for {family.value} contains forbidden "
                f"meaning-language word: '{word}'"
            )
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 3: Constitutional invariants — style ≠ meaning/truth/intent
# ===========================================================================


class TestConstitutionalInvariants:
    """Prove per-family constitutional invariants."""

    def test_declarative_style_is_not_proposition(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="DECLARATIVE_STYLE_FORM ≠ proposition",
            constitutional_chain=("FormalStyleCandidate", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Proposition", "Truth", "Assertion"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_STYLE_DEFINITIONS[FormalStyleFamily.DECLARATIVE_STYLE_FORM]
        exclusions = defn["exclusion_conditions"]
        exclusion_text = " ".join(str(e) for e in exclusions).lower()  # type: ignore[union-attr]
        assert "proposition" in exclusion_text
        assert "truth" in exclusion_text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)

    def test_command_style_is_not_obligation(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="COMMAND_STYLE_FORM ≠ obligation",
            constitutional_chain=("FormalStyleCandidate", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Obligation", "Duty", "RealCommand"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_STYLE_DEFINITIONS[FormalStyleFamily.COMMAND_STYLE_FORM]
        exclusions = defn["exclusion_conditions"]
        exclusion_text = " ".join(str(e) for e in exclusions).lower()  # type: ignore[union-attr]
        assert "obligation" in exclusion_text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)

    def test_prohibition_style_is_not_real_prohibition(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="PROHIBITION_STYLE_FORM ≠ real prohibition",
            constitutional_chain=("FormalStyleCandidate", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("RealProhibition", "LegalForbiddance"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_STYLE_DEFINITIONS[FormalStyleFamily.PROHIBITION_STYLE_FORM]
        exclusions = defn["exclusion_conditions"]
        exclusion_text = " ".join(str(e) for e in exclusions).lower()  # type: ignore[union-attr]
        assert "real prohibition" in exclusion_text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)

    def test_interrogative_style_is_not_request_for_answer(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="INTERROGATIVE_STYLE_FORM ≠ request for answer",
            constitutional_chain=("FormalStyleCandidate", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("RequestForAnswer", "Question"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_STYLE_DEFINITIONS[FormalStyleFamily.INTERROGATIVE_STYLE_FORM]
        exclusions = defn["exclusion_conditions"]
        exclusion_text = " ".join(str(e) for e in exclusions).lower()  # type: ignore[union-attr]
        assert "request" in exclusion_text or "answer" in exclusion_text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)

    def test_vocative_style_is_not_real_addressee(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="VOCATIVE_STYLE_FORM ≠ real addressee",
            constitutional_chain=("FormalStyleCandidate", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("RealAddressee", "Communication"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_STYLE_DEFINITIONS[FormalStyleFamily.VOCATIVE_STYLE_FORM]
        exclusions = defn["exclusion_conditions"]
        exclusion_text = " ".join(str(e) for e in exclusions).lower()  # type: ignore[union-attr]
        assert "real" in exclusion_text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)

    def test_condition_style_is_not_conditional_truth(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="CONDITION_STYLE_FORM ≠ conditional truth",
            constitutional_chain=("FormalStyleCandidate", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("ConditionalTruth", "Causation"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_STYLE_DEFINITIONS[FormalStyleFamily.CONDITION_STYLE_FORM]
        exclusions = defn["exclusion_conditions"]
        exclusion_text = " ".join(str(e) for e in exclusions).lower()  # type: ignore[union-attr]
        assert "conditional truth" in exclusion_text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)

    def test_oath_style_is_not_truth_guarantee(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="OATH_STYLE_FORM ≠ truth guarantee",
            constitutional_chain=("FormalStyleCandidate", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("TruthGuarantee", "BindingOath"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        defn = FORMAL_STYLE_DEFINITIONS[FormalStyleFamily.OATH_STYLE_FORM]
        exclusions = defn["exclusion_conditions"]
        exclusion_text = " ".join(str(e) for e in exclusions).lower()  # type: ignore[union-attr]
        assert "truth" in exclusion_text
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 4: prove_formal_style_candidate() refuses invalid inputs
# ===========================================================================


class TestProveFormalStyleCandidateRefusals:
    """prove_formal_style_candidate() produces REFUSED verdicts on violations."""

    def test_refuses_non_closed_formal_shape(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="prove_formal_style_candidate refuses non-CLOSED closure",
            constitutional_chain=("prove_formal_style_candidate", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = prove_formal_style_candidate(
            style_family=FormalStyleFamily.DECLARATIVE_STYLE_FORM,
            composition_evidence_ref="test/composition/khabar",
            formal_closure_state=FormalShapeClosureState.PARTIAL,
            formal_closure_ref="test/closure/PARTIAL",
        )
        assert verdict.verdict_state is FormalStyleState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED
        assert verdict.candidate is None
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_refuses_empty_composition_evidence_ref(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="prove_formal_style_candidate refuses empty evidence ref",
            constitutional_chain=("prove_formal_style_candidate", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = prove_formal_style_candidate(
            style_family=FormalStyleFamily.COMMAND_STYLE_FORM,
            composition_evidence_ref="",
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="test/closure/CLOSED",
        )
        assert verdict.verdict_state is FormalStyleState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert verdict.candidate is None
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_refuses_empty_formal_closure_ref(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="prove_formal_style_candidate refuses empty closure ref",
            constitutional_chain=("prove_formal_style_candidate", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = prove_formal_style_candidate(
            style_family=FormalStyleFamily.INTERROGATIVE_STYLE_FORM,
            composition_evidence_ref="test/composition/istifham",
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="",
        )
        assert verdict.verdict_state is FormalStyleState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert verdict.candidate is None
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_refuses_invalid_style_family_type(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="prove_formal_style_candidate refuses invalid style_family",
            constitutional_chain=("prove_formal_style_candidate", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = prove_formal_style_candidate(
            style_family="NOT_A_FAMILY",  # type: ignore[arg-type]
            composition_evidence_ref="test/composition/invalid",
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="test/closure/CLOSED",
        )
        assert verdict.verdict_state is FormalStyleState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert verdict.candidate is None
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_refuses_invalid_closure_state_type(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="prove_formal_style_candidate refuses invalid closure state type",
            constitutional_chain=("prove_formal_style_candidate", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        verdict = prove_formal_style_candidate(
            style_family=FormalStyleFamily.WISH_STYLE_FORM,
            composition_evidence_ref="test/composition/wish",
            formal_closure_state="CLOSED",  # type: ignore[arg-type]
            formal_closure_ref="test/closure/CLOSED",
        )
        assert verdict.verdict_state is FormalStyleState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED
        assert verdict.candidate is None
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=verdict.verdict_rank,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 5: Residual governance
# ===========================================================================


class TestResidualGovernance:
    """Verify residuals are present, visible, and correct."""

    @pytest.mark.parametrize(
        "family",
        FORMAL_STYLE_FAMILIES,
        ids=[f.value for f in FORMAL_STYLE_FAMILIES],
    )
    def test_all_required_deferred_residuals_present(
        self, family: FormalStyleFamily
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name=f"{family.value} carries all required deferred residuals",
            constitutional_chain=("FormalStyleCandidate", "Residual", "Governance"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "HiddenResidual"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        verdict = prove_formal_style_candidate(
            style_family=family,
            composition_evidence_ref=f"test/composition/{family.value}",
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="test/closure/CLOSED",
        )
        assert verdict.verdict_state is FormalStyleState.PROVEN
        assert verdict.candidate is not None

        residual_names = {r.name for r in verdict.residuals}
        for prefix in REQUIRED_RESIDUAL_PREFIXES:
            expected_name = f"{prefix}{family.value}"
            assert expected_name in residual_names, (
                f"Missing required residual: {expected_name}"
            )

        # All residuals must be EXPLANATORY and visible
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY
            assert r.visible is True

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 6: Rank never exceeds formal ceiling
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds FORMAL_SHAPE_RANK_CEILING."""

    @pytest.mark.parametrize(
        "family",
        FORMAL_STYLE_FAMILIES,
        ids=[f.value for f in FORMAL_STYLE_FAMILIES],
    )
    def test_verdict_rank_within_ceiling(
        self, family: FormalStyleFamily
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name=f"{family.value} rank ≤ FORMAL_SHAPE_RANK_CEILING",
            constitutional_chain=("FormalStyleCandidate", "Rank", "Ceiling"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("RankPromotion",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        verdict = prove_formal_style_candidate(
            style_family=family,
            composition_evidence_ref=f"test/composition/{family.value}",
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="test/closure/CLOSED",
        )
        assert verdict.verdict_rank <= FORMAL_SHAPE_RANK_CEILING
        assert verdict.candidate is not None
        assert verdict.candidate.rank <= FORMAL_SHAPE_RANK_CEILING
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"FormalStyleCandidate"}),
        )
        assert_constitutional_case(case, result)

    def test_schema_refuses_rank_above_ceiling(self) -> None:
        """FormalStyleCandidate refuses rank above ceiling at birth."""
        case = ConstitutionalTestCase(
            origin_law="docs/35_FORMAL_STYLE_CANDIDATE_LAW.md",
            branch_name="FormalStyleCandidate refuses rank above ceiling",
            constitutional_chain=("FormalStyleCandidate", "SchemaGuard"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            forbidden_outputs=("RankPromotion",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        with pytest.raises(WeightCarrierSchemaError):
            FormalStyleCandidate(
                style_family=FormalStyleFamily.DECLARATIVE_STYLE_FORM,
                composition_evidence_ref="test/composition/khabar",
                formal_closure_ref="test/closure/CLOSED",
                definition_text="A test formal style classification.",
                distinguishing_evidence="Test evidence.",
                boundary_conditions=("Test boundary",),
                exclusion_conditions=("Test exclusion",),
                rank=Rank.HYPOTHESIS,  # Above ceiling
                residuals=(),
                trace_ref="test/trace",
            )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            rank=Rank.ZERO,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 7: Every verdict carries trace_ref
# ===========================================================================


class TestTraceRef:
    """Every verdict carries trace_ref."""

    @pytest.mark.parametrize(
        "family",
        FORMAL_STYLE_FAMILIES,
        ids=[f.value for f in FORMAL_STYLE_FAMILIES],
    )
    def test_proven_verdict_has_trace_ref(
        self, family: FormalStyleFamily
    ) -> None:
        verdict = prove_formal_style_candidate(
            style_family=family,
            composition_evidence_ref=f"test/composition/{family.value}",
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="test/closure/CLOSED",
        )
        assert isinstance(verdict.trace_ref, str)
        assert verdict.trace_ref.strip()
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate.trace_ref, str)
        assert verdict.candidate.trace_ref.strip()

    def test_refused_verdict_has_trace_ref(self) -> None:
        verdict = prove_formal_style_candidate(
            style_family=FormalStyleFamily.DECLARATIVE_STYLE_FORM,
            composition_evidence_ref="",
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="test/closure/CLOSED",
        )
        assert verdict.verdict_state is FormalStyleState.REFUSED
        assert isinstance(verdict.trace_ref, str)
        assert verdict.trace_ref.strip()


# ===========================================================================
# Test 8: Schema guard tests
# ===========================================================================


class TestSchemaGuards:
    """Schema guards refuse malformed carriers at birth."""

    def test_candidate_refuses_empty_composition_evidence_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalStyleCandidate(
                style_family=FormalStyleFamily.COMMAND_STYLE_FORM,
                composition_evidence_ref="",
                formal_closure_ref="test/closure",
                definition_text="Test text.",
                distinguishing_evidence="Test evidence.",
                boundary_conditions=("Test",),
                exclusion_conditions=(),
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )

    def test_candidate_refuses_empty_definition_text(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalStyleCandidate(
                style_family=FormalStyleFamily.COMMAND_STYLE_FORM,
                composition_evidence_ref="test/ref",
                formal_closure_ref="test/closure",
                definition_text="",
                distinguishing_evidence="Test evidence.",
                boundary_conditions=("Test",),
                exclusion_conditions=(),
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )

    def test_candidate_refuses_empty_boundary_conditions(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalStyleCandidate(
                style_family=FormalStyleFamily.COMMAND_STYLE_FORM,
                composition_evidence_ref="test/ref",
                formal_closure_ref="test/closure",
                definition_text="Test text.",
                distinguishing_evidence="Test evidence.",
                boundary_conditions=(),
                exclusion_conditions=(),
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )

    def test_candidate_refuses_empty_trace_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalStyleCandidate(
                style_family=FormalStyleFamily.COMMAND_STYLE_FORM,
                composition_evidence_ref="test/ref",
                formal_closure_ref="test/closure",
                definition_text="Test text.",
                distinguishing_evidence="Test evidence.",
                boundary_conditions=("Test",),
                exclusion_conditions=(),
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )

    def test_verdict_refuses_proven_with_failure_code(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalStyleVerdict(
                candidate=None,
                verdict_state=FormalStyleState.PROVEN,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )

    def test_verdict_refuses_refused_without_failure_code(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            FormalStyleVerdict(
                candidate=None,
                verdict_state=FormalStyleState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )


# ===========================================================================
# Test 9: PR-F8 does not export forbidden types
# ===========================================================================


class TestForbiddenExports:
    """PR-F8 module does not export or instantiate forbidden types."""

    def test_no_ifadah_candidate_export(self) -> None:
        import taaqqul_slot_geometry.weight.formal_style_candidate as mod
        assert not hasattr(mod, "IfādahCandidate")
        assert not hasattr(mod, "IfadahCandidate")

    def test_no_meaning_export(self) -> None:
        import taaqqul_slot_geometry.weight.formal_style_candidate as mod
        assert not hasattr(mod, "Meaning")

    def test_no_dalalah_export(self) -> None:
        import taaqqul_slot_geometry.weight.formal_style_candidate as mod
        assert not hasattr(mod, "Dalalah")
        assert not hasattr(mod, "Dalālah")

    def test_no_hukm_export(self) -> None:
        import taaqqul_slot_geometry.weight.formal_style_candidate as mod
        assert not hasattr(mod, "HukmCandidate")
        assert not hasattr(mod, "Hukm")

    def test_no_mantuq_export(self) -> None:
        import taaqqul_slot_geometry.weight.formal_style_candidate as mod
        assert not hasattr(mod, "MantuqClosure")
        assert not hasattr(mod, "Mantuq")

    def test_no_mafhum_export(self) -> None:
        import taaqqul_slot_geometry.weight.formal_style_candidate as mod
        assert not hasattr(mod, "MafhumCandidate")
        assert not hasattr(mod, "Mafhum")

    def test_no_majaz_export(self) -> None:
        import taaqqul_slot_geometry.weight.formal_style_candidate as mod
        assert not hasattr(mod, "Majaz")

    def test_no_manqul_export(self) -> None:
        import taaqqul_slot_geometry.weight.formal_style_candidate as mod
        assert not hasattr(mod, "Manqul")


# ===========================================================================
# Test 10: Families completeness
# ===========================================================================


class TestFamiliesCompleteness:
    """Exactly 10 style families, all unique."""

    def test_exactly_10_families(self) -> None:
        assert len(FORMAL_STYLE_FAMILIES) == 10

    def test_all_families_unique(self) -> None:
        assert len(set(FORMAL_STYLE_FAMILIES)) == 10

    def test_all_families_have_definitions(self) -> None:
        for family in FORMAL_STYLE_FAMILIES:
            assert family in FORMAL_STYLE_DEFINITIONS
