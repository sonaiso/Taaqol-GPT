"""PR-D.1 carrier-bound transition-execution preflight hardening (no execution)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.x0r.canonical_domain_registry import (
    DomainId,
    EvidenceKind,
    ResidualKind,
    canonical_domain_registry,
)
from taaqqul_slot_geometry.x0r.canonical_transition_contract_registry import (
    CanonicalTransitionContract,
    TransitionContractId,
    canonical_transition_contract_registry,
)


class PRD1PreflightSchemaError(TypeError):
    """Raised when PR-D.1 preflight inputs or outputs are malformed."""


class PRD1PreflightState(StrEnum):
    """Bounded decision states for PR-D.1 preflight."""

    ADMISSIBLE = "ADMISSIBLE"
    ADMISSIBLE_WITH_RESIDUALS = "ADMISSIBLE_WITH_RESIDUALS"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    INVALID = "INVALID"


class PRD1PreflightFailureCode(StrEnum):
    """Named local refusal reasons for PR-D.1 carrier-bound decisions."""

    CONTRACT_DOMAIN_MISMATCH = "CONTRACT_DOMAIN_MISMATCH"
    INPUT_CARRIER_KIND_MISMATCH = "INPUT_CARRIER_KIND_MISMATCH"
    REQUIRED_FIELD_VALUE_MISSING = "REQUIRED_FIELD_VALUE_MISSING"
    REQUIRED_EVIDENCE_MISSING = "REQUIRED_EVIDENCE_MISSING"
    EVIDENCE_SUBJECT_MISMATCH = "EVIDENCE_SUBJECT_MISMATCH"
    EVIDENCE_CONTRACT_MISMATCH = "EVIDENCE_CONTRACT_MISMATCH"
    EVIDENCE_EXPIRED = "EVIDENCE_EXPIRED"
    RESIDUAL_KIND_NOT_ALLOWED = "RESIDUAL_KIND_NOT_ALLOWED"
    BLOCKING_RESIDUAL_PRESENT = "BLOCKING_RESIDUAL_PRESENT"
    REQUESTED_RANK_EXCEEDS_PREFLIGHT_CEILING = "REQUESTED_RANK_EXCEEDS_PREFLIGHT_CEILING"
    REGISTRY_VERSION_MISMATCH = "REGISTRY_VERSION_MISMATCH"
    CONTRACT_DIGEST_MISMATCH = "CONTRACT_DIGEST_MISMATCH"
    INPUT_IDENTITY_INVARIANT_MISSING = "INPUT_IDENTITY_INVARIANT_MISSING"


_PREFLIGHT_REQUEST_RANK_CEILING = Rank.TRACE
_POLICY_VERSION = "pr-d1-carrier-bound-preflight-policy-v1"
_DECISION_PRIORITY = (
    PRD1PreflightState.INVALID,
    PRD1PreflightState.BLOCKED,
    PRD1PreflightState.DEFERRED,
    PRD1PreflightState.ADMISSIBLE_WITH_RESIDUALS,
    PRD1PreflightState.ADMISSIBLE,
)
_POLICY_DIGEST = sha256(
    (
        f"{_POLICY_VERSION}|"
        f"ceiling={int(_PREFLIGHT_REQUEST_RANK_CEILING)}|"
        f"priority={','.join(state.value for state in _DECISION_PRIORITY)}"
    ).encode()
).hexdigest()


@dataclass(frozen=True, slots=True)
class CarrierFieldValue:
    """Typed field-value reference carried by the input carrier."""

    field_name: str
    value_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "field_name", self.field_name)
        _require_str(cls, "value_ref", self.value_ref)


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    """Typed evidence instance reference bound to a request subject."""

    evidence_id: str
    kind: EvidenceKind
    provenance_ref: str
    subject_ref: str
    scope_ref: str
    contract_id: TransitionContractId
    evidence_rank: Rank
    trace_ref: str
    valid_until_epoch: int | None = None

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "evidence_id", self.evidence_id)
        if not isinstance(self.kind, EvidenceKind):
            raise PRD1PreflightSchemaError(f"{cls}.kind must be EvidenceKind")
        _require_str(cls, "provenance_ref", self.provenance_ref)
        _require_str(cls, "subject_ref", self.subject_ref)
        _require_str(cls, "scope_ref", self.scope_ref)
        if not isinstance(self.contract_id, TransitionContractId):
            raise PRD1PreflightSchemaError(f"{cls}.contract_id must be TransitionContractId")
        if not isinstance(self.evidence_rank, Rank):
            raise PRD1PreflightSchemaError(f"{cls}.evidence_rank must be Rank")
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if self.valid_until_epoch is not None:
            _require_int(cls, "valid_until_epoch", self.valid_until_epoch)


@dataclass(frozen=True, slots=True)
class PreservedInvariant:
    """Invariant expected to remain preserved across the transition request."""

    name: str
    value_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "name", self.name)
        _require_str(cls, "value_ref", self.value_ref)


@dataclass(frozen=True, slots=True)
class InputCarrierSnapshot:
    """Bounded input-carrier snapshot for PR-D.1 preflight."""

    carrier_id: str
    carrier_kind: str
    input_identity: str
    predecessor_closure_ref: str
    field_values: tuple[CarrierFieldValue, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "carrier_id", self.carrier_id)
        _require_str(cls, "carrier_kind", self.carrier_kind)
        _require_str(cls, "input_identity", self.input_identity)
        _require_trace_ref(cls, "predecessor_closure_ref", self.predecessor_closure_ref)
        _require_unique_dataclass_tuple(cls, "field_values", self.field_values, CarrierFieldValue)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class TransitionExecutionPreflightHardeningRequest:
    """Carrier-bound PR-D.1 request with evidence instances and snapshot pins."""

    request_id: str
    contract_id: TransitionContractId
    domain: DomainId
    input_carrier: InputCarrierSnapshot
    evidence_refs: tuple[EvidenceRef, ...]
    residual_kinds: tuple[ResidualKind, ...]
    requested_rank: Rank
    preserved_invariants: tuple[PreservedInvariant, ...]
    expected_domain_registry_version: str
    expected_contract_registry_version: str
    expected_contract_digest: str
    trace_ref: str
    request_epoch_seconds: int

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "request_id", self.request_id)
        if not isinstance(self.contract_id, TransitionContractId):
            raise PRD1PreflightSchemaError(f"{cls}.contract_id must be TransitionContractId")
        if not isinstance(self.domain, DomainId):
            raise PRD1PreflightSchemaError(f"{cls}.domain must be DomainId")
        if not isinstance(self.input_carrier, InputCarrierSnapshot):
            raise PRD1PreflightSchemaError(f"{cls}.input_carrier must be InputCarrierSnapshot")
        _require_unique_dataclass_tuple(cls, "evidence_refs", self.evidence_refs, EvidenceRef)
        _require_unique_enum_tuple(cls, "residual_kinds", self.residual_kinds, ResidualKind)
        if not isinstance(self.requested_rank, Rank):
            raise PRD1PreflightSchemaError(f"{cls}.requested_rank must be Rank")
        _require_unique_dataclass_tuple(
            cls,
            "preserved_invariants",
            self.preserved_invariants,
            PreservedInvariant,
        )
        _require_str(
            cls,
            "expected_domain_registry_version",
            self.expected_domain_registry_version,
        )
        _require_str(
            cls,
            "expected_contract_registry_version",
            self.expected_contract_registry_version,
        )
        _require_str(cls, "expected_contract_digest", self.expected_contract_digest)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        _require_int(cls, "request_epoch_seconds", self.request_epoch_seconds)


@dataclass(frozen=True, slots=True)
class TransitionExecutionPreflightHardeningResult:
    """PR-D.1 preflight result surface with carrier-bound trace/snapshot metadata."""

    request_id: str
    contract_id: TransitionContractId
    state: PRD1PreflightState
    failure_codes: tuple[PRD1PreflightFailureCode, ...]
    visible_residual_kinds: tuple[ResidualKind, ...]
    contract_declared_output_types: tuple[str, ...]
    granted_rank: Rank
    request_trace_ref: str
    preflight_trace_ref: str
    parent_trace_ref: str
    domain_registry_version: str
    contract_registry_version: str
    contract_digest: str
    policy_digest: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "request_id", self.request_id)
        if not isinstance(self.contract_id, TransitionContractId):
            raise PRD1PreflightSchemaError(f"{cls}.contract_id must be TransitionContractId")
        if not isinstance(self.state, PRD1PreflightState):
            raise PRD1PreflightSchemaError(f"{cls}.state must be PRD1PreflightState")
        _require_unique_enum_tuple(
            cls,
            "failure_codes",
            self.failure_codes,
            PRD1PreflightFailureCode,
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
            "contract_declared_output_types",
            self.contract_declared_output_types,
            allow_empty=True,
        )
        if not isinstance(self.granted_rank, Rank):
            raise PRD1PreflightSchemaError(f"{cls}.granted_rank must be Rank")
        _require_trace_ref(cls, "request_trace_ref", self.request_trace_ref)
        _require_trace_ref(cls, "preflight_trace_ref", self.preflight_trace_ref)
        _require_trace_ref(cls, "parent_trace_ref", self.parent_trace_ref)
        _require_str(cls, "domain_registry_version", self.domain_registry_version)
        _require_str(cls, "contract_registry_version", self.contract_registry_version)
        _require_str(cls, "contract_digest", self.contract_digest)
        _require_str(cls, "policy_digest", self.policy_digest)

        admissible_states = {
            PRD1PreflightState.ADMISSIBLE,
            PRD1PreflightState.ADMISSIBLE_WITH_RESIDUALS,
        }
        if self.state in admissible_states:
            if self.failure_codes:
                raise PRD1PreflightSchemaError(
                    f"{cls} admissible states cannot carry failure_codes"
                )
            if not self.contract_declared_output_types:
                raise PRD1PreflightSchemaError(
                    f"{cls} admissible states must expose contract_declared_output_types"
                )
        if self.state is PRD1PreflightState.ADMISSIBLE and self.visible_residual_kinds:
            raise PRD1PreflightSchemaError(
                f"{cls}.ADMISSIBLE cannot carry visible residual kinds"
            )
        if self.state is PRD1PreflightState.ADMISSIBLE_WITH_RESIDUALS:
            if not self.visible_residual_kinds:
                raise PRD1PreflightSchemaError(
                    f"{cls}.ADMISSIBLE_WITH_RESIDUALS requires visible residual kinds"
                )
            if ResidualKind.BLOCKING in self.visible_residual_kinds:
                raise PRD1PreflightSchemaError(
                    f"{cls}.ADMISSIBLE_WITH_RESIDUALS cannot carry BLOCKING residuals"
                )
        if self.state in {
            PRD1PreflightState.DEFERRED,
            PRD1PreflightState.BLOCKED,
            PRD1PreflightState.INVALID,
        }:
            if not self.failure_codes:
                raise PRD1PreflightSchemaError(
                    f"{cls} non-admissible states require at least one failure code"
                )
            if self.contract_declared_output_types:
                raise PRD1PreflightSchemaError(
                    f"{cls} non-admissible states cannot expose declared outputs"
                )
        if self.state is PRD1PreflightState.BLOCKED and not self.visible_residual_kinds:
            raise PRD1PreflightSchemaError(f"{cls}.BLOCKED requires visible residual kinds")

        if self.granted_rank is not Rank.ZERO:
            raise PRD1PreflightSchemaError(f"{cls} must keep granted_rank at Rank.ZERO")


def compute_transition_contract_digest(contract: CanonicalTransitionContract) -> str:
    """Return deterministic digest for one canonical transition contract row."""

    payload = "|".join(
        (
            contract.contract_id.value,
            contract.domain.value,
            contract.transition_kind.value,
            contract.source_slot,
            contract.target_slot,
            ",".join(contract.required_conditions),
            ",".join(contract.required_fields),
            ",".join(contract.outputs),
            ",".join(kind.value for kind in contract.evidence_kinds),
            ",".join(kind.value for kind in contract.residual_kinds),
            str(contract.allows_multi_candidate),
            contract.law_ref,
            contract.trace_ref,
        )
    )
    return sha256(payload.encode("utf-8")).hexdigest()


def evaluate_transition_execution_preflight_hardening(
    request: TransitionExecutionPreflightHardeningRequest,
) -> TransitionExecutionPreflightHardeningResult:
    """Evaluate carrier-bound transition preflight without opening execution."""

    if not isinstance(request, TransitionExecutionPreflightHardeningRequest):
        raise PRD1PreflightSchemaError(
            "evaluate_transition_execution_preflight_hardening requires "
            "TransitionExecutionPreflightHardeningRequest"
        )

    domain_registry = canonical_domain_registry()
    contract_registry = canonical_transition_contract_registry()
    contract = contract_registry.contract_by_id(request.contract_id)
    contract_digest = compute_transition_contract_digest(contract)

    failure_codes: list[PRD1PreflightFailureCode] = []

    if request.domain not in domain_registry.domains or contract.domain is not request.domain:
        failure_codes.append(PRD1PreflightFailureCode.CONTRACT_DOMAIN_MISMATCH)

    if request.input_carrier.carrier_kind != contract.source_slot:
        failure_codes.append(PRD1PreflightFailureCode.INPUT_CARRIER_KIND_MISMATCH)

    if request.expected_domain_registry_version != domain_registry.version:
        failure_codes.append(PRD1PreflightFailureCode.REGISTRY_VERSION_MISMATCH)

    if request.expected_contract_registry_version != contract_registry.version:
        failure_codes.append(PRD1PreflightFailureCode.REGISTRY_VERSION_MISMATCH)

    if request.expected_contract_digest != contract_digest:
        failure_codes.append(PRD1PreflightFailureCode.CONTRACT_DIGEST_MISMATCH)

    field_map = {entry.field_name: entry.value_ref for entry in request.input_carrier.field_values}
    missing_field_values = tuple(
        field_name
        for field_name in contract.required_fields
        if field_name not in field_map or not field_map[field_name].strip()
    )
    if missing_field_values:
        failure_codes.append(PRD1PreflightFailureCode.REQUIRED_FIELD_VALUE_MISSING)

    evidence_by_kind = {evidence.kind for evidence in request.evidence_refs}
    missing_evidence = tuple(
        kind for kind in contract.evidence_kinds if kind not in evidence_by_kind
    )
    if missing_evidence:
        failure_codes.append(PRD1PreflightFailureCode.REQUIRED_EVIDENCE_MISSING)

    has_subject_mismatch = any(
        evidence.subject_ref != request.input_carrier.input_identity
        for evidence in request.evidence_refs
    )
    if has_subject_mismatch:
        failure_codes.append(PRD1PreflightFailureCode.EVIDENCE_SUBJECT_MISMATCH)

    has_contract_mismatch = any(
        evidence.contract_id is not request.contract_id for evidence in request.evidence_refs
    )
    if has_contract_mismatch:
        failure_codes.append(PRD1PreflightFailureCode.EVIDENCE_CONTRACT_MISMATCH)

    has_expired_evidence = any(
        evidence.valid_until_epoch is not None
        and evidence.valid_until_epoch < request.request_epoch_seconds
        for evidence in request.evidence_refs
    )
    if has_expired_evidence:
        failure_codes.append(PRD1PreflightFailureCode.EVIDENCE_EXPIRED)

    disallowed_residuals = tuple(
        kind for kind in request.residual_kinds if kind not in contract.residual_kinds
    )
    if disallowed_residuals:
        failure_codes.append(PRD1PreflightFailureCode.RESIDUAL_KIND_NOT_ALLOWED)

    has_blocking_residual = ResidualKind.BLOCKING in request.residual_kinds
    if has_blocking_residual:
        failure_codes.append(PRD1PreflightFailureCode.BLOCKING_RESIDUAL_PRESENT)

    if request.requested_rank > _PREFLIGHT_REQUEST_RANK_CEILING:
        failure_codes.append(PRD1PreflightFailureCode.REQUESTED_RANK_EXCEEDS_PREFLIGHT_CEILING)

    identity_invariant_ok = any(
        item.name == "input_identity" and item.value_ref == request.input_carrier.input_identity
        for item in request.preserved_invariants
    )
    if not identity_invariant_ok:
        failure_codes.append(PRD1PreflightFailureCode.INPUT_IDENTITY_INVARIANT_MISSING)

    state = PRD1PreflightState.ADMISSIBLE
    visible_residuals: tuple[ResidualKind, ...] = ()
    contract_declared_output_types: tuple[str, ...] = contract.outputs

    invalid_codes = {
        PRD1PreflightFailureCode.CONTRACT_DOMAIN_MISMATCH,
        PRD1PreflightFailureCode.INPUT_CARRIER_KIND_MISMATCH,
        PRD1PreflightFailureCode.REGISTRY_VERSION_MISMATCH,
        PRD1PreflightFailureCode.CONTRACT_DIGEST_MISMATCH,
    }
    blocked_codes = {
        PRD1PreflightFailureCode.RESIDUAL_KIND_NOT_ALLOWED,
        PRD1PreflightFailureCode.BLOCKING_RESIDUAL_PRESENT,
        PRD1PreflightFailureCode.REQUESTED_RANK_EXCEEDS_PREFLIGHT_CEILING,
    }
    deferred_codes = {
        PRD1PreflightFailureCode.REQUIRED_FIELD_VALUE_MISSING,
        PRD1PreflightFailureCode.REQUIRED_EVIDENCE_MISSING,
        PRD1PreflightFailureCode.EVIDENCE_SUBJECT_MISMATCH,
        PRD1PreflightFailureCode.EVIDENCE_CONTRACT_MISMATCH,
        PRD1PreflightFailureCode.EVIDENCE_EXPIRED,
        PRD1PreflightFailureCode.INPUT_IDENTITY_INVARIANT_MISSING,
    }

    unique_codes = tuple(dict.fromkeys(failure_codes))

    if any(code in invalid_codes for code in unique_codes):
        state = PRD1PreflightState.INVALID
        contract_declared_output_types = ()
    elif any(code in blocked_codes for code in unique_codes):
        state = PRD1PreflightState.BLOCKED
        visible_residuals = request.residual_kinds
        contract_declared_output_types = ()
    elif any(code in deferred_codes for code in unique_codes):
        state = PRD1PreflightState.DEFERRED
        contract_declared_output_types = ()
    elif request.residual_kinds:
        state = PRD1PreflightState.ADMISSIBLE_WITH_RESIDUALS
        visible_residuals = request.residual_kinds

    preflight_trace_ref = _make_preflight_trace_ref(request)

    return TransitionExecutionPreflightHardeningResult(
        request_id=request.request_id,
        contract_id=request.contract_id,
        state=state,
        failure_codes=unique_codes,
        visible_residual_kinds=visible_residuals,
        contract_declared_output_types=contract_declared_output_types,
        granted_rank=Rank.ZERO,
        request_trace_ref=request.trace_ref,
        preflight_trace_ref=preflight_trace_ref,
        parent_trace_ref=request.trace_ref,
        domain_registry_version=domain_registry.version,
        contract_registry_version=contract_registry.version,
        contract_digest=contract_digest,
        policy_digest=_POLICY_DIGEST,
    )


def _make_preflight_trace_ref(request: TransitionExecutionPreflightHardeningRequest) -> str:
    token = sha256(
        (
            f"{request.request_id}|{request.contract_id.value}|"
            f"{request.input_carrier.carrier_id}|{request.trace_ref}"
        ).encode()
    ).hexdigest()[:24]
    return f"trace://x0r/pr-d1/preflight/{token}"


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_trace_ref(cls_name: str, field_name: str, value: object) -> None:
    _require_str(cls_name, field_name, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} must start with 'trace://'")


def _require_int(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, int):
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} must be int")


def _require_unique_non_empty_str_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise PRD1PreflightSchemaError(
                f"{cls_name}.{field_name} entries must be non-empty strings"
            )
    if len(set(value)) != len(value):
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} entries must be unique")


def _require_unique_enum_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    enum_type: type[StrEnum],
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, tuple):
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} must be tuple")
    if not allow_empty and not value:
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} must be non-empty")
    for entry in value:
        if not isinstance(entry, enum_type):
            raise PRD1PreflightSchemaError(
                f"{cls_name}.{field_name} entries must be {enum_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} entries must be unique")


def _require_unique_dataclass_tuple(
    cls_name: str,
    field_name: str,
    value: object,
    expected_type: type[object],
) -> None:
    if not isinstance(value, tuple) or not value:
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} must be a non-empty tuple")
    for entry in value:
        if not isinstance(entry, expected_type):
            raise PRD1PreflightSchemaError(
                f"{cls_name}.{field_name} entries must be {expected_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise PRD1PreflightSchemaError(f"{cls_name}.{field_name} entries must be unique")


__all__ = [
    "CarrierFieldValue",
    "EvidenceRef",
    "InputCarrierSnapshot",
    "PRD1PreflightFailureCode",
    "PRD1PreflightSchemaError",
    "PRD1PreflightState",
    "PreservedInvariant",
    "TransitionExecutionPreflightHardeningRequest",
    "TransitionExecutionPreflightHardeningResult",
    "compute_transition_contract_digest",
    "evaluate_transition_execution_preflight_hardening",
]
