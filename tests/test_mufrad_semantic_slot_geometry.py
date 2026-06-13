"""Constitutional tests for PR-D1: Mufrad Semantic Slot Geometry.

Origin law: docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md.

This test module proves:
1. prove_mufrad_semantic_slot_geometry() returns PROVEN with valid inputs.
2. SemanticSlotFrame ≠ meaning / dalalah / ifadah.
3. WadEvidenceCarrier ≠ lexical meaning.
4. KulliJuziiAxisVerdict is a verdict, not a label.
5. BranchLinkCandidate ≠ qiyas result / free reasoning.
6. All five semantic categories are readiness, not meaning.
7. prove refuses invalid FormalStyleCandidate type.
8. prove refuses invalid DalOnlyCandidate type.
9. prove refuses invalid VerbalMadlulCandidate type.
10. prove refuses invalid ContractableUnitGeometry type.
11. prove refuses non-CLOSED formal shape.
12. prove refuses invalid semantic category.
13. prove refuses empty string fields.
14. Rank never exceeds SEMANTIC_SLOT_GEOMETRY_RANK_CEILING.
15. All 16 required deferred residuals are present, visible, EXPLANATORY.
16. Every verdict carries trace_ref.
17. Sub-carriers (Wad, Profile, Axis, Branch) have birth guards.
18. PR-D1 does not export forbidden symbols.
19. prove refuses invalid wad/kulli/branch types.
20. PROVEN/REFUSED verdict invariants hold.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    BindingState,
    BoundaryEvidence,
    ContractableUnitGeometry,
    ContractableUnitState,
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
from taaqqul_slot_geometry.weight.formal_shape import (
    FormalShapeClosureState,
)
from taaqqul_slot_geometry.weight.formal_style_candidate import (
    FormalStyleCandidate,
    FormalStyleFamily,
    FormalStyleState,
    prove_formal_style_candidate,
)
from taaqqul_slot_geometry.weight.mufrad_semantic_slot_geometry import (
    SEMANTIC_CATEGORIES,
    SEMANTIC_SLOT_GEOMETRY_RANK_CEILING,
    BranchLinkCandidate,
    KulliJuziiAxis,
    KulliJuziiAxisVerdict,
    MufradSemanticSlotGeometryVerdict,
    MufradSemanticState,
    ParticularitySource,
    PerUnitFormalProfileClosure,
    SemanticCategory,
    SemanticSlotFrame,
    WadEvidenceCarrier,
    WadEvidenceType,
    WadOriginDomain,
    prove_mufrad_semantic_slot_geometry,
)
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
)
from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

# ===========================================================================
# Required deferred residual names
# ===========================================================================

REQUIRED_DEFERRED_RESIDUAL_NAMES = (
    "SEMANTIC_SLOT_GEOMETRY_NOT_DALALAH",
    "MUTABAQAH_DEFERRED_TO_PR_D2",
    "TADAMMUN_DEFERRED_TO_PR_D2",
    "ILTIZAM_DEFERRED_TO_PR_D2",
    "MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3",
    "IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE",
    "MANTUQ_DEFERRED_UNTIL_IFADAH",
    "MAFHUM_DEFERRED_UNTIL_MANTUQ",
    "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
    "MANQUL_DEFERRED_UNTIL_TRANSFER_GATE",
    "TAWATUI_READINESS",
    "TASHKIK_READINESS",
    "TABAYUN_READINESS",
    "TARADUF_READINESS",
    "ISHTIRAK_READINESS",
    "NAQL_READINESS",
)

# Forbidden symbols that PR-D1 must NOT export or instantiate.
FORBIDDEN_SYMBOLS = (
    "MutabaqahCandidate",
    "TadammunCandidate",
    "IltizamCandidate",
    "IfadahCandidate",
    "HukmCandidate",
    "Meaning",
    "MantuqClosure",
    "MafhumCandidate",
    "TanzilCandidate",
)

# ===========================================================================
# Test fixtures — build prior-layer candidates through the lawful chain
# ===========================================================================


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr-d1-semantic-slot-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr-d1/kataba", kind="DECLARED_ENTRY"),
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
    candidate = _weight_readiness()
    governance = omega_governance((), Rank.CANDIDATE)
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED
    assert result.candidate is not None
    return result.candidate


def _licensing_verdict() -> LicensingBoundaryVerdict:
    fit = _weight_fit_candidate()
    governance = omega_governance((), Rank.CANDIDATE)
    evidence = BoundaryEvidence(
        kind=LicenseBoundaryKind.LEXICAL,
        attestation="lexical_root_attested",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
    )
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    return result.verdict


def _dal_only_candidate() -> DalOnlyCandidate:
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "kataba", "phonetic://kataba", "graphic://kataba")
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _madlul_candidate(dal: DalOnlyCandidate) -> VerbalMadlulCandidate:
    result = prove_verbal_madlul(
        prior_dal=dal,
        wad_usage_boundary="lexical-wad-boundary",
        correspondence_candidate="correspondence/kataba",
        inclusion_candidate="inclusion/kataba",
        iltizam_condition="iltizam/kataba",
    )
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _dal_registry_proof() -> RegistryLookupResult:
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
    dal = _dal_only_candidate()
    madlul = _madlul_candidate(dal)
    result = bind_dal_madlul(dal, madlul, _dal_registry_proof(), _madlul_registry_proof())
    assert result.verdict_state is BindingState.BOUND
    assert result.candidate is not None
    return result.candidate


def _contractable_unit() -> ContractableUnitGeometry:
    binding = _binding_candidate()
    result = prove_contractable_unit(
        binding_candidate=binding,
        admissible_roles=("subject", "object"),
        blocked_roles=(),
        path_profile="root_path",
        word_class_affordance="verb",
        inflection_affordance="past_active",
        derivational_affordance="triliteral_basic",
    )
    assert result.verdict_state is ContractableUnitState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _formal_style_candidate() -> FormalStyleCandidate:
    verdict = prove_formal_style_candidate(
        style_family=FormalStyleFamily.DECLARATIVE_STYLE_FORM,
        composition_evidence_ref="test/composition/khabar",
        formal_closure_state=FormalShapeClosureState.CLOSED,
        formal_closure_ref="test/closure/CLOSED",
    )
    assert verdict.verdict_state is FormalStyleState.PROVEN
    assert verdict.candidate is not None
    return verdict.candidate


def _proven_verdict(
    *,
    semantic_category: SemanticCategory = SemanticCategory.JAMID,
) -> MufradSemanticSlotGeometryVerdict:
    """Build a PROVEN verdict through the lawful chain."""
    dal = _dal_only_candidate()
    madlul = _madlul_candidate(dal)
    unit = _contractable_unit()
    style = _formal_style_candidate()

    return prove_mufrad_semantic_slot_geometry(
        formal_style_candidate=style,
        dal_only_candidate=dal,
        verbal_madlul_candidate=madlul,
        contractable_unit=unit,
        formal_closure_state=FormalShapeClosureState.CLOSED,
        semantic_category=semantic_category,
        wad_origin_domain=WadOriginDomain.LUGHAWI,
        wad_evidence_type=WadEvidenceType.SAMA,
        wad_scope="arabic_lexical",
        wad_evidence_ref="wad/kataba/sama",
        word_class_closure_ref="word_class/ISM/closed",
        weight_pattern_closure_ref="weight/fail/closed",
        inflection_closure_ref="inflection/murab/closed",
        contract_slot_readiness_ref="contract/subject/closed",
        composition_participation_ref="composition/nominal/closed",
        kulli_juzii_axis=KulliJuziiAxis.KULLI,
        particularity_source=ParticularitySource.NOT_APPLICABLE,
        predication_test_passed=True,
        reference_resolution_status="not_applicable",
        branch_origin_ref="origin/kataba/root",
        branch_ref="branch/kataba/derived",
        branch_relation_type="morphological_derivation",
        branch_illa_jamia="shared_root_pattern",
        branch_evidence_ref="evidence/kataba/root_attestation",
        branch_domain_compatibility="arabic_morphophonology",
        branch_no_preventer=True,
        naql_readiness="naql_not_applicable",
        majaz_readiness="majaz_not_applicable",
    )


# ===========================================================================
# Test 1: prove returns PROVEN with valid inputs
# ===========================================================================


class TestProvenVerdict:
    """prove_mufrad_semantic_slot_geometry() returns PROVEN with valid inputs."""

    @pytest.mark.parametrize(
        "category",
        SEMANTIC_CATEGORIES,
        ids=[c.value for c in SEMANTIC_CATEGORIES],
    )
    def test_proven_for_each_semantic_category(
        self, category: SemanticCategory
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name=f"prove({category.value}) returns PROVEN",
            constitutional_chain=(
                "prove_mufrad_semantic_slot_geometry", "Verdict", "Rank", "Trace",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Ifadah", "HukmCandidate", "Dalalah"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict(semantic_category=category)

        assert verdict.verdict_state is MufradSemanticState.PROVEN
        assert verdict.failure_code is None
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate, SemanticSlotFrame)
        assert verdict.candidate.semantic_category is category
        assert verdict.verdict_rank <= SEMANTIC_SLOT_GEOMETRY_RANK_CEILING
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
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)

    def test_proven_frame_carries_identity_continuity(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="SemanticSlotFrame carries identity continuity refs",
            constitutional_chain=(
                "prove_mufrad_semantic_slot_geometry", "IdentityContinuity",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert verdict.candidate is not None
        frame = verdict.candidate

        # Identity continuity: all refs are non-empty strings
        assert isinstance(frame.dal_identity_ref, str)
        assert frame.dal_identity_ref.strip()
        assert isinstance(frame.verbal_madlul_ref, str)
        assert frame.verbal_madlul_ref.strip()
        assert isinstance(frame.contractable_unit_ref, str)
        assert frame.contractable_unit_ref.strip()
        assert isinstance(frame.formal_shape_ref, str)
        assert frame.formal_shape_ref.strip()
        assert isinstance(frame.formal_style_ref, str)
        assert frame.formal_style_ref.strip()

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 2: SemanticSlotFrame ≠ meaning / dalalah / ifadah
# ===========================================================================


class TestSemanticSlotFrameNotMeaning:
    """SemanticSlotFrame is geometry, never meaning."""

    def test_frame_does_not_carry_meaning_fields(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="SemanticSlotFrame ≠ meaning",
            constitutional_chain=("SemanticSlotFrame", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "Dalalah", "Ifadah", "Hukm"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert verdict.candidate is not None
        frame = verdict.candidate

        # SemanticSlotFrame must not have fields for meaning content
        field_names = {f for f in frame.__dataclass_fields__}
        forbidden_field_names = {
            "meaning", "dalalah", "ifadah", "hukm",
            "mantuq", "mafhum", "majaz_result", "manqul_result",
            "truth_value", "semantic_content", "dictionary_definition",
        }
        present = field_names & forbidden_field_names
        assert not present, f"Forbidden meaning fields present: {present}"

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 3: WadEvidenceCarrier ≠ lexical meaning
# ===========================================================================


class TestWadEvidenceNotMeaning:
    """WadEvidenceCarrier is evidence classification, not meaning."""

    def test_wad_evidence_has_no_meaning_fields(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="WadEvidenceCarrier ≠ lexical meaning",
            constitutional_chain=("WadEvidenceCarrier", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "DictionaryDefinition"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert verdict.candidate is not None
        wad = verdict.candidate.wad_evidence

        field_names = {f for f in wad.__dataclass_fields__}
        forbidden = {"meaning", "definition", "lexical_content", "semantic_value"}
        present = field_names & forbidden
        assert not present, f"Forbidden meaning fields in WadEvidence: {present}"

        # WadEvidence fields are evidence classification
        assert isinstance(wad.origin_domain, WadOriginDomain)
        assert isinstance(wad.evidence_type, WadEvidenceType)
        assert wad.scope.strip()
        assert wad.evidence_ref.strip()

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"WadEvidenceCarrier"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 4: KulliJuziiAxisVerdict is a verdict, not a label
# ===========================================================================


class TestKulliJuziiIsVerdict:
    """KulliJuziiAxisVerdict is a verdict with tests, not a bare label."""

    def test_kulli_verdict_has_predication_test(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="KulliJuziiAxisVerdict is verdict, not label",
            constitutional_chain=("KulliJuziiAxisVerdict", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("OntologicalClaim",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert verdict.candidate is not None
        axis_verdict = verdict.candidate.kulli_juzii_axis

        # It carries structural fields for a verdict, not just a label
        assert isinstance(axis_verdict.axis, KulliJuziiAxis)
        assert isinstance(axis_verdict.particularity_source, ParticularitySource)
        assert isinstance(axis_verdict.predication_test_passed, bool)
        assert axis_verdict.reference_resolution_status.strip()
        assert axis_verdict.trace_ref.strip()

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"KulliJuziiAxisVerdict"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 5: BranchLinkCandidate ≠ qiyas result / free reasoning
# ===========================================================================


class TestBranchLinkNotQiyas:
    """BranchLinkCandidate is origin/branch geometry, not qiyas."""

    def test_branch_link_has_illa_and_preventer(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="BranchLinkCandidate ≠ qiyas result",
            constitutional_chain=("BranchLinkCandidate", "Invariant"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("QiyasResult", "FreeReasoning"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert verdict.candidate is not None
        branch = verdict.candidate.branch_link

        # Structural fields for branch geometry
        assert branch.origin_ref.strip()
        assert branch.branch_ref.strip()
        assert branch.relation_type.strip()
        assert branch.illa_jamia.strip()  # 'illa jamia evidence
        assert branch.evidence_ref.strip()
        assert branch.domain_compatibility.strip()
        assert isinstance(branch.no_preventer, bool)
        assert isinstance(branch.rank, Rank)
        assert branch.trace_ref.strip()

        # No meaning fields
        field_names = {f for f in branch.__dataclass_fields__}
        forbidden = {"meaning", "qiyas_result", "hukm", "semantic_conclusion"}
        present = field_names & forbidden
        assert not present, f"Forbidden fields in BranchLink: {present}"

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"BranchLinkCandidate"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 6: All five semantic categories are readiness, not meaning
# ===========================================================================


class TestSemanticCategoriesAreReadiness:
    """Each SemanticCategory is readiness classification, not meaning."""

    def test_all_five_categories_exist(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="All 5 SemanticCategory members exist",
            constitutional_chain=("SemanticCategory", "Completeness"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        expected = {"JAMID", "MASDAR", "MUSHTAQ", "HARF", "REFERENCE"}
        actual = {c.value for c in SemanticCategory}
        assert actual == expected

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticCategory"}),
        )
        assert_constitutional_case(case, result)

    @pytest.mark.parametrize(
        "category",
        SEMANTIC_CATEGORIES,
        ids=[c.value for c in SEMANTIC_CATEGORIES],
    )
    def test_category_produces_proven_verdict(
        self, category: SemanticCategory
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name=f"{category.value} produces PROVEN verdict",
            constitutional_chain=(
                "prove_mufrad_semantic_slot_geometry", "SemanticCategory",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict(semantic_category=category)
        assert verdict.verdict_state is MufradSemanticState.PROVEN
        assert verdict.candidate is not None
        assert verdict.candidate.semantic_category is category

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 7-12: prove refuses invalid inputs
# ===========================================================================


class TestProveRefusals:
    """prove_mufrad_semantic_slot_geometry() refuses invalid inputs."""

    def _base_kwargs(self) -> dict[str, object]:
        """Baseline valid kwargs for prove_mufrad_semantic_slot_geometry."""
        return dict(
            formal_style_candidate=_formal_style_candidate(),
            dal_only_candidate=_dal_only_candidate(),
            verbal_madlul_candidate=_madlul_candidate(_dal_only_candidate()),
            contractable_unit=_contractable_unit(),
            formal_closure_state=FormalShapeClosureState.CLOSED,
            semantic_category=SemanticCategory.JAMID,
            wad_origin_domain=WadOriginDomain.LUGHAWI,
            wad_evidence_type=WadEvidenceType.SAMA,
            wad_scope="arabic_lexical",
            wad_evidence_ref="wad/kataba/sama",
            word_class_closure_ref="word_class/ISM/closed",
            weight_pattern_closure_ref="weight/fail/closed",
            inflection_closure_ref="inflection/murab/closed",
            contract_slot_readiness_ref="contract/subject/closed",
            composition_participation_ref="composition/nominal/closed",
            kulli_juzii_axis=KulliJuziiAxis.KULLI,
            particularity_source=ParticularitySource.NOT_APPLICABLE,
            predication_test_passed=True,
            reference_resolution_status="not_applicable",
            branch_origin_ref="origin/kataba/root",
            branch_ref="branch/kataba/derived",
            branch_relation_type="morphological_derivation",
            branch_illa_jamia="shared_root_pattern",
            branch_evidence_ref="evidence/kataba/root_attestation",
            branch_domain_compatibility="arabic_morphophonology",
            branch_no_preventer=True,
            naql_readiness="naql_not_applicable",
            majaz_readiness="majaz_not_applicable",
        )

    def test_refuses_invalid_formal_style_type(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses invalid FormalStyleCandidate type",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["formal_style_candidate"] = "not_a_candidate"
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_invalid_dal_only_type(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses invalid DalOnlyCandidate type",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["dal_only_candidate"] = "not_a_candidate"
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_invalid_verbal_madlul_type(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses invalid VerbalMadlulCandidate type",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["verbal_madlul_candidate"] = "not_a_candidate"
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_invalid_contractable_unit_type(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses invalid ContractableUnitGeometry type",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["contractable_unit"] = "not_a_candidate"
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_non_closed_formal_shape(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses non-CLOSED FormalShapeClosureState",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["formal_closure_state"] = FormalShapeClosureState.PARTIAL
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_invalid_semantic_category(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses invalid semantic category",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["semantic_category"] = "NOT_A_CATEGORY"
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_empty_wad_scope(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses empty wad_scope",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["wad_scope"] = ""
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_empty_branch_illa_jamia(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses empty branch_illa_jamia",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["branch_illa_jamia"] = ""
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_invalid_wad_origin_domain(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses invalid WadOriginDomain",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["wad_origin_domain"] = "INVALID"
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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

    def test_refuses_invalid_kulli_juzii_axis(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="prove refuses invalid KulliJuziiAxis",
            constitutional_chain=("prove_mufrad_semantic_slot_geometry", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        kwargs = self._base_kwargs()
        kwargs["kulli_juzii_axis"] = "INVALID"
        verdict = prove_mufrad_semantic_slot_geometry(**kwargs)  # type: ignore[arg-type]
        assert verdict.verdict_state is MufradSemanticState.REFUSED
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


# ===========================================================================
# Test 13: Rank governance
# ===========================================================================


class TestRankGovernance:
    """Rank never exceeds SEMANTIC_SLOT_GEOMETRY_RANK_CEILING."""

    @pytest.mark.parametrize(
        "category",
        SEMANTIC_CATEGORIES,
        ids=[c.value for c in SEMANTIC_CATEGORIES],
    )
    def test_verdict_rank_within_ceiling(
        self, category: SemanticCategory
    ) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name=f"{category.value} rank ≤ SEMANTIC_SLOT_GEOMETRY_RANK_CEILING",
            constitutional_chain=("SemanticSlotFrame", "Rank", "Ceiling"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("RankPromotion",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )
        verdict = _proven_verdict(semantic_category=category)
        assert verdict.verdict_rank <= SEMANTIC_SLOT_GEOMETRY_RANK_CEILING
        assert verdict.candidate is not None
        assert verdict.candidate.rank <= SEMANTIC_SLOT_GEOMETRY_RANK_CEILING
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)

    def test_schema_refuses_rank_above_ceiling(self) -> None:
        """SemanticSlotFrame refuses rank above ceiling at birth."""
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="SemanticSlotFrame refuses rank above ceiling",
            constitutional_chain=("SemanticSlotFrame", "SchemaGuard"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            forbidden_outputs=("RankPromotion",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )

        # Build valid sub-carriers first
        verdict = _proven_verdict()
        assert verdict.candidate is not None
        frame = verdict.candidate

        with pytest.raises(WeightCarrierSchemaError):
            SemanticSlotFrame(
                dal_identity_ref=frame.dal_identity_ref,
                verbal_madlul_ref=frame.verbal_madlul_ref,
                contractable_unit_ref=frame.contractable_unit_ref,
                formal_shape_ref=frame.formal_shape_ref,
                formal_style_ref=frame.formal_style_ref,
                wad_evidence=frame.wad_evidence,
                per_unit_profile=frame.per_unit_profile,
                kulli_juzii_axis=frame.kulli_juzii_axis,
                branch_link=frame.branch_link,
                naql_readiness="naql_stub",
                majaz_readiness="majaz_stub",
                semantic_category=SemanticCategory.JAMID,
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
# Test 14: All 16 required deferred residuals
# ===========================================================================


class TestDeferredResiduals:
    """All 16 required deferred residuals are present, visible, EXPLANATORY."""

    def test_all_16_deferred_residuals_present(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="SemanticSlotFrame carries all 16 deferred residuals",
            constitutional_chain=("SemanticSlotFrame", "Residual", "Governance"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("HiddenResidual",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert verdict.candidate is not None

        residual_names = {r.name for r in verdict.residuals}
        for required_name in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert required_name in residual_names, (
                f"Missing required deferred residual: {required_name}"
            )

        # All residuals must be EXPLANATORY and visible
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY, (
                f"Residual {r.name} is {r.kind}, expected EXPLANATORY"
            )
            assert r.visible is True, (
                f"Residual {r.name} is not visible"
            )

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)

    def test_exactly_16_deferred_residuals(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="SemanticSlotFrame carries exactly 16 deferred residuals",
            constitutional_chain=("SemanticSlotFrame", "Residual", "Count"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("HiddenResidual",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert len(verdict.residuals) == 16

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 15: Every verdict carries trace_ref
# ===========================================================================


class TestTraceRef:
    """Every verdict and carrier carries a non-empty trace_ref."""

    def test_proven_verdict_has_trace(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="PROVEN verdict has trace_ref",
            constitutional_chain=("MufradSemanticSlotGeometryVerdict", "Trace"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert verdict.trace_ref.strip()
        assert verdict.candidate is not None
        assert verdict.candidate.trace_ref.strip()
        # Sub-carriers also carry trace
        assert verdict.candidate.wad_evidence.trace_ref.strip()
        assert verdict.candidate.per_unit_profile.trace_ref.strip()
        assert verdict.candidate.kulli_juzii_axis.trace_ref.strip()
        assert verdict.candidate.branch_link.trace_ref.strip()

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)

    def test_refused_verdict_has_trace(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="REFUSED verdict has trace_ref",
            constitutional_chain=("MufradSemanticSlotGeometryVerdict", "Trace"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )

        verdict = prove_mufrad_semantic_slot_geometry(
            formal_style_candidate="invalid",  # type: ignore[arg-type]
            dal_only_candidate="invalid",  # type: ignore[arg-type]
            verbal_madlul_candidate="invalid",  # type: ignore[arg-type]
            contractable_unit="invalid",  # type: ignore[arg-type]
            formal_closure_state=FormalShapeClosureState.CLOSED,
            semantic_category=SemanticCategory.JAMID,
            wad_origin_domain=WadOriginDomain.LUGHAWI,
            wad_evidence_type=WadEvidenceType.SAMA,
            wad_scope="scope",
            wad_evidence_ref="ref",
            word_class_closure_ref="ref",
            weight_pattern_closure_ref="ref",
            inflection_closure_ref="ref",
            contract_slot_readiness_ref="ref",
            composition_participation_ref="ref",
            kulli_juzii_axis=KulliJuziiAxis.KULLI,
            particularity_source=ParticularitySource.NOT_APPLICABLE,
            predication_test_passed=True,
            reference_resolution_status="na",
            branch_origin_ref="origin",
            branch_ref="branch",
            branch_relation_type="type",
            branch_illa_jamia="illa",
            branch_evidence_ref="evidence",
            branch_domain_compatibility="domain",
            branch_no_preventer=True,
            naql_readiness="naql",
            majaz_readiness="majaz",
        )
        assert verdict.verdict_state is MufradSemanticState.REFUSED
        assert verdict.trace_ref.strip()

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
# Test 16: Sub-carrier birth guards
# ===========================================================================


class TestSubCarrierBirthGuards:
    """Sub-carriers enforce birth guards."""

    def test_wad_evidence_refuses_invalid_origin_domain(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="WadEvidenceCarrier refuses invalid origin_domain",
            constitutional_chain=("WadEvidenceCarrier", "SchemaGuard"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        with pytest.raises(WeightCarrierSchemaError):
            WadEvidenceCarrier(
                origin_domain="INVALID",  # type: ignore[arg-type]
                evidence_type=WadEvidenceType.SAMA,
                scope="scope",
                evidence_ref="ref",
                rank=Rank.ZERO,
                residuals=(),
                trace_ref="trace",
            )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=Rank.ZERO,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_per_unit_profile_refuses_empty_ref(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="PerUnitFormalProfileClosure refuses empty ref",
            constitutional_chain=("PerUnitFormalProfileClosure", "SchemaGuard"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        with pytest.raises(WeightCarrierSchemaError):
            PerUnitFormalProfileClosure(
                word_class_closure_ref="",
                weight_pattern_closure_ref="valid",
                inflection_closure_ref="valid",
                contract_slot_readiness_ref="valid",
                composition_participation_ref="valid",
                trace_ref="trace",
            )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=Rank.ZERO,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_kulli_juzii_refuses_invalid_axis(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="KulliJuziiAxisVerdict refuses invalid axis",
            constitutional_chain=("KulliJuziiAxisVerdict", "SchemaGuard"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        with pytest.raises(WeightCarrierSchemaError):
            KulliJuziiAxisVerdict(
                axis="INVALID",  # type: ignore[arg-type]
                particularity_source=ParticularitySource.NOT_APPLICABLE,
                predication_test_passed=True,
                reference_resolution_status="na",
                trace_ref="trace",
            )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=Rank.ZERO,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_branch_link_refuses_empty_illa_jamia(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="BranchLinkCandidate refuses empty illa_jamia",
            constitutional_chain=("BranchLinkCandidate", "SchemaGuard"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        with pytest.raises(WeightCarrierSchemaError):
            BranchLinkCandidate(
                origin_ref="origin",
                branch_ref="branch",
                relation_type="type",
                illa_jamia="",  # empty
                evidence_ref="evidence",
                domain_compatibility="domain",
                no_preventer=True,
                rank=Rank.ZERO,
                residuals=(),
                trace_ref="trace",
            )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=Rank.ZERO,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_branch_link_refuses_rank_above_ceiling(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="BranchLinkCandidate refuses rank above ceiling",
            constitutional_chain=("BranchLinkCandidate", "SchemaGuard"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.RANK_EXCEEDS_CEILING,
            forbidden_outputs=("RankPromotion",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        with pytest.raises(WeightCarrierSchemaError):
            BranchLinkCandidate(
                origin_ref="origin",
                branch_ref="branch",
                relation_type="type",
                illa_jamia="shared_root",
                evidence_ref="evidence",
                domain_compatibility="domain",
                no_preventer=True,
                rank=Rank.HYPOTHESIS,  # Above ceiling
                residuals=(),
                trace_ref="trace",
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
# Test 17: PR-D1 does not export forbidden symbols
# ===========================================================================


class TestForbiddenExports:
    """PR-D1 module does not export or instantiate forbidden symbols."""

    def test_module_has_no_forbidden_exports(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="PR-D1 module has no forbidden exports",
            constitutional_chain=("Module", "ForbiddenExports"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=tuple(FORBIDDEN_SYMBOLS),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        module_path = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/mufrad_semantic_slot_geometry.py"
        )
        source = module_path.read_text()
        tree = ast.parse(source)

        # Check class definitions
        class_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        }
        for forbidden in FORBIDDEN_SYMBOLS:
            assert forbidden not in class_names, (
                f"PR-D1 module defines forbidden class: {forbidden}"
            )

        # Check that forbidden names don't appear in __all__
        from taaqqul_slot_geometry.weight.mufrad_semantic_slot_geometry import (
            __all__ as module_all,
        )
        for forbidden in FORBIDDEN_SYMBOLS:
            assert forbidden not in module_all, (
                f"PR-D1 module exports forbidden symbol: {forbidden}"
            )

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=Rank.CANDIDATE,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 18: PROVEN/REFUSED verdict invariants
# ===========================================================================


class TestVerdictInvariants:
    """MufradSemanticSlotGeometryVerdict enforces state invariants."""

    def test_proven_verdict_must_have_candidate(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="PROVEN verdict must have candidate",
            constitutional_chain=("MufradSemanticSlotGeometryVerdict", "Invariant"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        with pytest.raises(WeightCarrierSchemaError):
            MufradSemanticSlotGeometryVerdict(
                candidate=None,  # Invalid for PROVEN
                verdict_state=MufradSemanticState.PROVEN,
                failure_code=None,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="test/trace",
            )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=Rank.ZERO,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_refused_verdict_must_have_failure_code(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="REFUSED verdict must have failure_code",
            constitutional_chain=("MufradSemanticSlotGeometryVerdict", "Invariant"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        with pytest.raises(WeightCarrierSchemaError):
            MufradSemanticSlotGeometryVerdict(
                candidate=None,
                verdict_state=MufradSemanticState.REFUSED,
                failure_code=None,  # Invalid for REFUSED
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="test/trace",
            )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=Rank.ZERO,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_refused_verdict_must_not_have_candidate(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="REFUSED verdict must not have candidate",
            constitutional_chain=("MufradSemanticSlotGeometryVerdict", "Invariant"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            forbidden_outputs=("Meaning",),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=False,
        )
        # Build a valid frame to try to attach to a REFUSED verdict
        verdict = _proven_verdict()
        assert verdict.candidate is not None

        with pytest.raises(WeightCarrierSchemaError):
            MufradSemanticSlotGeometryVerdict(
                candidate=verdict.candidate,  # Invalid for REFUSED
                verdict_state=MufradSemanticState.REFUSED,
                failure_code=FailureCode.GATE_REQUIRED,
                verdict_rank=Rank.ZERO,
                residuals=(),
                trace_ref="test/trace",
            )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            rank=Rank.ZERO,
            residual_visibility=False,
            trace_present=True,
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 19: Inter-frame relation readiness stubs
# ===========================================================================


class TestInterFrameRelationStubs:
    """Inter-frame relation readiness stubs are present as EXPLANATORY residuals."""

    RELATION_STUBS = (
        "TAWATUI_READINESS",
        "TASHKIK_READINESS",
        "TABAYUN_READINESS",
        "TARADUF_READINESS",
        "ISHTIRAK_READINESS",
        "NAQL_READINESS",
    )

    def test_all_relation_stubs_present(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="All 6 inter-frame relation readiness stubs present",
            constitutional_chain=("SemanticSlotFrame", "InterFrameStubs"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Meaning", "SemanticRelation"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        residual_names = {r.name for r in verdict.residuals}

        for stub in self.RELATION_STUBS:
            assert stub in residual_names, (
                f"Missing inter-frame relation readiness stub: {stub}"
            )

        # Each stub must be EXPLANATORY and visible
        for r in verdict.residuals:
            if r.name in self.RELATION_STUBS:
                assert r.kind is ResidualKind.EXPLANATORY
                assert r.visible is True

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 20: Naql/Majaz readiness strings
# ===========================================================================


class TestReadinessStrings:
    """Naql and majaz readiness are carried as strings, not operations."""

    def test_naql_majaz_readiness_are_strings(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/36_MUFRAD_SEMANTIC_SLOT_GEOMETRY_LAW.md",
            branch_name="naql/majaz readiness are strings, not operations",
            constitutional_chain=("SemanticSlotFrame", "ReadinessStrings"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Naql", "Majaz"),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_verdict()
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate.naql_readiness, str)
        assert verdict.candidate.naql_readiness.strip()
        assert isinstance(verdict.candidate.majaz_readiness, str)
        assert verdict.candidate.majaz_readiness.strip()

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=True,
            produced_outputs=frozenset({"SemanticSlotFrame"}),
        )
        assert_constitutional_case(case, result)
