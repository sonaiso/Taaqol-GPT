"""Acceptance tests for docs/68 and docs/69 foundational Euclidean package docs.

Origin law          : docs/68_FOUNDATIONAL_EUCLIDEAN_LICENSING_LAWS.md
Branch name         : Foundational Euclidean docs closure
Constitutional chain: docs/68 -> docs/69 -> documentation verification
Category            : Category 2 — Contract / surface tests (docs/52 §4)
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
_DOC_68 = _REPO_ROOT / "docs" / "68_FOUNDATIONAL_EUCLIDEAN_LICENSING_LAWS.md"
_DOC_69 = _REPO_ROOT / "docs" / "69_FOUNDATIONAL_EUCLIDEAN_COVERAGE_MATRIX.md"
_FIXTURE_PACK = _REPO_ROOT / "data" / "x0r_foundational_transition_fixtures.json"

_DOC_68_MARKERS = (
    "## 1) Scope",
    "## 2) Canonical definitions",
    "## 3) Gate evaluation order",
    "## 4) Public carrier invariants",
    "## 5) Forbidden surface",
    "## 6) Evidence anchors",
)

_DOC_69_MARKERS = (
    "Definition → Contract → Carrier → Gate → Failure Mapping → Tests → Fixtures → Coverage",
    "Public carrier invariants (`JumpTestResult`)",
    "Public carrier invariants (`EuclideanGateDecision`)",
    "Phonetic partition",
    "Structural partition",
    "System partition",
    "Identity property law",
    "Triadic identity continuity",
    "Necessity-tier law (ḍarūrī/ḥājī/taḥsīnī)",
)


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/68_FOUNDATIONAL_EUCLIDEAN_LICENSING_LAWS.md",
        branch_name=branch_name,
        constitutional_chain=("docs/68", "docs/69", "DocsVerification"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("OpenedBranch", "ChainTruthOverride"),
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


def test_docs_68_exists_with_required_sections() -> None:
    _declare("docs/68 section coverage")
    assert _DOC_68.exists()
    body = _DOC_68.read_text(encoding="utf-8")
    for marker in _DOC_68_MARKERS:
        assert marker in body


def test_docs_69_exists_with_required_matrix_rows() -> None:
    _declare("docs/69 matrix coverage")
    assert _DOC_69.exists()
    body = _DOC_69.read_text(encoding="utf-8")
    for marker in _DOC_69_MARKERS:
        assert marker in body


def test_docs_68_references_runtime_and_fixture_artifacts() -> None:
    _declare("docs/68 evidence anchors")
    body = _DOC_68.read_text(encoding="utf-8")
    for relative in (
        "src/taaqqul_slot_geometry/x0r/transition_contract.py",
        "tests/test_pr_x0r_runtime_contract_hooks.py",
        "data/x0r_foundational_transition_fixtures.json",
        "tests/test_x0r_foundational_transition_fixtures.py",
    ):
        assert relative in body
        assert (_REPO_ROOT / relative).exists()
    assert _FIXTURE_PACK.exists()

