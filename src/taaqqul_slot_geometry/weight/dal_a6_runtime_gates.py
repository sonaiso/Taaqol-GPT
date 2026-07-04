"""DAL-A6 runtime gates for detailed waqf/wasl closure only.

This module consumes only DAL-A5 runtime verdicts and remains bounded to
local DAL-A6 waqf/wasl closure execution. It does not open DAL-A7/DAL-A8,
LAFZI, parser/morphology/syntax, or semantic/hukm/reality outputs.
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
from taaqqul_slot_geometry.weight.dal_a5_runtime_gates import (
    DalA5RuntimeStatus,
    DalA5RuntimeVerdict,
)

DAL_A6_RANK_CEILING: Rank = Rank.CANDIDATE
DAL_A6_ALLOWED_SCOPE: str = "DETAILED_WAQF_WASL_CLOSURE_ONLY"
DAL_A6_GATE_ORDER: tuple[str, ...] = (
    "WaqfGate",
    "WaslGate",
    "RuntimeVerdictGate",
)
DAL_A6_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "DAL_A7",
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
DAL_A6_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "MISSING_DAL_A5_RUNTIME_TRACE",
    "DAL_A5_RUNTIME_REQUIRED",
    "RAW_INPUT_FORBIDDEN",
    "DAL_A7_USAGE_POLICY_REQUIRED",
    "LAFZI_OUTPUT_FORBIDDEN",
    "SEMANTIC_OUTPUT_FORBIDDEN",
    "HUKM_OUTPUT_FORBIDDEN",
    "ROOT_WEIGHT_OUTPUT_FORBIDDEN",
    "GLOBAL_METRIC_ENGINE_FORBIDDEN",
    "FORBIDDEN_DOWNSTREAM_RUNTIME",
    "DAL_A6_LOCAL_RUNTIME_TRACE",
)
DAL_A6_RUNTIME_VERDICT: dict[str, str] = {
    "status": "RUNTIME_GATES_CLOSED",
    "scope": "DETAILED_WAQF_WASL_CLOSURE_ONLY",
    "upstream_required": "DAL_A5_RUNTIME_CLOSED",
    "dal_a7_status": "DEFERRED",
    "dal_a8_status": "DEFERRED",
    "lafzi_b_status": "DEFERRED",
    "semantic_hukm_reality_status": "FORBIDDEN",
    "next_permitted_pr": "DAL-A7 runtime gates only",
}


class DalA6WaqfClosure(StrEnum):
    """Closed DAL-A6 waqf-closure vocabulary."""

    WAQF_SUKUN = "WAQF_SUKUN"
    TA_MARBUTA_STOP_HA = "TA_MARBUTA_STOP_HA"
    TANWIN_STOP_DROP = "TANWIN_STOP_DROP"


class DalA6WaslClosure(StrEnum):
    """Closed DAL-A6 wasl-closure vocabulary."""

    WASL_CONTINUE_HARAKA = "WASL_CONTINUE_HARAKA"
    HAMZAT_WASL_DROP = "HAMZAT_WASL_DROP"
    TANWIN_LINK_CONTINUE = "TANWIN_LINK_CONTINUE"


class DalA6RuntimeStatus(StrEnum):
    """DAL-A6 runtime verdict status labels."""

    RUNTIME_GATES_CLOSED = "RUNTIME_GATES_CLOSED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class DalA6RuntimeInput:
    """DAL-A6 input wrapper over completed DAL-A5 runtime output only."""

    upstream_result: object
    unit_ref: str
    upstream_trace_ref: str
    local_trace_ref: str
    requested_handoff: str = "DAL_A6_LOCAL_ONLY"

    def __post_init__(self) -> None:
        _require_non_empty(self.unit_ref, "DalA6RuntimeInput.unit_ref", FailureCode.TRACE_MISSING)
        _require_non_empty(
            self.local_trace_ref,
            "DalA6RuntimeInput.local_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.requested_handoff,
            "DalA6RuntimeInput.requested_handoff",
            FailureCode.BOUNDARY_MISSING,
        )


@dataclass(frozen=True, slots=True)
class DalA6WaqfWaslCandidate:
    """DAL-A6 bounded waqf/wasl closure candidate."""

    input_ref: str
    waqf_closure: DalA6WaqfClosure
    wasl_closure: DalA6WaslClosure
    upstream_trace_ref: str
    trace_ref: str
    residuals: tuple[str, ...]
    rank: Rank = Rank.CANDIDATE
    forbidden_outputs: tuple[str, ...] = DAL_A6_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.input_ref,
            "DalA6WaqfWaslCandidate.input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.waqf_closure, DalA6WaqfClosure):
            raise WeightCarrierSchemaError(
                "DalA6WaqfWaslCandidate.waqf_closure must be DalA6WaqfClosure "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.wasl_closure, DalA6WaslClosure):
            raise WeightCarrierSchemaError(
                "DalA6WaqfWaslCandidate.wasl_closure must be DalA6WaslClosure "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.upstream_trace_ref,
            "DalA6WaqfWaslCandidate.upstream_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.trace_ref,
            "DalA6WaqfWaslCandidate.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA6WaqfWaslCandidate.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA6WaqfWaslCandidate.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _validate_rank(self.rank, "DalA6WaqfWaslCandidate")
        _validate_forbidden_outputs(self.forbidden_outputs, "DalA6WaqfWaslCandidate")


@dataclass(frozen=True, slots=True)
class DalA6RuntimeVerdict:
    """DAL-A6 runtime verdict wrapper."""

    status: DalA6RuntimeStatus
    candidate: DalA6WaqfWaslCandidate | None
    residuals: tuple[str, ...]
    trace_ref: str
    upstream_trace_ref: str | None
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, DalA6RuntimeStatus):
            raise WeightCarrierSchemaError(
                "DalA6RuntimeVerdict.status must be DalA6RuntimeStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.candidate is not None and not isinstance(self.candidate, DalA6WaqfWaslCandidate):
            raise WeightCarrierSchemaError(
                "DalA6RuntimeVerdict.candidate must be DalA6WaqfWaslCandidate or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA6RuntimeVerdict.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA6RuntimeVerdict.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _require_non_empty(
            self.trace_ref,
            "DalA6RuntimeVerdict.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.upstream_trace_ref is not None:
            _require_non_empty(
                self.upstream_trace_ref,
                "DalA6RuntimeVerdict.upstream_trace_ref",
                FailureCode.TRACE_MISSING,
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise WeightCarrierSchemaError(
                "DalA6RuntimeVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=DAL_A6_RANK_CEILING)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


def _as_input(value: DalA6RuntimeInput | object) -> DalA6RuntimeInput:
    if isinstance(value, DalA6RuntimeInput):
        return value
    if isinstance(value, DalA5RuntimeVerdict):
        input_ref = (
            value.candidate.input_ref
            if value.candidate is not None
            else "dal-a6://missing-dal-a5-candidate"
        )
        return DalA6RuntimeInput(
            upstream_result=value,
            unit_ref=input_ref,
            upstream_trace_ref=value.trace_ref,
            local_trace_ref=f"{value.trace_ref}/dal-a6",
        )
    raise WeightCarrierSchemaError(
        "prove_dal_a6_runtime_gates input must be DalA6RuntimeInput or DalA5RuntimeVerdict "
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
    status: DalA6RuntimeStatus = DalA6RuntimeStatus.REFUSED,
) -> DalA6RuntimeVerdict:
    return DalA6RuntimeVerdict(
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
) -> DalA6RuntimeVerdict | None:
    token = requested_handoff.strip().upper()
    if token in {"DAL_A6_LOCAL_ONLY", "DAL-A6", "DAL_A6", "WAQF", "WASL"}:
        return None
    if token in {"DAL-A7", "DAL_A7", "USAGE", "LOAN", "UNVOCALIZED", "DELETION"}:
        return _refusal(
            residual="DAL_A7_USAGE_POLICY_REQUIRED",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA6RuntimeStatus.DEFERRED,
        )
    if token in {"LAFZI", "LAFZI_B", "LAFZI_MADLUL_GATE"}:
        return _refusal(
            residual="LAFZI_OUTPUT_FORBIDDEN",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
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
        "DAL-A8",
        "DAL_A8",
        "DAL-A7-RUNTIME",
        "DAL-A8-RUNTIME",
    }:
        return _refusal(
            residual="FORBIDDEN_DOWNSTREAM_RUNTIME",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    return None


def prove_dal_a6_runtime_gates(
    *,
    runtime_input: DalA6RuntimeInput | DalA5RuntimeVerdict,
    waqf_closure: DalA6WaqfClosure,
    wasl_closure: DalA6WaslClosure,
) -> DalA6RuntimeVerdict:
    """Prove DAL-A6 local waqf/wasl runtime gates over DAL-A5 output only."""
    dal_a6_input = _as_input(runtime_input)

    if not isinstance(dal_a6_input.upstream_result, DalA5RuntimeVerdict):
        return _refusal(
            residual="RAW_INPUT_FORBIDDEN",
            trace_ref=dal_a6_input.local_trace_ref,
            upstream_trace_ref=dal_a6_input.upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )

    if (
        dal_a6_input.upstream_result.status is not DalA5RuntimeStatus.RUNTIME_GATES_CLOSED
        or dal_a6_input.upstream_result.candidate is None
    ):
        return _refusal(
            residual="DAL_A5_RUNTIME_REQUIRED",
            trace_ref=dal_a6_input.local_trace_ref,
            upstream_trace_ref=dal_a6_input.upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA6RuntimeStatus.DEFERRED,
        )

    if not dal_a6_input.upstream_trace_ref.strip():
        return _refusal(
            residual="MISSING_DAL_A5_RUNTIME_TRACE",
            trace_ref=dal_a6_input.local_trace_ref,
            upstream_trace_ref=None,
            failure_code=FailureCode.TRACE_MISSING,
        )

    if not isinstance(waqf_closure, DalA6WaqfClosure):
        raise WeightCarrierSchemaError(
            "prove_dal_a6_runtime_gates.waqf_closure must be DalA6WaqfClosure "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(wasl_closure, DalA6WaslClosure):
        raise WeightCarrierSchemaError(
            "prove_dal_a6_runtime_gates.wasl_closure must be DalA6WaslClosure "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    handoff_refusal = _handoff_refusal(
        dal_a6_input.requested_handoff,
        dal_a6_input.local_trace_ref,
        dal_a6_input.upstream_trace_ref,
    )
    if handoff_refusal is not None:
        return handoff_refusal

    residuals = tuple(
        dict.fromkeys(
            (*dal_a6_input.upstream_result.candidate.residuals, "DAL_A6_LOCAL_RUNTIME_TRACE")
        )
    )
    candidate = DalA6WaqfWaslCandidate(
        input_ref=dal_a6_input.unit_ref,
        waqf_closure=waqf_closure,
        wasl_closure=wasl_closure,
        upstream_trace_ref=dal_a6_input.upstream_trace_ref,
        trace_ref=dal_a6_input.local_trace_ref,
        residuals=residuals,
    )
    return DalA6RuntimeVerdict(
        status=DalA6RuntimeStatus.RUNTIME_GATES_CLOSED,
        candidate=candidate,
        residuals=residuals,
        trace_ref=dal_a6_input.local_trace_ref,
        upstream_trace_ref=dal_a6_input.upstream_trace_ref,
        failure_code=None,
    )


__all__ = [
    "DAL_A6_ALLOWED_SCOPE",
    "DAL_A6_FORBIDDEN_OUTPUTS",
    "DAL_A6_GATE_ORDER",
    "DAL_A6_RANK_CEILING",
    "DAL_A6_RESIDUAL_VOCABULARY",
    "DAL_A6_RUNTIME_VERDICT",
    "DalA6RuntimeInput",
    "DalA6RuntimeStatus",
    "DalA6RuntimeVerdict",
    "DalA6WaqfClosure",
    "DalA6WaqfWaslCandidate",
    "DalA6WaslClosure",
    "prove_dal_a6_runtime_gates",
]
