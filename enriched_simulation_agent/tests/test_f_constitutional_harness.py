from __future__ import annotations

import pytest
from sim_agent.f_constitutional_harness import (
    ConstitutionalCaseReport,
    ConstitutionalChainHarness,
    ConstitutionalChainTestCase,
    build_falsification_cases,
)
from sim_agent.f_experiment import TenConditionAuditor, TenConditionCode, build_f_experiment

FALSIFICATION_CASES = build_falsification_cases()


def _expected_code(case: ConstitutionalChainTestCase) -> str:
    return next(iter(case.expected_violation_codes))


def test_falsification_fixture_covers_all_ten_conditions() -> None:
    expected = {code.value for code in TenConditionCode}
    observed = {_expected_code(case) for case in FALSIFICATION_CASES}
    assert observed == expected
    assert len(FALSIFICATION_CASES) == 10


@pytest.mark.parametrize("case", FALSIFICATION_CASES, ids=lambda c: c.case_id)
def test_constitutional_harness_detects_each_falsification_case(
    case: ConstitutionalChainTestCase,
) -> None:
    report = ConstitutionalChainHarness().execute(case)

    assert report.passed
    assert report.falsification_triggered
    assert case.expected_violation_codes <= report.detected_violation_codes
    assert report.missing_trace_anchors == ()
    assert report.missing_intermediates == ()
    assert report.lost_residuals == ()


def test_constitutional_harness_is_equivalent_to_ten_condition_auditor() -> None:
    audit = TenConditionAuditor(build_f_experiment()).run()
    reports: tuple[ConstitutionalCaseReport, ...] = tuple(
        ConstitutionalChainHarness().execute(case) for case in FALSIFICATION_CASES
    )

    detected = set().union(*(report.detected_violation_codes for report in reports))
    auditor_detected = {result.code.value for result in audit.results if result.passed}

    assert detected == auditor_detected
    assert all(report.structural_report.structural_valid for report in reports)
