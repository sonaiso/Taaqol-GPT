"""Acceptance tests for docs/72 POST-B7.1 chain consistency audit.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (LAFZI-B7 closure reconciliation)
Branch         : POST-B7.1 Chain Consistency Audit
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
_DOC_72 = _REPO_ROOT / "docs" / "72_POST_B7_1_CHAIN_CONSISTENCY_AUDIT.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


_ROADMAP_B7_DONE = (
    "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration                 ✓ done"
)
_C_D_HISTORICAL_NOTE = (
    "downstream LAFZI-C* and LAFZI-D* entries remain historical done markers"
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"POST-B7.1 ({branch_note})",
        constitutional_chain=("DAL-A8", "LAFZI-B0", "LAFZI-B7", "POST-B7.1-AUDIT"),
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


def test_docs_72_exists_with_required_sections() -> None:
    _declare("document presence")
    assert _DOC_72.exists(), "docs/72_POST_B7_1_CHAIN_CONSISTENCY_AUDIT.md must exist"

    body = _DOC_72.read_text(encoding="utf-8")
    required_markers = (
        "## §1 Scope and boundary",
        "## §2 Evidence set",
        "## §3 Chain marker status",
        "## §4 Runtime invariant status",
        "## §5 Forbidden reopening matrix",
        "## §6 Post-merge validation record",
        "## §7 Final verdict",
    )
    for marker in required_markers:
        assert marker in body, f"docs/72 missing required section: {marker}"


def test_docs_72_declares_no_runtime_opening() -> None:
    _declare("no runtime opening")
    body = _DOC_72.read_text(encoding="utf-8")

    required_statements = (
        "Scope: documentation/test synchronization only; no runtime opening.",
        "open `WadiMadlulClosed`",
        "reopen `LAFZI-C*` or `LAFZI-D*` runtime paths",
        "POST_B7_1_CHAIN_AUDIT_VERDICT = PASS",
        "runtime_opening: FORBIDDEN_AND_NOT_PRESENT",
    )
    for statement in required_statements:
        assert statement in body, f"docs/72 missing boundary assertion: {statement}"


def test_docs_72_records_b7_done_and_cd_historical_not_reopened() -> None:
    _declare("chain marker status")
    body = _DOC_72.read_text(encoding="utf-8")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert _ROADMAP_B7_DONE in body
    assert _ROADMAP_B7_DONE in roadmap
    assert _ROADMAP_B7_DONE in claude
    assert _C_D_HISTORICAL_NOTE in body
    assert _C_D_HISTORICAL_NOTE in roadmap
    assert "lafzi_c_d_status: HISTORICAL_DONE_NOT_REOPENED" in body


def test_docs_72_records_forbidden_outputs_from_b7_layer() -> None:
    _declare("forbidden outputs")
    body = _DOC_72.read_text(encoding="utf-8")

    required = (
        "LafziMadlulClosed -> WadiMadlulClosed",
        "relation/semantic/ifādah/hukm/reality output from B7 layer",
        "wadi_madlul_closed_from_b7: FORBIDDEN_AND_NOT_PRESENT",
        "semantic_ifadah_hukm_reality_from_b7: FORBIDDEN_AND_NOT_PRESENT",
    )
    for marker in required:
        assert marker in body, f"docs/72 missing forbidden-output marker: {marker}"
