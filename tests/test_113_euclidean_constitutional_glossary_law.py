"""Acceptance tests for docs/113 — Euclidean Constitutional Glossary Law.

Origin law     : docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md
Branch         : GLOSSARY-E0 (law-only constitutional glossary appendix)
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
_DOC_113 = _REPO_ROOT / "docs" / "113_EUCLIDEAN_CONSTITUTIONAL_GLOSSARY_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=f"GLOSSARY-E0 law-only ({branch_note})",
        constitutional_chain=("docs/112", "GLOSSARY-E0", "docs/113"),
        chain_position="GLOSSARY-E0 law-only constitutional appendix step",
        origin_law_ref="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_of_origin=(
            "Independent Euclidean constitutional glossary appendix that "
            "enforces definition/distinction/dependency boundaries."
        ),
        forbidden_shortcut_assertions=(
            "GlossaryTerm -> RuntimeLicense",
            "Closure -> Truth",
            "InterchangeableTerms -> HiddenSynonymy",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "TruthClaim",
            "CertificateIssuanceClaim",
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


def test_docs_113_exists_and_declares_law_only_boundary() -> None:
    _declare("document boundary")
    body = _DOC_113.read_text(encoding="utf-8")

    assert _DOC_113.exists()
    assert "Euclidean Constitutional Glossary Law (GLOSSARY-E0)" in body
    assert "constitutional appendix law document (law-only)" in body
    assert "RUNTIME_NOT_OPENED = {" in body


def test_docs_113_declares_core_form_and_distinction_contract() -> None:
    _declare("core glossary contract")
    body = _DOC_113.read_text(encoding="utf-8")

    required_markers = (
        "Definition",
        "Distinction",
        "LicensedDependency",
        "Term(X)=",
        r"Reality\neq Representation",
        r"Trace(x)\neq x",
        r"Closure\neq Truth.",
        r"Gate\neq Bridge.",
        r"\Delta ConstitutionalType\neq\varnothing",
        "BridgeRequired.",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_113_declares_zero_to_one_and_residual_rank_laws() -> None:
    _declare("zero/one/residual/rank laws")
    body = _DOC_113.read_text(encoding="utf-8")

    required_markers = (
        r"AbsoluteZero\nRightarrow LicensedDistinction.",
        r"0^{+}",
        r"0^{\ast}",
        r"1_{\min}(X)",
        "MCE(X)=PASS.",
        r"Residual_{out}",
        r"Residual_{in}",
        r"Rank(Output)",
        r"\bigwedge Rank(RequiredInputs).",
        r"Computation\nRightarrow Promotion.",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_113_declares_dependency_and_closure_conditions() -> None:
    _declare("dependency/closure conditions")
    body = _DOC_113.read_text(encoding="utf-8")

    required_markers = (
        r"Acyclic(G_{\mathrm{Glossary}})=TRUE.",
        r"Interchangeable(A,B)",
        r"DistinctionLaw(A,B).",
        r"\Delta(A,B)\neq\varnothing.",
        "Glossary is closed not by count of definitions, but iff:",
        "GlossaryMCE=",
        "GlossaryMCE=PASS",
        r"Glossary=1_{\min}.",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_index_references_docs_113() -> None:
    _declare("docs index mapping")
    index_body = _DOCS_INDEX.read_text(encoding="utf-8")
    assert "113_EUCLIDEAN_CONSTITUTIONAL_GLOSSARY_LAW.md" in index_body
