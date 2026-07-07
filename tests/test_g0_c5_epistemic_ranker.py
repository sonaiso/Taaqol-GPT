"""Acceptance tests for G0-C5 epistemic ranker.

Origin law     : docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md
Branch         : G0-C5 (epistemic ranker from §4 after G0-C4)
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
    compute_g0_bounded_epistemic_distance,
)
from taaqqul_slot_geometry.g0_c4_ontological_classifier import classify_g0_ontological_origin
from taaqqul_slot_geometry.g0_c5_epistemic_ranker import (
    G0_C5_ALLOWED_OUTPUT,
    G0_C5_RANK_CEILING,
    G0C5RankerSchemaError,
    G0EpistemicRankerState,
    G0EpistemicResidualKind,
    rank_g0_epistemic_origin,
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
    "G0AnchorCertificateIssuance",
    "HukmVerdict",
    "TruthCertificate",
    "CertaintyCertificate",
    "RealityClaim",
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md",
        branch_name=f"G0-C5 ({branch_note})",
        constitutional_chain=("G0-L0", "G0-C1", "G0-C2", "G0-C3", "G0-C4", "G0-C5"),
        chain_position="G0-C5",
        origin_law_ref=(
            "docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md#4-epistemic-classification-evidence-strength"
        ),
        branch_of_origin="G0 reserved successor chain after G0-C4 classifier output.",
        forbidden_shortcut_assertions=(
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
        produced_outputs=frozenset({G0_C5_ALLOWED_OUTPUT}),
    )
    assert_constitutional_case(case, result)


def _candidate(
    *,
    ontological_class: OntologicalClass = OntologicalClass.O1,
    d_form: float = 0.0,
    d_wad: float = 0.0,
    d_onto: float = 0.0,
    lexical_truth_status: LexicalTruthStatus = LexicalTruthStatus.ATTESTED,
    epistemic_rank: EpistemicRank = EpistemicRank.E2,
    jamid: bool = True,
    gender: StemGender = StemGender.MASCULINE,
    trace_ref: str = "trace://g0-c5/candidate/001",
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


def _classifier_verdict(candidate: BareJamidStemCandidate) -> object:
    gate = prove_g0_hard_blocker_gates(
        candidate,
        detected_blockers=(),
        trace_ref="trace://g0-c5/gate/passed",
    )
    distance = compute_g0_bounded_epistemic_distance(
        candidate,
        hard_blocker_verdict=gate,
        trace_ref="trace://g0-c5/distance/input",
    )
    return classify_g0_ontological_origin(
        candidate,
        bounded_distance_verdict=distance,
        trace_ref="trace://g0-c5/classifier/input",
    )


def test_g0_c5_ranks_e1_e2_and_e3_with_visible_residuals() -> None:
    _declare("ranked outputs from classified upstream")

    e2_candidate = _candidate(epistemic_rank=EpistemicRank.E2)
    e2_verdict = rank_g0_epistemic_origin(
        e2_candidate,
        ontological_classifier_verdict=_classifier_verdict(e2_candidate),
        trace_ref="trace://g0-c5/ranker/e2",
    )
    assert e2_verdict.state is G0EpistemicRankerState.RANKED
    assert e2_verdict.epistemic_rank is EpistemicRank.E2
    assert e2_verdict.residuals == ()
    assert e2_verdict.failure_code is None
    assert e2_verdict.rank is G0_C5_RANK_CEILING
    assert e2_verdict.output == G0_C5_ALLOWED_OUTPUT

    e3_candidate = _candidate(
        epistemic_rank=EpistemicRank.E3,
    )
    e3_verdict = rank_g0_epistemic_origin(
        e3_candidate,
        ontological_classifier_verdict=_classifier_verdict(e3_candidate),
        trace_ref="trace://g0-c5/ranker/e3",
    )
    assert e3_verdict.state is G0EpistemicRankerState.RANKED
    assert e3_verdict.epistemic_rank is EpistemicRank.E3
    assert all(not residual.blocking for residual in e3_verdict.residuals)
    assert {residual.kind for residual in e3_verdict.residuals} == {
        G0EpistemicResidualKind.REAL_MULTIPLICITY_UNDECIDED_E3,
    }

    conditional_candidate = _candidate(
        epistemic_rank=EpistemicRank.E2,
        d_form=0.8,
        d_wad=0.2,
        d_onto=0.2,
        lexical_truth_status=LexicalTruthStatus.ATTESTED,
    )
    conditional_verdict = rank_g0_epistemic_origin(
        conditional_candidate,
        ontological_classifier_verdict=_classifier_verdict(conditional_candidate),
        trace_ref="trace://g0-c5/ranker/conditional",
    )
    assert conditional_verdict.state is G0EpistemicRankerState.RANKED
    assert all(not residual.blocking for residual in conditional_verdict.residuals)
    assert {residual.kind for residual in conditional_verdict.residuals} == {
        G0EpistemicResidualKind.UPSTREAM_CLASSIFIER_CONDITIONAL,
    }


def test_g0_c5_defers_for_e0_e4_and_upstream_deferred() -> None:
    _declare("deferred outcomes from E0/E4 and deferred upstream")

    e0_candidate = _candidate(epistemic_rank=EpistemicRank.E0)
    e0_verdict = rank_g0_epistemic_origin(
        e0_candidate,
        ontological_classifier_verdict=_classifier_verdict(e0_candidate),
        trace_ref="trace://g0-c5/ranker/e0",
    )
    assert e0_verdict.state is G0EpistemicRankerState.DEFERRED
    assert e0_verdict.failure_code is FailureCode.GATE_REQUIRED
    assert {residual.kind for residual in e0_verdict.residuals} == {
        G0EpistemicResidualKind.NOMINATION_ONLY_E0
    }

    e4_candidate = _candidate(epistemic_rank=EpistemicRank.E4)
    e4_verdict = rank_g0_epistemic_origin(
        e4_candidate,
        ontological_classifier_verdict=_classifier_verdict(e4_candidate),
        trace_ref="trace://g0-c5/ranker/e4",
    )
    assert e4_verdict.state is G0EpistemicRankerState.DEFERRED
    assert e4_verdict.failure_code is FailureCode.GATE_REQUIRED
    assert {residual.kind for residual in e4_verdict.residuals} == {
        G0EpistemicResidualKind.INSUFFICIENT_WITNESS_E4
    }

    deferred_candidate = _candidate(epistemic_rank=EpistemicRank.E2, jamid=False)
    deferred_upstream_verdict = rank_g0_epistemic_origin(
        deferred_candidate,
        ontological_classifier_verdict=_classifier_verdict(deferred_candidate),
        trace_ref="trace://g0-c5/ranker/upstream-deferred",
    )
    assert deferred_upstream_verdict.state is G0EpistemicRankerState.DEFERRED
    assert deferred_upstream_verdict.failure_code is FailureCode.GATE_REQUIRED
    assert {residual.kind for residual in deferred_upstream_verdict.residuals} == {
        G0EpistemicResidualKind.UPSTREAM_CLASSIFIER_DEFERRED
    }


def test_g0_c5_forbids_for_e5_and_upstream_forbidden() -> None:
    _declare("forbidden outcomes from E5 and forbidden upstream")

    e5_candidate = _candidate(epistemic_rank=EpistemicRank.E5)
    e5_verdict = rank_g0_epistemic_origin(
        e5_candidate,
        ontological_classifier_verdict=_classifier_verdict(e5_candidate),
        trace_ref="trace://g0-c5/ranker/e5",
    )
    assert e5_verdict.state is G0EpistemicRankerState.FORBIDDEN
    assert e5_verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert any(residual.blocking for residual in e5_verdict.residuals)
    assert {residual.kind for residual in e5_verdict.residuals} == {
        G0EpistemicResidualKind.CONTEXT_OR_TRANSFER_REQUIRED_E5
    }

    forbidden_candidate = _candidate(
        epistemic_rank=EpistemicRank.E2,
        d_form=1.0,
        d_wad=1.0,
        d_onto=1.0,
        lexical_truth_status=LexicalTruthStatus.SUSPENDED,
        jamid=False,
        gender=StemGender.COMMON,
    )
    forbidden_upstream_verdict = rank_g0_epistemic_origin(
        forbidden_candidate,
        ontological_classifier_verdict=_classifier_verdict(forbidden_candidate),
        trace_ref="trace://g0-c5/ranker/upstream-forbidden",
    )
    assert forbidden_upstream_verdict.state is G0EpistemicRankerState.FORBIDDEN
    assert forbidden_upstream_verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert any(residual.blocking for residual in forbidden_upstream_verdict.residuals)
    assert {residual.kind for residual in forbidden_upstream_verdict.residuals} == {
        G0EpistemicResidualKind.UPSTREAM_CLASSIFIER_FORBIDDEN
    }


def test_g0_c5_requires_valid_handoff_inputs_and_trace() -> None:
    _declare("schema guards and upstream continuity")
    candidate = _candidate()
    other_candidate = _candidate(trace_ref="trace://g0-c5/candidate/other")

    with pytest.raises(G0C5RankerSchemaError, match="requires BareJamidStemCandidate"):
        rank_g0_epistemic_origin(  # type: ignore[arg-type]
            "not-a-candidate",
            ontological_classifier_verdict=_classifier_verdict(candidate),
            trace_ref="trace://g0-c5/ranker/bad-candidate",
        )

    with pytest.raises(
        G0C5RankerSchemaError,
        match="ontological_classifier_verdict must be G0OntologicalClassifierResult",
    ):
        rank_g0_epistemic_origin(  # type: ignore[arg-type]
            candidate,
            ontological_classifier_verdict="not-a-verdict",
            trace_ref="trace://g0-c5/ranker/bad-verdict",
        )

    with pytest.raises(G0C5RankerSchemaError, match="continuity"):
        rank_g0_epistemic_origin(
            other_candidate,
            ontological_classifier_verdict=_classifier_verdict(candidate),
            trace_ref="trace://g0-c5/ranker/bad-continuity",
        )

    with pytest.raises(G0C5RankerSchemaError, match="trace_ref"):
        rank_g0_epistemic_origin(
            candidate,
            ontological_classifier_verdict=_classifier_verdict(candidate),
            trace_ref="bad-trace",
        )


def test_docs_14_and_claude_record_g0_c5_done() -> None:
    _declare("chain-state recording")
    body14 = _DOC_14.read_text(encoding="utf-8")
    body_claude = _CLAUDE.read_text(encoding="utf-8")
    assert "G0-C5   Epistemic ranker" in body14
    assert "G0-C5\n    Origin" in body14
    assert "Amendment-62 (G0-C5" in body14
    assert "G0-C5   Epistemic ranker" in body_claude
    assert "✓ done" in body_claude
