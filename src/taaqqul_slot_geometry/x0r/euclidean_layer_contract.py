"""X0R-E1 generic Euclidean layer-contract carriers (carrier-only surface)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EuclideanLayerContractSchemaError(TypeError):
    """Raised when X0R-E1 carriers are malformed."""


class LayerQuestionKind(StrEnum):
    """The fixed LAW-E0 eight-question vocabulary."""

    CONDITION_OF_POSSIBILITY = "CONDITION_OF_POSSIBILITY"
    MINIMUM_COMPLETE_LIMIT = "MINIMUM_COMPLETE_LIMIT"
    OPENING = "OPENING"
    DEMAND = "DEMAND"
    IDENTITY_PRESERVATION = "IDENTITY_PRESERVATION"
    CLOSURE = "CLOSURE"
    RESIDUAL = "RESIDUAL"
    LICENSED_TRANSITION = "LICENSED_TRANSITION"


class LayerClosureStatus(StrEnum):
    """Carrier-level closure labels (never a verdict engine)."""

    NOT_OPENED = "NOT_OPENED"
    BOUNDED = "BOUNDED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class LayerReadinessState(StrEnum):
    """Carrier-level readiness labels for downstream staging."""

    LINK_READY = "LINK_READY"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class LayerQuestionSet:
    """Ordered LAW-E0 question-set carrier."""

    domain: str
    trace_ref: str
    questions: tuple[LayerQuestionKind, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_tuple(cls, "questions", self.questions)
        if not self.questions:
            raise EuclideanLayerContractSchemaError(f"{cls}.questions must not be empty")
        for question in self.questions:
            if not isinstance(question, LayerQuestionKind):
                raise EuclideanLayerContractSchemaError(
                    f"{cls}.questions entries must be LayerQuestionKind members"
                )


@dataclass(frozen=True, slots=True)
class LayerResidual:
    """Local residual carrier for X0R-E1."""

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
class LayerClosureSurface:
    """Layer closure surface carrier (label-only)."""

    layer_name: str
    status: LayerClosureStatus
    trace_ref: str
    residual_visible: bool

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "layer_name", self.layer_name)
        if not isinstance(self.status, LayerClosureStatus):
            raise EuclideanLayerContractSchemaError(f"{cls}.status must be LayerClosureStatus")
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_bool(cls, "residual_visible", self.residual_visible)


@dataclass(frozen=True, slots=True)
class LayerTransitionReadiness:
    """Transition-readiness carrier (no gate execution)."""

    source_layer: str
    target_layer: str
    readiness: LayerReadinessState
    trace_ref: str
    residual_visible: bool

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "source_layer", self.source_layer)
        _require_str(cls, "target_layer", self.target_layer)
        if not isinstance(self.readiness, LayerReadinessState):
            raise EuclideanLayerContractSchemaError(
                f"{cls}.readiness must be LayerReadinessState"
            )
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_bool(cls, "residual_visible", self.residual_visible)


@dataclass(frozen=True, slots=True)
class EuclideanLayerContract:
    """Generic Euclidean layer-contract carrier bundle."""

    domain: str
    scope: str
    trace_ref: str
    question_set: LayerQuestionSet
    closure_surface: LayerClosureSurface
    transition_readiness: LayerTransitionReadiness
    residuals: tuple[LayerResidual, ...] = ()

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "scope", self.scope)
        _require_str(cls, "trace_ref", self.trace_ref)
        if not isinstance(self.question_set, LayerQuestionSet):
            raise EuclideanLayerContractSchemaError(f"{cls}.question_set must be LayerQuestionSet")
        if not isinstance(self.closure_surface, LayerClosureSurface):
            raise EuclideanLayerContractSchemaError(
                f"{cls}.closure_surface must be LayerClosureSurface"
            )
        if not isinstance(self.transition_readiness, LayerTransitionReadiness):
            raise EuclideanLayerContractSchemaError(
                f"{cls}.transition_readiness must be LayerTransitionReadiness"
            )
        _require_tuple(cls, "residuals", self.residuals)
        for residual in self.residuals:
            if not isinstance(residual, LayerResidual):
                raise EuclideanLayerContractSchemaError(
                    f"{cls}.residuals entries must be LayerResidual"
                )

        if self.question_set.domain != self.domain:
            raise EuclideanLayerContractSchemaError(
                f"{cls}.question_set.domain must match {cls}.domain"
            )
        for field_name, value in (
            ("question_set.trace_ref", self.question_set.trace_ref),
            ("closure_surface.trace_ref", self.closure_surface.trace_ref),
            ("transition_readiness.trace_ref", self.transition_readiness.trace_ref),
        ):
            if value != self.trace_ref:
                raise EuclideanLayerContractSchemaError(
                    f"{cls}.{field_name} must match {cls}.trace_ref"
                )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EuclideanLayerContractSchemaError(
            f"{cls_name}.{field_name} must be a non-empty string"
        )


def _require_bool(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, bool):
        raise EuclideanLayerContractSchemaError(f"{cls_name}.{field_name} must be bool")


def _require_tuple(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise EuclideanLayerContractSchemaError(f"{cls_name}.{field_name} must be tuple")
