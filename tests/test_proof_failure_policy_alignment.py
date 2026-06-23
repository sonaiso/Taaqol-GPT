"""Acceptance tests for PR #60 proof failure-policy alignment (audit-only).

Origin law     : docs/61 (ProofObject Failure-Policy Alignment)
Branch         : PR-60 (audit-only policy surface)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import csv
import functools
import json
import pathlib

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_POLICY_DOC = _REPO_ROOT / "docs" / "61_PROOF_FAILURE_POLICY_ALIGNMENT.md"
_POLICY_CSV = _REPO_ROOT / "data" / "proof_failure_policy.csv"
_CANONICAL_FAMILIES = _REPO_ROOT / "data" / "failure_alignment_canonical_families.json"
_COVERAGE_SCHEMA = _REPO_ROOT / "schemas" / "coverage_case.schema.json"

_EXPECTED_PROOFS = {
    "MRKProof",
    "DomainProof",
    "IdentityProof",
    "GateProof",
    "BridgeProof",
    "EvidenceProof",
    "CoverageProof",
}


@functools.cache
def _read_csv_rows_cached() -> tuple[tuple[tuple[str, str], ...], ...]:
    with _POLICY_CSV.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return tuple(tuple((key, value) for key, value in row.items()) for row in rows)


def _policy_rows() -> list[dict[str, str]]:
    return [dict(row) for row in _read_csv_rows_cached()]


@functools.cache
def _load_schema() -> dict[str, object]:
    return json.loads(_COVERAGE_SCHEMA.read_text(encoding="utf-8"))


def _schema_allowed_verdicts() -> set[str]:
    schema_doc = _load_schema()
    return set(schema_doc["properties"]["expected_verdict"]["enum"])


def _assert_case_allowed_by_schema(case: dict[str, object]) -> None:
    schema = _load_schema()
    required = set(schema["required"])
    missing = [name for name in required if name not in case]
    assert not missing

    verdict = case["expected_verdict"]
    assert verdict in schema["properties"]["expected_verdict"]["enum"]

    if verdict in {"EXPECTED_BLOCKED", "EXPECTED_PROOF_REQUIRED"}:
        assert isinstance(case.get("expected_failure_family"), str)
        assert case["expected_failure_family"]
    if verdict == "EXPECTED_RESIDUAL":
        assert isinstance(case.get("expected_residual_policy"), str)
        assert case["expected_residual_policy"]
    if verdict == "EXPECTED_BRIDGE_REQUIRED":
        bridges = case.get("required_bridges")
        assert isinstance(bridges, list)
        assert bridges and all(isinstance(item, str) and item for item in bridges)

    forbidden_fields = {
        "computed_verdict",
        "manual_verdict",
        "domain_proved",
        "identity_preserved",
        "gate_passed",
    }
    assert forbidden_fields.isdisjoint(case)


def test_pr60_policy_surface_exists_and_is_audit_only() -> None:
    content = _POLICY_DOC.read_text(encoding="utf-8")
    assert "Audit-only" in content
    assert "does not evaluate proofs" in content
    assert "does not emit computed verdict" in content
    assert "does not open runtime" in content


def test_every_proof_object_has_policy_row() -> None:
    rows = _policy_rows()
    proof_kinds = {row["proof_object"] for row in rows}
    assert proof_kinds == _EXPECTED_PROOFS
    assert len(rows) == len(_EXPECTED_PROOFS)


def test_policy_families_are_canonical() -> None:
    rows = _policy_rows()
    canonical = json.loads(_CANONICAL_FAMILIES.read_text(encoding="utf-8"))["canonical_families"]
    canonical_set = set(canonical)
    for row in rows:
        assert row["failure_family"] in canonical_set


def test_policy_verdicts_are_schema_accepted() -> None:
    allowed = _schema_allowed_verdicts()
    for row in _policy_rows():
        for verdict in row["allowed_expected_verdicts"].split("|"):
            assert verdict in allowed


def test_bridgeproof_maps_to_bridge_required_and_bridge_family() -> None:
    row = next(item for item in _policy_rows() if item["proof_object"] == "BridgeProof")
    assert row["failure_family"] == "BRIDGE"
    assert row["allowed_expected_verdicts"] == "EXPECTED_BRIDGE_REQUIRED"
    assert "required_bridges" in row["required_metadata"].split("|")


def test_identityproof_not_residual_only() -> None:
    row = next(item for item in _policy_rows() if item["proof_object"] == "IdentityProof")
    verdicts = set(row["allowed_expected_verdicts"].split("|"))
    assert "EXPECTED_BLOCKED" in verdicts or "EXPECTED_PROOF_REQUIRED" in verdicts
    assert "EXPECTED_RESIDUAL" not in verdicts


def test_evidenceproof_cannot_promote_rank() -> None:
    row = next(item for item in _policy_rows() if item["proof_object"] == "EvidenceProof")
    assert row["rank_promotion_allowed"] == "false"


def test_coverageproof_cannot_emit_computed_verdict() -> None:
    row = next(item for item in _policy_rows() if item["proof_object"] == "CoverageProof")
    assert row["computed_verdict_allowed"] == "false"


def test_all_rows_are_audit_only_and_non_executable() -> None:
    for row in _policy_rows():
        assert row["runtime_status"] == "AUDIT_ONLY"
        assert row["executable"] == "false"


def test_schema_conditionals_and_antipattern_rejection() -> None:
    _assert_case_allowed_by_schema(
        {
            "case_id": "c-1",
            "proof_object": "IdentityProof",
            "expected_verdict": "EXPECTED_BLOCKED",
            "expected_failure_family": "IDENTITY",
        }
    )
    _assert_case_allowed_by_schema(
        {
            "case_id": "c-2",
            "proof_object": "BridgeProof",
            "expected_verdict": "EXPECTED_BRIDGE_REQUIRED",
            "required_bridges": ["bridge/identity"],
        }
    )


def test_forbidden_runtime_files_remain_absent() -> None:
    forbidden_paths = (
        _REPO_ROOT / "binding_kernel.py",
        _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "binding_kernel.py",
        _REPO_ROOT / "coverage_matrix_v0.1.yaml",
        _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "coverage_matrix_v0.1.yaml",
    )
    assert all(not path.exists() for path in forbidden_paths)
