"""Constitutional KPI report over the Archimedean/Euclidean stress benchmark.

This module implements ``docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md``
§4 (``PLAN_3_NAME = KPI_PERFORMANCE_LAYER``) as a measurement-only surface
above :class:`ConstitutionalStressBenchmarkRunner`.

It is deliberately not:

* an Arabic parser, morphology engine, or diacritization runtime;
* a grounding / evidence-fitness API;
* a semantic / hukm / truth / certainty / reality producer;
* a rank engine or `RankVector` runtime.

The report only counts and ratios what the audit surface already emits
(``ConstitutionalStressCaseResult``). It never mutates chain order and
never opens a new constitutional layer (``docs/80`` §4
``PLAN_3_RULE``).
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.x0r.archimedean_euclidean_audit import (
    ConstitutionalStressCaseResult,
    RankBoundStatus,
    StressCaseStatus,
    TraceReplayStatus,
)


@dataclass(frozen=True, slots=True)
class ConstitutionalKPIReport:
    """Aggregated KPI surface over a run of stress benchmark cases.

    The four ``docs/80`` §4 canonical metrics are first-class:

    * ``jump_refusal_precision`` — of cases whose ``expected_status`` is
      ``BLOCKED``, the fraction that were actually blocked.
    * ``trace_completeness_rate`` — fraction of cases whose trace was
      present in some replayable form (``PASS`` or ``SNAPSHOT_ONLY``).
    * ``residual_visibility_consistency`` — fraction of cases whose
      residual/leakage discipline is coherent: any forbidden output
      violation forces ``BLOCKED``, and any declared blocking residual
      forces a non-``LICENSED`` status.
    * ``structural_error_rate`` — fraction of cases whose observed
      ``final_status`` disagrees with the fixture's declared
      ``expected_status``.

    The remaining fields are operational counters intended for KPI
    dashboards; none of them promote a rank, ground a claim, or open
    any semantic surface.

    Rates are expressed as ``0.0..1.0`` and are defined as ``1.0`` for
    denominators of zero when the metric asserts a *coherence*
    property (``jump_refusal_precision``, ``trace_completeness_rate``,
    ``residual_visibility_consistency``) and as ``0.0`` for denominators
    of zero when the metric asserts a *failure* property
    (``structural_error_rate``, ``forbidden_output_leakage_rate``).
    """

    total_cases: int
    expected_match_count: int
    expected_match_rate: float
    blocked_forbidden_target_count: int
    forbidden_output_violation_count: int
    forbidden_output_leakage_rate: float
    residual_visible_rate: float
    trace_replay_pass_rate: float
    trace_snapshot_only_rate: float
    trace_missing_rate: float
    rank_bound_failure_count: int
    # docs/80 §4 canonical metrics
    jump_refusal_precision: float
    trace_completeness_rate: float
    residual_visibility_consistency: float
    structural_error_rate: float


def compute_kpi_report(
    results: tuple[ConstitutionalStressCaseResult, ...],
) -> ConstitutionalKPIReport:
    """Compute a :class:`ConstitutionalKPIReport` over a benchmark run.

    The function is pure: it reads only the audit fields already
    present on each :class:`ConstitutionalStressCaseResult` and returns
    a new frozen report. It never inspects text, never invokes a
    parser, never emits a forbidden output name.
    """

    total = len(results)

    if total == 0:
        return ConstitutionalKPIReport(
            total_cases=0,
            expected_match_count=0,
            expected_match_rate=1.0,
            blocked_forbidden_target_count=0,
            forbidden_output_violation_count=0,
            forbidden_output_leakage_rate=0.0,
            residual_visible_rate=1.0,
            trace_replay_pass_rate=1.0,
            trace_snapshot_only_rate=0.0,
            trace_missing_rate=0.0,
            rank_bound_failure_count=0,
            jump_refusal_precision=1.0,
            trace_completeness_rate=1.0,
            residual_visibility_consistency=1.0,
            structural_error_rate=0.0,
        )

    expected_match_count = 0
    blocked_forbidden_target_count = 0
    forbidden_output_violation_count = 0
    residual_visible_count = 0
    trace_pass_count = 0
    trace_snapshot_only_count = 0
    trace_missing_count = 0
    rank_bound_failure_count = 0

    expected_blocked_count = 0
    expected_blocked_actually_blocked = 0

    consistent_count = 0
    structural_error_count = 0

    for item in results:
        audit = item.audit

        if item.matches_expected:
            expected_match_count += 1
        else:
            structural_error_count += 1

        if item.expected_status is StressCaseStatus.BLOCKED:
            expected_blocked_count += 1
            if item.actual_status is StressCaseStatus.BLOCKED:
                expected_blocked_actually_blocked += 1

        if audit.forbidden_output_violations:
            forbidden_output_violation_count += 1

        # A "blocked forbidden target" is a case that landed on BLOCKED
        # because a direct forbidden target (Meaning/Hukm/Truth/Certainty
        # /Reality) was requested. The audit surface signals this via the
        # combined FAIL_NON_DECOMPOSABLE + FAIL_UNCONSTRUCTED_STEP shape
        # (docs/80 + archimedean_euclidean_audit._FORBIDDEN_DIRECT_TARGETS).
        if (
            audit.final_status is StressCaseStatus.BLOCKED
            and audit.archimedean_status.value == "FAIL_NON_DECOMPOSABLE"
            and audit.euclidean_status.value == "FAIL_UNCONSTRUCTED_STEP"
            and not audit.forbidden_output_violations
        ):
            blocked_forbidden_target_count += 1

        if audit.blocking_residuals or audit.final_status in (
            StressCaseStatus.RESIDUAL,
            StressCaseStatus.EXCEPTIONAL,
        ):
            residual_visible_count += 1

        if audit.trace_replay_status is TraceReplayStatus.PASS:
            trace_pass_count += 1
        elif audit.trace_replay_status is TraceReplayStatus.SNAPSHOT_ONLY:
            trace_snapshot_only_count += 1
        else:
            trace_missing_count += 1

        if audit.rank_bound_status is RankBoundStatus.FAIL:
            rank_bound_failure_count += 1

        # Residual/leakage coherence — see the class docstring.
        leakage_ok = (
            not audit.forbidden_output_violations
            or audit.final_status is StressCaseStatus.BLOCKED
        )
        blocking_ok = (
            not audit.blocking_residuals
            or audit.final_status is not StressCaseStatus.LICENSED
        )
        if leakage_ok and blocking_ok:
            consistent_count += 1

    trace_completeness_numerator = trace_pass_count + trace_snapshot_only_count

    if expected_blocked_count > 0:
        jump_refusal_precision = expected_blocked_actually_blocked / expected_blocked_count
    else:
        jump_refusal_precision = 1.0

    return ConstitutionalKPIReport(
        total_cases=total,
        expected_match_count=expected_match_count,
        expected_match_rate=expected_match_count / total,
        blocked_forbidden_target_count=blocked_forbidden_target_count,
        forbidden_output_violation_count=forbidden_output_violation_count,
        forbidden_output_leakage_rate=forbidden_output_violation_count / total,
        residual_visible_rate=residual_visible_count / total,
        trace_replay_pass_rate=trace_pass_count / total,
        trace_snapshot_only_rate=trace_snapshot_only_count / total,
        trace_missing_rate=trace_missing_count / total,
        rank_bound_failure_count=rank_bound_failure_count,
        jump_refusal_precision=jump_refusal_precision,
        trace_completeness_rate=trace_completeness_numerator / total,
        residual_visibility_consistency=consistent_count / total,
        structural_error_rate=structural_error_count / total,
    )


__all__ = [
    "ConstitutionalKPIReport",
    "compute_kpi_report",
]
