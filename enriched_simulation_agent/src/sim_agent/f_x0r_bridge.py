from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

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
class FToX0RBridgeReport:
    declaration: MappingBridgeDeclaration
    cases: tuple[FBridgeCaseReport, ...]
    bridge_residuals: tuple[str, ...]


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
    return FToX0RBridgeReport(
        declaration=declaration,
        cases=reports,
        bridge_residuals=(
            EXTERNAL_VALIDITY_RESIDUAL,
            CONSTITUTIONAL_PROMOTION_RESIDUAL,
            BRIDGE_RESIDUAL,
        ),
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
