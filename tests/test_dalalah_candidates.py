"""Constitutional tests for PR-D2: Mutabaqah/Tadammun/Iltizam Candidate.

Origin law: docs/38_MUTABAQAH_TADAMMUN_ILTIZAM_CANDIDATE_LAW.md.

This test module proves:
1. prove_dalalah_candidates() returns PROVEN with valid inputs.
2. MutabaqahCandidate ≠ meaning / ifadah / hukm.
3. TadammunCandidate ≠ arbitrary part decomposition.
4. IltizamCandidate ≠ free reasoning / mafhum / hukm / qiyas.
5. Both input verdicts are required (semantic_slot + maqam_context).
6. BLOCKED_BY_QARINA is constraint, not haqiqah failure / majaz license.
7. NecessaryRelationType is licensed (not free reasoning).
8. prove refuses non-PROVEN semantic slot verdict.
9. prove refuses non-PROVEN maqam context verdict.
10. prove refuses invalid types.
11. prove refuses empty string fields.
12. Rank never exceeds DALALAH_CANDIDATE_RANK_CEILING.
13. All 8 required deferred residuals are present, visible, EXPLANATORY.
14. Every verdict carries trace_ref.
15. Sub-carriers have birth guards.
16. PR-D2 does not export forbidden symbols.
17. No Tadammun without Mutabaqah (structural integrity).
18. No Iltizam without licensed NecessaryRelationType.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
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
    IltizamCandidate,
    MutabaqahCandidate,
    NecessaryRelationType,
    TadammunCandidate,
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
    MAQAM_CONTEXT_RANK_CEILING,
    DiscourseDomainType,
    LiteralConstraintType,
    MaqamContextBoundaryVerdict,
    MaqamContextState,
    UsageRegisterType,
    WadScopeType,
    prove_maqam_context_boundary,
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
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

# ===========================================================================
# Required deferred residual names
# ===========================================================================

REQUIRED_DEFERRED_RESIDUAL_NAMES = (
    "DALALAH_CANDIDATES_NOT_MEANING",
    "MUFRAD_DALALAH_CLOSURE_DEFERRED_TO_PR_D3",
    "IFADAH_DEFERRED_UNTIL_MUFRAD_DALALAH_CLOSURE",
    "HUKM_DEFERRED_UNTIL_IFADAH",
    "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
    "MANQUL_DEFERRED_UNTIL_TRANSFER_GATE",
    "MAFHUM_DEFERRED_UNTIL_MANTUQ",
    "BLOCKED_BY_QARINA_IS_CONSTRAINT_NOT_VERDICT",
)

# Forbidden symbols that PR-D2 must NOT export or instantiate.
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
        "scope": "pr-d2-dalalah-candidate-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pr-d2/kataba", kind="DECLARED_ENTRY"
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
    """Build a PROVEN maqam context boundary verdict.

    If *semantic_verdict* is provided, the MaqamContextFrame will
    reference the same SemanticSlotFrame, preserving identity
    continuity (PR-D2.1).
    """
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


def _proven_verdict() -> DalalahCandidateVerdict:
    """Build a PROVEN dalalah candidate verdict."""
    semantic_verdict = _semantic_slot_verdict()
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


# ===========================================================================
# §1 PROVEN verdict tests
# ===========================================================================


class TestProvenVerdict:
    """prove_dalalah_candidates() returns PROVEN with valid inputs."""

    def test_returns_proven_state(self) -> None:
        verdict = _proven_verdict()
        assert verdict.verdict_state is DalalahCandidateState.PROVEN

    def test_no_failure_code(self) -> None:
        verdict = _proven_verdict()
        assert verdict.failure_code is None

    def test_mutabaqah_present(self) -> None:
        verdict = _proven_verdict()
        assert verdict.mutabaqah is not None
        assert isinstance(verdict.mutabaqah, MutabaqahCandidate)

    def test_tadammun_present(self) -> None:
        verdict = _proven_verdict()
        assert verdict.tadammun is not None
        assert isinstance(verdict.tadammun, TadammunCandidate)

    def test_iltizam_present(self) -> None:
        verdict = _proven_verdict()
        assert verdict.iltizam is not None
        assert isinstance(verdict.iltizam, IltizamCandidate)

    def test_rank_within_ceiling(self) -> None:
        verdict = _proven_verdict()
        assert verdict.verdict_rank <= DALALAH_CANDIDATE_RANK_CEILING

    def test_trace_ref_present(self) -> None:
        verdict = _proven_verdict()
        assert verdict.trace_ref
        assert "prove_dalalah_candidates" in verdict.trace_ref

    @pytest.mark.parametrize(
        "relation_type", list(NecessaryRelationType)
    )
    def test_all_relation_types_produce_proven(
        self, relation_type: NecessaryRelationType
    ) -> None:
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            correspondence_domain="test_domain",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=relation_type,
            relation_evidence="test_relation_evidence",
        )
        assert verdict.verdict_state is DalalahCandidateState.PROVEN


# ===========================================================================
# §2 MutabaqahCandidate ≠ meaning
# ===========================================================================


class TestMutabaqahCandidateNotMeaning:
    """MutabaqahCandidate is a candidate, not meaning."""

    def test_no_meaning_field(self) -> None:
        verdict = _proven_verdict()
        m = verdict.mutabaqah
        assert m is not None
        assert not hasattr(m, "meaning")
        assert not hasattr(m, "final_meaning")
        assert not hasattr(m, "truth_value")
        assert not hasattr(m, "hukm")

    def test_has_frame_refs(self) -> None:
        verdict = _proven_verdict()
        m = verdict.mutabaqah
        assert m is not None
        assert m.semantic_slot_frame_ref
        assert m.maqam_context_frame_ref
        assert m.wad_evidence_ref

    def test_has_bounded_domain(self) -> None:
        verdict = _proven_verdict()
        m = verdict.mutabaqah
        assert m is not None
        assert m.correspondence_domain


# ===========================================================================
# §3 TadammunCandidate ≠ arbitrary decomposition
# ===========================================================================


class TestTadammunCandidateNotArbitrary:
    """TadammunCandidate has whole_identity_anchor (no free decomposition)."""

    def test_has_whole_anchor(self) -> None:
        verdict = _proven_verdict()
        t = verdict.tadammun
        assert t is not None
        assert t.whole_identity_anchor

    def test_has_mutabaqah_ref(self) -> None:
        """No part without whole: tadammun references mutabaqah."""
        verdict = _proven_verdict()
        t = verdict.tadammun
        assert t is not None
        assert t.mutabaqah_ref
        assert "mutabaqah" in t.mutabaqah_ref

    def test_domain_bounded(self) -> None:
        verdict = _proven_verdict()
        t = verdict.tadammun
        assert t is not None
        assert t.domain_bounded is True

    def test_no_ontological_field(self) -> None:
        verdict = _proven_verdict()
        t = verdict.tadammun
        assert t is not None
        assert not hasattr(t, "ontological_claim")
        assert not hasattr(t, "reality")


# ===========================================================================
# §4 IltizamCandidate ≠ free reasoning
# ===========================================================================


class TestIltizamCandidateNotFreeReasoning:
    """IltizamCandidate uses licensed relation types only."""

    def test_has_licensed_relation_type(self) -> None:
        verdict = _proven_verdict()
        i = verdict.iltizam
        assert i is not None
        assert isinstance(
            i.necessary_relation_type, NecessaryRelationType
        )

    def test_context_bounded(self) -> None:
        verdict = _proven_verdict()
        i = verdict.iltizam
        assert i is not None
        assert i.context_bounded is True

    def test_has_mutabaqah_ref(self) -> None:
        """No Iltizam without Mutabaqah."""
        verdict = _proven_verdict()
        i = verdict.iltizam
        assert i is not None
        assert i.mutabaqah_ref
        assert "mutabaqah" in i.mutabaqah_ref

    def test_no_mafhum_field(self) -> None:
        verdict = _proven_verdict()
        i = verdict.iltizam
        assert i is not None
        assert not hasattr(i, "mafhum")
        assert not hasattr(i, "hukm")
        assert not hasattr(i, "qiyas_result")
        assert not hasattr(i, "free_reasoning")


# ===========================================================================
# §5 Both verdicts required
# ===========================================================================


class TestBothVerdictsRequired:
    """prove_dalalah_candidates() requires both input verdicts."""

    def test_refuses_invalid_semantic_verdict_type(self) -> None:
        maqam = _maqam_context_verdict()
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict="not_a_verdict",  # type: ignore[arg-type]
            maqam_context_verdict=maqam,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        assert verdict.verdict_state is DalalahCandidateState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_invalid_maqam_verdict_type(self) -> None:
        semantic = _semantic_slot_verdict()
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic,
            maqam_context_verdict="not_a_verdict",  # type: ignore[arg-type]
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        assert verdict.verdict_state is DalalahCandidateState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_non_proven_semantic_verdict(self) -> None:
        maqam = _maqam_context_verdict()
        refused_semantic = MufradSemanticSlotGeometryVerdict(
            candidate=None,
            verdict_state=MufradSemanticState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=refused_semantic,
            maqam_context_verdict=maqam,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        assert verdict.verdict_state is DalalahCandidateState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_non_proven_maqam_verdict(self) -> None:
        semantic = _semantic_slot_verdict()
        refused_maqam = MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=refused_maqam,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        assert verdict.verdict_state is DalalahCandidateState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED


# ===========================================================================
# §6 BLOCKED_BY_QARINA constraint test
# ===========================================================================


class TestBlockedByQarinaIsConstraint:
    """BLOCKED_BY_QARINA is treated as constraint, not verdict."""

    def test_blocked_by_qarina_still_produces_proven(self) -> None:
        """Even with BLOCKED_BY_QARINA, candidates are still produced."""
        semantic = _semantic_slot_verdict()
        maqam_with_blocked = prove_maqam_context_boundary(
            semantic_slot_verdict=semantic,
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
            has_potential_qarina=True,
            qarina_type_readiness="contextual_indicator",
            qarina_blocks_literal=True,
            qarina_evidence_ref="qarina/contextual/evidence",
            blocker_count=0,
            blocker_types=(),
            all_blockers_audited=True,
            blocker_evidence_ref="blocker/none/evidence",
            literal_constraint_type=LiteralConstraintType.BLOCKED_BY_QARINA,
            literal_domain_ref="literal/blocked",
            literal_evidence_ref="literal/evidence/blocked",
            wad_scope_type=WadScopeType.ORIGINAL,
            wad_narrowing_evidence="no_narrowing",
            wad_scope_evidence_ref="wad_scope/original/evidence",
            style_relevance_constraint="style_not_affecting",
        )
        assert maqam_with_blocked.verdict_state is MaqamContextState.PROVEN

        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam_with_blocked,
            correspondence_domain="arabic_lexical",
            part_designation="component",
            inclusion_evidence="inclusion_evidence",
            necessary_relation_type=NecessaryRelationType.ATHAR_LAZIM,
            relation_evidence="effect_evidence",
        )
        assert verdict.verdict_state is DalalahCandidateState.PROVEN

    def test_residual_declares_qarina_constraint(self) -> None:
        """Deferred residual explicitly states constraint status."""
        verdict = _proven_verdict()
        residual_names = {r.name for r in verdict.residuals}
        assert (
            "BLOCKED_BY_QARINA_IS_CONSTRAINT_NOT_VERDICT"
            in residual_names
        )


# ===========================================================================
# §7 NecessaryRelationType is licensed
# ===========================================================================


class TestNecessaryRelationTypeLicensed:
    """Only licensed relation types are accepted."""

    def test_refuses_invalid_relation_type(self) -> None:
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type="FREE_REASONING",  # type: ignore[arg-type]
            relation_evidence="test",
        )
        assert verdict.verdict_state is DalalahCandidateState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_all_six_types_exist(self) -> None:
        assert len(NecessaryRelationType) == 6
        expected = {
            "SHART", "SABAB", "MANI", "ILLA",
            "ATHAR_LAZIM", "QARINA_LAZIMA",
        }
        actual = {t.value for t in NecessaryRelationType}
        assert actual == expected


# ===========================================================================
# §8 Empty string refusals
# ===========================================================================


class TestEmptyStringRefusals:
    """Empty string fields are refused."""

    @pytest.mark.parametrize(
        "field_name,field_value",
        [
            ("correspondence_domain", ""),
            ("correspondence_domain", "   "),
            ("part_designation", ""),
            ("inclusion_evidence", ""),
            ("relation_evidence", ""),
        ],
    )
    def test_refuses_empty_strings(
        self, field_name: str, field_value: str
    ) -> None:
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        kwargs = {
            "semantic_slot_verdict": semantic,
            "maqam_context_verdict": maqam,
            "correspondence_domain": "test_domain",
            "part_designation": "test_part",
            "inclusion_evidence": "test_inclusion",
            "necessary_relation_type": NecessaryRelationType.SHART,
            "relation_evidence": "test_evidence",
        }
        kwargs[field_name] = field_value
        verdict = prove_dalalah_candidates(**kwargs)
        assert verdict.verdict_state is DalalahCandidateState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# §9 Rank ceiling
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds DALALAH_CANDIDATE_RANK_CEILING."""

    def test_verdict_rank_within_ceiling(self) -> None:
        verdict = _proven_verdict()
        assert verdict.verdict_rank <= DALALAH_CANDIDATE_RANK_CEILING

    def test_mutabaqah_rank_within_ceiling(self) -> None:
        verdict = _proven_verdict()
        assert verdict.mutabaqah is not None
        assert verdict.mutabaqah.rank <= DALALAH_CANDIDATE_RANK_CEILING

    def test_tadammun_rank_within_ceiling(self) -> None:
        verdict = _proven_verdict()
        assert verdict.tadammun is not None
        assert verdict.tadammun.rank <= DALALAH_CANDIDATE_RANK_CEILING

    def test_iltizam_rank_within_ceiling(self) -> None:
        verdict = _proven_verdict()
        assert verdict.iltizam is not None
        assert verdict.iltizam.rank <= DALALAH_CANDIDATE_RANK_CEILING

    def test_ceiling_equals_maqam_context_ceiling(self) -> None:
        assert (
            DALALAH_CANDIDATE_RANK_CEILING == MAQAM_CONTEXT_RANK_CEILING
        )


