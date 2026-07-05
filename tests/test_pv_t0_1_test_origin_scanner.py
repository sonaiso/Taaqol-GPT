"""PV-T0.1 test-origin scanner (CLOSE-3).

Origin law     : docs/52_CONSTITUTIONAL_TEST_ORIGIN_COVENANT.md
Branch         : CLOSE-3 (PV-T0.1 test-origin scanner)
Category       : Category 4 — Support / fixture tests (docs/52 §4)
"""

from __future__ import annotations

import ast
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_CLOSE_3_DONE = "CLOSE-3 PV-T0.1 test-origin scanner                                  ✓ done"
_CLOSE_3_1_DONE = (
    "CLOSE-3.1 Lift-the-Ban Matrix Law                                        ✓ done"
)
_CLOSE_4_DONE_ROADMAP = (
    "CLOSE-4 Golden closure fixtures                                          ✓ done"
)
_CLOSE_4_DONE_CLAUDE = (
    "CLOSE-4 Golden closure fixtures                                            ✓ done"
)
_CLOSE_5_DONE_ROADMAP = (
    "CLOSE-5 Final closure audit                                              ✓ done"
)
_CLOSE_5_DONE_CLAUDE = (
    "CLOSE-5 Final closure audit                                                ✓ done"
)
_DAL_A4_DONE_LABEL = "DAL-A4  Hamza / shadda / tanwin / sukun / madd gates"
_DAL_A4_ADMIT_LABEL = "DAL-A4-ADMIT post-CLOSE-6 admission decision (DAL-A4 scope only)"
_DAL_A5_ADMIT_LABEL = "DAL-A5-ADMIT admission boundary after DAL-A4 runtime"
_DAL_A5_RUNTIME_LABEL = "DAL-A5  Syllable / transition / adjacency / S1-S5 gates"
_DAL_A6_ADMIT_LABEL = "DAL-A6-ADMIT admission boundary after DAL-A5 runtime"
_DAL_A6_RUNTIME_LABEL = "DAL-A6  Detailed waqf / wasl closure"
_DAL_A7_RUNTIME_LABEL = "DAL-A7  Usage / loan / unvocalized / deletion residual gates"
_DAL_A7_1_DONE_LABEL = "DAL-A7.1 Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics"
_DAL_A8_DONE_LABEL = "DAL-A8  DalAloneClosed -> LafziMadlulGate integration"
_DAL_A8_1_CURRENT_LABEL = "DAL-A8.1 Harden forbidden-neighbor proof after DAL-A8 merge"

_REQUIRED_DECLARATION_KEYS = frozenset({"origin_law", "branch_name", "constitutional_chain"})
# These are the exact constructor keyword names in ConstitutionalTestCase /
# ConstitutionalChainTestCase and docs/52 §2/§3.


# PV-T0 transition rule (docs/52 §5): existing orphan tests are a deferred
# residual and must be listed explicitly, while new tests must declare the
# mandatory origin fields.
_LEGACY_DEFERRED_ORPHAN_MODULES = frozenset(
    {
        "tests/test_arabic_euclidean_layer_contract_law.py",
        "tests/test_audit_tanzil_bridge.py",
        "tests/test_carrier_not_verdict.py",
        "tests/test_chain_report.py",
        "tests/test_contractable_unit_geometry.py",
        "tests/test_dal_atomic_surface.py",
        "tests/test_dal_madlul_binding.py",
        "tests/test_dal_only_boundary.py",
        "tests/test_gpt_answer_reasonableness_objective_law.py",
        "tests/test_gpt_k1_constitutional_checklist.py",
        "tests/test_gpt_k2_golden_dataset.py",
        "tests/test_gpt_r1_input_contract.py",
        "tests/test_gpt_r2_maqam_boundary.py",
        "tests/test_gpt_r3_mantuq_boundary.py",
        "tests/test_gpt_r4_mafhum_boundary.py",
        "tests/test_gpt_r5_origin_binding_gate.py",
        "tests/test_gpt_r6_reasonableness_gates.py",
        "tests/test_gpt_r7_reasonableness_verdict.py",
        "tests/test_gpt_r8_audit_integration_law.py",
        "tests/test_gpt_r8_hallucination_leak_closure.py",
        "tests/test_hukm_candidate.py",
        "tests/test_ifadah_candidate.py",
        "tests/test_knowledge_origins_boundary_law.py",
        "tests/test_licensing_boundary.py",
        "tests/test_manat_candidate.py",
        "tests/test_mantuq_closure.py",
        "tests/test_mu_chain.py",
        "tests/test_mufrad_dalalah_closure.py",
        "tests/test_origin_schema_carriers.py",
        "tests/test_package_imports.py",
        "tests/test_path_gate_pre_weight.py",
        "tests/test_pr_x0_jump_test_matrix_law.py",
        "tests/test_pr_x0l_euclidean_learning_loop.py",
        "tests/test_pr_x0r_runtime_contract_hooks.py",
        "tests/test_project_methodology_objectives_kpi_plan.py",
        "tests/test_proof_failure_policy_alignment.py",
        "tests/test_registry_closure.py",
        "tests/test_registry_contract.py",
        "tests/test_relation_candidate.py",
        "tests/test_relation_closure.py",
        "tests/test_source_hygiene.py",
        "tests/test_tanzil_candidate.py",
        "tests/test_verbal_madlul_boundary.py",
        "tests/test_vertical_path_closure.py",
        "tests/test_weight_carriers.py",
        "tests/test_weight_fit.py",
    }
)


