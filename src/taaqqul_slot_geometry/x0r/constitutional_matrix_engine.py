"""Constitutional matrix runtime engine for the 38-operation dataset.

This module provides a strict data surface (frozen dataclasses) and a small
pure transition engine that:

1. Loads the matrix JSON.
2. Verifies structural integrity (declared origins, no cycles, no orphan
   operations, Euclidean progression).
3. Evaluates handoff from a current operation to its next operation.

No I/O is performed during transition evaluation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from taaqqul_slot_geometry.core.closure_state import ClosureState
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.trace_ledger import TraceEntryCandidate
from taaqqul_slot_geometry.core.transition_state import TransitionState


class MatrixSchemaError(ValueError):
    """Raised when matrix carriers violate the required schema."""


class ClosureVerdict(StrEnum):
    """Local transition verdict surface for ConstitutionalMatrixEngine."""

    CLOSED = "CLOSED"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"


@dataclass(frozen=True, slots=True)
class ConstitutionalOperation:
    """One constitutional operation in the matrix."""

    operation_id: str
    name: str
    origins: tuple[str, ...]
    inputs: tuple[str, ...]
    slots: tuple[str, ...]
    licensing: str
    local_closure: str
    residuals: tuple[str, ...]
    handoff_gate: str
    next_operations: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_empty_str("operation_id", self.operation_id)
        _require_non_empty_str("name", self.name)
        _require_non_empty_tuple("origins", self.origins)
        _require_non_empty_tuple("inputs", self.inputs)
        _require_non_empty_tuple("slots", self.slots)
        _require_non_empty_str("licensing", self.licensing)
        _require_non_empty_str("local_closure", self.local_closure)
        _require_non_empty_tuple("residuals", self.residuals)
        _require_non_empty_str("handoff_gate", self.handoff_gate)
        _require_tuple("next_operations", self.next_operations)


@dataclass(frozen=True, slots=True)
class ConstitutionalMatrix:
    """Canonical matrix surface with strict schema."""

    matrix_id: str
    version: str
    declared_origins: tuple[str, ...]
    operations: tuple[ConstitutionalOperation, ...]

    def __post_init__(self) -> None:
        _require_non_empty_str("matrix_id", self.matrix_id)
        _require_non_empty_str("version", self.version)
        _require_non_empty_tuple("declared_origins", self.declared_origins)
        _require_non_empty_tuple("operations", self.operations)

        op_ids = [op.operation_id for op in self.operations]
        if len(set(op_ids)) != len(op_ids):
            raise MatrixSchemaError("operation_id values must be unique")


@dataclass(frozen=True, slots=True)
class MatrixVerification:
    """Static verification report for the loaded matrix."""

    all_origins_defined: bool
    acyclic_dag: bool
    no_orphans: bool
    euclidean_gradient: bool
    residual_vocabulary_count: int


@dataclass(frozen=True, slots=True)
class TransitionResult:
    """Engine output for one transition request."""

    next_operation_id: str | None
    closure_verdict: ClosureVerdict
    residuals: tuple[str, ...]
    trace_entry: TraceEntryCandidate
    failure_code: FailureCode | None


class ConstitutionalMatrixEngine:
    """Pure transition engine over the constitutional matrix."""

    def __init__(self, matrix: ConstitutionalMatrix) -> None:
        self._matrix = matrix
        self._ops_by_id = {op.operation_id: op for op in matrix.operations}

    @classmethod
    def from_json_file(cls, path: str | Path) -> ConstitutionalMatrixEngine:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(_parse_matrix(raw))

    @property
    def matrix(self) -> ConstitutionalMatrix:
        return self._matrix

    def verify(self) -> MatrixVerification:
        ops = self._matrix.operations
        ids = {op.operation_id for op in ops}
        declared = set(self._matrix.declared_origins)

        all_origins_defined = all(
            all(origin in ids or origin in declared for origin in op.origins) for op in ops
        )

        no_orphans = all(len(op.origins) > 0 for op in ops)

        acyclic_dag = _is_acyclic(ops)

        levels = _compute_levels(ops, declared)
        euclidean_gradient = all(
            all(
                levels[origin] < levels[op.operation_id]
                for origin in op.origins
                if origin in levels
            )
            for op in ops
        )

        residuals = {res for op in ops for res in op.residuals}

        return MatrixVerification(
            all_origins_defined=all_origins_defined,
            acyclic_dag=acyclic_dag,
            no_orphans=no_orphans,
            euclidean_gradient=euclidean_gradient,
            residual_vocabulary_count=len(residuals),
        )

    def evaluate_transition(
        self,
        current_operation_id: str,
        inputs: dict[str, object],
        evidence: dict[str, object],
    ) -> TransitionResult:
        _require_non_empty_str("current_operation_id", current_operation_id)

        op = self._ops_by_id.get(current_operation_id)
        if op is None:
            return self._build_refusal(
                residuals=("UNKNOWN_OPERATION",),
                failure_code=FailureCode.GATE_REQUIRED,
            )

        missing_inputs = [name for name in op.inputs if name not in inputs]
        if missing_inputs:
            return self._build_deferred(
                residuals=tuple(f"MISSING_INPUT:{name}" for name in missing_inputs)
            )

        if not evidence or not bool(evidence.get("visible", False)):
            return self._build_refusal(
                residuals=("EVIDENCE_NOT_VISIBLE",),
                failure_code=FailureCode.GATE_REQUIRED,
            )

        if not op.next_operations:
            return TransitionResult(
                next_operation_id=None,
                closure_verdict=ClosureVerdict.CLOSED,
                residuals=op.residuals,
                trace_entry=_trace(
                    closure=ClosureState.MINIMALLY_CLOSED,
                    transition=TransitionState.APPROVED,
                    failure=None,
                ),
                failure_code=None,
            )

        return TransitionResult(
            next_operation_id=op.next_operations[0],
            closure_verdict=ClosureVerdict.CLOSED,
            residuals=op.residuals,
            trace_entry=_trace(
                closure=ClosureState.MINIMALLY_CLOSED,
                transition=TransitionState.APPROVED,
                failure=None,
            ),
            failure_code=None,
        )

    def _build_deferred(self, residuals: tuple[str, ...]) -> TransitionResult:
        return TransitionResult(
            next_operation_id=None,
            closure_verdict=ClosureVerdict.DEFERRED,
            residuals=residuals,
            trace_entry=_trace(
                closure=ClosureState.OPEN,
                transition=TransitionState.DEFERRED,
                failure=FailureCode.REQUIRED_SLOT_EMPTY,
            ),
            failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        )

    def _build_refusal(
        self,
        residuals: tuple[str, ...],
        failure_code: FailureCode,
    ) -> TransitionResult:
        return TransitionResult(
            next_operation_id=None,
            closure_verdict=ClosureVerdict.REFUSED,
            residuals=residuals,
            trace_entry=_trace(
                closure=ClosureState.BLOCKED,
                transition=TransitionState.REJECTED,
                failure=failure_code,
            ),
            failure_code=failure_code,
        )


def _parse_matrix(payload: dict[str, object]) -> ConstitutionalMatrix:
    if not isinstance(payload, dict):
        raise MatrixSchemaError("matrix JSON payload must be an object")

    operations_raw = payload.get("operations")
    if not isinstance(operations_raw, list):
        raise MatrixSchemaError("operations must be a list")

    operations: list[ConstitutionalOperation] = []
    for entry in operations_raw:
        if not isinstance(entry, dict):
            raise MatrixSchemaError("each operation must be an object")
        operations.append(
            ConstitutionalOperation(
                operation_id=_expect_str(entry, "operation_id"),
                name=_expect_str(entry, "name"),
                origins=_expect_tuple_of_str(entry, "origins"),
                inputs=_expect_tuple_of_str(entry, "inputs"),
                slots=_expect_tuple_of_str(entry, "slots"),
                licensing=_expect_str(entry, "licensing"),
                local_closure=_expect_str(entry, "local_closure"),
                residuals=_expect_tuple_of_str(entry, "residuals"),
                handoff_gate=_expect_str(entry, "handoff_gate"),
                next_operations=_expect_tuple_of_str(entry, "next_operations"),
            )
        )

    return ConstitutionalMatrix(
        matrix_id=_expect_str(payload, "matrix_id"),
        version=_expect_str(payload, "version"),
        declared_origins=_expect_tuple_of_str(payload, "declared_origins"),
        operations=tuple(operations),
    )


def _is_acyclic(operations: tuple[ConstitutionalOperation, ...]) -> bool:
    graph: dict[str, tuple[str, ...]] = {
        op.operation_id: tuple(o for o in op.origins if o.startswith("OP-")) for op in operations
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str) -> bool:
        if node in visiting:
            return False
        if node in visited:
            return True
        visiting.add(node)
        for parent in graph.get(node, ()):
            if parent in graph and not dfs(parent):
                return False
        visiting.remove(node)
        visited.add(node)
        return True

    return all(dfs(node) for node in graph)


def _compute_levels(
    operations: tuple[ConstitutionalOperation, ...], declared_origins: set[str]
) -> dict[str, int]:
    levels: dict[str, int] = {origin: 0 for origin in declared_origins}
    pending = {op.operation_id: op for op in operations}
    while pending:
        progressed = False
        for op_id, op in list(pending.items()):
            if all(origin in levels for origin in op.origins):
                levels[op_id] = max(levels[origin] for origin in op.origins) + 1
                del pending[op_id]
                progressed = True
        if not progressed:
            # Cycles or undefined roots prevent full leveling.
            for op_id in pending:
                levels[op_id] = -1
            break
    return levels


def _trace(
    closure: ClosureState,
    transition: TransitionState,
    failure: FailureCode | None,
) -> TraceEntryCandidate:
    return TraceEntryCandidate(
        parent_anchor="trace://constitutional-matrix-engine",
        stage="gate",
        consulted_gamma_state=closure,
        gate_transition_state=transition,
        snapshot_failure=failure,
        snapshot_rank=Rank.CANDIDATE,
    )


def _expect_str(payload: dict[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise MatrixSchemaError(f"{key} must be a non-empty string")
    return value.strip()


def _expect_tuple_of_str(payload: dict[str, object], key: str) -> tuple[str, ...]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise MatrixSchemaError(f"{key} must be a list")
    out: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise MatrixSchemaError(f"{key} entries must be non-empty strings")
        out.append(item.strip())
    return tuple(out)


def _require_non_empty_str(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise MatrixSchemaError(f"{name} must be a non-empty string")


def _require_non_empty_tuple(name: str, value: tuple[object, ...]) -> None:
    _require_tuple(name, value)
    if not value:
        raise MatrixSchemaError(f"{name} must not be empty")


def _require_tuple(name: str, value: tuple[object, ...]) -> None:
    if not isinstance(value, tuple):
        raise MatrixSchemaError(f"{name} must be a tuple")


__all__ = [
    "ClosureVerdict",
    "ConstitutionalMatrix",
    "ConstitutionalMatrixEngine",
    "ConstitutionalOperation",
    "MatrixSchemaError",
    "MatrixVerification",
    "TransitionResult",
]
