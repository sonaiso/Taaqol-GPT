"""Wad'iMadlul carrier surface — LAFZI-C1.

LAFZI-C1 binding of ``docs/60_WADI_MADLUL_CONDITION_LAW.md``.
This module introduces carrier-only surfaces and a local residual vocabulary
for the wadʿī condition layer opened by LAFZI-C0.

Constitutional invariants (docs/60):

* carriers only: no gates, operations, verdicts, or closure functions;
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
        if self.status_kind is TransferOrMajazKind.MANQUL:
            for field_name in (
                "original_wad_ref",
                "transfer_cause",
                "new_usage_scope",
                "preserved_trace_ref",
                "qadih_difference",
            ):
                _require_non_empty(
                    getattr(self, field_name),
                    f"TransferOrMajazStatus.{field_name}",
                    FailureCode.BOUNDARY_MISSING,
                )
        if self.status_kind is TransferOrMajazKind.MAJAZI:
            for field_name in (
                "original_haqiqah_ref",
                "relation_ref",
                "qarinah_ref",
                "literal_preventer_ref",
            ):
                _require_non_empty(
                    getattr(self, field_name),
                    f"TransferOrMajazStatus.{field_name}",
                    FailureCode.BOUNDARY_MISSING,
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


__all__ = [
    "WADI_C1_FORBIDDEN_OUTPUTS",
    "WADI_C1_RANK_CEILING",
    "WADI_C1_RESIDUAL_VOCABULARY",
    "MeaningIdentity",
    "MeaningIdentityKind",
    "TransferOrMajazKind",
    "TransferOrMajazStatus",
    "UsageScope",
    "UsageScopeKind",
    "WadAuthority",
    "WadAuthorityFamily",
    "WadKind",
    "WadiMadlulContract",
    "WadiResidual",
    "WadiResidualKind",
]
