"""Acceptance tests for docs/95 AUX-ESA-1 post-merge verification record.

Origin law     : docs/94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md
Branch         : AUX-ESA-1 post-merge verification + harness plan
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
_DOC_95 = _REPO_ROOT / "docs" / "95_AUX_ESA_1_POST_MERGE_VERIFICATION_AND_HARNESS_PLAN.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md",
        branch_name=f"AUX-ESA-1 ({branch_note})",
        constitutional_chain=("docs/94", "AUX-ESA-1", "POST-MERGE-VERIFICATION"),
        chain_position="AUX-ESA-1 post-merge auxiliary verification record",
        origin_law_ref=(
            "docs/94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md#4-forbidden-"
            "transitions-and-outputs"
        ),
        branch_of_origin=(
            "Auxiliary verification/planning step that keeps quarantine boundaries and "
            "defers constitutional admission."
        ),
        forbidden_shortcut_assertions=(
            "AUX-ESA-1 -> docs/14_chain_unlock",
            "AUX-ESA-1 -> core_runtime_mutation",
            "AUX-ESA-1 -> linguistic_to_knowledge_bridge_proof",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ConstitutionalAdmissionCertificate",
            "RoadmapAdvanceClaim",
            "BridgeLicensedClaim",
            "RelationIfadahHukmUnlock",
            "GlobalConstitutionalVerdict",
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


def test_docs_95_exists_with_required_sections() -> None:
    _declare("document presence")
    body = _DOC_95.read_text(encoding="utf-8")

    required_markers = (
        "## §1 Verified merge and CI state",
        "## §2 Scope quarantine verification",
        "## §3 AUX-ESA law-coverage surface (v0)",
        "## §4 Known open limits after AUX-ESA-1",
        "## §5 Constitutional harness migration plan (not executed in this step)",
        "## §6 Post-merge validation record",
        "## §7 Final post-merge verdict",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_95_records_merge_scope_and_quarantine_assertions() -> None:
    _declare("merge and scope assertions")
    body = _DOC_95.read_text(encoding="utf-8")

    required_markers = (
        "c39a75a",
        "71e05dc",
        "`enriched_simulation_agent/**`",
        "`src/taaqqul_slot_geometry/**`",
        "`docs/14_PR_CHAIN_ROADMAP.md` remains unchanged",
        "WordCapability -> Relation` / `Ifadah` / `Hukm`",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_95_records_v0_law_coverage_and_open_limits() -> None:
    _declare("law coverage and open limits")
    body = _DOC_95.read_text(encoding="utf-8")

    required_markers = (
        "check_identity_simulation_law",
        "check_composition_simulation_law",
        "check_operation_homomorphism_law",
        "check_residual_reflection_law",
        "check_coverage_contract_law",
        "check_nontriviality_strengthening_law",
        "check_triad_mapping_hypothesis",
        "CoverageContract",
        "OperationPath",
        "ResidualMapping",
        "ResidualReflectionReport",
        "TriadMappingHypothesis",
        "composition checks transitions as provided and does not yet construct full `G∘F`",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_95_records_harness_plan_and_non_admission_verdict() -> None:
    _declare("harness plan and verdict")
    body = _DOC_95.read_text(encoding="utf-8")

    required_markers = (
        "define translation contract for `SOURCE_BLOCKER_UNMAPPED`",
        "`tests/support/constitutional_case.py`",
        "AUX_ESA_1_POST_MERGE_VERDICT = PASS_QUARANTINED",
        "constitutional_chain_status: NOT_ADMITTED",
        "roadmap_unlock: FORBIDDEN_AND_NOT_PRESENT",
        "bridge_claim_status: FORBIDDEN_AND_NOT_PRESENT",
        "constitutional_harness_migration: PLANNED_NOT_EXECUTED",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_index_references_docs_95_record() -> None:
    _declare("docs index mapping")
    index_body = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "95_AUX_ESA_1_POST_MERGE_VERIFICATION_AND_HARNESS_PLAN.md" in index_body
    assert "auxiliary" in index_body
    assert "post-merge verification + harness planning record" in index_body
