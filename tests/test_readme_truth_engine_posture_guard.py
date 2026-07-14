"""README Truth Engine posture guard tests.

Origin law     : docs/53 (Project Methodology, Objectives, and KPI Plan)
Branch         : CLOSE-2 hardening (README posture guard)
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

_README = Path(__file__).resolve().parent.parent / "README.md"


def _read_readme() -> str:
    return _README.read_text(encoding="utf-8")


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md",
        branch_name=f"README Truth Engine posture guard ({branch_note})",
        constitutional_chain=("CLOSE-2", "README", "PostureGuard"),
        chain_position="README public posture hardening",
        origin_law_ref="docs/53_PROJECT_METHODOLOGY_OBJECTIVES_AND_KPI_PLAN.md#14-truth-engine-first-experiment-posture",
        branch_of_origin=(
            "Public README wording guard aligned with docs/53 bounded "
            "Truth Engine posture and docs/91 execution-gap classification."
        ),
        forbidden_shortcut_assertions=(
            "GovernancePass -> ExternalTruth",
            "CertificateRank -> ExternalTruth",
            "ExecutionGapMatrix -> CompleteTruthEngine",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "CompleteTruthEngineClaim",
            "UniversalTruthEngineClaim",
            "GovernancePassProvesRealityClaim",
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


def test_readme_truth_engine_posture_is_bounded() -> None:
    _declare("required guard clauses")
    content = _read_readme()
    required_clauses = [
        "first bounded Truth Engine experiment",
        "not a universal truth engine",
        "Passing governance gates does not prove reality",
        "certificate rank does not imply external truth",
        "Truth requires correspondence and evidence",
        "docs/53",
        "docs/91",
        "execution-gap matrix",
    ]
    for clause in required_clauses:
        assert clause in content, (
            f"README must include bounded Truth Engine posture clause: '{clause}'"
        )


def test_readme_truth_engine_totalizing_claims_absent() -> None:
    _declare("forbidden totalizing clauses")
    content = _read_readme().lower()
    forbidden_clauses = [
        "project is now a complete truth engine",
        "all produced knowledge is true",
        "passing governance gates proves reality",
        "is a universal truth engine",
    ]
    for clause in forbidden_clauses:
        assert clause not in content, (
            f"README must not include forbidden totalizing claim: '{clause}'"
        )
