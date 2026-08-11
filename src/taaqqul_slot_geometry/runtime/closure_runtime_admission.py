"""V0.231 narrow runtime admission gate for ratified Closure law only.

Runtime consumes independently reconstructible closure proof objects.
It does not discover, derive, or ratify the law it applies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core import FailureCode, Rank
from taaqqul_slot_geometry.runtime.execution_record import (
    StageExecutionRecord,
    StageTransitionState,
)

_DOC_110 = "docs/110_RUNTIME_ADMISSION_BY_INDEPENDENT_RATIFICATION_LAW.md"


class ClosureRuntimeAdmissionError(TypeError):
    """Raised when V0.231 closure-admission carriers are malformed."""


class ClosureAdmissionState(StrEnum):
    ADMITTED = "ADMITTED"
    REFUSED = "REFUSED"


class ClosureRefusalFamily(StrEnum):
    MISSING_REQUIREMENT = "MissingRequirement"
    BLOCKING_RESIDUAL = "BlockingResidual"
    BROKEN_TRACE_CONTINUITY = "BrokenTraceContinuity"
    RANK_ABOVE_EVIDENCE = "RankAboveEvidence"


@dataclass(frozen=True, slots=True)
class ClosureObservedArtifact:
    artifact_id: str
    stage_records: tuple[StageExecutionRecord, ...]
    law_ref: str = _DOC_110

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_non_empty_str(cls, "artifact_id", self.artifact_id)
        _require_non_empty_str(cls, "law_ref", self.law_ref)
        if not isinstance(self.stage_records, tuple) or not self.stage_records:
            raise ClosureRuntimeAdmissionError(
                f"{cls}.stage_records must be a non-empty tuple "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )
        for record in self.stage_records:
            if not isinstance(record, StageExecutionRecord):
                raise ClosureRuntimeAdmissionError(
                    f"{cls}.stage_records entries must be StageExecutionRecord "
                    f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
                )


@dataclass(frozen=True, slots=True)
class ClosureProofObject:
    artifact_id: str
    law_ref: str
    requirements_complete: bool
    no_blocking_residual: bool
    trace_continuous: bool
    supported_rank: Rank
    peak_rank: Rank
    requirements_observed: frozenset[str]
    witnesses_observed: frozenset[str]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_non_empty_str(cls, "artifact_id", self.artifact_id)
        _require_non_empty_str(cls, "law_ref", self.law_ref)
        _require_bool(cls, "requirements_complete", self.requirements_complete)
        _require_bool(cls, "no_blocking_residual", self.no_blocking_residual)
        _require_bool(cls, "trace_continuous", self.trace_continuous)
        if not isinstance(self.supported_rank, Rank):
            raise ClosureRuntimeAdmissionError(f"{cls}.supported_rank must be Rank")
        if not isinstance(self.peak_rank, Rank):
            raise ClosureRuntimeAdmissionError(f"{cls}.peak_rank must be Rank")
        if not isinstance(self.requirements_observed, frozenset):
            raise ClosureRuntimeAdmissionError(f"{cls}.requirements_observed must be frozenset")
        if not isinstance(self.witnesses_observed, frozenset):
            raise ClosureRuntimeAdmissionError(f"{cls}.witnesses_observed must be frozenset")


@dataclass(frozen=True, slots=True)
class ClosureRuntimeAdmissionDecision:
    state: ClosureAdmissionState
    admitted: bool
    refusal_family: ClosureRefusalFamily | None
    failure_code: FailureCode | None
    proof_object: ClosureProofObject
    message: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.state, ClosureAdmissionState):
            raise ClosureRuntimeAdmissionError(f"{cls}.state must be ClosureAdmissionState")
        _require_bool(cls, "admitted", self.admitted)
        if self.refusal_family is not None and not isinstance(
            self.refusal_family, ClosureRefusalFamily
        ):
            raise ClosureRuntimeAdmissionError(
                f"{cls}.refusal_family must be ClosureRefusalFamily or None"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise ClosureRuntimeAdmissionError(f"{cls}.failure_code must be FailureCode or None")
        if not isinstance(self.proof_object, ClosureProofObject):
            raise ClosureRuntimeAdmissionError(f"{cls}.proof_object must be ClosureProofObject")
        _require_non_empty_str(cls, "message", self.message)

        if self.admitted:
            if self.state is not ClosureAdmissionState.ADMITTED:
                raise ClosureRuntimeAdmissionError(
                    f"{cls}.admitted=True requires state=ADMITTED"
                )
            if self.refusal_family is not None or self.failure_code is not None:
                raise ClosureRuntimeAdmissionError(
                    f"{cls}.admitted=True cannot carry refusal data"
                )
            return

        if self.state is not ClosureAdmissionState.REFUSED:
            raise ClosureRuntimeAdmissionError(
                f"{cls}.admitted=False requires state=REFUSED"
            )
        if self.refusal_family is None or self.failure_code is None:
            raise ClosureRuntimeAdmissionError(
                f"{cls} refusal requires refusal_family and failure_code"
            )


class ClosureRuntimeAdmissionGate:
    """StageArtifacts -> ClosureProofObject -> Verify -> AdmissionDecision."""

    @staticmethod
    def reconstruct_proof(observed: ClosureObservedArtifact) -> ClosureProofObject:
        if not isinstance(observed, ClosureObservedArtifact):
            raise ClosureRuntimeAdmissionError(
                "observed must be ClosureObservedArtifact "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )

        executed = tuple(
            record
            for record in observed.stage_records
            if record.transition_state is StageTransitionState.EXECUTED
        )
        requirements_complete = bool(executed) and all(
            bool(record.identity_invariants_checked) and bool(record.evidence_refs)
            for record in executed
        )
        no_blocking_residual = all(
            not any(residual.startswith("BLOCKING") for residual in record.residuals_after)
            for record in observed.stage_records
        )
        trace_continuous = _trace_is_continuous(observed.stage_records)

        supported_rank = max((record.rank_after for record in executed), default=Rank.ZERO)
        peak_rank = max(
            (record.rank_after for record in observed.stage_records),
            default=Rank.ZERO,
        )
        requirements_observed = frozenset(
            requirement
            for record in observed.stage_records
            for requirement in record.identity_invariants_checked
        )
        witnesses_observed = frozenset(
            witness for record in observed.stage_records for witness in record.evidence_refs
        )

        return ClosureProofObject(
            artifact_id=observed.artifact_id,
            law_ref=observed.law_ref,
            requirements_complete=requirements_complete,
            no_blocking_residual=no_blocking_residual,
            trace_continuous=trace_continuous,
            supported_rank=supported_rank,
            peak_rank=peak_rank,
            requirements_observed=requirements_observed,
            witnesses_observed=witnesses_observed,
        )

    @staticmethod
    def verify(proof: ClosureProofObject) -> ClosureRuntimeAdmissionDecision:
        if not isinstance(proof, ClosureProofObject):
            raise ClosureRuntimeAdmissionError(
                "proof must be ClosureProofObject "
                f"({FailureCode.REQUIRED_SLOT_EMPTY.value})"
            )

        if not proof.requirements_complete:
            return _refusal(
                proof=proof,
                family=ClosureRefusalFamily.MISSING_REQUIREMENT,
                detail="requirements/witnesses incomplete on executed stages",
            )
        if not proof.no_blocking_residual:
            return _refusal(
                proof=proof,
                family=ClosureRefusalFamily.BLOCKING_RESIDUAL,
                detail="blocking residual present in observed residual surface",
            )
        if not proof.trace_continuous:
            return _refusal(
                proof=proof,
                family=ClosureRefusalFamily.BROKEN_TRACE_CONTINUITY,
                detail="trace continuity is broken in observed artifact chain",
            )
        if proof.peak_rank.value > proof.supported_rank.value:
            return _refusal(
                proof=proof,
                family=ClosureRefusalFamily.RANK_ABOVE_EVIDENCE,
                detail="peak rank exceeds supported rank extracted from executed evidence",
            )

        return ClosureRuntimeAdmissionDecision(
            state=ClosureAdmissionState.ADMITTED,
            admitted=True,
            refusal_family=None,
            failure_code=None,
            proof_object=proof,
            message=(
                "Closure admission passed under docs/110 discipline; "
                "runtime opens for Closure law only."
            ),
        )

    @classmethod
    def admit_from_observed(
        cls, observed: ClosureObservedArtifact
    ) -> ClosureRuntimeAdmissionDecision:
        proof = cls.reconstruct_proof(observed)
        return cls.verify(proof)


def _refusal(
    *,
    proof: ClosureProofObject,
    family: ClosureRefusalFamily,
    detail: str,
) -> ClosureRuntimeAdmissionDecision:
    return ClosureRuntimeAdmissionDecision(
        state=ClosureAdmissionState.REFUSED,
        admitted=False,
        refusal_family=family,
        failure_code=_FAILURE_BY_REFUSAL[family],
        proof_object=proof,
        message=f"Closure runtime admission refused: {family.value} ({detail}).",
    )


def _trace_is_continuous(records: tuple[StageExecutionRecord, ...]) -> bool:
    return all(
        bool(record.trace_parent_ids)
        and len(record.trace_entry_id.split(":")) >= 2
        and ":".join(record.trace_entry_id.split(":")[:2]) in record.trace_parent_ids
        for record in records
    )


def _require_non_empty_str(owner: str, field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ClosureRuntimeAdmissionError(f"{owner}.{field_name} must be a non-empty string")


def _require_bool(owner: str, field_name: str, value: bool) -> None:
    if not isinstance(value, bool):
        raise ClosureRuntimeAdmissionError(f"{owner}.{field_name} must be bool")


_FAILURE_BY_REFUSAL = {
    ClosureRefusalFamily.MISSING_REQUIREMENT: FailureCode.REQUIRED_SLOT_EMPTY,
    ClosureRefusalFamily.BLOCKING_RESIDUAL: FailureCode.BLOCKING_RESIDUAL_PRESENT,
    ClosureRefusalFamily.BROKEN_TRACE_CONTINUITY: FailureCode.TRACE_MISSING,
    ClosureRefusalFamily.RANK_ABOVE_EVIDENCE: FailureCode.RANK_EXCEEDS_CEILING,
}


__all__ = [
    "ClosureAdmissionState",
    "ClosureObservedArtifact",
    "ClosureProofObject",
    "ClosureRefusalFamily",
    "ClosureRuntimeAdmissionDecision",
    "ClosureRuntimeAdmissionError",
    "ClosureRuntimeAdmissionGate",
]
