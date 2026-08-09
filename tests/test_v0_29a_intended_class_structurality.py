"""Constitutional tests for V0.29a Intended-Class Structurality Attack.

Origin law     : docs/107 (Intended-Class Structurality Attack)
Branch         : V0.29a Intended-Class Structurality Attack
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r.intended_class_structurality import (
    ANTI_SMUGGLING_FORBIDDEN_TOKENS,
    SIGMA_K_S0,
    T_K_S0,
    EvaluationOverlay,
    ExtendedFragmentModel,
    StructuralAxiom,
    StructuralFragmentModel,
    StructuralNode,
    StructuralTheory,
    anti_smuggling_holds,
    anti_smuggling_violations,
    classify_membership,
    in_intended_class,
    models_of,
    non_membership_has_witness,
    structurality_theorem_holds,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_107 = _REPO_ROOT / "docs" / "107_INTENDED_CLASS_STRUCTURALITY_ATTACK_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/107_INTENDED_CLASS_STRUCTURALITY_ATTACK_LAW.md",
        branch_name=f"V0.29a Intended-Class Structurality Attack ({branch_note})",
        constitutional_chain=("docs/12", "docs/52", "docs/107"),
        chain_position=(
            "V0.29a fixes fragment-local structural intended class before "
            "any projection/equivalence/cutoff work"
        ),
        origin_law_ref="docs/107_INTENDED_CLASS_STRUCTURALITY_ATTACK_LAW.md",
        branch_of_origin="V0.29 pre-PR-126 structurality gate",
        forbidden_shortcut_assertions=(
            "V0.29a -> claim-equivalence",
            "V0.29a -> FRP",
            "V0.29a -> cutoff-theorem",
            "V0.29a -> checker-completeness",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "FRPTheorem",
            "CutoffTheorem",
            "CheckerCompleteness",
            "GeneralArabicCorrectness",
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


def _valid_structural_model(model_id: str = "m://valid/1") -> StructuralFragmentModel:
    return StructuralFragmentModel(
        model_id=model_id,
        nodes=(
            StructuralNode(
                node_id="n1",
                boundary_id="b1",
                domain_id="d1",
                scope_id="s1",
                trace_ref="t://1",
            ),
            StructuralNode(
                node_id="n2",
                boundary_id="b1",
                domain_id="d1",
                scope_id="s1",
                trace_ref="t://2",
            ),
        ),
    )


def test_docs_107_declares_structurality_scope_and_stop_gate() -> None:
    _declare("docs boundary and stop condition")
    body = _DOC_107.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "Model != Realization != Context != IntendedClass" in body
    assert "K_S0 := Mod(T_K_S0)" in body
    assert "M not in K_S0 => exists w : Violation_K(M, w)" in body
    assert "M1|Σ_K = M2|Σ_K" in body
    assert "STRUCTURALITY_PASS" in body
    assert "STRUCTURALITY_FAIL" in body
    assert "107_INTENDED_CLASS_STRUCTURALITY_ATTACK_LAW.md" in index


def test_anti_smuggling_holds_for_v0_29a_default_theory() -> None:
    _declare("anti-smuggling default theory pass")
    assert anti_smuggling_holds(T_K_S0)
    assert anti_smuggling_violations(T_K_S0) == ()


def test_anti_smuggling_refuses_claim_checker_vocabulary_in_signature_and_axioms() -> None:
    _declare("anti-smuggling rejection")

    bad_theory = StructuralTheory(
        fragment_id="bad_fragment",
        signature_sigma_k=SIGMA_K_S0 | {"checker_accept_flag", "psi"},
        axioms=(
            StructuralAxiom(
                axiom_id="AXIOM_checker_gate",
                symbols=frozenset({"Node", "accept_status"}),
                validator=lambda model: (),
            ),
        ),
    )

    violations = anti_smuggling_violations(bad_theory)
    assert violations
    assert not anti_smuggling_holds(bad_theory)
    seen = {v.forbidden_token for v in violations}
    assert "checker" in seen
    assert "psi" in seen
    assert "accept" in seen
    assert "cutoff" not in seen
    assert "checker" in ANTI_SMUGGLING_FORBIDDEN_TOKENS


def test_valid_structure_membership_is_independent_from_downstream_claim_truth_values() -> None:
    _declare("claim-independence on valid structure")
    structural = _valid_structural_model()

    left = ExtendedFragmentModel(
        structural=structural,
        overlay=EvaluationOverlay(
            claim_truth_value=True,
            checker_output="PASS",
            extractor_output="B_min := 3",
            cutoff_result="N=9",
            contextual_equivalence_result="eq_A",
            algorithm_success=True,
        ),
    )
    right = ExtendedFragmentModel(
        structural=structural,
        overlay=EvaluationOverlay(
            claim_truth_value=False,
            checker_output="FAIL",
            extractor_output="B_min := 4",
            cutoff_result="N=13",
            contextual_equivalence_result="eq_B",
            algorithm_success=False,
        ),
    )

    assert in_intended_class(structural)
    assert structurality_theorem_holds(left, right)


def test_structural_violation_excludes_membership_even_if_overlay_looks_successful() -> None:
    _declare("structural exclusion dominates downstream success")
    invalid = StructuralFragmentModel(
        model_id="m://invalid/1",
        nodes=(
            StructuralNode(
                node_id="n1",
                boundary_id="b1",
                domain_id="d1",
                scope_id="s1",
                trace_ref="",
            ),
        ),
    )
    optimistic_overlay = ExtendedFragmentModel(
        structural=invalid,
        overlay=EvaluationOverlay(
            claim_truth_value=True,
            checker_output="ACCEPT",
            extractor_output="approved",
            algorithm_success=True,
        ),
    )

    verdict = classify_membership(optimistic_overlay.structural)
    assert not verdict.in_intended_class
    assert non_membership_has_witness(optimistic_overlay.structural)
    assert any(w.axiom_id == "TK_S0_A3_TOTAL_STRUCTURAL_FIELDS" for w in verdict.witnesses)


def test_checker_or_extractor_acceptance_cannot_create_membership() -> None:
    _declare("acceptance cannot force K-membership")
    invalid = StructuralFragmentModel(
        model_id="m://invalid/2",
        nodes=(
            StructuralNode(
                node_id="n1",
                boundary_id="b1",
                domain_id="d1",
                scope_id="s1",
                trace_ref="t://same",
            ),
            StructuralNode(
                node_id="n1",
                boundary_id="b2",
                domain_id="d2",
                scope_id="s2",
                trace_ref="t://same",
            ),
        ),
    )

    overlay_a = ExtendedFragmentModel(
        structural=invalid,
        overlay=EvaluationOverlay(checker_output="ACCEPT", extractor_output="ACCEPT"),
    )
    overlay_b = ExtendedFragmentModel(
        structural=invalid,
        overlay=EvaluationOverlay(checker_output="REJECT", extractor_output="REJECT"),
    )

    assert not in_intended_class(overlay_a.structural)
    assert not in_intended_class(overlay_b.structural)


def test_models_of_realizes_fragment_wise_class_and_keeps_scope_local() -> None:
    _declare("fragment-wise Ki realization")
    valid = _valid_structural_model("m://valid/2")
    invalid = StructuralFragmentModel(
        model_id="m://invalid/3",
        nodes=(
            StructuralNode(
                node_id="n1",
                boundary_id="",
                domain_id="d1",
                scope_id="s1",
                trace_ref="t://1",
            ),
        ),
    )

    selected = models_of(T_K_S0, (valid, invalid))
    assert selected == (valid,)
