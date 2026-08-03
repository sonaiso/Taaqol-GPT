"""Acceptance tests for docs/100 Licensed Lexicon Slot Geometry Boundary Law.

Origin law     : docs/81 + docs/82 + docs/89 + docs/99 + docs/100
Branch         : LEXICON-SLOT-L0 (law-only lexicon slot boundary)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_100 = _REPO_ROOT / "docs" / "100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/81_LEXICAL_EVIDENCE_DATA_LAW.md + "
            "docs/82_WADI_TO_NAQL_MAJAZ_BOUNDARY_LAW.md + "
            "docs/89_PRECOMPOSITION_VERIFICATION_CONTRACTABILITY_LAW.md + "
            "docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md + "
            "docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md"
        ),
        branch_name=f"LEXICON-SLOT-L0 ({branch_note})",
        constitutional_chain=("docs/81", "docs/82", "docs/89", "docs/99", "docs/100"),
        chain_position="LEXICON-SLOT-L0 law-only lexical slot geometry boundary",
        origin_law_ref="docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md#1-constitutional-definition-of-lexicon-responsibility",
        branch_of_origin=(
            "Law-only lexical slot geometry boundary that constrains lexicon output "
            "to licensed candidate slots with visible residuals and trace."
        ),
        forbidden_shortcut_assertions=(
            "Lexicon -> FinalContextualMeaning",
            "LexiconClosure -> MeaningClosure",
            "LexicalSlot -> Hukm",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "FinalContextualMeaning",
            "OntologicalFact",
            "EmpiricalFact",
            "Ifadah",
            "Hukm",
            "Truth",
            "RealityCertificate",
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


def test_docs_100_exists_and_is_law_only() -> None:
    _declare("document existence")
    body = _DOC_100.read_text(encoding="utf-8")

    assert _DOC_100.exists()
    assert "Status: constitutional law document (law-only)." in body
    assert "RUNTIME_NOT_OPENED = {" in body
    assert "introduces no direct semantic/hukm/truth closure runtime" in body


def test_docs_100_declares_slot_geometry_rank_vector_and_contract_surface() -> None:
    _declare("slot geometry and transition contracts")
    body = _DOC_100.read_text(encoding="utf-8")

    required_markers = (
        "LexicalSlot = <",
        "RankVector = (",
        (
            "GraphicIdentity != PhonologicalIdentity != LexemeIdentity != "
            "RootIdentity != SenseIdentity"
        ),
        "TC_SR : SourceSlot",
        "TC_RI : ReadingCandidate",
        "TC_IL : IdentityCarrier",
        "TC_LW : LexicalEntitySlot",
        "TC_WS : WadCandidate",
        "TC_SD : LexicalSenseSlot",
        (
            "SourceSlot -> ReadingSlot -> IdentitySlot -> LexicalEntitySlot -> "
            "WadSlot -> LexicalSenseSlot -> UsageSlot -> DalalahCandidateSlot"
        ),
    )
    for marker in required_markers:
        assert marker in body


def test_docs_100_declares_final_responsibility_rules() -> None:
    _declare("final responsibility rules")
    body = _DOC_100.read_text(encoding="utf-8")

    required_markers = (
        "No Lexical Output Without LicensedSlot",
        "No LicensedSlot Without Source+Identity+Type+Domain+Evidence+RankVector+Residuals+Trace",
        "LexiconClosure != MeaningClosure",
    )
    for marker in required_markers:
        assert marker in body
