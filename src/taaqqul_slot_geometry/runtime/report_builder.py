from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from taaqqul_slot_geometry.runtime.corpus_runner import CorpusRunResult
from taaqqul_slot_geometry.runtime.execution_record import StageTransitionState


@dataclass(frozen=True, slots=True)
class NativeCorpusReport:
    run_id: str
    corpus_id: str
    source_commit_sha: str
    registry_hash: str
    total_records: int
    by_state: dict[str, int]
    by_path: dict[str, int]
    deepest_stage_by_token: dict[str, str]


def build_native_report(result: CorpusRunResult) -> NativeCorpusReport:
    state_counts: Counter[str] = Counter()
    path_counts: Counter[str] = Counter()
    deepest: dict[str, str] = {}
    total = 0

    for token in result.token_results:
        executed = [r for r in token.records if r.transition_state is StageTransitionState.EXECUTED]
        deepest[token.token_id] = executed[-1].stage_id if executed else "NONE"
        for record in token.records:
            total += 1
            state_counts[record.transition_state.value] += 1
            path_counts[record.path_id] += 1

    return NativeCorpusReport(
        run_id=result.run_id,
        corpus_id=result.corpus_id,
        source_commit_sha=result.source_commit_sha,
        registry_hash=result.registry_hash,
        total_records=total,
        by_state=dict(state_counts),
        by_path=dict(path_counts),
        deepest_stage_by_token=deepest,
    )
