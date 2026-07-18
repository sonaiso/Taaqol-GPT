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


class LocalCandidateShapeFailureCode(StrEnum):
    STRICT_AUDIT_REQUIRED = "STRICT_AUDIT_REQUIRED"
    MANDATORY_RESIDUAL_MISSING = "MANDATORY_RESIDUAL_MISSING"


class LocalContractReadinessCheckCode(StrEnum):
    SHAPED_CANDIDATES_PRESENT = "SHAPED_CANDIDATES_PRESENT"
    AUXILIARY_SURFACE_LOCKED = "AUXILIARY_SURFACE_LOCKED"
    REQUIRED_IDENTITY_FIELDS_PRESENT = "REQUIRED_IDENTITY_FIELDS_PRESENT"
    NON_ADMISSION_RESIDUALS_VISIBLE = "NON_ADMISSION_RESIDUALS_VISIBLE"
    NO_ADMISSION_FLAGS_IN_CANDIDATES = "NO_ADMISSION_FLAGS_IN_CANDIDATES"


class LocalContractReadinessFailureCode(StrEnum):
    SHAPED_CANDIDATES_REQUIRED = "SHAPED_CANDIDATES_REQUIRED"
    AUXILIARY_LOCK_REQUIRED = "AUXILIARY_LOCK_REQUIRED"
    REQUIRED_FIELDS_MISSING = "REQUIRED_FIELDS_MISSING"
    MANDATORY_RESIDUAL_MISSING = "MANDATORY_RESIDUAL_MISSING"
    NON_ADMISSION_FLAG_VIOLATION = "NON_ADMISSION_FLAG_VIOLATION"


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


@dataclass(frozen=True)
class LocalShapedX0RCandidate:
    case_name: str
    origin: str
    branch: str
    readiness_state: LocalTransitionReadinessState
    rank: int
    residuals: tuple[str, ...]
    auxiliary_only: bool
    admitted: bool
    chain_advancing: bool
    external_validity_certified: bool


@dataclass(frozen=True)
class LocalCandidateShapingResult:
    shaped: bool
    failure_code: LocalCandidateShapeFailureCode | None
    candidates: tuple[LocalShapedX0RCandidate, ...]
    carry_forward_residuals: tuple[str, ...]
    auxiliary_only: bool
    non_admitted: bool
    non_chain_advancing: bool
    external_validity_certified: bool


@dataclass(frozen=True)
class LocalContractReadinessCheck:
    code: LocalContractReadinessCheckCode
    passed: bool
    detail: str


@dataclass(frozen=True)
class LocalContractResidualMatrix:
    admission_blocking_residuals: tuple[str, ...]
    bridge_deferred_residuals: tuple[str, ...]
    observed_residuals: tuple[str, ...]


@dataclass(frozen=True)
class LocalContractReadinessResult:
    contract_ready: bool
    failure_code: LocalContractReadinessFailureCode | None
    checks: tuple[LocalContractReadinessCheck, ...]
    residual_matrix: LocalContractResidualMatrix
    carry_forward_residuals: tuple[str, ...]
    auxiliary_only: bool
    non_admitted: bool
    non_chain_advancing: bool
    external_validity_certified: bool


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


def shape_f_to_x0r_local_candidates(report: FToX0RBridgeReport) -> LocalCandidateShapingResult:
    required_residuals = _required_non_admission_residuals()
    if not report.strict_field_completion_audit.all_passed:
        return LocalCandidateShapingResult(
            shaped=False,
            failure_code=LocalCandidateShapeFailureCode.STRICT_AUDIT_REQUIRED,
            candidates=(),
            carry_forward_residuals=required_residuals,
            auxiliary_only=True,
            non_admitted=True,
            non_chain_advancing=True,
            external_validity_certified=False,
        )
    if not _shape_has_required_residuals(report=report, required_residuals=required_residuals):
        return LocalCandidateShapingResult(
            shaped=False,
            failure_code=LocalCandidateShapeFailureCode.MANDATORY_RESIDUAL_MISSING,
            candidates=(),
            carry_forward_residuals=required_residuals,
            auxiliary_only=True,
            non_admitted=True,
            non_chain_advancing=True,
            external_validity_certified=False,
        )

    candidates = tuple(
        LocalShapedX0RCandidate(
            case_name=case.case_name,
            origin=report.declaration.origin,
            branch=report.declaration.branch,
            readiness_state=case.local_decision.readiness_state,
            rank=case.audit.rank,
            residuals=tuple(dict.fromkeys((*case.audit.residuals, BRIDGE_RESIDUAL))),
            auxiliary_only=True,
            admitted=False,
            chain_advancing=False,
            external_validity_certified=False,
        )
        for case in report.cases
    )
    return LocalCandidateShapingResult(
        shaped=True,
        failure_code=None,
        candidates=candidates,
        carry_forward_residuals=required_residuals,
        auxiliary_only=True,
        non_admitted=True,
        non_chain_advancing=True,
        external_validity_certified=False,
    )


