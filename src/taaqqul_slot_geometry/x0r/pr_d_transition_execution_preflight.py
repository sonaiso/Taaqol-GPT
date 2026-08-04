"""PR-D bounded transition-execution preflight (evaluation only, no execution)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.x0r.canonical_domain_registry import (
    DomainId,
    EvidenceKind,
    ResidualKind,
    canonical_domain_registry,
)
from taaqqul_slot_geometry.x0r.canonical_transition_contract_registry import (
    TransitionContractId,
    canonical_transition_contract_registry,
)


class PRDPreflightSchemaError(TypeError):
    """Raised when PR-D preflight inputs or outputs are malformed."""


class PRDPreflightState(StrEnum):
    """Bounded decision states for PR-D execution preflight."""

    ADMISSIBLE = "ADMISSIBLE"
    ADMISSIBLE_WITH_RESIDUALS = "ADMISSIBLE_WITH_RESIDUALS"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"


class PRDPreflightFailureCode(StrEnum):
    """Named local refusal reasons for PR-D preflight decisions."""

    CONTRACT_DOMAIN_MISMATCH = "CONTRACT_DOMAIN_MISMATCH"
    REQUIRED_FIELD_MISSING = "REQUIRED_FIELD_MISSING"
    REQUIRED_EVIDENCE_MISSING = "REQUIRED_EVIDENCE_MISSING"
    RESIDUAL_KIND_NOT_ALLOWED = "RESIDUAL_KIND_NOT_ALLOWED"
    BLOCKING_RESIDUAL_PRESENT = "BLOCKING_RESIDUAL_PRESENT"


@dataclass(frozen=True, slots=True)
class TransitionExecutionPreflightRequest:
    """Execution-candidate preflight request bound to canonical registries."""

    request_id: str
    contract_id: TransitionContractId
    domain: DomainId
    provided_fields: tuple[str, ...]
    evidence_kinds: tuple[EvidenceKind, ...]
    residual_kinds: tuple[ResidualKind, ...]
    requested_rank: Rank
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "request_id", self.request_id)
        if not isinstance(self.contract_id, TransitionContractId):
            raise PRDPreflightSchemaError(f"{cls}.contract_id must be TransitionContractId")
        if not isinstance(self.domain, DomainId):
            raise PRDPreflightSchemaError(f"{cls}.domain must be DomainId")
        _require_unique_non_empty_str_tuple(cls, "provided_fields", self.provided_fields)
        _require_unique_enum_tuple(cls, "evidence_kinds", self.evidence_kinds, EvidenceKind)
        _require_unique_enum_tuple(cls, "residual_kinds", self.residual_kinds, ResidualKind)
        if not isinstance(self.requested_rank, Rank):
            raise PRDPreflightSchemaError(f"{cls}.requested_rank must be Rank")
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class TransitionExecutionPreflightResult:
    """Bounded non-executive preflight result for transition execution requests."""

    request_id: str
    contract_id: TransitionContractId
    state: PRDPreflightState
    failure_codes: tuple[PRDPreflightFailureCode, ...]
    visible_residual_kinds: tuple[ResidualKind, ...]
    allowed_outputs: tuple[str, ...]
    granted_rank: Rank
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "request_id", self.request_id)
        if not isinstance(self.contract_id, TransitionContractId):
            raise PRDPreflightSchemaError(f"{cls}.contract_id must be TransitionContractId")
        if not isinstance(self.state, PRDPreflightState):
            raise PRDPreflightSchemaError(f"{cls}.state must be PRDPreflightState")
        _require_unique_enum_tuple(
            cls,
            "failure_codes",
            self.failure_codes,
            PRDPreflightFailureCode,
            allow_empty=True,
        )
        _require_unique_enum_tuple(
            cls,
            "visible_residual_kinds",
            self.visible_residual_kinds,
            ResidualKind,
            allow_empty=True,
        )
        _require_unique_non_empty_str_tuple(
            cls,
            "allowed_outputs",
            self.allowed_outputs,
            allow_empty=True,
        )
        if not isinstance(self.granted_rank, Rank):
            raise PRDPreflightSchemaError(f"{cls}.granted_rank must be Rank")
        _require_trace_ref(cls, "trace_ref", self.trace_ref)

        admissible_states = {
            PRDPreflightState.ADMISSIBLE,
            PRDPreflightState.ADMISSIBLE_WITH_RESIDUALS,
        }
        if self.state in admissible_states:
            if self.failure_codes:
                raise PRDPreflightSchemaError(
                    f"{cls} admissible states cannot carry failure_codes"
                )
            if not self.allowed_outputs:
                raise PRDPreflightSchemaError(
                    f"{cls} admissible states must expose allowed_outputs"
                )
        if (
            self.state is PRDPreflightState.ADMISSIBLE
            and self.visible_residual_kinds
        ):
            raise PRDPreflightSchemaError(
                f"{cls}.ADMISSIBLE cannot carry visible residual kinds"
            )
        if self.state is PRDPreflightState.ADMISSIBLE_WITH_RESIDUALS:
            if not self.visible_residual_kinds:
                raise PRDPreflightSchemaError(
                    f"{cls}.ADMISSIBLE_WITH_RESIDUALS requires visible residual kinds"
                )
            if ResidualKind.BLOCKING in self.visible_residual_kinds:
                raise PRDPreflightSchemaError(
                    f"{cls}.ADMISSIBLE_WITH_RESIDUALS cannot carry BLOCKING residuals"
                )
        if self.state in {
            PRDPreflightState.DEFERRED,
            PRDPreflightState.BLOCKED,
            PRDPreflightState.INVALID,
        }:
            if not self.failure_codes:
                raise PRDPreflightSchemaError(
                    f"{cls} non-admissible states require at least one failure code"
                )
            if self.allowed_outputs:
                raise PRDPreflightSchemaError(
                    f"{cls} non-admissible states cannot expose allowed_outputs"
                )
        if self.state is PRDPreflightState.BLOCKED and not self.visible_residual_kinds:
            raise PRDPreflightSchemaError(f"{cls}.BLOCKED requires visible residual kinds")

        # PR-D is preflight-only: it never promotes rank.
        if self.granted_rank is not Rank.ZERO:
            raise PRDPreflightSchemaError(f"{cls} must keep granted_rank at Rank.ZERO")


def evaluate_transition_execution_preflight(
    request: TransitionExecutionPreflightRequest,
) -> TransitionExecutionPreflightResult:
    """Evaluate bounded execution eligibility against canonical contract/domain registries."""

    if not isinstance(request, TransitionExecutionPreflightRequest):
        raise PRDPreflightSchemaError(
            "evaluate_transition_execution_preflight requires "
            "TransitionExecutionPreflightRequest"
        )

    domain_registry = canonical_domain_registry()
    contract_registry = canonical_transition_contract_registry()
    contract = contract_registry.contract_by_id(request.contract_id)

    failure_codes: list[PRDPreflightFailureCode] = []

    if request.domain not in domain_registry.domains or contract.domain is not request.domain:
        failure_codes.append(PRDPreflightFailureCode.CONTRACT_DOMAIN_MISMATCH)

    missing_fields = tuple(
        field_name
        for field_name in contract.required_fields
        if field_name not in request.provided_fields
    )
    if missing_fields:
        failure_codes.append(PRDPreflightFailureCode.REQUIRED_FIELD_MISSING)

    missing_evidence = tuple(
        kind
        for kind in contract.evidence_kinds
        if kind not in request.evidence_kinds
    )
    if missing_evidence:
        failure_codes.append(PRDPreflightFailureCode.REQUIRED_EVIDENCE_MISSING)

    disallowed_residuals = tuple(
        kind for kind in request.residual_kinds if kind not in contract.residual_kinds
    )
    if disallowed_residuals:
        failure_codes.append(PRDPreflightFailureCode.RESIDUAL_KIND_NOT_ALLOWED)

    has_blocking_residual = ResidualKind.BLOCKING in request.residual_kinds
    if has_blocking_residual:
        failure_codes.append(PRDPreflightFailureCode.BLOCKING_RESIDUAL_PRESENT)

    state = PRDPreflightState.ADMISSIBLE
    visible_residuals: tuple[ResidualKind, ...] = ()
    allowed_outputs: tuple[str, ...] = contract.outputs

    if PRDPreflightFailureCode.CONTRACT_DOMAIN_MISMATCH in failure_codes:
        state = PRDPreflightState.INVALID
        allowed_outputs = ()
    elif any(
        code in failure_codes
        for code in (
            PRDPreflightFailureCode.RESIDUAL_KIND_NOT_ALLOWED,
            PRDPreflightFailureCode.BLOCKING_RESIDUAL_PRESENT,
        )
    ):
        state = PRDPreflightState.BLOCKED
        visible_residuals = request.residual_kinds
        allowed_outputs = ()
    elif any(
        code in failure_codes
        for code in (
            PRDPreflightFailureCode.REQUIRED_FIELD_MISSING,
            PRDPreflightFailureCode.REQUIRED_EVIDENCE_MISSING,
        )
    ):
        state = PRDPreflightState.DEFERRED
        allowed_outputs = ()
    elif request.residual_kinds:
        state = PRDPreflightState.ADMISSIBLE_WITH_RESIDUALS
        visible_residuals = request.residual_kinds

    return TransitionExecutionPreflightResult(
        request_id=request.request_id,
        contract_id=request.contract_id,
        state=state,
        failure_codes=tuple(dict.fromkeys(failure_codes)),
        visible_residual_kinds=visible_residuals,
        allowed_outputs=allowed_outputs,
        granted_rank=Rank.ZERO,
        trace_ref=request.trace_ref,
    )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise PRDPreflightSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_trace_ref(cls_name: str, field_name: str, value: object) -> None:
    _require_str(cls_name, field_name, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise PRDPreflightSchemaError(f"{cls_name}.{field_name} must start with 'trace://'")


def _require_unique_non_empty_str_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PRDPreflightSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PRDPreflightSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise PRDPreflightSchemaError(
                f"{cls_name}.{field_name} entries must be non-empty strings"
            )
    if len(set(value)) != len(value):
        raise PRDPreflightSchemaError(f"{cls_name}.{field_name} entries must be unique")


def _require_unique_enum_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    enum_type: type[StrEnum],
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PRDPreflightSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PRDPreflightSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, enum_type):
            raise PRDPreflightSchemaError(
                f"{cls_name}.{field_name} entries must be {enum_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise PRDPreflightSchemaError(f"{cls_name}.{field_name} entries must be unique")


__all__ = [
    "PRDPreflightFailureCode",
    "PRDPreflightSchemaError",
    "PRDPreflightState",
    "TransitionExecutionPreflightRequest",
    "TransitionExecutionPreflightResult",
    "evaluate_transition_execution_preflight",
]
