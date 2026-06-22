"""GPT-R5 — Origin Binding Gate.

Binding:
- docs/54 §3.4 (OriginBinding)
- docs/55 §8 (OriginBinding rules and residuals)
- docs/14 chain row GPT-R5 (bind extracted claims/implications to origins)

This module binds MantuqGPT / MafhumGPT claim surfaces to the existing
Knowledge Origin carriers. It does not run reasonableness gates, produce a
reasonableness verdict, mutate audit surfaces, or introduce a pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.gpt.knowledge_origins import (
    AttributeEventOrigin,
    BindingVerdict,
    EntityGenusOrigin,
    EvidenceOrigin,
    OriginBinding,
    OriginResidual,
    OriginResidualKind,
    ReferenceOrigin,
    RelationOperatorOrigin,
)
from taaqqul_slot_geometry.gpt.mafhum_boundary import MafhumGPT
from taaqqul_slot_geometry.gpt.mantuq_boundary import ClaimBoundary, MantuqGPT
from taaqqul_slot_geometry.x0r import TransitionContract

KnowledgeOrigin: TypeAlias = (
    EntityGenusOrigin
    | AttributeEventOrigin
    | RelationOperatorOrigin
    | ReferenceOrigin
    | EvidenceOrigin
)


class OriginBindingGateSchemaError(TypeError):
    """A GPT-R5 origin-binding gate surface was constructed incorrectly."""


class OriginBindingRequiredOriginType(StrEnum):
    """Licensed Knowledge Origin carrier requirements for GPT-R5 binding."""

    ENTITY_GENUS = "EntityGenusOrigin"
    ATTRIBUTE_EVENT = "AttributeEventOrigin"
    RELATION_OPERATOR = "RelationOperatorOrigin"
    REFERENCE = "ReferenceOrigin"
    EVIDENCE = "EvidenceOrigin"


class OriginBindingSourceKind(StrEnum):
    """Licensed GPT-R5 source surfaces."""

    MANTUQ_CLAIM = "MANTUQ_CLAIM"
    MAFHUM_CANDIDATE = "MAFHUM_CANDIDATE"


class OriginBindingGateState(StrEnum):
    """Origin binding gate state; never a reasonableness verdict."""

    BOUND = "BOUND"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


GPT_ORIGIN_BINDING_TRANSITION_CONTRACT = TransitionContract(
    declared_transitions=frozenset(
        {
            (
                "MantuqGPT",
                "OriginBindingClaim",
                "select_mantuq_claim",
                "gpt_reasonableness",
            ),
            (
                "MafhumGPT",
                "OriginBindingClaim",
                "select_mafhum_candidate",
                "gpt_reasonableness",
            ),
            (
                "OriginBindingClaim",
                "KnowledgeOrigin",
                "consult_required_origin",
                "gpt_reasonableness",
            ),
            (
                "KnowledgeOrigin",
                "OriginBinding",
                "record_origin_binding",
                "gpt_reasonableness",
            ),
            (
                "OriginBinding",
                "OriginBindingGateResult",
                "surface_origin_binding_gate",
                "gpt_reasonableness",
            ),
        }
    )
)


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise OriginBindingGateSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise OriginBindingGateSchemaError(f"{cls_name}.{field} must start with 'trace://'")


def _require_origin_residuals(value: object) -> None:
    if not isinstance(value, tuple):
        raise OriginBindingGateSchemaError("residuals must be a tuple of OriginResidual carriers")
    for residual in value:
        if not isinstance(residual, OriginResidual):
            raise OriginBindingGateSchemaError("residuals entries must be OriginResidual carriers")


@dataclass(frozen=True, slots=True)
class OriginBindingClaim:
    """A trace-bound GPT claim selected for Knowledge Origin binding."""

    claim_ref: str
    claim_trace_ref: str
    domain: str
    required_origin_type: OriginBindingRequiredOriginType
    source_kind: OriginBindingSourceKind
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "claim_ref", self.claim_ref)
        _require_trace_ref(cls, "claim_trace_ref", self.claim_trace_ref)
        _require_nonempty_str(cls, "domain", self.domain)
        if not isinstance(self.required_origin_type, OriginBindingRequiredOriginType):
            raise OriginBindingGateSchemaError(
                f"{cls}.required_origin_type must be an OriginBindingRequiredOriginType member"
            )
        if not isinstance(self.source_kind, OriginBindingSourceKind):
            raise OriginBindingGateSchemaError(
                f"{cls}.source_kind must be an OriginBindingSourceKind member"
            )
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class OriginBindingGateResult:
    """Result surface for GPT-R5 origin binding."""

    state: OriginBindingGateState
    binding: OriginBinding | None
    failure_code: FailureCode | None
    residuals: tuple[OriginResidual, ...]
    source_claim_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.state, OriginBindingGateState):
            raise OriginBindingGateSchemaError(
                f"{cls}.state must be an OriginBindingGateState member"
            )
        if self.binding is not None and not isinstance(self.binding, OriginBinding):
            raise OriginBindingGateSchemaError(f"{cls}.binding must be an OriginBinding or None")
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise OriginBindingGateSchemaError(
                f"{cls}.failure_code must be a FailureCode member or None"
            )
        _require_origin_residuals(self.residuals)
        _require_nonempty_str(cls, "source_claim_ref", self.source_claim_ref)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if self.state is OriginBindingGateState.BOUND:
            if self.binding is None:
                raise OriginBindingGateSchemaError(f"{cls}.BOUND requires an OriginBinding")
            if self.failure_code is not None:
                raise OriginBindingGateSchemaError(f"{cls}.BOUND must not carry failure_code")
        elif self.failure_code is None:
            raise OriginBindingGateSchemaError(
                f"{cls}.{self.state.value} requires a named failure_code"
            )


def claim_from_mantuq_boundary(
    mantuq: MantuqGPT,
    boundary: ClaimBoundary,
    *,
    required_origin_type: OriginBindingRequiredOriginType,
    trace_ref: str,
) -> OriginBindingClaim:
    """Select an explicit MantuqGPT claim for GPT-R5 origin binding."""

    if not isinstance(mantuq, MantuqGPT):
        raise OriginBindingGateSchemaError("mantuq must be a MantuqGPT")
    if not isinstance(boundary, ClaimBoundary):
        raise OriginBindingGateSchemaError("boundary must be a ClaimBoundary")
    if boundary not in mantuq.explicit_claims:
        raise OriginBindingGateSchemaError("boundary must belong to mantuq.explicit_claims")
    return OriginBindingClaim(
        claim_ref=boundary.claim.claim_id,
        claim_trace_ref=boundary.trace_ref,
        domain=boundary.claim.domain,
        required_origin_type=required_origin_type,
        source_kind=OriginBindingSourceKind.MANTUQ_CLAIM,
        trace_ref=trace_ref,
    )


def claim_from_mafhum(
    mafhum: MafhumGPT,
    *,
    required_origin_type: OriginBindingRequiredOriginType,
    trace_ref: str,
) -> OriginBindingClaim:
    """Select a licensed MafhumGPT candidate for GPT-R5 origin binding."""

    if not isinstance(mafhum, MafhumGPT):
        raise OriginBindingGateSchemaError("mafhum must be a MafhumGPT")
    return OriginBindingClaim(
        claim_ref=mafhum.source_claim_ref,
        claim_trace_ref=mafhum.trace_ref,
        domain=mafhum.scope_boundary.domain,
        required_origin_type=required_origin_type,
        source_kind=OriginBindingSourceKind.MAFHUM_CANDIDATE,
        trace_ref=trace_ref,
    )


def bind_origin_to_claim(
    claim: OriginBindingClaim | None,
    origin: KnowledgeOrigin | None,
    *,
    verdict: BindingVerdict | None,
    residuals: tuple[OriginResidual, ...],
    trace_ref: str,
) -> OriginBindingGateResult:
    """Bind one selected GPT claim to one required Knowledge Origin."""

    if claim is None:
        return _result(
            OriginBindingGateState.REFUSED,
            None,
            FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=residuals,
            source_claim_ref="missing-claim",
            trace_ref=trace_ref,
        )
    _require_trace_ref("OriginBindingGateResult", "trace_ref", trace_ref)
    _require_origin_residuals(residuals)

    if origin is None:
        visible_residuals = residuals or (
            OriginResidual(
                kind=OriginResidualKind.ORIGIN_ABSENT,
                description="No Knowledge Origin was available for the selected claim.",
                claim_ref=claim.claim_ref,
            ),
        )
        binding = _binding(
            claim,
            origin_type=claim.required_origin_type.value,
            origin_id="missing-origin",
            verdict=BindingVerdict.UNSUPPORTED,
            residuals=visible_residuals,
            trace_ref=trace_ref,
        )
        return _result(
            OriginBindingGateState.DEFERRED,
            binding,
            FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=visible_residuals,
            source_claim_ref=claim.claim_ref,
            trace_ref=trace_ref,
        )

    origin_type = _origin_type(origin)
    origin_residuals = _origin_residual_strings(origin)
    if claim.required_origin_type != origin_type:
        visible_residuals = residuals or (
            OriginResidual(
                kind=OriginResidualKind.BINDING_AMBIGUOUS,
                description=(
                    f"Claim requires {claim.required_origin_type.value}, "
                    f"but consulted origin is {origin_type.value}."
                ),
                claim_ref=claim.claim_ref,
            ),
        )
        binding = _binding(
            claim,
            origin_type=origin_type.value,
            origin_id=_origin_id(origin),
            verdict=BindingVerdict.UNSUPPORTED,
            residuals=visible_residuals,
            trace_ref=trace_ref,
        )
        return _result(
            OriginBindingGateState.DEFERRED,
            binding,
            FailureCode.REQUIRED_SLOT_EMPTY,
            residuals=visible_residuals,
            source_claim_ref=claim.claim_ref,
            trace_ref=trace_ref,
        )

    if claim.domain != _origin_domain(origin):
        visible_residuals = residuals or (
            OriginResidual(
                kind=OriginResidualKind.DOMAIN_MISMATCH,
                description="Claim domain does not match consulted origin domain.",
                claim_ref=claim.claim_ref,
            ),
        )
        binding = _binding(
            claim,
            origin_type=origin_type.value,
            origin_id=_origin_id(origin),
            verdict=BindingVerdict.PARTIALLY_COMPATIBLE,
            residuals=visible_residuals,
            trace_ref=trace_ref,
        )
        return _result(
            OriginBindingGateState.DEFERRED,
            binding,
            FailureCode.DOMAIN_MISSING,
            residuals=visible_residuals,
            source_claim_ref=claim.claim_ref,
            trace_ref=trace_ref,
        )

    if verdict is None:
        return _result(
            OriginBindingGateState.REFUSED,
            None,
            FailureCode.GATE_REQUIRED,
            residuals=residuals,
            source_claim_ref=claim.claim_ref,
            trace_ref=trace_ref,
        )
    if not isinstance(verdict, BindingVerdict):
        raise OriginBindingGateSchemaError("verdict must be a BindingVerdict member or None")

    if verdict is BindingVerdict.COMPATIBLE and origin_residuals and not residuals:
        return _result(
            OriginBindingGateState.REFUSED,
            None,
            FailureCode.HIDDEN_RESIDUAL,
            residuals=(
                OriginResidual(
                    kind=OriginResidualKind.BINDING_AMBIGUOUS,
                    description="Compatible binding would hide residuals declared by the origin.",
                    claim_ref=claim.claim_ref,
                ),
            ),
            source_claim_ref=claim.claim_ref,
            trace_ref=trace_ref,
        )

    visible_residuals = _visible_residuals_for_verdict(claim, verdict, residuals)
    binding = _binding(
        claim,
        origin_type=origin_type.value,
        origin_id=_origin_id(origin),
        verdict=verdict,
        residuals=visible_residuals,
        trace_ref=trace_ref,
    )
    return _result(
        _state_for_verdict(verdict),
        binding,
        _failure_for_verdict(verdict),
        residuals=visible_residuals,
        source_claim_ref=claim.claim_ref,
        trace_ref=trace_ref,
    )


def _visible_residuals_for_verdict(
    claim: OriginBindingClaim,
    verdict: BindingVerdict,
    residuals: tuple[OriginResidual, ...],
) -> tuple[OriginResidual, ...]:
    if residuals:
        return residuals
    if verdict is BindingVerdict.CONTRADICTED:
        return (
            OriginResidual(
                kind=OriginResidualKind.EVIDENCE_CONTRADICTED,
                description="Consulted origin contradicts the selected claim.",
                claim_ref=claim.claim_ref,
            ),
        )
    if verdict is BindingVerdict.UNSUPPORTED:
        return (
            OriginResidual(
                kind=OriginResidualKind.EVIDENCE_MISSING,
                description="Consulted origin does not support the selected claim.",
                claim_ref=claim.claim_ref,
            ),
        )
    if verdict is BindingVerdict.PARTIALLY_COMPATIBLE:
        return (
            OriginResidual(
                kind=OriginResidualKind.BINDING_AMBIGUOUS,
                description="Consulted origin only partially matches the selected claim.",
                claim_ref=claim.claim_ref,
            ),
        )
    return ()


def _binding(
    claim: OriginBindingClaim,
    *,
    origin_type: str,
    origin_id: str,
    verdict: BindingVerdict,
    residuals: tuple[OriginResidual, ...],
    trace_ref: str,
) -> OriginBinding:
    return OriginBinding(
        claim_ref=claim.claim_ref,
        origin_type=origin_type,
        origin_id=origin_id,
        verdict=verdict,
        residuals=residuals,
        trace_ref=trace_ref,
    )


def _result(
    state: OriginBindingGateState,
    binding: OriginBinding | None,
    failure_code: FailureCode | None,
    *,
    residuals: tuple[OriginResidual, ...],
    source_claim_ref: str,
    trace_ref: str,
) -> OriginBindingGateResult:
    return OriginBindingGateResult(
        state=state,
        binding=binding,
        failure_code=failure_code,
        residuals=residuals,
        source_claim_ref=source_claim_ref,
        trace_ref=trace_ref,
    )


def _state_for_verdict(verdict: BindingVerdict) -> OriginBindingGateState:
    if verdict is BindingVerdict.COMPATIBLE:
        return OriginBindingGateState.BOUND
    if verdict is BindingVerdict.CONTRADICTED:
        return OriginBindingGateState.BLOCKED
    return OriginBindingGateState.DEFERRED


def _failure_for_verdict(verdict: BindingVerdict) -> FailureCode | None:
    if verdict is BindingVerdict.COMPATIBLE:
        return None
    if verdict is BindingVerdict.CONTRADICTED:
        return FailureCode.BLOCKING_RESIDUAL_PRESENT
    return FailureCode.REQUIRED_SLOT_EMPTY


def _origin_type(origin: KnowledgeOrigin) -> OriginBindingRequiredOriginType:
    if isinstance(origin, EntityGenusOrigin):
        return OriginBindingRequiredOriginType.ENTITY_GENUS
    if isinstance(origin, AttributeEventOrigin):
        return OriginBindingRequiredOriginType.ATTRIBUTE_EVENT
    if isinstance(origin, RelationOperatorOrigin):
        return OriginBindingRequiredOriginType.RELATION_OPERATOR
    if isinstance(origin, ReferenceOrigin):
        return OriginBindingRequiredOriginType.REFERENCE
    if isinstance(origin, EvidenceOrigin):
        return OriginBindingRequiredOriginType.EVIDENCE
    raise OriginBindingGateSchemaError("origin must be a licensed Knowledge Origin carrier")


def _origin_id(origin: KnowledgeOrigin) -> str:
    if isinstance(origin, EntityGenusOrigin):
        return origin.entity_id
    if isinstance(origin, AttributeEventOrigin):
        return origin.attribute_id
    if isinstance(origin, RelationOperatorOrigin):
        return origin.relation_id
    if isinstance(origin, ReferenceOrigin):
        return origin.reference_id
    return origin.claim_ref


def _origin_domain(origin: KnowledgeOrigin) -> str:
    return origin.domain


def _origin_residual_strings(origin: KnowledgeOrigin) -> tuple[str, ...]:
    return origin.residuals


__all__ = [
    "GPT_ORIGIN_BINDING_TRANSITION_CONTRACT",
    "KnowledgeOrigin",
    "OriginBindingClaim",
    "OriginBindingGateResult",
    "OriginBindingGateSchemaError",
    "OriginBindingGateState",
    "OriginBindingRequiredOriginType",
    "OriginBindingSourceKind",
    "bind_origin_to_claim",
    "claim_from_mafhum",
    "claim_from_mantuq_boundary",
]
