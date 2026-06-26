"""PR-X0R runtime transition contract hooks (no linguistic inference)."""

from taaqqul_slot_geometry.x0r.learning_loop import (
    EuclideanLearningLoopResult,
    EuclideanLearningLoopSchemaError,
    EuclideanLearningState,
    learn_failure,
    learn_success,
    promote_rank_if_evidence_sufficient,
    refine_contract,
)
from taaqqul_slot_geometry.x0r.transition_contract import (
    EuclideanFailureRecord,
    EuclideanGateDecision,
    EuclideanLearningEvidence,
    EuclideanTransitionContract,
    JumpTestContractError,
    JumpTestInput,
    JumpTestResult,
    MinimalCompleteRequirement,
    RankedBranchPrediction,
    ResidualKind,
    TransitionContract,
)

__all__ = [
    "EuclideanFailureRecord",
    "EuclideanGateDecision",
    "EuclideanLearningEvidence",
    "EuclideanLearningLoopResult",
    "EuclideanLearningLoopSchemaError",
    "EuclideanLearningState",
    "EuclideanTransitionContract",
    "JumpTestContractError",
    "JumpTestInput",
    "JumpTestResult",
    "MinimalCompleteRequirement",
    "RankedBranchPrediction",
    "ResidualKind",
    "TransitionContract",
    "learn_failure",
    "learn_success",
    "promote_rank_if_evidence_sufficient",
    "refine_contract",
]
