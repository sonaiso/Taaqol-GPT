"""Acceptance tests for docs/60 — Wad'i Madlul Condition Law.

Origin law     : docs/60 (Wad'i Madlul Condition Law)
Branch         : LAFZI-C0 (law-only wadʿī condition staging)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_60 = _REPO_ROOT / "docs" / "60_WADI_MADLUL_CONDITION_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"

_FORBIDDEN_WADI_OUTPUTS = (
    "MutabaqahCandidate",
    "TadammunCandidate",
    "IltizamCandidate",
    "IfadahCandidate",
    "HukmCandidate",
    "TanzilCandidate",
    "Reality",
)


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/60_WADI_MADLUL_CONDITION_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("LAFZI-B7", "LAFZI-C0", "Wad'iMadlulConditionLaw"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=forbidden_outputs,
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


def _read(path: pathlib.Path) -> str:
    if not path.exists():
        pytest.skip(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def test_docs_60_exists_and_is_law_only() -> None:
    _declare("document existence")
    content = _read(_DOC_60)
    assert len(content) > 500
    assert "Status:" in content
    assert "law-only" in content
    assert "no runtime code" in content


def test_docs_60_defines_wadi_not_automatic_closure() -> None:
    _declare("Wad'iMadlulConditionLaw")
    content = _read(_DOC_60)
    assert "LafziMadlulClosed" in content
    assert "Wad'iMadlulGate" in content
    assert "Wad'iMadlulContract" in content
    assert "LafziMadlulClosed -> Wad'iMadlulClosed" in content
    assert "No Wad'iMadlulClosed from LafziMadlulClosed alone" in content


def test_docs_60_declares_licensed_chain_order() -> None:
    _declare("licensed chain order")
    content = _read(_DOC_60)
    chain_terms = [
        "DalAloneClosed",
        "LafziMadlulClosed",
        "Wad'iMadlulClosed",
        "CoupledDalalah",
        "Mutabaqah",
        "Tadammun",
        "Iltizam",
    ]
    for term in chain_terms:
        assert term in content
    assert content.index("Wad'iMadlulClosed") < content.index("CoupledDalalah")
    assert content.index("CoupledDalalah") < content.index("Mutabaqah")


def test_docs_60_specifies_wadi_contract_fields_and_forbidden_surface() -> None:
    _declare("Wad'iMadlulContract", _FORBIDDEN_WADI_OUTPUTS)
    content = _read(_DOC_60)
    for field in [
        "lafzi_madlul_closed_ref",
        "wad_kind",
        "wad_authority",
        "usage_scope",
        "meaning_identity",
        "transfer_or_majaz_status",
        "residuals",
        "rank",
        "trace_ref",
    ]:
        assert field in content
    for forbidden in ["mutabaqah", "tadammun", "iltizam", "ifada", "hukm", "tanzil", "reality"]:
        assert forbidden in content


def test_docs_60_declares_w0_w7_gate_sequence() -> None:
    _declare("W0-W7 gates")
    content = _read(_DOC_60)
    for gate in [
        "W0  LafziMadlulClosedGate",
        "W1  WadKindGate",
        "W2  WadAuthorityGate",
        "W3  UsageScopeGate",
        "W4  MeaningIdentityGate",
        "W5  TransferMajazGate",
        "W6  WadiResidualAudit",
        "W7  WadiStopGate",
    ]:
        assert gate in content


def test_docs_60_declares_transfer_and_majaz_requirements() -> None:
    _declare("transfer and majaz requirements")
    content = _read(_DOC_60)
    for requirement in [
        "OriginalWad'",
        "TransferCause",
        "NewUsageScope",
        "PreservedTrace",
        "QadihDifference",
        "OriginalHaqiqah",
        "Relation",
        "Qarinah",
        "PreventerOfLiteralMeaning",
    ]:
        assert requirement in content


def test_docs_60_declares_local_wadi_residual_vocabulary() -> None:
    _declare("local wadʿī residual vocabulary")
    content = _read(_DOC_60)
    for residual in [
        "LAFZI_MADLUL_CLOSED_REQUIRED",
        "WAD_KIND_REQUIRED",
        "WAD_AUTHORITY_REQUIRED",
        "USAGE_SCOPE_REQUIRED",
        "MEANING_IDENTITY_REQUIRED",
        "TRANSFER_ORIGIN_REQUIRED",
        "MAJAZ_HAQIQAH_REQUIRED",
        "MAJAZ_QARINAH_REQUIRED",
        "HIDDEN_WADI_RESIDUAL",
        "FORBIDDEN_MUTABAQA_JUMP",
        "FORBIDDEN_TADAMMUN_JUMP",
        "FORBIDDEN_ILTIZAM_JUMP",
        "FORBIDDEN_HUKM_JUMP",
    ]:
        assert residual in content


def test_docs_60_forbids_relation_ifadah_hukm_and_reality_jumps() -> None:
    _declare("forbidden wadʿī jumps", _FORBIDDEN_WADI_OUTPUTS)
    content = _read(_DOC_60)
    for forbidden in _FORBIDDEN_WADI_OUTPUTS:
        assert forbidden in content
    for shortcut in [
        "LafziMadlul -> Mutabaqah",
        "LafziMadlul -> Tadammun",
        "LafziMadlul -> Iltizam",
        "Wad'iMadlulClosed -> Mutabaqah",
        "Wad'iMadlulClosed -> Tadammun",
        "Wad'iMadlulClosed -> Iltizam",
        "Wad'iMadlulClosed -> Ifadah",
        "Wad'iMadlulClosed -> Hukm",
        "Wad'iMadlulClosed -> Reality",
    ]:
        assert shortcut in content


def test_docs_60_preserves_legacy_surfaces_without_reinterpretation() -> None:
    _declare("legacy surface reconciliation")
    content = _read(_DOC_60)
    for surface in ["VerbalMadlulCandidate", "SemanticSlotFrame", "MutabaqahCandidate"]:
        assert surface in content
    assert "not silently reinterpreted" in content


def test_docs_60_declares_future_runtime_sequence_without_shipping_it() -> None:
    _declare("future runtime sequence")
    content = _read(_DOC_60)
    for step in [
        "LAFZI-C1",
        "LAFZI-C2",
        "LAFZI-C3",
        "LAFZI-C4",
        "LAFZI-C5",
        "LAFZI-C6",
        "LAFZI-C7",
        "LAFZI-C8",
    ]:
        assert step in content
    assert "LAFZI-C0` itself ships no runtime code" in content


def test_roadmap_and_claude_register_lafzi_c0_after_lafzi_b7() -> None:
    _declare("roadmap registration")
    roadmap = _read(_DOC_14)
    claude = _read(_CLAUDE)
    assert "Amendment-37 (LAFZI-C0" in roadmap
    assert "docs/60 Wad'i Madlul Condition Law" in roadmap
    assert "LAFZI-C0 Wad'iMadlulConditionLaw" in roadmap
    assert "LAFZI-C0 Wad'iMadlulConditionLaw" in claude
    assert "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration" in roadmap
    lafzi_b7 = "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration"
    lafzi_c0 = "LAFZI-C0 Wad'iMadlulConditionLaw"
    assert roadmap.index(lafzi_b7) < roadmap.index(lafzi_c0)
    assert claude.index(lafzi_b7) < claude.index(lafzi_c0)
