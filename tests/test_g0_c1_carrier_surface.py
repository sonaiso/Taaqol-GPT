"""Acceptance tests for G0-C1 bare-stem carrier surface.

Origin law     : docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md
Branch         : G0-C1 (BareJamidStemCandidate + AnchorCertificate carriers)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.g0_c1_carriers import (
    AnchorCertificate,
    BareJamidStemCandidate,
    EntityRank,
    EpistemicRank,
    G0C1CarrierSchemaError,
    LexicalTruthStatus,
    OntologicalClass,
    StemGender,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md",
        branch_name=f"G0-C1 ({branch_note})",
        constitutional_chain=("G0-L0", "G0-C1"),
        chain_position="G0-C1",
        origin_law_ref="docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md#13-reserved-successor-steps-not-shipped-by-this-pr",
        branch_of_origin="G0 reserved successor chain after zero-layer law-only covenant.",
        forbidden_shortcut_assertions=(
            "BareJamidStemCandidate -> HukmVerdict",
            "BareJamidStemCandidate -> TruthCertificate",
            "BareJamidStemCandidate -> TransitionGate",
            "AnchorCertificate -> ApprovalVerdict",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "HukmVerdict",
            "TruthCertificate",
            "AuthorityExecution",
            "TransitionGateDecision",
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


def _sample_candidate() -> BareJamidStemCandidate:
    return BareJamidStemCandidate(
        stem="جبل",
        vocalized="جَبَل",
        size=3,
        pattern="فَعَل",
        has_productive_addition=False,
        jamid=True,
        ontological_class=OntologicalClass.O1,
        entity_rank=EntityRank.INDIVIDUAL,
        gender=StemGender.MASCULINE,
        gender_evidence="lexical assignment",
        epistemic_rank=EpistemicRank.E2,
        lexical_truth_status=LexicalTruthStatus.ATTESTED,
        hard_blockers_passed=("NO_DUAL", "NO_PLURAL"),
        d_form=0.0,
        d_wad=0.0,
        d_onto=0.0,
        trace_ref="trace://g0-c1/candidate/001",
    )


def _sample_certificate() -> AnchorCertificate:
    return AnchorCertificate(
        certificate_id="g0-anchor-001",
        stem_key="ENT_MOUNTAIN",
        ontological_class=OntologicalClass.O1,
        epistemic_rank=EpistemicRank.E2,
        entity_rank=EntityRank.INDIVIDUAL,
        source_trace_ref="trace://g0-c1/cert/001",
        residuals=("ONTOLOGY_CLASS_PENDING_G0_C4",),
    )


def test_candidate_and_certificate_construct() -> None:
    _declare("carrier construction")
    candidate = _sample_candidate()
    certificate = _sample_certificate()
    assert candidate.stem == "جبل"
    assert certificate.certificate_id == "g0-anchor-001"


def test_carriers_are_frozen() -> None:
    _declare("frozen carriers")
    candidate = _sample_candidate()
    certificate = _sample_certificate()
    with pytest.raises(dataclasses.FrozenInstanceError):
        candidate.stem = "ماء"  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        certificate.stem_key = "ENT_WATER"  # type: ignore[misc]


def test_candidate_refuses_invalid_trace_ref() -> None:
    _declare("candidate trace schema")
    with pytest.raises(G0C1CarrierSchemaError, match="trace_ref"):
        BareJamidStemCandidate(
            stem="جبل",
            vocalized="جَبَل",
            size=3,
            pattern="فَعَل",
            has_productive_addition=False,
            jamid=True,
            ontological_class=OntologicalClass.O1,
            entity_rank=EntityRank.INDIVIDUAL,
            gender=StemGender.MASCULINE,
            gender_evidence="lexical assignment",
            epistemic_rank=EpistemicRank.E2,
            lexical_truth_status=LexicalTruthStatus.ATTESTED,
            hard_blockers_passed=("NO_DUAL",),
            d_form=0.0,
            d_wad=0.0,
            d_onto=0.0,
            trace_ref="bad-trace",
        )


def test_certificate_refuses_empty_residual_item() -> None:
    _declare("certificate residual schema")
    with pytest.raises(G0C1CarrierSchemaError, match="residuals"):
        AnchorCertificate(
            certificate_id="g0-anchor-001",
            stem_key="ENT_MOUNTAIN",
            ontological_class=OntologicalClass.O1,
            epistemic_rank=EpistemicRank.E2,
            entity_rank=EntityRank.INDIVIDUAL,
            source_trace_ref="trace://g0-c1/cert/001",
            residuals=("",),
        )


def test_docs_14_and_claude_record_g0_c1_done() -> None:
    _declare("chain-state recording")
    body14 = _DOC_14.read_text(encoding="utf-8")
    body_claude = _CLAUDE.read_text(encoding="utf-8")
    assert "G0-C1   Bare-stem carrier surface" in body14
    assert "G0-C1\n    Origin" in body14
    assert "G0-C1   Bare-stem carrier surface" in body_claude
