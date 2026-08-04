"""Constitutional tests for PR-F permit consumption + execution candidate.

Origin law     : docs/14 (PR-F registration) + docs/106 (consumption/execution-candidate boundary)
Branch         : PR-F Permit Consumption and Execution Candidate
Category       : Category 3 — Gate/operation-level bounded runtime tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r.canonical_domain_registry import DomainId, EvidenceKind, ResidualKind
from taaqqul_slot_geometry.x0r.canonical_transition_contract_registry import (
    TransitionContractId,
    canonical_transition_contract_registry,
)
from taaqqul_slot_geometry.x0r.pr_d1_transition_execution_preflight_hardening import (
    CarrierFieldValue,
    EvidenceRef,
    InputCarrierSnapshot,
    PreservedInvariant,
    TransitionExecutionPreflightHardeningRequest,
    compute_transition_contract_digest,
    evaluate_transition_execution_preflight_hardening,
)
from taaqqul_slot_geometry.x0r.pr_e_transition_permit_issuance import (
    TransitionPermit,
    TransitionPermitIssuanceRequest,
    issue_transition_permit,
)
from taaqqul_slot_geometry.x0r.pr_f_permit_consumption_execution_candidate import (
    CurrentRegistrySnapshot,
    ObservedInvariant,
    PermitLifecycleSnapshot,
    PRFExecutionFailureCode,
    PRFExecutionState,
    PRFPermitLifecycleState,
    TransitionExecutionRequest,
    consume_permit_and_emit_execution_candidate,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_106 = _REPO_ROOT / "docs" / "106_PERMIT_CONSUMPTION_EXECUTION_CANDIDATE_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/14_PR_CHAIN_ROADMAP.md + "
            "docs/106_PERMIT_CONSUMPTION_EXECUTION_CANDIDATE_LAW.md"
        ),
        branch_name=f"PR-F Permit Consumption and Execution Candidate ({branch_note})",
        constitutional_chain=("docs/14", "PR-E", "PR-F", "docs/106"),
        chain_position="PR-F consumes one permit atomically and emits ExecutionCandidate only",
        origin_law_ref="docs/106_PERMIT_CONSUMPTION_EXECUTION_CANDIDATE_LAW.md",
        branch_of_origin="Post-PR-E consumption/execution-candidate step",
        forbidden_shortcut_assertions=(
            "PR-F ExecutionCandidate -> PostflightApprovedExecution",
            "PR-F ExecutionCandidate -> CommitDecision",
            "PR-F ExecutionCandidate -> SemanticTruthClaim",
            "PR-F ExecutionCandidate -> HukmVerdict",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "PostflightVerdict",
            "CommitMutation",
            "SemanticTruth",
            "HukmVerdict",
            "RealityCertificate",
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


def _issued_permit() -> TransitionPermit:
    registry = canonical_transition_contract_registry()
    contract = registry.contract_by_id(TransitionContractId.TC_SR)

    preflight_request = TransitionExecutionPreflightHardeningRequest(
        request_id="req://pr-f/1",
        contract_id=TransitionContractId.TC_SR,
        domain=DomainId.LEXICON,
        input_carrier=InputCarrierSnapshot(
            carrier_id="carrier://src/1",
            carrier_kind="SourceSlot",
            input_identity="identity://source/1",
            predecessor_closure_ref="trace://x0r/pr-f/predecessor/1",
            field_values=(
                CarrierFieldValue("source_ref", "src-1"),
                CarrierFieldValue("span_ref", "span-1"),
                CarrierFieldValue("raw_text", "raw-1"),
                CarrierFieldValue("reading_evidence", "ev-1"),
                CarrierFieldValue("trace_ref", "trace://payload/1"),
            ),
            trace_ref="trace://carrier/1",
        ),
        evidence_refs=(
            EvidenceRef(
                evidence_id="evidence://1",
                kind=EvidenceKind.SOURCE_TEXT,
                provenance_ref="prov://a",
                subject_ref="identity://source/1",
                scope_ref="scope://lexicon",
                contract_id=TransitionContractId.TC_SR,
                evidence_rank=Rank.TRACE,
                trace_ref="trace://evidence/1",
                valid_until_epoch=2_000_000_000,
            ),
            EvidenceRef(
                evidence_id="evidence://2",
                kind=EvidenceKind.STRUCTURAL_VALIDATION,
                provenance_ref="prov://b",
                subject_ref="identity://source/1",
                scope_ref="scope://lexicon",
                contract_id=TransitionContractId.TC_SR,
                evidence_rank=Rank.TRACE,
                trace_ref="trace://evidence/2",
                valid_until_epoch=2_000_000_000,
            ),
        ),
        residual_kinds=(ResidualKind.NON_BLOCKING,),
        requested_rank=Rank.TRACE,
        preserved_invariants=(
            PreservedInvariant("input_identity", "identity://source/1"),
            PreservedInvariant("predecessor", "trace://x0r/pr-f/predecessor/1"),
        ),
        expected_domain_registry_version="canonical-domain-registry-v1",
        expected_contract_registry_version="canonical-transition-contract-registry-v1",
        expected_contract_digest=compute_transition_contract_digest(contract),
        trace_ref="trace://x0r/pr-f/request/1",
        request_epoch_seconds=1_900_000_000,
    )
    preflight = evaluate_transition_execution_preflight_hardening(preflight_request)

    permit_result = issue_transition_permit(
        TransitionPermitIssuanceRequest(
            permit_request_id="permit-req://pr-f/1",
            preflight_result=preflight,
            requested_output_types=("ReadingCandidate",),
            ttl_seconds=300,
            issue_at_epoch_seconds=1_900_000_100,
            trace_ref="trace://x0r/pr-f/permit/1",
        )
    )
    assert permit_result.permit is not None
    return permit_result.permit


def _request(*, permit: TransitionPermit) -> TransitionExecutionRequest:
    return TransitionExecutionRequest(
        execution_request_id="exec-req://pr-f/1",
        permit=permit,
        permit_lifecycle=PermitLifecycleSnapshot(
            permit_id=permit.permit_id,
            state=PRFPermitLifecycleState.ISSUED,
            consumed_nonces=(),
            revoked_permit_ids=(),
        ),
        input_carrier_snapshot=InputCarrierSnapshot(
            carrier_id="carrier://src/1",
            carrier_kind="SourceSlot",
            input_identity="identity://source/1",
            predecessor_closure_ref="trace://x0r/pr-f/predecessor/1",
            field_values=(
                CarrierFieldValue("source_ref", "src-1"),
                CarrierFieldValue("span_ref", "span-1"),
                CarrierFieldValue("raw_text", "raw-1"),
                CarrierFieldValue("reading_evidence", "ev-1"),
                CarrierFieldValue("trace_ref", "trace://payload/1"),
            ),
            trace_ref="trace://carrier/1",
        ),
        input_identity_pin="identity://source/1",
        executor_identity="executor://trusted/1",
        authorized_executors=("executor://trusted/1",),
        requested_operation="CARRIER_DECLARATION",
        requested_output_type="ReadingCandidate",
        output_candidate_ref="candidate://reading/1",
        observed_invariants=(
            ObservedInvariant("input_identity", "identity://source/1"),
            ObservedInvariant("contract_id", "TC_SR"),
        ),
        observed_residual_kinds=(ResidualKind.NON_BLOCKING,),
        current_time_epoch_seconds=1_900_000_200,
        current_registry_snapshot=CurrentRegistrySnapshot(
            expected_contract_registry_version="canonical-transition-contract-registry-v1",
        ),
        trace_ref="trace://x0r/pr-f/execute/1",
    )


def test_pr_f_consumes_permit_once_and_emits_execution_candidate_only() -> None:
    _declare("single atomic consumption and candidate-only output")
    permit = _issued_permit()

    result = consume_permit_and_emit_execution_candidate(_request(permit=permit))

    assert result.state is PRFExecutionState.EXECUTED
    assert result.failure_codes == ()
    assert result.consumed_nonce == permit.permit_nonce
    assert result.lifecycle_transition == (
        PRFPermitLifecycleState.ISSUED,
        PRFPermitLifecycleState.CONSUMED,
    )
    assert result.execution_candidate is not None
    candidate = result.execution_candidate
    assert candidate.postflight_required is True
    assert candidate.rank is Rank.ZERO
    assert candidate.execution_status == "EXECUTED"
    assert not hasattr(candidate, "approved_output")


def test_pr_f_refuses_when_permit_already_consumed() -> None:
    _declare("double consumption is refused")
    permit = _issued_permit()
    request = _request(permit=permit)
    request = TransitionExecutionRequest(
        execution_request_id=request.execution_request_id,
        permit=request.permit,
        permit_lifecycle=PermitLifecycleSnapshot(
            permit_id=permit.permit_id,
            state=PRFPermitLifecycleState.CONSUMED,
            consumed_nonces=(permit.permit_nonce,),
            revoked_permit_ids=(),
        ),
        input_carrier_snapshot=request.input_carrier_snapshot,
        input_identity_pin=request.input_identity_pin,
        executor_identity=request.executor_identity,
        authorized_executors=request.authorized_executors,
        requested_operation=request.requested_operation,
        requested_output_type=request.requested_output_type,
        output_candidate_ref=request.output_candidate_ref,
        observed_invariants=request.observed_invariants,
        observed_residual_kinds=request.observed_residual_kinds,
        current_time_epoch_seconds=request.current_time_epoch_seconds,
        current_registry_snapshot=request.current_registry_snapshot,
        trace_ref=request.trace_ref,
    )

    result = consume_permit_and_emit_execution_candidate(request)

    assert result.state is PRFExecutionState.REFUSED
    assert PRFExecutionFailureCode.PERMIT_ALREADY_CONSUMED in result.failure_codes
    assert result.execution_candidate is None


def test_pr_f_deferred_when_permit_expired() -> None:
    _declare("expired permit is deferred and cannot execute")
    permit = _issued_permit()
    request = _request(permit=permit)
    request = TransitionExecutionRequest(
        execution_request_id=request.execution_request_id,
        permit=request.permit,
        permit_lifecycle=request.permit_lifecycle,
        input_carrier_snapshot=request.input_carrier_snapshot,
        input_identity_pin=request.input_identity_pin,
        executor_identity=request.executor_identity,
        authorized_executors=request.authorized_executors,
        requested_operation=request.requested_operation,
        requested_output_type=request.requested_output_type,
        output_candidate_ref=request.output_candidate_ref,
        observed_invariants=request.observed_invariants,
        observed_residual_kinds=request.observed_residual_kinds,
        current_time_epoch_seconds=permit.expires_at_epoch,
        current_registry_snapshot=request.current_registry_snapshot,
        trace_ref=request.trace_ref,
    )

    result = consume_permit_and_emit_execution_candidate(request)

    assert result.state is PRFExecutionState.DEFERRED
    assert PRFExecutionFailureCode.PERMIT_EXPIRED in result.failure_codes


def test_pr_f_refuses_when_nonce_replay_detected() -> None:
    _declare("nonce replay is refused")
    permit = _issued_permit()
    request = _request(permit=permit)
    request = TransitionExecutionRequest(
        execution_request_id=request.execution_request_id,
        permit=request.permit,
        permit_lifecycle=PermitLifecycleSnapshot(
            permit_id=permit.permit_id,
            state=PRFPermitLifecycleState.ISSUED,
            consumed_nonces=(permit.permit_nonce,),
            revoked_permit_ids=(),
        ),
        input_carrier_snapshot=request.input_carrier_snapshot,
        input_identity_pin=request.input_identity_pin,
        executor_identity=request.executor_identity,
        authorized_executors=request.authorized_executors,
        requested_operation=request.requested_operation,
        requested_output_type=request.requested_output_type,
        output_candidate_ref=request.output_candidate_ref,
        observed_invariants=request.observed_invariants,
        observed_residual_kinds=request.observed_residual_kinds,
        current_time_epoch_seconds=request.current_time_epoch_seconds,
        current_registry_snapshot=request.current_registry_snapshot,
        trace_ref=request.trace_ref,
    )

    result = consume_permit_and_emit_execution_candidate(request)

    assert result.state is PRFExecutionState.REFUSED
    assert PRFExecutionFailureCode.PERMIT_NONCE_REPLAYED in result.failure_codes


def test_pr_f_refuses_when_contract_digest_mismatches_current_registry() -> None:
    _declare("contract digest pin must match current registry")
    permit = _issued_permit()
    forged_permit = TransitionPermit(
        permit_id=permit.permit_id,
        permit_nonce=permit.permit_nonce,
        request_id=permit.request_id,
        contract_id=permit.contract_id,
        allowed_output_types=permit.allowed_output_types,
        consumption_limit=permit.consumption_limit,
        issued_rank=permit.issued_rank,
        issued_at_epoch=permit.issued_at_epoch,
        expires_at_epoch=permit.expires_at_epoch,
        preflight_trace_ref=permit.preflight_trace_ref,
        permit_trace_ref=permit.permit_trace_ref,
        contract_digest="digest://mismatch",
        policy_digest=permit.policy_digest,
    )

    result = consume_permit_and_emit_execution_candidate(_request(permit=forged_permit))

    assert result.state is PRFExecutionState.REFUSED
    assert PRFExecutionFailureCode.CONTRACT_DIGEST_MISMATCH in result.failure_codes


def test_pr_f_refuses_when_input_identity_pin_mismatches_snapshot() -> None:
    _declare("input identity pin must match carrier identity")
    permit = _issued_permit()
    request = _request(permit=permit)
    request = TransitionExecutionRequest(
        execution_request_id=request.execution_request_id,
        permit=request.permit,
        permit_lifecycle=request.permit_lifecycle,
        input_carrier_snapshot=request.input_carrier_snapshot,
        input_identity_pin="identity://source/DIFFERENT",
        executor_identity=request.executor_identity,
        authorized_executors=request.authorized_executors,
        requested_operation=request.requested_operation,
        requested_output_type=request.requested_output_type,
        output_candidate_ref=request.output_candidate_ref,
        observed_invariants=request.observed_invariants,
        observed_residual_kinds=request.observed_residual_kinds,
        current_time_epoch_seconds=request.current_time_epoch_seconds,
        current_registry_snapshot=request.current_registry_snapshot,
        trace_ref=request.trace_ref,
    )

    result = consume_permit_and_emit_execution_candidate(request)

    assert result.state is PRFExecutionState.REFUSED
    assert PRFExecutionFailureCode.INPUT_IDENTITY_MISMATCH in result.failure_codes


def test_pr_f_refuses_when_requested_operation_does_not_match_contract() -> None:
    _declare("requested operation must match permit contract operation")
    permit = _issued_permit()
    request = _request(permit=permit)
    request = TransitionExecutionRequest(
        execution_request_id=request.execution_request_id,
        permit=request.permit,
        permit_lifecycle=request.permit_lifecycle,
        input_carrier_snapshot=request.input_carrier_snapshot,
        input_identity_pin=request.input_identity_pin,
        executor_identity=request.executor_identity,
        authorized_executors=request.authorized_executors,
        requested_operation="EXECUTION_CANDIDATE",
        requested_output_type=request.requested_output_type,
        output_candidate_ref=request.output_candidate_ref,
        observed_invariants=request.observed_invariants,
        observed_residual_kinds=request.observed_residual_kinds,
        current_time_epoch_seconds=request.current_time_epoch_seconds,
        current_registry_snapshot=request.current_registry_snapshot,
        trace_ref=request.trace_ref,
    )

    result = consume_permit_and_emit_execution_candidate(request)

    assert result.state is PRFExecutionState.REFUSED
    assert PRFExecutionFailureCode.REQUESTED_OPERATION_MISMATCH in result.failure_codes


def test_pr_f_refuses_when_executor_is_not_authorized() -> None:
    _declare("executor identity must be authorized")
    permit = _issued_permit()
    request = _request(permit=permit)
    request = TransitionExecutionRequest(
        execution_request_id=request.execution_request_id,
        permit=request.permit,
        permit_lifecycle=request.permit_lifecycle,
        input_carrier_snapshot=request.input_carrier_snapshot,
        input_identity_pin=request.input_identity_pin,
        executor_identity="executor://untrusted/1",
        authorized_executors=request.authorized_executors,
        requested_operation=request.requested_operation,
        requested_output_type=request.requested_output_type,
        output_candidate_ref=request.output_candidate_ref,
        observed_invariants=request.observed_invariants,
        observed_residual_kinds=request.observed_residual_kinds,
        current_time_epoch_seconds=request.current_time_epoch_seconds,
        current_registry_snapshot=request.current_registry_snapshot,
        trace_ref=request.trace_ref,
    )

    result = consume_permit_and_emit_execution_candidate(request)

    assert result.state is PRFExecutionState.REFUSED
    assert PRFExecutionFailureCode.EXECUTOR_NOT_AUTHORIZED in result.failure_codes


def test_docs_register_pr_f_and_law_file() -> None:
    _declare("chain/law synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    law = _DOC_106.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "PR-F  Permit Consumption and Execution Candidate" in roadmap
    assert "Amendment-81 (PR-F — Permit Consumption and Execution Candidate)" in roadmap
    assert "Status: constitutional execution-governor boundary + bounded runtime document." in law
    assert "TransitionExecutionRequest" in law
    assert "ExecutionCandidate" in law
    assert "No postflight approval from PR-F." in law
    assert "106_PERMIT_CONSUMPTION_EXECUTION_CANDIDATE_LAW.md" in index
