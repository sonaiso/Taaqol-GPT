"""Acceptance tests for GPT-K1 — Origin Schema Carriers.

These tests verify that the five Knowledge Origin carriers, OriginBinding,
and OriginResidual carriers exist, enforce their schema constraints, and
produce frozen immutable instances as declared in docs/55.

Origin law     : docs/55 (Knowledge Origins Boundary Law)
Branch         : GPT-K1 (origin schema carriers)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses

import pytest

from taaqqul_slot_geometry.gpt import (
    AttributeEventOrigin,
    BindingVerdict,
    EntityGenusOrigin,
    EvidenceDirection,
    EvidenceOrigin,
    OriginBinding,
    OriginCarrierSchemaError,
    OriginRank,
    OriginResidual,
    OriginResidualKind,
    OriginStability,
    ReferenceOrigin,
    RelationOperatorOrigin,
    ResolutionType,
)

# ---------------------------------------------------------------------------
# Helpers — canonical test instances
# ---------------------------------------------------------------------------


def _make_entity_genus() -> EntityGenusOrigin:
    return EntityGenusOrigin(
        entity_id="moon",
        genus="celestial body / natural satellite",
        essential_properties=("reflects light", "orbits Earth"),
        bearing_capacity=("illumination (reflected)", "orbital motion"),
        bearing_refusal=("self-luminosity", "atmosphere"),
        domain="physical astronomy",
        stability=OriginStability.PERMANENT,
        source_ref="established astronomy",
        rank=OriginRank.HIGH,
        residuals=("exact albedo values",),
    )


def _make_attribute_event() -> AttributeEventOrigin:
    return AttributeEventOrigin(
        attribute_id="self_luminous",
        required_conditions=("internal energy source",),
        contradicting_conditions=("receives all light from external source",),
        typical_bearers=("stars", "bioluminescent organisms"),
        impossible_bearers=("natural satellites",),
        domain="physical optics",
        stability=OriginStability.PERMANENT,
        source_ref="established physics",
        rank=OriginRank.HIGH,
        residuals=("edge cases",),
    )


def _make_relation_operator() -> RelationOperatorOrigin:
    return RelationOperatorOrigin(
        relation_id="causal_bi",
        argument_structure="entity (source) — event (caused)",
        presuppositions=("source has causal power for the event",),
        binding_semantics="X is the source/cause of Y",
        domain="causal relations",
        stability=OriginStability.PERMANENT,
        source_ref="Arabic grammar + causal logic",
        rank=OriginRank.HIGH,
        residuals=("figurative uses",),
    )


def _make_reference() -> ReferenceOrigin:
    return ReferenceOrigin(
        reference_id="dhatihi",
        referent="the moon",
        resolution_type=ResolutionType.ANAPHORIC,
        confidence=OriginRank.HIGH,
        domain="textual reference",
        maqam_dependency=OriginRank.LOW,
        residuals=(),
    )


def _make_evidence() -> EvidenceOrigin:
    return EvidenceOrigin(
        claim_ref="the moon is self-luminous",
        evidence_type="scientific consensus",
        evidence_direction=EvidenceDirection.REFUTES,
        evidence_content="the moon reflects sunlight; no internal light source",
        source="established astronomy (NASA, IAU)",
        source_rank=OriginRank.HIGH,
        recency=OriginStability.PERMANENT,
        domain="physical astronomy",
        stability=OriginStability.PERMANENT,
        residuals=("exact reflectance percentages",),
        contradiction_with=("the claim itself",),
    )


def _make_origin_residual() -> OriginResidual:
    return OriginResidual(
        kind=OriginResidualKind.EVIDENCE_CONTRADICTED,
        description="Evidence refutes the claim",
        claim_ref="the moon is self-luminous",
    )


def _make_origin_binding() -> OriginBinding:
    return OriginBinding(
        claim_ref="the moon is self-luminous",
        origin_type="EvidenceOrigin",
        origin_id="evidence_moon_self_luminous",
        verdict=BindingVerdict.CONTRADICTED,
        residuals=(_make_origin_residual(),),
        trace_ref="trace://gpt-k1/binding/001",
    )


# ---------------------------------------------------------------------------
# Test: Module export surface
# ---------------------------------------------------------------------------


class TestModuleExports:
    """All GPT-K1 carriers must be importable from the gpt package."""

    def test_entity_genus_origin_importable(self) -> None:
        assert EntityGenusOrigin is not None

    def test_attribute_event_origin_importable(self) -> None:
        assert AttributeEventOrigin is not None

    def test_relation_operator_origin_importable(self) -> None:
        assert RelationOperatorOrigin is not None

    def test_reference_origin_importable(self) -> None:
        assert ReferenceOrigin is not None

    def test_evidence_origin_importable(self) -> None:
        assert EvidenceOrigin is not None

    def test_origin_binding_importable(self) -> None:
        assert OriginBinding is not None

    def test_origin_residual_importable(self) -> None:
        assert OriginResidual is not None

    def test_origin_residual_kind_importable(self) -> None:
        assert OriginResidualKind is not None

    def test_origin_rank_importable(self) -> None:
        assert OriginRank is not None

    def test_origin_stability_importable(self) -> None:
        assert OriginStability is not None

    def test_binding_verdict_importable(self) -> None:
        assert BindingVerdict is not None

    def test_evidence_direction_importable(self) -> None:
        assert EvidenceDirection is not None

    def test_resolution_type_importable(self) -> None:
        assert ResolutionType is not None

    def test_origin_carrier_schema_error_importable(self) -> None:
        assert OriginCarrierSchemaError is not None


# ---------------------------------------------------------------------------
# Test: Enum completeness (docs/55 declarations)
# ---------------------------------------------------------------------------


class TestEnumCompleteness:
    """Enum members must match docs/55 declarations."""

    def test_origin_rank_has_four_members(self) -> None:
        assert set(OriginRank) == {
            OriginRank.HIGH,
            OriginRank.MEDIUM,
            OriginRank.LOW,
            OriginRank.UNKNOWN,
        }

    def test_origin_stability_has_four_members(self) -> None:
        assert set(OriginStability) == {
            OriginStability.PERMANENT,
            OriginStability.PERIOD_BOUND,
            OriginStability.CONTESTED,
            OriginStability.PROVISIONAL,
        }

    def test_origin_residual_kind_exhaustive_members(self) -> None:
        expected = {
            "ORIGIN_ABSENT",
            "ORIGIN_OUTDATED",
            "ORIGIN_CONTESTED",
            "BINDING_AMBIGUOUS",
            "EVIDENCE_MISSING",
            "EVIDENCE_INSUFFICIENT",
            "EVIDENCE_CONTRADICTED",
            "REFERENCE_AMBIGUOUS",
            "DOMAIN_MISMATCH",
            "REFERENCE_WITHOUT_TRACE",
            "REFERENCE_BINDING_WITHOUT_SOURCE",
            "REFERENCE_AMBIGUOUS_UNCLOSED",
            "REFERENCE_RESOLVED_BY_PROBABILITY_ONLY",
            "REFERENCE_BINDING_COMPETITOR_UNHANDLED",
            "UNLICENSED_ELLIPSIS",
            "MISSING_QARINAH_FOR_DELETION",
            "ELLIPSIS_FILLED_BY_PROBABILITY_ONLY",
            "MULTIPLE_ELLIPSIS_CANDIDATES_UNRESOLVED",
            "ELLIPSIS_CLOSURE_NOT_PROVEN",
            "DOMAIN_TRANSFER_WITHOUT_MANAT",
            "DOMAIN_LEAP_WITHOUT_BRIDGE",
            "PRESERVED_MANAT_MISSING",
            "QADIH_DIFFERENCE_UNCHECKED",
            "QADIH_DIFFERENCE_BLOCKING",
            "RANK_CEILING_MISSING_FOR_BRIDGE",
            "PREMATURE_R7_AUDIT_CONSUMPTION",
            "VERDICT_USED_AS_FINAL_AUDIT",
            "R7_OUTPUT_PROMOTED_TO_CERTIFICATE",
            "MISSING_R8_AUDIT_INTEGRATION",
        }
        assert {m.value for m in OriginResidualKind} == expected

    def test_binding_verdict_has_four_members(self) -> None:
        assert set(BindingVerdict) == {
            BindingVerdict.COMPATIBLE,
            BindingVerdict.CONTRADICTED,
            BindingVerdict.UNSUPPORTED,
            BindingVerdict.PARTIALLY_COMPATIBLE,
        }

    def test_evidence_direction_has_four_members(self) -> None:
        assert set(EvidenceDirection) == {
            EvidenceDirection.SUPPORTS,
            EvidenceDirection.REFUTES,
            EvidenceDirection.PARTIALLY_SUPPORTS,
            EvidenceDirection.NEUTRAL,
        }

    def test_resolution_type_has_four_members(self) -> None:
        assert set(ResolutionType) == {
            ResolutionType.ANAPHORIC,
            ResolutionType.CATAPHORIC,
            ResolutionType.DEICTIC,
            ResolutionType.EXOPHORIC,
        }


# ---------------------------------------------------------------------------
# Test: Carrier construction (happy path)
# ---------------------------------------------------------------------------


class TestCarrierConstruction:
    """Valid carriers construct without error."""

    def test_entity_genus_origin_constructs(self) -> None:
        origin = _make_entity_genus()
        assert origin.entity_id == "moon"
        assert origin.genus == "celestial body / natural satellite"

    def test_attribute_event_origin_constructs(self) -> None:
        origin = _make_attribute_event()
        assert origin.attribute_id == "self_luminous"

    def test_relation_operator_origin_constructs(self) -> None:
        origin = _make_relation_operator()
        assert origin.relation_id == "causal_bi"

    def test_reference_origin_constructs(self) -> None:
        origin = _make_reference()
        assert origin.reference_id == "dhatihi"

    def test_evidence_origin_constructs(self) -> None:
        origin = _make_evidence()
        assert origin.claim_ref == "the moon is self-luminous"

    def test_origin_residual_constructs(self) -> None:
        r = _make_origin_residual()
        assert r.kind == OriginResidualKind.EVIDENCE_CONTRADICTED

    def test_origin_binding_constructs(self) -> None:
        b = _make_origin_binding()
        assert b.verdict == BindingVerdict.CONTRADICTED


# ---------------------------------------------------------------------------
# Test: Carriers are frozen (immutable)
# ---------------------------------------------------------------------------


class TestCarriersFrozen:
    """All carriers must be frozen dataclasses."""

    def test_entity_genus_is_frozen(self) -> None:
        origin = _make_entity_genus()
        with pytest.raises(dataclasses.FrozenInstanceError):
            origin.entity_id = "sun"  # type: ignore[misc]

    def test_attribute_event_is_frozen(self) -> None:
        origin = _make_attribute_event()
        with pytest.raises(dataclasses.FrozenInstanceError):
            origin.attribute_id = "opaque"  # type: ignore[misc]

    def test_relation_operator_is_frozen(self) -> None:
        origin = _make_relation_operator()
        with pytest.raises(dataclasses.FrozenInstanceError):
            origin.relation_id = "x"  # type: ignore[misc]

    def test_reference_is_frozen(self) -> None:
        origin = _make_reference()
        with pytest.raises(dataclasses.FrozenInstanceError):
            origin.reference_id = "x"  # type: ignore[misc]

    def test_evidence_is_frozen(self) -> None:
        origin = _make_evidence()
        with pytest.raises(dataclasses.FrozenInstanceError):
            origin.claim_ref = "x"  # type: ignore[misc]

    def test_origin_residual_is_frozen(self) -> None:
        r = _make_origin_residual()
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.kind = OriginResidualKind.ORIGIN_ABSENT  # type: ignore[misc]

    def test_origin_binding_is_frozen(self) -> None:
        b = _make_origin_binding()
        with pytest.raises(dataclasses.FrozenInstanceError):
            b.verdict = BindingVerdict.COMPATIBLE  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Test: Schema refusal (birth validation)
# ---------------------------------------------------------------------------


class TestSchemaRefusal:
    """Carriers refuse malformed construction with named errors."""

    def test_entity_genus_refuses_empty_entity_id(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="entity_id"):
            EntityGenusOrigin(
                entity_id="",
                genus="thing",
                essential_properties=("x",),
                bearing_capacity=("y",),
                bearing_refusal=("z",),
                domain="test",
                stability=OriginStability.PERMANENT,
                source_ref="test",
                rank=OriginRank.HIGH,
                residuals=("r",),
            )

    def test_entity_genus_refuses_invalid_rank(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="rank"):
            EntityGenusOrigin(
                entity_id="moon",
                genus="thing",
                essential_properties=("x",),
                bearing_capacity=("y",),
                bearing_refusal=("z",),
                domain="test",
                stability=OriginStability.PERMANENT,
                source_ref="test",
                rank="not_a_rank",  # type: ignore[arg-type]
                residuals=("r",),
            )

    def test_attribute_event_refuses_empty_id(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="attribute_id"):
            AttributeEventOrigin(
                attribute_id="  ",
                required_conditions=("x",),
                contradicting_conditions=("y",),
                typical_bearers=("z",),
                impossible_bearers=("w",),
                domain="test",
                stability=OriginStability.PERMANENT,
                source_ref="test",
                rank=OriginRank.HIGH,
                residuals=("r",),
            )

    def test_relation_operator_refuses_invalid_stability(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="stability"):
            RelationOperatorOrigin(
                relation_id="x",
                argument_structure="a — b",
                presuppositions=("p",),
                binding_semantics="X causes Y",
                domain="test",
                stability="wrong",  # type: ignore[arg-type]
                source_ref="test",
                rank=OriginRank.HIGH,
                residuals=("r",),
            )

    def test_reference_refuses_invalid_resolution_type(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="resolution_type"):
            ReferenceOrigin(
                reference_id="x",
                referent="y",
                resolution_type="bad",  # type: ignore[arg-type]
                confidence=OriginRank.HIGH,
                domain="test",
                maqam_dependency=OriginRank.LOW,
                residuals=(),
            )

    def test_evidence_refuses_invalid_direction(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="evidence_direction"):
            EvidenceOrigin(
                claim_ref="x",
                evidence_type="scientific",
                evidence_direction="bad",  # type: ignore[arg-type]
                evidence_content="content",
                source="src",
                source_rank=OriginRank.HIGH,
                recency=OriginStability.PERMANENT,
                domain="test",
                stability=OriginStability.PERMANENT,
                residuals=("r",),
                contradiction_with=("c",),
            )

    def test_origin_residual_refuses_invalid_kind(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="kind"):
            OriginResidual(
                kind="bad",  # type: ignore[arg-type]
                description="desc",
                claim_ref="claim",
            )

    def test_origin_binding_refuses_invalid_verdict(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="verdict"):
            OriginBinding(
                claim_ref="x",
                origin_type="EntityGenusOrigin",
                origin_id="moon",
                verdict="bad",  # type: ignore[arg-type]
                residuals=(),
                trace_ref="trace://x",
            )

    def test_origin_binding_refuses_invalid_residual_entries(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="residuals"):
            OriginBinding(
                claim_ref="x",
                origin_type="EntityGenusOrigin",
                origin_id="moon",
                verdict=BindingVerdict.COMPATIBLE,
                residuals=("not_a_residual",),  # type: ignore[arg-type]
                trace_ref="trace://x",
            )

    def test_origin_binding_refuses_empty_trace_ref(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="trace_ref"):
            OriginBinding(
                claim_ref="x",
                origin_type="EntityGenusOrigin",
                origin_id="moon",
                verdict=BindingVerdict.COMPATIBLE,
                residuals=(),
                trace_ref="",
            )

    def test_origin_binding_refuses_non_trace_scheme(self) -> None:
        with pytest.raises(OriginCarrierSchemaError, match="trace_ref"):
            OriginBinding(
                claim_ref="x",
                origin_type="EntityGenusOrigin",
                origin_id="moon",
                verdict=BindingVerdict.COMPATIBLE,
                residuals=(),
                trace_ref="binding/001",
            )


# ---------------------------------------------------------------------------
# Test: Carrier field completeness (docs/55 required fields)
# ---------------------------------------------------------------------------


class TestFieldCompleteness:
    """Carriers must have all fields declared in docs/55."""

    def test_entity_genus_has_required_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(EntityGenusOrigin)}
        required = {
            "entity_id", "genus", "essential_properties",
            "bearing_capacity", "bearing_refusal", "domain",
            "stability", "source_ref", "rank", "residuals",
        }
        assert required <= fields

    def test_attribute_event_has_required_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(AttributeEventOrigin)}
        required = {
            "attribute_id", "required_conditions", "contradicting_conditions",
            "typical_bearers", "impossible_bearers", "domain",
            "stability", "source_ref", "rank", "residuals",
        }
        assert required <= fields

    def test_relation_operator_has_required_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(RelationOperatorOrigin)}
        required = {
            "relation_id", "argument_structure", "presuppositions",
            "binding_semantics", "domain", "stability",
            "source_ref", "rank", "residuals",
        }
        assert required <= fields

    def test_reference_has_required_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(ReferenceOrigin)}
        required = {
            "reference_id", "referent", "resolution_type",
            "confidence", "domain", "maqam_dependency", "residuals",
        }
        assert required <= fields

    def test_evidence_has_required_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(EvidenceOrigin)}
        required = {
            "claim_ref", "evidence_type", "evidence_direction",
            "evidence_content", "source", "source_rank",
            "recency", "domain", "stability", "residuals",
            "contradiction_with",
        }
        assert required <= fields

    def test_origin_binding_has_required_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(OriginBinding)}
        required = {
            "claim_ref", "origin_type", "origin_id",
            "verdict", "residuals", "trace_ref",
        }
        assert required <= fields

    def test_origin_residual_has_required_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(OriginResidual)}
        required = {"kind", "description", "claim_ref"}
        assert required <= fields


# ---------------------------------------------------------------------------
# Test: No forbidden outputs in GPT-K1
# ---------------------------------------------------------------------------


class TestForbiddenOutputs:
    """GPT-K1 must NOT export verdicts, gates, or pipeline code."""

    def test_no_reasonableness_verdict_exported(self) -> None:
        import taaqqul_slot_geometry.gpt as gpt_module
        assert not hasattr(gpt_module, "ReasonablenessVerdict")

    def test_no_maqam_gpt_verdict_exported(self) -> None:
        import taaqqul_slot_geometry.gpt as gpt_module
        assert not hasattr(gpt_module, "MaqamGPTVerdict")

    def test_no_origin_binding_gate_exported(self) -> None:
        import taaqqul_slot_geometry.gpt as gpt_module
        assert not hasattr(gpt_module, "OriginBindingGate")

    def test_no_reasonableness_pipeline_exported(self) -> None:
        import taaqqul_slot_geometry.gpt as gpt_module
        assert not hasattr(gpt_module, "ReasonablenessPipeline")

    def test_no_pipeline_exported(self) -> None:
        import taaqqul_slot_geometry.gpt as gpt_module
        assert not hasattr(gpt_module, "Pipeline")

    def test_no_need_gate_exported(self) -> None:
        import taaqqul_slot_geometry.gpt as gpt_module
        assert not hasattr(gpt_module, "NeedGate")
