"""PR-F permit consumption + execution-candidate emission (no postflight/commit)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Literal

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.x0r.canonical_domain_registry import ResidualKind
from taaqqul_slot_geometry.x0r.canonical_transition_contract_registry import (
    TransitionContractId,
    canonical_transition_contract_registry,
)
from taaqqul_slot_geometry.x0r.pr_d1_transition_execution_preflight_hardening import (
    InputCarrierSnapshot,
    compute_transition_contract_digest,
)
from taaqqul_slot_geometry.x0r.pr_e_transition_permit_issuance import TransitionPermit


class PRFExecutionSchemaError(TypeError):
    """Raised when PR-F request/result surfaces are malformed."""


class PRFPermitLifecycleState(StrEnum):
    """Closed permit lifecycle states admitted by PR-F checks."""

    ISSUED = "ISSUED"
    CONSUMED = "CONSUMED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    SUPERSEDED = "SUPERSEDED"


class PRFExecutionState(StrEnum):
    """Decision states for PR-F consumption/execution boundary."""

    EXECUTED = "EXECUTED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


class PRFExecutionFailureCode(StrEnum):
    """Named refusal/defer reasons for PR-F."""

    PERMIT_NOT_ISSUED_STATE = "PERMIT_NOT_ISSUED_STATE"
    PERMIT_ALREADY_CONSUMED = "PERMIT_ALREADY_CONSUMED"
    PERMIT_EXPIRED = "PERMIT_EXPIRED"
    PERMIT_REVOKED = "PERMIT_REVOKED"
    PERMIT_SUPERSEDED = "PERMIT_SUPERSEDED"
    PERMIT_NONCE_REPLAYED = "PERMIT_NONCE_REPLAYED"
    CONTRACT_REGISTRY_VERSION_MISMATCH = "CONTRACT_REGISTRY_VERSION_MISMATCH"
    CONTRACT_DIGEST_MISMATCH = "CONTRACT_DIGEST_MISMATCH"
    INPUT_IDENTITY_MISMATCH = "INPUT_IDENTITY_MISMATCH"
    REQUESTED_OPERATION_MISMATCH = "REQUESTED_OPERATION_MISMATCH"
    REQUESTED_OUTPUT_NOT_PERMITTED = "REQUESTED_OUTPUT_NOT_PERMITTED"
    EXECUTOR_NOT_AUTHORIZED = "EXECUTOR_NOT_AUTHORIZED"


@dataclass(frozen=True, slots=True)
class PermitLifecycleSnapshot:
    """External lifecycle snapshot consumed by the pure PR-F evaluator."""

    permit_id: str
    state: PRFPermitLifecycleState
    consumed_nonces: tuple[str, ...]
    revoked_permit_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "permit_id", self.permit_id)
        if not isinstance(self.state, PRFPermitLifecycleState):
            raise PRFExecutionSchemaError(f"{cls}.state must be PRFPermitLifecycleState")
        _require_unique_non_empty_str_tuple(
            cls,
            "consumed_nonces",
            self.consumed_nonces,
            allow_empty=True,
        )
        _require_unique_non_empty_str_tuple(
            cls,
            "revoked_permit_ids",
            self.revoked_permit_ids,
            allow_empty=True,
        )


@dataclass(frozen=True, slots=True)
class CurrentRegistrySnapshot:
    """Pinned runtime snapshot for replay-safe PR-F contract checks."""

    expected_contract_registry_version: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(
            cls,
            "expected_contract_registry_version",
            self.expected_contract_registry_version,
        )


@dataclass(frozen=True, slots=True)
class ObservedInvariant:
    """Invariant observed during isolated PR-F execution."""

    name: str
    value_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "name", self.name)
        _require_str(cls, "value_ref", self.value_ref)


@dataclass(frozen=True, slots=True)
class TransitionExecutionRequest:
    """Bounded PR-F request that consumes one permit and emits one candidate."""

    execution_request_id: str
    permit: TransitionPermit
    permit_lifecycle: PermitLifecycleSnapshot
    input_carrier_snapshot: InputCarrierSnapshot
    input_identity_pin: str
    executor_identity: str
    authorized_executors: tuple[str, ...]
    requested_operation: str
    requested_output_type: str
    output_candidate_ref: str
    observed_invariants: tuple[ObservedInvariant, ...]
    observed_residual_kinds: tuple[ResidualKind, ...]
    current_time_epoch_seconds: int
    current_registry_snapshot: CurrentRegistrySnapshot
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "execution_request_id", self.execution_request_id)
        if not isinstance(self.permit, TransitionPermit):
            raise PRFExecutionSchemaError(f"{cls}.permit must be TransitionPermit")
        if not isinstance(self.permit_lifecycle, PermitLifecycleSnapshot):
            raise PRFExecutionSchemaError(
                f"{cls}.permit_lifecycle must be PermitLifecycleSnapshot"
            )
        if not isinstance(self.input_carrier_snapshot, InputCarrierSnapshot):
            raise PRFExecutionSchemaError(
                f"{cls}.input_carrier_snapshot must be InputCarrierSnapshot"
            )
        _require_str(cls, "input_identity_pin", self.input_identity_pin)
        _require_str(cls, "executor_identity", self.executor_identity)
        _require_unique_non_empty_str_tuple(cls, "authorized_executors", self.authorized_executors)
        _require_str(cls, "requested_operation", self.requested_operation)
        _require_str(cls, "requested_output_type", self.requested_output_type)
        _require_str(cls, "output_candidate_ref", self.output_candidate_ref)
        _require_unique_dataclass_tuple(
            cls,
            "observed_invariants",
            self.observed_invariants,
            ObservedInvariant,
            allow_empty=True,
        )
        _require_unique_enum_tuple(
            cls,
            "observed_residual_kinds",
            self.observed_residual_kinds,
            ResidualKind,
            allow_empty=True,
        )
        _require_int(cls, "current_time_epoch_seconds", self.current_time_epoch_seconds)
        if not isinstance(self.current_registry_snapshot, CurrentRegistrySnapshot):
            raise PRFExecutionSchemaError(
                f"{cls}.current_registry_snapshot must be CurrentRegistrySnapshot"
            )
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class ExecutionCandidate:
    """PR-F output candidate; never approved output and never commit."""

    execution_id: str
    permit_id: str
    input_identity: str
    requested_operation: str
    requested_output_type: str
    output_candidate_ref: str
    operation_trace_ref: str
    observed_invariants: tuple[ObservedInvariant, ...]
    observed_residual_kinds: tuple[ResidualKind, ...]
    execution_status: Literal["EXECUTED"]
    postflight_required: Literal[True]
    rank: Rank

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "execution_id", self.execution_id)
        _require_str(cls, "permit_id", self.permit_id)
        _require_str(cls, "input_identity", self.input_identity)
        _require_str(cls, "requested_operation", self.requested_operation)
        _require_str(cls, "requested_output_type", self.requested_output_type)
        _require_str(cls, "output_candidate_ref", self.output_candidate_ref)
        _require_trace_ref(cls, "operation_trace_ref", self.operation_trace_ref)
        _require_unique_dataclass_tuple(
            cls,
            "observed_invariants",
            self.observed_invariants,
            ObservedInvariant,
            allow_empty=True,
        )
        _require_unique_enum_tuple(
            cls,
            "observed_residual_kinds",
            self.observed_residual_kinds,
            ResidualKind,
            allow_empty=True,
        )
        if self.execution_status != "EXECUTED":
            raise PRFExecutionSchemaError(f"{cls}.execution_status must be 'EXECUTED'")
        if self.postflight_required is not True:
            raise PRFExecutionSchemaError(f"{cls}.postflight_required must be True")
        if self.rank is not Rank.ZERO:
            raise PRFExecutionSchemaError(f"{cls}.rank must remain Rank.ZERO")


@dataclass(frozen=True, slots=True)
class TransitionExecutionResult:
    """PR-F decision result with optional execution candidate."""

    execution_request_id: str
    state: PRFExecutionState
    failure_codes: tuple[PRFExecutionFailureCode, ...]
    consumed_nonce: str | None
    lifecycle_transition: tuple[PRFPermitLifecycleState, PRFPermitLifecycleState] | None
    execution_candidate: ExecutionCandidate | None
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "execution_request_id", self.execution_request_id)
        if not isinstance(self.state, PRFExecutionState):
            raise PRFExecutionSchemaError(f"{cls}.state must be PRFExecutionState")
        _require_unique_enum_tuple(
            cls,
            "failure_codes",
            self.failure_codes,
            PRFExecutionFailureCode,
            allow_empty=True,
        )
        if self.consumed_nonce is not None:
            _require_str(cls, "consumed_nonce", self.consumed_nonce)
        if self.lifecycle_transition is not None and (
            not isinstance(self.lifecycle_transition, tuple)
            or len(self.lifecycle_transition) != 2
            or not isinstance(self.lifecycle_transition[0], PRFPermitLifecycleState)
            or not isinstance(self.lifecycle_transition[1], PRFPermitLifecycleState)
        ):
            raise PRFExecutionSchemaError(
                f"{cls}.lifecycle_transition must be "
                "tuple[PRFPermitLifecycleState, PRFPermitLifecycleState] or None"
            )
        if self.execution_candidate is not None and not isinstance(
            self.execution_candidate, ExecutionCandidate
        ):
            raise PRFExecutionSchemaError(
                f"{cls}.execution_candidate must be ExecutionCandidate or None"
            )
        _require_trace_ref(cls, "trace_ref", self.trace_ref)

        if self.state is PRFExecutionState.EXECUTED:
            if self.failure_codes:
                raise PRFExecutionSchemaError(f"{cls}.EXECUTED cannot carry failure_codes")
            if self.consumed_nonce is None:
                raise PRFExecutionSchemaError(f"{cls}.EXECUTED requires consumed_nonce")
            if self.lifecycle_transition != (
                PRFPermitLifecycleState.ISSUED,
                PRFPermitLifecycleState.CONSUMED,
            ):
                raise PRFExecutionSchemaError(
                    f"{cls}.EXECUTED requires lifecycle transition ISSUED->CONSUMED"
                )
            if self.execution_candidate is None:
                raise PRFExecutionSchemaError(f"{cls}.EXECUTED requires execution_candidate")
        else:
            if not self.failure_codes:
                raise PRFExecutionSchemaError(
                    f"{cls} non-EXECUTED states require failure_codes"
                )
            if self.consumed_nonce is not None:
                raise PRFExecutionSchemaError(
                    f"{cls} non-EXECUTED states cannot consume nonce"
                )
            if self.lifecycle_transition is not None:
                raise PRFExecutionSchemaError(
                    f"{cls} non-EXECUTED states cannot carry lifecycle transition"
                )
            if self.execution_candidate is not None:
                raise PRFExecutionSchemaError(
                    f"{cls} non-EXECUTED states cannot carry execution candidate"
                )


def consume_permit_and_emit_execution_candidate(
    request: TransitionExecutionRequest,
) -> TransitionExecutionResult:
    """Consume a valid single-use permit and emit one execution candidate only."""

    if not isinstance(request, TransitionExecutionRequest):
        raise PRFExecutionSchemaError(
            "consume_permit_and_emit_execution_candidate requires TransitionExecutionRequest"
        )

    failure_codes: list[PRFExecutionFailureCode] = []

    contract_registry = canonical_transition_contract_registry()
    contract = contract_registry.contract_by_id(TransitionContractId(request.permit.contract_id))
    computed_contract_digest = compute_transition_contract_digest(contract)

    if (
        request.current_registry_snapshot.expected_contract_registry_version
        != contract_registry.version
    ):
        failure_codes.append(PRFExecutionFailureCode.CONTRACT_REGISTRY_VERSION_MISMATCH)

    lifecycle = request.permit_lifecycle
    if lifecycle.permit_id != request.permit.permit_id:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_NOT_ISSUED_STATE)

    if lifecycle.state is PRFPermitLifecycleState.CONSUMED:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_ALREADY_CONSUMED)
    elif lifecycle.state is PRFPermitLifecycleState.EXPIRED:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_EXPIRED)
    elif lifecycle.state is PRFPermitLifecycleState.REVOKED:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_REVOKED)
    elif lifecycle.state is PRFPermitLifecycleState.SUPERSEDED:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_SUPERSEDED)
    elif lifecycle.state is not PRFPermitLifecycleState.ISSUED:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_NOT_ISSUED_STATE)

    if request.permit.permit_id in lifecycle.revoked_permit_ids:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_REVOKED)

    if request.current_time_epoch_seconds >= request.permit.expires_at_epoch:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_EXPIRED)

    if request.permit.permit_nonce in lifecycle.consumed_nonces:
        failure_codes.append(PRFExecutionFailureCode.PERMIT_NONCE_REPLAYED)

    if request.permit.contract_digest != computed_contract_digest:
        failure_codes.append(PRFExecutionFailureCode.CONTRACT_DIGEST_MISMATCH)

    if request.input_carrier_snapshot.input_identity != request.input_identity_pin:
        failure_codes.append(PRFExecutionFailureCode.INPUT_IDENTITY_MISMATCH)

    if request.requested_operation != contract.transition_kind.value:
        failure_codes.append(PRFExecutionFailureCode.REQUESTED_OPERATION_MISMATCH)

    if request.requested_output_type not in request.permit.allowed_output_types:
        failure_codes.append(PRFExecutionFailureCode.REQUESTED_OUTPUT_NOT_PERMITTED)

    if request.executor_identity not in request.authorized_executors:
        failure_codes.append(PRFExecutionFailureCode.EXECUTOR_NOT_AUTHORIZED)

    unique_codes = tuple(dict.fromkeys(failure_codes))
    trace_ref = _make_execution_trace_ref(request)

    if unique_codes:
        state = PRFExecutionState.REFUSED
        if any(
            code
            in {
                PRFExecutionFailureCode.PERMIT_EXPIRED,
                PRFExecutionFailureCode.PERMIT_REVOKED,
                PRFExecutionFailureCode.PERMIT_SUPERSEDED,
            }
            for code in unique_codes
        ):
            state = PRFExecutionState.DEFERRED
        return TransitionExecutionResult(
            execution_request_id=request.execution_request_id,
            state=state,
            failure_codes=unique_codes,
            consumed_nonce=None,
            lifecycle_transition=None,
            execution_candidate=None,
            trace_ref=trace_ref,
        )

    execution_token = sha256(
        (
            f"{request.execution_request_id}|{request.permit.permit_id}|"
            f"{request.executor_identity}|{trace_ref}"
        ).encode()
    ).hexdigest()

    candidate = ExecutionCandidate(
        execution_id=f"exec://pr-f/{execution_token[:24]}",
        permit_id=request.permit.permit_id,
        input_identity=request.input_carrier_snapshot.input_identity,
        requested_operation=request.requested_operation,
        requested_output_type=request.requested_output_type,
        output_candidate_ref=request.output_candidate_ref,
        operation_trace_ref=trace_ref,
        observed_invariants=request.observed_invariants,
        observed_residual_kinds=request.observed_residual_kinds,
        execution_status="EXECUTED",
        postflight_required=True,
        rank=Rank.ZERO,
    )

    return TransitionExecutionResult(
        execution_request_id=request.execution_request_id,
        state=PRFExecutionState.EXECUTED,
        failure_codes=(),
        consumed_nonce=request.permit.permit_nonce,
        lifecycle_transition=(PRFPermitLifecycleState.ISSUED, PRFPermitLifecycleState.CONSUMED),
        execution_candidate=candidate,
        trace_ref=trace_ref,
    )


def _make_execution_trace_ref(request: TransitionExecutionRequest) -> str:
    token = sha256(
        (
            f"{request.execution_request_id}|{request.permit.permit_id}|"
            f"{request.trace_ref}|{request.current_time_epoch_seconds}"
        ).encode()
    ).hexdigest()[:24]
    return f"trace://x0r/pr-f/execution/{token}"


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_trace_ref(cls_name: str, field_name: str, value: object) -> None:
    _require_str(cls_name, field_name, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must start with 'trace://'")


def _require_int(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, int):
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must be int")


def _require_unique_non_empty_str_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise PRFExecutionSchemaError(
                f"{cls_name}.{field_name} entries must be non-empty strings"
            )
    if len(set(value)) != len(value):
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} entries must be unique")


def _require_unique_enum_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    enum_type: type[StrEnum],
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, enum_type):
            raise PRFExecutionSchemaError(
                f"{cls_name}.{field_name} entries must be {enum_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} entries must be unique")


def _require_unique_dataclass_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    expected_type: type[object],
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, expected_type):
            raise PRFExecutionSchemaError(
                f"{cls_name}.{field_name} entries must be {expected_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise PRFExecutionSchemaError(f"{cls_name}.{field_name} entries must be unique")


__all__ = [
    "CurrentRegistrySnapshot",
    "ExecutionCandidate",
    "ObservedInvariant",
    "PRFExecutionFailureCode",
    "PRFExecutionSchemaError",
    "PRFExecutionState",
    "PRFPermitLifecycleState",
    "PermitLifecycleSnapshot",
    "TransitionExecutionRequest",
    "TransitionExecutionResult",
    "consume_permit_and_emit_execution_candidate",
]
