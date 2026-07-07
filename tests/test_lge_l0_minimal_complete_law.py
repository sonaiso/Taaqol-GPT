"""Acceptance tests for docs/79 — Licensed Surface Geometry Minimal-Complete Law.

Origin law     : docs/14_PR_CHAIN_ROADMAP.md (Amendment-67 / LGE-L0)
Branch         : LGE-L0 (law-only branch origin)
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
_DOC_79 = _REPO_ROOT / "docs" / "79_LICENSED_SURFACE_GEOMETRY_MINIMAL_COMPLETE_LAW.md"
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"


def _declare(branch_note: str) -> None:
    assert _DOC_79.exists(), "docs/79 must exist"
    assert _DOC_14.exists(), "docs/14_PR_CHAIN_ROADMAP.md must exist"
    assert _CLAUDE.exists(), "CLAUDE.md must exist"

    case = ConstitutionalChainTestCase(
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"LGE-L0 ({branch_note})",
        constitutional_chain=("X0R-E2", "LGE-L0"),
        chain_position="LGE-L0",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md#1-per-step-boundary-summary",
        branch_of_origin="Licensed surface geometry minimum-complete law-only origin",
        forbidden_shortcut_assertions=(
            "SurfaceToken -> Meaning",
            "SentenceSlot -> Ifadah",
            "RelationSlot -> Hukm",
            "IrabMark -> Truth",
            "StyleSlot -> Certainty",
            "LGE-L0 -> Runtime",
            "LGE-L0 -> BranchClosure",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeCode",
            "Carrier",
            "Gate",
            "VerdictEngine",
            "SemanticOutput",
            "Ifadah",
            "Mafhum",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
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


def test_docs_79_exists_and_declares_lge_identity() -> None:
    _declare("document presence and identity")
    body = _DOC_79.read_text(encoding="utf-8")
    for marker in (
        "79 — Licensed Surface Geometry Minimal-Complete Law",
        "FAMILY               = LGE",
        "STEP                 = LGE-L0",
        "STEP_KIND            = LAW_ONLY",
        "DOMAIN               = SURFACE_NUMERIC_GEOMETRY",
        "TRANSITION_RULE      = MINIMUM_COMPLETE_REQUIRED",
    ):
        assert marker in body, f"docs/79 missing required marker: {marker}"


def test_docs_79_declares_surface_token_family() -> None:
    _declare("surface token family")
    body = _DOC_79.read_text(encoding="utf-8")
    for marker in (
        "حرف + حركة token",
        "مقطع token",
        "الاقتصاد الصوتي token",
        "أدوات token",
        "مبنيات token",
        "وزن جامد token",
        "وزن مشتق token",
        "مشتقات token",
        "اسم / فعل / حرف surface closure token",
    ):
        assert marker in body, f"docs/79 missing token family marker: {marker}"


def test_docs_79_declares_sentence_relation_i3rab_style_surfaces() -> None:
    _declare("slot/relation/inflection/style families")
    body = _DOC_79.read_text(encoding="utf-8")
    for marker in (
        "الجملة الاسمية",
        "الجملة الفعلية",
        "شبه جملة",
        "النسب الإسنادية",
        "النسب التضمينية",
        "النسب التقييدية",
        "العلامات الإعرابية الأصلية",
        "العلامات الإعرابية الفرعية",
        "الأخبار",
        "الإنشاء",
    ):
        assert marker in body, f"docs/79 missing surface marker: {marker}"


def test_docs_79_declares_minimum_complete_conditions() -> None:
    _declare("minimum-complete conditions")
    body = _DOC_79.read_text(encoding="utf-8")
    for marker in (
        "origin law is declared",
        "branch step is declared",
        "constitutional chain position is declared",
        "trace is present",
        "rank ceiling is declared",
        "residual visibility is enforced",
        "forbidden outputs are declared",
    ):
        assert marker in body, f"docs/79 missing minimum-complete condition: {marker}"


def test_docs_79_reserves_successor_steps() -> None:
    _declare("reserved successor steps")
    body = _DOC_79.read_text(encoding="utf-8")
    for step in ("LGE-C1", "LGE-C2", "LGE-C3", "LGE-C4", "LGE-C5"):
        assert step in body, f"docs/79 must reserve {step}"


def test_docs_79_declares_law_only_forbidden_surface() -> None:
    _declare("law-only forbidden surface")
    body = _DOC_79.read_text(encoding="utf-8")
    lowered = body.lower()
    for marker in (
        "law-only",
        "no runtime code",
        "no semantic",
        "FORBIDDEN_LEAP",
    ):
        assert marker.lower() in lowered, f"docs/79 must declare: {marker}"


def test_docs_14_records_lge_l0_chain_row_and_per_step_boundary_block() -> None:
    _declare("docs/14 chain synchronization")
    body = _DOC_14.read_text(encoding="utf-8")
    assert "LGE-L0  Licensed Surface Geometry Minimal-Complete Law" in body
    assert "LGE-L0\n    Origin   :" in body
    assert "Amendment-67 (LGE-L0" in body


def test_claude_records_lge_l0_and_reserved_successors() -> None:
    _declare("CLAUDE.md synchronization")
    body = _CLAUDE.read_text(encoding="utf-8")
    assert "LGE-L0  Licensed Surface Geometry Minimal-Complete Law" in body
    for step in ("LGE-C1", "LGE-C2", "LGE-C3", "LGE-C4", "LGE-C5"):
        assert step in body
