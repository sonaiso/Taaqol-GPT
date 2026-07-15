"""Constitutional surface tests for docs/92 integrated slot-engineering proposal.

Origin law          : docs/13_CONSTITUTIONAL_PR_GEOMETRY.md
Branch name         : DOC92-SLOT-ENGINEERING-PROPOSAL
Constitutional chain: docs/12 -> docs/13 -> docs/92
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOC_92 = _REPO_ROOT / "docs" / "92_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_SLOTS_90_113.md"


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/13_CONSTITUTIONAL_PR_GEOMETRY.md",
        branch_name=f"DOC92-SLOT-ENGINEERING-PROPOSAL ({branch_note})",
        constitutional_chain=("docs/12", "docs/13", "docs/92"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeOpeningClaim",
            "RatificationClaim",
            "ChainMutationClaim",
            "CertificateIssuanceClaim",
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


def _body() -> str:
    return _DOC_92.read_text(encoding="utf-8")


def test_docs_92_declares_proposal_scope_and_no_runtime_opening() -> None:
    _declare("proposal-only boundary")
    body = _body()
    assert (
        "Status: architectural constitutional proposal "
        "(proposal-only, non-ratified chain step)."
    ) in body
    assert "No chain amendment claim in this document." in body
    assert "No runtime opening claim in this document." in body
    assert "DOC92_STATUS = PROPOSAL_ONLY" in body


def test_docs_92_declares_slot_licensed_transition_contract() -> None:
    _declare("slot transition licensing contract")
    body = _body()
    for marker in (
        "SlotLicensedTransition(X -> Y)",
        "X has closed its MRK",
        "Y demand is declared",
        "trace is replayable",
        "residuals are visible",
        "rank policy allows the transition",
        "no forbidden shortcut is crossed",
    ):
        assert marker in body


def test_docs_92_declares_mandatory_template_and_readiness_only() -> None:
    _declare("template and readiness-only discipline")
    body = _body()
    for marker in (
        "SLOT NAME:",
        "القابلية المكشوفة:",
        "السطح اللغوي:",
        "المدخل:",
        "المخرج المسموح:",
        "المخرج الممنوع:",
        "MRK:",
        "البقايا:",
        "الجوار:",
        "القفزات الممنوعة:",
        "المثال الأدنى:",
        "Readiness/Candidate output only.",
        "No certificate/truth/hukm closure at slot-level.",
    ):
        assert marker in body


def test_docs_92_registers_full_slot_range_90_to_113() -> None:
    _declare("full slot registry markers")
    body = _body()
    for slot in (
        "## 90 — PHON-L0",
        "## 91 — SYLLABLE-L0",
        "## 92 — ROOT-L0",
        "## 93 — WEIGHT-REBASE-L0",
        "## 94 — SOURCE-L0",
        "## 95 — MUJARRAD-L0",
        "## 96 — MAZID-L0",
        "## 97 — DERIVED-NOUN-L0",
        "## 98 — HARF-L0",
        "## 99 — AMIL-L0",
        "## 100 — IRAB-L0",
        "## 101 — NAWASIKH-L0",
        "## 102 — SENTENCE-FORM-L0",
        "## 103 — SUBREL-L0",
        "## 104 — USLUB-L0",
        "## 105 — MAQAM-L0",
        "## 106 — CONFLICT-L0",
        "## 107 — DISCOURSE-L0",
        "## 108 — ELLIPSIS-L0",
        "## 109 — QUANT-L0",
        "## 110 — NEGATION-L0",
        "## 111 — EVIDENCE-L0",
        "## 112 — TRACE-REPLAY-L0",
        "## 113 — RANK-POLICY-L0",
    ):
        assert slot in body


def test_docs_92_declares_wave_order_and_early_governance_priority() -> None:
    _declare("wave decomposition and governance prioritization")
    body = _body()
    for marker in (
        "Wave 1: 90 PHON-L0, 91 SYLLABLE-L0, 92 ROOT-L0, 93 WEIGHT-REBASE-L0",
        "Wave 6: 111 EVIDENCE-L0, 112 TRACE-REPLAY-L0, 113 RANK-POLICY-L0",
        "Constitutional priority allows promoting 111/112/113 immediately after Wave 1",
    ):
        assert marker in body
