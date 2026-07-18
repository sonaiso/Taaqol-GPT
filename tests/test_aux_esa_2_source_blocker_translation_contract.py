"""Acceptance tests for docs/96 AUX-ESA-2 SOURCE_BLOCKER_UNMAPPED contract.

Origin law     : docs/94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md
Branch         : AUX-ESA-2 source blocker translation contract
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_96 = _REPO_ROOT / "docs" / "96_AUX_ESA_2_SOURCE_BLOCKER_TRANSLATION_CONTRACT.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md",
        branch_name=f"AUX-ESA-2 ({branch_note})",
        constitutional_chain=("docs/94", "AUX-ESA-1", "AUX-ESA-2"),
        chain_position="AUX-ESA-2 SOURCE_BLOCKER_UNMAPPED translation contract",
        origin_law_ref=(
            "docs/94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md#4-forbidden-"
            "transitions-and-outputs"
        ),
        branch_of_origin=(
            "Auxiliary contract tightening step that preserves quarantine and blocks "
            "unmapped source-blocker collapse into ACCEPT."
        ),
        forbidden_shortcut_assertions=(
            "AUX-ESA-2 -> docs/14_chain_unlock",
            "AUX-ESA-2 -> linguistic_to_knowledge_bridge_proof",
            "AUX-ESA-2 -> global_constitutional_verdict",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ConstitutionalAdmissionCertificate",
            "RoadmapAdvanceClaim",
            "BridgeLicensedClaim",
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


def test_docs_96_exists_with_contract_sections() -> None:
    _declare("document presence")
    body = _DOC_96.read_text(encoding="utf-8")

    required_markers = (
        "## §1 Scope and quarantine",
        "## §2 Contract statement",
        "## §3 Allowed outcomes",
        "## §4 Forbidden outcome",
        "## §5 Minimal runtime obligations",
        "## §6 Constitutional non-admission statement",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_96_records_required_policy() -> None:
    _declare("policy assertions")
    body = _DOC_96.read_text(encoding="utf-8")

    required_markers = (
        "DEFER + SOURCE_BLOCKER_UNMAPPED",
        "or escalate to `BLOCK`",
        "must never resolve to `ACCEPT`",
        "unexplained target blocker must yield `BLOCK`",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_96_keeps_quarantine_boundaries() -> None:
    _declare("quarantine assertions")
    body = _DOC_96.read_text(encoding="utf-8")

    required_markers = (
        "does not admit AUX-ESA into `docs/14_PR_CHAIN_ROADMAP.md`",
        "does not license any Arabic/programming or linguistic/knowledge bridge",
        "does not mutate `src/taaqqul_slot_geometry/**`",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_index_references_docs_96_record() -> None:
    _declare("docs index mapping")
    index_body = _DOCS_INDEX.read_text(encoding="utf-8")
    assert "96_AUX_ESA_2_SOURCE_BLOCKER_TRANSLATION_CONTRACT.md" in index_body
