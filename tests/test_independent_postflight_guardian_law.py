"""Constitutional tests for docs/111 independent postflight guardian law.

Origin law     : docs/111 (Independent Postflight Guardian Law)
Branch         : PR-G independent postflight guardian
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_111 = _REPO_ROOT / "docs" / "111_INDEPENDENT_POSTFLIGHT_GUARDIAN_LAW.md"
_DOC_110 = _REPO_ROOT / "docs" / "110_RUNTIME_ADMISSION_BY_INDEPENDENT_RATIFICATION_LAW.md"
_DOC_106 = _REPO_ROOT / "docs" / "106_PERMIT_CONSUMPTION_EXECUTION_CANDIDATE_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/111_INDEPENDENT_POSTFLIGHT_GUARDIAN_LAW.md",
        branch_name=f"PR-G Independent Postflight Guardian ({branch_note})",
        constitutional_chain=("docs/106", "docs/110", "docs/111"),
        chain_position="PR-G opens independent postflight evaluation only",
        origin_law_ref="docs/111_INDEPENDENT_POSTFLIGHT_GUARDIAN_LAW.md",
        branch_of_origin="Post-PR-F execution-governor completion path",
        forbidden_shortcut_assertions=(
            "ExecutionCandidate -> CommitDecision",
            "ExecutionCandidate -> CertificateIssuance",
            "ExecutionCandidate -> SemanticTruth",
            "ExecutionCandidate -> HukmVerdict",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "CommitDecision",
            "CanonicalMutation",
            "CertificateIssuance",
            "SemanticTruthClosure",
            "HukmClosure",
            "RealityCertificate",
            "RankPromotion",
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


def test_docs_111_exists_and_is_law_only_surface() -> None:
    _declare("law-only boundary registration")
    body = _DOC_111.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "Status: constitutional execution-governor boundary document (law-only)." in body
    assert "This step introduces no runtime code." in body
    assert "111_INDEPENDENT_POSTFLIGHT_GUARDIAN_LAW.md" in index


def test_docs_111_declares_closed_postflight_verdict_vocabulary() -> None:
    _declare("closed postflight verdict vocabulary")
    body = _DOC_111.read_text(encoding="utf-8")

    assert "POSTFLIGHT_APPROVED" in body
    assert "POSTFLIGHT_REJECTED" in body
    assert "POSTFLIGHT_SUSPENDED" in body
    assert "No other postflight state is licensed in this step." in body


def test_docs_111_requires_independent_rechecks_and_refusal_families() -> None:
    _declare("independent recheck + refusal discipline")
    body = _DOC_111.read_text(encoding="utf-8")

    for marker in (
        "input_identity",
        "requested_output_type",
        "observed_invariants",
        "observed_residual_kinds",
        "trace_ref",
        "Rank.ZERO",
        "permit/contract continuity",
    ):
        assert marker in body

    for failure in (
        "POSTFLIGHT_INPUT_IDENTITY_MISMATCH",
        "POSTFLIGHT_OUTPUT_TYPE_MISMATCH",
        "POSTFLIGHT_INVARIANT_BREAK",
        "POSTFLIGHT_TRACE_CONTINUITY_BROKEN",
        "POSTFLIGHT_RANK_ABOVE_ZERO",
        "POSTFLIGHT_PERMIT_CONTRACT_CONTINUITY_BROKEN",
        "POSTFLIGHT_BLOCKING_RESIDUAL_PRESENT",
        "POSTFLIGHT_EVIDENCE_CONTINUITY_MISSING",
    ):
        assert failure in body


def test_docs_111_binds_to_docs_110_runtime_admission_and_forbids_commit_path() -> None:
    _declare("runtime-admission binding + commit embargo")
    law_111 = _DOC_111.read_text(encoding="utf-8")
    law_110 = _DOC_110.read_text(encoding="utf-8")
    law_106 = _DOC_106.read_text(encoding="utf-8")

    assert "LawRatified(111)" in law_111
    assert "ProofObjectsPass(111)" in law_111
    assert "CountermodelsPass(111)" in law_111
    assert "ReconstructionStable(111)" in law_111
    assert "NegativeRegressionStable(111)" in law_111
    assert "ResidualRegressionStable(111)" in law_111
    assert "Law -> ProofObjects -> Countermodels -> Regression -> RuntimeAdmission" in law_111

    assert "Not(POSTFLIGHT_APPROVED) => Not(Commit)" in law_111
    assert "NoCanonicalMutationBeforeCommit." in law_111
    assert "ExecutionCandidate.postflight_required = True" in law_111
    assert "postflight_required: True," in law_106
    assert "Runtime implements proven law; runtime does not prove its own law." in law_110
