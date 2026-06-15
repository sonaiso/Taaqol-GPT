"""Constitutional tests for PR-21M: ManāṭCandidate.

Origin law: docs/44_MANAT_BOUNDARY_LAW.md.

This test module proves:
1. prove_manat_candidate() returns PROVEN with valid inputs for all 3 modes.
2. ManatCandidate ≠ tanzil / reality application / execution / authority.
3. PROVEN HukmVerdict required.
4. ManatMode required (TAKHRIJ_CANDIDATE | TANQIH_CANDIDATE | TAHQIQ_READINESS_ONLY).
5. manat_description, effective_attribute_candidate, manat_evidence,
   manat_domain, closure_scope required (non-empty).
6. conditions and preventers must be tuple[str, ...].
7. TAHQIQ_READINESS_ONLY must not claim verification (overclaim guard).
8. Forbidden mode names rejected.
9. Residual governance (HIDDEN_FORBIDDEN / BLOCKING → REFUSED).
10. Rank never exceeds MANAT_RANK_CEILING.
11. All 6 required deferred residuals present, visible, EXPLANATORY.
12. Every verdict carries trace_ref.
13. Sub-carrier has birth guards.
14. PR-21M does not export forbidden symbols.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    MANAT_RANK_CEILING,
    BindingState,
    BoundaryEvidence,
    ContractableUnitGeometry,
    ContractableUnitState,
    DalBoundaryState,
    DalMadlulBindingCandidate,
    DalOnlyCandidate,
    EvaluationDomain,
    HukmState,
    HukmVerdict,
    IfadahState,
    IfadahVerdict,
    LicenseBoundaryKind,
    LicensingBoundaryState,
    LicensingBoundaryVerdict,
    ManatCandidate,
    ManatMode,
    ManatState,
    ManatVerdict,
    PathKind,
    PreWeightSurface,
    RegistryDomain,
    RegistryEntry,
    RegistryLookupResult,
    RegistryLookupState,
    SpeechForceKind,
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
    prove_hukm_candidate,
    prove_ifadah_candidate,
    prove_manat_candidate,
    prove_verbal_madlul,
    weigh,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.dalalah_candidates import (
    DalalahCandidateState,
    DalalahCandidateVerdict,
    NecessaryRelationType,
    prove_dalalah_candidates,
)
from taaqqul_slot_geometry.weight.formal_shape import FormalShapeClosureState
from taaqqul_slot_geometry.weight.formal_style_candidate import (
    FormalStyleFamily,
    FormalStyleState,
    FormalStyleVerdict,
    prove_formal_style_candidate,
)
from taaqqul_slot_geometry.weight.maqam_context_boundary import (
    DiscourseDomainType,
    LiteralConstraintType,
    MaqamContextBoundaryVerdict,
    MaqamContextState,
    UsageRegisterType,
    WadScopeType,
    prove_maqam_context_boundary,
)
from taaqqul_slot_geometry.weight.mufrad_dalalah_closure import (
    MufradDalalahClosureState,
    MufradDalalahClosureVerdict,
    prove_mufrad_dalalah_closure,
)
from taaqqul_slot_geometry.weight.mufrad_semantic_slot_geometry import (
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
from taaqqul_slot_geometry.weight.relation_closure import (
    RelationClosureState,
    RelationClosureVerdict,
    RelationType,
    prove_relation_closure,
)
from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState

# ===========================================================================
# Required deferred residual names (docs/44 §11)
# ===========================================================================

REQUIRED_DEFERRED_RESIDUAL_NAMES = (
    "MANAT_NOT_TANZIL",
    "TAHQIQ_FINAL_DEFERRED",
    "TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW",
    "REALITY_APPLICATION_DEFERRED",
    "NO_PREVENTER_CHECK_DEFERRED",
    "EXTERNAL_EXECUTION_FORBIDDEN",
)

# Forbidden symbols that PR-21M must NOT export or instantiate.
FORBIDDEN_SYMBOLS = (
    "TanzilCandidate",
    "TanzilVerdict",
    "TanzilState",
    "RealityApplication",
    "RealityVerification",
    "VerifiedRealityClaim",
    "Execution",
    "ExternalAction",
    "Enforcement",
    "Fatwa",
    "Qada",
    "FinalAuthority",
    "DivineAuthorityClaim",
    "MafhumCandidate",
    "MantuqClosure",
    "MajazVerdict",
    "MajazLicense",
    "ManqulVerdict",
    "ManqulLicense",
    "HaqiqahAttemptVerdict",
    "SpeakerIntentVerdict",
    "FinalMeaning",
    "Meaning",
    "OntologicalClaim",
    "FreeReasoning",
    "PropositionTruthValue",
    "AuthorityClaim",
    "NormativeJudgment",
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
        "scope": "pr-21m-manat-candidate-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pr-21m/kataba", kind="DECLARED_ENTRY"
        ),
    }


def _syllable(prefix: str = "ka") -> SyllableCandidate:
    return SyllableCandidate(
        **_base("syllable", f"syll-{prefix}", prefix),
        units=((prefix[0], prefix[1] if len(prefix) > 1 else "a"),),
    )


def _syllables(root: str = "kataba") -> tuple[SyllableCandidate, ...]:
    parts = [root[i:i+2] for i in range(0, len(root) - 1, 2)]
    if len(root) % 2 == 1:
        parts.append(root[-1] + "a")
    return tuple(
        SyllableCandidate(
            **_base("syllable", f"syll-{p}", p),
            units=((p[0], p[1] if len(p) > 1 else "a"),),
        )
        for p in parts[:3]
    )


def _sequence(root: str = "kataba") -> SyllableSequenceCandidate:
    return SyllableSequenceCandidate(
        **_base("syllable_sequence", f"seq-{root}", root),
        syllables=_syllables(root),
    )


def _boundary(root: str = "kataba") -> WordBoundaryCandidate:
    return WordBoundaryCandidate(
        **_base("word_boundary", f"wb-{root}", root),
        sequence=_sequence(root),
    )


def _word_carrier(root: str = "kataba") -> WordCarrierCandidate:
    return WordCarrierCandidate(
        **_base("word_carrier", f"wc-{root}", root),
        bounded_surface=_boundary(root),
    )


def _original_extra(root: str = "kataba") -> OriginalExtraMap:
    letters = list(root[:3])
    return OriginalExtraMap(
        **_base("original_extra_map", f"oem-{root}", root),
        underlying_form=root,
        assignments=tuple(
            (ch, LetterStanding.ORIGINAL) for ch in letters
        ),
    )


def _operations(root: str = "kataba") -> OperationTraceCandidate:
    return OperationTraceCandidate(
        **_base("operation_trace", f"ops-{root}", "declared-steps"),
        steps=("declared_seq", "declared_boundary"),
    )


def _surface(root: str = "kataba") -> PreWeightSurface:
    carrier = _word_carrier(root)
    return PreWeightSurface(
        **_base("pre_weight_surface", f"pws-{root}", root),
        carrier=carrier,
        path=PathCandidate(
            **_base("path", f"path-{root}", "root_path"),
            kind=PathKind.ROOT,
            carrier=carrier,
        ),
        original_extra=_original_extra(root),
        operations=_operations(root),
    )


def _weight_readiness(root: str = "kataba") -> WeightReadinessCandidate:
    return WeightReadinessCandidate(
        **_base("weight_readiness", f"wr-{root}", root),
        surface=_surface(root),
    )


def _weight_fit_candidate(root: str = "kataba") -> WeightFitCandidate:
    candidate = _weight_readiness(root)
    governance = omega_governance((), Rank.CANDIDATE)
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED
    assert result.candidate is not None
    return result.candidate


def _licensing_verdict(root: str = "kataba") -> LicensingBoundaryVerdict:
    fit = _weight_fit_candidate(root)
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


def _dal_only_candidate(root: str = "kataba") -> DalOnlyCandidate:
    verdict = _licensing_verdict(root)
    result = prove_dal(
        verdict, root, f"phonetic://{root}", f"graphic://{root}"
    )
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _madlul_candidate(
    dal: DalOnlyCandidate, root: str = "kataba"
) -> VerbalMadlulCandidate:
    result = prove_verbal_madlul(
        prior_dal=dal,
        wad_usage_boundary=f"lexical-wad-boundary-{root}",
        correspondence_candidate=f"correspondence/{root}",
        inclusion_candidate=f"inclusion/{root}",
        iltizam_condition=f"iltizam/{root}",
    )
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _dal_registry_proof(root: str = "kataba") -> RegistryLookupResult:
    entry = RegistryEntry(
        key=root,
        domain=RegistryDomain.DAL_ONLY,
        non_meaning_proof="signifier candidacy only, not meaning",
        rank=Rank.HYPOTHESIS,
        residuals=(),
        trace_ref=f"registry/dal/{root}",
    )
    return RegistryLookupResult(
        state=RegistryLookupState.FOUND,
        entry=entry,
        failure_code=None,
    )


def _madlul_registry_proof(root: str = "kataba") -> RegistryLookupResult:
    entry = RegistryEntry(
        key=root,
        domain=RegistryDomain.VERBAL_MADLUL,
        non_meaning_proof="verbal signified candidacy only, not meaning",
        rank=Rank.HYPOTHESIS,
        residuals=(),
        trace_ref=f"registry/madlul/{root}",
    )
    return RegistryLookupResult(
        state=RegistryLookupState.FOUND,
        entry=entry,
        failure_code=None,
    )


def _binding_candidate(
    dal: DalOnlyCandidate | None = None,
    madlul: VerbalMadlulCandidate | None = None,
    root: str = "kataba",
) -> DalMadlulBindingCandidate:
    if dal is None:
        dal = _dal_only_candidate(root)
    if madlul is None:
        madlul = _madlul_candidate(dal, root)
    result = bind_dal_madlul(
        dal, madlul, _dal_registry_proof(root), _madlul_registry_proof(root)
    )
    assert result.verdict_state is BindingState.BOUND
    assert result.candidate is not None
    return result.candidate


def _contractable_unit(
    dal: DalOnlyCandidate | None = None,
    madlul: VerbalMadlulCandidate | None = None,
    root: str = "kataba",
) -> ContractableUnitGeometry:
    binding = _binding_candidate(dal, madlul, root)
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


def _formal_style_verdict(
    style_family: FormalStyleFamily = FormalStyleFamily.DECLARATIVE_STYLE_FORM,
) -> FormalStyleVerdict:
    verdict = prove_formal_style_candidate(
        style_family=style_family,
        composition_evidence_ref="test/composition/khabar",
        formal_closure_state=FormalShapeClosureState.CLOSED,
        formal_closure_ref="test/closure/CLOSED",
    )
    assert verdict.verdict_state is FormalStyleState.PROVEN
    assert verdict.candidate is not None
    return verdict


def _semantic_slot_verdict(
    root: str = "kataba",
    semantic_category: SemanticCategory = SemanticCategory.JAMID,
) -> MufradSemanticSlotGeometryVerdict:
    dal = _dal_only_candidate(root)
    madlul = _madlul_candidate(dal, root)
    unit = _contractable_unit(dal, madlul, root)
    style = _formal_style_verdict()

    verdict = prove_mufrad_semantic_slot_geometry(
        formal_style_candidate=style.candidate,
        dal_only_candidate=dal,
        verbal_madlul_candidate=madlul,
        contractable_unit=unit,
        formal_closure_state=FormalShapeClosureState.CLOSED,
        semantic_category=semantic_category,
        wad_origin_domain=WadOriginDomain.LUGHAWI,
        wad_evidence_type=WadEvidenceType.SAMA,
        wad_scope="arabic_lexical",
        wad_evidence_ref=f"wad/{root}/sama",
        word_class_closure_ref="word_class/ISM/closed",
        weight_pattern_closure_ref="weight/fail/closed",
        inflection_closure_ref="inflection/murab/closed",
        contract_slot_readiness_ref="contract/subject/closed",
        composition_participation_ref="composition/nominal/closed",
        kulli_juzii_axis=KulliJuziiAxis.KULLI,
        particularity_source=ParticularitySource.NOT_APPLICABLE,
        predication_test_passed=True,
        reference_resolution_status="not_applicable",
        branch_origin_ref=f"origin/{root}/root",
        branch_ref=f"branch/{root}/derived",
        branch_relation_type="morphological_derivation",
        branch_illa_jamia="shared_root_pattern",
        branch_evidence_ref=f"evidence/{root}/root_attestation",
        branch_domain_compatibility="arabic_morphophonology",
        branch_no_preventer=True,
        naql_readiness="naql_not_applicable",
        majaz_readiness="majaz_not_applicable",
    )
    assert verdict.verdict_state is MufradSemanticState.PROVEN
    assert verdict.candidate is not None
    return verdict


def _maqam_context_verdict(
    semantic_verdict: MufradSemanticSlotGeometryVerdict,
) -> MaqamContextBoundaryVerdict:
    verdict = prove_maqam_context_boundary(
        semantic_slot_verdict=semantic_verdict,
        discourse_domain_type=DiscourseDomainType.LUGHAWI,
        discourse_evidence_ref="discourse/lughawi/evidence",
        usage_register_type=UsageRegisterType.HAQIQI,
        usage_evidence_ref="usage/haqiqi/evidence",
        technical_domain_name="general_arabic",
        is_technical=False,
        technical_evidence_ref="technical/general/evidence",
        speaker_position="narrator",
        addressee_position="reader",
        textual_context_window="kataba al-waladu",
        has_potential_qarina=False,
        qarina_type_readiness="no_qarinah",
        qarina_blocks_literal=False,
        qarina_evidence_ref="qarina/none/evidence",
        blocker_count=0,
        blocker_types=(),
        all_blockers_audited=True,
        blocker_evidence_ref="blocker/none/evidence",
        literal_constraint_type=LiteralConstraintType.UNCONSTRAINED,
        literal_domain_ref="literal/unconstrained",
        literal_evidence_ref="literal/evidence/none",
        wad_scope_type=WadScopeType.ORIGINAL,
        wad_narrowing_evidence="no_narrowing",
        wad_scope_evidence_ref="wad_scope/original/evidence",
        style_relevance_constraint="style_not_affecting",
    )
    assert verdict.verdict_state is MaqamContextState.PROVEN
    assert verdict.candidate is not None
    return verdict


def _dalalah_candidate_verdict(
    semantic_verdict: MufradSemanticSlotGeometryVerdict,
    maqam_verdict: MaqamContextBoundaryVerdict,
) -> DalalahCandidateVerdict:
    verdict = prove_dalalah_candidates(
        semantic_slot_verdict=semantic_verdict,
        maqam_context_verdict=maqam_verdict,
        correspondence_domain="arabic_lexical_full_extension",
        part_designation="semantic_component_action",
        inclusion_evidence="part_of_verbal_meaning_field",
        necessary_relation_type=NecessaryRelationType.SABAB,
        relation_evidence="cause_effect_linguistic_evidence",
    )
    assert verdict.verdict_state is DalalahCandidateState.PROVEN
    return verdict


def _proven_mufrad_closure(
    root: str = "kataba",
) -> MufradDalalahClosureVerdict:
    semantic = _semantic_slot_verdict(root)
    maqam = _maqam_context_verdict(semantic)
    dalalah = _dalalah_candidate_verdict(semantic, maqam)
    verdict = prove_mufrad_dalalah_closure(
        semantic_slot_verdict=semantic,
        maqam_context_verdict=maqam,
        dalalah_candidate_verdict=dalalah,
        closure_scope="mufrad_dalalah_minimum_complete",
    )
    assert verdict.verdict_state is MufradDalalahClosureState.PROVEN
    assert verdict.candidate is not None
    return verdict


def _proven_relation_closure_verdict(
    maqam: str = "general_arabic_discourse",
) -> RelationClosureVerdict:
    first = _proven_mufrad_closure("kataba")
    second = _proven_mufrad_closure("darasa")
    verdict = prove_relation_closure(
        first_verdict=first,
        second_verdict=second,
        relation_type=RelationType.PREDICATIVE,
        relation_maqam=maqam,
        relation_evidence="subject_predicate_evidence",
        closure_scope="relation_closure_minimal",
    )
    assert verdict.verdict_state is RelationClosureState.PROVEN
    return verdict


def _proven_ifadah_verdict(
    speech_force: SpeechForceKind = SpeechForceKind.KHABAR,
    style_family: FormalStyleFamily = FormalStyleFamily.DECLARATIVE_STYLE_FORM,
) -> IfadahVerdict:
    fs_verdict = _formal_style_verdict(style_family)
    semantic = _semantic_slot_verdict("kataba")
    maqam_verdict = _maqam_context_verdict(semantic)
    first = _proven_mufrad_closure("kataba")
    second = _proven_mufrad_closure("darasa")
    rc_verdict = prove_relation_closure(
        first_verdict=first,
        second_verdict=second,
        relation_type=RelationType.PREDICATIVE,
        relation_maqam=maqam_verdict.trace_ref,
        relation_evidence="subject_predicate_evidence",
        closure_scope="relation_closure_minimal",
    )
    assert rc_verdict.verdict_state is RelationClosureState.PROVEN

    verdict = prove_ifadah_candidate(
        relation_closure_verdict=rc_verdict,
        formal_style_verdict=fs_verdict,
        ifadah_maqam_verdict=maqam_verdict,
        speech_force=speech_force,
        ifadah_evidence="speech_level_closure_evidence",
        closure_scope="ifadah_minimal_scope",
    )
    assert verdict.verdict_state is IfadahState.PROVEN
    return verdict


def _proven_hukm_verdict(
    domain: EvaluationDomain = EvaluationDomain.LINGUISTIC,
) -> HukmVerdict:
    ifadah = _proven_ifadah_verdict()
    verdict = prove_hukm_candidate(
        ifadah_verdict=ifadah,
        evaluation_domain=domain,
        hukm_claim="grammatical_correctness_claim",
        hukm_evidence="morphosyntactic_evidence",
        hukm_maqam="linguistic_evaluation_maqam",
        closure_scope="hukm_minimal_scope",
    )
    assert verdict.verdict_state is HukmState.PROVEN
    return verdict


def _proven_manat_verdict(
    mode: ManatMode = ManatMode.TAKHRIJ_CANDIDATE,
) -> ManatVerdict:
    """Build a PROVEN manat verdict through the full lawful chain."""
    hukm = _proven_hukm_verdict()
    verdict = prove_manat_candidate(
        hukm_verdict=hukm,
        manat_mode=mode,
        manat_description="effective_attribute_extraction_from_hukm",
        effective_attribute_candidate="al_wasf_al_muaththir_fiiliyya",
        conditions=("condition_agent_mukalaf", "condition_action_exists"),
        preventers=("preventer_jahil_candidate",),
        manat_evidence="lexical_attestation_plus_qiyas",
        manat_domain="arabic_morphosyntactic_ruling",
        closure_scope="manat_minimal_scope",
    )
    return verdict


# ===========================================================================
# §1 PROVEN verdict tests (all three modes)
# ===========================================================================


class TestProvenVerdict:
    """prove_manat_candidate() returns PROVEN with valid inputs."""

    def test_proven_takhrij_candidate(self) -> None:
        verdict = _proven_manat_verdict(ManatMode.TAKHRIJ_CANDIDATE)
        assert verdict.verdict_state is ManatState.PROVEN

    def test_proven_tanqih_candidate(self) -> None:
        verdict = _proven_manat_verdict(ManatMode.TANQIH_CANDIDATE)
        assert verdict.verdict_state is ManatState.PROVEN

    def test_proven_tahqiq_readiness_only(self) -> None:
        verdict = _proven_manat_verdict(ManatMode.TAHQIQ_READINESS_ONLY)
        assert verdict.verdict_state is ManatState.PROVEN

    def test_no_failure_code(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.failure_code is None

    def test_candidate_present(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate, ManatCandidate)

    def test_rank_within_ceiling(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.verdict_rank <= MANAT_RANK_CEILING

    def test_trace_ref_present(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.trace_ref
        assert "prove_manat_candidate" in verdict.trace_ref

    def test_candidate_has_all_required_fields(self) -> None:
        verdict = _proven_manat_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.hukm_verdict_ref
        assert isinstance(c.manat_mode, ManatMode)
        assert c.manat_description
        assert c.effective_attribute_candidate
        assert isinstance(c.conditions, tuple)
        assert isinstance(c.preventers, tuple)
        assert c.manat_evidence
        assert c.manat_domain
        assert c.closure_scope
        assert isinstance(c.rank, Rank)
        assert isinstance(c.residuals, tuple)
        assert c.trace_ref


# ===========================================================================
# §2 ManatCandidate is NOT tanzil / reality / execution / authority
# ===========================================================================


class TestNotTanzilNotReality:
    """ManatCandidate does not produce tanzil, reality application, execution."""

    def test_manat_candidate_is_not_tanzil(self) -> None:
        verdict = _proven_manat_verdict()
        c = verdict.candidate
        assert c is not None
        assert not hasattr(c, "tanzil_claim")
        assert not hasattr(c, "reality_application")
        assert not hasattr(c, "execution")

    def test_manat_candidate_is_not_authority(self) -> None:
        verdict = _proven_manat_verdict()
        c = verdict.candidate
        assert c is not None
        assert not hasattr(c, "authority")
        assert not hasattr(c, "fatwa")
        assert not hasattr(c, "qada")

    def test_manat_candidate_is_not_reality_verification(self) -> None:
        verdict = _proven_manat_verdict()
        c = verdict.candidate
        assert c is not None
        assert not hasattr(c, "reality_verified")
        assert not hasattr(c, "verified_reality_claim")


# ===========================================================================
# §3 Refuses without PROVEN HukmVerdict
# ===========================================================================


class TestRefusesWithoutHukm:
    """prove_manat_candidate() refuses without a PROVEN HukmVerdict."""

    def test_refuses_without_hukm(self) -> None:
        verdict = prove_manat_candidate(
            hukm_verdict="not_a_verdict",  # type: ignore[arg-type]
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_HUKM

    def test_refuses_non_proven_hukm(self) -> None:
        hukm = HukmVerdict(
            candidate=None,
            verdict_state=HukmState.REFUSED,
            failure_code=FailureCode.NO_IFADAH,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused_hukm",
        )
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_HUKM

    def test_refuses_missing_hukm_candidate(self) -> None:
        hukm = HukmVerdict(
            candidate=None,
            verdict_state=HukmState.PROVEN,
            failure_code=None,
            verdict_rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="test/proven_but_no_candidate",
        )
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_HUKM


# ===========================================================================
# §4 Refuses missing fields
# ===========================================================================


class TestRefusesMissingFields:
    """prove_manat_candidate() refuses when required fields are empty."""

    def test_refuses_empty_manat_description(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANAT_DESCRIPTION

    def test_refuses_empty_effective_attribute_candidate(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="   ",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_EFFECTIVE_ATTRIBUTE

    def test_refuses_empty_manat_evidence(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANAT_EVIDENCE

    def test_refuses_empty_manat_domain(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANAT_DOMAIN

    def test_refuses_empty_closure_scope(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# §5 Mode guard — rejects forbidden modes, collapse
# ===========================================================================


class TestModeGuard:
    """ManatMode guards: invalid modes refused, collapse refused."""

    def test_rejects_invalid_mode_type(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode="TAHQIQ_FINAL",  # type: ignore[arg-type]
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANAT_MODE

    def test_rejects_reality_verified_mode(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode="REALITY_VERIFIED",  # type: ignore[arg-type]
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANAT_MODE

    def test_rejects_applied_manat_mode(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode="APPLIED_MANAT",  # type: ignore[arg-type]
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANAT_MODE


# ===========================================================================
# §6 TAHQIQ overclaim guard
# ===========================================================================


class TestTahqiqOverclaim:
    """TAHQIQ_READINESS_ONLY must not claim verification."""

    def test_tahqiq_readiness_is_not_verification(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAHQIQ_READINESS_ONLY,
            manat_description="verified reality in the world",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.TAHQIQ_OVERCLAIM

    def test_tahqiq_overclaim_in_attribute(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAHQIQ_READINESS_ONLY,
            manat_description="candidate_locus",
            effective_attribute_candidate="reality_checked confirmed",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.TAHQIQ_OVERCLAIM

    def test_takhrij_allows_readiness_language(self) -> None:
        """TAKHRIJ mode should not trigger the overclaim guard."""
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="verified in lexical records",
            effective_attribute_candidate="confirmed attribute",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        # TAKHRIJ does not trigger the overclaim guard
        assert verdict.verdict_state is ManatState.PROVEN


# ===========================================================================
# §7 Conditions and preventers
# ===========================================================================


class TestConditionsAndPreventers:
    """conditions and preventers must be tuple[str, ...]."""

    def test_conditions_must_be_tuple(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=["not", "a", "tuple"],  # type: ignore[arg-type]
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_preventers_must_be_tuple(self) -> None:
        hukm = _proven_hukm_verdict()
        verdict = prove_manat_candidate(
            hukm_verdict=hukm,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=["not_a_tuple"],  # type: ignore[arg-type]
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_conditions_are_candidates_not_verified(self) -> None:
        """Conditions are candidate strings (not verified fact booleans)."""
        verdict = _proven_manat_verdict()
        c = verdict.candidate
        assert c is not None
        for cond in c.conditions:
            assert isinstance(cond, str)

    def test_preventers_are_candidates_not_absent_verified(self) -> None:
        """Preventers are candidate strings (not absence-verification)."""
        verdict = _proven_manat_verdict()
        c = verdict.candidate
        assert c is not None
        for prev in c.preventers:
            assert isinstance(prev, str)


# ===========================================================================
# §8 Residual governance
# ===========================================================================


class TestResidualGovernance:
    """Hidden/blocking residuals refuse."""

    def test_hidden_residual_refuses(self) -> None:
        hukm = _proven_hukm_verdict()
        # Inject a hidden residual into the hukm verdict
        poisoned = HukmVerdict(
            candidate=hukm.candidate,
            verdict_state=HukmState.PROVEN,
            failure_code=None,
            verdict_rank=hukm.verdict_rank,
            residuals=(
                Residual(
                    name="POISON",
                    kind=ResidualKind.HIDDEN_FORBIDDEN,
                    visible=False,
                    note="injected hidden residual",
                ),
            ),
            trace_ref=hukm.trace_ref,
        )
        verdict = prove_manat_candidate(
            hukm_verdict=poisoned,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL

    def test_blocking_residual_refuses(self) -> None:
        hukm = _proven_hukm_verdict()
        poisoned = HukmVerdict(
            candidate=hukm.candidate,
            verdict_state=HukmState.PROVEN,
            failure_code=None,
            verdict_rank=hukm.verdict_rank,
            residuals=(
                Residual(
                    name="BLOCKER",
                    kind=ResidualKind.BLOCKING,
                    visible=True,
                    note="injected blocking residual",
                ),
            ),
            trace_ref=hukm.trace_ref,
        )
        verdict = prove_manat_candidate(
            hukm_verdict=poisoned,
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.verdict_state is ManatState.REFUSED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT

    def test_deferred_residuals_visible_explanatory(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.verdict_state is ManatState.PROVEN
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY
            assert r.visible is True

    def test_all_6_deferred_residuals_present(self) -> None:
        verdict = _proven_manat_verdict()
        names = {r.name for r in verdict.residuals}
        for expected in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert expected in names, f"Missing deferred residual: {expected}"


# ===========================================================================
# §9 Rank ceiling
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds MANAT_RANK_CEILING."""

    def test_rank_never_exceeds_manat_ceiling(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.verdict_rank <= MANAT_RANK_CEILING

    def test_candidate_rank_within_ceiling(self) -> None:
        verdict = _proven_manat_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.rank <= MANAT_RANK_CEILING


# ===========================================================================
# §10 Trace presence
# ===========================================================================


class TestTrace:
    """Every verdict carries trace_ref."""

    def test_trace_ref_present_on_proven(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.trace_ref
        assert "proven" in verdict.trace_ref

    def test_trace_ref_present_on_refused(self) -> None:
        verdict = prove_manat_candidate(
            hukm_verdict="invalid",  # type: ignore[arg-type]
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=(),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert verdict.trace_ref
        assert "refused" in verdict.trace_ref


# ===========================================================================
# §11 Birth guards (sub-carrier)
# ===========================================================================


class TestBirthGuards:
    """ManatCandidate dataclass __post_init__ guards."""

    def test_rejects_empty_hukm_verdict_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            ManatCandidate(
                hukm_verdict_ref="",
                manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
                manat_description="desc",
                effective_attribute_candidate="attr",
                conditions=(),
                preventers=(),
                manat_evidence="evidence",
                manat_domain="domain",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )

    def test_rejects_invalid_mode(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            ManatCandidate(
                hukm_verdict_ref="hukm/ref",
                manat_mode="INVALID",  # type: ignore[arg-type]
                manat_description="desc",
                effective_attribute_candidate="attr",
                conditions=(),
                preventers=(),
                manat_evidence="evidence",
                manat_domain="domain",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/trace",
            )

    def test_rejects_empty_trace_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            ManatCandidate(
                hukm_verdict_ref="hukm/ref",
                manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
                manat_description="desc",
                effective_attribute_candidate="attr",
                conditions=(),
                preventers=(),
                manat_evidence="evidence",
                manat_domain="domain",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# §12 Forbidden symbol scan (docs/44 §10)
# ===========================================================================


class TestForbiddenSymbolScan:
    """PR-21M must not export forbidden symbols."""

    def test_manat_module_does_not_define_forbidden_symbols(self) -> None:
        source_path = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/manat_candidate.py"
        )
        tree = ast.parse(source_path.read_text())
        defined_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_names.add(target.id)
        for forbidden in FORBIDDEN_SYMBOLS:
            assert forbidden not in defined_names, (
                f"Forbidden symbol {forbidden!r} found in manat_candidate.py"
            )

    def test_forbidden_mode_names_not_in_enum(self) -> None:
        """ManatMode must not contain forbidden mode names."""
        forbidden_modes = (
            "TAHQIQ_FINAL",
            "REALITY_VERIFIED",
            "APPLIED_MANAT",
            "EXECUTED_MANAT",
            "FINAL_ILLA",
            "FINAL_QIYAS_RESULT",
            "VERIFIED_CONDITION",
            "VERIFIED_PREVENTER",
            "EXTERNAL_APPLICATION",
        )
        mode_names = {m.name for m in ManatMode}
        for fm in forbidden_modes:
            assert fm not in mode_names, (
                f"Forbidden mode {fm!r} found in ManatMode enum"
            )
