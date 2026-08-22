"""SLGE-SDLC-P0 deterministic lifecycle current-state projection runtime."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from jsonschema import Draft202012Validator

from taaqqul_slot_geometry.governance.slge_sdlc_e0_runtime import T_SLGE_CUT_ID, T_SLGE_MIN_ORDER

LIFECYCLE_EVENTS_PATH = "governance/registry/slge_sdlc_p0_lifecycle_events.json"
LIFECYCLE_EVENTS_SCHEMA_PATH = "schemas/governance/slge_sdlc_p0_lifecycle_events.schema.json"
LIFECYCLE_PROJECTION_PATH = "governance/projections/slge_sdlc_current_lifecycle_state.json"


class LifecycleProjectionError(ValueError):
    """Named fail-closed error for lifecycle projection runtime."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


class SLGEP0FailureCode(StrEnum):
    """Named failure inventory for SLGE-SDLC-P0 fail-closed boundaries."""

    DUPLICATE_EVENT_ID = "DUPLICATE_EVENT_ID"
    DUPLICATE_DECISION_ID = "DUPLICATE_DECISION_ID"
    DANGLING_REFERENCE = "DANGLING_REFERENCE"
    UNKNOWN_ARTIFACT_OR_LINEAGE = "UNKNOWN_ARTIFACT_OR_LINEAGE"
    TEMPORAL_CUT_VIOLATION = "TEMPORAL_CUT_VIOLATION"
    SYNTHETIC_HISTORICAL_MCLT = "SYNTHETIC_HISTORICAL_MCLT"
    DECISION_EVENT_MISMATCH = "DECISION_EVENT_MISMATCH"
    DECISION_NOT_APPROVED = "DECISION_NOT_APPROVED"
    SOURCE_STATE_MISMATCH = "SOURCE_STATE_MISMATCH"
    ILLEGAL_SLOT_TRANSITION = "ILLEGAL_SLOT_TRANSITION"
    TRACE_LOSS = "TRACE_LOSS"
    BLOCKING_RESIDUAL_VIOLATION = "BLOCKING_RESIDUAL_VIOLATION"
    RANK_AUTHORITY_INFLATION = "RANK_AUTHORITY_INFLATION"
    CONFLICTING_CURRENT_STATE = "CONFLICTING_CURRENT_STATE"
    NON_DETERMINISTIC_ORDERING = "NON_DETERMINISTIC_ORDERING"
    LIFECYCLE_PROJECTION_DRIFT = "LIFECYCLE_PROJECTION_DRIFT"


_ALLOWED_SLOT_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "SLGE-SDLC-M0": ("SLGE-SDLC-E0",),
    "SLGE-SDLC-E0": ("SLGE-SDLC-P0",),
    "SLGE-SDLC-P0": ("SLGE-SDLC-G0",),
    "SLGE-SDLC-G0": ("SLGE-SDLC-C0",),
}

_RANK_ORDER = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4, "E5": 5}
_AUTHORITY_ORDER = {
    "LawAuthority": 0,
    "ProjectionContractAuthority": 1,
    "ProjectionRuntimeAuthority": 2,
    "CurrentStateProjectionAuthority": 3,
    "RuntimeAuthority": 4,
    "EvidenceAuthority": 5,
}


@dataclass(frozen=True, slots=True)
class ArtifactLifecycleState:
    """Reduced current lifecycle state for one governed artifact lineage."""

    artifact_id: str
    lineage_id: str
    current_lifecycle_slot: str
    baseline_ref: str | None
    last_applied_event: str | None
    maturity_coordinates: dict[str, str]
    rank_ceiling: str
    authority_ceiling: str
    open_residual_refs: tuple[str, ...]
    trace_refs: tuple[str, ...]
    allowed_next_openings: tuple[str, ...]
    historical_uncertainty_boundary: dict[str, Any]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise LifecycleProjectionError(
            "PROJECTION_SCHEMA_INVALID",
            f"Malformed JSON in {path}: {exc.msg}",
        ) from exc
    if not isinstance(payload, dict):
        raise LifecycleProjectionError(
            "PROJECTION_SCHEMA_INVALID",
            f"Top-level JSON must be object in {path}",
        )
    return payload


def _schema_validator(schema_path: Path) -> Draft202012Validator:
    schema = _read_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _validate_schema(
    validator: Draft202012Validator,
    payload: dict[str, Any],
    path: Path,
) -> None:
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        messages = "; ".join(error.message for error in errors)
        raise LifecycleProjectionError("PROJECTION_SCHEMA_INVALID", f"{path}: {messages}")


