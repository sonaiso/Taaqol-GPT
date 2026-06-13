"""Constitutional tests for PR-17: DalMadlulBindingCandidate Boundary.

Origin: docs/26, docs/27, docs/29, docs/31_DAL_MADLUL_BINDING_LAW.md.

Coverage of the 15 required constitutional tests:

1.  DalMadlulBindingCandidate requires DalOnlyCandidate.
2.  DalMadlulBindingCandidate requires VerbalMadlulCandidate.
3.  DalMadlulBindingCandidate requires registry evidence (both FOUND).
4.  DalMadlulBindingCandidate requires identity match (madlul.dal_only is dal).
5.  DalMadlulBindingCandidate is not Meaning.
6.  DalMadlulBindingCandidate carries no ifadah/hukm/reality fields.
7.  DalMadlulBindingCandidate is not ContractableUnitGeometry.
8.  DalMadlulBindingCandidate is not RelationCandidate.
9.  Rank is bounded.
10. Residual governance: HIDDEN_FORBIDDEN refused.
11. Residual governance: BLOCKING refused.
12. Residuals from both candidates are merged.
13. trace_ref remains reference, not ledger commit.
14. Every refusal has named FailureCode.
15. PR-17 imports/defines no ContractableUnitGeometry, ExtraLetterLicense,
    C_Aug, Ifadah, Hukm, or Reality.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank, RankLattice
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    BINDING_RANK_CEILING,
    MADLUL_BOUNDARY_RANK_CEILING,
    BindingState,
    BoundaryEvidence,
    DalBoundaryState,
    DalMadlulBindingCandidate,
    DalMadlulBindingVerdict,
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
    ResidualGovernanceVerdict,
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
    prove_dal,
    prove_verbal_madlul,
    weigh,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
)

# ---------------------------------------------------------------------------
# Test fixtures — build a DalOnlyCandidate through the lawful chain
# (Mirrors test_verbal_madlul_boundary.py pattern)
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr17-binding-boundary-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr17/kataba", kind="DECLARED_ENTRY"),
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
    """Produce a valid WeightFitCandidate through the lawful chain."""
    candidate = _weight_readiness()
    governance = omega_governance((), Rank.CANDIDATE)
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED
    assert result.candidate is not None
    return result.candidate


def _granted_governance() -> ResidualGovernanceVerdict:
    """A GRANTED omega governance verdict with no residuals."""
    return omega_governance((), Rank.CANDIDATE)


def _lexical_evidence() -> BoundaryEvidence:
    return BoundaryEvidence(
        kind=LicenseBoundaryKind.LEXICAL,
        attestation="lexical_root_attested",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
    )


def _licensing_verdict() -> LicensingBoundaryVerdict:
    """Produce a valid LicensingBoundaryVerdict through the lawful chain."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = _lexical_evidence()
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    return result.verdict


def _dal_only_candidate() -> DalOnlyCandidate:
    """Produce a valid DalOnlyCandidate through the lawful chain."""
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "kataba", "phonetic://kataba", "graphic://kataba")
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _madlul_candidate(dal: DalOnlyCandidate) -> VerbalMadlulCandidate:
    """Produce a valid VerbalMadlulCandidate from a given DalOnlyCandidate."""
    from taaqqul_slot_geometry.weight.verbal_madlul import MadlulBoundaryState

    result = prove_verbal_madlul(
        prior_dal=dal,
        wad_usage_boundary="lexical-wadʿ-boundary",
        correspondence_candidate="correspondence/kataba",
        inclusion_candidate="inclusion/kataba",
        iltizam_condition="iltizam/kataba",
    )
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _dal_registry_proof() -> RegistryLookupResult:
    """Build a FOUND RegistryLookupResult for DAL_ONLY."""
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
    """Build a FOUND RegistryLookupResult for VERBAL_MADLUL."""
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


# ---------------------------------------------------------------------------
# 1-4. Input boundary enforcement
# ---------------------------------------------------------------------------


