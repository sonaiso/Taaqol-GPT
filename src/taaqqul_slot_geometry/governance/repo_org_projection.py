"""Deterministic repository current-state projection (REPO-ORG-P0).

StateIsProjection:
    RepositoryCurrentState = Projection(
        History,
        Dependencies,
        Runtime,
        Tests/Evidence,
        Residuals,
    )
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from jsonschema import Draft202012Validator

AUTHORITY_ROLES = {
    "LawAuthority",
    "RuntimeAuthority",
    "EvidenceAuthority",
    "HistoricalAuthority",
    "ProjectionAuthority",
    "ProjectionContractAuthority",
    "ProjectionRuntimeAuthority",
    "CurrentStateProjectionAuthority",
}

DEPENDENCY_RELATION_KINDS = {
    "REQUIRES",
    "DERIVES_FROM",
    "IMPLEMENTS",
    "EVIDENCES",
    "SUPERSEDES",
    "REFINES",
    "BLOCKS",
    "OPENS",
    "HISTORICALLY_FOLLOWS",
}

EVIDENCE_KINDS = {
    "ConstitutionalRatificationEvidence",
    "RuntimeVerificationEvidence",
    "ClosureEvidence",
    "EpistemicClaimEvidence",
    "GovernanceEvidence",
    "SemanticIdentityEvidence",
    "ReplicationEvidence",
    "CrossDomainComparisonEvidence",
}

EVIDENCE_VERDICTS = {"UNEVIDENCED", "PARTIAL", "PROVEN", "REFUSED", "DEFERRED"}
RESIDUAL_DISPOSITIONS = {"OPEN", "CLOSED", "DEFERRED"}

GOVERNANCE_INPUT_FILES: tuple[str, ...] = (
    "governance/history/amendments.jsonl",
    "governance/registry/artifacts.json",
    "governance/registry/branches.json",
    "governance/registry/dependencies.json",
    "governance/registry/runtime_map.json",
    "governance/registry/evidence_map.json",
    "governance/registry/residuals.json",
    "governance/registry/projection_inputs.json",
    "governance/registry/slge_sdlc_r0_contracts.json",
    "governance/registry/slge_sdlc_m0_legacy_remap.json",
    "governance/registry/slge_sdlc_e0_runtime.json",
)
CURRENT_STATE_PATH = "governance/projections/current_state.json"


class ProjectionError(ValueError):
    """Named fail-closed error for governance projection."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        raise ProjectionError(
            "PROJECTION_SCHEMA_INVALID",
            f"Malformed JSON in {path}: {exc}",
        ) from exc
    if not isinstance(payload, dict):
        raise ProjectionError(
            "PROJECTION_SCHEMA_INVALID",
            f"Top-level JSON must be object in {path}",
        )
    return payload


def _parse_amendments_jsonl(path: Path) -> list[dict[str, Any]]:
    lines = _read_text(path).splitlines()
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise ProjectionError(
                "MALFORMED_AMENDMENTS_JSONL",
                f"Blank line not allowed in {path}:{line_number}",
            )
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ProjectionError(
                "MALFORMED_AMENDMENTS_JSONL",
                f"Malformed JSONL at {path}:{line_number}: {exc.msg}",
            ) from exc
        if not isinstance(record, dict):
            raise ProjectionError(
                "MALFORMED_AMENDMENTS_JSONL",
                f"Line {line_number} in {path} must be an object",
            )
        required = {
            "id",
            "record_kind",
            "artifact",
            "historical_order",
            "dependency_order",
            "branch",
            "note",
        }
        missing = sorted(required.difference(record))
        if missing:
            raise ProjectionError(
                "MALFORMED_AMENDMENTS_JSONL",
                f"Line {line_number} in {path} missing fields: {missing}",
            )
        records.append(record)

    seen: dict[str, dict[str, Any]] = {}
    for record in records:
        identity = str(record["id"])
        if identity not in seen:
            seen[identity] = record
            continue
        if seen[identity] != record:
            raise ProjectionError(
                "CONTRADICTORY_GOVERNED_IDENTITY",
                f"Amendment id {identity} has contradictory records",
            )
        raise ProjectionError("DUPLICATE_AMENDMENT_ID", f"Duplicate amendment id {identity}")
    return records


def _schema_validator(schema_path: Path) -> Draft202012Validator:
    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _validate_schema(validator: Draft202012Validator, payload: dict[str, Any], path: Path) -> None:
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        messages = "; ".join(error.message for error in errors)
        raise ProjectionError("PROJECTION_SCHEMA_INVALID", f"{path}: {messages}")


def _require_unique(records: list[dict[str, Any]], key: str, code: str) -> set[str]:
    seen: set[str] = set()
    for record in records:
        value = str(record[key])
        if value in seen:
            raise ProjectionError(code, f"Duplicate {key}: {value}")
        seen.add(value)
    return seen


def _require_subset(values: list[str], allowed: set[str], code: str, label: str) -> None:
    for value in values:
        if value not in allowed:
            raise ProjectionError(code, f"Invalid {label}: {value}")


