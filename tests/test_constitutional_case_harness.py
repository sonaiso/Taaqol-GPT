"""Tests for the constitutional test-case harness.

These tests are meta-tests: they prove that
``tests/support/constitutional_case.py`` enforces the discipline
required by ``docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md`` before any
PR-2+ test is written. The harness must refuse malformed cases at
construction time and must refuse to silently accept a partial pass.

No SlotGraph or gamma is exercised here — they land in PR-2.
"""

from __future__ import annotations

import pytest
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalSchemaError,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank


def _hidden_residual_case() -> ConstitutionalTestCase:
    """Reference negative case used by several tests below.

    Origin: "No closure with hidden residuals."
    Branch: a SlotGraph whose required slots look closed but whose
    residual surface hides a forbidden residual.
    """

    return ConstitutionalTestCase(
        origin_law="No closure with hidden residuals.",
        branch_name="hidden-residual branch",
        constitutional_chain=(
            "SlotGraph",
            "Gamma",
            "ResidualVisibility",
            "FailureTaxonomy",
            "TraceCandidate",
        ),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.HIDDEN_RESIDUAL,
        forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )


def _minimally_closed_case() -> ConstitutionalTestCase:
    """Reference positive case used to prove the closure branch."""

    return ConstitutionalTestCase(
        origin_law="Closure without hidden residuals is minimally closed.",
        branch_name="all-required-slots-closed branch",
        constitutional_chain=(
            "SlotGraph",
            "Gamma",
            "RankCeiling",
            "ResidualVisibility",
            "Trace",
            "OutputBoundary",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE",),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
    )


# ---------------------------------------------------------------------------
# Schema: the case itself must declare origin / branch / chain / verdict.
# ---------------------------------------------------------------------------


def test_case_requires_non_empty_origin_law() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalTestCase(
            origin_law="   ",
            branch_name="b",
            constitutional_chain=("SlotGraph",),
            expected_state=ClosureState.INVALID,
            expected_failure_code=FailureCode.CENTER_MISSING,
            forbidden_outputs=(),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
        )


def test_case_requires_non_empty_branch_name() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalTestCase(
            origin_law="some law",
            branch_name="",
            constitutional_chain=("SlotGraph",),
            expected_state=ClosureState.INVALID,
            expected_failure_code=FailureCode.CENTER_MISSING,
            forbidden_outputs=(),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
        )


def test_case_requires_non_empty_constitutional_chain() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalTestCase(
            origin_law="law",
            branch_name="branch",
            constitutional_chain=(),
            expected_state=ClosureState.INVALID,
            expected_failure_code=FailureCode.CENTER_MISSING,
            forbidden_outputs=(),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
        )


def test_case_rejects_blank_chain_layer() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalTestCase(
            origin_law="law",
            branch_name="branch",
            constitutional_chain=("SlotGraph", " "),
            expected_state=ClosureState.INVALID,
            expected_failure_code=FailureCode.CENTER_MISSING,
            forbidden_outputs=(),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
        )


def test_closure_verdict_must_not_name_a_failure_code() -> None:
    """Docs/12 §4: ``Every rejection must be named.`` Conversely, a
    closure verdict must not pretend to refuse anything."""

    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalTestCase(
            origin_law="closure law",
            branch_name="branch",
            constitutional_chain=("SlotGraph", "Gamma"),
            expected_state=ClosureState.MINIMALLY_CLOSED,
            expected_failure_code=FailureCode.CENTER_MISSING,
            forbidden_outputs=(),
            max_rank=Rank.CANDIDATE,
            required_trace=True,
            required_residual_visibility=True,
        )


def test_refusal_verdict_must_name_a_failure_code() -> None:
    """Anti-agent-hallucination rule: a test cannot assert ``not
    approved`` without naming the refusal."""

    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalTestCase(
            origin_law="refusal law",
            branch_name="branch",
            constitutional_chain=("SlotGraph",),
            expected_state=ClosureState.INVALID,
            expected_failure_code=None,
            forbidden_outputs=(),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
        )


def test_case_rejects_non_enum_expected_state() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalTestCase(
            origin_law="law",
            branch_name="branch",
            constitutional_chain=("SlotGraph",),
            expected_state="INVALID",  # type: ignore[arg-type]
            expected_failure_code=FailureCode.CENTER_MISSING,
            forbidden_outputs=(),
            max_rank=Rank.ZERO,
            required_trace=True,
            required_residual_visibility=True,
        )


# ---------------------------------------------------------------------------
# Assertion helper: refuse to silently accept a partial pass.
# ---------------------------------------------------------------------------


def test_assert_helper_accepts_exact_match_for_negative_branch() -> None:
    case = _hidden_residual_case()
    result = ConstitutionalChainResult(
        state=ClosureState.INVALID,
        failure_code=FailureCode.HIDDEN_RESIDUAL,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )

    assert_constitutional_case(case, result)


def test_assert_helper_accepts_exact_match_for_positive_branch() -> None:
    case = _minimally_closed_case()
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset({"CANDIDATE_OUTPUT"}),
    )

    assert_constitutional_case(case, result)


def test_assert_helper_fails_when_state_mismatches() -> None:
    case = _hidden_residual_case()
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
    )

    with pytest.raises(AssertionError):
        assert_constitutional_case(case, result)


def test_assert_helper_fails_when_failure_code_mismatches() -> None:
    case = _hidden_residual_case()
    result = ConstitutionalChainResult(
        state=ClosureState.INVALID,
        failure_code=FailureCode.CENTER_MISSING,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
    )

    with pytest.raises(AssertionError):
        assert_constitutional_case(case, result)


def test_assert_helper_fails_when_rank_exceeds_ceiling() -> None:
    """Anti-agent-hallucination: green state + over-ceiling rank is
    still a constitutional failure."""

    case = _minimally_closed_case()
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CERTIFICATE,
        residual_visibility=True,
        trace_present=True,
    )

    with pytest.raises(AssertionError):
        assert_constitutional_case(case, result)


def test_assert_helper_fails_when_trace_is_missing() -> None:
    case = _minimally_closed_case()
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=False,
    )

    with pytest.raises(AssertionError):
        assert_constitutional_case(case, result)


def test_assert_helper_fails_when_residual_visibility_is_missing() -> None:
    case = _minimally_closed_case()
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=False,
        trace_present=True,
    )

    with pytest.raises(AssertionError):
        assert_constitutional_case(case, result)


def test_assert_helper_fails_when_forbidden_output_is_produced() -> None:
    case = _minimally_closed_case()
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset({"CERTIFICATE"}),
    )

    with pytest.raises(AssertionError):
        assert_constitutional_case(case, result)


# ---------------------------------------------------------------------------
# Provenance: the documents that bind this harness must remain present.
# ---------------------------------------------------------------------------


def test_constitutional_geometry_docs_are_present() -> None:
    """If any of these documents disappears, the harness is unmoored.

    These checks are intentionally cheap and string-based: the
    point is to fail a PR that ships harness changes without their
    governing law.
    """

    import pathlib

    repo_root = pathlib.Path(__file__).resolve().parent.parent
    for relative in (
        "docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md",
        "docs/13_CONSTITUTIONAL_PR_GEOMETRY.md",
        "docs/14_PR_CHAIN_ROADMAP.md",
        ".github/pull_request_template.md",
    ):
        path = repo_root / relative
        assert path.is_file(), f"missing constitutional document: {relative}"
        assert path.read_text(encoding="utf-8").strip(), (
            f"constitutional document is empty: {relative}"
        )
