"""Acceptance tests for CLOSE-5.1 closure normalization scope.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (CLOSE-5.1 corrective normalization)
Branch         : CLOSE-5.1 (closure wording + procedural residual record)
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
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_71 = _REPO_ROOT / "docs" / "71_CLOSE_5_FINAL_CLOSURE_AUDIT_REPORT.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"CLOSE-5.1 ({branch_note})",
        constitutional_chain=("CLOSE-5", "CLOSE-5.1", "CLOSE-6-deferred"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeBranchOpening",
            "ReleaseTag",
            "ReadinessCertificate",
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


def test_no_docs_54_closure_audit_reference_remains() -> None:
    _declare("docs/54 wording removed")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    report = _DOC_71.read_text(encoding="utf-8")

    assert "CLOSE-5 (docs/54 closure audit)" not in roadmap
    assert "CLOSE-5 (docs/54 closure audit)" not in report
    assert "CLOSE-5 (docs/71 final closure audit report)" in roadmap


def test_pr_169_procedural_residual_is_recorded() -> None:
    _declare("procedural residual recording")
    report = _DOC_71.read_text(encoding="utf-8")

    assert "G-02" in report
    assert "PR #169 bundled DAL-A3-B corrective runtime/law synchronization" in report
    assert "RECORDED_PROCEDURAL_NOTE" in report


def test_close_6_still_not_claimed() -> None:
    _declare("close-6 still deferred")
    report = _DOC_71.read_text(encoding="utf-8")

    assert "`CLOSE-6` release step: **DEFERRED**" in report
    assert "not a release tag" in report


def test_no_runtime_files_touched_scope_claim_remains() -> None:
    _declare("runtime remains closed")
    report = _DOC_71.read_text(encoding="utf-8")

    assert "no new runtime layer" in report
    assert "No runtime mismatch was found in `src/` for this audit." in report
