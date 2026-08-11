"""Runtime admission tests for V0.231 closure-only gate.

Origin law     : docs/110 (Runtime Admission by Independent Ratification Law)
Branch         : V0.231 ClosureRuntimeAdmissionGate
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.runtime import (
    ClosureAdmissionState,
    ClosureObservedArtifact,
    ClosureRefusalFamily,
    ClosureRuntimeAdmissionGate,
    StageApplicability,
    StageExecutionRecord,
    StageTransitionState,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/110_RUNTIME_ADMISSION_BY_INDEPENDENT_RATIFICATION_LAW.md",
        branch_name=f"V0.231 ClosureRuntimeAdmissionGate ({branch_note})",
        constitutional_chain=("docs/12", "docs/52", "docs/110", "V0.231"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "AuthorityRuntimeOpen",
            "BridgeRuntimeOpen",
            "SemanticOutputOpen",
            "HukmRuntimeOpen",
            "TruthRuntimeOpen",
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


def _record(
    *,
    transition_state: StageTransitionState = StageTransitionState.EXECUTED,
    rank_before: Rank = Rank.ZERO,
    rank_after: Rank = Rank.ZERO,
    requirements: tuple[str, ...] = ("req://closure",),
    witnesses: tuple[str, ...] = ("evidence://closure",),
    residuals_after: tuple[str, ...] = ("RESIDUAL:VISIBLE",),
    trace_entry: str = "trace://closure/1",
    trace_parents: tuple[str, ...] = ("trace://closure/1",),
    failure_code: FailureCode | None = None,
) -> StageExecutionRecord:
    return StageExecutionRecord(
        run_id="run://v0.231",
        corpus_id="corpus://closure",
        token_id="token://1",
        span_id=None,
        stage_id="ClosureStage",
        path_id="path://closure",
        input_carrier_id="carrier://in",
        output_carrier_id="carrier://out",
        applicability=StageApplicability.APPLICABLE,
        transition_state=transition_state,
        evidence_refs=witnesses,
        rank_before=rank_before,
        rank_after=rank_after,
        residuals_before=(),
        residuals_after=residuals_after,
        identity_invariants_checked=requirements,
        trace_parent_ids=trace_parents,
        trace_entry_id=trace_entry,
        failure_code=failure_code,
        remediation_hints=(),
        next_admissible_stage_ids=(),
        source_commit_sha="deadbeef",
        registry_version="test-v0.231",
        registry_hash="hash-v0.231",
    )


def test_roadmap_registers_v0_230_and_v0_231_closure_admission_branch() -> None:
    _declare("roadmap registration")
    body = _DOC_14.read_text(encoding="utf-8")
    assert "V0.230 Runtime Admission by Independent Ratification Law" in body
    assert "V0.231 ClosureRuntimeAdmissionGate" in body


def test_gate_admits_when_closure_requirements_are_complete() -> None:
    _declare("admitted closure-only gate")
    decision = ClosureRuntimeAdmissionGate.admit_from_observed(
        ClosureObservedArtifact(
            artifact_id="artifact://closure/admitted",
            stage_records=(
                _record(
                    rank_after=Rank.TRACE,
                    trace_entry="trace://closure/1",
                    trace_parents=("trace://closure/1",),
                ),
            ),
        )
    )

    assert decision.admitted is True
    assert decision.state is ClosureAdmissionState.ADMITTED
    assert decision.refusal_family is None
    assert decision.failure_code is None


def test_gate_refuses_missing_requirement_countermodel() -> None:
    _declare("MissingRequirement countermodel")
    decision = ClosureRuntimeAdmissionGate.admit_from_observed(
        ClosureObservedArtifact(
            artifact_id="artifact://closure/missing-requirement",
            stage_records=(
                _record(requirements=(), witnesses=()),
            ),
        )
    )
    assert decision.admitted is False
    assert decision.refusal_family is ClosureRefusalFamily.MISSING_REQUIREMENT
    assert decision.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


def test_gate_refuses_blocking_residual_countermodel() -> None:
    _declare("BlockingResidual countermodel")
    decision = ClosureRuntimeAdmissionGate.admit_from_observed(
        ClosureObservedArtifact(
            artifact_id="artifact://closure/blocking-residual",
            stage_records=(
                _record(residuals_after=("RESIDUAL:VISIBLE", "BLOCKING:TRACE")),
            ),
        )
    )
    assert decision.admitted is False
    assert decision.refusal_family is ClosureRefusalFamily.BLOCKING_RESIDUAL
    assert decision.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


def test_gate_refuses_broken_trace_continuity_countermodel() -> None:
    _declare("BrokenTraceContinuity countermodel")
    decision = ClosureRuntimeAdmissionGate.admit_from_observed(
        ClosureObservedArtifact(
            artifact_id="artifact://closure/broken-trace",
            stage_records=(
                _record(
                    trace_entry="trace://closure/1",
                    trace_parents=("trace://another-root",),
                ),
            ),
        )
    )
    assert decision.admitted is False
    assert decision.refusal_family is ClosureRefusalFamily.BROKEN_TRACE_CONTINUITY
    assert decision.failure_code is FailureCode.TRACE_MISSING


def test_gate_refuses_rank_above_evidence_countermodel() -> None:
    _declare("RankAboveEvidence countermodel")
    decision = ClosureRuntimeAdmissionGate.admit_from_observed(
        ClosureObservedArtifact(
            artifact_id="artifact://closure/rank-above-evidence",
            stage_records=(
                _record(transition_state=StageTransitionState.EXECUTED, rank_after=Rank.TRACE),
                _record(
                    transition_state=StageTransitionState.BLOCKED,
                    rank_before=Rank.CANDIDATE,
                    rank_after=Rank.CANDIDATE,
                    failure_code=FailureCode.GATE_REQUIRED,
                ),
            ),
        )
    )
    assert decision.admitted is False
    assert decision.refusal_family is ClosureRefusalFamily.RANK_ABOVE_EVIDENCE
    assert decision.failure_code is FailureCode.RANK_EXCEEDS_CEILING