class TestInputBoundary:
    """Tests for bind_dal_madlul() input boundary enforcement."""

    def test_non_dal_candidate_refused(self) -> None:
        """1. bind_dal_madlul() refuses non-DalOnlyCandidate input."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal_candidate="not a candidate",  # type: ignore[arg-type]
            madlul_candidate=madlul,
            dal_registry=_dal_registry_proof(),
            madlul_registry=_madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert result.candidate is None

    def test_non_madlul_candidate_refused(self) -> None:
        """2. bind_dal_madlul() refuses non-VerbalMadlulCandidate input."""
        dal = _dal_only_candidate()
        result = bind_dal_madlul(
            dal_candidate=dal,
            madlul_candidate="not a candidate",  # type: ignore[arg-type]
            dal_registry=_dal_registry_proof(),
            madlul_registry=_madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert result.candidate is None

    def test_identity_mismatch_refused(self) -> None:
        """4. bind_dal_madlul() refuses when madlul.dal_only is not dal_candidate."""
        # Create a lawful dal and madlul pair
        dal1 = _dal_only_candidate()
        madlul = _madlul_candidate(dal1)
        # Create a DIFFERENT DalOnlyCandidate
        dal2 = _dal_only_candidate()
        # dal2 is a different instance than dal1
        assert dal2 is not dal1

        result = bind_dal_madlul(
            dal_candidate=dal2,
            madlul_candidate=madlul,
            dal_registry=_dal_registry_proof(),
            madlul_registry=_madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.REFUSED
        assert result.failure_code is FailureCode.IDENTITY_BROKEN
        assert result.candidate is None

    def test_dal_registry_not_found_refused(self) -> None:
        """3a. bind_dal_madlul() refuses when dal_registry is not FOUND."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        refused_registry = RegistryLookupResult(
            state=RegistryLookupState.REFUSED,
            entry=None,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        )
        result = bind_dal_madlul(
            dal_candidate=dal,
            madlul_candidate=madlul,
            dal_registry=refused_registry,
            madlul_registry=_madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None

    def test_madlul_registry_not_found_refused(self) -> None:
        """3b. bind_dal_madlul() refuses when madlul_registry is not FOUND."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        refused_registry = RegistryLookupResult(
            state=RegistryLookupState.REFUSED,
            entry=None,
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        )
        result = bind_dal_madlul(
            dal_candidate=dal,
            madlul_candidate=madlul,
            dal_registry=_dal_registry_proof(),
            madlul_registry=refused_registry,
        )
        assert result.verdict_state is BindingState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None

    def test_invalid_dal_registry_type_refused(self) -> None:
        """3c. bind_dal_madlul() refuses non-RegistryLookupResult for dal_registry."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal_candidate=dal,
            madlul_candidate=madlul,
            dal_registry="not a result",  # type: ignore[arg-type]
            madlul_registry=_madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert result.candidate is None


# ---------------------------------------------------------------------------
# 5-8. DalMadlulBindingCandidate boundary invariants
# ---------------------------------------------------------------------------


class TestBoundaryInvariants:
    """Tests proving DalMadlulBindingCandidate is NOT meaning/ifadah/hukm/reality."""

    def test_binding_candidate_is_not_meaning(self) -> None:
        """5. DalMadlulBindingCandidate is not Meaning."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.BOUND
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "meaning")
        assert not hasattr(candidate, "reference")
        assert not hasattr(candidate, "denotation")
        assert not hasattr(candidate, "concept")
        assert not hasattr(candidate, "semantic_content")

    def test_binding_candidate_carries_no_ifadah_hukm_reality(self) -> None:
        """6. DalMadlulBindingCandidate carries no ifadah/hukm/reality fields."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "ifadah")
        assert not hasattr(candidate, "hukm")
        assert not hasattr(candidate, "reality")
        assert not hasattr(candidate, "truth_value")
        assert not hasattr(candidate, "tanzil")

    def test_binding_candidate_is_not_contractable_unit(self) -> None:
        """7. DalMadlulBindingCandidate is not ContractableUnitGeometry."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "contractability")
        assert not hasattr(candidate, "unit_geometry")
        assert type(candidate).__name__ == "DalMadlulBindingCandidate"

    def test_binding_candidate_is_not_relation_candidate(self) -> None:
        """8. DalMadlulBindingCandidate is not RelationCandidate."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "composition")
        assert not hasattr(candidate, "relation")
        assert not hasattr(candidate, "nisba")


# ---------------------------------------------------------------------------
# 9. Rank is bounded
# ---------------------------------------------------------------------------


class TestRankBounding:
    """Tests proving rank is bounded by BINDING_RANK_CEILING."""

    def test_binding_rank_bounded(self) -> None:
        """9. Rank is bounded to BINDING_RANK_CEILING."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.BOUND
        assert result.verdict_rank <= BINDING_RANK_CEILING
        assert result.candidate is not None
        assert result.candidate.binding_rank <= BINDING_RANK_CEILING

    def test_binding_rank_ceiling_equals_madlul_ceiling(self) -> None:
        """9b. BINDING_RANK_CEILING == MADLUL_BOUNDARY_RANK_CEILING."""
        assert BINDING_RANK_CEILING == MADLUL_BOUNDARY_RANK_CEILING

    def test_binding_rank_is_meet_of_inputs(self) -> None:
        """9c. Binding rank is RankLattice.meet of both input ranks."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        assert result.candidate is not None
        expected = RankLattice.meet(dal.dal_rank, madlul.madlul_rank)
        expected = RankLattice.meet(expected, BINDING_RANK_CEILING)
        assert result.candidate.binding_rank == expected


# ---------------------------------------------------------------------------
# 10-12. Residual governance
# ---------------------------------------------------------------------------


class TestResidualGovernance:
    """Tests proving residual governance is enforced."""

    def test_hidden_forbidden_residual_refused(self) -> None:
        """10. HIDDEN_FORBIDDEN residual in dal_candidate triggers refusal."""
        # Build dal/madlul with a HIDDEN_FORBIDDEN residual through direct construction
        verdict = _licensing_verdict()
        hidden_r = Residual(
            name="hidden_residual",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=True,
        )
        dal = DalOnlyCandidate(
            signifier_identity="kataba",
            phonetic_trace_ref="phonetic://kataba",
            graphic_trace_ref="graphic://kataba",
            prior_licensing_verdict=verdict,
            dal_rank=Rank.HYPOTHESIS,
            residuals=(hidden_r,),
            trace_ref="dal/hidden_test",
        )
        madlul = VerbalMadlulCandidate(
            dal_only=dal,
            wad_usage_boundary="lexical-wadʿ",
            correspondence_candidate="",
            inclusion_candidate="",
            iltizam_condition="",
            existence_carrier_candidate="",
            event_carrier_candidate="",
            relation_affordance_candidate="",
            madlul_rank=Rank.HYPOTHESIS,
            residuals=(),
            trace_ref="madlul/hidden_test",
        )
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.REFUSED
        assert result.failure_code is FailureCode.HIDDEN_RESIDUAL

    def test_blocking_residual_refused(self) -> None:
        """11. BLOCKING residual in madlul_candidate triggers refusal."""
        verdict = _licensing_verdict()
        blocking_r = Residual(
            name="blocking_residual",
            kind=ResidualKind.BLOCKING,
            visible=True,
        )
        dal = DalOnlyCandidate(
            signifier_identity="kataba",
            phonetic_trace_ref="phonetic://kataba",
            graphic_trace_ref="graphic://kataba",
            prior_licensing_verdict=verdict,
            dal_rank=Rank.HYPOTHESIS,
            residuals=(),
            trace_ref="dal/blocking_test",
        )
        madlul = VerbalMadlulCandidate(
            dal_only=dal,
            wad_usage_boundary="lexical-wadʿ",
            correspondence_candidate="",
            inclusion_candidate="",
            iltizam_condition="",
            existence_carrier_candidate="",
            event_carrier_candidate="",
            relation_affordance_candidate="",
            madlul_rank=Rank.HYPOTHESIS,
            residuals=(blocking_r,),
            trace_ref="madlul/blocking_test",
        )
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.REFUSED
        assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT

    def test_residuals_merged_from_both_candidates(self) -> None:
        """12. Residuals from both candidates are merged."""
        verdict = _licensing_verdict()
        r1 = Residual(
            name="dal_residual",
            kind=ResidualKind.NON_BLOCKING,
            visible=True,
        )
        r2 = Residual(
            name="madlul_residual",
            kind=ResidualKind.NON_BLOCKING,
            visible=True,
        )
        dal = DalOnlyCandidate(
            signifier_identity="kataba",
            phonetic_trace_ref="phonetic://kataba",
            graphic_trace_ref="graphic://kataba",
            prior_licensing_verdict=verdict,
            dal_rank=Rank.HYPOTHESIS,
            residuals=(r1,),
            trace_ref="dal/merge_test",
        )
        madlul = VerbalMadlulCandidate(
            dal_only=dal,
            wad_usage_boundary="lexical-wadʿ",
            correspondence_candidate="",
            inclusion_candidate="",
            iltizam_condition="",
            existence_carrier_candidate="",
            event_carrier_candidate="",
            relation_affordance_candidate="",
            madlul_rank=Rank.HYPOTHESIS,
            residuals=(r2,),
            trace_ref="madlul/merge_test",
        )
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.BOUND
        assert result.candidate is not None
        assert r1 in result.candidate.residuals
        assert r2 in result.candidate.residuals
        assert len(result.candidate.residuals) == 2


# ---------------------------------------------------------------------------
# 13. trace_ref remains reference
# ---------------------------------------------------------------------------


class TestTraceRef:
    """Tests proving trace_ref is a reference, not a ledger commit."""

    def test_trace_ref_is_reference(self) -> None:
        """13. trace_ref is a reference string, not a ledger commit."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        assert result.verdict_state is BindingState.BOUND
        assert result.candidate is not None
        assert isinstance(result.candidate.trace_ref, str)
        assert result.candidate.trace_ref.startswith("bind_dal_madlul/")
        assert "/" in result.candidate.trace_ref


# ---------------------------------------------------------------------------
# 14. Every refusal has named FailureCode
# ---------------------------------------------------------------------------


class TestFailureCodes:
    """Tests proving every refusal carries a named FailureCode."""

    def test_all_refusals_carry_failure_code(self) -> None:
        """14. Every REFUSED verdict carries a named FailureCode."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        cases = [
            # Invalid dal_candidate
            bind_dal_madlul(
                "bad", madlul,  # type: ignore[arg-type]
                _dal_registry_proof(), _madlul_registry_proof(),
            ),
            # Invalid madlul_candidate
            bind_dal_madlul(
                dal, "bad",  # type: ignore[arg-type]
                _dal_registry_proof(), _madlul_registry_proof(),
            ),
            # Invalid dal_registry type
            bind_dal_madlul(
                dal, madlul,
                "bad", _madlul_registry_proof(),  # type: ignore[arg-type]
            ),
            # Invalid madlul_registry type
            bind_dal_madlul(
                dal, madlul,
                _dal_registry_proof(), "bad",  # type: ignore[arg-type]
            ),
        ]
        for verdict in cases:
            assert verdict.verdict_state is BindingState.REFUSED
            assert verdict.failure_code is not None
            assert isinstance(verdict.failure_code, FailureCode)


