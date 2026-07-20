from __future__ import annotations

import pytest
from sim_agent.f_constitutional_harness import (
    ConstitutionalCaseReport,
    ConstitutionalChainHarness,
    ConstitutionalChainTestCase,
    build_falsification_cases,
)
from sim_agent.f_experiment import TenConditionCode

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
    assert case.expected_violation_codes == report.detected_violation_codes
    assert report.missing_trace_anchors == ()
    assert report.missing_intermediates == ()
    assert report.lost_residuals == ()


def test_falsification_cases_use_non_empty_system_payloads() -> None:
    for case in FALSIFICATION_CASES:
        assert case.source_system.states
        assert case.target_system.states
        assert case.source_system.operations
        assert case.target_system.operations
        assert case.simulation_map.state_map
        assert case.simulation_map.operation_map


def test_falsification_cases_use_dual_typed_separation() -> None:
    for case in FALSIFICATION_CASES:
        assert case.source_carrier_type == "LINGUISTIC_CARRIER"
        assert case.target_carrier_type == "MEASUREMENT_CARRIER"
        assert case.source_carrier_type != case.target_carrier_type
        assert not case.allow_identity_simulation
        assert case.identity_simulation_id is None


def test_constitutional_harness_rejects_invalid_case_contract() -> None:
    case = FALSIFICATION_CASES[0]
    invalid_case = ConstitutionalChainTestCase(
        case_id=case.case_id,
        title=case.title,
        source_system=case.source_system,
        target_system=case.target_system,
        simulation_map=type(case.simulation_map)(state_map={}, operation_map={}),
        expected_verdict=case.expected_verdict,
        expected_violation_codes=case.expected_violation_codes,
        required_intermediate_identities=case.required_intermediate_identities,
        required_trace_anchors=case.required_trace_anchors,
        required_residual_codes=case.required_residual_codes,
        falsification_condition=case.falsification_condition,
        constitutional_law=case.constitutional_law,
        source_fragment_id=case.source_fragment_id,
        target_fragment_id=case.target_fragment_id,
        source_carrier_type=case.source_carrier_type,
        target_carrier_type=case.target_carrier_type,
        allow_identity_simulation=case.allow_identity_simulation,
        identity_simulation_id=case.identity_simulation_id,
        tags=case.tags,
    )
    report: ConstitutionalCaseReport = ConstitutionalChainHarness().execute(invalid_case)
    assert not report.passed
    assert not report.structural_report.structural_valid


def test_constitutional_harness_rejects_same_type_without_identity_simulation() -> None:
    case = FALSIFICATION_CASES[0]
    invalid_case = ConstitutionalChainTestCase(
        case_id=case.case_id,
        title=case.title,
        source_system=case.source_system,
        target_system=case.target_system,
        simulation_map=case.simulation_map,
        expected_verdict=case.expected_verdict,
        expected_violation_codes=case.expected_violation_codes,
        required_intermediate_identities=case.required_intermediate_identities,
        required_trace_anchors=case.required_trace_anchors,
        required_residual_codes=case.required_residual_codes,
        falsification_condition=case.falsification_condition,
        constitutional_law=case.constitutional_law,
        source_fragment_id=case.source_fragment_id,
        target_fragment_id=case.target_fragment_id,
        source_carrier_type="LINGUISTIC_CARRIER",
        target_carrier_type="LINGUISTIC_CARRIER",
        allow_identity_simulation=False,
        identity_simulation_id=None,
        tags=case.tags,
    )
    report: ConstitutionalCaseReport = ConstitutionalChainHarness().execute(invalid_case)
    assert not report.passed
    assert not report.structural_report.structural_valid


def test_constitutional_harness_rejects_untyped_mapping_contract() -> None:
    case = FALSIFICATION_CASES[0]
    invalid_case = ConstitutionalChainTestCase(
        case_id=case.case_id,
        title=case.title,
        source_system=case.source_system,
        target_system=case.target_system,
        simulation_map=case.simulation_map,
        expected_verdict=case.expected_verdict,
        expected_violation_codes=case.expected_violation_codes,
        required_intermediate_identities=case.required_intermediate_identities,
        required_trace_anchors=case.required_trace_anchors,
        required_residual_codes=case.required_residual_codes,
        falsification_condition=case.falsification_condition,
        constitutional_law=case.constitutional_law,
        source_fragment_id=case.source_fragment_id,
        target_fragment_id=case.target_fragment_id,
        source_carrier_type="",
        target_carrier_type="MEASUREMENT_CARRIER",
        allow_identity_simulation=False,
        identity_simulation_id=None,
        tags=case.tags,
    )
    report: ConstitutionalCaseReport = ConstitutionalChainHarness().execute(invalid_case)
    assert not report.passed
    assert not report.structural_report.structural_valid


def test_constitutional_harness_allows_explicit_identity_simulation() -> None:
    case = FALSIFICATION_CASES[0]
    identity_case = ConstitutionalChainTestCase(
        case_id=case.case_id,
        title=case.title,
        source_system=case.source_system,
        target_system=case.target_system,
        simulation_map=case.simulation_map,
        expected_verdict=case.expected_verdict,
        expected_violation_codes=case.expected_violation_codes,
        required_intermediate_identities=case.required_intermediate_identities,
        required_trace_anchors=case.required_trace_anchors,
        required_residual_codes=case.required_residual_codes,
        falsification_condition=case.falsification_condition,
        constitutional_law=case.constitutional_law,
        source_fragment_id=case.source_fragment_id,
        target_fragment_id=case.target_fragment_id,
        source_carrier_type="LINGUISTIC_CARRIER",
        target_carrier_type="LINGUISTIC_CARRIER",
        allow_identity_simulation=True,
        identity_simulation_id="Id_S",
        tags=case.tags,
    )
    report: ConstitutionalCaseReport = ConstitutionalChainHarness().execute(identity_case)
    assert report.passed
    assert report.structural_report.structural_valid
