"""Acceptance tests for G0-C3 bounded epistemic distance computation.

Origin law     : docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md
Branch         : G0-C3 (bounded distance computation from §6 only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.g0_c1_carriers import (
    BareJamidStemCandidate,
    EntityRank,
    EpistemicRank,
    LexicalTruthStatus,
    OntologicalClass,
    StemGender,
)
from taaqqul_slot_geometry.g0_c2_hard_blocker_gates import (
    G0HardBlocker,
    prove_g0_hard_blocker_gates,
)
from taaqqul_slot_geometry.g0_c3_bounded_epistemic_distance import (
    G0_C3_ALLOWED_OUTPUT,
    G0_C3_RANK_CEILING,
    G0C3DistanceSchemaError,
    G0DistanceBand,
    G0DistanceResidualKind,
    compute_g0_bounded_epistemic_distance,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"

_FORBIDDEN_OUTPUTS = (
    "G0OntologicalClassifier",
    "G0EpistemicRanker",
    "G0AnchorCertificateIssuance",
    "HukmVerdict",
    "TruthCertificate",
    "CertaintyCertificate",
    "RealityClaim",
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md",
        branch_name=f"G0-C3 ({branch_note})",
        constitutional_chain=("G0-L0", "G0-C1", "G0-C2", "G0-C3"),
        chain_position="G0-C3",
        origin_law_ref="docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md#6-bounded-epistemic-distance-law",
        branch_of_origin="G0 reserved successor chain after G0-C2 gate execution.",
        forbidden_shortcut_assertions=(
            "BareJamidStemCandidate -> OntologicalClassifier",
            "BareJamidStemCandidate -> EpistemicRanker",
            "BareJamidStemCandidate -> AnchorCertificateIssuance",
            "BareJamidStemCandidate -> HukmVerdict",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=_FORBIDDEN_OUTPUTS,
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset({G0_C3_ALLOWED_OUTPUT}),
    )
    assert_constitutional_case(case, result)


def _candidate(
    *,
    d_form: float = 0.0,
    d_wad: float = 0.0,
    d_onto: float = 0.0,
    lexical_truth_status: LexicalTruthStatus = LexicalTruthStatus.ATTESTED,
    epistemic_rank: EpistemicRank = EpistemicRank.E5,
    jamid: bool = True,
    gender: StemGender = StemGender.MASCULINE,
) -> BareJamidStemCandidate:
    return BareJamidStemCandidate(
        stem="جبل",
        vocalized="جَبَل",
        size=3,
        pattern="فَعَل",
        has_productive_addition=False,
        jamid=jamid,
        ontological_class=OntologicalClass.O1,
        entity_rank=EntityRank.INDIVIDUAL,
        gender=gender,
        gender_evidence="lexical assignment",
        epistemic_rank=epistemic_rank,
        lexical_truth_status=lexical_truth_status,
        hard_blockers_passed=("NO_DUAL", "NO_PLURAL"),
        d_form=d_form,
        d_wad=d_wad,
        d_onto=d_onto,
        trace_ref="trace://g0-c3/candidate/001",
    )


def _passed_gate() -> object:
    return prove_g0_hard_blocker_gates(
        _candidate(),
        detected_blockers=(),
        trace_ref="trace://g0-c3/gate/passed",
    )


def test_g0_c3_full_real_origin_band() -> None:
    _declare("full real-origin band")
    verdict = compute_g0_bounded_epistemic_distance(
        _candidate(),
        hard_blocker_verdict=_passed_gate(),
        trace_ref="trace://g0-c3/distance/full",
    )
    assert verdict.state is G0DistanceBand.FULL_REAL_ORIGIN
    assert verdict.distance <= 0.10
    assert verdict.failure_code is None
    assert verdict.residuals == ()
    assert verdict.rank is G0_C3_RANK_CEILING
    assert verdict.output == G0_C3_ALLOWED_OUTPUT


def test_g0_c3_conditional_visible_residual_band() -> None:
    _declare("conditional visible residual band")
    verdict = compute_g0_bounded_epistemic_distance(
        _candidate(
            d_form=1.0,
            d_wad=0.2,
            d_onto=0.2,
            lexical_truth_status=LexicalTruthStatus.ATTESTED,
            epistemic_rank=EpistemicRank.E4,
        ),
        hard_blocker_verdict=_passed_gate(),
        trace_ref="trace://g0-c3/distance/conditional",
    )
    assert verdict.state is G0DistanceBand.LICENSED_CONDITIONAL_VISIBLE_RESIDUAL
    assert 0.25 < verdict.distance <= 0.40
    assert verdict.failure_code is None
    assert all(not residual.blocking for residual in verdict.residuals)
    assert {residual.kind for residual in verdict.residuals} == {
        G0DistanceResidualKind.CONDITIONAL_WITNESS_REQUIRED
    }


def test_g0_c3_suspended_and_insufficient_bands() -> None:
    _declare("suspended and insufficient distance bands")
    suspended = compute_g0_bounded_epistemic_distance(
        _candidate(
            d_form=1.0,
            d_wad=0.2,
            d_onto=0.2,
            lexical_truth_status=LexicalTruthStatus.CANDIDATE,
            epistemic_rank=EpistemicRank.E4,
            jamid=False,
        ),
        hard_blocker_verdict=_passed_gate(),
        trace_ref="trace://g0-c3/distance/suspended",
    )
    assert suspended.state is G0DistanceBand.SUSPENDED
    assert 0.40 < suspended.distance <= 0.60
    assert suspended.failure_code is FailureCode.GATE_REQUIRED
    assert all(not residual.blocking for residual in suspended.residuals)
    assert {residual.kind for residual in suspended.residuals} == {
        G0DistanceResidualKind.DISTANCE_SUSPENDED
    }

    insufficient = compute_g0_bounded_epistemic_distance(
        _candidate(
            d_form=1.0,
            d_wad=1.0,
            d_onto=1.0,
            lexical_truth_status=LexicalTruthStatus.SUSPENDED,
            epistemic_rank=EpistemicRank.E0,
            jamid=False,
            gender=StemGender.COMMON,
        ),
        hard_blocker_verdict=_passed_gate(),
        trace_ref="trace://g0-c3/distance/insufficient",
    )
    assert insufficient.state is G0DistanceBand.INSUFFICIENT
    assert insufficient.distance > 0.60
    assert insufficient.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert any(residual.blocking for residual in insufficient.residuals)
    assert {residual.kind for residual in insufficient.residuals} == {
        G0DistanceResidualKind.DISTANCE_INSUFFICIENT
    }


def test_g0_c3_requires_passed_g0_c2_gate_and_valid_inputs() -> None:
    _declare("schema guards and gate continuity")
    deferred_gate = prove_g0_hard_blocker_gates(
        _candidate(),
        detected_blockers=(G0HardBlocker.CONTEXT_POLYSEMY_REQUIRED,),
        trace_ref="trace://g0-c3/gate/deferred-upstream",
    )
    with pytest.raises(G0C3DistanceSchemaError, match="requires PASSED"):
        compute_g0_bounded_epistemic_distance(
            _candidate(),
            hard_blocker_verdict=deferred_gate,
            trace_ref="trace://g0-c3/distance/bad-upstream",
        )

    with pytest.raises(G0C3DistanceSchemaError, match="requires BareJamidStemCandidate"):
        compute_g0_bounded_epistemic_distance(  # type: ignore[arg-type]
            "not-a-candidate",
            hard_blocker_verdict=_passed_gate(),
            trace_ref="trace://g0-c3/distance/bad-candidate",
        )

    with pytest.raises(G0C3DistanceSchemaError, match="trace_ref"):
        compute_g0_bounded_epistemic_distance(
            _candidate(),
            hard_blocker_verdict=_passed_gate(),
            trace_ref="bad-trace",
        )


def test_docs_14_and_claude_record_g0_c3_done() -> None:
    _declare("chain-state recording")
    body14 = _DOC_14.read_text(encoding="utf-8")
    body_claude = _CLAUDE.read_text(encoding="utf-8")
    assert "G0-C3   Bounded epistemic distance computation" in body14
    assert "G0-C3\n    Origin" in body14
    assert "Amendment-60 (G0-C3" in body14
    assert "G0-C3   Bounded epistemic distance computation" in body_claude
