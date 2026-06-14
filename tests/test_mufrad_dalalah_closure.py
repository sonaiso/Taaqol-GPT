"""Constitutional tests for PR-D3: Mufrad Dalalah Closure.

Origin law: docs/39_MUFRAD_DALALAH_CLOSURE_LAW.md.

This test module proves:
1. prove_mufrad_dalalah_closure() returns PROVEN with valid inputs.
2. MufradDalalahClosureCandidate ≠ meaning / ifadah / hukm.
3. All identity continuity links are enforced.
4. All three dalalah candidates required.
5. Closure_scope required.
6. Residual governance (HIDDEN_FORBIDDEN / BLOCKING → REFUSED).
7. Rank never exceeds MUFRAD_DALALAH_CLOSURE_RANK_CEILING.
8. All 7 required deferred residuals present, visible, EXPLANATORY.
9. Every verdict carries trace_ref.
10. Sub-carrier has birth guards.
11. PR-D3 does not export forbidden symbols.
12. Refuses invalid types / non-PROVEN verdicts.
13. Structural integrity: tadammun/iltizam → mutabaqah.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
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
from taaqqul_slot_geometry.weight.dalalah_candidates import (
    DALALAH_CANDIDATE_RANK_CEILING,
    DalalahCandidateState,
    DalalahCandidateVerdict,
    NecessaryRelationType,
    prove_dalalah_candidates,
)
from taaqqul_slot_geometry.weight.formal_shape import FormalShapeClosureState
from taaqqul_slot_geometry.weight.formal_style_candidate import (
    FormalStyleCandidate,
    FormalStyleFamily,
    FormalStyleState,
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
    MUFRAD_DALALAH_CLOSURE_RANK_CEILING,
    MufradDalalahClosureCandidate,
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
from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState

# ===========================================================================
# Required deferred residual names
# ===========================================================================

REQUIRED_DEFERRED_RESIDUAL_NAMES = (
    "MUFRAD_DALALAH_CLOSURE_NOT_MEANING",
    "HAQIQAH_ATTEMPT_DEFERRED_TO_POST_CLOSURE",
    "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
    "MANQUL_DEFERRED_UNTIL_TRANSFER_GATE",
    "IFADAH_DEFERRED_UNTIL_RELATION_CLOSURE",
    "HUKM_DEFERRED_UNTIL_IFADAH",
    "MAFHUM_DEFERRED_UNTIL_MANTUQ",
)

# Forbidden symbols that PR-D3 must NOT export or instantiate.
FORBIDDEN_SYMBOLS = (
    "Meaning",
    "FinalMeaning",
    "IfadahCandidate",
    "HukmCandidate",
    "TanzilCandidate",
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
        "scope": "pr-d3-mufrad-dalalah-closure-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pr-d3/kataba", kind="DECLARED_ENTRY"
        ),
    }


def _syllable() -> SyllableCandidate:
    return SyllableCandidate(
        **_base("syllable", "syll-ka", "ka"), units=(("k", "a"),)
    )


def _syllables() -> tuple[SyllableCandidate, ...]:
    return (
        _syllable(),
        SyllableCandidate(
            **_base("syllable", "syll-ta", "ta"), units=(("t", "a"),)
        ),
        SyllableCandidate(
            **_base("syllable", "syll-ba", "ba"), units=(("b", "a"),)
        ),
    )


def _sequence() -> SyllableSequenceCandidate:
    return SyllableSequenceCandidate(
        **_base("syllable_sequence", "seq-kataba", "ka-ta-ba"),
        syllables=_syllables(),
    )


def _boundary() -> WordBoundaryCandidate:
    return WordBoundaryCandidate(
        **_base("word_boundary", "wb-kataba", "kataba"),
        sequence=_sequence(),
    )


def _word_carrier() -> WordCarrierCandidate:
    return WordCarrierCandidate(
        **_base("word_carrier", "wc-kataba", "kataba"),
        bounded_surface=_boundary(),
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
    result = prove_dal(
        verdict, "kataba", "phonetic://kataba", "graphic://kataba"
    )
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
    result = bind_dal_madlul(
        dal, madlul, _dal_registry_proof(), _madlul_registry_proof()
    )
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


def _semantic_slot_verdict(
    semantic_category: SemanticCategory = SemanticCategory.JAMID,
) -> MufradSemanticSlotGeometryVerdict:
    """Build a PROVEN semantic slot geometry verdict."""
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
    assert verdict.verdict_state is MufradSemanticState.PROVEN
    assert verdict.candidate is not None
    return verdict


def _maqam_context_verdict(
    semantic_verdict: MufradSemanticSlotGeometryVerdict | None = None,
) -> MaqamContextBoundaryVerdict:
    """Build a PROVEN maqam context boundary verdict."""
    if semantic_verdict is None:
        semantic_verdict = _semantic_slot_verdict()
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
    semantic_verdict: MufradSemanticSlotGeometryVerdict | None = None,
    maqam_verdict: MaqamContextBoundaryVerdict | None = None,
) -> DalalahCandidateVerdict:
    """Build a PROVEN dalalah candidate verdict."""
    if semantic_verdict is None:
        semantic_verdict = _semantic_slot_verdict()
    if maqam_verdict is None:
        maqam_verdict = _maqam_context_verdict(semantic_verdict)
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


def _proven_closure_verdict() -> MufradDalalahClosureVerdict:
    """Build a PROVEN mufrad dalalah closure verdict."""
    semantic_verdict = _semantic_slot_verdict()
    maqam_verdict = _maqam_context_verdict(semantic_verdict)
    dalalah_verdict = _dalalah_candidate_verdict(
        semantic_verdict, maqam_verdict
    )
    return prove_mufrad_dalalah_closure(
        semantic_slot_verdict=semantic_verdict,
        maqam_context_verdict=maqam_verdict,
        dalalah_candidate_verdict=dalalah_verdict,
        closure_scope="mufrad_dalalah_minimum_complete",
    )


# ===========================================================================
# §1 PROVEN verdict tests
# ===========================================================================


class TestProvenVerdict:
    """prove_mufrad_dalalah_closure() returns PROVEN with valid inputs."""

    def test_returns_proven_state(self) -> None:
        verdict = _proven_closure_verdict()
        assert verdict.verdict_state is MufradDalalahClosureState.PROVEN

    def test_no_failure_code(self) -> None:
        verdict = _proven_closure_verdict()
        assert verdict.failure_code is None

    def test_candidate_present(self) -> None:
        verdict = _proven_closure_verdict()
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate, MufradDalalahClosureCandidate)

    def test_rank_within_ceiling(self) -> None:
        verdict = _proven_closure_verdict()
        assert verdict.verdict_rank <= MUFRAD_DALALAH_CLOSURE_RANK_CEILING

    def test_trace_ref_present(self) -> None:
        verdict = _proven_closure_verdict()
        assert verdict.trace_ref
        assert "prove_mufrad_dalalah_closure" in verdict.trace_ref

    def test_candidate_has_all_required_refs(self) -> None:
        verdict = _proven_closure_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.semantic_slot_frame_ref
        assert c.maqam_context_frame_ref
        assert c.mutabaqah_ref
        assert c.tadammun_ref
        assert c.iltizam_ref
        assert c.dal_identity_ref
        assert c.closure_scope == "mufrad_dalalah_minimum_complete"


# ===========================================================================
# §2 MufradDalalahClosureCandidate ≠ meaning
# ===========================================================================


class TestClosureCandidateNotMeaning:
    """MufradDalalahClosureCandidate is closure, not meaning."""

    def test_no_meaning_field(self) -> None:
        verdict = _proven_closure_verdict()
        c = verdict.candidate
        assert c is not None
        assert not hasattr(c, "meaning")
        assert not hasattr(c, "final_meaning")
        assert not hasattr(c, "truth_value")
        assert not hasattr(c, "hukm")
        assert not hasattr(c, "ifadah")
        assert not hasattr(c, "tanzil")
        assert not hasattr(c, "mafhum")
        assert not hasattr(c, "majaz")
        assert not hasattr(c, "manqul")

    def test_is_closure_not_verdict_on_truth(self) -> None:
        verdict = _proven_closure_verdict()
        c = verdict.candidate
        assert c is not None
        assert not hasattr(c, "haqiqah")
        assert not hasattr(c, "speaker_intent")
        assert not hasattr(c, "ontological_claim")


# ===========================================================================
# §3 Identity continuity enforcement
# ===========================================================================


class TestIdentityContinuity:
    """Identity links must be consistent across all layers."""

    def test_refuses_maqam_semantic_frame_mismatch(self) -> None:
        """maqam_frame.semantic_slot_frame_ref != slot_frame.trace_ref."""
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        dalalah = _dalalah_candidate_verdict(semantic, maqam)
        # Use a different semantic category to get a different trace_ref
        semantic_alt = _semantic_slot_verdict(SemanticCategory.MUSHTAQ)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic_alt,
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict=dalalah,
            closure_scope="test",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.IDENTITY_BROKEN

    def test_refuses_mutabaqah_semantic_frame_mismatch(self) -> None:
        """mutabaqah.semantic_slot_frame_ref != slot_frame.trace_ref."""
        # Build dalalah from one semantic, then close with a different one
        semantic_orig = _semantic_slot_verdict()
        maqam_orig = _maqam_context_verdict(semantic_orig)
        dalalah = _dalalah_candidate_verdict(semantic_orig, maqam_orig)
        # Use a different semantic category to get a different trace_ref
        semantic_alt = _semantic_slot_verdict(SemanticCategory.MUSHTAQ)
        maqam_alt = _maqam_context_verdict(semantic_alt)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic_alt,
            maqam_context_verdict=maqam_alt,
            dalalah_candidate_verdict=dalalah,
            closure_scope="test",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.IDENTITY_BROKEN

    def test_proven_preserves_identity(self) -> None:
        """All refs in candidate point to the same chain."""
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        dalalah = _dalalah_candidate_verdict(semantic, maqam)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict=dalalah,
            closure_scope="test_scope",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.PROVEN
        c = verdict.candidate
        assert c is not None
        assert c.semantic_slot_frame_ref == semantic.candidate.trace_ref
        assert c.maqam_context_frame_ref == maqam.candidate.trace_ref
        assert c.mutabaqah_ref == dalalah.mutabaqah.trace_ref
        assert c.tadammun_ref == dalalah.tadammun.trace_ref
        assert c.iltizam_ref == dalalah.iltizam.trace_ref
        assert c.dal_identity_ref == semantic.candidate.dal_identity_ref


# ===========================================================================
# §4 All three dalalah candidates required
# ===========================================================================


class TestAllThreeCandidatesRequired:
    """prove_mufrad_dalalah_closure() requires all three candidates."""

    def test_refuses_invalid_dalalah_verdict_type(self) -> None:
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict="not_a_verdict",  # type: ignore[arg-type]
            closure_scope="test",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_non_proven_dalalah_verdict(self) -> None:
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        refused = DalalahCandidateVerdict(
            mutabaqah=None,
            tadammun=None,
            iltizam=None,
            verdict_state=DalalahCandidateState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict=refused,
            closure_scope="test",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED


# ===========================================================================
# §5 closure_scope required
# ===========================================================================


class TestClosureScopeRequired:
    """closure_scope must be a non-empty string."""

    @pytest.mark.parametrize("bad_scope", ["", "   ", None, 123])
    def test_refuses_empty_or_invalid_scope(self, bad_scope: object) -> None:
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        dalalah = _dalalah_candidate_verdict(semantic, maqam)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict=dalalah,
            closure_scope=bad_scope,  # type: ignore[arg-type]
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# §6 Residual governance
# ===========================================================================


class TestResidualSurfaceOnRefusal:
    """Hidden/blocking residuals cause REFUSED."""

    def test_hidden_residual_causes_refusal(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """HIDDEN_FORBIDDEN residual → REFUSED with HIDDEN_RESIDUAL."""
        import taaqqul_slot_geometry.weight.mufrad_dalalah_closure as mod

        hidden = Residual(
            name="INJECTED_HIDDEN",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=False,
            note="injected for test",
        )
        monkeypatch.setattr(mod, "_build_deferred_residuals", lambda: (hidden,))

        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        dalalah = _dalalah_candidate_verdict(semantic, maqam)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict=dalalah,
            closure_scope="test_scope",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL
        assert verdict.residuals == (hidden,)

    def test_blocking_residual_causes_refusal(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """BLOCKING residual → REFUSED with BLOCKING_RESIDUAL_PRESENT."""
        import taaqqul_slot_geometry.weight.mufrad_dalalah_closure as mod

        blocking = Residual(
            name="INJECTED_BLOCKING",
            kind=ResidualKind.BLOCKING,
            visible=True,
            note="injected for test",
        )
        monkeypatch.setattr(mod, "_build_deferred_residuals", lambda: (blocking,))

        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        dalalah = _dalalah_candidate_verdict(semantic, maqam)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict=dalalah,
            closure_scope="test_scope",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
        assert verdict.residuals == (blocking,)


# ===========================================================================
# §7 Rank ceiling
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds MUFRAD_DALALAH_CLOSURE_RANK_CEILING."""

    def test_ceiling_inherits_from_dalalah_candidate(self) -> None:
        assert (
            MUFRAD_DALALAH_CLOSURE_RANK_CEILING
            == DALALAH_CANDIDATE_RANK_CEILING
        )

    def test_proven_verdict_rank_within_ceiling(self) -> None:
        verdict = _proven_closure_verdict()
        assert verdict.verdict_rank <= MUFRAD_DALALAH_CLOSURE_RANK_CEILING

    def test_candidate_rank_within_ceiling(self) -> None:
        verdict = _proven_closure_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.rank <= MUFRAD_DALALAH_CLOSURE_RANK_CEILING

    def test_carrier_rejects_rank_above_ceiling(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MufradDalalahClosureCandidate(
                semantic_slot_frame_ref="test",
                maqam_context_frame_ref="test",
                mutabaqah_ref="test",
                tadammun_ref="test",
                iltizam_ref="test",
                dal_identity_ref="test",
                closure_scope="test",
                rank=Rank.CERTIFICATE,  # exceeds ceiling
                residuals=(),
                trace_ref="test",
            )


# ===========================================================================
# §8 Deferred residuals
# ===========================================================================


class TestDeferredResiduals:
    """All 7 required deferred residuals present, visible, EXPLANATORY."""

    def test_all_required_names_present(self) -> None:
        verdict = _proven_closure_verdict()
        residual_names = {r.name for r in verdict.residuals}
        for name in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert name in residual_names, f"Missing residual: {name}"

    def test_all_visible(self) -> None:
        verdict = _proven_closure_verdict()
        for r in verdict.residuals:
            assert r.visible is True, f"Residual {r.name} not visible"

    def test_all_explanatory(self) -> None:
        verdict = _proven_closure_verdict()
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY, (
                f"Residual {r.name} not EXPLANATORY"
            )

    def test_all_have_notes(self) -> None:
        verdict = _proven_closure_verdict()
        for r in verdict.residuals:
            assert r.note, f"Residual {r.name} has empty note"

    def test_exactly_seven_residuals(self) -> None:
        verdict = _proven_closure_verdict()
        assert len(verdict.residuals) == 7


# ===========================================================================
# §9 Trace reference
# ===========================================================================


class TestTraceRef:
    """Every verdict carries trace_ref."""

    def test_proven_has_trace(self) -> None:
        verdict = _proven_closure_verdict()
        assert verdict.trace_ref
        assert "proven" in verdict.trace_ref

    def test_refused_has_trace(self) -> None:
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict="bad",  # type: ignore[arg-type]
            maqam_context_verdict="bad",  # type: ignore[arg-type]
            dalalah_candidate_verdict="bad",  # type: ignore[arg-type]
            closure_scope="test",
        )
        assert verdict.trace_ref
        assert "refused" in verdict.trace_ref

    def test_candidate_trace_ref(self) -> None:
        verdict = _proven_closure_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.trace_ref
        assert "proven" in c.trace_ref


