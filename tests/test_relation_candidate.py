"""Constitutional tests for PR-19: Composition / RelationCandidate Boundary.

Origin: docs/32, docs/33_RELATION_CANDIDATE_BOUNDARY_LAW.md, docs/04.

Coverage of the 17 required constitutional tests:

1.  prove_relation_candidate() requires ContractableUnitGeometry (governor).
2.  prove_relation_candidate() requires ContractableUnitGeometry (dependent).
3.  prove_relation_candidate() refuses empty relation_basis.
4.  prove_relation_candidate() refuses empty governor_role_claim.
5.  prove_relation_candidate() refuses empty dependent_role_claim.
6.  prove_relation_candidate() refuses non-admissible governor role.
7.  prove_relation_candidate() refuses blocked governor role.
8.  prove_relation_candidate() refuses non-admissible dependent role.
9.  prove_relation_candidate() refuses blocked dependent role.
10. RelationCandidate is not Meaning.
11. RelationCandidate carries no ifadah/hukm/reality fields.
12. RelationCandidate is not IfadahCandidate / HukmCandidate.
13. Rank is bounded to RELATION_CANDIDATE_RANK_CEILING.
14. Residual governance: HIDDEN_FORBIDDEN refused.
15. Residual governance: BLOCKING refused.
16. trace_ref remains reference, not ledger commit.
17. PR-19 imports/defines no forbidden symbols.
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
    CONTRACTABLE_UNIT_RANK_CEILING,
    RELATION_CANDIDATE_RANK_CEILING,
    BindingState,
    BoundaryEvidence,
    ContractabilityProfile,
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
    RelationCandidate,
    RelationState,
    RelationVerdict,
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
    prove_contractable_unit,
    prove_dal,
    prove_relation_candidate,
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
# Test fixtures — build ContractableUnitGeometry through the lawful chain
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr19-relation-candidate-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr19/kataba", kind="DECLARED_ENTRY"),
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


def _binding_candidate() -> DalMadlulBindingCandidate:
    """Produce a valid DalMadlulBindingCandidate through the lawful chain."""
    dal = _dal_only_candidate()
    madlul = _madlul_candidate(dal)
    result = bind_dal_madlul(dal, madlul, _dal_registry_proof(), _madlul_registry_proof())
    assert result.verdict_state is BindingState.BOUND
    assert result.candidate is not None
    return result.candidate


def _contractable_unit(
    admissible_roles: tuple[str, ...] = ("governor", "dependent"),
    blocked_roles: tuple[str, ...] = ("forbidden_role",),
    residuals: tuple[Residual, ...] | None = None,
) -> ContractableUnitGeometry:
    """Produce a valid ContractableUnitGeometry through the lawful chain.

    If residuals is provided, constructs geometry directly with them
    (bypasses prove_contractable_unit which would refuse HIDDEN/BLOCKING).
    """
    binding = _binding_candidate()
    if residuals is None:
        result = prove_contractable_unit(
            binding_candidate=binding,
            admissible_roles=admissible_roles,
            blocked_roles=blocked_roles,
            path_profile="root_path/kataba",
            word_class_affordance="verbal",
            inflection_affordance="muʿrab",
            derivational_affordance="mushtaqq",
        )
        assert result.verdict_state is ContractableUnitState.PROVEN
        assert result.candidate is not None
        return result.candidate
    else:
        # Build geometry directly with injected residuals for test purposes.
        # This bypasses prove_contractable_unit() to test that
        # prove_relation_candidate() independently checks residuals.
        profile = ContractabilityProfile(
            admissible_roles=admissible_roles,
            blocked_roles=blocked_roles,
            path_profile="root_path/kataba",
            word_class_affordance="verbal",
            inflection_affordance="muʿrab",
            derivational_affordance="mushtaqq",
        )
        return ContractableUnitGeometry(
            binding_candidate=binding,
            unit_identity=binding.dal_candidate.signifier_identity,
            contractability_profile=profile,
            objecthood_rank=RankLattice.meet(
                binding.binding_rank, CONTRACTABLE_UNIT_RANK_CEILING
            ),
            residuals=residuals,
            trace_ref="prove_contractable_unit/proven/test-injected",
        )


def _governor_unit() -> ContractableUnitGeometry:
    """A unit that can serve as governor."""
    return _contractable_unit(
        admissible_roles=("governor", "subject"),
        blocked_roles=("forbidden_role",),
    )


def _dependent_unit() -> ContractableUnitGeometry:
    """A unit that can serve as dependent."""
    return _contractable_unit(
        admissible_roles=("dependent", "object"),
        blocked_roles=("forbidden_role",),
    )


# ---------------------------------------------------------------------------
# 1-5. Input boundary enforcement
# ---------------------------------------------------------------------------


class TestInputBoundary:
    """prove_relation_candidate() refuses invalid inputs."""

    def test_non_geometry_governor_refused(self) -> None:
        """Governor must be ContractableUnitGeometry."""
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor="not a geometry",  # type: ignore[arg-type]
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert result.candidate is None

    def test_non_geometry_dependent_refused(self) -> None:
        """Dependent must be ContractableUnitGeometry."""
        gov = _governor_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent="not a geometry",  # type: ignore[arg-type]
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert result.candidate is None

    def test_empty_relation_basis_refused(self) -> None:
        """Empty relation_basis is refused."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None

    def test_empty_governor_role_claim_refused(self) -> None:
        """Empty governor_role_claim is refused."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None

    def test_empty_dependent_role_claim_refused(self) -> None:
        """Empty dependent_role_claim is refused."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY
        assert result.candidate is None


