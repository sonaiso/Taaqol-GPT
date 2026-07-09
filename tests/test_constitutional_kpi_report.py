"""Runtime tests for the Constitutional KPI report over the stress benchmark.

Origin law          : docs/11 + docs/13 + docs/63 + docs/80 §4 (Plan-3)
Branch name         : X0R ConstitutionalKPIReport
Constitutional chain: docs/11 -> docs/13 -> docs/63 -> docs/80 -> KPI report
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r import (
    ArchimedeanStatus,
    ConstitutionalKPIReport,
    ConstitutionalStressBenchmarkRunner,
    ConstitutionalStressCaseResult,
    EuclideanStatus,
    RankBoundStatus,
    StressCaseStatus,
    TraceReplayStatus,
    audit_transition,
    compute_kpi_report,
)
from taaqqul_slot_geometry.x0r.archimedean_euclidean_audit import (
    ArchimedeanEuclideanTransitionAuditResult,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FIXTURE = _REPO_ROOT / "data" / "constitutional_stress_benchmark_v1.json"

_FORBIDDEN_OUTPUTS = ("Meaning", "Hukm", "Truth", "Certainty", "Reality")


def _declare(branch_name: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md + "
            "docs/13_CONSTITUTIONAL_PR_GEOMETRY.md + "
            "docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md + "
            "docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md"
        ),
        branch_name=branch_name,
        constitutional_chain=(
            "docs/11",
            "docs/13",
            "docs/63",
            "docs/80#Plan-3",
            "X0R.KPIReport",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=_FORBIDDEN_OUTPUTS,
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="X0R KPI report over stress benchmark (docs/80 §4 Plan-3)",
        origin_law_ref=(
            "docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md#4-plan-3"
        ),
        branch_of_origin="X0R ConstitutionalKPIReport",
        forbidden_shortcut_assertions=(
            "Benchmark -> Truth",
            "Metric -> Certainty",
            "KPI -> Meaning",
        ),
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


def _leakage_case() -> ConstitutionalStressCaseResult:
    """Build a synthetic case with a forbidden output leaked."""

    verdict = audit_transition(
        origin="BenchmarkCase",
        target="SurfaceResolution",
        domain="arabic_surface",
        trace_ref="trace://kpi/leakage-injection/1",
        provided_steps=("MULTI_IRAB_CANDIDATE",),
        required_units=("MULTI_IRAB_CANDIDATE",),
        provided_gates=("MULTI_IRAB_GATE",),
        required_gates=("MULTI_IRAB_GATE",),
        provided_evidence=("GRAMMAR_EVIDENCE",),
        required_evidence=("GRAMMAR_EVIDENCE",),
        forbidden_outputs=_FORBIDDEN_OUTPUTS,
        produced_outputs=("Truth",),
        requested_rank=2,
        evidence_rank=2,
        trace_replay_available=True,
        trace_snapshot_only=False,
    )
    return ConstitutionalStressCaseResult(
        case_id="INJECTED_LEAKAGE",
        stress_family="MULTI_IRAB_ANALYSIS",
        expected_status=StressCaseStatus.RESIDUAL,
        actual_status=verdict.final_status,
        matches_expected=False,
        audit=verdict,
    )


def test_kpi_report_matches_fixture_expected_statuses_at_full_rate() -> None:
    _declare("fixture expected-match rate")
    runner = ConstitutionalStressBenchmarkRunner(_FIXTURE)
    report = compute_kpi_report(runner.run())

    assert isinstance(report, ConstitutionalKPIReport)
    assert report.total_cases == 6
    assert report.expected_match_count == 6
    assert report.expected_match_rate == 1.0
    assert report.structural_error_rate == 0.0


def test_kpi_report_shows_no_forbidden_output_leakage_on_current_fixture() -> None:
    _declare("fixture forbidden-output leakage rate")
    runner = ConstitutionalStressBenchmarkRunner(_FIXTURE)
    report = compute_kpi_report(runner.run())

    assert report.forbidden_output_violation_count == 0
    assert report.forbidden_output_leakage_rate == 0.0


def test_kpi_report_detects_injected_forbidden_output_leakage() -> None:
    _declare("injected forbidden-output leakage detection")
    runner = ConstitutionalStressBenchmarkRunner(_FIXTURE)
    baseline = compute_kpi_report(runner.run())

    with_leak = compute_kpi_report(tuple(runner.run()) + (_leakage_case(),))

    assert with_leak.forbidden_output_violation_count == (
        baseline.forbidden_output_violation_count + 1
    )
    assert with_leak.forbidden_output_leakage_rate > 0.0
    assert with_leak.total_cases == baseline.total_cases + 1
    # A leaked forbidden output must appear as a structural error
    # because the injected case's expected_status was RESIDUAL but
    # the audit blocks it.
    assert with_leak.structural_error_rate > 0.0


def test_kpi_report_does_not_produce_any_forbidden_output() -> None:
    _declare("report emits no forbidden semantic output")
    runner = ConstitutionalStressBenchmarkRunner(_FIXTURE)
    report = compute_kpi_report(runner.run())

    # The KPI report is a pure numeric surface. It must not carry any
    # forbidden semantic token as a field value or as a stringified
    # payload. This is the docs/80 §4 PLAN_3_RULE guarantee.
    produced_surface = repr(report)
    for name in _FORBIDDEN_OUTPUTS:
        assert name not in produced_surface


def test_kpi_report_metric_semantics_match_docs_80_plan_3() -> None:
    _declare("docs/80 §4 metric semantics")
    runner = ConstitutionalStressBenchmarkRunner(_FIXTURE)
    results = runner.run()
    report = compute_kpi_report(results)

    # jump_refusal_precision: of expected-BLOCKED cases, fraction
    # actually blocked. The current fixture contains exactly one
    # BLOCKED-expected case (docs/80 §3), and it is correctly blocked
    # by the audit surface.
    expected_blocked = [r for r in results if r.expected_status is StressCaseStatus.BLOCKED]
    actually_blocked = [r for r in expected_blocked if r.actual_status is StressCaseStatus.BLOCKED]
    assert len(expected_blocked) >= 1
    assert report.jump_refusal_precision == len(actually_blocked) / len(expected_blocked)

    # trace_completeness_rate: fraction whose trace_replay_status is
    # PASS or SNAPSHOT_ONLY. In the current fixture no case has
    # MISSING trace, so completeness must be 1.0.
    complete = [
        r
        for r in results
        if r.audit.trace_replay_status
        in (TraceReplayStatus.PASS, TraceReplayStatus.SNAPSHOT_ONLY)
    ]
    assert report.trace_completeness_rate == len(complete) / len(results)
    missing = [
        r for r in results if r.audit.trace_replay_status is TraceReplayStatus.MISSING
    ]
    assert report.trace_missing_rate == len(missing) / len(results)
    # Completeness and missing are complementary partitions.
    assert report.trace_completeness_rate + report.trace_missing_rate == 1.0

    # residual_visibility_consistency: no leaked forbidden outputs
    # here, and the RESIDUAL/EXCEPTIONAL cases already sit in a
    # non-LICENSED status, so the whole fixture must be coherent.
    assert report.residual_visibility_consistency == 1.0

    # structural_error_rate: current fixture matches expectations
    # exactly.
    assert report.structural_error_rate == 0.0

    # rank_bound_failure_count: the fixture is calibrated so that
    # requested_rank <= evidence_rank everywhere.
    assert report.rank_bound_failure_count == 0


def test_kpi_report_reports_direct_forbidden_target_blocks() -> None:
    _declare("blocked forbidden target counter")
    # Build one synthetic case that requests Truth directly with
    # otherwise complete prerequisites, and one that does not.
    truth_verdict = audit_transition(
        origin="SurfaceText",
        target="Truth",
        domain="arabic_surface",
        trace_ref="trace://kpi/direct-truth/1",
        provided_steps=("DIACRITIZATION_CANDIDATE",),
        required_units=("DIACRITIZATION_CANDIDATE",),
        provided_gates=("ARCHIMEDEAN_EUCLIDEAN_GATE",),
        required_gates=("ARCHIMEDEAN_EUCLIDEAN_GATE",),
        provided_evidence=("EXTERNAL_EVIDENCE_BUNDLE",),
        required_evidence=("EXTERNAL_EVIDENCE_BUNDLE",),
        forbidden_outputs=_FORBIDDEN_OUTPUTS,
        produced_outputs=(),
        requested_rank=2,
        evidence_rank=2,
        trace_replay_available=True,
        trace_snapshot_only=False,
    )
    assert isinstance(truth_verdict, ArchimedeanEuclideanTransitionAuditResult)
    assert truth_verdict.archimedean_status is ArchimedeanStatus.FAIL_NON_DECOMPOSABLE
    assert truth_verdict.euclidean_status is EuclideanStatus.FAIL_UNCONSTRUCTED_STEP
    assert truth_verdict.rank_bound_status is RankBoundStatus.PASS

    truth_case = ConstitutionalStressCaseResult(
        case_id="INJECTED_TRUTH_TARGET",
        stress_family="MULTI_IRAB_ANALYSIS",
        expected_status=StressCaseStatus.BLOCKED,
        actual_status=truth_verdict.final_status,
        matches_expected=truth_verdict.final_status is StressCaseStatus.BLOCKED,
        audit=truth_verdict,
    )

    runner = ConstitutionalStressBenchmarkRunner(_FIXTURE)
    report = compute_kpi_report(tuple(runner.run()) + (truth_case,))

    assert report.blocked_forbidden_target_count >= 1