# ---------------------------------------------------------------------------
# 15. Forbidden imports
# ---------------------------------------------------------------------------


class TestForbiddenImports:
    """Tests proving PR-17 module does not import forbidden symbols."""

    def test_no_forbidden_symbols_in_module(self) -> None:
        """15. PR-17 imports/defines no forbidden symbols."""
        src = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/dal_madlul_binding.py"
        ).read_text()
        tree = ast.parse(src)

        forbidden_names = {
            "ContractableUnitGeometry",
            "ExtraLetterLicense",
            "C_Aug",
            "Ifadah",
            "IfadahCandidate",
            "Hukm",
            "HukmCandidate",
            "Reality",
            "RealityCandidate",
            "TanzilCandidate",
            "RelationCandidate",
            "CompositionCandidate",
            "LexicalMadlul",
            "SemanticVerdict",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    assert alias.name not in forbidden_names, (
                        f"PR-17 module must not import {alias.name}"
                    )
            elif isinstance(node, ast.ClassDef):
                assert node.name not in forbidden_names, (
                    f"PR-17 module must not define {node.name}"
                )


# ---------------------------------------------------------------------------
# Happy path — full binding success
# ---------------------------------------------------------------------------


class TestHappyPath:
    """Test the complete happy path through bind_dal_madlul()."""

    def test_successful_binding(self) -> None:
        """Full happy path: valid inputs produce BOUND verdict."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        dal_reg = _dal_registry_proof()
        madlul_reg = _madlul_registry_proof()
        result = bind_dal_madlul(dal, madlul, dal_reg, madlul_reg)
        assert result.verdict_state is BindingState.BOUND
        assert result.failure_code is None
        assert result.candidate is not None
        assert isinstance(result.candidate, DalMadlulBindingCandidate)
        assert result.candidate.dal_candidate is dal
        assert result.candidate.madlul_candidate is madlul
        assert result.candidate.dal_registry_proof is dal_reg
        assert result.candidate.madlul_registry_proof is madlul_reg
        assert result.verdict_rank <= BINDING_RANK_CEILING

    def test_binding_candidate_is_frozen(self) -> None:
        """DalMadlulBindingCandidate is frozen (immutable)."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        result = bind_dal_madlul(
            dal, madlul, _dal_registry_proof(), _madlul_registry_proof(),
        )
        assert result.candidate is not None
        with pytest.raises(AttributeError):
            result.candidate.binding_rank = Rank.ZERO  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Carrier schema enforcement
