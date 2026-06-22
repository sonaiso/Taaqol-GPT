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


class TestGptK1AndR1Surface:
    """Hard-stop checks: GPT export surface stays boundary-only through GPT-R5."""

    def test_gpt_surface_matches_carrier_scope(self) -> None:
        assert set(gpt_module.__all__) == {
            "ClaimBoundary",
            "ExplicitClaim",
            "ExplicitRestriction",
            "GPT_MAFHUM_TRANSITION_CONTRACT",
            "GPT_ORIGIN_BINDING_TRANSITION_CONTRACT",
            "GPTAnswerInput",
            "InputContractSchemaError",
            "InputEvidenceNeed",
            "InputRiskLevel",
            "InputTimeSensitivity",
            "KnowledgeOrigin",
            "MafhumGPT",
            "MafhumGPTResult",
            "MafhumGPTSchemaError",
            "MafhumGPTState",
            "MafhumType",
            "MaqamCommunicationMode",
            "MaqamGPT",
            "MaqamGPTSchemaError",
            "MantuqGPT",
            "MantuqGPTSchemaError",
            "PreventerGateResult",
            "PreventerKind",
            "RestrictionKind",
            "ScopeBoundary",
            "SilenceNonMention",
            "bind_origin_to_claim",
            "build_mafhum_gpt",
            "build_maqam_gpt",
            "build_mantuq_gpt",
            "claim_from_mafhum",
            "claim_from_mantuq_boundary",
            "classify_maqam_communication_mode",
            "AttributeEventOrigin",
            "BindingVerdict",
            "EntityGenusOrigin",
            "EvidenceDirection",
            "EvidenceOrigin",
            "OriginBinding",
            "OriginBindingClaim",
            "OriginBindingGateResult",
            "OriginBindingGateSchemaError",
            "OriginBindingGateState",
            "OriginBindingSourceKind",
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

    def test_roadmap_declares_remaining_handoff_after_r4(self) -> None:
        content = _ROADMAP.read_text(encoding="utf-8")
        assert "GPT-R6 through GPT-R8" in content
