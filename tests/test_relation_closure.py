"""Constitutional tests for PR-D4: Relation Closure.

Origin law: docs/40_RELATION_CLOSURE_LAW.md.

This test module proves:
1. prove_relation_closure() returns PROVEN with valid inputs.
2. RelationClosureCandidate ≠ meaning / ifadah / hukm.
3. Both inputs must be PROVEN MufradDalalahClosureVerdicts.
4. RelationType required.
5. relation_maqam and relation_evidence required.
6. closure_scope required.
7. Identity distinctness: two different dal_identity_ref values.
8. Residual governance (HIDDEN_FORBIDDEN / BLOCKING → REFUSED).
9. Rank never exceeds RELATION_CLOSURE_RANK_CEILING.
10. All 5 required deferred residuals present, visible, EXPLANATORY.
11. Every verdict carries trace_ref.
12. Sub-carrier has birth guards.
13. PR-D4 does not export forbidden symbols.
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
    RelationClosureCandidate,
    RelationClosureState,
    RelationClosureVerdict,
    RelationType,
    prove_relation_closure,
)
from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState

# ===========================================================================
# Required deferred residual names
# ===========================================================================

REQUIRED_DEFERRED_RESIDUAL_NAMES = (
    "RELATION_CLOSURE_NOT_MEANING",
    "IFADAH_DEFERRED_UNTIL_SPEECH_FORCE",
    "HUKM_DEFERRED_UNTIL_IFADAH",
    "MAFHUM_DEFERRED_UNTIL_MANTUQ",
    "HAQIQAH_MAJAZ_DEFERRED_TO_POST_RELATION",
)

# Forbidden symbols that PR-D4 must NOT export or instantiate.
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
        "scope": "pr-d4-relation-closure-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pr-d4/kataba", kind="DECLARED_ENTRY"
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
    root: str = "kataba",
    semantic_category: SemanticCategory = SemanticCategory.JAMID,
) -> MufradSemanticSlotGeometryVerdict:
    """Build a PROVEN semantic slot geometry verdict."""
    dal = _dal_only_candidate(root)
    madlul = _madlul_candidate(dal, root)
    unit = _contractable_unit(dal, madlul, root)
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


def _proven_relation_closure_verdict() -> RelationClosureVerdict:
    """Build a PROVEN relation closure verdict with two distinct units."""
    first = _proven_mufrad_closure("kataba")
    second = _proven_mufrad_closure("darasa")
    return prove_relation_closure(
        first_verdict=first,
        second_verdict=second,
        relation_type=RelationType.PREDICATIVE,
        relation_maqam="general_arabic_discourse",
        relation_evidence="subject_predicate_evidence",
        closure_scope="relation_closure_minimal",
    )


# ===========================================================================
# §1 PROVEN verdict tests
# ===========================================================================


class TestProvenVerdict:
    """prove_relation_closure() returns PROVEN with valid inputs."""

    def test_returns_proven_state(self) -> None:
        verdict = _proven_relation_closure_verdict()
        assert verdict.verdict_state is RelationClosureState.PROVEN

    def test_no_failure_code(self) -> None:
        verdict = _proven_relation_closure_verdict()
        assert verdict.failure_code is None

    def test_candidate_present(self) -> None:
        verdict = _proven_relation_closure_verdict()
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate, RelationClosureCandidate)

    def test_rank_within_ceiling(self) -> None:
        verdict = _proven_relation_closure_verdict()
        assert verdict.verdict_rank <= RELATION_CLOSURE_RANK_CEILING

    def test_trace_ref_present(self) -> None:
        verdict = _proven_relation_closure_verdict()
        assert verdict.trace_ref
        assert "prove_relation_closure" in verdict.trace_ref

    def test_candidate_has_all_required_fields(self) -> None:
        verdict = _proven_relation_closure_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.first_closure_ref
        assert c.second_closure_ref
        assert c.first_dal_identity_ref
        assert c.second_dal_identity_ref
        assert c.relation_type is RelationType.PREDICATIVE
        assert c.relation_maqam == "general_arabic_discourse"
        assert c.relation_evidence == "subject_predicate_evidence"
        assert c.closure_scope == "relation_closure_minimal"

    def test_all_relation_types_accepted(self) -> None:
        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        for rt in RelationType:
            verdict = prove_relation_closure(
                first_verdict=first,
                second_verdict=second,
                relation_type=rt,
                relation_maqam="maqam_test",
                relation_evidence="evidence_test",
                closure_scope="scope_test",
            )
            assert verdict.verdict_state is RelationClosureState.PROVEN


# ===========================================================================
# §2 RelationClosureCandidate ≠ meaning
# ===========================================================================


class TestClosureCandidateNotMeaning:
    """RelationClosureCandidate is closure, not meaning."""

    def test_no_meaning_field(self) -> None:
        verdict = _proven_relation_closure_verdict()
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
        assert not hasattr(c, "haqiqah")
        assert not hasattr(c, "speaker_intent")
        assert not hasattr(c, "ontological_claim")


# ===========================================================================
# §3 Both inputs must be PROVEN MufradDalalahClosureVerdicts
# ===========================================================================


class TestBothInputsRequired:
    """Both verdicts must be PROVEN MufradDalalahClosureVerdicts."""

    def test_refuses_invalid_first_verdict_type(self) -> None:
        second = _proven_mufrad_closure("darasa")
        verdict = prove_relation_closure(
            first_verdict="not_a_verdict",  # type: ignore[arg-type]
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_non_proven_first_verdict(self) -> None:
        second = _proven_mufrad_closure("darasa")
        refused = MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        verdict = prove_relation_closure(
            first_verdict=refused,
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_invalid_second_verdict_type(self) -> None:
        first = _proven_mufrad_closure("kataba")
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict="not_a_verdict",  # type: ignore[arg-type]
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED

    def test_refuses_non_proven_second_verdict(self) -> None:
        first = _proven_mufrad_closure("kataba")
        refused = MufradDalalahClosureVerdict(
            candidate=None,
            verdict_state=MufradDalalahClosureState.REFUSED,
            failure_code=FailureCode.GATE_REQUIRED,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/refused",
        )
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=refused,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED


# ===========================================================================
# §4 RelationType required
# ===========================================================================


class TestRelationTypeRequired:
    """relation_type must be a valid RelationType."""

    def test_refuses_invalid_relation_type(self) -> None:
        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=second,
            relation_type="not_a_type",  # type: ignore[arg-type]
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    def test_refuses_none_relation_type(self) -> None:
        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=second,
            relation_type=None,  # type: ignore[arg-type]
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# §5 relation_maqam and relation_evidence required
# ===========================================================================


class TestMaqamAndEvidenceRequired:
    """relation_maqam and relation_evidence must be non-empty strings."""

    @pytest.mark.parametrize("bad_maqam", ["", "   ", None, 123])
    def test_refuses_empty_or_invalid_maqam(self, bad_maqam: object) -> None:
        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam=bad_maqam,  # type: ignore[arg-type]
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY

    @pytest.mark.parametrize("bad_evidence", ["", "   ", None, 123])
    def test_refuses_empty_or_invalid_evidence(
        self, bad_evidence: object
    ) -> None:
        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence=bad_evidence,  # type: ignore[arg-type]
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# §6 closure_scope required
# ===========================================================================


class TestClosureScopeRequired:
    """closure_scope must be a non-empty string."""

    @pytest.mark.parametrize("bad_scope", ["", "   ", None, 123])
    def test_refuses_empty_or_invalid_scope(self, bad_scope: object) -> None:
        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope=bad_scope,  # type: ignore[arg-type]
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


# ===========================================================================
# §7 Identity distinctness
# ===========================================================================


class TestIdentityDistinctness:
    """Two units must have distinct dal_identity_ref values."""

    def test_refuses_same_dal_identity(self) -> None:
        first = _proven_mufrad_closure("kataba")
        # Use the same verdict for both
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=first,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.IDENTITY_BROKEN

    def test_distinct_units_accepted(self) -> None:
        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        assert (
            first.candidate.dal_identity_ref
            != second.candidate.dal_identity_ref
        )
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.PROVEN


# ===========================================================================
# §8 Residual governance
# ===========================================================================


class TestResidualGovernance:
    """Hidden/blocking residuals cause REFUSED."""

    def test_hidden_residual_causes_refusal(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """HIDDEN_FORBIDDEN residual → REFUSED with HIDDEN_RESIDUAL."""
        import taaqqul_slot_geometry.weight.relation_closure as mod

        hidden = Residual(
            name="INJECTED_HIDDEN",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=False,
            note="injected for test",
        )
        monkeypatch.setattr(mod, "_build_deferred_residuals", lambda: (hidden,))

        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL
        assert verdict.residuals == (hidden,)

    def test_blocking_residual_causes_refusal(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """BLOCKING residual → REFUSED with BLOCKING_RESIDUAL_PRESENT."""
        import taaqqul_slot_geometry.weight.relation_closure as mod

        blocking = Residual(
            name="INJECTED_BLOCKING",
            kind=ResidualKind.BLOCKING,
            visible=True,
            note="injected for test",
        )
        monkeypatch.setattr(
            mod, "_build_deferred_residuals", lambda: (blocking,)
        )

        first = _proven_mufrad_closure("kataba")
        second = _proven_mufrad_closure("darasa")
        verdict = prove_relation_closure(
            first_verdict=first,
            second_verdict=second,
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.verdict_state is RelationClosureState.REFUSED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
        assert verdict.residuals == (blocking,)


# ===========================================================================
# §9 Rank ceiling
# ===========================================================================


class TestRankCeiling:
    """Rank never exceeds RELATION_CLOSURE_RANK_CEILING."""

    def test_ceiling_inherits_from_mufrad_dalalah_closure(self) -> None:
        assert (
            RELATION_CLOSURE_RANK_CEILING
            == MUFRAD_DALALAH_CLOSURE_RANK_CEILING
        )

    def test_proven_verdict_rank_within_ceiling(self) -> None:
        verdict = _proven_relation_closure_verdict()
        assert verdict.verdict_rank <= RELATION_CLOSURE_RANK_CEILING

    def test_candidate_rank_within_ceiling(self) -> None:
        verdict = _proven_relation_closure_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.rank <= RELATION_CLOSURE_RANK_CEILING

    def test_carrier_rejects_rank_above_ceiling(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            RelationClosureCandidate(
                first_closure_ref="test",
                second_closure_ref="test",
                first_dal_identity_ref="id1",
                second_dal_identity_ref="id2",
                relation_type=RelationType.PREDICATIVE,
                relation_maqam="maqam",
                relation_evidence="evidence",
                closure_scope="scope",
                rank=Rank.CERTIFICATE,  # exceeds ceiling
                residuals=(),
                trace_ref="test",
            )


# ===========================================================================
# §10 Deferred residuals
# ===========================================================================


class TestDeferredResiduals:
    """All 5 required deferred residuals present, visible, EXPLANATORY."""

    def test_all_required_names_present(self) -> None:
        verdict = _proven_relation_closure_verdict()
        residual_names = {r.name for r in verdict.residuals}
        for name in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert name in residual_names, f"Missing residual: {name}"

    def test_all_visible(self) -> None:
        verdict = _proven_relation_closure_verdict()
        for r in verdict.residuals:
            assert r.visible is True, f"Residual {r.name} not visible"

    def test_all_explanatory(self) -> None:
        verdict = _proven_relation_closure_verdict()
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY, (
                f"Residual {r.name} not EXPLANATORY"
            )

    def test_all_have_notes(self) -> None:
        verdict = _proven_relation_closure_verdict()
        for r in verdict.residuals:
            assert r.note, f"Residual {r.name} has empty note"

    def test_exactly_five_residuals(self) -> None:
        verdict = _proven_relation_closure_verdict()
        assert len(verdict.residuals) == 5


# ===========================================================================
# §11 Trace reference
# ===========================================================================


class TestTraceRef:
    """Every verdict carries trace_ref."""

    def test_proven_has_trace(self) -> None:
        verdict = _proven_relation_closure_verdict()
        assert verdict.trace_ref
        assert "proven" in verdict.trace_ref

    def test_refused_has_trace(self) -> None:
        verdict = prove_relation_closure(
            first_verdict="bad",  # type: ignore[arg-type]
            second_verdict="bad",  # type: ignore[arg-type]
            relation_type=RelationType.PREDICATIVE,
            relation_maqam="maqam",
            relation_evidence="evidence",
            closure_scope="scope",
        )
        assert verdict.trace_ref
        assert "refused" in verdict.trace_ref

    def test_candidate_trace_ref(self) -> None:
        verdict = _proven_relation_closure_verdict()
        c = verdict.candidate
        assert c is not None
        assert c.trace_ref
        assert "proven" in c.trace_ref


# ===========================================================================
# §12 Birth guards
# ===========================================================================


class TestBirthGuards:
    """RelationClosureCandidate has birth validation."""

    @pytest.mark.parametrize(
        "field",
        [
            "first_closure_ref",
            "second_closure_ref",
            "first_dal_identity_ref",
            "second_dal_identity_ref",
            "relation_maqam",
            "relation_evidence",
            "closure_scope",
        ],
    )
    def test_empty_string_field_rejected(self, field: str) -> None:
        kwargs = {
            "first_closure_ref": "ref1",
            "second_closure_ref": "ref2",
            "first_dal_identity_ref": "id1",
            "second_dal_identity_ref": "id2",
            "relation_type": RelationType.PREDICATIVE,
            "relation_maqam": "maqam",
            "relation_evidence": "evidence",
            "closure_scope": "scope",
            "rank": Rank.CANDIDATE,
            "residuals": (),
            "trace_ref": "test_trace",
        }
        kwargs[field] = ""
        with pytest.raises(WeightCarrierSchemaError):
            RelationClosureCandidate(**kwargs)  # type: ignore[arg-type]

    def test_empty_trace_ref_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            RelationClosureCandidate(
                first_closure_ref="ref1",
                second_closure_ref="ref2",
                first_dal_identity_ref="id1",
                second_dal_identity_ref="id2",
                relation_type=RelationType.PREDICATIVE,
                relation_maqam="maqam",
                relation_evidence="evidence",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )

    def test_invalid_rank_type_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            RelationClosureCandidate(
                first_closure_ref="ref1",
                second_closure_ref="ref2",
                first_dal_identity_ref="id1",
                second_dal_identity_ref="id2",
                relation_type=RelationType.PREDICATIVE,
                relation_maqam="maqam",
                relation_evidence="evidence",
                closure_scope="scope",
                rank="not_a_rank",  # type: ignore[arg-type]
                residuals=(),
                trace_ref="test",
            )

    def test_invalid_relation_type_rejected(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            RelationClosureCandidate(
                first_closure_ref="ref1",
                second_closure_ref="ref2",
                first_dal_identity_ref="id1",
                second_dal_identity_ref="id2",
                relation_type="INVALID",  # type: ignore[arg-type]
                relation_maqam="maqam",
                relation_evidence="evidence",
                closure_scope="scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test",
            )


# ===========================================================================
# §13 Forbidden symbols
# ===========================================================================


class TestForbiddenSymbols:
    """PR-D4 must NOT export or instantiate forbidden symbols."""

    def test_module_does_not_export_forbidden(self) -> None:
        import taaqqul_slot_geometry.weight.relation_closure as mod

        exported = set(mod.__all__)
        for sym in FORBIDDEN_SYMBOLS:
            assert sym not in exported, f"Forbidden symbol exported: {sym}"

    def test_source_does_not_define_forbidden(self) -> None:
        repo_root = pathlib.Path(__file__).resolve().parent.parent
        src = repo_root / "src" / "taaqqul_slot_geometry" / "weight" / "relation_closure.py"
        tree = ast.parse(src.read_text(encoding="utf-8"))
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
# §14 Package export surface continuity
# ===========================================================================


class TestPackageExportSurface:
    """weight package exports all declared symbols without failure."""

    def test_weight_package_exports_semantic_categories(self) -> None:
        import taaqqul_slot_geometry.weight as weight

        assert hasattr(weight, "SEMANTIC_CATEGORIES")

    def test_weight_package_exports_semantic_slot_geometry_rank_ceiling(
        self,
    ) -> None:
        import taaqqul_slot_geometry.weight as weight

        assert hasattr(weight, "SEMANTIC_SLOT_GEOMETRY_RANK_CEILING")

    def test_weight_package_exports_branch_link_candidate(self) -> None:
        import taaqqul_slot_geometry.weight as weight

        assert hasattr(weight, "BranchLinkCandidate")

    def test_weight_package_exports_relation_closure_symbols(self) -> None:
        import taaqqul_slot_geometry.weight as weight

        assert hasattr(weight, "RelationClosureCandidate")
        assert hasattr(weight, "RelationClosureVerdict")
        assert hasattr(weight, "RelationClosureState")
        assert hasattr(weight, "RelationType")
        assert hasattr(weight, "prove_relation_closure")

    def test_weight_import_star_surface_does_not_fail(self) -> None:
        namespace: dict[str, object] = {}
        exec("from taaqqul_slot_geometry.weight import *", namespace)  # noqa: S102
        assert "RelationClosureCandidate" in namespace
        assert "SEMANTIC_CATEGORIES" in namespace
        assert "BranchLinkCandidate" in namespace
