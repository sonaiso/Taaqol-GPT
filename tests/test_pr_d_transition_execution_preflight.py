"""Constitutional tests for PR-D bounded transition execution preflight.

Origin law     : docs/14 (PR-D registration) + docs/103 (preflight boundary)
Branch         : PR-D Canonical Transition Execution Preflight
Category       : Category 3 — Gate/operation-level bounded runtime tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r.canonical_domain_registry import DomainId, EvidenceKind, ResidualKind
from taaqqul_slot_geometry.x0r.canonical_transition_contract_registry import TransitionContractId
from taaqqul_slot_geometry.x0r.pr_d_transition_execution_preflight import (
    PRDPreflightFailureCode,
    PRDPreflightSchemaError,
    PRDPreflightState,
    TransitionExecutionPreflightRequest,
    TransitionExecutionPreflightResult,
    evaluate_transition_execution_preflight,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_103 = _REPO_ROOT / "docs" / "103_CANONICAL_TRANSITION_EXECUTION_PREFLIGHT_BOUNDARY_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/14_PR_CHAIN_ROADMAP.md + "
            "docs/103_CANONICAL_TRANSITION_EXECUTION_PREFLIGHT_BOUNDARY_LAW.md"
        ),
        branch_name=f"PR-D Canonical Transition Execution Preflight ({branch_note})",
        constitutional_chain=("docs/14", "PR-C", "PR-D", "docs/103"),
        chain_position="PR-D bounded execution-level preflight without execution",
        origin_law_ref="docs/103_CANONICAL_TRANSITION_EXECUTION_PREFLIGHT_BOUNDARY_LAW.md",
        branch_of_origin="Post-PR-C dedicated execution-level successor",
        forbidden_shortcut_assertions=(
            "TransitionExecutionPreflightResult -> TransitionExecution",
            "TransitionExecutionPreflightResult -> PermitIssuance",
            "TransitionExecutionPreflightResult -> CertificateIssuance",
            "TransitionExecutionPreflightResult -> SemanticTruthClaim",
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


def test_pr_d_admissible_preflight_yields_allowed_outputs_without_execution() -> None:
    _declare("admissible no-residual request")
    request = TransitionExecutionPreflightRequest(
        request_id="req://pr-d/1",
        contract_id=TransitionContractId.TC_SR,
        domain=DomainId.LEXICON,
        provided_fields=(
            "source_ref",
            "span_ref",
            "raw_text",
            "reading_evidence",
            "trace_ref",
        ),
        evidence_kinds=(EvidenceKind.SOURCE_TEXT, EvidenceKind.STRUCTURAL_VALIDATION),
        residual_kinds=(ResidualKind.NON_BLOCKING,),
        requested_rank=Rank.TRACE,
        trace_ref="trace://pr-d/test/admissible",
    )

    result = evaluate_transition_execution_preflight(request)

    assert result.state is PRDPreflightState.ADMISSIBLE_WITH_RESIDUALS
    assert result.failure_codes == ()
    assert result.allowed_outputs == ("ReadingCandidate",)
    assert result.granted_rank is Rank.ZERO
    assert not hasattr(result, "execute")


def test_pr_d_deferred_when_required_field_missing() -> None:
    _declare("missing required field defers")
    request = TransitionExecutionPreflightRequest(
        request_id="req://pr-d/2",
        contract_id=TransitionContractId.TC_SR,
        domain=DomainId.LEXICON,
        provided_fields=("source_ref", "span_ref", "raw_text", "trace_ref"),
        evidence_kinds=(EvidenceKind.SOURCE_TEXT, EvidenceKind.STRUCTURAL_VALIDATION),
        residual_kinds=(ResidualKind.NON_BLOCKING,),
        requested_rank=Rank.TRACE,
        trace_ref="trace://pr-d/test/deferred-field",
    )

    result = evaluate_transition_execution_preflight(request)

    assert result.state is PRDPreflightState.DEFERRED
    assert PRDPreflightFailureCode.REQUIRED_FIELD_MISSING in result.failure_codes
    assert result.allowed_outputs == ()


def test_pr_d_blocked_when_blocking_residual_present() -> None:
    _declare("blocking residual refusal")
    request = TransitionExecutionPreflightRequest(
        request_id="req://pr-d/3",
        contract_id=TransitionContractId.TC_SR,
        domain=DomainId.LEXICON,
        provided_fields=(
            "source_ref",
            "span_ref",
            "raw_text",
            "reading_evidence",
            "trace_ref",
        ),
        evidence_kinds=(EvidenceKind.SOURCE_TEXT, EvidenceKind.STRUCTURAL_VALIDATION),
        residual_kinds=(ResidualKind.BLOCKING,),
        requested_rank=Rank.TRACE,
        trace_ref="trace://pr-d/test/blocked",
    )

    result = evaluate_transition_execution_preflight(request)

    assert result.state is PRDPreflightState.BLOCKED
    assert PRDPreflightFailureCode.BLOCKING_RESIDUAL_PRESENT in result.failure_codes
    assert result.visible_residual_kinds == (ResidualKind.BLOCKING,)
    assert result.allowed_outputs == ()


def test_pr_d_invalid_on_domain_contract_mismatch() -> None:
    _declare("domain mismatch invalid")
    request = TransitionExecutionPreflightRequest(
        request_id="req://pr-d/4",
        contract_id=TransitionContractId.TC_SR,
        domain=DomainId.USM,
        provided_fields=(
            "source_ref",
            "span_ref",
            "raw_text",
            "reading_evidence",
            "trace_ref",
        ),
        evidence_kinds=(EvidenceKind.SOURCE_TEXT, EvidenceKind.STRUCTURAL_VALIDATION),
        residual_kinds=(ResidualKind.NON_BLOCKING,),
        requested_rank=Rank.TRACE,
        trace_ref="trace://pr-d/test/invalid-domain",
    )

    result = evaluate_transition_execution_preflight(request)

    assert result.state is PRDPreflightState.INVALID
    assert PRDPreflightFailureCode.CONTRACT_DOMAIN_MISMATCH in result.failure_codes
    assert result.allowed_outputs == ()


def test_pr_d_result_rejects_rank_promotion() -> None:
    _declare("rank-promotion refusal")
    with pytest.raises(PRDPreflightSchemaError, match="granted_rank"):
        TransitionExecutionPreflightResult(
            request_id="req://pr-d/5",
            contract_id=TransitionContractId.TC_SR,
            state=PRDPreflightState.ADMISSIBLE,
            failure_codes=(),
            visible_residual_kinds=(),
            allowed_outputs=("ReadingCandidate",),
            granted_rank=Rank.TRACE,
            trace_ref="trace://pr-d/test/rank-promotion",
        )


def test_docs_register_pr_d_and_preflight_law_file() -> None:
    _declare("chain/law synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    law = _DOC_103.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "PR-D  Canonical Transition Execution Preflight" in roadmap
    assert "Amendment-78 (PR-D — Canonical Transition Execution Preflight)" in roadmap
    assert (
        "Status: constitutional boundary + bounded execution-level preflight runtime document."
        in law
    )
    assert "ADMISSIBLE / ADMISSIBLE_WITH_RESIDUALS / DEFERRED / BLOCKED / INVALID" in law
    assert "103_CANONICAL_TRANSITION_EXECUTION_PREFLIGHT_BOUNDARY_LAW.md" in index
