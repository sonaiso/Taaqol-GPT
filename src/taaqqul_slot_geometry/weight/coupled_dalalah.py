"""LAFZI-D1 CoupledDalalah carrier surface and LAFZI-D2 MutabaqahGate.

This module consumes the bounded LAFZI-C8 CoupledDalalahGateResult surface
and introduces only the first D-stage carrier surface.

Constitutional invariants:

* CoupledDalalahSurface is a carrier, not mutabaqah, tadammun, or iltizam;
* MutabaqahGateResult is bounded to mutabaqah correspondence only;
* no dalalah matrix verdict, ifadah, hukm, tanzil, truth, or reality output;
* no global FailureCode expansion;
* residuals, rank, and trace remain visible at birth.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.wadi_c8_integration import (
    WADI_C8_RANK_CEILING,
    CoupledDalalahGateResult,
    WadiMadlulState,
)
from taaqqul_slot_geometry.weight.wadi_madlul import WadiMadlulContract, WadiResidual

LAFZI_D1_RANK_CEILING: Rank = WADI_C8_RANK_CEILING
LAFZI_D1_ALLOWED_OUTPUT: str = "COUPLED_DALALAH_SURFACE"
LAFZI_D2_RANK_CEILING: Rank = LAFZI_D1_RANK_CEILING
LAFZI_D2_ALLOWED_OUTPUT: str = "MUTABAQAH_GATE_RESULT"

LAFZI_D1_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "MADLUL_BOUNDARY_REQUIRED",
    "WAD_AUTHORITY_REQUIRED",
    "USAGE_SCOPE_REQUIRED",
    "MUTABAQAH_REQUIRED",
    "INTERNAL_PART_REQUIRED",
    "PART_OUTSIDE_MADLUL",
    "LAZIM_OUTSIDE_REQUIRED",
    "LUZUM_EVIDENCE_REQUIRED",
    "MERE_ASSOCIATION_NOT_LUZUM",
    "DOMAIN_MISMATCH",
    "ISHTIRAK_REQUIRES_QARINAH",
    "NAQL_SCOPE_REQUIRED",
    "MAJAZ_LICENSE_REQUIRED",
    "HIDDEN_DALALAH_MATRIX_RESIDUAL",
    "FORBIDDEN_IFADAH_JUMP",
    "FORBIDDEN_HUKM_JUMP",
)

LAFZI_D1_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "MUTABAQAH",
    "TADAMMUN",
    "ILTIZAM",
    "DALALAH_MATRIX",
    "IFADAH",
    "MAFHUM",
    "HUKM",
    "TANZIL",
    "REALITY",
    "TRUTH_VALUE",
    "ONTOLOGY",
    "FINAL_MEANING",
)

LAFZI_D2_FORBIDDEN_OUTPUTS: tuple[str, ...] = tuple(
    output for output in LAFZI_D1_FORBIDDEN_OUTPUTS if output != "MUTABAQAH"
)


class CoupledDalalahResidualKind(StrEnum):
    """Local LAFZI-D1 residual names from docs/62 §6."""

    MADLUL_BOUNDARY_REQUIRED = "MADLUL_BOUNDARY_REQUIRED"
    WAD_AUTHORITY_REQUIRED = "WAD_AUTHORITY_REQUIRED"
    USAGE_SCOPE_REQUIRED = "USAGE_SCOPE_REQUIRED"
    MUTABAQAH_REQUIRED = "MUTABAQAH_REQUIRED"
    INTERNAL_PART_REQUIRED = "INTERNAL_PART_REQUIRED"
    PART_OUTSIDE_MADLUL = "PART_OUTSIDE_MADLUL"
    LAZIM_OUTSIDE_REQUIRED = "LAZIM_OUTSIDE_REQUIRED"
    LUZUM_EVIDENCE_REQUIRED = "LUZUM_EVIDENCE_REQUIRED"
    MERE_ASSOCIATION_NOT_LUZUM = "MERE_ASSOCIATION_NOT_LUZUM"
    DOMAIN_MISMATCH = "DOMAIN_MISMATCH"
    ISHTIRAK_REQUIRES_QARINAH = "ISHTIRAK_REQUIRES_QARINAH"
    NAQL_SCOPE_REQUIRED = "NAQL_SCOPE_REQUIRED"
    MAJAZ_LICENSE_REQUIRED = "MAJAZ_LICENSE_REQUIRED"
    HIDDEN_DALALAH_MATRIX_RESIDUAL = "HIDDEN_DALALAH_MATRIX_RESIDUAL"
    FORBIDDEN_IFADAH_JUMP = "FORBIDDEN_IFADAH_JUMP"
    FORBIDDEN_HUKM_JUMP = "FORBIDDEN_HUKM_JUMP"


class MutabaqahGateState(StrEnum):
    """Bounded LAFZI-D2 MutabaqahGate states."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    if not isinstance(value, str) or not value.strip():
        raise WeightCarrierSchemaError(
            f"{field_name} must be a non-empty string ({failure_code.value})"
        )


