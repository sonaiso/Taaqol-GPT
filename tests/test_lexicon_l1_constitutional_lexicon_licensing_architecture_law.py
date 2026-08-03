"""Acceptance tests for docs/99 — Constitutional Lexicon Licensing Architecture Law.

Origin law     : docs/81 + docs/82 + docs/89 + docs/99
Branch         : LEXICON-L1 (law-only lexical licensing architecture)
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
_DOC_81 = _REPO_ROOT / "docs" / "81_LEXICAL_EVIDENCE_DATA_LAW.md"
_DOC_82 = _REPO_ROOT / "docs" / "82_WADI_TO_NAQL_MAJAZ_BOUNDARY_LAW.md"
_DOC_89 = _REPO_ROOT / "docs" / "89_PRECOMPOSITION_VERIFICATION_CONTRACTABILITY_LAW.md"
_DOC_99 = _REPO_ROOT / "docs" / "99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/81_LEXICAL_EVIDENCE_DATA_LAW.md + "
            "docs/82_WADI_TO_NAQL_MAJAZ_BOUNDARY_LAW.md + "
            "docs/89_PRECOMPOSITION_VERIFICATION_CONTRACTABILITY_LAW.md + "
            "docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md"
        ),
        branch_name=f"LEXICON-L1 ({branch_note})",
        constitutional_chain=("docs/81", "docs/82", "docs/89", "docs/99", "LEXICON-L1"),
        chain_position="LEXICON-L1 law-only multi-layer lexical licensing architecture",
        origin_law_ref="docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md#1-governing-role-and-constitutional-equation",
        branch_of_origin=(
            "Law-only declaration of layered lexical licensing architecture from "
            "source preservation to lexical-license boundary."
        ),
        forbidden_shortcut_assertions=(
            "LexiconEntry -> FinalMeaning",
            "LexiconEntry -> Hukm",
            "SurfaceForm -> RootIdentity",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RelationCandidate",
            "IfadahCandidate",
            "HukmCandidate",
            "RealityCandidate",
            "FinalMeaning",
            "Truth",
            "Certainty",
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


def test_docs_99_exists_and_is_law_only() -> None:
    _declare("document existence")
    body = _DOC_99.read_text(encoding="utf-8")

    assert _DOC_99.exists()
    assert "Status: constitutional law document (law-only)." in body
    assert "RUNTIME_NOT_OPENED = {" in body
    assert "introduces no runtime code" in body


def test_docs_99_declares_governing_lexicon_role_and_transition() -> None:
    _declare("governing role and transition")
    body = _DOC_99.read_text(encoding="utf-8")

    required_markers = (
        "LEXICON_NOT_EQUAL = {MeaningGenerator, Ifadah, Hukm, Truth, Certainty, Reality}",
        "LEXICON_ROLE = LicensedConventionRegistry + EvidenceGraph + "
        "ConceptualCapability + ResidualAudit",
        "LICENSED_TRANSITION = ContractableUnit -> LexicalMadlulCandidate",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_99_declares_multi_entity_and_layer_separation() -> None:
    _declare("entity and layer separation")
    body = _DOC_99.read_text(encoding="utf-8")

    required_markers = (
        "LexicalEntity",
        "JamidStemEntity",
        "BorrowedEntity",
        "RawReading NOT_EQUAL CriticalReading",
        "SurfaceForm DOES_NOT_IMPLY RootIdentity",
        "RootIdentity requires RootPathGate",
        "SourceGloss NOT_EQUAL ConceptualOrigin",
        "ConceptualOrigin NOT_EQUAL LexicalSense",
        "LexicalSense NOT_EQUAL ContextualSenseCandidate",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_99_declares_ingestion_pipeline_and_auto_agreed_boundary() -> None:
    _declare("ingestion and status boundary")
    body = _DOC_99.read_text(encoding="utf-8")

    required_markers = (
        "HTML Entry",
        "-> RawImportedEntry",
        "-> StructuralValidation",
        "-> ReadingCandidateSet",
        "-> RootIdentityCandidate",
        "-> SourceClaimCandidate",
        "-> Human/Rule Review",
        "-> LicensedLexicalRecord",
        "`AUTO_AGREED` is extraction agreement only.",
        "`HUMAN_VERIFIED`",
        "`CONSTITUTIONALLY_LICENSED`",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_99_declares_residual_rank_and_lexical_license_boundary() -> None:
    _declare("residual/rank/license boundary")
    body = _DOC_99.read_text(encoding="utf-8")

    required_markers = (
        "OCR_UNCERTAIN",
        "ROOT_BOUNDARY_UNCERTAIN",
        "LEXEME_ROOT_CONFLICT",
        "CONTRADICTORY",
        "CROSS_SOURCE_SUPPORTED",
        "CONSTITUTIONALLY_LICENSED",
        "LexicalLicense(x)=1 iff",
        "AND NoBlockingResidual(x)",
        "AND Rank >= MinimumLexicalRank",
        "LexicalMadlulCandidate",
        "CompositionReadiness",
        "IfadahCandidate",
        "HukmCandidate",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_99_continuity_with_docs_81_82_89() -> None:
    _declare("continuity with upstream boundaries")
    body = _DOC_99.read_text(encoding="utf-8")

    assert "Continuity with docs/81" in body
    assert "Continuity with docs/82" in body
    assert "Continuity with docs/89" in body

    assert "LEX_DATA_1_ALLOWED_OUTPUTS" in _DOC_81.read_text(encoding="utf-8")
    assert "Wad'iMadlulLicensed DOES_NOT_IMPLY NaqliMadlulLicensed" in _DOC_82.read_text(
        encoding="utf-8"
    )
    assert "LexemeContractabilityReadiness" in _DOC_89.read_text(encoding="utf-8")
