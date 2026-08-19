"""Acceptance tests for Z0-M3 legacy-path quarantine registry.

Origin law     : docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md
Branch         : Z0-M3 (legacy-path quarantine registry)
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

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_112 = _REPO_ROOT / "docs" / "112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_SCHEMA_PATH = _REPO_ROOT / "schemas" / "z0_legacy_path_quarantine.schema.json"
_DATA_PATH = _REPO_ROOT / "data" / "z0_legacy_path_quarantine.json"
_REMAP_PATH = _REPO_ROOT / "data" / "z0_legacy_remap.json"
_EXPECTED_SHORTCUTS = {
    "S1_DAL_ONLY_TO_VERBAL_MADLUL": "DalOnly -> VerbalMadlul",
    "S2_BINDING_TO_RELATION_AS_SOLE_PATH": (
        "DalMadlulBinding -> ContractableUnit -> Relation as sole composition path"
    ),
    "S3_RELATION_CLOSURE_TO_IFADAH_WITHOUT_PCC": (
        "RelationClosure -> Ifadah without PreIfadahConceptualClosure"
    ),
}


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=f"Z0-M3 quarantine registry ({branch_note})",
        constitutional_chain=("docs/112", "Z0-M1", "Z0-M1.1", "Z0-M2", "Z0-M3"),
        chain_position="Z0-M3 bounded legacy-path quarantine registry publication",
        origin_law_ref="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_of_origin=(
            "Machine-readable quarantine registry over legacy forward shortcuts "
            "forbidden by Z0 §6, preserving backward trace and visible residuals."
        ),
        forbidden_shortcut_assertions=(
            "DalOnly -> VerbalMadlul",
            "DalMadlulBinding -> ContractableUnit -> Relation (sole path)",
            "RelationClosure -> Ifadah (without PCC)",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeMutationClaim",
            "CertificateIssuanceClaim",
            "TruthRealityClosureClaim",
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


def test_z0_m3_files_exist_and_law_refs_are_bound() -> None:
    _declare("presence and law binding")
    assert _DOC_112.exists()
    assert _DOC_14.exists()
    assert _SCHEMA_PATH.exists()
    assert _DATA_PATH.exists()
    assert _REMAP_PATH.exists()

    payload = _load_json(_DATA_PATH)
    schema = _load_json(_SCHEMA_PATH)

    assert payload["law_ref"] == "docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md"
    assert schema["properties"]["law_ref"]["const"] == payload["law_ref"]
    assert payload["source_remap_ledger_ref"] == "data/z0_legacy_remap.json"


def test_payload_validates_against_schema() -> None:
    _declare("schema validation")
    schema = _load_json(_SCHEMA_PATH)
    payload = _load_json(_DATA_PATH)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(payload)


def test_registry_covers_exactly_the_three_z0_prohibitions() -> None:
    _declare("prohibition coverage")
    payload = _load_json(_DATA_PATH)

    by_id = {entry["shortcut_id"]: entry for entry in payload["entries"]}
    assert set(by_id) == set(_EXPECTED_SHORTCUTS)

    for shortcut_id, forbidden_text in _EXPECTED_SHORTCUTS.items():
        assert by_id[shortcut_id]["forbidden_shortcut"] == forbidden_text


def test_entries_reference_known_remap_artifacts_and_preserve_quarantine_boundary() -> None:
    _declare("artifact reference and boundary coherence")
    payload = _load_json(_DATA_PATH)
    remap = _load_json(_REMAP_PATH)

    by_artifact = {record["artifact_id"]: record for record in remap["records"]}

    for entry in payload["entries"]:
        assert entry["enforcement"] == "FORWARD_LICENSE_FORBIDDEN"
        assert entry["residuals"]

        has_quarantine_source = False
        for artifact_id in entry["legacy_artifact_ids"]:
            assert artifact_id in by_artifact
            record = by_artifact[artifact_id]
            assert record["remap_state"] in {"RETYPE", "QUARANTINE"}
            if record["remap_state"] == "QUARANTINE":
                has_quarantine_source = True
                assert record["target_z0_stage"] == payload["quarantine_stage"]
        assert has_quarantine_source


def test_baseline_and_traceability_align_with_z0_m1_ledger() -> None:
    _declare("baseline and trace alignment")
    payload = _load_json(_DATA_PATH)
    remap = _load_json(_REMAP_PATH)

    assert payload["legacy_baseline_sha"] == remap["legacy_baseline_sha"]
    assert payload["prohibition_ref"] == (
        "docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md#6-immediate-z0-prohibitions"
    )


def test_docs14_marks_z0_m2_done_and_z0_m3_current_not_complete() -> None:
    _declare("roadmap status transition")
    roadmap = _DOC_14.read_text(encoding="utf-8")

    assert "Amendment-88 (Z0-M3 — Legacy-Path Quarantine Registry)" in roadmap
    assert "Z0-M2 is now marked done as bounded hardening baseline." in roadmap
    assert "Z0-M3 is current (not complete)" in roadmap
