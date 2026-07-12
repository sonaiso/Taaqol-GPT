"""Constitutional surface tests for docs/90 governor/proof contract hardening.

Origin law          : docs/13_CONSTITUTIONAL_PR_GEOMETRY.md
Branch name         : DOC90-HARDENING-R3
Constitutional chain: docs/12 -> docs/13 -> docs/90
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOC_90 = _REPO_ROOT / "docs" / "90_REBUILT_CONSTITUTIONAL_GOVERNANCE_ARCHITECTURE.md"

_REQUIRED_MARKERS = (
    "PreflightResult =",
    "Permit",
    "PreflightRejected",
    "PreflightSuspended",
    "NoPermit => NoEffectfulExecution",
    "NoApprovedPostflight => NoCommit",
    "StageExecute:",
    "Permit x InputSnapshot -> ExecutionCandidate",
    "class PreflightDecision(str, Enum):",
    "class PostflightDecision(str, Enum):",
    "class CommitState(str, Enum):",
    "class ArtifactLifecycle(str, Enum):",
    "MatchingPermit(x)",
    "PermitAuthentic(x)",
    "PermitUnconsumed(x)",
    "PermitUnexpired(x)",
    "RelevantSnapshotUnchanged(x)",
    "IdentityObligationsSatisfied(x)",
    "NoBlockingResidual(x)",
    "ProofDerivationSubgraph H",
    "AllRequiredPremisesActive(H)",
    "NoDefeatingDifference(H, c)",
    "RankCeiling(H) >= RequiredRank(c)",
    "ResidualCategory:",
    "ResidualDisposition:",
    "ReferenceSufficiencyForProposition",
    "Every output has provenance/execution origin.",
    "Every committed epistemic claim has evidentiary support.",
    "No approved epistemic output without proof/dependency graph.",
    "MaqamConstraint = CandidateFilter + CompatibilityEvidence + ScopeConstraint + "
    "SelectionPreference",
    "Maqam cannot directly promote rank outside gate discipline.",
    "MufradMadlulCandidate",
    "STABLE | SUSPENDED | CONTRADICTORY | LIMIT_REACHED",
)

_FORBIDDEN_MARKERS = (
    "TransitionResult =\nGovernorPostflight(",
    "EngineExecute(\n    GovernorPreflight(",
    "class DecisionState(str, Enum):",
    "residual_type: str",
    "blocking_status: str",
    "rank_impact: str",
    "_governor_token: object",
    "there exists p such that:",
    "Rank(path) = min Rank(node_i) on that path.",
    "ReferenceResolution",
    "No output without proof graph.",
    "MaqamConstraint = Filter + RankAdjustment + SelectionPressure",
    "Carrier -> Form -> Path -> Root/Stem -> Weight -> Lexeme -> Anchors",
    "Relation -> Coupling -> MaqamConstraint -> Ifadah -> Mantuq -> DerivedDalalah",
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/13_CONSTITUTIONAL_PR_GEOMETRY.md",
        branch_name=f"DOC90-HARDENING-R3 ({branch_note})",
        constitutional_chain=("docs/12", "docs/13", "docs/90"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "RatificationClaim",
            "ChainMutationClaim",
            "ScopeCollapseClaim",
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


def test_docs_90_contains_required_hardening_markers() -> None:
    _declare("required constitutional markers")
    body = _DOC_90.read_text(encoding="utf-8")
    for marker in _REQUIRED_MARKERS:
        assert marker in body, f"docs/90 missing required marker: {marker}"


def test_docs_90_excludes_regressed_forbidden_markers() -> None:
    _declare("forbidden regression markers")
    body = _DOC_90.read_text(encoding="utf-8")
    for marker in _FORBIDDEN_MARKERS:
        assert marker not in body, f"docs/90 still contains forbidden marker: {marker}"