def _validate_rank(rank: Rank, owner: str) -> None:
    if not isinstance(rank, Rank):
        raise WeightCarrierSchemaError(
            f"{owner}.rank must be a Rank member "
            f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
        )
    if rank > LAFZI_D1_RANK_CEILING:
        raise WeightCarrierSchemaError(
            f"{owner}.rank must not exceed CANDIDATE ({FailureCode.RANK_EXCEEDS_CEILING.value})"
        )


def _validate_string_tuple(values: tuple[str, ...], owner: str, failure_code: FailureCode) -> None:
    if not isinstance(values, tuple):
        raise WeightCarrierSchemaError(f"{owner} must be a tuple ({failure_code.value})")
    if not values:
        raise WeightCarrierSchemaError(f"{owner} must not be empty ({failure_code.value})")
    for value in values:
        _require_non_empty(value, f"{owner} entry", failure_code)


def _validate_wadi_residuals(residuals: tuple[WadiResidual, ...], owner: str) -> None:
    if not isinstance(residuals, tuple):
        raise WeightCarrierSchemaError(
            f"{owner} must be a tuple ({FailureCode.HIDDEN_RESIDUAL.value})"
        )
    for residual in residuals:
        if not isinstance(residual, WadiResidual):
            raise WeightCarrierSchemaError(
                f"{owner} entries must be WadiResidual ({FailureCode.HIDDEN_RESIDUAL.value})"
            )


def _validate_surface_disjoint(
    included_surface: tuple[str, ...],
    excluded_surface: tuple[str, ...],
    owner: str,
) -> None:
    overlap = set(included_surface).intersection(excluded_surface)
    if overlap:
        raise WeightCarrierSchemaError(
            f"{owner}.included_surface and excluded_surface must not overlap "
            f"({FailureCode.BOUNDARY_MISSING.value})"
        )


def _validate_forbidden_outputs(
    forbidden_outputs: tuple[str, ...],
    owner: str,
    expected: tuple[str, ...] = LAFZI_D1_FORBIDDEN_OUTPUTS,
) -> None:
    _validate_string_tuple(
        forbidden_outputs,
        f"{owner}.forbidden_outputs",
        FailureCode.OUTPUT_EXCEEDS_LAYER,
    )
    if forbidden_outputs != expected:
        raise WeightCarrierSchemaError(
            f"{owner}.forbidden_outputs must preserve the declared forbidden surface "
            f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
        )


