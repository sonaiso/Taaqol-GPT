"""Acceptance tests for docs/93 AUX-ESA-0 post-merge quarantine audit.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (chain authority remains unchanged)
Branch         : AUX-ESA-0 post-merge audit
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
_DOC_93 = _REPO_ROOT / "docs" / "93_AUX_ESA_0_POST_MERGE_AUDIT.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"AUX-ESA-0 ({branch_note})",
        constitutional_chain=("docs/14", "AUX-ESA-0", "POST-MERGE-AUDIT"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RoadmapUnlock",
            "RuntimeMutationInCoreKernel",
            "BridgeLicenseClaim",
            "RelationIfadahHukmUnlock",
            "GlobalConstitutionalVerdict",
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


def test_docs_93_exists_with_required_sections() -> None:
    _declare("document presence")
    assert _DOC_93.exists(), "docs/93_AUX_ESA_0_POST_MERGE_AUDIT.md must exist"

    body = _DOC_93.read_text(encoding="utf-8")
    required_markers = (
        "## §1 Scope and boundary",
        "## §2 Auxiliary kernel surface confirmed",
        "## §3 Evidence set for this post-merge audit",
        "## §4 What is proven vs. not proven",
        "## §5 Post-merge validation record",
        "## §6 Final audit verdict",
    )
    for marker in required_markers:
        assert marker in body, f"docs/93 missing required section: {marker}"


def test_docs_93_declares_quarantine_boundary_without_chain_opening() -> None:
    _declare("quarantine boundary")
    body = _DOC_93.read_text(encoding="utf-8")
    required_assertions = (
        "isolated auxiliary prototype",
        "amend `docs/14_PR_CHAIN_ROADMAP.md`",
        "alter `src/taaqqul_slot_geometry/**` runtime",
        "claim any linguistic-to-knowledge bridge",
        "license `WordCapability -> Relation` / `Ifadah` / `Hukm`",
        "migrate auxiliary tests into `tests/support/constitutional_case.py` harness",
    )
    for statement in required_assertions:
        assert statement in body, f"docs/93 missing quarantine boundary assertion: {statement}"


def test_docs_93_captures_local_validation_and_non_admission_verdict() -> None:
    _declare("validation and verdict")
    body = _DOC_93.read_text(encoding="utf-8")
    required_markers = (
        "`ruff check .` -> PASS",
        "`pytest` -> PASS",
        "`cd enriched_simulation_agent && pytest -q` -> PASS",
        "AUX_ESA_0_POST_MERGE_VERDICT = PASS_QUARANTINED",
        "constitutional_chain_status: NOT_ADMITTED",
        "roadmap_unlock: FORBIDDEN_AND_NOT_PRESENT",
        "linguistic_to_knowledge_bridge_claim: FORBIDDEN_AND_NOT_PRESENT",
    )
    for marker in required_markers:
        assert marker in body, f"docs/93 missing validation marker: {marker}"


def test_docs_index_references_docs_93_audit_record() -> None:
    _declare("docs index mapping")
    index_body = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "93_AUX_ESA_0_POST_MERGE_AUDIT.md" in index_body
    assert "auxiliary-kernel quarantine audit" in index_body
