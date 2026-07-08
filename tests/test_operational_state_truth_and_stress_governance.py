"""Acceptance tests for docs/80 operational state-truth and stress governance.

Origin law     : docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md
Branch         : OPS-GOV-80 (post-closure governance + stress benchmark discipline)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOC_80 = _REPO_ROOT / "docs" / "80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_71 = _REPO_ROOT / "docs" / "71_CLOSE_5_FINAL_CLOSURE_AUDIT_REPORT.md"
_DOC_76 = _REPO_ROOT / "docs" / "76_PHASE_2_X0R_E1_ADMISSION_DECLARATION.md"
_FIXTURE = _REPO_ROOT / "data" / "constitutional_stress_benchmark_v1.json"


def _declare(branch_note: str) -> None:
    assert _DOC_80.exists(), "docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md must exist"
    assert _DOC_14.exists(), "docs/14_PR_CHAIN_ROADMAP.md must exist"
    assert _FIXTURE.exists(), "data/constitutional_stress_benchmark_v1.json must exist"

    case = ConstitutionalChainTestCase(
        origin_law="docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md",
        branch_name=f"OPS-GOV-80 ({branch_note})",
        constitutional_chain=("CLOSE-2", "CLOSE-6.1", "OPS-GOV-80"),
        chain_position="OPS-GOV-80",
        origin_law_ref="docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md#1-live-reference-truth-vs-historical-snapshot-records",
        branch_of_origin="Post-closure state-truth and operational stress governance declaration.",
        forbidden_shortcut_assertions=(
            "Snapshot-only file -> current runtime truth",
            "Stress benchmark case -> semantic/hukm/truth authority",
            "Reasonableness claim -> approval without external evidence bundle",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("SemanticAuthority", "HukmAuthority", "TruthAuthority"),
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


def test_docs_80_declares_live_reference_vs_snapshot_resolution() -> None:
    _declare("state truth resolution")
    body = _DOC_80.read_text(encoding="utf-8")

    required_markers = (
        "LIVE_REFERENCE_SET = {",
        "HISTORICAL_SNAPSHOT_SET = {",
        "docs/14_PR_CHAIN_ROADMAP.md",
        "docs/71_CLOSE_5_FINAL_CLOSURE_AUDIT_REPORT.md",
        "docs/76_PHASE_2_X0R_E1_ADMISSION_DECLARATION.md",
        "SNAPSHOT_INTERPRETATION_RULE = HISTORICAL_RECORD_NOT_CURRENT_RUNTIME_STATE",
        "STATE_TRUTH_RESOLUTION_ORDER = LIVE_REFERENCE_FIRST_THEN_SNAPSHOT_CONTEXT",
    )
    for marker in required_markers:
        assert marker in body, f"docs/80 missing required state-truth marker: {marker}"


def test_docs_80_encodes_all_five_priority_plans() -> None:
    _declare("five-plan governance")
    body = _DOC_80.read_text(encoding="utf-8")

    required_markers = (
        "PLAN_1_NAME = STATE_TRUTH_UNIFICATION",
        "PLAN_2_NAME = CONSTITUTIONAL_STRESS_BENCHMARK",
        "PLAN_3_NAME = KPI_PERFORMANCE_LAYER",
        "PLAN_4_NAME = ARABIC_HARD_GAP_READINESS",
        "PLAN_5_NAME = PRACTICAL_GROUNDING",
        "PLAN_4_FUTURE_LICENSED_TRACKS = {",
        "DIACRITIZATION_CANDIDATE",
        "SENSE_DISAMBIGUATION_CANDIDATE",
        "ELLIPSIS_ESTIMATION_DISCIPLINE",
        "PLAN_5_MINIMUM_BUNDLE = {source_id, source_type, citation_span, trace_ref}",
        "RUNTIME_OPENING = FORBIDDEN_AND_NOT_PRESENT",
    )
    for marker in required_markers:
        assert marker in body, f"docs/80 missing required plan marker: {marker}"


def test_constitutional_stress_fixture_schema_and_status_legend() -> None:
    _declare("fixture schema")
    payload = json.loads(_FIXTURE.read_text(encoding="utf-8"))

    assert payload["version"] == "1.0"
    assert payload["status_legend"] == [
        "LICENSED",
        "BLOCKED",
        "PENDING",
        "EXCEPTIONAL",
        "RESIDUAL",
        "OUT_OF_SCOPE",
    ]

    cases = payload["cases"]
    assert len(cases) >= 6
    for case in cases:
        assert set(case) == {
            "id",
            "stress_family",
            "input",
            "expected_status",
            "expected_residual_policy",
            "required_chain_anchor",
            "forbidden_outputs",
        }
        assert case["expected_status"] in payload["status_legend"]
        assert case["expected_residual_policy"] == "VISIBLE"
        assert case["forbidden_outputs"], "forbidden_outputs must be non-empty"


def test_constitutional_stress_fixture_covers_requested_families() -> None:
    _declare("required stress families")
    payload = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    families = {case["stress_family"] for case in payload["cases"]}

    assert families.issuperset(
        {
            "UNVOCALIZED_TEXT",
            "MULTI_IRAB_ANALYSIS",
            "AMBIGUOUS_PRONOUN",
            "MAJAZ_SIGNAL",
            "ELLIPSIS_ESTIMATION",
            "CLAIM_WITHOUT_EXTERNAL_EVIDENCE",
        }
    )


def test_docs_80_links_state_truth_to_existing_chain_material() -> None:
    _declare("continuity with existing docs")
    body = _DOC_80.read_text(encoding="utf-8")
    chain_body = _DOC_14.read_text(encoding="utf-8")
    doc_71 = _DOC_71.read_text(encoding="utf-8")
    doc_76 = _DOC_76.read_text(encoding="utf-8")

    assert "CHAIN_STATUS_SOURCE = LIVE_REFERENCE_SET" in body
    assert "SNAPSHOT_STATUS_SOURCE = HISTORICAL_SNAPSHOT_SET" in body
    assert "This file is the authoritative chain of pull requests." in chain_body
    assert "Snapshot date:" in doc_71
    assert "Snapshot date:" in doc_76