def _validate_slge_r0_contracts(repo_root: Path, contracts: dict[str, Any]) -> None:
    artifact_kind_ids = _require_unique(
        list(contracts["artifact_kinds"]),
        "artifact_kind_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    slot_ids = _require_unique(
        list(contracts["lifecycle_slots"]),
        "slot_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    project_artifacts = list(contracts["project_artifacts"])
    project_artifact_ids = _require_unique(
        project_artifacts,
        "artifact_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    evidence_requirements = list(contracts["evidence_requirements"])
    evidence_requirement_ids = _require_unique(
        evidence_requirements,
        "evidence_requirement_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    gate_ids = _require_unique(
        list(contracts["gate_references"]),
        "gate_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    gate_decision_records = list(contracts["gate_decisions"])
    gate_decision_ids = _require_unique(
        gate_decision_records,
        "gate_decision_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    transition_contracts = list(contracts["lifecycle_transition_contracts"])
    transition_ids = _require_unique(
        transition_contracts,
        "transition_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    residual_records = list(contracts["residual_records"])
    residual_ids = _require_unique(
        residual_records,
        "residual_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    residual_delta_records = list(contracts["residual_deltas"])
    residual_delta_ids = _require_unique(
        residual_delta_records,
        "residual_delta_id",
        "DUPLICATE_LIFECYCLE_ID",
    )
    trace_records = list(contracts["trace_records"])
    trace_ids = _require_unique(trace_records, "trace_id", "DUPLICATE_LIFECYCLE_ID")
    event_records = list(contracts["lifecycle_events"])
    _require_unique(event_records, "event_id", "DUPLICATE_LIFECYCLE_ID")
    mclt_contracts = list(contracts["mclt_contracts"])
    _require_unique(mclt_contracts, "mclt_id", "DUPLICATE_LIFECYCLE_ID")

    maturity_dimensions = list(contracts["maturity_dimensions"])
    dimensions: dict[str, set[str]] = {}
    for dimension in maturity_dimensions:
        dimension_id = str(dimension["dimension_id"])
        values = {str(value) for value in dimension["allowed_values"]}
        if dimension_id in dimensions:
            raise ProjectionError(
                "DUPLICATE_LIFECYCLE_ID",
                f"Duplicate maturity dimension id: {dimension_id}",
            )
        dimensions[dimension_id] = values

    required_dimensions = {
        "LifecycleSlot",
        "EpistemicRank",
        "ConstitutionalMaturity",
        "RuntimeMaturity",
        "ReleaseMaturity",
        "GeneralityScope",
    }
    if set(dimensions) != required_dimensions:
        raise ProjectionError(
            "INVALID_MATURITY_COORDINATE",
            "SLGE-SDLC-R0 maturity dimensions must exactly cover the required six axes",
        )

    for slot in contracts["lifecycle_slots"]:
        for kind in slot["accepted_artifact_kinds"]:
            if str(kind) not in artifact_kind_ids:
                raise ProjectionError(
                    "UNKNOWN_ARTIFACT_KIND",
                    f"Slot {slot['slot_id']} references unknown artifact kind {kind}",
                )
        for next_slot in slot["allowed_next_slot_refs"]:
            if str(next_slot) not in slot_ids:
                raise ProjectionError(
                    "INVALID_NEXT_SLOT_REFERENCE",
                    f"Slot {slot['slot_id']} has unknown next slot {next_slot}",
                )
        if str(slot["gate_ref"]) not in gate_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                f"Slot {slot['slot_id']} references unknown gate {slot['gate_ref']}",
            )
        for evidence_ref in slot["evidence_policy_refs"]:
            if str(evidence_ref) not in evidence_requirement_ids:
                raise ProjectionError(
                    "INVALID_EVIDENCE_REQUIREMENT",
                    (
                        f"Slot {slot['slot_id']} references unknown evidence "
                        f"requirement {evidence_ref}"
                    ),
                )

    for artifact in project_artifacts:
        artifact_id = str(artifact["artifact_id"])
        kind = str(artifact["artifact_kind"])
        if kind not in artifact_kind_ids:
            raise ProjectionError(
                "UNKNOWN_ARTIFACT_KIND",
                f"Artifact {artifact_id} has unknown artifact kind {kind}",
            )
        current_slot_ref = str(artifact["current_lifecycle_slot_ref"])
        if current_slot_ref not in slot_ids:
            raise ProjectionError(
                "UNKNOWN_LIFECYCLE_SLOT",
                f"Artifact {artifact_id} references unknown lifecycle slot {current_slot_ref}",
            )
        if current_slot_ref not in dimensions["LifecycleSlot"]:
            raise ProjectionError(
                "INVALID_MATURITY_COORDINATE",
                f"Artifact {artifact_id} uses lifecycle slot not declared in maturity dimensions",
            )
        dimension_checks = {
            "EpistemicRank": str(artifact["epistemic_rank_ref"]),
            "ConstitutionalMaturity": str(artifact["constitutional_maturity_ref"]),
            "RuntimeMaturity": str(artifact["runtime_maturity_ref"]),
            "ReleaseMaturity": str(artifact["release_maturity_ref"]),
            "GeneralityScope": str(artifact["generality_scope_ref"]),
        }
        for dimension_id, value in dimension_checks.items():
            if value not in dimensions[dimension_id]:
                raise ProjectionError(
                    "INVALID_MATURITY_COORDINATE",
                    f"Artifact {artifact_id} has invalid {dimension_id} value {value}",
                )
        for evidence_ref in artifact["evidence_requirement_refs"]:
            if str(evidence_ref) not in evidence_requirement_ids:
                raise ProjectionError(
                    "INVALID_EVIDENCE_REQUIREMENT",
                    (
                        f"Artifact {artifact_id} references unknown evidence "
                        f"requirement {evidence_ref}"
                    ),
                )
        for residual_ref in artifact["residual_refs"]:
            if str(residual_ref) not in residual_ids:
                raise ProjectionError(
                    "MISSING_RESIDUAL_POLICY",
                    f"Artifact {artifact_id} references unknown residual {residual_ref}",
                )
        for dependency_ref in artifact["dependency_refs"]:
            if not str(dependency_ref).strip():
                raise ProjectionError(
                    "DANGLING_LIFECYCLE_REFERENCE",
                    f"Artifact {artifact_id} has empty dependency reference",
                )
        for trace_ref in artifact["trace_refs"]:
            if not str(trace_ref).strip():
                raise ProjectionError(
                    "MISSING_TRACE_REQUIREMENT",
                    f"Artifact {artifact_id} has empty trace reference",
                )
        roles = set(str(role) for role in artifact["authority_roles"])
        if "LawAuthority" in roles and "ProjectionRuntimeAuthority" in roles:
            raise ProjectionError(
                "ONTOLOGY_CONFLICT",
                (
                    f"Artifact {artifact_id} cannot hold both LawAuthority and "
                    "ProjectionRuntimeAuthority"
                ),
            )
        if artifact_id.startswith("DOC-") and "ProjectionRuntimeAuthority" in roles:
            raise ProjectionError(
                "INVALID_AUTHORITY_ROLE",
                f"Law document artifact {artifact_id} cannot claim ProjectionRuntimeAuthority",
            )

    for gate in contracts["gate_references"]:
        decision_ref = str(gate["decision_contract_ref"])
        if decision_ref not in gate_decision_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                (
                    f"Gate {gate['gate_id']} references unknown gate decision "
                    f"contract {decision_ref}"
                ),
            )

    for gate_decision in gate_decision_records:
        gate_ref = str(gate_decision["gate_ref"])
        if gate_ref not in gate_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                (
                    f"Gate decision {gate_decision['gate_decision_id']} references unknown "
                    f"gate {gate_ref}"
                ),
            )

    for requirement in evidence_requirements:
        target = str(requirement["target_artifact_or_transition"])
        if target not in project_artifact_ids and target not in transition_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                (
                    f"Evidence requirement {requirement['evidence_requirement_id']} has unknown "
                    f"target {target}"
                ),
            )
        for observed_ref in requirement["observed_refs"]:
            file_path, _, _ = str(observed_ref).partition("#")
            if not (repo_root / file_path).exists():
                raise ProjectionError(
                    "DANGLING_LIFECYCLE_REFERENCE",
                    (
                        f"Evidence requirement {requirement['evidence_requirement_id']} "
                        f"references missing path {observed_ref}"
                    ),
                )

    for contract in transition_contracts:
        from_slot_ref = str(contract["from_slot_ref"])
        to_slot_ref = str(contract["to_slot_ref"])
        if from_slot_ref not in slot_ids or to_slot_ref not in slot_ids:
            raise ProjectionError(
                "UNKNOWN_LIFECYCLE_SLOT",
                (
                    f"Transition {contract['transition_id']} references unknown slot "
                    f"{from_slot_ref} -> {to_slot_ref}"
                ),
            )
        for kind in contract["accepted_artifact_kinds"]:
            if str(kind) not in artifact_kind_ids:
                raise ProjectionError(
                    "UNKNOWN_ARTIFACT_KIND",
                    (
                        f"Transition {contract['transition_id']} references "
                        f"unknown artifact kind {kind}"
                    ),
                )
        for evidence_ref in contract["required_evidence_refs"]:
            if str(evidence_ref) not in evidence_requirement_ids:
                raise ProjectionError(
                    "INVALID_EVIDENCE_REQUIREMENT",
                    (
                        f"Transition {contract['transition_id']} references unknown evidence "
                        f"requirement {evidence_ref}"
                    ),
                )
        if str(contract["required_gate_ref"]) not in gate_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                f"Transition {contract['transition_id']} references unknown gate",
            )
        if not contract["failure_codes"]:
            raise ProjectionError(
                "INVALID_TRANSITION_CONTRACT",
                f"Transition {contract['transition_id']} must define failure codes",
            )

    for residual in residual_records:
        owner = str(residual["owner_artifact"])
        transition_ref = str(residual["transition_ref"])
        trace_ref = str(residual["trace_ref"])
        if owner not in project_artifact_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                f"Residual {residual['residual_id']} references unknown owner artifact {owner}",
            )
        if transition_ref not in transition_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                (
                    f"Residual {residual['residual_id']} references unknown transition "
                    f"{transition_ref}"
                ),
            )
        if trace_ref not in trace_ids and not (repo_root / trace_ref.partition("#")[0]).exists():
            raise ProjectionError(
                "MISSING_TRACE_REQUIREMENT",
                f"Residual {residual['residual_id']} has unresolved trace {trace_ref}",
            )

    for delta in residual_delta_records:
        residual_ref = str(delta["residual_ref"])
        transition_ref = str(delta["transition_ref"])
        trace_ref = str(delta["trace_ref"])
        if residual_ref not in residual_ids:
            raise ProjectionError(
                "MISSING_RESIDUAL_POLICY",
                (
                    f"Residual delta {delta['residual_delta_id']} references unknown "
                    f"residual {residual_ref}"
                ),
            )
        if transition_ref not in transition_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                (
                    f"Residual delta {delta['residual_delta_id']} references unknown "
                    f"transition {transition_ref}"
                ),
            )
        if trace_ref not in trace_ids and not (repo_root / trace_ref.partition("#")[0]).exists():
            raise ProjectionError(
                "MISSING_TRACE_REQUIREMENT",
                (
                    f"Residual delta {delta['residual_delta_id']} has unresolved trace "
                    f"{trace_ref}"
                ),
            )

    for trace in trace_records:
        artifact_id = str(trace["artifact_id"])
        transition_ref = str(trace["transition_ref"])
        if artifact_id not in project_artifact_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                f"Trace {trace['trace_id']} references unknown artifact {artifact_id}",
            )
        if transition_ref not in transition_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                f"Trace {trace['trace_id']} references unknown transition {transition_ref}",
            )
        if str(trace["gate_decision_ref"]) not in gate_decision_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                (
                    f"Trace {trace['trace_id']} references unknown gate decision "
                    f"{trace['gate_decision_ref']}"
                ),
            )
        for evidence_ref in trace["evidence_refs"]:
            if str(evidence_ref) not in evidence_requirement_ids:
                raise ProjectionError(
                    "INVALID_EVIDENCE_REQUIREMENT",
                    (
                        f"Trace {trace['trace_id']} references unknown evidence "
                        f"requirement {evidence_ref}"
                    ),
                )
        for residual_ref in trace["residual_refs"]:
            if str(residual_ref) not in residual_ids:
                raise ProjectionError(
                    "MISSING_RESIDUAL_POLICY",
                    f"Trace {trace['trace_id']} references unknown residual {residual_ref}",
                )

    for event in event_records:
        if str(event["artifact_id"]) not in project_artifact_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                f"Event {event['event_id']} references unknown artifact",
            )
        if str(event["transition_contract_ref"]) not in transition_ids:
            raise ProjectionError(
                "INVALID_TRANSITION_CONTRACT",
                f"Event {event['event_id']} references unknown transition contract",
            )
        from_slot_ref = str(event["from_slot_ref"])
        to_slot_ref = str(event["to_slot_ref"])
        if from_slot_ref not in slot_ids or to_slot_ref not in slot_ids:
            raise ProjectionError(
                "UNKNOWN_LIFECYCLE_SLOT",
                f"Event {event['event_id']} references unknown slot",
            )
        if str(event["gate_decision_ref"]) not in gate_decision_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                (
                    f"Event {event['event_id']} references unknown gate decision "
                    f"{event['gate_decision_ref']}"
                ),
            )
        for evidence_ref in event["evidence_refs"]:
            if str(evidence_ref) not in evidence_requirement_ids:
                raise ProjectionError(
                    "INVALID_EVIDENCE_REQUIREMENT",
                    (
                        f"Event {event['event_id']} references unknown evidence "
                        f"requirement {evidence_ref}"
                    ),
                )
        for residual_delta in event["residual_delta_refs"]:
            if str(residual_delta) not in residual_delta_ids:
                raise ProjectionError(
                    "MISSING_RESIDUAL_POLICY",
                    (
                        f"Event {event['event_id']} references unknown residual delta "
                        f"{residual_delta}"
                    ),
                )
        trace_ref = str(event["trace_ref"])
        if trace_ref not in trace_ids:
            raise ProjectionError(
                "MISSING_TRACE_REQUIREMENT",
                f"Event {event['event_id']} references unknown trace id {trace_ref}",
            )

    for mclt in mclt_contracts:
        if str(mclt["artifact_id_ref"]) not in project_artifact_ids:
            raise ProjectionError(
                "INVALID_MCLT_CONTRACT",
                f"MCLT {mclt['mclt_id']} references unknown artifact",
            )
        from_slot_ref = str(mclt["from_slot_ref"])
        to_slot_ref = str(mclt["to_slot_ref"])
        if from_slot_ref not in slot_ids or to_slot_ref not in slot_ids:
            raise ProjectionError(
                "UNKNOWN_LIFECYCLE_SLOT",
                f"MCLT {mclt['mclt_id']} references unknown slots",
            )
        if str(mclt["transition_contract_ref"]) not in transition_ids:
            raise ProjectionError(
                "INVALID_MCLT_CONTRACT",
                f"MCLT {mclt['mclt_id']} references unknown transition contract",
            )
        for evidence_ref in mclt["evidence_bundle_refs"]:
            if str(evidence_ref) not in evidence_requirement_ids:
                raise ProjectionError(
                    "INVALID_EVIDENCE_REQUIREMENT",
                    (
                        f"MCLT {mclt['mclt_id']} references unknown evidence "
                        f"requirement {evidence_ref}"
                    ),
                )
        if str(mclt["gate_decision_ref"]) not in gate_decision_ids:
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                (
                    f"MCLT {mclt['mclt_id']} references unknown gate decision "
                    f"{mclt['gate_decision_ref']}"
                ),
            )
        for residual_delta in mclt["residual_delta_refs"]:
            if str(residual_delta) not in residual_delta_ids:
                raise ProjectionError(
                    "MISSING_RESIDUAL_POLICY",
                    (
                        f"MCLT {mclt['mclt_id']} references unknown residual delta "
                        f"{residual_delta}"
                    ),
                )
        if str(mclt["trace_ref"]) not in trace_ids:
            raise ProjectionError(
                "MISSING_TRACE_REQUIREMENT",
                f"MCLT {mclt['mclt_id']} references unknown trace id",
            )


