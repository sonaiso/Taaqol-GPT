"""PR-X0R runtime contract hooks (no linguistic runtime inference).

This module binds the minimal executable contract surface deferred by PR-X0:

* ``JumpTestInput``
* ``JumpTestResult``
* ``ResidualKind`` (minimal vocabulary)
* ``TransitionContract``

The surface is intentionally generic and domain-relative. It does not parse
language, detect roots, detect weights, infer meaning, or classify particles.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode


class JumpTestContractError(TypeError):
    """Raised when the runtime contract is constructed with malformed types."""


class ResidualKind(StrEnum):
    """Minimal residual vocabulary declared by PR-X0."""

    BLOCKING = "BLOCKING"
    DEFERRED = "DEFERRED"
    REPAIRABLE = "REPAIRABLE"
    NON_BLOCKING = "NON_BLOCKING"
    CONTRADICTORY = "CONTRADICTORY"


@dataclass(frozen=True, slots=True)
class JumpTestInput:
    """Input surface for a single transition jump test."""

    source_level: str
    target_level: str
    transition_name: str
    domain: str
    trace_ref: str
    sufficiency: bool
    necessity: bool
    preserved_trace: bool
    qadih_difference: bool
    residual_kinds: tuple[ResidualKind, ...]
    blocking_residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "source_level", self.source_level)
        _require_str(cls, "target_level", self.target_level)
        _require_str(cls, "transition_name", self.transition_name)
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_bool(cls, "sufficiency", self.sufficiency)
        _require_bool(cls, "necessity", self.necessity)
        _require_bool(cls, "preserved_trace", self.preserved_trace)
        _require_bool(cls, "qadih_difference", self.qadih_difference)
        _require_tuple(cls, "residual_kinds", self.residual_kinds)
        for kind in self.residual_kinds:
            if not isinstance(kind, ResidualKind):
                raise JumpTestContractError(
                    f"{cls}.residual_kinds entries must be ResidualKind members"
                )
        _require_tuple(cls, "blocking_residuals", self.blocking_residuals)
        for name in self.blocking_residuals:
            _require_str(cls, "blocking_residuals entry", name)


@dataclass(frozen=True, slots=True)
class JumpTestResult:
    """Result surface for a transition jump test."""

    allowed: bool
    failure_code: FailureCode | None
    domain: str
    trace_ref: str
    transition_name: str
    source_level: str
    target_level: str
    residual_policy: str
    residual_kinds: tuple[ResidualKind, ...]
    blocking_residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_bool(cls, "allowed", self.allowed)
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise JumpTestContractError(f"{cls}.failure_code must be a FailureCode member or None")
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_str(cls, "transition_name", self.transition_name)
        _require_str(cls, "source_level", self.source_level)
        _require_str(cls, "target_level", self.target_level)
        _require_str(cls, "residual_policy", self.residual_policy)
        _require_tuple(cls, "residual_kinds", self.residual_kinds)
        for kind in self.residual_kinds:
            if not isinstance(kind, ResidualKind):
                raise JumpTestContractError(
                    f"{cls}.residual_kinds entries must be ResidualKind members"
                )
        _require_tuple(cls, "blocking_residuals", self.blocking_residuals)
        for name in self.blocking_residuals:
            _require_str(cls, "blocking_residuals entry", name)
        if self.allowed and self.failure_code is not None:
            raise JumpTestContractError(
                f"{cls} cannot be allowed=True while carrying a failure_code"
            )
        if (not self.allowed) and self.failure_code is None:
            raise JumpTestContractError(
                f"{cls} cannot be allowed=False without a named failure_code"
            )


@dataclass(frozen=True, slots=True)
class TransitionContract:
    """Declared transition matrix + jump-test gate (PR-X0R)."""

    declared_transitions: frozenset[tuple[str, str, str, str]]
    residual_policy: str = "VISIBLE_TYPED_MINIMAL_VOCAB"

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.declared_transitions, frozenset):
            raise JumpTestContractError(f"{cls}.declared_transitions must be a frozenset")
        for row in self.declared_transitions:
            if not isinstance(row, tuple) or len(row) != 4:
                raise JumpTestContractError(
                    f"{cls}.declared_transitions entries must be 4-tuples"
                )
            source, target, transition_name, domain = row
            _require_str(cls, "declared transition source_level", source)
            _require_str(cls, "declared transition target_level", target)
            _require_str(cls, "declared transition transition_name", transition_name)
            _require_str(cls, "declared transition domain", domain)
        _require_str(cls, "residual_policy", self.residual_policy)

    def evaluate(self, jump: JumpTestInput) -> JumpTestResult:
        """Evaluate one jump according to PR-X0 / PR-X0R contract discipline."""

        if not jump.domain.strip():
            return self._refuse(jump, FailureCode.DOMAIN_MISSING)
        if not jump.trace_ref.strip():
            return self._refuse(jump, FailureCode.TRACE_MISSING)

        key = (jump.source_level, jump.target_level, jump.transition_name, jump.domain)
        if key not in self.declared_transitions:
            return self._refuse(jump, FailureCode.FORBIDDEN_STRAIGHT_LINE)

        if jump.blocking_residuals or any(
            kind in {ResidualKind.BLOCKING, ResidualKind.CONTRADICTORY}
            for kind in jump.residual_kinds
        ):
            return self._refuse(jump, FailureCode.BLOCKING_RESIDUAL_PRESENT)

        if not all(
            (
                jump.sufficiency,
                jump.necessity,
                jump.preserved_trace,
                jump.qadih_difference,
            )
        ):
            return self._refuse(jump, FailureCode.FORBIDDEN_STRAIGHT_LINE)

        return JumpTestResult(
            allowed=True,
            failure_code=None,
            domain=jump.domain,
            trace_ref=jump.trace_ref,
            transition_name=jump.transition_name,
            source_level=jump.source_level,
            target_level=jump.target_level,
            residual_policy=self.residual_policy,
            residual_kinds=jump.residual_kinds,
            blocking_residuals=jump.blocking_residuals,
        )

    def _refuse(self, jump: JumpTestInput, code: FailureCode) -> JumpTestResult:
        return JumpTestResult(
            allowed=False,
            failure_code=code,
            domain=jump.domain,
            trace_ref=jump.trace_ref,
            transition_name=jump.transition_name,
            source_level=jump.source_level,
            target_level=jump.target_level,
            residual_policy=self.residual_policy,
            residual_kinds=jump.residual_kinds,
            blocking_residuals=jump.blocking_residuals,
        )


def _require_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str):
        raise JumpTestContractError(f"{cls_name}.{field} must be a string")


def _require_bool(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, bool):
        raise JumpTestContractError(f"{cls_name}.{field} must be a bool")


def _require_tuple(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise JumpTestContractError(f"{cls_name}.{field} must be a tuple")


__all__ = [
    "JumpTestContractError",
    "JumpTestInput",
    "JumpTestResult",
    "ResidualKind",
    "TransitionContract",
]
