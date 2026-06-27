"""Knowledge Origins Schema Carriers — GPT-K1.

Binding: ``docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md`` §§3–8.
Chain position: GPT-K1 (Origin Schema Carriers).
Forbidden: verdicts, gates, pipeline code, adapter/audit changes.

This module defines the frozen dataclasses for the five Knowledge Origins,
the OriginBinding carrier, and the OriginResidual carrier. Every carrier
is frozen and carries typed fields declared in docs/55.

The carriers are Prior Classified Knowledge for claim verification — not
encyclopedic lexicons, not truth authorities. Each origin carries a rank
and residuals (what it does NOT cover), following the constitutional
principle: no approved output with hidden residuals.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

# ---------------------------------------------------------------------------
# Shared enums (docs/55 §11, §8.3)
# ---------------------------------------------------------------------------


class OriginRank(StrEnum):
    """Epistemic rank of a Knowledge Origin (docs/55 §11)."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class OriginStability(StrEnum):
    """Stability classification of a Knowledge Origin (docs/55 §11)."""

    PERMANENT = "PERMANENT"
    PERIOD_BOUND = "PERIOD_BOUND"
    CONTESTED = "CONTESTED"
    PROVISIONAL = "PROVISIONAL"


class OriginResidualKind(StrEnum):
    """Typed residual kinds from origin binding (docs/55 §8.3)."""

    ORIGIN_ABSENT = "ORIGIN_ABSENT"
    ORIGIN_OUTDATED = "ORIGIN_OUTDATED"
    ORIGIN_CONTESTED = "ORIGIN_CONTESTED"
    BINDING_AMBIGUOUS = "BINDING_AMBIGUOUS"
    EVIDENCE_MISSING = "EVIDENCE_MISSING"
    EVIDENCE_INSUFFICIENT = "EVIDENCE_INSUFFICIENT"
    EVIDENCE_CONTRADICTED = "EVIDENCE_CONTRADICTED"
    REFERENCE_AMBIGUOUS = "REFERENCE_AMBIGUOUS"
    DOMAIN_MISMATCH = "DOMAIN_MISMATCH"
    REFERENCE_WITHOUT_TRACE = "REFERENCE_WITHOUT_TRACE"
    REFERENCE_BINDING_WITHOUT_SOURCE = "REFERENCE_BINDING_WITHOUT_SOURCE"
    REFERENCE_AMBIGUOUS_UNCLOSED = "REFERENCE_AMBIGUOUS_UNCLOSED"
    REFERENCE_RESOLVED_BY_PROBABILITY_ONLY = "REFERENCE_RESOLVED_BY_PROBABILITY_ONLY"
    REFERENCE_BINDING_COMPETITOR_UNHANDLED = "REFERENCE_BINDING_COMPETITOR_UNHANDLED"
    UNLICENSED_ELLIPSIS = "UNLICENSED_ELLIPSIS"
    MISSING_QARINAH_FOR_DELETION = "MISSING_QARINAH_FOR_DELETION"
    ELLIPSIS_FILLED_BY_PROBABILITY_ONLY = "ELLIPSIS_FILLED_BY_PROBABILITY_ONLY"
    MULTIPLE_ELLIPSIS_CANDIDATES_UNRESOLVED = "MULTIPLE_ELLIPSIS_CANDIDATES_UNRESOLVED"
    ELLIPSIS_CLOSURE_NOT_PROVEN = "ELLIPSIS_CLOSURE_NOT_PROVEN"
    DOMAIN_TRANSFER_WITHOUT_MANAT = "DOMAIN_TRANSFER_WITHOUT_MANAT"
    DOMAIN_LEAP_WITHOUT_BRIDGE = "DOMAIN_LEAP_WITHOUT_BRIDGE"
    PRESERVED_MANAT_MISSING = "PRESERVED_MANAT_MISSING"
    QADIH_DIFFERENCE_UNCHECKED = "QADIH_DIFFERENCE_UNCHECKED"
    QADIH_DIFFERENCE_BLOCKING = "QADIH_DIFFERENCE_BLOCKING"
    RANK_CEILING_MISSING_FOR_BRIDGE = "RANK_CEILING_MISSING_FOR_BRIDGE"
    PREMATURE_R7_AUDIT_CONSUMPTION = "PREMATURE_R7_AUDIT_CONSUMPTION"
    VERDICT_USED_AS_FINAL_AUDIT = "VERDICT_USED_AS_FINAL_AUDIT"
    R7_OUTPUT_PROMOTED_TO_CERTIFICATE = "R7_OUTPUT_PROMOTED_TO_CERTIFICATE"
    MISSING_R8_AUDIT_INTEGRATION = "MISSING_R8_AUDIT_INTEGRATION"


