"""Acceptance tests for docs/55 — Knowledge Origins Boundary Law.

These are Layer 1 (document existence) and Layer 2 (contract surface)
tests. They verify that docs/55 exists and contains the constitutionally
required declarations.

Origin law     : docs/55 (Knowledge Origins Boundary Law)
Branch         : GPT-K0 (knowledge origins boundary)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

_DOCS_DIR = pathlib.Path(__file__).resolve().parent.parent / "docs"
_DOC_55 = _DOCS_DIR / "55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md"


# ---------------------------------------------------------------------------
# Layer 1 — Document existence
# ---------------------------------------------------------------------------


class TestDocs55Exists:
    """docs/55 must exist as the Knowledge Origins Boundary Law."""

    def test_docs_55_exists(self) -> None:
        assert _DOC_55.exists(), (
            "docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md must exist"
        )

    def test_docs_55_is_not_empty(self) -> None:
        content = _DOC_55.read_text(encoding="utf-8")
        assert len(content) > 500, "docs/55 must not be a stub"


# ---------------------------------------------------------------------------
# Layer 2 — Contract surface (required declarations)
# ---------------------------------------------------------------------------


def _read_doc() -> str:
    """Read docs/55 content, skipping if missing."""
    if not _DOC_55.exists():
        pytest.skip("docs/55 not yet created")
    return _DOC_55.read_text(encoding="utf-8")


class TestTransparentReasonablenessBarrier:
    """docs/55 must declare the Transparent Reasonableness Barrier framing."""

    def test_declares_transparent_reasonableness_barrier(self) -> None:
        content = _read_doc()
        assert "Transparent Reasonableness Barrier" in content

    def test_barrier_does_not_open_black_box(self) -> None:
        content = _read_doc()
        assert "Does NOT open the black box" in content

    def test_barrier_does_not_produce_truth_certificates(self) -> None:
        content = _read_doc()
        assert "Does NOT produce truth certificates" in content

    def test_barrier_does_not_prove_reality(self) -> None:
        content = _read_doc()
        assert "Does NOT prove that GPT" in content

    def test_barrier_proves_procedural_validity(self) -> None:
        content = _read_doc()
        assert "procedurally valid" in content or "procedural validity" in content

    def test_barrier_arabic_framing(self) -> None:
        content = _read_doc()
        assert "حاجز معقولية شفاف" in content


class TestKnowledgeOriginsDefined:
    """docs/55 must define all five Knowledge Origins."""

    def test_entity_genus_origin(self) -> None:
        content = _read_doc()
        assert "EntityGenusOrigin" in content

    def test_attribute_event_origin(self) -> None:
        content = _read_doc()
        assert "AttributeEventOrigin" in content

    def test_relation_operator_origin(self) -> None:
        content = _read_doc()
        assert "RelationOperatorOrigin" in content

    def test_reference_origin(self) -> None:
        content = _read_doc()
        assert "ReferenceOrigin" in content

    def test_evidence_origin(self) -> None:
        content = _read_doc()
        assert "EvidenceOrigin" in content

    def test_five_origins_table(self) -> None:
        content = _read_doc()
        # All five should appear in a table
        for origin in [
            "EntityGenusOrigin",
            "AttributeEventOrigin",
            "RelationOperatorOrigin",
            "ReferenceOrigin",
            "EvidenceOrigin",
        ]:
            assert origin in content, f"{origin} must appear in docs/55"


class TestOriginStructuralDefinitions:
    """docs/55 must provide structural definitions for each origin."""

    def test_entity_genus_has_required_fields(self) -> None:
        content = _read_doc()
        assert "entity_id" in content
        assert "genus" in content
        assert "bearing_capacity" in content

    def test_attribute_event_has_required_fields(self) -> None:
        content = _read_doc()
        assert "attribute_id" in content
        assert "required_conditions" in content

    def test_relation_operator_has_required_fields(self) -> None:
        content = _read_doc()
        assert "relation_id" in content
        assert "binding_semantics" in content

    def test_reference_has_required_fields(self) -> None:
        content = _read_doc()
        assert "reference_id" in content
        assert "referent" in content

    def test_evidence_has_required_fields(self) -> None:
        content = _read_doc()
        assert "evidence_type" in content
        assert "evidence_direction" in content
        assert "source_rank" in content


class TestOriginBinding:
    """docs/55 must define OriginBinding rules."""

    def test_origin_binding_defined(self) -> None:
        content = _read_doc()
        assert "OriginBinding" in content

    def test_binding_rules(self) -> None:
        content = _read_doc()
        assert "COMPATIBLE" in content
        assert "CONTRADICTED" in content
        assert "UNSUPPORTED" in content

    def test_binding_completeness(self) -> None:
        content = _read_doc()
        assert "BINDING_MISSING" in content or "binding is complete" in content.lower()


class TestOriginResidual:
    """docs/55 must define OriginResidual types."""

    def test_origin_residual_defined(self) -> None:
        content = _read_doc()
        assert "OriginResidual" in content

    def test_residual_types(self) -> None:
        content = _read_doc()
        expected_types = [
            "ORIGIN_ABSENT",
            "EVIDENCE_MISSING",
            "EVIDENCE_CONTRADICTED",
        ]
        for rt in expected_types:
            assert rt in content, f"OriginResidual type {rt} must be declared"

    def test_residuals_always_visible(self) -> None:
        content = _read_doc()
        assert "ALWAYS visible" in content or "always visible" in content.lower()


class TestNeedGateIntegration:
    """docs/55 must integrate with NeedGate from docs/54."""

    def test_needgate_referenced(self) -> None:
        content = _read_doc()
        assert "NeedGate" in content

    def test_conditional_origin_consultation(self) -> None:
        content = _read_doc()
        # Origins are consumed on demand
        assert "on demand" in content or "conditional" in content.lower()

    def test_not_unconditional_full_analysis(self) -> None:
        content = _read_doc()
        # Must forbid unconditional full analysis
        assert "unconditional" in content.lower()


class TestForbiddenOutputs:
    """docs/55 must declare forbidden outputs."""

    def test_forbids_verdict_without_origin_binding(self) -> None:
        content = _read_doc()
        assert "without origin binding" in content

    def test_forbids_truth_certification(self) -> None:
        content = _read_doc()
        # Must forbid Certificate/Truth terminology
        assert "Certificate" in content and "forbidden" in content.lower()

    def test_forbids_claiming_model_internals(self) -> None:
        content = _read_doc()
        assert "model internals" in content

    def test_forbids_euclidean_proof_terminology(self) -> None:
        content = _read_doc()
        assert "Euclidean" in content

    def test_forbids_judging_from_text_alone(self) -> None:
        content = _read_doc()
        assert "text alone" in content


class TestOriginRankAndStability:
    """docs/55 must define origin rank and stability classifications."""

    def test_rank_levels(self) -> None:
        content = _read_doc()
        assert "HIGH" in content
        assert "MEDIUM" in content
        assert "LOW" in content

    def test_stability_levels(self) -> None:
        content = _read_doc()
        assert "PERMANENT" in content
        assert "PERIOD_BOUND" in content
        assert "CONTESTED" in content


class TestBindingDeclarations:
    """docs/55 must declare binding status."""

    def test_binding_for_gpt_k_family(self) -> None:
        content = _read_doc()
        assert "GPT-K" in content

    def test_docs_54_remains_binding(self) -> None:
        content = _read_doc()
        assert "docs/54" in content

    def test_opens_gpt_k1(self) -> None:
        content = _read_doc()
        assert "GPT-K1" in content

    def test_defers_docs_56(self) -> None:
        content = _read_doc()
        assert "docs/56" in content and "deferred" in content.lower()


class TestProceduralValidityDistinction:
    """docs/55 must maintain the procedural vs absolute truth distinction."""

    def test_not_absolute_truth(self) -> None:
        content = _read_doc()
        assert "absolutely true" in content.lower() or "absolute truth" in content.lower()

    def test_procedurally_justified(self) -> None:
        content = _read_doc()
        assert "procedurally justified" in content or "procedurally valid" in content
