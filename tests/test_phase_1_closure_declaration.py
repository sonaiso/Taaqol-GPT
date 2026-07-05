"""Acceptance tests for docs/75 Phase-1 closure declaration.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (chain-state truth)
Branch         : PHASE-1-CLOSE (bounded declaration)
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
_DOC_75 = _REPO_ROOT / "docs" / "75_PHASE_1_CLOSURE_DECLARATION.md"
_DOC_74 = _REPO_ROOT / "docs" / "74_STATE_TRUTH_AND_LAFZI_TRACE_AUDIT.md"
_DOC_63 = _REPO_ROOT / "docs" / "63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"PHASE-1-CLOSE ({branch_note})",
        constitutional_chain=("LAFZI-D6", "AUDIT-74", "PHASE-1-CLOSE"),
        chain_position="PHASE-1-CLOSE",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md#1-per-step-boundary-summary",
        branch_of_origin="Post-audit bounded phase declaration",
        forbidden_shortcut_assertions=(
            "Phase-1 closure -> MGCM runtime",
            "Phase-1 closure -> semantic runtime",
            "WordCapability -> Relation",
            "WordCapability -> Sentence",
            "WordCapability -> Ifadah",
            "WordCapability -> Hukm",
            "WordCapability -> Truth",
            "WordCapability -> Reality",
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


def test_docs_75_exists_and_declares_three_phases() -> None:
    _declare("document presence and phase anchor")
    assert _DOC_75.exists(), "docs/75_PHASE_1_CLOSURE_DECLARATION.md must exist"

    body = _DOC_75.read_text(encoding="utf-8")
    required_markers = (
        "PHASE_1 = Constitutional + PreSemantic/Lafzi Closure (bounded)",
        "PHASE_2 = Readiness + Carrier Contracts",
        "PHASE_3 = Arabic Linguistic Algebra Runtime",
        "PHASE_1_VERDICT = CLOSED_WITH_BOUNDARIES",
    )
    for marker in required_markers:
        assert marker in body, f"docs/75 missing required marker: {marker}"


def test_docs_75_declares_terminal_output_forbidden_outputs_and_next_action() -> None:
    _declare("terminal boundary and next action")
    body = _DOC_75.read_text(encoding="utf-8")

    assert "PHASE_1_TERMINAL_ALLOWED_OUTPUT = WORD_CAPABILITY" in body
    assert (
        "PHASE_1_FORBIDDEN_OUTPUTS = RELATION, SENTENCE, IFADAH, HUKM, TRUTH, CERTAINTY, REALITY"
        in body
    )
    assert "NEXT_PERMITTED_ACTION = X0R_E1_CARRIER_ONLY_ADMISSION" in body


def test_docs_75_keeps_runtime_opening_forbidden_and_law_e0_planned() -> None:
    _declare("runtime opening remains forbidden")
    body = _DOC_75.read_text(encoding="utf-8")
    doc_74 = _DOC_74.read_text(encoding="utf-8")
    doc_63 = _DOC_63.read_text(encoding="utf-8")

    assert "RUNTIME_OPENING = FORBIDDEN_AND_NOT_PRESENT" in body
    assert "LAW_E0_STATUS = PLANNED_LAW_ONLY" in body
    assert "next_permitted_action: X0R_E1_CARRIER_ONLY_WHEN_CHAIN_ADMITTED" in doc_74
    assert "X0R-E1  Generic EuclideanLayerContract carriers   runtime, generic only" in doc_63


def test_docs_75_does_not_claim_relation_sentence_ifadah_hukm_truth_reality_opening() -> None:
    _declare("no downstream opening claim")
    body = _DOC_75.read_text(encoding="utf-8")

    assert "does **not** open:" in body
    for marker in (
        "relation runtime",
        "sentence runtime",
        "ifādah runtime",
        "hukm/truth/certainty/reality outputs",
        "MGCM runtime",
    ):
        assert marker in body, f"docs/75 must explicitly keep forbidden opening: {marker}"
