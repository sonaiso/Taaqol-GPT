"""Constitutional tests for PV-A4: MafhūmClosure.

Origin law: docs/50_MAFHUM_BOUNDARY_LAW.md.

This test module proves:
1. prove_mafhum_closure() returns PROVEN with valid inputs.
2. MafhumClosureCandidate ≠ hukm / tanzil / reality / majaz / naql.
3. Law 1: Reject without closed Mantuq.
4. Law 2: Reject without outside boundary.
5. Law 3: Reject without declared meta-term domain.
6. Law 4: Reject without branch relation (type + qayd).
7. Law 5: Reject unlicensed cross-domain transfer.
8. Law 6: Reject when Mantuq blocks Mafhum.
9. Law 7: Reject hidden/blocking residuals.
10. Law 8: No hukm, tanzil, or reality output.
11. Preserve source Mantuq trace.
12. Preserve branch relation trace.
13. Do not promote rank beyond CANDIDATE.
14. Every verdict carries trace_ref.
15. Sub-carrier has birth guards.
16. PV-A4 does not export forbidden symbols.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.weight import (
    MAFHUM_RANK_CEILING,
    MantuqClosureCandidate,
    MantuqClosureState,
    MantuqClosureVerdict,
    prove_mafhum_closure,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.mafhum_closure import (
    MafhumBranchType,
    MafhumClosureCandidate,
    MafhumClosureState,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

# ===========================================================================
# Forbidden symbols that PV-A4 must NOT export or instantiate.
# ===========================================================================

FORBIDDEN_SYMBOLS = (
    "HukmFromMafhum",
    "TanzilFromMafhum",
    "RealityClaim",
    "MajazVerdict",
    "MajazLicense",
    "NaqlVerdict",
    "NaqlLicense",
    "HaqiqahAttempt",
    "GPTProposer",
    "GeneralEnergyConservationLaw",
    "ConditionsDAG",
    "Certificate",
    "Execution",
    "Fatwa",
    "Qada",
    "FinalAuthority",
)


# ===========================================================================
# Test fixtures — build a valid MantuqClosureVerdict
# ===========================================================================


def _build_mantuq_closure_verdict(
    *,
    state: MantuqClosureState = MantuqClosureState.PROVEN,
    rank: Rank = Rank.CANDIDATE,
) -> MantuqClosureVerdict:
    """Build a valid PROVEN MantuqClosureVerdict for test inputs."""
    deferred_residuals = tuple(
        Residual(
            name=name,
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note=f"deferred: {name}",
        )
        for name in (
            "MAFHUM_NOT_YET_OPENED",
            "MANTUQ_NOT_MAFHUM",
            "MAJAZ_DEFERRED_UNTIL_HAQIQAH_ATTEMPT",
            "HAQIQAH_ATTEMPT_DEFERRED",
            "NAQL_DEFERRED_UNTIL_TRANSFER_GATE",
        )
    )

    candidate = MantuqClosureCandidate(
        ifadah_verdict_ref="prove_ifadah/proven",
        maqam_verdict_ref="prove_maqam/proven",
        mantuq_scope="preserved_explicit_indication",
        spoken_surface_ref="la_taqul_lahuma_uff",
        mantuq_evidence="explicit prohibition of lesser harm",
        closure_scope="sarf_nahw_dalalah",
        rank=rank,
        residuals=deferred_residuals,
        trace_ref="prove_mantuq_closure/proven",
    )

    return MantuqClosureVerdict(
        candidate=candidate,
        verdict_state=state,
        failure_code=None,
        verdict_rank=rank,
        residuals=deferred_residuals,
        trace_ref="prove_mantuq_closure/proven",
    )


def _valid_residuals() -> tuple[Residual, ...]:
    """Build valid residuals for a MafhumClosureCandidate."""
    return (
        Residual(
            name="MAFHUM_MUKHALAFAH_DEFERRED",
            kind=ResidualKind.EXPLANATORY,
            visible=True,
            note="mafhum al-mukhalafah subtypes deferred",
        ),
    )


# ===========================================================================
# §1 — PROVEN path (happy path)
# ===========================================================================


class TestMafhumClosureProven:
    """prove_mafhum_closure() returns PROVEN with valid inputs."""

    def test_proven_muwafaqah(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="prohibition of greater harm",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="prohibition of uff (lesser harm)",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=_valid_residuals(),
        )
        assert verdict.verdict_state is MafhumClosureState.PROVEN
        assert verdict.failure_code is None
        assert verdict.candidate is not None
        assert isinstance(verdict.candidate, MafhumClosureCandidate)
        assert verdict.candidate.branch_type is MafhumBranchType.MUWAFAQAH
        assert verdict.candidate.mantuq_closure_ref == mantuq.trace_ref
        assert verdict.trace_ref == "prove_mafhum_closure/proven"

    def test_proven_mukhalafah(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="grazing camels are not zakatable",
            branch_type=MafhumBranchType.MUKHALAFAH,
            branch_subtype="sifah",
            qayd="sa'imah (grazing) qualifier",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=_valid_residuals(),
        )
        assert verdict.verdict_state is MafhumClosureState.PROVEN
        assert verdict.candidate is not None
        assert verdict.candidate.branch_type is MafhumBranchType.MUKHALAFAH
        assert verdict.candidate.branch_subtype == "sifah"

    def test_proven_preserves_mantuq_trace(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="nahw",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.candidate is not None
        assert verdict.candidate.mantuq_closure_ref == mantuq.trace_ref

    def test_proven_rank_never_exceeds_candidate(self) -> None:
        # MantuqClosureCandidate is itself bounded at CANDIDATE, so the
        # meet of CANDIDATE and MAFHUM_RANK_CEILING is always CANDIDATE.
        mantuq = _build_mantuq_closure_verdict(rank=Rank.CANDIDATE)
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.PROVEN
        assert verdict.candidate is not None
        assert verdict.candidate.rank <= MAFHUM_RANK_CEILING
        assert verdict.verdict_rank <= MAFHUM_RANK_CEILING

    def test_proven_carries_residuals(self) -> None:
        residuals = _valid_residuals()
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=residuals,
        )
        assert verdict.candidate is not None
        assert verdict.candidate.residuals == residuals


# ===========================================================================
# §2 — Law 1: No mafhum before closed Mantuq
# ===========================================================================


class TestLaw1NoMafhumBeforeMantuqClosure:
    """Law 1: MantuqClosureCandidate PROVEN required."""

    def test_reject_non_mantuq_verdict(self) -> None:
        verdict = prove_mafhum_closure(
            mantuq_verdict="not_a_verdict",  # type: ignore[arg-type]
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_BEFORE_MANTUQ_CLOSURE

    def test_reject_mantuq_refused(self) -> None:
        mantuq = MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.REFUSED,
            failure_code=FailureCode.NO_IFADAH,
            verdict_rank=Rank.ZERO,
            residuals=(),
            trace_ref="prove_mantuq_closure/refused/test",
        )
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_BEFORE_MANTUQ_CLOSURE

    def test_reject_mantuq_proven_but_no_candidate(self) -> None:
        mantuq = MantuqClosureVerdict(
            candidate=None,
            verdict_state=MantuqClosureState.PROVEN,
            failure_code=None,
            verdict_rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="prove_mantuq_closure/proven",
        )
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_BEFORE_MANTUQ_CLOSURE


# ===========================================================================
# §3 — Law 2: No outside without defined inside boundary
# ===========================================================================


class TestLaw2NoOutsideBoundary:
    """Law 2: outside_boundary must be non-empty."""

    @pytest.mark.parametrize("boundary", ["", "  ", None])
    def test_reject_empty_outside_boundary(self, boundary: str | None) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary=boundary,  # type: ignore[arg-type]
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_WITHOUT_OUTSIDE_BOUNDARY


# ===========================================================================
# §4 — Law 3: No mafhum without declared source domain
# ===========================================================================


class TestLaw3NoSourceDomain:
    """Law 3: source_domain must be non-empty."""

    @pytest.mark.parametrize("domain", ["", "  ", None])
    def test_reject_empty_source_domain(self, domain: str | None) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain=domain,  # type: ignore[arg-type]
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_WITHOUT_SOURCE_DOMAIN


# ===========================================================================
# §5 — Law 4: No mafhum without branch relation
# ===========================================================================


class TestLaw4NoBranchRelation:
    """Law 4: branch_type and qayd must be valid."""

    def test_reject_invalid_branch_type(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type="invalid",  # type: ignore[arg-type]
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_WITHOUT_BRANCH_RELATION

    @pytest.mark.parametrize("qayd", ["", "  ", None])
    def test_reject_empty_qayd(self, qayd: str | None) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd=qayd,  # type: ignore[arg-type]
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_WITHOUT_BRANCH_RELATION


# ===========================================================================
# §6 — Law 5: No unlicensed cross-domain transfer
# ===========================================================================


class TestLaw5CrossDomainLeap:
    """Law 5: cross-domain transfer detection."""

    def test_reject_sarf_to_nahw_transfer(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="sarf",
            cross_domain_transfer="SARF_TO_NAHW_ROLE_LEAP",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_CROSS_DOMAIN_LEAP

    def test_reject_nahw_to_reality_transfer(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="nahw",
            cross_domain_transfer="NAHW_TO_REALITY_ROLE_LEAP",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.NO_MAFHUM_CROSS_DOMAIN_LEAP

    def test_accept_empty_transfer(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.PROVEN


# ===========================================================================
# §7 — Law 6: No mafhum when Mantuq blocks it
# ===========================================================================


class TestLaw6MantuqBlocks:
    """Law 6: mantuq_blocks flag."""

    def test_reject_when_mantuq_blocks(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUKHALAFAH,
            branch_subtype="sifah",
            qayd="qualifier present",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=True,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.MANTUQ_BLOCKS_MAFHUM

    def test_accept_when_mantuq_allows(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUKHALAFAH,
            branch_subtype="sifah",
            qayd="qualifier present",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.PROVEN


# ===========================================================================
# §8 — Law 7: No mafhum with hidden residuals
# ===========================================================================


class TestLaw7HiddenResiduals:
    """Law 7: residuals must be visible and not blocking."""

    def test_reject_hidden_forbidden_residual(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        bad_residuals = (
            Residual(
                name="SECRET_RESIDUAL",
                kind=ResidualKind.HIDDEN_FORBIDDEN,
                visible=False,
                note="hidden residual",
            ),
        )
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=bad_residuals,
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.MAFHUM_HIDDEN_RESIDUAL

    def test_reject_blocking_residual(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        bad_residuals = (
            Residual(
                name="BLOCKING_ISSUE",
                kind=ResidualKind.BLOCKING,
                visible=True,
                note="blocking residual",
            ),
        )
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=bad_residuals,
        )
        assert verdict.verdict_state is MafhumClosureState.REFUSED
        assert verdict.failure_code is FailureCode.MAFHUM_HIDDEN_RESIDUAL

    def test_accept_explanatory_residual(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        good_residuals = (
            Residual(
                name="DEFERRED_SUBTYPES",
                kind=ResidualKind.EXPLANATORY,
                visible=True,
                note="subtypes deferred",
            ),
        )
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=good_residuals,
        )
        assert verdict.verdict_state is MafhumClosureState.PROVEN


# ===========================================================================
# §9 — Law 8: No hukm or tanzil from mafhum
# ===========================================================================


class TestLaw8NoHukmTanzil:
    """Law 8: MafhumClosureCandidate must not produce hukm or tanzil."""

    def test_candidate_has_no_hukm_field(self) -> None:
        """Candidate dataclass does not carry hukm or tanzil fields."""
        from dataclasses import fields as dc_fields

        field_names = {f.name for f in dc_fields(MafhumClosureCandidate)}
        assert "hukm" not in field_names
        assert "tanzil" not in field_names
        assert "reality" not in field_names
        assert "authority" not in field_names
        assert "certificate" not in field_names

    def test_rank_ceiling_is_candidate(self) -> None:
        """MAFHUM_RANK_CEILING is CANDIDATE — never CERTIFIED/STRONG."""
        assert MAFHUM_RANK_CEILING == Rank.CANDIDATE
        assert MAFHUM_RANK_CEILING < Rank.HYPOTHESIS


# ===========================================================================
# §10 — Rank enforcement
# ===========================================================================


class TestRankEnforcement:
    """Rank never exceeds MAFHUM_RANK_CEILING (CANDIDATE)."""

    def test_rank_ceiling_constant(self) -> None:
        assert MAFHUM_RANK_CEILING is Rank.CANDIDATE

    def test_proven_verdict_rank_bounded(self) -> None:
        # MantuqClosureCandidate ceiling is CANDIDATE, so verdict_rank
        # from prove_mantuq_closure is at most CANDIDATE. The mafhum meet
        # with MAFHUM_RANK_CEILING (also CANDIDATE) stays at CANDIDATE.
        mantuq = _build_mantuq_closure_verdict(rank=Rank.CANDIDATE)
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.verdict_state is MafhumClosureState.PROVEN
        assert verdict.verdict_rank <= MAFHUM_RANK_CEILING

    def test_candidate_rank_bounded(self) -> None:
        mantuq = _build_mantuq_closure_verdict(rank=Rank.CANDIDATE)
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.candidate is not None
        assert verdict.candidate.rank <= MAFHUM_RANK_CEILING


# ===========================================================================
# §11 — Trace
# ===========================================================================


class TestTrace:
    """Every verdict carries trace_ref."""

    def test_proven_trace(self) -> None:
        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.trace_ref
        assert "prove_mafhum_closure" in verdict.trace_ref

    def test_refused_trace(self) -> None:
        verdict = prove_mafhum_closure(
            mantuq_verdict="invalid",  # type: ignore[arg-type]
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )
        assert verdict.trace_ref
        assert "prove_mafhum_closure" in verdict.trace_ref


# ===========================================================================
# §12 — Birth guards (carrier __post_init__)
# ===========================================================================


class TestBirthGuards:
    """MafhumClosureCandidate birth guards refuse ill-formed carriers."""

    def test_reject_empty_mantuq_closure_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MafhumClosureCandidate(
                mantuq_closure_ref="",
                outside_boundary="outside",
                branch_type=MafhumBranchType.MUWAFAQAH,
                branch_subtype="",
                qayd="qayd",
                source_domain="usul",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_reject_empty_outside_boundary(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MafhumClosureCandidate(
                mantuq_closure_ref="ref",
                outside_boundary="",
                branch_type=MafhumBranchType.MUWAFAQAH,
                branch_subtype="",
                qayd="qayd",
                source_domain="usul",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_reject_rank_exceeds_ceiling(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MafhumClosureCandidate(
                mantuq_closure_ref="ref",
                outside_boundary="outside",
                branch_type=MafhumBranchType.MUWAFAQAH,
                branch_subtype="",
                qayd="qayd",
                source_domain="usul",
                rank=Rank.CERTIFICATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_reject_empty_qayd(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MafhumClosureCandidate(
                mantuq_closure_ref="ref",
                outside_boundary="outside",
                branch_type=MafhumBranchType.MUWAFAQAH,
                branch_subtype="",
                qayd="",
                source_domain="usul",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_reject_empty_source_domain(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MafhumClosureCandidate(
                mantuq_closure_ref="ref",
                outside_boundary="outside",
                branch_type=MafhumBranchType.MUWAFAQAH,
                branch_subtype="",
                qayd="qayd",
                source_domain="",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="trace",
            )

    def test_reject_empty_trace_ref(self) -> None:
        with pytest.raises(WeightCarrierSchemaError):
            MafhumClosureCandidate(
                mantuq_closure_ref="ref",
                outside_boundary="outside",
                branch_type=MafhumBranchType.MUWAFAQAH,
                branch_subtype="",
                qayd="qayd",
                source_domain="usul",
                rank=Rank.CANDIDATE,
                residuals=(),
                trace_ref="",
            )


# ===========================================================================
# §13 — Forbidden symbols
# ===========================================================================


class TestForbiddenSymbols:
    """PV-A4 does not export forbidden symbols."""

    def test_mafhum_closure_module_forbidden_symbols(self) -> None:
        source = pathlib.Path(
            "src/taaqqul_slot_geometry/weight/mafhum_closure.py"
        ).read_text()
        tree = ast.parse(source)
        defined_names = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                defined_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_names.add(target.id)
        for forbidden in FORBIDDEN_SYMBOLS:
            assert forbidden not in defined_names, (
                f"Forbidden symbol {forbidden!r} found in mafhum_closure.py"
            )


# ===========================================================================
# §14 — Constitutional chain test cases
# ===========================================================================


class TestConstitutionalChainCases:
    """Constitutional chain tests following docs/12 schema."""

    def test_chain_proven_muwafaqah(self) -> None:
        case = ConstitutionalChainTestCase(
            origin_law="docs/50_MAFHUM_BOUNDARY_LAW.md",
            branch_name="mafhum_closure_proven_muwafaqah",
            constitutional_chain=(
                "MantuqClosureVerdict",
                "MafhumClosureCandidate",
                "MafhumClosureVerdict",
            ),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=None,
            forbidden_outputs=(
                "HukmCandidate",
                "TanzilCandidate",
                "Certificate",
                "RealityClaim",
            ),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
            chain_position="PV-A4",
            origin_law_ref="docs/50_MAFHUM_BOUNDARY_LAW.md#§4",
            branch_of_origin="post-vertical-family-A",
            forbidden_shortcut_assertions=(
                "Mafhum → Hukm",
                "Mafhum → Tanzil",
                "Mafhum → Reality",
            ),
        )

        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=_valid_residuals(),
        )

        result = ConstitutionalChainResult(
            state=ClosureState.MINIMALLY_CLOSED,
            failure_code=None,
            rank=verdict.verdict_rank,
            residual_visibility=all(
                r.visible for r in verdict.residuals
            ),
            trace_present=bool(verdict.trace_ref),
            produced_outputs=frozenset({"MafhumClosureCandidate"}),
        )
        assert_constitutional_case(case, result)

    def test_chain_refused_no_mantuq(self) -> None:
        case = ConstitutionalChainTestCase(
            origin_law="docs/50_MAFHUM_BOUNDARY_LAW.md",
            branch_name="mafhum_closure_refused_no_mantuq",
            constitutional_chain=(
                "MantuqClosureVerdict",
                "MafhumClosureCandidate",
                "MafhumClosureVerdict",
            ),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.NO_MAFHUM_BEFORE_MANTUQ_CLOSURE,
            forbidden_outputs=(
                "MafhumClosureCandidate",
                "HukmCandidate",
                "TanzilCandidate",
            ),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
            chain_position="PV-A4",
            origin_law_ref="docs/50_MAFHUM_BOUNDARY_LAW.md#§4-law1",
            branch_of_origin="post-vertical-family-A",
            forbidden_shortcut_assertions=(
                "Mafhum → Hukm",
                "Evidence → Certainty",
            ),
        )

        verdict = prove_mafhum_closure(
            mantuq_verdict="invalid",  # type: ignore[arg-type]
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="usul",
            cross_domain_transfer="",
            mantuq_blocks=False,
            residuals=(),
        )

        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=verdict.failure_code,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=bool(verdict.trace_ref),
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)

    def test_chain_refused_cross_domain(self) -> None:
        case = ConstitutionalChainTestCase(
            origin_law="docs/50_MAFHUM_BOUNDARY_LAW.md",
            branch_name="mafhum_closure_refused_cross_domain",
            constitutional_chain=(
                "MantuqClosureVerdict",
                "MafhumClosureCandidate",
                "MafhumClosureVerdict",
            ),
            expected_state=ClosureState.BLOCKED,
            expected_failure_code=FailureCode.NO_MAFHUM_CROSS_DOMAIN_LEAP,
            forbidden_outputs=(
                "MafhumClosureCandidate",
                "HukmCandidate",
            ),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
            chain_position="PV-A4",
            origin_law_ref="docs/50_MAFHUM_BOUNDARY_LAW.md#§4-law5",
            branch_of_origin="post-vertical-family-A",
            forbidden_shortcut_assertions=(
                "Sarf → Nahw (unlicensed)",
                "Evidence → Certainty",
            ),
        )

        mantuq = _build_mantuq_closure_verdict()
        verdict = prove_mafhum_closure(
            mantuq_verdict=mantuq,
            outside_boundary="outside",
            branch_type=MafhumBranchType.MUWAFAQAH,
            branch_subtype="",
            qayd="qayd",
            source_domain="sarf",
            cross_domain_transfer="SARF_TO_NAHW_ROLE_LEAP",
            mantuq_blocks=False,
            residuals=(),
        )

        result = ConstitutionalChainResult(
            state=ClosureState.BLOCKED,
            failure_code=verdict.failure_code,
            rank=verdict.verdict_rank,
            residual_visibility=True,
            trace_present=bool(verdict.trace_ref),
            produced_outputs=frozenset(),
        )
        assert_constitutional_case(case, result)