# ===========================================================================
# §10 Birth guards
# ===========================================================================


class TestBirthGuards:
    """MufradDalalahClosureCandidate has birth validation."""

    @pytest.mark.parametrize(
        "field",
        [
            "semantic_slot_frame_ref",
            "maqam_context_frame_ref",
            "mutabaqah_ref",
            "tadammun_ref",
            "iltizam_ref",
            "dal_identity_ref",
            "closure_scope",
        ],
    )
    def test_empty_string_field_rejected(self, field: str) -> None:
        kwargs = {
            "semantic_slot_frame_ref": "test_ref",
            "maqam_context_frame_ref": "test_ref",
            "mutabaqah_ref": "test_ref",
            "tadammun_ref": "test_ref",
            "iltizam_ref": "test_ref",
            "dal_identity_ref": "test_ref",
            "closure_scope": "test_scope",
            "rank": Rank.CANDIDATE,
            "residuals": (),
            "trace_ref": "test_trace",
        }
        kwargs[field] = ""
        with pytest.raises(WeightCarrierSchemaError):
            MufradDalalahClosureCandidate(**kwargs)  # type: ignore[arg-type]

    def test_empty_trace_ref_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MufradDalalahClosureCandidate(
                semantic_slot_frame_ref="test",
                maqam_context_frame_ref="test",
                mutabaqah_ref="test",
                tadammun_ref="test",
                iltizam_ref="test",
                dal_identity_ref="test",
                closure_scope="test",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )

    def test_invalid_rank_type_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MufradDalalahClosureCandidate(
                semantic_slot_frame_ref="test",
                maqam_context_frame_ref="test",
                mutabaqah_ref="test",
                tadammun_ref="test",
                iltizam_ref="test",
                dal_identity_ref="test",
                closure_scope="test",
                rank="not_a_rank",  # type: ignore[arg-type]
                residuals=(),
                trace_ref="test",
            )


