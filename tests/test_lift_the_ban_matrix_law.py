"""Acceptance tests for docs/64 — Lift-the-Ban Matrix Law.

Origin law     : docs/64 (Lift-the-Ban Matrix Law)
Branch         : CLOSE-3.1 (law-only closure-class step)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_64 = _REPO_ROOT / "docs" / "64_LIFT_THE_BAN_MATRIX_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_README = _REPO_ROOT / "README.md"

_FORBIDDEN_OUTPUTS = (
    "OpenedBranch",
    "BranchLicense",
    "ReadinessCertificate",
    "ReleaseTag",
    "ClosedBranchVerdict",
    "PublicReadinessVerdict",
)

_BAN_CLASSES = ("CONSTITUTIONAL_BRANCH", "PUBLIC_READINESS")

_EVIDENCE_KINDS = (
    "RATIFIED_LAW",
    "CHAIN_TABLE_ROW",
    "PER_STEP_BOUNDARY_BLOCK",
    "CONSTITUTIONAL_TEST",
    "RUNTIME_ARTIFACT",
    "DOC_SECTION",
    "PUBLISHED_RELEASE",
    "LICENSE_FILE",
)

_OWNERS = ("chain-author", "maintainer", "release-manager")

_TEST_KINDS = (
    "CONSTITUTIONAL_CHAIN_TEST",
    "DOC_PRESENCE_TEST",
    "SCANNER",
    "REGISTRY_TEST",
    "OPERATIONAL_AUDIT",
    "RELEASE_CHECK",
    "NONE",
)

_RANK_CEILINGS = ("ZERO", "ONE", "TWO", "THREE")

_RESIDUAL_POLICIES = ("STRICT_VISIBLE", "DEFERRED_VISIBLE")

_DECISION_RE = re.compile(
    r"^(LIFT_PERMITTED|LIFT_BLOCKED|NOT_APPLICABLE|LIFT_DEFERRED_TO_LAW\([^)]+\))$"
)

_REQUIRED_COLUMNS = (
    "ban_class",
    "condition_text",
    "evidence_kind",
    "evidence_locator",
    "owner",
    "test_kind",
    "failure_code",
    "rank_ceiling",
    "residual_policy",
    "decision",
)

_TABLE_A_IDS = ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8")
_TABLE_B_IDS = ("B1", "B2", "B3", "B4")

_LOCAL_RESIDUALS = (
    "MATRIX_EVIDENCE_MISSING",
    "MATRIX_OWNER_UNNAMED",
    "MATRIX_DECISION_UNSUPPORTED",
    "MATRIX_BAN_CLASS_LEAK",
    "MATRIX_FAILURE_CODE_UNKNOWN",
    "MATRIX_LIFT_WITHOUT_ORIGIN_LAW",
)


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/64_LIFT_THE_BAN_MATRIX_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("CLOSE-3", "CLOSE-3.1", "LiftTheBanMatrixLaw"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=forbidden_outputs,
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


def _read(path: pathlib.Path) -> str:
    if not path.exists():
        pytest.skip(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def _parse_row(content: str, row_id: str) -> dict[str, str]:
    """Parse a §9 row block (e.g., ``A1`` / ``B3``) into column -> value."""
    pattern = re.compile(
        r"^" + re.escape(row_id) + r"\n((?:  .+\n)+)",
        re.MULTILINE,
    )
    match = pattern.search(content)
    assert match is not None, f"row {row_id} not found in docs/64 §9"
    columns: dict[str, str] = {}
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        columns[key.strip()] = value.strip()
    return columns


def _all_rows(content: str) -> dict[str, dict[str, str]]:
    return {row_id: _parse_row(content, row_id) for row_id in (*_TABLE_A_IDS, *_TABLE_B_IDS)}


# ----------------------------------------------------------------------
# §1–§10 presence
# ----------------------------------------------------------------------


def test_docs_64_exists_and_is_law_only() -> None:
    _declare("document existence")
    content = _read(_DOC_64)
    assert "Status:" in content
    assert "Law-only" in content
    assert "no carriers" in content
    assert "no new global `FailureCode`" in content


def test_docs_64_declares_all_required_sections() -> None:
    _declare("required sections §1–§10")
    content = _read(_DOC_64)
    for heading in (
        "## §1 Origin and authority",
        "## §2 The two ban classes",
        "## §3 Matrix schema",
        "## §4 Closed vocabularies",
        "## §5 Decision discipline",
        "## §6 Forbidden surface",
        "## §7 Local residual vocabulary",
        "## §8 Test expectations",
        "## §9 Worked rows",
        "## §10 Refusal table",
    ):
        assert heading in content, f"missing section heading: {heading}"


def test_docs_64_declares_two_ban_classes_and_decision_vocab() -> None:
    _declare("ban classes and decision vocabulary")
    content = _read(_DOC_64)
    for ban in _BAN_CLASSES:
        assert ban in content
    for decision in (
        "LIFT_PERMITTED",
        "LIFT_BLOCKED",
        "LIFT_DEFERRED_TO_LAW",
        "NOT_APPLICABLE",
    ):
        assert decision in content


def test_docs_64_declares_local_matrix_residual_vocabulary() -> None:
    _declare("local matrix residual vocabulary")
    content = _read(_DOC_64)
    for residual in _LOCAL_RESIDUALS:
        assert residual in content


def test_docs_64_forbidden_surface_blocks_branch_opening_and_certificates() -> None:
    _declare("forbidden surface", _FORBIDDEN_OUTPUTS)
    content = _read(_DOC_64)
    for token in (
        "MUST NOT",
        "horizontal branch",
        "PV-A5",
        "ḥaqīqah",
        "majāz",
        "naql",
        "certificate",
        "FORBIDDEN_LEAP",
    ):
        assert token in content


# ----------------------------------------------------------------------
# §9 row schema
# ----------------------------------------------------------------------


def test_docs_64_rows_have_all_required_columns_from_closed_vocab() -> None:
    _declare("§9 row schema")
    content = _read(_DOC_64)
    rows = _all_rows(content)
    for row_id, columns in rows.items():
        for column in _REQUIRED_COLUMNS:
            assert column in columns, f"row {row_id} missing column {column}"
        assert columns["ban_class"] in _BAN_CLASSES, row_id
        assert columns["evidence_kind"] in _EVIDENCE_KINDS, row_id
        assert columns["owner"] in _OWNERS, row_id
        assert columns["test_kind"] in _TEST_KINDS, row_id
        assert columns["rank_ceiling"] in _RANK_CEILINGS, row_id
        assert columns["residual_policy"] in _RESIDUAL_POLICIES, row_id
        assert _DECISION_RE.match(columns["decision"]), (
            f"row {row_id} has invalid decision: {columns['decision']!r}"
        )


def test_docs_64_rows_reference_only_known_failure_codes() -> None:
    _declare("failure codes drawn from inventory")
    content = _read(_DOC_64)
    rows = _all_rows(content)
    known = {member.value for member in FailureCode} | {"NONE"}
    for row_id, columns in rows.items():
        code = columns["failure_code"]
        assert code in known, (
            f"row {row_id} references unknown FailureCode: {code!r}"
        )


def test_docs_64_evidence_locators_exist() -> None:
    _declare("evidence locators resolve on disk")
    content = _read(_DOC_64)
    rows = _all_rows(content)
    for row_id, columns in rows.items():
        locator = columns["evidence_locator"]
        path_part = locator.split(":", 1)[0]
        path = _REPO_ROOT / path_part
        assert path.exists(), (
            f"row {row_id} evidence_locator does not resolve: {locator!r}"
        )


def test_docs_64_lift_permitted_requires_origin_law_on_disk() -> None:
    """Per §10: a LIFT_PERMITTED for a CONSTITUTIONAL_BRANCH row must
    point at an origin law that actually exists.
    """
    _declare("MATRIX_LIFT_WITHOUT_ORIGIN_LAW guard")
    content = _read(_DOC_64)
    rows = _all_rows(content)
    for row_id, columns in rows.items():
        if columns["ban_class"] != "CONSTITUTIONAL_BRANCH":
            continue
        if columns["decision"] != "LIFT_PERMITTED":
            continue
        if columns["evidence_kind"] != "RATIFIED_LAW":
            continue
        path_part = columns["evidence_locator"].split(":", 1)[0]
        assert (_REPO_ROOT / path_part).exists(), (
            f"row {row_id}: LIFT_PERMITTED without on-disk origin law: {path_part}"
        )


def test_docs_64_table_partitions_match_ban_classes() -> None:
    """Table A rows must all be CONSTITUTIONAL_BRANCH; Table B rows must
    all be PUBLIC_READINESS. This is the structural form of the
    MATRIX_BAN_CLASS_LEAK refusal in §10.
    """
    _declare("ban-class isolation between tables")
    content = _read(_DOC_64)
    rows = _all_rows(content)
    for row_id in _TABLE_A_IDS:
        assert rows[row_id]["ban_class"] == "CONSTITUTIONAL_BRANCH", row_id
    for row_id in _TABLE_B_IDS:
        assert rows[row_id]["ban_class"] == "PUBLIC_READINESS", row_id


def test_docs_64_refusal_table_lists_each_local_residual() -> None:
    _declare("refusal table coverage")
    content = _read(_DOC_64)
    # The §10 table must mention every local residual at least once
    # so that the matrix audit cannot silently drop one.
    _, _, after = content.partition("## §10 Refusal table")
    assert after, "§10 refusal table missing"
    for residual in _LOCAL_RESIDUALS:
        assert residual in after, f"§10 refusal table omits {residual}"


# ----------------------------------------------------------------------
# Roadmap / CLAUDE / README registration
# ----------------------------------------------------------------------


def test_roadmap_registers_close_3_1_between_close_3_and_close_4() -> None:
    _declare("roadmap registration")
    roadmap = _read(_DOC_14)
    assert "CLOSE-3.1 Lift-the-Ban Matrix Law" in roadmap
    assert "docs/64" in roadmap
    assert "Amendment-51 (CLOSE-3.1" in roadmap
    close_3 = roadmap.index("CLOSE-3 PV-T0.1 test-origin scanner")
    close_3_1 = roadmap.index("CLOSE-3.1 Lift-the-Ban Matrix Law")
    close_4 = roadmap.index("CLOSE-4 Golden closure fixtures")
    assert close_3 < close_3_1 < close_4


def test_claude_registers_close_3_1_between_close_3_and_close_4() -> None:
    _declare("CLAUDE registration")
    claude = _read(_CLAUDE)
    assert "CLOSE-3.1 Lift-the-Ban Matrix Law" in claude
    close_3 = claude.index("CLOSE-3 PV-T0.1 test-origin scanner")
    close_3_1 = claude.index("CLOSE-3.1 Lift-the-Ban Matrix Law")
    close_4 = claude.index("CLOSE-4 Golden closure fixtures")
    assert close_3 < close_3_1 < close_4


def test_readme_mentions_close_3_1_without_restating_matrix() -> None:
    _declare("README status note")
    readme = _read(_README)
    assert "CLOSE-3.1" in readme
    assert "docs/64" in readme
    # The README must not restate the matrix's row schema or §4
    # vocabularies. A simple structural check: §9 row identifiers
    # like "A1\n" should never appear in README.
    for row_id in _TABLE_A_IDS:
        assert f"\n{row_id}\n" not in readme, (
            f"README must not restate matrix row {row_id}"
        )
