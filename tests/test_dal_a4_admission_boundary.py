"""DAL-A4 admission-only boundary tests.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (DAL-A4-ADMIT admission-only step)
Branch         : DAL-A4-ADMIT (post-CLOSE-6 admission decision)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"DAL-A4-ADMIT ({branch_note})",
        constitutional_chain=("CLOSE-6", "CLOSE-6.1", "DAL-A4-ADMIT"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "OpenedRuntimeBranch",
            "DALA4RuntimeImplementation",
            "DALA5AdmissionByImplication",
            "MeaningOrHukmOutput",
            "GreenCICertification",
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


def test_dal_a4_admission_verdict_exists() -> None:
    _declare("verdict exists")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for marker in (
        "DAL_A4_ADMISSION_VERDICT = {",
        "status: ADMISSION_ONLY",
        "dal_a4_runtime_opening: NOT_OPENED_BY_THIS_PR",
        "latest_completed_arabic_dal_surface: DAL_A3",
        "admitted_next_runtime_branch: DAL_A4_ONLY_IF_THIS_MATRIX_PASSES",
        "dal_a5_to_a8: DEFERRED",
        "lafzi_b0_to_b7: DEFERRED",
        "law_e0_metric_runtime: DEFERRED",
    ):
        assert marker in roadmap, f"Missing DAL-A4 admission verdict marker: {marker}"


def test_dal_a4_admission_matrix_rows_a_to_n_are_present() -> None:
    _declare("matrix rows A-N")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for row in (
        "| A | CLOSE-6 declaration-only boundary is done. |",
        "| B | CLOSE-6.1 post-merge normalization is done. |",
        "| C | DAL-A3 is the latest completed Arabic DAL surface. |",
        "| D | docs/58 defines DAL-A4 law names and scope. |",
        "| E | HamzaResolutionGate is admitted only as a future DAL-A4 gate. |",
        "| F | ShaddaIdghamGate is admitted only as a future DAL-A4 gate. |",
        "| G | TanwinTraceGate is admitted only as a future DAL-A4 gate. |",
        "| H | SukunCollisionGate is admitted only as a future DAL-A4 gate. |",
        "| I | MaddExtensionGate is admitted only as a future DAL-A4 gate. |",
        "| J | No syllable / adjacency / S1-S5 execution is admitted in this PR. |",
        "| K | No waqf / wasl execution is admitted in this PR. |",
        (
            "| L | No usage / loan / unvocalized / deletion execution is admitted "
            "in this PR. |"
        ),
        (
            "| M | No DalAloneClosed -> LafziMadlulGate integration is admitted "
            "in this PR. |"
        ),
        (
            "| N | No word kind, root, pattern, lexical meaning, relation, ifadah, "
            "hukm, tanzil, ontology, or reality output is admitted. |"
        ),
    ):
        assert row in roadmap, f"Missing DAL_A4_ADMISSION_MATRIX row: {row}"


def test_chain_status_shows_close_6_1_done_and_dal_a4_admit_current() -> None:
    _declare("chain status synchronization")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")
    assert (
        "CLOSE-6.1 Post-merge release-boundary verification + admission matrix    ✓ done"
        in roadmap
    )
    assert (
        "DAL-A4-ADMIT post-CLOSE-6 admission decision (DAL-A4 scope only)         → current"
        in roadmap
    )
    assert (
        "CLOSE-6.1 Post-merge release-boundary verification + admission matrix      ✓ done"
        in claude
    )
    assert (
        "DAL-A4-ADMIT post-CLOSE-6 admission decision (DAL-A4 scope only)           → current"
        in claude
    )


def test_admission_forbids_runtime_opening_and_output_layers() -> None:
    _declare("runtime/output boundary refusals")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for marker in (
        "src_runtime_opening: FORBIDDEN_AND_NOT_PRESENT",
        "parser_runtime: NOT_OPENED",
        "morphology_runtime: NOT_OPENED",
        "syntax_runtime: NOT_OPENED",
        "semantic_runtime: NOT_OPENED",
        "ifadah_runtime: NOT_OPENED",
        "mafhum_runtime: NOT_OPENED",
        "hukm_runtime: NOT_OPENED",
        "truth_certainty_reality_runtime: NOT_OPENED",
        "forbidden_outputs: [",
        "ROOT,",
        "PATTERN,",
        "WORD_KIND,",
        "IFADAH,",
        "HUKM,",
        "REALITY,",
        "ONTOLOGY",
    ):
        assert marker in roadmap, f"Missing runtime/output refusal marker: {marker}"


def test_admission_does_not_mark_dal_a4_runtime_done_or_open_dal_a5() -> None:
    _declare("no DAL-A4 runtime and no DAL-A5 implication")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for marker in (
        "DAL-A4  Hamza / shadda / tanwin / sukun / madd gates                      planned",
        "DAL-A5  Syllable / transition / adjacency / S1-S5 gates                   planned",
        "DAL-A6  Detailed waqf / wasl closure                                      planned",
        "DAL-A7  Usage / loan / unvocalized / deletion residual gates              planned",
        "DAL-A8  DalAloneClosed -> LafziMadlulGate integration                     planned",
    ):
        assert marker in roadmap


def test_admission_keeps_lafzi_b_and_law_e0_runtime_deferred() -> None:
    _declare("lafzi/law-e0 deferred")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    assert re.search(r"LAFZI-B0\s+Lafzi Madlul Correspondence Law[\s\S]{0,80}planned", roadmap)
    assert re.search(
        r"LAFZI-B7\s+LafziMadlulClosed -> Wad'iMadlulGate integration\s+planned",
        roadmap,
    )
    assert re.search(r"LAW-E0\s+Arabic Euclidean Layer Contract Law\s+planned", roadmap)


def test_admitted_gate_names_are_future_scope_only() -> None:
    _declare("future gate scope only")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    for gate in (
        "HamzaResolutionGate is admitted only as a future DAL-A4 gate.",
        "ShaddaIdghamGate is admitted only as a future DAL-A4 gate.",
        "TanwinTraceGate is admitted only as a future DAL-A4 gate.",
        "SukunCollisionGate is admitted only as a future DAL-A4 gate.",
        "MaddExtensionGate is admitted only as a future DAL-A4 gate.",
    ):
        assert gate in roadmap


def test_negative_no_runtime_reopening_or_closure_claims() -> None:
    _declare("negative runtime reopening checks")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    assert "it does not implement DAL-A4 runtime." in roadmap
    assert "full_arabic_linguistic_algebra_runtime_closure: NOT_CLAIMED" in roadmap
    assert "No DalAloneClosed -> LafziMadlulGate integration is admitted in this PR." in roadmap
    assert (
        "No word kind, root, pattern, lexical meaning, relation, ifadah, hukm, "
        "tanzil, ontology, or reality output is admitted."
    ) in roadmap


def test_negative_green_ci_not_equal_constitutional_runtime_opening() -> None:
    _declare("negative green-ci shortcut")
    claude = _CLAUDE.read_text(encoding="utf-8")
    assert "Green pytest is not constitutional success." in claude
