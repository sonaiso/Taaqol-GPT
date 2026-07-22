from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum


class BoundaryStatus(StrEnum):
    DEFINED = "DEFINED"
    UNDEFINED = "UNDEFINED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class DomainCheckState(StrEnum):
    PASS = "PASS"
    DELEGATED = "DELEGATED"
    BLOCKED = "BLOCKED"


class ClosureState(StrEnum):
    CLOSED = "CLOSED"
    CLOSED_WITH_RESIDUALS = "CLOSED_WITH_RESIDUALS"
    DEFERRED = "DEFERRED"
    AMBIGUOUS = "AMBIGUOUS"
    BLOCKED = "BLOCKED"
    REOPEN_REQUIRED = "REOPEN_REQUIRED"


class ExplicitResultKind(StrEnum):
    SUCCESS = "SUCCESS"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    UNDEFINED = "UNDEFINED"
    FAILURE = "FAILURE"


@dataclass(frozen=True)
class CandidateProposal:
    operation_id: str
    input_ids: tuple[str, ...]
    input_types: tuple[str, ...]
    target_type: str
    source_domain: str
    target_domain: str
    evidence_ids: tuple[str, ...]
    expected_effect: str
    identity_snapshot: dict[str, str]
    input_rank: int


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    evidence_type: str
    source: str
    domain: str
    rank: int
    valid: bool = True
    revoked: bool = False


@dataclass(frozen=True)
class ResidualRecord:
    code: str
    severity: str
    source: str
    effect: str
    blocking: bool
    remediation: str
    reopen_target: str | None = None


@dataclass(frozen=True)
class DomainContext:
    licensed_bridges: frozenset[tuple[str, str]] = frozenset()
    delegated_bridges: frozenset[tuple[str, str]] = frozenset()
    bridge_rank: int = 0


@dataclass(frozen=True)
class AuthorizationCheck:
    stage: str
    passed: bool
    code: str
    detail: str


@dataclass(frozen=True)
class OperationContract:
    operation_id: str
    source_types: frozenset[str]
    target_type: str
    domain: str
    preconditions: tuple[str, ...]
    evidence_policy: frozenset[str]
    blockers: frozenset[str]
    identity_policy: frozenset[str]
    effect_function: Callable[[ApprovedTransitionContext], dict[str, str]]
    rank_policy: int
    residual_policy: tuple[str, ...] = ()
    closure_policy: str = "LOCAL_CLOSURE"
    transition_policy: tuple[str, ...] = ()


@dataclass(frozen=True)
class ApprovedTransitionContext:
    contract: OperationContract
    proposal: CandidateProposal
    evidence: tuple[EvidenceItem, ...]
    context: DomainContext
    checks: tuple[AuthorizationCheck, ...]
    declared_effect: str
    preserved_identities: tuple[str, ...]


@dataclass(frozen=True)
class AuthorizationDecision:
    is_approved: bool
    boundary_status: BoundaryStatus
    checks: tuple[AuthorizationCheck, ...]
    failure_code: str | None
    residuals: tuple[ResidualRecord, ...]
    approved_context: ApprovedTransitionContext | None = None

    def to_explicit_result(self) -> TransitionResult:
        kind_map = {
            BoundaryStatus.UNDEFINED: ExplicitResultKind.UNDEFINED,
            BoundaryStatus.DEFERRED: ExplicitResultKind.DEFERRED,
            BoundaryStatus.BLOCKED: ExplicitResultKind.BLOCKED,
            BoundaryStatus.DEFINED: ExplicitResultKind.FAILURE,
        }
        return TransitionResult(
            kind=kind_map[self.boundary_status],
            status=self.boundary_status,
            failure_code=self.failure_code,
            output=None,
            residuals=self.residuals,
            checks=self.checks,
            trace=None,
            closure_state=ClosureState.BLOCKED
            if self.boundary_status is BoundaryStatus.BLOCKED
            else ClosureState.DEFERRED,
            transition_readiness=(),
            rank_after=0,
        )


@dataclass(frozen=True)
class TraceEvent:
    input_ids: tuple[str, ...]
    operation_id: str
    contract_version: str
    evidence_ids: tuple[str, ...]
    checks: tuple[str, ...]
    preserved_identities: tuple[str, ...]
    declared_effect: str
    rank_before: int
    rank_after: int
    residuals: tuple[str, ...]
    output_id: str


