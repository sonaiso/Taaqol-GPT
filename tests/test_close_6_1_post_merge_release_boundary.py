"""Acceptance tests for CLOSE-6.1 post-merge release-boundary verification.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (CLOSE-6.1 verification boundary)
Branch         : CLOSE-6.1 (post-merge release/tag verification + normalization)
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
_README = _REPO_ROOT / "README.md"
_CHANGELOG = _REPO_ROOT / "CHANGELOG.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"CLOSE-6.1 ({branch_note})",
        constitutional_chain=("CLOSE-6", "CLOSE-6.1", "post-close-6-admission"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "OpenedRuntimeBranch",
            "DALA4Activation",
            "FullArabicRuntimeClosureClaim",
            "RankResidualTraceRuntimeMutation",
            "TagReleaseShortcut",
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


def test_close_6_1_verdict_and_runtime_non_opening_are_declared() -> None:
    _declare("verdict surface")
    roadmap = _DOC_14.read_text(encoding="utf-8")

    required = (
        "CLOSE_6_1_VERDICT =",
        "status: POST_MERGE_RELEASE_BOUNDARY_VERIFIED_OR_NORMALIZED",
        "runtime_opening: FORBIDDEN_AND_NOT_PRESENT",
        "full_arabic_linguistic_algebra_runtime_closure: NOT_CLAIMED",
        "latest_completed_arabic_dal_surface: DAL_A3",
        "dal_a4_to_a8: DEFERRED",
        "lafzi_b0_to_b7: DEFERRED",
        "law_e0_metric_runtime: DEFERRED",
        "next_admissible_branch_family: POST_CLOSE_6_BRANCH_ADMISSION_ONLY",
    )
    for marker in required:
        assert marker in roadmap, f"docs/14 missing CLOSE-6.1 marker: {marker}"


def test_close_6_1_gap_matrix_contains_all_required_rows() -> None:
    _declare("gap matrix rows")
    roadmap = _DOC_14.read_text(encoding="utf-8")

    for row in (
        "| 1 | CLOSE-6 release-boundary declaration exists |",
        "| 2 | v0.1.0 tag/release action status is explicit |",
        "| 3 | Chain table is synchronized post-merge |",
        "| 4 | README status is synchronized |",
        "| 5 | CHANGELOG status is synchronized |",
        "| 6 | CLAUDE.md status is synchronized |",
        "| 7 | DAL-A3 remains latest completed Arabic DAL surface |",
        "| 8 | DAL-A4 remains deferred to licensed branch |",
        "| 9 | DAL-A5..A8 remain deferred |",
        "| 10 | LAFZI-B0..B7 remain deferred |",
        "| 11 | LAW-E0 metric/runtime remains deferred |",
        "| 12 | CLOSE-6/CLOSE-6.1 do not open runtime |",
        "| 13 | No full Arabic linguistic algebra runtime closure claim |",
        "| 14 | Next branch opens only through admission matrix |",
    ):
        assert row in roadmap, f"docs/14 CLOSE-6.1 matrix missing row: {row}"


def test_close_6_1_documents_forbidden_runtime_shortcuts() -> None:
    _declare("forbidden shortcuts")
    roadmap = _DOC_14.read_text(encoding="utf-8")

    assert "Implementing DAL-A4 gates in CLOSE-6.1" in roadmap
    assert "Adding runtime carriers/gates/contracts here" in roadmap
    assert "Claiming full algebra runtime closure" in roadmap
    assert "Treating declaration text as completed release operation" in roadmap


def test_close_6_1_status_is_synchronized_across_docs() -> None:
    _declare("cross-doc synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    readme = _README.read_text(encoding="utf-8")
    changelog = _CHANGELOG.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert (
        "CLOSE-6.1 Post-merge release-boundary verification + admission matrix    ✓ done"
        in roadmap
    )
    assert (
        "DAL-A4  Hamza / shadda / tanwin / sukun / madd gates                      ✓ done"
        in roadmap
    )
    assert (
        "DAL-A5-ADMIT admission boundary after DAL-A4 runtime                      ✓ done"
        in roadmap
    )
    assert "current chain step is `DAL-A5` runtime" in readme
    assert "Tag/release execution remains a separate post-merge release action" in readme
    assert "CLOSE-6.1 post-merge release-boundary verification" in changelog
    assert (
        "CLOSE-6.1 Post-merge release-boundary verification + admission matrix      ✓ done"
        in claude
    )
    assert (
        "DAL-A4  Hamza / shadda / tanwin / sukun / madd gates                      ✓ done"
        in claude
    )
    assert (
        "DAL-A5-ADMIT admission boundary after DAL-A4 runtime                      ✓ done"
        in claude
    )
