"""DAL-A8 runtime integration gates for DalAloneClosed -> LafziMadlulGate only.

This module consumes only DAL-A7 runtime verdicts and remains bounded to
DalAloneClosed -> LafziMadlulGate integration. It does not open LAFZI-B
runtime surfaces, parser/morphology/syntax, or semantic/hukm/reality outputs.
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
from taaqqul_slot_geometry.weight.dal_a7_runtime_gates import (
    DalA7RuntimeStatus,
    DalA7RuntimeVerdict,
)

DAL_A8_RANK_CEILING: Rank = Rank.CANDIDATE
DAL_A8_ALLOWED_SCOPE: str = "DAL_ALONE_CLOSED_TO_LAFZI_GATE_INTEGRATION_ONLY"
DAL_A8_GATE_ORDER: tuple[str, ...] = (
    "DalAloneClosedIntegrationGate",
    "LafziMadlulGateBoundaryGate",
    "RuntimeVerdictGate",
)
DAL_A8_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "LAFZI_B1",
    "LAFZI_B2",
    "LAFZI_B3",
    "LAFZI_B4",
    "LAFZI_B5",
    "LAFZI_B6",
    "LAFZI_B7",
    "LafziMadlulCandidateSet",
    "WadiMadlulGate",
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
DAL_A8_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "MISSING_DAL_A7_RUNTIME_TRACE",
    "DAL_A7_RUNTIME_REQUIRED",
    "RAW_INPUT_FORBIDDEN",
    "LAFZI_B0_LAW_REQUIRED",
    "SEMANTIC_OUTPUT_FORBIDDEN",
    "HUKM_OUTPUT_FORBIDDEN",
    "ROOT_WEIGHT_OUTPUT_FORBIDDEN",
    "GLOBAL_METRIC_ENGINE_FORBIDDEN",
    "FORBIDDEN_DOWNSTREAM_RUNTIME",
    "DAL_A8_LOCAL_RUNTIME_TRACE",
)
DAL_A8_RUNTIME_VERDICT: dict[str, str] = {
    "status": "RUNTIME_GATES_CLOSED",
    "scope": "DAL_ALONE_CLOSED_TO_LAFZI_GATE_INTEGRATION_ONLY",
    "upstream_required": "DAL_A7_RUNTIME_CLOSED",
    "lafzi_gate_status": "OPENED_BOUNDARY_ONLY",
    "lafzi_candidate_set_status": "NOT_OPENED",
    "semantic_hukm_reality_status": "FORBIDDEN",
    "next_permitted_pr": "DAL-A8.1 corrective hardening only",
}


class DalA8IntegrationState(StrEnum):
    """Closed DAL-A8 integration-state vocabulary."""

    DAL_ALONE_CLOSED = "DAL_ALONE_CLOSED"


class DalA8LafziGateState(StrEnum):
    """Closed DAL-A8 Lafzi gate-state vocabulary."""

    OPENED_BOUNDARY_ONLY = "OPENED_BOUNDARY_ONLY"


class DalA8RuntimeStatus(StrEnum):
    """DAL-A8 runtime verdict status labels."""

    RUNTIME_GATES_CLOSED = "RUNTIME_GATES_CLOSED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class DalA8RuntimeInput:
    """DAL-A8 input wrapper over completed DAL-A7 runtime output only."""

    upstream_result: object
    unit_ref: str
    upstream_trace_ref: str
    local_trace_ref: str
    requested_handoff: str = "DAL_A8_INTEGRATION_ONLY"

    def __post_init__(self) -> None:
        _require_non_empty(self.unit_ref, "DalA8RuntimeInput.unit_ref", FailureCode.TRACE_MISSING)
        _require_non_empty(
            self.local_trace_ref,
            "DalA8RuntimeInput.local_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.requested_handoff,
            "DalA8RuntimeInput.requested_handoff",
            FailureCode.BOUNDARY_MISSING,
        )


@dataclass(frozen=True, slots=True)
class DalA8IntegrationCandidate:
    """DAL-A8 bounded integration candidate."""

    input_ref: str
    integration_state: DalA8IntegrationState
    lafzi_gate_state: DalA8LafziGateState
    upstream_trace_ref: str
    trace_ref: str
    residuals: tuple[str, ...]
    rank: Rank = Rank.CANDIDATE
    forbidden_outputs: tuple[str, ...] = DAL_A8_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.input_ref,
            "DalA8IntegrationCandidate.input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.integration_state, DalA8IntegrationState):
            raise WeightCarrierSchemaError(
                "DalA8IntegrationCandidate.integration_state must be DalA8IntegrationState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.lafzi_gate_state, DalA8LafziGateState):
            raise WeightCarrierSchemaError(
                "DalA8IntegrationCandidate.lafzi_gate_state must be DalA8LafziGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.upstream_trace_ref,
            "DalA8IntegrationCandidate.upstream_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.trace_ref,
            "DalA8IntegrationCandidate.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA8IntegrationCandidate.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA8IntegrationCandidate.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _validate_rank(self.rank, "DalA8IntegrationCandidate")
        _validate_forbidden_outputs(self.forbidden_outputs, "DalA8IntegrationCandidate")


@dataclass(frozen=True, slots=True)
class DalA8RuntimeVerdict:
    """DAL-A8 runtime verdict wrapper."""

    status: DalA8RuntimeStatus
    candidate: DalA8IntegrationCandidate | None
    residuals: tuple[str, ...]
    trace_ref: str
    upstream_trace_ref: str | None
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, DalA8RuntimeStatus):
            raise WeightCarrierSchemaError(
                "DalA8RuntimeVerdict.status must be DalA8RuntimeStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.candidate is not None and not isinstance(self.candidate, DalA8IntegrationCandidate):
            raise WeightCarrierSchemaError(
                "DalA8RuntimeVerdict.candidate must be DalA8IntegrationCandidate or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA8RuntimeVerdict.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA8RuntimeVerdict.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _require_non_empty(
            self.trace_ref,
            "DalA8RuntimeVerdict.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.upstream_trace_ref is not None:
            _require_non_empty(
                self.upstream_trace_ref,
                "DalA8RuntimeVerdict.upstream_trace_ref",
                FailureCode.TRACE_MISSING,
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise WeightCarrierSchemaError(
                "DalA8RuntimeVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=DAL_A8_RANK_CEILING)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


def _as_input(value: DalA8RuntimeInput | object) -> DalA8RuntimeInput:
    if isinstance(value, DalA8RuntimeInput):
        return value
    if isinstance(value, DalA7RuntimeVerdict):
        input_ref = (
            value.candidate.input_ref
            if value.candidate is not None
            else "dal-a8://missing-dal-a7-candidate"
        )
        return DalA8RuntimeInput(
            upstream_result=value,
            unit_ref=input_ref,
            upstream_trace_ref=value.trace_ref,
            local_trace_ref=f"{value.trace_ref}/dal-a8",
        )
    raise WeightCarrierSchemaError(
        "prove_dal_a8_runtime_gates input must be DalA8RuntimeInput or DalA7RuntimeVerdict "
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
    status: DalA8RuntimeStatus = DalA8RuntimeStatus.REFUSED,
) -> DalA8RuntimeVerdict:
    return DalA8RuntimeVerdict(
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
) -> DalA8RuntimeVerdict | None:
    token = requested_handoff.strip().upper()
    if token in {
        "DAL_A8_INTEGRATION_ONLY",
        "DAL-A8",
        "DAL_A8",
        "DALALONECLOSED",
        "LAFZI_MADLUL_GATE",
        "LAFZI",
        "LAFZI_B",
    }:
        return None
    if token in {"LAFZI-B0", "LAFZI_B0"}:
        return _refusal(
            residual="LAFZI_B0_LAW_REQUIRED",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA8RuntimeStatus.DEFERRED,
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
        "LAFZI_RUNTIME",
        "LAFZI_OUTPUT",
        "LAFZI_MADLUL",
        "LAFZI_OBJECT",
        "LAFZI_CANDIDATE_SET",
        "LAFZI_B1",
        "LAFZI_B2",
        "LAFZI_B3",
        "LAFZI_B4",
        "LAFZI_B5",
        "LAFZI_B6",
        "LAFZI_B7",
    }:
        return _refusal(
            residual="FORBIDDEN_DOWNSTREAM_RUNTIME",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    return None


def prove_dal_a8_runtime_gates(
    *,
    runtime_input: DalA8RuntimeInput | DalA7RuntimeVerdict,
) -> DalA8RuntimeVerdict:
    """Prove DAL-A8 DalAloneClosed -> LafziMadlulGate integration only."""
    dal_a8_input = _as_input(runtime_input)

    if not isinstance(dal_a8_input.upstream_result, DalA7RuntimeVerdict):
        return _refusal(
            residual="RAW_INPUT_FORBIDDEN",
            trace_ref=dal_a8_input.local_trace_ref,
            upstream_trace_ref=dal_a8_input.upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )

    if (
        dal_a8_input.upstream_result.status is not DalA7RuntimeStatus.RUNTIME_GATES_CLOSED
        or dal_a8_input.upstream_result.candidate is None
    ):
        return _refusal(
            residual="DAL_A7_RUNTIME_REQUIRED",
            trace_ref=dal_a8_input.local_trace_ref,
            upstream_trace_ref=dal_a8_input.upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA8RuntimeStatus.DEFERRED,
        )

    if not dal_a8_input.upstream_trace_ref.strip():
        return _refusal(
            residual="MISSING_DAL_A7_RUNTIME_TRACE",
            trace_ref=dal_a8_input.local_trace_ref,
            upstream_trace_ref=None,
            failure_code=FailureCode.TRACE_MISSING,
        )

    handoff_refusal = _handoff_refusal(
        dal_a8_input.requested_handoff,
        dal_a8_input.local_trace_ref,
        dal_a8_input.upstream_trace_ref,
    )
    if handoff_refusal is not None:
        return handoff_refusal

    residuals = tuple(
        dict.fromkeys(
            (*dal_a8_input.upstream_result.candidate.residuals, "DAL_A8_LOCAL_RUNTIME_TRACE")
        )
    )
    candidate = DalA8IntegrationCandidate(
        input_ref=dal_a8_input.unit_ref,
        integration_state=DalA8IntegrationState.DAL_ALONE_CLOSED,
        lafzi_gate_state=DalA8LafziGateState.OPENED_BOUNDARY_ONLY,
        upstream_trace_ref=dal_a8_input.upstream_trace_ref,
        trace_ref=dal_a8_input.local_trace_ref,
        residuals=residuals,
    )
    return DalA8RuntimeVerdict(
        status=DalA8RuntimeStatus.RUNTIME_GATES_CLOSED,
        candidate=candidate,
        residuals=residuals,
        trace_ref=dal_a8_input.local_trace_ref,
        upstream_trace_ref=dal_a8_input.upstream_trace_ref,
        failure_code=None,
    )


__all__ = [
    "DAL_A8_ALLOWED_SCOPE",
    "DAL_A8_FORBIDDEN_OUTPUTS",
    "DAL_A8_GATE_ORDER",
    "DAL_A8_RANK_CEILING",
    "DAL_A8_RESIDUAL_VOCABULARY",
    "DAL_A8_RUNTIME_VERDICT",
    "DalA8IntegrationCandidate",
    "DalA8IntegrationState",
    "DalA8LafziGateState",
    "DalA8RuntimeInput",
    "DalA8RuntimeStatus",
    "DalA8RuntimeVerdict",
    "prove_dal_a8_runtime_gates",
]