@dataclass(frozen=True)
class TransitionResult:
    kind: ExplicitResultKind
    status: BoundaryStatus
    failure_code: str | None
    output: dict[str, str] | None
    residuals: tuple[ResidualRecord, ...]
    checks: tuple[AuthorizationCheck, ...]
    trace: TraceEvent | None
    closure_state: ClosureState
    transition_readiness: tuple[str, ...]
    rank_after: int


def authorize(
    *,
    proposal: CandidateProposal,
    contract: OperationContract,
    evidence: tuple[EvidenceItem, ...],
    context: DomainContext,
    active_blockers: frozenset[str] = frozenset(),
) -> AuthorizationDecision:
    checks: list[AuthorizationCheck] = []

    type_ok = (
        proposal.operation_id == contract.operation_id
        and set(proposal.input_types) <= contract.source_types
        and proposal.target_type == contract.target_type
    )
    checks.append(
        AuthorizationCheck(
            stage="TypeCheck",
            passed=type_ok,
            code="TYPE_OK" if type_ok else "TYPE_MISMATCH",
            detail=f"expected={sorted(contract.source_types)} received={proposal.input_types}",
        )
    )
    if not type_ok:
        return _blocked_decision(
            status=BoundaryStatus.UNDEFINED,
            checks=checks,
            failure_code="TYPE_MISMATCH",
            residual_code="TYPE_MISMATCH",
            detail="operation inputs are outside contract source types",
        )

    bridge = (proposal.source_domain, proposal.target_domain)
    if (
        proposal.source_domain == contract.domain
        and proposal.target_domain == contract.domain
        or bridge in context.licensed_bridges
    ):
        domain_state = DomainCheckState.PASS
    elif bridge in context.delegated_bridges:
        domain_state = DomainCheckState.DELEGATED
    else:
        domain_state = DomainCheckState.BLOCKED

    checks.append(
        AuthorizationCheck(
            stage="DomainCheck",
            passed=domain_state is DomainCheckState.PASS,
            code=f"DOMAIN_{domain_state.value}",
            detail=f"bridge={bridge}",
        )
    )
    if domain_state is DomainCheckState.DELEGATED:
        return _blocked_decision(
            status=BoundaryStatus.DEFERRED,
            checks=checks,
            failure_code="DOMAIN_DELEGATED",
            residual_code="DOMAIN_BRIDGE_REVIEW_REQUIRED",
            detail="domain bridge requires path auditor",
        )
    if domain_state is DomainCheckState.BLOCKED:
        return _blocked_decision(
            status=BoundaryStatus.BLOCKED,
            checks=checks,
            failure_code="FORBIDDEN_DOMAIN_LEAP",
            residual_code="FORBIDDEN_DOMAIN_LEAP",
            detail="domain bridge is not licensed",
        )

    missing_preconditions = tuple(
        pre for pre in contract.preconditions if pre not in proposal.identity_snapshot
    )
    preconditions_ok = not missing_preconditions
    checks.append(
        AuthorizationCheck(
            stage="PreconditionsCheck",
            passed=preconditions_ok,
            code="PRECONDITIONS_OK" if preconditions_ok else "PRECONDITION_MISSING",
            detail=",".join(missing_preconditions) if missing_preconditions else "all present",
        )
    )
    if not preconditions_ok:
        return _blocked_decision(
            status=BoundaryStatus.DEFERRED,
            checks=checks,
            failure_code="PRECONDITION_MISSING",
            residual_code=missing_preconditions[0],
            detail="required preconditions are missing",
        )

    required_evidence = contract.evidence_policy
    evidence_types = {item.evidence_type for item in evidence if item.valid and not item.revoked}
    evidence_domains = {item.domain for item in evidence if item.valid and not item.revoked}
    evidence_ok = required_evidence <= evidence_types and contract.domain in evidence_domains
    checks.append(
        AuthorizationCheck(
            stage="EvidenceCheck",
            passed=evidence_ok,
            code="EVIDENCE_OK" if evidence_ok else "EVIDENCE_INSUFFICIENT",
            detail=f"required={sorted(required_evidence)} observed={sorted(evidence_types)}",
        )
    )
    if not evidence_ok:
        return _blocked_decision(
            status=BoundaryStatus.DEFERRED,
            checks=checks,
            failure_code="EVIDENCE_INSUFFICIENT",
            residual_code="EVIDENCE_INSUFFICIENT",
            detail="required evidence is missing or out-of-domain",
        )

    blocking = bool(contract.blockers & active_blockers)
    checks.append(
        AuthorizationCheck(
            stage="BlockerCheck",
            passed=not blocking,
            code="BLOCKER_FREE" if not blocking else "BLOCKER_PRESENT",
            detail=f"active={sorted(contract.blockers & active_blockers)}",
        )
    )
    if blocking:
        return _blocked_decision(
            status=BoundaryStatus.BLOCKED,
            checks=checks,
            failure_code="BLOCKING_RESIDUAL_PRESENT",
            residual_code="BLOCKING_RESIDUAL_PRESENT",
            detail="blocking residuals prevent execution",
        )

    missing_identity = tuple(
        key for key in contract.identity_policy if key not in proposal.identity_snapshot
    )
    identity_precheck_ok = not missing_identity
    checks.append(
        AuthorizationCheck(
            stage="IdentityCheck",
            passed=identity_precheck_ok,
            code="IDENTITY_POLICY_OK" if identity_precheck_ok else "IDENTITY_POLICY_MISSING",
            detail=",".join(missing_identity) if missing_identity else "all identities present",
        )
    )
    if not identity_precheck_ok:
        return _blocked_decision(
            status=BoundaryStatus.DEFERRED,
            checks=checks,
            failure_code="IDENTITY_POLICY_MISSING",
            residual_code="IDENTITY_POLICY_MISSING",
            detail="identity invariants are incomplete",
        )

    approved_context = ApprovedTransitionContext(
        contract=contract,
        proposal=proposal,
        evidence=evidence,
        context=context,
        checks=tuple(checks),
        declared_effect=proposal.expected_effect,
        preserved_identities=tuple(sorted(contract.identity_policy)),
    )
    return AuthorizationDecision(
        is_approved=True,
        boundary_status=BoundaryStatus.DEFINED,
        checks=tuple(checks),
        failure_code=None,
        residuals=(),
        approved_context=approved_context,
    )