class BindingVerdict(StrEnum):
    """Binding verdict from origin consultation (docs/55 §8.1 rule 4)."""

    COMPATIBLE = "COMPATIBLE"
    CONTRADICTED = "CONTRADICTED"
    UNSUPPORTED = "UNSUPPORTED"
    PARTIALLY_COMPATIBLE = "PARTIALLY_COMPATIBLE"


class EvidenceDirection(StrEnum):
    """Direction of evidence relative to a claim (docs/55 §7.1)."""

    SUPPORTS = "SUPPORTS"
    REFUTES = "REFUTES"
    PARTIALLY_SUPPORTS = "PARTIALLY_SUPPORTS"
    NEUTRAL = "NEUTRAL"


class ResolutionType(StrEnum):
    """Reference resolution type (docs/55 §6.1)."""

    ANAPHORIC = "ANAPHORIC"
    CATAPHORIC = "CATAPHORIC"
    DEICTIC = "DEICTIC"
    EXOPHORIC = "EXOPHORIC"


# ---------------------------------------------------------------------------
# Schema error
# ---------------------------------------------------------------------------


class OriginCarrierSchemaError(TypeError):
    """A Knowledge Origin carrier was constructed with a malformed field.

    Raised at carrier birth (__post_init__), before any carrier can travel.
    Mirrors WeightCarrierSchemaError: a programmer mistake, not a
    constitutional verdict. The message always names the violated axis.
    """


# ---------------------------------------------------------------------------
# Helper: birth validation
# ---------------------------------------------------------------------------


def _require_nonempty_str(cls_name: str, field: str, value: object) -> None:
    """Refuse empty or non-string values at birth."""
    if not isinstance(value, str) or not value.strip():
        raise OriginCarrierSchemaError(
            f"{cls_name}.{field} must be a non-empty string"
        )


def _require_tuple(cls_name: str, field: str, value: object) -> None:
    """Refuse non-tuple values at birth."""
    if not isinstance(value, tuple):
        raise OriginCarrierSchemaError(
            f"{cls_name}.{field} must be a tuple"
        )


def _require_trace_ref(cls_name: str, field: str, value: object) -> None:
    """Refuse malformed trace references at birth."""
    _require_nonempty_str(cls_name, field, value)
    assert isinstance(value, str)  # narrows type after _require_nonempty_str
    if not value.startswith("trace://"):
        raise OriginCarrierSchemaError(
            f"{cls_name}.{field} must start with 'trace://'"
        )


# ---------------------------------------------------------------------------
# §3 — EntityGenusOrigin
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class EntityGenusOrigin:
    """What an entity IS: genus, essential properties, bearing capacity.

    docs/55 §3.1 — Required Fields.
    """

    entity_id: str
    genus: str
    essential_properties: tuple[str, ...]
    bearing_capacity: tuple[str, ...]
    bearing_refusal: tuple[str, ...]
    domain: str
    stability: OriginStability
    source_ref: str
    rank: OriginRank
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "entity_id", self.entity_id)
        _require_nonempty_str(cls, "genus", self.genus)
        _require_tuple(cls, "essential_properties", self.essential_properties)
        _require_tuple(cls, "bearing_capacity", self.bearing_capacity)
        _require_tuple(cls, "bearing_refusal", self.bearing_refusal)
        _require_nonempty_str(cls, "domain", self.domain)
        if not isinstance(self.stability, OriginStability):
            raise OriginCarrierSchemaError(
                f"{cls}.stability must be an OriginStability member"
            )
        _require_nonempty_str(cls, "source_ref", self.source_ref)
        if not isinstance(self.rank, OriginRank):
            raise OriginCarrierSchemaError(
                f"{cls}.rank must be an OriginRank member"
            )
        _require_tuple(cls, "residuals", self.residuals)


