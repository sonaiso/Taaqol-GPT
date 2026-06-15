"""Constitutional tests for PV-A2: ManṭūqClosure.

Origin law: docs/48_MANTUQ_BOUNDARY_LAW.md.

This test module proves:
1. prove_mantuq_closure() returns PROVEN with valid inputs.
2. MantuqClosureCandidate ≠ mafhum / majaz / haqiqah / naql.
3. PROVEN IfadahVerdict required.
4. PROVEN MaqamContextBoundaryVerdict required.
5. Maqam concordance: maqam verdict ref must match ifadah's maqam ref.
6. mantuq_scope, spoken_surface_ref, mantuq_evidence, closure_scope required.
7. Residual governance (HIDDEN_FORBIDDEN / BLOCKING → REFUSED).
8. Rank never exceeds MANTUQ_RANK_CEILING.
9. All 5 required deferred residuals present, visible, EXPLANATORY.
10. Every verdict carries trace_ref.
11. Sub-carrier has birth guards.
12. PV-A2 does not export forbidden symbols.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    MANTUQ_RANK_CEILING,
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
    MantuqClosureCandidate,
    MantuqClosureState,
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
    prove_mantuq_closure,
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
    RelationType,
    prove_relation_closure,
)
from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState

# ===========================================================================
# Required deferred residual names (docs/48 §5)
# ===========================================================================

REQUIRED_DEFERRED_RESIDUAL_NAMES = (
    "MAFHUM_NOT_YET_OPENED",
    "MANTUQ_NOT_MAFHUM",
    "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
    "HAQIQAH_ATTEMPT_DEFERRED",
    "NAQL_DEFERRED_UNTIL_TRANSFER_GATE",
)

# Forbidden symbols that PV-A2 must NOT export or instantiate.
FORBIDDEN_SYMBOLS = (
    "MafhumCandidate",
    "MafhumVerdict",
    "MafhumState",
    "MajazVerdict",
    "MajazLicense",
    "ManqulVerdict",
    "ManqulLicense",
    "HaqiqahAttempt",
    "HaqiqahAttemptVerdict",
    "ReferenceExpansion",
    "GPTProposer",
    "GovernmentServiceEngine",
    "ArabicConditionsDAG",
    "Execution",
    "Fatwa",
    "Qada",
    "FinalAuthority",
    "Certificate",
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
        "scope": "pv-a2-mantuq-closure-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(
            anchor="trace://pv-a2/kataba", kind="DECLARED_ENTRY"
        ),
    }


def _syllable(prefix: str = "ka") -> SyllableCandidate:
    return SyllableCandidate(
        **_base("syllable", f"syll-{prefix}", prefix),
        units=((prefix[0], prefix[1] if len(prefix) > 1 else "a"),),
    )


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


def _semantic_slot_verdict(
    root: str = "kataba",
) -> MufradSemanticSlotGeometryVerdict:
    """Build a PROVEN mufrad semantic slot geometry verdict."""
    dal = _dal_only_candidate(root)
    madlul = _madlul_candidate(dal, root)
    cu = _contractable_unit(dal, madlul, root)
    style = _formal_style_verdict()

    verdict = prove_mufrad_semantic_slot_geometry(
        formal_style_candidate=style.candidate,
        dal_only_candidate=dal,
        verbal_madlul_candidate=madlul,
        contractable_unit=cu,
        formal_closure_state=FormalShapeClosureState.CLOSED,
        semantic_category=SemanticCategory.JAMID,
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
    result = prove_dalalah_candidates(
        semantic_slot_verdict=semantic_verdict,
        maqam_context_verdict=maqam_verdict,
        correspondence_domain="arabic_lexical_full_extension",
        part_designation="semantic_component_action",
        inclusion_evidence="part_of_verbal_meaning_field",
        necessary_relation_type=NecessaryRelationType.SABAB,
        relation_evidence="cause_effect_linguistic_evidence",
    )
    assert result.verdict_state is DalalahCandidateState.PROVEN
    return result


def _proven_mufrad_closure(
    root: str = "kataba",
) -> MufradDalalahClosureVerdict:
    """Build a PROVEN mufrad dalalah closure verdict."""
    semantic = _semantic_slot_verdict(root)
    maqam = _maqam_context_verdict(semantic)
    dalalah = _dalalah_candidate_verdict(semantic, maqam)
    closure = prove_mufrad_dalalah_closure(
        semantic_slot_verdict=semantic,
        maqam_context_verdict=maqam,
        dalalah_candidate_verdict=dalalah,
        closure_scope="mufrad_dalalah_minimum_complete",
    )
    assert closure.verdict_state is MufradDalalahClosureState.PROVEN
    return closure


def _formal_style_verdict(
    family: FormalStyleFamily = FormalStyleFamily.DECLARATIVE_STYLE_FORM,
) -> FormalStyleVerdict:
    """Build a PROVEN formal style verdict."""
    verdict = prove_formal_style_candidate(
        style_family=family,
        composition_evidence_ref="test/composition/khabar",
        formal_closure_state=FormalShapeClosureState.CLOSED,
        formal_closure_ref="test/closure/CLOSED",
    )
    assert verdict.verdict_state is FormalStyleState.PROVEN
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


def _proven_maqam_for_ifadah() -> MaqamContextBoundaryVerdict:
    """Return the PROVEN maqam verdict that matches the ifadah chain."""
    semantic = _semantic_slot_verdict("kataba")
    return _maqam_context_verdict(semantic)


# ===========================================================================
# Tests — PROVEN ManṭūqClosure path
# ===========================================================================


class TestProvenMantuqClosure:
    """Tests for the successful PROVEN path."""

    def test_prove_mantuq_closure_returns_proven(self):
        """prove_mantuq_closure() with valid inputs → PROVEN."""
        ifadah_verdict = _proven_ifadah_verdict()
        # Use the same maqam that the ifadah verdict carries
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)
        # The ifadah candidate has maqam_verdict_ref = maqam_verdict.trace_ref
        assert ifadah_verdict.candidate is not None
        assert ifadah_verdict.candidate.maqam_verdict_ref == maqam_verdict.trace_ref

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )

        assert verdict.verdict_state is MantuqClosureState.PROVEN
        assert verdict.candidate is not None
        assert verdict.failure_code is None
        assert verdict.verdict_rank <= MANTUQ_RANK_CEILING
        assert verdict.trace_ref != ""

    def test_proven_candidate_fields(self):
        """The MantuqClosureCandidate carries all required fields."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )
        assert verdict.candidate is not None
        c = verdict.candidate
        assert c.ifadah_verdict_ref == ifadah_verdict.trace_ref
        assert c.maqam_verdict_ref == maqam_verdict.trace_ref
        assert c.mantuq_scope == "explicit_spoken_indication"
        assert c.spoken_surface_ref == "surface://kataba-al-waladu"
        assert c.mantuq_evidence == "preserved_spoken_origin_evidence"
        assert c.closure_scope == "mantuq_closure_minimal"
        assert c.rank <= MANTUQ_RANK_CEILING
        assert c.trace_ref != ""

    def test_trace_ref_present(self):
        """Every PROVEN verdict carries a non-empty trace_ref."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )
        assert verdict.trace_ref
        assert verdict.candidate is not None
        assert verdict.candidate.trace_ref


# ===========================================================================
# Tests — ManṭūqClosure ≠ Mafhum / Majaz / Haqiqah / Naql
# ===========================================================================


class TestMantuqNotMafhum:
    """MantuqClosure does not produce any forbidden horizontal output."""

    def test_mantuq_closure_is_not_mafhum(self):
        """MantuqClosureCandidate is not a MafhumCandidate."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )
        assert verdict.verdict_state is MantuqClosureState.PROVEN
        # The class name proves this is NOT mafhum
        assert type(verdict.candidate).__name__ == "MantuqClosureCandidate"
        assert type(verdict.candidate).__name__ != "MafhumCandidate"

    def test_mantuq_closure_is_not_majaz(self):
        """MantuqClosureCandidate does not claim majaz."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )
        assert verdict.verdict_state is MantuqClosureState.PROVEN
        assert type(verdict.candidate).__name__ != "MajazVerdict"

    def test_mantuq_closure_is_not_haqiqah_attempt(self):
        """MantuqClosureCandidate does not attempt haqiqah."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )
        assert verdict.verdict_state is MantuqClosureState.PROVEN
        assert type(verdict.candidate).__name__ != "HaqiqahAttempt"

    def test_forbidden_symbols_not_in_module(self):
        """PV-A2 module does not define or export forbidden symbols."""
        mod_path = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/mantuq_closure.py"
        )
        tree = ast.parse(mod_path.read_text())
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
                f"Forbidden symbol '{sym}' found in mantuq_closure.py"
            )


