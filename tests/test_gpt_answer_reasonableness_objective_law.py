"""Acceptance tests for docs/54 — GPT Answer Reasonableness Objective Law.

These are Layer 1 (document existence) and Layer 2 (contract surface)
tests. They verify that docs/54 exists and contains the constitutionally
required declarations.

Origin law     : docs/54 (GPT Answer Reasonableness Objective Law)
Branch         : GPT-R0 (operational objective correction)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

_DOCS_DIR = pathlib.Path(__file__).resolve().parent.parent / "docs"
_DOC_54 = _DOCS_DIR / "54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md"


# ---------------------------------------------------------------------------
# Layer 1 — Document existence
# ---------------------------------------------------------------------------


class TestDocs54Exists:
    """docs/54 must exist as the GPT reasonableness objective law."""

    def test_docs_54_exists(self) -> None:
        assert _DOC_54.exists(), (
            "docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md must exist"
        )

    def test_docs_54_is_not_empty(self) -> None:
        content = _DOC_54.read_text(encoding="utf-8")
        assert len(content) > 500, "docs/54 must not be a stub"


# ---------------------------------------------------------------------------
# Layer 2 — Contract surface (required declarations)
# ---------------------------------------------------------------------------


def _read_doc() -> str:
    """Read docs/54 content, skipping if missing."""
    if not _DOC_54.exists():
        pytest.skip("docs/54 not yet created")
    return _DOC_54.read_text(encoding="utf-8")


class TestDocs54DefinesGPTReasonableness:
    """docs/54 must define GPT answer reasonableness as the objective."""

    def test_docs_54_defines_gpt_reasonableness(self) -> None:
        content = _read_doc()
        assert "GPT answer reasonableness" in content or "Reasonableness" in content, (
            "docs/54 must define GPT answer reasonableness as the objective"
        )

    def test_docs_54_declares_operational_objective(self) -> None:
        content = _read_doc()
        assert "Operational Objective" in content or "operational objective" in content, (
            "docs/54 must declare the operational objective (§1)"
        )

    def test_docs_54_forbids_analysis_for_own_sake(self) -> None:
        content = _read_doc()
        assert "not" in content.lower() and "for its own sake" in content, (
            "docs/54 must forbid Arabic analysis for its own sake"
        )


class TestDocs54DefinesMantuqGPT:
    """docs/54 must define MantuqGPT as explicit claims."""

    def test_docs_54_defines_mantuq_gpt(self) -> None:
        content = _read_doc()
        assert "MantuqGPT" in content, (
            "docs/54 must define MantuqGPT"
        )

    def test_docs_54_mantuq_is_explicit_claims(self) -> None:
        content = _read_doc()
        assert "explicit claim" in content.lower(), (
            "docs/54 must define MantuqGPT as explicit claims"
        )


class TestDocs54DefinesMafhumGPT:
    """docs/54 must define MafhumGPT as implicit commitments."""

    def test_docs_54_defines_mafhum_gpt(self) -> None:
        content = _read_doc()
        assert "MafhumGPT" in content, (
            "docs/54 must define MafhumGPT"
        )

    def test_docs_54_mafhum_is_implicit_commitments(self) -> None:
        content = _read_doc()
        assert "implicit commitment" in content.lower() or "implicit" in content.lower(), (
            "docs/54 must define MafhumGPT as implicit commitments/risks"
        )

    def test_docs_54_mafhum_requires_mantuq(self) -> None:
        content = _read_doc()
        assert "MafhumGPT requires MantuqGPT" in content or "No mafhūm without manṭūq" in content, (
            "docs/54 must declare that MafhumGPT requires MantuqGPT"
        )


class TestDocs54DefinesMaqamGPT:
    """docs/54 must define MaqamGPT as user constraints."""

    def test_docs_54_defines_maqam_gpt(self) -> None:
        content = _read_doc()
        assert "MaqamGPT" in content, (
            "docs/54 must define MaqamGPT"
        )

    def test_docs_54_maqam_has_required_fields(self) -> None:
        content = _read_doc()
        required_fields = ["question_type", "domain", "evidence_need", "risk_level"]
        for field in required_fields:
            assert field in content, (
                f"docs/54 MaqamGPT must declare field: {field}"
            )


class TestDocs54DeclaresNeedGate:
    """docs/54 must declare the NeedGate principle."""

    def test_docs_54_declares_need_gate(self) -> None:
        content = _read_doc()
        assert "NeedGate" in content, (
            "docs/54 must declare the NeedGate principle"
        )

    def test_docs_54_need_gate_is_conditional(self) -> None:
        content = _read_doc()
        assert "conditional" in content.lower() or "unless needed" in content.lower(), (
            "docs/54 NeedGate must declare analysis is conditional"
        )


class TestDocs54DeclaresKnowledgeOrigins:
    """docs/54 must declare the five Knowledge Origins."""

    def test_docs_54_declares_entity_genus_origin(self) -> None:
        content = _read_doc()
        assert "EntityGenusOrigin" in content, (
            "docs/54 must declare EntityGenusOrigin"
        )

    def test_docs_54_declares_attribute_event_origin(self) -> None:
        content = _read_doc()
        assert "AttributeEventOrigin" in content, (
            "docs/54 must declare AttributeEventOrigin"
        )

    def test_docs_54_declares_relation_operator_origin(self) -> None:
        content = _read_doc()
        assert "RelationOperatorOrigin" in content, (
            "docs/54 must declare RelationOperatorOrigin"
        )

    def test_docs_54_declares_reference_origin(self) -> None:
        content = _read_doc()
        assert "ReferenceOrigin" in content, (
            "docs/54 must declare ReferenceOrigin"
        )

    def test_docs_54_declares_evidence_origin(self) -> None:
        content = _read_doc()
        assert "EvidenceOrigin" in content, (
            "docs/54 must declare EvidenceOrigin"
        )

    def test_docs_54_five_origins_count(self) -> None:
        content = _read_doc()
        origins = [
            "EntityGenusOrigin",
            "AttributeEventOrigin",
            "RelationOperatorOrigin",
            "ReferenceOrigin",
            "EvidenceOrigin",
        ]
        found = sum(1 for o in origins if o in content)
        assert found == 5, (
            f"docs/54 must declare all 5 Knowledge Origins, found {found}"
        )


class TestDocs54DeclaresReasonablenessVerdict:
    """docs/54 must declare the ReasonablenessVerdict."""

    def test_docs_54_declares_reasonableness_verdict(self) -> None:
        content = _read_doc()
        assert "GPTAnswerReasonablenessVerdict" in content or "ReasonablenessVerdict" in content, (
            "docs/54 must declare the GPTAnswerReasonablenessVerdict"
        )

    def test_docs_54_verdict_states_include_unreasonable(self) -> None:
        content = _read_doc()
        assert "UNREASONABLE" in content, (
            "docs/54 verdict states must include UNREASONABLE"
        )

    def test_docs_54_verdict_states_include_reasonable(self) -> None:
        content = _read_doc()
        assert "REASONABLE" in content, (
            "docs/54 verdict states must include REASONABLE"
        )

    def test_docs_54_verdict_states_include_origin_contradiction(self) -> None:
        content = _read_doc()
        assert "ORIGIN_CONTRADICTION" in content, (
            "docs/54 verdict states must include ORIGIN_CONTRADICTION"
        )

    def test_docs_54_verdict_states_include_forbidden_leap(self) -> None:
        content = _read_doc()
        assert "FORBIDDEN_LEAP" in content, (
            "docs/54 verdict states must include FORBIDDEN_LEAP"
        )


class TestDocs54ForbiddenOutputs:
    """docs/54 must declare forbidden outputs."""

    def test_docs_54_forbids_verdict_as_certificate(self) -> None:
        content = _read_doc()
        assert "certificate" in content.lower(), (
            "docs/54 must forbid treating verdict as certificate"
        )

    def test_docs_54_forbids_verdict_as_truth(self) -> None:
        content = _read_doc()
        assert "truth" in content.lower(), (
            "docs/54 must forbid treating verdict as truth declaration"
        )

    def test_docs_54_forbids_hidden_residuals(self) -> None:
        content = _read_doc()
        assert "hidden residual" in content.lower() or "Hidden residuals" in content, (
            "docs/54 must forbid hidden residuals in verdicts"
        )


class TestDocs54DeclaresRoadmap:
    """docs/54 must declare the GPT-R branch family roadmap."""

    def test_docs_54_declares_gpt_r_family(self) -> None:
        content = _read_doc()
        assert "GPT-R" in content, (
            "docs/54 must declare the GPT-R branch family"
        )

    def test_docs_54_roadmap_includes_gpt_k0(self) -> None:
        content = _read_doc()
        assert "GPT-K0" in content, (
            "docs/54 roadmap must include GPT-K0 as next step"
        )

    def test_docs_54_roadmap_includes_gpt_r7(self) -> None:
        content = _read_doc()
        assert "GPT-R7" in content, (
            "docs/54 roadmap must include GPT-R7 (final verdict)"
        )


class TestDocs54DeclaresKPIs:
    """docs/54 must declare measurable KPIs."""

    def test_docs_54_kpi_origin_contradiction_zero(self) -> None:
        content = _read_doc()
        assert "0 false accept" in content.lower() or "0 false" in content, (
            "docs/54 KPIs must require 0 false accepts for origin contradiction"
        )

    def test_docs_54_kpi_need_gate_zero(self) -> None:
        content = _read_doc()
        assert "0 unconditional" in content.lower(), (
            "docs/54 KPIs must require 0 unconditional Arabic analysis"
        )