# ---------------------------------------------------------------------------
# 6-9. Role re-gating enforcement
# ---------------------------------------------------------------------------


class TestRoleReGating:
    """prove_relation_candidate() re-gates role claims independently."""

    def test_governor_role_not_admissible_refused(self) -> None:
        """Governor role not in admissible_roles is refused."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="unknown_role",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert result.candidate is None
        assert "governor_role_not_admissible" in result.trace_ref

    def test_governor_role_blocked_refused(self) -> None:
        """Governor role in blocked_roles is refused even if admissible."""
        # Create a unit with "special" in both admissible and blocked
        unit = _contractable_unit(
            admissible_roles=("governor", "special"),
            blocked_roles=("special",),
        )
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=unit,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="special",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert "governor_role_blocked" in result.trace_ref

    def test_dependent_role_not_admissible_refused(self) -> None:
        """Dependent role not in admissible_roles is refused."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="unknown_role",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert result.candidate is None
        assert "dependent_role_not_admissible" in result.trace_ref

    def test_dependent_role_blocked_refused(self) -> None:
        """Dependent role in blocked_roles is refused even if admissible."""
        gov = _governor_unit()
        unit = _contractable_unit(
            admissible_roles=("dependent", "blocked_dep"),
            blocked_roles=("blocked_dep",),
        )
        result = prove_relation_candidate(
            governor=gov,
            dependent=unit,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="blocked_dep",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
        assert "dependent_role_blocked" in result.trace_ref


# ---------------------------------------------------------------------------
# 10-12. Boundary invariants — relation is not meaning
# ---------------------------------------------------------------------------


class TestBoundaryInvariants:
    """RelationCandidate carries no semantic content."""

    def test_relation_candidate_is_not_meaning(self) -> None:
        """RelationCandidate has no meaning/reference/concept fields."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.COMPOSED
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "meaning")
        assert not hasattr(candidate, "reference")
        assert not hasattr(candidate, "concept")
        assert not hasattr(candidate, "denotation")

    def test_relation_candidate_no_ifadah_hukm_reality(self) -> None:
        """RelationCandidate has no ifadah/hukm/reality fields."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        candidate = result.candidate
        assert candidate is not None
        assert not hasattr(candidate, "ifadah")
        assert not hasattr(candidate, "hukm")
        assert not hasattr(candidate, "reality")
        assert not hasattr(candidate, "truth_value")
        assert not hasattr(candidate, "proposition")

    def test_relation_candidate_is_not_ifadah_or_hukm_candidate(self) -> None:
        """RelationCandidate is neither IfadahCandidate nor HukmCandidate."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        candidate = result.candidate
        assert candidate is not None
        # These types should not exist yet (PR-20 / PR-21)
        assert type(candidate).__name__ == "RelationCandidate"
        assert type(candidate).__name__ != "IfadahCandidate"
        assert type(candidate).__name__ != "HukmCandidate"


# ---------------------------------------------------------------------------
# 13. Rank bounding
# ---------------------------------------------------------------------------


class TestRankBounding:
    """Rank is bounded to RELATION_CANDIDATE_RANK_CEILING."""

    def test_rank_bounded_to_ceiling(self) -> None:
        """Verdict rank ≤ RELATION_CANDIDATE_RANK_CEILING."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.COMPOSED
        assert result.verdict_rank <= RELATION_CANDIDATE_RANK_CEILING

    def test_ceiling_equals_contractable_unit_ceiling(self) -> None:
        """RELATION_CANDIDATE_RANK_CEILING == CONTRACTABLE_UNIT_RANK_CEILING."""
        assert RELATION_CANDIDATE_RANK_CEILING == CONTRACTABLE_UNIT_RANK_CEILING

    def test_relation_rank_is_meet_of_inputs(self) -> None:
        """relation_rank = meet(governor_rank, dependent_rank, ceiling)."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        expected = RankLattice.meet(
            gov.objecthood_rank,
            dep.objecthood_rank,
            RELATION_CANDIDATE_RANK_CEILING,
        )
        assert result.verdict_rank == expected
        assert result.candidate is not None
        assert result.candidate.relation_rank == expected


# ---------------------------------------------------------------------------
# 14-15. Residual governance
# ---------------------------------------------------------------------------


class TestResidualGovernance:
    """HIDDEN_FORBIDDEN and BLOCKING residuals cause refusal."""

    def test_hidden_forbidden_residual_refuses(self) -> None:
        """HIDDEN_FORBIDDEN residual in governor triggers refusal."""
        hidden = Residual(
            name="hidden_test",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=True,
            note="test hidden residual",
        )
        gov = _contractable_unit(
            admissible_roles=("governor",),
            blocked_roles=(),
            residuals=(hidden,),
        )
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.HIDDEN_RESIDUAL
        assert result.candidate is None

    def test_blocking_residual_refuses(self) -> None:
        """BLOCKING residual in dependent triggers refusal."""
        blocking = Residual(
            name="blocking_test",
            kind=ResidualKind.BLOCKING,
            visible=True,
            note="test blocking residual",
        )
        gov = _governor_unit()
        dep = _contractable_unit(
            admissible_roles=("dependent",),
            blocked_roles=(),
            residuals=(blocking,),
        )
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
        assert result.candidate is None


# ---------------------------------------------------------------------------
# 16. Trace governance
# ---------------------------------------------------------------------------


class TestTraceRef:
    """trace_ref is a reference string, not a ledger commit."""

    def test_trace_ref_is_reference(self) -> None:
        """Trace ref is a structured string, never a ledger object."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.COMPOSED
        assert isinstance(result.trace_ref, str)
        assert "prove_relation_candidate/" in result.trace_ref
        assert result.candidate is not None
        assert isinstance(result.candidate.trace_ref, str)


# ---------------------------------------------------------------------------
# 17. Forbidden symbols
# ---------------------------------------------------------------------------


class TestForbiddenImports:
    """PR-19 imports/defines no forbidden symbols."""

    def test_no_forbidden_symbols_in_module(self) -> None:
        """relation_candidate.py must not define forbidden symbols."""
        src = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/relation_candidate.py"
        )
        tree = ast.parse(src.read_text())
        names_defined = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
                names_defined.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names_defined.add(target.id)

        forbidden = {
            "IfadahCandidate",
            "HukmCandidate",
            "TanzilCandidate",
            "SemanticLexicon",
            "DalalahMutabaqah",
            "DalalahTadammun",
            "DalalahIltizam",
            "ExtraLetterLicense",
            "C_Aug",
            "SyntaxRole",
            "TruthValue",
            "Reality",
        }
        found = names_defined & forbidden
        assert not found, f"Forbidden symbols found: {found}"


