"""PR-E guardian-issued transition permit surface (no execution)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Literal

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.x0r.pr_d1_transition_execution_preflight_hardening import (
    PRD1PreflightState,
    TransitionExecutionPreflightHardeningResult,
)


class PREPermitSchemaError(TypeError):
    """Raised when PR-E permit inputs or outputs are malformed."""


class PREPermitState(StrEnum):
    """Bounded decision states for PR-E permit issuance."""

    GRANTED = "GRANTED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


class PREPermitFailureCode(StrEnum):
    """Named refusal reasons for PR-E permit issuance."""

    PREFLIGHT_NOT_ADMISSIBLE = "PREFLIGHT_NOT_ADMISSIBLE"
    REQUESTED_OUTPUT_NOT_DECLARED = "REQUESTED_OUTPUT_NOT_DECLARED"
    PERMIT_TTL_NON_POSITIVE = "PERMIT_TTL_NON_POSITIVE"
    PERMIT_TTL_EXCEEDS_MAX = "PERMIT_TTL_EXCEEDS_MAX"


PERMIT_MAX_TTL_SECONDS = 3600


@dataclass(frozen=True, slots=True)
class TransitionPermit:
    """Single-use transition permit emitted by PR-E issuance."""

    permit_id: str
    permit_nonce: str
    request_id: str
    contract_id: str
    allowed_output_types: tuple[str, ...]
    consumption_limit: Literal[1]
    issued_rank: Rank
    issued_at_epoch: int
    expires_at_epoch: int
    preflight_trace_ref: str
    permit_trace_ref: str
    contract_digest: str
    policy_digest: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "permit_id", self.permit_id)
        _require_str(cls, "permit_nonce", self.permit_nonce)
        _require_str(cls, "request_id", self.request_id)
        _require_str(cls, "contract_id", self.contract_id)
        _require_unique_non_empty_str_tuple(cls, "allowed_output_types", self.allowed_output_types)
        if self.consumption_limit != 1:
            raise PREPermitSchemaError(f"{cls}.consumption_limit must be 1")
        if self.issued_rank is not Rank.ZERO:
            raise PREPermitSchemaError(f"{cls}.issued_rank must remain Rank.ZERO")
        _require_int(cls, "issued_at_epoch", self.issued_at_epoch)
        _require_int(cls, "expires_at_epoch", self.expires_at_epoch)
        if self.expires_at_epoch <= self.issued_at_epoch:
            raise PREPermitSchemaError(
                f"{cls}.expires_at_epoch must be greater than issued_at_epoch"
            )
        _require_trace_ref(cls, "preflight_trace_ref", self.preflight_trace_ref)
        _require_trace_ref(cls, "permit_trace_ref", self.permit_trace_ref)
        _require_str(cls, "contract_digest", self.contract_digest)
        _require_str(cls, "policy_digest", self.policy_digest)


@dataclass(frozen=True, slots=True)
class TransitionPermitIssuanceRequest:
    """Request to issue a guardian permit from a hardened preflight outcome."""

    permit_request_id: str
    preflight_result: TransitionExecutionPreflightHardeningResult
    requested_output_types: tuple[str, ...]
    ttl_seconds: int
    issue_at_epoch_seconds: int
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "permit_request_id", self.permit_request_id)
        if not isinstance(self.preflight_result, TransitionExecutionPreflightHardeningResult):
            raise PREPermitSchemaError(
                f"{cls}.preflight_result must be TransitionExecutionPreflightHardeningResult"
            )
        _require_unique_non_empty_str_tuple(
            cls,
            "requested_output_types",
            self.requested_output_types,
        )
        _require_int(cls, "ttl_seconds", self.ttl_seconds)
        _require_int(cls, "issue_at_epoch_seconds", self.issue_at_epoch_seconds)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class TransitionPermitIssuanceResult:
    """PR-E permit issuance decision result."""

    permit_request_id: str
    state: PREPermitState
    failure_codes: tuple[PREPermitFailureCode, ...]
    permit: TransitionPermit | None
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "permit_request_id", self.permit_request_id)
        if not isinstance(self.state, PREPermitState):
            raise PREPermitSchemaError(f"{cls}.state must be PREPermitState")
        _require_unique_enum_tuple(
            cls,
            "failure_codes",
            self.failure_codes,
            PREPermitFailureCode,
            allow_empty=True,
        )
        if self.permit is not None and not isinstance(self.permit, TransitionPermit):
            raise PREPermitSchemaError(f"{cls}.permit must be TransitionPermit or None")
        _require_trace_ref(cls, "trace_ref", self.trace_ref)

        if self.state is PREPermitState.GRANTED:
            if self.failure_codes:
                raise PREPermitSchemaError(f"{cls}.GRANTED cannot carry failure_codes")
            if self.permit is None:
                raise PREPermitSchemaError(f"{cls}.GRANTED requires permit")
        else:
            if not self.failure_codes:
                raise PREPermitSchemaError(f"{cls} non-GRANTED states require failure_codes")
            if self.permit is not None:
                raise PREPermitSchemaError(f"{cls} non-GRANTED states cannot carry permit")


def issue_transition_permit(
    request: TransitionPermitIssuanceRequest,
) -> TransitionPermitIssuanceResult:
    """Issue a single-use permit from PR-D.1 preflight output without execution."""

    if not isinstance(request, TransitionPermitIssuanceRequest):
        raise PREPermitSchemaError(
            "issue_transition_permit requires TransitionPermitIssuanceRequest"
        )

    failure_codes: list[PREPermitFailureCode] = []
    preflight = request.preflight_result

    if request.ttl_seconds <= 0:
        failure_codes.append(PREPermitFailureCode.PERMIT_TTL_NON_POSITIVE)
    if request.ttl_seconds > PERMIT_MAX_TTL_SECONDS:
        failure_codes.append(PREPermitFailureCode.PERMIT_TTL_EXCEEDS_MAX)

    admissible_states = {
        PRD1PreflightState.ADMISSIBLE,
        PRD1PreflightState.ADMISSIBLE_WITH_RESIDUALS,
    }
    if preflight.state not in admissible_states:
        failure_codes.append(PREPermitFailureCode.PREFLIGHT_NOT_ADMISSIBLE)

    undeclared_outputs = tuple(
        output
        for output in request.requested_output_types
        if output not in preflight.contract_declared_output_types
    )
    if undeclared_outputs:
        failure_codes.append(PREPermitFailureCode.REQUESTED_OUTPUT_NOT_DECLARED)

    unique_codes = tuple(dict.fromkeys(failure_codes))
    result_trace = _make_permit_trace_ref(request)

    has_refusal = any(
        code
        in {
            PREPermitFailureCode.PREFLIGHT_NOT_ADMISSIBLE,
            PREPermitFailureCode.REQUESTED_OUTPUT_NOT_DECLARED,
            PREPermitFailureCode.PERMIT_TTL_NON_POSITIVE,
            PREPermitFailureCode.PERMIT_TTL_EXCEEDS_MAX,
        }
        for code in unique_codes
    )
    if has_refusal:
        state = PREPermitState.REFUSED
        if preflight.state is PRD1PreflightState.DEFERRED:
            state = PREPermitState.DEFERRED
        return TransitionPermitIssuanceResult(
            permit_request_id=request.permit_request_id,
            state=state,
            failure_codes=unique_codes,
            permit=None,
            trace_ref=result_trace,
        )

    issued_at = request.issue_at_epoch_seconds
    expires_at = issued_at + request.ttl_seconds

    permit_token = sha256(
        (
            f"{request.permit_request_id}|{preflight.request_id}|"
            f"{preflight.contract_id.value}|{result_trace}|{issued_at}|{expires_at}"
        ).encode()
    ).hexdigest()

    permit = TransitionPermit(
        permit_id=f"permit://pr-e/{permit_token[:24]}",
        permit_nonce=permit_token[24:48],
        request_id=preflight.request_id,
        contract_id=preflight.contract_id.value,
        allowed_output_types=request.requested_output_types,
        consumption_limit=1,
        issued_rank=Rank.ZERO,
        issued_at_epoch=issued_at,
        expires_at_epoch=expires_at,
        preflight_trace_ref=preflight.preflight_trace_ref,
        permit_trace_ref=result_trace,
        contract_digest=preflight.contract_digest,
        policy_digest=preflight.policy_digest,
    )

    return TransitionPermitIssuanceResult(
        permit_request_id=request.permit_request_id,
        state=PREPermitState.GRANTED,
        failure_codes=(),
        permit=permit,
        trace_ref=result_trace,
    )


def _make_permit_trace_ref(request: TransitionPermitIssuanceRequest) -> str:
    token = sha256(
        (
            f"{request.permit_request_id}|{request.preflight_result.preflight_trace_ref}|"
            f"{request.trace_ref}|{request.issue_at_epoch_seconds}"
        ).encode()
    ).hexdigest()[:24]
    return f"trace://x0r/pr-e/permit/{token}"


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise PREPermitSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_trace_ref(cls_name: str, field_name: str, value: object) -> None:
    _require_str(cls_name, field_name, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise PREPermitSchemaError(f"{cls_name}.{field_name} must start with 'trace://'")


def _require_int(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, int):
        raise PREPermitSchemaError(f"{cls_name}.{field_name} must be int")


def _require_unique_non_empty_str_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PREPermitSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PREPermitSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise PREPermitSchemaError(
                f"{cls_name}.{field_name} entries must be non-empty strings"
            )
    if len(set(value)) != len(value):
        raise PREPermitSchemaError(f"{cls_name}.{field_name} entries must be unique")


def _require_unique_enum_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    enum_type: type[StrEnum],
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PREPermitSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PREPermitSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, enum_type):
            raise PREPermitSchemaError(
                f"{cls_name}.{field_name} entries must be {enum_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise PREPermitSchemaError(f"{cls_name}.{field_name} entries must be unique")


__all__ = [
    "PERMIT_MAX_TTL_SECONDS",
    "PREPermitFailureCode",
    "PREPermitSchemaError",
    "PREPermitState",
    "TransitionPermit",
    "TransitionPermitIssuanceRequest",
    "TransitionPermitIssuanceResult",
    "issue_transition_permit",
]
