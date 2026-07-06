"""Tests for the short G₀ PoC classifier and explanation engine."""

from __future__ import annotations

import json
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.g0_poc import (
    AnalysisPath,
    DecisionState,
    EvaluationSample,
    analyze_token,
    decide_go_no_go,
    evaluate_poc,
    load_g0_poc_stores,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md",
        branch_name=f"G0-POC ({branch_note})",
        constitutional_chain=("CLOSE-2", "G0-L0", "G0-POC"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("HukmVerdict", "TruthCertificate", "AuthorityExecution"),
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


def test_poc_data_stores_exist_and_have_expected_baseline_size() -> None:
    _declare("data stores baseline")
    law_rows = json.loads(
        (_REPO_ROOT / "data/g0_poc_law_registry.json").read_text(encoding="utf-8")
    )
    lexical_rows = json.loads(
        (_REPO_ROOT / "data/g0_poc_lexical_evidence.json").read_text(encoding="utf-8")
    )
    ontology_rows = json.loads(
        (_REPO_ROOT / "data/g0_poc_ontology_store.json").read_text(encoding="utf-8")
    )
    assert len(law_rows) == 30
    assert len(lexical_rows) == 20
    assert len(ontology_rows) == 11


def test_load_stores_success() -> None:
    _declare("store loading")
    stores = load_g0_poc_stores(_REPO_ROOT / "data")
    assert len(stores.laws) == 30
    assert stores.lexical
    assert stores.ontology


def test_g0_licensed_decision_produces_full_trace() -> None:
    _declare("licensed decision path")
    stores = load_g0_poc_stores(_REPO_ROOT / "data")
    card = analyze_token("جبل", stores, "trace://g0-poc/unit/001")
    assert card.decision is DecisionState.LICENSED
    assert card.path is AnalysisPath.G0
    assert card.trace.selected_laws
    assert card.trace.reason
    assert card.failure_code is None


def test_g0_refused_decision_for_blocked_non_rational_case() -> None:
    _declare("blocked non-rational refusal")
    stores = load_g0_poc_stores(_REPO_ROOT / "data")
    card = analyze_token("حمار", stores, "trace://g0-poc/unit/002")
    assert card.decision is DecisionState.REFUSED
    assert card.preventer == "NON_RATIONAL_BLOCKER"
    assert "PREVENTER_TRIGGERED" in card.residuals


def test_non_g0_token_is_routed() -> None:
    _declare("non-g0 routing")
    stores = load_g0_poc_stores(_REPO_ROOT / "data")
    card = analyze_token("دخان", stores, "trace://g0-poc/unit/003")
    assert card.decision is DecisionState.ROUTED
    assert card.path is AnalysisPath.M0
    assert card.preventer == "G0_SCOPE_ONLY"


def test_unknown_token_is_deferred_with_gap_residual() -> None:
    _declare("deferred gap")
    stores = load_g0_poc_stores(_REPO_ROOT / "data")
    card = analyze_token("لفظ_غير_معروف", stores, "trace://g0-poc/unit/004")
    assert card.decision is DecisionState.DEFERRED
    assert "LEXICAL_EVIDENCE_MISSING" in card.residuals


def test_conflicting_top_laws_return_refused() -> None:
    _declare("conflicting laws")
    stores = load_g0_poc_stores(_REPO_ROOT / "data")
    card = analyze_token("عين", stores, "trace://g0-poc/unit/005")
    assert card.decision is DecisionState.REFUSED
    assert card.preventer == "CONFLICTING_TOP_LAWS"
    assert card.trace.reason == "LAW_CONFLICT"


def test_composed_top_laws_are_visible_in_residuals() -> None:
    _declare("law composition")
    stores = load_g0_poc_stores(_REPO_ROOT / "data")
    card = analyze_token("نهر", stores, "trace://g0-poc/unit/006")
    assert card.decision is DecisionState.LICENSED
    assert "LAW_COMPOSITION" in card.residuals
    assert len(card.law_ids) >= 2


def test_evaluation_report_and_go_no_go() -> None:
    _declare("evaluation and transition")
    stores = load_g0_poc_stores(_REPO_ROOT / "data")
    samples = (
        EvaluationSample(token="جبل", expected_decision=DecisionState.LICENSED),
        EvaluationSample(token="ماء", expected_decision=DecisionState.LICENSED),
        EvaluationSample(token="حمار", expected_decision=DecisionState.REFUSED),
        EvaluationSample(token="دخان", expected_decision=DecisionState.ROUTED),
        EvaluationSample(token="كاتب", expected_decision=DecisionState.ROUTED),
        EvaluationSample(token="من", expected_decision=DecisionState.ROUTED),
        EvaluationSample(token="عين", expected_decision=DecisionState.REFUSED),
        EvaluationSample(token="نهر", expected_decision=DecisionState.LICENSED),
    )
    report = evaluate_poc(samples, stores)
    assert report.total == 8
    assert report.trace_completeness_rate == 1.0
    assert report.correct_refusal_rate == 1.0

    decision = decide_go_no_go(report)
    assert decision.verdict == "GO"
    assert decision.reasons == ("THRESHOLDS_MET",)
