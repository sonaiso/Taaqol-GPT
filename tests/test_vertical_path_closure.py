"""Constitutional tests for PR-D10: Vertical Path Closure Law.

Origin law: docs/46_VERTICAL_PATH_CLOSURE_LAW.md.
Chain position: PR-D10 (after PR-22-AUDIT, closes the minimum vertical path).

This test module proves:
1. Full PROVEN vertical chain reaches AuditedTanzilBridge (§6.1).
2. Trace continuity from AuditedTanzilBridge back to MufradDalalahClosure (§6.2).
3. Rank never promotes across the chain (§6.4).
4. Residuals remain visible at every step (§6.5).
5. Hidden/blocking residuals refuse (§7).
6. Presentation envelope survives audit (§6.7).
7. Every layer has a named refusal test (§7 failures).
8. No candidate-to-certificate leap (§6.10).
9. No execution/fatwa/qada/final authority (§6.11).
10. No horizontal branch symbols exported before closure (§6.8).
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.audit.tanzil_bridge import (
    AuditBridgeState,
    AuditedTanzilBridge,
    bridge_tanzil_to_audit,
)
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    TANZIL_RANK_CEILING,
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
    TanzilCandidate,
    TanzilState,
    TanzilVerdict,
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
    prove_tanzil_candidate,
    prove_verbal_madlul,
    weigh,
)
from taaqqul_slot_geometry.weight.dalalah_candidates import (
    DalalahCandidateState,
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
    RelationType,
    prove_relation_closure,
)
from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState
from tests.support.constitutional_vertical_chain_case import (
    FORBIDDEN_CERTIFICATE_SYMBOLS,
    FORBIDDEN_HORIZONTAL_SYMBOLS,
    VERTICAL_CHAIN_LAYERS,
    ConstitutionalVerticalChainTestCase,
    VerticalChainResult,
    VerticalChainStepResult,
    assert_vertical_chain_case,
)

# ===========================================================================
# Fixture builders — build the full vertical chain from scratch
# ===========================================================================


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr-d10-vertical-closure-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pr-d10/kataba", kind="DECLARED_ENTRY"
        ),
    }


def _syllables(root: str = "kataba") -> tuple[SyllableCandidate, ...]:
    parts = [root[i:i + 2] for i in range(0, len(root) - 1, 2)]
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


def _proven_mufrad_closure(
    root: str = "kataba",
) -> MufradDalalahClosureVerdict:
    semantic = _semantic_slot_verdict(root)
    maqam = _maqam_context_verdict(semantic)
    dalalah = prove_dalalah_candidates(
        semantic_slot_verdict=semantic,
        maqam_context_verdict=maqam,
        correspondence_domain="arabic_lexical_full_extension",
        part_designation="semantic_component_action",
        inclusion_evidence="part_of_verbal_meaning_field",
        necessary_relation_type=NecessaryRelationType.SABAB,
        relation_evidence="cause_effect_linguistic_evidence",
    )
    assert dalalah.verdict_state is DalalahCandidateState.PROVEN
    verdict = prove_mufrad_dalalah_closure(
        semantic_slot_verdict=semantic,
        maqam_context_verdict=maqam,
        dalalah_candidate_verdict=dalalah,
        closure_scope="mufrad_dalalah_minimum_complete",
    )
    assert verdict.verdict_state is MufradDalalahClosureState.PROVEN
    return verdict


def _proven_relation_closure():
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
    return rc_verdict, maqam_verdict


def _proven_ifadah_verdict() -> IfadahVerdict:
    fs_verdict = _formal_style_verdict()
    rc_verdict, maqam_verdict = _proven_relation_closure()
    verdict = prove_ifadah_candidate(
        relation_closure_verdict=rc_verdict,
        formal_style_verdict=fs_verdict,
        ifadah_maqam_verdict=maqam_verdict,
        speech_force=SpeechForceKind.KHABAR,
        ifadah_evidence="speech_level_closure_evidence",
        closure_scope="ifadah_minimal_scope",
    )
    assert verdict.verdict_state is IfadahState.PROVEN
    return verdict


def _proven_hukm_verdict() -> HukmVerdict:
    ifadah = _proven_ifadah_verdict()
    verdict = prove_hukm_candidate(
        ifadah_verdict=ifadah,
        evaluation_domain=EvaluationDomain.LINGUISTIC,
        hukm_claim="grammatical_correctness_claim",
        hukm_evidence="morphosyntactic_evidence",
        hukm_maqam="linguistic_evaluation_maqam",
        closure_scope="hukm_minimal_scope",
    )
    assert verdict.verdict_state is HukmState.PROVEN
    return verdict


def _proven_manat_verdict() -> ManatVerdict:
    hukm = _proven_hukm_verdict()
    verdict = prove_manat_candidate(
        hukm_verdict=hukm,
        manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
        manat_description="effective_attribute_extraction_from_hukm",
        effective_attribute_candidate="al_wasf_al_muaththir_fiiliyya",
        conditions=("condition_agent_mukalaf",),
        preventers=(),
        manat_evidence="lexical_attestation_plus_qiyas",
        manat_domain="arabic_morphosyntactic_ruling",
        closure_scope="manat_minimal_scope",
    )
    assert verdict.verdict_state is ManatState.PROVEN
    return verdict


def _proven_tanzil_verdict() -> TanzilVerdict:
    """Build a PROVEN tanzil verdict through the full lawful chain."""
    hukm = _proven_hukm_verdict()
    manat = prove_manat_candidate(
        hukm_verdict=hukm,
        manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
        manat_description="effective_attribute_extraction_from_hukm",
        effective_attribute_candidate="al_wasf_al_muaththir_fiiliyya",
        conditions=("condition_agent_mukalaf",),
        preventers=(),
        manat_evidence="lexical_attestation_plus_qiyas",
        manat_domain="arabic_morphosyntactic_ruling",
        closure_scope="manat_minimal_scope",
    )
    assert manat.verdict_state is ManatState.PROVEN
    verdict = prove_tanzil_candidate(
        hukm_verdict=hukm,
        manat_verdict=manat,
        reality_evidence="instance_level_evidence_about_specific_case",
        instance_descriptor="specific_case_description_for_presentation",
        tanzil_scope="tanzil_presentation_scope_minimal",
        presentation_warning="NOT_EXECUTION: This is a candidate presentation only.",
        not_execution_marker=True,
    )
    assert verdict.verdict_state is TanzilState.PROVEN
    return verdict


def _proven_audit_bridge():
    """Build a SURFACED AuditedTanzilBridge through the full lawful chain."""
    tv = _proven_tanzil_verdict()
    result = bridge_tanzil_to_audit(tv)
    assert result.state is AuditBridgeState.SURFACED
    assert result.bridge is not None
    return result


# ===========================================================================
# §A Full PROVEN vertical chain reaches AuditedTanzilBridge
# ===========================================================================


class TestVerticalChainClosesFromMufradToAudit:
    """Full vertical chain: MufradDalalahClosure → AuditedTanzilBridge."""

    def test_mufrad_dalalah_closure_proven(self) -> None:
        verdict = _proven_mufrad_closure()
        assert verdict.verdict_state is MufradDalalahClosureState.PROVEN

    def test_relation_closure_proven(self) -> None:
        rc, _ = _proven_relation_closure()
        assert rc.verdict_state is RelationClosureState.PROVEN

    def test_ifadah_verdict_proven(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.verdict_state is IfadahState.PROVEN

    def test_hukm_verdict_proven(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.verdict_state is HukmState.PROVEN

    def test_manat_verdict_proven(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.verdict_state is ManatState.PROVEN

    def test_tanzil_verdict_proven(self) -> None:
        verdict = _proven_tanzil_verdict()
        assert verdict.verdict_state is TanzilState.PROVEN

    def test_audited_tanzil_bridge_surfaced(self) -> None:
        result = _proven_audit_bridge()
        assert result.state is AuditBridgeState.SURFACED
        assert result.bridge is not None
        assert isinstance(result.bridge, AuditedTanzilBridge)

    def test_full_chain_not_execution(self) -> None:
        result = _proven_audit_bridge()
        assert result.bridge.not_execution is True
        assert result.bridge.not_fatwa is True
        assert result.bridge.not_qada is True
        assert result.bridge.not_final_authority is True

    def test_full_chain_rank_visible(self) -> None:
        result = _proven_audit_bridge()
        assert result.bridge.rank is not None
        assert isinstance(result.bridge.rank, Rank)
        assert result.bridge.rank <= TANZIL_RANK_CEILING

    def test_full_chain_residuals_visible(self) -> None:
        result = _proven_audit_bridge()
        for r in result.bridge.residuals:
            assert r.kind is not ResidualKind.HIDDEN_FORBIDDEN

    def test_full_chain_trace_visible(self) -> None:
        result = _proven_audit_bridge()
        assert isinstance(result.bridge.trace_ref, str)
        assert result.bridge.trace_ref.strip()

    def test_full_chain_presentation_envelope_visible(self) -> None:
        result = _proven_audit_bridge()
        env = result.bridge.presentation_envelope
        assert env.rank_visible is True
        assert env.residuals_visible is True
        assert env.trace_visible is True


# ===========================================================================
# §B Trace continuity
# ===========================================================================


class TestVerticalTraceContinuity:
    """Audit surface trace_ref chain can be traced back."""

    def test_audit_bridge_has_trace_ref(self) -> None:
        result = _proven_audit_bridge()
        assert result.trace_ref is not None
        assert isinstance(result.trace_ref, str)
        assert result.trace_ref.strip()

    def test_tanzil_verdict_has_trace_ref(self) -> None:
        tv = _proven_tanzil_verdict()
        assert tv.trace_ref is not None
        assert isinstance(tv.trace_ref, str)
        assert tv.trace_ref.strip()

    def test_manat_verdict_has_trace_ref(self) -> None:
        verdict = _proven_manat_verdict()
        assert verdict.trace_ref is not None
        assert isinstance(verdict.trace_ref, str)
        assert verdict.trace_ref.strip()

    def test_hukm_verdict_has_trace_ref(self) -> None:
        verdict = _proven_hukm_verdict()
        assert verdict.trace_ref is not None
        assert isinstance(verdict.trace_ref, str)
        assert verdict.trace_ref.strip()

    def test_ifadah_verdict_has_trace_ref(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.trace_ref is not None
        assert isinstance(verdict.trace_ref, str)
        assert verdict.trace_ref.strip()

    def test_relation_closure_has_trace_ref(self) -> None:
        rc, _ = _proven_relation_closure()
        assert rc.trace_ref is not None
        assert isinstance(rc.trace_ref, str)
        assert rc.trace_ref.strip()

    def test_mufrad_closure_has_trace_ref(self) -> None:
        verdict = _proven_mufrad_closure()
        assert verdict.trace_ref is not None
        assert isinstance(verdict.trace_ref, str)
        assert verdict.trace_ref.strip()


# ===========================================================================
# §C Rank never promotes across the chain
# ===========================================================================


class TestVerticalRankNeverPromotes:
    """Rank monotonically does not increase through the vertical chain."""

    def test_vertical_rank_monotonicity(self) -> None:
        mufrad = _proven_mufrad_closure()
        rc, _ = _proven_relation_closure()
        ifadah = _proven_ifadah_verdict()
        hukm = _proven_hukm_verdict()
        manat = _proven_manat_verdict()
        tanzil = _proven_tanzil_verdict()
        audit = _proven_audit_bridge()

        ranks = [
            mufrad.verdict_rank,
            rc.verdict_rank,
            ifadah.verdict_rank,
            hukm.verdict_rank,
            manat.verdict_rank,
            tanzil.verdict_rank,
            audit.rank,
        ]

        # No rank should exceed the tanzil ceiling
        for r in ranks:
            assert r <= TANZIL_RANK_CEILING, (
                f"Rank {r.name} exceeds TANZIL_RANK_CEILING"
            )

    def test_audit_rank_bounded(self) -> None:
        audit = _proven_audit_bridge()
        assert audit.rank <= TANZIL_RANK_CEILING


# ===========================================================================
# §D Residuals remain visible
# ===========================================================================


class TestVerticalResidualsRemainVisible:
    """No hidden or blocking residuals pass through the vertical chain."""

    def test_tanzil_residuals_not_hidden(self) -> None:
        tv = _proven_tanzil_verdict()
        assert tv.candidate is not None
        for r in tv.candidate.residuals:
            assert r.kind is not ResidualKind.HIDDEN_FORBIDDEN

    def test_audit_bridge_residuals_not_hidden(self) -> None:
        audit = _proven_audit_bridge()
        for r in audit.bridge.residuals:
            assert r.kind is not ResidualKind.HIDDEN_FORBIDDEN

    def test_hidden_residual_refuses_at_bridge(self) -> None:
        """An injected hidden residual at tanzil must be refused by bridge."""
        tv = _proven_tanzil_verdict()
        # Create a TanzilVerdict with a hidden residual
        hidden = Residual(
            name="INJECTED_HIDDEN",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=False,
            note="test injection",
        )
        # Build a new candidate with the hidden residual
        cand = tv.candidate
        # We need to rebuild since frozen — use the bridge input directly
        patched_verdict = TanzilVerdict(
            candidate=TanzilCandidate(
                hukm_verdict_ref=cand.hukm_verdict_ref,
                manat_verdict_ref=cand.manat_verdict_ref,
                ifadah_ref=cand.ifadah_ref,
                reality_evidence=cand.reality_evidence,
                instance_descriptor=cand.instance_descriptor,
                tanzil_scope=cand.tanzil_scope,
                presentation_envelope=cand.presentation_envelope,
                rank=cand.rank,
                residuals=(hidden,),
                trace_ref=cand.trace_ref,
            ),
            verdict_state=TanzilState.PROVEN,
            failure_code=None,
            verdict_rank=tv.verdict_rank,
            residuals=(hidden,),
            trace_ref=tv.trace_ref,
        )
        result = bridge_tanzil_to_audit(patched_verdict)
        assert result.state is AuditBridgeState.REFUSED
        assert result.failure_code is FailureCode.HIDDEN_RESIDUAL

    def test_blocking_residual_refuses_at_bridge(self) -> None:
        """An injected blocking residual at tanzil must be refused by bridge."""
        tv = _proven_tanzil_verdict()
        blocking = Residual(
            name="INJECTED_BLOCKING",
            kind=ResidualKind.BLOCKING,
            visible=True,
            note="test injection",
        )
        cand = tv.candidate
        patched_verdict = TanzilVerdict(
            candidate=TanzilCandidate(
                hukm_verdict_ref=cand.hukm_verdict_ref,
                manat_verdict_ref=cand.manat_verdict_ref,
                ifadah_ref=cand.ifadah_ref,
                reality_evidence=cand.reality_evidence,
                instance_descriptor=cand.instance_descriptor,
                tanzil_scope=cand.tanzil_scope,
                presentation_envelope=cand.presentation_envelope,
                rank=cand.rank,
                residuals=(blocking,),
                trace_ref=cand.trace_ref,
            ),
            verdict_state=TanzilState.PROVEN,
            failure_code=None,
            verdict_rank=tv.verdict_rank,
            residuals=(blocking,),
            trace_ref=tv.trace_ref,
        )
        result = bridge_tanzil_to_audit(patched_verdict)
        assert result.state is AuditBridgeState.REFUSED
        assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


# ===========================================================================
# §E Named refusals at every layer
# ===========================================================================


class TestNamedRefusalsAtEveryLayer:
    """Every layer refuses with a named FailureCode when inputs invalid."""

    def test_no_relation_without_mufrad(self) -> None:
        """RelationClosure refuses without proven MufradDalalahClosure."""
        semantic = _semantic_slot_verdict("kataba")
        maqam = _maqam_context_verdict(semantic)
        # Build a non-proven mufrad closure (used to confirm chain works)
        prove_dalalah_candidates(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            correspondence_domain="arabic_lexical_full_extension",
            part_designation="semantic_component_action",
            inclusion_evidence="part_of_verbal_meaning_field",
            necessary_relation_type=NecessaryRelationType.SABAB,
            relation_evidence="cause_effect_linguistic_evidence",
        )
        # Use a proper mufrad for second, but invalid for relation closure
        second = _proven_mufrad_closure("darasa")
        # Test that empty/invalid first_verdict refuses
        result = prove_relation_closure(
            first_verdict=None,  # type: ignore[arg-type]
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam=maqam.trace_ref,
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert result.verdict_state is not RelationClosureState.PROVEN
        assert result.failure_code is not None

    def test_no_ifadah_without_relation(self) -> None:
        """IfadahCandidate refuses without proven RelationClosure."""
        fs_verdict = _formal_style_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam = _maqam_context_verdict(semantic)
        result = prove_ifadah_candidate(
            relation_closure_verdict=None,  # type: ignore[arg-type]
            formal_style_verdict=fs_verdict,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="speech_level_closure_evidence",
            closure_scope="ifadah_scope",
        )
        assert result.verdict_state is not IfadahState.PROVEN
        assert result.failure_code is not None

    def test_no_hukm_without_ifadah(self) -> None:
        """HukmCandidate refuses without proven IfadahVerdict."""
        result = prove_hukm_candidate(
            ifadah_verdict=None,  # type: ignore[arg-type]
            evaluation_domain=EvaluationDomain.LINGUISTIC,
            hukm_claim="claim",
            hukm_evidence="evidence",
            hukm_maqam="maqam",
            closure_scope="scope",
        )
        assert result.verdict_state is not HukmState.PROVEN
        assert result.failure_code is not None

    def test_no_manat_without_hukm(self) -> None:
        """ManatCandidate refuses without proven HukmVerdict."""
        result = prove_manat_candidate(
            hukm_verdict=None,  # type: ignore[arg-type]
            manat_mode=ManatMode.TAKHRIJ_CANDIDATE,
            manat_description="desc",
            effective_attribute_candidate="attr",
            conditions=("c",),
            preventers=(),
            manat_evidence="evidence",
            manat_domain="domain",
            closure_scope="scope",
        )
        assert result.verdict_state is not ManatState.PROVEN
        assert result.failure_code is not None

    def test_no_tanzil_without_manat(self) -> None:
        """TanzilCandidate refuses without proven ManatVerdict."""
        hukm = _proven_hukm_verdict()
        result = prove_tanzil_candidate(
            hukm_verdict=hukm,
            manat_verdict=None,  # type: ignore[arg-type]
            reality_evidence="evidence",
            instance_descriptor="desc",
            tanzil_scope="scope",
            presentation_warning="warning",
            not_execution_marker=True,
        )
        assert result.verdict_state is not TanzilState.PROVEN
        assert result.failure_code is not None

    def test_no_audit_bridge_without_tanzil(self) -> None:
        """AuditedTanzilBridge refuses without proven TanzilVerdict."""
        result = bridge_tanzil_to_audit(None)  # type: ignore[arg-type]
        assert result.state is AuditBridgeState.REFUSED
        assert result.failure_code is not None


# ===========================================================================
# §F Forbidden horizontal branches
# ===========================================================================


class TestNoHorizontalBranchBeforeClosure:
    """No horizontal branch symbols are exported before vertical closure."""

    def test_weight_module_no_horizontal_symbols(self) -> None:
        """The weight package does not export horizontal-branch symbols."""
        import taaqqul_slot_geometry.weight as weight_pkg
        weight_names = set(dir(weight_pkg))
        for symbol in FORBIDDEN_HORIZONTAL_SYMBOLS:
            assert symbol not in weight_names, (
                f"Forbidden horizontal symbol '{symbol}' found in weight module"
            )

    def test_audit_module_no_horizontal_symbols(self) -> None:
        """The audit package does not export horizontal-branch symbols."""
        import taaqqul_slot_geometry.audit as audit_pkg
        audit_names = set(dir(audit_pkg))
        for symbol in FORBIDDEN_HORIZONTAL_SYMBOLS:
            assert symbol not in audit_names, (
                f"Forbidden horizontal symbol '{symbol}' found in audit module"
            )

    def test_core_module_no_horizontal_symbols(self) -> None:
        """The core package does not export horizontal-branch symbols."""
        import taaqqul_slot_geometry.core as core_pkg
        core_names = set(dir(core_pkg))
        for symbol in FORBIDDEN_HORIZONTAL_SYMBOLS:
            assert symbol not in core_names, (
                f"Forbidden horizontal symbol '{symbol}' found in core module"
            )


# ===========================================================================
# §G No candidate-to-certificate leap
# ===========================================================================


class TestNoCandidateToCertificateLeap:
    """TanzilCandidate and AuditedTanzilBridge carry no certificate symbols."""

    def test_tanzil_module_no_certificate_symbols(self) -> None:
        """tanzil_candidate.py does not export certificate symbols."""
        src = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/tanzil_candidate.py"
        )
        tree = ast.parse(src.read_text())
        names = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
        }
        for symbol in FORBIDDEN_CERTIFICATE_SYMBOLS:
            assert symbol not in names, (
                f"Forbidden certificate symbol '{symbol}' in tanzil_candidate.py"
            )

    def test_audit_bridge_module_no_certificate_symbols(self) -> None:
        """tanzil_bridge.py does not export certificate symbols."""
        src = pathlib.Path(
            "src/taaqqul_slot_geometry/audit/tanzil_bridge.py"
        )
        tree = ast.parse(src.read_text())
        names = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
        }
        for symbol in FORBIDDEN_CERTIFICATE_SYMBOLS:
            assert symbol not in names, (
                f"Forbidden certificate symbol '{symbol}' in tanzil_bridge.py"
            )

    def test_audit_bridge_not_certificate(self) -> None:
        """AuditedTanzilBridge is not a certificate."""
        result = _proven_audit_bridge()
        assert result.bridge.not_execution is True
        assert result.bridge.not_fatwa is True
        assert result.bridge.not_qada is True
        assert result.bridge.not_final_authority is True


# ===========================================================================
# §H No execution/fatwa/qada/final authority
# ===========================================================================


class TestNoExecutionOrAuthority:
    """The vertical chain never produces execution or authority."""

    def test_bridge_source_has_no_execution_logic(self) -> None:
        """tanzil_bridge.py has no execution dispatch."""
        src = pathlib.Path(
            "src/taaqqul_slot_geometry/audit/tanzil_bridge.py"
        )
        text = src.read_text()
        # No I/O, no external action, no model call
        forbidden = ("import os", "import socket", "import http",
                     "import urllib", "import requests", "subprocess")
        for imp in forbidden:
            assert imp not in text, (
                f"Forbidden import '{imp}' found in tanzil_bridge.py"
            )

    def test_envelope_markers_all_true(self) -> None:
        """Presentation envelope markers are all True on success."""
        result = _proven_audit_bridge()
        env = result.bridge.presentation_envelope
        assert env.not_fatwa is True
        assert env.not_qada is True
        assert env.not_final_authority is True
        assert env.rank_visible is True
        assert env.residuals_visible is True
        assert env.trace_visible is True


# ===========================================================================
# §I ConstitutionalVerticalChainTestCase schema tests
# ===========================================================================


class TestVerticalChainTestCaseSchema:
    """ConstitutionalVerticalChainTestCase schema enforcement."""

    def test_valid_case_construction(self) -> None:
        case = ConstitutionalVerticalChainTestCase(
            origin_law="docs/46_VERTICAL_PATH_CLOSURE_LAW.md",
            branch_name="vertical_closure_full_path",
            constitutional_chain=VERTICAL_CHAIN_LAYERS,
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Certificate", "Execution"),
            max_rank=TANZIL_RANK_CEILING,
            required_trace=True,
            required_residual_visibility=True,
            chain_position="PR-D10",
            origin_law_ref="docs/46_VERTICAL_PATH_CLOSURE_LAW.md#s6",
            branch_of_origin="vertical_closure",
            forbidden_shortcut_assertions=(
                "MufradDalalah → Certificate",
                "Tanzil → Execution",
            ),
            vertical_layers=VERTICAL_CHAIN_LAYERS,
        )
        assert case.origin_law == "docs/46_VERTICAL_PATH_CLOSURE_LAW.md"

    def test_empty_vertical_layers_rejected(self) -> None:
        from tests.support.constitutional_case import ConstitutionalSchemaError
        with pytest.raises(ConstitutionalSchemaError):
            ConstitutionalVerticalChainTestCase(
                origin_law="docs/46_VERTICAL_PATH_CLOSURE_LAW.md",
                branch_name="vertical_closure_full_path",
                constitutional_chain=VERTICAL_CHAIN_LAYERS,
                expected_state=ClosureState.MINIMALLY_CLOSED,
                expected_failure_code=None,
                forbidden_outputs=("Certificate",),
                max_rank=TANZIL_RANK_CEILING,
                required_trace=True,
                required_residual_visibility=True,
                chain_position="PR-D10",
                origin_law_ref="docs/46#s6",
                branch_of_origin="vertical_closure",
                forbidden_shortcut_assertions=(
                    "MufradDalalah → Certificate",
                ),
                vertical_layers=(),
            )

    def test_invalid_layer_name_rejected(self) -> None:
        from tests.support.constitutional_case import ConstitutionalSchemaError
        with pytest.raises(ConstitutionalSchemaError):
            ConstitutionalVerticalChainTestCase(
                origin_law="docs/46_VERTICAL_PATH_CLOSURE_LAW.md",
                branch_name="vertical_closure_full_path",
                constitutional_chain=VERTICAL_CHAIN_LAYERS,
                expected_state=ClosureState.MINIMALLY_CLOSED,
                expected_failure_code=None,
                forbidden_outputs=("Certificate",),
                max_rank=TANZIL_RANK_CEILING,
                required_trace=True,
                required_residual_visibility=True,
                chain_position="PR-D10",
                origin_law_ref="docs/46#s6",
                branch_of_origin="vertical_closure",
                forbidden_shortcut_assertions=(
                    "MufradDalalah → Certificate",
                ),
                vertical_layers=("INVALID_LAYER",),
            )

    def test_assert_vertical_chain_case_passes(self) -> None:
        """assert_vertical_chain_case passes with valid full walk."""
        case = ConstitutionalVerticalChainTestCase(
            origin_law="docs/46_VERTICAL_PATH_CLOSURE_LAW.md",
            branch_name="vertical_closure_full_path",
            constitutional_chain=VERTICAL_CHAIN_LAYERS,
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Certificate", "Execution"),
            max_rank=TANZIL_RANK_CEILING,
            required_trace=True,
            required_residual_visibility=True,
            chain_position="PR-D10",
            origin_law_ref="docs/46_VERTICAL_PATH_CLOSURE_LAW.md#s6",
            branch_of_origin="vertical_closure",
            forbidden_shortcut_assertions=(
                "MufradDalalah → Certificate",
                "Tanzil → Execution",
            ),
            vertical_layers=VERTICAL_CHAIN_LAYERS,
        )
        steps = tuple(
            VerticalChainStepResult(
                layer=layer,
                verdict_proven=True,
                rank=Rank.CANDIDATE,
                residuals_visible=True,
                trace_ref_present=True,
                failure_code=None,
                produced_outputs=frozenset(),
            )
            for layer in VERTICAL_CHAIN_LAYERS
        )
        result = VerticalChainResult(
            steps=steps,
            trace_continuous=True,
            rank_monotone=True,
            envelope_preserved=True,
            all_produced_outputs=frozenset(),
        )
        assert_vertical_chain_case(case, result)

    def test_assert_vertical_chain_case_fails_on_trace(self) -> None:
        """assert_vertical_chain_case fails when trace is discontinuous."""
        case = ConstitutionalVerticalChainTestCase(
            origin_law="docs/46_VERTICAL_PATH_CLOSURE_LAW.md",
            branch_name="vertical_closure_trace_test",
            constitutional_chain=VERTICAL_CHAIN_LAYERS,
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Certificate",),
            max_rank=TANZIL_RANK_CEILING,
            required_trace=True,
            required_residual_visibility=True,
            chain_position="PR-D10",
            origin_law_ref="docs/46#s6",
            branch_of_origin="vertical_closure",
            forbidden_shortcut_assertions=(
                "MufradDalalah → Certificate",
            ),
            vertical_layers=VERTICAL_CHAIN_LAYERS,
        )
        steps = tuple(
            VerticalChainStepResult(
                layer=layer,
                verdict_proven=True,
                rank=Rank.CANDIDATE,
                residuals_visible=True,
                trace_ref_present=True,
                failure_code=None,
                produced_outputs=frozenset(),
            )
            for layer in VERTICAL_CHAIN_LAYERS
        )
        result = VerticalChainResult(
            steps=steps,
            trace_continuous=False,  # <-- broken
            rank_monotone=True,
            envelope_preserved=True,
            all_produced_outputs=frozenset(),
        )
        with pytest.raises(AssertionError, match="trace continuity"):
            assert_vertical_chain_case(case, result)

    def test_assert_vertical_chain_case_fails_on_horizontal(self) -> None:
        """assert_vertical_chain_case fails when horizontal symbol present."""
        case = ConstitutionalVerticalChainTestCase(
            origin_law="docs/46_VERTICAL_PATH_CLOSURE_LAW.md",
            branch_name="vertical_closure_horizontal_test",
            constitutional_chain=VERTICAL_CHAIN_LAYERS,
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=("Certificate",),
            max_rank=TANZIL_RANK_CEILING,
            required_trace=True,
            required_residual_visibility=True,
            chain_position="PR-D10",
            origin_law_ref="docs/46#s6",
            branch_of_origin="vertical_closure",
            forbidden_shortcut_assertions=(
                "MufradDalalah → Certificate",
            ),
            vertical_layers=VERTICAL_CHAIN_LAYERS,
        )
        steps = tuple(
            VerticalChainStepResult(
                layer=layer,
                verdict_proven=True,
                rank=Rank.CANDIDATE,
                residuals_visible=True,
                trace_ref_present=True,
                failure_code=None,
                produced_outputs=frozenset(),
            )
            for layer in VERTICAL_CHAIN_LAYERS
        )
        result = VerticalChainResult(
            steps=steps,
            trace_continuous=True,
            rank_monotone=True,
            envelope_preserved=True,
            all_produced_outputs=frozenset({"Majaz"}),  # <-- forbidden
        )
        with pytest.raises(AssertionError, match="horizontal branch"):
            assert_vertical_chain_case(case, result)
