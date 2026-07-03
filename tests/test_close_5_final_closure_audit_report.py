"""Acceptance tests for docs/71 CLOSE-5 final closure audit report.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (CLOSE-5 boundary summary)
Branch         : CLOSE-5 (final closure audit report)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_71 = _REPO_ROOT / "docs" / "71_CLOSE_5_FINAL_CLOSURE_AUDIT_REPORT.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"CLOSE-5 ({branch_note})",
        constitutional_chain=("CLOSE-4", "CLOSE-5", "CLOSE-6-deferred"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "OpenedBranch",
            "ReadinessCertificate",
            "ReleaseTag",
            "ChainTruthOverride",
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


def test_docs_71_exists_and_has_core_sections() -> None:
    _declare("report presence")
    assert _DOC_71.exists(), "docs/71_CLOSE_5_FINAL_CLOSURE_AUDIT_REPORT.md must exist"
    body = _DOC_71.read_text(encoding="utf-8")
    required_markers = (
        "## §1 Scope and boundary",
        "## §2 Evidence set",
        "## §3 Constitutional closure checks",
        "## §4 Gap register (for `CLOSE-5.1` if needed)",
        "## §5 Execution-order verdicts",
        "## §6 Final CLOSE-5 verdict",
    )
    for marker in required_markers:
        assert marker in body, f"docs/71 missing required section: {marker}"


def test_docs_71_records_core_state_assertions() -> None:
    _declare("core state assertions")
    body = _DOC_71.read_text(encoding="utf-8")
    required_statements = (
        "Project objective is constitutional engine (not parser/clone)",
        "Chain status is synchronized (`CLOSE-5` current, `CLOSE-6` planned)",
        "DAL runtime progression remains staged (`DAL-A4..A8` planned)",
        "CLOSE-5_AUDIT_VERDICT = PASS_WITH_CORRECTIVE_NOTE",
    )
    for statement in required_statements:
        assert statement in body, f"docs/71 must include audit statement: {statement}"


def test_docs_71_gap_register_tracks_docs_54_reference_drift() -> None:
    _declare("gap register")
    body = _DOC_71.read_text(encoding="utf-8")
    assert "G-01" in body, "docs/71 must keep a named gap row"
    assert "CLOSE-5 (docs/54 closure audit)" in body, (
        "docs/71 gap register must record historical docs/54 wording drift"
    )


def test_chain_still_marks_close_5_current_and_close_6_planned() -> None:
    _declare("chain marker synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(r"CLOSE-5\\s+Final closure audit\\s+→ current", roadmap), (
        "docs/14 must keep CLOSE-5 as current during CLOSE-5 audit-report step"
    )
    assert re.search(
        r"CLOSE-6\\s+v0\\.1\\.0 tag \\+ closure announcement\\s+planned", roadmap
    ), (
        "docs/14 must keep CLOSE-6 planned during CLOSE-5 audit-report step"
    )

    assert re.search(r"CLOSE-5\\s+Final closure audit\\s+→ current", claude), (
        "CLAUDE.md must keep CLOSE-5 as current during CLOSE-5 audit-report step"
    )
    assert re.search(
        r"CLOSE-6\\s+v0\\.1\\.0 tag \\+ closure announcement\\s+planned", claude
    ), (
        "CLAUDE.md must keep CLOSE-6 planned during CLOSE-5 audit-report step"
    )
