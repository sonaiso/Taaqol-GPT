"""Acceptance tests for docs/77 G₀ Bare Jamid Stem / Identity Anchor Law.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (chain-state truth)
Branch         : G0-L0 (Bare Jamid Stem / Identity Anchor Zero-Layer Law)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_77 = _REPO_ROOT / "docs" / "77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_note: str) -> None:
    assert _DOC_77.exists(), "docs/77_G0_BARE_JAMID_STEM_IDENTITY_ANCHOR_LAW.md must exist"
    assert _DOC_14.exists(), "docs/14_PR_CHAIN_ROADMAP.md must exist"
    assert _CLAUDE.exists(), "CLAUDE.md must exist"

    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"G0-L0 ({branch_note})",
        constitutional_chain=("LAW-E1R-A", "G0-L0"),
        chain_position="G0-L0",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md#1-per-step-boundary-summary",
        branch_of_origin="Zero-layer covenant preceding derivation/plural/nisbah/majāz/isnād/ḥukm",
        forbidden_shortcut_assertions=(
            "BareJamidStem -> Meaning",
            "BareJamidStem -> Hukm",
            "BareJamidStem -> Derivation",
            "BareJamidStem -> Plural",
            "BareJamidStem -> Nisbah",
            "BareJamidStem -> Majaz",
            "BareJamidStem -> Context",
            "G0-L0 -> Runtime",
            "G0-L0 -> HorizontalBranch",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeCode",
            "Carrier",
            "Gate",
            "Verdict",
            "Derivation",
            "Plural",
            "Dual",
            "Nisbah",
            "Majaz",
            "Naql",
            "Context",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "FailureCodeExpansion",
            "ResidualKindExpansion",
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


def test_docs_77_exists_and_declares_g0_identity() -> None:
    _declare("document presence and G0 identity")
    body = _DOC_77.read_text(encoding="utf-8")
    required_markers = (
        "77 — G₀ Bare Jamid Stem / Identity Anchor Law",
        "FAMILY               = G0",
        "STEP                 = G0-L0",
        "STEP_KIND            = LAW_ONLY",
        "ADMISSION_GATE       = docs/76 Phase-2 X0R-E1 admission (law-only clause)",
    )
    for marker in required_markers:
        assert marker in body, f"docs/77 missing required marker: {marker}"


def test_docs_77_declares_all_structural_sections() -> None:
    _declare("structural sections §1–§15")
    body = _DOC_77.read_text(encoding="utf-8")
    required_sections = (
        "## §1 Constitutional definition",
        "## §2 What enters and what leaves",
        "## §3 Minimum ontological matrix",
        "## §4 Epistemic classification (evidence strength)",
        "## §5 Bare Jamid Stem Card (the sole output of G₀)",
        "## §6 Bounded epistemic distance law",
        "## §7 Hard blockers (applied before the distance)",
        "## §8 Constitutional golden rule",
        "## §9 Minimal G₀-only matrix (illustrative, not exhaustive)",
        "## §10 Binding between G₀ and later layers",
        "## §11 Constitutional closing",
        "## §12 Chain position and admission",
        "## §13 Reserved successor steps (not shipped by this PR)",
        "## §14 What this law does *not* claim",
        "## §15 Trace",
    )
    for section in required_sections:
        assert section in body, f"docs/77 missing required section header: {section}"


def test_docs_77_lists_all_ten_ontological_classes() -> None:
    _declare("ontological classes O₁ … O₁₀")
    body = _DOC_77.read_text(encoding="utf-8")
    for code in ("O₁", "O₂", "O₃", "O₄", "O₅", "O₆", "O₇", "O₈", "O₉", "O₁₀"):
        assert code in body, f"docs/77 must list ontological class {code}"


def test_docs_77_lists_all_six_epistemic_ranks() -> None:
    _declare("epistemic ranks E₀ … E₅")
    body = _DOC_77.read_text(encoding="utf-8")
    for rank in ("E₀", "E₁", "E₂", "E₃", "E₄", "E₅"):
        assert rank in body, f"docs/77 must list epistemic rank {rank}"


def test_docs_77_lists_all_ten_hard_blockers() -> None:
    _declare("ten hard blockers in §7")
    body = _DOC_77.read_text(encoding="utf-8")
    required_blockers = (
        "Presence of a dual",
        "Presence of a sound or broken plural",
        "Presence of a nisbah",
        "Presence of a ṣināʿī maṣdar",
        "Presence of verbal form or tense",
        "Presence of event-maṣdar",
        "Presence of standard fāʿil / mafʿūl / ālah derivation",
        "Requires majāz",
        "Requires terminological naql",
        "Requires context for polysemy resolution",
    )
    for blocker in required_blockers:
        assert blocker in body, f"docs/77 §7 must list hard blocker: {blocker}"


def test_docs_77_reserves_all_six_successor_steps() -> None:
    _declare("reserved successors G0-C1 … G0-C6")
    body = _DOC_77.read_text(encoding="utf-8")
    for step in ("G0-C1", "G0-C2", "G0-C3", "G0-C4", "G0-C5", "G0-C6"):
        assert step in body, f"docs/77 §13 must reserve {step}"


def test_docs_77_declares_law_only_scope_and_forbidden_surface() -> None:
    _declare("law-only scope and forbidden surface")
    body = _DOC_77.read_text(encoding="utf-8")
    required_markers = (
        "law only",
        "no `src/`",
        "any runtime code",
        "new global `FailureCode`",
        "ResidualKind",
        "horizontal branch",
        "no ḥukm",
    )
    lower = body.lower()
    for marker in required_markers:
        assert marker.lower() in lower, f"docs/77 must declare: {marker}"


def test_docs_14_records_g0_l0_in_chain_table_and_per_step_block() -> None:
    _declare("docs/14 chain-table row + per-step block")
    body = _DOC_14.read_text(encoding="utf-8")
    assert "G0-L0   G₀ Bare Jamid Stem / Identity Anchor Zero-Layer Law" in body, (
        "docs/14 chain table must include the G0-L0 row"
    )
    assert "G0-L0\n    Origin   :" in body, (
        "docs/14 §1 must contain a per-step G0-L0 boundary block"
    )
    assert "Amendment-57 (G0-L0" in body, (
        "docs/14 must contain Amendment-57 record for G0-L0"
    )


def test_claude_md_records_g0_l0_and_reserved_successors() -> None:
    _declare("CLAUDE.md staging table entries")
    body = _CLAUDE.read_text(encoding="utf-8")
    assert "G0-L0   G₀ Bare Jamid Stem / Identity Anchor Zero-Layer Law" in body, (
        "CLAUDE.md PR staging must include G0-L0 done row"
    )
    for step in ("G0-C1", "G0-C2", "G0-C3", "G0-C4", "G0-C5", "G0-C6"):
        assert step in body, f"CLAUDE.md PR staging must reserve {step}"
