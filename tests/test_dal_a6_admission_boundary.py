"""DAL-A6 admission-only boundary tests.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (DAL-A6-ADMIT admission-only step)
Branch         : DAL-A6-ADMIT (post-DAL-A5 runtime admission decision)
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
        branch_name=f"DAL-A6-ADMIT ({branch_note})",
        constitutional_chain=("DAL-A5", "DAL-A6-ADMIT", "DAL-A6"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "DALA6RuntimeOpening",
            "WaqfWaslRuntimeCertificate",
            "DALA7RuntimeDecision",
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


def test_dal_a6_admission_chain_state_is_synchronized() -> None:
    _declare("dal-a6-admit done + dal-a7.1 runtime current")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    for marker in (
        "DAL-A5  Syllable / transition / adjacency / S1-S5 gates                   ✓ done",
        "DAL-A6-ADMIT admission boundary after DAL-A5 runtime                      ✓ done",
        "DAL-A6  Detailed waqf / wasl closure                                      ✓ done",
        "DAL-A7  Usage / loan / unvocalized / deletion residual gates              ✓ done",
        "DAL-A7.1 Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics          ✓ done",
    ):
        assert marker in roadmap
        assert marker in claude


def test_dal_a6_admission_verdict_is_admission_only() -> None:
    _declare("admission verdict remains non-runtime")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for marker in (
        "DAL_A6_ADMISSION_MATRIX =",
        "DAL_A6_ADMISSION_VERDICT = {",
        "status: ADMITTED_ONLY",
        "dal_a6_runtime_status: DEFERRED",
        "next_permitted_pr: DAL-A6 runtime gates only,",
        "runtime_certificate: NOT_PRODUCED",
    ):
        assert marker in roadmap


def test_dal_a6_admission_keeps_downstream_layers_deferred() -> None:
    _declare("downstream deferred")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for marker in (
        "DAL-A7  Usage / loan / unvocalized / deletion residual gates              ✓ done",
        "DAL-A7.1 Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics          ✓ done",
        "DAL-A8  DalAloneClosed -> LafziMadlulGate integration                     ✓ done",
        "DAL-A8.1 Harden forbidden-neighbor proof after DAL-A8 merge              ✓ done",
    ):
        assert marker in roadmap
    assert re.search(r"LAFZI-B0\s+Lafzi Madlul Correspondence Law[\s\S]{0,80}✓ done", roadmap)
    assert re.search(
        r"LAFZI-B7\s+LafziMadlulClosed -> Wad'iMadlulGate integration\s+✓ done",
        roadmap,
    )
    assert re.search(r"LAW-E0\s+Arabic Euclidean Layer Contract Law\s+✓ done", roadmap)


def test_dal_a6_admission_forbids_runtime_and_semantic_outputs() -> None:
    _declare("runtime and semantic outputs forbidden")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for marker in (
        "DAL-A6 runtime implementation, waqf/wasl evaluators,",
        "parser/morphology/syntax/semantic/",
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


def test_dal_a6_admission_keeps_green_ci_outside_constitutional_proof() -> None:
    _declare("green ci not constitutional approval")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")
    assert "Green CI is not constitutional approval." in roadmap
    assert "Green pytest is not constitutional success." in claude
