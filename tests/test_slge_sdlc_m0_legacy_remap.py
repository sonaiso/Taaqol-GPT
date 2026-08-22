"""Constitutional tests for SLGE-SDLC-M0 legacy remap staging.

Origin law     :
    docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md
Branch         : SLGE-SDLC-M0
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.governance import repo_org_projection as projector
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
        branch_name=f"SLGE-SDLC-M0 ({branch_note})",
        constitutional_chain=(
            "docs/124",
            "docs/126",
            "schemas/governance/slge_sdlc_m0_legacy_remap.schema.json",
            "governance/registry/slge_sdlc_m0_legacy_remap.json",
            "src/taaqqul_slot_geometry/governance/repo_org_projection.py",
            "governance/projections/current_state.json",
        ),
        chain_position="SLGE-SDLC-M0",
        origin_law_ref=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        ),
        branch_of_origin=(
            "Legacy repository remap with explicit historical-proof boundary, "
            "coverage completeness, and no synthetic historical MCLT issuance."
        ),
        forbidden_shortcut_assertions=(
            "LegacyExistence -> HistoricallyLicensedTransition",
            "CurrentArtifactPresence -> HistoricalMCLT",
            "RemapDecision -> TransitionApproval",
            "KEEP -> HistoricalClosure",
            "RETYPE -> RuntimeAdmission",
            "REORDER -> HistoryRewrite",
            "QUARANTINE -> Deletion",
            "REBUILD -> RebuiltArtifact",
            "RemapEvidence -> EpistemicTruth",
            "ContractFixture -> GovernanceAuthority",
            "SameRankLabel -> SameRankMeaning",
            "SupportingAuthority -> ExecutingAuthority",
            "SchemaValidity -> LifecycleApproval",
            "Merge -> Closure",
            "GreenCI -> Closure",
            "ReviewerApproval -> EpistemicTruth",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "LifecycleRuntimeExecution",
            "TransitionApproval",
            "HistoricalCertificateFabrication",
            "ClosureClaim",
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


def test_slge_m0_registry_validates_against_schema() -> None:
    _declare("schema surface validation")
    schema = _load_json(_SCHEMAS / "slge_sdlc_m0_legacy_remap.schema.json")
    payload = _load_json(_REGISTRY / "slge_sdlc_m0_legacy_remap.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda e: list(e.path))
    assert not errors, [e.message for e in errors]


def test_slge_m0_semantic_contract_integrity_passes() -> None:
    _declare("semantic contract integrity")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    projector._validate_semantics(_REPO_ROOT, inputs)


def test_coverage_ledger_is_deterministic_and_complete() -> None:
    _declare("coverage law")
    payload = _load_json(_REGISTRY / "slge_sdlc_m0_legacy_remap.json")

    eligible = set(payload["eligible_artifact_ids"])
    coverage = payload["coverage_ledger"]

    covered = {entry["artifact_id"] for entry in coverage}
    assert covered == eligible

    statuses = {entry["coverage_status"] for entry in coverage}
    assert statuses.issubset(
        {
            "COVERED_KEEP",
            "COVERED_RETYPE",
            "COVERED_REORDER",
            "COVERED_QUARANTINE",
            "COVERED_REBUILD",
            "OUT_OF_SCOPE_WITH_REASON",
        }
    )


def test_fixture_is_not_authoritative_and_not_used_as_remap_authority() -> None:
    _declare("fixture-authority separation")
    payload = _load_json(_REGISTRY / "slge_sdlc_m0_legacy_remap.json")

    fixture_ids = {fixture["fixture_id"] for fixture in payload["contract_fixtures"]}
    assert all(not fixture["is_authoritative"] for fixture in payload["contract_fixtures"])

    coverage_ids = {
        entry.get("remap_record_id")
        for entry in payload["coverage_ledger"]
        if entry["coverage_status"].startswith("COVERED_")
    }
    assert fixture_ids.isdisjoint(coverage_ids)


def test_unproven_historical_status_never_carries_synthetic_mclt() -> None:
    _declare("historical-proof boundary")
    payload = _load_json(_REGISTRY / "slge_sdlc_m0_legacy_remap.json")

    for record in payload["authoritative_legacy_remap_records"]:
        status = record["historical_transition_status"]
        if status == "PROVEN":
            continue
        assert record["historical_mclt_ref"] is None
        assert "HISTORICAL_MCLT_NOT_PROVEN" in set(record["unresolved_residual_refs"])


def test_branch_and_residual_state_reflect_m0_completion_without_e0_runtime() -> None:
    _declare("chain state boundary")
    branches = _load_json(_REGISTRY / "branches.json")["branch_statuses"]
    residuals = _load_json(_REGISTRY / "residuals.json")["residuals"]
    chain = (_DOCS / "14_PR_CHAIN_ROADMAP.md").read_text(encoding="utf-8")

    m0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-M0")
    e0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-E0")
    m0_pending = next(
        item for item in residuals if item["residual_id"] == "SLGE_M0_LEGACY_REMAP_PENDING"
    )

    assert m0["constitutional_status"] == "RATIFIED"
    assert m0["runtime_status"] == "ABSENT"
    assert m0["evidence_status"] == "PROVEN"

    assert e0["constitutional_status"] == "RATIFIED"
    assert e0["runtime_status"] == "EXECUTABLE"
    assert e0["evidence_status"] == "PROVEN"

    assert m0_pending["disposition"] == "CLOSED"
    assert "Amendment-104 (SLGE-SDLC-M0 — Legacy Repository Lifecycle Remap)" in chain
    assert "Immediate successor after `SLGE-SDLC-M0` is" in chain
    assert "`SLGE-SDLC-E0` only." in chain


def test_semantic_validation_refuses_synthetic_historical_mclt() -> None:
    _declare("synthetic historical mclt refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)

    tampered["slge_m0_remap"]["authoritative_legacy_remap_records"][0][
        "historical_mclt_ref"
    ] = "MCLT-SYNTHETIC"

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected SYNTHETIC_HISTORICAL_MCLT_FORBIDDEN"
    except projector.ProjectionError as exc:
        assert exc.code == "SYNTHETIC_HISTORICAL_MCLT_FORBIDDEN"


def test_semantic_validation_refuses_duplicate_coverage() -> None:
    _declare("duplicate coverage refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["slge_m0_remap"]["coverage_ledger"].append(
        copy.deepcopy(tampered["slge_m0_remap"]["coverage_ledger"][0])
    )

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected DUPLICATE_ARTIFACT_COVERAGE"
    except projector.ProjectionError as exc:
        assert exc.code == "DUPLICATE_ARTIFACT_COVERAGE"


def test_semantic_validation_refuses_missing_remap_evidence() -> None:
    _declare("missing remap evidence refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["slge_m0_remap"]["authoritative_legacy_remap_records"][0][
        "decision_evidence_refs"
    ] = []

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected MISSING_REMAP_EVIDENCE"
    except projector.ProjectionError as exc:
        assert exc.code == "MISSING_REMAP_EVIDENCE"


def test_semantic_validation_refuses_fixture_used_as_authority() -> None:
    _declare("fixture misuse refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    fixture_id = tampered["slge_m0_remap"]["contract_fixtures"][0]["fixture_id"]
    tampered["slge_m0_remap"]["coverage_ledger"][0]["remap_record_id"] = fixture_id

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected FIXTURE_USED_AS_AUTHORITY"
    except projector.ProjectionError as exc:
        assert exc.code == "FIXTURE_USED_AS_AUTHORITY"


def test_semantic_validation_refuses_authority_inflation() -> None:
    _declare("authority inflation refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["slge_m0_remap"]["authoritative_legacy_remap_records"][0]["authority_roles"][
        "executing_surfaces"
    ] = ["docs/14_PR_CHAIN_ROADMAP.md"]

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected AUTHORITY_INFLATION"
    except projector.ProjectionError as exc:
        assert exc.code == "AUTHORITY_INFLATION"


def test_semantic_validation_refuses_unlicensed_rank_mapping() -> None:
    _declare("rank mapping refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["slge_m0_remap"]["authoritative_legacy_remap_records"][0]["epistemic_rank_mapping"][
        "core_rank_mapping_status"
    ] = "MAPPED"

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected RANK_MAPPING_UNLICENSED"
    except projector.ProjectionError as exc:
        assert exc.code == "RANK_MAPPING_UNLICENSED"
