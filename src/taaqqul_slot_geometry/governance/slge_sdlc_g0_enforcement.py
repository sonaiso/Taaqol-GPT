"""SLGE-SDLC-G0 repository and pull-request lifecycle declaration enforcement."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Any

from taaqqul_slot_geometry.governance import slge_sdlc_p0_projection as p0
from taaqqul_slot_geometry.governance.slge_sdlc_e0_runtime import (
    SLGEE0DecisionState,
    TransitionAttempt,
    TransitionDecision,
    TransitionExecutionContract,
    _evaluate_transition_attempt,
)

G0_RUNTIME_PATH = "src/taaqqul_slot_geometry/governance/slge_sdlc_g0_enforcement.py"
G0_CONTRACT_PATH = "governance/registry/slge_sdlc_g0_runtime.json"
G0_TEST_PATH = "tests/test_slge_sdlc_g0_runtime.py"
G0_TRANSITION_CONTRACT = TransitionExecutionContract(
    transition_contract_ref="TX-SLGE-P0-TO-G0-001",
    from_slot_ref="SLGE-SDLC-P0",
    to_slot_ref="SLGE-SDLC-G0",
    authority_ceiling="RuntimeAuthority",
    rank_ceiling="E1",
    next_openings=("SLGE-SDLC-C0",),
)
_REQUIRED_FIELDS = (
    "Origin law",
    "Origin law reference (file#section)",
    "Branch",
    "Branch of origin (the constitutional branch, not just the local label)",
    "Previous required PR",
    "Current PR (PR-N from docs/14)",
    "Next permitted PR",
    "Does this PR introduce rank behavior?",
    "Does this PR introduce residual behavior?",
    "Does this PR introduce trace behavior?",
)
_REQUIRED_G0_TESTS = (
    "test_accepts_g0_pr_with_derived_p0_state",
    "test_refuses_missing_evidence",
    "test_refuses_unauthorized_stage_jump",
    "test_refuses_missing_trace",
    "test_refuses_approval_prose_without_evidence",
)
_FORBIDDEN_PATH_PART = re.compile(
    r"(^|[/_-])(spell(?:ing)?|orthograph(?:ic|y)?|count(?:ing)?|morpholog(?:y|ical|ies)?|ṣarf)([/_.-]|$)",
    re.IGNORECASE,
)


class G0EnforcementError(ValueError):
    """Named failure when the G0 execution boundary cannot be evaluated."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise G0EnforcementError("G0_CONTRACT_INVALID", f"cannot read {path}") from exc
    if not isinstance(value, dict):
        raise G0EnforcementError("G0_CONTRACT_INVALID", f"{path} must contain an object")
    return value


def _section_lines(body: str, heading: str) -> list[str]:
    lines = body.splitlines()
    selected: list[str] = []
    in_section = False
    for line in lines:
        if line.startswith("#"):
            in_section = line.strip("# ").casefold() == heading.casefold()
            continue
        if in_section:
            selected.append(line)
    return selected


