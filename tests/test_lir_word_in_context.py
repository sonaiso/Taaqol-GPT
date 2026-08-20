"""Constitutional tests for minimal executable L-IR + breaker experiment.

Origin law          : docs/53 + docs/115 (bounded falsifiable closure discipline)
Branch name         : L-IR ArabicWordInContext minimal executable surface
Constitutional chain: docs/53 -> docs/115 -> x0r/lir_word_in_context.py
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r.lir_word_in_context import (
    ArabicWordInContextInput,
    ECWBit,
    EpistemicCircuitBreaker,
    EpistemicCircuitBreakerState,
    LIRCandidateType,
    LIRDecisionState,
    LIRPolicy,
    LIRResidualFlags,
    apply_epistemic_circuit_breaker,
    evaluate_lir_decision,
    observe_breaker_close_outcome,
    run_falsifiable_lir_experiment,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

ORIGIN_LAW = "docs/53 + docs/115 (bounded falsifiable closure discipline)"
BRANCH_NAME = "L-IR ArabicWordInContext minimal executable surface"
CONSTITUTIONAL_CHAIN = ("docs/53", "docs/115", "x0r/lir_word_in_context.py")


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law=ORIGIN_LAW,
        branch_name=branch_name,
        constitutional_chain=CONSTITUTIONAL_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("UnlicensedClosure",),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _candidate(
    *,
    candidate_type: LIRCandidateType = LIRCandidateType.MUSHTAQ,
    morphological_evidence: tuple[str, ...] = ("origin:lemma:علم",),
    derivational_evidence: tuple[str, ...] = ("path:masdar->form",),
    lexical_evidence: tuple[str, ...] = ("lexicon:علم",),
    contextual_evidence: tuple[str, ...] = ("ctx:verb-compatible",),
    residuals: LIRResidualFlags = LIRResidualFlags(),
    pattern_candidate: bool = True,
) -> ArabicWordInContextInput:
    return ArabicWordInContextInput(
        input_id="w1",
        surface_form="عالم",
        context_ref="c1",
        candidate_type=candidate_type,
        lexical_evidence=lexical_evidence,
        morphological_evidence=morphological_evidence,
        derivational_evidence=derivational_evidence,
        contextual_evidence=contextual_evidence,
        pattern_candidate=pattern_candidate,
        residuals=residuals,
    )


def _policy() -> LIRPolicy:
    return LIRPolicy(policy_version="lir-v0", require_origin_evidence_for_mushtaq=True)


def test_declares_identity_fields_for_lir_surface() -> None:
    _declare("identity declaration")
    assert ORIGIN_LAW
    assert BRANCH_NAME
    assert CONSTITUTIONAL_CHAIN


def test_pattern_match_alone_does_not_close_mushtaq() -> None:
    decision = evaluate_lir_decision(
        _candidate(
            morphological_evidence=("origin:lemma:علم",),
            derivational_evidence=(),
            pattern_candidate=True,
        ),
        proposed_rank=3,
        trace_ref="trace://lir/1",
        policy=_policy(),
    )

    assert decision.state is LIRDecisionState.DEFER
    assert decision.closed_as is None
    assert "DEFERRED:DERIVATION_PATH_NOT_PROVEN" in decision.residuals


def test_mushtaq_blocks_without_origin_evidence_when_policy_requires_it() -> None:
    decision = evaluate_lir_decision(
        _candidate(morphological_evidence=()),
        proposed_rank=3,
        trace_ref="trace://lir/2",
        policy=_policy(),
    )

    assert decision.state is LIRDecisionState.BLOCK
    assert "BLOCKING:ORIGIN_EVIDENCE_REQUIRED" in decision.residuals


def test_mushtaq_closes_when_all_five_gates_pass() -> None:
    decision = evaluate_lir_decision(
        _candidate(),
        proposed_rank=3,
        trace_ref="trace://lir/3",
        policy=_policy(),
    )

    assert decision.state is LIRDecisionState.CLOSE
    assert decision.closed_as is LIRCandidateType.MUSHTAQ
    assert decision.gates.surface_closed
    assert decision.gates.word_class_closed
    assert decision.gates.derivation_path_found
    assert decision.gates.origin_evidence_present
    assert decision.gates.blocking_exception_absent


def test_blocking_residual_forces_block_and_sets_ecw_block_bit() -> None:
    decision = evaluate_lir_decision(
        _candidate(
            residuals=LIRResidualFlags(
                proper_name_possible=True,
                transferred_usage_possible=False,
                shared_pattern=False,
                lexical_gap=False,
                contextual_ambiguity=False,
            )
        ),
        proposed_rank=3,
        trace_ref="trace://lir/4",
        policy=_policy(),
    )

    assert decision.state is LIRDecisionState.BLOCK
    assert decision.ecw & (1 << ECWBit.BLOCKING_RESIDUAL)
    assert decision.ecw & (1 << ECWBit.HUMAN_REVIEW_REQUIRED)
    assert not decision.ecw & (1 << ECWBit.COMMIT_PERMITTED)


def test_breaker_open_blocked_forces_close_to_defer() -> None:
    close_decision = evaluate_lir_decision(
        _candidate(),
        proposed_rank=3,
        trace_ref="trace://lir/5",
        policy=_policy(),
    )
    breaker = EpistemicCircuitBreaker(
        domain="ARABIC_MORPHOLOGY",
        gate_type="LIR_MUSHTAQ_JAMID",
        tau_alert=0.25,
        tau_critical=0.5,
        window_size=8,
        min_samples=4,
        recovery_success_target=3,
        registered_max_permitted_rank=3,
        max_permitted_rank=1,
        state=EpistemicCircuitBreakerState.OPEN_BLOCKED,
    )
    gated = apply_epistemic_circuit_breaker(close_decision, breaker)

    assert gated.state is LIRDecisionState.DEFER
    assert gated.closed_as is None
    assert "ECB:OPEN_BLOCKED_FORCE_DEFER" in gated.residuals


def test_breaker_enters_open_blocked_when_recent_wrong_closures_are_high() -> None:
    breaker = EpistemicCircuitBreaker(
        domain="ARABIC_MORPHOLOGY",
        gate_type="LIR_MUSHTAQ_JAMID",
        tau_alert=0.25,
        tau_critical=0.5,
        window_size=8,
        min_samples=4,
        recovery_success_target=3,
        registered_max_permitted_rank=3,
        max_permitted_rank=3,
    )

    updated = breaker
    for _ in range(4):
        updated = observe_breaker_close_outcome(updated, close_was_wrong=True)

    assert updated.state is EpistemicCircuitBreakerState.OPEN_BLOCKED
    assert updated.max_permitted_rank <= 2


def test_breaker_can_recover_after_half_open_correct_streak() -> None:
    breaker = EpistemicCircuitBreaker(
        domain="ARABIC_MORPHOLOGY",
        gate_type="LIR_MUSHTAQ_JAMID",
        tau_alert=0.25,
        tau_critical=0.5,
        window_size=8,
        min_samples=4,
        recovery_success_target=3,
        registered_max_permitted_rank=3,
        max_permitted_rank=3,
    )
    for _ in range(4):
        breaker = observe_breaker_close_outcome(breaker, close_was_wrong=True)
    assert breaker.state is EpistemicCircuitBreakerState.OPEN_BLOCKED

    for _ in range(6):
        breaker = observe_breaker_close_outcome(breaker, close_was_wrong=False)

    assert breaker.state is EpistemicCircuitBreakerState.CLOSED_TRUSTED
    assert breaker.max_permitted_rank == 3


def test_falsifiable_experiment_shows_safety_coverage_tradeoff() -> None:
    breaker = EpistemicCircuitBreaker(
        domain="ARABIC_MORPHOLOGY",
        gate_type="LIR_MUSHTAQ_JAMID",
        tau_alert=0.25,
        tau_critical=0.5,
        window_size=10,
        min_samples=4,
        recovery_success_target=3,
        registered_max_permitted_rank=3,
        max_permitted_rank=3,
    )
    outcomes = (True, True, True, True, True, True, False, False, False, False, False, False)
    summary = run_falsifiable_lir_experiment(
        wrong_close_stream=outcomes,
        candidate=_candidate(),
        policy=_policy(),
        breaker=breaker,
        proposed_rank=3,
    )

    assert summary.static_wrong_close_count > summary.breaker_wrong_close_count
    assert summary.breaker_coverage < summary.static_coverage
