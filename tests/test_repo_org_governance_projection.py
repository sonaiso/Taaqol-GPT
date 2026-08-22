"""Constitutional tests for REPO-ORG-P0 governance projection runtime.

Origin law     : docs/123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md
Branch         : REPO-ORG-P0
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
        origin_law="docs/123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md",
        branch_name=f"REPO-ORG-P0 ({branch_note})",
        constitutional_chain=(
            "docs/123",
            "governance/registry",
            "src/taaqqul_slot_geometry/governance/repo_org_projection.py",
            "governance/projections/current_state.json",
        ),
        chain_position="REPO-ORG-P0",
        origin_law_ref="docs/123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md#6-registry-and-projection-contract",
        branch_of_origin=(
            "Deterministic computed current-state projection from typed governance records "
            "with fail-closed validation and drift enforcement."
        ),
        forbidden_shortcut_assertions=(
            "READMEText -> AuthorityRole",
            "HistoricalOrder -> DependencyOrder",
            "ReviewerApproval -> EpistemicTruthEvidence",
            "GreenCI -> ClosureEvidence",
            "Ratification -> EmpiricalTruth",
            "Merge -> Closure",
            "RegistryExistence -> V1ClosedClaim",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "ORMOpeningClaim",
            "V1ClosedClaim",
            "SLGESDLCOpeningClaim",
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


def _serialize(payload: dict) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def test_registry_files_validate_against_governance_schema() -> None:
    _declare("registry schema validation")
    schema = _load_json(_SCHEMAS / "registry.schema.json")
    validator = Draft202012Validator(schema)

    registry_files = (
        "artifacts.json",
        "branches.json",
        "dependencies.json",
        "runtime_map.json",
        "evidence_map.json",
        "residuals.json",
        "data_taxonomy.json",
        "schema_taxonomy.json",
        "projection_inputs.json",
    )
    for name in registry_files:
        payload = _load_json(_REGISTRY / name)
        errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
        assert not errors, f"{name} violates registry schema: {[e.message for e in errors]}"


def test_current_state_projection_validates_against_schema() -> None:
    _declare("projection schema validation")
    schema = _load_json(_SCHEMAS / "current_state.schema.json")
    validator = Draft202012Validator(schema)
    payload = _load_json(_GOVERNANCE / "projections" / "current_state.json")
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    assert not errors, [e.message for e in errors]


def test_projection_is_deterministically_recomputed_and_byte_stable() -> None:
    _declare("deterministic recomputation")
    computed = projector.compute_projection_payload(_REPO_ROOT)
    checked_in = (_GOVERNANCE / "projections" / "current_state.json").read_bytes()

    assert _serialize(computed) == checked_in
    assert projector.compute_projection_payload(_REPO_ROOT) == computed


def test_projection_drift_detection_fails_closed() -> None:
    _declare("drift detection")
    original = (_GOVERNANCE / "projections" / "current_state.json").read_text(encoding="utf-8")
    try:
        payload = json.loads(original)
        current_version = payload["version"]
        (_GOVERNANCE / "projections" / "current_state.json").write_text(
            original.replace(
                f'"version": "{current_version}"',
                f'"version": "{current_version}-drift"',
                1,
            ),
            encoding="utf-8",
        )
        try:
            projector.check_projection_drift(_REPO_ROOT)
            assert False, "expected PROJECTION_DRIFT"
        except projector.ProjectionError as exc:
            assert exc.code == "PROJECTION_DRIFT"
    finally:
        (_GOVERNANCE / "projections" / "current_state.json").write_text(original, encoding="utf-8")


def test_projection_and_evidence_requirements_keep_v1_44_refused_visible() -> None:
    _declare("v1 closure visibility")
    projection = _load_json(_GOVERNANCE / "projections" / "current_state.json")
    requirements = _load_json(_REGISTRY / "evidence_map.json")["evidence_requirements"]
    v1_ledger = (_DOCS / "116_V1_CLOSURE_EVIDENCE_LEDGER.md").read_text(encoding="utf-8")

    v1_44 = next(item for item in requirements if item["artifact_id"] == "V1-44")
    assert v1_44["evidence_kind"] == "ClosureEvidence"
    assert v1_44["verdict"] == "REFUSED"
    assert projection["highlights"]["v1_closure"]["objective_v1_44"] == "REFUSED"
    assert "| V1-44 | REFUSED |" in v1_ledger


def test_declared_projection_residual_is_closed_and_not_active() -> None:
    _declare("projection residual closure")
    projection = _load_json(_GOVERNANCE / "projections" / "current_state.json")
    residuals = _load_json(_REGISTRY / "residuals.json")["residuals"]

    declared = next(
        item
        for item in residuals
        if item["residual_id"] == "DECLARED_PROJECTION_NOT_YET_COMPUTED"
    )
    assert declared["owner_artifact"] == "REPO-ORG-P0"
    assert declared["disposition"] == "CLOSED"
    assert "DECLARED_PROJECTION_NOT_YET_COMPUTED" not in projection["technical_residuals"]


def test_readme_and_docs_index_are_declared_as_derived_views_only() -> None:
    _declare("derived-view drift guard")
    readme = (_REPO_ROOT / "README.md").read_text(encoding="utf-8")
    docs_index = (_DOCS / "README.md").read_text(encoding="utf-8")
    artifacts = _load_json(_REGISTRY / "artifacts.json")["artifacts"]

    readme_artifact = next(item for item in artifacts if item["artifact_id"] == "README")
    assert readme_artifact["authority_roles"] == ["ProjectionAuthority"]

    assert "governance/projections/current_state.json" in readme
    assert "Implemented runtime surfaces are not equivalent to closure evidence" in readme
    assert "shipped and constitutionally closed" not in readme

    assert "## 4) Governance, proposals, and refoundation records" in docs_index
    assert "123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md" in docs_index
    assert (
        "124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        in docs_index
    )
    assert "governance/registry/*.json" in docs_index


def test_projector_inputs_exclude_readme_text_as_authority_surface() -> None:
    _declare("narrative non-authority")
    projection = projector.compute_projection_payload(_REPO_ROOT)
    source_fingerprints = projection["projection_metadata"]["source_fingerprints"]

    assert "README.md" not in projection["projection_metadata"]["authoritative_inputs"]
    assert all(not path.endswith("README.md") for path in source_fingerprints)


def test_semantic_validation_refuses_duplicate_artifact_ids() -> None:
    _declare("duplicate artifact id refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["artifacts"].append(copy.deepcopy(tampered["artifacts"][0]))

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected DUPLICATE_ARTIFACT_ID"
    except projector.ProjectionError as exc:
        assert exc.code == "DUPLICATE_ARTIFACT_ID"


def test_semantic_validation_refuses_dangling_dependency_refs() -> None:
    _declare("dangling dependency refusal")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    tampered = copy.deepcopy(inputs)
    tampered["artifacts"][0]["dependency_refs"] = ["DEP-DOES-NOT-EXIST"]

    try:
        projector._validate_semantics(_REPO_ROOT, tampered)
        assert False, "expected DANGLING_DEPENDENCY_REF"
    except projector.ProjectionError as exc:
        assert exc.code == "DANGLING_DEPENDENCY_REF"


def test_runtime_map_and_branch_status_for_repo_org_p0_are_coherent() -> None:
    _declare("runtime posture coherence")
    projection = _load_json(_GOVERNANCE / "projections" / "current_state.json")
    branch_statuses = _load_json(_REGISTRY / "branches.json")["branch_statuses"]
    runtime_map = _load_json(_REGISTRY / "runtime_map.json")["runtime_map"]

    assert projection["highlights"]["observatory_program"]["scope"] == "POST_V1_RESEARCH"
    assert projection["highlights"]["observatory_program"]["does_not_imply"] == "V1_CLOSED"

    repo_org_p0 = next(item for item in branch_statuses if item["branch_id"] == "REPO-ORG-P0")
    assert repo_org_p0["runtime_status"] == "EXECUTABLE"

    p0_runtime = next(item for item in runtime_map if item["branch_id"] == "REPO-ORG-P0")
    assert p0_runtime["runtime_status"] == "EXECUTABLE"


def test_chain_announces_repo_org_r0_then_p0_then_slge_sdlc_l0() -> None:
    _declare("chain successor ordering")
    chain = (_DOCS / "14_PR_CHAIN_ROADMAP.md").read_text(encoding="utf-8")
    branch_statuses = _load_json(_REGISTRY / "branches.json")["branch_statuses"]
    runtime_map = _load_json(_REGISTRY / "runtime_map.json")["runtime_map"]

    assert "Amendment-100 (REPO-ORG-R0 — Registry Semantic Hardening)" in chain
    assert "Amendment-101 (REPO-ORG-P0 — Derived Projection Engine & Drift Enforcement)" in chain
    assert "Amendment-102 (SLGE-SDLC-L0 — Project Lifecycle Constitution)" in chain
    assert "Amendment-103 (SLGE-SDLC-R0 — Lifecycle Registry and Machine Contracts)" in chain
    assert "Immediate successor after `REPO-ORG-R0` is `REPO-ORG-P0` only." in chain
    assert "Immediate successor after `REPO-ORG-P0` is `SLGE-SDLC-L0`." in chain
    assert "Immediate successor after `SLGE-SDLC-L0` is" in chain
    assert "`SLGE-SDLC-R0` only." in chain
    assert "Immediate successor after `SLGE-SDLC-R0` is" in chain
    assert "`SLGE-SDLC-M0` only." in chain

    slge_l0 = next(item for item in branch_statuses if item["branch_id"] == "SLGE-SDLC-L0")
    assert slge_l0["runtime_status"] == "ABSENT"
    assert slge_l0["constitutional_status"] == "RATIFIED"

    slge_r0_runtime = next(item for item in runtime_map if item["branch_id"] == "SLGE-SDLC-R0")
    assert slge_r0_runtime["runtime_status"] == "ABSENT"