def _validate_slge_m0_remap(
    repo_root: Path,
    remap: dict[str, Any],
    artifact_ids: set[str],
    branch_ids: set[str],
    residual_ids: set[str],
) -> None:
    if remap["branch_ref"] != "SLGE-SDLC-M0":
        raise ProjectionError(
            "INVALID_LEGACY_SLOT_MAPPING",
            "SLGE-SDLC-M0 remap contract must declare branch_ref as SLGE-SDLC-M0",
        )

    fixture_ids = _require_unique(
        remap["contract_fixtures"],
        "fixture_id",
        "DUPLICATE_REMAP_RECORD",
    )
    remap_evidence = remap["remap_evidence_records"]
    evidence_ids = _require_unique(remap_evidence, "evidence_id", "DUPLICATE_REMAP_RECORD")
    authoritative = remap["authoritative_legacy_remap_records"]
    remap_ids = _require_unique(authoritative, "remap_id", "DUPLICATE_REMAP_RECORD")
    _require_unique(remap["rank_mapping_contracts"], "mapping_id", "DUPLICATE_REMAP_RECORD")
    _require_unique(
        remap["authority_surface_contracts"],
        "artifact_id",
        "DUPLICATE_ARTIFACT_COVERAGE",
    )
    local_residual_ids = _require_unique(
        remap["residual_records"],
        "residual_id",
        "DUPLICATE_REMAP_RECORD",
    )

    for fixture in remap["contract_fixtures"]:
        if fixture["is_authoritative"]:
            raise ProjectionError(
                "FIXTURE_USED_AS_AUTHORITY",
                f"Fixture {fixture['fixture_id']} cannot be authoritative",
            )

    remap_decisions = set(remap["remap_decision_values"])
    historical_status_values = set(remap["historical_transition_status_values"])
    eligible = set(str(artifact_id) for artifact_id in remap["eligible_artifact_ids"])
    coverage = remap["coverage_ledger"]
    covered_artifacts: set[str] = set()
    remap_by_id = {record["remap_id"]: record for record in authoritative}
    remap_by_artifact: dict[str, dict[str, Any]] = {}

    for record in authoritative:
        artifact_id = str(record["artifact_id"])
        if artifact_id in remap_by_artifact:
            raise ProjectionError(
                "DUPLICATE_ARTIFACT_COVERAGE",
                f"Duplicate authoritative remap coverage for artifact {artifact_id}",
            )
        remap_by_artifact[artifact_id] = record

        if record["record_class"] != "AuthoritativeLegacyRemap":
            raise ProjectionError(
                "FIXTURE_USED_AS_AUTHORITY",
                f"Non-authoritative class used in remap record {record['remap_id']}",
            )
        if artifact_id not in artifact_ids:
            raise ProjectionError(
                "DANGLING_REMAP_REFERENCE",
                f"Remap record {record['remap_id']} references unknown artifact {artifact_id}",
            )
        if str(record["inferred_lifecycle_slot"]) != "SLGE-SDLC-M0":
            raise ProjectionError(
                "INVALID_LEGACY_SLOT_MAPPING",
                (
                    f"Remap record {record['remap_id']} must infer lifecycle slot "
                    "SLGE-SDLC-M0"
                ),
            )
        if str(record["remap_decision"]) not in remap_decisions:
            raise ProjectionError(
                "INVALID_REMAP_DECISION",
                f"Invalid remap decision in {record['remap_id']}",
            )
        if str(record["historical_transition_status"]) not in historical_status_values:
            raise ProjectionError(
                "HISTORICAL_TRANSITION_UNPROVEN",
                f"Unknown historical transition status in {record['remap_id']}",
            )

        if not record["decision_evidence_refs"]:
            raise ProjectionError(
                "MISSING_REMAP_EVIDENCE",
                f"Remap record {record['remap_id']} must include decision evidence refs",
            )
        for evidence_ref in record["decision_evidence_refs"]:
            if str(evidence_ref) not in evidence_ids:
                raise ProjectionError(
                    "DANGLING_REMAP_REFERENCE",
                    (
                        f"Remap record {record['remap_id']} references unknown evidence "
                        f"id {evidence_ref}"
                    ),
                )

        status = str(record["historical_transition_status"])
        mclt_ref = record["historical_mclt_ref"]
        if status != "PROVEN" and mclt_ref not in (None, ""):
            raise ProjectionError(
                "SYNTHETIC_HISTORICAL_MCLT_FORBIDDEN",
                (
                    f"Remap record {record['remap_id']} cannot claim historical MCLT "
                    f"for status {status}"
                ),
            )
        if status in {"UNKNOWN", "UNASSESSED", "PARTIAL", "REFUSED"} and not record[
            "unresolved_residual_refs"
        ]:
            raise ProjectionError(
                "HISTORICAL_TRANSITION_UNPROVEN",
                (
                    f"Remap record {record['remap_id']} must keep residual visibility "
                    "for unproven historical transition"
                ),
            )
        if status in {"UNKNOWN", "UNASSESSED", "PARTIAL", "REFUSED"} and (
            "HISTORICAL_MCLT_NOT_PROVEN" not in set(record["unresolved_residual_refs"])
        ):
            raise ProjectionError(
                "LEGACY_HISTORY_GAP",
                (
                    f"Remap record {record['remap_id']} must include "
                    "HISTORICAL_MCLT_NOT_PROVEN residual"
                ),
            )

        for residual_ref in record["unresolved_residual_refs"]:
            residual_ref = str(residual_ref)
            if residual_ref not in residual_ids and residual_ref not in local_residual_ids:
                raise ProjectionError(
                    "DANGLING_REMAP_REFERENCE",
                    (
                        f"Remap record {record['remap_id']} references unknown residual "
                        f"{residual_ref}"
                    ),
                )

        decision = str(record["remap_decision"])
        if decision == "QUARANTINE" and not record.get("quarantine_reason"):
            raise ProjectionError(
                "QUARANTINE_REASON_REQUIRED",
                f"Remap record {record['remap_id']} requires quarantine_reason",
            )
        if decision == "REBUILD" and not record.get("rebuild_requirement"):
            raise ProjectionError(
                "REBUILD_REQUIREMENT_REQUIRED",
                f"Remap record {record['remap_id']} requires rebuild_requirement",
            )

        rank_mapping = record["epistemic_rank_mapping"]
        for status_key in ("core_rank_mapping_status", "learning_rank_mapping_status"):
            mapping_status = str(rank_mapping[status_key])
            mapping_ref = rank_mapping["mapping_ref"]
            if mapping_status == "MAPPED" and not mapping_ref:
                raise ProjectionError(
                    "RANK_MAPPING_UNLICENSED",
                    (
                        f"Remap record {record['remap_id']} claims mapped rank semantics "
                        f"without mapping_ref"
                    ),
                )
            if mapping_status == "NO_LICENSED_MAPPING" and mapping_ref:
                raise ProjectionError(
                    "RANK_MAPPING_UNLICENSED",
                    (
                        f"Remap record {record['remap_id']} provides mapping_ref for "
                        "NO_LICENSED_MAPPING status"
                    ),
                )

        executing_surfaces = [str(path) for path in record["authority_roles"]["executing_surfaces"]]
        for path in executing_surfaces:
            if path.startswith("docs/") or path.startswith("tests/") or path.endswith(".md"):
                raise ProjectionError(
                    "AUTHORITY_INFLATION",
                    (
                        f"Remap record {record['remap_id']} uses non-executing path "
                        f"as execution authority: {path}"
                    ),
                )

    for evidence in remap_evidence:
        artifact_id = str(evidence["artifact_id"])
        if artifact_id not in eligible:
                raise ProjectionError(
                    "DANGLING_REMAP_REFERENCE",
                    (
                        f"Evidence {evidence['evidence_id']} references non-eligible "
                        f"artifact {artifact_id}"
                    ),
                )
        if str(evidence["future_resolution_branch"]) not in branch_ids:
            raise ProjectionError(
                "DANGLING_REMAP_REFERENCE",
                (
                    f"Evidence {evidence['evidence_id']} references unknown future branch "
                    f"{evidence['future_resolution_branch']}"
                ),
            )
        for observed_ref in evidence["observed_refs"]:
            file_path, _, _ = str(observed_ref).partition("#")
            if not (repo_root / file_path).exists():
                raise ProjectionError(
                    "DANGLING_REMAP_REFERENCE",
                    f"Evidence {evidence['evidence_id']} has missing observed ref {observed_ref}",
                )

    for mapping in remap["rank_mapping_contracts"]:
        mapping_status = str(mapping["mapping_status"])
        mapping_ref = mapping["mapping_ref"]
        if mapping_status == "LICENSED_MAPPING" and not mapping_ref:
            raise ProjectionError(
                "RANK_MAPPING_UNLICENSED",
                f"Rank mapping {mapping['mapping_id']} is licensed but missing mapping_ref",
            )
        if mapping_status == "NO_LICENSED_MAPPING" and mapping_ref:
            raise ProjectionError(
                "RANK_MAPPING_UNLICENSED",
                f"Rank mapping {mapping['mapping_id']} provides mapping_ref while unlicensed",
            )

    for surface in remap["authority_surface_contracts"]:
        artifact_id = str(surface["artifact_id"])
        if artifact_id not in eligible:
            raise ProjectionError(
                "DANGLING_REMAP_REFERENCE",
                f"Authority surface contract references non-eligible artifact {artifact_id}",
            )
        executing = {str(path) for path in surface["executing_surface_refs"]}
        supporting = {str(path) for path in surface["supporting_surface_refs"]}
        if executing.intersection(supporting):
            raise ProjectionError(
                "AUTHORITY_INFLATION",
                (
                    f"Authority surface {artifact_id} has same path in supporting "
                    "and executing surfaces"
                ),
            )

    for residual in remap["residual_records"]:
        target = str(residual["target_resolution_branch"])
        if target not in branch_ids:
            raise ProjectionError(
                "DANGLING_REMAP_REFERENCE",
                f"Residual {residual['residual_id']} references unknown branch {target}",
            )
        trace_path, _, _ = str(residual["trace_ref"]).partition("#")
        if not (repo_root / trace_path).exists():
            raise ProjectionError(
                "DANGLING_REMAP_REFERENCE",
                f"Residual {residual['residual_id']} has missing trace path {trace_path}",
            )

    for entry in coverage:
        artifact_id = str(entry["artifact_id"])
        if artifact_id in covered_artifacts:
            raise ProjectionError(
                "DUPLICATE_ARTIFACT_COVERAGE",
                f"Duplicate coverage entry for artifact {artifact_id}",
            )
        covered_artifacts.add(artifact_id)
        if artifact_id not in eligible:
            raise ProjectionError(
                "DANGLING_REMAP_REFERENCE",
                f"Coverage entry references non-eligible artifact {artifact_id}",
            )
        if artifact_id not in artifact_ids:
            raise ProjectionError(
                "DANGLING_REMAP_REFERENCE",
                f"Coverage entry references unknown governed artifact {artifact_id}",
            )
        status = str(entry["coverage_status"])
        if status == "OUT_OF_SCOPE_WITH_REASON":
            if not entry.get("out_of_scope_reason"):
                raise ProjectionError(
                    "MISSING_REMAP_COVERAGE",
                    f"Out-of-scope entry for {artifact_id} requires out_of_scope_reason",
                )
            continue

        remap_record_id = str(entry.get("remap_record_id", ""))
        if not remap_record_id:
            raise ProjectionError(
                "MISSING_REMAP_COVERAGE",
                f"Covered entry for {artifact_id} requires remap_record_id",
            )
        if remap_record_id in fixture_ids:
            raise ProjectionError(
                "FIXTURE_USED_AS_AUTHORITY",
                (
                    f"Coverage entry for {artifact_id} references fixture "
                    f"{remap_record_id} as authority"
                ),
            )
        if remap_record_id not in remap_ids:
            raise ProjectionError(
                "DANGLING_REMAP_REFERENCE",
                (
                    f"Coverage entry for {artifact_id} references unknown remap record "
                    f"{remap_record_id}"
                ),
            )
        record = remap_by_id[remap_record_id]
        if str(record["artifact_id"]) != artifact_id:
            raise ProjectionError(
                "DUPLICATE_ARTIFACT_COVERAGE",
                (
                    f"Coverage entry {artifact_id} mismatches remap record "
                    f"{remap_record_id} artifact {record['artifact_id']}"
                ),
            )

    if covered_artifacts != eligible:
        missing = sorted(eligible.difference(covered_artifacts))
        extra = sorted(covered_artifacts.difference(eligible))
        raise ProjectionError(
            "MISSING_REMAP_COVERAGE",
            (
                "Coverage ledger must equal eligible artifact set; "
                f"missing={missing} extra={extra}"
            ),
        )

    if set(remap_by_artifact) != eligible:
        missing = sorted(eligible.difference(set(remap_by_artifact)))
        extra = sorted(set(remap_by_artifact).difference(eligible))
        raise ProjectionError(
            "MISSING_REMAP_COVERAGE",
            (
                "Authoritative remap records must cover each eligible artifact once; "
                f"missing={missing} extra={extra}"
            ),
        )


