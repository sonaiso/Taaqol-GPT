"""Acceptance tests for docs/70 critical linguistic partition law.

Origin law          : docs/70_CRITICAL_LINGUISTIC_SYSTEM_PARTITION_LAWS.md
Branch name         : LAW-E1 critical partition law-only registration
Constitutional chain: docs/70 -> docs/69 -> docs/14 -> CLAUDE
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_70 = _REPO_ROOT / "docs" / "70_CRITICAL_LINGUISTIC_SYSTEM_PARTITION_LAWS.md"
_DOC_69 = _REPO_ROOT / "docs" / "69_FOUNDATIONAL_EUCLIDEAN_COVERAGE_MATRIX.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/70_CRITICAL_LINGUISTIC_SYSTEM_PARTITION_LAWS.md",
        branch_name=branch_name,
        constitutional_chain=("docs/70", "docs/69", "docs/14", "CLAUDE"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("RuntimePartitionGate", "SemanticClosureClaim"),
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


def test_docs_70_exists_with_required_sections() -> None:
    _declare("docs/70 section surface")
    assert _DOC_70.exists()
    content = _DOC_70.read_text(encoding="utf-8")
    for marker in (
        "## §1 Scope",
        "## §2 Partition boundary definitions",
        "## §3 Identity conservation law",
        "## §4 Necessity-tier discipline",
        "## §5 Failure mapping and residual policy",
        "## §6 Golden fixtures and staged opening",
        "## §7 Forbidden surface",
        "## §8 Evidence anchors",
    ):
        assert marker in content


def test_docs_70_declares_partition_identity_and_tier_terms() -> None:
    _declare("docs/70 required terms")
    content = _DOC_70.read_text(encoding="utf-8")
    for term in (
        "PhoneticPartition",
        "StructuralPartition",
        "SystemicPartition",
        "IdentityPropertyConservation",
        "LicensedIdentityTransition",
        "PreviousIdentityLink",
        "NextIdentityLink",
        "PreviousNextIdentityBridge",
        "DARURI",
        "HAJI",
        "TAHSINI",
        "FORBIDDEN_STRAIGHT_LINE",
    ):
        assert term in content
    assert "no runtime code" in content
    assert "no parser" in content


def test_docs_69_marks_partition_rows_as_law_only_opening() -> None:
    _declare("docs/69 law-only opening rows")
    content = _DOC_69.read_text(encoding="utf-8")
    for row_key in (
        "Phonetic partition | ✅ docs/70 §2",
        "Structural partition | ✅ docs/70 §2",
        "System partition | ✅ docs/70 §2",
        "Identity property law | ✅ docs/70 §3",
        "Triadic identity continuity | ✅ docs/70 §3",
        "Necessity-tier law (ḍarūrī/ḥājī/taḥsīnī) | ✅ docs/70 §4",
    ):
        assert row_key in content
    assert "◐ law-only" in content


def test_chain_records_law_e1_as_planned_without_displacing_close_5() -> None:
    _declare("chain registration for law-e1")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(r"LAW-E1\s+Critical Linguistic System Partition Laws\s+✓ done", roadmap)
    assert re.search(r"LAW-E1\s+Critical Linguistic System Partition Laws\s+✓ done", claude)
    assert re.search(r"CLOSE-5\s+Final closure audit\s+→ current", roadmap)
    assert re.search(r"CLOSE-5\s+Final closure audit\s+→ current", claude)
