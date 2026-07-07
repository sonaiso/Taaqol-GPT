"""Acceptance tests for docs/74 state-truth and LAFZI trace audit.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (chain-state truth)
Branch         : STATE-TRUTH + LAFZI TRACE AUDIT
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_74 = _REPO_ROOT / "docs" / "74_STATE_TRUTH_AND_LAFZI_TRACE_AUDIT.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_README = _REPO_ROOT / "README.md"
_CHANGELOG = _REPO_ROOT / "CHANGELOG.md"
_LAFZI_B = _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "lafzi_madlul.py"
_LAFZI_B7 = (
    _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "lafzi_b7_integration.py"
)
_COUPLED_D = _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "coupled_dalalah.py"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"STATE-TRUTH-LAFZI-TRACE ({branch_note})",
        constitutional_chain=("LAFZI-B7", "LAFZI-C8", "LAFZI-D6", "AUDIT-74"),
        chain_position="AUDIT-74",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md#1-per-step-boundary-summary",
        branch_of_origin="Post-LAFZI closure audit lineage",
        forbidden_shortcut_assertions=(
            "WordCapability → Relation",
            "WordCapability → Sentence",
            "WordCapability → Ifadah",
            "WordCapability → Hukm",
            "WordCapability → Truth",
            "WordCapability → Reality",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeCarrierMutation",
            "RuntimeGateMutation",
            "Relation",
            "Sentence",
            "Ifadah",
            "Hukm",
            "Truth",
            "Reality",
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


def test_docs_74_exists_with_required_sections_and_final_verdict() -> None:
    _declare("document presence")
    assert _DOC_74.exists(), "docs/74_STATE_TRUTH_AND_LAFZI_TRACE_AUDIT.md must exist"

    body = _DOC_74.read_text(encoding="utf-8")
    required_markers = (
        "## §1 Scope and boundary",
        "## §2 State-truth synchronization verdict",
        "## §3 LAFZI-B1..B7 proof map (Trace Audit)",
        "## §4 LAFZI-C/D closure evidence after B7",
        "## §5 Explicit negative proof (no jump after WordCapability)",
        "## §6 LAW-E0 status truth",
        "## §7 Final verdict",
        "STATE_TRUTH_LAFZI_TRACE_AUDIT_VERDICT = PASS_WITH_CORRECTIVE_NOTE",
    )
    for marker in required_markers:
        assert marker in body, f"docs/74 missing required marker: {marker}"


def test_state_truth_sync_removes_stale_readme_markers_and_aligns_law_e0() -> None:
    _declare("state-truth synchronization")
    body = _DOC_74.read_text(encoding="utf-8")
    readme = _README.read_text(encoding="utf-8")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")
    changelog = _CHANGELOG.read_text(encoding="utf-8")

    assert "PASS_WITH_CORRECTIVE_NOTE" in body
    assert "DAL-A5 current" not in readme
    assert "LAFZI-B0..B7, LAW-E0 runtime" not in readme
    assert "`LAW-E0` is **✓ done (law-only)**" in readme
    assert re.search(r"LAW-E0\s+Arabic Euclidean Layer Contract Law\s+✓ done", roadmap)
    assert re.search(r"LAW-E0\s+Arabic Euclidean Layer Contract Law\s+✓ done", claude)
    assert "state-truth synchronization + LAFZI trace audit" in changelog


def test_b7_trace_map_explicitly_distinguishes_b1_b6_from_b7_integration() -> None:
    _declare("b7 trace mapping")
    body = _DOC_74.read_text(encoding="utf-8")
    lafzi_b = _LAFZI_B.read_text(encoding="utf-8")
    lafzi_b7 = _LAFZI_B7.read_text(encoding="utf-8")

    assert "LAFZI-B1..B6" in lafzi_b.splitlines()[0]
    assert "LAFZI-B7" in body
    assert "weight/lafzi_b7_integration.py" in body
    assert "prove_lafzi_madlul_closed" in body
    assert "def prove_lafzi_madlul_closed(" in lafzi_b7


def test_cd_closure_and_negative_wordcapability_jump_are_explicit() -> None:
    _declare("c/d closure and no-jump proof")
    body = _DOC_74.read_text(encoding="utf-8")
    coupled = _COUPLED_D.read_text(encoding="utf-8")

    assert "LAFZI-C8" in body
    assert "LAFZI-D1..D6" in body
    assert "NO_WORDCAPABILITY_TO_RELATION_SENTENCE_IFADAH_HUKM_TRUTH = PASS" in body
    assert 'LAFZI_D6_ALLOWED_OUTPUT: str = "WORD_CAPABILITY"' in coupled
    for forbidden in ("RELATION", "SENTENCE", "IFADAH", "HUKM", "TRUTH_VALUE"):
        assert forbidden in coupled