def load_lifecycle_inputs(repo_root: Path) -> dict[str, Any]:
    """Load the authoritative P0 lifecycle event registry and source bytes."""

    events_path = repo_root / LIFECYCLE_EVENTS_PATH
    schema_path = repo_root / LIFECYCLE_EVENTS_SCHEMA_PATH

    payload = _read_json(events_path)
    _validate_schema(_schema_validator(schema_path), payload, events_path)

    return {
        "events": payload,
        "source_bytes": {
            LIFECYCLE_EVENTS_PATH: events_path.read_bytes(),
        },
    }


def _require_unique_id(records: list[dict[str, Any]], key: str, code: SLGEP0FailureCode) -> None:
    seen: set[str] = set()
    for record in records:
        value = str(record[key])
        if value in seen:
            raise LifecycleProjectionError(code.value, f"Duplicate {key}: {value}")
        seen.add(value)


def _rank_not_higher(candidate: str, ceiling: str) -> bool:
    return _RANK_ORDER.get(candidate, -1) <= _RANK_ORDER.get(ceiling, -1)


def _authority_not_higher(candidate: str, ceiling: str) -> bool:
    return _AUTHORITY_ORDER.get(candidate, -1) <= _AUTHORITY_ORDER.get(ceiling, -1)


def validate_lifecycle_semantics(inputs: dict[str, Any]) -> None:
    """Validate P0 lifecycle semantics before reduction."""

    payload = inputs["events"]
    baselines = list(payload["legacy_baseline_records"])
    decisions = list(payload["transition_decisions"])
    events = list(payload["applied_lifecycle_events"])

    _require_unique_id(baselines, "baseline_id", SLGEP0FailureCode.DANGLING_REFERENCE)
    _require_unique_id(decisions, "decision_id", SLGEP0FailureCode.DUPLICATE_DECISION_ID)
    _require_unique_id(events, "event_id", SLGEP0FailureCode.DUPLICATE_EVENT_ID)

    decision_by_id = {str(record["decision_id"]): record for record in decisions}
    baseline_by_artifact = {str(record["artifact_id"]): record for record in baselines}
    baseline_lineage: dict[str, str] = {
        str(record["artifact_id"]): str(record["lineage_id"]) for record in baselines
    }

    seen_orders: set[int] = set()
    for event in events:
        event_id = str(event["event_id"])
        event_order = int(event["event_order"])
        if event_order in seen_orders:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.NON_DETERMINISTIC_ORDERING.value,
                f"Conflicting event_order for {event_id}: {event_order}",
            )
        seen_orders.add(event_order)

        if (
            int(event["governance_order"]) < T_SLGE_MIN_ORDER
            or int(event["dependency_order"]) < T_SLGE_MIN_ORDER
        ):
            raise LifecycleProjectionError(
                SLGEP0FailureCode.TEMPORAL_CUT_VIOLATION.value,
                f"{event_id} occurs before temporal cut orders",
            )
        temporal_epoch_ref = str(event["temporal_epoch_ref"])
        if not temporal_epoch_ref.startswith(f"{T_SLGE_CUT_ID}::"):
            raise LifecycleProjectionError(
                SLGEP0FailureCode.TEMPORAL_CUT_VIOLATION.value,
                f"{event_id} has invalid temporal epoch ref {temporal_epoch_ref}",
            )

        decision_ref = str(event["decision_ref"])
        if decision_ref not in decision_by_id:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.DANGLING_REFERENCE.value,
                f"{event_id} references unknown decision {decision_ref}",
            )
        decision = decision_by_id[decision_ref]
        if str(decision["state"]) != "APPROVED":
            raise LifecycleProjectionError(
                SLGEP0FailureCode.DECISION_NOT_APPROVED.value,
                f"{event_id} references non-APPROVED decision {decision_ref}",
            )

        if (
            str(decision["artifact_id"]) != str(event["artifact_id"])
            or str(decision["lineage_id"]) != str(event["lineage_id"])
            or str(decision["from_slot_ref"]) != str(event["from_slot_ref"])
            or str(decision["to_slot_ref"]) != str(event["to_slot_ref"])
        ):
            raise LifecycleProjectionError(
                SLGEP0FailureCode.DECISION_EVENT_MISMATCH.value,
                f"Decision/event mismatch for {event_id}",
            )

        from_slot = str(event["from_slot_ref"])
        to_slot = str(event["to_slot_ref"])
        if to_slot not in _ALLOWED_SLOT_TRANSITIONS.get(from_slot, ()):  # fail closed
            raise LifecycleProjectionError(
                SLGEP0FailureCode.ILLEGAL_SLOT_TRANSITION.value,
                f"Illegal lifecycle transition in {event_id}: {from_slot}->{to_slot}",
            )

        rank_ceiling = str(event["rank_ceiling"])
        authority_ceiling = str(event["authority_ceiling"])
        if not _rank_not_higher(rank_ceiling, str(decision["rank_ceiling"])):
            raise LifecycleProjectionError(
                SLGEP0FailureCode.RANK_AUTHORITY_INFLATION.value,
                f"Rank inflation in {event_id}",
            )
        if not _authority_not_higher(authority_ceiling, str(decision["authority_ceiling"])):
            raise LifecycleProjectionError(
                SLGEP0FailureCode.RANK_AUTHORITY_INFLATION.value,
                f"Authority inflation in {event_id}",
            )

        trace_refs = tuple(str(item) for item in event["trace_refs"])
        if not trace_refs or str(decision["decision_trace_ref"]) not in trace_refs:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.TRACE_LOSS.value,
                f"Trace continuity lost for {event_id}",
            )

        blocking_residuals = [
            ref for ref in event["open_residual_refs"] if str(ref).startswith("BLOCKING:")
        ]
        if blocking_residuals:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.BLOCKING_RESIDUAL_VIOLATION.value,
                f"Blocking residual present in {event_id}: {blocking_residuals}",
            )

        artifact_id = str(event["artifact_id"])
        lineage_id = str(event["lineage_id"])
        if artifact_id in baseline_lineage and baseline_lineage[artifact_id] != lineage_id:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.UNKNOWN_ARTIFACT_OR_LINEAGE.value,
                f"Lineage mismatch for baseline artifact {artifact_id}",
            )

    for baseline in baselines:
        status = str(baseline["historical_transition_status"])
        if status != "PROVEN" and baseline["historical_mclt_ref"] is not None:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.SYNTHETIC_HISTORICAL_MCLT.value,
                (
                    f"Baseline {baseline['baseline_id']} must not synthesize historical_mclt_ref "
                    f"for status {status}"
                ),
            )

    # Explicitly preserve the Decision != Event invariant:
    # approved decisions may exist and still not mutate state unless event-applied.
    referenced_decisions = {str(event["decision_ref"]) for event in events}
    for decision in decisions:
        decision_id = str(decision["decision_id"])
        if str(decision["state"]) == "APPROVED" and decision_id not in referenced_decisions:
            continue

    # Ensure no forked final state for one artifact/lineage at the same order.
    seen_artifact_order: set[tuple[str, str, int]] = set()
    for event in events:
        key = (str(event["artifact_id"]), str(event["lineage_id"]), int(event["event_order"]))
        if key in seen_artifact_order:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.CONFLICTING_CURRENT_STATE.value,
                f"Conflicting lifecycle events at identical order for {key[0]}",
            )
        seen_artifact_order.add(key)

    # Require every event artifact either appears in baseline or has a typed approved decision.
    for event in events:
        artifact_id = str(event["artifact_id"])
        if artifact_id in baseline_by_artifact:
            continue
        decision_ref = str(event["decision_ref"])
        decision = decision_by_id[decision_ref]
        if str(decision["artifact_id"]) != artifact_id:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.UNKNOWN_ARTIFACT_OR_LINEAGE.value,
                f"Unknown event artifact lineage binding for {artifact_id}",
            )


