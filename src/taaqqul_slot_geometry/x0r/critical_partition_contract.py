"""LAW-E1R critical partition runtime contract surface (no inference runtime)."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode


class CriticalPartitionContractError(TypeError):
    """Raised when LAW-E1R carriers are malformed."""


class PartitionKind(StrEnum):
    """Licensed LAW-E1 partition kinds."""

    PHONETIC = "PHONETIC"
    STRUCTURAL = "STRUCTURAL"
    SYSTEMIC = "SYSTEMIC"


class NecessityTier(StrEnum):
    """Declared LAW-E1 necessity tiers (labels only, never closure)."""

    DARURI = "DARURI"
    HAJI = "HAJI"
    TAHSINI = "TAHSINI"


class PartitionReadinessState(StrEnum):
    """Readiness states for LAW-E1R contract decisions."""

    LINK_READY = "LINK_READY"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    REFUSED = "REFUSED"


class CriticalPartitionStage(StrEnum):
    """Ordered LAW-E1R runtime stages."""

    PARTITION_DECLARATION = "PARTITION_DECLARATION"
    PARTITION_BRIDGE = "PARTITION_BRIDGE"
    IDENTITY_PROPERTY = "IDENTITY_PROPERTY"
    TRIADIC_IDENTITY = "TRIADIC_IDENTITY"
    NECESSITY_TIER = "NECESSITY_TIER"
    RESIDUALS = "RESIDUALS"
    HANDOFF = "HANDOFF"


@dataclass(frozen=True, slots=True)
class PartitionDeclaration:
    """Runtime declaration of a licensed partition boundary."""

    partition_kind: PartitionKind
    domain: str
    scope: str
    trace_ref: str
    residual_visible: bool

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.partition_kind, PartitionKind):
            raise CriticalPartitionContractError(f"{cls}.partition_kind must be PartitionKind")
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "scope", self.scope)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_bool(cls, "residual_visible", self.residual_visible)


@dataclass(frozen=True, slots=True)
class PartitionBridgeProof:
    """Bridge proof between partition boundaries."""

    source_partition: PartitionKind
    target_partition: PartitionKind
    domain: str
    scope: str
    trace_ref: str
    residual_visible: bool
    bridge_name: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.source_partition, PartitionKind):
            raise CriticalPartitionContractError(f"{cls}.source_partition must be PartitionKind")
        if not isinstance(self.target_partition, PartitionKind):
            raise CriticalPartitionContractError(f"{cls}.target_partition must be PartitionKind")
        _require_str(cls, "domain", self.domain)
        _require_str(cls, "scope", self.scope)
        _require_str(cls, "trace_ref", self.trace_ref)
        _require_bool(cls, "residual_visible", self.residual_visible)
        _require_str(cls, "bridge_name", self.bridge_name)


@dataclass(frozen=True, slots=True)
class IdentityPropertyConservationProof:
    """Identity-property conservation proof carrier."""

    identity_anchor: str
    preserved_properties: tuple[str, ...]
    licensed_variants: tuple[str, ...]
    broken_properties: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "identity_anchor", self.identity_anchor)
        _require_tuple(cls, "preserved_properties", self.preserved_properties)
        _require_tuple(cls, "licensed_variants", self.licensed_variants)
        _require_tuple(cls, "broken_properties", self.broken_properties)
        _require_str(cls, "trace_ref", self.trace_ref)
        for field_name, values in (
            ("preserved_properties", self.preserved_properties),
            ("licensed_variants", self.licensed_variants),
            ("broken_properties", self.broken_properties),
        ):
            for value in values:
                _require_str(cls, f"{field_name} entry", value)


@dataclass(frozen=True, slots=True)
class TriadicIdentityContinuityProof:
    """Triadic identity continuity proof (previous/current/next)."""

    previous_identity_ref: str
    current_identity_ref: str
    next_identity_ref: str
    previous_current_link: str
    current_next_link: str
    bridge_coherent: bool
    residual_visible: bool

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "previous_identity_ref", self.previous_identity_ref)
        _require_str(cls, "current_identity_ref", self.current_identity_ref)
        _require_str(cls, "next_identity_ref", self.next_identity_ref)
        _require_str(cls, "previous_current_link", self.previous_current_link)
        _require_str(cls, "current_next_link", self.current_next_link)
        _require_bool(cls, "bridge_coherent", self.bridge_coherent)
        _require_bool(cls, "residual_visible", self.residual_visible)


@dataclass(frozen=True, slots=True)
class NecessityTierProof:
    """Necessity-tier declaration proof (label only, no closure)."""

    tier: NecessityTier
    declared_cause: str
    evidence_ref: str
    transition_ref: str
    residual_visible: bool

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.tier, NecessityTier):
            raise CriticalPartitionContractError(f"{cls}.tier must be NecessityTier")
        _require_str(cls, "declared_cause", self.declared_cause)
        _require_str(cls, "evidence_ref", self.evidence_ref)
        _require_str(cls, "transition_ref", self.transition_ref)
        _require_bool(cls, "residual_visible", self.residual_visible)


@dataclass(frozen=True, slots=True)
class CriticalPartitionDecision:
    """Decision surface for LAW-E1R critical partition runtime contract."""

    partition_allowed: bool
    readiness_state: PartitionReadinessState
    failed_stage: CriticalPartitionStage | None
    local_failure_name: str | None
    failure_code: FailureCode | None
    residuals: tuple[str, ...]
    handoff: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_bool(cls, "partition_allowed", self.partition_allowed)
        if not isinstance(self.readiness_state, PartitionReadinessState):
            raise CriticalPartitionContractError(
                f"{cls}.readiness_state must be PartitionReadinessState"
            )
        if self.failed_stage is not None and not isinstance(
            self.failed_stage, CriticalPartitionStage
        ):
            raise CriticalPartitionContractError(
                f"{cls}.failed_stage must be CriticalPartitionStage or None"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise CriticalPartitionContractError(f"{cls}.failure_code must be FailureCode or None")
        if self.local_failure_name is not None:
            _require_str(cls, "local_failure_name", self.local_failure_name)
        _require_tuple(cls, "residuals", self.residuals)
        for residual in self.residuals:
            _require_str(cls, "residuals entry", residual)
        _require_str(cls, "handoff", self.handoff)

        if self.partition_allowed:
            if self.failed_stage is not None or self.failure_code is not None:
                raise CriticalPartitionContractError(
                    f"{cls} cannot be partition_allowed=True with a failure"
                )
            if self.local_failure_name is not None:
                raise CriticalPartitionContractError(
                    f"{cls} cannot be partition_allowed=True with local_failure_name"
                )
            if self.readiness_state is not PartitionReadinessState.LINK_READY:
                raise CriticalPartitionContractError(
                    f"{cls}.partition_allowed=True requires readiness_state=LINK_READY"
                )
            return

        if (
            self.failed_stage is None
            or self.failure_code is None
            or self.local_failure_name is None
        ):
            raise CriticalPartitionContractError(
                f"{cls} refusal requires failed_stage, local_failure_name, and failure_code"
            )
        if self.readiness_state is PartitionReadinessState.LINK_READY:
            raise CriticalPartitionContractError(
                f"{cls}.partition_allowed=False cannot carry readiness_state=LINK_READY"
            )


@dataclass(frozen=True, slots=True)
class CriticalPartitionRuntimeContract:
    """LAW-E1R runtime contract for partition/identity/tier surfaces only."""

    declared_partitions: frozenset[tuple[PartitionKind, str, str]]
    declared_bridges: frozenset[tuple[PartitionKind, PartitionKind, str, str, str]]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.declared_partitions, frozenset):
            raise CriticalPartitionContractError(f"{cls}.declared_partitions must be frozenset")
        if not isinstance(self.declared_bridges, frozenset):
            raise CriticalPartitionContractError(f"{cls}.declared_bridges must be frozenset")
        for row in self.declared_partitions:
            if not isinstance(row, tuple) or len(row) != 3:
                raise CriticalPartitionContractError(
                    f"{cls}.declared_partitions entries must be 3-tuples"
                )
            kind, domain, scope = row
            if not isinstance(kind, PartitionKind):
                raise CriticalPartitionContractError(
                    f"{cls}.declared_partitions kind must be PartitionKind"
                )
            _require_str(cls, "declared_partitions domain", domain)
            _require_str(cls, "declared_partitions scope", scope)

        for row in self.declared_bridges:
            if not isinstance(row, tuple) or len(row) != 5:
                raise CriticalPartitionContractError(
                    f"{cls}.declared_bridges entries must be 5-tuples"
                )
            source, target, domain, scope, bridge_name = row
            if not isinstance(source, PartitionKind) or not isinstance(target, PartitionKind):
                raise CriticalPartitionContractError(
                    f"{cls}.declared_bridges source/target must be PartitionKind"
                )
            _require_str(cls, "declared_bridges domain", domain)
            _require_str(cls, "declared_bridges scope", scope)
            _require_str(cls, "declared_bridges bridge_name", bridge_name)

    def evaluate(
        self,
        declaration: PartitionDeclaration,
        bridge_proof: PartitionBridgeProof,
        identity_proof: IdentityPropertyConservationProof,
        triadic_proof: TriadicIdentityContinuityProof,
        tier_proof: NecessityTierProof,
        *,
        handoff: str,
        residuals: tuple[str, ...] = (),
    ) -> CriticalPartitionDecision:
        """Evaluate LAW-E1R contract stages without semantic/hukm runtime opening."""

        if not isinstance(declaration, PartitionDeclaration):
            raise CriticalPartitionContractError("declaration must be PartitionDeclaration")
        if not isinstance(bridge_proof, PartitionBridgeProof):
            raise CriticalPartitionContractError("bridge_proof must be PartitionBridgeProof")
        if not isinstance(identity_proof, IdentityPropertyConservationProof):
            raise CriticalPartitionContractError(
                "identity_proof must be IdentityPropertyConservationProof"
            )
        if not isinstance(triadic_proof, TriadicIdentityContinuityProof):
            raise CriticalPartitionContractError(
                "triadic_proof must be TriadicIdentityContinuityProof"
            )
        if not isinstance(tier_proof, NecessityTierProof):
            raise CriticalPartitionContractError("tier_proof must be NecessityTierProof")
        _require_str(self.__class__.__name__, "handoff", handoff)
        _require_tuple(self.__class__.__name__, "residuals", residuals)
        for residual in residuals:
            _require_str(self.__class__.__name__, "residuals entry", residual)

        partition_key = (declaration.partition_kind, declaration.domain, declaration.scope)
        if partition_key not in self.declared_partitions:
            return self._refuse(
                name="PARTITION_UNDECLARED",
                stage=CriticalPartitionStage.PARTITION_DECLARATION,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if not declaration.residual_visible:
            return self._refuse(
                name="HIDDEN_RESIDUAL",
                stage=CriticalPartitionStage.RESIDUALS,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        bridge_key = (
            bridge_proof.source_partition,
            bridge_proof.target_partition,
            bridge_proof.domain,
            bridge_proof.scope,
            bridge_proof.bridge_name,
        )
        if bridge_key not in self.declared_bridges:
            return self._refuse(
                name="PARTITION_BRIDGE_MISSING",
                stage=CriticalPartitionStage.PARTITION_BRIDGE,
                state=PartitionReadinessState.DEFERRED,
                residuals=residuals,
                handoff=handoff,
            )

        if _is_forbidden_skip(bridge_proof.source_partition, bridge_proof.target_partition):
            return self._refuse(
                name="PARTITION_BRIDGE_FORBIDDEN",
                stage=CriticalPartitionStage.PARTITION_BRIDGE,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if (
            bridge_proof.domain != declaration.domain
            or bridge_proof.scope != declaration.scope
            or bridge_proof.trace_ref != declaration.trace_ref
        ):
            return self._refuse(
                name="PARTITION_BRIDGE_METADATA_MISMATCH",
                stage=CriticalPartitionStage.PARTITION_BRIDGE,
                state=PartitionReadinessState.DEFERRED,
                residuals=residuals,
                handoff=handoff,
            )

        if not bridge_proof.residual_visible:
            return self._refuse(
                name="HIDDEN_RESIDUAL",
                stage=CriticalPartitionStage.RESIDUALS,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if not identity_proof.identity_anchor.strip():
            return self._refuse(
                name="IDENTITY_TRANSITION_UNLICENSED",
                stage=CriticalPartitionStage.IDENTITY_PROPERTY,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if not identity_proof.preserved_properties:
            return self._refuse(
                name="IDENTITY_PROPERTY_BROKEN",
                stage=CriticalPartitionStage.IDENTITY_PROPERTY,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if identity_proof.broken_properties:
            return self._refuse(
                name="IDENTITY_PROPERTY_BROKEN",
                stage=CriticalPartitionStage.IDENTITY_PROPERTY,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if identity_proof.trace_ref != declaration.trace_ref:
            return self._refuse(
                name="IDENTITY_TRANSITION_UNLICENSED",
                stage=CriticalPartitionStage.IDENTITY_PROPERTY,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if (
            not triadic_proof.previous_identity_ref.strip()
            or not triadic_proof.current_identity_ref.strip()
            or not triadic_proof.next_identity_ref.strip()
            or not triadic_proof.previous_current_link.strip()
            or not triadic_proof.current_next_link.strip()
            or not triadic_proof.bridge_coherent
        ):
            return self._refuse(
                name="TRIADIC_IDENTITY_GAP",
                stage=CriticalPartitionStage.TRIADIC_IDENTITY,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if not triadic_proof.residual_visible:
            return self._refuse(
                name="HIDDEN_RESIDUAL",
                stage=CriticalPartitionStage.RESIDUALS,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if not tier_proof.declared_cause.strip():
            return self._refuse(
                name="NECESSITY_TIER_UNDECLARED",
                stage=CriticalPartitionStage.NECESSITY_TIER,
                state=PartitionReadinessState.DEFERRED,
                residuals=residuals,
                handoff=handoff,
            )

        if not tier_proof.residual_visible:
            return self._refuse(
                name="HIDDEN_RESIDUAL",
                stage=CriticalPartitionStage.RESIDUALS,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if tier_proof.tier is NecessityTier.DARURI and not tier_proof.evidence_ref.strip():
            return self._refuse(
                name="NECESSITY_TIER_PROMOTION_UNLICENSED",
                stage=CriticalPartitionStage.NECESSITY_TIER,
                state=PartitionReadinessState.DEFERRED,
                residuals=residuals,
                handoff=handoff,
            )

        if (
            tier_proof.tier in {NecessityTier.DARURI, NecessityTier.HAJI}
            and not tier_proof.transition_ref.strip()
        ):
            return self._refuse(
                name="NECESSITY_TIER_PROMOTION_UNLICENSED",
                stage=CriticalPartitionStage.NECESSITY_TIER,
                state=PartitionReadinessState.DEFERRED,
                residuals=residuals,
                handoff=handoff,
            )

        if tier_proof.tier is NecessityTier.TAHSINI and _looks_like_closure_claim(
            tier_proof.evidence_ref, tier_proof.declared_cause
        ):
            return self._refuse(
                name="TIER_LABEL_AS_CLOSURE_FORBIDDEN",
                stage=CriticalPartitionStage.NECESSITY_TIER,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if _is_forbidden_neighbor_handoff(declaration.partition_kind, handoff):
            return self._refuse(
                name="FORBIDDEN_NEIGHBOR_LEAP",
                stage=CriticalPartitionStage.HANDOFF,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        if not handoff.strip():
            return self._refuse(
                name="HANDOFF_REQUIRED",
                stage=CriticalPartitionStage.HANDOFF,
                state=PartitionReadinessState.REFUSED,
                residuals=residuals,
                handoff=handoff,
            )

        return CriticalPartitionDecision(
            partition_allowed=True,
            readiness_state=PartitionReadinessState.LINK_READY,
            failed_stage=None,
            local_failure_name=None,
            failure_code=None,
            residuals=residuals,
            handoff=handoff,
        )

    def _refuse(
        self,
        *,
        name: str,
        stage: CriticalPartitionStage,
        state: PartitionReadinessState,
        residuals: tuple[str, ...],
        handoff: str,
    ) -> CriticalPartitionDecision:
        return CriticalPartitionDecision(
            partition_allowed=False,
            readiness_state=state,
            failed_stage=stage,
            local_failure_name=name,
            failure_code=_LOCAL_FAILURE_MAP[name],
            residuals=residuals,
            handoff=handoff,
        )


_LOCAL_FAILURE_MAP: dict[str, FailureCode] = {
    "PARTITION_UNDECLARED": FailureCode.FORBIDDEN_STRAIGHT_LINE,
    "PARTITION_BRIDGE_MISSING": FailureCode.GATE_REQUIRED,
    "PARTITION_BRIDGE_METADATA_MISMATCH": FailureCode.GATE_REQUIRED,
    "PARTITION_BRIDGE_FORBIDDEN": FailureCode.FORBIDDEN_STRAIGHT_LINE,
    "IDENTITY_TRANSITION_UNLICENSED": FailureCode.GATE_REQUIRED,
    "IDENTITY_PROPERTY_BROKEN": FailureCode.IDENTITY_BROKEN,
    "TRIADIC_IDENTITY_GAP": FailureCode.FORBIDDEN_STRAIGHT_LINE,
    "NECESSITY_TIER_UNDECLARED": FailureCode.GATE_REQUIRED,
    "NECESSITY_TIER_PROMOTION_UNLICENSED": FailureCode.GATE_REQUIRED,
    "TIER_LABEL_AS_CLOSURE_FORBIDDEN": FailureCode.FORBIDDEN_STRAIGHT_LINE,
    "FORBIDDEN_NEIGHBOR_LEAP": FailureCode.FORBIDDEN_STRAIGHT_LINE,
    "HANDOFF_REQUIRED": FailureCode.GATE_REQUIRED,
    "HIDDEN_RESIDUAL": FailureCode.HIDDEN_RESIDUAL,
}


def _is_forbidden_skip(source: PartitionKind, target: PartitionKind) -> bool:
    return source is PartitionKind.PHONETIC and target is PartitionKind.SYSTEMIC


_FORBIDDEN_CLOSURE_CLAIM_TOKENS: frozenset[str] = frozenset(
    {"closure", "certainty", "truth", "semantic", "hukm", "ifadah", "mafhum"}
)
_ARABIC_BLOCK_START = 0x0600
_ARABIC_BLOCK_END = 0x06FF

_FORBIDDEN_HANDOFF_TOKENS_BY_PARTITION: dict[PartitionKind, frozenset[str]] = {
    PartitionKind.PHONETIC: frozenset(
        {
            "meaning",
            "semantic",
            "ifadah",
            "mafhum",
            "معنى",
            "دلالة",
            "افادة",
            "إفادة",
            "مفهوم",
        }
    ),
    PartitionKind.STRUCTURAL: frozenset(
        {
            "meaning",
            "semantic",
            "ifadah",
            "mafhum",
            "hukm",
            "معنى",
            "دلالة",
            "افادة",
            "إفادة",
            "مفهوم",
            "حكم",
            "حکم",
        }
    ),
    PartitionKind.SYSTEMIC: frozenset(
        {
            "truth",
            "certainty",
            "reality",
            "حقيقة",
            "واقع",
        }
    ),
}


def _looks_like_closure_claim(*values: str) -> bool:
    return bool(_FORBIDDEN_CLOSURE_CLAIM_TOKENS & _tokens(*values))


def _is_forbidden_neighbor_handoff(partition: PartitionKind, handoff: str) -> bool:
    tokens = _tokens(handoff)
    return bool(tokens & _FORBIDDEN_HANDOFF_TOKENS_BY_PARTITION[partition])


def _tokens(*values: str) -> set[str]:
    """Normalize and split mixed-script handoff text into comparable tokens."""
    joined = _strip_combining_marks(" ".join(values).lower())
    separated = "".join(char if _is_valid_token_char(char) else " " for char in joined)
    return {token for token in re.split(r"\s+", separated) if token}


def _strip_combining_marks(value: str) -> str:
    """Drop combining marks so diacritic variants map to a stable token form."""
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def _is_valid_token_char(char: str) -> bool:
    """Allow only letter/number token characters in ASCII and Arabic Unicode block."""
    if char.isascii():
        return char.isalnum()
    in_arabic_block = _ARABIC_BLOCK_START <= ord(char) <= _ARABIC_BLOCK_END
    return in_arabic_block and unicodedata.category(char)[0] in {"L", "N"}


def _require_str(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, str):
        raise CriticalPartitionContractError(f"{cls_name}.{field} must be a string")


def _require_bool(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, bool):
        raise CriticalPartitionContractError(f"{cls_name}.{field} must be a bool")


def _require_tuple(cls_name: str, field: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise CriticalPartitionContractError(f"{cls_name}.{field} must be a tuple")


__all__ = [
    "CriticalPartitionContractError",
    "CriticalPartitionDecision",
    "CriticalPartitionRuntimeContract",
    "CriticalPartitionStage",
    "IdentityPropertyConservationProof",
    "NecessityTier",
    "NecessityTierProof",
    "PartitionBridgeProof",
    "PartitionDeclaration",
    "PartitionKind",
    "PartitionReadinessState",
    "TriadicIdentityContinuityProof",
]