def process(
    *,
    proposal: CandidateProposal,
    contract: OperationContract,
    evidence: tuple[EvidenceItem, ...],
    context: DomainContext,
    active_blockers: frozenset[str] = frozenset(),
) -> TransitionResult:
    authorization = authorize(
        proposal=proposal,
        contract=contract,
        evidence=evidence,
        context=context,
        active_blockers=active_blockers,
    )
    if not authorization.is_approved:
        return authorization.to_explicit_result()
    if authorization.approved_context is None:
        raise RuntimeError("Approved authorization must contain ApprovedTransitionContext")

    effect = execute_effect(authorization.approved_context)
    identity_ok = _identity_preserved(
        before=proposal.identity_snapshot,
        after=effect,
        required=contract.identity_policy,
    )
    if not identity_ok:
        return TransitionResult(
            kind=ExplicitResultKind.FAILURE,
            status=BoundaryStatus.DEFINED,
            failure_code="IDENTITY_VIOLATION",
            output=effect,
            residuals=(
                ResidualRecord(
                    code="IDENTITY_VIOLATION",
                    severity="HIGH",
                    source="IdentityCheck",
                    effect="execution rejected",
                    blocking=True,
                    remediation="restore required identity fields before closure",
                    reopen_target="IdentityCheck",
                ),
            ),
            checks=authorization.checks,
            trace=None,
            closure_state=ClosureState.REOPEN_REQUIRED,
            transition_readiness=(),
            rank_after=0,
        )

    rank_after, rank_residual = _apply_rank_bound(
        input_rank=proposal.input_rank,
        evidence_rank=max(item.rank for item in evidence),
        operation_rank=contract.rank_policy,
        bridge_rank=context.bridge_rank,
    )
    residuals = tuple(
        record
        for record in (
            rank_residual,
            *(
                ResidualRecord(
                    code=code,
                    severity="LOW",
                    source="ResidualEmit",
                    effect="carry forward",
                    blocking=False,
                    remediation="review before next transition",
                )
                for code in contract.residual_policy
            ),
        )
        if record is not None
    )
    trace = _commit_trace(
        proposal=proposal,
        contract=contract,
        checks=authorization.checks,
        residuals=residuals,
        rank_after=rank_after,
        output_id=effect.get("output_id", "unknown_output"),
    )
    closure = _evaluate_closure(residuals)
    readiness = _evaluate_transition_readiness(
        closure_state=closure,
        transition_policy=contract.transition_policy,
    )
    return TransitionResult(
        kind=ExplicitResultKind.SUCCESS,
        status=BoundaryStatus.DEFINED,
        failure_code=None,
        output=effect,
        residuals=residuals,
        checks=authorization.checks,
        trace=trace,
        closure_state=closure,
        transition_readiness=readiness,
        rank_after=rank_after,
    )