def normalize_lifecycle_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    """Canonicalize ordering and immutable tuple surfaces before reduction."""

    payload = inputs["events"]

    baselines = sorted(
        payload["legacy_baseline_records"],
        key=lambda item: (
            str(item["artifact_id"]),
            str(item["lineage_id"]),
            str(item["baseline_id"]),
        ),
    )
    decisions = sorted(
        payload["transition_decisions"],
        key=lambda item: (int(item["decision_order"]), str(item["decision_id"])),
    )
    events = sorted(
        payload["applied_lifecycle_events"],
        key=lambda item: (int(item["event_order"]), str(item["event_id"])),
    )

    return {
        "meta": {
            "version": str(payload["version"]),
            "contract_version": str(payload["contract_version"]),
            "branch_ref": str(payload["branch_ref"]),
            "origin_refs": tuple(sorted(str(item) for item in payload["origin_refs"])),
            "projection_algorithm_id": str(payload["projection_algorithm_id"]),
            "runtime_ref": str(payload["runtime_ref"]),
            "projection_path": str(payload["projection_path"]),
            "temporal_cut": dict(payload["temporal_cut"]),
            "reduction_contract": tuple(
                sorted(str(item) for item in payload["reduction_contract"])
            ),
        },
        "baselines": baselines,
        "decisions": decisions,
        "events": events,
        "source_bytes": dict(inputs["source_bytes"]),
    }


