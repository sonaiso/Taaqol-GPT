"""Reusable test-side constitutional observer over runtime artifacts.

This module decodes ``ConstitutionalChainResult`` from observed
``StageExecutionRecord`` sequences, so constitutional verdict assertions
are grounded in runtime evidence surfaces rather than expected constants.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.runtime import (
    IstidlalRuntimeResult,
    StageExecutionRecord,
    StageTransitionState,
)
from tests.support.constitutional_case import ConstitutionalChainResult


@dataclass(frozen=True, slots=True)
class ObservedStageArtifact:
    stage_id: str
    input_carrier_id: str
    output_carrier_id: str | None
    transition_state: StageTransitionState
    requirements_observed: tuple[str, ...]
    witness_refs: tuple[str, ...]
    rank_before: Rank
    rank_after: Rank
    residuals_before: tuple[str, ...]
    residuals_after: tuple[str, ...]
    trace_id: str
    parent_trace_ids: tuple[str, ...]
    failure_code: FailureCode | None


@dataclass(frozen=True, slots=True)
class ObservedArtifact:
    stage_artifacts: tuple[ObservedStageArtifact, ...]
    stage_verdict_vector: tuple[StageTransitionState, ...]
    trace_surface_present: bool
    trace_continuity_present: bool
    residual_surface_visible: bool
    produced_outputs: frozenset[str]
    blocking_failure: FailureCode | None
    peak_rank: Rank
    final_rank: Rank


@dataclass(frozen=True, slots=True)
class ClosureProofObject:
    premises: tuple[str, ...]
    requirements_observed: frozenset[str]
    satisfied_witnesses: frozenset[str]
    successful_operations: tuple[str, ...]
    trace_path: tuple[str, ...]
    trace_surface_present: bool
    trace_continuity_present: bool
    residual_surface_visible: bool
    peak_rank: Rank
    final_rank: Rank
    supported_rank: Rank
    failure_code: FailureCode | None
    conclusion_state: ClosureState
    produced_outputs: frozenset[str]


def observe_stage_artifacts(
    records: Iterable[StageExecutionRecord],
) -> ObservedArtifact:
    """Observe runtime records into a descriptive artifact surface only."""

    stage_artifacts = tuple(
        ObservedStageArtifact(
            stage_id=record.stage_id,
            input_carrier_id=record.input_carrier_id,
            output_carrier_id=record.output_carrier_id,
            transition_state=record.transition_state,
            requirements_observed=record.identity_invariants_checked,
            witness_refs=record.evidence_refs,
            rank_before=record.rank_before,
            rank_after=record.rank_after,
            residuals_before=record.residuals_before,
            residuals_after=record.residuals_after,
            trace_id=record.trace_entry_id,
            parent_trace_ids=record.trace_parent_ids,
            failure_code=record.failure_code,
        )
        for record in records
    )

    trace_surface_present = bool(stage_artifacts) and all(
        artifact.trace_id.startswith("trace:")
        and bool(artifact.parent_trace_ids)
        and all(parent.startswith("trace:") for parent in artifact.parent_trace_ids)
        for artifact in stage_artifacts
    )
    trace_continuity_present = trace_surface_present and _has_trace_continuity(
        stage_artifacts
    )
    residual_surface_visible = bool(stage_artifacts) and all(
        isinstance(artifact.residuals_before, tuple)
        and isinstance(artifact.residuals_after, tuple)
        and all(item.strip() for item in artifact.residuals_before)
        and all(item.strip() for item in artifact.residuals_after)
        and (
            artifact.transition_state is StageTransitionState.EXECUTED
            or bool(artifact.residuals_after)
        )
        for artifact in stage_artifacts
    )
    produced_outputs = frozenset(
        output
        for artifact in stage_artifacts
        for output in (
            artifact.stage_id,
            artifact.output_carrier_id,
            f"transition:{artifact.transition_state.value}",
        )
        if output is not None
    )
    peak_rank = max((artifact.rank_after for artifact in stage_artifacts), default=Rank.ZERO)
    final_rank = stage_artifacts[-1].rank_after if stage_artifacts else Rank.ZERO
    blocking_failure = next(
        (
            artifact.failure_code
            for artifact in stage_artifacts
            if artifact.failure_code is not None
        ),
        None,
    )
    return ObservedArtifact(
        stage_artifacts=stage_artifacts,
        stage_verdict_vector=tuple(
            artifact.transition_state for artifact in stage_artifacts
        ),
        trace_surface_present=trace_surface_present,
        trace_continuity_present=trace_continuity_present,
        residual_surface_visible=residual_surface_visible,
        produced_outputs=produced_outputs,
        blocking_failure=blocking_failure,
        peak_rank=peak_rank,
        final_rank=final_rank,
    )


def reconstruct_closure_proof(observed: ObservedArtifact) -> ClosureProofObject:
    """Reconstruct a closure-only proof object from observed artifacts."""

    executed_artifacts = tuple(
        artifact
        for artifact in observed.stage_artifacts
        if artifact.transition_state is StageTransitionState.EXECUTED
    )
    requirements_observed = frozenset(
        requirement
        for artifact in observed.stage_artifacts
        for requirement in artifact.requirements_observed
    )
    satisfied_witnesses = frozenset(
        witness
        for artifact in observed.stage_artifacts
        for witness in artifact.witness_refs
    )
    successful_operations = tuple(artifact.stage_id for artifact in executed_artifacts)
    trace_path = tuple(artifact.trace_id for artifact in observed.stage_artifacts)

    missing_requirement = any(
        artifact.transition_state is StageTransitionState.EXECUTED
        and (
            not artifact.requirements_observed
            or not artifact.witness_refs
        )
        for artifact in observed.stage_artifacts
    )
    inferred_failure = observed.blocking_failure
    if inferred_failure is None and missing_requirement:
        inferred_failure = FailureCode.REQUIRED_SLOT_EMPTY
    if inferred_failure is None and any(
        artifact.transition_state is StageTransitionState.BLOCKED
        for artifact in observed.stage_artifacts
    ):
        inferred_failure = FailureCode.GATE_REQUIRED

    supported_rank = max(
        (artifact.rank_after for artifact in executed_artifacts),
        default=Rank.ZERO,
    )

    if inferred_failure is not None:
        conclusion_state = ClosureState.BLOCKED
    elif any(
        transition
        in (
            StageTransitionState.DEFERRED,
            StageTransitionState.NOT_OPENED,
            StageTransitionState.DECLARED_NOT_IMPLEMENTED,
        )
        for transition in observed.stage_verdict_vector
    ):
        conclusion_state = ClosureState.PERFORATED_CLOSED
    else:
        conclusion_state = ClosureState.MINIMALLY_CLOSED

    return ClosureProofObject(
        premises=(
            "ObservedArtifact.trace_surface_present",
            "ObservedArtifact.residual_surface_visible",
            "ObservedArtifact.stage_verdict_vector",
        ),
        requirements_observed=requirements_observed,
        satisfied_witnesses=satisfied_witnesses,
        successful_operations=successful_operations,
        trace_path=trace_path,
        trace_surface_present=observed.trace_surface_present,
        trace_continuity_present=observed.trace_continuity_present,
        residual_surface_visible=observed.residual_surface_visible,
        peak_rank=observed.peak_rank,
        final_rank=observed.final_rank,
        supported_rank=supported_rank,
        failure_code=inferred_failure,
        conclusion_state=conclusion_state,
        produced_outputs=observed.produced_outputs,
    )


def verify_closure_proof(proof: ClosureProofObject) -> ConstitutionalChainResult:
    """Verify closure proof object into constitutional chain result."""

    return ConstitutionalChainResult(
        state=proof.conclusion_state,
        failure_code=proof.failure_code,
        rank=proof.supported_rank,
        residual_visibility=proof.residual_surface_visible,
        trace_present=proof.trace_surface_present,
        produced_outputs=proof.produced_outputs,
    )


def observe_constitutional_result_from_stage_records(
    records: Iterable[StageExecutionRecord],
) -> ConstitutionalChainResult:
    """Observe -> reconstruct -> verify from runtime stage records."""

    observed = observe_stage_artifacts(records)
    proof = reconstruct_closure_proof(observed)
    return verify_closure_proof(proof)


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


def _has_trace_continuity(stage_artifacts: tuple[ObservedStageArtifact, ...]) -> bool:
    if not stage_artifacts:
        return False
    anchor = stage_artifacts[0].parent_trace_ids[0]
    return all(
        bool(artifact.parent_trace_ids)
        and anchor in artifact.parent_trace_ids
        for artifact in stage_artifacts
    )


__all__ = [
    "ObservedStageArtifact",
    "ObservedArtifact",
    "ClosureProofObject",
    "observe_stage_artifacts",
    "reconstruct_closure_proof",
    "verify_closure_proof",
    "observe_constitutional_result_from_stage_records",
    "observe_istidlal_runtime_result",
]
