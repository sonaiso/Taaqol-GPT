"""Constitutional tests for PR-18: ContractableUnitGeometry Boundary.

Origin: docs/26, docs/27, docs/31, docs/32_CONTRACTABLE_UNIT_GEOMETRY_LAW.md.

Coverage of the 15 required constitutional tests:

1.  ContractableUnitGeometry requires DalMadlulBindingCandidate.
2.  prove_contractable_unit() refuses non-DalMadlulBindingCandidate input.
3.  prove_contractable_unit() refuses empty admissible_roles.
4.  prove_contractable_unit() refuses empty path_profile.
5.  prove_contractable_unit() refuses empty word_class_affordance.
6.  prove_contractable_unit() refuses empty inflection/derivational affordance.
7.  ContractableUnitGeometry is not Meaning.
8.  ContractableUnitGeometry carries no ifadah/hukm/reality fields.
9.  ContractableUnitGeometry is not RelationCandidate.
10. ContractableUnitGeometry is not CompositionCandidate.
11. Rank is bounded.
12. Residual governance: HIDDEN_FORBIDDEN refused.
13. Residual governance: BLOCKING refused.
14. trace_ref remains reference, not ledger commit.
15. Every refusal has named FailureCode.
16. PR-18 imports/defines no forbidden symbols.
17. ContractabilityProfile is affordance, not SyntaxRole.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    BINDING_RANK_CEILING,
    CONTRACTABLE_UNIT_RANK_CEILING,
    BindingState,
    BoundaryEvidence,
    ContractabilityProfile,
    ContractableUnitGeometry,
    ContractableUnitState,
    ContractableUnitVerdict,
    DalBoundaryState,
    DalMadlulBindingCandidate,
    DalOnlyCandidate,
    LicenseBoundaryKind,
    LicensingBoundaryState,
    LicensingBoundaryVerdict,
    PathKind,
    PreWeightSurface,
    RegistryDomain,
    RegistryEntry,
    RegistryLookupResult,
    RegistryLookupState,
    ResidualGovernanceVerdict,
    SyllableCandidate,
    SyllableSequenceCandidate,
    VerbalMadlulCandidate,
    WeightFitCandidate,
    WeightFitState,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
    assess_license,
    bind_dal_madlul,
    omega_governance,
    prove_contractable_unit,
    prove_dal,
    prove_verbal_madlul,
    weigh,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
)

# ---------------------------------------------------------------------------
# Test fixtures — build a DalMadlulBindingCandidate through the lawful chain
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr18-contractable-unit-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr18/kataba", kind="DECLARED_ENTRY"),
    }


def _syllable() -> SyllableCandidate:
    return SyllableCandidate(**_base("syllable", "syll-ka", "ka"), units=(("k", "a"),))


def _syllables() -> tuple[SyllableCandidate, ...]:
    return (
        _syllable(),
        SyllableCandidate(**_base("syllable", "syll-ta", "ta"), units=(("t", "a"),)),
        SyllableCandidate(**_base("syllable", "syll-ba", "ba"), units=(("b", "a"),)),
    )


def _sequence() -> SyllableSequenceCandidate:
    return SyllableSequenceCandidate(
        **_base("syllable_sequence", "seq-kataba", "ka-ta-ba"),
        syllables=_syllables(),
    )


def _boundary() -> WordBoundaryCandidate:
    return WordBoundaryCandidate(
        **_base("word_boundary", "wb-kataba", "kataba"), sequence=_sequence()
    )


def _word_carrier() -> WordCarrierCandidate:
    return WordCarrierCandidate(
        **_base("word_carrier", "wc-kataba", "kataba"), bounded_surface=_boundary()
    )


def _original_extra() -> OriginalExtraMap:
    return OriginalExtraMap(
        **_base("original_extra_map", "oem-kataba", "kataba"),
        underlying_form="kataba",
        assignments=(
            ("k", LetterStanding.ORIGINAL),
            ("t", LetterStanding.ORIGINAL),
            ("b", LetterStanding.ORIGINAL),
        ),
    )


def _operations() -> OperationTraceCandidate:
    return OperationTraceCandidate(
        **_base("operation_trace", "ops-kataba", "declared-steps"),
        steps=("declared_seq", "declared_boundary"),
    )


def _surface() -> PreWeightSurface:
    carrier = _word_carrier()
    return PreWeightSurface(
        **_base("pre_weight_surface", "pws-kataba", "kataba"),
        carrier=carrier,
        path=PathCandidate(
            **_base("path", "path-kataba", "root_path"),
            kind=PathKind.ROOT,
            carrier=carrier,
        ),
        original_extra=_original_extra(),
        operations=_operations(),
    )


def _weight_readiness() -> WeightReadinessCandidate:
    return WeightReadinessCandidate(
        **_base("weight_readiness", "wr-kataba", "kataba"),
        surface=_surface(),
    )


def _weight_fit_candidate() -> WeightFitCandidate:
    """Produce a valid WeightFitCandidate through the lawful chain."""
    candidate = _weight_readiness()
    governance = omega_governance((), Rank.CANDIDATE)
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED
    assert result.candidate is not None
    return result.candidate


def _granted_governance() -> ResidualGovernanceVerdict:
    """A GRANTED omega governance verdict with no residuals."""
    return omega_governance((), Rank.CANDIDATE)


def _lexical_evidence() -> BoundaryEvidence:
    return BoundaryEvidence(
        kind=LicenseBoundaryKind.LEXICAL,
        attestation="lexical_root_attested",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
    )


def _licensing_verdict() -> LicensingBoundaryVerdict:
    """Produce a valid LicensingBoundaryVerdict through the lawful chain."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = _lexical_evidence()
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    return result.verdict


