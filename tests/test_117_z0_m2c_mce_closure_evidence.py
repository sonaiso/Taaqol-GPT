"""Acceptance tests for docs/117 — Z0-M2C MCE closure evidence.

Origin law     : docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md
Branch         : Z0-M2C (closure-evidence only)
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
_DOC_117 = _REPO_ROOT / "docs" / "117_Z0_M2C_MCE_CLOSURE_EVIDENCE.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_116 = _REPO_ROOT / "docs" / "116_V1_CLOSURE_EVIDENCE_LEDGER.md"
_DATA_PATH = _REPO_ROOT / "data" / "z0_legacy_remap.json"
_REQUIRED_PROOF_REFS = {
    "backward_proof": "docs/117_Z0_M2C_MCE_CLOSURE_EVIDENCE.md#3-backward-proof-evidence",
    "forward_readiness": "docs/117_Z0_M2C_MCE_CLOSURE_EVIDENCE.md#4-forward-readiness-evidence",
    "triangle_coherence": "docs/117_Z0_M2C_MCE_CLOSURE_EVIDENCE.md#5-triangle-coherence-evidence",
}


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md",
        branch_name=f"Z0-M2C MCE closure evidence ({branch_note})",
        constitutional_chain=("docs/112", "Z0-M1", "Z0-M1.1", "Z0-M2", "Z0-M2C"),
        chain_position="Z0-M2C dedicated closure-evidence step (docs/data/tests only)",
        origin_law_ref="docs/112_ZERO_CONSTITUTION_REFOUNDATION_LAW.md#10-next-licensed-steps",
        branch_of_origin=(
            "Dedicated MCE triangle closure evidence binding over the remap ledger "
            "without runtime mutation."
        ),
        forbidden_shortcut_assertions=(
            "EvidenceLedgerUpdate -> RuntimeMutation",
            "Z0-M2ClosureEvidence -> V1GlobalClosure",
            "DocsOnlyClosure -> AuthorityCertificateIssuance",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeMutationClaim",
            "V1AggregateClosureClaim",
            "AuthorityPromotionClaim",
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


def test_docs_117_exists_and_declares_docs_only_boundary() -> None:
    _declare("document boundary")
    body = _DOC_117.read_text(encoding="utf-8")
    assert _DOC_117.exists()
    assert "Z0-M2C MCE Closure Evidence Record" in body
    assert "docs/data/tests only" in body
    assert "does not open new runtime behavior" in body


def test_remap_records_are_proven_with_resolvable_mce_triangle_refs() -> None:
    _declare("remap evidence closure")
    payload = _load_json(_DATA_PATH)

    records = payload["records"]
    assert records

    for record in records:
        assert record["remap_status"] == "PROVEN"
        for field, expected_ref in _REQUIRED_PROOF_REFS.items():
            proof = record[field]
            assert proof["status"] == "PROVEN"
            assert proof["proof_ref"] == expected_ref


def test_roadmap_registers_amendment_91_and_m2c_effect() -> None:
    _declare("roadmap amendment record")
    body = _DOC_14.read_text(encoding="utf-8")

    assert "Amendment-91 (Z0-M2C — MCE Closure Evidence Record)" in body
    assert "records `Z0-M2` as done via dedicated evidence closure" in body
    assert "`Z0-M3` is now the current bounded successor branch." in body


def test_v1_ledger_objective_05_is_no_longer_missing_m2_closure() -> None:
    _declare("v1 objective linkage")
    body = _DOC_116.read_text(encoding="utf-8")

    assert "| V1-05 | PROVEN |" in body
    assert "Z0_M2_MCE_CLOSURE_MISSING" not in body
    assert "tests/test_117_z0_m2c_mce_closure_evidence.py" in body
