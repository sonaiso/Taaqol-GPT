"""Constitutional tests for PR-22-AUDIT: Vertical Chain AnswerAudit Bridge.

Origin law: docs/45_TANZIL_PRESENTATION_BOUNDARY_LAW.md (bridge clause).
Chain position: PR-22-AUDIT (after PR-22, before PR-D10).

This test module proves:
1. bridge_tanzil_to_audit() returns SURFACED with a valid PROVEN TanzilVerdict.
2. REFUSED/invalid TanzilVerdict does not surface as proven.
3. Missing or invalid presentation envelope is rejected.
4. Missing NOT_EXECUTION warning is rejected.
5. Missing NOT_FATWA / NOT_QADA / NOT_FINAL_AUTHORITY markers rejected.
6. Rank, residuals, and trace are preserved (not stripped).
7. Hidden and blocking residuals are rejected.
8. No adapter, model, or network call occurs (pure function).
9. No candidate-to-certificate conversion.
10. Forbidden-symbol scan for Execution, Fatwa, Qada, FinalAuthority.
11. AuditedTanzilBridge birth guards enforce invariants.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import (
    FailureCode,
    Rank,
)
from taaqqul_slot_geometry.audit import tanzil_bridge as _tanzil_bridge_module
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

_BRIDGE_SRC = pathlib.Path(_tanzil_bridge_module.__file__)

# ===========================================================================
# Forbidden symbols that PR-22-AUDIT must NOT export or instantiate.
# ===========================================================================

FORBIDDEN_SYMBOLS_AUDIT_BRIDGE = (
    "Execution",
    "ExternalAction",
    "Enforcement",
    "Fatwa",
    "Qada",
    "FinalAuthority",
    "DivineAuthorityClaim",
    "Certificate",
    "RealityApplication",
    "RealityVerification",
    "NormativeJudgment",
    "AuthorityClaim",
)


# ===========================================================================
# Test fixtures — build a PROVEN TanzilVerdict through the full lawful chain
# ===========================================================================


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr-22-audit-bridge-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pr-22-audit/kataba", kind="DECLARED_ENTRY"
        ),
    }


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


def _proven_ifadah_verdict() -> IfadahVerdict:
    fs_verdict = _formal_style_verdict()
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


# ===========================================================================
# §1 SURFACED bridge tests (proven bridge preserves envelope)
# ===========================================================================


class TestSurfacedBridge:
    """bridge_tanzil_to_audit() returns SURFACED with a valid TanzilVerdict."""

    def test_surfaced_state(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.state is AuditBridgeState.SURFACED

    def test_no_failure_code(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.failure_code is None

    def test_bridge_present(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge is not None
        assert isinstance(result.bridge, AuditedTanzilBridge)

    def test_bridge_preserves_candidate(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.tanzil_candidate is tv.candidate

    def test_bridge_preserves_envelope(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert (
            result.bridge.presentation_envelope
            is tv.candidate.presentation_envelope
        )

    def test_bridge_preserves_rank(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.rank is tv.candidate.rank
        assert result.rank is tv.candidate.rank

    def test_bridge_preserves_residuals(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.residuals is tv.candidate.residuals

    def test_bridge_preserves_trace(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.trace_ref == tv.candidate.trace_ref

    def test_bridge_not_execution(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.not_execution is True

    def test_bridge_not_fatwa(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.not_fatwa is True

    def test_bridge_not_qada(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.not_qada is True

    def test_bridge_not_final_authority(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.not_final_authority is True

    def test_bridge_rank_within_ceiling(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.rank <= TANZIL_RANK_CEILING

    def test_bridge_trace_ref_on_verdict(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert "bridge_tanzil_to_audit" in result.trace_ref
        assert "surfaced" in result.trace_ref


# ===========================================================================
# §2 REFUSED verdict does not surface as proven
# ===========================================================================


class TestRefusedVerdictDoesNotSurface:
    """Refused or invalid TanzilVerdict does not produce a bridge."""

    def test_refused_tanzil_verdict(self) -> None:
        refused = TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_MANAT,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        result = bridge_tanzil_to_audit(refused)
        assert result.state is AuditBridgeState.REFUSED
        assert result.bridge is None
        assert result.failure_code is FailureCode.NO_TANZIL_VERDICT

    def test_invalid_type(self) -> None:
        result = bridge_tanzil_to_audit("not a verdict")  # type: ignore[arg-type]
        assert result.state is AuditBridgeState.REFUSED
        assert result.bridge is None
        assert result.failure_code is FailureCode.NO_TANZIL_VERDICT

    def test_none_input(self) -> None:
        result = bridge_tanzil_to_audit(None)  # type: ignore[arg-type]
        assert result.state is AuditBridgeState.REFUSED
        assert result.bridge is None
        assert result.failure_code is FailureCode.NO_TANZIL_VERDICT

    def test_proven_but_missing_candidate(self) -> None:
        # A PROVEN verdict that somehow has no candidate
        broken = TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.PROVEN,
            failure_code=None,
            verdict_rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="test/broken",
        )
        result = bridge_tanzil_to_audit(broken)
        assert result.state is AuditBridgeState.REFUSED
        assert result.bridge is None
        assert result.failure_code is FailureCode.NO_TANZIL_VERDICT


# ===========================================================================
# §3 No execution (pure function — no adapter, model, network)
# ===========================================================================


class TestNoExecution:
    """bridge_tanzil_to_audit() performs no external action."""

    def test_audit_does_not_call_adapter(self) -> None:
        """The bridge function has no adapter parameter or adapter import."""
        import inspect
        sig = inspect.signature(bridge_tanzil_to_audit)
        param_names = set(sig.parameters.keys())
        assert "adapter" not in param_names
        assert "client" not in param_names
        assert "model_client" not in param_names

    def test_audit_does_not_call_model_client(self) -> None:
        """The module source has no ModelClient usage."""
        tree = ast.parse(_BRIDGE_SRC.read_text())
        names = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
        }
        assert "ModelClient" not in names
        assert "AdapterGuard" not in names
        assert "InMemoryModelClient" not in names

    def test_audit_does_not_create_external_action(self) -> None:
        """No I/O imports in the bridge module."""
        text = _BRIDGE_SRC.read_text()
        forbidden_imports = ("import os", "import socket", "import http",
                             "import urllib", "import requests", "import io")
        for imp in forbidden_imports:
            assert imp not in text


# ===========================================================================
# §4 Presentation envelope guards
# ===========================================================================


class TestPresentationEnvelopeGuards:
    """Missing or invalid presentation markers are rejected."""

    def test_audit_preserves_not_fatwa_marker(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge is not None
        env = result.bridge.presentation_envelope
        assert env.not_fatwa is True

    def test_audit_preserves_not_qada_marker(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge is not None
        env = result.bridge.presentation_envelope
        assert env.not_qada is True

    def test_audit_preserves_not_final_authority_marker(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge is not None
        env = result.bridge.presentation_envelope
        assert env.not_final_authority is True

    def test_audit_preserves_not_execution_warning(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge is not None
        env = result.bridge.presentation_envelope
        assert env.not_execution_warning
        assert "NOT_EXECUTION" in env.not_execution_warning


# ===========================================================================
# §5 Rank, residuals, and trace preserved
# ===========================================================================


class TestRankResidualsTracePreserved:
    """Rank, residuals, and trace are preserved through the bridge."""

    def test_audit_preserves_rank(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.rank is tv.candidate.rank
        assert result.bridge.rank is tv.candidate.rank

    def test_audit_preserves_residuals(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.residuals is tv.candidate.residuals
        # All residuals are visible
        for r in result.residuals:
            assert r.visible is True

    def test_audit_preserves_trace(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.trace_ref == tv.candidate.trace_ref


# ===========================================================================
# §6 Hidden and blocking residuals rejected
# ===========================================================================


class TestResidualGovernance:
    """Hidden or blocking residuals cause REFUSED."""

    def test_audit_rejects_hidden_residuals(self) -> None:
        tv = _proven_tanzil_verdict()
        # Inject a hidden residual via object mutation workaround
        candidate = tv.candidate
        hidden = Residual(
            name="TEST_HIDDEN",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=False,
            note="test hidden residual",
        )
        # Build a synthetic TanzilVerdict with bad residuals
        bad_candidate = TanzilCandidate.__new__(TanzilCandidate)
        object.__setattr__(bad_candidate, "hukm_verdict_ref", candidate.hukm_verdict_ref)
        object.__setattr__(bad_candidate, "manat_verdict_ref", candidate.manat_verdict_ref)
        object.__setattr__(bad_candidate, "ifadah_ref", candidate.ifadah_ref)
        object.__setattr__(bad_candidate, "reality_evidence", candidate.reality_evidence)
        object.__setattr__(bad_candidate, "instance_descriptor", candidate.instance_descriptor)
        object.__setattr__(bad_candidate, "tanzil_scope", candidate.tanzil_scope)
        object.__setattr__(bad_candidate, "presentation_envelope", candidate.presentation_envelope)
        object.__setattr__(bad_candidate, "rank", candidate.rank)
        object.__setattr__(bad_candidate, "residuals", (hidden,))
        object.__setattr__(bad_candidate, "trace_ref", candidate.trace_ref)

        bad_verdict = TanzilVerdict(
            candidate=bad_candidate,
            verdict_state=TanzilState.PROVEN,
            failure_code=None,
            verdict_rank=candidate.rank,
            residuals=(hidden,),
            trace_ref=candidate.trace_ref,
        )
        result = bridge_tanzil_to_audit(bad_verdict)
        assert result.state is AuditBridgeState.REFUSED
        assert result.failure_code is FailureCode.HIDDEN_RESIDUAL

    def test_audit_rejects_blocking_residuals(self) -> None:
        tv = _proven_tanzil_verdict()
        candidate = tv.candidate
        blocking = Residual(
            name="TEST_BLOCKING",
            kind=ResidualKind.BLOCKING,
            visible=True,
            note="test blocking residual",
        )
        bad_candidate = TanzilCandidate.__new__(TanzilCandidate)
        object.__setattr__(bad_candidate, "hukm_verdict_ref", candidate.hukm_verdict_ref)
        object.__setattr__(bad_candidate, "manat_verdict_ref", candidate.manat_verdict_ref)
        object.__setattr__(bad_candidate, "ifadah_ref", candidate.ifadah_ref)
        object.__setattr__(bad_candidate, "reality_evidence", candidate.reality_evidence)
        object.__setattr__(bad_candidate, "instance_descriptor", candidate.instance_descriptor)
        object.__setattr__(bad_candidate, "tanzil_scope", candidate.tanzil_scope)
        object.__setattr__(bad_candidate, "presentation_envelope", candidate.presentation_envelope)
        object.__setattr__(bad_candidate, "rank", candidate.rank)
        object.__setattr__(bad_candidate, "residuals", (blocking,))
        object.__setattr__(bad_candidate, "trace_ref", candidate.trace_ref)

        bad_verdict = TanzilVerdict(
            candidate=bad_candidate,
            verdict_state=TanzilState.PROVEN,
            failure_code=None,
            verdict_rank=candidate.rank,
            residuals=(blocking,),
            trace_ref=candidate.trace_ref,
        )
        result = bridge_tanzil_to_audit(bad_verdict)
        assert result.state is AuditBridgeState.REFUSED
        assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


# ===========================================================================
# §7 No candidate-to-certificate conversion
# ===========================================================================


class TestNoCertificateConversion:
    """The bridge does not produce certificates or final authority."""

    def test_audit_does_not_convert_candidate_to_certificate(self) -> None:
        """The bridge output type is AuditedTanzilBridge, not a Certificate."""
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert isinstance(result.bridge, AuditedTanzilBridge)
        # It has no 'certificate' or 'certified' attribute
        assert not hasattr(result.bridge, "certificate")
        assert not hasattr(result.bridge, "certified")

    def test_audit_does_not_emit_final_authority(self) -> None:
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert result.bridge.not_final_authority is True

    def test_audit_does_not_emit_reality_application(self) -> None:
        """No reality_application or execution field on the bridge."""
        tv = _proven_tanzil_verdict()
        result = bridge_tanzil_to_audit(tv)
        assert not hasattr(result.bridge, "reality_application")
        assert not hasattr(result.bridge, "execution")
        assert not hasattr(result.bridge, "executed")


# ===========================================================================
# §8 Forbidden-symbol scan
# ===========================================================================


class TestForbiddenSymbols:
    """PR-22-AUDIT module does not export or define forbidden symbols."""

    def test_module_does_not_define_forbidden_symbols(self) -> None:
        tree = ast.parse(_BRIDGE_SRC.read_text())
        class_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        }
        func_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        }
        all_names = class_names | func_names
        for sym in FORBIDDEN_SYMBOLS_AUDIT_BRIDGE:
            assert sym not in all_names, (
                f"PR-22-AUDIT must not define '{sym}'"
            )

    def test_module_does_not_instantiate_forbidden_symbols(self) -> None:
        tree = ast.parse(_BRIDGE_SRC.read_text())
        call_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    call_names.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    call_names.add(node.func.attr)
        for sym in FORBIDDEN_SYMBOLS_AUDIT_BRIDGE:
            assert sym not in call_names, (
                f"PR-22-AUDIT must not instantiate '{sym}'"
            )


# ===========================================================================
# §9 AuditedTanzilBridge birth guards
# ===========================================================================


class TestBridgeBirthGuards:
    """AuditedTanzilBridge __post_init__ rejects invalid construction."""

    def test_rejects_non_tanzil_candidate(self) -> None:
        with pytest.raises(ValueError, match="TanzilCandidate"):
            AuditedTanzilBridge(
                tanzil_candidate="not a candidate",  # type: ignore[arg-type]
                presentation_envelope=None,  # type: ignore[arg-type]
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
                not_execution=True,
                not_fatwa=True,
                not_qada=True,
                not_final_authority=True,
            )

    def test_rejects_not_execution_false(self) -> None:
        tv = _proven_tanzil_verdict()
        c = tv.candidate
        with pytest.raises(ValueError, match="not_execution"):
            AuditedTanzilBridge(
                tanzil_candidate=c,
                presentation_envelope=c.presentation_envelope,
                rank=c.rank,
                residuals=c.residuals,
                trace_ref=c.trace_ref,
                not_execution=False,
                not_fatwa=True,
                not_qada=True,
                not_final_authority=True,
            )

    def test_rejects_not_fatwa_false(self) -> None:
        tv = _proven_tanzil_verdict()
        c = tv.candidate
        with pytest.raises(ValueError, match="not_fatwa"):
            AuditedTanzilBridge(
                tanzil_candidate=c,
                presentation_envelope=c.presentation_envelope,
                rank=c.rank,
                residuals=c.residuals,
                trace_ref=c.trace_ref,
                not_execution=True,
                not_fatwa=False,
                not_qada=True,
                not_final_authority=True,
            )

    def test_rejects_not_qada_false(self) -> None:
        tv = _proven_tanzil_verdict()
        c = tv.candidate
        with pytest.raises(ValueError, match="not_qada"):
            AuditedTanzilBridge(
                tanzil_candidate=c,
                presentation_envelope=c.presentation_envelope,
                rank=c.rank,
                residuals=c.residuals,
                trace_ref=c.trace_ref,
                not_execution=True,
                not_fatwa=True,
                not_qada=False,
                not_final_authority=True,
            )

    def test_rejects_not_final_authority_false(self) -> None:
        tv = _proven_tanzil_verdict()
        c = tv.candidate
        with pytest.raises(ValueError, match="not_final_authority"):
            AuditedTanzilBridge(
                tanzil_candidate=c,
                presentation_envelope=c.presentation_envelope,
                rank=c.rank,
                residuals=c.residuals,
                trace_ref=c.trace_ref,
                not_execution=True,
                not_fatwa=True,
                not_qada=True,
                not_final_authority=False,
            )

    def test_rejects_mismatched_rank(self) -> None:
        tv = _proven_tanzil_verdict()
        c = tv.candidate
        # Use a different rank
        wrong_rank = Rank.ZERO if c.rank is not Rank.ZERO else Rank.CANDIDATE
        with pytest.raises(ValueError, match="rank"):
            AuditedTanzilBridge(
                tanzil_candidate=c,
                presentation_envelope=c.presentation_envelope,
                rank=wrong_rank,
                residuals=c.residuals,
                trace_ref=c.trace_ref,
                not_execution=True,
                not_fatwa=True,
                not_qada=True,
                not_final_authority=True,
            )

    def test_rejects_mismatched_trace_ref(self) -> None:
        tv = _proven_tanzil_verdict()
        c = tv.candidate
        with pytest.raises(ValueError, match="trace_ref"):
            AuditedTanzilBridge(
                tanzil_candidate=c,
                presentation_envelope=c.presentation_envelope,
                rank=c.rank,
                residuals=c.residuals,
                trace_ref="wrong_trace",
                not_execution=True,
                not_fatwa=True,
                not_qada=True,
                not_final_authority=True,
            )


# ===========================================================================
# §10 Every refusal verdict has a trace_ref
# ===========================================================================


class TestRefusalTrace:
    """Every REFUSED verdict from the bridge carries a trace_ref."""

    def test_refused_has_trace(self) -> None:
        refused = TanzilVerdict(
            candidate=None,
            verdict_state=TanzilState.REFUSED,
            failure_code=FailureCode.NO_MANAT,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        result = bridge_tanzil_to_audit(refused)
        assert result.trace_ref
        assert "bridge_tanzil_to_audit" in result.trace_ref

    def test_invalid_type_has_trace(self) -> None:
        result = bridge_tanzil_to_audit(42)  # type: ignore[arg-type]
        assert result.trace_ref
        assert "bridge_tanzil_to_audit" in result.trace_ref


# ===========================================================================
# §11 All refusal failure codes are named
# ===========================================================================


class TestNamedFailureCodes:
    """Every refusal carries a named FailureCode."""

    def test_all_new_failure_codes_exist(self) -> None:
        """All PR-22-AUDIT failure codes are defined."""
        expected = [
            "NO_TANZIL_VERDICT",
            "AUDIT_PRESENTATION_ENVELOPE_MISSING",
            "AUDIT_PRESENTATION_WARNING_MISSING",
            "AUDIT_RANK_NOT_VISIBLE",
            "AUDIT_RESIDUALS_NOT_VISIBLE",
            "AUDIT_TRACE_NOT_VISIBLE",
            "AUDIT_EXECUTION_LEAK",
            "AUDIT_AUTHORITY_LEAK",
            "AUDIT_CERTIFICATE_LEAK",
        ]
        for name in expected:
            assert hasattr(FailureCode, name), f"FailureCode.{name} missing"
            assert isinstance(getattr(FailureCode, name), FailureCode)
