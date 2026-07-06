"""Acceptance tests for docs/76 Phase-2 X0R-E1 admission declaration.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (chain-state truth)
Branch         : X0R-E1-ADMIT (bounded admission declaration)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_76 = _REPO_ROOT / "docs" / "76_PHASE_2_X0R_E1_ADMISSION_DECLARATION.md"
_DOC_75 = _REPO_ROOT / "docs" / "75_PHASE_1_CLOSURE_DECLARATION.md"
_DOC_74 = _REPO_ROOT / "docs" / "74_STATE_TRUTH_AND_LAFZI_TRACE_AUDIT.md"
_DOC_63 = _REPO_ROOT / "docs" / "63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md"


def _declare(branch_note: str) -> None:
    assert _DOC_76.exists(), "docs/76_PHASE_2_X0R_E1_ADMISSION_DECLARATION.md must exist"
    assert _DOC_75.exists(), "docs/75_PHASE_1_CLOSURE_DECLARATION.md must exist"
    assert _DOC_74.exists(), "docs/74_STATE_TRUTH_AND_LAFZI_TRACE_AUDIT.md must exist"
    assert _DOC_63.exists(), "docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md must exist"

    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"X0R-E1-ADMIT ({branch_note})",
        constitutional_chain=("LAFZI-D6", "PHASE-1-CLOSE", "X0R-E1-ADMIT"),
        chain_position="X0R-E1-ADMIT",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md#1-per-step-boundary-summary",
        branch_of_origin="Post Phase-1 bounded closure admission",
        forbidden_shortcut_assertions=(
            "WordCapability -> Truth",
            "WordCapability -> Certainty",
            "WordCapability -> Reality",
            "X0R-E1 admission -> semantic/hukm/truth outputs",
            "X0R-E1 admission -> MGCM runtime",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ParserRuntime",
            "MorphologyRuntime",
            "SyntaxRuntime",
            "SemanticRuntime",
            "Relation",
            "Sentence",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "MGCMRuntime",
        ),
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
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def test_docs_76_exists_and_declares_admission_identity() -> None:
    _declare("document presence and branch identity")
    body = _DOC_76.read_text(encoding="utf-8")
    required_markers = (
        "BRANCH_NAME = X0R-E1-ADMIT",
        "BRANCH_SCOPE = ADMISSION_ONLY",
        "TARGET_RUNTIME_BRANCH = X0R-E1",
        "TARGET_RUNTIME_SCOPE = GENERIC_EUCLIDEAN_LAYER_CONTRACT_CARRIERS_ONLY",
    )
    for marker in required_markers:
        assert marker in body, f"docs/76 missing required marker: {marker}"


def test_docs_76_preserves_phase_continuity_and_law_e0_boundary() -> None:
    _declare("phase continuity and law-e0 boundary")
    body = _DOC_76.read_text(encoding="utf-8")
    doc_75 = _DOC_75.read_text(encoding="utf-8")
    doc_74 = _DOC_74.read_text(encoding="utf-8")

    assert "NEXT_PERMITTED_ACTION = X0R_E1_CARRIER_ONLY_ADMISSION" in doc_75
    assert "next_permitted_action: X0R_E1_CARRIER_ONLY_WHEN_CHAIN_ADMITTED" in doc_74
    assert "LAW-E0` remains law-only" in body


def test_docs_76_keeps_runtime_opening_forbidden_and_not_present() -> None:
    _declare("runtime opening forbidden")
    body = _DOC_76.read_text(encoding="utf-8")
    assert "RUNTIME_OPENING = FORBIDDEN_AND_NOT_PRESENT" in body
    assert "X0R_E1_RUNTIME = NOT_OPENED" in body
    assert "NEXT_PERMITTED_ACTION = X0R_E1_RUNTIME_CARRIER_IMPLEMENTATION_ONLY" in body


def test_docs_76_keeps_x0r_e2_dal_and_mgcm_unopened() -> None:
    _declare("neighbor branches remain deferred")
    body = _DOC_76.read_text(encoding="utf-8")
    for marker in (
        "deferred_neighbors: [X0R-E2, DAL-A2_PLUS, MGCM_L0_PLUS]",
        "`X0R-E2`, `DAL-A2+`, and `MGCM-*` remain unopened in this step.",
        "- `X0R-E2` runtime,",
        "- `DAL-A2+` runtime,",
        "- `MGCM-*` runtime.",
    ):
        assert marker in body, f"docs/76 must keep deferred boundary marker: {marker}"


def test_docs_76_requires_x0r_e1_line_from_docs_63() -> None:
    _declare("x0r-e1 line exists in law-e0 doc")
    doc_63 = _DOC_63.read_text(encoding="utf-8")
    assert "X0R-E1  Generic EuclideanLayerContract carriers   runtime, generic only" in doc_63
