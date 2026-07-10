"""Acceptance tests for docs/89 — PRECOMP-L0 law-only boundary.

Origin law     : docs/89 (PRECOMP-L0)
Branch         : PRECOMP-L0 (law-only pre-composition verification and contractability)
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
_DOC_89 = _REPO_ROOT / "docs" / "89_PRECOMPOSITION_VERIFICATION_CONTRACTABILITY_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/89_PRECOMPOSITION_VERIFICATION_CONTRACTABILITY_LAW.md",
        branch_name=f"PRECOMP-L0 ({branch_note})",
        constitutional_chain=("docs/89", "PRECOMP-L0"),
        chain_position=(
            "PRECOMP-L0 law-only pre-composition verification and "
            "contractability boundary"
        ),
        origin_law_ref="docs/89_PRECOMPOSITION_VERIFICATION_CONTRACTABILITY_LAW.md#1-governing-law",
        branch_of_origin=(
            "Law-only boundary: pre-composition verification produces contractability "
            "readiness only and does not produce final syntax/meaning/ifadah/hukm/truth."
        ),
        forbidden_shortcut_assertions=(
            "AtomicUnit -> DerivationFinal",
            "AtomicUnit -> SyntaxFinal",
            "AtomicUnit -> WadiMeaning",
            "PathCandidate -> FinalPathCertificate",
            "LexemeContractabilityReadiness -> FinalMeaning",
            "LexemeContractabilityReadiness -> FinalSyntax",
            "CompositionPreconditionCandidate -> Ifadah",
            "CompositionPreconditionCandidate -> Hukm",
            "CompositionPreconditionCandidate -> Truth",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "AtomicMeaning",
            "FinalWordMeaning",
            "FinalMeaning",
            "FinalSyntax",
            "FinalSyntacticRole",
            "FinalSyntacticSlot",
            "NounIdentityCertificate",
            "VerbIdentityCertificate",
            "ParticleIdentityCertificate",
            "ReferenceResolved",
            "FinalRelation",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
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


def test_docs_89_exists_and_declares_identity() -> None:
    _declare("document presence and branch identity")
    assert _DOC_89.exists(), "docs/89 PRECOMP law must exist"
    body = _DOC_89.read_text(encoding="utf-8")

    for marker in (
        "89 — Pre-Composition Verification and Contractability Law (PRECOMP-L0)",
        "FAMILY               = PRECOMPOSITION",
        "STEP                 = PRECOMP-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = PRECOMPOSITION_VERIFICATION_AND_CONTRACTABILITY",
    ):
        assert marker in body


def test_docs_89_declares_non_implication_core() -> None:
    _declare("governing non-implication boundary")
    body = _DOC_89.read_text(encoding="utf-8")

    for marker in (
        "No Composition Before Verification.",
        "Verification before composition yields ContractabilityReadiness only.",
        "ContractabilityReadiness DOES_NOT_IMPLY FinalSyntax.",
        "ContractabilityReadiness DOES_NOT_IMPLY FinalMeaning.",
        "ContractabilityReadiness DOES_NOT_IMPLY Ifadah.",
        "ContractabilityReadiness DOES_NOT_IMPLY Hukm.",
        "ContractabilityReadiness DOES_NOT_IMPLY Truth.",
        "AtomicSurfaceReadiness DOES_NOT_IMPLY DerivationFinal.",
        "AtomicSurfaceReadiness DOES_NOT_IMPLY SyntaxFinal.",
        "AtomicSurfaceReadiness DOES_NOT_IMPLY WadiMeaning.",
        (
            "Any transition from readiness/candidate naming to final closure naming "
            "at PRECOMP-L0 is a FORBIDDEN_LEAP."
        ),
    ):
        assert marker in body


def test_docs_89_declares_layers_atomic_rules_and_neighbors() -> None:
    _declare("layer model and neighbor continuity")
    body = _DOC_89.read_text(encoding="utf-8")

    for marker in (
        "A0: Atomic Surface Verification",
        "A1: Word Surface Verification",
        "A2: Path Readiness Verification",
        "A3: Lexeme Contractability Verification",
        "A4: Composition Precondition Verification",
        "AtomicUnit -> AtomicSurfaceReadiness",
        "AtomicUnit -> Derivation + Syntax + Wadi",
        "PHONETIC_TENSION_VISIBLE is residual-visible, not automatic failure.",
        "PASS_WITH_RESIDUAL is admissible where hard prohibition is absent.",
        "Atomic rank remains SurfaceReadiness",
        "NOUN-L0",
        "VERB-L0",
        "LGE-LINK-L0",
        "REF-PRON-L0",
        "MABNI-L0",
        "ZARF-L0",
        "LEX-DATA-1",
        "LEX-BOUNDARY-L0",
    ):
        assert marker in body


def test_docs_89_declares_allowed_forbidden_and_embargo() -> None:
    _declare("allowed outputs, forbidden outputs, and runtime embargo")
    body = _DOC_89.read_text(encoding="utf-8")

    for marker in (
        "AtomicSurfaceReadiness",
        "WordSurfaceReadinessCandidate",
        "PathReadinessCandidate",
        "LexemeContractabilityReadiness",
        "SlotEligibilityCandidate",
        "CompositionPreconditionCandidate",
        "PreCompositionAuditResult",
        "AtomicMeaning",
        "FinalMeaning",
        "FinalSyntax",
        "Ifadah",
        "Hukm",
        "Truth",
        "RUNTIME_NOT_OPENED = {",
        "precomp_verifier_runtime",
        "parser_changes",
        "morphology_runtime",
        "syntax_authority",
        "semantic_runtime",
        "ifadah_engine",
        "hukm_engine",
        "truth_engine",
        "PRECOMP-C1 carrier surface",
        "PRECOMP-G1 verifier gates",
        "PRECOMP-T1 stress fixtures",
    ):
        assert marker in body


def test_docs_89_declares_checklist_and_examples() -> None:
    _declare("checklist and constitutional examples")
    body = _DOC_89.read_text(encoding="utf-8")

    for marker in (
        "PRECOMP-L0 CHECKLIST",
        "Atomic units verified?",
        "Word surface verified?",
        "Path candidates declared?",
        "Neighbor laws respected?",
        "Contractability declared?",
        "Composition precondition satisfied?",
        "Forbidden outputs absent?",
        '"unit": "بَ"',
        '"unit": "ضِ"',
        '"status": "PASS_WITH_RESIDUAL"',
        '"residuals": ["PHONETIC_TENSION_VISIBLE"]',
        '"surface": "كتب"',
        '"residuals": ["UNVOCALIZED_SURFACE_RESIDUAL"]',
        '"surface": "جبل"',
        '"surface": "ضرب"',
        '"surface": "من"',
        '"residuals": ["MABNI_FAMILY_AMBIGUOUS"]',
        '"surface": "ضرب زيد"',
        '"residuals": ["LINK_OPERATOR_TRIAD_PARTIAL_OR_IMPLICIT"]',
    ):
        assert marker in body
