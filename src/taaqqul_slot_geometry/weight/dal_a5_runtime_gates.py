"""DAL-A5 runtime gates for syllable/transition/adjacency/S1-S5 only.

This module consumes only DAL-A4 runtime gate outputs and remains bounded to
local DAL-A5 runtime classification. It does not open DAL-A6/DAL-A7/DAL-A8,
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
from taaqqul_slot_geometry.weight.dal_a4_runtime_gates import DalA4GateResult

DAL_A5_RANK_CEILING: Rank = Rank.CANDIDATE
DAL_A5_ALLOWED_SCOPE: str = "SYLLABLE_TRANSITION_ADJACENCY_S1_S5_ONLY"
DAL_A5_GATE_ORDER: tuple[str, ...] = (
    "SyllableShapeGate",
    "TransitionGate",
    "AdjacencyGate",
    "S1S5VocabularyGate",
    "RuntimeVerdictGate",
)
DAL_A5_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "DAL_A6",
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
DAL_A5_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "MISSING_DAL_A4_RUNTIME_TRACE",
    "RAW_INPUT_FORBIDDEN",
    "DAL_A6_WAQF_WASL_REQUIRED",
    "DAL_A7_USAGE_POLICY_REQUIRED",
    "LAFZI_OUTPUT_FORBIDDEN",
    "SEMANTIC_OUTPUT_FORBIDDEN",
    "HUKM_OUTPUT_FORBIDDEN",
    "ROOT_WEIGHT_OUTPUT_FORBIDDEN",
    "GLOBAL_METRIC_ENGINE_FORBIDDEN",
    "FORBIDDEN_DOWNSTREAM_RUNTIME",
)
DAL_A5_RUNTIME_VERDICT: dict[str, str] = {
    "status": "RUNTIME_GATES_CLOSED",
    "scope": "SYLLABLE_TRANSITION_ADJACENCY_S1_S5_ONLY",
    "upstream_required": "DAL_A4_RUNTIME_CLOSED",
    "dal_a6_status": "DEFERRED",
    "dal_a7_status": "DEFERRED",
    "dal_a8_status": "DEFERRED",
    "lafzi_b_status": "DEFERRED",
    "semantic_hukm_reality_status": "FORBIDDEN",
}


class DalA5SyllableShape(StrEnum):
    """Closed DAL-A5 syllable-shape vocabulary."""

    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"
    S5 = "S5"


class DalA5TransitionKind(StrEnum):
    """DAL-A5 local transition labels."""

    OPEN_TO_CLOSED = "OPEN_TO_CLOSED"
    CLOSED_TO_OPEN = "CLOSED_TO_OPEN"
    CLOSED_TO_CLOSED = "CLOSED_TO_CLOSED"
    OPEN_TO_OPEN = "OPEN_TO_OPEN"


class DalA5AdjacencyVerdict(StrEnum):
    """DAL-A5 local adjacency verdict labels."""

    ADJACENT_ALLOWED = "ADJACENT_ALLOWED"
    ADJACENT_DEFERRED = "ADJACENT_DEFERRED"


class DalA5RuntimeStatus(StrEnum):
    """DAL-A5 runtime verdict status labels."""

    RUNTIME_GATES_CLOSED = "RUNTIME_GATES_CLOSED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class DalA5SyllableInput:
    """DAL-A5 input wrapper over completed DAL-A4 runtime surface only."""

    upstream_result: object
    unit_ref: str
    upstream_trace_ref: str
    local_trace_ref: str
    requested_handoff: str = "DAL_A5_LOCAL_ONLY"

    def __post_init__(self) -> None:
        _require_non_empty(self.unit_ref, "DalA5SyllableInput.unit_ref", FailureCode.TRACE_MISSING)
        _require_non_empty(
            self.local_trace_ref,
            "DalA5SyllableInput.local_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.requested_handoff,
            "DalA5SyllableInput.requested_handoff",
            FailureCode.BOUNDARY_MISSING,
        )


@dataclass(frozen=True, slots=True)
class DalA5TransitionCandidate:
    """Local DAL-A5 transition candidate only."""

    transition_kind: DalA5TransitionKind
    adjacency: DalA5AdjacencyVerdict
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.transition_kind, DalA5TransitionKind):
            raise WeightCarrierSchemaError(
                "DalA5TransitionCandidate.transition_kind must be DalA5TransitionKind "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.adjacency, DalA5AdjacencyVerdict):
            raise WeightCarrierSchemaError(
                "DalA5TransitionCandidate.adjacency must be DalA5AdjacencyVerdict "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.trace_ref,
            "DalA5TransitionCandidate.trace_ref",
            FailureCode.TRACE_MISSING,
        )


@dataclass(frozen=True, slots=True)
class DalA5SyllableCandidate:
    """DAL-A5 bounded syllable/transition/adjacency candidate."""

    input_ref: str
    syllable_shape: DalA5SyllableShape
    transition: DalA5TransitionCandidate
    upstream_trace_ref: str
    trace_ref: str
    residuals: tuple[str, ...]
    rank: Rank = Rank.CANDIDATE
    forbidden_outputs: tuple[str, ...] = DAL_A5_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.input_ref,
            "DalA5SyllableCandidate.input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.syllable_shape, DalA5SyllableShape):
            raise WeightCarrierSchemaError(
                "DalA5SyllableCandidate.syllable_shape must be DalA5SyllableShape "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.transition, DalA5TransitionCandidate):
            raise WeightCarrierSchemaError(
                "DalA5SyllableCandidate.transition must be DalA5TransitionCandidate "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.upstream_trace_ref,
            "DalA5SyllableCandidate.upstream_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.trace_ref,
            "DalA5SyllableCandidate.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA5SyllableCandidate.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA5SyllableCandidate.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _validate_rank(self.rank, "DalA5SyllableCandidate")
        _validate_forbidden_outputs(self.forbidden_outputs, "DalA5SyllableCandidate")


@dataclass(frozen=True, slots=True)
class DalA5RuntimeVerdict:
    """DAL-A5 runtime verdict wrapper."""

    status: DalA5RuntimeStatus
    candidate: DalA5SyllableCandidate | None
    residuals: tuple[str, ...]
    trace_ref: str
    upstream_trace_ref: str | None
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.status, DalA5RuntimeStatus):
            raise WeightCarrierSchemaError(
                "DalA5RuntimeVerdict.status must be DalA5RuntimeStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.candidate is not None and not isinstance(self.candidate, DalA5SyllableCandidate):
            raise WeightCarrierSchemaError(
                "DalA5RuntimeVerdict.candidate must be DalA5SyllableCandidate or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA5RuntimeVerdict.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA5RuntimeVerdict.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _require_non_empty(
            self.trace_ref,
            "DalA5RuntimeVerdict.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.upstream_trace_ref is not None:
            _require_non_empty(
                self.upstream_trace_ref,
                "DalA5RuntimeVerdict.upstream_trace_ref",
                FailureCode.TRACE_MISSING,
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise WeightCarrierSchemaError(
                "DalA5RuntimeVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=DAL_A5_RANK_CEILING)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


def _as_input(value: DalA5SyllableInput | object) -> DalA5SyllableInput:
    if isinstance(value, DalA5SyllableInput):
        return value
    if isinstance(value, DalA4GateResult):
        return DalA5SyllableInput(
            upstream_result=value,
            unit_ref=value.certificate.input_ref,
            upstream_trace_ref=value.certificate.trace_ref,
            local_trace_ref=f"{value.certificate.trace_ref}/dal-a5",
        )
    raise WeightCarrierSchemaError(
        "prove_dal_a5_runtime_gates input must be DalA5SyllableInput or DalA4GateResult "
        f"({FailureCode.GATE_REQUIRED.value})"
    )


def _refusal(
    *,
    residual: str,
    trace_ref: str,
    upstream_trace_ref: str | None,
    failure_code: FailureCode,
    status: DalA5RuntimeStatus = DalA5RuntimeStatus.REFUSED,
) -> DalA5RuntimeVerdict:
    return DalA5RuntimeVerdict(
        status=status,
        candidate=None,
        residuals=(residual,),
        trace_ref=trace_ref,
        upstream_trace_ref=upstream_trace_ref,
        failure_code=failure_code,
    )


def _handoff_refusal(
    requested_handoff: str,
    trace_ref: str,
    upstream_trace_ref: str,
) -> DalA5RuntimeVerdict | None:
    token = requested_handoff.strip().upper()
    if token in {"DAL-A6", "DAL_A6", "WAQF", "WASL"}:
        return _refusal(
            residual="DAL_A6_WAQF_WASL_REQUIRED",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA5RuntimeStatus.DEFERRED,
        )
    if token in {"DAL-A7", "DAL_A7", "USAGE", "LOAN", "DELETION", "UNVOCALIZED"}:
        return _refusal(
            residual="DAL_A7_USAGE_POLICY_REQUIRED",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.BOUNDARY_MISSING,
            status=DalA5RuntimeStatus.DEFERRED,
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
        "DAL-A6-RUNTIME",
        "DAL-A7-RUNTIME",
    }:
        return _refusal(
            residual="FORBIDDEN_DOWNSTREAM_RUNTIME",
            trace_ref=trace_ref,
            upstream_trace_ref=upstream_trace_ref,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )
    return None


def prove_dal_a5_runtime_gates(
    *,
    runtime_input: DalA5SyllableInput | DalA4GateResult,
    syllable_shape: DalA5SyllableShape,
    transition_kind: DalA5TransitionKind,
    adjacency_ok: bool,
) -> DalA5RuntimeVerdict:
    """Prove DAL-A5 local runtime gates over DAL-A4 output only."""
    dal_a5_input = _as_input(runtime_input)

    if not isinstance(dal_a5_input.upstream_result, DalA4GateResult):
        return _refusal(
            residual="RAW_INPUT_FORBIDDEN",
            trace_ref=dal_a5_input.local_trace_ref,
            upstream_trace_ref=dal_a5_input.upstream_trace_ref or None,
            failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
        )

    if not dal_a5_input.upstream_trace_ref.strip():
        return _refusal(
            residual="MISSING_DAL_A4_RUNTIME_TRACE",
            trace_ref=dal_a5_input.local_trace_ref,
            upstream_trace_ref=None,
            failure_code=FailureCode.TRACE_MISSING,
        )

    if not isinstance(syllable_shape, DalA5SyllableShape):
        raise WeightCarrierSchemaError(
            "prove_dal_a5_runtime_gates.syllable_shape must be DalA5SyllableShape "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(transition_kind, DalA5TransitionKind):
        raise WeightCarrierSchemaError(
            "prove_dal_a5_runtime_gates.transition_kind must be DalA5TransitionKind "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(adjacency_ok, bool):
        raise WeightCarrierSchemaError(
            "prove_dal_a5_runtime_gates.adjacency_ok must be bool "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    handoff_refusal = _handoff_refusal(
        dal_a5_input.requested_handoff,
        dal_a5_input.local_trace_ref,
        dal_a5_input.upstream_trace_ref,
    )
    if handoff_refusal is not None:
        return handoff_refusal

    adjacency = (
        DalA5AdjacencyVerdict.ADJACENT_ALLOWED
        if adjacency_ok
        else DalA5AdjacencyVerdict.ADJACENT_DEFERRED
    )
    transition = DalA5TransitionCandidate(
        transition_kind=transition_kind,
        adjacency=adjacency,
        trace_ref=dal_a5_input.local_trace_ref,
    )
    residuals = tuple(dict.fromkeys(
        (*dal_a5_input.upstream_result.certificate.residuals, "DAL_A5_LOCAL_RUNTIME_TRACE")
    ))
    candidate = DalA5SyllableCandidate(
        input_ref=dal_a5_input.unit_ref,
        syllable_shape=syllable_shape,
        transition=transition,
        upstream_trace_ref=dal_a5_input.upstream_trace_ref,
        trace_ref=dal_a5_input.local_trace_ref,
        residuals=residuals,
    )
    return DalA5RuntimeVerdict(
        status=DalA5RuntimeStatus.RUNTIME_GATES_CLOSED,
        candidate=candidate,
        residuals=residuals,
        trace_ref=dal_a5_input.local_trace_ref,
        upstream_trace_ref=dal_a5_input.upstream_trace_ref,
        failure_code=None,
    )


__all__ = [
    "DAL_A5_ALLOWED_SCOPE",
    "DAL_A5_FORBIDDEN_OUTPUTS",
    "DAL_A5_GATE_ORDER",
    "DAL_A5_RANK_CEILING",
    "DAL_A5_RESIDUAL_VOCABULARY",
    "DAL_A5_RUNTIME_VERDICT",
    "DalA5AdjacencyVerdict",
    "DalA5RuntimeStatus",
    "DalA5RuntimeVerdict",
    "DalA5SyllableCandidate",
    "DalA5SyllableInput",
    "DalA5SyllableShape",
    "DalA5TransitionCandidate",
    "DalA5TransitionKind",
    "prove_dal_a5_runtime_gates",
]
