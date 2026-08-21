"""Acceptance tests for Z0-M1 legacy remap machine-readable registry.

Origin law     : docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md
Branch         : Z0-M1.1 (corrective hardening)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
import re
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
_SCHEMA_PATH = _REPO_ROOT / "schemas" / "z0_legacy_remap.schema.json"
_DATA_PATH = _REPO_ROOT / "data" / "z0_legacy_remap.json"
_SCOPE_PATH = _REPO_ROOT / "data" / "z0_legacy_scope.json"
_EXPECTED_STAGE_REGISTRY = [
    "REALITY_OPEN",
    "TRACE_AND_PRIOR_KNOWLEDGE",
    "UNIT",
    "IDENTITY",
    "MCE",
    "DAL_GEOMETRY",
    "EXHAUSTED_WORD_FORM_GEOMETRY",
    "SEMANTIC_BRANCH",
    "FORMAL_COMPOSITION_BRANCH",
    "PRE_IFADAH_CONCEPTUAL_CLOSURE",
    "IFADAH",
    "MANTUQ",
    "MAFHUM",
    "HUKM",
    "REALITY_CLOSE",
    "LEGACY_HISTORICAL_ONLY",
]


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=f"Z0-M1.1 machine-readable remap ({branch_note})",
        constitutional_chain=("docs/112", "Z0-M1", "Z0-M1.1"),
        chain_position="Z0-M1.1 corrective hardening",
        origin_law_ref="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_of_origin=(
            "Machine-readable remap ledger over in-scope legacy artifacts "
            "with single-state mapping, explicit proof status, and exhaustive scope."
        ),
        forbidden_shortcut_assertions=(
            "LegacyRuntimeClosed -> Z0RuntimeLicensed",
            "MissingRemapState -> Z0Compatible",
            "RequirementRef -> ProofRef",
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


def _slugify_markdown_anchor(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[`*_~]", "", value)
    value = re.sub(r"[^a-z0-9\-\s]", "", value)
    value = re.sub(r"[\s\-]+", "-", value)
    return value.strip("-")


def _extract_local_anchors(doc_text: str) -> set[str]:
    anchors: set[str] = set()
    for line in doc_text.splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading:
                anchors.add(_slugify_markdown_anchor(heading))
    return anchors


def _resolve_docs_reference(ref: str) -> bool:
    if "#" in ref:
        rel, anchor = ref.split("#", 1)
    else:
        rel, anchor = ref, ""

    doc_path = _REPO_ROOT / rel
    if not doc_path.exists():
        return False
    if not anchor:
        return True

    anchors = _extract_local_anchors(doc_path.read_text(encoding="utf-8"))
    return anchor in anchors


def test_z0_m1_1_files_exist_and_reference_law_112() -> None:
    _declare("presence and law authority")
    assert _DOC_112.exists()
    assert _DOC_14.exists()
    assert _SCHEMA_PATH.exists()
    assert _DATA_PATH.exists()
    assert _SCOPE_PATH.exists()

    schema = _load_json(_SCHEMA_PATH)
    payload = _load_json(_DATA_PATH)

    assert payload["law_ref"] == "docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md"
    assert schema["properties"]["law_ref"]["const"] == payload["law_ref"]


def test_payload_validates_against_draft_2020_12_schema() -> None:
    _declare("json-schema validity and payload validation")
    schema = _load_json(_SCHEMA_PATH)
    payload = _load_json(_DATA_PATH)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(payload)


def test_scope_inventory_exactly_equals_remap_inventory() -> None:
    _declare("exhaustive scope coverage")
    payload = _load_json(_DATA_PATH)
    scope = _load_json(_SCOPE_PATH)

    scope_ids = set(scope["artifacts"])
    remap_ids = {record["artifact_id"] for record in payload["records"]}

    assert scope_ids == remap_ids


def test_every_remap_unit_is_atomic_or_explicit_bundle() -> None:
    _declare("atomicity declaration")
    payload = _load_json(_DATA_PATH)

    for record in payload["records"]:
        atomicity = record["artifact_atomicity"]
        members = record["members"]
        assert atomicity in {"ATOMIC", "BUNDLE"}
        if atomicity == "ATOMIC":
            assert members == []
        else:
            assert len(members) >= 2


def test_every_bundle_member_has_no_conflicting_state() -> None:
    _declare("bundle-state conflict exclusion")
    payload = _load_json(_DATA_PATH)
    records = payload["records"]
    by_id = {record["artifact_id"]: record for record in records}

    for record in records:
        if record["artifact_atomicity"] != "BUNDLE":
            continue
        for member in record["members"]:
            if member not in by_id:
                continue
            assert by_id[member]["remap_state"] == record["remap_state"]


def test_every_source_and_local_reference_resolves() -> None:
    _declare("reference resolution")
    payload = _load_json(_DATA_PATH)

    for record in payload["records"]:
        source_law = record["source_law"]
        source_module = record["source_module"]
        assert (_REPO_ROOT / source_law).exists()
        assert (_REPO_ROOT / source_module).exists()

        assert _resolve_docs_reference(record["backward_proof"]["requirement_ref"])
        assert _resolve_docs_reference(record["forward_readiness"]["requirement_ref"])
        assert _resolve_docs_reference(record["triangle_coherence"]["requirement_ref"])

        for proof_ref_field in (
            record["backward_proof"]["proof_ref"],
            record["forward_readiness"]["proof_ref"],
            record["triangle_coherence"]["proof_ref"],
        ):
            if proof_ref_field is None:
                continue
            assert _resolve_docs_reference(proof_ref_field)


def test_target_stage_belongs_to_fixed_z0_stage_registry() -> None:
    _declare("fixed stage registry")
    payload = _load_json(_DATA_PATH)
    allowed_states = set(payload["remap_states"])

    assert payload["target_z0_stage_registry"] == _EXPECTED_STAGE_REGISTRY

    used_states = {record["remap_state"] for record in payload["records"]}
    assert used_states.issubset(allowed_states)

    allowed_stages = set(payload["target_z0_stage_registry"])
    for record in payload["records"]:
        assert record["target_z0_stage"] in allowed_stages


def test_keep_residual_does_not_hide_triangle_evidence() -> None:
    _declare("keep residual with visible closure evidence")
    payload = _load_json(_DATA_PATH)

    for record in payload["records"]:
        if record["remap_state"] != "KEEP":
            continue
        if "POSITION_REPROOF_REQUIRED" not in record["residuals"]:
            continue
        assert record["remap_status"] == "PROVEN"
        assert record["triangle_coherence"]["status"] == "PROVEN"
        assert (
            record["triangle_coherence"]["proof_ref"]
            == "docs/117_Z0_M2C_MCE_CLOSURE_EVIDENCE.md#5-triangle-coherence-evidence"
        )


def test_rebuild_requires_declared_replacement() -> None:
    _declare("rebuild replacement declaration")
    payload = _load_json(_DATA_PATH)

    for record in payload["records"]:
        if record["remap_state"] != "REBUILD":
            continue
        replacement = record["replacement_artifact"]
        assert isinstance(replacement, str)
        assert replacement


def test_quarantine_has_no_z0_forward_authority() -> None:
    _declare("quarantine authority boundary")
    payload = _load_json(_DATA_PATH)

    for record in payload["records"]:
        if record["remap_state"] != "QUARANTINE":
            continue
        assert record["target_z0_stage"] == "LEGACY_HISTORICAL_ONLY"
        authority_after = record["authority_after"].lower()
        assert (
            "no z0 forward licensing" in authority_after
            or "not a licensed forward path in z0 mode" in authority_after
        )


def test_legacy_baseline_sha_is_pinned() -> None:
    _declare("baseline pin")
    payload = _load_json(_DATA_PATH)
    scope = _load_json(_SCOPE_PATH)

    baseline = payload["legacy_baseline_sha"]
    assert isinstance(baseline, str)
    assert re.fullmatch(r"[0-9a-f]{40}", baseline)
    assert scope["legacy_baseline_sha"] == baseline


def test_docs14_retains_m1_1_status_clarification() -> None:
    _declare("chain status boundary within m1.1 scope")
    roadmap = _DOC_14.read_text(encoding="utf-8")

    assert "Amendment-87 (Z0-M2 — Execution Status Clarification)" in roadmap
    assert "Z0-M1.1 is now marked done as corrective hardening baseline." in roadmap
    assert "Z0-M2 is current (not complete)" in roadmap


def test_z0_forbidden_legacy_shortcuts_remain_covered() -> None:
    _declare("forbidden legacy shortcut coverage")
    payload = _load_json(_DATA_PATH)
    by_id = {record["artifact_id"]: record for record in payload["records"]}

    assert by_id["VERBAL_MADLUL_CANDIDATE"]["remap_state"] in {"RETYPE", "QUARANTINE"}
    assert by_id["DAL_MADLUL_BINDING_CANDIDATE"]["remap_state"] == "QUARANTINE"
    assert by_id["RELATION_CLOSURE"]["remap_state"] == "RETYPE"
    assert by_id["NATIVE_RUNTIME_REGISTRY_LEGACY_FORWARD_PATH"]["remap_state"] == "QUARANTINE"
