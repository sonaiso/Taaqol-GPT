"""Acceptance tests for GPT-R5 Origin Binding Gate.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law) + docs/55
Branch         : GPT-R5 (Origin Binding Gate)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.gpt import (
    GPT_ORIGIN_BINDING_TRANSITION_CONTRACT,
    AttributeEventOrigin,
    BindingVerdict,
    EntityGenusOrigin,
    EvidenceDirection,
    EvidenceOrigin,
    ExplicitClaim,
    GPTAnswerInput,
    InputEvidenceNeed,
    InputRiskLevel,
    InputTimeSensitivity,
    MafhumGPTState,
    MafhumType,
    MantuqGPT,
    OriginBindingClaim,
    OriginBindingGateSchemaError,
    OriginBindingGateState,
    OriginBindingRequiredOriginType,
    OriginRank,
    OriginResidual,
    OriginResidualKind,
    OriginStability,
    PreventerGateResult,
    PreventerKind,
    RestrictionKind,
    bind_origin_to_claim,
    build_mafhum_gpt,
    build_mantuq_gpt,
    build_maqam_gpt,
    claim_from_mafhum,
    claim_from_mantuq_boundary,
)
from taaqqul_slot_geometry.gpt.mafhum_boundary import (
    ExplicitRestriction,
    ScopeBoundary,
    SilenceNonMention,
)
from taaqqul_slot_geometry.gpt.mantuq_boundary import ClaimBoundary
from taaqqul_slot_geometry.x0r import JumpTestInput, ResidualKind


def _make_mantuq() -> tuple[MantuqGPT, ClaimBoundary]:
    answer_input = GPTAnswerInput(
        request_id="req-r5-001",
        user_question="هل جواب GPT معقول؟",
        gpt_answer="زيد إنسان.",
        question_type_hint="factual",
        domain_hint="gpt_reasonableness",
        constraints=("show-origins",),
        evidence_need=InputEvidenceNeed.MEDIUM,
        risk_level=InputRiskLevel.MEDIUM,
        time_sensitivity=InputTimeSensitivity.STATIC,
        forbidden_answer_forms=("truth-declaration",),
        trace_ref="trace://gpt-r1/input/r5-001",
    )
    maqam = build_maqam_gpt(answer_input, trace_ref="trace://gpt-r2/maqam/r5-001")
    claim = ExplicitClaim(
        claim_id="claim/entity/1",
        subject="زيد",
        predicate="إنسان",
        qualifiers=("explicit",),
        modality="asserted",
        domain="gpt_reasonableness",
        span_trace="trace://gpt-r3/span/r5/entity/1",
    )
    boundary = ClaimBoundary(
        claim=claim,
        source_maqam_ref=maqam.trace_ref,
        trace_ref="trace://gpt-r3/claim-boundary/r5/entity/1",
    )
    mantuq = build_mantuq_gpt(
        maqam,
        answer_ref="answer://gpt/r5/001",
        explicit_claims=(boundary,),
        span_traces=("trace://gpt-r3/span/r5/entity/1",),
        residuals=("OriginBinding deferred until GPT-R5.",),
        trace_ref="trace://gpt-r3/mantuq/r5/001",
    )
    return mantuq, boundary


def _entity_origin(*, residuals: tuple[str, ...] = ()) -> EntityGenusOrigin:
    return EntityGenusOrigin(
        entity_id="entity/zayd",
        genus="human",
        essential_properties=("rational animal",),
        bearing_capacity=("predicate:human",),
        bearing_refusal=("predicate:stone",),
        domain="gpt_reasonableness",
        stability=OriginStability.PERMANENT,
        source_ref="origin://entity/zayd",
        rank=OriginRank.HIGH,
        residuals=residuals,
    )


def _attribute_origin() -> AttributeEventOrigin:
    return AttributeEventOrigin(
        attribute_id="attribute/flying",
        required_conditions=("has wings or aircraft support",),
        contradicting_conditions=("ordinary unaided human",),
        typical_bearers=("bird", "aircraft"),
        impossible_bearers=("ordinary unaided human",),
        domain="gpt_reasonableness",
        stability=OriginStability.PERMANENT,
        source_ref="origin://attribute/flying",
        rank=OriginRank.HIGH,
        residuals=(),
    )


def _evidence_origin() -> EvidenceOrigin:
    return EvidenceOrigin(
        claim_ref="claim/entity/1",
        evidence_type="source",
        evidence_direction=EvidenceDirection.NEUTRAL,
        evidence_content="No supporting source is available.",
        source="origin://evidence/neutral",
        source_rank=OriginRank.LOW,
        recency=OriginStability.PROVISIONAL,
        domain="gpt_reasonableness",
        stability=OriginStability.PROVISIONAL,
        residuals=(),
        contradiction_with=(),
    )


def _claim() -> OriginBindingClaim:
    mantuq, boundary = _make_mantuq()
    return claim_from_mantuq_boundary(
        mantuq,
        boundary,
        required_origin_type=OriginBindingRequiredOriginType.ENTITY_GENUS,
        trace_ref="trace://gpt-r5/claim/entity/1",
    )


def test_compatible_origin_binding_is_gate_result_only() -> None:
    result = bind_origin_to_claim(
        _claim(),
        _entity_origin(),
        verdict=BindingVerdict.COMPATIBLE,
        residuals=(),
        trace_ref="trace://gpt-r5/binding/entity/1",
    )

    assert result.state is OriginBindingGateState.BOUND
    assert result.binding is not None
    assert result.binding.verdict is BindingVerdict.COMPATIBLE
    assert result.failure_code is None
    assert not hasattr(result, "reasonableness_verdict")
    assert not hasattr(result, "truth")


def test_unsupported_origin_creates_visible_residual() -> None:
    result = bind_origin_to_claim(
        _claim(),
        None,
        verdict=None,
        residuals=(),
        trace_ref="trace://gpt-r5/binding/unsupported/1",
    )

    assert result.state is OriginBindingGateState.DEFERRED
    assert result.binding is not None
    assert result.binding.verdict is BindingVerdict.UNSUPPORTED
    assert result.residuals
    assert result.residuals[0].kind is OriginResidualKind.ORIGIN_ABSENT
    assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


def test_contradicted_origin_blocks_with_visible_residual() -> None:
    result = bind_origin_to_claim(
        OriginBindingClaim(
            claim_ref="claim/attribute/1",
            claim_trace_ref="trace://gpt-r3/claim-boundary/r5/attribute/1",
            domain="gpt_reasonableness",
            required_origin_type=OriginBindingRequiredOriginType.ATTRIBUTE_EVENT,
            source_kind=_claim().source_kind,
            trace_ref="trace://gpt-r5/claim/attribute/1",
        ),
        _attribute_origin(),
        verdict=BindingVerdict.CONTRADICTED,
        residuals=(),
        trace_ref="trace://gpt-r5/binding/contradicted/1",
    )

    assert result.state is OriginBindingGateState.BLOCKED
    assert result.binding is not None
    assert result.binding.verdict is BindingVerdict.CONTRADICTED
    assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert result.residuals[0].kind is OriginResidualKind.EVIDENCE_CONTRADICTED


def test_missing_claim_refuses_origin_binding() -> None:
    result = bind_origin_to_claim(
        None,
        _entity_origin(),
        verdict=BindingVerdict.COMPATIBLE,
        residuals=(),
        trace_ref="trace://gpt-r5/binding/missing-claim",
    )

    assert result.state is OriginBindingGateState.REFUSED
    assert result.binding is None
    assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


def test_missing_trace_refuses_jump_contract() -> None:
    result = GPT_ORIGIN_BINDING_TRANSITION_CONTRACT.evaluate(
        JumpTestInput(
            source_level="OriginBindingClaim",
            target_level="KnowledgeOrigin",
            transition_name="consult_required_origin",
            domain="gpt_reasonableness",
            trace_ref="",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(),
        )
    )

    assert result.allowed is False
    assert result.failure_code is FailureCode.TRACE_MISSING


def test_compatible_binding_cannot_hide_origin_residuals() -> None:
    result = bind_origin_to_claim(
        _claim(),
        _entity_origin(residuals=("origin remains contested in one source",)),
        verdict=BindingVerdict.COMPATIBLE,
        residuals=(),
        trace_ref="trace://gpt-r5/binding/hidden-residual",
    )

    assert result.state is OriginBindingGateState.REFUSED
    assert result.failure_code is FailureCode.HIDDEN_RESIDUAL
    assert result.residuals


def test_compatible_bound_result_with_visible_residuals_is_not_reasonableness() -> None:
    visible_residual = OriginResidual(
        kind=OriginResidualKind.BINDING_AMBIGUOUS,
        description="Compatible origin binding still carries a non-blocking visible residual.",
        claim_ref="claim/entity/1",
    )
    result = bind_origin_to_claim(
        _claim(),
        _entity_origin(),
        verdict=BindingVerdict.COMPATIBLE,
        residuals=(visible_residual,),
        trace_ref="trace://gpt-r5/binding/bound-with-residual",
    )

    assert result.state is OriginBindingGateState.BOUND
    assert result.binding is not None
    assert result.binding.verdict is BindingVerdict.COMPATIBLE
    assert result.residuals == (visible_residual,)
    assert result.failure_code is None
    assert not hasattr(result, "reasonableness_verdict")
    assert not hasattr(result, "truth")
    assert not hasattr(result, "certificate")


def test_mafhum_candidate_can_be_selected_for_origin_binding() -> None:
    mantuq, _ = _make_mantuq()
    mafhum_result = build_mafhum_gpt(
        mantuq,
        source_claim_ref="claim/entity/1",
        restriction=ExplicitRestriction(
            source_claim_ref="claim/entity/1",
            kind=RestrictionKind.DESCRIPTION,
            text="زيد إنسان",
            trace_ref="trace://gpt-r4/restriction/r5/1",
        ),
        scope_boundary=ScopeBoundary(
            source_claim_ref="claim/entity/1",
            domain="gpt_reasonableness",
            scope="زيد/إنسان",
            trace_ref="trace://gpt-r4/scope/r5/1",
        ),
        unmentioned_counterpart=SilenceNonMention(
            source_claim_ref="claim/entity/1",
            counterpart="غير زيد",
            relation="description does not license a universal counterpart",
            trace_ref="trace://gpt-r4/silence/r5/1",
        ),
        mafhum_type=MafhumType.DESCRIPTION,
        preventer=PreventerGateResult(
            source_claim_ref="claim/entity/1",
            preventer=PreventerKind.NONE_VISIBLE,
            explanation="No visible preventer at selection time.",
            trace_ref="trace://gpt-r4/preventer/r5/1",
        ),
        residuals=("OriginBinding opens only at GPT-R5.",),
        trace_ref="trace://gpt-r4/mafhum/r5/1",
    )

    assert mafhum_result.state is MafhumGPTState.LICENSED
    assert mafhum_result.candidate is not None
    claim = claim_from_mafhum(
        mafhum_result.candidate,
        required_origin_type=OriginBindingRequiredOriginType.EVIDENCE,
        trace_ref="trace://gpt-r5/claim/mafhum/1",
    )
    result = bind_origin_to_claim(
        claim,
        _evidence_origin(),
        verdict=BindingVerdict.PARTIALLY_COMPATIBLE,
        residuals=(
            OriginResidual(
                kind=OriginResidualKind.EVIDENCE_INSUFFICIENT,
                description=(
                    "Evidence origin is neutral and does not fully support the implication."
                ),
                claim_ref="claim/entity/1",
            ),
        ),
        trace_ref="trace://gpt-r5/binding/mafhum/1",
    )

    assert result.state is OriginBindingGateState.DEFERRED
    assert result.binding is not None
    assert result.binding.origin_type == "EvidenceOrigin"


def test_required_origin_contract_controls_origin_type_mismatch() -> None:
    result = bind_origin_to_claim(
        _claim(),
        _attribute_origin(),
        verdict=BindingVerdict.COMPATIBLE,
        residuals=(),
        trace_ref="trace://gpt-r5/binding/required-type-mismatch",
    )

    assert result.state is OriginBindingGateState.DEFERRED
    assert result.binding is not None
    assert result.binding.origin_type == OriginBindingRequiredOriginType.ATTRIBUTE_EVENT.value
    assert result.binding.verdict is BindingVerdict.UNSUPPORTED
    assert result.residuals[0].kind is OriginResidualKind.BINDING_AMBIGUOUS
    assert "Claim requires EntityGenusOrigin" in result.residuals[0].description


def test_direct_claim_to_reasonableness_transition_is_forbidden() -> None:
    result = GPT_ORIGIN_BINDING_TRANSITION_CONTRACT.evaluate(
        JumpTestInput(
            source_level="OriginBindingClaim",
            target_level="ReasonablenessVerdict",
            transition_name="direct_reasonableness",
            domain="gpt_reasonableness",
            trace_ref="trace://gpt-r5/jump/direct-reasonableness",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(),
        )
    )

    assert result.allowed is False
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_bound_result_to_reasonableness_transition_is_forbidden() -> None:
    result = GPT_ORIGIN_BINDING_TRANSITION_CONTRACT.evaluate(
        JumpTestInput(
            source_level="OriginBindingGateResult",
            target_level="ReasonablenessVerdict",
            transition_name="silent_bound_to_reasonableness",
            domain="gpt_reasonableness",
            trace_ref="trace://gpt-r5/jump/bound-to-reasonableness",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=("BINDING_AMBIGUOUS",),
        )
    )

    assert result.allowed is False
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_raw_string_required_origin_type_is_schema_error() -> None:
    with pytest.raises(OriginBindingGateSchemaError):
        OriginBindingClaim(
            claim_ref="claim/entity/1",
            claim_trace_ref="trace://gpt-r3/claim-boundary/r5/entity/1",
            domain="gpt_reasonableness",
            required_origin_type="EntityGenusOrigin",
            source_kind=_claim().source_kind,
            trace_ref="trace://gpt-r5/claim/raw-origin-type",
        )


def test_forbidden_later_outputs_still_absent_after_gpt_r5() -> None:
    import taaqqul_slot_geometry.gpt as gpt_module

    for forbidden in (
        "ReasonablenessGate",
        "EvidenceSupportGate",
        "ReasonablenessVerdict",
        "GPTAnswerReasonablenessVerdict",
        "ReasonablenessPipeline",
        "AuditIntegration",
    ):
        assert not hasattr(gpt_module, forbidden)