# ---------------------------------------------------------------------------
# §4 — AttributeEventOrigin
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AttributeEventOrigin:
    """What a predicate REQUIRES: conditions for truthful attribution.

    docs/55 §4.1 — Required Fields.
    """

    attribute_id: str
    required_conditions: tuple[str, ...]
    contradicting_conditions: tuple[str, ...]
    typical_bearers: tuple[str, ...]
    impossible_bearers: tuple[str, ...]
    domain: str
    stability: OriginStability
    source_ref: str
    rank: OriginRank
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "attribute_id", self.attribute_id)
        _require_tuple(cls, "required_conditions", self.required_conditions)
        _require_tuple(cls, "contradicting_conditions", self.contradicting_conditions)
        _require_tuple(cls, "typical_bearers", self.typical_bearers)
        _require_tuple(cls, "impossible_bearers", self.impossible_bearers)
        _require_nonempty_str(cls, "domain", self.domain)
        if not isinstance(self.stability, OriginStability):
            raise OriginCarrierSchemaError(
                f"{cls}.stability must be an OriginStability member"
            )
        _require_nonempty_str(cls, "source_ref", self.source_ref)
        if not isinstance(self.rank, OriginRank):
            raise OriginCarrierSchemaError(
                f"{cls}.rank must be an OriginRank member"
            )
        _require_tuple(cls, "residuals", self.residuals)


# ---------------------------------------------------------------------------
# §5 — RelationOperatorOrigin
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RelationOperatorOrigin:
    """What a relation/operator MEANS: argument structure and binding.

    docs/55 §5.1 — Required Fields.
    """

    relation_id: str
    argument_structure: str
    presuppositions: tuple[str, ...]
    binding_semantics: str
    domain: str
    stability: OriginStability
    source_ref: str
    rank: OriginRank
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "relation_id", self.relation_id)
        _require_nonempty_str(cls, "argument_structure", self.argument_structure)
        _require_tuple(cls, "presuppositions", self.presuppositions)
        _require_nonempty_str(cls, "binding_semantics", self.binding_semantics)
        _require_nonempty_str(cls, "domain", self.domain)
        if not isinstance(self.stability, OriginStability):
            raise OriginCarrierSchemaError(
                f"{cls}.stability must be an OriginStability member"
            )
        _require_nonempty_str(cls, "source_ref", self.source_ref)
        if not isinstance(self.rank, OriginRank):
            raise OriginCarrierSchemaError(
                f"{cls}.rank must be an OriginRank member"
            )
        _require_tuple(cls, "residuals", self.residuals)


# ---------------------------------------------------------------------------
# §6 — ReferenceOrigin
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ReferenceOrigin:
    """What a reference expression POINTS TO in context.

    docs/55 §6.1 — Required Fields.
    """

    reference_id: str
    referent: str
    resolution_type: ResolutionType
    confidence: OriginRank
    domain: str
    maqam_dependency: OriginRank
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "reference_id", self.reference_id)
        _require_nonempty_str(cls, "referent", self.referent)
        if not isinstance(self.resolution_type, ResolutionType):
            raise OriginCarrierSchemaError(
                f"{cls}.resolution_type must be a ResolutionType member"
            )
        if not isinstance(self.confidence, OriginRank):
            raise OriginCarrierSchemaError(
                f"{cls}.confidence must be an OriginRank member"
            )
        _require_nonempty_str(cls, "domain", self.domain)
        if not isinstance(self.maqam_dependency, OriginRank):
            raise OriginCarrierSchemaError(
                f"{cls}.maqam_dependency must be an OriginRank member"
            )
        _require_tuple(cls, "residuals", self.residuals)


