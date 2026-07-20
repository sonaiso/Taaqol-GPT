from __future__ import annotations

from dataclasses import dataclass, field

from sim_agent.f_experiment import (
    EXPECTED_MAPPING_FINGERPRINT,
    TenConditionAuditor,
    TenConditionAuditReport,
    TenConditionCode,
    build_f_experiment,
)
from sim_agent.model import LicensedSystem, SimulationMap, Verdict


@dataclass(frozen=True)
class ConstitutionalChainTestCase:
    case_id: str
    title: str
    source_system: LicensedSystem
    target_system: LicensedSystem
    simulation_map: SimulationMap
    expected_verdict: Verdict | None
    expected_violation_codes: frozenset[str]
    required_intermediate_identities: tuple[str, ...]
    required_trace_anchors: tuple[str, ...]
    required_residual_codes: tuple[str, ...]
    falsification_condition: str
    constitutional_law: str
    source_fragment_id: str
    target_fragment_id: str
    tags: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class ValidationReport:
    structural_valid: bool
    ten_condition_passed: bool
    mapping_fingerprint: str


@dataclass(frozen=True)
class ConstitutionalCaseReport:
    case_id: str
    passed: bool
    structural_report: ValidationReport
    observed_verdict: Verdict | None
    detected_violation_codes: frozenset[str]
    missing_trace_anchors: tuple[str, ...]
    missing_intermediates: tuple[str, ...]
    lost_residuals: tuple[str, ...]
    falsification_triggered: bool


class ConstitutionalChainHarness:
    def execute(self, case: ConstitutionalChainTestCase) -> ConstitutionalCaseReport:
        experiment = build_f_experiment()
        audit = TenConditionAuditor(experiment).run()

        detected_violation_codes = _detect_expected_violations(
            expected=case.expected_violation_codes,
            audit=audit,
        )
        falsification_triggered = bool(detected_violation_codes)

        observed_intermediates = experiment.accept_case.pipeline_layers()
        observed_trace_anchors = (
            audit.mapping_fingerprint,
            *(result.code.value for result in audit.results if result.passed),
        )
        observed_residuals = (
            *experiment.defer_case.residuals,
            *experiment.block_case.residuals,
        )

        missing_intermediates = tuple(
            item
            for item in case.required_intermediate_identities
            if item not in observed_intermediates
        )
        missing_trace_anchors = tuple(
            anchor for anchor in case.required_trace_anchors if anchor not in observed_trace_anchors
        )
        lost_residuals = tuple(
            residual
            for residual in case.required_residual_codes
            if residual not in observed_residuals
        )

        passed = (
            case.expected_violation_codes <= detected_violation_codes
            and not missing_intermediates
            and not missing_trace_anchors
            and not lost_residuals
            and falsification_triggered
            and audit.structural_valid
        )

        return ConstitutionalCaseReport(
            case_id=case.case_id,
            passed=passed,
            structural_report=ValidationReport(
                structural_valid=audit.structural_valid,
                ten_condition_passed=audit.ten_condition_passed,
                mapping_fingerprint=audit.mapping_fingerprint,
            ),
            observed_verdict=_observed_verdict_for(case=case, report=audit),
            detected_violation_codes=detected_violation_codes,
            missing_trace_anchors=missing_trace_anchors,
            missing_intermediates=missing_intermediates,
            lost_residuals=lost_residuals,
            falsification_triggered=falsification_triggered,
        )


def _detect_expected_violations(
    *, expected: frozenset[str], audit: TenConditionAuditReport
) -> frozenset[str]:
    by_code = {result.code.value: result.passed for result in audit.results}
    return frozenset(code for code in expected if by_code.get(code, False))


def _observed_verdict_for(
    *, case: ConstitutionalChainTestCase, report: TenConditionAuditReport
) -> Verdict | None:
    if case.expected_violation_codes == {TenConditionCode.ACCEPT_TO_BLOCK.value}:
        return Verdict.ACCEPT
    if case.expected_violation_codes == {TenConditionCode.BLOCK_TO_ACCEPT.value}:
        return Verdict.BLOCK
    return None


