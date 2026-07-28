"""Constitutional tests for PR-141 transition carrier surfaces.

Origin law     : docs/13_CONSTITUTIONAL_PR_GEOMETRY.md
Branch         : PR-141 transition carriers/dataclasses only
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r import (
    ApprovedTransitionContext,
    ConstitutionalForgeryError,
    GuardianDecision,
    GuardianDecisionStatus,
    TransitionProposal,
    TransitionSurfaceSchemaError,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)


def _declared_case(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/13_CONSTITUTIONAL_PR_GEOMETRY.md",
        branch_name=f"PR-141 transition carriers ({branch_note})",
        constitutional_chain=("docs/12", "docs/13", "PR-141"),
        chain_position="PR-141",
        origin_law_ref="docs/13_CONSTITUTIONAL_PR_GEOMETRY.md#4-operational-pr-template",
        branch_of_origin=(
            "Carrier-only transition surfaces for executor->guardian->approved-context"
        ),
        forbidden_shortcut_assertions=(
            "PR-141 -> runtime execution engine",
            "PR-141 -> guardian verdict engine",
            "PR-141 -> semantic/hukm/truth outputs",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ExecutionEngine",
            "GateExecution",
            "SemanticRuntime",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
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


def _proposal() -> TransitionProposal:
    return TransitionProposal(
        proposal_id="proposal://pr-141/001",
        source_layer="PRECOMP-L0",
        target_layer="IFADAH-CANDIDATE",
        input_identity="input://lexeme/katib",
        operation_id="op://ifadah/propose",
        candidate_output="output://ifadah/candidate/surface/001",
        preserved_invariants=("trace-preserved", "rank-bounded"),
        changed_properties=("scope-resolved",),
        evidence=("evidence://surface/001",),
        residuals=("residual://deferred/001",),
        trace_id="trace://pr-141/001",
        claimed_rank="CANDIDATE",
    )


def test_pr_141_declares_constitutional_surface() -> None:
    _declared_case("constitutional declaration")


def test_pr_141_transition_carriers_construct_as_schema_only() -> None:
    proposal = _proposal()
    decision = GuardianDecision(
        decision_id="decision://pr-141/001",
        proposal_id=proposal.proposal_id,
        status=GuardianDecisionStatus.APPROVED_WITH_RESIDUALS,
        approved_rank="CANDIDATE",
        nonblocking_residuals=("residual://nonblocking/001",),
        failure_codes=(),
        trace_reference=proposal.trace_id,
    )
    context = ApprovedTransitionContext.from_guardian(
        decision=decision,
        proposal=proposal,
        output_identity="output://ifadah/candidate/001",
    )

    assert decision.proposal_id == proposal.proposal_id
    assert context.decision_id == decision.decision_id
    assert context.trace_id == proposal.trace_id


def test_pr_141_rejects_approved_guardian_decision_without_rank() -> None:
    with pytest.raises(TransitionSurfaceSchemaError):
        GuardianDecision(
            decision_id="decision://pr-141/invalid/001",
            proposal_id="proposal://pr-141/001",
            status=GuardianDecisionStatus.APPROVED,
            approved_rank=None,
            nonblocking_residuals=(),
            failure_codes=(),
            trace_reference="trace://pr-141/001",
        )


def test_pr_141_rejects_rejected_guardian_decision_without_failure_codes() -> None:
    with pytest.raises(TransitionSurfaceSchemaError):
        GuardianDecision(
            decision_id="decision://pr-141/invalid/002",
            proposal_id="proposal://pr-141/001",
            status=GuardianDecisionStatus.REJECTED,
            approved_rank=None,
            nonblocking_residuals=(),
            failure_codes=(),
            trace_reference="trace://pr-141/001",
        )


def test_pr_141_rejects_non_string_invariant_entries() -> None:
    with pytest.raises(TransitionSurfaceSchemaError):
        TransitionProposal(
            proposal_id="proposal://pr-141/invalid/001",
            source_layer="PRECOMP-L0",
            target_layer="IFADAH-CANDIDATE",
            input_identity="input://x",
            operation_id="op://x",
            candidate_output="output://x",
            preserved_invariants=("ok", 1),  # type: ignore[arg-type]
            changed_properties=("delta",),
            evidence=(),
            residuals=(),
            trace_id="trace://pr-141/invalid",
            claimed_rank="CANDIDATE",
        )


def test_pr_141_rejects_direct_approved_context_construction() -> None:
    with pytest.raises(ConstitutionalForgeryError):
        ApprovedTransitionContext(
            decision_id="decision://pr-141/001",
            source_layer="PRECOMP-L0",
            target_layer="IFADAH-CANDIDATE",
            input_identity="input://lexeme/katib",
            output_identity="output://ifadah/candidate/001",
            approved_operation="op://ifadah/propose",
            approved_rank="CANDIDATE",
            preserved_invariants=("trace-preserved", "rank-bounded"),
            nonblocking_residuals=("residual://nonblocking/001",),
            trace_id="trace://pr-141/001",
            _approval_token=object(),
        )


def test_pr_141_rejects_non_string_schema_entries() -> None:
    with pytest.raises(TransitionSurfaceSchemaError):
        TransitionProposal(
            proposal_id="proposal://pr-141/invalid/002",
            source_layer="PRECOMP-L0",
            target_layer="IFADAH-CANDIDATE",
            input_identity="input://x",
            operation_id="op://x",
            candidate_output="output://x",
            preserved_invariants=("trace-preserved",),
            changed_properties=("delta",),
            evidence=("evidence://ok", 1),  # type: ignore[arg-type]
            residuals=("residual://ok",),
            trace_id="trace://pr-141/invalid",
            claimed_rank="CANDIDATE",
        )

    with pytest.raises(TransitionSurfaceSchemaError):
        GuardianDecision(
            decision_id="decision://pr-141/invalid/003",
            proposal_id="proposal://pr-141/001",
            status=GuardianDecisionStatus.APPROVED_WITH_RESIDUALS,
            approved_rank="CANDIDATE",
            nonblocking_residuals=("residual://ok", object()),  # type: ignore[arg-type]
            failure_codes=(),
            trace_reference="trace://pr-141/001",
        )


def test_pr_141_is_carrier_only_without_execution_surface() -> None:
    proposal = _proposal()
    assert not hasattr(proposal, "evaluate")
    assert not hasattr(proposal, "execute")
    assert not hasattr(proposal, "prove")
