"""Acceptance tests for docs/94 — AUX-ESA-0 boundary law.

Origin law     : docs/93 + docs/94
Branch         : AUX-ESA-0 (law-only quarantine boundary)
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
_DOC_93 = _REPO_ROOT / "docs" / "93_AUX_ESA_0_POST_MERGE_AUDIT.md"
_DOC_94 = _REPO_ROOT / "docs" / "94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/93_AUX_ESA_0_POST_MERGE_AUDIT.md + "
            "docs/94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md"
        ),
        branch_name=f"AUX-ESA-0 ({branch_note})",
        constitutional_chain=("docs/93", "docs/94", "AUX-ESA-0-LAW"),
        chain_position="AUX-ESA-0 law-only quarantine boundary",
        origin_law_ref="docs/94_AUX_ESA_0_ENRICHED_SIMULATION_AGENT_BOUNDARY_LAW.md#2-governing-boundary-equation",
        branch_of_origin=(
            "Law-only auxiliary quarantine boundary that prevents roadmap/runtime/bridge "
            "openings from enriched_simulation_agent."
        ),
        forbidden_shortcut_assertions=(
            "AUX_ESA_0 -> docs/14_chain_unlock",
            "AUX_ESA_0 -> linguistic_to_knowledge_bridge_proof",
            "AUX_ESA_0 -> WordCapability_to_Ifadah",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "ConstitutionalAdmissionCertificate",
            "RoadmapAdvanceClaim",
            "BridgeLicensedClaim",
            "RelationUnlockedByAux",
            "IfadahUnlockedByAux",
            "HukmUnlockedByAux",
            "GlobalConstitutionalVerdict",
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


def test_docs_94_exists_and_declares_law_only_quarantine() -> None:
    _declare("document existence and law-only identity")
    body = _DOC_94.read_text(encoding="utf-8")

    assert _DOC_94.exists()
    assert "Status: constitutional boundary law document (law-only)." in body
    assert "AUXILIARY_KERNEL_ONLY" in body
    assert "QUARANTINED_FROM_CONSTITUTIONAL_CHAIN_RUNTIME" in body


def test_docs_94_declares_governing_boundary_equation_terms() -> None:
    _declare("boundary equation")
    body = _DOC_94.read_text(encoding="utf-8")

    required_terms = (
        "AUX_ESA_0_BOUNDARY_EQUATION :=",
        "ROADMAP_UNLOCK = FORBIDDEN_AND_NOT_PRESENT",
        "CORE_RUNTIME_MUTATION = FORBIDDEN_AND_NOT_PRESENT",
        "LINGUISTIC_TO_KNOWLEDGE_BRIDGE = FORBIDDEN_AND_NOT_PRESENT",
        "WORDCAPABILITY_TO_RELATION_IFADAH_HUKM = FORBIDDEN_AND_NOT_PRESENT",
        "CONSTITUTIONAL_HARNESS_ADMISSION = NOT_PRESENT",
    )
    for term in required_terms:
        assert term in body


def test_docs_94_forbids_unlocks_and_declares_runtime_embargo() -> None:
    _declare("forbidden unlocks and runtime embargo")
    body = _DOC_94.read_text(encoding="utf-8")

    required_markers = (
        "AUX_ESA_0 -> docs/14_chain_unlock",
        "AUX_ESA_0 -> core_runtime_mutation",
        "AUX_ESA_0 -> linguistic_to_knowledge_bridge_proof",
        "AUX_ESA_0 -> WordCapability_to_Relation",
        "AUX_ESA_0 -> WordCapability_to_Ifadah",
        "AUX_ESA_0 -> WordCapability_to_Hukm",
        "RUNTIME_NOT_OPENED = {",
        "src/taaqqul_slot_geometry/**",
        "docs/14 chain mutation",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_94_declares_rank_residual_and_deferred_law_obligations() -> None:
    _declare("rank residual and deferred obligations")
    body = _DOC_94.read_text(encoding="utf-8")

    for token in (
        "MAX_RANK_FOR_AUX_LAW_STEP = ZERO",
        "RESIDUAL_VISIBILITY = REQUIRED",
        "HIDDEN_RESIDUALS_ON_APPROVAL = FORBIDDEN",
        "DEFAULT_FAILURE_CODE_ON_BOUNDARY_BREACH = UNLICENSED_OPENING",
        "IdentitySimulationLaw",
        "CompositionSimulationLaw",
        "OperationHomomorphismLaw",
        "ResidualReflectionLaw",
        "CoverageContractLaw",
        "NonTrivialityStrengtheningLaw",
    ):
        assert token in body


def test_docs_93_to_docs_94_trace_continuity() -> None:
    _declare("trace continuity")
    doc_93_body = _DOC_93.read_text(encoding="utf-8")
    doc_94_body = _DOC_94.read_text(encoding="utf-8")

    assert "next_permitted_action: AUX_BOUNDARY_LAW_AND_ADMISSION_PATH_ONLY" in doc_93_body
    assert "Trace path:" in doc_94_body
    assert "`docs/13` -> `docs/14` -> `docs/93` -> `docs/94`." in doc_94_body