def reduce_current_lifecycle_state(normalized: dict[str, Any]) -> dict[str, ArtifactLifecycleState]:
    """Reduce baseline + authorized post-cut events into current lifecycle state."""

    decision_by_id = {str(record["decision_id"]): record for record in normalized["decisions"]}

    states: dict[str, ArtifactLifecycleState] = {}
    for baseline in normalized["baselines"]:
        artifact_id = str(baseline["artifact_id"])
        state = ArtifactLifecycleState(
            artifact_id=artifact_id,
            lineage_id=str(baseline["lineage_id"]),
            current_lifecycle_slot=str(baseline["inferred_lifecycle_slot_ref"]),
            baseline_ref=str(baseline["baseline_id"]),
            last_applied_event=None,
            maturity_coordinates=dict(baseline["maturity_coordinates"]),
            rank_ceiling=str(baseline["rank_ceiling"]),
            authority_ceiling=str(baseline["authority_ceiling"]),
            open_residual_refs=tuple(sorted(str(item) for item in baseline["open_residual_refs"])),
            trace_refs=tuple(sorted(str(item) for item in baseline["trace_refs"])),
            allowed_next_openings=tuple(
                sorted(str(item) for item in baseline["allowed_next_openings"])
            ),
            historical_uncertainty_boundary={
                "status": str(baseline["historical_transition_status"]),
                "historical_mclt_ref": baseline["historical_mclt_ref"],
                "legacy_boundary_preserved": True,
                "baseline_origin_ref": str(baseline["baseline_origin_ref"]),
            },
        )
        states[artifact_id] = state

    for event in normalized["events"]:
        artifact_id = str(event["artifact_id"])
        lineage_id = str(event["lineage_id"])
        source_slot = str(event["from_slot_ref"])

        if artifact_id in states:
            current = states[artifact_id]
            if current.lineage_id != lineage_id:
                raise LifecycleProjectionError(
                    SLGEP0FailureCode.UNKNOWN_ARTIFACT_OR_LINEAGE.value,
                    f"Lineage mismatch while reducing {artifact_id}",
                )
            if current.current_lifecycle_slot != source_slot:
                raise LifecycleProjectionError(
                    SLGEP0FailureCode.SOURCE_STATE_MISMATCH.value,
                    (
                        f"Event {event['event_id']} expects {source_slot} but current state is "
                        f"{current.current_lifecycle_slot}"
                    ),
                )
        elif source_slot not in {"SLGE-SDLC-M0", "SLGE-SDLC-E0"}:
            raise LifecycleProjectionError(
                SLGEP0FailureCode.UNKNOWN_ARTIFACT_OR_LINEAGE.value,
                f"Unknown new artifact {artifact_id} must enter through M0/E0 boundary",
            )

        decision = decision_by_id[str(event["decision_ref"])]
        states[artifact_id] = ArtifactLifecycleState(
            artifact_id=artifact_id,
            lineage_id=lineage_id,
            current_lifecycle_slot=str(event["to_slot_ref"]),
            baseline_ref=states[artifact_id].baseline_ref if artifact_id in states else None,
            last_applied_event=str(event["event_id"]),
            maturity_coordinates=dict(event["maturity_coordinates"]),
            rank_ceiling=str(event["rank_ceiling"]),
            authority_ceiling=str(event["authority_ceiling"]),
            open_residual_refs=tuple(sorted(str(item) for item in event["open_residual_refs"])),
            trace_refs=tuple(sorted(str(item) for item in event["trace_refs"])),
            allowed_next_openings=tuple(
                sorted(str(item) for item in event["allowed_next_openings"])
            ),
            historical_uncertainty_boundary={
                "status": (
                    states[artifact_id].historical_uncertainty_boundary["status"]
                    if artifact_id in states
                    else "POST_CUT_ONLY"
                ),
                "historical_mclt_ref": (
                    states[artifact_id].historical_uncertainty_boundary["historical_mclt_ref"]
                    if artifact_id in states
                    else None
                ),
                "legacy_boundary_preserved": True,
                "decision_ref": str(decision["decision_id"]),
                "event_ref": str(event["event_id"]),
            },
        )

    return states


