"""Acceptance tests for docs/83 — Pronoun Reference Surface Geometry Law.

Origin law     : docs/83 (REF-PRON-L0)
Branch         : REF-PRON-L0 (law-only pronoun reference boundary)
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
_DOC_83 = _REPO_ROOT / "docs" / "83_PRONOUN_REFERENCE_SURFACE_GEOMETRY_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/83_PRONOUN_REFERENCE_SURFACE_GEOMETRY_LAW.md",
        branch_name=f"REF-PRON-L0 ({branch_note})",
        constitutional_chain=("docs/83", "REF-PRON-L0"),
        chain_position="REF-PRON-L0 law-only pronoun-reference surface boundary",
        origin_law_ref="docs/83_PRONOUN_REFERENCE_SURFACE_GEOMETRY_LAW.md#1-governing-law",
        branch_of_origin=(
            "Law-only boundary: pronouns open reference-demand surface and do not "
            "produce final reference/ifadah/hukm/truth."
        ),
        forbidden_shortcut_assertions=(
            "PronounSurface -> ReferenceResolved",
            "PronounSurface -> Ifadah",
            "PronounSurface -> Hukm",
            "PronounSurface -> Truth",
            "PronounCandidate -> FinalReferenceCertificate",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ReferenceResolved",
            "FinalReferenceCertificate",
            "FinalMeaning",
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


def test_docs_83_pron_exists_and_declares_ref_pron_identity() -> None:
    _declare("document presence and identity")
    assert _DOC_83.exists(), "docs/83 pronoun law must exist"
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "83 — Pronoun Reference Surface Geometry Law (REF-PRON-L0)",
        "FAMILY               = REF-PRON",
        "STEP                 = REF-PRON-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = PRONOUN_REFERENCE_SURFACE_GEOMETRY",
    ):
        assert marker in body


def test_docs_83_pron_declares_non_implication_core() -> None:
    _declare("governing non-implication boundary")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "PronounSurface DOES_NOT_IMPLY ReferenceResolved",
        "PronounSurface DOES_NOT_IMPLY Ifadah",
        "PronounSurface DOES_NOT_IMPLY Hukm",
        "PronounSurface DOES_NOT_IMPLY Truth",
        "ContractReadiness DOES_NOT_IMPLY FinalReferenceCertificate",
    ):
        assert marker in body


def test_docs_83_pron_declares_mrk_and_residual_vocabulary() -> None:
    _declare("mrk and local residual discipline")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "MRK(PronounCandidate)",
        "PronounIdentity",
        "PronounClass",
        "AttachmentMode",
        "PersonNumberGenderFeatures",
        "HostOrAntecedentDemand",
        "CaseRoleReadinessSurface",
        "ReferenceSearchDomain",
        "VisibleResiduals",
        "TraceRef",
        "ForbiddenOutputs",
        "ANTECEDENT_MISSING",
        "ANTECEDENT_AMBIGUOUS",
        "HOST_MISSING",
        "ATTACHMENT_TYPE_AMBIGUOUS",
        "PERSON_NUMBER_GENDER_MISMATCH",
        "CASE_ROLE_PENDING",
        "MAQAM_CONTEXT_REQUIRED",
        "REFERENCE_DOMAIN_UNDECLARED",
        "TRACE_REF_MISSING",
    ):
        assert marker in body


def test_docs_83_pron_declares_detached_and_attached_pronoun_classes() -> None:
    _declare("detached and attached pronoun classes")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "DetachedPronounCandidate",
        "AttachedPronounCandidate",
        "VerbAttachedPronoun",
        "NounAttachedPronoun",
        "ParticleAttachedPronoun",
        "AttachedPronoun DOES_NOT_IMPLY FinalReference",
        "AttachedPronoun DOES_NOT_IMPLY SyntacticRoleFinal",
        "AttachedPronoun DOES_NOT_IMPLY Ifadah",
    ):
        assert marker in body


def test_docs_83_pron_constitutional_examples_cover_required_inputs() -> None:
    _declare("constitutional examples for required cases")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        'Input: "هو"',
        "Residual: ANTECEDENT_MISSING or MAQAM_CONTEXT_REQUIRED",
        "Forbidden: ReferenceResolved",
        'Input: "جاء زيد ثم سلّم عليه"',
        "Residual (if unresolved in this layer): ANTECEDENT_AMBIGUOUS or REFERENCE_SEARCH_REQUIRED",
        "Forbidden: FinalReferenceCertificate",
        'Input: "كتابه"',
        "NounAttachedPronoun LICENSED + IdafaReadinessCandidate",
        "Forbidden: FinalOwnershipMeaning",
        'Input: "ضربته"',
        "VerbAttachedPronoun LICENSED + RoleReadinessCandidate",
        "Forbidden: FinalObjecthood / SyntacticAuthority",
    ):
        assert marker in body


def test_docs_83_pron_declares_runtime_embargo_and_safe_staging() -> None:
    _declare("runtime embargo and safe staging")
    body = _DOC_83.read_text(encoding="utf-8")

    for marker in (
        "RUNTIME_NOT_OPENED = {",
        "reference_resolver_runtime",
        "semantic_runtime",
        "ifadah_engine",
        "hukm_engine",
        "truth_engine",
        "global_rank_engine",
        "external_grounding_api",
        "EvidenceFitnessCarrier",
        "TraceReplayVerifier",
        "RankVector/DomainPolicy",
        "REF-PRON-C1",
        "REF-PRON-G1",
        "REF-PRON-T1",
    ):
        assert marker in body
