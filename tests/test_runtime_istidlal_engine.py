"""Runtime istidlal engine surface tests.

Origin law  : docs/13 + docs/01
Branch      : Bounded runtime orchestration (no semantic/hukm/truth closure)
Category    : Category 2 (contract/surface)
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.runtime import (
    IstidlalEngine,
    IstidlalRuntimeResult,
    StageExecutionRecord,
    StageTransitionState,
    TokenRuntimeResult,
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
        expected_state=ClosureState.PERFORATED_CLOSED,
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
    trace_present = bool(records) and all(
        record.trace_entry_id.startswith("trace:")
        and bool(record.trace_parent_ids)
        and all(parent.startswith("trace:") for parent in record.trace_parent_ids)
        for record in records
    )
    residual_visibility = bool(records) and all(
        isinstance(record.residuals_before, tuple)
        and isinstance(record.residuals_after, tuple)
        and all(item.strip() for item in record.residuals_before)
        and all(item.strip() for item in record.residuals_after)
        and (
            record.transition_state is StageTransitionState.EXECUTED
            or bool(record.residuals_after)
        )
        for record in records
    )

    blocking_failure = next(
        (record.failure_code for record in records if record.failure_code is not None),
        None,
    )
    failure_code = (
        blocking_failure
        if blocking_failure is not None
        else (
            FailureCode.GATE_REQUIRED
            if any(
                record.transition_state is StageTransitionState.BLOCKED
                for record in records
            )
            else None
        )
    )

    if failure_code is not None:
        observed_state = ClosureState.BLOCKED
    elif any(
        record.transition_state
        in (
            StageTransitionState.DEFERRED,
            StageTransitionState.NOT_OPENED,
            StageTransitionState.DECLARED_NOT_IMPLEMENTED,
        )
        for record in records
    ):
        observed_state = ClosureState.PERFORATED_CLOSED
    else:
        observed_state = ClosureState.MINIMALLY_CLOSED

    observed_outputs = frozenset(
        output
        for record in records
        for output in (
            record.stage_id,
            record.output_carrier_id,
            f"transition:{record.transition_state.value}",
        )
        if output is not None
    )
    observed_rank = max((record.rank_after for record in records), default=Rank.ZERO)
    return ConstitutionalChainResult(
        state=observed_state,
        failure_code=failure_code,
        rank=observed_rank,
        residual_visibility=residual_visibility,
        trace_present=trace_present,
        produced_outputs=observed_outputs,
    )


def _mutate_runtime_record(
    runtime_result: IstidlalRuntimeResult,
    *,
    selector: Callable[[StageExecutionRecord], bool],
    mutator: Callable[[StageExecutionRecord], StageExecutionRecord],
) -> IstidlalRuntimeResult:
    token_results: list[TokenRuntimeResult] = []
    replaced = False
    for token_result in runtime_result.corpus_result.token_results:
        records = list(token_result.records)
        for index, record in enumerate(records):
            if not replaced and selector(record):
                records[index] = mutator(record)
                replaced = True
                break
        token_results.append(replace(token_result, records=tuple(records)))
    if not replaced:
        raise AssertionError("countermodel mutation selector matched no runtime record")
    corpus_result = replace(
        runtime_result.corpus_result,
        token_results=tuple(token_results),
    )
    return replace(runtime_result, corpus_result=corpus_result)


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


def test_istidlal_engine_countermodel_rejects_broken_trace_surface() -> None:
    case = _declare("countermodel broken trace")
    runtime_result = IstidlalEngine().run_tokens(
        "demo",
        ("كلمة",),
        source_text=None,
    )
    mutated = _mutate_runtime_record(
        runtime_result,
        selector=lambda record: record.transition_state is StageTransitionState.EXECUTED,
        mutator=lambda record: replace(record, trace_entry_id="invalid_trace_entry_id"),
    )
    with pytest.raises(AssertionError, match="trace candidate was required"):
        assert_constitutional_case(case, _observe_result(mutated))


def test_istidlal_engine_countermodel_rejects_rank_overflow() -> None:
    case = _declare("countermodel rank overflow")
    runtime_result = IstidlalEngine().run_tokens(
        "demo",
        ("كلمة",),
        source_text=None,
    )
    mutated = _mutate_runtime_record(
        runtime_result,
        selector=lambda record: record.transition_state is StageTransitionState.EXECUTED,
        mutator=lambda record: replace(record, rank_after=Rank.HYPOTHESIS),
    )
    with pytest.raises(AssertionError, match="exceeds declared ceiling"):
        assert_constitutional_case(case, _observe_result(mutated))


def test_istidlal_engine_countermodel_rejects_residual_visibility_break() -> None:
    case = _declare("countermodel residual visibility break")
    runtime_result = IstidlalEngine().run_tokens(
        "demo",
        ("كلمة",),
        source_text=None,
    )
    mutated = _mutate_runtime_record(
        runtime_result,
        selector=lambda record: record.transition_state is StageTransitionState.NOT_OPENED,
        mutator=lambda record: replace(record, residuals_after=()),
    )
    with pytest.raises(AssertionError, match="residual visibility was required"):
        assert_constitutional_case(case, _observe_result(mutated))


def test_istidlal_engine_countermodel_rejects_forbidden_output_injection() -> None:
    case = _declare("countermodel forbidden output injection")
    runtime_result = IstidlalEngine().run_tokens(
        "demo",
        ("كلمة",),
        source_text=None,
    )
    mutated = _mutate_runtime_record(
        runtime_result,
        selector=lambda record: record.transition_state is StageTransitionState.EXECUTED,
        mutator=lambda record: replace(record, output_carrier_id="TruthClaim"),
    )
    with pytest.raises(AssertionError, match="forbidden outputs were produced"):
        assert_constitutional_case(case, _observe_result(mutated))