def _field_values(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in body.splitlines():
        question = re.match(
            r"^\s*-\s*(Does this PR introduce (?:rank|residual|trace) behavior\?)"
            r"\s*:?\s*(yes|no)\s*$",
            line,
            re.IGNORECASE,
        )
        if question:
            fields[question.group(1)] = question.group(2).casefold()
            continue
        match = re.match(r"^\s*-\s*([^:]+):\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1).strip()] = match.group(2).strip().strip("`").strip()
    return fields


def _bullets(lines: list[str]) -> tuple[str, ...]:
    return tuple(
        match.group(1).strip()
        for line in lines
        if (match := re.match(r"^\s*-\s+(.+?)\s*$", line))
        and match.group(1).strip() not in {"", "-"}
    )


def _output_bullets(lines: list[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    allowed: list[str] = []
    forbidden: list[str] = []
    boundary: list[str] | None = None
    for line in lines:
        lowered = line.casefold()
        if "this pr is allowed to produce" in lowered:
            boundary = allowed
        elif "this pr is forbidden from producing" in lowered:
            boundary = forbidden
        elif boundary is not None:
            match = re.match(r"^\s*-\s+(.+?)\s*$", line)
            if match:
                boundary.append(match.group(1).strip())
    return tuple(allowed), tuple(forbidden)


def _declared_paths(values: tuple[str, ...]) -> tuple[str, ...]:
    found: list[str] = []
    for value in values:
        for path in re.findall(r"(?:src|tests|docs|governance)/[\w./-]+", value):
            path = path.rstrip(".,;:`)")
            if path not in found:
                found.append(path)
    return tuple(found)


def _declared_test_names(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        name
        for value in values
        for name in re.findall(r"::(test_[A-Za-z0-9_]+)", value)
    )


def _test_references_resolve(root: Path, values: tuple[str, ...]) -> bool:
    for value in values:
        match = re.search(
            r"`?(tests/[\w./-]+\.py)(?:::([A-Za-z_][A-Za-z0-9_]*))?`?",
            value,
        )
        if not match:
            return False
        path, function_name = match.groups()
        test_file = root / path
        if not test_file.is_file():
            return False
        if function_name:
            try:
                tree = ast.parse(test_file.read_text(encoding="utf-8"))
            except (OSError, SyntaxError):
                return False
            if not any(
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == function_name
                for node in ast.walk(tree)
            ):
                return False
    return True


def _reference_resolves(root: Path, value: str) -> bool:
    path, separator, fragment = value.partition("#")
    if not separator or not fragment or not (root / path).is_file():
        return False
    headings = (
        re.sub(r"[^a-z0-9 -]", "", line.lstrip("#").strip().casefold())
        .replace(" ", "-")
        for line in (root / path).read_text(encoding="utf-8").splitlines()
        if line.startswith("#")
    )
    return fragment in headings


def _load_contract(root: Path) -> dict[str, Any]:
    contract = _read_json(root / G0_CONTRACT_PATH)
    if (
        contract.get("branch_ref") != "SLGE-SDLC-G0"
        or contract.get("predecessor_slot_ref") != "SLGE-SDLC-P0"
        or contract.get("next_slot_ref") != "SLGE-SDLC-C0"
        or contract.get("operation") != "EnforceLifecycleDeclarations"
        or contract.get("transition_contract_ref")
        != G0_TRANSITION_CONTRACT.transition_contract_ref
        or contract.get("authority_ceiling") != G0_TRANSITION_CONTRACT.authority_ceiling
        or contract.get("rank_ceiling") != G0_TRANSITION_CONTRACT.rank_ceiling
        or contract.get("required_inputs")
        != ["LifecycleProjection", "EnforcementContracts"]
        or contract.get("residual_policy")
        != {
            "resolved": ["SLGE_G0_PR_ENFORCEMENT_PENDING"],
            "remains_open": ["SLGE_C0_CLOSURE_AUDIT_PENDING"],
        }
        or not {
            "ClosureClaim",
            "SLGE-SDLC-C0",
            "SpellingBridge",
            "CountingRuntime",
            "MorphologyRuntime",
            "ArabicLicensing",
            "V1ClosedClaim",
        }.issubset(contract.get("forbidden_outputs", ()))
    ):
        raise G0EnforcementError("G0_CONTRACT_INVALID", "G0 contract boundary is inconsistent")
    return contract


def _g0_transition(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    try:
        p0.check_projection_drift(root)
        projection = p0.compute_projection_payload(root)
        inputs = p0.load_lifecycle_inputs(root)
    except (p0.LifecycleProjectionError, OSError) as exc:
        code = getattr(exc, "code", "PROJECTION_INPUT_INVALID")
        raise G0EnforcementError(code, str(exc)) from exc

    current = next(
        (
            item
            for item in projection["current_lifecycle_states"]
            if item["artifact_id"] == "SLGE-SDLC-P0-PROJECTION"
        ),
        None,
    )
    if (
        current is None
        or current["current_lifecycle_slot"] != "SLGE-SDLC-G0"
        or current["allowed_next_openings"] != ["SLGE-SDLC-C0"]
    ):
        raise G0EnforcementError(
            "G0_STATE_NOT_DERIVED",
            "G0 must be present as the reducer-derived current slot with C0 as its only successor",
        )

    events = inputs["events"]["applied_lifecycle_events"]
    event = next(
        (
            item
            for item in events
            if item["event_id"] == current["last_applied_event"]
            and item["from_slot_ref"] == "SLGE-SDLC-P0"
            and item["to_slot_ref"] == "SLGE-SDLC-G0"
        ),
        None,
    )
    if event is None:
        raise G0EnforcementError("G0_STATE_NOT_DERIVED", "G0 has no applied P0-to-G0 event")
    prior_event = next(
        (
            item
            for item in events
            if item["artifact_id"] == event["artifact_id"]
            and item["lineage_id"] == event["lineage_id"]
            and item["to_slot_ref"] == "SLGE-SDLC-P0"
            and item["event_order"] < event["event_order"]
        ),
        None,
    )
    if (
        prior_event is None
        or "SLGE-SDLC-G0" not in prior_event["allowed_next_openings"]
        or prior_event["post_state_ref"] != event["source_state_ref"]
    ):
        raise G0EnforcementError("G0_STATE_NOT_DERIVED", "G0 is not licensed by the prior P0 event")
    decisions = inputs["events"]["transition_decisions"]
    decision = next(
        (item for item in decisions if item["decision_id"] == event["decision_ref"]),
        None,
    )
    if decision is None:
        raise G0EnforcementError("G0_STATE_NOT_DERIVED", "G0 event has no transition decision")
    return event, decision, current


def evaluate_pull_request(
    repo_root: Path,
    *,
    pull_request_body: str,
    changed_paths: tuple[str, ...],
) -> TransitionDecision:
    """Evaluate PR declarations against G0 contracts and reducer-derived lifecycle state."""

    root = repo_root.resolve()
    contract = _load_contract(root)
    event, recorded_decision, current = _g0_transition(root)
    fields = _field_values(pull_request_body)

    missing = [field for field in _REQUIRED_FIELDS if not fields.get(field)]
    origin_reference = fields.get("Origin law reference (file#section)", "")
    required_path = (
        "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
        "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
    )
    declaration_matches = (
        fields.get("Origin law") == required_path
        and origin_reference.startswith(required_path + "#")
        and fields.get("Branch") == "SLGE-SDLC-G0"
        and fields.get("Previous required PR") == "SLGE-SDLC-P0"
        and fields.get("Current PR (PR-N from docs/14)") == "SLGE-SDLC-G0"
        and fields.get("Next permitted PR") == "SLGE-SDLC-C0"
    )

    allowed_scope = _bullets(_section_lines(pull_request_body, "Allowed Scope"))
    forbidden_scope = _bullets(_section_lines(pull_request_body, "Forbidden Scope"))
    allowed_outputs, forbidden_outputs = _output_bullets(
        _section_lines(pull_request_body, "Output Boundary")
    )
    constitutional_tests = _bullets(
        _section_lines(pull_request_body, "Constitutional Tests")
    )
    negative_tests = _bullets(_section_lines(pull_request_body, "Negative Tests"))
    residuals = _bullets(_section_lines(pull_request_body, "Residuals After Merge"))

    declared_test_paths = _declared_paths(constitutional_tests + negative_tests)
    test_names = _declared_test_names(constitutional_tests + negative_tests)
    required_refs = (
        required_path,
        "docs/127_SLGE_SDLC_E0_LIFECYCLE_EXECUTION_ENGINE.md",
        "docs/128_SLGE_SDLC_P0_DETERMINISTIC_LIFECYCLE_PROJECTION.md",
        "docs/14_PR_CHAIN_ROADMAP.md",
        G0_RUNTIME_PATH,
        G0_CONTRACT_PATH,
    )
    trace_refs = tuple(
        dict.fromkeys(
            path
            for path in (*required_refs, *declared_test_paths)
            if (root / path).is_file()
        )
    )
    evidence_refs = tuple(
        dict.fromkeys(
            path
            for path in (G0_RUNTIME_PATH, G0_CONTRACT_PATH, *declared_test_paths)
            if (root / path).is_file()
        )
    )
    expected_tests = {G0_TEST_PATH}
    tests_present = (
        bool(constitutional_tests)
        and expected_tests.issubset(declared_test_paths)
        and all(name in test_names for name in _REQUIRED_G0_TESTS)
        and _test_references_resolve(root, constitutional_tests + negative_tests)
    )
    forbidden_changes = tuple(
        path for path in changed_paths if _FORBIDDEN_PATH_PART.search(path.replace("\\", "/"))
    )
    no_closure_claim = any("ClosureClaim" in value for value in forbidden_outputs)
    no_c0_output = any(
        "SLGE-SDLC-C0" in value
        or ("c0" in value.casefold() and "closure" in value.casefold())
        for value in forbidden_outputs
    )
    allowed_output_text = " ".join(allowed_outputs).casefold()
    forbidden_output_terms = (
        "closureclaim",
        "slge-sdlc-c0",
        "closure audit",
        "spellingbridge",
        "spelling bridge",
        "countingruntime",
        "counting runtime",
        "morphologyruntime",
        "morphology runtime",
        "arabiclicensing",
        "arabic licensing",
        "v1closedclaim",
        "v1 closure",
    )
    allowed_outputs_respect_contract = not any(
        term in allowed_output_text for term in forbidden_output_terms
    )
    forbidden_scope_text = " ".join(forbidden_scope).casefold()
    scope_boundaries_declared = all(
        value in forbidden_scope_text
        for value in ("closure", "spelling", "counting", "morphology", "arabic licensing")
    )
    residual_policy = (
        "SLGE_G0_PR_ENFORCEMENT_PENDING"
        not in event["open_residual_refs"]
        and "SLGE_C0_CLOSURE_AUDIT_PENDING" in event["open_residual_refs"]
        and any("SLGE_C0_CLOSURE_AUDIT_PENDING" in item for item in residuals)
    )
    trace_reconstructible = (
        not missing
        and bool(origin_reference)
        and _reference_resolves(root, origin_reference)
        and set(required_refs).issubset(trace_refs)
        and all((root / path).is_file() for path in declared_test_paths)
        and bool(event["trace_refs"])
        and all(
            ref.startswith("trace://") or (root / ref).is_file()
            for ref in event["trace_refs"]
        )
    )
    stage_consistent = (
        declaration_matches
        and bool(allowed_scope)
        and bool(forbidden_scope)
        and bool(allowed_outputs)
        and no_closure_claim
        and no_c0_output
        and allowed_outputs_respect_contract
        and re.search(r"\b(?:SLGE-SDLC-)?G0\b", " ".join(allowed_scope), re.IGNORECASE)
        and scope_boundaries_declared
        and not forbidden_changes
        and current["allowed_next_openings"] == ["SLGE-SDLC-C0"]
        and contract["required_inputs"] == ["LifecycleProjection", "EnforcementContracts"]
    )
    evidence_adequate = tests_present and bool(evidence_refs) and residual_policy
    proof_flags = {
        "identity_preserved": event["artifact_id"] == current["artifact_id"],
        "origin_preserved": declaration_matches,
        "domain_scope_valid": stage_consistent,
        "temporal_policy_valid": event["temporal_epoch_ref"].startswith("T_SLGE::"),
        "source_state_admissible": event["from_slot_ref"] == "SLGE-SDLC-P0",
        "transition_contract_valid": (
            recorded_decision["attempt_id"] == event["decision_ref"].replace("DEC-", "ATTEMPT-")
            or recorded_decision["attempt_id"] == event["decision_id"]
        ),
        "preconditions_satisfied": bool(allowed_scope and forbidden_scope),
        "evidence_adequate": evidence_adequate,
        "gate_approved": evidence_adequate and stage_consistent and trace_reconstructible,
        "rank_authority_bounded": (
            event["rank_ceiling"] == contract["rank_ceiling"]
            and event["authority_ceiling"] == contract["authority_ceiling"]
        ),
        "residual_policy_satisfied": residual_policy,
        "trace_reconstructible": trace_reconstructible,
        "backward_proof_valid": (
            event["source_state_ref"] == "STATE-SLGE-P0-PROJECTION-OPEN"
            and bool(current["trace_refs"])
        ),
        "forward_readiness_valid": (
            event["allowed_next_openings"] == ["SLGE-SDLC-C0"]
        ),
        "triangle_coherence_valid": (
            event["from_slot_ref"] == "SLGE-SDLC-P0"
            and event["to_slot_ref"] == "SLGE-SDLC-G0"
            and current["last_applied_event"] == event["event_id"]
        ),
    }
    attempt = TransitionAttempt(
        attempt_id=event["decision_ref"].replace("DEC-", "ATTEMPT-"),
        artifact_id=event["artifact_id"],
        lineage_ref=event["lineage_id"],
        transition_contract_ref=G0_TRANSITION_CONTRACT.transition_contract_ref,
        from_slot_ref=fields.get("Previous required PR", ""),
        to_slot_ref=fields.get("Current PR (PR-N from docs/14)", ""),
        temporal_epoch_ref=event["temporal_epoch_ref"],
        governance_order=event["governance_order"],
        dependency_order=event["dependency_order"],
        identity_proof_ref=event["source_state_ref"],
        origin_proof_ref=origin_reference or "missing-origin",
        domain_scope_proof_ref=G0_CONTRACT_PATH,
        evidence_refs=evidence_refs,
        residual_refs=tuple(event["open_residual_refs"]),
        blocking_residual_refs=(),
        trace_ref=event["trace_refs"][0] if event["trace_refs"] else "missing-trace",
        backward_proof_ref=event["source_state_ref"],
        forward_readiness_ref="SLGE-SDLC-C0",
        triangle_coherence_ref=event["event_id"],
        **proof_flags,
    )
    computed = _evaluate_transition_attempt(
        attempt,
        legacy_baseline=None,
        contract=G0_TRANSITION_CONTRACT,
    )
    if recorded_decision["state"] != computed.state.value:
        return _evaluate_transition_attempt(
            replace(attempt, gate_approved=False, evidence_adequate=False),
            legacy_baseline=None,
            contract=G0_TRANSITION_CONTRACT,
        )
    return computed


def _changed_paths(base_sha: str, head_sha: str, root: Path) -> tuple[str, ...]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base_sha}...{head_sha}"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise G0EnforcementError("PR_DIFF_UNAVAILABLE", "cannot derive PR changed paths") from exc
    return tuple(path for path in result.stdout.splitlines() if path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SLGE-SDLC-G0 PR declaration gate")
    parser.add_argument("--event", default=os.environ.get("GITHUB_EVENT_PATH"))
    parser.add_argument("--base-sha")
    parser.add_argument("--head-sha")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    try:
        if not args.event or not args.base_sha or not args.head_sha:
            raise G0EnforcementError(
                "PR_EVENT_REQUIRED",
                "PR event and base/head SHAs are required",
            )
        payload = _read_json(Path(args.event))
        body = payload.get("pull_request", {}).get("body")
        if not isinstance(body, str):
            raise G0EnforcementError("PR_BODY_REQUIRED", "pull request body is missing")
        result = evaluate_pull_request(
            root,
            pull_request_body=body,
            changed_paths=_changed_paths(args.base_sha, args.head_sha, root),
        )
        if result.state is not SLGEE0DecisionState.APPROVED:
            codes = ", ".join(code.value for code in result.failure_codes)
            raise G0EnforcementError(codes, "lifecycle declaration refused")
        print(
            "G0 declaration verified "
            f"(trace={result.trace_ref}; next={','.join(result.next_openings)})"
        )
        return 0
    except G0EnforcementError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
