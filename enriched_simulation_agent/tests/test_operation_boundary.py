from __future__ import annotations

import pytest
from sim_agent.operation_boundary import (
    BoundaryStatus,
    CandidateProposal,
    ClosureState,
    DomainContext,
    EvidenceItem,
    ExplicitResultKind,
    OperationContract,
    authorize,
    execute_effect,
    process,
)


def _effect_ok(ctx) -> dict[str, str]:
    return {
        "output_id": "out-1",
        "RootId": ctx.proposal.identity_snapshot["RootId"],
        "CarrierId": ctx.proposal.identity_snapshot["CarrierId"],
    }


def _effect_break_identity(ctx) -> dict[str, str]:
    return {
        "output_id": "out-2",
        "RootId": "mutated-root",
        "CarrierId": ctx.proposal.identity_snapshot["CarrierId"],
    }


def _contract(effect_fn) -> OperationContract:
    return OperationContract(
        operation_id="WEIGH",
        source_types=frozenset({"LetterCarrier"}),
        target_type="AtomicPhonologicalUnit",
        domain="Morphology",
        preconditions=("RootLicensed", "SurfaceComplete"),
        evidence_policy=frozenset({"MorphEvidence"}),
        blockers=frozenset({"BLOCKING_RESIDUAL"}),
        identity_policy=frozenset({"RootId", "CarrierId"}),
        effect_function=effect_fn,
        rank_policy=2,
        residual_policy=("DOMAIN_BRIDGE_UNPROVEN",),
        transition_policy=("READY_FOR_SYNTAX", "NOT_READY_FOR_SEMANTICS"),
    )


def _proposal() -> CandidateProposal:
    return CandidateProposal(
        operation_id="WEIGH",
        input_ids=("c1",),
        input_types=("LetterCarrier",),
        target_type="AtomicPhonologicalUnit",
        source_domain="Morphology",
        target_domain="Morphology",
        evidence_ids=("ev1",),
        expected_effect="derive_pattern",
        identity_snapshot={
            "RootLicensed": "yes",
            "SurfaceComplete": "yes",
            "RootId": "r-1",
            "CarrierId": "car-1",
        },
        input_rank=3,
    )


def _evidence() -> tuple[EvidenceItem, ...]:
    return (
        EvidenceItem(
            evidence_id="ev1",
            evidence_type="MorphEvidence",
            source="golden-dataset",
            domain="Morphology",
            rank=2,
        ),
    )


def test_authorize_defined_for_valid_boundary() -> None:
    decision = authorize(
        proposal=_proposal(),
        contract=_contract(_effect_ok),
        evidence=_evidence(),
        context=DomainContext(bridge_rank=2),
        active_blockers=frozenset(),
    )
    assert decision.is_approved
    assert decision.boundary_status == BoundaryStatus.DEFINED
    assert decision.approved_context is not None


def test_process_success_returns_trace_and_readiness() -> None:
    result = process(
        proposal=_proposal(),
        contract=_contract(_effect_ok),
        evidence=_evidence(),
        context=DomainContext(bridge_rank=2),
        active_blockers=frozenset(),
    )
    assert result.kind == ExplicitResultKind.SUCCESS
    assert result.status == BoundaryStatus.DEFINED
    assert result.trace is not None
    assert result.closure_state == ClosureState.CLOSED_WITH_RESIDUALS
    assert result.transition_readiness == ("READY_FOR_SYNTAX", "NOT_READY_FOR_SEMANTICS")
    assert any(res.code == "RANK_LIMITED" for res in result.residuals)


def test_process_type_mismatch_is_undefined() -> None:
    bad = CandidateProposal(
        **{**_proposal().__dict__, "input_types": ("RootCandidate",)}
    )
    result = process(
        proposal=bad,
        contract=_contract(_effect_ok),
        evidence=_evidence(),
        context=DomainContext(bridge_rank=2),
    )
    assert result.kind == ExplicitResultKind.UNDEFINED
    assert result.failure_code == "TYPE_MISMATCH"


def test_process_missing_precondition_is_deferred() -> None:
    bad = CandidateProposal(
        **{
            **_proposal().__dict__,
            "identity_snapshot": {"RootLicensed": "yes", "RootId": "r-1", "CarrierId": "car-1"},
        }
    )
    result = process(
        proposal=bad,
        contract=_contract(_effect_ok),
        evidence=_evidence(),
        context=DomainContext(bridge_rank=2),
    )
    assert result.kind == ExplicitResultKind.DEFERRED
    assert result.failure_code == "PRECONDITION_MISSING"


def test_process_blocker_is_blocked() -> None:
    result = process(
        proposal=_proposal(),
        contract=_contract(_effect_ok),
        evidence=_evidence(),
        context=DomainContext(bridge_rank=2),
        active_blockers=frozenset({"BLOCKING_RESIDUAL"}),
    )
    assert result.kind == ExplicitResultKind.BLOCKED
    assert result.failure_code == "BLOCKING_RESIDUAL_PRESENT"


def test_process_identity_violation_returns_failure() -> None:
    result = process(
        proposal=_proposal(),
        contract=_contract(_effect_break_identity),
        evidence=_evidence(),
        context=DomainContext(bridge_rank=2),
    )
    assert result.kind == ExplicitResultKind.FAILURE
    assert result.failure_code == "IDENTITY_VIOLATION"
    assert result.closure_state == ClosureState.REOPEN_REQUIRED


def test_execute_effect_requires_approved_transition_context() -> None:
    with pytest.raises(TypeError, match="ApprovedTransitionContext"):
        execute_effect(_proposal())  # type: ignore[arg-type]