def _dal_only_candidate() -> DalOnlyCandidate:
    """Produce a valid DalOnlyCandidate through the lawful chain."""
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "kataba", "phonetic://kataba", "graphic://kataba")
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _madlul_candidate(dal: DalOnlyCandidate) -> VerbalMadlulCandidate:
    """Produce a valid VerbalMadlulCandidate from a given DalOnlyCandidate."""
    from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState

    result = prove_verbal_madlul(
        prior_dal=dal,
        wad_usage_boundary="lexical-wadʿ-boundary",
        correspondence_candidate="correspondence/kataba",
        inclusion_candidate="inclusion/kataba",
        iltizam_condition="iltizam/kataba",
    )
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _dal_registry_proof() -> RegistryLookupResult:
    """Build a FOUND RegistryLookupResult for DAL_ONLY."""
    entry = RegistryEntry(
        key="kataba",
        domain=RegistryDomain.DAL_ONLY,
        non_meaning_proof="signifier candidacy only, not meaning",
        rank=Rank.HYPOTHESIS,
        residuals=(),
        trace_ref="registry/dal/kataba",
    )
    return RegistryLookupResult(
        state=RegistryLookupState.FOUND,
        entry=entry,
        failure_code=None,
    )


def _madlul_registry_proof() -> RegistryLookupResult:
    """Build a FOUND RegistryLookupResult for VERBAL_MADLUL."""
    entry = RegistryEntry(
        key="kataba",
        domain=RegistryDomain.VERBAL_MADLUL,
        non_meaning_proof="verbal signified candidacy only, not meaning",
        rank=Rank.HYPOTHESIS,
        residuals=(),
        trace_ref="registry/madlul/kataba",
    )
    return RegistryLookupResult(
        state=RegistryLookupState.FOUND,
        entry=entry,
        failure_code=None,
    )


def _binding_candidate() -> DalMadlulBindingCandidate:
    """Produce a valid DalMadlulBindingCandidate through the lawful chain."""
    dal = _dal_only_candidate()
    madlul = _madlul_candidate(dal)
    result = bind_dal_madlul(dal, madlul, _dal_registry_proof(), _madlul_registry_proof())
    assert result.verdict_state is BindingState.BOUND
    assert result.candidate is not None
    return result.candidate


