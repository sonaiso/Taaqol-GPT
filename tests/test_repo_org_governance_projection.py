"""Constitutional tests for REPO-ORG-L0 governance projection surfaces.

Origin law     : docs/123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md
Branch         : REPO-ORG-L0
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
        branch_name=f"REPO-ORG-L0 ({branch_note})",
        constitutional_chain=("docs/123", "governance/registry", "governance/projections"),
        chain_position="REPO-ORG-L0",
        origin_law_ref="docs/123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md#6-registry-and-projection-contract",
        branch_of_origin=(
            "Repository authority separation and machine-readable current-state projection "
            "without runtime opening or chain displacement."
        ),
        forbidden_shortcut_assertions=(
            "READMEText -> CurrentStateAuthority",
            "HistoricalOrder -> DependencyOrder",
            "ImplementedSurface -> V1Closed",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "V1ClosedClaim",
            "HiddenResidualClaim",
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


def test_registry_paths_and_taxonomy_targets_exist() -> None:
    _declare("artifact and taxonomy path integrity")
    artifacts = _load_json(_REGISTRY / "artifacts.json")["artifacts"]
    data_taxonomy = _load_json(_REGISTRY / "data_taxonomy.json")["taxonomy"]
    schema_taxonomy = _load_json(_REGISTRY / "schema_taxonomy.json")["taxonomy"]

    for artifact in artifacts:
        assert (_REPO_ROOT / artifact["path"]).exists(), artifact["path"]

    for entries in data_taxonomy.values():
        for rel_path in entries:
            assert (_REPO_ROOT / rel_path).exists(), rel_path

    for entries in schema_taxonomy.values():
        for rel_path in entries:
            assert (_REPO_ROOT / rel_path).exists(), rel_path


def test_projection_and_evidence_maps_keep_v1_44_refused_visible() -> None:
    _declare("v1 closure visibility")
    projection = _load_json(_GOVERNANCE / "projections" / "current_state.json")
    evidence_map = _load_json(_REGISTRY / "evidence_map.json")["evidence_map"]
    v1_ledger = (_DOCS / "116_V1_CLOSURE_EVIDENCE_LEDGER.md").read_text(encoding="utf-8")

    v1_44 = next(item for item in evidence_map if item["artifact_id"] == "V1-44")
    assert v1_44["evidence_status"] == "REFUSED"
    assert projection["highlights"]["v1_closure"]["objective_v1_44"] == "REFUSED"
    assert "| V1-44 | REFUSED |" in v1_ledger


def test_historical_order_is_not_dependency_order() -> None:
    _declare("historical/dependency separation")
    amendments = []
    history_lines = (
        (_GOVERNANCE / "history" / "amendments.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    for line in history_lines:
        line = line.strip()
        if line:
            amendments.append(json.loads(line))

    a97 = next(item for item in amendments if item["id"] == "Amendment-97")
    a98 = next(item for item in amendments if item["id"] == "Amendment-98")

    assert a97["historical_order"] < a98["historical_order"]
    assert a97["dependency_order"] > a98["dependency_order"]


def test_readme_and_docs_index_are_declared_as_derived_views() -> None:
    _declare("derived-view drift guard")
    readme = (_REPO_ROOT / "README.md").read_text(encoding="utf-8")
    docs_index = (_DOCS / "README.md").read_text(encoding="utf-8")

    assert "governance/projections/current_state.json" in readme
    assert "Implemented runtime surfaces are not equivalent to closure evidence" in readme
    assert "shipped and constitutionally closed" not in readme

    assert "## 4) Governance, proposals, and refoundation records" in docs_index
    assert "123_REPOSITORY_STATE_AUTHORITY_AND_TOPOLOGY_LAW.md" in docs_index
    assert "governance/registry/*.json" in docs_index


def test_observatory_scope_is_post_v1_research_only() -> None:
    _declare("observatory/v1 separation")
    projection = _load_json(_GOVERNANCE / "projections" / "current_state.json")
    observatory = projection["highlights"]["observatory_program"]

    assert observatory["scope"] == "POST_V1_RESEARCH"
    assert observatory["does_not_imply"] == "V1_CLOSED"
    assert observatory["authority_impact"] == "NONE_ON_V1_CLOSURE"
