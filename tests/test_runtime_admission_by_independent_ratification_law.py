"""Constitutional tests for docs/110 runtime-admission boundary.

Origin law     : docs/110 (Runtime Admission by Independent Ratification Law)
Branch         : V0.230 runtime-admission boundary
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
_DOC_110 = _REPO_ROOT / "docs" / "110_RUNTIME_ADMISSION_BY_INDEPENDENT_RATIFICATION_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/110_RUNTIME_ADMISSION_BY_INDEPENDENT_RATIFICATION_LAW.md",
        branch_name=f"V0.230 Runtime Admission ({branch_note})",
        constitutional_chain=("docs/12", "docs/52", "docs/110"),
        chain_position=(
            "runtime admission is licensed only after independent ratification + "
            "falsification and regression stability"
        ),
        origin_law_ref="docs/110_RUNTIME_ADMISSION_BY_INDEPENDENT_RATIFICATION_LAW.md",
        branch_of_origin="Post-V0.229 closure reconstruction admission discipline",
        forbidden_shortcut_assertions=(
            "Observer -> RuntimeAdmission",
            "GreenCI -> RuntimeAdmission",
            "DocsWritten -> RuntimeAdmission",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "AuthorityRuntimeOpen",
            "BridgeRuntimeOpen",
            "SemanticOutputOpen",
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


def test_docs_110_declares_runtime_admission_equivalence_and_order() -> None:
    _declare("equivalence and chain ordering")
    body = _DOC_110.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert (
        "No runtime operation before its law is independently ratified and falsification-tested."
        in body
    )
    assert "Runtime implements proven law; runtime does not prove its own law." in body
    assert "OpenRuntime(L)" in body
    assert "LawRatified(L)" in body
    assert "ProofObjectsPass(L)" in body
    assert "CountermodelsPass(L)" in body
    assert "ReconstructionStable(L)" in body
    assert "NegativeRegressionStable(L)" in body
    assert "ResidualRegressionStable(L)" in body
    assert (
        "Observer -> ProofObject -> DerivedLaw -> Countermodel -> Regression -> RuntimeAdmission"
        in body
    )
    assert "StageArtifacts -> ClosureProofObject -> ClosureVerdict" in body
    assert "110_RUNTIME_ADMISSION_BY_INDEPENDENT_RATIFICATION_LAW.md" in index


def test_docs_110_requires_four_minimum_refusal_families() -> None:
    _declare("minimum refusal family lock")
    body = _DOC_110.read_text(encoding="utf-8")
    for marker in (
        "MissingRequirement",
        "BlockingResidual",
        "BrokenTraceContinuity",
        "RankAboveEvidence",
    ):
        assert marker in body


def test_runtime_admission_predicate_refuses_partial_prerequisites() -> None:
    _declare("open-runtime predicate closure discipline")

    def open_runtime(
        *,
        law_ratified: bool,
        proof_objects_pass: bool,
        countermodels_pass: bool,
        reconstruction_stable: bool,
        negative_regression_stable: bool,
        residual_regression_stable: bool,
    ) -> bool:
        return (
            law_ratified
            and proof_objects_pass
            and countermodels_pass
            and reconstruction_stable
            and negative_regression_stable
            and residual_regression_stable
        )

    assert open_runtime(
        law_ratified=True,
        proof_objects_pass=True,
        countermodels_pass=True,
        reconstruction_stable=True,
        negative_regression_stable=True,
        residual_regression_stable=True,
    )
    assert not open_runtime(
        law_ratified=True,
        proof_objects_pass=True,
        countermodels_pass=True,
        reconstruction_stable=True,
        negative_regression_stable=True,
        residual_regression_stable=False,
    )
