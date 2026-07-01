"""PR-X0L — Euclidean learning loop over X0R transition contracts.

This module implements a bounded learning loop on top of
``EuclideanTransitionContract`` only:

* ``learn_success``
* ``learn_failure``
* ``refine_contract``
* ``promote_rank_if_evidence_sufficient``

It does not add parser/syntax/semantic runtime behavior and does not touch
DAL/LAFZI/WAD'I branches.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.x0r.transition_contract import (
    EuclideanLearningEvidence,
    EuclideanTransitionContract,
)

_LEARNING_RESIDUAL_POLICY = "VISIBLE_EVIDENCE_RESIDUAL_POLICY"


class EuclideanLearningLoopSchemaError(TypeError):
    """Raised when PR-X0L learning-loop surfaces are malformed."""


class EuclideanLearningState(StrEnum):
    """PR-X0L learning-loop decision states."""

    SUCCESS_RECORDED = "SUCCESS_RECORDED"
    FAILURE_RECORDED = "FAILURE_RECORDED"
    CONTRACT_REFINED = "CONTRACT_REFINED"
    RANK_PROMOTED = "RANK_PROMOTED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class EuclideanLearningLoopResult:
    """Result surface for one PR-X0L learning-loop step."""

    state: EuclideanLearningState
    contract: EuclideanTransitionContract
    evidence_refs: tuple[str, ...]
    residuals: tuple[str, ...]
    failure_code: FailureCode | None
    trace_ref: str
    residual_policy: str = _LEARNING_RESIDUAL_POLICY

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.state, EuclideanLearningState):
            raise EuclideanLearningLoopSchemaError(
                f"{cls}.state must be a EuclideanLearningState member"
            )
        if not isinstance(self.contract, EuclideanTransitionContract):
            raise EuclideanLearningLoopSchemaError(
                f"{cls}.contract must be a EuclideanTransitionContract"
            )
        _require_nonempty_str(cls, "trace_ref", self.trace_ref)
        _require_nonempty_str(cls, "residual_policy", self.residual_policy)
        _require_str_tuple(cls, "evidence_refs", self.evidence_refs)
        _require_str_tuple(cls, "residuals", self.residuals)
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise EuclideanLearningLoopSchemaError(
                f"{cls}.failure_code must be a FailureCode member or None"
            )
        if self.state is EuclideanLearningState.REFUSED and self.failure_code is None:
            raise EuclideanLearningLoopSchemaError(f"{cls}.REFUSED requires a named failure_code")
        if self.state is EuclideanLearningState.RANK_PROMOTED and self.failure_code is not None:
            raise EuclideanLearningLoopSchemaError(
                f"{cls}.RANK_PROMOTED must not carry a failure_code"
            )


def learn_success(
    contract: EuclideanTransitionContract,
    evidence: EuclideanLearningEvidence,
    *,
    trace_ref: str,
) -> EuclideanLearningLoopResult:
    """Record a successful learning observation with visible evidence."""

    _require_contract(contract)
    _require_evidence(evidence)
    _require_trace_ref(trace_ref)

    refined_contract = _with_residuals(
        contract,
        (
            f"learning:success:evidence:{evidence.evidence_ref}",
            f"learning:success:source:{evidence.source}",
        ),
    )
    if not contract.can_transition():
        failure = contract.to_failure_record().failure_code or FailureCode.GATE_REQUIRED
        return _result(
            state=EuclideanLearningState.REFUSED,
            contract=refined_contract,
            evidence_refs=(evidence.evidence_ref,),
            failure_code=failure,
            trace_ref=trace_ref,
        )
    return _result(
        state=EuclideanLearningState.SUCCESS_RECORDED,
        contract=refined_contract,
        evidence_refs=(evidence.evidence_ref,),
        failure_code=None,
        trace_ref=trace_ref,
    )


def learn_failure(
    contract: EuclideanTransitionContract,
    evidence: EuclideanLearningEvidence,
    *,
    failure_note: str,
    trace_ref: str,
) -> EuclideanLearningLoopResult:
    """Record a failed learning observation with a visible blocking residual."""

    _require_contract(contract)
    _require_evidence(evidence)
    _require_trace_ref(trace_ref)
    if not isinstance(failure_note, str) or not failure_note.strip():
        raise EuclideanLearningLoopSchemaError("failure_note must be a non-empty string")

    failure = contract.to_failure_record().failure_code or FailureCode.BLOCKING_RESIDUAL_PRESENT
    refined_contract = _with_residuals(
        contract,
        (
            f"blocking:learning:failure:{failure_note.strip()}",
            f"learning:failure:evidence:{evidence.evidence_ref}",
        ),
    )
    return _result(
        state=EuclideanLearningState.FAILURE_RECORDED,
        contract=refined_contract,
        evidence_refs=(evidence.evidence_ref,),
        failure_code=failure,
        trace_ref=trace_ref,
    )


def refine_contract(
    contract: EuclideanTransitionContract,
    evidences: tuple[EuclideanLearningEvidence, ...],
    *,
    refinement_note: str | None,
    trace_ref: str,
) -> EuclideanLearningLoopResult:
    """Refine contract description/residual surface using visible evidence refs."""

    _require_contract(contract)
    _require_trace_ref(trace_ref)
    if not isinstance(evidences, tuple) or not evidences:
        raise EuclideanLearningLoopSchemaError("evidences must be a non-empty tuple")
    for evidence in evidences:
        _require_evidence(evidence)
    if refinement_note is not None and not isinstance(refinement_note, str):
        raise EuclideanLearningLoopSchemaError("refinement_note must be a string or None")

    evidence_refs = tuple(evidence.evidence_ref for evidence in evidences)
    residuals = tuple(f"learning:refine:evidence:{ref}" for ref in evidence_refs)
    updated_description = contract.effective_description
    if refinement_note and refinement_note.strip():
        updated_description = f"{updated_description} | refine:{refinement_note.strip()}"
        residuals = (*residuals, f"learning:refine:note:{refinement_note.strip()}")
    refined_contract = replace(
        _with_residuals(contract, residuals),
        effective_description=updated_description,
    )
    return _result(
        state=EuclideanLearningState.CONTRACT_REFINED,
        contract=refined_contract,
        evidence_refs=evidence_refs,
        failure_code=None,
        trace_ref=trace_ref,
    )


def promote_rank_if_evidence_sufficient(
    contract: EuclideanTransitionContract,
    evidences: tuple[EuclideanLearningEvidence, ...],
    *,
    trace_ref: str,
    min_evidence_count: int = 2,
) -> EuclideanLearningLoopResult:
    """Promote rank only when visible evidence is sufficient and gate-safe."""

    _require_contract(contract)
    _require_trace_ref(trace_ref)
    if not isinstance(evidences, tuple) or not evidences:
        raise EuclideanLearningLoopSchemaError("evidences must be a non-empty tuple")
    for evidence in evidences:
        _require_evidence(evidence)
    if not isinstance(min_evidence_count, int) or min_evidence_count < 1:
        raise EuclideanLearningLoopSchemaError("min_evidence_count must be a positive int")

    evidence_refs = tuple(evidence.evidence_ref for evidence in evidences)
    deferred_contract = _with_residuals(
        contract,
        tuple(f"learning:promotion:evidence:{ref}" for ref in evidence_refs),
    )
    if len(evidences) < min_evidence_count:
        return _result(
            state=EuclideanLearningState.REFUSED,
            contract=deferred_contract,
            evidence_refs=evidence_refs,
            failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            trace_ref=trace_ref,
        )
    if not contract.can_transition():
        failure = contract.to_failure_record().failure_code or FailureCode.GATE_REQUIRED
        return _result(
            state=EuclideanLearningState.REFUSED,
            contract=deferred_contract,
            evidence_refs=evidence_refs,
            failure_code=failure,
            trace_ref=trace_ref,
        )

    candidate_rank = _candidate_promoted_rank(contract, evidences)
    if candidate_rank <= contract.rank:
        return _result(
            state=EuclideanLearningState.REFUSED,
            contract=deferred_contract,
            evidence_refs=evidence_refs,
            failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            trace_ref=trace_ref,
        )
    if not contract.minimal_complete_requirement.is_satisfied_for_rank(candidate_rank):
        return _result(
            state=EuclideanLearningState.REFUSED,
            contract=deferred_contract,
            evidence_refs=evidence_refs,
            failure_code=FailureCode.RANK_PROMOTION_WITHOUT_GATE,
            trace_ref=trace_ref,
        )

    promoted_contract = replace(
        deferred_contract,
        rank=candidate_rank,
        residuals=_merged(
            deferred_contract.residuals,
            (
                f"learning:promotion:rank:{candidate_rank}",
                "learning:promotion:evidence-sufficient",
            ),
        ),
    )
    return _result(
        state=EuclideanLearningState.RANK_PROMOTED,
        contract=promoted_contract,
        evidence_refs=evidence_refs,
        failure_code=None,
        trace_ref=trace_ref,
    )


def _candidate_promoted_rank(
    contract: EuclideanTransitionContract,
    evidences: tuple[EuclideanLearningEvidence, ...],
) -> int:
    rank_hints = [
        hint for hint in (evidence.rank_hint for evidence in evidences) if hint is not None
    ]
    requested_rank = max([contract.rank + 1, *rank_hints])

    ceiling = contract.force_rank_ceiling()
    return min(requested_rank, ceiling)


def _result(
    *,
    state: EuclideanLearningState,
    contract: EuclideanTransitionContract,
    evidence_refs: tuple[str, ...],
    failure_code: FailureCode | None,
    trace_ref: str,
) -> EuclideanLearningLoopResult:
    return EuclideanLearningLoopResult(
        state=state,
        contract=contract,
        evidence_refs=evidence_refs,
        residuals=contract.residuals,
        failure_code=failure_code,
        trace_ref=trace_ref,
        residual_policy=_LEARNING_RESIDUAL_POLICY,
    )


def _with_residuals(
    contract: EuclideanTransitionContract,
    residuals: tuple[str, ...],
) -> EuclideanTransitionContract:
    return replace(contract, residuals=_merged(contract.residuals, residuals))


def _merged(base: tuple[str, ...], extra: tuple[str, ...]) -> tuple[str, ...]:
    ordered: list[str] = list(base)
    for item in extra:
        if item not in ordered:
            ordered.append(item)
    return tuple(ordered)


def _require_contract(contract: object) -> None:
    if not isinstance(contract, EuclideanTransitionContract):
        raise EuclideanLearningLoopSchemaError("contract must be a EuclideanTransitionContract")


def _require_evidence(evidence: object) -> None:
    if not isinstance(evidence, EuclideanLearningEvidence):
        raise EuclideanLearningLoopSchemaError("evidence must be EuclideanLearningEvidence")


def _require_trace_ref(trace_ref: object) -> None:
    if not isinstance(trace_ref, str) or not trace_ref.strip():
        raise EuclideanLearningLoopSchemaError("trace_ref must be a non-empty string")
    if not trace_ref.startswith("trace://"):
        raise EuclideanLearningLoopSchemaError("trace_ref must start with 'trace://'")


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EuclideanLearningLoopSchemaError(f"{cls_name}.{field} must be a non-empty string")


def _require_str_tuple(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise EuclideanLearningLoopSchemaError(f"{cls_name}.{field} must be a tuple")
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise EuclideanLearningLoopSchemaError(
                f"{cls_name}.{field} entries must be non-empty strings"
            )


__all__ = [
    "EuclideanLearningLoopResult",
    "EuclideanLearningLoopSchemaError",
    "EuclideanLearningState",
    "learn_failure",
    "learn_success",
    "promote_rank_if_evidence_sufficient",
    "refine_contract",
]
