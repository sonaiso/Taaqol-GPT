from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from sim_agent.f_experiment import FExperiment, FVerdict, build_f_experiment, run_f_experiment

EXTERNAL_VALIDITY_RESIDUAL = "EXTERNAL_VALIDITY_NOT_PROVEN"
CONSTITUTIONAL_PROMOTION_RESIDUAL = "AUXILIARY_NOT_MAIN_CHAIN"
BRIDGE_RESIDUAL = "X0R_CONTRACT_BRIDGE_PENDING"


class LocalTransitionReadinessState(StrEnum):
    LINK_READY = "LINK_READY"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class LocalFailureCode(StrEnum):
    GATE_REQUIRED = "GATE_REQUIRED"
    BLOCKING_RESIDUAL_PRESENT = "BLOCKING_RESIDUAL_PRESENT"


class StrictX0RFieldCheckCode(StrEnum):
    ORIGIN_PRESENT = "ORIGIN_PRESENT"
    BRANCH_PRESENT = "BRANCH_PRESENT"
    PRESERVED_IDENTITY_PRESENT = "PRESERVED_IDENTITY_PRESENT"
    EVIDENCE_FINGERPRINT_PRESENT = "EVIDENCE_FINGERPRINT_PRESENT"
    CONDITION_SABAB_PREVENTER_SEPARATE = "CONDITION_SABAB_PREVENTER_SEPARATE"
    RANK_PROJECTION_NO_KERNEL_PROMOTION = "RANK_PROJECTION_NO_KERNEL_PROMOTION"
    REQUIRED_RESIDUALS_PRESERVED = "REQUIRED_RESIDUALS_PRESERVED"
    NO_KERNEL_X0R_IMPORT = "NO_KERNEL_X0R_IMPORT"
    NO_EUCLIDEAN_TRANSITION_CONTRACT_MUTATION = "NO_EUCLIDEAN_TRANSITION_CONTRACT_MUTATION"
    NO_KERNEL_CAN_TRANSITION_CALL = "NO_KERNEL_CAN_TRANSITION_CALL"


@dataclass(frozen=True)
class MappingBridgeDeclaration:
    origin: str
    branch: str
    preserved_identity: bool
    evidence_fingerprint: str


@dataclass(frozen=True)
class LocalEuclideanGateDecision:
    transition_allowed: bool
    readiness_state: LocalTransitionReadinessState
    failure_code: LocalFailureCode | None


@dataclass(frozen=True)
class FBridgeAuditSnapshot:
    condition: bool
    sabab: bool
    preventer: bool
    rank: int
    residuals: tuple[str, ...]


@dataclass(frozen=True)
class FBridgeCaseReport:
    case_name: str
    source_verdict: FVerdict
    audit: FBridgeAuditSnapshot
    local_decision: LocalEuclideanGateDecision


@dataclass(frozen=True)
class StrictX0RFieldCheck:
    code: StrictX0RFieldCheckCode
    passed: bool
    detail: str


@dataclass(frozen=True)
class StrictX0RFieldCompletionAudit:
    all_passed: bool
    checks: tuple[StrictX0RFieldCheck, ...]


@dataclass(frozen=True)
class FToX0RBridgeReport:
    declaration: MappingBridgeDeclaration
    cases: tuple[FBridgeCaseReport, ...]
    bridge_residuals: tuple[str, ...]
    strict_field_completion_audit: StrictX0RFieldCompletionAudit


def bridge_f_experiment_to_x0r_vocabulary(
    experiment: FExperiment | None = None,
) -> FToX0RBridgeReport:
    experiment = experiment or build_f_experiment()
    audit = run_f_experiment()

    mapped_origin = experiment.accept_case.abstract_state
    mapped_branch = experiment.declaration.state_map.get(mapped_origin, "")
    declaration = MappingBridgeDeclaration(
        origin=mapped_origin,
        branch=mapped_branch,
        preserved_identity=_preserved_identity(experiment),
        evidence_fingerprint=audit.mapping_fingerprint,
    )
    reports = (
        _bridge_case("accept_case", experiment.accept_case.evaluate(), experiment, audit),
        _bridge_case("defer_case", experiment.defer_case.evaluate(), experiment, audit),
        _bridge_case("block_case", experiment.block_case.evaluate(), experiment, audit),
    )
    bridge_residuals = (
        EXTERNAL_VALIDITY_RESIDUAL,
        CONSTITUTIONAL_PROMOTION_RESIDUAL,
        BRIDGE_RESIDUAL,
    )
    strict_audit = _strict_field_completion_audit(
        declaration=declaration,
        cases=reports,
        bridge_residuals=bridge_residuals,
        experiment=experiment,
    )
    return FToX0RBridgeReport(
        declaration=declaration,
        cases=reports,
        bridge_residuals=bridge_residuals,
        strict_field_completion_audit=strict_audit,
    )


