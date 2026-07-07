"""Constitutional/runtime tests for LGE-C1..LGE-C5 runtime coverage.

Origin law     : docs/79_LICENSED_SURFACE_GEOMETRY_MINIMAL_COMPLETE_LAW.md
Branch         : LGE-C1..LGE-C5 runtime surfaces
Category       : Category 2 — contract/surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.lge.c1_surface_token_runtime import (
    LGE_C1_FORBIDDEN_OUTPUTS,
    LgeC1TokenFamily,
    emit_lge_c1_surface_token,
)
from taaqqul_slot_geometry.lge.c2_sentence_slot_runtime import (
    LGE_C2_FORBIDDEN_OUTPUTS,
    LgeC2RuntimeStatus,
    LgeC2SentenceFamily,
    prove_lge_c2_sentence_slot,
)
from taaqqul_slot_geometry.lge.c3_relation_slot_runtime import (
    LGE_C3_FORBIDDEN_OUTPUTS,
    LgeC3RelationFamily,
    LgeC3RuntimeStatus,
    prove_lge_c3_relation_slot,
)
from taaqqul_slot_geometry.lge.c4_inflection_mark_runtime import (
    LGE_C4_FORBIDDEN_OUTPUTS,
    LgeC4MarkFamily,
    LgeC4RuntimeStatus,
    prove_lge_c4_inflection_surface,
)
from taaqqul_slot_geometry.lge.c5_style_slot_runtime import (
    LGE_C5_FORBIDDEN_OUTPUTS,
    LgeC5RuntimeStatus,
    LgeC5StyleFamily,
    prove_lge_c5_style_surface,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"

_ORIGIN = "docs/79_LICENSED_SURFACE_GEOMETRY_MINIMAL_COMPLETE_LAW.md"
_CHAIN = ("LGE-L0", "LGE-C1", "LGE-C2", "LGE-C3", "LGE-C4", "LGE-C5")


_ALL_FORBIDDEN = tuple(
    sorted(
        set(
            LGE_C1_FORBIDDEN_OUTPUTS
            + LGE_C2_FORBIDDEN_OUTPUTS
            + LGE_C3_FORBIDDEN_OUTPUTS
            + LGE_C4_FORBIDDEN_OUTPUTS
            + LGE_C5_FORBIDDEN_OUTPUTS
        )
    )
)


def _declare(branch_name: str, produced_outputs: frozenset[str]) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=_ALL_FORBIDDEN,
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=produced_outputs,
    )
    assert_constitutional_case(case, result)


def _build_full_chain():
    c1 = emit_lge_c1_surface_token(
        input_ref="lge://c1/input",
        family=LgeC1TokenFamily.LETTER_HARAKA,
        token="بَ",
        trace_ref="trace://lge/c1/token",
        residuals=("LGE_C1_SURFACE_FORMAL_ONLY",),
    )
    c2 = prove_lge_c2_sentence_slot(
        upstream_token=c1,
        family=LgeC2SentenceFamily.NOMINAL,
        input_ref="lge://c2/input",
        trace_ref="trace://lge/c2/slot",
    )
    c3 = prove_lge_c3_relation_slot(
        upstream_slot=c2.slot,
        family=LgeC3RelationFamily.ISNADI,
        input_ref="lge://c3/input",
        trace_ref="trace://lge/c3/slot",
    )
    c4 = prove_lge_c4_inflection_surface(
        upstream_slot=c3.slot,
        family=LgeC4MarkFamily.ORIGINAL,
        input_ref="lge://c4/input",
        trace_ref="trace://lge/c4/surface",
    )
    c5 = prove_lge_c5_style_surface(
        upstream_surface=c4.surface,
        family=LgeC5StyleFamily.AKHBAR,
        input_ref="lge://c5/input",
        trace_ref="trace://lge/c5/surface",
    )
    return c1, c2, c3, c4, c5


def test_chain_records_lge_c1_through_lge_c5_done() -> None:
    _declare("chain registration for lge runtime steps", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    labels = (
        "LGE-C1  surface token carrier runtime",
        "LGE-C2  sentence-slot runtime",
        "LGE-C3  relation-engineering slot runtime",
        "LGE-C4  inflection-mark surface runtime",
        "LGE-C5  style-slot runtime",
    )
    for label in labels:
        assert label in roadmap and "✓ done" in roadmap.split(label, maxsplit=1)[1][:80]
        assert label in claude and "✓ done" in claude.split(label, maxsplit=1)[1][:80]


def test_lge_c1_emits_surface_token() -> None:
    _declare("lge-c1 surface token emission", frozenset({"LGE_C1_SURFACE_TOKEN"}))
    c1 = emit_lge_c1_surface_token(
        input_ref="lge://c1/input",
        family=LgeC1TokenFamily.SYLLABLE,
        token="مق",
        trace_ref="trace://lge/c1/syllable",
    )
    assert c1.family is LgeC1TokenFamily.SYLLABLE
    assert c1.trace_ref == "trace://lge/c1/syllable"


def test_lge_c2_refuses_when_upstream_is_not_lge_c1() -> None:
    _declare("lge-c2 upstream guard", frozenset())
    verdict = prove_lge_c2_sentence_slot(
        upstream_token=object(),
        family=LgeC2SentenceFamily.NOMINAL,
        input_ref="lge://c2/input",
        trace_ref="trace://lge/c2/refusal",
    )
    assert verdict.status is LgeC2RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.GATE_REQUIRED


def test_lge_c3_refuses_when_upstream_is_not_lge_c2() -> None:
    _declare("lge-c3 upstream guard", frozenset())
    verdict = prove_lge_c3_relation_slot(
        upstream_slot=object(),
        family=LgeC3RelationFamily.TAQYIDI,
        input_ref="lge://c3/input",
        trace_ref="trace://lge/c3/refusal",
    )
    assert verdict.status is LgeC3RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.GATE_REQUIRED


def test_lge_c4_refuses_when_upstream_is_not_lge_c3() -> None:
    _declare("lge-c4 upstream guard", frozenset())
    verdict = prove_lge_c4_inflection_surface(
        upstream_slot=object(),
        family=LgeC4MarkFamily.SUBSIDIARY,
        input_ref="lge://c4/input",
        trace_ref="trace://lge/c4/refusal",
    )
    assert verdict.status is LgeC4RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.GATE_REQUIRED


def test_lge_c5_refuses_when_upstream_is_not_lge_c4() -> None:
    _declare("lge-c5 upstream guard", frozenset())
    verdict = prove_lge_c5_style_surface(
        upstream_surface=object(),
        family=LgeC5StyleFamily.INSHA,
        input_ref="lge://c5/input",
        trace_ref="trace://lge/c5/refusal",
    )
    assert verdict.status is LgeC5RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.GATE_REQUIRED


def test_lge_runtime_chain_closes_surface_only_without_semantic_outputs() -> None:
    _declare(
        "lge-c1..lge-c5 full runtime chain",
        frozenset(
            {
                "LGE_C1_SURFACE_TOKEN",
                "LGE_C2_SENTENCE_SLOT",
                "LGE_C3_RELATION_SLOT",
                "LGE_C4_INFLECTION_MARK_SLOT",
                "LGE_C5_STYLE_SLOT",
            }
        ),
    )
    c1, c2, c3, c4, c5 = _build_full_chain()

    assert c2.status is LgeC2RuntimeStatus.RUNTIME_GATES_CLOSED
    assert c3.status is LgeC3RuntimeStatus.RUNTIME_GATES_CLOSED
    assert c4.status is LgeC4RuntimeStatus.RUNTIME_GATES_CLOSED
    assert c5.status is LgeC5RuntimeStatus.RUNTIME_GATES_CLOSED

    assert "Hukm" in c1.forbidden_outputs
    assert "Hukm" in c2.slot.forbidden_outputs
    assert "Hukm" in c3.slot.forbidden_outputs
    assert "Hukm" in c4.surface.forbidden_outputs
    assert "Hukm" in c5.surface.forbidden_outputs


def test_lge_c1_trace_must_be_trace_ref() -> None:
    _declare("lge-c1 trace schema guard", frozenset())
    with pytest.raises(TypeError):
        emit_lge_c1_surface_token(
            input_ref="lge://c1/input",
            family=LgeC1TokenFamily.TOOLS,
            token="أداة",
            trace_ref="lge/c1/missing-prefix",
        )
