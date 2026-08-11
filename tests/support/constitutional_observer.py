"""Reusable test-side constitutional observer over runtime artifacts.

This module decodes ``ConstitutionalChainResult`` from observed
``StageExecutionRecord`` sequences, so constitutional verdict assertions
are grounded in runtime evidence surfaces rather than expected constants.
"""

from __future__ import annotations

from collections.abc import Iterable

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.runtime import (
    IstidlalRuntimeResult,
    StageExecutionRecord,
    StageTransitionState,
)
from tests.support.constitutional_case import ConstitutionalChainResult


def observe_constitutional_result_from_stage_records(
    records: Iterable[StageExecutionRecord],
) -> ConstitutionalChainResult:
    """Decode a constitutional chain result from runtime stage records."""

    stage_records = tuple(records)

    trace_present = bool(stage_records) and all(
        record.trace_entry_id.startswith("trace:")
        and bool(record.trace_parent_ids)
        and all(parent.startswith("trace:") for parent in record.trace_parent_ids)
        for record in stage_records
    )
    residual_visibility = bool(stage_records) and all(
        isinstance(record.residuals_before, tuple)
        and isinstance(record.residuals_after, tuple)
        and all(item.strip() for item in record.residuals_before)
        and all(item.strip() for item in record.residuals_after)
        and (
            record.transition_state is StageTransitionState.EXECUTED
            or bool(record.residuals_after)
        )
        for record in stage_records
    )

    blocking_failure = next(
        (record.failure_code for record in stage_records if record.failure_code is not None),
        None,
    )
    failure_code = (
        blocking_failure
        if blocking_failure is not None
        else (
            FailureCode.GATE_REQUIRED
            if any(
                record.transition_state is StageTransitionState.BLOCKED
                for record in stage_records
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
        for record in stage_records
    ):
        observed_state = ClosureState.PERFORATED_CLOSED
    else:
        observed_state = ClosureState.MINIMALLY_CLOSED

    observed_outputs = frozenset(
        output
        for record in stage_records
        for output in (
            record.stage_id,
            record.output_carrier_id,
            f"transition:{record.transition_state.value}",
        )
        if output is not None
    )
    observed_rank = max((record.rank_after for record in stage_records), default=Rank.ZERO)
    return ConstitutionalChainResult(
        state=observed_state,
        failure_code=failure_code,
        rank=observed_rank,
        residual_visibility=residual_visibility,
        trace_present=trace_present,
        produced_outputs=observed_outputs,
    )


def observe_istidlal_runtime_result(
    runtime_result: IstidlalRuntimeResult,
) -> ConstitutionalChainResult:
    """Decode constitutional chain result from ``IstidlalRuntimeResult``."""

    records = tuple(
        record
        for token_result in runtime_result.corpus_result.token_results
        for record in token_result.records
    )
    return observe_constitutional_result_from_stage_records(records)


__all__ = [
    "observe_constitutional_result_from_stage_records",
    "observe_istidlal_runtime_result",
]