# ---------------------------------------------------------------------------
# 1-6. Input boundary enforcement
# ---------------------------------------------------------------------------


class TestInputBoundary:
    """Tests for prove_contractable_unit() input boundary enforcement."""

    def test_non_binding_candidate_refused(self) -> None:
        """1/2. prove_contractable_unit() refuses non-DalMadlulBindingCandidate."""
        result = prove_contractable_unit(
            binding_candidate="not a candidate",  # type: ignore[arg-type]
            admissible_roles=("subject", "object"),
            blocked_roles=(),
            path_profile="root_path",
            word_class_affordance="verb",
            inflection_affordance="past_active",
            derivational_affordance="triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert result.candidate is None

    def test_empty_admissible_roles_refused(self) -> None:
        """3. prove_contractable_unit() refuses empty admissible_roles."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding_candidate=binding,
            admissible_roles=(),
            blocked_roles=(),
            path_profile="root_path",
            word_class_affordance="verb",
            inflection_affordance="past_active",
            derivational_affordance="triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None

    def test_empty_path_profile_refused(self) -> None:
        """4. prove_contractable_unit() refuses empty path_profile."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding_candidate=binding,
            admissible_roles=("subject",),
            blocked_roles=(),
            path_profile="",
            word_class_affordance="verb",
            inflection_affordance="past_active",
            derivational_affordance="triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None

    def test_empty_word_class_affordance_refused(self) -> None:
        """5. prove_contractable_unit() refuses empty word_class_affordance."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding_candidate=binding,
            admissible_roles=("subject",),
            blocked_roles=(),
            path_profile="root_path",
            word_class_affordance="",
            inflection_affordance="past_active",
            derivational_affordance="triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None

    def test_empty_inflection_affordance_refused(self) -> None:
        """6a. prove_contractable_unit() refuses empty inflection_affordance."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding_candidate=binding,
            admissible_roles=("subject",),
            blocked_roles=(),
            path_profile="root_path",
            word_class_affordance="verb",
            inflection_affordance="",
            derivational_affordance="triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None

    def test_empty_derivational_affordance_refused(self) -> None:
        """6b. prove_contractable_unit() refuses empty derivational_affordance."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding_candidate=binding,
            admissible_roles=("subject",),
            blocked_roles=(),
            path_profile="root_path",
            word_class_affordance="verb",
            inflection_affordance="past_active",
            derivational_affordance="",
        )
        assert result.verdict_state is ContractableUnitState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None


# ---------------------------------------------------------------------------
# 7-10. ContractableUnitGeometry boundary invariants
# ---------------------------------------------------------------------------


class TestBoundaryInvariants:
    """Tests proving ContractableUnitGeometry is NOT meaning/relation/composition."""

    def test_geometry_is_not_meaning(self) -> None:
        """7. ContractableUnitGeometry is not Meaning."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject", "object"), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.PROVEN
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "meaning")
        assert not hasattr(candidate, "reference")
        assert not hasattr(candidate, "denotation")
        assert not hasattr(candidate, "concept")
        assert not hasattr(candidate, "semantic_content")

    def test_geometry_carries_no_ifadah_hukm_reality(self) -> None:
        """8. ContractableUnitGeometry carries no ifadah/hukm/reality fields."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "ifadah")
        assert not hasattr(candidate, "hukm")
        assert not hasattr(candidate, "reality")
        assert not hasattr(candidate, "truth_value")
        assert not hasattr(candidate, "tanzil")

    def test_geometry_is_not_relation_candidate(self) -> None:
        """9. ContractableUnitGeometry is not RelationCandidate."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "relation")
        assert not hasattr(candidate, "nisba")
        assert not hasattr(candidate, "composition")
        assert type(candidate).__name__ == "ContractableUnitGeometry"

    def test_geometry_is_not_composition_candidate(self) -> None:
        """10. ContractableUnitGeometry is not CompositionCandidate."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "components")
        assert not hasattr(candidate, "composed_meaning")
        assert not hasattr(candidate, "proposition")


# ---------------------------------------------------------------------------
# 11. Rank is bounded
# ---------------------------------------------------------------------------


class TestRankBounding:
    """Tests proving rank is bounded by CONTRACTABLE_UNIT_RANK_CEILING."""

    def test_objecthood_rank_bounded(self) -> None:
        """11. Rank is bounded to CONTRACTABLE_UNIT_RANK_CEILING."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.PROVEN
        assert result.verdict_rank <= CONTRACTABLE_UNIT_RANK_CEILING
        assert result.candidate is not None
        assert result.candidate.objecthood_rank <= CONTRACTABLE_UNIT_RANK_CEILING

    def test_ceiling_equals_binding_ceiling(self) -> None:
        """11b. CONTRACTABLE_UNIT_RANK_CEILING == BINDING_RANK_CEILING."""
        assert CONTRACTABLE_UNIT_RANK_CEILING == BINDING_RANK_CEILING

    def test_objecthood_rank_is_meet_of_binding(self) -> None:
        """11c. Objecthood rank is RankLattice.meet of binding rank and ceiling."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.candidate is not None
        expected = RankLattice.meet(binding.binding_rank, CONTRACTABLE_UNIT_RANK_CEILING)
        assert result.candidate.objecthood_rank == expected


# ---------------------------------------------------------------------------
# 12-13. Residual governance
# ---------------------------------------------------------------------------


class TestResidualGovernance:
    """Tests proving residual governance is enforced."""

    def test_hidden_forbidden_residual_refused(self) -> None:
        """12. HIDDEN_FORBIDDEN residual triggers refusal."""
        verdict = _licensing_verdict()
        hidden_r = Residual(
            name="hidden_residual",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=True,
        )
        dal = DalOnlyCandidate(
            signifier_identity="kataba",
            phonetic_trace_ref="phonetic://kataba",
            graphic_trace_ref="graphic://kataba",
            prior_licensing_verdict=verdict,
            dal_rank=Rank.HYPOTHESIS,
            residuals=(hidden_r,),
            trace_ref="dal/hidden_test",
        )
        madlul = VerbalMadlulCandidate(
            dal_only=dal,
            wad_usage_boundary="lexical-wadʿ",
            correspondence_candidate="",
            inclusion_candidate="",
            iltizam_condition="",
            existence_carrier_candidate="",
            event_carrier_candidate="",
            relation_affordance_candidate="",
            madlul_rank=Rank.HYPOTHESIS,
            residuals=(),
            trace_ref="madlul/hidden_test",
        )
        # Build binding with hidden residual (will be refused at binding level,
        # so we construct directly)
        binding = DalMadlulBindingCandidate(
            dal_candidate=dal,
            madlul_candidate=madlul,
            dal_registry_proof=_dal_registry_proof(),
            madlul_registry_proof=_madlul_registry_proof(),
            binding_rank=Rank.HYPOTHESIS,
            residuals=(hidden_r,),
            trace_ref="binding/hidden_test",
        )
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.REFUSED
        assert result.failure_code is FailureCode.HIDDEN_RESIDUAL

    def test_blocking_residual_refused(self) -> None:
        """13. BLOCKING residual triggers refusal."""
        verdict = _licensing_verdict()
        blocking_r = Residual(
            name="blocking_residual",
            kind=ResidualKind.BLOCKING,
            visible=True,
        )
        dal = DalOnlyCandidate(
            signifier_identity="kataba",
            phonetic_trace_ref="phonetic://kataba",
            graphic_trace_ref="graphic://kataba",
            prior_licensing_verdict=verdict,
            dal_rank=Rank.HYPOTHESIS,
            residuals=(),
            trace_ref="dal/blocking_test",
        )
        madlul = VerbalMadlulCandidate(
            dal_only=dal,
            wad_usage_boundary="lexical-wadʿ",
            correspondence_candidate="",
            inclusion_candidate="",
            iltizam_condition="",
            existence_carrier_candidate="",
            event_carrier_candidate="",
            relation_affordance_candidate="",
            madlul_rank=Rank.HYPOTHESIS,
            residuals=(blocking_r,),
            trace_ref="madlul/blocking_test",
        )
        binding = DalMadlulBindingCandidate(
            dal_candidate=dal,
            madlul_candidate=madlul,
            dal_registry_proof=_dal_registry_proof(),
            madlul_registry_proof=_madlul_registry_proof(),
            binding_rank=Rank.HYPOTHESIS,
            residuals=(blocking_r,),
            trace_ref="binding/blocking_test",
        )
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.REFUSED
        assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


# ---------------------------------------------------------------------------
# 14. trace_ref remains reference
# ---------------------------------------------------------------------------


class TestTraceRef:
    """Tests proving trace_ref is a reference, not a ledger commit."""

    def test_trace_ref_is_reference(self) -> None:
        """14. trace_ref is a reference string, not a ledger commit."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.PROVEN
        assert result.candidate is not None
        assert isinstance(result.candidate.trace_ref, str)
        assert result.candidate.trace_ref.startswith("prove_contractable_unit/")
        assert "/" in result.candidate.trace_ref


