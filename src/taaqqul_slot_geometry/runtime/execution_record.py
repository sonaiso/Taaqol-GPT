from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank


class StageApplicability(StrEnum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class StageTransitionState(StrEnum):
    EXECUTED = "EXECUTED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    DECLARED_NOT_IMPLEMENTED = "DECLARED_NOT_IMPLEMENTED"
    NOT_OPENED = "NOT_OPENED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, slots=True)
class StageExecutionRecord:
    run_id: str
    corpus_id: str
    token_id: str | None
    span_id: str | None
    stage_id: str
    path_id: str
    input_carrier_id: str
    output_carrier_id: str | None
    applicability: StageApplicability
    transition_state: StageTransitionState
    evidence_refs: tuple[str, ...]
    rank_before: Rank
    rank_after: Rank
    residuals_before: tuple[str, ...]
    residuals_after: tuple[str, ...]
    identity_invariants_checked: tuple[str, ...]
    trace_parent_ids: tuple[str, ...]
    trace_entry_id: str
    failure_code: FailureCode | None
    remediation_hints: tuple[str, ...]
    next_admissible_stage_ids: tuple[str, ...]
    source_commit_sha: str
    registry_version: str
    registry_hash: str

    def __post_init__(self) -> None:
        if not self.run_id.strip() or not self.corpus_id.strip():
            raise ValueError("run_id and corpus_id must be non-empty")
        if not self.stage_id.strip():
            raise ValueError("stage_id must be non-empty")
        if (self.token_id is None) == (self.span_id is None):
            raise ValueError("exactly one of token_id or span_id must be set")
        if (
            not self.path_id.strip()
            or not self.input_carrier_id.strip()
            or not self.trace_entry_id.strip()
        ):
            raise ValueError(
                "path_id, input_carrier_id, and trace_entry_id must be non-empty"
            )
        if self.output_carrier_id is not None and not self.output_carrier_id.strip():
            raise ValueError("output_carrier_id must be non-empty when provided")

        # Rule 1: no output carrier without preserved input carrier.
        if self.output_carrier_id is not None and not self.input_carrier_id:
            raise ValueError("output carrier cannot exist without input carrier")

        # Rule 3: no implicit rank upgrade.
        rank_upgraded = self.rank_after.value > self.rank_before.value
        if rank_upgraded and self.transition_state is not StageTransitionState.EXECUTED:
            raise ValueError("rank upgrade is only allowed on executed transitions")

        # Rule 4: no residual deletion.
        if not set(self.residuals_before).issubset(set(self.residuals_after)):
            raise ValueError("residuals_after must keep all residuals_before")

        # Rule 6: no executed stage without traceability.
        if self.transition_state is StageTransitionState.EXECUTED and not self.trace_entry_id:
            raise ValueError("executed stage must have a trace entry")

        # Rule 7: deferred must declare missing condition.
        if (
            self.transition_state is StageTransitionState.DEFERRED
            and not self.remediation_hints
        ):
            raise ValueError("deferred stage must include remediation hints")

        # Rule 8: blocked must carry failure code.
        if (
            self.transition_state is StageTransitionState.BLOCKED
            and self.failure_code is None
        ):
            raise ValueError("blocked stage must include failure_code")

        # Rule 9: NOT_APPLICABLE requires NOT_APPLICABLE applicability.
        if (
            self.transition_state is StageTransitionState.NOT_APPLICABLE
            and self.applicability is not StageApplicability.NOT_APPLICABLE
        ):
            raise ValueError(
                "NOT_APPLICABLE transition requires "
                "NOT_APPLICABLE applicability"
            )
