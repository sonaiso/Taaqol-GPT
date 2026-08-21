"""Acceptance tests for docs/117 — Z0-M2 minimal complete triangle closure evidence.

Origin law     : docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md
Branch         : Z0-M2C (bounded closure evidence)
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
_DOC_117 = _REPO_ROOT / "docs" / "117_Z0_M2_MINIMAL_COMPLETE_TRIANGLE_CLOSURE_EVIDENCE.md"
_DOC_116 = _REPO_ROOT / "docs" / "116_V1_CLOSURE_EVIDENCE_LEDGER.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_SCHEMA = _REPO_ROOT / "schemas" / "z0_m2_mce_closure_evidence.schema.json"
_DATA = _REPO_ROOT / "data" / "z0_m2_mce_closure_evidence.json"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=f"Z0-M2C closure evidence ({branch_note})",
        constitutional_chain=("docs/112", "Z0-M1", "Z0-M1.1", "Z0-M2", "Z0-M2C"),
        chain_position="Z0-M2C bounded MCE closure evidence",
        origin_law_ref=(
            "docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md"
            "#4-minimal-complete-expansion-law"
        ),
        branch_of_origin=(
            "Bounded machine-auditable closure evidence that proves InternalClosure, "
            "BackwardProof, ForwardReadiness, and TriangleCoherence for Z0-M2."
        ),
        forbidden_shortcut_assertions=(
            "ClosureEvidence -> RuntimeOpening",
            "ClosureEvidence -> V1Closed",
            "Z0-M2C -> SuccessorRuntimeOpening",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeMutation",
            "SemanticClosure",
            "HukmClosure",
            "TruthCertification",
            "RealityClosure",
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


def test_z0_m2c_files_exist() -> None:
    _declare("presence")
    assert _DOC_112.exists()
    assert _DOC_117.exists()
    assert _DOC_116.exists()
    assert _DOC_14.exists()
    assert _SCHEMA.exists()
    assert _DATA.exists()


def test_z0_m2c_payload_validates_against_schema() -> None:
    _declare("schema validity")
    schema = _load_json(_SCHEMA)
    payload = _load_json(_DATA)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(payload)


def test_z0_m2c_components_are_all_proven_and_complete() -> None:
    _declare("four-component MCE proof")
    payload = _load_json(_DATA)
    by_name = {component["name"]: component for component in payload["components"]}

    assert payload["closure_state"] == "CLOSED"
    assert payload["closure_step_id"] == "Z0-M2C"
    assert payload["closure_formula"] == (
        "MCE_Z0-M2 = InternalClosure + BackwardProof + ForwardReadiness + TriangleCoherence"
    )

    assert set(by_name) == {
        "InternalClosure",
        "BackwardProof",
        "ForwardReadiness",
        "TriangleCoherence",
    }
    for component in by_name.values():
        assert component["status"] == "PROVEN"
        assert component["evidence_refs"]
        assert component["test_refs"]


def test_docs_117_declares_non_opening_boundary_and_trace_chain() -> None:
    _declare("boundary and trace")
    body = _DOC_117.read_text(encoding="utf-8")

    required_markers = (
        "Z0-M2C",
        "MCE_Z0-M2 =",
        "InternalClosure",
        "BackwardProof",
        "ForwardReadiness",
        "TriangleCoherence",
        "ClosureEvidence != RuntimeOpening",
        "ClosureEvidence != V1Closure",
        "no runtime mutation",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_14_registers_amendment_91_and_docs_116_proves_v1_05() -> None:
    _declare("roadmap + V1 ledger sync")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    v1_ledger = _DOC_116.read_text(encoding="utf-8")

    assert "Amendment-91 (Z0-M2C — Minimal Complete Triangle Closure Evidence)" in roadmap
    assert "Z0-M2 is marked done for bounded MCE closure evidence." in roadmap
    assert "| V1-05 | PROVEN |" in v1_ledger
    assert "tests/test_z0_m2_minimal_complete_triangle_closure_evidence.py" in v1_ledger
