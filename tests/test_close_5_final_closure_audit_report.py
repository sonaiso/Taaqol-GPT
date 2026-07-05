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
        "## §4 Gap register (normalized by `CLOSE-5.1`)",
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


def test_docs_71_gap_register_tracks_close_5_1_normalization() -> None:
    _declare("gap register")
    body = _DOC_71.read_text(encoding="utf-8")
    assert "G-01" in body, "docs/71 must keep a named gap row"
    assert "CLOSE-5 (docs/71 final closure audit report)" in body, (
        "docs/71 gap register must record normalized CLOSE-5 wording"
    )
    assert "G-02" in body, "docs/71 must record PR #169 procedural residual note"


def test_chain_marks_close_6_and_close_6_1_done_with_dal_a8_1_current() -> None:
    _declare("post-close-6 chain marker synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(r"CLOSE-5\s+Final closure audit\s+✓ done", roadmap), (
        "docs/14 must keep CLOSE-5 marked done after CLOSE-6 merge"
    )
    assert re.search(r"CLOSE-6\s+v0\.1\.0 tag \+ closure announcement\s+✓ done", roadmap), (
        "docs/14 must keep CLOSE-6 marked done after PR #173"
    )
    assert re.search(
        r"CLOSE-6\.1\s+Post-merge release-boundary verification \+ admission matrix\s+✓ done",
        roadmap,
    ), (
        "docs/14 must keep CLOSE-6.1 marked done after DAL-A4 runtime opening step"
    )
    assert re.search(r"DAL-A4\s+Hamza / shadda / tanwin / sukun / madd gates\s+✓ done", roadmap), (
        "docs/14 must keep DAL-A4 runtime recorded as done"
    )
    assert re.search(
        r"DAL-A5-ADMIT\s+admission boundary after DAL-A4 runtime\s+✓ done",
        roadmap,
    ), ("docs/14 must keep DAL-A5-ADMIT marked done")
    assert re.search(
        r"DAL-A5\s+Syllable / transition / adjacency / S1-S5 gates\s+✓ done",
        roadmap,
    ), ("docs/14 must keep DAL-A5 runtime marked done")
    assert re.search(
        r"DAL-A6-ADMIT\s+admission boundary after DAL-A5 runtime\s+✓ done",
        roadmap,
    ), ("docs/14 must keep DAL-A6-ADMIT marked done")
    assert re.search(
        r"DAL-A6\s+Detailed waqf / wasl closure\s+✓ done",
        roadmap,
    ), ("docs/14 must keep DAL-A6 marked done")
    assert re.search(
        r"DAL-A7\s+Usage / loan / unvocalized / deletion residual gates\s+✓ done",
        roadmap,
    ), ("docs/14 must keep DAL-A7 marked done after DAL-A7.1 corrective slot")
    assert re.search(
        r"DAL-A7\.1\s+Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics\s+✓ done",
        roadmap,
    ), ("docs/14 must keep DAL-A7.1 marked done after DAL-A8 opening")
    assert re.search(
        r"DAL-A8\s+DalAloneClosed -> LafziMadlulGate integration\s+✓ done",
        roadmap,
    ), ("docs/14 must keep DAL-A8 marked done before DAL-A8.1 corrective step")
    assert re.search(
        r"DAL-A8\.1\s+Harden forbidden-neighbor proof after DAL-A8 merge\s+✓ done",
        roadmap,
    ), ("docs/14 must keep DAL-A8.1 marked done once LAFZI-B0 opens")
    assert re.search(
        r"LAFZI-B0\s+Lafzi Madlul Correspondence Law\s+→ current",
        roadmap,
    ), ("docs/14 must mark LAFZI-B0 as the current chain step")

    assert re.search(r"CLOSE-5\s+Final closure audit\s+✓ done", claude), (
        "CLAUDE.md must keep CLOSE-5 marked done after CLOSE-6 merge"
    )
    assert re.search(r"CLOSE-6\s+v0\.1\.0 tag \+ closure announcement\s+✓ done", claude), (
        "CLAUDE.md must keep CLOSE-6 marked done after PR #173"
    )
    assert re.search(
        r"CLOSE-6\.1\s+Post-merge release-boundary verification \+ admission matrix\s+✓ done",
        claude,
    ), (
        "CLAUDE.md must keep CLOSE-6.1 marked done after DAL-A4 runtime opening step"
    )
    assert re.search(r"DAL-A4\s+Hamza / shadda / tanwin / sukun / madd gates\s+✓ done", claude), (
        "CLAUDE.md must keep DAL-A4 runtime recorded as done"
    )
    assert re.search(
        r"DAL-A5-ADMIT\s+admission boundary after DAL-A4 runtime\s+✓ done",
        claude,
    ), ("CLAUDE.md must keep DAL-A5-ADMIT marked done")
    assert re.search(
        r"DAL-A5\s+Syllable / transition / adjacency / S1-S5 gates\s+✓ done",
        claude,
    ), ("CLAUDE.md must keep DAL-A5 runtime marked done")
    assert re.search(
        r"DAL-A6-ADMIT\s+admission boundary after DAL-A5 runtime\s+✓ done",
        claude,
    ), ("CLAUDE.md must keep DAL-A6-ADMIT marked done")
    assert re.search(
        r"DAL-A6\s+Detailed waqf / wasl closure\s+✓ done",
        claude,
    ), ("CLAUDE.md must keep DAL-A6 marked done")
    assert re.search(
        r"DAL-A7\s+Usage / loan / unvocalized / deletion residual gates\s+✓ done",
        claude,
    ), ("CLAUDE.md must keep DAL-A7 marked done after DAL-A7.1 corrective slot")
    assert re.search(
        r"DAL-A7\.1\s+Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics\s+✓ done",
        claude,
    ), ("CLAUDE.md must keep DAL-A7.1 marked done after DAL-A8 opening")
    assert re.search(
        r"DAL-A8\s+DalAloneClosed -> LafziMadlulGate integration\s+✓ done",
        claude,
    ), ("CLAUDE.md must keep DAL-A8 marked done before DAL-A8.1 corrective step")
    assert re.search(
        r"DAL-A8\.1\s+Harden forbidden-neighbor proof after DAL-A8 merge\s+✓ done",
        claude,
    ), ("CLAUDE.md must keep DAL-A8.1 marked done once LAFZI-B0 opens")
    assert re.search(
        r"LAFZI-B0\s+Lafzi Madlul Correspondence Law.*→ current",
        claude,
    ), ("CLAUDE.md must mark LAFZI-B0 as the current chain step")
