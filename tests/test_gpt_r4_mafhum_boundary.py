"""Acceptance tests for GPT-R4 MafhumGPT licensed implication boundary.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law)
Branch         : GPT-R4 (MafhumGPT Implication Extraction)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.gpt import (
    GPT_MAFHUM_TRANSITION_CONTRACT,
    ClaimBoundary,
    ExplicitClaim,
    ExplicitRestriction,
    GPTAnswerInput,
    InputEvidenceNeed,
    InputRiskLevel,
    InputTimeSensitivity,
    MafhumGPT,
    MafhumGPTState,
    MafhumType,
    MantuqGPT,
    PreventerGateResult,
    PreventerKind,
    RestrictionKind,
    ScopeBoundary,
    SilenceNonMention,
    build_mafhum_gpt,
    build_mantuq_gpt,
    build_maqam_gpt,
)
from taaqqul_slot_geometry.x0r import JumpTestInput


def _make_mantuq() -> MantuqGPT:
    answer_input = GPTAnswerInput(
        request_id="req-r4-001",
        user_question="هل جواب GPT معقول؟",
        gpt_answer="إن نجح زيد فأكرمه.",
        question_type_hint="factual",
        domain_hint="reasonableness-audit",
        constraints=("show-residuals",),
        evidence_need=InputEvidenceNeed.MEDIUM,
        risk_level=InputRiskLevel.MEDIUM,
        time_sensitivity=InputTimeSensitivity.STATIC,
        forbidden_answer_forms=("truth-declaration",),
        trace_ref="trace://gpt-r1/input/r4-001",
    )
    maqam = build_maqam_gpt(answer_input, trace_ref="trace://gpt-r2/maqam/r4-001")
    claim = ExplicitClaim(
        claim_id="claim/condition/1",
        subject="زيد",
        predicate="إكرامه عند النجاح",
        qualifiers=("إن نجح",),
        modality="asserted",
        domain="reasonableness-audit",
        span_trace="trace://gpt-r3/span/r4/condition/1",
    )
    boundary = ClaimBoundary(
        claim=claim,
        source_maqam_ref=maqam.trace_ref,
        trace_ref="trace://gpt-r3/claim-boundary/r4/condition/1",
    )
    return build_mantuq_gpt(
        maqam,
        answer_ref="answer://gpt/r4/001",
        explicit_claims=(boundary,),
        span_traces=("trace://gpt-r3/span/r4/condition/1",),
        residuals=("MafhumGPT deferred until GPT-R4.",),
        trace_ref="trace://gpt-r3/mantuq/r4/001",
    )


def _restriction() -> ExplicitRestriction:
    return ExplicitRestriction(
        source_claim_ref="claim/condition/1",
        kind=RestrictionKind.CONDITION,
        text="إن نجح",
        trace_ref="trace://gpt-r4/restriction/condition/1",
    )


def _scope() -> ScopeBoundary:
    return ScopeBoundary(
        source_claim_ref="claim/condition/1",
        domain="reasonableness-audit",
        scope="زيد/الإكرام",
        trace_ref="trace://gpt-r4/scope/condition/1",
    )


def _silence() -> SilenceNonMention:
    return SilenceNonMention(
        source_claim_ref="claim/condition/1",
        counterpart="عدم النجاح",
        relation="absence of the explicit condition affects only the scoped case",
        trace_ref="trace://gpt-r4/silence/condition/1",
    )


def test_condition_mafhum_success_is_candidate_only() -> None:
    result = build_mafhum_gpt(
        _make_mantuq(),
        source_claim_ref="claim/condition/1",
        restriction=_restriction(),
        scope_boundary=_scope(),
        unmentioned_counterpart=_silence(),
        mafhum_type=MafhumType.CONDITION,
        preventer=PreventerGateResult(
            source_claim_ref="claim/condition/1",
            preventer=PreventerKind.NONE_VISIBLE,
            explanation="No visible preventer at this boundary.",
            trace_ref="trace://gpt-r4/preventer/condition/1",
        ),
        residuals=("OriginBinding not opened at GPT-R4.",),
        trace_ref="trace://gpt-r4/mafhum/condition/1",
    )

    assert result.state is MafhumGPTState.LICENSED
    assert isinstance(result.candidate, MafhumGPT)
    assert result.failure_code is None
    assert result.candidate.unmentioned_counterpart.counterpart == "عدم النجاح"
    assert not hasattr(result.candidate, "truth")
    assert not hasattr(result.candidate, "reasonableness_verdict")


def test_preventer_blocks_mafhum_candidate() -> None:
    result = build_mafhum_gpt(
        _make_mantuq(),
        source_claim_ref="claim/condition/1",
        restriction=ExplicitRestriction(
            source_claim_ref="claim/condition/1",
            kind=RestrictionKind.DESCRIPTION,
            text="أضعافًا مضاعفة",
            trace_ref="trace://gpt-r4/restriction/riba/1",
        ),
        scope_boundary=ScopeBoundary(
            source_claim_ref="claim/condition/1",
            domain="reasonableness-audit",
            scope="النهي عن الربا في مقام التغليظ",
            trace_ref="trace://gpt-r4/scope/riba/1",
        ),
        unmentioned_counterpart=SilenceNonMention(
            source_claim_ref="claim/condition/1",
            counterpart="غير أضعاف مضاعفة",
            relation="description absence is tested only inside the scoped prohibition",
            trace_ref="trace://gpt-r4/silence/riba/1",
        ),
        mafhum_type=MafhumType.DESCRIPTION,
        preventer=PreventerGateResult(
            source_claim_ref="claim/condition/1",
            preventer=PreventerKind.COMMON_CASE,
            explanation="The description may be for intensification or common occurrence.",
            trace_ref="trace://gpt-r4/preventer/riba/1",
        ),
        residuals=("Visible preventer blocks licensing.",),
        trace_ref="trace://gpt-r4/mafhum/riba/1",
    )

    assert result.state is MafhumGPTState.BLOCKED
    assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert result.candidate is not None
    assert result.candidate.preventer.preventer is PreventerKind.COMMON_CASE


def test_no_mantuq_refuses_mafhum() -> None:
    result = build_mafhum_gpt(
        "not-mantuq",  # type: ignore[arg-type]
        source_claim_ref="claim/condition/1",
        restriction=_restriction(),
        scope_boundary=_scope(),
        unmentioned_counterpart=_silence(),
        mafhum_type=MafhumType.CONDITION,
        preventer=PreventerGateResult(
            source_claim_ref="claim/condition/1",
            preventer=PreventerKind.NONE_VISIBLE,
            explanation="No visible preventer.",
            trace_ref="trace://gpt-r4/preventer/no-mantuq",
        ),
        residuals=("No MantuqGPT.",),
        trace_ref="trace://gpt-r4/mafhum/no-mantuq",
    )

    assert result.state is MafhumGPTState.REFUSED
    assert result.failure_code is FailureCode.MAFHUM_BEFORE_MANTUQ
    assert result.candidate is None


def test_no_restriction_refuses_mafhum() -> None:
    result = build_mafhum_gpt(
        _make_mantuq(),
        source_claim_ref="claim/condition/1",
        restriction=None,
        scope_boundary=_scope(),
        unmentioned_counterpart=_silence(),
        mafhum_type=MafhumType.CONDITION,
        preventer=PreventerGateResult(
            source_claim_ref="claim/condition/1",
            preventer=PreventerKind.NONE_VISIBLE,
            explanation="No visible preventer.",
            trace_ref="trace://gpt-r4/preventer/no-restriction",
        ),
        residuals=("No restriction.",),
        trace_ref="trace://gpt-r4/mafhum/no-restriction",
    )

    assert result.state is MafhumGPTState.REFUSED
    assert result.failure_code is FailureCode.REQUIRED_SLOT_EMPTY


def test_no_scope_defers_mafhum() -> None:
    result = build_mafhum_gpt(
        _make_mantuq(),
        source_claim_ref="claim/condition/1",
        restriction=_restriction(),
        scope_boundary=None,
        unmentioned_counterpart=_silence(),
        mafhum_type=MafhumType.CONDITION,
        preventer=PreventerGateResult(
            source_claim_ref="claim/condition/1",
            preventer=PreventerKind.NONE_VISIBLE,
            explanation="No visible preventer.",
            trace_ref="trace://gpt-r4/preventer/no-scope",
        ),
        residuals=("No scope.",),
        trace_ref="trace://gpt-r4/mafhum/no-scope",
    )

    assert result.state is MafhumGPTState.DEFERRED
    assert result.failure_code is FailureCode.SCOPE_MISSING


def test_direct_maqam_to_mafhum_transition_is_forbidden() -> None:
    result = GPT_MAFHUM_TRANSITION_CONTRACT.evaluate(
        JumpTestInput(
            source_level="MaqamGPT",
            target_level="MafhumGPT",
            transition_name="direct_implication",
            domain="gpt_reasonableness",
            trace_ref="trace://gpt-r4/jump/direct",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(),
        )
    )

    assert result.allowed is False
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_forbidden_later_outputs_still_absent_after_gpt_r4() -> None:
    import taaqqul_slot_geometry.gpt as gpt_module

    for forbidden in (
        "ReasonablenessVerdict",
        "OriginBindingGate",
        "EvidenceSupportGate",
        "Pipeline",
        "NeedGate",
    ):
        assert not hasattr(gpt_module, forbidden)
