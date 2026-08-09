"""Constitutional tests for V0.29b.0 TraceRef Elimination Attack.

Origin law     : docs/108 (V0.29b.0 TraceRef Elimination Attack)
Branch         : V0.29b.0 TraceRef Elimination Attack
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r.intended_class_structurality import (
    T_K_S0,
    StructuralAxiom,
    StructuralTheory,
    TraceRefConstitutivityDecision,
    anti_smuggling_holds,
    build_trace_ref_elided_theory,
    renaming_smuggling_violations,
    run_trace_ref_elimination_attack,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_108 = _REPO_ROOT / "docs" / "108_V0_29B0_TRACE_REF_ELIMINATION_ATTACK_LAW.md"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/108_V0_29B0_TRACE_REF_ELIMINATION_ATTACK_LAW.md",
        branch_name=f"V0.29b.0 TraceRef Elimination Attack ({branch_note})",
        constitutional_chain=("docs/12", "docs/52", "docs/107", "docs/108"),
        chain_position=(
            "V0.29b.0 closes trace_ref constitutivity before opening V0.29b.1 "
            "projection independence"
        ),
        origin_law_ref="docs/108_V0_29B0_TRACE_REF_ELIMINATION_ATTACK_LAW.md",
        branch_of_origin="V0.29b trace_ref closure gate",
        forbidden_shortcut_assertions=(
            "V0.29b.0 -> pi_psi",
            "V0.29b.0 -> claim-equivalence",
            "V0.29b.0 -> FRP",
            "V0.29b.0 -> finite-quotient",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "PiPsiProjection",
            "FiniteQuotient",
            "FRPTheorem",
            "ClaimEquivalence",
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


def test_docs_108_registers_scope_and_acceptance_matrix() -> None:
    _declare("docs boundary")
    body = _DOC_108.read_text(encoding="utf-8")
    index = _DOCS_INDEX.read_text(encoding="utf-8")

    assert "TraceRefConstitutivity = OPEN" in body
    assert "TRACE_REF_NON_CONSTITUTIVE_REALIZATION_ONLY" in body
    assert "No-Renaming-Smuggling" in body
    assert "Claim blindness" in body
    assert "Non-Trivial Compression" in body
    assert "108_V0_29B0_TRACE_REF_ELIMINATION_ATTACK_LAW.md" in index


def test_trace_ref_elimination_attack_closes_with_explicit_decision() -> None:
    _declare("decision completeness")
    result = run_trace_ref_elimination_attack()

    assert result.audited
    assert result.decision in {
        TraceRefConstitutivityDecision.TRACE_REF_CONSTITUTIVE,
        TraceRefConstitutivityDecision.TRACE_REF_NON_CONSTITUTIVE_REALIZATION_ONLY,
    }
    assert (
        result.decision
        is TraceRefConstitutivityDecision.TRACE_REF_NON_CONSTITUTIVE_REALIZATION_ONLY
    )
    assert result.counterexamples


def test_counterexamples_are_trace_only_exclusions() -> None:
    _declare("trace-only witness discipline")
    result = run_trace_ref_elimination_attack()

    assert result.counterexamples
    for witness_bundle in result.counterexamples:
        assert witness_bundle.model_id
        for witness in witness_bundle.base_theory_witnesses:
            assert witness.locus.endswith(".trace_ref")
            assert witness.axiom_id in {
                "TK_S0_A3_TOTAL_STRUCTURAL_FIELDS",
                "TK_S0_A4_TRACE_REF_INJECTIVE",
            }
        assert witness_bundle.elided_theory_witnesses == tuple()


def test_elided_theory_removes_trace_ref_from_signature_and_keeps_anti_smuggling() -> None:
    _declare("elided theory structural hygiene")
    elided = build_trace_ref_elided_theory(T_K_S0)

    assert "trace_ref" not in elided.signature_sigma_k
    assert anti_smuggling_holds(elided)


def test_no_renaming_smuggling_detects_trace_alias_reinjection() -> None:
    _declare("no-renaming-smuggling")
    elided = build_trace_ref_elided_theory(T_K_S0)
    smuggled = StructuralTheory(
        fragment_id="K_S0_ELIDED_SMUGGLED",
        signature_sigma_k=elided.signature_sigma_k | {"origin_ref"},
        axioms=(
            *elided.axioms,
            StructuralAxiom(
                axiom_id="TK_S0_ORIGIN_REF_SHADOW",
                symbols=frozenset({"Node", "origin_ref"}),
                validator=lambda model: tuple(),
            ),
        ),
    )

    violations = renaming_smuggling_violations(smuggled)
    assert violations
    assert {v.alias_token for v in violations} == {"origin_ref"}
