"""Wad'iMadlul carrier surface and wadʿī gates through LAFZI-C6.

LAFZI-C1 binding of ``docs/60_WADI_MADLUL_CONDITION_LAW.md``.
This module introduces carrier-only surfaces, a local residual vocabulary,
and the first separately staged wadʿī condition gate opened by LAFZI-C0.

Constitutional invariants (docs/60):

* LAFZI-C1 carriers remain carrier-only;
* LAFZI-C2 checks WadKind only and emits no closure function;
* LAFZI-C3 checks WadAuthority only and emits no closure function;
* LAFZI-C4 checks UsageScope only and emits no closure function;
* LAFZI-C5 checks MeaningIdentity only and emits no closure function;
* LAFZI-C6 checks TransferMajaz only and emits no closure function;
* no ``Wad'iMadlulClosed`` runtime verdict;
* no CoupledDalalah, Mutabaqah, Tadammun, Iltizam, Ifadah, Hukm, Tanzil,
  or Reality output;
* residual names are local and do not expand global ``FailureCode``;
* all carrier surfaces preserve visible residuals, rank, and trace.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError

WADI_C1_RANK_CEILING: Rank = Rank.CANDIDATE
WADI_C2_RANK_CEILING: Rank = Rank.CANDIDATE
WADI_C2_ALLOWED_OUTPUT: str = "WAD_KIND_GATE_RESULT"
WADI_C3_RANK_CEILING: Rank = Rank.CANDIDATE
WADI_C3_ALLOWED_OUTPUT: str = "WAD_AUTHORITY_GATE_RESULT"
WADI_C4_RANK_CEILING: Rank = Rank.CANDIDATE
WADI_C4_ALLOWED_OUTPUT: str = "USAGE_SCOPE_GATE_RESULT"
WADI_C5_RANK_CEILING: Rank = Rank.CANDIDATE
WADI_C5_ALLOWED_OUTPUT: str = "MEANING_IDENTITY_GATE_RESULT"
WADI_C6_RANK_CEILING: Rank = Rank.CANDIDATE
WADI_C6_ALLOWED_OUTPUT: str = "TRANSFER_MAJAZ_GATE_RESULT"

WADI_C1_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "LAFZI_MADLUL_CLOSED_REQUIRED",
    "WAD_KIND_REQUIRED",
    "WAD_AUTHORITY_REQUIRED",
    "USAGE_SCOPE_REQUIRED",
    "MEANING_IDENTITY_REQUIRED",
    "TRANSFER_ORIGIN_REQUIRED",
    "TRANSFER_CAUSE_REQUIRED",
    "MAJAZ_HAQIQAH_REQUIRED",
    "MAJAZ_RELATION_REQUIRED",
    "MAJAZ_QARINAH_REQUIRED",
    "MAJAZ_LITERAL_PREVENTER_REQUIRED",
    "MULTIPLE_WADI_CANDIDATES",
    "HIDDEN_WADI_RESIDUAL",
    "FORBIDDEN_WADI_CLOSURE_JUMP",
    "FORBIDDEN_COUPLED_DALALAH_JUMP",
    "FORBIDDEN_MUTABAQA_JUMP",
    "FORBIDDEN_TADAMMUN_JUMP",
    "FORBIDDEN_ILTIZAM_JUMP",
    "FORBIDDEN_IFADAH_JUMP",
    "FORBIDDEN_HUKM_JUMP",
)

WADI_C1_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "WADI_MADLUL_CLOSED",
    "COUPLED_DALALAH",
    "MUTABAQAH",
    "TADAMMUN",
    "ILTIZAM",
    "IFADAH",
    "HUKM",
    "TANZIL",
    "REALITY",
    "ONTOLOGY",
)


class WadiResidualKind(StrEnum):
    """Local LAFZI-C1 residual names from docs/60 §6."""

    LAFZI_MADLUL_CLOSED_REQUIRED = "LAFZI_MADLUL_CLOSED_REQUIRED"
    WAD_KIND_REQUIRED = "WAD_KIND_REQUIRED"
    WAD_AUTHORITY_REQUIRED = "WAD_AUTHORITY_REQUIRED"
    USAGE_SCOPE_REQUIRED = "USAGE_SCOPE_REQUIRED"
    MEANING_IDENTITY_REQUIRED = "MEANING_IDENTITY_REQUIRED"
    TRANSFER_ORIGIN_REQUIRED = "TRANSFER_ORIGIN_REQUIRED"
    TRANSFER_CAUSE_REQUIRED = "TRANSFER_CAUSE_REQUIRED"
    MAJAZ_HAQIQAH_REQUIRED = "MAJAZ_HAQIQAH_REQUIRED"
    MAJAZ_RELATION_REQUIRED = "MAJAZ_RELATION_REQUIRED"
    MAJAZ_QARINAH_REQUIRED = "MAJAZ_QARINAH_REQUIRED"
    MAJAZ_LITERAL_PREVENTER_REQUIRED = "MAJAZ_LITERAL_PREVENTER_REQUIRED"
    MULTIPLE_WADI_CANDIDATES = "MULTIPLE_WADI_CANDIDATES"
    HIDDEN_WADI_RESIDUAL = "HIDDEN_WADI_RESIDUAL"
    FORBIDDEN_WADI_CLOSURE_JUMP = "FORBIDDEN_WADI_CLOSURE_JUMP"
    FORBIDDEN_COUPLED_DALALAH_JUMP = "FORBIDDEN_COUPLED_DALALAH_JUMP"
    FORBIDDEN_MUTABAQA_JUMP = "FORBIDDEN_MUTABAQA_JUMP"
    FORBIDDEN_TADAMMUN_JUMP = "FORBIDDEN_TADAMMUN_JUMP"
    FORBIDDEN_ILTIZAM_JUMP = "FORBIDDEN_ILTIZAM_JUMP"
    FORBIDDEN_IFADAH_JUMP = "FORBIDDEN_IFADAH_JUMP"
    FORBIDDEN_HUKM_JUMP = "FORBIDDEN_HUKM_JUMP"


class WadKind(StrEnum):
    """WadKind labels licensed by docs/60 §5.2."""

    LUGHAWI = "LUGHAWI"
    URFI = "URFI"
    ISTILAHI = "ISTILAHI"
    MANQUL = "MANQUL"
    MAJAZI = "MAJAZI"
    DEFERRED = "DEFERRED"


class WadKindGateState(StrEnum):
    """LAFZI-C2 WadKindGate state; not Wad'iMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class WadAuthorityGateState(StrEnum):
    """LAFZI-C3 WadAuthorityGate state; not Wad'iMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class UsageScopeGateState(StrEnum):
    """LAFZI-C4 UsageScopeGate state; not Wad'iMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class MeaningIdentityGateState(StrEnum):
    """LAFZI-C5 MeaningIdentityGate state; not Wad'iMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class TransferMajazGateState(StrEnum):
    """LAFZI-C6 TransferMajazGate state; not Wad'iMadlulClosed."""

    PROVEN = "PROVEN"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class WadAuthorityFamily(StrEnum):
    """Visible authority families for a wadʿī condition carrier."""

    LUGHAWI = "LUGHAWI"
    URFI = "URFI"
    ISTILAHI = "ISTILAHI"
    MANQUL = "MANQUL"
    MAJAZI = "MAJAZI"
    DEFERRED = "DEFERRED"