def execute_effect(approved_context: ApprovedTransitionContext) -> dict[str, str]:
    if not isinstance(approved_context, ApprovedTransitionContext):
        raise TypeError("execute_effect requires ApprovedTransitionContext")
    return approved_context.contract.effect_function(approved_context)


def _blocked_decision(
    *,
    status: BoundaryStatus,
    checks: list[AuthorizationCheck],
    failure_code: str,
    residual_code: str,
    detail: str,
) -> AuthorizationDecision:
    return AuthorizationDecision(
        is_approved=False,
        boundary_status=status,
        checks=tuple(checks),
        failure_code=failure_code,
        residuals=(
            ResidualRecord(
                code=residual_code,
                severity="HIGH" if status is BoundaryStatus.BLOCKED else "MEDIUM",
                source=checks[-1].stage,
                effect=detail,
                blocking=status is BoundaryStatus.BLOCKED,
                remediation="satisfy boundary checks before execution",
                reopen_target=checks[-1].stage,
            ),
        ),
    )


def _identity_preserved(
    *, before: dict[str, str], after: dict[str, str], required: frozenset[str]
) -> bool:
    return all(before.get(key) == after.get(key) for key in required)


def _apply_rank_bound(
    *, input_rank: int, evidence_rank: int, operation_rank: int, bridge_rank: int
) -> tuple[int, ResidualRecord | None]:
    ceiling = min(input_rank, evidence_rank, operation_rank, bridge_rank)
    residual = None
    if input_rank > ceiling:
        residual = ResidualRecord(
            code="RANK_LIMITED",
            severity="MEDIUM",
            source="RankBound",
            effect=f"bounded from {input_rank} to {ceiling}",
            blocking=False,
            remediation="collect stronger evidence before promotion",
            reopen_target="RankBound",
        )
    return ceiling, residual


def _commit_trace(
    *,
    proposal: CandidateProposal,
    contract: OperationContract,
    checks: tuple[AuthorizationCheck, ...],
    residuals: tuple[ResidualRecord, ...],
    rank_after: int,
    output_id: str,
) -> TraceEvent:
    return TraceEvent(
        input_ids=proposal.input_ids,
        operation_id=contract.operation_id,
        contract_version="v1",
        evidence_ids=proposal.evidence_ids,
        checks=tuple(check.code for check in checks),
        preserved_identities=tuple(sorted(contract.identity_policy)),
        declared_effect=proposal.expected_effect,
        rank_before=proposal.input_rank,
        rank_after=rank_after,
        residuals=tuple(residual.code for residual in residuals),
        output_id=output_id,
    )


def _evaluate_closure(residuals: tuple[ResidualRecord, ...]) -> ClosureState:
    if any(record.blocking for record in residuals):
        return ClosureState.REOPEN_REQUIRED
    if residuals:
        return ClosureState.CLOSED_WITH_RESIDUALS
    return ClosureState.CLOSED


def _evaluate_transition_readiness(
    *, closure_state: ClosureState, transition_policy: tuple[str, ...]
) -> tuple[str, ...]:
    if closure_state in {ClosureState.BLOCKED, ClosureState.REOPEN_REQUIRED}:
        return ("BLOCKED_FROM_NEXT",)
    if closure_state in {ClosureState.DEFERRED, ClosureState.AMBIGUOUS}:
        return ("NOT_READY_FOR_NEXT",)
    if transition_policy:
        return transition_policy
    return ("READY_FOR_NEXT",)
