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


def load_governance_inputs(repo_root: Path) -> dict[str, Any]:
    schema_validator_registry = _schema_validator(
        repo_root / "schemas/governance/registry.schema.json"
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

    artifact_ids = _require_unique(artifacts, "artifact_id", "DUPLICATE_ARTIFACT_ID")
    branch_ids = _require_unique(branches, "branch_id", "DUPLICATE_BRANCH_ID")
    dependency_ids = _require_unique(dependencies, "dependency_id", "DUPLICATE_DEPENDENCY_ID")
    requirement_ids = _require_unique(
        evidence_requirements,
        "requirement_id",
        "DUPLICATE_EVIDENCE_REQUIREMENT_ID",
    )
    residual_ids = _require_unique(residuals, "residual_id", "DUPLICATE_RESIDUAL_ID")

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
    evidence_authority: list[str] = []
    historical_authority: list[str] = ["governance/history/amendments.jsonl"]

    for artifact in artifacts:
        roles = set(artifact["authority_roles"])
        if "LawAuthority" in roles:
            law_authority.extend(artifact["evidence_refs"])
            law_authority.extend(artifact["trace_refs"])
        if "RuntimeAuthority" in roles:
            runtime_authority.extend(artifact["runtime_refs"])
        if "EvidenceAuthority" in roles:
            evidence_authority.extend(artifact["evidence_refs"])
            evidence_authority.extend(artifact["runtime_refs"])
        if "HistoricalAuthority" in roles:
            historical_authority.extend(artifact["evidence_refs"])
            historical_authority.extend(artifact["trace_refs"])

    for branch in branches:
        roles = set(branch["authority_roles"])
        refs = list(branch.get("primary_refs", []))
        if "LawAuthority" in roles:
            law_authority.extend(refs)
        if "RuntimeAuthority" in roles:
            runtime_authority.extend(refs)
        if "EvidenceAuthority" in roles:
            evidence_authority.extend(refs)
        if "HistoricalAuthority" in roles:
            historical_authority.extend(refs)

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
            ],
        },
        "authority_surfaces": {
            "law_authority": _sorted_unique(law_authority),
            "runtime_authority": _sorted_unique(runtime_authority),
            "evidence_authority": _sorted_unique(evidence_authority),
            "historical_authority": _sorted_unique(historical_authority),
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
