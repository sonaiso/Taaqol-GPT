"""Acceptance tests for docs/62 — Coupled Dalalah Matrix Law.

Origin law     : docs/62 (Coupled Dalālah Matrix Law)
Branch         : LAFZI-D0 (law-only coupled dalālah matrix staging)
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
_DOC_62 = _REPO_ROOT / "docs" / "62_COUPLED_DALALAH_MATRIX_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"

_FORBIDDEN_OUTPUTS = (
    "IfadahCandidate",
    "MafhumCandidate",
    "HukmCandidate",
    "TanzilCandidate",
    "Reality",
    "TruthValue",
)


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/62_COUPLED_DALALAH_MATRIX_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("LAFZI-C8", "LAFZI-D0", "CoupledDalalahMatrixLaw"),
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


def test_docs_62_exists_and_is_law_only() -> None:
    _declare("document existence")
    content = _read(_DOC_62)

    assert "Status:" in content
    assert "law-only" in content
    assert "no runtime code" in content
    assert "no global `FailureCode` expansion" in content


def test_docs_62_places_threefold_dalalah_after_wadi_and_coupling() -> None:
    _declare("corrected placement")
    content = _read(_DOC_62)

    assert "No Mutabaqah without Wad'iMadlulClosed." in content
    assert "No Mutabaqah without CoupledDalalah." in content
    assert "No Tadammun without Mutabaqah." in content
    assert "No Iltizam without Tadammun." in content
    assert (
        "DalAloneClosed\n"
        " -> LafziMadlulClosed\n"
        " -> Wad'iMadlulClosed\n"
        " -> CoupledDalalah\n"
        " -> DalalahMatrix\n"
        " -> WordCapability\n"
        " -> Relation\n"
        " -> Sentence\n"
        " -> Ifadah\n"
        " -> Mantuq\n"
        " -> Mafhum\n"
        " -> Hukm"
    ) in content


def test_docs_62_distinguishes_dalalah_correspondence_from_hukm() -> None:
    _declare("mutabaqah is not hukm correspondence", _FORBIDDEN_OUTPUTS)
    content = _read(_DOC_62)

    assert "MutabaqahDalalah != HukmCorrespondence" in content
    assert "judgment to reality or evidence" in content
    for forbidden in _FORBIDDEN_OUTPUTS:
        assert forbidden in content


def test_docs_62_declares_gate_matrix_and_inverse_tests() -> None:
    _declare("gate matrix inverse tests")
    content = _read(_DOC_62)

    for gate in [
        "CoupledDalalah",
        "MutabaqahGate",
        "TadammunGate",
        "IltizamGate",
        "ResidualAudit",
    ]:
        assert gate in content
    for inverse_test in [
        "does the result return to the whole placed meaning?",
        "is the part inside the bounded definition?",
        "is it outside the definition and linked by evidence?",
    ]:
        assert inverse_test in content


def test_docs_62_declares_local_residual_vocabulary() -> None:
    _declare("local dalālah matrix residual vocabulary")
    content = _read(_DOC_62)

    for residual in [
        "MADLUL_BOUNDARY_REQUIRED",
        "WAD_AUTHORITY_REQUIRED",
        "USAGE_SCOPE_REQUIRED",
        "MUTABAQAH_REQUIRED",
        "INTERNAL_PART_REQUIRED",
        "PART_OUTSIDE_MADLUL",
        "LAZIM_OUTSIDE_REQUIRED",
        "LUZUM_EVIDENCE_REQUIRED",
        "MERE_ASSOCIATION_NOT_LUZUM",
        "DOMAIN_MISMATCH",
        "ISHTIRAK_REQUIRES_QARINAH",
        "NAQL_SCOPE_REQUIRED",
        "MAJAZ_LICENSE_REQUIRED",
        "HIDDEN_DALALAH_MATRIX_RESIDUAL",
        "FORBIDDEN_IFADAH_JUMP",
        "FORBIDDEN_HUKM_JUMP",
    ]:
        assert residual in content


def test_docs_62_preserves_historical_dalalah_surfaces() -> None:
    _declare("legacy surface reconciliation")
    content = _read(_DOC_62)

    for surface in ["MutabaqahCandidate", "TadammunCandidate", "IltizamCandidate"]:
        assert surface in content
    assert "not silently" in content
    assert "consumer of Wad'iMadlulClosed / CoupledDalalah" in content


def test_roadmap_and_claude_register_lafzi_d_sequence_after_lafzi_c8() -> None:
    _declare("roadmap registration")
    roadmap = _read(_DOC_14)
    claude = _read(_CLAUDE)

    for content in (roadmap, claude):
        assert "LAFZI-D0 Coupled Dalalah Matrix Law" in content
        assert "LAFZI-D1 CoupledDalalah carrier surface" in content
        assert "LAFZI-D2 MutabaqahGate" in content
        assert "LAFZI-D3 TadammunGate" in content
        assert "LAFZI-D4 IltizamGate" in content
        assert "LAFZI-D5 DalalahMatrixResidualAudit" in content
        assert "LAFZI-D6 DalalahMatrixClosed -> WordCapability" in content
        assert content.index("LAFZI-C8 Wad'iMadlulClosed -> CoupledDalalahGate") < (
            content.index("LAFZI-D0 Coupled Dalalah Matrix Law")
        )

    assert "Amendment-42 (LAFZI-D0" in roadmap
    assert "docs/62" in roadmap
