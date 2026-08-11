"""Runtime istidlal engine surface tests.

Origin law  : docs/80 + docs/91
Branch      : Bounded runtime orchestration (no semantic/hukm/truth closure)
Category    : Category 2 (contract/surface)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.runtime import (
    IstidlalEngine,
    StageTransitionState,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)


def _declare(branch: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md",
        branch_name=f"runtime istidlal/{branch}",
        constitutional_chain=("docs/80", "runtime/istidlal_engine"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("RuntimeInferenceVerdict", "HukmShortcut", "TruthClaim"),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="bounded runtime orchestration",
        origin_law_ref=(
            "docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md"
            "#1-live-reference-truth-vs-historical-snapshot-records"
        ),
        branch_of_origin="runtime token execution and reporting",
        forbidden_shortcut_assertions=(
            "TokenPath -> Meaning",
            "Ifadah -> Hukm without chain closure",
        ),
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def test_istidlal_engine_run_text_orchestrates_runner_and_report() -> None:
    _declare("run_text orchestration")
    engine = IstidlalEngine()
    result = engine.run_text("demo-runtime", "يا أيها الذين آمنوا")

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
    _declare("input guards")
    engine = IstidlalEngine()

    with pytest.raises(ValueError):
        engine.tokenize("   ")
    with pytest.raises(ValueError):
        engine.run_tokens("", ("كلمة",))
    with pytest.raises(ValueError):
        engine.run_tokens("demo", ("",))
