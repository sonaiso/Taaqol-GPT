"""Constitutional tests for REPO-ORG-R0 governance projection surfaces.

Origin law     : docs/123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md
Branch         : REPO-ORG-R0
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from taaqqul_slot_geometry import ClosureState, Rank
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
        branch_name=f"REPO-ORG-R0 ({branch_note})",
        constitutional_chain=("docs/123", "governance/registry", "governance/projections"),
        chain_position="REPO-ORG-R0",
        origin_law_ref="docs/123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md#12-successor-sequencing-boundary",
        branch_of_origin=(
            "Repository authority-role separation and typed governance registry hardening "
            "without projector runtime opening."
        ),
        forbidden_shortcut_assertions=(
            "READMEText -> AuthorityRole",
            "HistoricalOrder -> DependencyOrder",
            "ReviewerApproval -> EpistemicTruthEvidence",
            "GreenCI -> ClosureEvidence",
            "Ratification -> EmpiricalTruth",
            "Registry -> V1ClosedClaim",
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


def test_artifact_refs_and_taxonomy_targets_exist() -> None:
    _declare("artifact and taxonomy reference integrity")
    artifacts = _load_json(_REGISTRY / "artifacts.json")["artifacts"]
    data_taxonomy = _load_json(_REGISTRY / "data_taxonomy.json")["taxonomy"]
    schema_taxonomy = _load_json(_REGISTRY / "schema_taxonomy.json")["taxonomy"]

    for artifact in artifacts:
        for ref in artifact["runtime_refs"]:
            assert (_REPO_ROOT / ref).exists(), ref
        for ref in artifact["evidence_refs"]:
            assert (_REPO_ROOT / ref).exists(), ref
        for ref in artifact["trace_refs"]:
            assert (_REPO_ROOT / ref).exists(), ref

    for entries in data_taxonomy.values():
        for rel_path in entries:
            assert (_REPO_ROOT / rel_path).exists(), rel_path

    for entries in schema_taxonomy.values():
        for rel_path in entries:
            assert (_REPO_ROOT / rel_path).exists(), rel_path


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


def test_historical_order_is_not_dependency_order() -> None:
    _declare("historical/dependency separation")
    edges = _load_json(_REGISTRY / "dependencies.json")["dependency_edges"]
    historical_edge = next(
        edge for edge in edges if edge["relation_kind"] == "HISTORICALLY_FOLLOWS"
    )

    assert historical_edge["required"] is False
    assert historical_edge["source_artifact"].startswith("Amendment-")
    assert historical_edge["target_artifact"].startswith("Amendment-")

    semantic_relations = {
        "REQUIRES",
        "DERIVES_FROM",
        "IMPLEMENTS",
        "EVIDENCES",
        "OPENS",
        "REFINES",
        "SUPERSEDES",
        "BLOCKS",
    }
    assert historical_edge["relation_kind"] not in semantic_relations


def test_artifact_can_hold_multiple_authority_roles() -> None:
    _declare("multi-role authority")
    artifacts = _load_json(_REGISTRY / "artifacts.json")["artifacts"]
    branch_statuses = _load_json(_REGISTRY / "branches.json")["branch_statuses"]

    doc123 = next(item for item in artifacts if item["artifact_id"] == "DOC-123")
    assert sorted(doc123["authority_roles"]) == ["LawAuthority", "ProjectionAuthority"]

    repo_org_l0 = next(item for item in branch_statuses if item["branch_id"] == "REPO-ORG-L0")
    assert len(repo_org_l0["authority_roles"]) >= 2


def test_typed_evidence_requirements_are_mandatory() -> None:
    _declare("typed evidence requirements")
    requirements = _load_json(_REGISTRY / "evidence_map.json")["evidence_requirements"]

    allowed_kinds = {
        "ConstitutionalRatificationEvidence",
        "RuntimeVerificationEvidence",
        "ClosureEvidence",
        "EpistemicClaimEvidence",
        "GovernanceEvidence",
    }
    assert requirements
    for requirement in requirements:
        assert requirement["evidence_kind"] in allowed_kinds
        assert requirement["target_claim_or_transition"]
        assert requirement["minimum_requirement"]
        assert requirement["observed_refs"]


def test_residuals_require_owner_and_trace() -> None:
    _declare("residual ownership and trace discipline")
    residuals = _load_json(_REGISTRY / "residuals.json")["residuals"]

    assert residuals
    for residual in residuals:
        assert residual["owner_artifact"]
        assert residual["trace_ref"]


def test_projection_residual_declared_not_computed_is_visible_and_owned_by_p0() -> None:
    _declare("projection compatibility residual")
    projection = _load_json(_GOVERNANCE / "projections" / "current_state.json")
    residuals = _load_json(_REGISTRY / "residuals.json")["residuals"]

    declared = next(
        item
        for item in residuals
        if item["residual_id"] == "DECLARED_PROJECTION_NOT_YET_COMPUTED"
    )
    assert declared["owner_artifact"] == "REPO-ORG-P0"
    assert declared["visibility"] == "VISIBLE"
    assert declared["disposition"] == "OPEN"
    assert "DECLARED_PROJECTION_NOT_YET_COMPUTED" in projection["technical_residuals"]


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
    assert "governance/registry/*.json" in docs_index


def test_ci_and_reviewer_approval_are_not_closure_or_epistemic_truth_evidence() -> None:
    _declare("evidence non-equivalence guards")
    requirements = _load_json(_REGISTRY / "evidence_map.json")["evidence_requirements"]

    closure_requirements = [
        item for item in requirements if item["evidence_kind"] == "ClosureEvidence"
    ]
    epistemic_requirements = [
        item for item in requirements if item["evidence_kind"] == "EpistemicClaimEvidence"
    ]

    assert closure_requirements
    assert all("ci" not in " ".join(item["observed_refs"]).lower() for item in closure_requirements)
    assert all("review" not in item["minimum_requirement"].lower() for item in closure_requirements)

    assert epistemic_requirements
    assert all(item["verdict"] != "PROVEN" for item in epistemic_requirements)


def test_registry_does_not_grant_v1_closed_or_obs_runtime_opening() -> None:
    _declare("status separation and boundary non-opening")
    projection = _load_json(_GOVERNANCE / "projections" / "current_state.json")
    branch_statuses = _load_json(_REGISTRY / "branches.json")["branch_statuses"]
    runtime_map = _load_json(_REGISTRY / "runtime_map.json")["runtime_map"]

    assert projection["highlights"]["v1_closure"]["objective_v1_44"] == "REFUSED"
    assert projection["highlights"]["observatory_program"]["scope"] == "POST_V1_RESEARCH"
    assert projection["highlights"]["observatory_program"]["does_not_imply"] == "V1_CLOSED"

    repo_org_r0 = next(item for item in branch_statuses if item["branch_id"] == "REPO-ORG-R0")
    assert repo_org_r0["runtime_status"] == "ABSENT"

    obs_h0_runtime = next(item for item in runtime_map if item["branch_id"] == "OBS-H0")
    assert obs_h0_runtime["runtime_status"] == "ABSENT"


def test_chain_announces_repo_org_r0_then_p0_only() -> None:
    _declare("chain successor ordering")
    chain = (_DOCS / "14_PR_CHAIN_ROADMAP.md").read_text(encoding="utf-8")

    assert "Amendment-100 (REPO-ORG-R0 — Registry Semantic Hardening)" in chain
    assert "Immediate successor after `REPO-ORG-R0` is `REPO-ORG-P0` only." in chain
    assert "SLGE-SDLC-L0" in chain
