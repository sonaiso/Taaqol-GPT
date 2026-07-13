"""Acceptance tests for docs/91 — execution gap matrix (46 items).

Origin law     : docs/80 (state-truth source order) + docs/14 (chain truth)
Branch         : docs/91 execution-gap operational classification matrix
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import re
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_91 = _REPO_ROOT / "docs" / "91_EXECUTION_GAP_MATRIX_46_ITEMS.md"
_ALLOWED_STATUSES = {"runtime-closed", "law-only", "proposal-only", "not-started"}
_ROW_PATTERN = re.compile(r"^\|\s*(\d+)\s*\|\s*.+\|\s*([a-z\-]+)\s*\|\s*$")


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md",
        branch_name=f"docs/91 execution-gap matrix ({branch_note})",
        constitutional_chain=("docs/14", "docs/80", "docs/91"),
        chain_position="Operational classification artifact (state-truth snapshot)",
        origin_law_ref="docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md#1-live-reference-truth-vs-historical-snapshot-records",
        branch_of_origin=(
            "State-truth snapshot matrix that classifies declared gaps without "
            "opening runtime or mutating chain order."
        ),
        forbidden_shortcut_assertions=(
            "SnapshotClassification -> ChainAmendment",
            "SnapshotClassification -> RuntimeOpening",
            "HistoricalSnapshot -> LiveTruthOverride",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ChainOrderMutation",
            "RuntimeOpening",
            "SemanticTruthClaim",
            "HiddenResidualStatusFlip",
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


def _matrix_rows(body: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for line in body.splitlines():
        match = _ROW_PATTERN.match(line)
        if not match:
            continue
        rows.append((int(match.group(1)), match.group(2)))
    return rows


def test_docs_91_exists_and_declares_scope() -> None:
    _declare("document presence and scope")
    assert _DOC_91.exists(), "docs/91 execution gap matrix must exist"
    body = _DOC_91.read_text(encoding="utf-8")

    for marker in (
        "91 — Execution Gap Matrix (46 Items)",
        "runtime-closed",
        "law-only",
        "proposal-only",
        "not-started",
        "STATE_TRUTH_SOURCE_ORDER = docs/14 -> runtime(src/) + tests/ -> docs/80",
        "NO_OVERCLAIM_RULE",
    ):
        assert marker in body


def test_docs_91_contains_exactly_46_indexed_rows() -> None:
    _declare("matrix cardinality")
    body = _DOC_91.read_text(encoding="utf-8")
    rows = _matrix_rows(body)

    assert len(rows) == 46, "matrix must contain exactly 46 indexed rows"
    indices = [index for index, _status in rows]
    assert indices == list(range(1, 47)), "matrix indices must be contiguous from 1..46"


def test_docs_91_uses_only_allowed_status_vocabulary() -> None:
    _declare("status vocabulary control")
    body = _DOC_91.read_text(encoding="utf-8")
    rows = _matrix_rows(body)

    statuses = {status for _index, status in rows}
    assert statuses.issubset(_ALLOWED_STATUSES)
    assert "runtime-closed" in statuses
    assert "law-only" in statuses
    assert "proposal-only" in statuses
    assert "not-started" in statuses


def test_docs_91_declares_integrity_notes() -> None:
    _declare("integrity notes")
    body = _DOC_91.read_text(encoding="utf-8")

    for marker in (
        "state-truth snapshot",
        "not a chain-amendment PR step",
        "status flip must follow constitutional chain discipline",
    ):
        assert marker in body
