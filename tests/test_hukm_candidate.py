"""Constitutional tests for PR-21: HukmCandidate.

Origin law: docs/43_HUKM_DOMAIN_BOUNDARY_LAW.md.

This test module proves:
1. prove_hukm_candidate() returns PROVEN with valid inputs.
2. HukmCandidate ≠ authority / meaning / manat / tanzil / execution.
3. PROVEN IfadahVerdict required.
4. EvaluationDomain required (LINGUISTIC | LOGICAL | NORMATIVE_CANDIDATE only).
5. hukm_claim, hukm_evidence, hukm_maqam, closure_scope required.
6. Bare NORMATIVE is AUTHORITY_LEAK (AST alias-drop guard).
7. Residual governance (HIDDEN_FORBIDDEN / BLOCKING → REFUSED).
8. Rank never exceeds HUKM_RANK_CEILING.
9. All 7 required deferred residuals present, visible, EXPLANATORY.
10. Every verdict carries trace_ref.
11. Sub-carrier has birth guards.
12. PR-21 does not export forbidden symbols.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    HUKM_RANK_CEILING,
    IFADAH_RANK_CEILING,
    BindingState,
    BoundaryEvidence,
    ContractableUnitGeometry,
    ContractableUnitState,
    DalBoundaryState,
    DalMadlulBindingCandidate,
    DalOnlyCandidate,
    EvaluationDomain,
    HukmCandidate,
    HukmState,
    HukmVerdict,
    IfadahState,
    IfadahVerdict,
    LicenseBoundaryKind,
    LicensingBoundaryState,
    LicensingBoundaryVerdict,
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
# Required deferred residual names (docs/43 §11)
# ===========================================================================

REQUIRED_DEFERRED_RESIDUAL_NAMES = (
    "HUKM_NOT_AUTHORITY",
    "MANAT_DEFERRED_UNTIL_MANAT_LAW",
    "TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW",
    "MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL",
    "EXTENDED_DOMAIN_DEFERRED",
    "REALITY_VERIFICATION_DEFERRED",
    "AUDIT_INTEGRATION_DEFERRED_UNTIL_PR_22_AUDIT",
)

# Forbidden symbols that PR-21 must NOT export or instantiate.
FORBIDDEN_SYMBOLS = (
    "ManatCandidate",
    "TanzilCandidate",
    "MafhumCandidate",
    "MantuqClosure",
    "MajazVerdict",
    "MajazLicense",
    "ManqulVerdict",
    "ManqulLicense",
    "SpeakerIntentVerdict",
    "HaqiqahAttemptVerdict",
    "OntologicalClaim",
    "FreeReasoning",
    "AuthorityClaim",
    "NormativeJudgment",
    "FinalMeaning",
    "Meaning",
    "PropositionTruthValue",
    "RealityApplication",
    "Execution",
    "Fatwa",
    "Qada",
    "DivineAuthorityClaim",
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
        "scope": "pr-21-hukm-candidate-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pr-21/kataba", kind="DECLARED_ENTRY"
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
    """Build a PROVEN semantic slot geometry verdict."""
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
    """Build a PROVEN maqam context boundary verdict."""
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
    """Build a PROVEN dalalah candidate verdict."""
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
    """Build a PROVEN mufrad dalalah closure verdict."""
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
    """Build a PROVEN relation closure verdict with two distinct units."""
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
    """Build a PROVEN ifadah verdict through the full lawful chain."""
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
    """Build a PROVEN hukm verdict through the full lawful chain."""
    ifadah = _proven_ifadah_verdict()
    verdict = prove_hukm_candidate(
        ifadah_verdict=ifadah,
        evaluation_domain=domain,
        hukm_claim="grammatical_correctness_claim",
        hukm_evidence="morphosyntactic_evidence",
        hukm_maqam="linguistic_evaluation_maqam",
        closure_scope="hukm_minimal_scope",
    )
    return verdict


# ===========================================================================
# §1 PROVEN verdict tests
# ===========================================================================


class TestProvenVerdict:
    """prove_hukm_candidate() returns PROVEN with valid inputs."""

    def test_returns_proven_state(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.verdict_state is HukmState.PROVEN

    def test_no_failure_code(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.failure_code is None

    def test_candidate_present(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate, HukmCandidate)

    def test_rank_within_ceiling(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.verdict_rank <= HUKM_RANK_CEILING

    def test_trace_ref_present(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.trace_ref
        assert "prove_hukm_candidate" in verdict.trace_ref

    def test_candidate_has_all_required_fields(self) -> None:
        verdict = _proven_hukm_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.ifadah_verdict_ref
        assert isinstance(c.evaluation_domain, EvaluationDomain)
        assert c.hukm_claim
        assert c.hukm_evidence
        assert c.hukm_maqam
        assert c.closure_scope
        assert isinstance(c.rank, Rank)
        assert isinstance(c.residuals, tuple)
        assert c.trace_ref

    def test_proven_with_linguistic(self) -> None:
        verdict = _proven_hukm_verdict(EvaluationDomain.LINGUISTIC)
        assert verdict.verdict_state is HukmState.PROVEN

    def test_proven_with_logical(self) -> None:
        verdict = _proven_hukm_verdict(EvaluationDomain.LOGICAL)
        assert verdict.verdict_state is HukmState.PROVEN

    def test_proven_with_normative_candidate(self) -> None:
        verdict = _proven_hukm_verdict(EvaluationDomain.NORMATIVE_CANDIDATE)
        assert verdict.verdict_state is HukmState.PROVEN


# ===========================================================================
# §2 Not authority / not final meaning / not tanzil
# ===========================================================================


class TestNotAuthority:
    """HukmCandidate is not authority, not tanzil, not final meaning."""

    def test_hukm_candidate_is_not_authority(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.candidate is not None
        # Authority would require a different carrier class
        assert not hasattr(verdict.candidate, "authority_claim")
        assert not hasattr(verdict.candidate, "enforcement")

    def test_hukm_candidate_is_not_tanzil(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.candidate is not None
        assert not hasattr(verdict.candidate, "presentation_envelope")
        assert not hasattr(verdict.candidate, "application_target")

    def test_hukm_candidate_is_not_final_meaning(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.candidate is not None
        assert not hasattr(verdict.candidate, "final_meaning")
        assert not hasattr(verdict.candidate, "proposition_truth_value")


# ===========================================================================
# §3 Input verdict refusal tests
# ===========================================================================


class TestInputVerdictRefusal:
    """IfadahVerdict must be valid and PROVEN."""

    def test_refuses_invalid_ifadah_type(self) -> None:
        verdict = prove_hukm_candidate(
            ifadah_verdict="not_a_verdict",  # type: ignore[arg-type]
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH

    def test_refuses_ifadah_not_proven(self) -> None:
        # Build a REFUSED ifadah verdict
        verdict_ifadah = prove_ifadah_candidate(
            relation_closure_verdict="not_valid",  # type: ignore[arg-type]
            formal_style_verdict=_formal_style_verdict(),
            ifadah_maqam_verdict=_maqam_context_verdict(_semantic_slot_verdict()),
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict_ifadah.verdict_state is IfadahState.REFUSED

        verdict = prove_hukm_candidate(
            ifadah_verdict=verdict_ifadah,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH

    def test_refuses_ifadah_candidate_missing(self) -> None:
        # Manually construct a verdict with None candidate but PROVEN state
        broken = IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.PROVEN,
            failure_code=None,
            verdict_rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="broken/proven/no_candidate",
        )
        verdict = prove_hukm_candidate(
            ifadah_verdict=broken,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH


# ===========================================================================
# §4 EvaluationDomain refusal tests
# ===========================================================================


class TestEvaluationDomainRefusal:
    """EvaluationDomain must be a valid minimal member."""

    def test_refuses_missing_evaluation_domain(self) -> None:
        ifadah = _proven_ifadah_verdict()
        verdict = prove_hukm_candidate(
            ifadah_verdict=ifadah,
            evaluation_domain="LINGUISTIC",  # type: ignore[arg-type]
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_EVALUATION_DOMAIN

    def test_refuses_invalid_domain_type(self) -> None:
        ifadah = _proven_ifadah_verdict()
        verdict = prove_hukm_candidate(
            ifadah_verdict=ifadah,
            evaluation_domain=42,  # type: ignore[arg-type]
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_EVALUATION_DOMAIN

    def test_allows_linguistic(self) -> None:
        verdict = _proven_hukm_verdict(EvaluationDomain.LINGUISTIC)
        assert verdict.verdict_state is HukmState.PROVEN

    def test_allows_logical(self) -> None:
        verdict = _proven_hukm_verdict(EvaluationDomain.LOGICAL)
        assert verdict.verdict_state is HukmState.PROVEN

    def test_allows_normative_candidate(self) -> None:
        verdict = _proven_hukm_verdict(EvaluationDomain.NORMATIVE_CANDIDATE)
        assert verdict.verdict_state is HukmState.PROVEN

    def test_only_three_domain_members(self) -> None:
        assert len(EvaluationDomain) == 3


# ===========================================================================
# §5 AUTHORITY_LEAK / bare NORMATIVE tests
# ===========================================================================


class TestAuthorityLeak:
    """Bare NORMATIVE is AUTHORITY_LEAK (docs/43 §6.2)."""

    def test_bare_normative_not_enum_member(self) -> None:
        """The bare string 'NORMATIVE' cannot be an EvaluationDomain."""
        with pytest.raises(ValueError):
            EvaluationDomain("NORMATIVE")

    def test_no_public_symbol_named_normative(self) -> None:
        """AST alias-drop guard: no bare NORMATIVE in hukm_candidate.py."""
        module_path = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/hukm_candidate.py"
        )
        source = module_path.read_text()
        tree = ast.parse(source)
        # Collect all assignment targets and class/function defs
        public_names: set[str] = set()
        for node in ast.walk(tree):
            if (
                isinstance(node, (ast.ClassDef, ast.FunctionDef))
                and not node.name.startswith("_")
            ):
                public_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("_"):
                        public_names.add(target.id)
        # NORMATIVE alone must not be a public name
        assert "NORMATIVE" not in public_names, (
            "Bare 'NORMATIVE' found as public symbol — AUTHORITY_LEAK"
        )

    def test_no_repr_drops_candidate_suffix(self) -> None:
        """NORMATIVE_CANDIDATE repr must not drop _CANDIDATE."""
        domain = EvaluationDomain.NORMATIVE_CANDIDATE
        assert "CANDIDATE" in repr(domain)
        assert "CANDIDATE" in str(domain)
        assert domain.value == "NORMATIVE_CANDIDATE"

    def test_ast_guard_no_bare_normative_in_package(self) -> None:
        """Scan all .py under src/taaqqul_slot_geometry for bare NORMATIVE.

        This is the constitutional AST alias-drop guard (docs/43 §6.2).
        """
        src_dir = pathlib.Path("src/taaqqul_slot_geometry")
        violations: list[str] = []
        for py_file in src_dir.rglob("*.py"):
            source = py_file.read_text()
            tree = ast.parse(source, filename=str(py_file))
            for node in ast.walk(tree):
                # Check class definitions
                if isinstance(node, ast.ClassDef) and node.name == "NORMATIVE":
                    violations.append(f"{py_file}:{node.lineno} class NORMATIVE")
                # Check function definitions
                elif isinstance(node, ast.FunctionDef) and node.name == "NORMATIVE":
                    violations.append(f"{py_file}:{node.lineno} def NORMATIVE")
                # Check assignment targets
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "NORMATIVE":
                            violations.append(
                                f"{py_file}:{node.lineno} "
                                f"assignment NORMATIVE"
                            )
        assert not violations, (
            "Bare 'NORMATIVE' found in package — AUTHORITY_LEAK:\n"
            + "\n".join(violations)
        )


# ===========================================================================
# §6 Required field refusal tests
# ===========================================================================


class TestFieldRefusal:
    """hukm_claim, hukm_evidence, hukm_maqam, closure_scope required."""

    def test_refuses_empty_hukm_claim(self) -> None:
        ifadah = _proven_ifadah_verdict()
        verdict = prove_hukm_candidate(
            ifadah_verdict=ifadah,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_HUKM_CLAIM

    def test_refuses_whitespace_hukm_claim(self) -> None:
        ifadah = _proven_ifadah_verdict()
        verdict = prove_hukm_candidate(
            ifadah_verdict=ifadah,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="   ",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_HUKM_CLAIM

    def test_refuses_empty_hukm_evidence(self) -> None:
        ifadah = _proven_ifadah_verdict()
        verdict = prove_hukm_candidate(
            ifadah_verdict=ifadah,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_HUKM_EVIDENCE

    def test_refuses_empty_hukm_maqam(self) -> None:
        ifadah = _proven_ifadah_verdict()
        verdict = prove_hukm_candidate(
            ifadah_verdict=ifadah,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.NO_HUKM_MAQAM

    def test_refuses_empty_closure_scope(self) -> None:
        ifadah = _proven_ifadah_verdict()
        verdict = prove_hukm_candidate(
            ifadah_verdict=ifadah,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# §7 Residual governance tests
# ===========================================================================


class TestResidualGovernance:
    """Hidden/blocking residuals refuse."""

    def test_hidden_residual_in_input_refuses(self) -> None:
        ifadah = _proven_ifadah_verdict()
        # Inject a hidden residual into the ifadah verdict
        hidden = Residual(
            name="INJECTED_HIDDEN",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=False,
            note="test",
        )
        poisoned = IfadahVerdict(
            candidate=ifadah.candidate,
            verdict_state=IfadahState.PROVEN,
            failure_code=None,
            verdict_rank=ifadah.verdict_rank,
            residuals=(hidden,),
            trace_ref=ifadah.trace_ref,
        )
        verdict = prove_hukm_candidate(
            ifadah_verdict=poisoned,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL

    def test_blocking_residual_in_input_refuses(self) -> None:
        ifadah = _proven_ifadah_verdict()
        blocking = Residual(
            name="INJECTED_BLOCKING",
            kind=ResidualKind.BLOCKING,
            visible=True,
            note="test",
        )
        poisoned = IfadahVerdict(
            candidate=ifadah.candidate,
            verdict_state=IfadahState.PROVEN,
            failure_code=None,
            verdict_rank=ifadah.verdict_rank,
            residuals=(blocking,),
            trace_ref=ifadah.trace_ref,
        )
        verdict = prove_hukm_candidate(
            ifadah_verdict=poisoned,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT

    def test_deferred_residuals_visible_explanatory(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.candidate is not None
        for r in verdict.candidate.residuals:
            assert r.kind is ResidualKind.EXPLANATORY
            assert r.visible is True


# ===========================================================================
# §8 Deferred residuals (docs/43 §11)
# ===========================================================================


class TestDeferredResiduals:
    """All 7 deferred residuals present, visible, EXPLANATORY."""

    def test_exactly_seven_residuals(self) -> None:
        verdict = _proven_hukm_verdict()
        assert len(verdict.residuals) == 7

    def test_all_residuals_explanatory(self) -> None:
        verdict = _proven_hukm_verdict()
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY

    def test_all_residuals_visible(self) -> None:
        verdict = _proven_hukm_verdict()
        for r in verdict.residuals:
            assert r.visible is True

    def test_all_required_names_present(self) -> None:
        verdict = _proven_hukm_verdict()
        names = {r.name for r in verdict.residuals}
        for required_name in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert required_name in names, f"Missing: {required_name}"

    def test_candidate_carries_same_residuals(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.candidate is not None
        assert verdict.candidate.residuals == verdict.residuals


# ===========================================================================
# §9 Rank ceiling tests
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds HUKM_RANK_CEILING."""

    def test_verdict_rank_within_ceiling(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.verdict_rank <= HUKM_RANK_CEILING

    def test_candidate_rank_within_ceiling(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.candidate is not None
        assert verdict.candidate.rank <= HUKM_RANK_CEILING

    def test_ceiling_equals_ifadah_ceiling(self) -> None:
        assert HUKM_RANK_CEILING == IFADAH_RANK_CEILING

    def test_rank_meet_with_ifadah_rank(self) -> None:
        """Rank is the meet of ifadah rank and HUKM_RANK_CEILING."""
        ifadah = _proven_ifadah_verdict()
        verdict = prove_hukm_candidate(
            ifadah_verdict=ifadah,
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.PROVEN
        expected_rank = min(ifadah.verdict_rank, HUKM_RANK_CEILING)
        assert verdict.verdict_rank == expected_rank


# ===========================================================================
# §10 Trace presence tests
# ===========================================================================


class TestTracePresence:
    """Every verdict carries a non-empty trace_ref."""

    def test_proven_verdict_has_trace(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.trace_ref
        assert "proven" in verdict.trace_ref

    def test_refused_verdict_has_trace(self) -> None:
        verdict = prove_hukm_candidate(
            ifadah_verdict="invalid",  # type: ignore[arg-type]
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert verdict.verdict_state is HukmState.REFUSED
        assert verdict.trace_ref
        assert "refused" in verdict.trace_ref


# ===========================================================================
# §11 HukmCandidate birth guard tests
# ===========================================================================


class TestHukmCandidateBirthGuards:
    """HukmCandidate dataclass rejects invalid construction."""

    def test_rejects_empty_ifadah_verdict_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            HukmCandidate(
                ifadah_verdict_ref="",
                evaluation_domain=EvaluationDomain.LINGUISTIC,
                hukm_claim="claim",
                hukm_evidence="evidence",
                hukm_maqam="maqam",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_empty_hukm_claim(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            HukmCandidate(
                ifadah_verdict_ref="ref",
                evaluation_domain=EvaluationDomain.LINGUISTIC,
                hukm_claim="",
                hukm_evidence="evidence",
                hukm_maqam="maqam",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_empty_hukm_evidence(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            HukmCandidate(
                ifadah_verdict_ref="ref",
                evaluation_domain=EvaluationDomain.LINGUISTIC,
                hukm_claim="claim",
                hukm_evidence="",
                hukm_maqam="maqam",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_empty_hukm_maqam(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            HukmCandidate(
                ifadah_verdict_ref="ref",
                evaluation_domain=EvaluationDomain.LINGUISTIC,
                hukm_claim="claim",
                hukm_evidence="evidence",
                hukm_maqam="",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_rank_exceeds_ceiling(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            HukmCandidate(
                ifadah_verdict_ref="ref",
                evaluation_domain=EvaluationDomain.LINGUISTIC,
                hukm_claim="claim",
                hukm_evidence="evidence",
                hukm_maqam="maqam",
                closure_scope="scope",
                rank=Rank.CERTIFICATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_empty_trace_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            HukmCandidate(
                ifadah_verdict_ref="ref",
                evaluation_domain=EvaluationDomain.LINGUISTIC,
                hukm_claim="claim",
                hukm_evidence="evidence",
                hukm_maqam="maqam",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# §12 Forbidden symbol test (docs/43 §10)
# ===========================================================================


class TestForbiddenSymbols:
    """PR-21 module does not export or instantiate forbidden symbols."""

    def test_no_forbidden_symbols_in_module(self) -> None:
        module_path = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/hukm_candidate.py"
        )
        source = module_path.read_text()
        tree = ast.parse(source)
        # Collect all Name nodes
        names_used = {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }
        for forbidden in FORBIDDEN_SYMBOLS:
            assert forbidden not in names_used, (
                f"Forbidden symbol '{forbidden}' found in hukm_candidate.py"
            )

    def test_no_forbidden_in_all_exports(self) -> None:
        from taaqqul_slot_geometry.weight import hukm_candidate

        for forbidden in FORBIDDEN_SYMBOLS:
            assert not hasattr(hukm_candidate, forbidden), (
                f"Forbidden symbol '{forbidden}' exported from module"
            )


# ===========================================================================
# §13 HukmState and EvaluationDomain enum tests
# ===========================================================================


class TestEnums:
    """HukmState has PROVEN/REFUSED; EvaluationDomain has 3 members."""

    def test_hukm_state_only_two_members(self) -> None:
        assert len(HukmState) == 2

    def test_hukm_state_proven_member(self) -> None:
        assert HukmState.PROVEN.value == "PROVEN"

    def test_hukm_state_refused_member(self) -> None:
        assert HukmState.REFUSED.value == "REFUSED"

    def test_evaluation_domain_three_members(self) -> None:
        assert len(EvaluationDomain) == 3

    def test_evaluation_domain_linguistic(self) -> None:
        assert EvaluationDomain.LINGUISTIC.value == "LINGUISTIC"

    def test_evaluation_domain_logical(self) -> None:
        assert EvaluationDomain.LOGICAL.value == "LOGICAL"

    def test_evaluation_domain_normative_candidate(self) -> None:
        assert EvaluationDomain.NORMATIVE_CANDIDATE.value == "NORMATIVE_CANDIDATE"