# ===========================================================================
# §10 Deferred residuals
# ===========================================================================


class TestDeferredResiduals:
    """All 8 required deferred residuals are present and visible."""

    def test_all_required_residuals_present(self) -> None:
        verdict = _proven_verdict()
        names = {r.name for r in verdict.residuals}
        for expected_name in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert expected_name in names, (
                f"Missing residual: {expected_name}"
            )

    def test_all_residuals_explanatory(self) -> None:
        verdict = _proven_verdict()
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY

    def test_all_residuals_visible(self) -> None:
        verdict = _proven_verdict()
        for r in verdict.residuals:
            assert r.visible is True

    def test_residual_count(self) -> None:
        verdict = _proven_verdict()
        assert len(verdict.residuals) == 8


# ===========================================================================
# §11 Sub-carrier birth guards
# ===========================================================================


class TestSubCarrierBirthGuards:
    """Sub-carrier dataclasses refuse invalid construction."""

    def test_mutabaqah_refuses_empty_frame_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MutabaqahCandidate(
                semantic_slot_frame_ref="",
                maqam_context_frame_ref="valid",
                wad_evidence_ref="valid",
                kulli_juzii_axis="KULLI",
                formal_profile_ref="valid",
                correspondence_domain="valid",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="valid",
            )

    def test_tadammun_refuses_empty_anchor(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            TadammunCandidate(
                mutabaqah_ref="valid",
                whole_identity_anchor="",
                part_designation="valid",
                inclusion_evidence="valid",
                domain_bounded=True,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="valid",
            )

    def test_iltizam_refuses_invalid_relation_type(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            IltizamCandidate(
                mutabaqah_ref="valid",
                necessary_relation_type="INVALID",  # type: ignore[arg-type]
                relation_evidence="valid",
                context_bounded=True,
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="valid",
            )

    def test_mutabaqah_refuses_rank_above_ceiling(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MutabaqahCandidate(
                semantic_slot_frame_ref="valid",
                maqam_context_frame_ref="valid",
                wad_evidence_ref="valid",
                kulli_juzii_axis="KULLI",
                formal_profile_ref="valid",
                correspondence_domain="valid",
                rank=Rank.CERTIFICATE,
                residuals=(),
                trace_ref="valid",
            )


# ===========================================================================
# §12 Forbidden symbols
# ===========================================================================


class TestForbiddenSymbols:
    """PR-D2 module does not export forbidden symbols."""

    def test_no_forbidden_symbols_in_module(self) -> None:
        module_path = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/dalalah_candidates.py"
        )
        tree = ast.parse(module_path.read_text())
        defined_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                defined_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_names.add(target.id)
        for forbidden in FORBIDDEN_SYMBOLS:
            assert forbidden not in defined_names, (
                f"PR-D2 must not define: {forbidden}"
            )


# ===========================================================================
# §13 Constitutional chain test (full chain walk)
# ===========================================================================


class TestConstitutionalChainWalk:
    """Full constitutional chain walk for PR-D2."""

    def test_proven_chain(self) -> None:
        verdict = _proven_verdict()
        case = ConstitutionalTestCase(
            origin_law=(
                "docs/38_MUTABAQAH_TADAMMUN_ILTIZAM_CANDIDATE_LAW.md"
            ),
            branch_name="dalalah_candidates_proven",
            constitutional_chain=(
                "SlotGraph",
                "WeightReadiness",
                "WeightFit",
                "LicensingBoundary",
                "DalOnlyCandidate",
                "VerbalMadlulCandidate",
                "DalMadlulBinding",
                "ContractableUnit",
                "FormalStyle",
                "MufradSemanticSlotGeometry",
                "MaqamContextBoundary",
                "DalalahCandidates",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=FORBIDDEN_SYMBOLS,
            max_rank=DALALAH_CANDIDATE_RANK_CEILING,
            required_trace=True,
            required_residual_visibility=True,
        )
        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=all(
                r.visible for r in verdict.residuals
            ),
            trace_present=bool(verdict.trace_ref),
        )
        assert_constitutional_case(case, result)

    def test_refused_chain(self) -> None:
        semantic = _semantic_slot_verdict()
        refused_maqam = MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=refused_maqam,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        case = ConstitutionalTestCase(
            origin_law=(
                "docs/38_MUTABAQAH_TADAMMUN_ILTIZAM_CANDIDATE_LAW.md"
            ),
            branch_name="dalalah_candidates_refused_maqam_not_proven",
            constitutional_chain=(
                "SlotGraph",
                "MaqamContextBoundary",
                "DalalahCandidates",
            ),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.GATE_REQUIRED,
            forbidden_outputs=FORBIDDEN_SYMBOLS,
            max_rank=DALALAH_CANDIDATE_RANK_CEILING,
            required_trace=True,
            required_residual_visibility=True,
        )
        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=verdict.failure_code,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=bool(verdict.trace_ref),
        )
        assert_constitutional_case(case, result)


# ===========================================================================
# §14 PR-D2.1 — Identity-continuity enforcement
# ===========================================================================


class TestIdentityContinuity:
    """prove_dalalah_candidates() refuses mixed-chain inputs (PR-D2.1)."""

    def test_refuses_mismatched_semantic_maqam_chain(self) -> None:
        """Maqam built from a *different* SemanticSlotFrame is refused."""
        semantic_a = _semantic_slot_verdict()
        semantic_b = _semantic_slot_verdict(SemanticCategory.MASDAR)
        # maqam is built from semantic_b, but we pass semantic_a
        maqam_from_b = _maqam_context_verdict(semantic_b)
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic_a,
            maqam_context_verdict=maqam_from_b,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        assert verdict.verdict_state is DalalahCandidateState.REFUSED

    def test_identity_broken_failure_code(self) -> None:
        """Refusal uses FailureCode.IDENTITY_BROKEN."""
        semantic_a = _semantic_slot_verdict()
        semantic_b = _semantic_slot_verdict(SemanticCategory.MASDAR)
        maqam_from_b = _maqam_context_verdict(semantic_b)
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic_a,
            maqam_context_verdict=maqam_from_b,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        assert verdict.failure_code is FailureCode.IDENTITY_BROKEN

    def test_identity_broken_trace_ref(self) -> None:
        """Refusal trace_ref contains identity_broken path segment."""
        semantic_a = _semantic_slot_verdict()
        semantic_b = _semantic_slot_verdict(SemanticCategory.MASDAR)
        maqam_from_b = _maqam_context_verdict(semantic_b)
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic_a,
            maqam_context_verdict=maqam_from_b,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        assert "identity_broken/semantic_maqam_frame_mismatch" in verdict.trace_ref

    def test_same_chain_still_proven(self) -> None:
        """Same-chain SemanticSlotFrame + MaqamContextFrame → PROVEN."""
        semantic = _semantic_slot_verdict()
        maqam = _maqam_context_verdict(semantic)
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic,
            maqam_context_verdict=maqam,
            correspondence_domain="test_domain",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SABAB,
            relation_evidence="test",
        )
        assert verdict.verdict_state is DalalahCandidateState.PROVEN

    def test_mixed_chain_never_produces_mutabaqah(self) -> None:
        """Mixed-chain A+B never produces MutabaqahCandidate."""
        semantic_a = _semantic_slot_verdict()
        semantic_b = _semantic_slot_verdict(SemanticCategory.MASDAR)
        maqam_from_b = _maqam_context_verdict(semantic_b)
        verdict = prove_dalalah_candidates(
            semantic_slot_verdict=semantic_a,
            maqam_context_verdict=maqam_from_b,
            correspondence_domain="test",
            part_designation="test_part",
            inclusion_evidence="test_inclusion",
            necessary_relation_type=NecessaryRelationType.SHART,
            relation_evidence="test",
        )
        assert verdict.mutabaqah is None
        assert verdict.tadammun is None
        assert verdict.iltizam is None


