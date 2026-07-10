"""Acceptance tests for docs/83 — Licensed Link Operators Surface Geometry Law.

Origin law     : docs/83 (LGE-LINK-L0)
Branch         : LGE-LINK-L0 (law-only link-operator boundary)
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
_DOC_83 = _REPO_ROOT / "docs" / "83_LINK_OPERATOR_SURFACE_GEOMETRY_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/83_LINK_OPERATOR_SURFACE_GEOMETRY_LAW.md",
        branch_name=f"LGE-LINK-L0 ({branch_note})",
        constitutional_chain=("docs/83", "LGE-LINK-L0"),
        chain_position="LGE-LINK-L0 law-only link-operator surface boundary",
        origin_law_ref="docs/83_LINK_OPERATOR_SURFACE_GEOMETRY_LAW.md#1-governing-law",
        branch_of_origin=(
            "Law-only boundary: link tools open relation-demand surface and do not "
            "produce relation closure/ifadah/hukm/truth."
        ),
        forbidden_shortcut_assertions=(
            "LinkTool -> Ifadah",
            "LinkTool -> Truth",
            "Particle -> Meaning",
            "Harf -> FinalRelation",
            "RelationDemand -> Hukm",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "FinalRelation",
            "FinalMeaning",
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


def test_docs_83_exists_and_declares_lge_link_identity() -> None:
    _declare("document presence and identity")
    assert _DOC_83.exists(), "docs/83 must exist"
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "83 — Licensed Link Operators Surface Geometry Law (LGE-LINK-L0)",
        "FAMILY               = LGE-LINK",
        "STEP                 = LGE-LINK-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = LINK_OPERATOR_SURFACE_GEOMETRY",
    ):
        assert marker in body


def test_docs_83_declares_relation_demand_not_relation_closure() -> None:
    _declare("governing relation-demand boundary")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "LinkTool DOES_NOT_IMPLY RelationClosure",
        "LinkTool DOES_IMPLY RelationDemand",
        "No link tool without demand.",
    ):
        assert marker in body


def test_docs_83_declares_allowed_outputs_and_forbidden_shortcuts() -> None:
    _declare("allowed/forbidden output boundary")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "LinkOperatorCandidate",
        "RelationDemandSurface",
        "LinkAttachmentReadiness",
        "LinkTool -> Ifadah",
        "LinkTool -> Truth",
        "Particle -> Meaning",
        "Harf -> FinalRelation",
        "RelationDemand -> Hukm",
        "FinalRelation",
        "FinalMeaning",
        "Ifadah",
        "Hukm",
        "Truth",
        "Certainty",
        "Reality",
    ):
        assert marker in body


def test_docs_83_declares_mrk_and_local_residual_vocabulary() -> None:
    _declare("mrk and residual discipline")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "MRK(LinkTool)",
        "ToolIdentity",
        "LinkFamily",
        "DemandType",
        "LeftAttachmentRequired",
        "RightAttachmentRequired",
        "TraceRef",
        "LINK_TOOL_UNKNOWN",
        "RIGHT_COMPLEMENT_MISSING",
        "LEFT_ANCHOR_MISSING",
        "CAUSAL_PROOF_PENDING",
        "MAQAM_CONTEXT_REQUIRED",
    ):
        assert marker in body


def test_docs_83_declares_staging_order_and_runtime_embargo() -> None:
    _declare("staging order and runtime embargo")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "LGE-LINK-L0",
        "LGE-LINK-C1",
        "LGE-LINK-G1",
        "LGE-LINK-T1",
        "LGE-LINK-R1",
        "EvidenceFitnessCarrier",
        "TraceReplayVerifier",
        "RankVector/DomainPolicy",
        "RUNTIME_NOT_OPENED = {",
        "parser_changes",
        "semantic_engine",
        "truth_engine",
    ):
        assert marker in body