# ---------------------------------------------------------------------------
# 15. Every refusal has named FailureCode
# ---------------------------------------------------------------------------


class TestFailureCodes:
    """Tests proving every refusal carries a named FailureCode."""

    def test_all_refusals_carry_failure_code(self) -> None:
        """15. Every REFUSED verdict carries a named FailureCode."""
        binding = _binding_candidate()
        cases = [
            # Invalid binding_candidate
            prove_contractable_unit(
                "bad", ("subject",), (), "root_path",  # type: ignore[arg-type]
                "verb", "past_active", "triliteral_basic",
            ),
            # Empty admissible_roles
            prove_contractable_unit(
                binding, (), (), "root_path",
                "verb", "past_active", "triliteral_basic",
            ),
            # Empty path_profile
            prove_contractable_unit(
                binding, ("subject",), (), "",
                "verb", "past_active", "triliteral_basic",
            ),
            # Empty word_class_affordance
            prove_contractable_unit(
                binding, ("subject",), (), "root_path",
                "", "past_active", "triliteral_basic",
            ),
        ]
        for verdict in cases:
            assert verdict.verdict_state is ContractableUnitState.REFUSED
            assert verdict.failure_code is not None
            assert isinstance(verdict.failure_code, FailureCode)


# ---------------------------------------------------------------------------
# 16. Forbidden imports
# ---------------------------------------------------------------------------


