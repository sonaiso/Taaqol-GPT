"""DAL-A7 runtime gates for usage/loan/unvocalized/deletion residual paths only.

This module consumes only DAL-A6 runtime gate outputs and remains bounded to
local DAL-A7 residual-gate execution. It does not open DAL-A8, LAFZI,
parser/morphology/syntax, or semantic/hukm/reality outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight._schema_helpers import (
    require_non_empty as _shared_require_non_empty,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_forbidden_outputs as _shared_validate_forbidden_outputs,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_rank as _shared_validate_rank,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.dal_a6_runtime_gates import (
    DalA6RuntimeStatus,
    DalA6RuntimeVerdict,
)

DAL_A7_RANK_CEILING: Rank = Rank.CANDIDATE
DAL_A7_ALLOWED_SCOPE: str = "USAGE_LOAN_UNVOCALIZED_DELETION_RESIDUAL_GATES_ONLY"
DAL_A7_GATE_ORDER: tuple[str, ...] = (
    "UsageBeforeMeaningGate",
    "LoanPathGate",
    "UnvocalizedSurfaceGate",
    "DeletionLicenseGate",
    "RuntimeVerdictGate",
)
DAL_A7_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "DAL_A8",
    "LAFZI_B",
    "RootIdentityGate",
    "WeightPathSelectionGate",
    "ParserRuntime",
    "MorphologyRuntime",
    "SyntaxRuntime",
    "MeaningGate",
    "IfadahGate",
    "MafhumGate",
    "HukmGate",
    "Truth",
    "Certainty",
    "Reality",
    "GlobalMetricEngine",
)
DAL_A7_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "MISSING_DAL_A6_RUNTIME_TRACE",
    "DAL_A6_RUNTIME_REQUIRED",
    "RAW_INPUT_FORBIDDEN",
    "UNVOCALIZED_SURFACE",
    "UNUSED_LAFZ",
    "LOAN_PATH_REQUIRED",
    "DELETION_UNLICENSED",
    "DAL_A8_INTEGRATION_REQUIRED",
    "LAFZI_OUTPUT_FORBIDDEN",
    "SEMANTIC_OUTPUT_FORBIDDEN",
    "HUKM_OUTPUT_FORBIDDEN",
    "ROOT_WEIGHT_OUTPUT_FORBIDDEN",
    "GLOBAL_METRIC_ENGINE_FORBIDDEN",
    "FORBIDDEN_DOWNSTREAM_RUNTIME",
    "DAL_A7_LOCAL_RUNTIME_TRACE",
)
DAL_A7_RUNTIME_VERDICT: dict[str, str] = {
    "status": "RUNTIME_GATES_CLOSED",
    "scope": "USAGE_LOAN_UNVOCALIZED_DELETION_RESIDUAL_GATES_ONLY",
    "upstream_required": "DAL_A6_RUNTIME_CLOSED",
    "dal_a8_status": "DEFERRED",
    "lafzi_b_status": "DEFERRED",
    "semantic_hukm_reality_status": "FORBIDDEN",
    "next_permitted_pr": "DAL-A8 integration gates only",
}


class DalA7UsageStatus(StrEnum):
    """Closed DAL-A7 usage-status vocabulary."""

    USED = "USED"
    UNUSED = "UNUSED"
    SYMBOLIC = "SYMBOLIC"
    UNRESOLVED = "UNRESOLVED"


class DalA7LoanStatus(StrEnum):
    """Closed DAL-A7 loan-path status vocabulary."""

    NATIVE = "NATIVE"
    LOAN_VISIBLE = "LOAN_VISIBLE"
    LOAN_REQUIRED = "LOAN_REQUIRED"


class DalA7UnvocalizedStatus(StrEnum):
    """Closed DAL-A7 unvocalized-surface status vocabulary."""

    RESOLVED_BY_EVIDENCE = "RESOLVED_BY_EVIDENCE"
    CANDIDATE_SET_ONLY = "CANDIDATE_SET_ONLY"


class DalA7DeletionStatus(StrEnum):
    """Closed DAL-A7 deletion-license status vocabulary."""

    LICENSED = "LICENSED"
    UNLICENSED = "UNLICENSED"


class DalA7RuntimeStatus(StrEnum):
    """DAL-A7 runtime verdict status labels."""

    RUNTIME_GATES_CLOSED = "RUNTIME_GATES_CLOSED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class DalA7RuntimeInput:
    """DAL-A7 input wrapper over completed DAL-A6 runtime output only."""

    upstream_result: object
    unit_ref: str
    upstream_trace_ref: str
    local_trace_ref: str
    requested_handoff: str = "DAL_A7_LOCAL_ONLY"

    def __post_init__(self) -> None:
        _require_non_empty(self.unit_ref, "DalA7RuntimeInput.unit_ref", FailureCode.TRACE_MISSING)
        _require_non_empty(
            self.local_trace_ref,
            "DalA7RuntimeInput.local_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.requested_handoff,
            "DalA7RuntimeInput.requested_handoff",
            FailureCode.BOUNDARY_MISSING,
        )


@dataclass(frozen=True, slots=True)
class DalA7ResidualCandidate:
    """DAL-A7 bounded residual-gate candidate."""

    input_ref: str
    usage_status: DalA7UsageStatus
    loan_status: DalA7LoanStatus
    unvocalized_status: DalA7UnvocalizedStatus
    deletion_status: DalA7DeletionStatus
    upstream_trace_ref: str
    trace_ref: str
    residuals: tuple[str, ...]
    rank: Rank = Rank.CANDIDATE
    forbidden_outputs: tuple[str, ...] = DAL_A7_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.input_ref,
            "DalA7ResidualCandidate.input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.usage_status, DalA7UsageStatus):
            raise WeightCarrierSchemaError(
                "DalA7ResidualCandidate.usage_status must be DalA7UsageStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.loan_status, DalA7LoanStatus):
            raise WeightCarrierSchemaError(
                "DalA7ResidualCandidate.loan_status must be DalA7LoanStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.unvocalized_status, DalA7UnvocalizedStatus):
            raise WeightCarrierSchemaError(
                "DalA7ResidualCandidate.unvocalized_status must be DalA7UnvocalizedStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.deletion_status, DalA7DeletionStatus):
            raise WeightCarrierSchemaError(
                "DalA7ResidualCandidate.deletion_status must be DalA7DeletionStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.upstream_trace_ref,
            "DalA7ResidualCandidate.upstream_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.trace_ref,
            "DalA7ResidualCandidate.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA7ResidualCandidate.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA7ResidualCandidate.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _validate_rank(self.rank, "DalA7ResidualCandidate")
        _validate_forbidden_outputs(self.forbidden_outputs, "DalA7ResidualCandidate")


@dataclass(frozen=True, slots=True)
class DalA7RuntimeVerdict:
    """DAL-A7 runtime verdict wrapper."""

    status: DalA7RuntimeStatus
    candidate: DalA7ResidualCandidate | None
    residuals: tuple[str, ...]
    trace_ref: str
    upstream_trace_ref: str | None
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, DalA7RuntimeStatus):
            raise WeightCarrierSchemaError(
                "DalA7RuntimeVerdict.status must be DalA7RuntimeStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.candidate is not None and not isinstance(self.candidate, DalA7ResidualCandidate):
            raise WeightCarrierSchemaError(
                "DalA7RuntimeVerdict.candidate must be DalA7ResidualCandidate or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA7RuntimeVerdict.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA7RuntimeVerdict.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _require_non_empty(
            self.trace_ref,
            "DalA7RuntimeVerdict.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.upstream_trace_ref is not None:
            _require_non_empty(
                self.upstream_trace_ref,
                "DalA7RuntimeVerdict.upstream_trace_ref",
                FailureCode.TRACE_MISSING,
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise WeightCarrierSchemaError(
                "DalA7RuntimeVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=DAL_A7_RANK_CEILING)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


def _as_input(value: DalA7RuntimeInput | object) -> DalA7RuntimeInput:
    if isinstance(value, DalA7RuntimeInput):
        return value
    if isinstance(value, DalA6RuntimeVerdict):
        input_ref = (
            value.candidate.input_ref
            if value.candidate is not None
            else "dal-a7://missing-dal-a6-candidate"
        )
        return DalA7RuntimeInput(
            upstream_result=value,
            unit_ref=input_ref,
            upstream_trace_ref=value.trace_ref,
            local_trace_ref=f"{value.trace_ref}/dal-a7",
        )
    raise WeightCarrierSchemaError(
        "prove_dal_a7_runtime_gates input must be DalA7RuntimeInput or DalA6RuntimeVerdict "
        f"({FailureCode.GATE_REQUIRED.value})"
    )


def _optional_trace_ref(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _refusal(
    *,
    residual: str,
    trace_ref: str,
    upstream_trace_ref: str | None,
    failure_code: FailureCode,
    status: DalA7RuntimeStatus = DalA7RuntimeStatus.REFUSED,
) -> DalA7RuntimeVerdict:
    return DalA7RuntimeVerdict(
        status=status,
        candidate=None,
        residuals=(residual,),
        trace_ref=trace_ref,
        upstream_trace_ref=_optional_trace_ref(upstream_trace_ref),
        failure_code=failure_code,
    )


def _handoff_refusal(
    requested_handoff: str,
    trace_ref: str,
    upstream_trace_ref: str,
) -> DalA7RuntimeVerdict | None:
    token = requested_handoff.strip().upper()
    if token in {"DAL_A7_LOCAL_ONLY", "DAL-A7", "DAL_A7", "USAGE", "LOAN", "UNVOCALIZED"}:
        return None
    if token in {"DAL-A8", "DAL_A8", "DALALONECLOSED", "LAFZI_MADLUL_GATE"}:
        return _refusal(
            residual="DAL_A8_INTEGRATION_REQUIRED",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA7RuntimeStatus.DEFERRED,
        )
    if token in {"LAFZI", "LAFZI_B"}:
        return _refusal(
            residual="DAL_A8_INTEGRATION_REQUIRED",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA7RuntimeStatus.DEFERRED,
        )
    if token in {"SEMANTIC", "MEANING", "IFADAH", "MAFHUM", "TRUTH", "CERTAINTY", "REALITY"}:
        return _refusal(
            residual="SEMANTIC_OUTPUT_FORBIDDEN",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    if token in {"HUKM"}:
        return _refusal(
            residual="HUKM_OUTPUT_FORBIDDEN",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    if token in {"ROOT", "WEIGHT", "ROOT_IDENTITY_GATE", "WEIGHT_PATH_SELECTION_GATE"}:
        return _refusal(
            residual="ROOT_WEIGHT_OUTPUT_FORBIDDEN",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    if token in {"LAW-E0", "LAW_E0", "GLOBAL_METRIC_ENGINE", "METRIC_ENGINE"}:
        return _refusal(
            residual="GLOBAL_METRIC_ENGINE_FORBIDDEN",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    if token in {
        "PARSER",
        "MORPHOLOGY",
        "SYNTAX",
        "DAL-A8-RUNTIME",
        "LAFZI_RUNTIME",
        "LAFZI_OUTPUT",
        "LAFZI_MADLUL",
        "LAFZI_OBJECT",
    }:
        return _refusal(
            residual="FORBIDDEN_DOWNSTREAM_RUNTIME",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    return None


def _local_residuals(
    usage_status: DalA7UsageStatus,
    loan_status: DalA7LoanStatus,
    unvocalized_status: DalA7UnvocalizedStatus,
    deletion_status: DalA7DeletionStatus,
) -> tuple[str, ...]:
    residuals: list[str] = []
    if usage_status is DalA7UsageStatus.UNUSED:
        residuals.append("UNUSED_LAFZ")
    if loan_status is DalA7LoanStatus.LOAN_REQUIRED:
        residuals.append("LOAN_PATH_REQUIRED")
    if unvocalized_status is DalA7UnvocalizedStatus.CANDIDATE_SET_ONLY:
        residuals.append("UNVOCALIZED_SURFACE")
    if deletion_status is DalA7DeletionStatus.UNLICENSED:
        residuals.append("DELETION_UNLICENSED")
    return tuple(residuals)


def _deferred_from_local_residuals(
    *,
    local_residuals: tuple[str, ...],
    trace_ref: str,
    upstream_trace_ref: str,
) -> DalA7RuntimeVerdict | None:
    if not local_residuals:
        return None
    return _refusal(
        residual=local_residuals[0],
        trace_ref=trace_ref,
        upstream_trace_ref=upstream_trace_ref,
        failure_code=FailureCode.BOUNDARY_MISSING,
        status=DalA7RuntimeStatus.DEFERRED,
    )


def prove_dal_a7_runtime_gates(
    *,
    runtime_input: DalA7RuntimeInput | DalA6RuntimeVerdict,
    usage_status: DalA7UsageStatus,
    loan_status: DalA7LoanStatus,
    unvocalized_status: DalA7UnvocalizedStatus,
    deletion_status: DalA7DeletionStatus,
) -> DalA7RuntimeVerdict:
    """Prove DAL-A7 local residual gates over DAL-A6 output only."""
    dal_a7_input = _as_input(runtime_input)

    if not isinstance(dal_a7_input.upstream_result, DalA6RuntimeVerdict):
        return _refusal(
            residual="RAW_INPUT_FORBIDDEN",
            trace_ref=dal_a7_input.local_trace_ref,
            upstream_trace_ref=dal_a7_input.upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )

    if (
        dal_a7_input.upstream_result.status is not DalA6RuntimeStatus.RUNTIME_GATES_CLOSED
        or dal_a7_input.upstream_result.candidate is None
    ):
        return _refusal(
            residual="DAL_A6_RUNTIME_REQUIRED",
            trace_ref=dal_a7_input.local_trace_ref,
            upstream_trace_ref=dal_a7_input.upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA7RuntimeStatus.DEFERRED,
        )

    if not dal_a7_input.upstream_trace_ref.strip():
        return _refusal(
            residual="MISSING_DAL_A6_RUNTIME_TRACE",
            trace_ref=dal_a7_input.local_trace_ref,
            upstream_trace_ref=None,
            failure_code=FailureCode.TRACE_MISSING,
        )

    if not isinstance(usage_status, DalA7UsageStatus):
        raise WeightCarrierSchemaError(
            "prove_dal_a7_runtime_gates.usage_status must be DalA7UsageStatus "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(loan_status, DalA7LoanStatus):
        raise WeightCarrierSchemaError(
            "prove_dal_a7_runtime_gates.loan_status must be DalA7LoanStatus "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(unvocalized_status, DalA7UnvocalizedStatus):
        raise WeightCarrierSchemaError(
            "prove_dal_a7_runtime_gates.unvocalized_status must be DalA7UnvocalizedStatus "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(deletion_status, DalA7DeletionStatus):
        raise WeightCarrierSchemaError(
            "prove_dal_a7_runtime_gates.deletion_status must be DalA7DeletionStatus "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    handoff_refusal = _handoff_refusal(
        dal_a7_input.requested_handoff,
        dal_a7_input.local_trace_ref,
        dal_a7_input.upstream_trace_ref,
    )
    if handoff_refusal is not None:
        return handoff_refusal

    local_residuals = _local_residuals(
        usage_status=usage_status,
        loan_status=loan_status,
        unvocalized_status=unvocalized_status,
        deletion_status=deletion_status,
    )
    deferred = _deferred_from_local_residuals(
        local_residuals=local_residuals,
        trace_ref=dal_a7_input.local_trace_ref,
        upstream_trace_ref=dal_a7_input.upstream_trace_ref,
    )
    if deferred is not None:
        return deferred

    residuals = tuple(
        dict.fromkeys(
            (*dal_a7_input.upstream_result.candidate.residuals, "DAL_A7_LOCAL_RUNTIME_TRACE")
        )
    )
    candidate = DalA7ResidualCandidate(
        input_ref=dal_a7_input.unit_ref,
        usage_status=usage_status,
        loan_status=loan_status,
        unvocalized_status=unvocalized_status,
        deletion_status=deletion_status,
        upstream_trace_ref=dal_a7_input.upstream_trace_ref,
        trace_ref=dal_a7_input.local_trace_ref,
        residuals=residuals,
    )
    return DalA7RuntimeVerdict(
        status=DalA7RuntimeStatus.RUNTIME_GATES_CLOSED,
        candidate=candidate,
        residuals=residuals,
        trace_ref=dal_a7_input.local_trace_ref,
        upstream_trace_ref=dal_a7_input.upstream_trace_ref,
        failure_code=None,
    )


__all__ = [
    "DAL_A7_ALLOWED_SCOPE",
    "DAL_A7_FORBIDDEN_OUTPUTS",
    "DAL_A7_GATE_ORDER",
    "DAL_A7_RANK_CEILING",
    "DAL_A7_RESIDUAL_VOCABULARY",
    "DAL_A7_RUNTIME_VERDICT",
    "DalA7DeletionStatus",
    "DalA7LoanStatus",
    "DalA7ResidualCandidate",
    "DalA7RuntimeInput",
    "DalA7RuntimeStatus",
    "DalA7RuntimeVerdict",
    "DalA7UnvocalizedStatus",
    "DalA7UsageStatus",
    "prove_dal_a7_runtime_gates",
]