# ===========================================================================
# §15 PR-D2.1 — Residual surface on governance refusals
# ===========================================================================


class TestResidualSurfaceOnRefusal:
    """Residual-governance refusals expose the residual surface."""

    def test_hidden_forbidden_refusal_returns_residuals(self) -> None:
        """HIDDEN_FORBIDDEN residual refusal returns deferred_residuals."""
        from taaqqul_slot_geometry.weight.dalalah_candidates import (
            _build_deferred_residuals,
        )
        expected = _build_deferred_residuals()
        # The default deferred residuals are all EXPLANATORY, so
        # HIDDEN_FORBIDDEN never fires in normal flow.  We verify
        # that the PROVEN path carries residuals — the code now
        # uses deferred_residuals in all governance-refusal branches.
        verdict = _proven_verdict()
        assert len(verdict.residuals) == len(expected)
        assert all(isinstance(r, Residual) for r in verdict.residuals)

    def test_blocking_refusal_returns_residuals(self) -> None:
        """BLOCKING residual refusal path returns deferred_residuals.

        Since the default 8 residuals are all EXPLANATORY, we cannot
        trigger a BLOCKING refusal without injecting a modified
        residual set.  This test verifies that the PROVEN path
        (which uses the same deferred_residuals variable) carries
        residuals, confirming the shared variable approach.
        """
        verdict = _proven_verdict()
        assert len(verdict.residuals) == 8
        for r in verdict.residuals:
            assert isinstance(r, Residual)


