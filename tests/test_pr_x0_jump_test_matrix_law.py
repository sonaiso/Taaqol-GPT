"""Acceptance tests for docs/14 Amendment-31 (PR-X0 law-only surface).

Origin law          : docs/14 Amendment-31 (PR-X0)
Branch name         : PR-X0 Jump-Test Matrix Law
Constitutional chain: docs/14 -> Amendment-31 -> Law-only assertions
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

ORIGIN_LAW = "docs/14 Amendment-31 (PR-X0 — Jump-Test Matrix Law + Minimal Residual Vocabulary)"
BRANCH_NAME = "PR-X0 Jump-Test Matrix Law"
CONSTITUTIONAL_CHAIN = ("docs/14", "Amendment-31", "Law-only assertions")

_DOC_14 = (
    pathlib.Path(__file__).resolve().parent.parent / "docs" / "14_PR_CHAIN_ROADMAP.md"
)


def _read_doc_14() -> str:
    if not _DOC_14.exists():
        pytest.skip("docs/14_PR_CHAIN_ROADMAP.md not found")
    return _DOC_14.read_text(encoding="utf-8")


def _normalized(content: str) -> str:
    return " ".join(content.split())


def test_declares_identity_fields_for_pr_x0_test_surface() -> None:
    assert ORIGIN_LAW
    assert BRANCH_NAME
    assert CONSTITUTIONAL_CHAIN


def test_jump_test_matrix_is_declared() -> None:
    content = _read_doc_14()
    for token in (
        "sufficiency",
        "necessity",
        "preserved_trace",
        "qadih_difference",
        "blocking_residuals",
    ):
        assert token in content, f"{ORIGIN_LAW}: missing jump-test element '{token}'"


def test_minimal_residual_vocabulary_is_declared() -> None:
    content = _read_doc_14()
    for token in (
        "BLOCKING",
        "DEFERRED",
        "REPAIRABLE",
        "NON_BLOCKING",
        "CONTRADICTORY",
    ):
        assert token in content, f"{ORIGIN_LAW}: missing residual category '{token}'"


def test_default_rejection_is_forbidden_straight_line() -> None:
    content = _read_doc_14()
    assert "FORBIDDEN_STRAIGHT_LINE" in content
    assert "more specific named" in content


def test_path_matrix_principle_is_explicit() -> None:
    content = _read_doc_14()
    assert "E0–E10 is explicitly non-mandatory as a single ladder" in content
    assert "after CellSequence, execution is a path matrix" in content
    assert "BuiltMinimalUnit is a valid closure path" in content
    assert "Root/Weight is only one possible post-CellSequence path" in content


def test_required_future_pr_declarations_are_explicit() -> None:
    content = _normalized(_read_doc_14())
    required = (
        "origin",
        "domain",
        "forbidden straight-line transition",
        "preserved trace",
        "residuals",
        "rank ceiling",
        "allowed closure boundary",
    )
    for token in required:
        assert token in content, f"{ORIGIN_LAW}: missing required declaration '{token}'"


def test_required_forbidden_jump_assertions_are_documented() -> None:
    content = _read_doc_14()
    required = (
        "Silence (NoDal) does not causally generate Motion",
        "Motion does not directly prove Fatha/Kasra/Damma/Sukun",
        "Fatha does not imply Alif absolutely",
        "ThreeLetters does not imply Root without RootLicense",
        "BuiltMinimalUnit blocks Weight interpretation",
        "SingleWordClosure does not imply Sentence without",
    )
    for token in required:
        assert token in content, f"{ORIGIN_LAW}: missing assertion '{token}'"


def test_no_silent_success_and_failure_are_documented() -> None:
    content = _read_doc_14()
    assert "No success is silent" in content
    assert "preserved trace, passed gates, and residual status" in content
    assert "No failure is silent" in content
    assert "rejection reason, residual category, and blocked" in content