# ---------------------------------------------------------------------------
# §7 — EvidenceOrigin
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class EvidenceOrigin:
    """What SUPPORTS or REFUTES a claim from external sources.

    docs/55 §7.1 — Required Fields.
    """

    claim_ref: str
    evidence_type: str
    evidence_direction: EvidenceDirection
    evidence_content: str
    source: str
    source_rank: OriginRank
    recency: OriginStability
    domain: str
    stability: OriginStability
    residuals: tuple[str, ...]
    contradiction_with: tuple[str, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "claim_ref", self.claim_ref)
        _require_nonempty_str(cls, "evidence_type", self.evidence_type)
        if not isinstance(self.evidence_direction, EvidenceDirection):
            raise OriginCarrierSchemaError(
                f"{cls}.evidence_direction must be an EvidenceDirection member"
            )
        _require_nonempty_str(cls, "evidence_content", self.evidence_content)
        _require_nonempty_str(cls, "source", self.source)
        if not isinstance(self.source_rank, OriginRank):
            raise OriginCarrierSchemaError(
                f"{cls}.source_rank must be an OriginRank member"
            )
        if not isinstance(self.recency, OriginStability):
            raise OriginCarrierSchemaError(
                f"{cls}.recency must be an OriginStability member"
            )
        _require_nonempty_str(cls, "domain", self.domain)
        if not isinstance(self.stability, OriginStability):
            raise OriginCarrierSchemaError(
                f"{cls}.stability must be an OriginStability member"
            )
        _require_tuple(cls, "residuals", self.residuals)
        _require_tuple(cls, "contradiction_with", self.contradiction_with)


# ---------------------------------------------------------------------------
# §8 — OriginBinding
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class OriginResidual:
    """A single residual from an incomplete or contested origin binding.

    docs/55 §8.3 — Every incomplete or contested binding produces an
    OriginResidual. These residuals are ALWAYS visible. No verdict may
    hide them.
    """

    kind: OriginResidualKind
    description: str
    claim_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.kind, OriginResidualKind):
            raise OriginCarrierSchemaError(
                f"{cls}.kind must be an OriginResidualKind member"
            )
        _require_nonempty_str(cls, "description", self.description)
        _require_nonempty_str(cls, "claim_ref", self.claim_ref)


@dataclass(frozen=True, slots=True)
class OriginBinding:
    """Connects a MantuqGPT claim to the required Knowledge Origins.

    docs/55 §8.1 — Binding Rules. Every MantuqGPT claim must bind to at
    least one origin. Each binding produces a BindingVerdict.
    The binding carries its verdict, the origin type consulted,
    and any residuals generated.
    """

    claim_ref: str
    origin_type: str
    origin_id: str
    verdict: BindingVerdict
    residuals: tuple[OriginResidual, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_nonempty_str(cls, "claim_ref", self.claim_ref)
        _require_nonempty_str(cls, "origin_type", self.origin_type)
        _require_nonempty_str(cls, "origin_id", self.origin_id)
        if not isinstance(self.verdict, BindingVerdict):
            raise OriginCarrierSchemaError(
                f"{cls}.verdict must be a BindingVerdict member"
            )
        if not isinstance(self.residuals, tuple):
            raise OriginCarrierSchemaError(
                f"{cls}.residuals must be a tuple of OriginResidual carriers"
            )
        for r in self.residuals:
            if not isinstance(r, OriginResidual):
                raise OriginCarrierSchemaError(
                    f"{cls}.residuals entries must be OriginResidual carriers"
                )
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


# ---------------------------------------------------------------------------
# Module export surface
# ---------------------------------------------------------------------------

__all__ = [
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
]
