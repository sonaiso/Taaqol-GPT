"""Acceptance tests for docs/97 — TGovA condensation law.

Origin law     : docs/90_REBUILT_CONSTITUTIONAL_GOVERNANCE_ARCHITECTURE.md
Branch         : PR-138 law-only condensation and theorem formalization
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
_DOC_97 = _REPO_ROOT / "docs" / "97_THEORY_OF_GOVERNED_ACTS_CONDENSATION_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/90_REBUILT_CONSTITUTIONAL_GOVERNANCE_ARCHITECTURE.md",
        branch_name=f"PR-138 TGovA condensation ({branch_note})",
        constitutional_chain=("docs/90", "PR-138", "docs/97"),
        chain_position="PR-138 law-only condensation and theorem surface lock",
        origin_law_ref="docs/90_REBUILT_CONSTITUTIONAL_GOVERNANCE_ARCHITECTURE.md",
        branch_of_origin=(
            "Condenses governed-acts constitutional clauses and fixes theorem "
            "surface before runtime binding/refactor PRs."
        ),
        forbidden_shortcut_assertions=(
            "PR-138 -> src_runtime_mutation",
            "PR-138 -> global_failure_taxonomy_expansion",
            "PR-138 -> executor_guardian_runtime_merge",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeMutationClaim",
            "SemanticOpeningClaim",
            "SelfLicensingExecutorClaim",
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


def test_docs_97_exists_and_declares_law_only_scope() -> None:
    _declare("document presence")
    body = _DOC_97.read_text(encoding="utf-8")
    for marker in (
        "Status:",
        "Law-only",
        "PR-138",
        "without opening runtime",
    ):
        assert marker in body


def test_docs_97_declares_q1_to_q7_condensed_laws() -> None:
    _declare("Q-law condensation surface")
    body = _DOC_97.read_text(encoding="utf-8")
    for marker in (
        "Q1: Separation Law",
        "Q2: Contract Law",
        "Q3: Identity Law",
        "Q4: Rank Law",
        "Q5: Residual Law",
        "Q6: Evidence Law",
        "Q7: Multiplicity Law",
    ):
        assert marker in body


def test_docs_97_declares_20_to_7_mapping() -> None:
    _declare("20→7 mapping")
    body = _DOC_97.read_text(encoding="utf-8")
    for marker in (
        "Q1 ← {1,2,3,4,16}",
        "Q2 ← {5,6,17}",
        "Q3 ← {8,18}",
        "Q4 ← {9,19}",
        "Q5 ← {10}",
        "Q6 ← {11,14,15}",
        "Q7 ← {12,13}",
    ):
        assert marker in body


def test_docs_97_declares_formal_theorems_t1_t3() -> None:
    _declare("formal theorem surface")
    body = _DOC_97.read_text(encoding="utf-8")
    for marker in (
        "T1 (No self-approval): ¬∃E: Executor(E) ∧ CanSelfApprove(E)",
        "T2 (No unlicensed jump): ∀i,j: Transition(L_i, L_j) ∧ j > i+1 ⇒ "
        "∃G: LicensedGate(G, L_i, L_j)",
        "T3 (Rank boundedness): ∀o: Rank(o) ≤ min(Rank(input(o)), "
        "Rank(evidence(o)), Rank(closure(o)))",
    ):
        assert marker in body


def test_docs_97_declares_order_pr_140_then_pr_139() -> None:
    _declare("post-condensation sequencing")
    body = _DOC_97.read_text(encoding="utf-8")
    assert "1. `PR-140`" in body
    assert "2. `PR-139`" in body


def test_docs_97_declares_forbidden_surface_and_local_residuals() -> None:
    _declare("forbidden surface and residual vocabulary")
    body = _DOC_97.read_text(encoding="utf-8")
    for marker in (
        "FORBIDDEN_LEAP",
        "mutate `src/taaqqul_slot_geometry/**`",
        "CONDENSATION_MAPPING_INCOMPLETE",
        "THEOREM_SURFACE_UNDECLARED",
        "SELF_APPROVAL_SURFACE_LEAK",
        "UNLICENSED_JUMP_SURFACE_LEAK",
        "RANK_BOUND_SURFACE_MISSING",
    ):
        assert marker in body


def test_docs_index_references_docs_97() -> None:
    _declare("docs index mapping")
    index_body = _DOCS_INDEX.read_text(encoding="utf-8")
    assert "97_THEORY_OF_GOVERNED_ACTS_CONDENSATION_LAW.md" in index_body
