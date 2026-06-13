"""Constitutional tests for PR-D1.2: Maqam/Context Boundary Readiness.

Origin law: docs/37_MAQAM_CONTEXT_BOUNDARY_READINESS_LAW.md.

This test module proves:
1. prove_maqam_context_boundary() returns PROVEN with valid inputs.
2. MaqamContextFrame ≠ meaning / dalalah / ifadah / speaker intent.
3. DiscourseDomainCandidate ≠ semantic content.
4. UsageRegisterCandidate ≠ meaning determination.
5. QarinaReadinessCarrier ≠ qarinah application.
6. BlockerCandidateSet ≠ blocker verdict.
7. LiteralDomainConstraint ≠ haqiqah verdict.
8. WadScopeConstraint ≠ wad' assignment.
9. prove refuses non-PROVEN semantic slot verdict.
10. prove refuses invalid SemanticSlotFrame type.
11. prove refuses invalid enum types.
12. prove refuses empty string fields.
13. prove refuses invalid bool fields.
14. Rank never exceeds MAQAM_CONTEXT_RANK_CEILING.
15. All 11 required deferred residuals are present, visible, EXPLANATORY.
16. Every verdict carries trace_ref.
17. Sub-carriers have birth guards.
18. PR-D1.2 does not export forbidden symbols.
19. PROVEN/REFUSED verdict invariants hold.
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
from taaqqul_slot_geometry.weight.formal_shape import FormalShapeClosureState
from taaqqul_slot_geometry.weight.formal_style_candidate import (
    FormalStyleCandidate,
    FormalStyleFamily,
    FormalStyleState,
    prove_formal_style_candidate,
)
from taaqqul_slot_geometry.weight.maqam_context_boundary import (
    MAQAM_CONTEXT_RANK_CEILING,
    BlockerCandidateSet,
    DiscourseDomainCandidate,
    DiscourseDomainType,
    LiteralConstraintType,
    LiteralDomainConstraint,
    MaqamContextBoundaryVerdict,
    MaqamContextFrame,
    MaqamContextState,
    QarinaReadinessCarrier,
    TechnicalDomainCandidate,
    UsageRegisterCandidate,
    UsageRegisterType,
    WadScopeConstraint,
    WadScopeType,
    prove_maqam_context_boundary,
)
from taaqqul_slot_geometry.weight.mufrad_semantic_slot_geometry import (
    SEMANTIC_SLOT_GEOMETRY_RANK_CEILING,
    KulliJuziiAxis,
    MufradSemanticSlotGeometryVerdict,
    MufradSemanticState,
    ParticularitySource,
    SemanticCategory,
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
    "MAQAM_CONTEXT_BOUNDARY_NOT_DALALAH",
    "MUTABAQAH_DEFERRED_TO_PR_D2",
    "TADAMMUN_DEFERRED_TO_PR_D2",
    "ILTIZAM_DEFERRED_TO_PR_D2",
    "MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3",
    "IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE",
    "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
    "MANQUL_DEFERRED_UNTIL_TRANSFER_GATE",
    "SPEAKER_INTENT_DEFERRED_UNTIL_IFADAH",
    "QARINA_APPLICATION_DEFERRED",
    "BLOCKER_VERDICT_DEFERRED",
)

# Forbidden symbols that PR-D1.2 must NOT export or instantiate.
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
    "SpeakerIntentVerdict",
    "QarinaApplicationVerdict",
    "BlockerVerdict",
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
        "scope": "pr-d12-maqam-context-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr-d12/kataba", kind="DECLARED_ENTRY"),
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


def _binding_candidate(
    dal: DalOnlyCandidate | None = None,
    madlul: VerbalMadlulCandidate | None = None,
) -> DalMadlulBindingCandidate:
    if dal is None:
        dal = _dal_only_candidate()
    if madlul is None:
        madlul = _madlul_candidate(dal)
    result = bind_dal_madlul(dal, madlul, _dal_registry_proof(), _madlul_registry_proof())
    assert result.verdict_state is BindingState.BOUND
    assert result.candidate is not None
    return result.candidate


def _contractable_unit(
    dal: DalOnlyCandidate | None = None,
    madlul: VerbalMadlulCandidate | None = None,
) -> ContractableUnitGeometry:
    binding = _binding_candidate(dal, madlul)
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


def _semantic_slot_verdict() -> MufradSemanticSlotGeometryVerdict:
    """Build a PROVEN semantic slot geometry verdict through the lawful chain."""
    dal = _dal_only_candidate()
    madlul = _madlul_candidate(dal)
    unit = _contractable_unit(dal, madlul)
    style = _formal_style_candidate()

    verdict = prove_mufrad_semantic_slot_geometry(
        formal_style_candidate=style,
        dal_only_candidate=dal,
        verbal_madlul_candidate=madlul,
        contractable_unit=unit,
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
    assert verdict.verdict_state is MufradSemanticState.PROVEN
    assert verdict.candidate is not None
    return verdict


def _proven_maqam_verdict() -> MaqamContextBoundaryVerdict:
    """Build a PROVEN maqam/context boundary verdict."""
    slot_verdict = _semantic_slot_verdict()
    return prove_maqam_context_boundary(
        semantic_slot_verdict=slot_verdict,
        discourse_domain_type=DiscourseDomainType.LUGHAWI,
        discourse_evidence_ref="evidence/discourse/lughawi",
        usage_register_type=UsageRegisterType.HAQIQI,
        usage_evidence_ref="evidence/register/haqiqi",
        technical_domain_name="NONE",
        is_technical=False,
        technical_evidence_ref="evidence/technical/none",
        speaker_position="neutral_speaker",
        addressee_position="neutral_addressee",
        textual_context_window="isolated_unit",
        has_potential_qarina=False,
        qarina_type_readiness="no_qarina",
        qarina_blocks_literal=False,
        qarina_evidence_ref="evidence/qarina/none",
        blocker_count=0,
        blocker_types=(),
        all_blockers_audited=True,
        blocker_evidence_ref="evidence/blocker/none",
        literal_constraint_type=LiteralConstraintType.UNCONSTRAINED,
        literal_domain_ref="domain/literal/unconstrained",
        literal_evidence_ref="evidence/literal/unconstrained",
        wad_scope_type=WadScopeType.ORIGINAL,
        wad_narrowing_evidence="no_narrowing",
        wad_scope_evidence_ref="evidence/scope/original",
        style_relevance_constraint="style_not_constraining",
    )


# ===========================================================================
# Test 1: prove returns PROVEN with valid inputs
# ===========================================================================


class TestProvenVerdict:
    """prove_maqam_context_boundary() returns PROVEN with valid inputs."""

    def test_proven_with_valid_inputs(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/37_MAQAM_CONTEXT_BOUNDARY_READINESS_LAW.md",
            branch_name="prove returns PROVEN with valid inputs",
            constitutional_chain=(
                "prove_maqam_context_boundary", "Verdict", "Rank", "Trace",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(
                "Meaning", "Ifadah", "HukmCandidate", "Dalalah",
                "SpeakerIntent", "QarinaApplication",
            ),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = _proven_maqam_verdict()

        assert verdict.verdict_state is MaqamContextState.PROVEN
        assert verdict.failure_code is None
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate, MaqamContextFrame)
        assert verdict.verdict_rank <= MAQAM_CONTEXT_RANK_CEILING
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
        )
        assert_constitutional_case(case, result)

    @pytest.mark.parametrize(
        "domain_type",
        list(DiscourseDomainType),
        ids=[d.value for d in DiscourseDomainType],
    )
    def test_proven_for_each_discourse_domain(
        self, domain_type: DiscourseDomainType
    ) -> None:
        slot_verdict = _semantic_slot_verdict()
        verdict = prove_maqam_context_boundary(
            semantic_slot_verdict=slot_verdict,
            discourse_domain_type=domain_type,
            discourse_evidence_ref="evidence/discourse/test",
            usage_register_type=UsageRegisterType.HAQIQI,
            usage_evidence_ref="evidence/register/haqiqi",
            technical_domain_name="NONE",
            is_technical=False,
            technical_evidence_ref="evidence/technical/none",
            speaker_position="neutral",
            addressee_position="neutral",
            textual_context_window="isolated",
            has_potential_qarina=False,
            qarina_type_readiness="none",
            qarina_blocks_literal=False,
            qarina_evidence_ref="evidence/qarina/none",
            blocker_count=0,
            blocker_types=(),
            all_blockers_audited=True,
            blocker_evidence_ref="evidence/blocker/none",
            literal_constraint_type=LiteralConstraintType.UNCONSTRAINED,
            literal_domain_ref="domain/literal/unconstrained",
            literal_evidence_ref="evidence/literal/unconstrained",
            wad_scope_type=WadScopeType.ORIGINAL,
            wad_narrowing_evidence="no_narrowing",
            wad_scope_evidence_ref="evidence/scope/original",
            style_relevance_constraint="not_constraining",
        )
        assert verdict.verdict_state is MaqamContextState.PROVEN
        assert verdict.candidate is not None
        assert verdict.candidate.discourse_domain.domain_type is domain_type


# ===========================================================================
# Test 2: prove refuses non-PROVEN semantic slot verdict
# ===========================================================================


class TestRefusesNonProvenSlotVerdict:
    """prove refuses when semantic slot verdict is not PROVEN."""

    def test_refuses_non_verdict_type(self) -> None:
        case = ConstitutionalTestCase(
            origin_law="docs/37_MAQAM_CONTEXT_BOUNDARY_READINESS_LAW.md",
            branch_name="prove refuses invalid verdict type",
            constitutional_chain=("prove_maqam_context_boundary", "Refusal"),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=("MaqamContextFrame",),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
        )

        verdict = prove_maqam_context_boundary(
            semantic_slot_verdict="not_a_verdict",  # type: ignore[arg-type]
            discourse_domain_type=DiscourseDomainType.LUGHAWI,
            discourse_evidence_ref="evidence/test",
            usage_register_type=UsageRegisterType.HAQIQI,
            usage_evidence_ref="evidence/test",
            technical_domain_name="NONE",
            is_technical=False,
            technical_evidence_ref="evidence/test",
            speaker_position="test",
            addressee_position="test",
            textual_context_window="test",
            has_potential_qarina=False,
            qarina_type_readiness="none",
            qarina_blocks_literal=False,
            qarina_evidence_ref="evidence/test",
            blocker_count=0,
            blocker_types=(),
            all_blockers_audited=True,
            blocker_evidence_ref="evidence/test",
            literal_constraint_type=LiteralConstraintType.UNCONSTRAINED,
            literal_domain_ref="test",
            literal_evidence_ref="evidence/test",
            wad_scope_type=WadScopeType.ORIGINAL,
            wad_narrowing_evidence="none",
            wad_scope_evidence_ref="evidence/test",
            style_relevance_constraint="test",
        )

        assert verdict.verdict_state is MaqamContextState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED
        assert verdict.candidate is None

        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=FailureCode.GATE_REQUIRED,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=bool(verdict.trace_ref.strip()),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# Test 3: prove refuses empty string fields
# ===========================================================================


class TestRefusesEmptyStrings:
    """prove refuses empty or whitespace string fields."""

    @pytest.mark.parametrize(
        "field_name",
        [
            "discourse_evidence_ref",
            "usage_evidence_ref",
            "technical_domain_name",
            "technical_evidence_ref",
            "speaker_position",
            "addressee_position",
            "textual_context_window",
            "qarina_type_readiness",
            "qarina_evidence_ref",
            "blocker_evidence_ref",
            "literal_domain_ref",
            "literal_evidence_ref",
            "wad_narrowing_evidence",
            "wad_scope_evidence_ref",
            "style_relevance_constraint",
        ],
    )
    def test_refuses_empty_string(self, field_name: str) -> None:
        slot_verdict = _semantic_slot_verdict()
        kwargs = {
            "semantic_slot_verdict": slot_verdict,
            "discourse_domain_type": DiscourseDomainType.LUGHAWI,
            "discourse_evidence_ref": "evidence/test",
            "usage_register_type": UsageRegisterType.HAQIQI,
            "usage_evidence_ref": "evidence/test",
            "technical_domain_name": "NONE",
            "is_technical": False,
            "technical_evidence_ref": "evidence/test",
            "speaker_position": "test",
            "addressee_position": "test",
            "textual_context_window": "test",
            "has_potential_qarina": False,
            "qarina_type_readiness": "none",
            "qarina_blocks_literal": False,
            "qarina_evidence_ref": "evidence/test",
            "blocker_count": 0,
            "blocker_types": (),
            "all_blockers_audited": True,
            "blocker_evidence_ref": "evidence/test",
            "literal_constraint_type": LiteralConstraintType.UNCONSTRAINED,
            "literal_domain_ref": "test",
            "literal_evidence_ref": "evidence/test",
            "wad_scope_type": WadScopeType.ORIGINAL,
            "wad_narrowing_evidence": "none",
            "wad_scope_evidence_ref": "evidence/test",
            "style_relevance_constraint": "test",
        }
        kwargs[field_name] = "   "  # whitespace-only
        verdict = prove_maqam_context_boundary(**kwargs)
        assert verdict.verdict_state is MaqamContextState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert verdict.candidate is None


# ===========================================================================
# Test 4: prove refuses invalid enum types
# ===========================================================================


class TestRefusesInvalidEnumTypes:
    """prove refuses invalid enum types."""

    def test_refuses_invalid_discourse_domain_type(self) -> None:
        slot_verdict = _semantic_slot_verdict()
        verdict = prove_maqam_context_boundary(
            semantic_slot_verdict=slot_verdict,
            discourse_domain_type="NOT_AN_ENUM",  # type: ignore[arg-type]
            discourse_evidence_ref="evidence/test",
            usage_register_type=UsageRegisterType.HAQIQI,
            usage_evidence_ref="evidence/test",
            technical_domain_name="NONE",
            is_technical=False,
            technical_evidence_ref="evidence/test",
            speaker_position="test",
            addressee_position="test",
            textual_context_window="test",
            has_potential_qarina=False,
            qarina_type_readiness="none",
            qarina_blocks_literal=False,
            qarina_evidence_ref="evidence/test",
            blocker_count=0,
            blocker_types=(),
            all_blockers_audited=True,
            blocker_evidence_ref="evidence/test",
            literal_constraint_type=LiteralConstraintType.UNCONSTRAINED,
            literal_domain_ref="test",
            literal_evidence_ref="evidence/test",
            wad_scope_type=WadScopeType.ORIGINAL,
            wad_narrowing_evidence="none",
            wad_scope_evidence_ref="evidence/test",
            style_relevance_constraint="test",
        )
        assert verdict.verdict_state is MaqamContextState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_refuses_invalid_usage_register_type(self) -> None:
        slot_verdict = _semantic_slot_verdict()
        verdict = prove_maqam_context_boundary(
            semantic_slot_verdict=slot_verdict,
            discourse_domain_type=DiscourseDomainType.LUGHAWI,
            discourse_evidence_ref="evidence/test",
            usage_register_type="NOT_AN_ENUM",  # type: ignore[arg-type]
            usage_evidence_ref="evidence/test",
            technical_domain_name="NONE",
            is_technical=False,
            technical_evidence_ref="evidence/test",
            speaker_position="test",
            addressee_position="test",
            textual_context_window="test",
            has_potential_qarina=False,
            qarina_type_readiness="none",
            qarina_blocks_literal=False,
            qarina_evidence_ref="evidence/test",
            blocker_count=0,
            blocker_types=(),
            all_blockers_audited=True,
            blocker_evidence_ref="evidence/test",
            literal_constraint_type=LiteralConstraintType.UNCONSTRAINED,
            literal_domain_ref="test",
            literal_evidence_ref="evidence/test",
            wad_scope_type=WadScopeType.ORIGINAL,
            wad_narrowing_evidence="none",
            wad_scope_evidence_ref="evidence/test",
            style_relevance_constraint="test",
        )
        assert verdict.verdict_state is MaqamContextState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# Test 5: all required deferred residuals present
# ===========================================================================


class TestDeferredResiduals:
    """All 11 required deferred residuals are present, visible, EXPLANATORY."""

    def test_all_residuals_present(self) -> None:
        verdict = _proven_maqam_verdict()
        residual_names = tuple(r.name for r in verdict.residuals)
        for name in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert name in residual_names, f"Missing residual: {name}"

    def test_all_residuals_visible_and_explanatory(self) -> None:
        verdict = _proven_maqam_verdict()
        for r in verdict.residuals:
            assert r.visible is True
            assert r.kind is ResidualKind.EXPLANATORY


# ===========================================================================
# Test 6: rank never exceeds ceiling
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds MAQAM_CONTEXT_RANK_CEILING."""

    def test_proven_verdict_rank_bounded(self) -> None:
        verdict = _proven_maqam_verdict()
        assert verdict.verdict_rank <= MAQAM_CONTEXT_RANK_CEILING
        assert verdict.candidate is not None
        assert verdict.candidate.rank <= MAQAM_CONTEXT_RANK_CEILING

    def test_ceiling_equals_semantic_slot_geometry_ceiling(self) -> None:
        assert MAQAM_CONTEXT_RANK_CEILING == SEMANTIC_SLOT_GEOMETRY_RANK_CEILING


