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

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    ConstitutionalSchemaError,
    ConstitutionalTestCase,
    assert_constitutional_case,
)


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


# ---------------------------------------------------------------------------
# PR-1C: ConstitutionalChainTestCase schema + chain-test docs presence.
# ---------------------------------------------------------------------------


def test_pr1c_constitutional_documents_are_present() -> None:
    """PR-1C ratifies docs 15/16/17. Their absence unmoors the
    ConstitutionalChainTestCase introduced alongside them.
    """

    import pathlib

    repo_root = pathlib.Path(__file__).resolve().parent.parent
    for relative in (
        "docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md",
        "docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md",
        "docs/17_SLOTGRAPH_GENERATION_LAW.md",
    ):
        path = repo_root / relative
        assert path.is_file(), f"missing PR-1C document: {relative}"
        assert path.read_text(encoding="utf-8").strip(), (
            f"PR-1C document is empty: {relative}"
        )


def _chain_case_kwargs(**overrides: object) -> dict[str, object]:
    """Reference kwargs for a refusal-branch chain case.

    Defaults form a valid case; tests below override one field at a
    time to prove the schema refuses each malformed declaration.
    """

    base: dict[str, object] = dict(
        origin_law="docs/17 §3 center-missing branch",
        branch_name="ctor-refuses-missing-center",
        constitutional_chain=("SlotGraph.Generation", "FailureTaxonomy"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.CENTER_MISSING,
        forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="SlotGraph.Generation.center",
        origin_law_ref=(
            "docs/17_SLOTGRAPH_GENERATION_LAW.md"
            "#3-the-constructor-refusal-table"
        ),
        branch_of_origin="No SlotGraph from raw value (missing-center sub-branch).",
        forbidden_shortcut_assertions=("Identity → Truth", "Candidate → Truth"),
    )
    base.update(overrides)
    return base


def test_chain_case_constructs_when_all_fields_are_valid() -> None:
    """Sanity check: the reference kwargs build a valid case."""

    case = ConstitutionalChainTestCase(**_chain_case_kwargs())  # type: ignore[arg-type]

    # A chain case is also a constitutional case.
    assert isinstance(case, ConstitutionalTestCase)
    assert case.chain_position == "SlotGraph.Generation.center"


def test_chain_case_requires_non_empty_chain_position() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalChainTestCase(**_chain_case_kwargs(chain_position="  "))  # type: ignore[arg-type]


def test_chain_case_requires_non_empty_origin_law_ref() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalChainTestCase(**_chain_case_kwargs(origin_law_ref=""))  # type: ignore[arg-type]


def test_chain_case_requires_non_empty_branch_of_origin() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalChainTestCase(**_chain_case_kwargs(branch_of_origin=""))  # type: ignore[arg-type]


def test_chain_case_rejects_non_string_forbidden_shortcut_entry() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalChainTestCase(
            **_chain_case_kwargs(forbidden_shortcut_assertions=("Identity → Truth", ""))  # type: ignore[arg-type]
        )


def test_chain_case_rejects_non_tuple_forbidden_shortcuts() -> None:
    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalChainTestCase(
            **_chain_case_kwargs(forbidden_shortcut_assertions=["Identity → Truth"])  # type: ignore[arg-type]
        )


def test_chain_case_closure_verdict_requires_at_least_one_shortcut() -> None:
    """docs/12 §9: a green closure verdict in a chain test is a
    partial pass unless it proves at least one forbidden neighbour.
    """

    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalChainTestCase(
            **_chain_case_kwargs(  # type: ignore[arg-type]
                expected_state=ClosureState.MINIMALLY_CLOSED,
                expected_failure_code=None,
                max_rank=Rank.CANDIDATE,
                forbidden_shortcut_assertions=(),
            )
        )


def test_chain_case_refusal_verdict_permits_empty_shortcuts() -> None:
    """Refusal verdicts already name a FailureCode; an empty
    forbidden_shortcut_assertions tuple is acceptable (though
    discouraged) because the named refusal alone proves the
    boundary held. The schema must therefore not raise.
    """

    case = ConstitutionalChainTestCase(
        **_chain_case_kwargs(forbidden_shortcut_assertions=())  # type: ignore[arg-type]
    )

    assert case.forbidden_shortcut_assertions == ()


def test_chain_case_inherits_parent_schema_rules() -> None:
    """A chain case is also a constitutional case; the parent rules
    (origin_law / branch_name / chain / verdict pairing) still bind.
    """

    with pytest.raises(ConstitutionalSchemaError):
        ConstitutionalChainTestCase(
            **_chain_case_kwargs(  # type: ignore[arg-type]
                expected_state=ClosureState.MINIMALLY_CLOSED,
                # A closure verdict that still names a failure code
                # violates the parent rule from docs/12 §4.
                expected_failure_code=FailureCode.CENTER_MISSING,
                max_rank=Rank.CANDIDATE,
            )
        )


# ---------------------------------------------------------------------------
# assert_constitutional_case: chain-aware step 11 (forbidden shortcuts).
# ---------------------------------------------------------------------------


def _positive_chain_case() -> ConstitutionalChainTestCase:
    """A positive (closure) chain case used by the assertion tests."""

    return ConstitutionalChainTestCase(
        origin_law="docs/16 §2 link 7 (Closure)",
        branch_name="closure-without-residuals-is-minimal",
        constitutional_chain=(
            "SlotGraph",
            "IdentityChain.link.7.Closure",
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
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref=(
            "docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md"
            "#2-the-ten-licensing-links"
        ),
        branch_of_origin="Closure is established (link 7 of 10).",
        forbidden_shortcut_assertions=(
            "Closure → Certificate",
            "Candidate → Truth",
        ),
    )


def test_assert_helper_accepts_chain_case_when_no_shortcut_produced() -> None:
    case = _positive_chain_case()
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset({"CANDIDATE_OUTPUT"}),
    )

    assert_constitutional_case(case, result)


def test_assert_helper_fails_when_forbidden_shortcut_is_produced() -> None:
    """docs/12 §9.2 step 11: a chain case rejects any result whose
    produced_outputs include a declared forbidden shortcut, even
    when state, failure code, rank, and residuals all match.
    """

    case = _positive_chain_case()
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset({"CANDIDATE_OUTPUT", "Closure → Certificate"}),
    )

    with pytest.raises(AssertionError):
        assert_constitutional_case(case, result)


def test_chain_case_origin_law_ref_points_at_a_real_file() -> None:
    """The origin_law_ref schema is textual, but a healthy chain
    case should point at a file that exists. We verify the two
    reference cases used in this module to keep the docs and the
    harness from drifting apart silently.
    """

    import pathlib

    repo_root = pathlib.Path(__file__).resolve().parent.parent
    for ref in (
        "docs/17_SLOTGRAPH_GENERATION_LAW.md",
        "docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md",
    ):
        assert (repo_root / ref).is_file(), f"origin_law_ref target missing: {ref}"