# ---------------------------------------------------------------------------


class TestCarrierSchema:
    """Tests for DalMadlulBindingCandidate carrier schema enforcement."""

    def test_candidate_schema_rejects_invalid_dal(self) -> None:
        """Direct construction with invalid dal_candidate raises."""
        dal = _dal_only_candidate()
        madlul = _madlul_candidate(dal)
        with pytest.raises(WeightCarrierSchemaError):
            DalMadlulBindingCandidate(
                dal_candidate="not valid",  # type: ignore[arg-type]
                madlul_candidate=madlul,
                dal_registry_proof=_dal_registry_proof(),
                madlul_registry_proof=_madlul_registry_proof(),
                binding_rank=Rank.HYPOTHESIS,
                residuals=(),
                trace_ref="test/schema",
            )

    def test_verdict_schema_enforces_bound_state(self) -> None:
        """BOUND verdict without candidate raises WeightCarrierSchemaError."""
        with pytest.raises(WeightCarrierSchemaError):
            DalMadlulBindingVerdict(
                candidate=None,
                verdict_state=BindingState.BOUND,
                failure_code=None,
                verdict_rank=Rank.HYPOTHESIS,
                residuals=(),
                trace_ref="test/invalid",
            )

    def test_verdict_schema_enforces_refused_state(self) -> None:
        """REFUSED verdict without failure_code raises WeightCarrierSchemaError."""
        with pytest.raises(WeightCarrierSchemaError):
            DalMadlulBindingVerdict(
                candidate=None,
                verdict_state=BindingState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.HYPOTHESIS,
                residuals=(),
                trace_ref="test/invalid",
            )
