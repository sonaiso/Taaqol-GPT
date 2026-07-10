"""Acceptance tests for docs/85 — Isolated Lexeme Adverbial Readiness Law.

Origin law     : docs/85 (ZARF-L0)
Branch         : ZARF-L0 (law-only isolated adverbial readiness boundary)
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
_DOC_85 = _REPO_ROOT / "docs" / "85_ZARF_ISOLATED_LEXEME_ADVERBIAL_READINESS_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/85_ZARF_ISOLATED_LEXEME_ADVERBIAL_READINESS_LAW.md",
        branch_name=f"ZARF-L0 ({branch_note})",
        constitutional_chain=("docs/85", "ZARF-L0"),
        chain_position="ZARF-L0 law-only isolated adverbial-readiness boundary",
        origin_law_ref=(
            "docs/85_ZARF_ISOLATED_LEXEME_ADVERBIAL_READINESS_LAW.md#1-governing-law"
        ),
        branch_of_origin=(
            "Law-only boundary: isolated lexeme may open adverbial readiness only "
            "and does not produce MafulFihFinal/final syntactic role/ifadah/hukm/truth."
        ),
        forbidden_shortcut_assertions=(
            "IsolatedLexeme -> MafulFihFinal",
            "ZarfReadiness -> FinalSyntacticRole",
            "BuiltZarf -> Ifadah",
            "TimePlaceLexeme -> Truth",
            "Weight -> ZarfFinal",
            "LexicalAttestation -> AdverbialTruth",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "MafulFihFinal",
            "FinalSyntacticRole",
            "FinalRelation",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "ExternalTemporalFact",
            "ExternalSpatialFact",
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


def test_docs_85_zarf_exists_and_declares_identity() -> None:
    _declare("document presence and branch identity")
    assert _DOC_85.exists(), "docs/85 ZARF law must exist"
    body = _DOC_85.read_text(encoding="utf-8")

    for marker in (
        "85 — Isolated Lexeme Adverbial Readiness Law (ZARF-L0)",
        "FAMILY               = ZARF",
        "STEP                 = ZARF-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = ISOLATED_ADVERBIAL_READINESS",
    ):
        assert marker in body


def test_docs_85_zarf_declares_non_implication_core() -> None:
    _declare("governing non-implication boundary")
    body = _DOC_85.read_text(encoding="utf-8")

    for marker in (
        "IsolatedLexeme DOES_NOT_IMPLY MafulFihFinal",
        "AdverbialReadinessCandidate DOES_NOT_IMPLY FinalSyntacticRole",
        "AdverbialReadinessCandidate DOES_NOT_IMPLY Ifadah",
        "AdverbialReadinessCandidate DOES_NOT_IMPLY Hukm",
        "AdverbialReadinessCandidate DOES_NOT_IMPLY Truth",
    ):
        assert marker in body


def test_docs_85_zarf_declares_allowed_and_forbidden_outputs() -> None:
    _declare("allowed and forbidden outputs")
    body = _DOC_85.read_text(encoding="utf-8")

    for marker in (
        "AdverbialReadinessCandidate",
        "TimeAdverbCandidate",
        "PlaceAdverbCandidate",
        "TimePlaceAmbivalentCandidate",
        "BuiltZarfCandidate",
        "MutasarrifZarfCandidate",
        "NonMutasarrifZarfCandidate",
        "AttachmentDemandSurface",
        "FactorDemandSurface",
        "CompositionReadinessCandidate",
        "MafulFihFinal",
        "FinalSyntacticRole",
        "FinalRelation",
        "Ifadah",
        "Hukm",
        "Truth",
        "Certainty",
        "Reality",
        "ExternalTemporalFact",
        "ExternalSpatialFact",
    ):
        assert marker in body


def test_docs_85_zarf_declares_shortcuts_mrk_and_residuals() -> None:
    _declare("shortcut discipline, MRK, and local residuals")
    body = _DOC_85.read_text(encoding="utf-8")

    for marker in (
        "IsolatedLexeme -> MafulFihFinal",
        "ZarfReadiness -> FinalSyntacticRole",
        "BuiltZarf -> Ifadah",
        "TimePlaceLexeme -> Truth",
        "Weight -> ZarfFinal",
        "LexicalAttestation -> AdverbialTruth",
        "MRK(ZarfReadiness)",
        "LexemeIdentity",
        "TimePlaceFamily",
        "MutasarrifOrNonMutasarrifStatus",
        "MabniOrMurabSurface",
        "EvidenceSource",
        "ExpectedAttachmentDemand",
        "ExpectedFactorDemand",
        "TraceRef",
        "VisibleResiduals",
        "ForbiddenOutputs",
        "ADVERBIAL_EVIDENCE_MISSING",
        "TIME_PLACE_AMBIGUITY",
        "MABNI_STATUS_AMBIGUOUS",
        "MUTASARRIF_STATUS_PENDING",
        "FACTOR_REQUIRED",
        "ATTACHMENT_REQUIRED",
        "IDAFHA_COMPLEMENT_REQUIRED",
        "LEXICAL_POLYSEMY_VISIBLE",
        "WEIGHT_ONLY_NOT_SUFFICIENT",
        "CONTEXT_REQUIRED_FOR_ADVERBIAL_ROLE",
    ):
        assert marker in body


def test_docs_85_zarf_declares_boundary_integration_embargo_and_sequence() -> None:
    _declare("integration boundaries, embargo, and safe sequence")
    body = _DOC_85.read_text(encoding="utf-8")

    for marker in (
        "No duplication of MABNI-L0",
        "No duplication of LGE-LINK-L0",
        "MabniStatus != ZarfReadiness",
        "LinkOperator != ZarfCandidate",
        "RUNTIME_NOT_OPENED = {",
        "parser_changes",
        "morphology_runtime",
        "syntax_authority",
        "semantic_runtime",
        "ifadah_engine",
        "hukm_engine",
        "truth_engine",
        "new_rank_engine",
        "external_grounding_api",
        "ZARF-L0",
        "EvidenceFitnessCarrier",
        "TraceReplayVerifier",
        "RankVector/DomainPolicy",
        "ZARF-C1",
        "ZARF-G1",
        "ZARF-T1",
    ):
        assert marker in body


def test_docs_85_zarf_contains_constitutional_examples() -> None:
    _declare("minimum constitutional examples")
    body = _DOC_85.read_text(encoding="utf-8")

    for marker in (
        'Input: "مساء"',
        "Output: TimeAdverbCandidate LICENSED + FactorDemandSurface + AttachmentDemandSurface",
        "Forbidden: MafulFihFinal / Ifadah / Hukm / Truth",
        'Input: "حيث"',
        "Output: BuiltZarfCandidate LICENSED + AttachmentDemandSurface",
        "Residuals: ATTACHMENT_REQUIRED + CONTEXT_REQUIRED_FOR_ADVERBIAL_ROLE",
        "Forbidden: FinalRelation / Ifadah / Hukm / Truth",
        'Input: "عند"',
        "Output: PlaceAdverbCandidate LICENSED + IDAFHA_COMPLEMENT_REQUIRED",
        "Forbidden: MafulFihFinal before composition",
    ):
        assert marker in body