def _validate_slge_e0_runtime_contract(repo_root: Path, contract: dict[str, Any]) -> None:
    if str(contract["branch_ref"]) != "SLGE-SDLC-E0":
        raise ProjectionError(
            "TRANSITION_NOT_LICENSED",
            "SLGE-SDLC-E0 runtime contract must declare branch_ref as SLGE-SDLC-E0",
        )

    runtime_ref = str(contract["runtime_ref"])
    if not (repo_root / runtime_ref).exists():
        raise ProjectionError(
            "DANGLING_LIFECYCLE_REFERENCE",
            f"SLGE-SDLC-E0 runtime_ref path is missing: {runtime_ref}",
        )

    temporal_cut = contract["temporal_cut"]
    if str(temporal_cut["cut_id"]) != "T_SLGE":
        raise ProjectionError(
            "TEMPORAL_CUT_VIOLATION",
            "SLGE-SDLC-E0 temporal cut id must be T_SLGE",
        )
    if int(temporal_cut["minimum_governance_order"]) < int(
        temporal_cut["minimum_dependency_order"]
    ):
        raise ProjectionError(
            "TEMPORAL_CUT_VIOLATION",
            "SLGE-SDLC-E0 temporal cut cannot have governance order lower than dependency order",
        )

    decision_states = {str(item) for item in contract["decision_states"]}
    required_states = {"APPROVED", "REFUSED", "DEFERRED", "SUSPENDED"}
    if decision_states != required_states:
        raise ProjectionError(
            "INVALID_TRANSITION_CONTRACT",
            "SLGE-SDLC-E0 decision_states must exactly match APPROVED/REFUSED/DEFERRED/SUSPENDED",
        )

    required_failure_codes = {
        "TEMPORAL_CUT_VIOLATION",
        "HISTORICAL_CERTIFICATION_FORBIDDEN",
        "HISTORICAL_MCLT_FABRICATION_FORBIDDEN",
        "LEGACY_BASELINE_REQUIRED",
        "REBUILD_REQUIRES_NEW_LINEAGE",
        "QUARANTINED_SOURCE",
        "UNCERTAIN_LEGACY_SLOT",
        "TRANSITION_NOT_LICENSED",
        "EVIDENCE_INSUFFICIENT",
        "GATE_NOT_APPROVED",
        "BLOCKING_RESIDUAL",
        "RESIDUAL_RESOLUTION_NOT_AUTHORIZED",
        "RANK_AUTHORITY_EXCEEDED",
        "TRACE_LOSS",
        "BACKWARD_PROOF_FAILED",
        "FORWARD_READINESS_FAILED",
        "TRIANGLE_COHERENCE_FAILED",
    }
    failure_codes = {str(item) for item in contract["failure_codes"]}
    missing_failure_codes = sorted(required_failure_codes.difference(failure_codes))
    if missing_failure_codes:
        raise ProjectionError(
            "INVALID_TRANSITION_CONTRACT",
            f"SLGE-SDLC-E0 failure_codes missing required entries: {missing_failure_codes}",
        )

    required_invariants = {
        "CurrentRuntimeAdmission != HistoricalCertification",
        "ResidualConsumption != ResidualResolution",
        "RebuildCreatesNewLicensedLineage != RepairsUnknownPast",
        "historical_status != PROVEN -> historical_mclt_ref = null",
    }
    invariants = {str(item) for item in contract["core_invariants"]}
    missing_invariants = sorted(required_invariants.difference(invariants))
    if missing_invariants:
        raise ProjectionError(
            "INVALID_TRANSITION_CONTRACT",
            f"SLGE-SDLC-E0 core_invariants missing required entries: {missing_invariants}",
        )

    required_predicates = {
        "IdentityPreserved",
        "OriginPreserved",
        "DomainScopeValid",
        "TemporalPolicyValid",
        "SourceStateAdmissible",
        "TransitionContractValid",
        "PreconditionsSatisfied",
        "EvidenceAdequate",
        "GateApproved",
        "RankAuthorityBounded",
        "ResidualPolicySatisfied",
        "TraceReconstructible",
        "BackwardProofValid",
        "ForwardReadinessValid",
        "TriangleCoherenceValid",
    }
    predicates = {str(item) for item in contract["mclt_approval_predicates"]}
    missing_predicates = sorted(required_predicates.difference(predicates))
    if missing_predicates:
        raise ProjectionError(
            "INVALID_MCLT_CONTRACT",
            f"SLGE-SDLC-E0 mclt_approval_predicates missing required entries: {missing_predicates}",
        )

    if contract["determinism_contract"]["same_input_same_decision"] is not True:
        raise ProjectionError(
            "INVALID_TRANSITION_CONTRACT",
            "SLGE-SDLC-E0 determinism contract must enforce same_input_same_decision=true",
        )

    for ref in contract["origin_refs"]:
        path_ref = str(ref).partition("#")[0]
        if not (repo_root / path_ref).exists():
            raise ProjectionError(
                "DANGLING_LIFECYCLE_REFERENCE",
                f"SLGE-SDLC-E0 origin ref is missing: {ref}",
            )


