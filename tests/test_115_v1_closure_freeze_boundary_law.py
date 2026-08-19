"""Acceptance tests for docs/115 — V1 Closure Freeze Boundary Law.

Origin law     : docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md
Branch         : V1-L0 (law-only closure/freeze governance appendix)
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
_DOC_115 = _REPO_ROOT / "docs" / "115_V1_CLOSURE_FREEZE_BOUNDARY_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md",
        branch_name=f"V1-L0 law-only closure/freeze governance ({branch_note})",
        constitutional_chain=("docs/53", "Z0-M2-current", "V1-L0", "docs/115"),
        chain_position="V1-L0 independent law-only closure/freeze governance appendix step",
        origin_law_ref="docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md",
        branch_of_origin=(
            "Bounded V1 closure law that distinguishes constitutional invariants "
            "from performance KPIs and enforces explicit defer-out records."
        ),
        forbidden_shortcut_assertions=(
            "ResearchRemaining -> V1Incomplete",
            "DeferredOutOfV1 -> HiddenResidual",
            "ClosureDeclaration -> RuntimeOpening",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "AuthorityLeakClaim",
            "TruthRealityClosureClaim",
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


def test_docs_115_exists_and_declares_law_only_boundary() -> None:
    _declare("document boundary")
    body = _DOC_115.read_text(encoding="utf-8")

    assert _DOC_115.exists()
    assert "V1 Closure Freeze Boundary Law" in body
    assert "Constitutional law document (law-only)." in body
    assert "RUNTIME_NOT_OPENED = {" in body


def test_docs_115_declares_closure_predicate_and_guards() -> None:
    _declare("closure predicate")
    body = _DOC_115.read_text(encoding="utf-8")

    required_markers = (
        "V1Closed",
        "AllDeclaredV1Obligations",
        "PROVEN",
        "REFUSED",
        "DEFERRED_OUT_OF_V1",
        "NoBlockingResidual",
        "NoHiddenObligation",
        "NoUnauthorizedTransition",
        r"ResearchRemaining\neq V1Incomplete",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_115_declares_invariants_defer_contract_and_freeze_rule() -> None:
    _declare("invariants/defer/freeze")
    body = _DOC_115.read_text(encoding="utf-8")

    required_markers = (
        "SafetyInvariant\\neq PerformanceKPI.",
        "FutureResearchRecord=",
        "WhyNotRequiredForV1",
        "NoAuthorityImpact",
        "FutureEntryCondition",
        "DeferredOutOfV1 \\neq HiddenResidual.",
        "V1ClosureFreezeMode",
        "Contradiction",
        "UndefinedRequiredPrimitive",
        "UnlicensedTransition",
        "FalseClosure",
        "CoverageBlockingGap",
    )
    for marker in required_markers:
        assert marker in body


def test_docs_115_declares_v1_matrix_and_dashboard_markers() -> None:
    _declare("matrix/dashboard")
    body = _DOC_115.read_text(encoding="utf-8")

    required_markers = (
        "| 44 | V1 launch gate | aggregate closure gates | `PASS` |",
        "GCR = GlossaryClosureRate",
        "TCR = TransitionClosureRate",
        "DCR = DomainContractRate",
        "MCR = MethodContractRate",
        "PCR = ProofCoverageRate",
        "RTR = RealityReturnCoverage",
        "RLR = ResidualLossRate",
        "ALR = AuthorityLeakRate",
        "FSR = FalseRefusalRate",
        "CDR = ConstitutionalDriftRate",
    )
    for marker in required_markers:
        assert marker in body


def test_roadmap_registers_amendment_89_v1_l0_without_runtime_displacement() -> None:
    _declare("roadmap amendment record")
    roadmap = _DOC_14.read_text(encoding="utf-8")

    assert "Amendment-89 (V1-L0 — V1 Closure Freeze Boundary Law)" in roadmap
    assert "without displacing Z0-M2 as the current runtime-hardening step." in roadmap


def test_docs_index_references_docs_115() -> None:
    _declare("docs index mapping")
    index_body = _DOCS_INDEX.read_text(encoding="utf-8")
    assert "115_V1_CLOSURE_FREEZE_BOUNDARY_LAW.md" in index_body

