"""Acceptance tests for docs/84 — Built-Form Surface Registry Boundary Law.

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
            "Law-only boundary: mabni forms open demand/readiness surfaces and do not "
            "produce final meaning/ifadah/hukm/truth/syntactic authority."
        ),
        forbidden_shortcut_assertions=(
            "MabniSurface -> FinalMeaning",
            "DemonstrativeCandidate -> ReferenceResolved",
            "RelativeNounCandidate -> ReferenceResolved",
            "InterrogativeCandidate -> Answer",
            "ConditionalNameCandidate -> Hukm",
            "VerbNounCandidate -> VerbRuntimeMeaning",
            "CompoundNumberCandidate -> QuantitativeTruth",
            "BuiltAdverbCandidate -> MafulFihFinal",
            "VocativeBuiltCaseCandidate -> FinalReferenceCertificate",
            "LaNafiyaBuiltCaseCandidate -> ExistentialTruth",
            "MabniCandidate -> SyntacticAuthority",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "FinalMeaning",
            "ContextualMeaning",
            "ReferenceResolved",
            "FinalReferenceCertificate",
            "FinalSyntacticRole",
            "SyntacticAuthority",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
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


def test_docs_84_mabni_exists_and_declares_identity() -> None:
    _declare("document presence and branch identity")
    assert _DOC_84.exists(), "docs/84 MABNI law must exist"
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "84 — Built-Form Surface Registry Boundary Law (MABNI-L0)",
        "FAMILY               = MABNI",
        "STEP                 = MABNI-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = MABNI_SURFACE_REGISTRY",
    ):
        assert marker in body


def test_docs_84_mabni_declares_corrected_golden_rule_and_non_implication_core() -> None:
    _declare("governing non-implication boundary")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "MabniSurface DOES_NOT_IMPLY FinalMeaning",
        "MabniSurface DOES_NOT_IMPLY Ifadah",
        "MabniSurface DOES_NOT_IMPLY Hukm",
        "MabniSurface DOES_NOT_IMPLY Truth",
        "MabniCandidate DOES_NOT_IMPLY SyntacticAuthority",
        "MabniCandidate path must be tested before Weight/Derivation closure for that token.",
        (
            "This rule is token-scoped. It does not require closing all built forms in Arabic "
            "before any"
        ),
    ):
        assert marker in body


def test_docs_84_mabni_declares_allowed_and_forbidden_output_surfaces() -> None:
    _declare("allowed and forbidden outputs")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "MabniCandidate",
        "DemonstrativeCandidate",
        "RelativeNounCandidate",
        "InterrogativeCandidate",
        "ConditionalNameCandidate",
        "VerbNounCandidate",
        "CompoundNumberCandidate",
        "BuiltAdverbCandidate",
        "VocativeBuiltCaseCandidate",
        "LaNafiyaBuiltCaseCandidate",
        "FunctionalDemandSurface",
        "ReferenceDemandSurface",
        "QuestionDemandSurface",
        "ConditionDemandSurface",
        "VocativeDemandSurface",
        "ExclamativeStyleSurface",
        "CompositionReadinessCandidate",
        "FinalMeaning",
        "ContextualMeaning",
        "ReferenceResolved",
        "FinalReferenceCertificate",
        "FinalSyntacticRole",
        "SyntacticAuthority",
        "Ifadah",
        "Hukm",
        "Truth",
        "Certainty",
        "Reality",
        "NaqliMadlulLicensed_without_NaqlGate",
        "MajaziMadlulLicensed_without_MajazGate",
    ):
        assert marker in body


def test_docs_84_mabni_declares_families_exceptions_and_residuals() -> None:
    _declare("families, exceptions, and residual discipline")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "Demonstratives (`هذا`, `هذه`",
        "Relatives (`الذي`, `التي`",
        "Interrogatives (`من`, `ما`, `أين`",
        "Condition names (`من`, `ما`, `مهما`",
        "Verb-nouns (`هيهات`, `شتان`",
        "Compound numbers (`أحد عشر`",
        "Built adverbs (`أمس`, `حيث`, `إذ`",
        "Vocative built case (e.g., `يا خالدُ`, `يا رجلُ`)",
        "La-nafiya built case (e.g., `لا رجلَ`)",
        "هذان / هاتان are dual i'rab exceptions",
        "اللذان / اللتان are dual i'rab exceptions",
        "أيّ is a mu'rab exception",
        "اثنا عشر / اثنتا عشرة are i'rab exceptions",
        "MABNI_FAMILY_AMBIGUOUS",
        "DUAL_EXCEPTION_REQUIRES_IRAB_DISCIPLINE",
        "AYY_MURAB_EXCEPTION",
        "WEIGHT_PATH_BLOCKED_BY_MABNI_CANDIDATE",
    ):
        assert marker in body


def test_docs_84_mabni_declares_forbidden_shortcuts_and_scope_non_duplication() -> None:
    _declare("forbidden shortcuts and anti-duplication")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "MabniSurface -> FinalMeaning",
        "DemonstrativeCandidate -> ReferenceResolved",
        "RelativeNounCandidate -> ReferenceResolved",
        "InterrogativeCandidate -> Answer",
        "ConditionalNameCandidate -> Hukm",
        "VerbNounCandidate -> VerbRuntimeMeaning",
        "CompoundNumberCandidate -> QuantitativeTruth",
        "BuiltAdverbCandidate -> MafulFihFinal",
        "VocativeBuiltCaseCandidate -> FinalReferenceCertificate",
        "LaNafiyaBuiltCaseCandidate -> ExistentialTruth",
        "MabniCandidate -> SyntacticAuthority",
        "No duplication of REF-PRON-L0",
        "No duplication of LGE-LINK-L0",
        "No duplication of LEX-DATA-1",
        "No duplication of LEX-BOUNDARY-L0",
        "No duplication of ZARF-L0",
    ):
        assert marker in body


def test_docs_84_mabni_declares_mrk_runtime_embargo_and_safe_sequence() -> None:
    _declare("mrk, embargo, and safe sequencing")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        "MRK(MabniCandidate)",
        "surface_identity",
        "built_family",
        "subfamily",
        "exception_status",
        "functional_or_reference_demand",
        "required_attachment_or_context",
        "trace_ref",
        "visible_residuals",
        "forbidden_outputs",
        "RUNTIME_NOT_OPENED = {",
        "executable_registry_runtime",
        "reference_resolver_runtime",
        "semantic_runtime",
        "ifadah_engine",
        "hukm_engine",
        "truth_engine",
        "new_rank_engine",
        "external_grounding_api",
        "MABNI-L0 (law-only)",
        "EvidenceFitnessCarrier",
        "TraceReplayVerifier",
        "RankVector/DomainPolicy",
        "MABNI-C1 carrier surface",
        "MABNI-G1 gates",
        "MABNI-T1 stress fixtures",
    ):
        assert marker in body


def test_docs_84_mabni_contains_nine_minimum_constitutional_examples() -> None:
    _declare("minimum examples")
    body = _DOC_84.read_text(encoding="utf-8")

    for marker in (
        'Input: "هذا"',
        "Allowed: DemonstrativeCandidate",
        "Required: DeicticDemandSurface",
        'Input: "الذي"',
        "Allowed: RelativeNounCandidate",
        "Required: SilaDemandSurface",
        'Input: "أين"',
        "Allowed: InterrogativeCandidate",
        "Required: ExpectedAnswerSlot",
        'Input: "من"',
        "Expected: MABNI_FAMILY_AMBIGUOUS",
        "Possible families: Interrogative / Conditional / Relative",
        'Input: "هيهات"',
        "Allowed: VerbNounCandidate",
        'Input: "أحد عشر"',
        "Allowed: CompoundNumberCandidate",
        'Input: "أمس"',
        "Allowed: BuiltAdverbCandidate",
        "Residual: ADVERBIAL_ATTACHMENT_REQUIRED",
        'Input: "يا خالدُ"',
        "Allowed: VocativeBuiltCaseCandidate",
        'Input: "لا رجلَ"',
        "Allowed: LaNafiyaBuiltCaseCandidate",
    ):
        assert marker in body
