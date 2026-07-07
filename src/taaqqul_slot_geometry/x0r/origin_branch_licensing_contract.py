"""X0R-E2 generic origin-branch licensing carriers (carrier-only surface)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class OriginBranchLicensingContractSchemaError(TypeError):
    """Raised when X0R-E2 carriers are malformed."""


class OriginBranchReadinessState(StrEnum):
    """Readiness labels for origin/branch licensing carriers."""

    LINK_READY = "LINK_READY"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class OriginBranchResidual:
    """Local residual carrier for X0R-E2."""

    name: str
    detail: str
    visible: bool = True
    blocking: bool = False

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "name", self.name)
        _require_str(cls, "detail", self.detail)
        _require_bool(cls, "visible", self.visible)
        _require_bool(cls, "blocking", self.blocking)


@dataclass(frozen=True, slots=True)
class OriginBranchLinkSurface:
    """Carrier for LAW-E0 origin→branch return-link requirements."""

    asl_identification: str
    far_identification: str
    shared_feature: str
    differentiating_feature: str
    common_illah: str
    effective_description: str
    linking_sabab: str
    preserved_condition: str
    absent_preventer: str
    absent_qadih_difference: str
    preserved_identity: bool
    trace_ref: str
    rank_ceiling: int
    residual_visible: bool

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "asl_identification", self.asl_identification)
        _require_str(cls, "far_identification", self.far_identification)
        _require_str(cls, "shared_feature", self.shared_feature)
        _require_str(cls, "differentiating_feature", self.differentiating_feature)
        _require_str(cls, "common_illah", self.common_illah)
        _require_str(cls, "effective_description", self.effective_description)
        _require_str(cls, "linking_sabab", self.linking_sabab)
        _require_str(cls, "preserved_condition", self.preserved_condition)
        _require_str(cls, "absent_preventer", self.absent_preventer)
        _require_str(cls, "absent_qadih_difference", self.absent_qadih_difference)
        _require_bool(cls, "preserved_identity", self.preserved_identity)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_int(cls, "rank_ceiling", self.rank_ceiling)
        _require_bool(cls, "residual_visible", self.residual_visible)


@dataclass(frozen=True, slots=True)
class OriginBranchLicensingContract:
    """Generic carrier-only contract for X0R-E2 origin/branch licensing."""

    domain: str
    scope: str
    trace_ref: str
    link_surface: OriginBranchLinkSurface
    readiness: OriginBranchReadinessState
    residuals: tuple[OriginBranchResidual, ...] = ()

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "scope", self.scope)
        _require_str(cls, "trace_ref", self.trace_ref)
        if not isinstance(self.link_surface, OriginBranchLinkSurface):
            raise OriginBranchLicensingContractSchemaError(
                f"{cls}.link_surface must be OriginBranchLinkSurface"
            )
        if not isinstance(self.readiness, OriginBranchReadinessState):
            raise OriginBranchLicensingContractSchemaError(
                f"{cls}.readiness must be OriginBranchReadinessState"
            )
        _require_tuple(cls, "residuals", self.residuals)
        for residual in self.residuals:
            if not isinstance(residual, OriginBranchResidual):
                raise OriginBranchLicensingContractSchemaError(
                    f"{cls}.residuals entries must be OriginBranchResidual"
                )

        if self.link_surface.trace_ref != self.trace_ref:
            raise OriginBranchLicensingContractSchemaError(
                f"{cls}.link_surface.trace_ref must match {cls}.trace_ref"
            )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise OriginBranchLicensingContractSchemaError(
            f"{cls_name}.{field_name} must be a non-empty string"
        )


def _require_bool(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, bool):
        raise OriginBranchLicensingContractSchemaError(f"{cls_name}.{field_name} must be bool")


def _require_int(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, int):
        raise OriginBranchLicensingContractSchemaError(f"{cls_name}.{field_name} must be int")


def _require_tuple(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise OriginBranchLicensingContractSchemaError(f"{cls_name}.{field_name} must be tuple")
