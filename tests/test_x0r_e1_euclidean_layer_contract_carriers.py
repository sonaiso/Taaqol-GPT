"""Constitutional tests for X0R-E1 Euclidean layer-contract carriers.

Origin law     : docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md
Branch         : X0R-E1 Generic EuclideanLayerContract carriers
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r import (
    EuclideanLayerContract,
    EuclideanLayerContractSchemaError,
    LayerClosureStatus,
    LayerClosureSurface,
    LayerQuestionKind,
    LayerQuestionSet,
    LayerReadinessState,
    LayerResidual,
    LayerTransitionReadiness,
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
        branch_name="X0R-E1 Generic EuclideanLayerContract carriers",
        constitutional_chain=("LAW-E0", "X0R-E1-ADMIT", "X0R-E1"),
        chain_position="X0R-E1",
        origin_law_ref="docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md#9-roadmap-constraint",
        branch_of_origin="Phase-2 runtime carrier implementation",
        forbidden_shortcut_assertions=(
            "X0R-E1 -> parser runtime",
            "X0R-E1 -> semantic/hukm/truth outputs",
            "X0R-E1 -> MGCM runtime",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ParserRuntime",
            "MorphologyRuntime",
            "SyntaxRuntime",
            "SemanticRuntime",
            "Ifadah",
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


def _valid_carrier() -> EuclideanLayerContract:
    trace_ref = "trace://x0r-e1/contract/001"
    return EuclideanLayerContract(
        domain="text_understanding",
        scope="GENERIC_EUCLIDEAN_LAYER_CONTRACT_CARRIERS_ONLY",
        trace_ref=trace_ref,
        question_set=LayerQuestionSet(
            domain="text_understanding",
            trace_ref=trace_ref,
            questions=(
                LayerQuestionKind.CONDITION_OF_POSSIBILITY,
                LayerQuestionKind.MINIMUM_COMPLETE_LIMIT,
                LayerQuestionKind.OPENING,
                LayerQuestionKind.DEMAND,
                LayerQuestionKind.IDENTITY_PRESERVATION,
                LayerQuestionKind.CLOSURE,
                LayerQuestionKind.RESIDUAL,
                LayerQuestionKind.LICENSED_TRANSITION,
            ),
        ),
        closure_surface=LayerClosureSurface(
            layer_name="X0R-E1",
            status=LayerClosureStatus.BOUNDED,
            trace_ref=trace_ref,
            residual_visible=True,
        ),
        transition_readiness=LayerTransitionReadiness(
            source_layer="X0R-E1",
            target_layer="X0R-E2",
            readiness=LayerReadinessState.DEFERRED,
            trace_ref=trace_ref,
            residual_visible=True,
        ),
        residuals=(
            LayerResidual(
                name="X0R_E2_NOT_ADMITTED",
                detail="X0R-E2 remains the next staged runtime neighbor.",
                visible=True,
                blocking=False,
            ),
        ),
    )


def test_x0r_e1_declares_constitutional_origin_branch_and_chain() -> None:
    _declared_case()


def test_x0r_e1_carrier_surface_constructs_with_generic_schema_only() -> None:
    contract = _valid_carrier()
    assert contract.domain == "text_understanding"
    assert contract.scope == "GENERIC_EUCLIDEAN_LAYER_CONTRACT_CARRIERS_ONLY"
    assert contract.closure_surface.status is LayerClosureStatus.BOUNDED
    assert contract.transition_readiness.readiness is LayerReadinessState.DEFERRED


def test_x0r_e1_rejects_trace_or_domain_mismatch_across_carriers() -> None:
    with pytest.raises(EuclideanLayerContractSchemaError):
        EuclideanLayerContract(
            domain="text_understanding",
            scope="GENERIC_EUCLIDEAN_LAYER_CONTRACT_CARRIERS_ONLY",
            trace_ref="trace://x0r-e1/contract/root",
            question_set=LayerQuestionSet(
                domain="other_domain",
                trace_ref="trace://x0r-e1/contract/root",
                questions=(LayerQuestionKind.OPENING,),
            ),
            closure_surface=LayerClosureSurface(
                layer_name="X0R-E1",
                status=LayerClosureStatus.BOUNDED,
                trace_ref="trace://x0r-e1/contract/root",
                residual_visible=True,
            ),
            transition_readiness=LayerTransitionReadiness(
                source_layer="X0R-E1",
                target_layer="X0R-E2",
                readiness=LayerReadinessState.DEFERRED,
                trace_ref="trace://x0r-e1/contract/root",
                residual_visible=True,
            ),
        )


def test_x0r_e1_is_carrier_only_without_gate_execution_surface() -> None:
    contract = _valid_carrier()
    assert not hasattr(contract, "evaluate")
    assert not hasattr(contract, "decide")
    assert not hasattr(contract, "prove")


def test_chain_state_records_mark_x0r_e1_done_and_bounded() -> None:
    doc_14 = _DOC_14.read_text(encoding="utf-8")
    claude_md = _CLAUDE_MD.read_text(encoding="utf-8")
    readme = _README.read_text(encoding="utf-8")

    assert re.search(r"X0R-E1\s+Generic EuclideanLayerContract carriers\s+✓ done", doc_14)
    assert re.search(r"X0R-E1\s+Generic EuclideanLayerContract carriers\s+✓ done", claude_md)
    assert "X0R-E1 carrier surface" in readme
