"""Acceptance tests for docs/87 — Isolated Verb Identity Readiness Law.

Origin law     : docs/87 (VERB-L0)
Branch         : VERB-L0 (law-only isolated verb-identity readiness boundary)
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
_DOC_87 = _REPO_ROOT / "docs" / "87_VERB_IDENTITY_READINESS_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/87_VERB_IDENTITY_READINESS_LAW.md",
        branch_name=f"VERB-L0 ({branch_note})",
        constitutional_chain=("docs/87", "VERB-L0"),
        chain_position="VERB-L0 law-only isolated verb identity-readiness boundary",
        origin_law_ref="docs/87_VERB_IDENTITY_READINESS_LAW.md#1-governing-law",
        branch_of_origin=(
            "Law-only boundary: isolated verb may open readiness demands only "
            "and does not produce certificate/meaning/ifadah/hukm/truth."
        ),
        forbidden_shortcut_assertions=(
            "VerbSurface -> EventTruth",
            "PastForm -> ExternalPastEvent",
            "ImperativeForm -> CommandJudgment",
            "TransitivityReadiness -> FinalObjecthood",
            "VerbOntologyDemand -> SubjectCompatibilityFinal",
            "SourceReadiness -> FinalSourceCertificate",
            "VerbReadiness -> Ifadah",
            "VerbReadiness -> Hukm",
            "VerbReadiness -> Truth",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "VerbIdentityCertificate",
            "FinalEventMeaning",
            "FinalSourceCertificate",
            "ExternalPastEvent",
            "FinalTransitivityCertificate",
            "FinalSyntacticRole",
            "SubjectCompatibilityFinal",
            "ObjectSlotFinal",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "CommandJudgment",
            "ObligationJudgment",
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


def test_docs_87_verb_exists_and_declares_identity() -> None:
    _declare("document presence and branch identity")
    assert _DOC_87.exists(), "docs/87 VERB law must exist"
    body = _DOC_87.read_text(encoding="utf-8")

    for marker in (
        "87 — Isolated Verb Identity Readiness Law (VERB-L0)",
        "FAMILY               = VERB",
        "STEP                 = VERB-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = ISOLATED_VERB_IDENTITY_READINESS",
    ):
        assert marker in body


def test_docs_87_verb_declares_non_implication_core() -> None:
    _declare("governing non-implication boundary")
    body = _DOC_87.read_text(encoding="utf-8")

    for marker in (
        "VerbSurface DOES_NOT_IMPLY EventTruth",
        "VerbIdentityReadinessCandidate DOES_NOT_IMPLY Ifadah",
        "VerbIdentityReadinessCandidate DOES_NOT_IMPLY Hukm",
        "VerbIdentityReadinessCandidate DOES_NOT_IMPLY Truth",
        "PastForm DOES_NOT_IMPLY ExternalPastEvent",
        "ImperativeForm DOES_NOT_IMPLY CommandJudgment",
        "TransitivityReadiness DOES_NOT_IMPLY FinalObjectSlots",
        "VerbOntologyDemand DOES_NOT_IMPLY SubjectCompatibilityFinal",
        "No VerbIdentityCertificate",
    ):
        assert marker in body


def test_docs_87_verb_declares_allowed_and_forbidden_outputs() -> None:
    _declare("allowed and forbidden outputs")
    body = _DOC_87.read_text(encoding="utf-8")

    for marker in (
        "VerbIdentityReadinessCandidate",
        "SourceReadinessCandidate",
        "TenseFormCandidate",
        "PastFormCandidate",
        "PresentFormCandidate",
        "ImperativeFormCandidate",
        "TransitivityReadinessCandidate",
        "ObjectDemandSurface",
        "SubjectDemandSurface",
        "ModeDemandSurface",
        "MaqamDemandSurface",
        "VerbOntologyDemandSurface",
        "AttachedPronounDemandSurface",
        "AdverbialDemandSurface",
        "PrepositionalTransitivityDemand",
        "CompositionReadinessCandidate",
        "VerbIdentityCertificate",
        "FinalEventMeaning",
        "FinalSourceCertificate",
        "ExternalPastEvent",
        "FinalTransitivityCertificate",
        "FinalSyntacticRole",
        "SubjectCompatibilityFinal",
        "ObjectSlotFinal",
        "Ifadah",
        "Hukm",
        "Truth",
        "CommandJudgment",
        "ObligationJudgment",
    ):
        assert marker in body


def test_docs_87_verb_declares_shortcuts_mrk_and_residuals() -> None:
    _declare("shortcut discipline, MRK, and local residuals")
    body = _DOC_87.read_text(encoding="utf-8")

    for marker in (
        "VerbSurface -> EventTruth",
        "PastForm -> ExternalPastEvent",
        "ImperativeForm -> CommandJudgment",
        "TransitivityReadiness -> FinalObjecthood",
        "VerbOntologyDemand -> SubjectCompatibilityFinal",
        "SourceReadiness -> FinalSourceCertificate",
        "VerbReadiness -> Ifadah",
        "VerbReadiness -> Hukm",
        "VerbReadiness -> Truth",
        "MRK(VerbReadiness)",
        "SurfaceIdentity",
        "VerbFormFamily",
        "SourceReadiness",
        "TenseForm",
        "SubjectDemand",
        "TransitivityReadiness",
        "ModeMaqamDemand",
        "OntologyDemand",
        "TraceRef",
        "VisibleResiduals",
        "ForbiddenOutputs",
        "SOURCE_EVIDENCE_MISSING",
        "SOURCE_PATTERN_AMBIGUOUS",
        "TENSE_FORM_AMBIGUOUS",
        "PAST_FORM_NOT_REAL_EVENT",
        "PRESENT_MODE_PENDING",
        "IMPERATIVE_ADDRESSEE_REQUIRED",
        "SUBJECT_DEMAND_UNFILLED",
        "OBJECT_DEMAND_UNFILLED",
        "TRANSITIVITY_ALTERNATION_VISIBLE",
        "PREPOSITIONAL_GOVERNANCE_PENDING",
        "ONTOLOGICAL_SUBJECT_COMPATIBILITY_PENDING",
        "RATIONAL_AGENT_REQUIRED",
        "MAQAM_CONTEXT_REQUIRED",
        "VERB_FORM_MABNI_MURAB_AMBIGUITY",
        "COMMAND_FORCE_NOT_HUKM",
    ):
        assert marker in body


def test_docs_87_verb_declares_boundaries_embargo_and_sequence() -> None:
    _declare("integration boundaries, embargo, and safe sequence")
    body = _DOC_87.read_text(encoding="utf-8")

    for marker in (
        "No duplication of NOUN-L0",
        "No duplication of REF-PRON-L0",
        "No duplication of LGE-LINK-L0",
        "No duplication of LEX-DATA-1 and LEX-BOUNDARY-L0",
        "No duplication of ZARF-L0",
        "RUNTIME_NOT_OPENED = {",
        "parser_changes",
        "morphology_runtime",
        "syntax_authority",
        "semantic_runtime",
        "ifadah_engine",
        "hukm_engine",
        "truth_engine",
        "verb_identity_gate_runtime",
        "verb_identity_certificate_runtime",
        "transitivity_gate_runtime",
        "source_gate_runtime",
        "mode_gate_runtime",
        "VERB-L0",
        "EvidenceFitnessCarrier",
        "TraceReplayVerifier",
        "RankVector/DomainPolicy",
        "VERB-C1",
        "VERB-G1",
    ):
        assert marker in body


def test_docs_87_verb_contains_constitutional_examples() -> None:
    _declare("minimum constitutional examples")
    body = _DOC_87.read_text(encoding="utf-8")

    for marker in (
        'Input: "ضرب"',
        (
            "Output: PastFormCandidate LICENSED + SourceReadinessCandidate + "
            "TransitivityReadinessCandidate + SubjectDemandSurface + ObjectDemandSurface"
        ),
        "Forbidden: ExternalPastEvent / FinalObjecthood / Ifadah / Truth",
        'Input: "ذهب"',
        (
            "Output: PastFormCandidate LICENSED + TransitivityReadinessCandidate + "
            "SubjectDemandSurface"
        ),
        "Residuals: PREPOSITIONAL_GOVERNANCE_PENDING",
        "Forbidden: FinalTransitivityCertificate",
        'Input: "يكتب"',
        (
            "Output: PresentFormCandidate LICENSED + ModeDemandSurface + SubjectDemandSurface + "
            "ObjectDemandSurface"
        ),
        "Forbidden: PresentRealityTruth",
        'Input: "اكتب"',
        "Output: ImperativeFormCandidate LICENSED + MaqamDemandSurface + SubjectDemandSurface",
        "Residuals: IMPERATIVE_ADDRESSEE_REQUIRED + COMMAND_FORCE_NOT_HUKM",
        "Forbidden: CommandJudgment / ObligationJudgment / Truth",
        'Input: "قال"',
        "Output: VerbOntologyDemandSurface LICENSED + RATIONAL_AGENT_REQUIRED",
        "Forbidden: SubjectCompatibilityFinal",
        'Input: "أمطر"',
        (
            "Output: VerbIdentityReadinessCandidate LICENSED + VerbOntologyDemandSurface + "
            "SubjectDemandSurface"
        ),
        "Forbidden: WeatherTruth / Reality",
    ):
        assert marker in body
