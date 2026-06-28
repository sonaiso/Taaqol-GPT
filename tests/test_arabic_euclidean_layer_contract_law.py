"""Acceptance tests for docs/63 — Arabic Euclidean Layer Contract Law.

Origin law     : docs/63 (Arabic Euclidean Layer Contract Law)
Branch         : LAW-E0 (law-only layer-contract registration)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

_DOCS_DIR = pathlib.Path(__file__).resolve().parent.parent / "docs"
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_63 = _DOCS_DIR / "63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md"
_DOC_14 = _DOCS_DIR / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"
_README = _REPO_ROOT / "README.md"


def _read_doc_63() -> str:
    return _DOC_63.read_text(encoding="utf-8")


def test_docs_63_exists_as_law_only_surface() -> None:
    assert _DOC_63.exists()
    content = _read_doc_63()
    assert "law-only" in content
    assert "no runtime code" in content
    assert "no global `FailureCode` expansion" in content


def test_layer_equation_declares_all_eight_euclidean_questions() -> None:
    content = _read_doc_63()
    required_terms = (
        "ConditionOfPossibility",
        "MinimumCompleteLimit",
        "Opening",
        "Demand",
        "IdentityPreservation",
        "Closure",
        "Residual",
        "LicensedTransition",
    )
    for term in required_terms:
        assert term in content
    assert "شرط إمكان" in content
    assert "انتقال مرخّص" in content


def test_law_links_existing_contract_surfaces_without_replacing_x0r() -> None:
    content = _read_doc_63()
    for reference in (
        "docs/11",
        "docs/14",
        "docs/58",
        "docs/62",
        "EuclideanTransitionContract",
        "MinimalCompleteRequirement",
        "TransitionContract.evaluate()",
    ):
        assert reference in content
    assert "builds over the X0R surfaces instead of replacing them" in content


def test_law_forbids_parser_semantics_and_downstream_outputs() -> None:
    content = _read_doc_63()
    forbidden_outputs = (
        "ArabicParser",
        "MorphologyRuntime",
        "SyntaxRuntime",
        "DalAloneClosed",
        "LafziMadlulGate",
        "LexicalMeaning",
        "IfadahCandidate",
        "HukmCandidate",
        "TruthValue",
        "Certainty",
        "Certificate",
    )
    for output in forbidden_outputs:
        assert output in content


def test_origin_branch_return_surface_is_readiness_only() -> None:
    content = _read_doc_63()
    required_fields = (
        "AslIdentification",
        "FarIdentification",
        "SharedFeature",
        "DifferentiatingFeature",
        "CommonIllah",
        "EffectiveDescription",
        "LinkingSabab",
        "PreservedCondition",
        "AbsentPreventer",
        "AbsentQadihDifference",
        "PreservedIdentity",
    )
    for field in required_fields:
        assert field in content
    for state in ("LINK_READY", "DEFERRED", "BLOCKED", "REFUSED"):
        assert state in content
    assert "must not produce hukm" in content


def test_future_runtime_carriers_are_staged_after_law() -> None:
    content = _read_doc_63()
    for carrier in (
        "LayerQuestionSet",
        "EuclideanLayerContract",
        "LayerResidual",
        "LayerClosureSurface",
        "LayerTransitionReadiness",
        "OriginBranchLicensingContract",
    ):
        assert carrier in content
    assert "Those carriers, if opened by a later PR" in content


def test_forbidden_straight_lines_include_requested_inverse_tests() -> None:
    content = _read_doc_63()
    for forbidden_line in (
        "Letter -> Word",
        "Weight -> Hukm",
        "Particle -> Ifadah without demanded complement",
        "Ikhbar -> Truth",
        "Ifadah -> Certainty",
        "Probability -> LicensedTransition",
    ):
        assert forbidden_line in content
    assert "FORBIDDEN_STRAIGHT_LINE" in content


def test_roadmap_registers_law_e0_without_displacing_gpt_r8() -> None:
    doc_14 = _DOC_14.read_text(encoding="utf-8")
    claude_md = _CLAUDE_MD.read_text(encoding="utf-8")
    readme = _README.read_text(encoding="utf-8")

    # GPT-R8L (docs/56) is the current law-only step that licenses GPT-R8;
    # GPT-R8 itself remains the next runtime step. LAW-E0 stays planned and
    # does not displace either of them.
    assert re.search(r"GPT-R8L\s+GPT-R8 Audit Integration Law\s+→ current", doc_14)
    assert re.search(r"GPT-R8\s+Audit Integration\s+→ next", doc_14)
    assert re.search(r"LAW-E0\s+Arabic Euclidean Layer Contract Law\s+planned", doc_14)
    assert re.search(r"LAW-E0\s+Arabic Euclidean Layer Contract Law\s+planned", claude_md)
    assert "docs/63" in readme
    assert "`GPT-R8` audit integration is now next" in readme
