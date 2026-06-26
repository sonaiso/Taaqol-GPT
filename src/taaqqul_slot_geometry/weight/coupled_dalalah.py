"""LAFZI-D1 CoupledDalalah carrier surface through LAFZI-D5 residual audit.

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
LAFZI_D3_RANK_CEILING: Rank = LAFZI_D2_RANK_CEILING
LAFZI_D3_ALLOWED_OUTPUT: str = "TADAMMUN_GATE_RESULT"
LAFZI_D4_RANK_CEILING: Rank = LAFZI_D3_RANK_CEILING
LAFZI_D4_ALLOWED_OUTPUT: str = "ILTIZAM_GATE_RESULT"
LAFZI_D5_RANK_CEILING: Rank = LAFZI_D4_RANK_CEILING
LAFZI_D5_ALLOWED_OUTPUT: str = "DALALAH_MATRIX_RESIDUAL_AUDIT_RESULT"

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

LAFZI_D3_FORBIDDEN_OUTPUTS: tuple[str, ...] = tuple(
    output for output in LAFZI_D2_FORBIDDEN_OUTPUTS if output != "TADAMMUN"
)

LAFZI_D4_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "DALALAH_MATRIX",
    "WORD_CAPABILITY",
    "IFADAH",
    "MAFHUM",
    "HUKM",
    "TANZIL",
    "REALITY",
    "TRUTH_VALUE",
    "ONTOLOGY",
    "FINAL_MEANING",
)

LAFZI_D5_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "DALALAH_MATRIX_CLOSED",
    "DALALAH_MATRIX",
    "WORD_CAPABILITY",
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


class MutabaqahGateState(StrEnum):
    """Bounded LAFZI-D2 MutabaqahGate states."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class TadammunGateState(StrEnum):
    """Bounded LAFZI-D3 TadammunGate states."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class IltizamGateState(StrEnum):
    """Bounded LAFZI-D4 IltizamGate states."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class DalalahMatrixResidualAuditState(StrEnum):
    """Bounded LAFZI-D5 residual-audit states; not matrix closure."""

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
    source_surface: CoupledDalalahSurface
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


