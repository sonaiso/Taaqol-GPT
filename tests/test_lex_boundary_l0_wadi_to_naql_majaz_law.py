"""Acceptance tests for docs/82 — Wad'i to Naql/Majaz Boundary Law.

Origin law     : docs/81 + docs/82
Branch         : LEX-BOUNDARY-L0 (law-only negative-neighbor boundary)
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
_DOC_81 = _REPO_ROOT / "docs" / "81_LEXICAL_EVIDENCE_DATA_LAW.md"
_DOC_82 = _REPO_ROOT / "docs" / "82_WADI_TO_NAQL_MAJAZ_BOUNDARY_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/81_LEXICAL_EVIDENCE_DATA_LAW.md + "
            "docs/82_WADI_TO_NAQL_MAJAZ_BOUNDARY_LAW.md"
        ),
        branch_name=f"LEX-BOUNDARY-L0 ({branch_note})",
        constitutional_chain=("docs/81", "docs/82", "LEX-BOUNDARY-L0"),
        chain_position="LEX-BOUNDARY-L0 law-only wad'i/naql/majaz transition boundary",
        origin_law_ref="docs/82_WADI_TO_NAQL_MAJAZ_BOUNDARY_LAW.md#1-governing-negative-neighbor-rule",
        branch_of_origin=(
            "Law-only boundary preventing automatic transitions from wad'i licensing "
            "to naqli/majazi licensing."
        ),
        forbidden_shortcut_assertions=(
            "Wad'iMadlulLicensed -> NaqliMadlulLicensed",
            "Wad'iMadlulLicensed -> MajaziMadlulLicensed",
            "LexicalAttestation -> FinalMeaning",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "NaqliMadlulLicensed_without_NaqlGate",
            "MajaziMadlulLicensed_without_MajazGate",
            "ContextualMeaning",
            "FinalMeaning",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
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


def test_docs_82_exists_and_is_law_only() -> None:
    _declare("document existence")
    body = _DOC_82.read_text(encoding="utf-8")

    assert _DOC_82.exists()
    assert "Status: constitutional law document (law-only)." in body
    assert "introduces no runtime code" in body
    assert "RUNTIME_NOT_OPENED = {" in body


def test_docs_82_declares_wadi_not_implying_naql_or_majaz() -> None:
    _declare("negative-neighbor transition rule")
    body = _DOC_82.read_text(encoding="utf-8")

    required_markers = (
        "Wad'iMadlulLicensed NOT_EQUAL NaqliMadlulLicensed",
        "Wad'iMadlulLicensed NOT_EQUAL MajaziMadlulLicensed",
        "Wad'iMadlulLicensed DOES_NOT_IMPLY NaqliMadlulLicensed",
        "Wad'iMadlulLicensed DOES_NOT_IMPLY MajaziMadlulLicensed",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_82_requires_independent_naql_and_majaz_gates() -> None:
    _declare("independent gate requirements")
    body = _DOC_82.read_text(encoding="utf-8")

    required_markers = (
        "NaqlGate  = required for any Wad'i -> Naqli transition",
        "MajazGate = required for any Wad'i -> Majazi transition",
        "transferred_usage_attestation",
        "historical_or_usage_evidence",
        "qarina_sarifa",
        "maqam_context_evidence",
        "literal_preventer",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_82_forbidden_outputs_block_meaning_and_truth_jump() -> None:
    _declare("forbidden output boundary")
    body = _DOC_82.read_text(encoding="utf-8")

    for token in (
        "NaqliMadlulLicensed_without_NaqlGate",
        "MajaziMadlulLicensed_without_MajazGate",
        "FinalMeaning",
        "Hukm",
        "Truth",
        "Certainty",
        "Reality",
    ):
        assert token in body


def test_docs_81_references_docs_82_boundary_continuity() -> None:
    _declare("docs/81 continuity with docs/82")
    body = _DOC_81.read_text(encoding="utf-8")

    assert "§6 Boundary continuity with docs/82 (LEX-BOUNDARY-L0)" in body
    assert "Wad'iMadlulLicensed DOES_NOT_IMPLY NaqliMadlulLicensed" in body
    assert "Wad'iMadlulLicensed DOES_NOT_IMPLY MajaziMadlulLicensed" in body
