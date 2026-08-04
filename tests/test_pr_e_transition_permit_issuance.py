"""Constitutional tests for PR-E guardian-issued transition permit issuance.

Origin law     : docs/14 (PR-E registration) + docs/105 (permit boundary)
Branch         : PR-E Guardian-Issued Single-Use Transition Permit
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
    PRD1PreflightFailureCode,
    PRD1PreflightState,
    PreservedInvariant,
    TransitionExecutionPreflightHardeningRequest,
    compute_transition_contract_digest,
    evaluate_transition_execution_preflight_hardening,
)
from taaqqul_slot_geometry.x0r.pr_e_transition_permit_issuance import (
    PERMIT_MAX_TTL_SECONDS,
    PREPermitFailureCode,
    PREPermitState,
    TransitionPermitIssuanceRequest,
    issue_transition_permit,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_105 = _REPO_ROOT / "docs" / "105_GUARDIAN_SINGLE_USE_TRANSITION_PERMIT_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/14_PR_CHAIN_ROADMAP.md + "
            "docs/105_GUARDIAN_SINGLE_USE_TRANSITION_PERMIT_LAW.md"
        ),
        branch_name=f"PR-E Guardian-Issued Single-Use Transition Permit ({branch_note})",
        constitutional_chain=("docs/14", "PR-D.1", "PR-E", "docs/105"),
        chain_position="PR-E issues single-use permits from hardened preflight only",
        origin_law_ref="docs/105_GUARDIAN_SINGLE_USE_TRANSITION_PERMIT_LAW.md",
        branch_of_origin="Post-PR-D.1 permit issuance step",
        forbidden_shortcut_assertions=(
            "PR-E Permit -> TransitionExecution",
            "PR-E Permit -> CommitDecision",
            "PR-E Permit -> SemanticTruthClaim",
            "PR-E Permit -> HukmVerdict",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "TransitionExecution",
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


def _admissible_preflight_result() -> object:
    registry = canonical_transition_contract_registry()
    contract = registry.contract_by_id(TransitionContractId.TC_SR)
    request = TransitionExecutionPreflightHardeningRequest(
        request_id="req://pr-e/1",
        contract_id=TransitionContractId.TC_SR,
        domain=DomainId.LEXICON,
        input_carrier=InputCarrierSnapshot(
            carrier_id="carrier://src/1",
            carrier_kind="SourceSlot",
            input_identity="identity://source/1",
            predecessor_closure_ref="trace://x0r/pr-e/predecessor/1",
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
            PreservedInvariant("predecessor", "trace://x0r/pr-e/predecessor/1"),
        ),
        expected_domain_registry_version="canonical-domain-registry-v1",
        expected_contract_registry_version="canonical-transition-contract-registry-v1",
        expected_contract_digest=compute_transition_contract_digest(contract),
        trace_ref="trace://x0r/pr-e/request/1",
        request_epoch_seconds=1_900_000_000,
    )
    return evaluate_transition_execution_preflight_hardening(request)


def test_pr_e_grants_single_use_permit_from_admissible_preflight() -> None:
    _declare("permit issuance from hardened admissible preflight")
    preflight = _admissible_preflight_result()

    result = issue_transition_permit(
        TransitionPermitIssuanceRequest(
            permit_request_id="permit-req://1",
            preflight_result=preflight,
            requested_output_types=("ReadingCandidate",),
            ttl_seconds=300,
            issue_at_epoch_seconds=1_900_000_100,
            trace_ref="trace://x0r/pr-e/issue/1",
        )
    )

    assert result.state is PREPermitState.GRANTED
    assert result.failure_codes == ()
    assert result.permit is not None
    permit = result.permit
    assert permit.consumption_limit == 1
    assert permit.issued_rank is Rank.ZERO
    assert permit.allowed_output_types == ("ReadingCandidate",)
    assert permit.permit_trace_ref.startswith("trace://x0r/pr-e/permit/")
    assert not hasattr(permit, "execute")


def test_pr_e_refuses_when_requested_output_not_declared_by_preflight_contract() -> None:
    _declare("permit cannot expand contract output surface")
    preflight = _admissible_preflight_result()

    result = issue_transition_permit(
        TransitionPermitIssuanceRequest(
            permit_request_id="permit-req://2",
            preflight_result=preflight,
            requested_output_types=("UndeclaredOutput",),
            ttl_seconds=120,
            issue_at_epoch_seconds=1_900_000_200,
            trace_ref="trace://x0r/pr-e/issue/2",
        )
    )

    assert result.state is PREPermitState.REFUSED
    assert PREPermitFailureCode.REQUESTED_OUTPUT_NOT_DECLARED in result.failure_codes
    assert result.permit is None


def test_pr_e_deferred_when_preflight_is_deferred() -> None:
    _declare("permit waits when preflight remains deferred")
    preflight = _admissible_preflight_result()
    deferred_preflight = type(preflight)(
        request_id=preflight.request_id,
        contract_id=preflight.contract_id,
        state=PRD1PreflightState.DEFERRED,
        failure_codes=(PRD1PreflightFailureCode.REQUIRED_EVIDENCE_MISSING,),
        visible_residual_kinds=preflight.visible_residual_kinds,
        contract_declared_output_types=(),
        granted_rank=Rank.ZERO,
        request_trace_ref=preflight.request_trace_ref,
        preflight_trace_ref=preflight.preflight_trace_ref,
        parent_trace_ref=preflight.parent_trace_ref,
        domain_registry_version=preflight.domain_registry_version,
        contract_registry_version=preflight.contract_registry_version,
        contract_digest=preflight.contract_digest,
        policy_digest=preflight.policy_digest,
    )

    result = issue_transition_permit(
        TransitionPermitIssuanceRequest(
            permit_request_id="permit-req://3",
            preflight_result=deferred_preflight,
            requested_output_types=("ReadingCandidate",),
            ttl_seconds=120,
            issue_at_epoch_seconds=1_900_000_300,
            trace_ref="trace://x0r/pr-e/issue/3",
        )
    )

    assert result.state is PREPermitState.DEFERRED
    assert PREPermitFailureCode.PREFLIGHT_NOT_ADMISSIBLE in result.failure_codes


def test_pr_e_refuses_when_ttl_exceeds_maximum() -> None:
    _declare("single-use permit ttl cap")
    preflight = _admissible_preflight_result()

    result = issue_transition_permit(
        TransitionPermitIssuanceRequest(
            permit_request_id="permit-req://4",
            preflight_result=preflight,
            requested_output_types=("ReadingCandidate",),
            ttl_seconds=PERMIT_MAX_TTL_SECONDS + 1,
            issue_at_epoch_seconds=1_900_000_400,
            trace_ref="trace://x0r/pr-e/issue/4",
        )
    )

    assert result.state is PREPermitState.REFUSED
    assert PREPermitFailureCode.PERMIT_TTL_EXCEEDS_MAX in result.failure_codes


def test_docs_register_pr_e_and_law_file() -> None:
    _declare("chain/law synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    law = _DOC_105.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "PR-E  Guardian-Issued Single-Use Transition Permit" in roadmap
    assert "Amendment-80 (PR-E — Guardian-Issued Single-Use Transition Permit)" in roadmap
    assert "Status: constitutional execution-governor boundary + bounded runtime document." in law
    assert "TransitionPermit" in law
    assert "consumption_limit: 1" in law
    assert "No execution from permit issuance." in law
    assert "105_GUARDIAN_SINGLE_USE_TRANSITION_PERMIT_LAW.md" in index
