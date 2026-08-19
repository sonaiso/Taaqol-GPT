"""Acceptance tests for docs/114 — Rational Method Governance and Defect Audit Law.

Origin law     : docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md
Branch         : RMG-L0 (law-only rational governance appendix)
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
_DOC_114 = _REPO_ROOT / "docs" / "114_RATIONAL_METHOD_GOVERNANCE_AND_DEFECT_AUDIT_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=f"RMG-L0 law-only ({branch_note})",
        constitutional_chain=("docs/112", "RMG-L0", "docs/114"),
        chain_position="RMG-L0 independent law-only constitutional appendix step",
        origin_law_ref="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_of_origin=(
            "Independent rational-governance appendix that separates "
            "truth, method validity, inference validity, rank, and defect causality."
        ),
        forbidden_shortcut_assertions=(
            "Claim -> Method",
            "InstrumentOutput -> AcceptedEvidence",
            "FalseResult -> DefectType",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "CertificateIssuanceClaim",
            "TruthRealityClosureClaim",
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


def test_docs_114_exists_and_declares_law_only_boundary() -> None:
    _declare("document boundary")
    body = _DOC_114.read_text(encoding="utf-8")

    assert _DOC_114.exists()
    assert "Rational Method Governance and Defect Audit Law (RMG-L0)" in body
    assert "constitutional law document (law-only)" in body
    assert "RUNTIME_NOT_OPENED = {" in body


def test_docs_114_declares_required_governance_chain_and_assessment_axes() -> None:
    _declare("governance chain and assessment axes")
    body = _DOC_114.read_text(encoding="utf-8")

    required_markers = (
        "Claim",
        "-> RationalMethodGovernance",
        "-> Audit",
        "ResultAssessment = <",
        "TruthStatus",
        "MethodStatus",
        "InferenceStatus",
        "Rank",
        "Defects",
        "Residuals",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_114_declares_defect_distinctions_without_runtime_opening() -> None:
    _declare("defect distinctions")
    body = _DOC_114.read_text(encoding="utf-8")

    required_markers = (
        "DefectType = {",
        "ERROR",
        "FALLACY",
        "LIE",
        "FORGETTING",
        "IGNORANCE",
        "UNCERTAINTY",
        "CONFLICT",
        "FalseResult != InvalidMethod",
        "TruthStatus != EpistemicRank",
        "Any runtime change before these explicit successors is a `FORBIDDEN_LEAP`.",
    )
    for marker in required_markers:
        assert marker in body


def test_roadmap_registers_amendment_85_without_displacing_z0_m1_1() -> None:
    _declare("roadmap amendment record")
    roadmap = _DOC_14.read_text(encoding="utf-8")

    assert "Amendment-85 (RMG-L0 — Rational Method Governance and Defect Audit Law)" in roadmap
    assert "Z0-M1.1 remains current" in roadmap
    assert "Z0-M2 remains not yet open" in roadmap


def test_docs_index_references_docs_114() -> None:
    _declare("docs index mapping")
    index_body = _DOCS_INDEX.read_text(encoding="utf-8")
    assert "114_RATIONAL_METHOD_GOVERNANCE_AND_DEFECT_AUDIT_LAW.md" in index_body