def _preserved_identity(experiment: FExperiment) -> bool:
    identities = tuple(case.identity for case in experiment.cases())
    has_nonempty = all(identity.strip() for identity in identities)
    return has_nonempty and len(set(identities)) == len(identities)


def _bridge_case(
    case_name: str,
    verdict: FVerdict,
    experiment: FExperiment,
    audit_report,
) -> FBridgeCaseReport:
    audit = FBridgeAuditSnapshot(
        condition=experiment.structural_valid(),
        sabab=audit_report.ten_condition_passed,
        preventer=verdict is FVerdict.BLOCK,
        rank=_rank_for(verdict, experiment),
        residuals=_residuals_for(verdict, experiment),
    )
    decision = _decision_for(verdict)
    return FBridgeCaseReport(
        case_name=case_name,
        source_verdict=verdict,
        audit=audit,
        local_decision=decision,
    )


def _decision_for(verdict: FVerdict) -> LocalEuclideanGateDecision:
    if verdict is FVerdict.ACCEPT:
        return LocalEuclideanGateDecision(
            transition_allowed=True,
            readiness_state=LocalTransitionReadinessState.LINK_READY,
            failure_code=None,
        )
    if verdict is FVerdict.DEFER:
        return LocalEuclideanGateDecision(
            transition_allowed=False,
            readiness_state=LocalTransitionReadinessState.DEFERRED,
            failure_code=LocalFailureCode.GATE_REQUIRED,
        )
    return LocalEuclideanGateDecision(
        transition_allowed=False,
        readiness_state=LocalTransitionReadinessState.BLOCKED,
        failure_code=LocalFailureCode.BLOCKING_RESIDUAL_PRESENT,
    )


def _rank_for(verdict: FVerdict, experiment: FExperiment) -> int:
    if verdict is FVerdict.ACCEPT:
        return int(experiment.accept_case.rank)
    if verdict is FVerdict.DEFER:
        return int(experiment.defer_case.rank)
    return int(experiment.block_case.rank)


def _residuals_for(verdict: FVerdict, experiment: FExperiment) -> tuple[str, ...]:
    if verdict is FVerdict.ACCEPT:
        base_residuals: tuple[str, ...] = ()
    elif verdict is FVerdict.DEFER:
        base_residuals = experiment.defer_case.residuals
    else:
        base_residuals = experiment.block_case.residuals

    merged = (*base_residuals, EXTERNAL_VALIDITY_RESIDUAL, CONSTITUTIONAL_PROMOTION_RESIDUAL)
    return tuple(dict.fromkeys(merged))


