from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass

from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.runtime.execution_record import (
    StageApplicability,
    StageExecutionRecord,
    StageTransitionState,
)
from taaqqul_slot_geometry.runtime.native_stage_registry import (
    PathEvidence,
    classify_token_paths,
    get_native_stage_registry,
    registry_hash,
    registry_version,
)


@dataclass(frozen=True, slots=True)
class TokenRuntimeResult:
    token_id: str
    surface: str
    paths: tuple[PathEvidence, ...]
    records: tuple[StageExecutionRecord, ...]


@dataclass(frozen=True, slots=True)
class CorpusRunResult:
    run_id: str
    corpus_id: str
    token_results: tuple[TokenRuntimeResult, ...]
    registry_version: str
    registry_hash: str
    source_commit_sha: str


def _commit_sha() -> str:
    env_sha = (
        os.environ.get("TAAQQUL_SOURCE_COMMIT_SHA")
        or os.environ.get("GITHUB_SHA")
        or os.environ.get("CI_COMMIT_SHA")
    )
    if env_sha:
        return env_sha.strip()

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNKNOWN_COMMIT_SHA"
    return result.stdout.strip() or "UNKNOWN_COMMIT_SHA"


def _record_for_stage(
    *,
    run_id: str,
    corpus_id: str,
    token_id: str,
    path_id: str,
    stage_id: str,
    applicable: bool,
    opened: bool,
    runtime_implemented: bool,
    deferred_hint: str | None,
    next_stage_ids: tuple[str, ...],
) -> StageExecutionRecord:
    if not applicable:
        transition = StageTransitionState.NOT_APPLICABLE
        applicability = StageApplicability.NOT_APPLICABLE
        hints: tuple[str, ...] = ()
        output_id = None
    elif not opened:
        transition = StageTransitionState.NOT_OPENED
        applicability = StageApplicability.APPLICABLE
        hints = ("previous_gate_not_proven",)
        output_id = None
    elif not runtime_implemented:
        transition = StageTransitionState.DECLARED_NOT_IMPLEMENTED
        applicability = StageApplicability.APPLICABLE
        hints = ("runtime_implementation_missing",)
        output_id = None
    elif deferred_hint is not None:
        transition = StageTransitionState.DEFERRED
        applicability = StageApplicability.APPLICABLE
        hints = (deferred_hint,)
        output_id = None
    else:
        transition = StageTransitionState.EXECUTED
        applicability = StageApplicability.APPLICABLE
        hints = ()
        output_id = f"{token_id}:{stage_id}:out"

    residuals_after = ()
    if transition is not StageTransitionState.EXECUTED:
        residuals_after = ("RUNTIME_CONTEXT_PENDING",)

    return StageExecutionRecord(
        run_id=run_id,
        corpus_id=corpus_id,
        token_id=token_id,
        span_id=None,
        stage_id=stage_id,
        path_id=path_id,
        input_carrier_id=f"{token_id}:in",
        output_carrier_id=output_id,
        applicability=applicability,
        transition_state=transition,
        evidence_refs=(f"token:{token_id}",),
        rank_before=Rank.ZERO,
        rank_after=Rank.ZERO,
        residuals_before=(),
        residuals_after=residuals_after,
        identity_invariants_checked=("token_surface_identity_preserved",),
        trace_parent_ids=(f"trace:{token_id}",),
        trace_entry_id=f"trace:{token_id}:{stage_id}",
        failure_code=None,
        remediation_hints=hints,
        next_admissible_stage_ids=next_stage_ids,
        source_commit_sha=_commit_sha(),
        registry_version=registry_version(),
        registry_hash=registry_hash(),
    )


def run_native_corpus(corpus_id: str, tokens: tuple[str, ...]) -> CorpusRunResult:
    run_id = f"native:{corpus_id}"
    specs = get_native_stage_registry()
    token_results: list[TokenRuntimeResult] = []

    for index, surface in enumerate(tokens):
        token_id = f"t{index:03d}"
        paths = classify_token_paths(surface)
        primary_path = paths[0].path_id.value

        records: list[StageExecutionRecord] = []
        opened_stages = {"PATH_CLASSIFICATION"}

        for spec in specs:
            applicable = spec.applicability_predicate(paths)
            required_open = all(
                predecessor in opened_stages
                for predecessor in spec.required_predecessors
            )
            alternative_open = (
                True
                if not spec.alternative_predecessors
                else any(
                    predecessor in opened_stages
                    for predecessor in spec.alternative_predecessors
                )
            )
            opened = required_open and alternative_open

            deferred_hint = None
            if (
                applicable
                and opened
                and spec.runtime_implemented
                and spec.stage_id != "PATH_CLASSIFICATION"
                and spec.context_requirement != "NONE"
            ):
                deferred_hint = f"missing_context:{spec.context_requirement}"

            rec = _record_for_stage(
                run_id=run_id,
                corpus_id=corpus_id,
                token_id=token_id,
                path_id=primary_path,
                stage_id=spec.stage_id,
                applicable=applicable,
                opened=opened,
                runtime_implemented=spec.runtime_implemented,
                deferred_hint=deferred_hint,
                next_stage_ids=spec.allowed_successors,
            )
            records.append(rec)
            if rec.transition_state is StageTransitionState.EXECUTED:
                opened_stages.add(spec.stage_id)

        token_results.append(
            TokenRuntimeResult(
                token_id=token_id,
                surface=surface,
                paths=paths,
                records=tuple(records),
            )
        )

    return CorpusRunResult(
        run_id=run_id,
        corpus_id=corpus_id,
        token_results=tuple(token_results),
        registry_version=registry_version(),
        registry_hash=registry_hash(),
        source_commit_sha=_commit_sha(),
    )
