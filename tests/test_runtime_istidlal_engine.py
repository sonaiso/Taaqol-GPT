"""Runtime istidlal engine surface tests.

Origin law  : docs/13 + docs/01
Branch      : Bounded runtime orchestration (no semantic/hukm/truth closure)
Category    : Category 2 (contract/surface)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.runtime import (
    IstidlalEngine,
    IstidlalRuntimeResult,
    StageTransitionState,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)


def _declare(branch: str) -> ConstitutionalChainTestCase:
    return ConstitutionalChainTestCase(
        origin_law=(
            "docs/13_CONSTITUTIONAL_PR_GEOMETRY.md + "
            "docs/01_BLACK_BOX_BOUNDARY.md"
        ),
        branch_name=f"runtime istidlal/{branch}",
        constitutional_chain=("docs/13", "docs/01", "runtime/istidlal_engine"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("RuntimeInferenceVerdict", "HukmShortcut", "TruthClaim"),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="bounded runtime orchestration",
        origin_law_ref=(
            "docs/13_CONSTITUTIONAL_PR_GEOMETRY.md"
            "#the-governing-statement"
        ),
        branch_of_origin="bounded runtime orchestration under black-box boundary",
        forbidden_shortcut_assertions=(
            "TokenPath -> Meaning",
            "Ifadah -> Hukm without chain closure",
        ),
    )


def _observe_result(runtime_result: IstidlalRuntimeResult) -> ConstitutionalChainResult:
    records = tuple(
        record
        for token_result in runtime_result.corpus_result.token_results
        for record in token_result.records
    )
    trace_present = bool(records) and all(bool(record.trace_entry_id.strip()) for record in records)
    residual_visibility = bool(records) and all(
        isinstance(record.residuals_before, tuple) and isinstance(record.residuals_after, tuple)
        for record in records
    )
    observed_rank = max((record.rank_after for record in records), default=Rank.ZERO)
    return ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=observed_rank,
        residual_visibility=residual_visibility,
        trace_present=trace_present,
        produced_outputs=frozenset(),
    )


def test_istidlal_engine_run_text_orchestrates_runner_and_report() -> None:
    case = _declare("run_text orchestration")
    engine = IstidlalEngine()
    result = engine.run_text("demo-runtime", "يا أيها الذين آمنوا")
    assert_constitutional_case(case, _observe_result(result))

    assert result.source_text == "يا أيها الذين آمنوا"
    assert result.tokens == ("يا", "أيها", "الذين", "آمنوا")
    assert result.corpus_result.corpus_id == "demo-runtime"
    assert result.report.corpus_id == "demo-runtime"
    assert result.report.total_records > 0
    assert result.corpus_result.token_results
    for token_result in result.corpus_result.token_results:
        assert token_result.records[0].stage_id == "PATH_CLASSIFICATION"
        assert token_result.records[0].transition_state is StageTransitionState.EXECUTED


def test_istidlal_engine_input_guards() -> None:
    case = _declare("input guards")
    engine = IstidlalEngine()
    observed = engine.run_tokens("demo", ("كلمة",), source_text=None)
    assert_constitutional_case(case, _observe_result(observed))

    with pytest.raises(ValueError):
        engine.tokenize("   ")
    with pytest.raises(ValueError):
        engine.run_tokens("", ("كلمة",))
    with pytest.raises(ValueError):
        engine.run_tokens("demo", ("",))