def load_governance_inputs(repo_root: Path) -> dict[str, Any]:
    schema_validator_registry = _schema_validator(
        repo_root / "schemas/governance/registry.schema.json"
    )
    schema_validator_slge_r0 = _schema_validator(
        repo_root / "schemas/governance/slge_sdlc_r0_contracts.schema.json"
    )
    schema_validator_slge_m0 = _schema_validator(
        repo_root / "schemas/governance/slge_sdlc_m0_legacy_remap.schema.json"
    )
    schema_validator_slge_e0 = _schema_validator(
        repo_root / "schemas/governance/slge_sdlc_e0_runtime.schema.json"
    )

    source_bytes = {
        rel_path: _read_bytes(repo_root / rel_path)
        for rel_path in GOVERNANCE_INPUT_FILES
    }

    artifacts = _load_json(repo_root / "governance/registry/artifacts.json")
    branches = _load_json(repo_root / "governance/registry/branches.json")
    dependencies = _load_json(repo_root / "governance/registry/dependencies.json")
    runtime_map = _load_json(repo_root / "governance/registry/runtime_map.json")
    evidence_map = _load_json(repo_root / "governance/registry/evidence_map.json")
    residuals = _load_json(repo_root / "governance/registry/residuals.json")
    projection_inputs_payload = _load_json(repo_root / "governance/registry/projection_inputs.json")
    slge_r0_contracts = _load_json(repo_root / "governance/registry/slge_sdlc_r0_contracts.json")
    slge_m0_remap = _load_json(repo_root / "governance/registry/slge_sdlc_m0_legacy_remap.json")
    slge_e0_runtime = _load_json(repo_root / "governance/registry/slge_sdlc_e0_runtime.json")

    for rel_path, payload in (
        ("governance/registry/artifacts.json", artifacts),
        ("governance/registry/branches.json", branches),
        ("governance/registry/dependencies.json", dependencies),
        ("governance/registry/runtime_map.json", runtime_map),
        ("governance/registry/evidence_map.json", evidence_map),
        ("governance/registry/residuals.json", residuals),
        ("governance/registry/projection_inputs.json", projection_inputs_payload),
    ):
        _validate_schema(schema_validator_registry, payload, repo_root / rel_path)
    _validate_schema(
        schema_validator_slge_r0,
        slge_r0_contracts,
        repo_root / "governance/registry/slge_sdlc_r0_contracts.json",
    )
    _validate_schema(
        schema_validator_slge_m0,
        slge_m0_remap,
        repo_root / "governance/registry/slge_sdlc_m0_legacy_remap.json",
    )
    _validate_schema(
        schema_validator_slge_e0,
        slge_e0_runtime,
        repo_root / "governance/registry/slge_sdlc_e0_runtime.json",
    )

    history_records = _parse_amendments_jsonl(repo_root / "governance/history/amendments.jsonl")

    projection_inputs = projection_inputs_payload["projection_inputs"]

    return {
        "history_records": history_records,
        "artifacts": artifacts["artifacts"],
        "branches": branches["branch_statuses"],
        "dependencies": dependencies["dependency_edges"],
        "runtime_map": runtime_map["runtime_map"],
        "evidence_requirements": evidence_map["evidence_requirements"],
        "residuals": residuals["residuals"],
        "projection_inputs": projection_inputs,
        "slge_r0_contracts": slge_r0_contracts,
        "slge_m0_remap": slge_m0_remap,
        "slge_e0_runtime": slge_e0_runtime,
        "source_bytes": source_bytes,
    }