@dataclass(frozen=True, slots=True)
class TadammunGateResult:
    """Bounded LAFZI-D3 output for TadammunGate only."""

    state: TadammunGateState
    source_result: MutabaqahGateResult
    mutabaqah_gate_result_ref: str
    wadi_madlul_closed_ref: str
    lafzi_madlul_closed_ref: str
    madlul_boundary_ref: str
    included_surface: tuple[str, ...]
    excluded_surface: tuple[str, ...]
    claimed_internal_part_ref: str
    domain_ref: str
    scope_ref: str
    residuals: tuple[CoupledDalalahResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["TADAMMUN_GATE_RESULT"] = "TADAMMUN_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_D3_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, TadammunGateState):
            raise WeightCarrierSchemaError(
                "TadammunGateResult.state must be TadammunGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.source_result, MutabaqahGateResult):
            raise WeightCarrierSchemaError(
                "TadammunGateResult requires MutabaqahGateResult "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.mutabaqah_gate_result_ref,
            "TadammunGateResult.mutabaqah_gate_result_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.wadi_madlul_closed_ref,
            "TadammunGateResult.wadi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "TadammunGateResult.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.madlul_boundary_ref,
            "TadammunGateResult.madlul_boundary_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.included_surface,
            "TadammunGateResult.included_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.excluded_surface,
            "TadammunGateResult.excluded_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_surface_disjoint(
            self.included_surface,
            self.excluded_surface,
            "TadammunGateResult",
        )
        _require_non_empty(
            self.claimed_internal_part_ref,
            "TadammunGateResult.claimed_internal_part_ref",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _require_non_empty(
            self.domain_ref,
            "TadammunGateResult.domain_ref",
            FailureCode.DOMAIN_MISSING,
        )
        _require_non_empty(
            self.scope_ref,
            "TadammunGateResult.scope_ref",
            FailureCode.SCOPE_MISSING,
        )
        _validate_coupled_residuals(self.residuals, "TadammunGateResult")
        _validate_rank(self.rank, "TadammunGateResult")
        _require_non_empty(
            self.trace_ref,
            "TadammunGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_D3_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "TadammunGateResult.output must stay inside LAFZI-D3 "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(
            self.forbidden_outputs,
            "TadammunGateResult",
            LAFZI_D3_FORBIDDEN_OUTPUTS,
        )
        source = self.source_result
        if (
            self.mutabaqah_gate_result_ref != source.trace_ref
            or self.wadi_madlul_closed_ref != source.wadi_madlul_closed_ref
            or self.lafzi_madlul_closed_ref != source.lafzi_madlul_closed_ref
            or self.madlul_boundary_ref != source.madlul_boundary_ref
            or self.included_surface != source.included_surface
            or self.excluded_surface != source.excluded_surface
            or self.scope_ref != source.scope_ref
        ):
            raise WeightCarrierSchemaError(
                "TadammunGateResult must preserve D2 boundary and identity "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.domain_ref != source.domain_ref:
            raise WeightCarrierSchemaError(
                "TadammunGateResult DOMAIN_MISMATCH against D2 result "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.rank != source.rank:
            raise WeightCarrierSchemaError(
                "TadammunGateResult must not promote rank beyond D2 "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.source_result.state is MutabaqahGateState.BLOCKED and (
            self.state is not TadammunGateState.BLOCKED
        ):
            raise WeightCarrierSchemaError(
                "TadammunGateResult must preserve blocked Mutabaqah state "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.source_result.state is MutabaqahGateState.DEFERRED and (
            self.state is TadammunGateState.PROVEN
        ):
            raise WeightCarrierSchemaError(
                "TadammunGateResult must not prove over deferred Mutabaqah "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not self.residuals[: len(source.residuals)] == source.residuals:
            raise WeightCarrierSchemaError(
                "TadammunGateResult must preserve D2 residuals "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class IltizamGateResult:
    """Bounded LAFZI-D4 output for IltizamGate only."""

    state: IltizamGateState
    source_result: TadammunGateResult
    tadammun_gate_result_ref: str
    wadi_madlul_closed_ref: str
    lafzi_madlul_closed_ref: str
    madlul_boundary_ref: str
    included_surface: tuple[str, ...]
    excluded_surface: tuple[str, ...]
    claimed_external_lazim_ref: str
    luzum_evidence_ref: str
    domain_ref: str
    scope_ref: str
    residuals: tuple[CoupledDalalahResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["ILTIZAM_GATE_RESULT"] = "ILTIZAM_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = LAFZI_D4_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, IltizamGateState):
            raise WeightCarrierSchemaError(
                "IltizamGateResult.state must be IltizamGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.source_result, TadammunGateResult):
            raise WeightCarrierSchemaError(
                "IltizamGateResult requires TadammunGateResult "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.tadammun_gate_result_ref,
            "IltizamGateResult.tadammun_gate_result_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.wadi_madlul_closed_ref,
            "IltizamGateResult.wadi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "IltizamGateResult.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.madlul_boundary_ref,
            "IltizamGateResult.madlul_boundary_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.included_surface,
            "IltizamGateResult.included_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.excluded_surface,
            "IltizamGateResult.excluded_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_surface_disjoint(
            self.included_surface,
            self.excluded_surface,
            "IltizamGateResult",
        )
        _require_non_empty(
            self.claimed_external_lazim_ref,
            "IltizamGateResult.claimed_external_lazim_ref",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _require_non_empty(
            self.luzum_evidence_ref,
            "IltizamGateResult.luzum_evidence_ref",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _require_non_empty(
            self.domain_ref,
            "IltizamGateResult.domain_ref",
            FailureCode.DOMAIN_MISSING,
        )
        _require_non_empty(
            self.scope_ref,
            "IltizamGateResult.scope_ref",
            FailureCode.SCOPE_MISSING,
        )
        _validate_coupled_residuals(self.residuals, "IltizamGateResult")
        _validate_rank(self.rank, "IltizamGateResult")
        _require_non_empty(
            self.trace_ref,
            "IltizamGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_D4_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "IltizamGateResult.output must stay inside LAFZI-D4 "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(
            self.forbidden_outputs,
            "IltizamGateResult",
            LAFZI_D4_FORBIDDEN_OUTPUTS,
        )
        source = self.source_result
        if (
            self.tadammun_gate_result_ref != source.trace_ref
            or self.wadi_madlul_closed_ref != source.wadi_madlul_closed_ref
            or self.lafzi_madlul_closed_ref != source.lafzi_madlul_closed_ref
            or self.madlul_boundary_ref != source.madlul_boundary_ref
            or self.included_surface != source.included_surface
            or self.excluded_surface != source.excluded_surface
            or self.scope_ref != source.scope_ref
        ):
            raise WeightCarrierSchemaError(
                "IltizamGateResult must preserve D3 boundary and identity "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.domain_ref != source.domain_ref:
            raise WeightCarrierSchemaError(
                "IltizamGateResult DOMAIN_MISMATCH against D3 result "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.rank != source.rank:
            raise WeightCarrierSchemaError(
                "IltizamGateResult must not promote rank beyond D3 "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.source_result.state is TadammunGateState.BLOCKED and (
            self.state is not IltizamGateState.BLOCKED
        ):
            raise WeightCarrierSchemaError(
                "IltizamGateResult must preserve blocked Tadammun state "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.source_result.state is TadammunGateState.DEFERRED and (
            self.state is IltizamGateState.PROVEN
        ):
            raise WeightCarrierSchemaError(
                "IltizamGateResult must not prove over deferred Tadammun "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not self.residuals[: len(source.residuals)] == source.residuals:
            raise WeightCarrierSchemaError(
                "IltizamGateResult must preserve D3 residuals "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


@dataclass(frozen=True, slots=True)
class DalalahMatrixResidualAuditResult:
    """Bounded LAFZI-D5 output for residual visibility audit only."""

    state: DalalahMatrixResidualAuditState
    source_result: IltizamGateResult
    iltizam_gate_result_ref: str
    tadammun_gate_result_ref: str
    mutabaqah_gate_result_ref: str
    coupled_dalalah_surface_ref: str
    wadi_madlul_closed_ref: str
    lafzi_madlul_closed_ref: str
    madlul_boundary_ref: str
    included_surface: tuple[str, ...]
    excluded_surface: tuple[str, ...]
    claimed_internal_part_ref: str
    claimed_external_lazim_ref: str
    luzum_evidence_ref: str
    domain_ref: str
    scope_ref: str
    residuals: tuple[CoupledDalalahResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["DALALAH_MATRIX_RESIDUAL_AUDIT_RESULT"] = (
        "DALALAH_MATRIX_RESIDUAL_AUDIT_RESULT"
    )
    forbidden_outputs: tuple[str, ...] = LAFZI_D5_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, DalalahMatrixResidualAuditState):
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult.state must be "
                "DalalahMatrixResidualAuditState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.source_result, IltizamGateResult):
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult requires IltizamGateResult "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.iltizam_gate_result_ref,
            "DalalahMatrixResidualAuditResult.iltizam_gate_result_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.tadammun_gate_result_ref,
            "DalalahMatrixResidualAuditResult.tadammun_gate_result_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.mutabaqah_gate_result_ref,
            "DalalahMatrixResidualAuditResult.mutabaqah_gate_result_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.coupled_dalalah_surface_ref,
            "DalalahMatrixResidualAuditResult.coupled_dalalah_surface_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.wadi_madlul_closed_ref,
            "DalalahMatrixResidualAuditResult.wadi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "DalalahMatrixResidualAuditResult.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.madlul_boundary_ref,
            "DalalahMatrixResidualAuditResult.madlul_boundary_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.included_surface,
            "DalalahMatrixResidualAuditResult.included_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_string_tuple(
            self.excluded_surface,
            "DalalahMatrixResidualAuditResult.excluded_surface",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_surface_disjoint(
            self.included_surface,
            self.excluded_surface,
            "DalalahMatrixResidualAuditResult",
        )
        _require_non_empty(
            self.claimed_internal_part_ref,
            "DalalahMatrixResidualAuditResult.claimed_internal_part_ref",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _require_non_empty(
            self.claimed_external_lazim_ref,
            "DalalahMatrixResidualAuditResult.claimed_external_lazim_ref",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _require_non_empty(
            self.luzum_evidence_ref,
            "DalalahMatrixResidualAuditResult.luzum_evidence_ref",
            FailureCode.REQUIRED_SLOT_EMPTY,
        )
        _require_non_empty(
            self.domain_ref,
            "DalalahMatrixResidualAuditResult.domain_ref",
            FailureCode.DOMAIN_MISSING,
        )
        _require_non_empty(
            self.scope_ref,
            "DalalahMatrixResidualAuditResult.scope_ref",
            FailureCode.SCOPE_MISSING,
        )
        _validate_coupled_residuals(self.residuals, "DalalahMatrixResidualAuditResult")
        _validate_rank(self.rank, "DalalahMatrixResidualAuditResult")
        _require_non_empty(
            self.trace_ref,
            "DalalahMatrixResidualAuditResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != LAFZI_D5_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult.output must stay inside LAFZI-D5 "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(
            self.forbidden_outputs,
            "DalalahMatrixResidualAuditResult",
            LAFZI_D5_FORBIDDEN_OUTPUTS,
        )

        d4 = self.source_result
        d3 = d4.source_result
        if not isinstance(d3, TadammunGateResult):
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult requires valid D3 ancestry "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        d2 = d3.source_result
        if not isinstance(d2, MutabaqahGateResult):
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult requires valid D2 ancestry "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        d1 = d2.source_surface
        if not isinstance(d1, CoupledDalalahSurface):
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult requires valid D1 ancestry "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if (
            self.iltizam_gate_result_ref != d4.trace_ref
            or self.tadammun_gate_result_ref != d3.trace_ref
            or self.mutabaqah_gate_result_ref != d2.trace_ref
            or self.coupled_dalalah_surface_ref != d1.trace_ref
            or self.wadi_madlul_closed_ref != d4.wadi_madlul_closed_ref
            or self.lafzi_madlul_closed_ref != d4.lafzi_madlul_closed_ref
            or self.madlul_boundary_ref != d4.madlul_boundary_ref
            or self.included_surface != d4.included_surface
            or self.excluded_surface != d4.excluded_surface
            or self.claimed_internal_part_ref != d3.claimed_internal_part_ref
            or self.claimed_external_lazim_ref != d4.claimed_external_lazim_ref
            or self.luzum_evidence_ref != d4.luzum_evidence_ref
            or self.scope_ref != d4.scope_ref
        ):
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult must preserve D1-D4 identity "
                "and boundary "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.domain_ref != d4.domain_ref:
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult DOMAIN_MISMATCH against D4 result "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.rank != d4.rank:
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult must not promote rank beyond D4 "
                f"({FailureCode.RANK_PROMOTION_WITHOUT_GATE.value})"
            )
        if self.residuals != d4.residuals:
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult must preserve D4 residual ancestry "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if d4.state is IltizamGateState.BLOCKED and (
            self.state is not DalalahMatrixResidualAuditState.BLOCKED
        ):
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult must preserve blocked D4 state "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if d4.state is IltizamGateState.DEFERRED and (
            self.state is DalalahMatrixResidualAuditState.PROVEN
        ):
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult must not prove over deferred D4 "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.residuals and self.state is DalalahMatrixResidualAuditState.PROVEN:
            raise WeightCarrierSchemaError(
                "DalalahMatrixResidualAuditResult cannot clear visible residuals "
                f"({FailureCode.GATE_REQUIRED.value})"
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


def prove_tadammun_gate(
    mutabaqah_result: MutabaqahGateResult,
    *,
    claimed_internal_part_ref: str,
    trace_ref: str,
) -> TadammunGateResult:
    """Run LAFZI-D3 TadammunGate without opening Iltizam or matrix closure."""

    if not isinstance(mutabaqah_result, MutabaqahGateResult):
        raise WeightCarrierSchemaError(
            "prove_tadammun_gate requires MutabaqahGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_tadammun_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )

    residuals = mutabaqah_result.residuals
    if not isinstance(claimed_internal_part_ref, str):
        raise WeightCarrierSchemaError(
            "prove_tadammun_gate.claimed_internal_part_ref must be a string "
            f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
        )
    claimed_part = claimed_internal_part_ref.strip()
    if not claimed_part:
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.INTERNAL_PART_REQUIRED,
            trace_ref=trace_ref,
        )
        claimed_part = "UNPROVEN_INTERNAL_PART"
    elif claimed_part not in mutabaqah_result.included_surface:
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.PART_OUTSIDE_MADLUL,
            trace_ref=trace_ref,
            detail=claimed_part,
            blocking=True,
        )
    if any(residual.visibility != "VISIBLE" for residual in residuals):
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.HIDDEN_DALALAH_MATRIX_RESIDUAL,
            trace_ref=trace_ref,
            blocking=True,
        )

    if mutabaqah_result.state is MutabaqahGateState.BLOCKED or any(
        residual.blocking for residual in residuals
    ):
        state = TadammunGateState.BLOCKED
    elif mutabaqah_result.state is MutabaqahGateState.DEFERRED or any(
        residual.kind
        in {
            CoupledDalalahResidualKind.MADLUL_BOUNDARY_REQUIRED,
            CoupledDalalahResidualKind.MUTABAQAH_REQUIRED,
            CoupledDalalahResidualKind.INTERNAL_PART_REQUIRED,
            CoupledDalalahResidualKind.DOMAIN_MISMATCH,
            CoupledDalalahResidualKind.HIDDEN_DALALAH_MATRIX_RESIDUAL,
        }
        for residual in residuals
    ):
        state = TadammunGateState.DEFERRED
    else:
        state = TadammunGateState.PROVEN

    return TadammunGateResult(
        state=state,
        source_result=mutabaqah_result,
        mutabaqah_gate_result_ref=mutabaqah_result.trace_ref,
        wadi_madlul_closed_ref=mutabaqah_result.wadi_madlul_closed_ref,
        lafzi_madlul_closed_ref=mutabaqah_result.lafzi_madlul_closed_ref,
        madlul_boundary_ref=mutabaqah_result.madlul_boundary_ref,
        included_surface=mutabaqah_result.included_surface,
        excluded_surface=mutabaqah_result.excluded_surface,
        claimed_internal_part_ref=claimed_part,
        domain_ref=mutabaqah_result.domain_ref,
        scope_ref=mutabaqah_result.scope_ref,
        residuals=residuals,
        rank=mutabaqah_result.rank,
        trace_ref=trace_ref,
    )


def prove_iltizam_gate(
    tadammun_result: TadammunGateResult,
    *,
    claimed_external_lazim_ref: str,
    luzum_evidence_ref: str,
    trace_ref: str,
) -> IltizamGateResult:
    """Run LAFZI-D4 IltizamGate without opening matrix closure or downstream outputs."""

    if not isinstance(tadammun_result, TadammunGateResult):
        raise WeightCarrierSchemaError(
            "prove_iltizam_gate requires TadammunGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_iltizam_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )

    residuals = tadammun_result.residuals
    if not isinstance(claimed_external_lazim_ref, str):
        raise WeightCarrierSchemaError(
            "prove_iltizam_gate.claimed_external_lazim_ref must be a string "
            f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
        )
    if not isinstance(luzum_evidence_ref, str):
        raise WeightCarrierSchemaError(
            "prove_iltizam_gate.luzum_evidence_ref must be a string "
            f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
        )
    claimed_lazim = claimed_external_lazim_ref.strip()
    evidence_ref = luzum_evidence_ref.strip()
    if not claimed_lazim:
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.LAZIM_OUTSIDE_REQUIRED,
            trace_ref=trace_ref,
        )
        claimed_lazim = "UNPROVEN_EXTERNAL_LAZIM"
    elif claimed_lazim in tadammun_result.included_surface:
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.LAZIM_OUTSIDE_REQUIRED,
            trace_ref=trace_ref,
            detail=claimed_lazim,
            blocking=True,
        )
    if not evidence_ref:
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.LUZUM_EVIDENCE_REQUIRED,
            trace_ref=trace_ref,
        )
        evidence_ref = "UNPROVEN_LUZUM_EVIDENCE"
    elif evidence_ref.startswith(("association://", "mere-association://")):
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.MERE_ASSOCIATION_NOT_LUZUM,
            trace_ref=trace_ref,
            detail=evidence_ref,
            blocking=True,
        )
    if any(residual.visibility != "VISIBLE" for residual in residuals):
        residuals = _append_residual_once(
            residuals,
            kind=CoupledDalalahResidualKind.HIDDEN_DALALAH_MATRIX_RESIDUAL,
            trace_ref=trace_ref,
            blocking=True,
        )

    if tadammun_result.state is TadammunGateState.BLOCKED or any(
        residual.blocking for residual in residuals
    ):
        state = IltizamGateState.BLOCKED
    elif tadammun_result.state is TadammunGateState.DEFERRED or any(
        residual.kind
        in {
            CoupledDalalahResidualKind.MADLUL_BOUNDARY_REQUIRED,
            CoupledDalalahResidualKind.MUTABAQAH_REQUIRED,
            CoupledDalalahResidualKind.INTERNAL_PART_REQUIRED,
            CoupledDalalahResidualKind.LAZIM_OUTSIDE_REQUIRED,
            CoupledDalalahResidualKind.LUZUM_EVIDENCE_REQUIRED,
            CoupledDalalahResidualKind.DOMAIN_MISMATCH,
            CoupledDalalahResidualKind.HIDDEN_DALALAH_MATRIX_RESIDUAL,
        }
        for residual in residuals
    ):
        state = IltizamGateState.DEFERRED
    else:
        state = IltizamGateState.PROVEN

    return IltizamGateResult(
        state=state,
        source_result=tadammun_result,
        tadammun_gate_result_ref=tadammun_result.trace_ref,
        wadi_madlul_closed_ref=tadammun_result.wadi_madlul_closed_ref,
        lafzi_madlul_closed_ref=tadammun_result.lafzi_madlul_closed_ref,
        madlul_boundary_ref=tadammun_result.madlul_boundary_ref,
        included_surface=tadammun_result.included_surface,
        excluded_surface=tadammun_result.excluded_surface,
        claimed_external_lazim_ref=claimed_lazim,
        luzum_evidence_ref=evidence_ref,
        domain_ref=tadammun_result.domain_ref,
        scope_ref=tadammun_result.scope_ref,
        residuals=residuals,
        rank=tadammun_result.rank,
        trace_ref=trace_ref,
    )


def prove_dalalah_matrix_residual_audit(
    iltizam_result: IltizamGateResult,
    *,
    trace_ref: str,
) -> DalalahMatrixResidualAuditResult:
    """Run LAFZI-D5, auditing residual visibility without matrix closure."""

    if not isinstance(iltizam_result, IltizamGateResult):
        raise WeightCarrierSchemaError(
            "prove_dalalah_matrix_residual_audit requires IltizamGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_dalalah_matrix_residual_audit.trace_ref",
        FailureCode.TRACE_MISSING,
    )

    residuals = iltizam_result.residuals
    if (
        any(residual.visibility != "VISIBLE" for residual in residuals)
        or iltizam_result.state is IltizamGateState.BLOCKED
        or any(residual.blocking for residual in residuals)
    ):
        state = DalalahMatrixResidualAuditState.BLOCKED
    elif iltizam_result.state is IltizamGateState.DEFERRED or residuals:
        state = DalalahMatrixResidualAuditState.DEFERRED
    else:
        state = DalalahMatrixResidualAuditState.PROVEN

    tadammun_result = iltizam_result.source_result
    mutabaqah_result = tadammun_result.source_result
    surface = mutabaqah_result.source_surface

    return DalalahMatrixResidualAuditResult(
        state=state,
        source_result=iltizam_result,
        iltizam_gate_result_ref=iltizam_result.trace_ref,
        tadammun_gate_result_ref=tadammun_result.trace_ref,
        mutabaqah_gate_result_ref=mutabaqah_result.trace_ref,
        coupled_dalalah_surface_ref=surface.trace_ref,
        wadi_madlul_closed_ref=iltizam_result.wadi_madlul_closed_ref,
        lafzi_madlul_closed_ref=iltizam_result.lafzi_madlul_closed_ref,
        madlul_boundary_ref=iltizam_result.madlul_boundary_ref,
        included_surface=iltizam_result.included_surface,
        excluded_surface=iltizam_result.excluded_surface,
        claimed_internal_part_ref=tadammun_result.claimed_internal_part_ref,
        claimed_external_lazim_ref=iltizam_result.claimed_external_lazim_ref,
        luzum_evidence_ref=iltizam_result.luzum_evidence_ref,
        domain_ref=iltizam_result.domain_ref,
        scope_ref=iltizam_result.scope_ref,
        residuals=residuals,
        rank=iltizam_result.rank,
        trace_ref=trace_ref,
    )


__all__ = [
    "CoupledDalalahResidual",
    "CoupledDalalahResidualKind",
    "CoupledDalalahSurface",
    "D1C8HandoffCard",
    "DalalahMatrixResidualAuditResult",
    "DalalahMatrixResidualAuditState",
    "LAFZI_D1_ALLOWED_OUTPUT",
    "LAFZI_D1_FORBIDDEN_OUTPUTS",
    "LAFZI_D1_RANK_CEILING",
    "LAFZI_D1_RESIDUAL_VOCABULARY",
    "LAFZI_D2_ALLOWED_OUTPUT",
    "LAFZI_D2_FORBIDDEN_OUTPUTS",
    "LAFZI_D2_RANK_CEILING",
    "LAFZI_D3_ALLOWED_OUTPUT",
    "LAFZI_D3_FORBIDDEN_OUTPUTS",
    "LAFZI_D3_RANK_CEILING",
    "LAFZI_D4_ALLOWED_OUTPUT",
    "LAFZI_D4_FORBIDDEN_OUTPUTS",
    "LAFZI_D4_RANK_CEILING",
    "LAFZI_D5_ALLOWED_OUTPUT",
    "LAFZI_D5_FORBIDDEN_OUTPUTS",
    "LAFZI_D5_RANK_CEILING",
    "IltizamGateResult",
    "IltizamGateState",
    "MutabaqahGateResult",
    "MutabaqahGateState",
    "TadammunGateResult",
    "TadammunGateState",
    "prove_dalalah_matrix_residual_audit",
    "prove_iltizam_gate",
    "prove_mutabaqah_gate",
    "prove_tadammun_gate",
]
