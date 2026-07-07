"""Constitutional tests for X0R-E2 origin-branch licensing carriers.

Origin law     : docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md
Branch         : X0R-E2 OriginBranchLicensingContract carriers
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r import (
    OriginBranchLicensingContract,
    OriginBranchLicensingContractSchemaError,
    OriginBranchLinkSurface,
    OriginBranchReadinessState,
    OriginBranchResidual,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"
_README = _REPO_ROOT / "README.md"


def _declared_case() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md",
        branch_name="X0R-E2 OriginBranchLicensingContract carriers",
        constitutional_chain=("LAW-E0", "X0R-E1", "X0R-E2"),
        chain_position="X0R-E2",
        origin_law_ref="docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md#5-returning-branch-to-origin",
        branch_of_origin="Phase-2 runtime carrier implementation",
        forbidden_shortcut_assertions=(
            "X0R-E2 -> parser runtime",
            "X0R-E2 -> semantic/hukm/truth outputs",
            "X0R-E2 -> MGCM runtime",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ParserRuntime",
            "MorphologyRuntime",
            "SyntaxRuntime",
            "SemanticRuntime",
            "Ifadah",
            "Mafhum",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "Certificate",
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


def _valid_carrier() -> OriginBranchLicensingContract:
    trace_ref = "trace://x0r-e2/contract/001"
    return OriginBranchLicensingContract(
        domain="text_understanding",
        scope="GENERIC_ORIGIN_BRANCH_LICENSING_CONTRACT_CARRIERS_ONLY",
        trace_ref=trace_ref,
        link_surface=OriginBranchLinkSurface(
            asl_identification="asl://cell-sequence",
            far_identification="far://licensed-branch",
            shared_feature="shared://continuity",
            differentiating_feature="diff://licensed-boundary",
            common_illah="illah://constitutional-link",
            effective_description="desc://bounded-origin-branch-link",
            linking_sabab="sabab://licensed-handoff",
            preserved_condition="condition://continuity",
            absent_preventer="preventer://none",
            absent_qadih_difference="qadih://absent",
            preserved_identity=True,
            trace_ref=trace_ref,
            rank_ceiling=0,
            residual_visible=True,
        ),
        readiness=OriginBranchReadinessState.DEFERRED,
        residuals=(
            OriginBranchResidual(
                name="X0R_E2_CARRIER_ONLY",
                detail="X0R-E2 remains schema-only with no gate execution.",
                visible=True,
                blocking=False,
            ),
        ),
    )


def test_x0r_e2_declares_constitutional_origin_branch_and_chain() -> None:
    _declared_case()


def test_x0r_e2_carrier_surface_constructs_with_generic_schema_only() -> None:
    contract = _valid_carrier()
    assert contract.domain == "text_understanding"
    assert contract.scope == "GENERIC_ORIGIN_BRANCH_LICENSING_CONTRACT_CARRIERS_ONLY"
    assert contract.readiness is OriginBranchReadinessState.DEFERRED
    assert contract.link_surface.preserved_identity is True


def test_x0r_e2_rejects_trace_mismatch_across_carriers() -> None:
    with pytest.raises(OriginBranchLicensingContractSchemaError):
        OriginBranchLicensingContract(
            domain="text_understanding",
            scope="GENERIC_ORIGIN_BRANCH_LICENSING_CONTRACT_CARRIERS_ONLY",
            trace_ref="trace://x0r-e2/root",
            link_surface=OriginBranchLinkSurface(
                asl_identification="asl://cell-sequence",
                far_identification="far://licensed-branch",
                shared_feature="shared://continuity",
                differentiating_feature="diff://licensed-boundary",
                common_illah="illah://constitutional-link",
                effective_description="desc://bounded-origin-branch-link",
                linking_sabab="sabab://licensed-handoff",
                preserved_condition="condition://continuity",
                absent_preventer="preventer://none",
                absent_qadih_difference="qadih://absent",
                preserved_identity=True,
                trace_ref="trace://x0r-e2/other",
                rank_ceiling=0,
                residual_visible=True,
            ),
            readiness=OriginBranchReadinessState.LINK_READY,
        )


def test_x0r_e2_is_carrier_only_without_gate_execution_surface() -> None:
    contract = _valid_carrier()
    assert not hasattr(contract, "evaluate")
    assert not hasattr(contract, "decide")
    assert not hasattr(contract, "prove")


def test_chain_state_records_mark_x0r_e2_done_and_bounded() -> None:
    doc_14 = _DOC_14.read_text(encoding="utf-8")
    claude_md = _CLAUDE_MD.read_text(encoding="utf-8")
    readme = _README.read_text(encoding="utf-8")

    assert re.search(r"X0R-E2\s+OriginBranchLicensingContract\s+✓ done", doc_14)
    assert re.search(r"X0R-E2\s+OriginBranchLicensingContract\s+✓ done", claude_md)
    assert "`X0R-E2` origin-branch licensing carrier surface" in readme
