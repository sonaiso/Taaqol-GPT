"""Acceptance tests for G0-C2 hard-blocker gates.

Origin law     : docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md
Branch         : G0-C2 (hard-blocker gates from §7 only)
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
    G0C2GateSchemaError,
    G0HardBlocker,
    G0HardBlockerGateState,
    G0HardBlockerResidualKind,
    G0_C2_ALLOWED_OUTPUT,
    G0_C2_RANK_CEILING,
    prove_g0_hard_blocker_gates,
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
    "G0BoundedDistanceComputation",
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
        branch_name=f"G0-C2 ({branch_note})",
        constitutional_chain=("G0-L0", "G0-C1", "G0-C2"),
        chain_position="G0-C2",
        origin_law_ref="docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md#7-hard-blockers-applied-before-the-distance",
        branch_of_origin="G0 reserved successor chain after zero-layer law-only covenant.",
        forbidden_shortcut_assertions=(
            "BareJamidStemCandidate -> BoundedDistance",
            "BareJamidStemCandidate -> OntologicalClassifier",
            "BareJamidStemCandidate -> EpistemicRanker",
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
        produced_outputs=frozenset({G0_C2_ALLOWED_OUTPUT}),
    )
    assert_constitutional_case(case, result)


def _candidate() -> BareJamidStemCandidate:
    return BareJamidStemCandidate(
        stem="جبل",
        vocalized="جَبَل",
        size=3,
        pattern="فَعَل",
        has_productive_addition=False,
        jamid=True,
        ontological_class=OntologicalClass.O1,
        entity_rank=EntityRank.INDIVIDUAL,
        gender=StemGender.MASCULINE,
        gender_evidence="lexical assignment",
        epistemic_rank=EpistemicRank.E2,
        lexical_truth_status=LexicalTruthStatus.ATTESTED,
        hard_blockers_passed=("NO_DUAL", "NO_PLURAL"),
        d_form=0.0,
        d_wad=0.0,
        d_onto=0.0,
        trace_ref="trace://g0-c2/candidate/001",
    )


def test_g0_c2_passes_when_no_hard_blocker_is_detected() -> None:
    _declare("passed with clean hard-blocker surface")
    verdict = prove_g0_hard_blocker_gates(
        _candidate(),
        detected_blockers=(),
        trace_ref="trace://g0-c2/gate/passed",
    )
    assert verdict.state is G0HardBlockerGateState.PASSED
    assert verdict.rank is G0_C2_RANK_CEILING
    assert verdict.failure_code is None
    assert verdict.residuals == ()
    assert verdict.output == G0_C2_ALLOWED_OUTPUT


def test_g0_c2_forbids_when_any_non_context_hard_blocker_is_detected() -> None:
    _declare("forbidden on hard blocker")
    verdict = prove_g0_hard_blocker_gates(
        _candidate(),
        detected_blockers=(G0HardBlocker.PLURAL_PRESENT, G0HardBlocker.MAJAZ_REQUIRED),
        trace_ref="trace://g0-c2/gate/forbidden",
    )
    assert verdict.state is G0HardBlockerGateState.FORBIDDEN
    assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert all(residual.blocking for residual in verdict.residuals)
    assert {residual.kind for residual in verdict.residuals} == {
        G0HardBlockerResidualKind.HARD_BLOCKER_PRESENT
    }


def test_g0_c2_defers_on_context_polysemy_only() -> None:
    _declare("deferred on context blocker only")
    verdict = prove_g0_hard_blocker_gates(
        _candidate(),
        detected_blockers=(G0HardBlocker.CONTEXT_POLYSEMY_REQUIRED,),
        trace_ref="trace://g0-c2/gate/deferred",
    )
    assert verdict.state is G0HardBlockerGateState.DEFERRED
    assert verdict.failure_code is FailureCode.GATE_REQUIRED
    assert all(not residual.blocking for residual in verdict.residuals)
    assert {residual.kind for residual in verdict.residuals} == {
        G0HardBlockerResidualKind.CONTEXT_POLYSEMY_DEFERRED
    }


def test_g0_c2_rejects_invalid_inputs_and_duplicate_blockers() -> None:
    _declare("schema guards")
    with pytest.raises(G0C2GateSchemaError, match="requires BareJamidStemCandidate"):
        prove_g0_hard_blocker_gates(  # type: ignore[arg-type]
            candidate="not-a-candidate",
            detected_blockers=(),
            trace_ref="trace://g0-c2/gate/bad-candidate",
        )

    with pytest.raises(G0C2GateSchemaError, match="must not contain duplicates"):
        prove_g0_hard_blocker_gates(
            _candidate(),
            detected_blockers=(G0HardBlocker.DUAL_PRESENT, G0HardBlocker.DUAL_PRESENT),
            trace_ref="trace://g0-c2/gate/duplicates",
        )

    with pytest.raises(G0C2GateSchemaError, match="trace_ref"):
        prove_g0_hard_blocker_gates(
            _candidate(),
            detected_blockers=(),
            trace_ref="bad-trace",
        )


def test_docs_14_and_claude_record_g0_c2_done() -> None:
    _declare("chain-state recording")
    body14 = _DOC_14.read_text(encoding="utf-8")
    body_claude = _CLAUDE.read_text(encoding="utf-8")
    assert "G0-C2   Hard-blocker gates" in body14
    assert "G0-C2\n    Origin" in body14
    assert "Amendment-59 (G0-C2" in body14
    assert "G0-C2   Hard-blocker gates" in body_claude
