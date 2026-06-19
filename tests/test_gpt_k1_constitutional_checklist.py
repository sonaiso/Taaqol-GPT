"""Executable constitutional checklist for GPT-K1 carrier-only scope.

Origin law     : docs/55 (Knowledge Origins Boundary Law)
Branch         : GPT-K1 (Origin Schema Carriers)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses
import pathlib

import taaqqul_slot_geometry.gpt as gpt_module
from taaqqul_slot_geometry.gpt import (
    AttributeEventOrigin,
    BindingVerdict,
    EntityGenusOrigin,
    EvidenceOrigin,
    OriginBinding,
    OriginResidual,
    OriginResidualKind,
    ReferenceOrigin,
    RelationOperatorOrigin,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_ROADMAP = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"


class TestGptK1CarrierOnlySurface:
    """Hard-stop checks: GPT-K1 exports only the licensed carrier surface."""

    def test_gpt_k1_export_surface_matches_carrier_scope(self) -> None:
        assert set(gpt_module.__all__) == {
            "AttributeEventOrigin",
            "BindingVerdict",
            "EntityGenusOrigin",
            "EvidenceDirection",
            "EvidenceOrigin",
            "OriginBinding",
            "OriginCarrierSchemaError",
            "OriginRank",
            "OriginResidual",
            "OriginResidualKind",
            "OriginStability",
            "ReferenceOrigin",
            "RelationOperatorOrigin",
            "ResolutionType",
        }

    def test_no_forbidden_runtime_symbols_are_exported(self) -> None:
        forbidden_symbols = {
            "GPTAnswerReasonablenessVerdict",
            "ReasonablenessVerdict",
            "MaqamGPT",
            "MantuqGPT",
            "MafhumGPT",
            "NeedGate",
            "Pipeline",
            "TransitionGate",
            "Bridge",
            "Certificate",
        }
        assert forbidden_symbols.isdisjoint(set(gpt_module.__all__))


class TestGptK1ProofDiscipline:
    """Schema-level discipline checks inside GPT-K1 carriers."""

    def test_no_boolean_as_proof_fields_in_k1_carriers(self) -> None:
        carriers = (
            EntityGenusOrigin,
            AttributeEventOrigin,
            RelationOperatorOrigin,
            ReferenceOrigin,
            EvidenceOrigin,
            OriginResidual,
            OriginBinding,
        )
        for carrier in carriers:
            assert all(field.type is not bool for field in dataclasses.fields(carrier))

    def test_origin_binding_keeps_residuals_visible_and_structured(self) -> None:
        residual = OriginResidual(
            kind=OriginResidualKind.EVIDENCE_CONTRADICTED,
            description="Evidence refutes claim",
            claim_ref="claim/1",
        )
        binding = OriginBinding(
            claim_ref="claim/1",
            origin_type="EvidenceOrigin",
            origin_id="evidence/1",
            verdict=BindingVerdict.CONTRADICTED,
            residuals=(residual,),
            trace_ref="trace://gpt-k1/binding/1",
        )
        assert isinstance(binding.residuals, tuple)
        assert binding.residuals and all(
            isinstance(item, OriginResidual) for item in binding.residuals
        )
        assert binding.trace_ref.startswith("trace://")


class TestGptK1HandoffVisibility:
    """Checklist handoff: next steps remain deferred to licensed chain rows."""

    def test_roadmap_declares_deferred_handoff_to_k2_and_r1(self) -> None:
        content = _ROADMAP.read_text(encoding="utf-8")
        assert "Deferred : GPT-K2 (Golden Dataset), GPT-R1 through GPT-R8" in content
