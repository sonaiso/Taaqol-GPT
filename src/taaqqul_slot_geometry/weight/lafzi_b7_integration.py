"""LAFZI-B7 runtime integration: LafziMadlulClosed -> Wad'iMadlulGate only.

This module consumes only LAFZI-B6 LafziResidualAudit output and closes
LafziMadlul under strict bounded conditions. It opens Wad'iMadlulGate as a
boundary only and does not cross into wad'i closure or downstream dalalah layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

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
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_residual_tuple as _shared_validate_residual_tuple,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lafzi_madlul import (
    LAFZI_B6_ALLOWED_OUTPUT,
    LAFZI_B6_RANK_CEILING,
    FormStateCandidate,
    InternalWordPathCandidate,
    LafziResidual,
    LafziResidualAuditResult,
    LafziResidualAuditState,
    SourceIdentityCandidate,
    WordKindCandidate,
)

LAFZI_B7_RANK_CEILING: Rank = Rank.CANDIDATE
LAFZI_B7_ALLOWED_OUTPUT: str = "LAFZI_MADLUL_CLOSED_RESULT"
LAFZI_B7_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "WADI_MADLUL_CLOSED",
    "MUTABAQAH",
    "TADAMMUN",
    "ILTIZAM",
    "RELATION",
    "COMPOSITION",
    "IFADAH",
    "MAFHUM",
    "HUKM",
    "TANZIL",
    "TRUTH",
    "CERTAINTY",
    "REALITY",
)


class LafziMadlulClosedState(StrEnum):
    """LAFZI-B7 state vocabulary."""

    CLOSED = "CLOSED"


class WadiMadlulGateState(StrEnum):
    """Wad'i boundary handoff state vocabulary for LAFZI-B7."""

    OPENED_BOUNDARY_ONLY = "OPENED_BOUNDARY_ONLY"


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=LAFZI_B7_RANK_CEILING)


def _validate_residuals(residuals: tuple[LafziResidual, ...], owner: str) -> None:
    _shared_validate_residual_tuple(residuals, owner, expected_type=LafziResidual)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


@dataclass(frozen=True, slots=True)
class LafziMadlulClosed:
    """Bounded LAFZI-B7 closure output that opens Wad'i gate only."""

    state: LafziMadlulClosedState
    lafzi_residual_audit_ref: str
    word_kind: WordKindCandidate
    source_identity: SourceIdentityCandidate
    form_state: FormStateCandidate
    internal_word_path: InternalWordPathCandidate
    residuals: tuple[LafziResidual, ...]
    wadi_gate_state: WadiMadlulGateState
    rank: Rank
    trace_ref: str
    output: Literal["LAFZI_MADLUL_CLOSED_RESULT"] = "LAFZI_MADLUL_CLOSED_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_B7_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, LafziMadlulClosedState):
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed.state must be LafziMadlulClosedState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.lafzi_residual_audit_ref,
            "LafziMadlulClosed.lafzi_residual_audit_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.word_kind, WordKindCandidate):
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed.word_kind must be WordKindCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.source_identity, SourceIdentityCandidate):
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed.source_identity must be SourceIdentityCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.form_state, FormStateCandidate):
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed.form_state must be FormStateCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.internal_word_path, InternalWordPathCandidate):
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed.internal_word_path must be InternalWordPathCandidate "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_residuals(self.residuals, "LafziMadlulClosed")
        if self.residuals:
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed must be residual-clean at closure "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.wadi_gate_state, WadiMadlulGateState):
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed.wadi_gate_state must be WadiMadlulGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _validate_rank(self.rank, "LafziMadlulClosed")
        _require_non_empty(
            self.trace_ref,
            "LafziMadlulClosed.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_B7_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed.output must stay inside LAFZI-B7 "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "LafziMadlulClosed")
        if self.forbidden_outputs != LAFZI_B7_FORBIDDEN_OUTPUTS:
            raise WeightCarrierSchemaError(
                "LafziMadlulClosed.forbidden_outputs must match LAFZI-B7 canonical ledger "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )


def prove_lafzi_madlul_closed(
    lafzi_residual_audit_result: LafziResidualAuditResult,
    *,
    trace_ref: str,
) -> LafziMadlulClosed:
    """Run LAFZI-B7 closure from LAFZI-B6 and open Wad'i gate boundary only."""

    if not isinstance(lafzi_residual_audit_result, LafziResidualAuditResult):
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed requires LafziResidualAuditResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_lafzi_madlul_closed.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    if lafzi_residual_audit_result.output != LAFZI_B6_ALLOWED_OUTPUT:
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed prior result must be LAFZI-B6 output "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if lafzi_residual_audit_result.rank > LAFZI_B6_RANK_CEILING:
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed prior rank must not exceed CANDIDATE "
            f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
        )
    if lafzi_residual_audit_result.state is not LafziResidualAuditState.PROVEN:
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed requires PROVEN LAFZI-B6 state "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if lafzi_residual_audit_result.word_kind in (
        WordKindCandidate.BLOCKED,
        WordKindCandidate.AMBIGUOUS,
    ):
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed refuses blocked/ambiguous word kind "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if lafzi_residual_audit_result.source_identity is SourceIdentityCandidate.DEFERRED_SOURCE:
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed refuses deferred source identity "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if lafzi_residual_audit_result.form_state is FormStateCandidate.DEFERRED:
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed refuses deferred form state "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if lafzi_residual_audit_result.internal_word_path is InternalWordPathCandidate.DEFERRED:
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed refuses deferred internal path "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if (
        lafzi_residual_audit_result.residuals
        or lafzi_residual_audit_result.blocking_residuals
        or lafzi_residual_audit_result.non_blocking_residuals
    ):
        raise WeightCarrierSchemaError(
            "prove_lafzi_madlul_closed requires no residuals at closure "
            f"({FailureCode.HIDDEN_RESIDUAL.value})"
        )

    return LafziMadlulClosed(
        state=LafziMadlulClosedState.CLOSED,
        lafzi_residual_audit_ref=lafzi_residual_audit_result.trace_ref,
        word_kind=lafzi_residual_audit_result.word_kind,
        source_identity=lafzi_residual_audit_result.source_identity,
        form_state=lafzi_residual_audit_result.form_state,
        internal_word_path=lafzi_residual_audit_result.internal_word_path,
        residuals=(),
        wadi_gate_state=WadiMadlulGateState.OPENED_BOUNDARY_ONLY,
        rank=LAFZI_B7_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "LAFZI_B7_ALLOWED_OUTPUT",
    "LAFZI_B7_FORBIDDEN_OUTPUTS",
    "LAFZI_B7_RANK_CEILING",
    "LafziMadlulClosed",
    "LafziMadlulClosedState",
    "WadiMadlulGateState",
    "prove_lafzi_madlul_closed",
]
