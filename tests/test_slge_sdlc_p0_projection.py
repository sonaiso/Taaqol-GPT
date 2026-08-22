"""Constitutional tests for SLGE-SDLC-P0 deterministic lifecycle projection.

Origin law     :
    docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md
Branch         : SLGE-SDLC-P0
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.governance import repo_org_projection as repo_projector
from taaqqul_slot_geometry.governance import slge_sdlc_p0_projection as projector
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_GOVERNANCE = _REPO_ROOT / "governance"
_REGISTRY = _GOVERNANCE / "registry"
_SCHEMAS = _REPO_ROOT / "schemas" / "governance"
_DOCS = _REPO_ROOT / "docs"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        ),
        branch_name=f"SLGE-SDLC-P0 ({branch_note})",
        constitutional_chain=(
            "docs/124",
            "docs/127",
            "docs/128",
            "governance/registry/slge_sdlc_p0_lifecycle_events.json",
            "governance/projections/slge_sdlc_current_lifecycle_state.json",
            "src/taaqqul_slot_geometry/governance/slge_sdlc_p0_projection.py",
            "src/taaqqul_slot_geometry/governance/repo_org_projection.py",
            "governance/projections/current_state.json",
        ),
        chain_position="SLGE-SDLC-P0",
        origin_law_ref=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        ),
        branch_of_origin=(
            "Deterministic lifecycle current-state projection from bounded legacy baseline "
            "plus authorized applied lifecycle events only."
        ),
        forbidden_shortcut_assertions=(
            "TransitionDecision -> StateMutation",
            "ApprovedDecisionWithoutEvent -> CurrentStateMutation",
            "Event -> HistoricalCertification",
            "Merge -> Closure",
            "GreenCI -> Closure",
            "READMEText -> LifecycleAuthority",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "G0PREnforcementOpening",
            "C0ClosureOpening",
            "HistoricalCertificationPromotion",
            "StateMutationWithoutAppliedEvent",
        ),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_p0_registry_and_projection_schemas_validate() -> None:
    _declare("schema validation")
    registry_schema = _load_json(_SCHEMAS / "slge_sdlc_p0_lifecycle_events.schema.json")
    projection_schema = _load_json(_SCHEMAS / "slge_sdlc_current_lifecycle_state.schema.json")
    registry_payload = _load_json(_REGISTRY / "slge_sdlc_p0_lifecycle_events.json")
    projection_payload = _load_json(_GOVERNANCE / "projections" / "slge_sdlc_current_lifecycle_state.json")

    registry_errors = sorted(
        Draft202012Validator(registry_schema).iter_errors(registry_payload),
        key=lambda error: list(error.path),
    )
    projection_errors = sorted(
        Draft202012Validator(projection_schema).iter_errors(projection_payload),
        key=lambda error: list(error.path),
    )
    assert not registry_errors, [error.message for error in registry_errors]
    assert not projection_errors, [error.message for error in projection_errors]


def test_valid_legacy_baseline_and_post_cut_events_derive_expected_state() -> None:
    _declare("legacy baseline + post-cut reduction")
    payload = projector.compute_projection_payload(_REPO_ROOT)
    by_artifact = {item["artifact_id"]: item for item in payload["current_lifecycle_states"]}

    assert by_artifact["DOC-124"]["current_lifecycle_slot"] == "SLGE-SDLC-M0"
    assert by_artifact["DOC-124"]["historical_uncertainty_boundary"]["status"] == "PARTIAL"
    assert by_artifact["SLGE-SDLC-P0-PROJECTION"]["current_lifecycle_slot"] == "SLGE-SDLC-P0"
    assert by_artifact["SLGE-SDLC-P0-PROJECTION"]["last_applied_event"] == "LCE-SLGE-P0-APPLIED-001"


def test_multiple_events_reduce_deterministically_and_byte_stably() -> None:
    _declare("deterministic reduction")
    first = projector.compute_projection_payload(_REPO_ROOT)
    second = projector.compute_projection_payload(_REPO_ROOT)

    assert first == second
    assert projector.serialize_lifecycle_projection(first) == projector.serialize_lifecycle_projection(second)


def test_residual_trace_rank_and_authority_preserved() -> None:
    _declare("residual/trace/rank/authority preservation")
    payload = projector.compute_projection_payload(_REPO_ROOT)
    p0_record = next(
        item for item in payload["current_lifecycle_states"] if item["artifact_id"] == "SLGE-SDLC-P0-PROJECTION"
    )
    assert "SLGE_G0_PR_ENFORCEMENT_PENDING" in p0_record["open_residual_refs"]
    assert p0_record["rank_ceiling"] == "E1"
    assert p0_record["authority_ceiling"] == "CurrentStateProjectionAuthority"
    assert p0_record["trace_refs"]


def test_approved_decision_without_event_does_not_mutate_state() -> None:
    _declare("decision != event")
    payload = projector.compute_projection_payload(_REPO_ROOT)
    traces = {
        item["historical_uncertainty_boundary"].get("decision_ref")
        for item in payload["current_lifecycle_states"]
    }
    assert "DEC-SLGE-E0-UNAPPLIED" not in traces


def test_pre_cut_unknown_history_is_not_certified() -> None:
    _declare("legacy uncertainty preserved")
    payload = projector.compute_projection_payload(_REPO_ROOT)
    doc_125 = next(item for item in payload["current_lifecycle_states"] if item["artifact_id"] == "DOC-125")
    boundary = doc_125["historical_uncertainty_boundary"]

    assert boundary["status"] == "UNKNOWN"
    assert boundary["historical_mclt_ref"] is None


def test_semantics_refuse_synthetic_historical_mclt() -> None:
    _declare("synthetic historical mclt refusal")
    inputs = projector.load_lifecycle_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["events"]["legacy_baseline_records"][0]["historical_mclt_ref"] = "MCLT-FAKE"

    try:
        projector.validate_lifecycle_semantics(tampered)
        assert False, "expected SYNTHETIC_HISTORICAL_MCLT"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.SYNTHETIC_HISTORICAL_MCLT


def test_semantics_refuse_illegal_event_ordering() -> None:
    _declare("illegal ordering refusal")
    inputs = projector.load_lifecycle_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["events"]["applied_lifecycle_events"][1]["event_order"] = 1

    try:
        projector.validate_lifecycle_semantics(tampered)
        assert False, "expected NON_DETERMINISTIC_ORDERING"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.NON_DETERMINISTIC_ORDERING


def test_semantics_refuse_source_slot_mismatch() -> None:
    _declare("source-slot mismatch refusal")
    inputs = projector.load_lifecycle_inputs(_REPO_ROOT)
    normalized = projector.normalize_lifecycle_inputs(inputs)
    tampered = copy.deepcopy(normalized)
    replay = copy.deepcopy(tampered["events"][0])
    replay["event_id"] = "LCE-SLGE-E0-APPLIED-REPLAY"
    replay["event_order"] = 99
    replay["from_slot_ref"] = "SLGE-SDLC-M0"
    tampered["events"].append(replay)

    try:
        projector.reduce_current_lifecycle_state(tampered)
        assert False, "expected SOURCE_STATE_MISMATCH"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.SOURCE_STATE_MISMATCH


def test_semantics_refuse_forbidden_jump() -> None:
    _declare("forbidden jump refusal")
    inputs = projector.load_lifecycle_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["events"]["applied_lifecycle_events"][1]["to_slot_ref"] = "SLGE-SDLC-C0"

    try:
        projector.validate_lifecycle_semantics(tampered)
        assert False, "expected ILLEGAL_SLOT_TRANSITION"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.ILLEGAL_SLOT_TRANSITION


def test_semantics_refuse_dangling_refs_and_duplicate_event_ids() -> None:
    _declare("dangling/duplicate event refusal")
    inputs = projector.load_lifecycle_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["events"]["applied_lifecycle_events"][0]["decision_ref"] = "DEC-MISSING"

    try:
        projector.validate_lifecycle_semantics(tampered)
        assert False, "expected DANGLING_REFERENCE"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.DANGLING_REFERENCE

    duplicate = copy.deepcopy(inputs)
    duplicate["events"]["applied_lifecycle_events"].append(
        copy.deepcopy(duplicate["events"]["applied_lifecycle_events"][0])
    )
    try:
        projector.validate_lifecycle_semantics(duplicate)
        assert False, "expected DUPLICATE_EVENT_ID"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.DUPLICATE_EVENT_ID


def test_semantics_refuse_trace_loss_blocking_residual_and_rank_inflation() -> None:
    _declare("trace/residual/rank refusal")
    inputs = projector.load_lifecycle_inputs(_REPO_ROOT)

    trace_tampered = copy.deepcopy(inputs)
    trace_tampered["events"]["applied_lifecycle_events"][0]["trace_refs"] = ["trace://missing"]
    try:
        projector.validate_lifecycle_semantics(trace_tampered)
        assert False, "expected TRACE_LOSS"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.TRACE_LOSS

    residual_tampered = copy.deepcopy(inputs)
    residual_tampered["events"]["applied_lifecycle_events"][0]["open_residual_refs"] = ["BLOCKING:LEGACY"]
    try:
        projector.validate_lifecycle_semantics(residual_tampered)
        assert False, "expected BLOCKING_RESIDUAL_VIOLATION"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.BLOCKING_RESIDUAL_VIOLATION

    rank_tampered = copy.deepcopy(inputs)
    rank_tampered["events"]["applied_lifecycle_events"][0]["rank_ceiling"] = "E5"
    try:
        projector.validate_lifecycle_semantics(rank_tampered)
        assert False, "expected RANK_AUTHORITY_INFLATION"
    except projector.LifecycleProjectionError as exc:
        assert exc.code == projector.SLGEP0FailureCode.RANK_AUTHORITY_INFLATION


def test_projection_drift_check_fails_closed() -> None:
    _declare("projection drift")
    path = _GOVERNANCE / "projections" / "slge_sdlc_current_lifecycle_state.json"
    original = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(original)
        path.write_text(
            original.replace(
                f'"version": "{payload["version"]}"',
                f'"version": "{payload["version"]}-drift"',
                1,
            ),
            encoding="utf-8",
        )
        try:
            projector.check_projection_drift(_REPO_ROOT)
            assert False, "expected LIFECYCLE_PROJECTION_DRIFT"
        except projector.LifecycleProjectionError as exc:
            assert exc.code == projector.SLGEP0FailureCode.LIFECYCLE_PROJECTION_DRIFT
    finally:
        path.write_text(original, encoding="utf-8")


def test_chain_and_registry_reflect_p0_opening_only() -> None:
    _declare("chain opening boundary")
    branches = _load_json(_REGISTRY / "branches.json")["branch_statuses"]
    runtime_map = _load_json(_REGISTRY / "runtime_map.json")["runtime_map"]
    residuals = _load_json(_REGISTRY / "residuals.json")["residuals"]
    chain = (_DOCS / "14_PR_CHAIN_ROADMAP.md").read_text(encoding="utf-8")

    p0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-P0")
    g0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-G0")
    c0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-C0")
    p0_runtime = next(item for item in runtime_map if item["branch_id"] == "SLGE-SDLC-P0")
    p0_pending = next(
        item for item in residuals if item["residual_id"] == "SLGE_P0_LIFECYCLE_PROJECTION_PENDING"
    )

    assert p0["constitutional_status"] == "RATIFIED"
    assert p0["runtime_status"] == "EXECUTABLE"
    assert p0["evidence_status"] == "PROVEN"
    assert p0_runtime["runtime_status"] == "EXECUTABLE"

    assert g0["runtime_status"] == "ABSENT"
    assert c0["runtime_status"] == "ABSENT"
    assert p0_pending["disposition"] == "CLOSED"

    assert "Amendment-106 (SLGE-SDLC-P0 — Deterministic Lifecycle Current-State Projection)" in chain
    assert "Immediate successor after `SLGE-SDLC-P0` is" in chain
    assert "`SLGE-SDLC-G0` only." in chain


def test_repo_projection_semantics_include_p0_surfaces() -> None:
    _declare("repo projection coherence")
    inputs = repo_projector.load_governance_inputs(_REPO_ROOT)
    repo_projector._validate_semantics(_REPO_ROOT, inputs)
    current = _load_json(_GOVERNANCE / "projections" / "current_state.json")

    assert "governance/registry/slge_sdlc_p0_lifecycle_events.json" in current["projection_metadata"][
        "authoritative_inputs"
    ]
    assert "governance/projections/slge_sdlc_current_lifecycle_state.json" in current[
        "projection_metadata"
    ]["authoritative_inputs"]