def project_lifecycle_state(normalized: dict[str, Any]) -> dict[str, Any]:
    """Materialize canonical lifecycle projection payload from normalized inputs."""

    reduced = reduce_current_lifecycle_state(normalized)
    source_bytes = dict(normalized["source_bytes"])

    records = []
    for artifact_id in sorted(reduced):
        state = reduced[artifact_id]
        records.append(
            {
                "artifact_id": state.artifact_id,
                "lineage_id": state.lineage_id,
                "current_lifecycle_slot": state.current_lifecycle_slot,
                "baseline_ref": state.baseline_ref,
                "last_applied_event": state.last_applied_event,
                "maturity_coordinates": dict(state.maturity_coordinates),
                "rank_ceiling": state.rank_ceiling,
                "authority_ceiling": state.authority_ceiling,
                "open_residual_refs": list(state.open_residual_refs),
                "trace_refs": list(state.trace_refs),
                "allowed_next_openings": list(state.allowed_next_openings),
                "historical_uncertainty_boundary": dict(state.historical_uncertainty_boundary),
            }
        )

    source_fingerprints = {
        rel_path: __import__("hashlib").sha256(raw).hexdigest()
        for rel_path, raw in sorted(source_bytes.items())
    }

    projection_id = "SLGE_SDLC_STATE_SHA256_" + __import__("hashlib").sha256(
        "".join(source_fingerprints.values()).encode("utf-8")
    ).hexdigest()[:16]

    return {
        "version": normalized["meta"]["version"],
        "projection_id": projection_id,
        "branch_ref": normalized["meta"]["branch_ref"],
        "derived_from": {
            "registry": [LIFECYCLE_EVENTS_PATH],
            "temporal_cut": normalized["meta"]["temporal_cut"],
        },
        "projection_metadata": {
            "projector_algorithm_id": normalized["meta"]["projection_algorithm_id"],
            "reduction_contract": list(normalized["meta"]["reduction_contract"]),
            "authoritative_inputs": [LIFECYCLE_EVENTS_PATH],
            "source_fingerprints": source_fingerprints,
            "origin_refs": list(normalized["meta"]["origin_refs"]),
            "runtime_ref": normalized["meta"]["runtime_ref"],
        },
        "current_lifecycle_states": records,
    }


def serialize_lifecycle_projection(payload: dict[str, Any]) -> bytes:
    """Canonical byte serialization for deterministic projection output."""

    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode(
        "utf-8"
    )


def compute_projection_payload(repo_root: Path) -> dict[str, Any]:
    """Compute and schema-validate the canonical SLGE lifecycle projection payload."""

    inputs = load_lifecycle_inputs(repo_root)
    validate_lifecycle_semantics(inputs)
    normalized = normalize_lifecycle_inputs(inputs)
    payload = project_lifecycle_state(normalized)

    validator = _schema_validator(
        repo_root / "schemas/governance/slge_sdlc_current_lifecycle_state.schema.json"
    )
    _validate_schema(validator, payload, repo_root / LIFECYCLE_PROJECTION_PATH)
    return payload


def check_projection_drift(repo_root: Path) -> None:
    """Fail closed if checked-in lifecycle projection drifts from deterministic recomputation."""

    computed = serialize_lifecycle_projection(compute_projection_payload(repo_root))
    checked_in = (repo_root / LIFECYCLE_PROJECTION_PATH).read_bytes()
    if computed != checked_in:
        raise LifecycleProjectionError(
            SLGEP0FailureCode.LIFECYCLE_PROJECTION_DRIFT.value,
            f"{LIFECYCLE_PROJECTION_PATH} drifted from deterministic recomputation",
        )


def write_projection(repo_root: Path) -> None:
    """Write lifecycle projection atomically from deterministic recomputation."""

    payload = compute_projection_payload(repo_root)
    encoded = serialize_lifecycle_projection(payload)
    out_path = repo_root / LIFECYCLE_PROJECTION_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with NamedTemporaryFile("wb", dir=out_path.parent, delete=False) as tmp_file:
        tmp_file.write(encoded)
        tmp_name = tmp_file.name
    os.replace(tmp_name, out_path)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SLGE-SDLC-P0 deterministic lifecycle projection"
    )
    parser.add_argument(
        "--root", default=".", help="Repository root (default: current directory)"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Check drift against checked-in projection",
    )
    mode.add_argument(
        "--write",
        action="store_true",
        help="Write deterministic projection atomically",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)
    repo_root = Path(args.root).resolve()

    try:
        if args.write:
            write_projection(repo_root)
            print(f"WROTE: {LIFECYCLE_PROJECTION_PATH}")
            return 0
        check_projection_drift(repo_root)
        print("OK: lifecycle projection matches deterministic recomputation")
        return 0
    except LifecycleProjectionError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