def _strict_field_completion_audit(
    declaration: MappingBridgeDeclaration,
    cases: tuple[FBridgeCaseReport, ...],
    bridge_residuals: tuple[str, ...],
    experiment: FExperiment,
) -> StrictX0RFieldCompletionAudit:
    source = Path(__file__).read_text(encoding="utf-8")
    source_tree = ast.parse(source)
    expected_rank_by_case = {
        "accept_case": min(
            int(experiment.accept_case.rank), int(experiment.accept_case.rank_ceiling)
        ),
        "defer_case": min(int(experiment.defer_case.rank), int(experiment.defer_case.rank_ceiling)),
        "block_case": min(int(experiment.block_case.rank), int(experiment.block_case.rank_ceiling)),
    }
    checks = (
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.ORIGIN_PRESENT,
            passed=bool(declaration.origin.strip()),
            detail="declaration.origin must be non-empty",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.BRANCH_PRESENT,
            passed=bool(declaration.branch.strip()),
            detail="declaration.branch must be non-empty",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.PRESERVED_IDENTITY_PRESENT,
            passed=declaration.preserved_identity,
            detail="preserved_identity must remain true",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.EVIDENCE_FINGERPRINT_PRESENT,
            passed=bool(declaration.evidence_fingerprint.strip()),
            detail="evidence_fingerprint must be present",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.CONDITION_SABAB_PREVENTER_SEPARATE,
            passed=_fields_are_separate(cases),
            detail="condition/sabab/preventer must remain independently carried booleans",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.RANK_PROJECTION_NO_KERNEL_PROMOTION,
            passed=all(
                case.audit.rank <= expected_rank_by_case[case.case_name]
                for case in cases
                if case.case_name in expected_rank_by_case
            ),
            detail="local rank projection must not exceed source rank or rank ceiling",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.REQUIRED_RESIDUALS_PRESERVED,
            passed=_required_residuals_present(cases=cases, bridge_residuals=bridge_residuals),
            detail="mandatory non-admission residuals must stay visible",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.NO_KERNEL_X0R_IMPORT,
            passed=_no_kernel_x0r_import(source_tree),
            detail="bridge must not import kernel x0r modules",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.NO_EUCLIDEAN_TRANSITION_CONTRACT_MUTATION,
            passed=_no_contract_mutation_reference(source_tree),
            detail="bridge must not reference kernel EuclideanTransitionContract",
        ),
        StrictX0RFieldCheck(
            code=StrictX0RFieldCheckCode.NO_KERNEL_CAN_TRANSITION_CALL,
            passed=_no_kernel_transition_call(source_tree),
            detail="bridge must not call kernel can_transition()",
        ),
    )
    return StrictX0RFieldCompletionAudit(
        all_passed=all(check.passed for check in checks),
        checks=checks,
    )


def _fields_are_separate(cases: tuple[FBridgeCaseReport, ...]) -> bool:
    if not cases:
        return False
    has_structural_bool_surface = all(
        isinstance(case.audit.condition, bool)
        and isinstance(case.audit.sabab, bool)
        and isinstance(case.audit.preventer, bool)
        for case in cases
    )
    has_non_collapsed_signal = any(
        case.audit.condition != case.audit.preventer for case in cases
    ) and any(
        case.audit.sabab != case.audit.preventer
        for case in cases
    )
    return has_structural_bool_surface and has_non_collapsed_signal


def _required_residuals_present(
    cases: tuple[FBridgeCaseReport, ...], bridge_residuals: tuple[str, ...]
) -> bool:
    bridge_has_required = (
        EXTERNAL_VALIDITY_RESIDUAL in bridge_residuals
        and CONSTITUTIONAL_PROMOTION_RESIDUAL in bridge_residuals
        and BRIDGE_RESIDUAL in bridge_residuals
    )
    case_residuals_preserved = all(
        EXTERNAL_VALIDITY_RESIDUAL in case.audit.residuals
        and CONSTITUTIONAL_PROMOTION_RESIDUAL in case.audit.residuals
        for case in cases
    )
    return bridge_has_required and case_residuals_preserved


def _no_kernel_x0r_import(source_tree: ast.AST) -> bool:
    for node in ast.walk(source_tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("taaqqul_slot_geometry.x0r"):
                    return False
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith("taaqqul_slot_geometry.x0r"):
                return False
    return True


def _no_contract_mutation_reference(source_tree: ast.AST) -> bool:
    forbidden_identifier = "EuclideanTransition" + "Contract"
    for node in ast.walk(source_tree):
        if isinstance(node, ast.Name) and node.id == forbidden_identifier:
            return False
        if isinstance(node, ast.Attribute) and node.attr == forbidden_identifier:
            return False
    return True


def _no_kernel_transition_call(source_tree: ast.AST) -> bool:
    forbidden_name = "can_" + "transition"
    for node in ast.walk(source_tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == forbidden_name:
            return False
        if isinstance(node.func, ast.Attribute) and node.func.attr == forbidden_name:
            return False
    return True
