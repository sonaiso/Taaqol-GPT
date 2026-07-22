from __future__ import annotations

from dataclasses import dataclass, field, replace

from sim_agent.f_experiment import (
    EXPECTED_MAPPING_FINGERPRINT,
    FExperiment,
    FVerdict,
    TenConditionCode,
    build_f_experiment,
)
from sim_agent.f_experiment import (
    Rank as FRank,
)
from sim_agent.model import (
    Domain,
    Identity,
    LicensedSystem,
    Operation,
    Rank,
    SimulationMap,
    State,
    Verdict,
)

LINGUISTIC_CARRIER = "LINGUISTIC_CARRIER"
MEASUREMENT_CARRIER = "MEASUREMENT_CARRIER"


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
    source_carrier_type: str
    target_carrier_type: str
    allow_identity_simulation: bool = False
    identity_simulation_id: str | None = None
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
        baseline = build_f_experiment()
        mutated = _apply_mutation(case=case, baseline=baseline)
        all_violations = _validate_mutation(case=case, baseline=baseline, mutated=mutated)
        detected_violation_codes = frozenset(
            code for code in case.expected_violation_codes if code in all_violations
        )
        falsification_triggered = bool(detected_violation_codes)

        observed_intermediates = mutated.accept_case.pipeline_layers()
        observed_trace_anchors = (
            mutated.declaration.computed_fingerprint(),
            *sorted(all_violations),
        )
        observed_residuals = (
            *mutated.defer_case.residuals,
            *mutated.block_case.residuals,
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
        case_contract_ok = _validate_case_contract(case=case, baseline=baseline)
        observed_verdict = _observed_verdict_for(case=case, mutated=mutated)

        passed = (
            case.expected_violation_codes <= detected_violation_codes
            and not missing_intermediates
            and not missing_trace_anchors
            and not lost_residuals
            and falsification_triggered
            and case_contract_ok
            and baseline.structural_valid()
            and (case.expected_verdict is None or observed_verdict == case.expected_verdict)
        )

        return ConstitutionalCaseReport(
            case_id=case.case_id,
            passed=passed,
            structural_report=ValidationReport(
                structural_valid=baseline.structural_valid() and case_contract_ok,
                ten_condition_passed=not all_violations,
                mapping_fingerprint=mutated.declaration.computed_fingerprint(),
            ),
            observed_verdict=observed_verdict,
            detected_violation_codes=detected_violation_codes,
            missing_trace_anchors=missing_trace_anchors,
            missing_intermediates=missing_intermediates,
            lost_residuals=lost_residuals,
            falsification_triggered=falsification_triggered,
        )


def _validate_case_contract(*, case: ConstitutionalChainTestCase, baseline: FExperiment) -> bool:
    if not case.source_system.states or not case.target_system.states:
        return False
    if not case.source_system.operations or not case.target_system.operations:
        return False
    if not case.simulation_map.state_map or not case.simulation_map.operation_map:
        return False
    if not set(case.simulation_map.state_map.keys()) <= set(case.source_system.states.keys()):
        return False
    if not set(case.simulation_map.state_map.values()) <= set(case.target_system.states.keys()):
        return False
    if not set(case.simulation_map.operation_map) <= set(case.source_system.operations):
        return False
    if not set(case.simulation_map.operation_map.values()) <= set(case.target_system.operations):
        return False

    source_type = case.source_carrier_type.strip()
    target_type = case.target_carrier_type.strip()
    if not source_type or not target_type:
        return False

    if case.allow_identity_simulation:
        if source_type != target_type:
            return False
        return bool(case.identity_simulation_id and case.identity_simulation_id.strip())

    if source_type == target_type:
        return False
    if source_type != LINGUISTIC_CARRIER:
        return False
    if target_type != MEASUREMENT_CARRIER:
        return False
    return (
        baseline.declaration.source_type == LINGUISTIC_CARRIER
        and baseline.declaration.target_type == MEASUREMENT_CARRIER
    )


def _apply_mutation(*, case: ConstitutionalChainTestCase, baseline: FExperiment) -> FExperiment:
    expected = tuple(case.expected_violation_codes)
    if len(expected) != 1:
        raise ValueError("Each falsification case must declare exactly one expected violation code")

    code = TenConditionCode(expected[0])
    if code is TenConditionCode.ACCEPT_TO_BLOCK:
        return replace(
            baseline,
            accept_case=replace(
                baseline.accept_case,
                state_licensed=False,
                protocol_licensed=False,
            ),
        )
    if code is TenConditionCode.BLOCK_TO_ACCEPT:
        return replace(
            baseline,
            block_case=replace(
                baseline.block_case,
                state_licensed=True,
                protocol_licensed=True,
                carrier_known=True,
                surface_visible=True,
                carrier_limited=False,
            ),
        )
    if code is TenConditionCode.OPERATION_COLLAPSE:
        collapsed = "merged_op"
        return replace(baseline, operations=(collapsed, collapsed))
    if code is TenConditionCode.COMPOSITION_FAILURE:
        return replace(baseline, operations=tuple(reversed(baseline.operations)))
    if code is TenConditionCode.INTERMEDIATE_LAYER_DELETED:
        return replace(baseline, accept_case=replace(baseline.accept_case, carrier=""))
    if code is TenConditionCode.RANK_INFLATION:
        return replace(
            baseline,
            accept_case=replace(
                baseline.accept_case,
                rank=FRank.HIGH,
                rank_ceiling=FRank.MEDIUM,
            ),
        )
    if code is TenConditionCode.IDENTITY_LOSS:
        return replace(
            baseline,
            accept_case=replace(
                baseline.accept_case,
                identity=f"{baseline.accept_case.identity}_mutated",
            ),
        )
    if code is TenConditionCode.BLOCKING_RESIDUAL_LOSS:
        return replace(baseline, block_case=replace(baseline.block_case, residuals=()))
    if code is TenConditionCode.POST_HOC_MAPPING:
        declaration = _clone_declaration(baseline)
        declaration.state_map["i3rab_raf3"] = "post_hoc_target"
        return replace(baseline, declaration=declaration)
    if code is TenConditionCode.RANDOM_SYMBOLIC_EQUIVALENCE:
        return replace(
            baseline,
            defer_case=replace(
                baseline.defer_case,
                abstract_state=baseline.accept_case.abstract_state,
                realization=baseline.accept_case.realization,
                carrier="random_symbolic_carrier",
                protocol="random_symbolic_protocol",
            ),
        )
    raise ValueError(f"Unsupported mutation code: {code.value}")


def _clone_declaration(baseline: FExperiment):
    declaration = baseline.declaration
    return type(declaration)(
        state_map=dict(declaration.state_map),
        operation_map=dict(declaration.operation_map),
        source_type=declaration.source_type,
        target_type=declaration.target_type,
        declared_fingerprint=declaration.declared_fingerprint,
    )


def _validate_mutation(
    *,
    case: ConstitutionalChainTestCase,
    baseline: FExperiment,
    mutated: FExperiment,
) -> frozenset[str]:
    violations: set[str] = set()
    if mutated.accept_case.evaluate() == FVerdict.BLOCK:
        violations.add(TenConditionCode.ACCEPT_TO_BLOCK.value)
    if mutated.block_case.evaluate() == FVerdict.ACCEPT:
        violations.add(TenConditionCode.BLOCK_TO_ACCEPT.value)
    if len(mutated.operations) > 1 and len(set(mutated.operations)) == 1:
        violations.add(TenConditionCode.OPERATION_COLLAPSE.value)
    if (
        mutated.operations != baseline.operations
        and tuple(reversed(mutated.operations)) == baseline.operations
    ):
        violations.add(TenConditionCode.COMPOSITION_FAILURE.value)
    if any(not layer for layer in mutated.accept_case.pipeline_layers()):
        violations.add(TenConditionCode.INTERMEDIATE_LAYER_DELETED.value)
    if mutated.accept_case.rank > mutated.accept_case.rank_ceiling:
        violations.add(TenConditionCode.RANK_INFLATION.value)
    if mutated.accept_case.identity != baseline.accept_case.identity:
        violations.add(TenConditionCode.IDENTITY_LOSS.value)
    if mutated.block_case.evaluate() == FVerdict.BLOCK and not mutated.block_case.residuals:
        violations.add(TenConditionCode.BLOCKING_RESIDUAL_LOSS.value)
    if (
        mutated.declaration.has_post_hoc_mutation()
        or mutated.declaration.declared_fingerprint != mutated.declaration.computed_fingerprint()
    ):
        violations.add(TenConditionCode.POST_HOC_MAPPING.value)

    symbolic_match = (
        mutated.accept_case.abstract_state == mutated.defer_case.abstract_state
        and mutated.accept_case.realization == mutated.defer_case.realization
    )
    functional_match = (
        mutated.accept_case.carrier == mutated.defer_case.carrier
        and mutated.accept_case.protocol == mutated.defer_case.protocol
        and mutated.accept_case.evaluate() == mutated.defer_case.evaluate()
    )
    if symbolic_match and not functional_match:
        violations.add(TenConditionCode.RANDOM_SYMBOLIC_EQUIVALENCE.value)

    if not _validate_case_contract(case=case, baseline=baseline):
        violations.add("INVALID_CASE_CONTRACT")
    return frozenset(violations)


def _observed_verdict_for(
    *, case: ConstitutionalChainTestCase, mutated: FExperiment
) -> Verdict | None:
    if case.expected_verdict is None:
        return None
    if case.expected_violation_codes == {TenConditionCode.ACCEPT_TO_BLOCK.value}:
        source_state = mutated.accept_case.abstract_state
        mapped_state = case.simulation_map.state_map.get(source_state)
        if mapped_state in case.target_system.states:
            return Verdict(mutated.accept_case.evaluate().value)
    if case.expected_violation_codes == {TenConditionCode.BLOCK_TO_ACCEPT.value}:
        source_state = mutated.block_case.abstract_state
        mapped_state = case.simulation_map.state_map.get(source_state)
        if mapped_state in case.target_system.states:
            return Verdict(mutated.block_case.evaluate().value)
    return None


def build_falsification_cases() -> tuple[ConstitutionalChainTestCase, ...]:
    experiment = build_f_experiment()
    source_system, target_system = _build_case_systems(experiment)
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
            required_intermediates=()
            if code is TenConditionCode.INTERMEDIATE_LAYER_DELETED
            else required_intermediates,
            required_residual_codes=(),
            required_trace_anchors=(condition_code_anchor(code), code.value),
            expected_verdict=Verdict.BLOCK
            if code is TenConditionCode.ACCEPT_TO_BLOCK
            else Verdict.ACCEPT
            if code is TenConditionCode.BLOCK_TO_ACCEPT
            else None,
            source_carrier_type=experiment.declaration.source_type,
            target_carrier_type=experiment.declaration.target_type,
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


def _build_case_systems(experiment: FExperiment) -> tuple[LicensedSystem, LicensedSystem]:
    source_states = {
        case.abstract_state: State(
            name=case.abstract_state,
            domain=Domain(name="source_domain"),
            identity=Identity(value=case.identity),
            rank=_to_model_rank(case.rank),
        )
        for case in experiment.cases()
    }
    target_state_names = set(experiment.declaration.state_map.values())
    target_states = {
        state_name: State(
            name=state_name,
            domain=Domain(name="target_domain"),
            identity=Identity(value=f"{state_name}_identity"),
            rank=Rank.MEDIUM,
        )
        for state_name in target_state_names
    }
    source_operations = {
        op: Operation(name=op, required_evidence=frozenset({"evidence"}))
        for op in experiment.declaration.operation_map
    }
    target_operations = {
        op: Operation(name=op, required_evidence=frozenset({"evidence"}))
        for op in experiment.declaration.operation_map.values()
    }
    return (
        LicensedSystem(name="F_SOURCE", states=source_states, operations=source_operations),
        LicensedSystem(name="F_TARGET", states=target_states, operations=target_operations),
    )


def _to_model_rank(rank: FRank) -> Rank:
    if rank is FRank.LOW:
        return Rank.LOW
    if rank is FRank.MEDIUM:
        return Rank.MEDIUM
    return Rank.HIGH


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
    required_trace_anchors: tuple[str, ...],
    expected_verdict: Verdict | None,
    source_carrier_type: str,
    target_carrier_type: str,
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
        required_trace_anchors=required_trace_anchors,
        required_residual_codes=required_residual_codes,
        falsification_condition=f"{condition_code.value} must be detectable",
        constitutional_law=(
            "Candidate before Result; Gate before Transition; Evidence before Rank; "
            "Residuals before Closure"
        ),
        source_fragment_id="sim_agent.f_experiment.TenConditionAuditor",
        target_fragment_id="sim_agent.f_constitutional_harness.ConstitutionalChainHarness",
        source_carrier_type=source_carrier_type,
        target_carrier_type=target_carrier_type,
        tags=frozenset({"AUX-ESA-F5.3", "constitutional-harness", "falsification"}),
    )


def condition_code_anchor(code: TenConditionCode) -> str:
    if code is TenConditionCode.POST_HOC_MAPPING:
        return code.value
    return EXPECTED_MAPPING_FINGERPRINT
