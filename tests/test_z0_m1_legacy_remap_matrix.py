"""Acceptance tests for Z0-M1 legacy remap machine-readable registry.

Origin law     : docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md
Branch         : Z0-M1 (compatibility matrix publication)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_112 = _REPO_ROOT / "docs" / "112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md"
_SCHEMA_PATH = _REPO_ROOT / "schemas" / "z0_legacy_remap.schema.json"
_DATA_PATH = _REPO_ROOT / "data" / "z0_legacy_remap.json"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=f"Z0-M1 machine-readable remap ({branch_note})",
        constitutional_chain=("docs/112", "Z0-M1"),
        chain_position="Z0-M1 compatibility matrix publication",
        origin_law_ref="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_of_origin=(
            "Machine-readable remap ledger over in-scope legacy artifacts "
            "with single-state mapping and explicit backward/forward proofs."
        ),
        forbidden_shortcut_assertions=(
            "LegacyRuntimeClosed -> Z0RuntimeLicensed",
            "MissingRemapState -> Z0Compatible",
            "RelationClosure -> IfadahWithoutPCC",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeMutationClaim",
            "RealityClosureClaim",
            "SilentLegacyContinuation",
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


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_z0_m1_files_exist_and_reference_law_112() -> None:
    _declare("presence and law authority")
    assert _DOC_112.exists()
    assert _SCHEMA_PATH.exists()
    assert _DATA_PATH.exists()

    schema = _load_json(_SCHEMA_PATH)
    payload = _load_json(_DATA_PATH)

    assert payload["law_ref"] == "docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md"
    assert schema["properties"]["law_ref"]["const"] == payload["law_ref"]


def test_z0_m1_schema_and_payload_state_inventory_match() -> None:
    _declare("state vocabulary")
    schema = _load_json(_SCHEMA_PATH)
    payload = _load_json(_DATA_PATH)

    schema_states = set(
        schema["$defs"]["LegacyRemapRecord"]["properties"]["remap_state"]["enum"]
    )
    payload_states = set(payload["remap_states"])
    assert payload_states == schema_states

    records = payload["records"]
    used_states = {record["remap_state"] for record in records}
    assert used_states == schema_states


def test_z0_m1_every_record_obeys_required_contract_fields() -> None:
    _declare("record contract completeness")
    schema = _load_json(_SCHEMA_PATH)
    payload = _load_json(_DATA_PATH)
    required_fields = schema["$defs"]["LegacyRemapRecord"]["required"]
    allowed_states = set(
        schema["$defs"]["LegacyRemapRecord"]["properties"]["remap_state"]["enum"]
    )

    records = payload["records"]
    assert records
    for record in records:
        assert set(record.keys()) == set(required_fields)
        assert record["artifact_id"]
        assert record["trace_ref"]
        assert record["source_law"].startswith("docs/")
        assert record["source_module"].startswith(("src/", "docs/"))
        assert record["remap_state"] in allowed_states
        assert isinstance(record["legacy_predecessors"], list)
        assert isinstance(record["legacy_successors"], list)
        assert isinstance(record["residuals"], list)
        assert all(isinstance(item, str) and item for item in record["residuals"])


def test_z0_m1_artifact_ids_are_unique_and_single_state_mapped() -> None:
    _declare("single-state mapping")
    payload = _load_json(_DATA_PATH)
    records = payload["records"]
    artifact_ids = [record["artifact_id"] for record in records]
    assert len(artifact_ids) == len(set(artifact_ids))

    state_by_artifact = {record["artifact_id"]: record["remap_state"] for record in records}
    assert len(state_by_artifact) == len(records)


def test_z0_m1_explicitly_covers_z0_forbidden_legacy_shortcuts() -> None:
    _declare("forbidden legacy shortcut coverage")
    payload = _load_json(_DATA_PATH)
    records = payload["records"]

    by_id = {record["artifact_id"]: record for record in records}
    assert by_id["VERBAL_MADLUL_CANDIDATE"]["remap_state"] in {"RETYPE", "QUARANTINE"}
    assert by_id["DAL_MADLUL_BINDING_CANDIDATE"]["remap_state"] == "QUARANTINE"
    assert by_id["RELATION_CLOSURE"]["remap_state"] == "RETYPE"
    assert by_id["NATIVE_RUNTIME_REGISTRY_LEGACY_FORWARD_PATH"]["remap_state"] == "QUARANTINE"

