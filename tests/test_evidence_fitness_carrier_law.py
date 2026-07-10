"""Acceptance tests for docs/88 — Evidence Fitness Carrier Boundary Law.

Origin law     : docs/88 (EVID-FIT-L0)
Branch         : EVID-FIT-L0 (law-only shared evidence-fitness carrier boundary)
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
_DOC_88 = _REPO_ROOT / "docs" / "88_EVIDENCE_FITNESS_CARRIER_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/88_EVIDENCE_FITNESS_CARRIER_LAW.md",
        branch_name=f"EVID-FIT-L0 ({branch_note})",
        constitutional_chain=("docs/88", "EVID-FIT-L0"),
        chain_position="EVID-FIT-L0 law-only shared evidence-fitness carrier boundary",
        origin_law_ref="docs/88_EVIDENCE_FITNESS_CARRIER_LAW.md#1-governing-law",
        branch_of_origin=(
            "Law-only boundary: shared evidence-fitness carrier may package readiness only "
            "and does not produce certificate/inference/ifadah/hukm/truth."
        ),
        forbidden_shortcut_assertions=(
            "EvidenceFitnessCarrier -> EvidenceFitnessCertificate",
            "EvidenceFitnessCarrier -> RuntimeInferenceVerdict",
            "EvidenceFitnessCarrier -> Ifadah",
            "EvidenceFitnessCarrier -> Hukm",
            "EvidenceFitnessCarrier -> Truth",
            "VerbReadiness -> EventTruth via EvidenceFitnessCarrier",
            "NounReadiness -> FinalMeaning via EvidenceFitnessCarrier",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "EvidenceFitnessCertificate",
            "RuntimeInferenceVerdict",
            "FinalEventMeaning",
            "FinalMeaning",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "FinalSyntacticRole",
            "FinalSourceCertificate",
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


def test_docs_88_exists_and_declares_identity() -> None:
    _declare("document presence and branch identity")
    assert _DOC_88.exists(), "docs/88 EvidenceFitness law must exist"
    body = _DOC_88.read_text(encoding="utf-8")

    for marker in (
        "88 — Evidence Fitness Carrier Boundary Law (EVID-FIT-L0)",
        "FAMILY               = EVIDENCE_FITNESS",
        "STEP                 = EVID-FIT-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = SHARED_PRE_VERIFIER_EVIDENCE_FITNESS",
    ):
        assert marker in body


def test_docs_88_declares_non_implication_core() -> None:
    _declare("governing non-implication boundary")
    body = _DOC_88.read_text(encoding="utf-8")

    for marker in (
        "EvidenceFitnessCarrier DOES_NOT_IMPLY EvidenceFitnessCertificate",
        "EvidenceFitnessCarrier DOES_NOT_IMPLY Ifadah",
        "EvidenceFitnessCarrier DOES_NOT_IMPLY Hukm",
        "EvidenceFitnessCarrier DOES_NOT_IMPLY Truth",
        "EvidenceFitnessCarrier DOES_NOT_IMPLY RuntimeInference",
        "VerbIdentityReadinessCandidate THROUGH EvidenceFitnessCarrier DOES_NOT_IMPLY EventTruth",
        "NounIdentityReadinessCandidate THROUGH EvidenceFitnessCarrier DOES_NOT_IMPLY FinalMeaning",
        "No EvidenceFitnessCertificate",
        (
            "Any transition from carrier/readiness naming to certificate or "
            "runtime inference at EVID-FIT-L0 is a FORBIDDEN_LEAP."
        ),
    ):
        assert marker in body


def test_docs_88_declares_allowed_and_forbidden_outputs() -> None:
    _declare("allowed and forbidden outputs")
    body = _DOC_88.read_text(encoding="utf-8")

    for marker in (
        "EvidenceFitnessCarrier",
        "EvidenceSurfaceRef",
        "UpstreamReadinessRef",
        "DomainScopeRef",
        "RankCeilingRef",
        "ResidualVisibilityRef",
        "TraceReplayDemandSurface",
        "RankPolicyDemandSurface",
        "PolicyPreconditionSurface",
        "EvidenceFitnessCertificate",
        "RuntimeInferenceVerdict",
        "Ifadah",
        "Hukm",
        "Truth",
        "FinalSyntacticRole",
    ):
        assert marker in body


def test_docs_88_declares_shortcuts_mrk_and_residuals() -> None:
    _declare("shortcut discipline, MRK, and local residuals")
    body = _DOC_88.read_text(encoding="utf-8")

    for marker in (
        "EvidenceFitnessCarrier -> EvidenceFitnessCertificate",
        "EvidenceFitnessCarrier -> RuntimeInferenceVerdict",
        "EvidenceFitnessCarrier -> Ifadah",
        "EvidenceFitnessCarrier -> Hukm",
        "EvidenceFitnessCarrier -> Truth",
        "VerbReadiness -> EventTruth via EvidenceFitnessCarrier",
        "NounReadiness -> FinalMeaning via EvidenceFitnessCarrier",
        "MRK(EvidenceFitnessCarrier)",
        "CarrierIdentity",
        "EvidenceSurfaceRef",
        "UpstreamReadinessRef",
        "DomainScopeRef",
        "RankCeilingRef",
        "ResidualVisibilityRef",
        "TraceReplayDemandSurface",
        "RankPolicyDemandSurface",
        "ForbiddenOutputs",
        "TraceRef",
        "EVIDENCE_SURFACE_MISSING",
        "UPSTREAM_READINESS_MISSING",
        "TRACE_REF_MISSING",
        "RANK_CEILING_UNDECLARED",
        "DOMAIN_SCOPE_UNDECLARED",
        "RESIDUAL_VISIBILITY_MISSING",
        "CERTIFICATE_JUMP_BLOCKED",
        "INFERENCE_JUMP_BLOCKED",
        "TRUTH_CLOSURE_BLOCKED",
        "IFADAH_HUKM_CLOSURE_BLOCKED",
    ):
        assert marker in body


def test_docs_88_declares_runtime_embargo_and_sequence() -> None:
    _declare("runtime embargo and sequence")
    body = _DOC_88.read_text(encoding="utf-8")

    for marker in (
        "RUNTIME_NOT_OPENED = {",
        "parser_changes",
        "morphology_runtime",
        "syntax_authority",
        "semantic_runtime",
        "ifadah_engine",
        "hukm_engine",
        "truth_engine",
        "evidence_fitness_verifier_runtime",
        "evidence_fitness_certificate_runtime",
        "runtime_inference_engine",
        "NOUN-L0 / VERB-L0 / REF-PRON-L0 / ZARF-L0 / LGE-LINK-L0",
        "-> EvidenceFitnessCarrier",
        "-> TraceReplayVerifier",
        "-> RankVector/DomainPolicy",
        "-> Branch-specific carrier/runtime steps (for example VERB-C1)",
    ):
        assert marker in body


def test_docs_88_contains_constitutional_examples() -> None:
    _declare("minimum constitutional examples")
    body = _DOC_88.read_text(encoding="utf-8")

    for marker in (
        'Input: VerbIdentityReadinessCandidate("ضرب")',
        (
            "Output: EvidenceFitnessCarrier LICENSED + TraceReplayDemandSurface + "
            "RankPolicyDemandSurface"
        ),
        "Forbidden: EvidenceFitnessCertificate / EventTruth / Ifadah / Hukm / Truth",
        'Input: NounIdentityReadinessCandidate("جبل")',
        "Output: EvidenceFitnessCarrier LICENSED + DomainScopeRef + ResidualVisibilityRef",
        "Forbidden: FinalMeaning / RuntimeInferenceVerdict",
        "Input: EvidenceFitnessCarrier(without TraceRef)",
        "Output: EvidenceFitnessCarrier remains pending with TRACE_REF_MISSING",
        "Forbidden: EvidenceFitnessCertificate",
    ):
        assert marker in body