def _declare(branch_name: str) -> None:
    """Assert the scanner test itself satisfies docs/52 declaration discipline."""
    case = ConstitutionalTestCase(
        origin_law="docs/52_CONSTITUTIONAL_TEST_ORIGIN_COVENANT.md",
        branch_name=branch_name,
        constitutional_chain=("PV-T0", "CLOSE-3", "PV-T0.1Scanner"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("OrphanTestJudgment",),
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


def _target_test_modules() -> tuple[Path, ...]:
    tests_root = _REPO_ROOT / "tests"
    return tuple(sorted(path for path in tests_root.glob("test_*.py") if path.is_file()))


def _has_required_origin_declaration(path: Path) -> bool:
    """Accept both test-case schemas because both remain constitutional."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        func_name: str | None = None
        if isinstance(func, ast.Name):
            func_name = func.id
        elif isinstance(func, ast.Attribute):
            func_name = func.attr
        if func_name not in {"ConstitutionalTestCase", "ConstitutionalChainTestCase"}:
            continue
        keys = {keyword.arg for keyword in node.keywords if keyword.arg is not None}
        if _REQUIRED_DECLARATION_KEYS.issubset(keys):
            return True
    return False


def _non_compliant_modules() -> tuple[str, ...]:
    missing: list[str] = []
    for path in _target_test_modules():
        if not _has_required_origin_declaration(path):
            missing.append(path.relative_to(_REPO_ROOT).as_posix())
    return tuple(missing)


def _has_current_chain_marker(text: str, label: str) -> bool:
    return any(line.strip().startswith(label) and "→ current" in line for line in text.splitlines())


def _has_done_chain_marker(text: str, label: str) -> bool:
    return any(line.strip().startswith(label) and "✓ done" in line for line in text.splitlines())


def test_pv_t0_1_blocks_new_orphan_test_modules() -> None:
    _declare("block new orphan modules")
    non_compliant = set(_non_compliant_modules())
    new_orphan_modules = sorted(non_compliant - _LEGACY_DEFERRED_ORPHAN_MODULES)
    assert not new_orphan_modules, (
        "PV-T0.1 violation: new test modules missing required declarations "
        f"{sorted(_REQUIRED_DECLARATION_KEYS)}. Add ConstitutionalTestCase/"
        "ConstitutionalChainTestCase with origin_law, branch_name, "
        f"constitutional_chain. New orphan modules: {new_orphan_modules}"
    )


def test_pv_t0_1_deferred_orphan_inventory_is_explicit() -> None:
    _declare("deferred orphan inventory")
    for relative in sorted(_LEGACY_DEFERRED_ORPHAN_MODULES):
        assert (_REPO_ROOT / relative).exists(), (
            "Deferred orphan inventory contains a missing file; "
            f"remove stale entry: {relative}"
        )


def test_pv_t0_1_chain_status_records_close_4_close_5_done_and_lafzi_b_transition() -> None:
    _declare("chain status synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert _CLOSE_3_DONE in roadmap
    assert _CLOSE_3_1_DONE in roadmap
    assert _CLOSE_4_DONE_ROADMAP in roadmap
    assert _CLOSE_5_DONE_ROADMAP in roadmap
    assert _has_done_chain_marker(roadmap, _DAL_A4_DONE_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A4_ADMIT_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A5_ADMIT_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A5_RUNTIME_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A6_ADMIT_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A6_RUNTIME_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A7_RUNTIME_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A7_1_DONE_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A8_DONE_LABEL)
    assert _has_done_chain_marker(roadmap, _DAL_A8_1_CURRENT_LABEL)
    assert _has_done_chain_marker(roadmap, "LAFZI-B0 Lafzi Madlul Correspondence Law")
    assert _has_done_chain_marker(
        roadmap, "LAFZI-B1 Lafzi carrier surface + local residual vocabulary"
    )
    assert _has_done_chain_marker(roadmap, "LAFZI-B2 WordKindCandidateGate")
    assert _has_done_chain_marker(roadmap, "LAFZI-B3 SourceIdentityGate")
    assert _has_done_chain_marker(roadmap, "LAFZI-B4 FormStateGate")
    assert _has_done_chain_marker(roadmap, "LAFZI-B5 InternalWordPathGate")
    assert _has_done_chain_marker(
        roadmap,
        "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration",
    )
    assert _CLOSE_3_DONE in claude
    assert _CLOSE_3_1_DONE in claude
    assert _CLOSE_4_DONE_CLAUDE in claude
    assert _CLOSE_5_DONE_CLAUDE in claude
    assert _has_done_chain_marker(claude, _DAL_A4_DONE_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A4_ADMIT_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A5_ADMIT_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A5_RUNTIME_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A6_ADMIT_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A6_RUNTIME_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A7_RUNTIME_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A7_1_DONE_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A8_DONE_LABEL)
    assert _has_done_chain_marker(claude, _DAL_A8_1_CURRENT_LABEL)
    assert _has_done_chain_marker(claude, "LAFZI-B0 Lafzi Madlul Correspondence Law")
    assert _has_done_chain_marker(
        claude, "LAFZI-B1 Lafzi carrier surface + local residual vocabulary"
    )
    assert _has_done_chain_marker(claude, "LAFZI-B2 WordKindCandidateGate")
    assert _has_done_chain_marker(claude, "LAFZI-B3 SourceIdentityGate")
    assert _has_done_chain_marker(claude, "LAFZI-B4 FormStateGate")
    assert _has_done_chain_marker(claude, "LAFZI-B5 InternalWordPathGate")
    assert _has_done_chain_marker(
        claude,
        "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration",
    )
