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
from typing import Literal

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode


class JumpTestContractError(TypeError):
    """Raised when the runtime contract is constructed with malformed types."""


_BLOCKING_TOKEN = "blocking"


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


@dataclass(frozen=True, slots=True)
class MinimalCompleteRequirement:
    """Minimal-complete transition law (energy-preserving guardrail).

    Origin law          : docs/14 Amendment-32 (PR-X0R)
    Branch case         : Minimal-complete Euclidean transition requirement
    Constitutional chain: docs/14 -> Amendment-32 -> Runtime contract hooks
    """

    current_stage_rank: int
    max_required_stage_rank: int
    requested_state: Literal["candidate", "deferred", "licensed"] = "candidate"
    candidate_or_deferred_sufficient: bool = True
    missing_requirements: tuple[str, ...] = ()
    rank_ceiling: int | None = None

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_int(cls, "current_stage_rank", self.current_stage_rank)
        _require_int(cls, "max_required_stage_rank", self.max_required_stage_rank)
        _require_str(cls, "requested_state", self.requested_state)
        _require_bool(
            cls,
            "candidate_or_deferred_sufficient",
            self.candidate_or_deferred_sufficient,
        )
        _require_tuple(cls, "missing_requirements", self.missing_requirements)
        for missing in self.missing_requirements:
            _require_str(cls, "missing_requirements entry", missing)
        if self.rank_ceiling is not None:
            _require_int(cls, "rank_ceiling", self.rank_ceiling)

    def is_satisfied_for_rank(self, rank: int) -> bool:
        """Check minimum-complete law without raising layer or verdict tier.

        ``rank`` is the attempted transition rank under evaluation. The check
        refuses attempted promotion beyond the current stage and refuses a
        ``licensed`` request when candidate/deferred already suffices.
        """

        # Guard 1: no promotion beyond current stage.
        if rank > self.current_stage_rank:
            return False
        # Guard 2: do not require checks from a higher stage.
        if self.max_required_stage_rank > self.current_stage_rank:
            return False
        if self.missing_requirements:
            return False
        if self.rank_ceiling is not None and rank > self.rank_ceiling:
            return False
        # Guard 3: minimal-complete law forbids over-claiming licensed state.
        return not (
            self.requested_state == "licensed" and self.candidate_or_deferred_sufficient
        )

    def closest_valid_stage(self) -> int:
        return min(self.current_stage_rank, self.max_required_stage_rank)


@dataclass(frozen=True, slots=True)
class EuclideanLearningEvidence:
    """Learning evidence carrier for transition-contract tuning (no verdict leak).

    Origin law          : docs/14 Amendment-32 (PR-X0R)
    Branch case         : Euclidean learning evidence carrier
    Constitutional chain: docs/14 -> Amendment-32 -> Runtime contract hooks
    """

    evidence_ref: str
    source: str
    observations: tuple[str, ...] = ()
    rank_hint: int | None = None

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "evidence_ref", self.evidence_ref)
        _require_str(cls, "source", self.source)
        _require_tuple(cls, "observations", self.observations)
        for observation in self.observations:
            _require_str(cls, "observations entry", observation)
        if self.rank_hint is not None:
            _require_int(cls, "rank_hint", self.rank_hint)


@dataclass(frozen=True, slots=True)
class EuclideanFailureRecord:
    """Structured failure record for refused Euclidean transitions.

    Origin law          : docs/14 Amendment-32 (PR-X0R)
    Branch case         : Euclidean transition failure surface
    Constitutional chain: docs/14 -> Amendment-32 -> Runtime contract hooks
    """

    failed_transition: bool
    missing_condition: tuple[str, ...]
    active_preventer: bool
    blocking_residual: tuple[str, ...]
    closest_valid_stage: int
    required_handoff: str
    repair_suggestion: str
    failure_code: FailureCode | None


@dataclass(frozen=True, slots=True)
class EuclideanGateDecision:
    """Gate decision carrier for Euclidean transition contract."""

    transition_allowed: bool
    failure_code: FailureCode | None
    rank: int
    residuals: tuple[str, ...]
    handoff: str


