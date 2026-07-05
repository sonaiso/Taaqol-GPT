"""Acceptance tests for docs/73 POST-B7-COMPAT-0 compatibility audit.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (LAFZI-B7 closure marker)
Branch         : POST-B7-COMPAT-0 Compatibility Audit
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_73 = _REPO_ROOT / "docs" / "73_POST_B7_COMPAT_0_COMPATIBILITY_AUDIT.md"
_DOC_72 = _REPO_ROOT / "docs" / "72_POST_B7_1_CHAIN_CONSISTENCY_AUDIT.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_B7_INTEGRATION = (
    _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "lafzi_b7_integration.py"
)

_ROADMAP_B7_DONE = (
    "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration                 ✓ done"
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"POST-B7-COMPAT-0 ({branch_note})",
        constitutional_chain=("DAL-A8", "LAFZI-B0", "LAFZI-B7", "POST-B7-COMPAT-0-AUDIT"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "WadiMadlulClosed",
            "ReopenedLAFZI_C",
            "ReopenedLAFZI_D",
            "Relation",
            "Ifadah",
            "Hukm",
            "Reality",
            "RuntimeCarrierMutation",
            "RuntimeGateMutation",
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


def test_docs_73_exists_with_required_sections() -> None:
    _declare("document presence")
    assert _DOC_73.exists(), "docs/73_POST_B7_COMPAT_0_COMPATIBILITY_AUDIT.md must exist"

    body = _DOC_73.read_text(encoding="utf-8")
    required_markers = (
        "## §1 Scope and boundary",
        "## §2 Evidence set",
        "## §3 Chain compatibility status",
        "## §4 Runtime surface compatibility invariants",
        "## §5 Forbidden compatibility breaches",
        "## §6 Post-merge validation record",
        "## §7 Final verdict",
    )
    for marker in required_markers:
        assert marker in body, f"docs/73 missing required section: {marker}"


def test_docs_73_declares_audit_only_no_runtime_opening() -> None:
    _declare("audit-only boundary")
    body = _DOC_73.read_text(encoding="utf-8")
    required_statements = (
        "Scope: documentation/test/code-surface compatibility verification only; "
        "no runtime opening.",
        "POST_B7_COMPAT_0_AUDIT_VERDICT = PASS",
        "runtime_opening: FORBIDDEN_AND_NOT_PRESENT",
        "next_permitted_action: AUDIT_ONLY_COMPATIBILITY_MAINTENANCE",
    )
    for statement in required_statements:
        assert statement in body, f"docs/73 missing boundary assertion: {statement}"


def test_docs_73_records_b7_chain_marker_compatibility() -> None:
    _declare("chain marker compatibility")
    body = _DOC_73.read_text(encoding="utf-8")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert _ROADMAP_B7_DONE in body
    assert _ROADMAP_B7_DONE in roadmap
    assert _ROADMAP_B7_DONE in claude
    assert "lafzi_b7_marker_status: SYNCHRONIZED_DONE" in body
    assert "lafzi_cd_reopening: FORBIDDEN_AND_NOT_PRESENT" in body


def test_docs_73_anchors_compatibility_to_b7_surface_and_post_b7_1() -> None:
    _declare("surface compatibility evidence")
    body = _DOC_73.read_text(encoding="utf-8")
    post_b7_1 = _DOC_72.read_text(encoding="utf-8")
    b7_runtime = _B7_INTEGRATION.read_text(encoding="utf-8")

    required_body_markers = (
        "/home/runner/work/Taaqol-GPT/Taaqol-GPT/docs/72_POST_B7_1_CHAIN_CONSISTENCY_AUDIT.md",
        "output is fixed to `LAFZI_MADLUL_CLOSED_RESULT`",
        "handoff state remains `OPENED_BOUNDARY_ONLY`",
        "`WADI_MADLUL_CLOSED` remains forbidden",
        "WadiMadlulClosed",
    )
    for marker in required_body_markers:
        assert marker in body, f"docs/73 missing compatibility marker: {marker}"

    assert "next_permitted_action: COMPATIBILITY_AUDIT_PLANNING_ONLY" in post_b7_1
    assert "LAFZI_B7_ALLOWED_OUTPUT: str = \"LAFZI_MADLUL_CLOSED_RESULT\"" in b7_runtime
    assert "WadiMadlulGateState" in b7_runtime
    assert "OPENED_BOUNDARY_ONLY" in b7_runtime
    assert "WADI_MADLUL_CLOSED" in b7_runtime
