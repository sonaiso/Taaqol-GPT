"""Constitutional tests for PR-B canonical domain registry surface.

Origin law     : docs/14 (PR-B registration) + docs/101 (registry boundary)
Branch         : PR-B Canonical Domain Registry
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r.canonical_domain_registry import (
    CanonicalDomainRegistry,
    CanonicalDomainRegistrySchemaError,
    CarrierKind,
    DomainId,
    RankChannel,
    ResidualKind,
    TransitionKind,
    canonical_domain_registry,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_101 = _REPO_ROOT / "docs" / "101_CANONICAL_DOMAIN_REGISTRY_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md + docs/101_CANONICAL_DOMAIN_REGISTRY_LAW.md",
        branch_name=f"PR-B Canonical Domain Registry ({branch_note})",
        constitutional_chain=("docs/14", "PR-B", "docs/101"),
        chain_position="PR-B canonical domain registry carrier-only step",
        origin_law_ref="docs/101_CANONICAL_DOMAIN_REGISTRY_LAW.md",
        branch_of_origin="Post-LEXICON-SLOT-L0 canonical registry unification",
        forbidden_shortcut_assertions=(
            "CanonicalDomainRegistry -> TransitionExecution",
            "CanonicalDomainRegistry -> CertificateIssuance",
            "CanonicalDomainRegistry -> SemanticTruthClaim",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "TransitionExecution",
            "ExecutionResultCandidate",
            "TransitionCertificate",
            "SemanticTruth",
            "HukmVerdict",
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


def test_registry_singleton_contains_requested_unified_kinds() -> None:
    _declare("unified base kinds")
    registry = canonical_domain_registry()

    assert registry.version == "canonical-domain-registry-v1"
    assert registry.trace_ref.startswith("trace://")
    assert registry.includes_domain(DomainId.USM)
    assert registry.includes_domain(DomainId.LEXICON)
    assert registry.includes_transition_kind(TransitionKind.EXECUTION_CANDIDATE)
    assert CarrierKind.TRANSITION_CONTRACT in registry.carrier_kinds
    assert ResidualKind.DEFERRED in registry.residual_kinds
    assert RankChannel.RESIDUAL_CEILING in registry.rank_channels


def test_registry_rejects_duplicate_entries() -> None:
    _declare("duplicate-entry refusal")
    valid = canonical_domain_registry()

    with pytest.raises(CanonicalDomainRegistrySchemaError, match="must be unique"):
        CanonicalDomainRegistry(
            version=valid.version,
            trace_ref=valid.trace_ref,
            domains=(DomainId.USM, DomainId.USM),
            transition_kinds=valid.transition_kinds,
            carrier_kinds=valid.carrier_kinds,
            evidence_kinds=valid.evidence_kinds,
            residual_kinds=valid.residual_kinds,
            rank_channels=valid.rank_channels,
        )


def test_registry_is_carrier_only_without_execution_surface() -> None:
    _declare("carrier-only non-execution posture")
    registry = canonical_domain_registry()

    assert not hasattr(registry, "execute")
    assert not hasattr(registry, "commit")
    assert not hasattr(registry, "prove")


def test_docs_register_pr_b_and_law_file() -> None:
    _declare("chain/law synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    law = _DOC_101.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "PR-B  Canonical Domain Registry" in roadmap
    assert "Amendment-76 (PR-B — Canonical Domain Registry)" in roadmap
    assert "Status: constitutional boundary + carrier-only runtime document." in law
    assert (
        "DomainId / TransitionKind / CarrierKind / EvidenceKind / ResidualKind / RankChannel"
        in law
    )
    assert "101_CANONICAL_DOMAIN_REGISTRY_LAW.md" in index
