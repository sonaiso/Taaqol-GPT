"""Acceptance tests for docs/59 — Lafzi Madlul Correspondence Law.

Origin law     : docs/59 (Lafzi Madlul Correspondence Law)
Branch         : LAFZI-B0 (law-only correspondence staging)
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
_DOC_59 = _REPO_ROOT / "docs" / "59_LAFZI_MADLUL_CORRESPONDENCE_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"

_FORBIDDEN_LAFZI_OUTPUTS = (
    "Wad'iMadlul",
    "MutabaqahCandidate",
    "TadammunCandidate",
    "IltizamCandidate",
    "RelationCandidate",
    "IfadahCandidate",
    "HukmCandidate",
    "ActualRelation",
)


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/59_LAFZI_MADLUL_CORRESPONDENCE_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("DAL-A8", "LAFZI-B0", "LafziMadlulCorrespondenceLaw"),
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


def test_docs_59_exists_and_is_law_only() -> None:
    _declare("document existence")
    content = _read(_DOC_59)
    assert len(content) > 500
    assert "Status:" in content
    assert "law-only" in content
    assert "no runtime code" in content


def test_docs_59_defines_correspondence_not_closure() -> None:
    _declare("CorrespondenceNotClosureLaw")
    content = _read(_DOC_59)
    assert "DalAloneClosed" in content
    assert "LafziMadlulCandidateSet" in content
    assert "LafziMadlulClosed" in content
    assert "NoAutomaticOneToOneMapping" in content
    assert "DalAloneClosed -> LafziMadlulClosed" in content
    assert "CorrespondenceNotClosureLaw" in content


def test_docs_59_declares_mapping_states() -> None:
    _declare("mapping states")
    content = _read(_DOC_59)
    for state in ["ONE_TO_ONE", "ONE_TO_MANY", "BLOCKED", "DEFERRED"]:
        assert state in content


def test_docs_59_declares_future_carriers_without_implementing_them() -> None:
    _declare("future carrier surface")
    content = _read(_DOC_59)
    for carrier in [
        "LafziMadlulCandidate",
        "LafziMadlulCandidateSet",
        "WordKindCandidate",
        "SourceIdentityCandidate",
        "FormStateCandidate",
        "InternalWordPathCandidate",
        "LafziResidual",
        "LafziScope",
    ]:
        assert carrier in content
    assert "LAFZI-B0 itself ships no runtime code" in content


def test_docs_59_declares_lafzi_gate_sequence() -> None:
    _declare("lafzi gate sequence")
    content = _read(_DOC_59)
    for gate in [
        "WordKindGate",
        "SourceIdentityGate",
        "FormStateGate",
        "InternalWordPathGate",
        "LafziResidualAudit",
        "Wad'iMadlulGate",
    ]:
        assert gate in content


def test_docs_59_declares_local_lafzi_residual_vocabulary() -> None:
    _declare("local lafzi residual vocabulary")
    content = _read(_DOC_59)
    for residual in [
        "WORD_KIND_AMBIGUOUS",
        "SOURCE_IDENTITY_REQUIRED",
        "FORM_STATE_REQUIRED",
        "ISM_PATH_AMBIGUOUS",
        "FIIL_MASDAR_REQUIRED",
        "FIIL_TEMPORAL_IMAGE_REQUIRED",
        "HARF_OPERATOR_REQUIRED",
        "REFERENCE_SOURCE_REQUIRED",
        "PROPER_SELF_DESIGNATION_REQUIRED",
        "MUSHTAQ_REQUIRES_MASDAR",
        "MULTIPLE_LAFZI_CANDIDATES",
        "LAFZI_SCOPE_REQUIRED",
        "UNUSED_DAL_NO_LAFZI",
        "LOAN_LAFZI_PATH_REQUIRED",
        "FORBIDDEN_WADI_JUMP",
        "FORBIDDEN_MUTABAQA_JUMP",
        "FORBIDDEN_RELATION_JUMP",
        "FORBIDDEN_HUKM_JUMP",
    ]:
        assert residual in content


def test_docs_59_forbids_semantic_and_relation_jumps() -> None:
    _declare("forbidden lafzi jumps", _FORBIDDEN_LAFZI_OUTPUTS)
    content = _read(_DOC_59)
    for forbidden in _FORBIDDEN_LAFZI_OUTPUTS:
        assert forbidden in content
    for shortcut in [
        "LafziMadlul -> Wad'iMadlul",
        "LafziMadlul -> Mutabaqah",
        "LafziMadlul -> Relation",
        "LafziMadlul -> Ifadah",
        "LafziMadlul -> Hukm",
        "Ism -> ActualFa'il",
        "Fiil -> ActualSubject",
        "Harf -> ActualRelation",
    ]:
        assert shortcut in content


def test_docs_59_declares_golden_examples() -> None:
    _declare("golden examples")
    content = _read(_DOC_59)
    for example in ["مِنْ", "رَجُل", "ضَرَبَ", "علم", "عين"]:
        assert example in content
    assert "ActualRelation" in content
    assert "ActualFa'il" in content
    assert "ActualSubject" in content


def test_roadmap_and_claude_register_lafzi_b0_after_dal_a8() -> None:
    _declare("roadmap registration")
    roadmap = _read(_DOC_14)
    claude = _read(_CLAUDE)
    assert "Amendment-36 (LAFZI-B0" in roadmap
    assert "docs/59 Lafzi Madlul Correspondence Law" in roadmap
    assert "LAFZI-B0 Lafzi Madlul Correspondence Law" in roadmap
    assert "LAFZI-B0 Lafzi Madlul Correspondence Law" in claude
    assert "DAL-A8  DalAloneClosed -> LafziMadlulGate integration" in roadmap
    assert roadmap.index("DAL-A8  DalAloneClosed -> LafziMadlulGate integration") < roadmap.index(
        "LAFZI-B0 Lafzi Madlul Correspondence Law"
    )
    assert claude.index("DAL-A8  DalAloneClosed -> LafziMadlulGate integration") < claude.index(
        "LAFZI-B0 Lafzi Madlul Correspondence Law"
    )
