"""Constitutional tests for PR-D.1 carrier-bound transition preflight hardening.

Origin law     : docs/14 (PR-D.1 registration) + docs/104 (hardening boundary)
Branch         : PR-D.1 Carrier-Bound Transition Preflight Hardening
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
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_104 = _REPO_ROOT / "docs" / "104_CARRIER_BOUND_TRANSITION_PREFLIGHT_HARDENING_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/14_PR_CHAIN_ROADMAP.md + "
            "docs/104_CARRIER_BOUND_TRANSITION_PREFLIGHT_HARDENING_LAW.md"
        ),
        branch_name=f"PR-D.1 Carrier-Bound Transition Preflight Hardening ({branch_note})",
        constitutional_chain=("docs/14", "PR-D", "PR-D.1", "docs/104"),
        chain_position="PR-D.1 hardens preflight with carrier/evidence/trace snapshot pins",
        origin_law_ref="docs/104_CARRIER_BOUND_TRANSITION_PREFLIGHT_HARDENING_LAW.md",
        branch_of_origin="Post-PR-D hardening step before permit issuance",
        forbidden_shortcut_assertions=(
            "PR-D.1 PreflightResult -> TransitionExecution",
            "PR-D.1 PreflightResult -> PermitIssuance",
            "PR-D.1 PreflightResult -> CertificateIssuance",
            "PR-D.1 PreflightResult -> SemanticTruthClaim",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "TransitionExecution",
            "TransitionCertificate",
            "PermitIssuance",
            "SemanticTruth",
            "HukmVerdict",
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


def _valid_request(
    *,
    requested_rank: Rank = Rank.TRACE,
    residual_kinds: tuple[ResidualKind, ...] = (ResidualKind.NON_BLOCKING,),
) -> TransitionExecutionPreflightHardeningRequest:
    registry = canonical_transition_contract_registry()
    contract = registry.contract_by_id(TransitionContractId.TC_SR)
    contract_digest = compute_transition_contract_digest(contract)

    return TransitionExecutionPreflightHardeningRequest(
        request_id="req://pr-d1/1",
        contract_id=TransitionContractId.TC_SR,
        domain=DomainId.LEXICON,
        input_carrier=InputCarrierSnapshot(
            carrier_id="carrier://src/1",
            carrier_kind="SourceSlot",
            input_identity="identity://source/1",
            predecessor_closure_ref="trace://x0r/pr-d1/predecessor/1",
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
        residual_kinds=residual_kinds,
        requested_rank=requested_rank,
        preserved_invariants=(
            PreservedInvariant("input_identity", "identity://source/1"),
            PreservedInvariant("predecessor", "trace://x0r/pr-d1/predecessor/1"),
        ),
        expected_domain_registry_version="canonical-domain-registry-v1",
        expected_contract_registry_version="canonical-transition-contract-registry-v1",
        expected_contract_digest=contract_digest,
        trace_ref="trace://x0r/pr-d1/request/1",
        request_epoch_seconds=1_900_000_000,
    )


def test_pr_d1_admissible_with_residuals_exposes_declared_outputs_and_trace_extension() -> None:
    _declare("admissible with explicit carrier/evidence pins")
    result = evaluate_transition_execution_preflight_hardening(_valid_request())

    assert result.state is PRD1PreflightState.ADMISSIBLE_WITH_RESIDUALS
    assert result.failure_codes == ()
    assert result.contract_declared_output_types == ("ReadingCandidate",)
    assert result.request_trace_ref == "trace://x0r/pr-d1/request/1"
    assert result.parent_trace_ref == result.request_trace_ref
    assert result.preflight_trace_ref.startswith("trace://x0r/pr-d1/preflight/")
    assert result.preflight_trace_ref != result.request_trace_ref
    assert result.granted_rank is Rank.ZERO


def test_pr_d1_blocks_when_requested_rank_exceeds_preflight_ceiling() -> None:
    _declare("requested-rank validity is separated from granted rank")
    result = evaluate_transition_execution_preflight_hardening(
        _valid_request(requested_rank=Rank.CANDIDATE)
    )

    assert result.state is PRD1PreflightState.BLOCKED
    assert PRD1PreflightFailureCode.REQUESTED_RANK_EXCEEDS_PREFLIGHT_CEILING in result.failure_codes
    assert result.contract_declared_output_types == ()


def test_pr_d1_defers_when_evidence_subject_does_not_bind_to_input_identity() -> None:
    _declare("evidence instance must bind to input identity")
    request = _valid_request()
    bad_evidence = EvidenceRef(
        evidence_id="evidence://3",
        kind=EvidenceKind.SOURCE_TEXT,
        provenance_ref="prov://bad",
        subject_ref="identity://different",
        scope_ref="scope://lexicon",
        contract_id=TransitionContractId.TC_SR,
        evidence_rank=Rank.TRACE,
        trace_ref="trace://evidence/3",
        valid_until_epoch=2_000_000_000,
    )
    request = TransitionExecutionPreflightHardeningRequest(
        request_id=request.request_id,
        contract_id=request.contract_id,
        domain=request.domain,
        input_carrier=request.input_carrier,
        evidence_refs=(bad_evidence, request.evidence_refs[1]),
        residual_kinds=request.residual_kinds,
        requested_rank=request.requested_rank,
        preserved_invariants=request.preserved_invariants,
        expected_domain_registry_version=request.expected_domain_registry_version,
        expected_contract_registry_version=request.expected_contract_registry_version,
        expected_contract_digest=request.expected_contract_digest,
        trace_ref=request.trace_ref,
        request_epoch_seconds=request.request_epoch_seconds,
    )

    result = evaluate_transition_execution_preflight_hardening(request)

    assert result.state is PRD1PreflightState.DEFERRED
    assert PRD1PreflightFailureCode.EVIDENCE_SUBJECT_MISMATCH in result.failure_codes


def test_pr_d1_invalid_when_contract_digest_pin_does_not_match_snapshot() -> None:
    _declare("replay-safe contract digest pin mismatch")
    request = _valid_request()
    request = TransitionExecutionPreflightHardeningRequest(
        request_id=request.request_id,
        contract_id=request.contract_id,
        domain=request.domain,
        input_carrier=request.input_carrier,
        evidence_refs=request.evidence_refs,
        residual_kinds=request.residual_kinds,
        requested_rank=request.requested_rank,
        preserved_invariants=request.preserved_invariants,
        expected_domain_registry_version=request.expected_domain_registry_version,
        expected_contract_registry_version=request.expected_contract_registry_version,
        expected_contract_digest="digest://mismatch",
        trace_ref=request.trace_ref,
        request_epoch_seconds=request.request_epoch_seconds,
    )

    result = evaluate_transition_execution_preflight_hardening(request)

    assert result.state is PRD1PreflightState.INVALID
    assert PRD1PreflightFailureCode.CONTRACT_DIGEST_MISMATCH in result.failure_codes


def test_docs_register_pr_d1_and_law_file() -> None:
    _declare("chain/law synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    law = _DOC_104.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "PR-D.1  Carrier-Bound Transition Preflight Hardening" in roadmap
    assert "Amendment-79 (PR-D.1 — Carrier-Bound Transition Preflight Hardening)" in roadmap
    assert "Status: constitutional hardening boundary + bounded runtime document." in law
    assert "input_carrier" in law
    assert "evidence_refs" in law
    assert "contract_digest" in law
    assert "104_CARRIER_BOUND_TRANSITION_PREFLIGHT_HARDENING_LAW.md" in index
