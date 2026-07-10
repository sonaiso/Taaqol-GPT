"""Acceptance tests for docs/86 — Isolated Noun Identity Readiness Law.

Origin law     : docs/86 (NOUN-L0)
Branch         : NOUN-L0 (law-only isolated noun-identity readiness boundary)
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
_DOC_86 = _REPO_ROOT / "docs" / "86_NOUN_IDENTITY_READINESS_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/86_NOUN_IDENTITY_READINESS_LAW.md",
        branch_name=f"NOUN-L0 ({branch_note})",
        constitutional_chain=("docs/86", "NOUN-L0"),
        chain_position="NOUN-L0 law-only isolated noun identity-readiness boundary",
        origin_law_ref="docs/86_NOUN_IDENTITY_READINESS_LAW.md#1-governing-law",
        branch_of_origin=(
            "Law-only boundary: isolated noun may open identity-readiness surfaces only "
            "and does not produce certificate/meaning/ifadah/hukm/truth."
        ),
        forbidden_shortcut_assertions=(
            "IsolatedNoun -> FinalMeaning",
            "NounReadiness -> Ifadah",
            "NounReadiness -> Hukm",
            "NounReadiness -> Truth",
            "LexicalWitness -> NounTruth",
            "WadiReadiness -> Naql/Majaz",
            "MabniCandidate -> ReferenceResolved",
            "ZarfReadiness -> MafulFihFinal",
            "RelativeReadiness -> ReferenceResolved",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "NounIdentityCertificate",
            "FinalMeaning",
            "ContextualMeaning",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "FinalSyntacticRole",
            "ReferenceResolved",
            "FinalReferenceCertificate",
            "NaqliMadlulLicensed_without_NaqlGate",
            "MajaziMadlulLicensed_without_MajazGate",
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


def test_docs_86_noun_exists_and_declares_identity() -> None:
    _declare("document presence and branch identity")
    assert _DOC_86.exists(), "docs/86 NOUN law must exist"
    body = _DOC_86.read_text(encoding="utf-8")

    for marker in (
        "86 — Isolated Noun Identity Readiness Law (NOUN-L0)",
        "FAMILY               = NOUN",
        "STEP                 = NOUN-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = ISOLATED_NOUN_IDENTITY_READINESS",
    ):
        assert marker in body


def test_docs_86_noun_declares_non_implication_core() -> None:
    _declare("governing non-implication boundary")
    body = _DOC_86.read_text(encoding="utf-8")

    for marker in (
        "IsolatedNoun DOES_NOT_IMPLY FinalMeaning",
        "NounIdentityReadinessCandidate DOES_NOT_IMPLY Ifadah",
        "NounIdentityReadinessCandidate DOES_NOT_IMPLY Hukm",
        "NounIdentityReadinessCandidate DOES_NOT_IMPLY Truth",
        "WadiReadinessCandidate DOES_NOT_IMPLY Naql/Majaz",
        "MabniCandidate DOES_NOT_IMPLY FinalReference",
        "No NounIdentityCertificate",
    ):
        assert marker in body


def test_docs_86_noun_declares_allowed_and_forbidden_outputs() -> None:
    _declare("allowed and forbidden outputs")
    body = _DOC_86.read_text(encoding="utf-8")

    for marker in (
        "NounIdentityReadinessCandidate",
        "DalSurfaceReadiness",
        "LafziReadiness",
        "WadiReadinessCandidate",
        "MabniPathCandidate",
        "MurabPathCandidate",
        "GenderNumberReadiness",
        "DefinitenessReadiness",
        "CompositionReadinessCandidate",
        "LexicalWitnessCandidate",
        "ReferenceDemandSurface",
        "AdverbialReadinessCandidate",
        "RelativeNounReadiness",
        "DemonstrativeReadiness",
        "NounIdentityCertificate",
        "FinalMeaning",
        "Ifadah",
        "Hukm",
        "Truth",
        "FinalSyntacticRole",
        "ReferenceResolved",
        "NaqliMadlulLicensed_without_NaqlGate",
        "MajaziMadlulLicensed_without_MajazGate",
    ):
        assert marker in body


def test_docs_86_noun_declares_shortcuts_mrk_and_residuals() -> None:
    _declare("shortcut discipline, MRK, and local residuals")
    body = _DOC_86.read_text(encoding="utf-8")

    for marker in (
        "IsolatedNoun -> FinalMeaning",
        "NounReadiness -> Ifadah",
        "NounReadiness -> Hukm",
        "NounReadiness -> Truth",
        "LexicalWitness -> NounTruth",
        "WadiReadiness -> Naql/Majaz",
        "MabniCandidate -> ReferenceResolved",
        "ZarfReadiness -> MafulFihFinal",
        "RelativeReadiness -> ReferenceResolved",
        "MRK(NounReadiness)",
        "SurfaceIdentity",
        "NounFamily",
        "MabniMurabPathStatus",
        "NumberGenderDefinitenessReadiness",
        "LexicalWitnessStatus",
        "CompositionDemandSurface",
        "TraceRef",
        "VisibleResiduals",
        "ForbiddenOutputs",
        "NOUN_SURFACE_IDENTITY_INCOMPLETE",
        "NOUN_FAMILY_AMBIGUOUS",
        "MABNI_MURAB_PATH_AMBIGUOUS",
        "NUMBER_GENDER_PENDING",
        "DEFINITENESS_PENDING",
        "LEXICAL_WITNESS_MISSING",
        "LEXICAL_WITNESS_AMBIGUOUS",
        "SENSE_AMBIGUITY_VISIBLE",
        "COMPOSITION_DEMAND_OPEN",
        "REFERENCE_DEMAND_UNRESOLVED",
        "NAQL_GATE_REQUIRED",
        "MAJAZ_GATE_REQUIRED",
    ):
        assert marker in body


def test_docs_86_noun_declares_boundaries_embargo_and_sequence() -> None:
    _declare("integration boundaries, embargo, and safe sequence")
    body = _DOC_86.read_text(encoding="utf-8")

    for marker in (
        "No duplication of LEX-DATA-1",
        "No duplication of LEX-BOUNDARY-L0",
        "No duplication of MABNI-L0",
        "No duplication of ZARF-L0",
        "No duplication of REF-PRON-L0",
        "RUNTIME_NOT_OPENED = {",
        "parser_changes",
        "morphology_runtime",
        "syntax_authority",
        "semantic_runtime",
        "ifadah_engine",
        "hukm_engine",
        "truth_engine",
        "noun_identity_gate_runtime",
        "noun_identity_certificate_runtime",
        "naql_gate_runtime",
        "majaz_gate_runtime",
        "NOUN-L0",
        "EvidenceFitnessCarrier",
        "TraceReplayVerifier",
        "RankVector/DomainPolicy",
        "NOUN-C1",
        "NOUN-G1",
    ):
        assert marker in body


def test_docs_86_noun_contains_constitutional_examples() -> None:
    _declare("minimum constitutional examples")
    body = _DOC_86.read_text(encoding="utf-8")

    for marker in (
        'Input: "جبل"',
        (
            "Output: NounIdentityReadinessCandidate LICENSED + WadiReadinessCandidate + "
            "CompositionReadinessCandidate"
        ),
        "Forbidden: FinalMeaning / Truth / Hukm",
        'Input: "هذا"',
        "Output: MabniPathCandidate LICENSED + DemonstrativeReadiness + ReferenceDemandSurface",
        "Forbidden: ReferenceResolved / FinalMeaning",
        'Input: "عين"',
        "Residuals: SENSE_AMBIGUITY_VISIBLE",
        "Forbidden: SenseResolved / Truth",
        'Input: "مساء"',
        "Output: NounIdentityReadinessCandidate LICENSED + AdverbialReadinessCandidate",
        "Forbidden: MafulFihFinal before composition",
        'Input: "الذي"',
        (
            "Output: RelativeNounReadiness LICENSED + ReferenceDemandSurface + "
            "CompositionReadinessCandidate"
        ),
        "Forbidden: ReferenceResolved / Ifadah",
    ):
        assert marker in body
