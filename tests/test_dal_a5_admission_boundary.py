"""DAL-A5 admission-only boundary tests.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (DAL-A5-ADMIT admission-only step)
Branch         : DAL-A5-ADMIT (post-DAL-A4 runtime admission decision)
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
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"DAL-A5-ADMIT ({branch_note})",
        constitutional_chain=("DAL-A4", "DAL-A5-ADMIT", "DAL-A5"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "DALA5RuntimeOpening",
            "SyllableRuntimeCertificate",
            "AdjacencyRuntimeDecision",
            "SemanticOrHukmOutput",
            "GreenCIShortcut",
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


def test_dal_a5_admission_marks_dal_a4_runtime_done() -> None:
    _declare("dal-a4 done + dal-a5-admit done")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert (
        "DAL-A4  Hamza / shadda / tanwin / sukun / madd gates                      ✓ done"
        in roadmap
    )
    assert (
        "DAL-A5-ADMIT admission boundary after DAL-A4 runtime                      ✓ done"
        in roadmap
    )
    assert (
        "DAL-A4  Hamza / shadda / tanwin / sukun / madd gates                      ✓ done"
        in claude
    )
    assert (
        "DAL-A5-ADMIT admission boundary after DAL-A4 runtime                      ✓ done"
        in claude
    )


def test_admission_verdict_remains_admitted_only_boundary_record() -> None:
    _declare("admission verdict remains historical boundary record")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    assert "DAL_A5_ADMISSION_VERDICT" in roadmap
    assert "dal_a5_runtime_status: DEFERRED" in roadmap
    assert "runtime_certificate: NOT_PRODUCED" in roadmap


def test_admission_keeps_dal_a6_to_a8_deferred() -> None:
    _declare("dal-a6..a8 deferred")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for marker in (
        "DAL-A6  Detailed waqf / wasl closure                                      ✓ done",
        "DAL-A7  Usage / loan / unvocalized / deletion residual gates              ✓ done",
        "DAL-A7.1 Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics          ✓ done",
        "DAL-A8  DalAloneClosed -> LafziMadlulGate integration                     ✓ done",
        "DAL-A8.1 Harden forbidden-neighbor proof after DAL-A8 merge              ✓ done",
    ):
        assert marker in roadmap


def test_admission_keeps_lafzi_b_and_law_e0_deferred() -> None:
    _declare("lafzi-b and law-e0 deferred")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    assert re.search(r"LAFZI-B0\s+Lafzi Madlul Correspondence Law[\s\S]{0,80}✓ done", roadmap)
    assert re.search(
        r"LAFZI-B7\s+LafziMadlulClosed -> Wad'iMadlulGate integration\s+→ current",
        roadmap,
    )
    assert re.search(r"LAW-E0\s+Arabic Euclidean Layer Contract Law\s+planned", roadmap)


def test_admission_forbids_semantic_and_hukm_outputs() -> None:
    _declare("semantic/hukm outputs forbidden")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for marker in (
        "Parser/morphology/syntax/semantic/hukm/reality outputs are forbidden.",
        "parser_runtime: NOT_OPENED",
        "morphology_runtime: NOT_OPENED",
        "syntax_runtime: NOT_OPENED",
        "semantic_runtime: NOT_OPENED",
        "ifadah_runtime: NOT_OPENED",
        "mafhum_runtime: NOT_OPENED",
        "hukm_runtime: NOT_OPENED",
        "truth_certainty_reality_runtime: NOT_OPENED",
        "rank_promotion: NOT_OPENED",
    ):
        assert marker in roadmap


def test_green_ci_is_not_admission_proof() -> None:
    _declare("green ci not constitutional approval")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")
    assert "Green CI is not constitutional approval." in roadmap
    assert "Green pytest is not constitutional success." in claude


def test_next_permitted_pr_is_dal_a5_runtime_only() -> None:
    _declare("next step dal-a5 runtime only")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    assert "next_permitted_pr: DAL-A5 runtime gates only" in roadmap
    assert "Admission verdict names next permitted PR as DAL-A5 runtime gates only." in roadmap
