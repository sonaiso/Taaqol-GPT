"""LAFZI-D1 CoupledDalalah carrier surface.

This module consumes the bounded LAFZI-C8 CoupledDalalahGateResult surface
and introduces only the first D-stage carrier surface.

Constitutional invariants:

* CoupledDalalahSurface is a carrier, not mutabaqah, tadammun, or iltizam;
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
from taaqqul_slot_geometry.weight.wadi_madlul import WadiResidual

LAFZI_D1_RANK_CEILING: Rank = WADI_C8_RANK_CEILING
LAFZI_D1_ALLOWED_OUTPUT: str = "COUPLED_DALALAH_SURFACE"

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
class CoupledDalalahSurface:
    """Carrier-only D1 surface preserving the C8 coupling handoff."""

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
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "CoupledDalalahSurface.residuals must be a tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            if not isinstance(residual, CoupledDalalahResidual):
                raise WeightCarrierSchemaError(
                    "CoupledDalalahSurface.residuals entries must be CoupledDalalahResidual "
                    f"({FailureCode.HIDDEN_RESIDUAL.value})"
                )
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
        _validate_string_tuple(
            self.forbidden_outputs,
            "CoupledDalalahSurface.forbidden_outputs",
            FailureCode.OUTPUT_EXCEEDS_LAYER,
        )

    @classmethod
    def from_c8_gate_result(
        cls,
        c8_gate_result: CoupledDalalahGateResult,
        *,
        madlul_boundary_ref: str,
        included_surface: tuple[str, ...],
        excluded_surface: tuple[str, ...],
        domain_ref: str,
        scope_ref: str,
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
        return cls(
            c8_gate_result_ref=c8_gate_result.coupled_dalalah_ref,
            wadi_madlul_closed_ref=c8_gate_result.wadi_madlul_closed_ref,
            lafzi_madlul_closed_ref=c8_gate_result.lafzi_madlul_closed_ref,
            madlul_boundary_ref=madlul_boundary_ref,
            included_surface=included_surface,
            excluded_surface=excluded_surface,
            domain_ref=domain_ref,
            scope_ref=scope_ref,
            prior_knowledge_refs=prior_knowledge_refs,
            c8_residuals=c8_gate_result.residuals,
            residuals=residuals,
            rank=LAFZI_D1_RANK_CEILING,
            trace_ref=trace_ref,
        )


__all__ = [
    "CoupledDalalahResidual",
    "CoupledDalalahResidualKind",
    "CoupledDalalahSurface",
    "LAFZI_D1_ALLOWED_OUTPUT",
    "LAFZI_D1_FORBIDDEN_OUTPUTS",
    "LAFZI_D1_RANK_CEILING",
    "LAFZI_D1_RESIDUAL_VOCABULARY",
]
