"""Acceptance tests for G0-C6 anchor issuance and downstream consumption gate.

Origin law     : docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md
Branch         : G0-C6 (anchor issuance + downstream consumption after G0-C5)
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
from taaqqul_slot_geometry.g0_c5_epistemic_ranker import rank_g0_epistemic_origin
from taaqqul_slot_geometry.g0_c6_anchor_gate import (
    G0_C6_CONSUMPTION_OUTPUT,
    G0_C6_ISSUANCE_OUTPUT,
    G0_C6_RANK_CEILING,
    G0AnchorGateState,
    G0AnchorResidualKind,
    G0C6AnchorSchemaError,
    enforce_g0_anchor_consumption,
    issue_g0_anchor_certificate,
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
    "HukmVerdict",
    "TruthCertificate",
    "CertaintyCertificate",
    "RealityClaim",
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md",
        branch_name=f"G0-C6 ({branch_note})",
        constitutional_chain=("G0-L0", "G0-C1", "G0-C2", "G0-C3", "G0-C4", "G0-C5", "G0-C6"),
        chain_position="G0-C6",
        origin_law_ref=(
            "docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md#10-binding-between-g₀-and-later-layers"
        ),
        branch_of_origin="G0 reserved successor chain after G0-C5 ranker output.",
        forbidden_shortcut_assertions=(
            "BareJamidStemCandidate -> HukmVerdict",
            "BareJamidStemCandidate -> TruthCertificate",
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
        produced_outputs=frozenset({G0_C6_ISSUANCE_OUTPUT, G0_C6_CONSUMPTION_OUTPUT}),
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
    trace_ref: str = "trace://g0-c6/candidate/001",
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


def _ranker_verdict(candidate: BareJamidStemCandidate) -> object:
    gate = prove_g0_hard_blocker_gates(
        candidate,
        detected_blockers=(),
        trace_ref="trace://g0-c6/gate/passed",
    )
    distance = compute_g0_bounded_epistemic_distance(
        candidate,
        hard_blocker_verdict=gate,
        trace_ref="trace://g0-c6/distance/input",
    )
    classifier = classify_g0_ontological_origin(
        candidate,
        bounded_distance_verdict=distance,
        trace_ref="trace://g0-c6/classifier/input",
    )
    return rank_g0_epistemic_origin(
        candidate,
        ontological_classifier_verdict=classifier,
        trace_ref="trace://g0-c6/ranker/input",
    )


def test_g0_c6_issues_anchor_and_opens_downstream_on_ranked_input() -> None:
    _declare("anchor issuance and consumption on ranked input")
    candidate = _candidate(epistemic_rank=EpistemicRank.E2)
    issuance = issue_g0_anchor_certificate(
        candidate,
        epistemic_ranker_verdict=_ranker_verdict(candidate),
        trace_ref="trace://g0-c6/issuance/e2",
    )
    assert issuance.state is G0AnchorGateState.ISSUED
    assert issuance.failure_code is None
    assert issuance.rank is G0_C6_RANK_CEILING
    assert issuance.output == G0_C6_ISSUANCE_OUTPUT
    assert issuance.anchor_certificate is not None
    assert issuance.anchor_certificate.stem_key == candidate.stem
    assert issuance.anchor_certificate.source_trace_ref == candidate.trace_ref

    downstream = enforce_g0_anchor_consumption(
        issuance,
        downstream_stage="mufrad-dalalah-admission",
        trace_ref="trace://g0-c6/consumption/e2",
    )
    assert downstream.state is G0AnchorGateState.ISSUED
    assert downstream.output == G0_C6_CONSUMPTION_OUTPUT
    assert downstream.failure_code is None
    assert downstream.anchor_certificate_id == issuance.anchor_certificate.certificate_id


def test_g0_c6_defers_for_upstream_deferred_and_preserves_visible_residuals() -> None:
    _declare("deferred issuance and downstream gate behavior")
    deferred_candidate = _candidate(epistemic_rank=EpistemicRank.E0)
    issuance = issue_g0_anchor_certificate(
        deferred_candidate,
        epistemic_ranker_verdict=_ranker_verdict(deferred_candidate),
        trace_ref="trace://g0-c6/issuance/deferred",
    )
    assert issuance.state is G0AnchorGateState.DEFERRED
    assert issuance.failure_code is FailureCode.GATE_REQUIRED
    assert issuance.anchor_certificate is None
    assert {residual.kind for residual in issuance.residuals} == {
        G0AnchorResidualKind.UPSTREAM_RANKER_DEFERRED
    }

    downstream = enforce_g0_anchor_consumption(
        issuance,
        downstream_stage="mufrad-dalalah-admission",
        trace_ref="trace://g0-c6/consumption/deferred",
    )
    assert downstream.state is G0AnchorGateState.DEFERRED
    assert downstream.failure_code is FailureCode.GATE_REQUIRED
    assert {residual.kind for residual in downstream.residuals} == {
        G0AnchorResidualKind.DOWNSTREAM_CONSUMPTION_DEFERRED
    }


def test_g0_c6_forbids_for_upstream_forbidden_and_blocks_downstream() -> None:
    _declare("forbidden issuance and downstream gate behavior")
    forbidden_candidate = _candidate(epistemic_rank=EpistemicRank.E5)
    issuance = issue_g0_anchor_certificate(
        forbidden_candidate,
        epistemic_ranker_verdict=_ranker_verdict(forbidden_candidate),
        trace_ref="trace://g0-c6/issuance/forbidden",
    )
    assert issuance.state is G0AnchorGateState.FORBIDDEN
    assert issuance.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert issuance.anchor_certificate is None
    assert any(residual.blocking for residual in issuance.residuals)
    assert {residual.kind for residual in issuance.residuals} == {
        G0AnchorResidualKind.UPSTREAM_RANKER_FORBIDDEN
    }

    downstream = enforce_g0_anchor_consumption(
        issuance,
        downstream_stage="mufrad-dalalah-admission",
        trace_ref="trace://g0-c6/consumption/forbidden",
    )
    assert downstream.state is G0AnchorGateState.FORBIDDEN
    assert downstream.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert any(residual.blocking for residual in downstream.residuals)
    assert {residual.kind for residual in downstream.residuals} == {
        G0AnchorResidualKind.DOWNSTREAM_CONSUMPTION_FORBIDDEN
    }


def test_g0_c6_requires_valid_handoff_inputs_and_trace() -> None:
    _declare("schema guards and upstream continuity")
    candidate = _candidate()
    other_candidate = _candidate(trace_ref="trace://g0-c6/candidate/other")

    with pytest.raises(G0C6AnchorSchemaError, match="requires BareJamidStemCandidate"):
        issue_g0_anchor_certificate(  # type: ignore[arg-type]
            "not-a-candidate",
            epistemic_ranker_verdict=_ranker_verdict(candidate),
            trace_ref="trace://g0-c6/issuance/bad-candidate",
        )

    with pytest.raises(
        G0C6AnchorSchemaError,
        match="epistemic_ranker_verdict must be G0EpistemicRankerResult",
    ):
        issue_g0_anchor_certificate(  # type: ignore[arg-type]
            candidate,
            epistemic_ranker_verdict="not-a-verdict",
            trace_ref="trace://g0-c6/issuance/bad-verdict",
        )

    with pytest.raises(G0C6AnchorSchemaError, match="continuity"):
        issue_g0_anchor_certificate(
            other_candidate,
            epistemic_ranker_verdict=_ranker_verdict(candidate),
            trace_ref="trace://g0-c6/issuance/bad-continuity",
        )

    with pytest.raises(G0C6AnchorSchemaError, match="trace_ref"):
        issue_g0_anchor_certificate(
            candidate,
            epistemic_ranker_verdict=_ranker_verdict(candidate),
            trace_ref="bad-trace",
        )

    issuance = issue_g0_anchor_certificate(
        candidate,
        epistemic_ranker_verdict=_ranker_verdict(candidate),
        trace_ref="trace://g0-c6/issuance/good",
    )
    with pytest.raises(G0C6AnchorSchemaError, match="downstream_stage"):
        enforce_g0_anchor_consumption(
            issuance,
            downstream_stage="",
            trace_ref="trace://g0-c6/consumption/bad-stage",
        )


def test_docs_14_and_claude_record_g0_c6_done() -> None:
    _declare("chain-state recording")
    body14 = _DOC_14.read_text(encoding="utf-8")
    body_claude = _CLAUDE.read_text(encoding="utf-8")
    assert "G0-C6   Anchor-certificate issuance + downstream consumption gate" in body14
    assert "G0-C6\n    Origin" in body14
    assert "Amendment-63 (G0-C6" in body14
    assert "G0-C6   Anchor-certificate issuance + downstream consumption gate" in body_claude
    assert "✓ done" in body_claude