# ===========================================================================
# Tests — refuses without Ifādah
# ===========================================================================


class TestRefusesWithoutIfadah:
    """Tests for refusal when IfadahVerdict is missing/invalid."""

    def test_refuses_non_ifadah_type(self):
        """REFUSED when ifadah_verdict is not an IfadahVerdict."""
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict="not_an_ifadah_verdict",  # type: ignore[arg-type]
            maqam_verdict=maqam_verdict,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH
        assert verdict.candidate is None

    def test_refuses_non_proven_ifadah(self):
        """REFUSED when IfadahVerdict is not PROVEN."""
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)
        refused_ifadah = IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.REFUSED,
            failure_code=FailureCode.NO_RELATION_CLOSURE,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="ifadah/refused",
        )

        verdict = prove_mantuq_closure(
            ifadah_verdict=refused_ifadah,
            maqam_verdict=maqam_verdict,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH

    def test_refuses_missing_ifadah_candidate(self):
        """REFUSED when IfadahVerdict has no candidate."""
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)
        # Manually craft a verdict with PROVEN state but None candidate
        broken_ifadah = IfadahVerdict(
            candidate=None,
            verdict_state=IfadahState.PROVEN,
            failure_code=None,
            verdict_rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="ifadah/broken",
        )

        verdict = prove_mantuq_closure(
            ifadah_verdict=broken_ifadah,
            maqam_verdict=maqam_verdict,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH


# ===========================================================================
# Tests — refuses without Maqam
# ===========================================================================


class TestRefusesWithoutMaqam:
    """Tests for refusal when MaqamContextBoundaryVerdict is invalid."""

    def test_refuses_non_maqam_type(self):
        """REFUSED when maqam_verdict is not a MaqamContextBoundaryVerdict."""
        ifadah_verdict = _proven_ifadah_verdict()

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict="not_a_maqam_verdict",  # type: ignore[arg-type]
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH_MAQAM
        assert verdict.candidate is None

    def test_refuses_non_proven_maqam(self):
        """REFUSED when MaqamContextBoundaryVerdict is not PROVEN."""
        ifadah_verdict = _proven_ifadah_verdict()
        refused_maqam = MaqamContextBoundaryVerdict(
            candidate=None,
            verdict_state=MaqamContextState.REFUSED,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="maqam/refused",
        )

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=refused_maqam,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_IFADAH_MAQAM

    def test_refuses_maqam_divergence(self):
        """REFUSED when maqam trace_ref doesn't match ifadah's maqam ref."""
        ifadah_verdict = _proven_ifadah_verdict()
        # Build a different maqam that doesn't match
        semantic2 = _semantic_slot_verdict("darasa")
        different_maqam = _maqam_context_verdict(semantic2)
        # Ensure it's a different trace ref from what ifadah expects
        assert ifadah_verdict.candidate is not None
        if different_maqam.trace_ref == ifadah_verdict.candidate.maqam_verdict_ref:
            # If they happen to be the same, create one with a different ref
            different_maqam = MaqamContextBoundaryVerdict(
                candidate=different_maqam.candidate,
                verdict_state=MaqamContextState.PROVEN,
                failure_code=None,
                verdict_rank=different_maqam.verdict_rank,
                residuals=different_maqam.residuals,
                trace_ref="maqam/different/divergent_ref",
            )

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=different_maqam,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.MANTUQ_MAQAM_DIVERGENCE


# ===========================================================================
# Tests — refuses empty fields
# ===========================================================================


class TestRefusesEmptyFields:
    """Tests for refusal when required string fields are empty."""

    def _valid_args(self) -> dict:
        """Return valid arguments for prove_mantuq_closure."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)
        return {
            "ifadah_verdict": ifadah_verdict,
            "maqam_verdict": maqam_verdict,
            "mantuq_scope": "explicit_spoken_indication",
            "spoken_surface_ref": "surface://kataba-al-waladu",
            "mantuq_evidence": "preserved_spoken_origin_evidence",
            "closure_scope": "mantuq_closure_minimal",
        }

    def test_refuses_empty_mantuq_scope(self):
        """REFUSED when mantuq_scope is empty."""
        args = self._valid_args()
        args["mantuq_scope"] = ""
        verdict = prove_mantuq_closure(**args)
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANTUQ_SCOPE

    def test_refuses_whitespace_mantuq_scope(self):
        """REFUSED when mantuq_scope is whitespace-only."""
        args = self._valid_args()
        args["mantuq_scope"] = "   "
        verdict = prove_mantuq_closure(**args)
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANTUQ_SCOPE

    def test_refuses_empty_spoken_surface_ref(self):
        """REFUSED when spoken_surface_ref is empty."""
        args = self._valid_args()
        args["spoken_surface_ref"] = ""
        verdict = prove_mantuq_closure(**args)
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_SPOKEN_SURFACE

    def test_refuses_empty_mantuq_evidence(self):
        """REFUSED when mantuq_evidence is empty."""
        args = self._valid_args()
        args["mantuq_evidence"] = ""
        verdict = prove_mantuq_closure(**args)
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANTUQ_EVIDENCE

    def test_refuses_empty_closure_scope(self):
        """REFUSED when closure_scope is empty."""
        args = self._valid_args()
        args["closure_scope"] = ""
        verdict = prove_mantuq_closure(**args)
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MANTUQ_CLOSURE_SCOPE


# ===========================================================================
# Tests — residuals and rank
# ===========================================================================


class TestResidualGovernance:
    """Tests for residual governance and rank ceiling."""

    def test_deferred_residuals_visible_explanatory(self):
        """All 5 required deferred residuals present, visible, EXPLANATORY."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )
        assert verdict.verdict_state is MantuqClosureState.PROVEN
        residual_names = tuple(r.name for r in verdict.residuals)
        for expected_name in REQUIRED_DEFERRED_RESIDUAL_NAMES:
            assert expected_name in residual_names, (
                f"Missing deferred residual: {expected_name}"
            )
        for r in verdict.residuals:
            assert r.kind is ResidualKind.EXPLANATORY
            assert r.visible is True

    def test_hidden_residual_refuses(self):
        """REFUSED when input ifadah verdict contains hidden residual."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        # Inject a HIDDEN_FORBIDDEN residual into the ifadah verdict
        hidden = Residual(
            name="INJECTED_HIDDEN",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=False,
            note="test injection",
        )
        poisoned = IfadahVerdict(
            candidate=ifadah_verdict.candidate,
            verdict_state=ifadah_verdict.verdict_state,
            failure_code=ifadah_verdict.failure_code,
            verdict_rank=ifadah_verdict.verdict_rank,
            residuals=(hidden,),
            trace_ref=ifadah_verdict.trace_ref,
        )

        verdict = prove_mantuq_closure(
            ifadah_verdict=poisoned,
            maqam_verdict=maqam_verdict,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL

    def test_blocking_residual_refuses(self):
        """REFUSED when input ifadah verdict contains blocking residual."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        blocking = Residual(
            name="INJECTED_BLOCKING",
            kind=ResidualKind.BLOCKING,
            visible=True,
            note="test injection",
        )
        poisoned = IfadahVerdict(
            candidate=ifadah_verdict.candidate,
            verdict_state=ifadah_verdict.verdict_state,
            failure_code=ifadah_verdict.failure_code,
            verdict_rank=ifadah_verdict.verdict_rank,
            residuals=(blocking,),
            trace_ref=ifadah_verdict.trace_ref,
        )

        verdict = prove_mantuq_closure(
            ifadah_verdict=poisoned,
            maqam_verdict=maqam_verdict,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT

    def test_rank_never_exceeds_mantuq_ceiling(self):
        """Rank of the candidate is bounded by MANTUQ_RANK_CEILING."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )
        assert verdict.verdict_state is MantuqClosureState.PROVEN
        assert verdict.verdict_rank <= MANTUQ_RANK_CEILING
        assert verdict.candidate is not None
        assert verdict.candidate.rank <= MANTUQ_RANK_CEILING

    def test_mantuq_rank_ceiling_bounded_by_tanzil(self):
        """MANTUQ_RANK_CEILING ≤ TANZIL_RANK_CEILING (docs/48 §5)."""
        from taaqqul_slot_geometry.weight import TANZIL_RANK_CEILING
        assert MANTUQ_RANK_CEILING <= TANZIL_RANK_CEILING


# ===========================================================================
# Tests — carrier birth guards
# ===========================================================================


class TestCarrierBirthGuards:
    """Tests for MantuqClosureCandidate __post_init__ validation."""

    def test_candidate_refuses_empty_ifadah_ref(self):
        """WeightCarrierSchemaError when ifadah_verdict_ref is empty."""
        with pytest.raises(WeightCarrierSchemaError):
            MantuqClosureCandidate(
                ifadah_verdict_ref="",
                maqam_verdict_ref="maqam_ref",
                mantuq_scope="scope",
                spoken_surface_ref="surface",
                mantuq_evidence="evidence",
                closure_scope="closure_scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_candidate_refuses_empty_mantuq_scope(self):
        """WeightCarrierSchemaError when mantuq_scope is empty."""
        with pytest.raises(WeightCarrierSchemaError):
            MantuqClosureCandidate(
                ifadah_verdict_ref="ifadah_ref",
                maqam_verdict_ref="maqam_ref",
                mantuq_scope="",
                spoken_surface_ref="surface",
                mantuq_evidence="evidence",
                closure_scope="closure_scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_candidate_refuses_rank_above_ceiling(self):
        """WeightCarrierSchemaError when rank exceeds ceiling."""
        # Find a rank above the ceiling if possible
        all_ranks = list(Rank)
        above_ceiling = [r for r in all_ranks if r > MANTUQ_RANK_CEILING]
        if above_ceiling:
            with pytest.raises(WeightCarrierSchemaError):
                MantuqClosureCandidate(
                    ifadah_verdict_ref="ifadah_ref",
                    maqam_verdict_ref="maqam_ref",
                    mantuq_scope="scope",
                    spoken_surface_ref="surface",
                    mantuq_evidence="evidence",
                    closure_scope="closure_scope",
                    rank=above_ceiling[0],
                    residuals=(),
                    trace_ref="trace",
                )

    def test_candidate_refuses_non_tuple_residuals(self):
        """WeightCarrierSchemaError when residuals is not a tuple."""
        with pytest.raises(WeightCarrierSchemaError):
            MantuqClosureCandidate(
                ifadah_verdict_ref="ifadah_ref",
                maqam_verdict_ref="maqam_ref",
                mantuq_scope="scope",
                spoken_surface_ref="surface",
                mantuq_evidence="evidence",
                closure_scope="closure_scope",
                rank=Rank.CANDIDATE,
                residuals=[],  # type: ignore[arg-type]
                trace_ref="trace",
            )

    def test_candidate_refuses_empty_trace_ref(self):
        """WeightCarrierSchemaError when trace_ref is empty."""
        with pytest.raises(WeightCarrierSchemaError):
            MantuqClosureCandidate(
                ifadah_verdict_ref="ifadah_ref",
                maqam_verdict_ref="maqam_ref",
                mantuq_scope="scope",
                spoken_surface_ref="surface",
                mantuq_evidence="evidence",
                closure_scope="closure_scope",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# Tests — Upstream MufradDalālah Continuity (PV-A2.2)
# ===========================================================================


class TestUpstreamMufradDalalahContinuity:
    """Tests that ManṭūqClosure enforces upstream MufradDalālah continuity.

    Origin law: docs/48_MANTUQ_BOUNDARY_LAW.md, PV-A1.1 clarification.

    The governing sentence:
        لا منطوق فوق سطح عارٍ.
        ولا منطوق بلا أثر دلالة مفردة مغلقة.

    ManṭūqClosure does NOT create the lexical meaning.
    ManṭūqClosure consumes IfadahVerdict built on RelationClosure
    built on MufradDalālahClosure. The relation_closure_ref in the
    IfadahCandidate is the trace-link to that upstream chain.
    """

    def test_refuses_if_ifadah_has_no_relation_closure_ref(self):
        """REFUSED when IfadahCandidate.relation_closure_ref is empty."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        # Craft an IfadahCandidate with an empty relation_closure_ref
        assert ifadah_verdict.candidate is not None
        original = ifadah_verdict.candidate
        # Use object.__setattr__ to bypass frozen dataclass
        broken_candidate = IfadahCandidate.__new__(IfadahCandidate)
        for field in (
            "formal_style_ref", "maqam_verdict_ref", "speech_force",
            "first_dal_identity_ref", "second_dal_identity_ref",
            "ifadah_evidence", "closure_scope", "bridge_compatible",
            "rank", "residuals", "trace_ref",
        ):
            object.__setattr__(broken_candidate, field, getattr(original, field))
        object.__setattr__(broken_candidate, "relation_closure_ref", "")

        broken_ifadah = IfadahVerdict(
            candidate=broken_candidate,
            verdict_state=IfadahState.PROVEN,
            failure_code=None,
            verdict_rank=ifadah_verdict.verdict_rank,
            residuals=ifadah_verdict.residuals,
            trace_ref=ifadah_verdict.trace_ref,
        )

        verdict = prove_mantuq_closure(
            ifadah_verdict=broken_ifadah,
            maqam_verdict=maqam_verdict,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.UPSTREAM_MUFRAD_DALALAH_MISSING
        assert verdict.candidate is None
        assert "upstream_mufrad_dalalah_missing" in verdict.trace_ref

    def test_refuses_if_ifadah_has_whitespace_relation_closure_ref(self):
        """REFUSED when IfadahCandidate.relation_closure_ref is whitespace."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        assert ifadah_verdict.candidate is not None
        original = ifadah_verdict.candidate
        broken_candidate = IfadahCandidate.__new__(IfadahCandidate)
        for field in (
            "formal_style_ref", "maqam_verdict_ref", "speech_force",
            "first_dal_identity_ref", "second_dal_identity_ref",
            "ifadah_evidence", "closure_scope", "bridge_compatible",
            "rank", "residuals", "trace_ref",
        ):
            object.__setattr__(broken_candidate, field, getattr(original, field))
        object.__setattr__(broken_candidate, "relation_closure_ref", "   ")

        broken_ifadah = IfadahVerdict(
            candidate=broken_candidate,
            verdict_state=IfadahState.PROVEN,
            failure_code=None,
            verdict_rank=ifadah_verdict.verdict_rank,
            residuals=ifadah_verdict.residuals,
            trace_ref=ifadah_verdict.trace_ref,
        )

        verdict = prove_mantuq_closure(
            ifadah_verdict=broken_ifadah,
            maqam_verdict=maqam_verdict,
            mantuq_scope="scope",
            spoken_surface_ref="surface",
            mantuq_evidence="evidence",
            closure_scope="closure_scope",
        )
        assert verdict.verdict_state is MantuqClosureState.REFUSED
        assert verdict.failure_code is FailureCode.UPSTREAM_MUFRAD_DALALAH_MISSING

    def test_proven_path_has_valid_relation_closure_ref(self):
        """The happy path IfadahCandidate has a non-empty relation_closure_ref."""
        ifadah_verdict = _proven_ifadah_verdict()
        assert ifadah_verdict.candidate is not None
        assert ifadah_verdict.candidate.relation_closure_ref.strip() != ""

    def test_upstream_mufrad_dalalah_trace_is_preserved(self):
        """PROVEN ManṭūqClosure preserves ifadah_verdict_ref linking upstream."""
        ifadah_verdict = _proven_ifadah_verdict()
        semantic = _semantic_slot_verdict("kataba")
        maqam_verdict = _maqam_context_verdict(semantic)

        verdict = prove_mantuq_closure(
            ifadah_verdict=ifadah_verdict,
            maqam_verdict=maqam_verdict,
            mantuq_scope="explicit_spoken_indication",
            spoken_surface_ref="surface://kataba-al-waladu",
            mantuq_evidence="preserved_spoken_origin_evidence",
            closure_scope="mantuq_closure_minimal",
        )
        assert verdict.verdict_state is MantuqClosureState.PROVEN
        assert verdict.candidate is not None
        # The candidate's ifadah_verdict_ref links to the full upstream chain
        assert verdict.candidate.ifadah_verdict_ref == ifadah_verdict.trace_ref
        # And the ifadah itself was built from relation_closure
        assert ifadah_verdict.candidate is not None
        assert ifadah_verdict.candidate.relation_closure_ref != ""

    def test_no_lexical_meaning_new_layer_created(self):
        """PV-A2.2 does NOT introduce LexicalMeaningClosure symbols."""
        import taaqqul_slot_geometry.weight.mantuq_closure as mc_mod
        all_names = dir(mc_mod)
        forbidden = [
            "LexicalMeaningClosure",
            "LexicalMeaningClosureCandidate",
            "LexicalAtomClosure",
            "LexicalAtomClosureCandidate",
        ]
        for name in forbidden:
            assert name not in all_names, (
                f"PV-A2.2 must not create {name}"
            )

    def test_no_lexical_atom_closure_symbols_exported(self):
        """The weight package does NOT export any LexicalAtomClosure symbol."""
        import taaqqul_slot_geometry.weight as weight_pkg
        all_names = dir(weight_pkg)
        forbidden = [
            "LexicalAtomClosure",
            "LexicalAtomClosureCandidate",
            "LexicalMeaningClosure",
            "LexicalMeaningClosureCandidate",
        ]
        for name in forbidden:
            assert name not in all_names, (
                f"weight package must not export {name}"
            )