def _validate_semantics(repo_root: Path, inputs: dict[str, Any]) -> None:
    artifacts = list(inputs["artifacts"])
    branches = list(inputs["branches"])
    dependencies = list(inputs["dependencies"])
    runtime_map = list(inputs["runtime_map"])
    evidence_requirements = list(inputs["evidence_requirements"])
    residuals = list(inputs["residuals"])
    projection_inputs = inputs["projection_inputs"]
    slge_r0_contracts = inputs["slge_r0_contracts"]
    slge_m0_remap = inputs["slge_m0_remap"]
    slge_e0_runtime = inputs["slge_e0_runtime"]

    _validate_slge_r0_contracts(repo_root, slge_r0_contracts)

    artifact_ids = _require_unique(artifacts, "artifact_id", "DUPLICATE_ARTIFACT_ID")
    branch_ids = _require_unique(branches, "branch_id", "DUPLICATE_BRANCH_ID")
    dependency_ids = _require_unique(dependencies, "dependency_id", "DUPLICATE_DEPENDENCY_ID")
    requirement_ids = _require_unique(
        evidence_requirements,
        "requirement_id",
        "DUPLICATE_EVIDENCE_REQUIREMENT_ID",
    )
    residual_ids = _require_unique(residuals, "residual_id", "DUPLICATE_RESIDUAL_ID")
    _validate_slge_m0_remap(repo_root, slge_m0_remap, artifact_ids, branch_ids, residual_ids)
    _validate_slge_e0_runtime_contract(repo_root, slge_e0_runtime)

    for artifact in artifacts:
        _require_subset(
            list(artifact["authority_roles"]),
            AUTHORITY_ROLES,
            "INVALID_AUTHORITY_ROLE",
            "authority role",
        )

    for dependency in dependencies:
        relation_kind = str(dependency["relation_kind"])
        if relation_kind not in DEPENDENCY_RELATION_KINDS:
            raise ProjectionError(
                "INVALID_DEPENDENCY_RELATION_KIND",
                f"Unknown relation kind: {relation_kind}",
            )

    for requirement in evidence_requirements:
        kind = str(requirement["evidence_kind"])
        verdict = str(requirement["verdict"])
        if kind not in EVIDENCE_KINDS:
            raise ProjectionError("INVALID_EVIDENCE_KIND", f"Unknown evidence kind: {kind}")
        if verdict not in EVIDENCE_VERDICTS:
            raise ProjectionError(
                "INVALID_EVIDENCE_VERDICT",
                f"Unknown evidence verdict: {verdict}",
            )

    for residual in residuals:
        disposition = str(residual["disposition"])
        if disposition not in RESIDUAL_DISPOSITIONS:
            raise ProjectionError(
                "INVALID_RESIDUAL_DISPOSITION",
                f"Unknown residual disposition: {disposition}",
            )

    synthetic_ids = {
        "RUNTIME_MAP",
        "EVIDENCE_REQUIREMENTS",
        "RESIDUALS",
        "SLGE_SDLC_R0_CONTRACTS",
        "SLGE_SDLC_M0_REMAP",
        "SLGE_SDLC_E0_RUNTIME",
        CURRENT_STATE_PATH,
    }
    evidence_artifact_ids = {
        str(requirement["artifact_id"]) for requirement in evidence_requirements
    }
    external_ids = {
        str(identity)
        for identity in projection_inputs.get("external_governed_identities", [])
        if str(identity)
    }
    history_ids = {str(record["id"]) for record in inputs["history_records"]}
    governed_ids = (
        artifact_ids
        | branch_ids
        | requirement_ids
        | residual_ids
        | history_ids
        | synthetic_ids
        | evidence_artifact_ids
        | external_ids
    )

    for dependency in dependencies:
        source = str(dependency["source_artifact"])
        target = str(dependency["target_artifact"])
        if source not in governed_ids:
            raise ProjectionError("DANGLING_DEPENDENCY_REF", f"Unknown dependency source: {source}")
        if target not in governed_ids:
            raise ProjectionError("DANGLING_DEPENDENCY_REF", f"Unknown dependency target: {target}")
        for residual_id in dependency["residuals"]:
            if residual_id not in residual_ids:
                raise ProjectionError(
                    "DANGLING_RESIDUAL_REF",
                    f"Unknown residual in dependency {dependency['dependency_id']}: {residual_id}",
                )

    for artifact in artifacts:
        for dep_ref in artifact["dependency_refs"]:
            if dep_ref not in dependency_ids:
                raise ProjectionError(
                    "DANGLING_DEPENDENCY_REF",
                    (
                        f"Artifact {artifact['artifact_id']} references "
                        f"unknown dependency id {dep_ref}"
                    ),
                )
        for req_ref in artifact["evidence_requirements"]:
            if req_ref not in requirement_ids:
                raise ProjectionError(
                    "DANGLING_EVIDENCE_REF",
                    f"Artifact {artifact['artifact_id']} references unknown requirement {req_ref}",
                )
        for residual_ref in artifact["residual_refs"]:
            if residual_ref not in residual_ids:
                raise ProjectionError(
                    "DANGLING_RESIDUAL_REF",
                    (
                        f"Artifact {artifact['artifact_id']} references "
                        f"unknown residual {residual_ref}"
                    ),
                )

    for requirement in evidence_requirements:
        if str(requirement["artifact_id"]) not in governed_ids:
            raise ProjectionError(
                "DANGLING_EVIDENCE_REF",
                (
                    f"Requirement {requirement['requirement_id']} has "
                    f"unknown artifact_id {requirement['artifact_id']}"
                ),
            )
        residual = requirement.get("residual")
        if residual and str(residual) not in residual_ids:
            raise ProjectionError(
                "DANGLING_RESIDUAL_REF",
                (
                    f"Requirement {requirement['requirement_id']} references "
                    f"unknown residual {residual}"
                ),
            )

    for item in runtime_map:
        if str(item["branch_id"]) not in branch_ids:
            raise ProjectionError(
                "DANGLING_BRANCH_REF",
                f"runtime_map references unknown branch {item['branch_id']}",
            )

    for residual in residuals:
        owner = str(residual["owner_artifact"])
        origin = str(residual["origin_transition"])
        target_branch = str(residual["target_resolution_branch"])
        if owner not in governed_ids:
            raise ProjectionError("DANGLING_RESIDUAL_OWNER", f"Unknown residual owner {owner}")
        if origin not in governed_ids:
            raise ProjectionError(
                "DANGLING_RESIDUAL_OWNER",
                f"Unknown residual origin transition {origin}",
            )
        if target_branch not in branch_ids and target_branch not in external_ids:
            raise ProjectionError(
                "DANGLING_BRANCH_REF",
                f"Unknown residual target_resolution_branch {target_branch}",
            )

    path_refs: set[str] = set()
    for artifact in artifacts:
        path_refs.update(str(path) for path in artifact["runtime_refs"])
        path_refs.update(str(path) for path in artifact["evidence_refs"])
        path_refs.update(str(path) for path in artifact["trace_refs"])
    for requirement in evidence_requirements:
        path_refs.update(str(path) for path in requirement["observed_refs"])
    for dependency in dependencies:
        evidence_ref = str(dependency["evidence_ref"])
        path_refs.add(evidence_ref)
    for residual in residuals:
        path_refs.add(str(residual["trace_ref"]))

    projection_trace_refs = projection_inputs.get("projection_trace_refs", [])
    if not isinstance(projection_trace_refs, list) or not projection_trace_refs:
        raise ProjectionError(
            "PROJECTION_SCHEMA_INVALID",
            "projection_inputs.projection_trace_refs must be a non-empty list",
        )
    path_refs.update(str(path) for path in projection_trace_refs)

    for rel_path in sorted(path_refs):
        if not rel_path:
            raise ProjectionError(
                "PROJECTION_SCHEMA_INVALID",
                "Empty trace/path reference is not allowed",
            )
        file_path, _, _ = rel_path.partition("#")
        if not (repo_root / file_path).exists():
            raise ProjectionError("DANGLING_ARTIFACT_REF", f"Missing referenced path: {rel_path}")


