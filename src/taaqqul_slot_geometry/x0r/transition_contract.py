"""PR-X0R runtime contract hooks (no linguistic runtime inference)."""

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


class TransitionReadinessState(StrEnum):
    """Constitutional readiness states for transition surfaces."""

    LINK_READY = "LINK_READY"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REFUSED = "REFUSED"


class EuclideanGateStage(StrEnum):
    """Ordered constitutional stages for Euclidean transition evaluation."""

    DOMAIN = "DOMAIN"
    TRACE = "TRACE"
    IDENTITY = "IDENTITY"
    MINIMUM_COMPLETE = "MINIMUM_COMPLETE"
    ORIGIN = "ORIGIN"
    BRANCH = "BRANCH"
    EFFECTIVE_DESCRIPTION = "EFFECTIVE_DESCRIPTION"
    DIFFERENTIATING_FEATURE = "DIFFERENTIATING_FEATURE"
    COMMON_ILLAH = "COMMON_ILLAH"
    QADIH = "QADIH"
    CONDITION = "CONDITION"
    SABAB = "SABAB"
    MANI = "MANI"
    EVIDENCE = "EVIDENCE"
    RANK_CEILING = "RANK_CEILING"
    RESIDUALS = "RESIDUALS"
    HANDOFF = "HANDOFF"


class QadihCheckStatus(StrEnum):
    """Explicit qadih check status table (no boolean ambiguity)."""

    UNCHECKED = "UNCHECKED"
    BLOCKING = "BLOCKING"
    CLEAR = "CLEAR"
    RESIDUAL = "RESIDUAL"


@dataclass(frozen=True, slots=True)
class OriginProof:
    """Origin proof carrier for constitutional origin validity."""

    origin_ref: str
    preserved_identity: bool
    domain: str
    trace_ref: str
    rank: int
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "origin_ref", self.origin_ref)
        _require_bool(cls, "preserved_identity", self.preserved_identity)
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_int(cls, "rank", self.rank)
        _require_tuple(cls, "residuals", self.residuals)
        for residual in self.residuals:
            _require_str(cls, "residuals entry", residual)


@dataclass(frozen=True, slots=True)
class BranchProof:
    """Branch proof carrier for constitutional branch validity."""

    branch_ref: str
    domain: str
    trace_ref: str
    rank: int
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "branch_ref", self.branch_ref)
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_int(cls, "rank", self.rank)
        _require_tuple(cls, "residuals", self.residuals)
        for residual in self.residuals:
            _require_str(cls, "residuals entry", residual)


@dataclass(frozen=True, slots=True)
class OriginBranchLinkProof:
    """Bidirectional origin/branch linking proof carrier."""

    origin_ref: str
    branch_ref: str
    origin_to_branch_linked: bool = True
    branch_to_origin_linked: bool = True
    reversible_to_origin: bool = True

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "origin_ref", self.origin_ref)
        _require_str(cls, "branch_ref", self.branch_ref)
        _require_bool(cls, "origin_to_branch_linked", self.origin_to_branch_linked)
        _require_bool(cls, "branch_to_origin_linked", self.branch_to_origin_linked)
        _require_bool(cls, "reversible_to_origin", self.reversible_to_origin)


@dataclass(frozen=True, slots=True)
class DifferentiatingFeatureProof:
    """Differentiating-feature proof carrier required by LAW-E0."""

    feature_ref: str
    verified: bool = True

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "feature_ref", self.feature_ref)
        _require_bool(cls, "verified", self.verified)


@dataclass(frozen=True, slots=True)
class RankForceCeiling:
    """Rank-force ceiling carriers; output rank cannot exceed their meet."""

    evidence_rank: int
    identity_rank: int
    gate_rank: int
    closure_rank: int
    residual_rank_ceiling: int
    explicit_rank_ceiling: int | None = None

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_int(cls, "evidence_rank", self.evidence_rank)
        _require_int(cls, "identity_rank", self.identity_rank)
        _require_int(cls, "gate_rank", self.gate_rank)
        _require_int(cls, "closure_rank", self.closure_rank)
        _require_int(cls, "residual_rank_ceiling", self.residual_rank_ceiling)
        if self.explicit_rank_ceiling is not None:
            _require_int(cls, "explicit_rank_ceiling", self.explicit_rank_ceiling)

    def meet_ceiling(self) -> int:
        values = [
            self.evidence_rank,
            self.identity_rank,
            self.gate_rank,
            self.closure_rank,
            self.residual_rank_ceiling,
        ]
        if self.explicit_rank_ceiling is not None:
            values.append(self.explicit_rank_ceiling)
        return min(values)