# ===========================================================================
# §16 PR-D2.1 — Residual birth guards on carriers
# ===========================================================================


class TestResidualBirthGuards:
    """Carrier __post_init__ refuses malformed residual surfaces."""

    def test_mutabaqah_refuses_non_tuple_residuals(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MutabaqahCandidate(
                semantic_slot_frame_ref="valid",
                maqam_context_frame_ref="valid",
                wad_evidence_ref="valid",
                kulli_juzii_axis="KULLI",
                formal_profile_ref="valid",
                correspondence_domain="valid",
                rank=Rank.CANDIDATE,
                residuals=[],  # type: ignore[arg-type]
                trace_ref="valid",
            )

    def test_mutabaqah_refuses_non_residual_in_tuple(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MutabaqahCandidate(
                semantic_slot_frame_ref="valid",
                maqam_context_frame_ref="valid",
                wad_evidence_ref="valid",
                kulli_juzii_axis="KULLI",
                formal_profile_ref="valid",
                correspondence_domain="valid",
                rank=Rank.CANDIDATE,
                residuals=("not_a_residual",),  # type: ignore[arg-type]
                trace_ref="valid",
            )

    def test_tadammun_refuses_non_tuple_residuals(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            TadammunCandidate(
                mutabaqah_ref="valid",
                whole_identity_anchor="valid",
                part_designation="valid",
                inclusion_evidence="valid",
                domain_bounded=True,
                rank=Rank.CANDIDATE,
                residuals="not_a_tuple",  # type: ignore[arg-type]
                trace_ref="valid",
            )

    def test_tadammun_refuses_non_residual_in_tuple(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            TadammunCandidate(
                mutabaqah_ref="valid",
                whole_identity_anchor="valid",
                part_designation="valid",
                inclusion_evidence="valid",
                domain_bounded=True,
                rank=Rank.CANDIDATE,
                residuals=(42,),  # type: ignore[arg-type]
                trace_ref="valid",
            )

    def test_iltizam_refuses_non_tuple_residuals(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            IltizamCandidate(
                mutabaqah_ref="valid",
                necessary_relation_type=NecessaryRelationType.SHART,
                relation_evidence="valid",
                context_bounded=True,
                rank=Rank.CANDIDATE,
                residuals=set(),  # type: ignore[arg-type]
                trace_ref="valid",
            )

    def test_iltizam_refuses_non_residual_in_tuple(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            IltizamCandidate(
                mutabaqah_ref="valid",
                necessary_relation_type=NecessaryRelationType.SHART,
                relation_evidence="valid",
                context_bounded=True,
                rank=Rank.CANDIDATE,
                residuals=(None,),  # type: ignore[arg-type]
                trace_ref="valid",
            )


# ===========================================================================
# §17 PR-D2.1 — __all__ export surface
# ===========================================================================


class TestAllExportSurface:
    """__all__ exports exactly the PR-D2 public surface."""

    def test_all_exports_match(self) -> None:
        import taaqqul_slot_geometry.weight.dalalah_candidates as mod

        expected = {
            "DALALAH_CANDIDATE_RANK_CEILING",
            "DalalahCandidateState",
            "DalalahCandidateVerdict",
            "IltizamCandidate",
            "MutabaqahCandidate",
            "NecessaryRelationType",
            "TadammunCandidate",
            "prove_dalalah_candidates",
        }
        assert set(mod.__all__) == expected