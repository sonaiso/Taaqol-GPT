"""GPT-R8 hallucination leak closure surfaces.

This module names the four leak ports left after the general
Candidate→Output and ReasonablenessVerdict→Certificate bans: reference
binding without internal trace, ellipsis without qarīnah, domain transfer
without preserved manāṭ, and premature R7 audit consumption.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.gpt.knowledge_origins import (
    OriginCarrierSchemaError,
    OriginRank,
    OriginResidual,
    OriginResidualKind,
    ResolutionType,
)
from taaqqul_slot_geometry.gpt.reasonableness_verdict import (
    GPTAnswerReasonablenessVerdict,
)


class HallucinationLeakKind(StrEnum):
    """Named GPT hallucination leak ports."""

    REFERENCE_BINDING = "REFERENCE_BINDING"
    ELLIPSIS_LICENSE = "ELLIPSIS_LICENSE"
    DOMAIN_BRIDGE = "DOMAIN_BRIDGE"
    R7_AUDIT_CONSUMPTION = "R7_AUDIT_CONSUMPTION"


class HallucinationLeakGateState(StrEnum):
    """Gate result state for a single leak port."""

    PASSED = "PASSED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


class BindingEvidenceType(StrEnum):
    """Licensed evidence kinds for reference binding."""

    EXPLICIT_PRIOR_TEXT = "explicit_prior_text"
    GRAMMATICAL_AGREEMENT = "grammatical_agreement"
    VISIBLE_CONTEXT = "visible_context"
    DEICTIC_CONTEXT = "deictic_context"
    PROBABILITY_ONLY = "probability_only"


class EllipsisQarinahType(StrEnum):
    """Qarīnah kinds accepted or refused for ellipsis licensing."""

    PREVIOUS_QUESTION = "previous_question"
    EXPLICIT_PRIOR_TEXT = "explicit_prior_text"
    SYNTACTIC_REQUIREMENT = "syntactic_requirement"
    VISIBLE_CONTEXT = "visible_context"
    ESTABLISHED_USAGE = "established_usage"
    CONTRASTIVE_STRUCTURE = "contrastive_structure"
    ANSWER_COMPLETION = "answer_completion"
    STATISTICAL_LIKELIHOOD = "statistical_likelihood"
    GENERAL_PLAUSIBILITY = "general_plausibility"
    MODEL_CONFIDENCE = "model_confidence"


_LICENSED_QARINAH_TYPES = frozenset(
    {
        EllipsisQarinahType.PREVIOUS_QUESTION,
        EllipsisQarinahType.EXPLICIT_PRIOR_TEXT,
        EllipsisQarinahType.SYNTACTIC_REQUIREMENT,
        EllipsisQarinahType.VISIBLE_CONTEXT,
        EllipsisQarinahType.ESTABLISHED_USAGE,
        EllipsisQarinahType.CONTRASTIVE_STRUCTURE,
        EllipsisQarinahType.ANSWER_COMPLETION,
    }
)


class DomainBridgeResult(StrEnum):
    """Domain bridge result surface; never truth/certificate."""

    BRIDGED = "BRIDGED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise OriginCarrierSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise OriginCarrierSchemaError(f"{cls_name}.{field} must start with 'trace://'")


def _require_tuple(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise OriginCarrierSchemaError(f"{cls_name}.{field} must be a tuple")


def _require_origin_residuals(value: object) -> None:
    if not isinstance(value, tuple):
        raise OriginCarrierSchemaError("residuals must be a tuple of OriginResidual carriers")
    for residual in value:
        if not isinstance(residual, OriginResidual):
            raise OriginCarrierSchemaError("residual entries must be OriginResidual carriers")


@dataclass(frozen=True, slots=True)
class ReferenceBindingEvidence:
    """Trace-bound evidence connecting a reference surface to a referent."""

    reference_id: str
    reference_surface: str
    reference_trace_ref: str
    candidate_referent: str
    referent_trace_ref: str
    binding_evidence_type: BindingEvidenceType
    binding_evidence_trace_ref: str
    resolution_type: ResolutionType
    resolution_rank: OriginRank
    competing_referents: tuple[str, ...]
    blocking_residuals: tuple[OriginResidual, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "reference_id", self.reference_id)
        _require_nonempty_str(cls, "reference_surface", self.reference_surface)
        _require_trace_ref(cls, "reference_trace_ref", self.reference_trace_ref)
        _require_nonempty_str(cls, "candidate_referent", self.candidate_referent)
        _require_trace_ref(cls, "referent_trace_ref", self.referent_trace_ref)
        if not isinstance(self.binding_evidence_type, BindingEvidenceType):
            raise OriginCarrierSchemaError(
                f"{cls}.binding_evidence_type must be a BindingEvidenceType member"
            )
        _require_trace_ref(cls, "binding_evidence_trace_ref", self.binding_evidence_trace_ref)
        if not isinstance(self.resolution_type, ResolutionType):
            raise OriginCarrierSchemaError(
                f"{cls}.resolution_type must be a ResolutionType member"
            )
        if not isinstance(self.resolution_rank, OriginRank):
            raise OriginCarrierSchemaError(f"{cls}.resolution_rank must be an OriginRank member")
        _require_tuple(cls, "competing_referents", self.competing_referents)
        _require_origin_residuals(self.blocking_residuals)


@dataclass(frozen=True, slots=True)
class EllipsisEstimate:
    """A proposed ellipsis fill licensed only by an explicit qarīnah."""

    ellipsis_id: str
    missing_slot: str
    proposed_fill: str
    opening_trigger: str
    qarinah_type: EllipsisQarinahType
    qarinah_trace_ref: str
    license_reason: str
    alternatives: tuple[str, ...]
    closure_effect: str
    residuals: tuple[OriginResidual, ...]
    rank: OriginRank

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "ellipsis_id", self.ellipsis_id)
        _require_nonempty_str(cls, "missing_slot", self.missing_slot)
        _require_nonempty_str(cls, "proposed_fill", self.proposed_fill)
        _require_nonempty_str(cls, "opening_trigger", self.opening_trigger)
        if not isinstance(self.qarinah_type, EllipsisQarinahType):
            raise OriginCarrierSchemaError(
                f"{cls}.qarinah_type must be an EllipsisQarinahType member"
            )
        _require_trace_ref(cls, "qarinah_trace_ref", self.qarinah_trace_ref)
        _require_nonempty_str(cls, "license_reason", self.license_reason)
        _require_tuple(cls, "alternatives", self.alternatives)
        _require_nonempty_str(cls, "closure_effect", self.closure_effect)
        _require_origin_residuals(self.residuals)
        if not isinstance(self.rank, OriginRank):
            raise OriginCarrierSchemaError(f"{cls}.rank must be an OriginRank member")


@dataclass(frozen=True, slots=True)
class DomainBridgeCard:
    """Trace-bound domain bridge requiring preserved manāṭ."""

    source_domain: str
    target_domain: str
    source_claim: str
    target_claim: str
    preserved_manat: str
    common_illah: str
    effective_description: str
    qadih_difference_check: bool
    bridge_evidence_trace_ref: str
    rank_ceiling: Rank
    residual_transfer_policy: str
    result: DomainBridgeResult

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "source_domain", self.source_domain)
        _require_nonempty_str(cls, "target_domain", self.target_domain)
        _require_nonempty_str(cls, "source_claim", self.source_claim)
        _require_nonempty_str(cls, "target_claim", self.target_claim)
        _require_nonempty_str(cls, "preserved_manat", self.preserved_manat)
        _require_nonempty_str(cls, "common_illah", self.common_illah)
        _require_nonempty_str(cls, "effective_description", self.effective_description)
        if not isinstance(self.qadih_difference_check, bool):
            raise OriginCarrierSchemaError(f"{cls}.qadih_difference_check must be a bool")
        _require_trace_ref(cls, "bridge_evidence_trace_ref", self.bridge_evidence_trace_ref)
        if not isinstance(self.rank_ceiling, Rank):
            raise OriginCarrierSchemaError(f"{cls}.rank_ceiling must be a Rank member")
        _require_nonempty_str(cls, "residual_transfer_policy", self.residual_transfer_policy)
        if not isinstance(self.result, DomainBridgeResult):
            raise OriginCarrierSchemaError(f"{cls}.result must be a DomainBridgeResult member")


@dataclass(frozen=True, slots=True)
class HallucinationLeakGateResult:
    """Visible result for one named leak closure gate."""

    leak: HallucinationLeakKind
    state: HallucinationLeakGateState
    failure_code: FailureCode | None
    residuals: tuple[OriginResidual, ...]
    source_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.leak, HallucinationLeakKind):
            raise OriginCarrierSchemaError(f"{cls}.leak must be a HallucinationLeakKind member")
        if not isinstance(self.state, HallucinationLeakGateState):
            raise OriginCarrierSchemaError(
                f"{cls}.state must be a HallucinationLeakGateState member"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise OriginCarrierSchemaError(f"{cls}.failure_code must be a FailureCode or None")
        _require_origin_residuals(self.residuals)
        _require_nonempty_str(cls, "source_ref", self.source_ref)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if self.state is HallucinationLeakGateState.PASSED and self.failure_code is not None:
            raise OriginCarrierSchemaError(f"{cls}.PASSED must not carry failure_code")
        if self.state is not HallucinationLeakGateState.PASSED and self.failure_code is None:
            raise OriginCarrierSchemaError(f"{cls}.{self.state.value} requires a failure_code")


def evaluate_reference_binding(
    evidence: ReferenceBindingEvidence | None,
    *,
    trace_ref: str,
) -> HallucinationLeakGateResult:
    """Approve a reference binding only when internal traces and source exist."""

    _require_trace_ref("HallucinationLeakGateResult", "trace_ref", trace_ref)
    if evidence is None:
        return _result(
            HallucinationLeakKind.REFERENCE_BINDING,
            HallucinationLeakGateState.DEFERRED,
            FailureCode.REFERENCE_WITHOUT_TRACE,
            residual_kind=OriginResidualKind.REFERENCE_WITHOUT_TRACE,
            source_ref="missing-reference-binding",
            trace_ref=trace_ref,
        )
    if evidence.binding_evidence_type is BindingEvidenceType.PROBABILITY_ONLY:
        return _result(
            HallucinationLeakKind.REFERENCE_BINDING,
            HallucinationLeakGateState.BLOCKED,
            FailureCode.REFERENCE_RESOLVED_BY_PROBABILITY_ONLY,
            residual_kind=OriginResidualKind.REFERENCE_RESOLVED_BY_PROBABILITY_ONLY,
            source_ref=evidence.reference_id,
            trace_ref=trace_ref,
        )
    if evidence.competing_referents or evidence.blocking_residuals:
        residuals = evidence.blocking_residuals or (
            _residual(
                OriginResidualKind.REFERENCE_BINDING_COMPETITOR_UNHANDLED,
                FailureCode.REFERENCE_BINDING_COMPETITOR_UNHANDLED.value,
                evidence.reference_id,
            ),
        )
        return HallucinationLeakGateResult(
            leak=HallucinationLeakKind.REFERENCE_BINDING,
            state=HallucinationLeakGateState.BLOCKED,
            failure_code=FailureCode.REFERENCE_BINDING_COMPETITOR_UNHANDLED,
            residuals=residuals,
            source_ref=evidence.reference_id,
            trace_ref=trace_ref,
        )
    return HallucinationLeakGateResult(
        leak=HallucinationLeakKind.REFERENCE_BINDING,
        state=HallucinationLeakGateState.PASSED,
        failure_code=None,
        residuals=(),
        source_ref=evidence.reference_id,
        trace_ref=trace_ref,
    )


def license_ellipsis_estimate(
    estimate: EllipsisEstimate | None,
    *,
    trace_ref: str,
) -> HallucinationLeakGateResult:
    """License an ellipsis fill only from an accepted qarīnah type."""

    _require_trace_ref("HallucinationLeakGateResult", "trace_ref", trace_ref)
    if estimate is None:
        return _result(
            HallucinationLeakKind.ELLIPSIS_LICENSE,
            HallucinationLeakGateState.DEFERRED,
            FailureCode.MISSING_QARINAH_FOR_DELETION,
            residual_kind=OriginResidualKind.MISSING_QARINAH_FOR_DELETION,
            source_ref="missing-ellipsis-estimate",
            trace_ref=trace_ref,
        )
    if estimate.qarinah_type not in _LICENSED_QARINAH_TYPES:
        return _result(
            HallucinationLeakKind.ELLIPSIS_LICENSE,
            HallucinationLeakGateState.BLOCKED,
            FailureCode.ELLIPSIS_FILLED_BY_PROBABILITY_ONLY,
            residual_kind=OriginResidualKind.ELLIPSIS_FILLED_BY_PROBABILITY_ONLY,
            source_ref=estimate.ellipsis_id,
            trace_ref=trace_ref,
        )
    if estimate.alternatives:
        return _result(
            HallucinationLeakKind.ELLIPSIS_LICENSE,
            HallucinationLeakGateState.DEFERRED,
            FailureCode.MULTIPLE_ELLIPSIS_CANDIDATES_UNRESOLVED,
            residual_kind=OriginResidualKind.MULTIPLE_ELLIPSIS_CANDIDATES_UNRESOLVED,
            source_ref=estimate.ellipsis_id,
            trace_ref=trace_ref,
        )
    return HallucinationLeakGateResult(
        leak=HallucinationLeakKind.ELLIPSIS_LICENSE,
        state=HallucinationLeakGateState.PASSED,
        failure_code=None,
        residuals=estimate.residuals,
        source_ref=estimate.ellipsis_id,
        trace_ref=trace_ref,
    )


def evaluate_domain_bridge(
    bridge: DomainBridgeCard | None,
    *,
    trace_ref: str,
) -> HallucinationLeakGateResult:
    """Block cross-domain transfer unless a preserved manāṭ bridge exists."""

    _require_trace_ref("HallucinationLeakGateResult", "trace_ref", trace_ref)
    if bridge is None:
        return _result(
            HallucinationLeakKind.DOMAIN_BRIDGE,
            HallucinationLeakGateState.BLOCKED,
            FailureCode.DOMAIN_TRANSFER_WITHOUT_MANAT,
            residual_kind=OriginResidualKind.DOMAIN_TRANSFER_WITHOUT_MANAT,
            source_ref="missing-domain-bridge",
            trace_ref=trace_ref,
        )
    if not bridge.qadih_difference_check:
        return _result(
            HallucinationLeakKind.DOMAIN_BRIDGE,
            HallucinationLeakGateState.BLOCKED,
            FailureCode.QADIH_DIFFERENCE_UNCHECKED,
            residual_kind=OriginResidualKind.QADIH_DIFFERENCE_UNCHECKED,
            source_ref=f"{bridge.source_domain}->{bridge.target_domain}",
            trace_ref=trace_ref,
        )
    if bridge.result is not DomainBridgeResult.BRIDGED:
        return _result(
            HallucinationLeakKind.DOMAIN_BRIDGE,
            HallucinationLeakGateState.BLOCKED,
            FailureCode.DOMAIN_LEAP_WITHOUT_BRIDGE,
            residual_kind=OriginResidualKind.DOMAIN_LEAP_WITHOUT_BRIDGE,
            source_ref=f"{bridge.source_domain}->{bridge.target_domain}",
            trace_ref=trace_ref,
        )
    return HallucinationLeakGateResult(
        leak=HallucinationLeakKind.DOMAIN_BRIDGE,
        state=HallucinationLeakGateState.PASSED,
        failure_code=None,
        residuals=(),
        source_ref=f"{bridge.source_domain}->{bridge.target_domain}",
        trace_ref=trace_ref,
    )


def refuse_r7_as_final_audit(
    verdict: GPTAnswerReasonablenessVerdict | None,
    *,
    trace_ref: str,
) -> HallucinationLeakGateResult:
    """Reject consuming GPT-R7 directly as a final AnswerAudit."""

    _require_trace_ref("HallucinationLeakGateResult", "trace_ref", trace_ref)
    source_ref = (
        verdict.trace_ref
        if isinstance(verdict, GPTAnswerReasonablenessVerdict)
        else "missing-r7"
    )
    return _result(
        HallucinationLeakKind.R7_AUDIT_CONSUMPTION,
        HallucinationLeakGateState.BLOCKED,
        FailureCode.PREMATURE_R7_AUDIT_CONSUMPTION,
        residual_kind=OriginResidualKind.PREMATURE_R7_AUDIT_CONSUMPTION,
        source_ref=source_ref,
        trace_ref=trace_ref,
    )


def _result(
    leak: HallucinationLeakKind,
    state: HallucinationLeakGateState,
    failure_code: FailureCode,
    *,
    residual_kind: OriginResidualKind,
    source_ref: str,
    trace_ref: str,
) -> HallucinationLeakGateResult:
    return HallucinationLeakGateResult(
        leak=leak,
        state=state,
        failure_code=failure_code,
        residuals=(_residual(residual_kind, failure_code.value, source_ref),),
        source_ref=source_ref,
        trace_ref=trace_ref,
    )


def _residual(kind: OriginResidualKind, description: str, claim_ref: str) -> OriginResidual:
    return OriginResidual(kind=kind, description=description, claim_ref=claim_ref)


__all__ = [
    "BindingEvidenceType",
    "DomainBridgeCard",
    "DomainBridgeResult",
    "EllipsisEstimate",
    "EllipsisQarinahType",
    "HallucinationLeakGateResult",
    "HallucinationLeakGateState",
    "HallucinationLeakKind",
    "ReferenceBindingEvidence",
    "evaluate_domain_bridge",
    "evaluate_reference_binding",
    "license_ellipsis_estimate",
    "refuse_r7_as_final_audit",
]
