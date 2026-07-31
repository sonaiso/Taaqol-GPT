"""Acceptance tests for docs/98 USM law-only boundary."""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_98 = _REPO_ROOT / "docs" / "98_UNIVERSAL_SCIENCE_MATRIX_CONSTITUTIONAL_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"USM-L0 law-only ({branch_note})",
        constitutional_chain=("docs/14", "USM-L0", "docs/98"),
        chain_position="USM-L0 law-only boundary step",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md",
        branch_of_origin="USM bounded constitutional admission branch",
        forbidden_shortcut_assertions=(
            "USM-L0 -> RuntimeOpening",
            "USM-L0 -> ValidatorExecution",
            "USM-L0 -> UniversalTruthClaim",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("RuntimeOpeningClaim", "UniversalCompletenessClaim"),
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


def test_docs_98_declares_law_only_boundary_and_next_step() -> None:
    _declare("document surface")
    body = _DOC_98.read_text(encoding="utf-8")
    assert "Law-only boundary (`USM-L0`)" in body
    assert "no runtime, no carriers, no validators" in body
    assert "USM-C1" in body


def test_docs_98_declares_forbidden_overclaims() -> None:
    _declare("forbidden overclaim markers")
    body = _DOC_98.read_text(encoding="utf-8")
    for marker in (
        "ThreeMatrices -> UniversalCompleteness",
        "StructuralValidation -> ScientificTruth",
        "GovernanceCertificate -> ExternalTruth",
        "EvidencePresent -> JudgmentCertified",
    ):
        assert marker in body


def test_docs_index_references_docs_98() -> None:
    _declare("docs index marker")
    body = _DOCS_INDEX.read_text(encoding="utf-8")
    assert "98_UNIVERSAL_SCIENCE_MATRIX_CONSTITUTIONAL_LAW.md" in body