class UsageScopeKind(StrEnum):
    """Bounded usage-scope families; not a semantic relation verdict."""

    LANGUAGE = "LANGUAGE"
    CUSTOMARY = "CUSTOMARY"
    TECHNICAL = "TECHNICAL"
    TRANSFERRED = "TRANSFERRED"
    FIGURATIVE = "FIGURATIVE"
    DEFERRED = "DEFERRED"


class MeaningIdentityKind(StrEnum):
    """Structural identity kinds from docs/60 §5.5."""

    ENTITY = "ENTITY"
    TRANSFORMATION = "TRANSFORMATION"
    ATTRIBUTE = "ATTRIBUTE"
    RELATION_OPERATOR = "RELATION_OPERATOR"
    REFERENCE_SPACE = "REFERENCE_SPACE"
    DEFERRED = "DEFERRED"


class TransferOrMajazKind(StrEnum):
    """Transfer/majaz status labels; not a closure verdict."""

    DIRECT = "DIRECT"
    MANQUL = "MANQUL"
    MAJAZI = "MAJAZI"
    DEFERRED = "DEFERRED"


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
    if rank > WADI_C1_RANK_CEILING:
        raise WeightCarrierSchemaError(
            f"{owner}.rank must not exceed CANDIDATE "
            f"({FailureCode.RANK_EXCEEDS_CEILING.value})"
        )


