"""Minimal executable L-IR + epistemic circuit breaker experiment surface.

This module provides a bounded, falsifiable runtime harness for:

ArabicWordInContext -> {JAMID, MUSHTAQ, DEFER, BLOCK}

It is intentionally small and deterministic:
proposal/evidence extraction/license decision remain separated.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import IntEnum, StrEnum
from math import sqrt


class LIRSchemaError(TypeError):
    """Raised when the L-IR surface is malformed."""


class LIRCandidateType(StrEnum):
    JAMID = "JAMID"
    MUSHTAQ = "MUSHTAQ"
    UNKNOWN = "UNKNOWN"


class LIRDecisionState(StrEnum):
    PROPOSED = "PROPOSED"
    CLOSE = "CLOSE"
    DEFER = "DEFER"
    BLOCK = "BLOCK"


class EpistemicCircuitBreakerState(StrEnum):
    CLOSED_TRUSTED = "CLOSED_TRUSTED"
    HALF_OPEN = "HALF_OPEN"
    OPEN_BLOCKED = "OPEN_BLOCKED"


class ECWBit(IntEnum):
    SURFACE_CLOSED = 0
    CONTEXT_BOUND = 1
    WORD_CLASS_CLOSED = 2
    PATTERN_CANDIDATE = 3
    DERIVATIONAL_PATH_FOUND = 4
    ORIGIN_EVIDENCE_PRESENT = 5
    LEXICAL_SUPPORT_PRESENT = 6
    CONTEXT_SUPPORT_PRESENT = 7
    PROPER_NAME_RESIDUAL = 8
    TRANSFERRED_USE_RESIDUAL = 9
    SHARED_PATTERN_RESIDUAL = 10
    LEXICAL_GAP_RESIDUAL = 11
    BLOCKING_RESIDUAL = 12
    TRACE_COMPLETE = 13
    HUMAN_REVIEW_REQUIRED = 14
    COMMIT_PERMITTED = 15


@dataclass(frozen=True, slots=True)
class LIRResidualFlags:
    proper_name_possible: bool = False
    transferred_usage_possible: bool = False
    shared_pattern: bool = False
    lexical_gap: bool = False
    contextual_ambiguity: bool = False

    @property
    def has_blocking(self) -> bool:
        return self.proper_name_possible or self.transferred_usage_possible

    @property
    def has_deferrable(self) -> bool:
        return self.shared_pattern or self.lexical_gap or self.contextual_ambiguity


@dataclass(frozen=True, slots=True)
class ArabicWordInContextInput:
    input_id: str
    surface_form: str
    context_ref: str
    candidate_type: LIRCandidateType
    lexical_evidence: tuple[str, ...] = ()
    morphological_evidence: tuple[str, ...] = ()
    derivational_evidence: tuple[str, ...] = ()
    contextual_evidence: tuple[str, ...] = ()
    pattern_candidate: bool = False
    residuals: LIRResidualFlags = LIRResidualFlags()

    def __post_init__(self) -> None:
        _require_nonempty(self.__class__.__name__, "input_id", self.input_id)
        _require_nonempty(self.__class__.__name__, "surface_form", self.surface_form)
        _require_nonempty(self.__class__.__name__, "context_ref", self.context_ref)
        if not isinstance(self.candidate_type, LIRCandidateType):
            raise LIRSchemaError("ArabicWordInContextInput.candidate_type must be LIRCandidateType")
        if not isinstance(self.pattern_candidate, bool):
            raise LIRSchemaError("ArabicWordInContextInput.pattern_candidate must be bool")
        _require_str_tuple(self.__class__.__name__, "lexical_evidence", self.lexical_evidence)
        _require_str_tuple(
            self.__class__.__name__,
            "morphological_evidence",
            self.morphological_evidence,
        )
        _require_str_tuple(
            self.__class__.__name__,
            "derivational_evidence",
            self.derivational_evidence,
        )
        _require_str_tuple(self.__class__.__name__, "contextual_evidence", self.contextual_evidence)
        if not isinstance(self.residuals, LIRResidualFlags):
            raise LIRSchemaError("ArabicWordInContextInput.residuals must be LIRResidualFlags")


@dataclass(frozen=True, slots=True)
class LIRPolicy:
    policy_version: str
    require_origin_evidence_for_mushtaq: bool = True
    max_permitted_rank: int = 3

    def __post_init__(self) -> None:
        _require_nonempty(self.__class__.__name__, "policy_version", self.policy_version)
        if not isinstance(self.require_origin_evidence_for_mushtaq, bool):
            raise LIRSchemaError("LIRPolicy.require_origin_evidence_for_mushtaq must be bool")
        if not isinstance(self.max_permitted_rank, int) or self.max_permitted_rank < 0:
            raise LIRSchemaError("LIRPolicy.max_permitted_rank must be int >= 0")


@dataclass(frozen=True, slots=True)
class LIRGateSnapshot:
    surface_closed: bool
    word_class_closed: bool
    derivation_path_found: bool
    origin_evidence_present: bool
    blocking_exception_absent: bool


@dataclass(frozen=True, slots=True)
class LIRDecision:
    input_id: str
    surface_form: str
    context_ref: str
    candidate_type: LIRCandidateType
    state: LIRDecisionState
    closed_as: LIRCandidateType | None
    gates: LIRGateSnapshot
    residuals: tuple[str, ...]
    proposed_rank: int
    max_permitted_rank: int
    ecw: int
    trace_ref: str
    policy_version: str

    def __post_init__(self) -> None:
        _require_nonempty(self.__class__.__name__, "input_id", self.input_id)
        _require_nonempty(self.__class__.__name__, "surface_form", self.surface_form)
        _require_nonempty(self.__class__.__name__, "context_ref", self.context_ref)
        _require_nonempty(self.__class__.__name__, "trace_ref", self.trace_ref)
        _require_nonempty(self.__class__.__name__, "policy_version", self.policy_version)
        if not isinstance(self.candidate_type, LIRCandidateType):
            raise LIRSchemaError("LIRDecision.candidate_type must be LIRCandidateType")
        if not isinstance(self.state, LIRDecisionState):
            raise LIRSchemaError("LIRDecision.state must be LIRDecisionState")
        if self.closed_as is not None and not isinstance(self.closed_as, LIRCandidateType):
            raise LIRSchemaError("LIRDecision.closed_as must be LIRCandidateType or None")
        if self.state is LIRDecisionState.CLOSE and self.closed_as is None:
            raise LIRSchemaError("LIRDecision.CLOSE requires closed_as")
        if self.state is not LIRDecisionState.CLOSE and self.closed_as is not None:
            raise LIRSchemaError("Only LIRDecision.CLOSE may carry closed_as")
        if not isinstance(self.gates, LIRGateSnapshot):
            raise LIRSchemaError("LIRDecision.gates must be LIRGateSnapshot")
        _require_str_tuple(self.__class__.__name__, "residuals", self.residuals)
        if not isinstance(self.proposed_rank, int) or self.proposed_rank < 0:
            raise LIRSchemaError("LIRDecision.proposed_rank must be int >= 0")
        if not isinstance(self.max_permitted_rank, int) or self.max_permitted_rank < 0:
            raise LIRSchemaError("LIRDecision.max_permitted_rank must be int >= 0")
        if self.max_permitted_rank > self.proposed_rank:
            raise LIRSchemaError("LIRDecision.max_permitted_rank must not exceed proposed_rank")
        if not isinstance(self.ecw, int) or self.ecw < 0 or self.ecw > 0xFFFF:
            raise LIRSchemaError("LIRDecision.ecw must be 16-bit int")

    @property
    def effective_rank(self) -> int:
        return min(self.proposed_rank, self.max_permitted_rank)


@dataclass(frozen=True, slots=True)
class EpistemicCircuitBreaker:
    domain: str
    gate_type: str
    tau_alert: float
    tau_critical: float
    window_size: int
    min_samples: int
    recovery_success_target: int
    registered_max_permitted_rank: int
    max_permitted_rank: int
    state: EpistemicCircuitBreakerState = EpistemicCircuitBreakerState.CLOSED_TRUSTED
    close_outcomes_wrong: tuple[bool, ...] = ()
    consecutive_correct_closures: int = 0

    def __post_init__(self) -> None:
        _require_nonempty(self.__class__.__name__, "domain", self.domain)
        _require_nonempty(self.__class__.__name__, "gate_type", self.gate_type)
        _require_threshold("tau_alert", self.tau_alert)
        _require_threshold("tau_critical", self.tau_critical)
        if not self.tau_alert < self.tau_critical:
            raise LIRSchemaError("tau_alert must be < tau_critical")
        if not isinstance(self.window_size, int) or self.window_size < 1:
            raise LIRSchemaError("window_size must be int >= 1")
        if not isinstance(self.min_samples, int) or self.min_samples < 1:
            raise LIRSchemaError("min_samples must be int >= 1")
        if self.min_samples > self.window_size:
            raise LIRSchemaError("min_samples must be <= window_size")
        if not isinstance(self.recovery_success_target, int) or self.recovery_success_target < 1:
            raise LIRSchemaError("recovery_success_target must be int >= 1")
        if (
            not isinstance(self.registered_max_permitted_rank, int)
            or self.registered_max_permitted_rank < 0
        ):
            raise LIRSchemaError("registered_max_permitted_rank must be int >= 0")
        if not isinstance(self.max_permitted_rank, int) or self.max_permitted_rank < 0:
            raise LIRSchemaError("max_permitted_rank must be int >= 0")
        if self.max_permitted_rank > self.registered_max_permitted_rank:
            raise LIRSchemaError("max_permitted_rank must not exceed registered_max_permitted_rank")
        if not isinstance(self.state, EpistemicCircuitBreakerState):
            raise LIRSchemaError("state must be EpistemicCircuitBreakerState")
        if not isinstance(self.close_outcomes_wrong, tuple):
            raise LIRSchemaError("close_outcomes_wrong must be tuple[bool, ...]")
        for value in self.close_outcomes_wrong:
            if not isinstance(value, bool):
                raise LIRSchemaError("close_outcomes_wrong entries must be bool")
        if len(self.close_outcomes_wrong) > self.window_size:
            raise LIRSchemaError("close_outcomes_wrong length must not exceed window_size")
        if (
            not isinstance(self.consecutive_correct_closures, int)
            or self.consecutive_correct_closures < 0
        ):
            raise LIRSchemaError("consecutive_correct_closures must be int >= 0")


@dataclass(frozen=True, slots=True)
class LIRExperimentSummary:
    total_cases: int
    static_close_count: int
    static_wrong_close_count: int
    static_wcr: float
    static_coverage: float
    breaker_close_count: int
    breaker_wrong_close_count: int
    breaker_wcr: float
    breaker_coverage: float
    final_breaker: EpistemicCircuitBreaker


def evaluate_lir_decision(
    candidate: ArabicWordInContextInput,
    *,
    proposed_rank: int,
    trace_ref: str,
    policy: LIRPolicy,
) -> LIRDecision:
    """Compute deterministic L-IR decision from typed gates + residual policy."""

    _require_nonempty("evaluate_lir_decision", "trace_ref", trace_ref)
    if not isinstance(candidate, ArabicWordInContextInput):
        raise LIRSchemaError("candidate must be ArabicWordInContextInput")
    if not isinstance(policy, LIRPolicy):
        raise LIRSchemaError("policy must be LIRPolicy")
    if not isinstance(proposed_rank, int) or proposed_rank < 0:
        raise LIRSchemaError("proposed_rank must be int >= 0")

    gates = _compute_gates(candidate)
    residuals: list[str] = []
    state = LIRDecisionState.PROPOSED
    closed_as: LIRCandidateType | None = None

    if not gates.surface_closed:
        state = LIRDecisionState.BLOCK
        residuals.append("BLOCKING:SURFACE_IDENTITY_MISSING")
    elif not gates.word_class_closed:
        state = LIRDecisionState.DEFER
        residuals.append("DEFERRED:WORD_CLASS_UNRESOLVED")
    elif not gates.blocking_exception_absent:
        state = LIRDecisionState.BLOCK
        residuals.extend(_blocking_residual_labels(candidate.residuals))
    elif candidate.candidate_type is LIRCandidateType.MUSHTAQ:
        if policy.require_origin_evidence_for_mushtaq and not gates.origin_evidence_present:
            state = LIRDecisionState.BLOCK
            residuals.append("BLOCKING:ORIGIN_EVIDENCE_REQUIRED")
        elif not gates.derivation_path_found:
            state = LIRDecisionState.DEFER
            residuals.append("DEFERRED:DERIVATION_PATH_NOT_PROVEN")
        elif candidate.residuals.has_deferrable:
            state = LIRDecisionState.DEFER
            residuals.extend(_deferrable_residual_labels(candidate.residuals))
        else:
            state = LIRDecisionState.CLOSE
            closed_as = LIRCandidateType.MUSHTAQ
    elif candidate.candidate_type is LIRCandidateType.JAMID:
        if candidate.residuals.has_deferrable:
            state = LIRDecisionState.DEFER
            residuals.extend(_deferrable_residual_labels(candidate.residuals))
        elif not (candidate.lexical_evidence or candidate.contextual_evidence):
            state = LIRDecisionState.DEFER
            residuals.append("DEFERRED:INSUFFICIENT_SUPPORT")
        else:
            state = LIRDecisionState.CLOSE
            closed_as = LIRCandidateType.JAMID
    else:
        state = LIRDecisionState.DEFER
        residuals.append("DEFERRED:UNKNOWN_CANDIDATE_TYPE")

    ecw = _encode_ecw(
        candidate,
        gates,
        state,
        trace_ref,
        human_review=state is not LIRDecisionState.CLOSE,
    )
    return LIRDecision(
        input_id=candidate.input_id,
        surface_form=candidate.surface_form,
        context_ref=candidate.context_ref,
        candidate_type=candidate.candidate_type,
        state=state,
        closed_as=closed_as,
        gates=gates,
        residuals=tuple(residuals),
        proposed_rank=proposed_rank,
        max_permitted_rank=min(proposed_rank, policy.max_permitted_rank),
        ecw=ecw,
        trace_ref=trace_ref,
        policy_version=policy.policy_version,
    )


def apply_epistemic_circuit_breaker(
    decision: LIRDecision,
    breaker: EpistemicCircuitBreaker,
) -> LIRDecision:
    """Apply breaker policy above the gate, never inside the gate logic."""

    if not isinstance(decision, LIRDecision):
        raise LIRSchemaError("decision must be LIRDecision")
    if not isinstance(breaker, EpistemicCircuitBreaker):
        raise LIRSchemaError("breaker must be EpistemicCircuitBreaker")

    if decision.state is not LIRDecisionState.CLOSE:
        return decision
    if breaker.state is EpistemicCircuitBreakerState.OPEN_BLOCKED:
        residuals = (*decision.residuals, "ECB:OPEN_BLOCKED_FORCE_DEFER")
        ecw = decision.ecw | (1 << ECWBit.HUMAN_REVIEW_REQUIRED)
        ecw = ecw & ~(1 << ECWBit.COMMIT_PERMITTED)
        return replace(
            decision,
            state=LIRDecisionState.DEFER,
            closed_as=None,
            residuals=residuals,
            max_permitted_rank=min(decision.max_permitted_rank, breaker.max_permitted_rank),
            ecw=ecw,
        )
    if breaker.state is EpistemicCircuitBreakerState.HALF_OPEN:
        clamped_rank = min(decision.max_permitted_rank, breaker.max_permitted_rank)
        if clamped_rank < decision.max_permitted_rank:
            residuals = (*decision.residuals, "ECB:HALF_OPEN_RANK_DOWNGRADE")
            return replace(decision, max_permitted_rank=clamped_rank, residuals=residuals)
    return decision


def observe_breaker_close_outcome(
    breaker: EpistemicCircuitBreaker,
    *,
    close_was_wrong: bool,
) -> EpistemicCircuitBreaker:
    """Update breaker from one observed CLOSE outcome."""

    if not isinstance(breaker, EpistemicCircuitBreaker):
        raise LIRSchemaError("breaker must be EpistemicCircuitBreaker")
    if not isinstance(close_was_wrong, bool):
        raise LIRSchemaError("close_was_wrong must be bool")

    outcomes = (*breaker.close_outcomes_wrong, close_was_wrong)[-breaker.window_size :]
    consecutive_correct = 0 if close_was_wrong else breaker.consecutive_correct_closures + 1

    total = len(outcomes)
    wrong = sum(1 for item in outcomes if item)
    ucb = _wilson_upper_bound(wrong=wrong, total=total)
    observed_wrong_rate = (wrong / total) if total else 0.0

    state = breaker.state
    max_rank = breaker.max_permitted_rank

    if (
        total >= breaker.min_samples
        and state
        in (
            EpistemicCircuitBreakerState.HALF_OPEN,
            EpistemicCircuitBreakerState.OPEN_BLOCKED,
        )
        and not close_was_wrong
        and consecutive_correct >= breaker.recovery_success_target
        and observed_wrong_rate <= breaker.tau_alert
    ):
        return replace(
            breaker,
            state=EpistemicCircuitBreakerState.CLOSED_TRUSTED,
            max_permitted_rank=breaker.registered_max_permitted_rank,
            close_outcomes_wrong=outcomes,
            consecutive_correct_closures=consecutive_correct,
        )

    if total >= breaker.min_samples:
        if ucb > breaker.tau_critical:
            state = EpistemicCircuitBreakerState.OPEN_BLOCKED
            if close_was_wrong:
                max_rank = max(0, min(max_rank, breaker.registered_max_permitted_rank) - 1)
                consecutive_correct = 0
        elif ucb > breaker.tau_alert:
            state = EpistemicCircuitBreakerState.HALF_OPEN
            max_rank = max(1, min(max_rank, breaker.registered_max_permitted_rank) - 1)
        elif state in (
            EpistemicCircuitBreakerState.HALF_OPEN,
            EpistemicCircuitBreakerState.OPEN_BLOCKED,
        ) and (
            consecutive_correct >= breaker.recovery_success_target
            and observed_wrong_rate <= breaker.tau_alert
        ):
            state = EpistemicCircuitBreakerState.CLOSED_TRUSTED
            max_rank = breaker.registered_max_permitted_rank

    return replace(
        breaker,
        state=state,
        max_permitted_rank=max_rank,
        close_outcomes_wrong=outcomes,
        consecutive_correct_closures=consecutive_correct,
    )


def run_falsifiable_lir_experiment(
    *,
    wrong_close_stream: tuple[bool, ...],
    candidate: ArabicWordInContextInput,
    policy: LIRPolicy,
    breaker: EpistemicCircuitBreaker,
    proposed_rank: int,
) -> LIRExperimentSummary:
    """Compare static licensing vs breaker-governed licensing on same stream."""

    if not isinstance(wrong_close_stream, tuple) or not wrong_close_stream:
        raise LIRSchemaError("wrong_close_stream must be non-empty tuple[bool, ...]")
    for item in wrong_close_stream:
        if not isinstance(item, bool):
            raise LIRSchemaError("wrong_close_stream entries must be bool")

    static_close = 0
    static_wrong = 0
    breaker_close = 0
    breaker_wrong = 0
    live_breaker = breaker

    for idx, is_wrong in enumerate(wrong_close_stream, start=1):
        static_decision = evaluate_lir_decision(
            candidate,
            proposed_rank=proposed_rank,
            trace_ref=f"trace://lir/static/{idx}",
            policy=policy,
        )
        if static_decision.state is LIRDecisionState.CLOSE:
            static_close += 1
            static_wrong += int(is_wrong)

        breaker_decision = evaluate_lir_decision(
            candidate,
            proposed_rank=proposed_rank,
            trace_ref=f"trace://lir/breaker/{idx}",
            policy=policy,
        )
        breaker_decision = apply_epistemic_circuit_breaker(breaker_decision, live_breaker)
        if breaker_decision.state is LIRDecisionState.CLOSE:
            breaker_close += 1
            breaker_wrong += int(is_wrong)
            live_breaker = observe_breaker_close_outcome(live_breaker, close_was_wrong=is_wrong)

    total = len(wrong_close_stream)
    static_wcr = (static_wrong / static_close) if static_close else 0.0
    static_coverage = static_close / total
    breaker_wcr = (breaker_wrong / breaker_close) if breaker_close else 0.0
    breaker_coverage = breaker_close / total
    return LIRExperimentSummary(
        total_cases=total,
        static_close_count=static_close,
        static_wrong_close_count=static_wrong,
        static_wcr=static_wcr,
        static_coverage=static_coverage,
        breaker_close_count=breaker_close,
        breaker_wrong_close_count=breaker_wrong,
        breaker_wcr=breaker_wcr,
        breaker_coverage=breaker_coverage,
        final_breaker=live_breaker,
    )


def _compute_gates(candidate: ArabicWordInContextInput) -> LIRGateSnapshot:
    return LIRGateSnapshot(
        surface_closed=bool(candidate.surface_form.strip()),
        word_class_closed=candidate.candidate_type is not LIRCandidateType.UNKNOWN,
        derivation_path_found=bool(candidate.derivational_evidence),
        origin_evidence_present=bool(candidate.morphological_evidence),
        blocking_exception_absent=not candidate.residuals.has_blocking,
    )


def _encode_ecw(
    candidate: ArabicWordInContextInput,
    gates: LIRGateSnapshot,
    state: LIRDecisionState,
    trace_ref: str,
    *,
    human_review: bool,
) -> int:
    word = 0
    word = _set_bit(word, ECWBit.SURFACE_CLOSED, gates.surface_closed)
    word = _set_bit(word, ECWBit.CONTEXT_BOUND, bool(candidate.context_ref.strip()))
    word = _set_bit(word, ECWBit.WORD_CLASS_CLOSED, gates.word_class_closed)
    word = _set_bit(word, ECWBit.PATTERN_CANDIDATE, candidate.pattern_candidate)
    word = _set_bit(word, ECWBit.DERIVATIONAL_PATH_FOUND, gates.derivation_path_found)
    word = _set_bit(word, ECWBit.ORIGIN_EVIDENCE_PRESENT, gates.origin_evidence_present)
    word = _set_bit(word, ECWBit.LEXICAL_SUPPORT_PRESENT, bool(candidate.lexical_evidence))
    word = _set_bit(word, ECWBit.CONTEXT_SUPPORT_PRESENT, bool(candidate.contextual_evidence))
    word = _set_bit(word, ECWBit.PROPER_NAME_RESIDUAL, candidate.residuals.proper_name_possible)
    word = _set_bit(
        word,
        ECWBit.TRANSFERRED_USE_RESIDUAL,
        candidate.residuals.transferred_usage_possible,
    )
    word = _set_bit(word, ECWBit.SHARED_PATTERN_RESIDUAL, candidate.residuals.shared_pattern)
    word = _set_bit(word, ECWBit.LEXICAL_GAP_RESIDUAL, candidate.residuals.lexical_gap)
    word = _set_bit(word, ECWBit.BLOCKING_RESIDUAL, candidate.residuals.has_blocking)
    word = _set_bit(word, ECWBit.TRACE_COMPLETE, bool(trace_ref.strip()))
    word = _set_bit(word, ECWBit.HUMAN_REVIEW_REQUIRED, human_review)
    word = _set_bit(
        word,
        ECWBit.COMMIT_PERMITTED,
        state is LIRDecisionState.CLOSE and not human_review,
    )
    return word


def _set_bit(word: int, bit: ECWBit, value: bool) -> int:
    return (word | (1 << int(bit))) if value else (word & ~(1 << int(bit)))


def _wilson_upper_bound(*, wrong: int, total: int, z: float = 1.96) -> float:
    if total == 0:
        return 0.0
    p_hat = wrong / total
    z2 = z * z
    denom = 1.0 + (z2 / total)
    center = p_hat + (z2 / (2.0 * total))
    margin = z * sqrt((p_hat * (1.0 - p_hat) / total) + (z2 / (4.0 * total * total)))
    return (center + margin) / denom


def _blocking_residual_labels(flags: LIRResidualFlags) -> tuple[str, ...]:
    labels: list[str] = []
    if flags.proper_name_possible:
        labels.append("BLOCKING:PROPER_NAME_POSSIBLE")
    if flags.transferred_usage_possible:
        labels.append("BLOCKING:TRANSFERRED_USAGE_POSSIBLE")
    return tuple(labels)


def _deferrable_residual_labels(flags: LIRResidualFlags) -> tuple[str, ...]:
    labels: list[str] = []
    if flags.shared_pattern:
        labels.append("DEFERRED:SHARED_PATTERN")
    if flags.lexical_gap:
        labels.append("DEFERRED:LEXICAL_GAP")
    if flags.contextual_ambiguity:
        labels.append("DEFERRED:CONTEXTUAL_AMBIGUITY")
    return tuple(labels)


def _require_nonempty(owner: str, field: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise LIRSchemaError(f"{owner}.{field} must be a non-empty string")


def _require_str_tuple(owner: str, field: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise LIRSchemaError(f"{owner}.{field} must be tuple[str, ...]")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise LIRSchemaError(f"{owner}.{field} entries must be non-empty strings")


def _require_threshold(name: str, value: float) -> None:
    if not isinstance(value, float) or not (0.0 < value < 1.0):
        raise LIRSchemaError(f"{name} must be float in (0, 1)")