class TestForbiddenImports:
    """Tests proving PR-18 module does not import forbidden symbols."""

    def test_no_forbidden_symbols_in_module(self) -> None:
        """16. PR-18 imports/defines no forbidden symbols."""
        src = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/contractable_unit_geometry.py"
        ).read_text()
        tree = ast.parse(src)

        forbidden_names = {
            "ExtraLetterLicense",
            "C_Aug",
            "Ifadah",
            "IfadahCandidate",
            "Hukm",
            "HukmCandidate",
            "Reality",
            "RealityCandidate",
            "TanzilCandidate",
            "RelationCandidate",
            "CompositionCandidate",
            "LexicalMadlul",
            "SemanticVerdict",
            "SyntaxRole",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    assert alias.name not in forbidden_names, (
                        f"PR-18 module must not import {alias.name}"
                    )
            elif isinstance(node, ast.ClassDef):
                assert node.name not in forbidden_names, (
                    f"PR-18 module must not define {node.name}"
                )


# ---------------------------------------------------------------------------
# 17. ContractabilityProfile is affordance, not SyntaxRole
# ---------------------------------------------------------------------------


class TestContractabilityProfile:
    """Tests proving ContractabilityProfile is affordance, not assignment."""

    def test_profile_has_affordance_fields(self) -> None:
        """17. ContractabilityProfile carries affordance fields only."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject", "object"), ("predicate",), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.candidate is not None
        profile = result.candidate.contractability_profile
        assert isinstance(profile, ContractabilityProfile)
        assert profile.admissible_roles == ("subject", "object")
        assert profile.blocked_roles == ("predicate",)
        assert profile.path_profile == "root_path"
        assert profile.word_class_affordance == "verb"
        assert profile.inflection_affordance == "past_active"
        assert profile.derivational_affordance == "triliteral_basic"
        # Affordance: no SyntaxRole, no final assignment
        assert not hasattr(profile, "syntax_role")
        assert not hasattr(profile, "assigned_role")
        assert not hasattr(profile, "grammatical_function")


# ---------------------------------------------------------------------------
# Happy path — full contractable unit success
# ---------------------------------------------------------------------------


class TestHappyPath:
    """Test the complete happy path through prove_contractable_unit()."""

    def test_successful_contractable_unit(self) -> None:
        """Full happy path: valid inputs produce PROVEN verdict."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding_candidate=binding,
            admissible_roles=("subject", "object"),
            blocked_roles=("predicate",),
            path_profile="root_path",
            word_class_affordance="verb",
            inflection_affordance="past_active",
            derivational_affordance="triliteral_basic",
        )
        assert result.verdict_state is ContractableUnitState.PROVEN
        assert result.failure_code is None
        assert result.candidate is not None
        assert isinstance(result.candidate, ContractableUnitGeometry)
        assert result.candidate.binding_candidate is binding
        assert result.candidate.unit_identity == "kataba"
        assert result.verdict_rank <= CONTRACTABLE_UNIT_RANK_CEILING

    def test_geometry_is_frozen(self) -> None:
        """ContractableUnitGeometry is frozen (immutable)."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.candidate is not None
        with pytest.raises(AttributeError):
            result.candidate.objecthood_rank = Rank.ZERO  # type: ignore[misc]

    def test_profile_is_frozen(self) -> None:
        """ContractabilityProfile is frozen (immutable)."""
        binding = _binding_candidate()
        result = prove_contractable_unit(
            binding, ("subject",), (), "root_path",
            "verb", "past_active", "triliteral_basic",
        )
        assert result.candidate is not None
        with pytest.raises(AttributeError):
            result.candidate.contractability_profile.path_profile = "x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Carrier schema enforcement
# ---------------------------------------------------------------------------


class TestCarrierSchema:
    """Tests for ContractableUnitGeometry carrier schema enforcement."""

    def test_geometry_schema_rejects_invalid_binding(self) -> None:
        """Direct construction with invalid binding_candidate raises."""
        with pytest.raises(WeightCarrierSchemaError):
            ContractableUnitGeometry(
                binding_candidate="not valid",  # type: ignore[arg-type]
                unit_identity="kataba",
                contractability_profile=ContractabilityProfile(
                    admissible_roles=("subject",),
                    blocked_roles=(),
                    path_profile="root_path",
                    word_class_affordance="verb",
                    inflection_affordance="past_active",
                    derivational_affordance="triliteral_basic",
                ),
                objecthood_rank=Rank.HYPOTHESIS,
                residuals=(),
                trace_ref="test/schema",
            )

    def test_verdict_schema_enforces_proven_state(self) -> None:
        """PROVEN verdict without candidate raises WeightCarrierSchemaError."""
        with pytest.raises(WeightCarrierSchemaError):
            ContractableUnitVerdict(
                candidate=None,
                verdict_state=ContractableUnitState.PROVEN,
                failure_code=None,
                verdict_rank=Rank.HYPOTHESIS,
                residuals=(),
                trace_ref="test/invalid",
            )

    def test_verdict_schema_enforces_refused_state(self) -> None:
        """REFUSED verdict without failure_code raises WeightCarrierSchemaError."""
        with pytest.raises(WeightCarrierSchemaError):
            ContractableUnitVerdict(
                candidate=None,
                verdict_state=ContractableUnitState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.HYPOTHESIS,
                residuals=(),
                trace_ref="test/invalid",
            )
