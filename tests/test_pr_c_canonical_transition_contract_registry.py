"""Constitutional tests for PR-C canonical transition contract registry surface.

Origin law     : docs/14 (PR-C registration) + docs/102 (registry boundary)
Branch         : PR-C Canonical Transition Contract Registry
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.weight.lexicon_slot_geometry import (
    TC_IL,
    TC_LW,
    TC_RI,
    TC_SD,
    TC_SR,
    TC_WS,
)
from taaqqul_slot_geometry.x0r.canonical_domain_registry import DomainId
from taaqqul_slot_geometry.x0r.canonical_transition_contract_registry import (
    CanonicalTransitionContract,
    CanonicalTransitionContractRegistry,
    CanonicalTransitionContractRegistrySchemaError,
    TransitionContractId,
    canonical_transition_contract_registry,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOC_102 = _REPO_ROOT / "docs" / "102_CANONICAL_TRANSITION_CONTRACT_REGISTRY_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/14_PR_CHAIN_ROADMAP.md + "
            "docs/102_CANONICAL_TRANSITION_CONTRACT_REGISTRY_LAW.md"
        ),
        branch_name=f"PR-C Canonical Transition Contract Registry ({branch_note})",
        constitutional_chain=("docs/14", "PR-C", "docs/102"),
        chain_position="PR-C canonical transition contract registry carrier-only step",
        origin_law_ref="docs/102_CANONICAL_TRANSITION_CONTRACT_REGISTRY_LAW.md",
        branch_of_origin="Post-PR-B canonical contract-source unification",
        forbidden_shortcut_assertions=(
            "CanonicalTransitionContractRegistry -> TransitionExecution",
            "CanonicalTransitionContractRegistry -> PermitIssuance",
            "CanonicalTransitionContractRegistry -> CertificateIssuance",
            "CanonicalTransitionContractRegistry -> SemanticTruthClaim",
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


def test_registry_singleton_contains_lexicon_contract_families() -> None:
    _declare("unified contract families")
    registry = canonical_transition_contract_registry()

    assert registry.version == "canonical-transition-contract-registry-v1"
    assert registry.trace_ref.startswith("trace://")
    assert registry.includes_contract(TransitionContractId.TC_01)
    assert registry.includes_contract(TransitionContractId.TC_06)
    assert registry.includes_contract(TransitionContractId.TC_SR)
    assert registry.includes_contract(TransitionContractId.TC_SD)

    contract = registry.contract_by_id(TransitionContractId.TC_SR)
    assert contract.domain is DomainId.LEXICON
    assert contract.source_slot == "SourceSlot"
    assert contract.target_slot == "ReadingCandidate"


def test_registry_rejects_duplicate_contract_ids() -> None:
    _declare("duplicate-contract-id refusal")
    valid = canonical_transition_contract_registry()
    row = valid.contract_by_id(TransitionContractId.TC_01)

    with pytest.raises(CanonicalTransitionContractRegistrySchemaError, match="unique contract_id"):
        CanonicalTransitionContractRegistry(
            version=valid.version,
            trace_ref=valid.trace_ref,
            contracts=(row, row),
        )


def test_registry_is_carrier_only_without_execution_surface() -> None:
    _declare("carrier-only non-execution posture")
    registry = canonical_transition_contract_registry()

    assert not hasattr(registry, "execute")
    assert not hasattr(registry, "commit")
    assert not hasattr(registry, "prove")


def test_lexicon_contract_constants_are_built_from_canonical_registry() -> None:
    _declare("lexicon contract source-of-truth alignment")
    registry = canonical_transition_contract_registry()

    pairings = (
        (TransitionContractId.TC_SR, TC_SR),
        (TransitionContractId.TC_RI, TC_RI),
        (TransitionContractId.TC_IL, TC_IL),
        (TransitionContractId.TC_LW, TC_LW),
        (TransitionContractId.TC_WS, TC_WS),
        (TransitionContractId.TC_SD, TC_SD),
    )

    for contract_id, lexical_contract in pairings:
        spec = registry.contract_by_id(contract_id)
        assert lexical_contract.contract_id == spec.contract_id.value
        assert lexical_contract.input_slot == spec.source_slot
        assert lexical_contract.output_slot == spec.target_slot
        assert lexical_contract.required_fields == spec.required_fields
        assert lexical_contract.allows_multi_candidate == spec.allows_multi_candidate


def test_docs_register_pr_c_and_law_file() -> None:
    _declare("chain/law synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    law = _DOC_102.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "PR-C  Canonical Transition Contract Registry" in roadmap
    assert "Amendment-77 (PR-C — Canonical Transition Contract Registry)" in roadmap
    assert "Status: constitutional boundary + carrier-only runtime document." in law
    assert "TC-01..TC-06 (docs/99)" in law
    assert "TC_SR..TC_SD (docs/100)" in law
    assert "102_CANONICAL_TRANSITION_CONTRACT_REGISTRY_LAW.md" in index


def test_contract_row_rejects_empty_required_fields() -> None:
    _declare("required-fields schema refusal")
    valid = canonical_transition_contract_registry().contract_by_id(TransitionContractId.TC_01)

    with pytest.raises(CanonicalTransitionContractRegistrySchemaError, match="required_fields"):
        CanonicalTransitionContract(
            contract_id=valid.contract_id,
            domain=valid.domain,
            transition_kind=valid.transition_kind,
            source_slot=valid.source_slot,
            target_slot=valid.target_slot,
            required_conditions=valid.required_conditions,
            required_fields=(),
            outputs=valid.outputs,
            evidence_kinds=valid.evidence_kinds,
            residual_kinds=valid.residual_kinds,
            allows_multi_candidate=valid.allows_multi_candidate,
            law_ref=valid.law_ref,
            trace_ref=valid.trace_ref,
        )