def _validate_residuals(residuals: tuple[WadiResidual, ...], owner: str) -> None:
    if not isinstance(residuals, tuple):
        raise WeightCarrierSchemaError(
            f"{owner}.residuals must be a tuple ({FailureCode.HIDDEN_RESIDUAL.value})"
        )
    for residual in residuals:
        if not isinstance(residual, WadiResidual):
            raise WeightCarrierSchemaError(
                f"{owner}.residuals entries must be WadiResidual "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    if not isinstance(forbidden_outputs, tuple):
        raise WeightCarrierSchemaError(
            f"{owner}.forbidden_outputs must be a tuple "
            f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
        )
    for output in forbidden_outputs:
        _require_non_empty(
            output,
            f"{owner}.forbidden_outputs entry",
            FailureCode.OUTPUT_EXCEEDS_LAYER,
        )


def _append_residual_once(
    residuals: tuple[WadiResidual, ...],
    *,
    kind: WadiResidualKind,
    trace_ref: str,
) -> tuple[WadiResidual, ...]:
    if any(residual.kind is kind for residual in residuals):
        return residuals
    return residuals + (WadiResidual(kind=kind, trace_ref=trace_ref),)


def _merge_residuals(
    *residual_groups: tuple[WadiResidual, ...],
) -> tuple[WadiResidual, ...]:
    merged: tuple[WadiResidual, ...] = ()
    for residual_group in residual_groups:
        for residual in residual_group:
            if residual not in merged:
                merged += (residual,)
    return merged


@dataclass(frozen=True, slots=True)
class WadiResidual:
    """Visible local wadʿī residual; not a global FailureCode."""

    kind: WadiResidualKind
    trace_ref: str
    visibility: Literal["VISIBLE"] = "VISIBLE"
    blocking: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.kind, WadiResidualKind):
            raise WeightCarrierSchemaError(
                "WadiResidual.kind must be a local WadiResidualKind "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if self.visibility != "VISIBLE":
            raise WeightCarrierSchemaError(
                "WadiResidual.visibility must be VISIBLE "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        if not isinstance(self.blocking, bool):
            raise WeightCarrierSchemaError(
                "WadiResidual.blocking must be a bool "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        _require_non_empty(self.trace_ref, "WadiResidual.trace_ref", FailureCode.TRACE_MISSING)


@dataclass(frozen=True, slots=True)
class WadAuthority:
    """Visible wadʿ authority surface; not a proof gate."""

    family: WadAuthorityFamily
    authority_ref: str
    evidence_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.family, WadAuthorityFamily):
            raise WeightCarrierSchemaError(
                "WadAuthority.family must be a WadAuthorityFamily "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_non_empty(
            self.authority_ref,
            "WadAuthority.authority_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(
            self.evidence_ref,
            "WadAuthority.evidence_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(self.trace_ref, "WadAuthority.trace_ref", FailureCode.TRACE_MISSING)


@dataclass(frozen=True, slots=True)
class UsageScope:
    """Bounded usage scope for wadʿī condition carriers."""

    scope_kind: UsageScopeKind
    domain_ref: str
    boundary_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.scope_kind, UsageScopeKind):
            raise WeightCarrierSchemaError(
                "UsageScope.scope_kind must be a UsageScopeKind "
                f"({FailureCode.SCOPE_MISSING.value})"
            )
        _require_non_empty(self.domain_ref, "UsageScope.domain_ref", FailureCode.DOMAIN_MISSING)
        _require_non_empty(self.boundary_ref, "UsageScope.boundary_ref", FailureCode.SCOPE_MISSING)
        _require_non_empty(self.trace_ref, "UsageScope.trace_ref", FailureCode.TRACE_MISSING)


@dataclass(frozen=True, slots=True)
class MeaningIdentity:
    """Structural identity boundary for a placed meaning candidate."""

    identity_kind: MeaningIdentityKind
    boundary: str
    included_surface: tuple[str, ...]
    excluded_surface: tuple[str, ...]
    residuals: tuple[WadiResidual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.identity_kind, MeaningIdentityKind):
            raise WeightCarrierSchemaError(
                "MeaningIdentity.identity_kind must be a MeaningIdentityKind "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        _require_non_empty(self.boundary, "MeaningIdentity.boundary", FailureCode.BOUNDARY_MISSING)
        for field_name, values in (
            ("included_surface", self.included_surface),
            ("excluded_surface", self.excluded_surface),
        ):
            if not isinstance(values, tuple):
                raise WeightCarrierSchemaError(
                    f"MeaningIdentity.{field_name} must be a tuple "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
            for value in values:
                _require_non_empty(
                    value,
                    f"MeaningIdentity.{field_name} entry",
                    FailureCode.BOUNDARY_MISSING,
                )
        _validate_residuals(self.residuals, "MeaningIdentity")
        _require_non_empty(self.trace_ref, "MeaningIdentity.trace_ref", FailureCode.TRACE_MISSING)


@dataclass(frozen=True, slots=True)
class TransferOrMajazStatus:
    """Transfer/majaz carrier surface; not an executable TransferMajazGate."""

    status_kind: TransferOrMajazKind
    original_wad_ref: str = ""
    transfer_cause: str = ""
    new_usage_scope: str = ""
    preserved_trace_ref: str = ""
    qadih_difference: str = ""
    original_haqiqah_ref: str = ""
    relation_ref: str = ""
    qarinah_ref: str = ""
    literal_preventer_ref: str = ""
    residuals: tuple[WadiResidual, ...] = ()
    trace_ref: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.status_kind, TransferOrMajazKind):
            raise WeightCarrierSchemaError(
                "TransferOrMajazStatus.status_kind must be a TransferOrMajazKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for field_name in (
            "original_wad_ref",
            "transfer_cause",
            "new_usage_scope",
            "preserved_trace_ref",
            "qadih_difference",
            "original_haqiqah_ref",
            "relation_ref",
            "qarinah_ref",
            "literal_preventer_ref",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise WeightCarrierSchemaError(
                    f"TransferOrMajazStatus.{field_name} must be a string "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        _validate_residuals(self.residuals, "TransferOrMajazStatus")
        _require_non_empty(
            self.trace_ref,
            "TransferOrMajazStatus.trace_ref",
            FailureCode.TRACE_MISSING,
        )


@dataclass(frozen=True, slots=True)
class WadiMadlulContract:
    """LAFZI-C1 wadʿī condition contract carrier; not Wad'iMadlulClosed."""

    lafzi_madlul_closed_ref: str
    wad_kind: WadKind
    wad_authority: WadAuthority
    usage_scope: UsageScope
    meaning_identity: MeaningIdentity
    transfer_or_majaz_status: TransferOrMajazStatus
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    identity: str
    domain_id: Literal["WADI_MADLUL"] = "WADI_MADLUL"
    scope: str = "WADI_CONDITION"
    forbidden_outputs: tuple[str, ...] = WADI_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.lafzi_madlul_closed_ref,
            "WadiMadlulContract.lafzi_madlul_closed_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.wad_kind, WadKind):
            raise WeightCarrierSchemaError(
                "WadiMadlulContract.wad_kind must be a WadKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.wad_authority, WadAuthority):
            raise WeightCarrierSchemaError(
                "WadiMadlulContract.wad_authority must be WadAuthority "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        if not isinstance(self.usage_scope, UsageScope):
            raise WeightCarrierSchemaError(
                "WadiMadlulContract.usage_scope must be UsageScope "
                f"({FailureCode.SCOPE_MISSING.value})"
            )
        if not isinstance(self.meaning_identity, MeaningIdentity):
            raise WeightCarrierSchemaError(
                "WadiMadlulContract.meaning_identity must be MeaningIdentity "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.transfer_or_majaz_status, TransferOrMajazStatus):
            raise WeightCarrierSchemaError(
                "WadiMadlulContract.transfer_or_majaz_status must be "
                f"TransferOrMajazStatus ({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_residuals(self.residuals, "WadiMadlulContract")
        _validate_rank(self.rank, "WadiMadlulContract")
        _require_non_empty(
            self.trace_ref,
            "WadiMadlulContract.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.identity,
            "WadiMadlulContract.identity",
            FailureCode.IDENTITY_BROKEN,
        )
        if self.domain_id != "WADI_MADLUL":
            raise WeightCarrierSchemaError(
                "WadiMadlulContract.domain_id must be WADI_MADLUL "
                f"({FailureCode.DOMAIN_MISSING.value})"
            )
        _require_non_empty(self.scope, "WadiMadlulContract.scope", FailureCode.SCOPE_MISSING)
        _validate_forbidden_outputs(self.forbidden_outputs, "WadiMadlulContract")


@dataclass(frozen=True, slots=True)
class WadKindGateResult:
    """Bounded LAFZI-C2 output for W1 WadKindGate only."""

    state: WadKindGateState
    contract_ref: str
    wad_kind: WadKind
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["WAD_KIND_GATE_RESULT"] = "WAD_KIND_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = WADI_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, WadKindGateState):
            raise WeightCarrierSchemaError(
                "WadKindGateResult.state must be a WadKindGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.contract_ref,
            "WadKindGateResult.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.wad_kind, WadKind):
            raise WeightCarrierSchemaError(
                "WadKindGateResult.wad_kind must be a WadKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _validate_residuals(self.residuals, "WadKindGateResult")
        _validate_rank(self.rank, "WadKindGateResult")
        _require_non_empty(
            self.trace_ref,
            "WadKindGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != WADI_C2_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "WadKindGateResult.output must stay inside WadKindGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "WadKindGateResult")


@dataclass(frozen=True, slots=True)
class WadAuthorityGateResult:
    """Bounded LAFZI-C3 output for W2 WadAuthorityGate only."""

    state: WadAuthorityGateState
    contract_ref: str
    authority_family: WadAuthorityFamily
    authority_ref: str
    evidence_ref: str
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["WAD_AUTHORITY_GATE_RESULT"] = "WAD_AUTHORITY_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = WADI_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, WadAuthorityGateState):
            raise WeightCarrierSchemaError(
                "WadAuthorityGateResult.state must be a WadAuthorityGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.contract_ref,
            "WadAuthorityGateResult.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.authority_family, WadAuthorityFamily):
            raise WeightCarrierSchemaError(
                "WadAuthorityGateResult.authority_family must be a WadAuthorityFamily "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        _require_non_empty(
            self.authority_ref,
            "WadAuthorityGateResult.authority_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _require_non_empty(
            self.evidence_ref,
            "WadAuthorityGateResult.evidence_ref",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_residuals(self.residuals, "WadAuthorityGateResult")
        _validate_rank(self.rank, "WadAuthorityGateResult")
        _require_non_empty(
            self.trace_ref,
            "WadAuthorityGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != WADI_C3_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "WadAuthorityGateResult.output must stay inside WadAuthorityGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "WadAuthorityGateResult")


@dataclass(frozen=True, slots=True)
class UsageScopeGateResult:
    """Bounded LAFZI-C4 output for W3 UsageScopeGate only."""

    state: UsageScopeGateState
    contract_ref: str
    scope_kind: UsageScopeKind
    domain_ref: str
    boundary_ref: str
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["USAGE_SCOPE_GATE_RESULT"] = "USAGE_SCOPE_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = WADI_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, UsageScopeGateState):
            raise WeightCarrierSchemaError(
                "UsageScopeGateResult.state must be a UsageScopeGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.contract_ref,
            "UsageScopeGateResult.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.scope_kind, UsageScopeKind):
            raise WeightCarrierSchemaError(
                "UsageScopeGateResult.scope_kind must be a UsageScopeKind "
                f"({FailureCode.SCOPE_MISSING.value})"
            )
        _require_non_empty(
            self.domain_ref,
            "UsageScopeGateResult.domain_ref",
            FailureCode.DOMAIN_MISSING,
        )
        _require_non_empty(
            self.boundary_ref,
            "UsageScopeGateResult.boundary_ref",
            FailureCode.SCOPE_MISSING,
        )
        _validate_residuals(self.residuals, "UsageScopeGateResult")
        _validate_rank(self.rank, "UsageScopeGateResult")
        _require_non_empty(
            self.trace_ref,
            "UsageScopeGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != WADI_C4_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "UsageScopeGateResult.output must stay inside UsageScopeGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "UsageScopeGateResult")


@dataclass(frozen=True, slots=True)
class MeaningIdentityGateResult:
    """Bounded LAFZI-C5 output for W4 MeaningIdentityGate only."""

    state: MeaningIdentityGateState
    contract_ref: str
    identity_kind: MeaningIdentityKind
    boundary: str
    included_surface: tuple[str, ...]
    excluded_surface: tuple[str, ...]
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["MEANING_IDENTITY_GATE_RESULT"] = "MEANING_IDENTITY_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = WADI_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, MeaningIdentityGateState):
            raise WeightCarrierSchemaError(
                "MeaningIdentityGateResult.state must be a MeaningIdentityGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.contract_ref,
            "MeaningIdentityGateResult.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.identity_kind, MeaningIdentityKind):
            raise WeightCarrierSchemaError(
                "MeaningIdentityGateResult.identity_kind must be a MeaningIdentityKind "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        _require_non_empty(
            self.boundary,
            "MeaningIdentityGateResult.boundary",
            FailureCode.BOUNDARY_MISSING,
        )
        for field_name, values in (
            ("included_surface", self.included_surface),
            ("excluded_surface", self.excluded_surface),
        ):
            if not isinstance(values, tuple):
                raise WeightCarrierSchemaError(
                    f"MeaningIdentityGateResult.{field_name} must be a tuple "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
            for value in values:
                _require_non_empty(
                    value,
                    f"MeaningIdentityGateResult.{field_name} entry",
                    FailureCode.BOUNDARY_MISSING,
                )
        _validate_residuals(self.residuals, "MeaningIdentityGateResult")
        _validate_rank(self.rank, "MeaningIdentityGateResult")
        _require_non_empty(
            self.trace_ref,
            "MeaningIdentityGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != WADI_C5_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "MeaningIdentityGateResult.output must stay inside MeaningIdentityGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "MeaningIdentityGateResult")


@dataclass(frozen=True, slots=True)
class TransferMajazGateResult:
    """Bounded LAFZI-C6 output for TransferMajazGate only."""

    state: TransferMajazGateState
    contract_ref: str
    status_kind: TransferOrMajazKind
    original_wad_ref: str
    transfer_cause: str
    new_usage_scope: str
    preserved_trace_ref: str
    qadih_difference: str
    original_haqiqah_ref: str
    relation_ref: str
    qarinah_ref: str
    literal_preventer_ref: str
    residuals: tuple[WadiResidual, ...]
    rank: Rank
    trace_ref: str
    output: Literal["TRANSFER_MAJAZ_GATE_RESULT"] = "TRANSFER_MAJAZ_GATE_RESULT"
    forbidden_outputs: tuple[str, ...] = WADI_C1_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        if not isinstance(self.state, TransferMajazGateState):
            raise WeightCarrierSchemaError(
                "TransferMajazGateResult.state must be a TransferMajazGateState "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        _require_non_empty(
            self.contract_ref,
            "TransferMajazGateResult.contract_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.status_kind, TransferOrMajazKind):
            raise WeightCarrierSchemaError(
                "TransferMajazGateResult.status_kind must be a TransferOrMajazKind "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )
        for field_name in (
            "original_wad_ref",
            "transfer_cause",
            "new_usage_scope",
            "preserved_trace_ref",
            "qadih_difference",
            "original_haqiqah_ref",
            "relation_ref",
            "qarinah_ref",
            "literal_preventer_ref",
        ):
            if not isinstance(getattr(self, field_name), str):
                raise WeightCarrierSchemaError(
                    f"TransferMajazGateResult.{field_name} must be a string "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )
        _validate_residuals(self.residuals, "TransferMajazGateResult")
        _validate_rank(self.rank, "TransferMajazGateResult")
        _require_non_empty(
            self.trace_ref,
            "TransferMajazGateResult.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        if self.output != WADI_C6_ALLOWED_OUTPUT:
            raise WeightCarrierSchemaError(
                "TransferMajazGateResult.output must stay inside TransferMajazGate "
                f"({FailureCode.OUTPUT_EXCEEDS_LAYER.value})"
            )
        _validate_forbidden_outputs(self.forbidden_outputs, "TransferMajazGateResult")


def prove_wad_kind_gate(
    contract: WadiMadlulContract,
    *,
    trace_ref: str,
) -> WadKindGateResult:
    """Run LAFZI-C2 W1 WadKindGate without crossing into W2 or closure."""

    if not isinstance(contract, WadiMadlulContract):
        raise WeightCarrierSchemaError(
            "prove_wad_kind_gate requires WadiMadlulContract "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(trace_ref, "prove_wad_kind_gate.trace_ref", FailureCode.TRACE_MISSING)

    residuals = contract.residuals
    if any(residual.blocking for residual in residuals):
        state = WadKindGateState.BLOCKED
    elif contract.wad_kind is WadKind.DEFERRED:
        residuals = residuals + (
            WadiResidual(
                kind=WadiResidualKind.WAD_KIND_REQUIRED,
                trace_ref=trace_ref,
            ),
        )
        state = WadKindGateState.DEFERRED
    else:
        state = WadKindGateState.PROVEN

    return WadKindGateResult(
        state=state,
        contract_ref=contract.identity,
        wad_kind=contract.wad_kind,
        residuals=residuals,
        rank=WADI_C2_RANK_CEILING,
        trace_ref=trace_ref,
    )


def prove_wad_authority_gate(
    contract: WadiMadlulContract,
    wad_kind_result: WadKindGateResult,
    *,
    trace_ref: str,
) -> WadAuthorityGateResult:
    """Run LAFZI-C3 W2 WadAuthorityGate without crossing into W3 or closure."""

    if not isinstance(contract, WadiMadlulContract):
        raise WeightCarrierSchemaError(
            "prove_wad_authority_gate requires WadiMadlulContract "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(wad_kind_result, WadKindGateResult):
        raise WeightCarrierSchemaError(
            "prove_wad_authority_gate requires WadKindGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_wad_authority_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    if wad_kind_result.contract_ref != contract.identity:
        raise WeightCarrierSchemaError(
            "WadKindGateResult.contract_ref must preserve WadiMadlulContract.identity "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )

    residuals = contract.residuals + tuple(
        residual for residual in wad_kind_result.residuals if residual not in contract.residuals
    )
    if wad_kind_result.state is WadKindGateState.BLOCKED or any(
        residual.blocking for residual in residuals
    ):
        state = WadAuthorityGateState.BLOCKED
    elif wad_kind_result.state is WadKindGateState.DEFERRED:
        state = WadAuthorityGateState.DEFERRED
    elif contract.wad_authority.family is WadAuthorityFamily.DEFERRED:
        residuals = _append_residual_once(
            residuals,
            kind=WadiResidualKind.WAD_AUTHORITY_REQUIRED,
            trace_ref=trace_ref,
        )
        state = WadAuthorityGateState.DEFERRED
    else:
        state = WadAuthorityGateState.PROVEN

    return WadAuthorityGateResult(
        state=state,
        contract_ref=contract.identity,
        authority_family=contract.wad_authority.family,
        authority_ref=contract.wad_authority.authority_ref,
        evidence_ref=contract.wad_authority.evidence_ref,
        residuals=residuals,
        rank=WADI_C3_RANK_CEILING,
        trace_ref=trace_ref,
    )


def prove_usage_scope_gate(
    contract: WadiMadlulContract,
    wad_authority_result: WadAuthorityGateResult,
    *,
    trace_ref: str,
) -> UsageScopeGateResult:
    """Run LAFZI-C4 W3 UsageScopeGate without crossing into W4 or closure."""

    if not isinstance(contract, WadiMadlulContract):
        raise WeightCarrierSchemaError(
            "prove_usage_scope_gate requires WadiMadlulContract "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(wad_authority_result, WadAuthorityGateResult):
        raise WeightCarrierSchemaError(
            "prove_usage_scope_gate requires WadAuthorityGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_usage_scope_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    if wad_authority_result.contract_ref != contract.identity:
        raise WeightCarrierSchemaError(
            "WadAuthorityGateResult.contract_ref must preserve "
            "WadiMadlulContract.identity "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )

    residuals = contract.residuals + tuple(
        residual
        for residual in wad_authority_result.residuals
        if residual not in contract.residuals
    )
    if wad_authority_result.state is WadAuthorityGateState.BLOCKED or any(
        residual.blocking for residual in residuals
    ):
        state = UsageScopeGateState.BLOCKED
    elif wad_authority_result.state is WadAuthorityGateState.DEFERRED:
        state = UsageScopeGateState.DEFERRED
    elif contract.usage_scope.scope_kind is UsageScopeKind.DEFERRED:
        residuals = _append_residual_once(
            residuals,
            kind=WadiResidualKind.USAGE_SCOPE_REQUIRED,
            trace_ref=trace_ref,
        )
        state = UsageScopeGateState.DEFERRED
    else:
        state = UsageScopeGateState.PROVEN

    return UsageScopeGateResult(
        state=state,
        contract_ref=contract.identity,
        scope_kind=contract.usage_scope.scope_kind,
        domain_ref=contract.usage_scope.domain_ref,
        boundary_ref=contract.usage_scope.boundary_ref,
        residuals=residuals,
        rank=WADI_C4_RANK_CEILING,
        trace_ref=trace_ref,
    )


def prove_meaning_identity_gate(
    contract: WadiMadlulContract,
    usage_scope_result: UsageScopeGateResult,
    *,
    trace_ref: str,
) -> MeaningIdentityGateResult:
    """Run LAFZI-C5 W4 MeaningIdentityGate while preserving local residual sources."""

    if not isinstance(contract, WadiMadlulContract):
        raise WeightCarrierSchemaError(
            "prove_meaning_identity_gate requires WadiMadlulContract "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(usage_scope_result, UsageScopeGateResult):
        raise WeightCarrierSchemaError(
            "prove_meaning_identity_gate requires UsageScopeGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_meaning_identity_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    if usage_scope_result.contract_ref != contract.identity:
        raise WeightCarrierSchemaError(
            "UsageScopeGateResult.contract_ref must preserve "
            "WadiMadlulContract.identity "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )

    residuals = _merge_residuals(
        contract.residuals,
        usage_scope_result.residuals,
        contract.meaning_identity.residuals,
    )
    if usage_scope_result.state is UsageScopeGateState.BLOCKED or any(
        residual.blocking for residual in residuals
    ):
        state = MeaningIdentityGateState.BLOCKED
    elif usage_scope_result.state is UsageScopeGateState.DEFERRED:
        state = MeaningIdentityGateState.DEFERRED
    elif contract.meaning_identity.identity_kind is MeaningIdentityKind.DEFERRED:
        residuals = _append_residual_once(
            residuals,
            kind=WadiResidualKind.MEANING_IDENTITY_REQUIRED,
            trace_ref=trace_ref,
        )
        state = MeaningIdentityGateState.DEFERRED
    else:
        state = MeaningIdentityGateState.PROVEN

    return MeaningIdentityGateResult(
        state=state,
        contract_ref=contract.identity,
        identity_kind=contract.meaning_identity.identity_kind,
        boundary=contract.meaning_identity.boundary,
        included_surface=contract.meaning_identity.included_surface,
        excluded_surface=contract.meaning_identity.excluded_surface,
        residuals=residuals,
        rank=WADI_C5_RANK_CEILING,
        trace_ref=trace_ref,
    )


def prove_transfer_majaz_gate(
    contract: WadiMadlulContract,
    meaning_identity_result: MeaningIdentityGateResult,
    *,
    trace_ref: str,
) -> TransferMajazGateResult:
    """Run LAFZI-C6 TransferMajazGate without crossing into closure or C7."""

    if not isinstance(contract, WadiMadlulContract):
        raise WeightCarrierSchemaError(
            "prove_transfer_majaz_gate requires WadiMadlulContract "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(meaning_identity_result, MeaningIdentityGateResult):
        raise WeightCarrierSchemaError(
            "prove_transfer_majaz_gate requires MeaningIdentityGateResult "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    _require_non_empty(
        trace_ref,
        "prove_transfer_majaz_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    if meaning_identity_result.output != WADI_C5_ALLOWED_OUTPUT:
        raise WeightCarrierSchemaError(
            "prove_transfer_majaz_gate prior result must be C5 "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if meaning_identity_result.contract_ref != contract.identity:
        raise WeightCarrierSchemaError(
            "MeaningIdentityGateResult.contract_ref must preserve "
            "WadiMadlulContract.identity "
            f"({FailureCode.IDENTITY_BROKEN.value})"
        )

    status = contract.transfer_or_majaz_status
    residuals = _merge_residuals(
        contract.residuals,
        meaning_identity_result.residuals,
        contract.meaning_identity.residuals,
        status.residuals,
    )

    if status.status_kind is TransferOrMajazKind.MANQUL:
        for field_name, residual_kind in (
            ("original_wad_ref", WadiResidualKind.TRANSFER_ORIGIN_REQUIRED),
            ("transfer_cause", WadiResidualKind.TRANSFER_CAUSE_REQUIRED),
            ("new_usage_scope", WadiResidualKind.TRANSFER_ORIGIN_REQUIRED),
            ("preserved_trace_ref", WadiResidualKind.TRANSFER_ORIGIN_REQUIRED),
            ("qadih_difference", WadiResidualKind.TRANSFER_ORIGIN_REQUIRED),
        ):
            if not getattr(status, field_name).strip():
                residuals = _append_residual_once(
                    residuals,
                    kind=residual_kind,
                    trace_ref=trace_ref,
                )
    elif status.status_kind is TransferOrMajazKind.MAJAZI:
        for field_name, residual_kind in (
            ("original_haqiqah_ref", WadiResidualKind.MAJAZ_HAQIQAH_REQUIRED),
            ("relation_ref", WadiResidualKind.MAJAZ_RELATION_REQUIRED),
            ("qarinah_ref", WadiResidualKind.MAJAZ_QARINAH_REQUIRED),
            ("literal_preventer_ref", WadiResidualKind.MAJAZ_LITERAL_PREVENTER_REQUIRED),
        ):
            if not getattr(status, field_name).strip():
                residuals = _append_residual_once(
                    residuals,
                    kind=residual_kind,
                    trace_ref=trace_ref,
                )
    elif status.status_kind is TransferOrMajazKind.DEFERRED:
        residuals = _append_residual_once(
            residuals,
            kind=WadiResidualKind.TRANSFER_ORIGIN_REQUIRED,
            trace_ref=trace_ref,
        )

    missing_transfer_or_majaz_residual = any(
        residual.kind
        in {
            WadiResidualKind.TRANSFER_ORIGIN_REQUIRED,
            WadiResidualKind.TRANSFER_CAUSE_REQUIRED,
            WadiResidualKind.MAJAZ_HAQIQAH_REQUIRED,
            WadiResidualKind.MAJAZ_RELATION_REQUIRED,
            WadiResidualKind.MAJAZ_QARINAH_REQUIRED,
            WadiResidualKind.MAJAZ_LITERAL_PREVENTER_REQUIRED,
        }
        for residual in residuals
    )

    if meaning_identity_result.state is MeaningIdentityGateState.BLOCKED or any(
        residual.blocking for residual in residuals
    ):
        state = TransferMajazGateState.BLOCKED
    elif (
        meaning_identity_result.state is MeaningIdentityGateState.DEFERRED
        or status.status_kind is TransferOrMajazKind.DEFERRED
        or (
            status.status_kind in (TransferOrMajazKind.MANQUL, TransferOrMajazKind.MAJAZI)
            and missing_transfer_or_majaz_residual
        )
    ):
        state = TransferMajazGateState.DEFERRED
    else:
        state = TransferMajazGateState.PROVEN

    return TransferMajazGateResult(
        state=state,
        contract_ref=contract.identity,
        status_kind=status.status_kind,
        original_wad_ref=status.original_wad_ref,
        transfer_cause=status.transfer_cause,
        new_usage_scope=status.new_usage_scope,
        preserved_trace_ref=status.preserved_trace_ref,
        qadih_difference=status.qadih_difference,
        original_haqiqah_ref=status.original_haqiqah_ref,
        relation_ref=status.relation_ref,
        qarinah_ref=status.qarinah_ref,
        literal_preventer_ref=status.literal_preventer_ref,
        residuals=residuals,
        rank=WADI_C6_RANK_CEILING,
        trace_ref=trace_ref,
    )


__all__ = [
    "WADI_C1_FORBIDDEN_OUTPUTS",
    "WADI_C1_RANK_CEILING",
    "WADI_C1_RESIDUAL_VOCABULARY",
    "WADI_C2_ALLOWED_OUTPUT",
    "WADI_C2_RANK_CEILING",
    "WADI_C3_ALLOWED_OUTPUT",
    "WADI_C3_RANK_CEILING",
    "WADI_C4_ALLOWED_OUTPUT",
    "WADI_C4_RANK_CEILING",
    "WADI_C5_ALLOWED_OUTPUT",
    "WADI_C5_RANK_CEILING",
    "WADI_C6_ALLOWED_OUTPUT",
    "WADI_C6_RANK_CEILING",
    "MeaningIdentity",
    "MeaningIdentityGateResult",
    "MeaningIdentityGateState",
    "MeaningIdentityKind",
    "TransferOrMajazKind",
    "TransferOrMajazStatus",
    "TransferMajazGateResult",
    "TransferMajazGateState",
    "UsageScope",
    "UsageScopeGateResult",
    "UsageScopeGateState",
    "UsageScopeKind",
    "WadAuthority",
    "WadAuthorityFamily",
    "WadAuthorityGateResult",
    "WadAuthorityGateState",
    "WadKind",
    "WadKindGateResult",
    "WadKindGateState",
    "WadiMadlulContract",
    "WadiResidual",
    "WadiResidualKind",
    "prove_meaning_identity_gate",
    "prove_transfer_majaz_gate",
    "prove_wad_authority_gate",
    "prove_usage_scope_gate",
    "prove_wad_kind_gate",
]