# ===========================================================================
# Test 7: sub-carrier birth guards
# ===========================================================================


class TestSubCarrierBirthGuards:
    """Sub-carriers refuse invalid construction."""

    def test_discourse_domain_refuses_invalid_type(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            DiscourseDomainCandidate(
                domain_type="NOT_ENUM",  # type: ignore[arg-type]
                evidence_ref="test",
                rank=Rank.CANDIDATE,
                trace_ref="test/trace",
            )

    def test_usage_register_refuses_invalid_type(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            UsageRegisterCandidate(
                register_type="NOT_ENUM",  # type: ignore[arg-type]
                evidence_ref="test",
                trace_ref="test/trace",
            )

    def test_technical_domain_refuses_empty_name(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            TechnicalDomainCandidate(
                domain_name="   ",
                is_technical=False,
                evidence_ref="test",
                trace_ref="test/trace",
            )

    def test_qarina_readiness_refuses_empty_type(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            QarinaReadinessCarrier(
                has_potential_qarina=False,
                qarina_type_readiness="   ",
                blocks_literal=False,
                evidence_ref="test",
                trace_ref="test/trace",
            )

    def test_blocker_set_refuses_negative_count(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            BlockerCandidateSet(
                blocker_count=-1,
                blocker_types=(),
                all_audited=True,
                evidence_ref="test",
                trace_ref="test/trace",
            )

    def test_literal_constraint_refuses_invalid_type(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            LiteralDomainConstraint(
                constraint_type="NOT_ENUM",  # type: ignore[arg-type]
                domain_ref="test",
                evidence_ref="test",
                trace_ref="test/trace",
            )

    def test_wad_scope_refuses_invalid_type(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            WadScopeConstraint(
                scope_type="NOT_ENUM",  # type: ignore[arg-type]
                narrowing_evidence="test",
                evidence_ref="test",
                trace_ref="test/trace",
            )

    def test_maqam_frame_refuses_invalid_discourse_domain(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MaqamContextFrame(
                semantic_slot_frame_ref="test/ref",
                discourse_domain="not_a_carrier",  # type: ignore[arg-type]
                usage_register=UsageRegisterCandidate(
                    register_type=UsageRegisterType.HAQIQI,
                    evidence_ref="test",
                    trace_ref="test/trace",
                ),
                technical_domain=TechnicalDomainCandidate(
                    domain_name="NONE",
                    is_technical=False,
                    evidence_ref="test",
                    trace_ref="test/trace",
                ),
                speaker_position="test",
                addressee_position="test",
                textual_context_window="test",
                qarina_readiness=QarinaReadinessCarrier(
                    has_potential_qarina=False,
                    qarina_type_readiness="none",
                    blocks_literal=False,
                    evidence_ref="test",
                    trace_ref="test/trace",
                ),
                blocker_candidate_set=BlockerCandidateSet(
                    blocker_count=0,
                    blocker_types=(),
                    all_audited=True,
                    evidence_ref="test",
                    trace_ref="test/trace",
                ),
                literal_domain_constraint=LiteralDomainConstraint(
                    constraint_type=LiteralConstraintType.UNCONSTRAINED,
                    domain_ref="test",
                    evidence_ref="test",
                    trace_ref="test/trace",
                ),
                wad_scope_constraint=WadScopeConstraint(
                    scope_type=WadScopeType.ORIGINAL,
                    narrowing_evidence="test",
                    evidence_ref="test",
                    trace_ref="test/trace",
                ),
                style_relevance_constraint="test",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )


# ===========================================================================
# Test 8: PR-D1.2 does not export forbidden symbols
# ===========================================================================


class TestForbiddenSymbols:
    """PR-D1.2 module does not export forbidden symbols."""

    def test_no_forbidden_symbols_in_module(self) -> None:
        source_path = (
            pathlib.Path(__file__).resolve().parents[1]
            / "src"
            / "taaqqul_slot_geometry"
            / "weight"
            / "maqam_context_boundary.py"
        )
        tree = ast.parse(source_path.read_text())
        defined_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_names.add(node.name)
        for forbidden in FORBIDDEN_SYMBOLS:
            assert forbidden not in defined_names, (
                f"Forbidden symbol '{forbidden}' found in PR-D1.2 module"
            )


# ===========================================================================
# Test 9: PROVEN/REFUSED verdict invariants
# ===========================================================================


class TestVerdictInvariants:
    """PROVEN/REFUSED verdict invariants hold."""

    def test_proven_verdict_has_no_failure_code(self) -> None:
        verdict = _proven_maqam_verdict()
        assert verdict.verdict_state is MaqamContextState.PROVEN
        assert verdict.failure_code is None
        assert verdict.candidate is not None

    def test_refused_verdict_has_no_candidate(self) -> None:
        verdict = prove_maqam_context_boundary(
            semantic_slot_verdict="invalid",  # type: ignore[arg-type]
            discourse_domain_type=DiscourseDomainType.LUGHAWI,
            discourse_evidence_ref="test",
            usage_register_type=UsageRegisterType.HAQIQI,
            usage_evidence_ref="test",
            technical_domain_name="NONE",
            is_technical=False,
            technical_evidence_ref="test",
            speaker_position="test",
            addressee_position="test",
            textual_context_window="test",
            has_potential_qarina=False,
            qarina_type_readiness="none",
            qarina_blocks_literal=False,
            qarina_evidence_ref="test",
            blocker_count=0,
            blocker_types=(),
            all_blockers_audited=True,
            blocker_evidence_ref="test",
            literal_constraint_type=LiteralConstraintType.UNCONSTRAINED,
            literal_domain_ref="test",
            literal_evidence_ref="test",
            wad_scope_type=WadScopeType.ORIGINAL,
            wad_narrowing_evidence="none",
            wad_scope_evidence_ref="test",
            style_relevance_constraint="test",
        )
        assert verdict.verdict_state is MaqamContextState.REFUSED
        assert verdict.candidate is None
        assert verdict.failure_code is not None

    def test_proven_verdict_schema_refuses_failure_code(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MaqamContextBoundaryVerdict(
                candidate=None,
                verdict_state=MaqamContextState.PROVEN,
                failure_code=FailureCode.GATE_REQUIRED,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )

    def test_refused_verdict_refuses_missing_failure_code(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MaqamContextBoundaryVerdict(
                candidate=None,
                verdict_state=MaqamContextState.REFUSED,
                failure_code=None,  # Must have a failure code
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )
