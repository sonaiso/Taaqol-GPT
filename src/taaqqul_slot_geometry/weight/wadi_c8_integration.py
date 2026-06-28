"""LAFZI-C8 Wad'iMadlulClosed -> CoupledDalalahGate integration.

This module consumes the completed LAFZI-C7 `WadiResidualAuditResult` and
produces the bounded C8 closure/integration surface only.

Constitutional invariants:

* no hidden residuals;
* no rank promotion above `CANDIDATE`;
* no jump to mutabaqah/tadammun/iltizam/ifadah/hukm/tanzil/reality;
* no global `FailureCode` expansion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight._schema_helpers import (
    merge_residuals as _shared_merge_residuals,
)
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
from taaqqul_slot_geometry.weight.wadi_madlul import (
    WADI_C7_RANK_CEILING,
    WadiMadlulContract,
    WadiResidual,
    WadiResidualAuditResult,
    WadiResidualAuditState,
)

WADI_C8_RANK_CEILING: Rank = WADI_C7_RANK_CEILING
WADI_C8_ALLOWED_OUTPUT: str = "COUPLED_DALALAH_GATE_RESULT"

WADI_C8_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "MUTABAQAH",
    "TADAMMUN",
    "ILTIZAM",
    "IFADAH",
    "HUKM",
    "TANZIL",
    "REALITY",
    "ONTOLOGY",
)


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=WADI_C8_RANK_CEILING)


def _validate_residuals(residuals: tuple[WadiResidual, ...], owner: str) -> None:
    _shared_validate_residual_tuple(residuals, owner, expected_type=WadiResidual)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


def _merge_residuals(
    *residual_groups: tuple[WadiResidual, ...],
) -> tuple[WadiResidual, ...]:
    return _shared_merge_residuals(*residual_groups)


class WadiMadlulState(StrEnum):
    """LAFZI-C8 closure state for W7 WadiStopGate."""

    CLOSED = "CLOSED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class WadiMadlulClosed:
    """Bounded closed wadʿī madlūl carrier opened by LAFZI-C8."""

    contract_ref: str
    lafzi_madlul_closed_ref: str
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["WADI_MADLUL_CLOSED"] = "WADI_MADLUL_CLOSED"
    forbidden_outputs: tuple[str, ...] = WADI_C8_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.contract_ref,
            "WadiMadlulClosed.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "WadiMadlulClosed.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _validate_residuals(self.residuals, "WadiMadlulClosed")
        _validate_rank(self.rank, "WadiMadlulClosed")
        _require_non_empty(
            self.trace_ref,
            "WadiMadlulClosed.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _validate_forbidden_outputs(self.forbidden_outputs, "WadiMadlulClosed")


@dataclass(frozen=True, slots=True)
class WadiMadlulVerdict:
    """W7 verdict from `prove_wadi_madlul()`."""

    state: WadiMadlulState
    contract_ref: str
    closed: WadiMadlulClosed | None
    failure_code: FailureCode | None
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, WadiMadlulState):
            raise WeightCarrierSchemaError(
                "WadiMadlulVerdict.state must be WadiMadlulState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.contract_ref,
            "WadiMadlulVerdict.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.closed is not None and not isinstance(self.closed, WadiMadlulClosed):
            raise WeightCarrierSchemaError(
                "WadiMadlulVerdict.closed must be WadiMadlulClosed or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.state is WadiMadlulState.CLOSED and self.closed is None:
            raise WeightCarrierSchemaError(
                "CLOSED WadiMadlulVerdict must include WadiMadlulClosed "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.state is not WadiMadlulState.CLOSED and self.closed is not None:
            raise WeightCarrierSchemaError(
                "Only CLOSED verdict may include WadiMadlulClosed "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise WeightCarrierSchemaError(
                "WadiMadlulVerdict.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _validate_residuals(self.residuals, "WadiMadlulVerdict")
        _validate_rank(self.rank, "WadiMadlulVerdict")
        _require_non_empty(
            self.trace_ref,
            "WadiMadlulVerdict.trace_ref",
            FailureCode.TRACE_MISSING,
        )


@dataclass(frozen=True, slots=True)
class WadiStopGateResult:
    """Bounded W7 output before opening CoupledDalalahGate."""

    state: WadiMadlulState
    contract_ref: str
    wadi_madlul_closed_ref: str
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["WADI_STOP_GATE_RESULT"] = "WADI_STOP_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = WADI_C8_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, WadiMadlulState):
            raise WeightCarrierSchemaError(
                "WadiStopGateResult.state must be WadiMadlulState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.contract_ref,
            "WadiStopGateResult.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.state is WadiMadlulState.CLOSED:
            _require_non_empty(
                self.wadi_madlul_closed_ref,
                "WadiStopGateResult.wadi_madlul_closed_ref",
                FailureCode.TRACE_MISSING,
            )
        elif self.wadi_madlul_closed_ref:
            raise WeightCarrierSchemaError(
                "Non-CLOSED WadiStopGateResult must not carry wadi_madlul_closed_ref "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _validate_residuals(self.residuals, "WadiStopGateResult")
        _validate_rank(self.rank, "WadiStopGateResult")
        _require_non_empty(
            self.trace_ref,
            "WadiStopGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _validate_forbidden_outputs(self.forbidden_outputs, "WadiStopGateResult")


@dataclass(frozen=True, slots=True)
class CoupledDalalahGateResult:
    """Bounded LAFZI-C8 integration output opening CoupledDalalahGate."""

    state: WadiMadlulState
    contract_ref: str
    wadi_madlul_closed_ref: str
    lafzi_madlul_closed_ref: str
    coupled_dalalah_ref: str
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["COUPLED_DALALAH_GATE_RESULT"] = "COUPLED_DALALAH_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = WADI_C8_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, WadiMadlulState):
            raise WeightCarrierSchemaError(
                "CoupledDalalahGateResult.state must be WadiMadlulState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.contract_ref,
            "CoupledDalalahGateResult.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "CoupledDalalahGateResult.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.state is WadiMadlulState.CLOSED:
            _require_non_empty(
                self.wadi_madlul_closed_ref,
                "CoupledDalalahGateResult.wadi_madlul_closed_ref",
                FailureCode.TRACE_MISSING,
            )
            _require_non_empty(
                self.coupled_dalalah_ref,
                "CoupledDalalahGateResult.coupled_dalalah_ref",
                FailureCode.TRACE_MISSING,
            )
        elif self.wadi_madlul_closed_ref or self.coupled_dalalah_ref:
            raise WeightCarrierSchemaError(
                "Non-CLOSED CoupledDalalahGateResult must not carry closure refs "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _validate_residuals(self.residuals, "CoupledDalalahGateResult")
        _validate_rank(self.rank, "CoupledDalalahGateResult")
        _require_non_empty(
            self.trace_ref,
            "CoupledDalalahGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != WADI_C8_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "CoupledDalalahGateResult.output must stay inside C8 integration "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "CoupledDalalahGateResult")


def prove_wadi_madlul(
    contract: WadiMadlulContract,
    residual_audit_result: WadiResidualAuditResult,
    *,
    trace_ref: str,
) -> WadiMadlulVerdict:
    """Run W7 closure decision from a validated C7 residual-audit result."""

    if not isinstance(contract, WadiMadlulContract):
        raise WeightCarrierSchemaError(
            "prove_wadi_madlul requires WadiMadlulContract "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(residual_audit_result, WadiResidualAuditResult):
        raise WeightCarrierSchemaError(
            "prove_wadi_madlul requires WadiResidualAuditResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(trace_ref, "prove_wadi_madlul.trace_ref", FailureCode.TRACE_MISSING)
    if residual_audit_result.contract_ref != contract.identity:
        raise WeightCarrierSchemaError(
            "WadiResidualAuditResult.contract_ref must preserve WadiMadlulContract.identity "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )

    residuals = _merge_residuals(contract.residuals, residual_audit_result.residuals)
    closed: WadiMadlulClosed | None = None

    if residual_audit_result.state is WadiResidualAuditState.BLOCKED or any(
        residual.blocking for residual in residuals
    ):
        state = WadiMadlulState.BLOCKED
        failure_code: FailureCode | None = FailureCode.BLOCKING_RESIDUAL_PRESENT
    elif residual_audit_result.state is WadiResidualAuditState.DEFERRED:
        state = WadiMadlulState.DEFERRED
        failure_code = None
    else:
        state = WadiMadlulState.CLOSED
        failure_code = None
        closed = WadiMadlulClosed(
            contract_ref=contract.identity,
            lafzi_madlul_closed_ref=contract.lafzi_madlul_closed_ref,
            residuals=residuals,
            rank=WADI_C8_RANK_CEILING,
            trace_ref=trace_ref,
        )

    return WadiMadlulVerdict(
        state=state,
        contract_ref=contract.identity,
        closed=closed,
        failure_code=failure_code,
        residuals=residuals,
        rank=WADI_C8_RANK_CEILING,
        trace_ref=trace_ref,
    )


def prove_wadi_stop_gate(
    wadi_madlul_verdict: WadiMadlulVerdict,
    *,
    trace_ref: str,
) -> WadiStopGateResult:
    """Emit bounded W7 stop-gate output before CoupledDalalahGate opening."""

    if not isinstance(wadi_madlul_verdict, WadiMadlulVerdict):
        raise WeightCarrierSchemaError(
            "prove_wadi_stop_gate requires WadiMadlulVerdict "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(trace_ref, "prove_wadi_stop_gate.trace_ref", FailureCode.TRACE_MISSING)

    return WadiStopGateResult(
        state=wadi_madlul_verdict.state,
        contract_ref=wadi_madlul_verdict.contract_ref,
        wadi_madlul_closed_ref=(
            wadi_madlul_verdict.closed.contract_ref
            if wadi_madlul_verdict.closed is not None
            else ""
        ),
        residuals=wadi_madlul_verdict.residuals,
        rank=WADI_C8_RANK_CEILING,
        trace_ref=trace_ref,
    )


def prove_coupled_dalalah_gate(
    contract: WadiMadlulContract,
    wadi_stop_result: WadiStopGateResult,
    *,
    trace_ref: str,
) -> CoupledDalalahGateResult:
    """Integrate W7 output into the bounded CoupledDalalahGate opening."""

    if not isinstance(contract, WadiMadlulContract):
        raise WeightCarrierSchemaError(
            "prove_coupled_dalalah_gate requires WadiMadlulContract "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(wadi_stop_result, WadiStopGateResult):
        raise WeightCarrierSchemaError(
            "prove_coupled_dalalah_gate requires WadiStopGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_coupled_dalalah_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    if wadi_stop_result.contract_ref != contract.identity:
        raise WeightCarrierSchemaError(
            "WadiStopGateResult.contract_ref must preserve WadiMadlulContract.identity "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )

    if wadi_stop_result.state is WadiMadlulState.CLOSED:
        coupled_dalalah_ref = f"coupled-dalalah://{contract.identity}"
        wadi_madlul_closed_ref = wadi_stop_result.wadi_madlul_closed_ref
    else:
        coupled_dalalah_ref = ""
        wadi_madlul_closed_ref = ""

    return CoupledDalalahGateResult(
        state=wadi_stop_result.state,
        contract_ref=contract.identity,
        wadi_madlul_closed_ref=wadi_madlul_closed_ref,
        lafzi_madlul_closed_ref=contract.lafzi_madlul_closed_ref,
        coupled_dalalah_ref=coupled_dalalah_ref,
        residuals=wadi_stop_result.residuals,
        rank=WADI_C8_RANK_CEILING,
        trace_ref=trace_ref,
    )


def prove_wadi_to_coupled_dalalah(
    contract: WadiMadlulContract,
    residual_audit_result: WadiResidualAuditResult,
    *,
    trace_ref: str,
) -> CoupledDalalahGateResult:
    """Run the full LAFZI-C8 chain: W7 closure + CoupledDalalahGate opening."""

    wadi_verdict = prove_wadi_madlul(
        contract,
        residual_audit_result,
        trace_ref=trace_ref,
    )
    wadi_stop_result = prove_wadi_stop_gate(wadi_verdict, trace_ref=trace_ref)
    return prove_coupled_dalalah_gate(contract, wadi_stop_result, trace_ref=trace_ref)


__all__ = [
    "CoupledDalalahGateResult",
    "WADI_C8_ALLOWED_OUTPUT",
    "WADI_C8_FORBIDDEN_OUTPUTS",
    "WADI_C8_RANK_CEILING",
    "WadiMadlulClosed",
    "WadiMadlulState",
    "WadiMadlulVerdict",
    "WadiStopGateResult",
    "prove_coupled_dalalah_gate",
    "prove_wadi_madlul",
    "prove_wadi_stop_gate",
    "prove_wadi_to_coupled_dalalah",
]
