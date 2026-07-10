"""Acceptance tests for docs/84 — Built-Form Surface Geometry Law.

Origin law     : docs/84 (MABNI-L0)
Branch         : MABNI-L0 (law-only built-form surface boundary)
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
_DOC_84 = _REPO_ROOT / "docs" / "84_MABNI_SURFACE_GEOMETRY_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/84_MABNI_SURFACE_GEOMETRY_LAW.md",
        branch_name=f"MABNI-L0 ({branch_note})",
        constitutional_chain=("docs/84", "MABNI-L0"),
        chain_position="MABNI-L0 law-only built-form surface boundary",
        origin_law_ref="docs/84_MABNI_SURFACE_GEOMETRY_LAW.md#1-governing-law",
        branch_of_origin=(
            "Law-only boundary: mabni forms open demand surfaces and do not "
            "produce final meaning/ifadah/hukm/truth."
        ),
        forbidden_shortcut_assertions=(
            "MabniSurface -> FinalMeaning",
            "MawsulCandidate -> ReferenceResolved",
            "IsharaCandidate -> ExternalReferent",
            "IstifhamCandidate -> Answer",
            "NidaCandidate -> FinalReferenceCertificate",
            "TaajjubCandidate -> Truth",
            "MabniCandidate -> Ifadah",
            "MabniCandidate -> Hukm",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "FinalMeaning",
            "ContextualMeaning",
            "ReferenceResolved",
            "FinalReferenceCertificate",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "SyntacticAuthority",
            "SemanticClosure",
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


def test_docs_84_mabni_exists_and_declares_identity() -> None:
    _declare("document presence and branch identity")
    assert _DOC_84.exists(), "docs/84 MABNI law must exist"
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "84 — Built-Form Surface Geometry Law (MABNI-L0)",
        "FAMILY               = MABNI",
        "STEP                 = MABNI-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = MABNI_SURFACE_GEOMETRY",
    ):
        assert marker in body


def test_docs_84_mabni_declares_non_implication_core() -> None:
    _declare("governing non-implication boundary")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "MabniSurface DOES_NOT_IMPLY FinalMeaning",
        "MabniSurface DOES_NOT_IMPLY Ifadah",
        "MabniSurface DOES_NOT_IMPLY Hukm",
        "MabniSurface DOES_NOT_IMPLY Truth",
        "ContractReadinessCandidate DOES_NOT_IMPLY FinalReferenceCertificate",
    ):
        assert marker in body


def test_docs_84_mabni_declares_allowed_and_forbidden_output_surfaces() -> None:
    _declare("allowed and forbidden outputs")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "MabniCandidate",
        "MawsulCandidate",
        "IsharaCandidate",
        "IstifhamCandidate",
        "NidaCandidate",
        "TaajjubCandidate",
        "FunctionalDemandSurface",
        "ReferenceDemandSurface",
        "QuestionDemandSurface",
        "VocativeDemandSurface",
        "ExclamativeStyleSurface",
        "ContractReadinessCandidate",
        "FinalMeaning",
        "ContextualMeaning",
        "ReferenceResolved",
        "FinalReferenceCertificate",
        "Ifadah",
        "Hukm",
        "Truth",
        "Certainty",
        "Reality",
        "SyntacticAuthority",
        "SemanticClosure",
    ):
        assert marker in body


def test_docs_84_mabni_declares_forbidden_shortcuts_and_scope_non_duplication() -> None:
    _declare("forbidden shortcuts and anti-duplication")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "MabniSurface -> FinalMeaning",
        "MawsulCandidate -> ReferenceResolved",
        "IsharaCandidate -> ExternalReferent",
        "IstifhamCandidate -> Answer",
        "NidaCandidate -> FinalReferenceCertificate",
        "TaajjubCandidate -> Truth",
        "MabniCandidate -> Ifadah",
        "MabniCandidate -> Hukm",
        "No duplication of REF-PRON-L0",
        "No duplication of LGE-LINK-L0",
        "No duplication of LEX-DATA",
        "No duplication of LEX-BOUNDARY-L0",
    ):
        assert marker in body


def test_docs_84_mabni_declares_mrk_runtime_embargo_and_safe_sequence() -> None:
    _declare("mrk, embargo, and safe sequencing")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "MRK(MabniCandidate)",
        "BuiltFormIdentity",
        "BuiltFormFamily",
        "DemandSurfaceType",
        "ScopeOrAnchorDemand",
        "MaqamContextNeed",
        "ResidualVisibility",
        "TraceRef",
        "ForbiddenOutputs",
        "RUNTIME_NOT_OPENED = {",
        "reference_resolver_runtime",
        "semantic_runtime",
        "ifadah_engine",
        "hukm_engine",
        "truth_engine",
        "new_rank_engine",
        "external_grounding_api",
        "MABNI-L0",
        "EvidenceFitnessCarrier",
        "TraceReplayVerifier",
        "RankVector/DomainPolicy",
        "MABNI-C1",
    ):
        assert marker in body


def test_docs_84_mabni_contains_five_minimum_constitutional_examples() -> None:
    _declare("five minimum examples")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        'Input: "الذي"',
        "Output: MawsulCandidate LICENSED + SilaDemandSurface",
        "Forbidden: ReferenceResolved / Ifadah / Hukm / Truth",
        'Input: "هذا"',
        "Output: IsharaCandidate LICENSED + DeicticDemandSurface",
        "Forbidden: ExternalReferent without Maqam/Context",
        'Input: "أين"',
        "Output: IstifhamCandidate LICENSED + ExpectedAnswerSlot",
        "Forbidden: Answer / Hukm / Truth",
        'Input: "يا زيد"',
        "Output: NidaCandidate LICENSED + VocativeDemandSurface",
        "Forbidden: FinalReferenceCertificate",
        'Input: "ما أجمل السماء"',
        "Output: TaajjubCandidate LICENSED + ExclamativeStyleSurface",
        "Forbidden: FinalAttributeJudgment / Truth",
    ):
        assert marker in body