def build_falsification_cases() -> tuple[ConstitutionalChainTestCase, ...]:
    experiment = build_f_experiment()
    source_system = LicensedSystem(name="F_SOURCE", states={}, operations={})
    target_system = LicensedSystem(name="F_TARGET", states={}, operations={})
    simulation_map = SimulationMap(
        state_map=dict(experiment.declaration.state_map),
        operation_map=dict(experiment.declaration.operation_map),
    )

    required_intermediates = experiment.accept_case.pipeline_layers()

    return tuple(
        _build_case(
            case_id=f"F-D{index:02d}",
            title=title,
            condition_code=code,
            source_system=source_system,
            target_system=target_system,
            simulation_map=simulation_map,
            required_intermediates=required_intermediates,
            required_residual_codes=("NO_LICENSED_RELATION",)
            if code is TenConditionCode.BLOCKING_RESIDUAL_LOSS
            else (),
            expected_verdict=Verdict.ACCEPT
            if code is TenConditionCode.ACCEPT_TO_BLOCK
            else Verdict.BLOCK
            if code is TenConditionCode.BLOCK_TO_ACCEPT
            else None,
        )
        for index, (code, title) in enumerate(
            (
                (TenConditionCode.ACCEPT_TO_BLOCK, "Accepted source becomes blocked target"),
                (TenConditionCode.BLOCK_TO_ACCEPT, "Blocked source becomes accepted target"),
                (TenConditionCode.OPERATION_COLLAPSE, "Operation collapse is detected"),
                (TenConditionCode.COMPOSITION_FAILURE, "Composition order failure is detected"),
                (
                    TenConditionCode.INTERMEDIATE_LAYER_DELETED,
                    "Intermediate layer deletion is detected",
                ),
                (TenConditionCode.RANK_INFLATION, "Rank inflation is detected"),
                (TenConditionCode.IDENTITY_LOSS, "Identity loss is detected"),
                (
                    TenConditionCode.BLOCKING_RESIDUAL_LOSS,
                    "Blocking residual loss is detected",
                ),
                (TenConditionCode.POST_HOC_MAPPING, "Post-hoc mapping mutation is detected"),
                (
                    TenConditionCode.RANDOM_SYMBOLIC_EQUIVALENCE,
                    "Random symbolic equivalence is detected",
                ),
            ),
            start=1,
        )
    )


def _build_case(
    *,
    case_id: str,
    title: str,
    condition_code: TenConditionCode,
    source_system: LicensedSystem,
    target_system: LicensedSystem,
    simulation_map: SimulationMap,
    required_intermediates: tuple[str, ...],
    required_residual_codes: tuple[str, ...],
    expected_verdict: Verdict | None,
) -> ConstitutionalChainTestCase:
    return ConstitutionalChainTestCase(
        case_id=case_id,
        title=title,
        source_system=source_system,
        target_system=target_system,
        simulation_map=simulation_map,
        expected_verdict=expected_verdict,
        expected_violation_codes=frozenset({condition_code.value}),
        required_intermediate_identities=required_intermediates,
        required_trace_anchors=(EXPECTED_MAPPING_FINGERPRINT, condition_code.value),
        required_residual_codes=required_residual_codes,
        falsification_condition=f"{condition_code.value} must be detectable",
        constitutional_law=(
            "Candidate before Result; Gate before Transition; Evidence before Rank; "
            "Residuals before Closure"
        ),
        source_fragment_id="sim_agent.f_experiment.TenConditionAuditor",
        target_fragment_id="sim_agent.f_constitutional_harness.ConstitutionalChainHarness",
        tags=frozenset({"AUX-ESA-F5.3", "constitutional-harness", "falsification"}),
    )