# ===========================================================================
# §11 Forbidden symbols
# ===========================================================================


class TestForbiddenSymbols:
    """PR-D3 must NOT export or instantiate forbidden symbols."""

    def test_module_does_not_export_forbidden(self) -> None:
        import taaqqul_slot_geometry.weight.mufrad_dalalah_closure as mod

        exported = set(mod.__all__)
        for sym in FORBIDDEN_SYMBOLS:
            assert sym not in exported, f"Forbidden symbol exported: {sym}"

    def test_source_does_not_define_forbidden(self) -> None:
        src = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/mufrad_dalalah_closure.py"
        )
        tree = ast.parse(src.read_text())
        defined_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                defined_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_names.add(target.id)
        for sym in FORBIDDEN_SYMBOLS:
            assert sym not in defined_names, (
                f"Forbidden symbol defined: {sym}"
            )


# ===========================================================================
# §12 Input verdict type validation
# ===========================================================================


class TestInputValidation:
    """Refuses invalid types / non-PROVEN verdicts."""

    def test_refuses_invalid_semantic_verdict_type(self) -> None:
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        dalalah = _dalalah_candidate_verdict(semantic, maqam)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict="not_valid",  # type: ignore[arg-type]
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict=dalalah,
            closure_scope="test",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_non_proven_semantic_verdict(self) -> None:
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        dalalah = _dalalah_candidate_verdict(semantic, maqam)
        refused_semantic = MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=refused_semantic,
            maqam_context_verdict=maqam,
            dalalah_candidate_verdict=dalalah,
            closure_scope="test",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_invalid_maqam_verdict_type(self) -> None:
        semantic = _semantic_slot_verdict()
        dalalah = _dalalah_candidate_verdict(semantic)
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic,
            maqam_context_verdict="not_valid",  # type: ignore[arg-type]
            dalalah_candidate_verdict=dalalah,
            closure_scope="test",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_non_proven_maqam_verdict(self) -> None:
        semantic = _semantic_slot_verdict()
        dalalah = _dalalah_candidate_verdict(semantic)
        refused_maqam = MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        verdict = prove_mufrad_dalalah_closure(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=refused_maqam,
            dalalah_candidate_verdict=dalalah,
            closure_scope="test",
        )
        assert verdict.verdict_state is MufradDalalahClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED


# ===========================================================================
# §13 Structural integrity
# ===========================================================================


class TestStructuralIntegrity:
    """tadammun/iltizam → mutabaqah integrity preserved."""

    def test_proven_tadammun_refs_mutabaqah(self) -> None:
        verdict = _proven_closure_verdict()
        c = verdict.candidate
        assert c is not None
        # The closure candidate's refs are consistent with dalalah chain
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        dalalah = _dalalah_candidate_verdict(semantic, maqam)
        # Verify from known good verdict
        assert dalalah.tadammun.mutabaqah_ref == dalalah.mutabaqah.trace_ref
        assert dalalah.iltizam.mutabaqah_ref == dalalah.mutabaqah.trace_ref
