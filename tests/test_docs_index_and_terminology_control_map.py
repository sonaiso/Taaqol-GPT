"""Acceptance tests for docs index and terminology control map.

Origin law     : docs/10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md
Branch         : DOCS-INDEX-TERM-CONTROL (documentation jump/gap hardening)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"
_TERMINOLOGY = _REPO_ROOT / "docs" / "TERMINOLOGY.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/10_TECHNICAL_TERMINOLOGY_NON_CONFUSION_LAW.md",
        branch_name=f"DOCS-INDEX-TERM-CONTROL ({branch_note})",
        constitutional_chain=("docs/10", "docs/49", "docs/13"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "ChainMutationClaim",
            "LawAmendmentClaim",
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


def test_docs_index_declares_jump_control_and_numbering_exceptions() -> None:
    _declare("index jump-control markers")
    body = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "## 8) Numbering gaps and jump-control notes" in body
    assert "`57_*` is" in body
    assert "83_LINK_OPERATOR_SURFACE_GEOMETRY_LAW.md" in body
    assert "83_PRONOUN_REFERENCE_SURFACE_GEOMETRY_LAW.md" in body
    assert "docs/14_PR_CHAIN_ROADMAP.md" in body
    assert "CLAUDE.md" in body


def test_docs_index_retains_document_only_boundary() -> None:
    _declare("index scope boundary")
    body = _DOCS_INDEX.read_text(encoding="utf-8")
    assert "This file is an index only." in body
    assert "does not add or amend constitutional law" in body
    assert "runtime permissions" in body


def test_terminology_map_covers_high_risk_boundary_terms() -> None:
    _declare("terminology canonical set")
    body = _TERMINOLOGY.read_text(encoding="utf-8")
    required_terms = (
        "`FormalShapeClosure`",
        "`FormalStyleCandidate`",
        "`NeedGate`",
        "`ReasonablenessVerdict`",
        "`TransitionGate`",
    )
    for term in required_terms:
        assert term in body, f"docs/TERMINOLOGY missing canonical term: {term}"