def assess_local_contract_readiness_preconditions(
    shaping: LocalCandidateShapingResult,
) -> LocalContractReadinessResult:
    required_residuals = _required_non_admission_residuals()
    candidates = shaping.candidates
    shaped_candidates_present = (
        shaping.shaped and shaping.failure_code is None and bool(candidates)
    )
    auxiliary_surface_locked = (
        shaping.auxiliary_only
        and shaping.non_admitted
        and shaping.non_chain_advancing
        and not shaping.external_validity_certified
    )
    required_identity_fields_present = all(
        candidate.origin.strip() and candidate.branch.strip() for candidate in candidates
    )
    non_admission_residuals_visible = (
        all(residual in shaping.carry_forward_residuals for residual in required_residuals)
        and all(
            all(residual in candidate.residuals for residual in required_residuals)
            for candidate in candidates
        )
    )
    no_admission_flags_in_candidates = all(
        candidate.auxiliary_only
        and not candidate.admitted
        and not candidate.chain_advancing
        and not candidate.external_validity_certified
        for candidate in candidates
    )

    checks = (
        LocalContractReadinessCheck(
            code=LocalContractReadinessCheckCode.SHAPED_CANDIDATES_PRESENT,
            passed=shaped_candidates_present,
            detail="F5 preconditions require shaped local candidates from F4",
        ),
        LocalContractReadinessCheck(
            code=LocalContractReadinessCheckCode.AUXILIARY_SURFACE_LOCKED,
            passed=auxiliary_surface_locked,
            detail="surface must remain auxiliary-only, non-admitted, non-chain-advancing",
        ),
        LocalContractReadinessCheck(
            code=LocalContractReadinessCheckCode.REQUIRED_IDENTITY_FIELDS_PRESENT,
            passed=required_identity_fields_present,
            detail="each candidate must carry non-empty origin and branch",
        ),
        LocalContractReadinessCheck(
            code=LocalContractReadinessCheckCode.NON_ADMISSION_RESIDUALS_VISIBLE,
            passed=non_admission_residuals_visible,
            detail=(
                "non-admission residuals must remain explicit in carried "
                "and candidate residuals"
            ),
        ),
        LocalContractReadinessCheck(
            code=LocalContractReadinessCheckCode.NO_ADMISSION_FLAGS_IN_CANDIDATES,
            passed=no_admission_flags_in_candidates,
            detail="candidate flags must not claim admission, chain progress, or external validity",
        ),
    )

    failure_code = _resolve_contract_readiness_failure(
        shaped_candidates_present=shaped_candidates_present,
        auxiliary_surface_locked=auxiliary_surface_locked,
        required_identity_fields_present=required_identity_fields_present,
        non_admission_residuals_visible=non_admission_residuals_visible,
        no_admission_flags_in_candidates=no_admission_flags_in_candidates,
    )

    residual_matrix = LocalContractResidualMatrix(
        admission_blocking_residuals=(
            EXTERNAL_VALIDITY_RESIDUAL,
            CONSTITUTIONAL_PROMOTION_RESIDUAL,
        ),
        bridge_deferred_residuals=(BRIDGE_RESIDUAL,),
        observed_residuals=_collect_observed_residuals(shaping),
    )
    return LocalContractReadinessResult(
        contract_ready=failure_code is None,
        failure_code=failure_code,
        checks=checks,
        residual_matrix=residual_matrix,
        carry_forward_residuals=shaping.carry_forward_residuals,
        auxiliary_only=True,
        non_admitted=True,
        non_chain_advancing=True,
        external_validity_certified=False,
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


def _required_non_admission_residuals() -> tuple[str, ...]:
    return (
        EXTERNAL_VALIDITY_RESIDUAL,
        CONSTITUTIONAL_PROMOTION_RESIDUAL,
        BRIDGE_RESIDUAL,
    )


def _shape_has_required_residuals(
    report: FToX0RBridgeReport, required_residuals: tuple[str, ...]
) -> bool:
    if not all(residual in report.bridge_residuals for residual in required_residuals):
        return False
    return all(
        EXTERNAL_VALIDITY_RESIDUAL in case.audit.residuals
        and CONSTITUTIONAL_PROMOTION_RESIDUAL in case.audit.residuals
        for case in report.cases
    )


def _resolve_contract_readiness_failure(
    *,
    shaped_candidates_present: bool,
    auxiliary_surface_locked: bool,
    required_identity_fields_present: bool,
    non_admission_residuals_visible: bool,
    no_admission_flags_in_candidates: bool,
) -> LocalContractReadinessFailureCode | None:
    if not shaped_candidates_present:
        return LocalContractReadinessFailureCode.SHAPED_CANDIDATES_REQUIRED
    if not auxiliary_surface_locked:
        return LocalContractReadinessFailureCode.AUXILIARY_LOCK_REQUIRED
    if not required_identity_fields_present:
        return LocalContractReadinessFailureCode.REQUIRED_FIELDS_MISSING
    if not non_admission_residuals_visible:
        return LocalContractReadinessFailureCode.MANDATORY_RESIDUAL_MISSING
    if not no_admission_flags_in_candidates:
        return LocalContractReadinessFailureCode.NON_ADMISSION_FLAG_VIOLATION
    return None


def _collect_observed_residuals(shaping: LocalCandidateShapingResult) -> tuple[str, ...]:
    merged = list(shaping.carry_forward_residuals)
    for candidate in shaping.candidates:
        merged.extend(candidate.residuals)
    return tuple(dict.fromkeys(merged))
