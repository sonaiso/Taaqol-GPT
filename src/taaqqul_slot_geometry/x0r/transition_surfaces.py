"""PR-141 transition carrier surfaces (carrier-only, schema-safe strings only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class TransitionSurfaceSchemaError(TypeError):
    """Raised when PR-141 transition carrier surfaces are malformed."""


class ConstitutionalForgeryError(TransitionSurfaceSchemaError):
    """Raised when approved transition context is forged outside guardian flow."""


class GuardianDecisionStatus(StrEnum):
    """Decision statuses for PR-141 guardian carrier surface."""

    APPROVED = "APPROVED"
    APPROVED_WITH_RESIDUALS = "APPROVED_WITH_RESIDUALS"
    SUSPENDED = "SUSPENDED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class TransitionProposal:
    """Carrier-only transition proposal from executor to guardian."""

    proposal_id: str
    source_layer: str
    target_layer: str
    input_identity: str
    operation_id: str
    candidate_output: str
    preserved_invariants: tuple[str, ...]
    changed_properties: tuple[str, ...]
    evidence: tuple[str, ...]
    residuals: tuple[str, ...]
    trace_id: str
    claimed_rank: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "proposal_id", self.proposal_id)
        _require_str(cls, "source_layer", self.source_layer)
        _require_str(cls, "target_layer", self.target_layer)
        _require_str(cls, "input_identity", self.input_identity)
        _require_str(cls, "operation_id", self.operation_id)
        _require_str(cls, "candidate_output", self.candidate_output)
        _require_tuple(cls, "preserved_invariants", self.preserved_invariants)
        _require_tuple(cls, "changed_properties", self.changed_properties)
        _require_tuple(cls, "evidence", self.evidence)
        _require_tuple(cls, "residuals", self.residuals)
        _require_str(cls, "trace_id", self.trace_id)
        _require_str(cls, "claimed_rank", self.claimed_rank)
        for entry in self.preserved_invariants:
            _require_str(cls, "preserved_invariants entry", entry)
        for entry in self.changed_properties:
            _require_str(cls, "changed_properties entry", entry)
        for entry in self.evidence:
            _require_str(cls, "evidence entry", entry)
        for entry in self.residuals:
            _require_str(cls, "residuals entry", entry)


@dataclass(frozen=True, slots=True)
class GuardianDecision:
    """Carrier-only guardian decision over a transition proposal."""

    decision_id: str
    proposal_id: str
    status: GuardianDecisionStatus
    approved_rank: str | None
    nonblocking_residuals: tuple[str, ...]
    failure_codes: tuple[str, ...]
    trace_reference: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "decision_id", self.decision_id)
        _require_str(cls, "proposal_id", self.proposal_id)
        if not isinstance(self.status, GuardianDecisionStatus):
            raise TransitionSurfaceSchemaError(
                f"{cls}.status must be GuardianDecisionStatus"
            )
        if self.approved_rank is not None:
            _require_str(cls, "approved_rank", self.approved_rank)
        _require_tuple(cls, "nonblocking_residuals", self.nonblocking_residuals)
        _require_tuple(cls, "failure_codes", self.failure_codes)
        for residual in self.nonblocking_residuals:
            _require_str(cls, "nonblocking_residuals entry", residual)
        for code in self.failure_codes:
            _require_str(cls, "failure_codes entry", code)
        _require_str(cls, "trace_reference", self.trace_reference)

        approved_state = self.status in {
            GuardianDecisionStatus.APPROVED,
            GuardianDecisionStatus.APPROVED_WITH_RESIDUALS,
        }
        if approved_state and self.approved_rank is None:
            raise TransitionSurfaceSchemaError(
                f"{cls} approved statuses require approved_rank"
            )
        if approved_state and self.failure_codes:
            raise TransitionSurfaceSchemaError(
                f"{cls} approved statuses cannot carry failure_codes"
            )
        if self.status is GuardianDecisionStatus.REJECTED and not self.failure_codes:
            raise TransitionSurfaceSchemaError(
                f"{cls}.REJECTED requires at least one failure code"
            )
        if self.status is GuardianDecisionStatus.REJECTED and self.approved_rank is not None:
            raise TransitionSurfaceSchemaError(
                f"{cls}.REJECTED cannot carry approved_rank"
            )


@dataclass(frozen=True, slots=True)
class ApprovedTransitionContext:
    """Carrier-only approved transition context passed to handoff layers."""

    decision_id: str
    source_layer: str
    target_layer: str
    input_identity: str
    output_identity: str
    approved_operation: str
    approved_rank: str
    preserved_invariants: tuple[str, ...]
    nonblocking_residuals: tuple[str, ...]
    trace_id: str
    _approval_token: object = field(repr=False, compare=False, hash=False, kw_only=True)

    @classmethod
    def from_guardian(
        cls,
        *,
        decision: GuardianDecision,
        proposal: TransitionProposal,
        output_identity: str,
    ) -> ApprovedTransitionContext:
        if decision.proposal_id != proposal.proposal_id:
            raise TransitionSurfaceSchemaError(
                "ApprovedTransitionContext proposal mismatch between decision and proposal"
            )
        if decision.trace_reference != proposal.trace_id:
            raise TransitionSurfaceSchemaError(
                "ApprovedTransitionContext trace mismatch between decision and proposal"
            )
        approved_state = decision.status in {
            GuardianDecisionStatus.APPROVED,
            GuardianDecisionStatus.APPROVED_WITH_RESIDUALS,
        }
        if not approved_state:
            raise TransitionSurfaceSchemaError(
                "ApprovedTransitionContext requires approved guardian decision status"
            )
        if decision.approved_rank is None:
            raise TransitionSurfaceSchemaError(
                "ApprovedTransitionContext requires guardian approved_rank"
            )
        return cls(
            decision_id=decision.decision_id,
            source_layer=proposal.source_layer,
            target_layer=proposal.target_layer,
            input_identity=proposal.input_identity,
            output_identity=output_identity,
            approved_operation=proposal.operation_id,
            approved_rank=decision.approved_rank,
            preserved_invariants=proposal.preserved_invariants,
            nonblocking_residuals=decision.nonblocking_residuals,
            trace_id=proposal.trace_id,
            _approval_token=_APPROVED_CONTEXT_TOKEN,
        )

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if self._approval_token is not _APPROVED_CONTEXT_TOKEN:
            raise ConstitutionalForgeryError(
                f"{cls} must be constructed via {cls}.from_guardian"
            )
        _require_str(cls, "decision_id", self.decision_id)
        _require_str(cls, "source_layer", self.source_layer)
        _require_str(cls, "target_layer", self.target_layer)
        _require_str(cls, "input_identity", self.input_identity)
        _require_str(cls, "output_identity", self.output_identity)
        _require_str(cls, "approved_operation", self.approved_operation)
        _require_str(cls, "approved_rank", self.approved_rank)
        _require_tuple(cls, "preserved_invariants", self.preserved_invariants)
        _require_tuple(cls, "nonblocking_residuals", self.nonblocking_residuals)
        _require_str(cls, "trace_id", self.trace_id)
        for entry in self.preserved_invariants:
            _require_str(cls, "preserved_invariants entry", entry)
        for residual in self.nonblocking_residuals:
            _require_str(cls, "nonblocking_residuals entry", residual)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise TransitionSurfaceSchemaError(
            f"{cls_name}.{field_name} must be a non-empty string"
        )


def _require_tuple(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise TransitionSurfaceSchemaError(f"{cls_name}.{field_name} must be tuple")


_APPROVED_CONTEXT_TOKEN = object()


__all__ = [
    "ApprovedTransitionContext",
    "ConstitutionalForgeryError",
    "GuardianDecision",
    "GuardianDecisionStatus",
    "TransitionProposal",
    "TransitionSurfaceSchemaError",
]