# ---------------------------------------------------------------------------
# Happy path — successful composition
# ---------------------------------------------------------------------------


class TestHappyPath:
    """Successful composition produces a valid RelationCandidate."""

    def test_successful_composition(self) -> None:
        """prove_relation_candidate() succeeds with valid inputs."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.COMPOSED
        assert result.failure_code is None
        assert result.candidate is not None
        assert result.candidate.governor is gov
        assert result.candidate.dependent is dep
        assert result.candidate.relation_basis == "isnad"
        assert result.candidate.governor_role == "governor"
        assert result.candidate.dependent_role == "dependent"

    def test_relation_candidate_is_frozen(self) -> None:
        """RelationCandidate instances are frozen/immutable."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        candidate = result.candidate
        assert candidate is not None
        with pytest.raises(AttributeError):
            candidate.governor_role = "mutated"  # type: ignore[misc]

    def test_verdict_is_frozen(self) -> None:
        """RelationVerdict instances are frozen/immutable."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        with pytest.raises(AttributeError):
            result.verdict_state = RelationState.REFUSED  # type: ignore[misc]

    def test_residuals_merged_from_both(self) -> None:
        """Merged residuals from governor and dependent are present."""
        non_blocking = Residual(
            name="informational",
            kind=ResidualKind.NON_BLOCKING,
            visible=True,
            note="informational residual",
        )
        gov = _contractable_unit(
            admissible_roles=("governor",),
            blocked_roles=(),
            residuals=(non_blocking,),
        )
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.COMPOSED
        assert non_blocking in result.residuals


# ---------------------------------------------------------------------------
# Carrier schema invariants
# ---------------------------------------------------------------------------


class TestCarrierSchema:
    """Schema validation on RelationCandidate and RelationVerdict."""

    def test_verdict_state_composed_requires_candidate(self) -> None:
        """COMPOSED state requires a non-None candidate."""
        with pytest.raises(WeightCarrierSchemaError):
            RelationVerdict(
                candidate=None,
                verdict_state=RelationState.COMPOSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/invalid",
            )

    def test_verdict_state_refused_requires_failure_code(self) -> None:
        """REFUSED state requires a named FailureCode."""
        with pytest.raises(WeightCarrierSchemaError):
            RelationVerdict(
                candidate=None,
                verdict_state=RelationState.REFUSED,
                failure_code=None,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/invalid",
            )

    def test_verdict_state_refused_rejects_candidate(self) -> None:
        """REFUSED state must have candidate=None."""
        gov = _governor_unit()
        dep = _dependent_unit()
        # Get a valid candidate first
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        candidate = result.candidate
        assert candidate is not None
        with pytest.raises(WeightCarrierSchemaError):
            RelationVerdict(
                candidate=candidate,
                verdict_state=RelationState.REFUSED,
                failure_code=FailureCode.GATE_REQUIRED,
                verdict_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/invalid",
            )

    def test_relation_candidate_rejects_invalid_governor(self) -> None:
        """RelationCandidate __post_init__ rejects non-geometry governor."""
        with pytest.raises(WeightCarrierSchemaError):
            RelationCandidate(
                governor="not_geometry",  # type: ignore[arg-type]
                dependent=_dependent_unit(),
                relation_basis="isnad",
                governor_role="governor",
                dependent_role="dependent",
                relation_rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="test/invalid",
            )


# ---------------------------------------------------------------------------
# ContractabilityProfile ≠ SyntaxRole enforcement
# ---------------------------------------------------------------------------


class TestProfileIsNotSyntaxRole:
    """ContractabilityProfile strings are affordance, not final syntax."""

    def test_roles_are_regated_not_inherited(self) -> None:
        """RelationCandidate re-gates roles; does not blindly copy from profile."""
        gov = _governor_unit()
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="governor",
            dependent_role_claim="dependent",
        )
        candidate = result.candidate
        assert candidate is not None
        # The role is set by re-gating, not by assignment
        assert candidate.governor_role == "governor"
        assert candidate.dependent_role == "dependent"
        # The candidate does NOT have a syntax_role field
        assert not hasattr(candidate, "syntax_role")
        assert not hasattr(candidate, "final_role")

    def test_non_admissible_role_blocked_even_if_valid_string(self) -> None:
        """A valid string is still rejected if not in admissible_roles."""
        gov = _contractable_unit(
            admissible_roles=("governor",),
            blocked_roles=(),
        )
        dep = _dependent_unit()
        result = prove_relation_candidate(
            governor=gov,
            dependent=dep,
            relation_basis="isnad",
            governor_role_claim="subject",  # Not in admissible_roles
            dependent_role_claim="dependent",
        )
        assert result.verdict_state is RelationState.REFUSED
        assert result.failure_code is FailureCode.GATE_REQUIRED
