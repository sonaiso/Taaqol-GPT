"""Acceptance tests for docs/58 — DalAlone Atomic Closure Law.

Origin law     : docs/58 (DalAlone Atomic Closure Law)
Branch         : DAL-A0 (law-only atomic DAL closure staging)
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
_DOC_58 = _REPO_ROOT / "docs" / "58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> ConstitutionalTestCase:
    case = ConstitutionalTestCase(
        origin_law="docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("DAL-A0", "DalAloneAtomicClosureLaw"),
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
    return case


def _read(path: pathlib.Path) -> str:
    if not path.exists():
        pytest.skip(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def test_docs_58_exists_and_is_law_only() -> None:
    _declare("document existence")
    content = _read(_DOC_58)
    assert len(content) > 500
    assert "Status:" in content
    assert "law-only" in content
    assert "no runtime code" in content


def test_docs_58_defines_dal_alone_before_lafzi_gate() -> None:
    _declare("DalAloneClosed before LafziMadlulGate")
    content = _read(_DOC_58)
    assert "DalAloneClosed" in content
    assert "LafziMadlulGate" in content
    assert "No LafziMadlulGate before DalAloneClosed" in content


def test_docs_58_forbids_required_shortcuts() -> None:
    _declare(
        "forbidden DAL shortcuts",
        ("ArabicSound", "DalAloneClosed", "Meaning", "Ifadah", "Hukm"),
    )
    content = _read(_DOC_58)
    assert "UnicodeTrace -> ArabicSound" in content
    assert "CellSequence != DalAloneClosed" in content
    assert "DalAloneClosed is atomic closure, not meaning" in content
    assert "meaning, word kind, root, pattern" in content


def test_docs_58_declares_required_atomic_gates() -> None:
    _declare("atomic gate inventory")
    content = _read(_DOC_58)
    for gate in [
        "RawAcousticTraceGate",
        "ArabicSoundInventoryGate",
        "MakhrajSifahMatrixGate",
        "HamzaResolutionGate",
        "ShaddaIdghamGate",
        "TanwinTraceGate",
        "SukunCollisionGate",
        "SyllableLicenseGate",
        "WaqfLicenseGate",
        "WaslLicenseGate",
        "UsageBeforeMeaningGate",
    ]:
        assert gate in content


def test_docs_58_declares_local_residual_vocabulary() -> None:
    _declare("local residual vocabulary")
    content = _read(_DOC_58)
    for residual in [
        "RAW_TRACE_NOT_SPEECH",
        "MAKHRAJ_MISSING",
        "SIFAH_MISSING",
        "QADIH_SOUND_DIFF_MISSING",
        "HARAKA_WITHOUT_CARRIER",
        "MADD_WITHOUT_EXTENSION",
        "SHADDA_UNEXPANDED",
        "HAMZA_UNRESOLVED",
        "WASL_HAMZA_UNRESOLVED",
        "SUKUN_COLLISION",
        "SYLLABLE_UNLICENSED",
        "WAQF_UNTESTED",
        "WASL_UNTESTED",
        "UNVOCALIZED_SURFACE",
        "PHONETIC_SEQUENCE_AMBIGUOUS",
        "UNUSED_LAFZ",
        "LOAN_PATH_REQUIRED",
        "DELETION_UNLICENSED",
        "ENERGY_COLLISION",
    ]:
        assert residual in content


def test_docs_58_preserves_pre_semantic_boundary() -> None:
    _declare("pre-semantic forbidden surface", ("WordKind", "IfadahCandidate", "HukmCandidate"))
    content = _read(_DOC_58)
    for forbidden in [
        "WordKind",
        "Root",
        "Pattern",
        "LexicalMeaning",
        "VerbalMadlulCandidate",
        "IfadahCandidate",
        "HukmCandidate",
        "TanzilCandidate",
        "Reality",
    ]:
        assert forbidden in content


def test_docs_58_registers_later_runtime_sequence_without_shipping_it() -> None:
    _declare("later runtime sequence")
    content = _read(_DOC_58)
    for step in ["DAL-A1", "DAL-A2", "DAL-A3", "DAL-A4", "DAL-A5", "DAL-A6", "DAL-A7", "DAL-A8"]:
        assert step in content
    assert "DAL-A0 itself ships no runtime code" in content


def test_roadmap_and_claude_register_dal_a0() -> None:
    _declare("roadmap registration")
    roadmap = _read(_DOC_14)
    claude = _read(_CLAUDE)
    assert "Amendment-35 (DAL-A0" in roadmap
    assert "DAL-A0  DalAlone Atomic Closure Law" in roadmap
    assert "DAL-A0  DalAlone Atomic Closure Law" in claude
    assert "docs/58" in roadmap
    assert "docs/58" in claude
