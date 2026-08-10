"""Constitutional tests for V0.229 Meta-Core Reconstruction law.

Origin law     : docs/109 (V0.229 Meta-Core Reconstruction & Derived-Law Recovery)
Branch         : V0.229 reconstruction boundary
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)
from tests.support.derived_law_proof_case import (
    DerivedLawProofCase,
    DerivedLawProofResult,
    DerivedLawProofSchemaError,
    assert_derived_law_proof_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_109 = (
    _REPO_ROOT / "docs" / "109_V0_229_META_CORE_RECONSTRUCTION_DERIVED_LAW_RECOVERY_LAW.md"
)
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/109_V0_229_META_CORE_RECONSTRUCTION_DERIVED_LAW_RECOVERY_LAW.md",
        branch_name=f"V0.229 Meta-Core Reconstruction ({branch_note})",
        constitutional_chain=("docs/12", "docs/52", "docs/109"),
        chain_position=(
            "V0.229 reconstructs pre-228 distinctions from the reduced core "
            "without introducing new primitives"
        ),
        origin_law_ref="docs/109_V0_229_META_CORE_RECONSTRUCTION_DERIVED_LAW_RECOVERY_LAW.md",
        branch_of_origin="V0.229 reconstruction boundary",
        forbidden_shortcut_assertions=(
            "V0.229 -> primitive-expansion-as-proof",
            "V0.229 -> global-reduction-restart",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "PrimitiveExpansionAcceptedAsReconstruction",
            "GlobalReopenWithoutLostDistinction",
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


def test_docs_109_registers_reconstruction_boundary_and_dlp_template() -> None:
    _declare("docs boundary + registration")
    body = _DOC_109.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "Reduction is licensed iff Reconstruction survives." in body
    assert "ReductionStop_C(M_C)" in body
    assert "RC = <Claim, OldVerdict, NewVerdict, Witness, TraceDifference, LostDistinction>" in body
    assert (
        "DLP_X = <Definition, Dependencies, PositiveWitness, Countermodel, "
        "Trace, EquivalenceProof>" in body
    )
    assert "Reopen(228, LostDistinction_X)" in body
    assert "109_V0_229_META_CORE_RECONSTRUCTION_DERIVED_LAW_RECOVERY_LAW.md" in index


def test_derived_law_proof_template_accepts_complete_case() -> None:
    _declare("DLP template completeness pass")
    case = DerivedLawProofCase(
        concept_name="Rank",
        definition="Rank is recovered as a trace/evidence-supported observational order.",
        dependencies=("Trace", "Evidence", "ObservationalOrder"),
        positive_witness="Two candidates are ordered with preserved trace reasons.",
        countermodel="Boolean-only order that drops trace is rejected.",
        trace="trace://v0_229/rank/recover/1",
        equivalence_proof="Decode_Rank(M_C) ~=_C Rank_pre228 under capability C_rank.",
        capability="C_rank",
    )
    result = DerivedLawProofResult(
        concept_name="Rank",
        decoded_equivalent=True,
        trace_present=True,
        lost_distinction=(),
        regression_positive_preserved=True,
        regression_negative_preserved=True,
        regression_residual_preserved=True,
        hidden_reintroduction_detected=False,
    )

    assert_derived_law_proof_case(case, result)


def test_derived_law_proof_template_refuses_missing_required_field() -> None:
    _declare("DLP schema refusal on missing field")
    with pytest.raises(DerivedLawProofSchemaError):
        DerivedLawProofCase(
            concept_name="NoJump",
            definition="",
            dependencies=("TypedTransport",),
            positive_witness="Unlicensed transport is absent by construction.",
            countermodel="Jump appears only when transport is introduced without evidence.",
            trace="trace://v0_229/nojump/recover/1",
            equivalence_proof="Decode_NoJump(M_C) ~=_C NoJump_pre228.",
            capability="C_transport",
        )


def test_derived_law_proof_template_refuses_lost_distinction() -> None:
    _declare("local reopening discipline")
    case = DerivedLawProofCase(
        concept_name="Boundary",
        definition="Boundary is recovered as failure/non-definition frontier.",
        dependencies=("FailureFrontier", "NonDefinitionFrontier"),
        positive_witness="Undefined transport emits boundary refusal with trace.",
        countermodel="Collapsed boundary accepts undefined operation.",
        trace="trace://v0_229/boundary/recover/1",
        equivalence_proof="Decode_Boundary(M_C) ~=_C Boundary_pre228.",
        capability="C_boundary",
    )
    result = DerivedLawProofResult(
        concept_name="Boundary",
        decoded_equivalent=True,
        trace_present=True,
        lost_distinction=("Boundary::UndefinedVsRefused",),
        regression_positive_preserved=True,
        regression_negative_preserved=True,
        regression_residual_preserved=True,
        hidden_reintroduction_detected=False,
    )

    with pytest.raises(AssertionError):
        assert_derived_law_proof_case(case, result)