def _validate_coupled_residuals(
    residuals: tuple[CoupledDalalahResidual, ...],
    owner: str,
) -> None:
    if not isinstance(residuals, tuple):
        raise WeightCarrierSchemaError(
            f"{owner}.residuals must be a tuple ({FailureCode.HIDDEN_RESIDUAL.value})"
        )
    for residual in residuals:
        if not isinstance(residual, CoupledDalalahResidual):
            raise WeightCarrierSchemaError(
                f"{owner}.residuals entries must be CoupledDalalahResidual "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if residual.visibility != "VISIBLE":
            raise WeightCarrierSchemaError(
                f"{owner}.residuals entries must remain VISIBLE "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


def _append_residual_once(
    residuals: tuple[CoupledDalalahResidual, ...],
    *,
    kind: CoupledDalalahResidualKind,
    trace_ref: str,
    detail: str = "",
    blocking: bool = False,
) -> tuple[CoupledDalalahResidual, ...]:
    if any(residual.kind is kind for residual in residuals):
        return residuals
    return residuals + (
        CoupledDalalahResidual(
            kind=kind,
            trace_ref=trace_ref,
            detail=detail,
            blocking=blocking,
        ),
    )


@dataclass(frozen=True, slots=True)
class CoupledDalalahResidual:
    """Visible local residual for the LAFZI-D1 carrier surface."""

    kind: CoupledDalalahResidualKind
    trace_ref: str
    detail: str = ""
    blocking: bool = False
    visibility: Literal["VISIBLE"] = "VISIBLE"

    def __post_init__(self) -> None:
        if not isinstance(self.kind, CoupledDalalahResidualKind):
            raise WeightCarrierSchemaError(
                "CoupledDalalahResidual.kind must be CoupledDalalahResidualKind "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        _require_non_empty(
            self.trace_ref,
            "CoupledDalalahResidual.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.visibility != "VISIBLE":
            raise WeightCarrierSchemaError(
                "CoupledDalalahResidual.visibility must remain VISIBLE "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise WeightCarrierSchemaError(
                "CoupledDalalahResidual.blocking must be bool "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class D1C8HandoffCard:
    """Explicit D1 birth card derived from a CLOSED C8 handoff and wadʿī contract."""

    c8_gate_result_ref: str
    c8_trace_ref: str
    contract_ref: str
    wadi_madlul_closed_ref: str
    lafzi_madlul_closed_ref: str
    madlul_boundary_ref: str
    included_surface: tuple[str, ...]
    excluded_surface: tuple[str, ...]
    domain_ref: str
    scope_ref: str
    prior_knowledge_refs: tuple[str, ...]
    c8_residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    c8_state: Literal["CLOSED"] = "CLOSED"

    def __post_init__(self) -> None:
        _require_non_empty(
            self.c8_gate_result_ref,
            "D1C8HandoffCard.c8_gate_result_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.c8_trace_ref,
            "D1C8HandoffCard.c8_trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.contract_ref,
            "D1C8HandoffCard.contract_ref",
            FailureCode.IDENTITY_BROKEN,
        )
        _require_non_empty(
            self.wadi_madlul_closed_ref,
            "D1C8HandoffCard.wadi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "D1C8HandoffCard.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.madlul_boundary_ref,
            "D1C8HandoffCard.madlul_boundary_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.included_surface,
            "D1C8HandoffCard.included_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.excluded_surface,
            "D1C8HandoffCard.excluded_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_surface_disjoint(
            self.included_surface,
            self.excluded_surface,
            "D1C8HandoffCard",
        )
        _require_non_empty(
            self.domain_ref,
            "D1C8HandoffCard.domain_ref",
            FailureCode.DOMAIN_MISSING,
        )
        _require_non_empty(self.scope_ref, "D1C8HandoffCard.scope_ref", FailureCode.SCOPE_MISSING)
        _validate_string_tuple(
            self.prior_knowledge_refs,
            "D1C8HandoffCard.prior_knowledge_refs",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _validate_wadi_residuals(self.c8_residuals, "D1C8HandoffCard.c8_residuals")
        _validate_rank(self.rank, "D1C8HandoffCard")
        _require_non_empty(self.trace_ref, "D1C8HandoffCard.trace_ref", FailureCode.TRACE_MISSING)
        if self.c8_state != "CLOSED":
            raise WeightCarrierSchemaError(
                "D1C8HandoffCard requires CLOSED C8 state "
                f"({FailureCode.GATE_REQUIRED.value})"
            )

    @classmethod
    def from_c8_gate_result(
        cls,
        c8_gate_result: CoupledDalalahGateResult,
        wadi_contract: WadiMadlulContract,
        *,
        prior_knowledge_refs: tuple[str, ...],
        trace_ref: str,
    ) -> D1C8HandoffCard:
        """Derive D1 birth fields from a CLOSED C8 result and its wadʿī contract."""

        if not isinstance(c8_gate_result, CoupledDalalahGateResult):
            raise WeightCarrierSchemaError(
                "D1C8HandoffCard requires CoupledDalalahGateResult "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(wadi_contract, WadiMadlulContract):
            raise WeightCarrierSchemaError(
                "D1C8HandoffCard requires WadiMadlulContract "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if c8_gate_result.state is not WadiMadlulState.CLOSED:
            raise WeightCarrierSchemaError(
                "D1C8HandoffCard requires CLOSED C8 gate result "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if c8_gate_result.contract_ref != wadi_contract.identity:
            raise WeightCarrierSchemaError(
                "CoupledDalalahGateResult.contract_ref must match WadiMadlulContract.identity "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if c8_gate_result.wadi_madlul_closed_ref != wadi_contract.identity:
            raise WeightCarrierSchemaError(
                "CoupledDalalahGateResult.wadi_madlul_closed_ref must match the closed "
                f"wadi contract ({FailureCode.IDENTITY_BROKEN.value})"
            )
        if c8_gate_result.lafzi_madlul_closed_ref != wadi_contract.lafzi_madlul_closed_ref:
            raise WeightCarrierSchemaError(
                "CoupledDalalahGateResult.lafzi_madlul_closed_ref must match "
                f"WadiMadlulContract.lafzi_madlul_closed_ref ({FailureCode.IDENTITY_BROKEN.value})"
            )

        return cls(
            c8_gate_result_ref=c8_gate_result.coupled_dalalah_ref,
            c8_trace_ref=c8_gate_result.trace_ref,
            contract_ref=wadi_contract.identity,
            wadi_madlul_closed_ref=c8_gate_result.wadi_madlul_closed_ref,
            lafzi_madlul_closed_ref=c8_gate_result.lafzi_madlul_closed_ref,
            madlul_boundary_ref=wadi_contract.meaning_identity.boundary,
            included_surface=wadi_contract.meaning_identity.included_surface,
            excluded_surface=wadi_contract.meaning_identity.excluded_surface,
            domain_ref=wadi_contract.usage_scope.domain_ref,
            scope_ref=wadi_contract.usage_scope.boundary_ref,
            prior_knowledge_refs=prior_knowledge_refs,
            c8_residuals=c8_gate_result.residuals,
            rank=LAFZI_D1_RANK_CEILING,
            trace_ref=trace_ref,
        )


@dataclass(frozen=True, slots=True)
class CoupledDalalahSurface:
    """Carrier-only D1 surface preserving the C8 coupling handoff."""

    birth_card: D1C8HandoffCard | None
    c8_gate_result_ref: str
    wadi_madlul_closed_ref: str
    lafzi_madlul_closed_ref: str
    madlul_boundary_ref: str
    included_surface: tuple[str, ...]
    excluded_surface: tuple[str, ...]
    domain_ref: str
    scope_ref: str
    prior_knowledge_refs: tuple[str, ...]
    c8_residuals: tuple[WadiResidual, ...]
    residuals: tuple[CoupledDalalahResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["COUPLED_DALALAH_SURFACE"] = "COUPLED_DALALAH_SURFACE"
    forbidden_outputs: tuple[str, ...] = LAFZI_D1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.birth_card, D1C8HandoffCard):
            raise WeightCarrierSchemaError(
                "CoupledDalalahSurface requires D1C8HandoffCard "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.c8_gate_result_ref,
            "CoupledDalalahSurface.c8_gate_result_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.wadi_madlul_closed_ref,
            "CoupledDalalahSurface.wadi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "CoupledDalalahSurface.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.madlul_boundary_ref,
            "CoupledDalalahSurface.madlul_boundary_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.included_surface,
            "CoupledDalalahSurface.included_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.excluded_surface,
            "CoupledDalalahSurface.excluded_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_surface_disjoint(
            self.included_surface,
            self.excluded_surface,
            "CoupledDalalahSurface",
        )
        _require_non_empty(
            self.domain_ref,
            "CoupledDalalahSurface.domain_ref",
            FailureCode.DOMAIN_MISSING,
        )
        _require_non_empty(
            self.scope_ref,
            "CoupledDalalahSurface.scope_ref",
            FailureCode.SCOPE_MISSING,
        )
        _validate_string_tuple(
            self.prior_knowledge_refs,
            "CoupledDalalahSurface.prior_knowledge_refs",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _validate_wadi_residuals(self.c8_residuals, "CoupledDalalahSurface.c8_residuals")
        _validate_coupled_residuals(self.residuals, "CoupledDalalahSurface")
        _validate_rank(self.rank, "CoupledDalalahSurface")
        _require_non_empty(
            self.trace_ref,
            "CoupledDalalahSurface.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_D1_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "CoupledDalalahSurface.output must stay inside D1 carrier surface "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "CoupledDalalahSurface")
        if (
            self.c8_gate_result_ref != self.birth_card.c8_gate_result_ref
            or self.wadi_madlul_closed_ref != self.birth_card.wadi_madlul_closed_ref
            or self.lafzi_madlul_closed_ref != self.birth_card.lafzi_madlul_closed_ref
            or self.madlul_boundary_ref != self.birth_card.madlul_boundary_ref
            or self.included_surface != self.birth_card.included_surface
            or self.excluded_surface != self.birth_card.excluded_surface
            or self.domain_ref != self.birth_card.domain_ref
            or self.scope_ref != self.birth_card.scope_ref
            or self.prior_knowledge_refs != self.birth_card.prior_knowledge_refs
            or self.c8_residuals != self.birth_card.c8_residuals
            or self.rank != self.birth_card.rank
        ):
            raise WeightCarrierSchemaError(
                "CoupledDalalahSurface fields must match D1C8HandoffCard "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )

    @classmethod
    def from_c8_gate_result(
        cls,
        c8_gate_result: CoupledDalalahGateResult,
        wadi_contract: WadiMadlulContract,
        *,
        prior_knowledge_refs: tuple[str, ...],
        residuals: tuple[CoupledDalalahResidual, ...] = (),
        trace_ref: str,
    ) -> CoupledDalalahSurface:
        """Construct the D1 carrier only from a CLOSED C8 handoff."""

        if not isinstance(c8_gate_result, CoupledDalalahGateResult):
            raise WeightCarrierSchemaError(
                "CoupledDalalahSurface requires CoupledDalalahGateResult "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if c8_gate_result.state is not WadiMadlulState.CLOSED:
            raise WeightCarrierSchemaError(
                "CoupledDalalahSurface requires CLOSED C8 gate result "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        birth_card = D1C8HandoffCard.from_c8_gate_result(
            c8_gate_result,
            wadi_contract,
            prior_knowledge_refs=prior_knowledge_refs,
            trace_ref=trace_ref,
        )
        return cls(
            birth_card=birth_card,
            c8_gate_result_ref=birth_card.c8_gate_result_ref,
            wadi_madlul_closed_ref=birth_card.wadi_madlul_closed_ref,
            lafzi_madlul_closed_ref=birth_card.lafzi_madlul_closed_ref,
            madlul_boundary_ref=birth_card.madlul_boundary_ref,
            included_surface=birth_card.included_surface,
            excluded_surface=birth_card.excluded_surface,
            domain_ref=birth_card.domain_ref,
            scope_ref=birth_card.scope_ref,
            prior_knowledge_refs=birth_card.prior_knowledge_refs,
            c8_residuals=birth_card.c8_residuals,
            residuals=residuals,
            rank=birth_card.rank,
            trace_ref=trace_ref,
        )


@dataclass(frozen=True, slots=True)
class MutabaqahGateResult:
    """Bounded LAFZI-D2 output for MutabaqahGate only."""

    state: MutabaqahGateState
    source_surface: CoupledDalalahSurface | None
    coupled_dalalah_surface_ref: str
    wadi_madlul_closed_ref: str
    lafzi_madlul_closed_ref: str
    madlul_boundary_ref: str
    included_surface: tuple[str, ...]
    excluded_surface: tuple[str, ...]
    domain_ref: str
    scope_ref: str
    residuals: tuple[CoupledDalalahResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["MUTABAQAH_GATE_RESULT"] = "MUTABAQAH_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_D2_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, MutabaqahGateState):
            raise WeightCarrierSchemaError(
                "MutabaqahGateResult.state must be MutabaqahGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.source_surface, CoupledDalalahSurface):
            raise WeightCarrierSchemaError(
                "MutabaqahGateResult requires CoupledDalalahSurface "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.coupled_dalalah_surface_ref,
            "MutabaqahGateResult.coupled_dalalah_surface_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.wadi_madlul_closed_ref,
            "MutabaqahGateResult.wadi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "MutabaqahGateResult.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.madlul_boundary_ref,
            "MutabaqahGateResult.madlul_boundary_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.included_surface,
            "MutabaqahGateResult.included_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.excluded_surface,
            "MutabaqahGateResult.excluded_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_surface_disjoint(
            self.included_surface,
            self.excluded_surface,
            "MutabaqahGateResult",
        )
        _require_non_empty(
            self.domain_ref,
            "MutabaqahGateResult.domain_ref",
            FailureCode.DOMAIN_MISSING,
        )
        _require_non_empty(
            self.scope_ref,
            "MutabaqahGateResult.scope_ref",
            FailureCode.SCOPE_MISSING,
        )
        _validate_coupled_residuals(self.residuals, "MutabaqahGateResult")
        _validate_rank(self.rank, "MutabaqahGateResult")
        _require_non_empty(
            self.trace_ref,
            "MutabaqahGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_D2_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "MutabaqahGateResult.output must stay inside LAFZI-D2 "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(
            self.forbidden_outputs,
            "MutabaqahGateResult",
            LAFZI_D2_FORBIDDEN_OUTPUTS,
        )
        source = self.source_surface
        if (
            self.coupled_dalalah_surface_ref != source.trace_ref
            or self.wadi_madlul_closed_ref != source.wadi_madlul_closed_ref
            or self.lafzi_madlul_closed_ref != source.lafzi_madlul_closed_ref
            or self.madlul_boundary_ref != source.madlul_boundary_ref
            or self.included_surface != source.included_surface
            or self.excluded_surface != source.excluded_surface
            or self.scope_ref != source.scope_ref
        ):
            raise WeightCarrierSchemaError(
                "MutabaqahGateResult must preserve source boundary and identity "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.domain_ref != source.domain_ref:
            raise WeightCarrierSchemaError(
                "MutabaqahGateResult DOMAIN_MISMATCH against source surface "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.rank != source.rank:
            raise WeightCarrierSchemaError(
                "MutabaqahGateResult must not promote rank beyond D1 "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )


def prove_mutabaqah_gate(
    surface: CoupledDalalahSurface,
    *,
    trace_ref: str,
) -> MutabaqahGateResult:
    """Run LAFZI-D2 MutabaqahGate without opening Tadammun or Iltizam."""

    if not isinstance(surface, CoupledDalalahSurface):
        raise WeightCarrierSchemaError(
            "prove_mutabaqah_gate requires CoupledDalalahSurface "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_mutabaqah_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )

    residuals = surface.residuals
    if not surface.madlul_boundary_ref.strip():
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.MADLUL_BOUNDARY_REQUIRED,
            trace_ref=trace_ref,
            blocking=True,
        )
    if not surface.included_surface:
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.MUTABAQAH_REQUIRED,
            trace_ref=trace_ref,
        )
    if any(residual.visibility != "VISIBLE" for residual in residuals):
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.HIDDEN_DALALAH_MATRIX_RESIDUAL,
            trace_ref=trace_ref,
            blocking=True,
        )

    if any(residual.blocking for residual in residuals):
        state = MutabaqahGateState.BLOCKED
    elif any(
        residual.kind
        in {
            CoupledDalalahResidualKind.MADLUL_BOUNDARY_REQUIRED,
            CoupledDalalahResidualKind.MUTABAQAH_REQUIRED,
            CoupledDalalahResidualKind.DOMAIN_MISMATCH,
            CoupledDalalahResidualKind.HIDDEN_DALALAH_MATRIX_RESIDUAL,
        }
        for residual in residuals
    ):
        state = MutabaqahGateState.DEFERRED
    else:
        state = MutabaqahGateState.PROVEN

    return MutabaqahGateResult(
        state=state,
        source_surface=surface,
        coupled_dalalah_surface_ref=surface.trace_ref,
        wadi_madlul_closed_ref=surface.wadi_madlul_closed_ref,
        lafzi_madlul_closed_ref=surface.lafzi_madlul_closed_ref,
        madlul_boundary_ref=surface.madlul_boundary_ref,
        included_surface=surface.included_surface,
        excluded_surface=surface.excluded_surface,
        domain_ref=surface.domain_ref,
        scope_ref=surface.scope_ref,
        residuals=residuals,
        rank=surface.rank,
        trace_ref=trace_ref,
    )


__all__ = [
    "CoupledDalalahResidual",
    "CoupledDalalahResidualKind",
    "CoupledDalalahSurface",
    "D1C8HandoffCard",
    "LAFZI_D1_ALLOWED_OUTPUT",
    "LAFZI_D1_FORBIDDEN_OUTPUTS",
    "LAFZI_D1_RANK_CEILING",
    "LAFZI_D1_RESIDUAL_VOCABULARY",
    "LAFZI_D2_ALLOWED_OUTPUT",
    "LAFZI_D2_FORBIDDEN_OUTPUTS",
    "LAFZI_D2_RANK_CEILING",
    "MutabaqahGateResult",
    "MutabaqahGateState",
    "prove_mutabaqah_gate",
]