@dataclass(frozen=True, slots=True)
class JumpTestInput:
    """Input surface for a single transition jump test."""

    source_level: str
    target_level: str
    transition_name: str
    domain: str
    trace_ref: str
    origin: str
    branch: str
    handoff: str
    rank: int
    rank_ceiling: int | None
    sufficiency: bool
    necessity: bool
    preserved_trace: bool
    residual_visible: bool
    differentiating_feature_verified: bool
    qadih_status: QadihCheckStatus
    residual_kinds: tuple[ResidualKind, ...]
    blocking_residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "source_level", self.source_level)
        _require_str(cls, "target_level", self.target_level)
        _require_str(cls, "transition_name", self.transition_name)
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_str(cls, "origin", self.origin)
        _require_str(cls, "branch", self.branch)
        _require_str(cls, "handoff", self.handoff)
        _require_int(cls, "rank", self.rank)
        if self.rank_ceiling is not None:
            _require_int(cls, "rank_ceiling", self.rank_ceiling)
        _require_bool(cls, "sufficiency", self.sufficiency)
        _require_bool(cls, "necessity", self.necessity)
        _require_bool(cls, "preserved_trace", self.preserved_trace)
        _require_bool(cls, "residual_visible", self.residual_visible)
        _require_bool(
            cls,
            "differentiating_feature_verified",
            self.differentiating_feature_verified,
        )
        if not isinstance(self.qadih_status, QadihCheckStatus):
            raise JumpTestContractError(f"{cls}.qadih_status must be QadihCheckStatus")
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
    readiness_state: TransitionReadinessState
    failure_code: FailureCode | None
    failed_stage: EuclideanGateStage | None
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
        if not isinstance(self.readiness_state, TransitionReadinessState):
            raise JumpTestContractError(
                f"{cls}.readiness_state must be a TransitionReadinessState member"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise JumpTestContractError(f"{cls}.failure_code must be a FailureCode member or None")
        if self.failed_stage is not None and not isinstance(self.failed_stage, EuclideanGateStage):
            raise JumpTestContractError(
                f"{cls}.failed_stage must be a EuclideanGateStage member or None"
            )
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
        if self.allowed and self.readiness_state is not TransitionReadinessState.LINK_READY:
            raise JumpTestContractError(
                f"{cls}.allowed=True requires readiness_state=LINK_READY"
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

        key = (jump.source_level, jump.target_level, jump.transition_name, jump.domain)

        if not jump.domain.strip():
            return self._decide(
                jump,
                TransitionReadinessState.REFUSED,
                FailureCode.DOMAIN_MISSING,
                EuclideanGateStage.DOMAIN,
            )
        if not jump.trace_ref.strip() or not jump.preserved_trace:
            return self._decide(
                jump,
                TransitionReadinessState.REFUSED,
                FailureCode.TRACE_MISSING,
                EuclideanGateStage.TRACE,
            )
        if not jump.origin.strip() or key not in self.declared_transitions:
            return self._decide(
                jump,
                TransitionReadinessState.REFUSED,
                FailureCode.FORBIDDEN_STRAIGHT_LINE,
                EuclideanGateStage.ORIGIN,
            )
        if not jump.branch.strip():
            return self._decide(
                jump,
                TransitionReadinessState.REFUSED,
                FailureCode.FORBIDDEN_STRAIGHT_LINE,
                EuclideanGateStage.BRANCH,
            )
        if not jump.differentiating_feature_verified:
            return self._decide(
                jump,
                TransitionReadinessState.DEFERRED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.DIFFERENTIATING_FEATURE,
            )

        qadih_decision = _qadih_decision(jump.qadih_status)
        if qadih_decision is not None:
            state, code = qadih_decision
            return self._decide(jump, state, code, EuclideanGateStage.QADIH)

        if not jump.sufficiency or not jump.necessity:
            return self._decide(
                jump,
                TransitionReadinessState.DEFERRED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.EVIDENCE,
            )

        if jump.rank_ceiling is not None and jump.rank > jump.rank_ceiling:
            return self._decide(
                jump,
                TransitionReadinessState.REFUSED,
                FailureCode.RANK_EXCEEDS_CEILING,
                EuclideanGateStage.RANK_CEILING,
            )
        if not jump.residual_visible:
            return self._decide(
                jump,
                TransitionReadinessState.REFUSED,
                FailureCode.HIDDEN_RESIDUAL,
                EuclideanGateStage.RESIDUALS,
            )
        if jump.blocking_residuals or any(
            kind in {ResidualKind.BLOCKING, ResidualKind.CONTRADICTORY}
            for kind in jump.residual_kinds
        ):
            return self._decide(
                jump,
                TransitionReadinessState.BLOCKED,
                FailureCode.BLOCKING_RESIDUAL_PRESENT,
                EuclideanGateStage.RESIDUALS,
            )

        if not jump.handoff.strip():
            return self._decide(
                jump,
                TransitionReadinessState.REFUSED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.HANDOFF,
            )

        return JumpTestResult(
            allowed=True,
            readiness_state=TransitionReadinessState.LINK_READY,
            failure_code=None,
            failed_stage=None,
            domain=jump.domain,
            trace_ref=jump.trace_ref,
            transition_name=jump.transition_name,
            source_level=jump.source_level,
            target_level=jump.target_level,
            residual_policy=self.residual_policy,
            residual_kinds=jump.residual_kinds,
            blocking_residuals=jump.blocking_residuals,
        )

    def _decide(
        self,
        jump: JumpTestInput,
        state: TransitionReadinessState,
        code: FailureCode,
        stage: EuclideanGateStage,
    ) -> JumpTestResult:
        return JumpTestResult(
            allowed=False,
            readiness_state=state,
            failure_code=code,
            failed_stage=stage,
            domain=jump.domain,
            trace_ref=jump.trace_ref,
            transition_name=jump.transition_name,
            source_level=jump.source_level,
            target_level=jump.target_level,
            residual_policy=self.residual_policy,
            residual_kinds=jump.residual_kinds,
            blocking_residuals=jump.blocking_residuals,
        )


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
        """Check minimum-complete law without raising layer or verdict tier."""

        if rank > self.current_stage_rank:
            return False
        if self.max_required_stage_rank > self.current_stage_rank:
            return False
        if self.missing_requirements:
            return False
        if self.rank_ceiling is not None and rank > self.rank_ceiling:
            return False
        return not (
            self.requested_state == "licensed" and self.candidate_or_deferred_sufficient
        )

    def closest_valid_stage(self) -> int:
        return min(self.current_stage_rank, self.max_required_stage_rank)


@dataclass(frozen=True, slots=True)
class EuclideanLearningEvidence:
    """Learning evidence carrier for transition-contract tuning (no verdict leak)."""

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
    """Structured failure record for refused Euclidean transitions."""

    failed_transition: bool
    readiness_state: TransitionReadinessState
    failed_stage: EuclideanGateStage | None
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
    readiness_state: TransitionReadinessState
    failed_stage: EuclideanGateStage | None
    failure_code: FailureCode | None
    rank: int
    residuals: tuple[str, ...]
    handoff: str


@dataclass(frozen=True, slots=True)
class RankedBranchPrediction:
    """Ranked branch expectation (prediction-only, never final judgment)."""

    predicted_branch: str
    predicted_rank: int
    residuals: tuple[str, ...]
    decision: EuclideanGateDecision
    is_final_judgment: bool = False
    predicts_next_token: bool = False


@dataclass(frozen=True, slots=True)
class EuclideanTransitionContract:
    """General Euclidean transition contract linking origin and branch."""

    domain: str
    trace_ref: str
    origin_proof: OriginProof
    branch_proof: BranchProof
    linking_proof: OriginBranchLinkProof
    differentiating_feature: DifferentiatingFeatureProof
    common_illah: str
    effective_description: str
    qadih_status: QadihCheckStatus
    condition: bool
    sabab: bool
    preventer: bool
    evidence_refs: tuple[str, ...]
    residuals: tuple[str, ...]
    rank: int
    minimal_complete_requirement: MinimalCompleteRequirement
    rank_force_ceiling: RankForceCeiling
    handoff: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "trace_ref", self.trace_ref)
        if not isinstance(self.origin_proof, OriginProof):
            raise JumpTestContractError(f"{cls}.origin_proof must be OriginProof")
        if not isinstance(self.branch_proof, BranchProof):
            raise JumpTestContractError(f"{cls}.branch_proof must be BranchProof")
        if not isinstance(self.linking_proof, OriginBranchLinkProof):
            raise JumpTestContractError(f"{cls}.linking_proof must be OriginBranchLinkProof")
        if not isinstance(self.differentiating_feature, DifferentiatingFeatureProof):
            raise JumpTestContractError(
                f"{cls}.differentiating_feature must be DifferentiatingFeatureProof"
            )
        _require_str(cls, "common_illah", self.common_illah)
        _require_str(cls, "effective_description", self.effective_description)
        if not isinstance(self.qadih_status, QadihCheckStatus):
            raise JumpTestContractError(f"{cls}.qadih_status must be QadihCheckStatus")
        _require_bool(cls, "condition", self.condition)
        _require_bool(cls, "sabab", self.sabab)
        _require_bool(cls, "preventer", self.preventer)
        _require_tuple(cls, "evidence_refs", self.evidence_refs)
        for evidence in self.evidence_refs:
            _require_str(cls, "evidence_refs entry", evidence)
        _require_tuple(cls, "residuals", self.residuals)
        for residual in self.residuals:
            _require_str(cls, "residuals entry", residual)
        _require_int(cls, "rank", self.rank)
        if not isinstance(self.minimal_complete_requirement, MinimalCompleteRequirement):
            raise JumpTestContractError(
                f"{cls}.minimal_complete_requirement must be MinimalCompleteRequirement"
            )
        if not isinstance(self.rank_force_ceiling, RankForceCeiling):
            raise JumpTestContractError(f"{cls}.rank_force_ceiling must be RankForceCeiling")
        _require_str(cls, "handoff", self.handoff)

    def has_preserved_identity(self) -> bool:
        return self.origin_proof.preserved_identity

    def has_common_illah(self) -> bool:
        return bool(self.common_illah.strip())

    def has_effective_description(self) -> bool:
        return bool(self.effective_description.strip())

    def condition_is_satisfied(self) -> bool:
        return self.condition

    def sabab_is_active(self) -> bool:
        return self.sabab

    def preventer_is_absent(self) -> bool:
        return not self.preventer

    def minimal_complete_is_satisfied(self) -> bool:
        return self.minimal_complete_requirement.is_satisfied_for_rank(self.rank)

    def force_rank_ceiling(self) -> int:
        minimal_rank_ceiling = self.minimal_complete_requirement.current_stage_rank
        if self.minimal_complete_requirement.rank_ceiling is not None:
            minimal_rank_ceiling = min(
                minimal_rank_ceiling,
                self.minimal_complete_requirement.rank_ceiling,
            )
        return min(self.rank_force_ceiling.meet_ceiling(), minimal_rank_ceiling)

    def evaluate_gate(self) -> EuclideanGateDecision:
        """Evaluate according to the constitutional 17-stage order."""

        decision = self._run_stage_checks()
        if decision is not None:
            return decision
        return EuclideanGateDecision(
            transition_allowed=True,
            readiness_state=TransitionReadinessState.LINK_READY,
            failed_stage=None,
            failure_code=None,
            rank=self.rank,
            residuals=self.residuals,
            handoff=self.handoff,
        )

    def can_transition(self) -> bool:
        return self.evaluate_gate().transition_allowed

    def to_failure_record(self) -> EuclideanFailureRecord:
        missing = self._missing_conditions()
        blocking = self._blocking_residuals()
        decision = self.evaluate_gate()
        failed = not decision.transition_allowed
        return EuclideanFailureRecord(
            failed_transition=failed,
            readiness_state=decision.readiness_state,
            failed_stage=decision.failed_stage,
            missing_condition=tuple(missing),
            active_preventer=not self.preventer_is_absent(),
            blocking_residual=tuple(blocking),
            closest_valid_stage=self.minimal_complete_requirement.closest_valid_stage(),
            required_handoff=self.handoff,
            repair_suggestion=self._repair_suggestion(missing, blocking),
            failure_code=decision.failure_code,
        )

    def predict_branch_ranked(self) -> RankedBranchPrediction:
        decision = self.evaluate_gate()
        return RankedBranchPrediction(
            predicted_branch=self.branch_proof.branch_ref,
            predicted_rank=decision.rank,
            residuals=self.residuals,
            decision=decision,
            is_final_judgment=False,
            predicts_next_token=False,
        )

    def _run_stage_checks(self) -> EuclideanGateDecision | None:
        if not self.domain.strip():
            return self._decision(
                TransitionReadinessState.REFUSED,
                FailureCode.DOMAIN_MISSING,
                EuclideanGateStage.DOMAIN,
            )
        if not self.trace_ref.strip():
            return self._decision(
                TransitionReadinessState.REFUSED,
                FailureCode.TRACE_MISSING,
                EuclideanGateStage.TRACE,
            )
        if not self.has_preserved_identity():
            return self._decision(
                TransitionReadinessState.REFUSED,
                FailureCode.IDENTITY_BROKEN,
                EuclideanGateStage.IDENTITY,
            )
        if not self.minimal_complete_is_satisfied():
            return self._decision(
                TransitionReadinessState.DEFERRED,
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
                EuclideanGateStage.MINIMUM_COMPLETE,
            )
        if not self._origin_is_valid():
            return self._decision(
                TransitionReadinessState.REFUSED,
                FailureCode.FORBIDDEN_STRAIGHT_LINE,
                EuclideanGateStage.ORIGIN,
            )
        if not self._branch_is_valid():
            return self._decision(
                TransitionReadinessState.REFUSED,
                FailureCode.FORBIDDEN_STRAIGHT_LINE,
                EuclideanGateStage.BRANCH,
            )
        if not self.has_effective_description():
            return self._decision(
                TransitionReadinessState.REFUSED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.EFFECTIVE_DESCRIPTION,
            )
        if not self.differentiating_feature.verified:
            return self._decision(
                TransitionReadinessState.DEFERRED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.DIFFERENTIATING_FEATURE,
            )
        if not self.has_common_illah():
            return self._decision(
                TransitionReadinessState.DEFERRED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.COMMON_ILLAH,
            )
        qadih_decision = _qadih_decision(self.qadih_status)
        if qadih_decision is not None:
            state, code = qadih_decision
            return self._decision(state, code, EuclideanGateStage.QADIH)
        if not self.condition_is_satisfied():
            return self._decision(
                TransitionReadinessState.DEFERRED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.CONDITION,
            )
        if not self.sabab_is_active():
            return self._decision(
                TransitionReadinessState.DEFERRED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.SABAB,
            )
        if not self.preventer_is_absent():
            return self._decision(
                TransitionReadinessState.BLOCKED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.MANI,
            )
        if not self.evidence_refs:
            return self._decision(
                TransitionReadinessState.DEFERRED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.EVIDENCE,
            )
        if self.rank > self.force_rank_ceiling():
            return self._decision(
                TransitionReadinessState.REFUSED,
                FailureCode.RANK_EXCEEDS_CEILING,
                EuclideanGateStage.RANK_CEILING,
            )
        if self._blocking_residuals():
            return self._decision(
                TransitionReadinessState.BLOCKED,
                FailureCode.BLOCKING_RESIDUAL_PRESENT,
                EuclideanGateStage.RESIDUALS,
            )
        if not self.handoff.strip():
            return self._decision(
                TransitionReadinessState.REFUSED,
                FailureCode.GATE_REQUIRED,
                EuclideanGateStage.HANDOFF,
            )
        return None

    def _origin_is_valid(self) -> bool:
        return (
            bool(self.origin_proof.origin_ref.strip())
            and self.origin_proof.domain == self.domain
            and self.origin_proof.trace_ref == self.trace_ref
            and self.linking_proof.origin_ref == self.origin_proof.origin_ref
            and self.linking_proof.origin_to_branch_linked
        )

    def _branch_is_valid(self) -> bool:
        return (
            bool(self.branch_proof.branch_ref.strip())
            and self.branch_proof.domain == self.domain
            and self.branch_proof.trace_ref == self.trace_ref
            and self.linking_proof.branch_ref == self.branch_proof.branch_ref
            and self.linking_proof.branch_to_origin_linked
            and self.linking_proof.reversible_to_origin
        )

    def _decision(
        self,
        state: TransitionReadinessState,
        failure_code: FailureCode,
        stage: EuclideanGateStage,
    ) -> EuclideanGateDecision:
        return EuclideanGateDecision(
            transition_allowed=False,
            readiness_state=state,
            failed_stage=stage,
            failure_code=failure_code,
            rank=self.rank,
            residuals=self.residuals,
            handoff=self.handoff,
        )

    def _blocking_residuals(self) -> tuple[str, ...]:
        return tuple(
            residual for residual in self.residuals if self._is_blocking_residual(residual)
        )

    @staticmethod
    def _is_blocking_residual(residual: str) -> bool:
        return _BLOCKING_TOKEN in residual.lower()

    def _missing_conditions(self) -> list[str]:
        missing: list[str] = []
        if not self.domain.strip():
            missing.append("domain")
        if not self.trace_ref.strip():
            missing.append("trace")
        if not self.has_preserved_identity():
            missing.append("preserved_identity")
        if not self.minimal_complete_is_satisfied():
            missing.append("minimal_complete_requirement")
        if not self._origin_is_valid():
            missing.append("origin_proof")
        if not self._branch_is_valid():
            missing.append("branch_proof")
        if not self.has_effective_description():
            missing.append("effective_description")
        if not self.differentiating_feature.verified:
            missing.append("differentiating_feature")
        if not self.has_common_illah():
            missing.append("common_illah")
        if self.qadih_status is QadihCheckStatus.UNCHECKED:
            missing.append("qadih_unchecked")
        if self.qadih_status is QadihCheckStatus.BLOCKING:
            missing.append("qadih_blocking")
        if not self.condition_is_satisfied():
            missing.append("condition")
        if not self.sabab_is_active():
            missing.append("sabab")
        if not self.preventer_is_absent():
            missing.append("preventer_absence")
        if not self.evidence_refs:
            missing.append("evidence")
        if self.rank > self.force_rank_ceiling():
            missing.append("rank_ceiling")
        if not self.handoff.strip():
            missing.append("handoff")
        return missing

    def _repair_suggestion(self, missing: list[str], blocking: tuple[str, ...]) -> str:
        if blocking:
            return "resolve blocking residuals before transition handoff"
        if missing:
            return f"satisfy missing requirements: {', '.join(missing)}"
        return "no repair required"


def _qadih_decision(
    status: QadihCheckStatus,
) -> tuple[TransitionReadinessState, FailureCode] | None:
    if status is QadihCheckStatus.CLEAR:
        return None
    if status is QadihCheckStatus.UNCHECKED:
        return (TransitionReadinessState.DEFERRED, FailureCode.QADIH_DIFFERENCE_UNCHECKED)
    if status is QadihCheckStatus.BLOCKING:
        return (TransitionReadinessState.BLOCKED, FailureCode.QADIH_DIFFERENCE_BLOCKING)
    return (TransitionReadinessState.DEFERRED, FailureCode.GATE_REQUIRED)


def _require_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str):
        raise JumpTestContractError(f"{cls_name}.{field} must be a string")


def _require_bool(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, bool):
        raise JumpTestContractError(f"{cls_name}.{field} must be a bool")


def _require_tuple(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise JumpTestContractError(f"{cls_name}.{field} must be a tuple")


def _require_int(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, int):
        raise JumpTestContractError(f"{cls_name}.{field} must be an int")


__all__ = [
    "BranchProof",
    "DifferentiatingFeatureProof",
    "EuclideanFailureRecord",
    "EuclideanGateDecision",
    "EuclideanGateStage",
    "EuclideanLearningEvidence",
    "EuclideanTransitionContract",
    "JumpTestContractError",
    "JumpTestInput",
    "JumpTestResult",
    "MinimalCompleteRequirement",
    "OriginBranchLinkProof",
    "OriginProof",
    "QadihCheckStatus",
    "RankForceCeiling",
    "RankedBranchPrediction",
    "ResidualKind",
    "TransitionContract",
    "TransitionReadinessState",
]
