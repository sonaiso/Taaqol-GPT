"""Acceptance tests for G0-C4 ontological classifier.

Origin law     : docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md
Branch         : G0-C4 (ontological classifier from §3 after G0-C3)
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
from taaqqul_slot_geometry.g0_c2_hard_blocker_gates import prove_g0_hard_blocker_gates
from taaqqul_slot_geometry.g0_c3_bounded_epistemic_distance import (
    G0DistanceBand,
    compute_g0_bounded_epistemic_distance,
)
from taaqqul_slot_geometry.g0_c4_ontological_classifier import (
    G0_C4_ALLOWED_OUTPUT,
    G0_C4_RANK_CEILING,
    G0C4ClassifierSchemaError,
    G0OntologicalClassifierState,
    G0OntologicalResidualKind,
    classify_g0_ontological_origin,
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
        branch_name=f"G0-C4 ({branch_note})",
        constitutional_chain=("G0-L0", "G0-C1", "G0-C2", "G0-C3", "G0-C4"),
        chain_position="G0-C4",
        origin_law_ref=(
            "docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md#3-minimum-ontological-matrix"
        ),
        branch_of_origin="G0 reserved successor chain after G0-C3 bounded distance output.",
        forbidden_shortcut_assertions=(
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
        produced_outputs=frozenset({G0_C4_ALLOWED_OUTPUT}),
    )
    assert_constitutional_case(case, result)


def _candidate(
    *,
    ontological_class: OntologicalClass = OntologicalClass.O1,
    d_form: float = 0.0,
    d_wad: float = 0.0,
    d_onto: float = 0.0,
    lexical_truth_status: LexicalTruthStatus = LexicalTruthStatus.ATTESTED,
    epistemic_rank: EpistemicRank = EpistemicRank.E5,
    jamid: bool = True,
    gender: StemGender = StemGender.MASCULINE,
    trace_ref: str = "trace://g0-c4/candidate/001",
) -> BareJamidStemCandidate:
    return BareJamidStemCandidate(
        stem="جبل",
        vocalized="جَبَل",
        size=3,
        pattern="فَعَل",
        has_productive_addition=False,
        jamid=jamid,
        ontological_class=ontological_class,
        entity_rank=EntityRank.INDIVIDUAL,
        gender=gender,
        gender_evidence="lexical assignment",
        epistemic_rank=epistemic_rank,
        lexical_truth_status=lexical_truth_status,
        hard_blockers_passed=("NO_DUAL", "NO_PLURAL"),
        d_form=d_form,
        d_wad=d_wad,
        d_onto=d_onto,
        trace_ref=trace_ref,
    )


def _distance_verdict(candidate: BareJamidStemCandidate) -> object:
    gate = prove_g0_hard_blocker_gates(
        candidate,
        detected_blockers=(),
        trace_ref="trace://g0-c4/gate/passed",
    )
    return compute_g0_bounded_epistemic_distance(
        candidate,
        hard_blocker_verdict=gate,
        trace_ref="trace://g0-c4/distance/input",
    )


def test_g0_c4_classifies_on_full_and_silent_distance_bands() -> None:
    _declare("classified state for full/silent distance bands")

    full_candidate = _candidate(ontological_class=OntologicalClass.O7)
    full_verdict = classify_g0_ontological_origin(
        full_candidate,
        bounded_distance_verdict=_distance_verdict(full_candidate),
        trace_ref="trace://g0-c4/classifier/full",
    )
    assert full_verdict.state is G0OntologicalClassifierState.CLASSIFIED
    assert full_verdict.upstream_distance_state is G0DistanceBand.FULL_REAL_ORIGIN
    assert full_verdict.ontological_class is OntologicalClass.O7
    assert full_verdict.residuals == ()
    assert full_verdict.failure_code is None
    assert full_verdict.rank is G0_C4_RANK_CEILING
    assert full_verdict.output == G0_C4_ALLOWED_OUTPUT

    silent_candidate = _candidate(
        ontological_class=OntologicalClass.O9,
        lexical_truth_status=LexicalTruthStatus.CANDIDATE,
        epistemic_rank=EpistemicRank.E5,
    )
    silent_verdict = classify_g0_ontological_origin(
        silent_candidate,
        bounded_distance_verdict=_distance_verdict(silent_candidate),
        trace_ref="trace://g0-c4/classifier/silent",
    )
    assert silent_verdict.state is G0OntologicalClassifierState.CLASSIFIED
    assert silent_verdict.upstream_distance_state is G0DistanceBand.LICENSED_SILENT_RESIDUAL
    assert silent_verdict.ontological_class is OntologicalClass.O9
    assert silent_verdict.residuals == ()
    assert silent_verdict.failure_code is None


def test_g0_c4_conditional_classification_preserves_visible_residuals() -> None:
    _declare("conditional classification with visible residual")
    candidate = _candidate(
        ontological_class=OntologicalClass.O10,
        d_form=1.0,
        d_wad=0.2,
        d_onto=0.2,
        lexical_truth_status=LexicalTruthStatus.ATTESTED,
        epistemic_rank=EpistemicRank.E4,
    )
    verdict = classify_g0_ontological_origin(
        candidate,
        bounded_distance_verdict=_distance_verdict(candidate),
        trace_ref="trace://g0-c4/classifier/conditional",
    )
    assert verdict.state is G0OntologicalClassifierState.CLASSIFIED
    assert verdict.upstream_distance_state is G0DistanceBand.LICENSED_CONDITIONAL_VISIBLE_RESIDUAL
    assert verdict.ontological_class is OntologicalClass.O10
    assert verdict.failure_code is None
    assert all(not residual.blocking for residual in verdict.residuals)
    assert {residual.kind for residual in verdict.residuals} == {
        G0OntologicalResidualKind.CONDITIONAL_DISTANCE_WITNESS_REQUIRED
    }


def test_g0_c4_defers_or_forbids_from_upstream_distance_state() -> None:
    _declare("deferred and forbidden outcomes from upstream distance state")
    suspended_candidate = _candidate(
        d_form=1.0,
        d_wad=0.2,
        d_onto=0.2,
        lexical_truth_status=LexicalTruthStatus.CANDIDATE,
        epistemic_rank=EpistemicRank.E4,
        jamid=False,
    )
    suspended_verdict = classify_g0_ontological_origin(
        suspended_candidate,
        bounded_distance_verdict=_distance_verdict(suspended_candidate),
        trace_ref="trace://g0-c4/classifier/suspended",
    )
    assert suspended_verdict.state is G0OntologicalClassifierState.DEFERRED
    assert suspended_verdict.upstream_distance_state is G0DistanceBand.SUSPENDED
    assert suspended_verdict.ontological_class is None
    assert suspended_verdict.failure_code is FailureCode.GATE_REQUIRED
    assert all(not residual.blocking for residual in suspended_verdict.residuals)
    assert {residual.kind for residual in suspended_verdict.residuals} == {
        G0OntologicalResidualKind.UPSTREAM_DISTANCE_SUSPENDED
    }

    insufficient_candidate = _candidate(
        d_form=1.0,
        d_wad=1.0,
        d_onto=1.0,
        lexical_truth_status=LexicalTruthStatus.SUSPENDED,
        epistemic_rank=EpistemicRank.E0,
        jamid=False,
        gender=StemGender.COMMON,
    )
    insufficient_verdict = classify_g0_ontological_origin(
        insufficient_candidate,
        bounded_distance_verdict=_distance_verdict(insufficient_candidate),
        trace_ref="trace://g0-c4/classifier/insufficient",
    )
    assert insufficient_verdict.state is G0OntologicalClassifierState.FORBIDDEN
    assert insufficient_verdict.upstream_distance_state is G0DistanceBand.INSUFFICIENT
    assert insufficient_verdict.ontological_class is None
    assert insufficient_verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert any(residual.blocking for residual in insufficient_verdict.residuals)
    assert {residual.kind for residual in insufficient_verdict.residuals} == {
        G0OntologicalResidualKind.UPSTREAM_DISTANCE_INSUFFICIENT
    }


def test_g0_c4_requires_valid_handoff_inputs_and_trace() -> None:
    _declare("schema guards and upstream continuity")
    candidate = _candidate()
    other_candidate = _candidate(trace_ref="trace://g0-c4/candidate/other")

    with pytest.raises(
        G0C4ClassifierSchemaError, match="requires BareJamidStemCandidate"
    ):
        classify_g0_ontological_origin(  # type: ignore[arg-type]
            "not-a-candidate",
            bounded_distance_verdict=_distance_verdict(candidate),
            trace_ref="trace://g0-c4/classifier/bad-candidate",
        )

    with pytest.raises(
        G0C4ClassifierSchemaError, match="bounded_distance_verdict must be G0BoundedDistanceResult"
    ):
        classify_g0_ontological_origin(  # type: ignore[arg-type]
            candidate,
            bounded_distance_verdict="not-a-verdict",
            trace_ref="trace://g0-c4/classifier/bad-verdict",
        )

    with pytest.raises(G0C4ClassifierSchemaError, match="continuity"):
        classify_g0_ontological_origin(
            other_candidate,
            bounded_distance_verdict=_distance_verdict(candidate),
            trace_ref="trace://g0-c4/classifier/bad-continuity",
        )

    with pytest.raises(G0C4ClassifierSchemaError, match="trace_ref"):
        classify_g0_ontological_origin(
            candidate,
            bounded_distance_verdict=_distance_verdict(candidate),
            trace_ref="bad-trace",
        )


def test_docs_14_and_claude_record_g0_c4_done() -> None:
    _declare("chain-state recording")
    body14 = _DOC_14.read_text(encoding="utf-8")
    body_claude = _CLAUDE.read_text(encoding="utf-8")
    assert "G0-C4   Ontological classifier" in body14
    assert "G0-C4\n    Origin" in body14
    assert "Amendment-61 (G0-C4" in body14
    assert "G0-C4   Ontological classifier" in body_claude
    assert "✓ done" in body_claude