def _sorted_unique(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def project_repository_state(inputs: dict[str, Any]) -> dict[str, Any]:
    artifacts = list(inputs["artifacts"])
    branches = list(inputs["branches"])
    evidence_requirements = list(inputs["evidence_requirements"])
    residuals = list(inputs["residuals"])
    projection_inputs = inputs["projection_inputs"]
    source_bytes = dict(inputs["source_bytes"])

    law_authority: list[str] = []
    runtime_authority: list[str] = []
    projection_contract_authority: list[str] = []
    projection_runtime_authority: list[str] = []
    evidence_authority: list[str] = []
    historical_authority: list[str] = ["governance/history/amendments.jsonl"]
    current_state_projection_authority: list[str] = [CURRENT_STATE_PATH]

    for artifact in artifacts:
        roles = set(artifact["authority_roles"])
        if "LawAuthority" in roles:
            law_authority.extend(artifact["evidence_refs"])
            law_authority.extend(artifact["trace_refs"])
        if "RuntimeAuthority" in roles:
            runtime_authority.extend(artifact["runtime_refs"])
        if "ProjectionContractAuthority" in roles:
            projection_contract_authority.extend(artifact["evidence_refs"])
            projection_contract_authority.extend(artifact["trace_refs"])
        if "ProjectionRuntimeAuthority" in roles:
            projection_runtime_authority.extend(artifact["runtime_refs"])
        if "CurrentStateProjectionAuthority" in roles:
            current_state_projection_authority.extend(artifact["trace_refs"])
        if "EvidenceAuthority" in roles:
            evidence_authority.extend(artifact["evidence_refs"])
            evidence_authority.extend(artifact["runtime_refs"])
        if "HistoricalAuthority" in roles:
            historical_authority.extend(artifact["evidence_refs"])
            historical_authority.extend(artifact["trace_refs"])
        if "ProjectionAuthority" in roles:
            projection_contract_authority.extend(artifact["evidence_refs"])
            projection_contract_authority.extend(artifact["trace_refs"])

    for branch in branches:
        roles = set(branch["authority_roles"])
        refs = list(branch.get("primary_refs", []))
        if "LawAuthority" in roles:
            law_authority.extend(refs)
        if "RuntimeAuthority" in roles:
            runtime_authority.extend(refs)
        if "ProjectionContractAuthority" in roles:
            projection_contract_authority.extend(refs)
        if "ProjectionRuntimeAuthority" in roles:
            projection_runtime_authority.extend(refs)
        if "CurrentStateProjectionAuthority" in roles:
            current_state_projection_authority.extend(refs)
        if "EvidenceAuthority" in roles:
            evidence_authority.extend(refs)
        if "HistoricalAuthority" in roles:
            historical_authority.extend(refs)
        if "ProjectionAuthority" in roles:
            projection_contract_authority.extend(refs)

    v1_requirement = next(
        (
            requirement
            for requirement in evidence_requirements
            if requirement["artifact_id"] == "V1-44"
            and requirement["evidence_kind"] == "ClosureEvidence"
        ),
        None,
    )
    if v1_requirement is None:
        raise ProjectionError("DANGLING_EVIDENCE_REF", "Missing V1-44 closure evidence requirement")

    observatory_program = projection_inputs["observatory_program"]
    gua_pilot_domains = projection_inputs["gua_pilot_domains"]

    active_residuals = [
        str(residual["residual_id"])
        for residual in residuals
        if residual["visibility"] == "VISIBLE" and residual["disposition"] != "CLOSED"
    ]

    input_fingerprints = {
        rel_path: hashlib.sha256(raw).hexdigest()
        for rel_path, raw in sorted(source_bytes.items())
    }

    projection = {
        "version": str(projection_inputs["version"]),
        "projection_id": "REPO_STATE_SHA256_" + hashlib.sha256(
            "".join(input_fingerprints.values()).encode("utf-8")
        ).hexdigest()[:16],
        "derived_from": {
            "history": "governance/history/amendments.jsonl",
            "registry": [
                "governance/registry/artifacts.json",
                "governance/registry/branches.json",
                "governance/registry/dependencies.json",
                "governance/registry/runtime_map.json",
                "governance/registry/evidence_map.json",
                "governance/registry/residuals.json",
                "governance/registry/projection_inputs.json",
                "governance/registry/slge_sdlc_r0_contracts.json",
                "governance/registry/slge_sdlc_m0_legacy_remap.json",
                "governance/registry/slge_sdlc_e0_runtime.json",
            ],
        },
        "authority_surfaces": {
            "law_authority": _sorted_unique(law_authority),
            "runtime_authority": _sorted_unique(runtime_authority),
            "projection_contract_authority": _sorted_unique(projection_contract_authority),
            "projection_runtime_authority": _sorted_unique(projection_runtime_authority),
            "evidence_authority": _sorted_unique(evidence_authority),
            "historical_authority": _sorted_unique(historical_authority),
            "current_state_projection_authority": _sorted_unique(
                current_state_projection_authority
            ),
            "current_state_projection": [CURRENT_STATE_PATH],
        },
        "highlights": {
            "v1_closure": {
                "objective_v1_44": v1_requirement["verdict"],
                "source": v1_requirement["observed_refs"][0],
                "note": v1_requirement["minimum_requirement"],
            },
            "observatory_program": {
                "scope": observatory_program["scope"],
                "does_not_imply": observatory_program["does_not_imply"],
                "authority_impact": observatory_program["authority_impact"],
            },
            "gua_pilot_domains": {
                "identifier": gua_pilot_domains["identifier"],
                "values": sorted(gua_pilot_domains["values"]),
                "note": gua_pilot_domains["note"],
            },
        },
        "technical_residuals": _sorted_unique(active_residuals),
        "projection_metadata": {
            "projection_schema_version": "2.0.0",
            "projector_algorithm_id": "REPO-ORG-P0.v1",
            "authoritative_inputs": list(GOVERNANCE_INPUT_FILES),
            "source_fingerprints": input_fingerprints,
            "reduction_contract": [
                "StateIsProjection",
                "HistoryAndTypedRecordsAreAuthority",
                "NarrativeViewsAreNotAuthority",
                "NoComputedStateWithoutReconstructibleProvenance",
            ],
        },
    }
    return projection


def _serialize_projection(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def compute_projection_payload(repo_root: Path) -> dict[str, Any]:
    inputs = load_governance_inputs(repo_root)
    _validate_semantics(repo_root, inputs)
    payload = project_repository_state(inputs)

    validator = _schema_validator(repo_root / "schemas/governance/current_state.schema.json")
    _validate_schema(validator, payload, repo_root / CURRENT_STATE_PATH)
    return payload


def check_projection_drift(repo_root: Path) -> None:
    computed = _serialize_projection(compute_projection_payload(repo_root))
    checked_in_path = repo_root / CURRENT_STATE_PATH
    checked_in = _read_bytes(checked_in_path)
    if computed != checked_in:
        raise ProjectionError(
            "PROJECTION_DRIFT",
            f"{CURRENT_STATE_PATH} drifted from deterministic recomputation",
        )


def write_projection(repo_root: Path) -> None:
    payload = compute_projection_payload(repo_root)
    out_path = repo_root / CURRENT_STATE_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    encoded = _serialize_projection(payload)

    with NamedTemporaryFile("wb", dir=out_path.parent, delete=False) as tmp_file:
        tmp_file.write(encoded)
        tmp_name = tmp_file.name
    os.replace(tmp_name, out_path)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="REPO-ORG-P0 deterministic projection tool")
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root (default: current directory)",
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
            print(f"WROTE: {CURRENT_STATE_PATH}")
            return 0

        check_projection_drift(repo_root)
        print("OK: projection matches deterministic recomputation")
        return 0
    except ProjectionError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