@dataclass(frozen=True, slots=True)
class RankedBranchPrediction:
    """Ranked branch expectation (prediction-only, never final judgment).

    Origin law          : docs/14 Amendment-32 (PR-X0R)
    Branch case         : Ranked branch prediction carrier
    Constitutional chain: docs/14 -> Amendment-32 -> Runtime contract hooks
    """

    predicted_branch: str
    predicted_rank: int
    residuals: tuple[str, ...]
    decision: EuclideanGateDecision
    is_final_judgment: bool = False
    predicts_next_token: bool = False


@dataclass(frozen=True, slots=True)
class EuclideanTransitionContract:
    """General Euclidean transition contract linking origin and branch.

    Origin law          : docs/14 Amendment-32 (PR-X0R)
    Branch case         : Euclidean origin↔branch transition contract
    Constitutional chain: docs/14 -> Amendment-32 -> Runtime contract hooks
    """

    origin: str
    branch: str
    preserved_identity: bool
    common_illah: str
    effective_description: str
    qadih_difference: bool
    condition: bool
    sabab: bool
    preventer: bool
    residuals: tuple[str, ...]
    rank: int
    minimal_complete_requirement: MinimalCompleteRequirement
    handoff: str
    origin_to_branch_linked: bool = True
    branch_to_origin_linked: bool = True

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "origin", self.origin)
        _require_str(cls, "branch", self.branch)
        _require_bool(cls, "preserved_identity", self.preserved_identity)
        _require_str(cls, "common_illah", self.common_illah)
        _require_str(cls, "effective_description", self.effective_description)
        _require_bool(cls, "qadih_difference", self.qadih_difference)
        _require_bool(cls, "condition", self.condition)
        _require_bool(cls, "sabab", self.sabab)
        _require_bool(cls, "preventer", self.preventer)
        _require_tuple(cls, "residuals", self.residuals)
        for residual in self.residuals:
            _require_str(cls, "residuals entry", residual)
        _require_int(cls, "rank", self.rank)
        if not isinstance(self.minimal_complete_requirement, MinimalCompleteRequirement):
            raise JumpTestContractError(
                f"{cls}.minimal_complete_requirement must be MinimalCompleteRequirement"
            )
        _require_str(cls, "handoff", self.handoff)
        _require_bool(cls, "origin_to_branch_linked", self.origin_to_branch_linked)
        _require_bool(cls, "branch_to_origin_linked", self.branch_to_origin_linked)

    def links_origin_to_branch(self) -> bool:
        return (
            bool(self.origin.strip())
            and bool(self.branch.strip())
            and self.origin_to_branch_linked
        )

    def links_branch_to_origin(self) -> bool:
        return (
            bool(self.branch.strip())
            and bool(self.origin.strip())
            and self.branch_to_origin_linked
        )

    def has_preserved_identity(self) -> bool:
        return self.preserved_identity

    def has_common_illah(self) -> bool:
        return bool(self.common_illah.strip())

    def has_effective_description(self) -> bool:
        return bool(self.effective_description.strip())

    def has_qadih_difference_check(self) -> bool:
        return self.qadih_difference

    def condition_is_satisfied(self) -> bool:
        return self.condition

    def sabab_is_active(self) -> bool:
        return self.sabab

    def preventer_is_absent(self) -> bool:
        return not self.preventer

    def minimal_complete_is_satisfied(self) -> bool:
        return self.minimal_complete_requirement.is_satisfied_for_rank(self.rank)

    def can_transition(self) -> bool:
        """Allow transition only when the full Euclidean gate law is satisfied."""

        return all(
            (
                self.has_preserved_identity(),
                self.links_origin_to_branch(),
                self.links_branch_to_origin(),
                self.has_common_illah(),
                self.has_effective_description(),
                self.has_qadih_difference_check(),
                self.condition_is_satisfied(),
                self.sabab_is_active(),
                self.preventer_is_absent(),
                not self._blocking_residuals(),
                self.minimal_complete_is_satisfied(),
                bool(self.handoff.strip()),
            )
        )

    def to_failure_record(self) -> EuclideanFailureRecord:
        missing = self._missing_conditions()
        blocking = self._blocking_residuals()
        failed = not self.can_transition()
        return EuclideanFailureRecord(
            failed_transition=failed,
            missing_condition=tuple(missing),
            active_preventer=not self.preventer_is_absent(),
            blocking_residual=tuple(blocking),
            closest_valid_stage=self.minimal_complete_requirement.closest_valid_stage(),
            required_handoff=self.handoff,
            repair_suggestion=self._repair_suggestion(missing, blocking),
            failure_code=self._failure_code(missing, blocking),
        )

    def predict_branch_ranked(self) -> RankedBranchPrediction:
        allowed = self.can_transition()
        decision = EuclideanGateDecision(
            transition_allowed=allowed,
            failure_code=self._failure_code(self._missing_conditions(), self._blocking_residuals()),
            rank=self.rank,
            residuals=self.residuals,
            handoff=self.handoff,
        )
        return RankedBranchPrediction(
            predicted_branch=self.branch,
            predicted_rank=decision.rank,
            residuals=self.residuals,
            decision=decision,
            is_final_judgment=False,
            predicts_next_token=False,
        )

    def _blocking_residuals(self) -> tuple[str, ...]:
        """Return blocking residuals.

        Expected residual shape is a visible, typed string such as
        ``"blocking:<reason>"``. The check is intentionally case-insensitive.
        """
        return tuple(
            residual for residual in self.residuals if self._is_blocking_residual(residual)
        )

    @staticmethod
    def _is_blocking_residual(residual: str) -> bool:
        return _BLOCKING_TOKEN in residual.lower()

    def _missing_conditions(self) -> list[str]:
        missing: list[str] = []
        if not self.has_preserved_identity():
            missing.append("preserved_identity")
        if not self.links_origin_to_branch():
            missing.append("origin_to_branch_link")
        if not self.links_branch_to_origin():
            missing.append("branch_to_origin_link")
        if not self.has_common_illah():
            missing.append("common_illah")
        if not self.has_effective_description():
            missing.append("effective_description")
        if not self.has_qadih_difference_check():
            missing.append("qadih_difference_check")
        if not self.condition_is_satisfied():
            missing.append("condition")
        if not self.sabab_is_active():
            missing.append("sabab")
        if not self.preventer_is_absent():
            missing.append("preventer_absence")
        if not self.minimal_complete_is_satisfied():
            missing.append("minimal_complete_requirement")
        if not self.handoff.strip():
            missing.append("handoff")
        return missing

    def _repair_suggestion(self, missing: list[str], blocking: tuple[str, ...]) -> str:
        if blocking:
            return "resolve blocking residuals before transition handoff"
        if missing:
            return f"satisfy missing requirements: {', '.join(missing)}"
        return "no repair required"

    def _failure_code(
        self,
        missing: list[str],
        blocking: tuple[str, ...],
    ) -> FailureCode | None:
        if not missing and not blocking:
            return None
        if blocking:
            return FailureCode.BLOCKING_RESIDUAL_PRESENT
        if "preserved_identity" in missing:
            return FailureCode.IDENTITY_BROKEN
        if "handoff" in missing:
            return FailureCode.GATE_REQUIRED
        if "sabab" in missing:
            return FailureCode.GATE_REQUIRED
        if "preventer_absence" in missing:
            return FailureCode.GATE_REQUIRED
        if "condition" in missing:
            return FailureCode.GATE_REQUIRED
        if "minimal_complete_requirement" in missing:
            return FailureCode.RANK_PROMOTION_WITHOUT_GATE
        return FailureCode.FORBIDDEN_STRAIGHT_LINE


def _require_int(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, int):
        raise JumpTestContractError(f"{cls_name}.{field} must be an int")


__all__ = [
    "EuclideanFailureRecord",
    "EuclideanGateDecision",
    "EuclideanLearningEvidence",
    "EuclideanTransitionContract",
    "JumpTestContractError",
    "JumpTestInput",
    "JumpTestResult",
    "MinimalCompleteRequirement",
    "RankedBranchPrediction",
    "ResidualKind",
    "TransitionContract",
]
