"""Constitutional tests for PR-20: IfādahCandidate.

Origin law: docs/41_IFADAH_BOUNDARY_LAW.md, docs/42_SPEECH_FORCE_FORMAL_STYLE_BRIDGE_LAW.md.

This test module proves:
1. prove_ifadah_candidate() returns PROVEN with valid inputs.
2. IfadahCandidate ≠ meaning / hukm / manat / tanzil / proposition / speaker-intent.
3. Three PROVEN input verdicts required (RelationClosure, FormalStyle, Maqam).
4. SpeechForceKind required (KHABAR or INSHA only).
5. Bridge compatibility (docs/42 §6): DECLARATIVE_STYLE_FORM ↔ KHABAR; inshāʾ families ↔ INSHA.
6. Maqam divergence: single shared maqam verdict.
7. ifadah_evidence and closure_scope required.
8. Identity continuity: first != second dal identity.
9. Residual governance (HIDDEN_FORBIDDEN / BLOCKING → REFUSED).
10. Rank never exceeds IFADAH_RANK_CEILING.
11. All 9 required deferred residuals present, visible, EXPLANATORY.
12. Every verdict carries trace_ref.
13. Sub-carrier has birth guards.
14. PR-20 does not export forbidden symbols.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    IFADAH_RANK_CEILING,
    BindingState,
    BoundaryEvidence,
    ContractableUnitGeometry,
    ContractableUnitState,
    DalBoundaryState,
    DalMadlulBindingCandidate,
    DalOnlyCandidate,
    IfadahCandidate,
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
    RELATION_CLOSURE_RANK_CEILING,
    RelationClosureState,
    RelationClosureVerdict,
    RelationType,
    prove_relation_closure,
)
from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState

# ===========================================================================
# Required deferred residual names (docs/41 §10, docs/42 §9)
# ===========================================================================

REQUIRED_DEFERRED_RESIDUAL_NAMES = (
    "IFADAH_NOT_PROPOSITION",
    "HUKM_DEFERRED_UNTIL_HUKM_DOMAIN_LAW",
    "MANAT_DEFERRED_UNTIL_MANAT_LAW",
    "TANZIL_DEFERRED_UNTIL_PRESENTATION_LAW",
    "MAFHUM_MANTUQ_DEFERRED_POST_VERTICAL",
    "MAJAZ_HAQIQAH_DEFERRED_POST_VERTICAL",
    "EXTRA_SPEECH_FORCE_DEFERRED",
    "SPEAKER_INTENT_DEFERRED",
    "AUDIT_INTEGRATION_DEFERRED_UNTIL_PR_22_AUDIT",
)

# Forbidden symbols that PR-20 must NOT export or instantiate.
FORBIDDEN_SYMBOLS = (
    "Meaning",
    "FinalMeaning",
    "HukmCandidate",
    "TanzilCandidate",
    "ManatCandidate",
    "MantuqClosure",
    "MafhumCandidate",
    "MajazVerdict",
    "MajazLicense",
    "ManqulVerdict",
    "ManqulLicense",
    "SpeakerIntentVerdict",
    "HaqiqahAttemptVerdict",
    "OntologicalClaim",
    "FreeReasoning",
    "QiyasResult",
    "PropositionTruthValue",
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
        "scope": "pr-20-ifadah-candidate-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pr-20/kataba", kind="DECLARED_ENTRY"
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
    # The maqam trace_ref must match rc_candidate.relation_maqam
    semantic = _semantic_slot_verdict("kataba")
    maqam_verdict = _maqam_context_verdict(semantic)
    # Build relation closure with maqam_verdict.trace_ref as relation_maqam
    # so the maqam divergence check passes.
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
    return verdict


# ===========================================================================
# §1 PROVEN verdict tests
# ===========================================================================


class TestProvenVerdict:
    """prove_ifadah_candidate() returns PROVEN with valid inputs."""

    def test_returns_proven_state(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.verdict_state is IfadahState.PROVEN

    def test_no_failure_code(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.failure_code is None

    def test_candidate_present(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate, IfadahCandidate)

    def test_rank_within_ceiling(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.verdict_rank <= IFADAH_RANK_CEILING

    def test_trace_ref_present(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.trace_ref
        assert "prove_ifadah_candidate" in verdict.trace_ref

    def test_candidate_has_all_required_fields(self) -> None:
        verdict = _proven_ifadah_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.relation_closure_ref
        assert c.formal_style_ref
        assert c.maqam_verdict_ref
        assert isinstance(c.speech_force, SpeechForceKind)
        assert c.first_dal_identity_ref
        assert c.second_dal_identity_ref
        assert c.ifadah_evidence
        assert c.closure_scope
        assert c.bridge_compatible is True
        assert isinstance(c.rank, Rank)
        assert isinstance(c.residuals, tuple)
        assert c.trace_ref

    def test_candidate_identity_distinct(self) -> None:
        verdict = _proven_ifadah_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.first_dal_identity_ref != c.second_dal_identity_ref

    def test_candidate_bridge_compatible(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.candidate is not None
        assert verdict.candidate.bridge_compatible is True

    def test_khabar_with_declarative(self) -> None:
        verdict = _proven_ifadah_verdict(
            speech_force=SpeechForceKind.KHABAR,
            style_family=FormalStyleFamily.DECLARATIVE_STYLE_FORM,
        )
        assert verdict.verdict_state is IfadahState.PROVEN

    def test_insha_with_command(self) -> None:
        verdict = _proven_ifadah_verdict(
            speech_force=SpeechForceKind.INSHA,
            style_family=FormalStyleFamily.COMMAND_STYLE_FORM,
        )
        assert verdict.verdict_state is IfadahState.PROVEN

    def test_insha_with_interrogative(self) -> None:
        verdict = _proven_ifadah_verdict(
            speech_force=SpeechForceKind.INSHA,
            style_family=FormalStyleFamily.INTERROGATIVE_STYLE_FORM,
        )
        assert verdict.verdict_state is IfadahState.PROVEN

    def test_insha_with_vocative(self) -> None:
        verdict = _proven_ifadah_verdict(
            speech_force=SpeechForceKind.INSHA,
            style_family=FormalStyleFamily.VOCATIVE_STYLE_FORM,
        )
        assert verdict.verdict_state is IfadahState.PROVEN


# ===========================================================================
# §2 Input verdict refusal tests
# ===========================================================================


class TestInputVerdictRefusal:
    """All three input verdicts must be valid and PROVEN."""

    def test_refuses_invalid_relation_closure_type(self) -> None:
        fs_verdict = _formal_style_verdict()
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_ifadah_candidate(
            relation_closure_verdict="not_a_verdict",  # type: ignore[arg-type]
            formal_style_verdict=fs_verdict,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_RELATION_CLOSURE

    def test_refuses_relation_closure_not_proven(self) -> None:
        # Build a REFUSED relation closure verdict
        first = _proven_mufrad_closure("kataba")
        rc_verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=first,  # same identity → REFUSED
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="test_maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert rc_verdict.verdict_state is RelationClosureState.REFUSED

        fs_verdict = _formal_style_verdict()
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_verdict,
            formal_style_verdict=fs_verdict,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_RELATION_CLOSURE

    def test_refuses_invalid_formal_style_type(self) -> None:
        rc_verdict = _proven_relation_closure_verdict()
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_verdict,
            formal_style_verdict="not_a_verdict",  # type: ignore[arg-type]
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_FORMAL_STYLE

    def test_refuses_formal_style_not_proven(self) -> None:
        # Build a REFUSED formal style verdict
        fs_verdict = prove_formal_style_candidate(
            style_family=FormalStyleFamily.DECLARATIVE_STYLE_FORM,
            composition_evidence_ref="",  # empty → REFUSED
            formal_closure_state=FormalShapeClosureState.CLOSED,
            formal_closure_ref="test/closure",
        )
        assert fs_verdict.verdict_state is FormalStyleState.REFUSED

        rc_verdict = _proven_relation_closure_verdict()
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_verdict,
            formal_style_verdict=fs_verdict,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_FORMAL_STYLE

    def test_refuses_invalid_speech_force_type(self) -> None:
        rc_verdict = _proven_relation_closure_verdict()
        fs_verdict = _formal_style_verdict()
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_verdict,
            formal_style_verdict=fs_verdict,
            ifadah_maqam_verdict=maqam,
            speech_force="KHABAR",  # type: ignore[arg-type]
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_SPEECH_FORCE

    def test_refuses_invalid_maqam_type(self) -> None:
        rc_verdict = _proven_relation_closure_verdict()
        fs_verdict = _formal_style_verdict()
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_verdict,
            formal_style_verdict=fs_verdict,
            ifadah_maqam_verdict="not_a_verdict",  # type: ignore[arg-type]
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH_MAQAM

    def test_refuses_maqam_not_proven(self) -> None:
        rc_verdict = _proven_relation_closure_verdict()
        fs_verdict = _formal_style_verdict()
        # Build a REFUSED maqam verdict
        semantic = _semantic_slot_verdict()
        maqam_verdict = prove_maqam_context_boundary(
            semantic_slot_verdict=semantic,
            discourse_domain_type=DiscourseDomainType.LUGHAWI,
            discourse_evidence_ref="",  # empty → REFUSED
            usage_register_type=UsageRegisterType.HAQIQI,
            usage_evidence_ref="usage/haqiqi/evidence",
            technical_domain_name="general_arabic",
            is_technical=False,
            technical_evidence_ref="technical/general/evidence",
            speaker_position="narrator",
            addressee_position="reader",
            textual_context_window="test",
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
        assert maqam_verdict.verdict_state is MaqamContextState.REFUSED

        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_verdict,
            formal_style_verdict=fs_verdict,
            ifadah_maqam_verdict=maqam_verdict,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH_MAQAM


# ===========================================================================
# §3 Evidence and scope refusal tests
# ===========================================================================


class TestEvidenceAndScopeRefusal:
    """ifadah_evidence and closure_scope must be non-empty strings."""

    def test_refuses_empty_ifadah_evidence(self) -> None:
        fs = _formal_style_verdict()
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        # Match maqam trace to relation_maqam
        rc_matched = prove_relation_closure(
            first_verdict=_proven_mufrad_closure("kataba"),
            second_verdict=_proven_mufrad_closure("darasa"),
            relation_type=RelationType.PREDICATIVE,
            relation_maqam=maqam.trace_ref,
            relation_evidence="evidence",
            closure_scope="scope",
        )
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_matched,
            formal_style_verdict=fs,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH_EVIDENCE

    def test_refuses_empty_closure_scope(self) -> None:
        fs = _formal_style_verdict()
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        rc_matched = prove_relation_closure(
            first_verdict=_proven_mufrad_closure("kataba"),
            second_verdict=_proven_mufrad_closure("darasa"),
            relation_type=RelationType.PREDICATIVE,
            relation_maqam=maqam.trace_ref,
            relation_evidence="evidence",
            closure_scope="scope",
        )
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_matched,
            formal_style_verdict=fs,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH_SCOPE


# ===========================================================================
# §4 Maqam divergence tests (docs/41 §6)
# ===========================================================================


class TestMaqamDivergence:
    """Single shared maqam required: rc.relation_maqam == maqam.trace_ref."""

    def test_refuses_maqam_divergence(self) -> None:
        # Build relation closure with one maqam, maqam verdict with different trace
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        # relation_maqam != maqam.trace_ref
        rc_divergent = prove_relation_closure(
            first_verdict=_proven_mufrad_closure("kataba"),
            second_verdict=_proven_mufrad_closure("darasa"),
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="DIFFERENT_MAQAM_ORIGIN",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert rc_divergent.verdict_state is RelationClosureState.PROVEN
        fs = _formal_style_verdict()
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc_divergent,
            formal_style_verdict=fs,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.MAQAM_DIVERGENCE
        assert "maqam_divergence" in verdict.trace_ref


# ===========================================================================
# §5 Bridge compatibility tests (docs/42 §6)
# ===========================================================================


class TestBridgeCompatibility:
    """Bridge: DECLARATIVE ↔ KHABAR; inshāʾ families ↔ INSHA."""

    def test_refuses_khabar_with_command(self) -> None:
        """KHABAR is only compatible with DECLARATIVE_STYLE_FORM."""
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        rc = prove_relation_closure(
            first_verdict=_proven_mufrad_closure("kataba"),
            second_verdict=_proven_mufrad_closure("darasa"),
            relation_type=RelationType.PREDICATIVE,
            relation_maqam=maqam.trace_ref,
            relation_evidence="evidence",
            closure_scope="scope",
        )
        fs = _formal_style_verdict(FormalStyleFamily.COMMAND_STYLE_FORM)
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc,
            formal_style_verdict=fs,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.FORMAL_STYLE_CONFLICT

    def test_refuses_insha_with_declarative(self) -> None:
        """INSHA is NOT compatible with DECLARATIVE_STYLE_FORM."""
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        rc = prove_relation_closure(
            first_verdict=_proven_mufrad_closure("kataba"),
            second_verdict=_proven_mufrad_closure("darasa"),
            relation_type=RelationType.PREDICATIVE,
            relation_maqam=maqam.trace_ref,
            relation_evidence="evidence",
            closure_scope="scope",
        )
        fs = _formal_style_verdict(FormalStyleFamily.DECLARATIVE_STYLE_FORM)
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc,
            formal_style_verdict=fs,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.INSHA,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.FORMAL_STYLE_CONFLICT

    def test_refuses_khabar_with_wish(self) -> None:
        """KHABAR is NOT compatible with WISH_STYLE_FORM."""
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        rc = prove_relation_closure(
            first_verdict=_proven_mufrad_closure("kataba"),
            second_verdict=_proven_mufrad_closure("darasa"),
            relation_type=RelationType.PREDICATIVE,
            relation_maqam=maqam.trace_ref,
            relation_evidence="evidence",
            closure_scope="scope",
        )
        fs = _formal_style_verdict(FormalStyleFamily.WISH_STYLE_FORM)
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc,
            formal_style_verdict=fs,
            ifadah_maqam_verdict=maqam,
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.failure_code is FailureCode.FORMAL_STYLE_CONFLICT


# ===========================================================================
# §6 Deferred residuals (docs/41 §10, docs/42 §9)
# ===========================================================================


class TestDeferredResiduals:
    """All 9 deferred residuals present, visible, EXPLANATORY."""

    def test_exactly_nine_residuals(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert len(verdict.residuals) == 9

    def test_all_residuals_explanatory(self) -> None:
        verdict = _proven_ifadah_verdict()
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY

    def test_all_residuals_visible(self) -> None:
        verdict = _proven_ifadah_verdict()
        for r in verdict.residuals:
            assert r.visible is True

    def test_all_required_names_present(self) -> None:
        verdict = _proven_ifadah_verdict()
        names = {r.name for r in verdict.residuals}
        for required_name in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert required_name in names, f"Missing: {required_name}"

    def test_candidate_carries_same_residuals(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.candidate is not None
        assert verdict.candidate.residuals == verdict.residuals


# ===========================================================================
# §7 Rank ceiling tests
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds IFADAH_RANK_CEILING."""

    def test_verdict_rank_within_ceiling(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.verdict_rank <= IFADAH_RANK_CEILING

    def test_candidate_rank_within_ceiling(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.candidate is not None
        assert verdict.candidate.rank <= IFADAH_RANK_CEILING

    def test_ceiling_equals_relation_closure_ceiling(self) -> None:
        assert IFADAH_RANK_CEILING == RELATION_CLOSURE_RANK_CEILING


# ===========================================================================
# §8 Trace presence tests
# ===========================================================================


class TestTracePresence:
    """Every verdict carries a non-empty trace_ref."""

    def test_proven_verdict_has_trace(self) -> None:
        verdict = _proven_ifadah_verdict()
        assert verdict.trace_ref
        assert "proven" in verdict.trace_ref

    def test_refused_verdict_has_trace(self) -> None:
        rc = _proven_relation_closure_verdict()
        fs = _formal_style_verdict()
        verdict = prove_ifadah_candidate(
            relation_closure_verdict=rc,
            formal_style_verdict=fs,
            ifadah_maqam_verdict="invalid",  # type: ignore[arg-type]
            speech_force=SpeechForceKind.KHABAR,
            ifadah_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is IfadahState.REFUSED
        assert verdict.trace_ref
        assert "refused" in verdict.trace_ref


# ===========================================================================
# §9 SpeechForceKind enum tests
# ===========================================================================


class TestSpeechForceKind:
    """SpeechForceKind has exactly KHABAR and INSHA."""

    def test_only_two_members(self) -> None:
        assert len(SpeechForceKind) == 2

    def test_khabar_is_member(self) -> None:
        assert SpeechForceKind.KHABAR.value == "KHABAR"

    def test_insha_is_member(self) -> None:
        assert SpeechForceKind.INSHA.value == "INSHA"


# ===========================================================================
# §10 IfadahCandidate birth guard tests
# ===========================================================================


class TestIfadahCandidateBirthGuards:
    """IfadahCandidate dataclass rejects invalid construction."""

    def test_rejects_empty_relation_closure_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            IfadahCandidate(
                relation_closure_ref="",
                formal_style_ref="fs_ref",
                maqam_verdict_ref="maqam_ref",
                speech_force=SpeechForceKind.KHABAR,
                first_dal_identity_ref="dal_1",
                second_dal_identity_ref="dal_2",
                ifadah_evidence="evidence",
                closure_scope="scope",
                bridge_compatible=True,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_empty_ifadah_evidence(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            IfadahCandidate(
                relation_closure_ref="rc_ref",
                formal_style_ref="fs_ref",
                maqam_verdict_ref="maqam_ref",
                speech_force=SpeechForceKind.KHABAR,
                first_dal_identity_ref="dal_1",
                second_dal_identity_ref="dal_2",
                ifadah_evidence="",
                closure_scope="scope",
                bridge_compatible=True,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_bridge_incompatible(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            IfadahCandidate(
                relation_closure_ref="rc_ref",
                formal_style_ref="fs_ref",
                maqam_verdict_ref="maqam_ref",
                speech_force=SpeechForceKind.KHABAR,
                first_dal_identity_ref="dal_1",
                second_dal_identity_ref="dal_2",
                ifadah_evidence="evidence",
                closure_scope="scope",
                bridge_compatible=False,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_rank_exceeds_ceiling(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            IfadahCandidate(
                relation_closure_ref="rc_ref",
                formal_style_ref="fs_ref",
                maqam_verdict_ref="maqam_ref",
                speech_force=SpeechForceKind.KHABAR,
                first_dal_identity_ref="dal_1",
                second_dal_identity_ref="dal_2",
                ifadah_evidence="evidence",
                closure_scope="scope",
                bridge_compatible=True,
                rank=Rank.CERTIFICATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_rejects_empty_trace_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            IfadahCandidate(
                relation_closure_ref="rc_ref",
                formal_style_ref="fs_ref",
                maqam_verdict_ref="maqam_ref",
                speech_force=SpeechForceKind.KHABAR,
                first_dal_identity_ref="dal_1",
                second_dal_identity_ref="dal_2",
                ifadah_evidence="evidence",
                closure_scope="scope",
                bridge_compatible=True,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# §11 Forbidden symbol test (docs/41 §3)
# ===========================================================================


class TestForbiddenSymbols:
    """PR-20 module does not export or instantiate forbidden symbols."""

    def test_no_forbidden_symbols_in_module(self) -> None:
        module_path = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/ifadah_candidate.py"
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
                f"Forbidden symbol '{forbidden}' found in ifadah_candidate.py"
            )

    def test_no_forbidden_in_all_exports(self) -> None:
        from taaqqul_slot_geometry.weight import ifadah_candidate

        for forbidden in FORBIDDEN_SYMBOLS:
            assert not hasattr(ifadah_candidate, forbidden), (
                f"Forbidden symbol '{forbidden}' exported from module"
            )


# ===========================================================================
# §12 IfadahState enum tests
# ===========================================================================


class TestIfadahState:
    """IfadahState has exactly PROVEN and REFUSED."""

    def test_only_two_members(self) -> None:
        assert len(IfadahState) == 2

    def test_proven_member(self) -> None:
        assert IfadahState.PROVEN.value == "PROVEN"

    def test_refused_member(self) -> None:
        assert IfadahState.REFUSED.value == "REFUSED"
