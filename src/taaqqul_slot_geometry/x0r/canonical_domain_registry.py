"""PR-B canonical domain registry (carrier-only unified kind surface)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CanonicalDomainRegistrySchemaError(TypeError):
    """Raised when the canonical domain registry surface is malformed."""


class DomainId(StrEnum):
    """Canonical domain identifiers shared across constitutional branches."""

    CORE_KERNEL = "CORE_KERNEL"
    X0R_CONTRACTS = "X0R_CONTRACTS"
    USM = "USM"
    WEIGHT = "WEIGHT"
    LEXICON = "LEXICON"
    DAL = "DAL"
    LAFZI = "LAFZI"
    GPT_REASONABLENESS = "GPT_REASONABLENESS"
    RUNTIME_PIPELINE = "RUNTIME_PIPELINE"
    AUDIT_LAYER = "AUDIT_LAYER"
    ADAPTER_BOUNDARY = "ADAPTER_BOUNDARY"
    G0_ZERO_LAYER = "G0_ZERO_LAYER"
    LGE_SURFACE = "LGE_SURFACE"


class TransitionKind(StrEnum):
    """Canonical transition kinds for cross-domain contract declarations."""

    LAW_ONLY_BOUNDARY = "LAW_ONLY_BOUNDARY"
    CARRIER_DECLARATION = "CARRIER_DECLARATION"
    GATE_EVALUATION = "GATE_EVALUATION"
    ELIGIBILITY_EVALUATION = "ELIGIBILITY_EVALUATION"
    LINKING = "LINKING"
    PROPOSAL_CONSTRUCTION = "PROPOSAL_CONSTRUCTION"
    EXECUTION_CANDIDATE = "EXECUTION_CANDIDATE"
    POSTFLIGHT_AUDIT = "POSTFLIGHT_AUDIT"
    COMMIT_DECISION = "COMMIT_DECISION"
    ROLLBACK_REOPEN = "ROLLBACK_REOPEN"


class CarrierKind(StrEnum):
    """Canonical carrier classes used by transition contracts."""

    SLOT_GRAPH = "SLOT_GRAPH"
    TRANSITION_CONTRACT = "TRANSITION_CONTRACT"
    EVIDENCE_CONTRACT = "EVIDENCE_CONTRACT"
    RESIDUAL = "RESIDUAL"
    RANK_VECTOR = "RANK_VECTOR"
    TRACE_REF = "TRACE_REF"
    CANDIDATE_SET = "CANDIDATE_SET"
    PROPOSAL = "PROPOSAL"
    GUARDIAN_DECISION = "GUARDIAN_DECISION"
    APPROVED_CONTEXT = "APPROVED_CONTEXT"


class EvidenceKind(StrEnum):
    """Canonical evidence classes recognized by registry-bound contracts."""

    SOURCE_TEXT = "SOURCE_TEXT"
    STRUCTURAL_VALIDATION = "STRUCTURAL_VALIDATION"
    RULE_PROOF = "RULE_PROOF"
    WITNESS_REPORT = "WITNESS_REPORT"
    MATRIX_REFERENCE = "MATRIX_REFERENCE"
    CROSS_SOURCE_CORROBORATION = "CROSS_SOURCE_CORROBORATION"


class ResidualKind(StrEnum):
    """Canonical residual classes used for cross-branch visibility alignment."""

    BLOCKING = "BLOCKING"
    DEFERRED = "DEFERRED"
    NON_BLOCKING = "NON_BLOCKING"
    CONTRADICTORY = "CONTRADICTORY"
    EXPLANATORY = "EXPLANATORY"
    REPAIRABLE = "REPAIRABLE"


class RankChannel(StrEnum):
    """Canonical rank channels for multi-channel rank declarations."""

    SOURCE = "SOURCE"
    IDENTITY = "IDENTITY"
    EVIDENCE = "EVIDENCE"
    GATE = "GATE"
    RESIDUAL_CEILING = "RESIDUAL_CEILING"
    TRANSITION = "TRANSITION"
    DOMAIN_READINESS = "DOMAIN_READINESS"


@dataclass(frozen=True, slots=True)
class CanonicalDomainRegistry:
    """Immutable canonical registry for cross-domain kind vocabularies."""

    version: str
    trace_ref: str
    domains: tuple[DomainId, ...]
    transition_kinds: tuple[TransitionKind, ...]
    carrier_kinds: tuple[CarrierKind, ...]
    evidence_kinds: tuple[EvidenceKind, ...]
    residual_kinds: tuple[ResidualKind, ...]
    rank_channels: tuple[RankChannel, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "version", self.version)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        _validate_enum_tuple(cls, "domains", self.domains, DomainId)
        _validate_enum_tuple(cls, "transition_kinds", self.transition_kinds, TransitionKind)
        _validate_enum_tuple(cls, "carrier_kinds", self.carrier_kinds, CarrierKind)
        _validate_enum_tuple(cls, "evidence_kinds", self.evidence_kinds, EvidenceKind)
        _validate_enum_tuple(cls, "residual_kinds", self.residual_kinds, ResidualKind)
        _validate_enum_tuple(cls, "rank_channels", self.rank_channels, RankChannel)

    def includes_domain(self, domain: DomainId) -> bool:
        return domain in self.domains

    def includes_transition_kind(self, kind: TransitionKind) -> bool:
        return kind in self.transition_kinds


def canonical_domain_registry() -> CanonicalDomainRegistry:
    """Return the immutable canonical domain registry singleton."""

    return _CANONICAL_DOMAIN_REGISTRY_V1


def _validate_enum_tuple(
    cls_name: str, field_name: str, value: object, expected_type: type[StrEnum]
) -> None:
    if not isinstance(value, tuple) or not value:
        raise CanonicalDomainRegistrySchemaError(
            f"{cls_name}.{field_name} must be a non-empty tuple"
        )
    for entry in value:
        if not isinstance(entry, expected_type):
            raise CanonicalDomainRegistrySchemaError(
                f"{cls_name}.{field_name} entries must be {expected_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise CanonicalDomainRegistrySchemaError(
            f"{cls_name}.{field_name} entries must be unique"
        )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CanonicalDomainRegistrySchemaError(
            f"{cls_name}.{field_name} must be a non-empty string"
        )


def _require_trace_ref(cls_name: str, field_name: str, value: object) -> None:
    _require_str(cls_name, field_name, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise CanonicalDomainRegistrySchemaError(
            f"{cls_name}.{field_name} must start with 'trace://'"
        )


_CANONICAL_DOMAIN_REGISTRY_V1 = CanonicalDomainRegistry(
    version="canonical-domain-registry-v1",
    trace_ref="trace://x0r/pr-b/canonical-domain-registry/v1",
    domains=(
        DomainId.CORE_KERNEL,
        DomainId.X0R_CONTRACTS,
        DomainId.USM,
        DomainId.WEIGHT,
        DomainId.LEXICON,
        DomainId.DAL,
        DomainId.LAFZI,
        DomainId.GPT_REASONABLENESS,
        DomainId.RUNTIME_PIPELINE,
        DomainId.AUDIT_LAYER,
        DomainId.ADAPTER_BOUNDARY,
        DomainId.G0_ZERO_LAYER,
        DomainId.LGE_SURFACE,
    ),
    transition_kinds=(
        TransitionKind.LAW_ONLY_BOUNDARY,
        TransitionKind.CARRIER_DECLARATION,
        TransitionKind.GATE_EVALUATION,
        TransitionKind.ELIGIBILITY_EVALUATION,
        TransitionKind.LINKING,
        TransitionKind.PROPOSAL_CONSTRUCTION,
        TransitionKind.EXECUTION_CANDIDATE,
        TransitionKind.POSTFLIGHT_AUDIT,
        TransitionKind.COMMIT_DECISION,
        TransitionKind.ROLLBACK_REOPEN,
    ),
    carrier_kinds=(
        CarrierKind.SLOT_GRAPH,
        CarrierKind.TRANSITION_CONTRACT,
        CarrierKind.EVIDENCE_CONTRACT,
        CarrierKind.RESIDUAL,
        CarrierKind.RANK_VECTOR,
        CarrierKind.TRACE_REF,
        CarrierKind.CANDIDATE_SET,
        CarrierKind.PROPOSAL,
        CarrierKind.GUARDIAN_DECISION,
        CarrierKind.APPROVED_CONTEXT,
    ),
    evidence_kinds=(
        EvidenceKind.SOURCE_TEXT,
        EvidenceKind.STRUCTURAL_VALIDATION,
        EvidenceKind.RULE_PROOF,
        EvidenceKind.WITNESS_REPORT,
        EvidenceKind.MATRIX_REFERENCE,
        EvidenceKind.CROSS_SOURCE_CORROBORATION,
    ),
    residual_kinds=(
        ResidualKind.BLOCKING,
        ResidualKind.DEFERRED,
        ResidualKind.NON_BLOCKING,
        ResidualKind.CONTRADICTORY,
        ResidualKind.EXPLANATORY,
        ResidualKind.REPAIRABLE,
    ),
    rank_channels=(
        RankChannel.SOURCE,
        RankChannel.IDENTITY,
        RankChannel.EVIDENCE,
        RankChannel.GATE,
        RankChannel.RESIDUAL_CEILING,
        RankChannel.TRANSITION,
        RankChannel.DOMAIN_READINESS,
    ),
)


__all__ = [
    "CanonicalDomainRegistry",
    "CanonicalDomainRegistrySchemaError",
    "CarrierKind",
    "DomainId",
    "EvidenceKind",
    "RankChannel",
    "ResidualKind",
    "TransitionKind",
    "canonical_domain_registry",
]
