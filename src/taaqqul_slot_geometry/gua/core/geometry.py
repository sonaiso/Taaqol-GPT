"""General-core extraction and freeze carriers for GUA."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from taaqqul_slot_geometry.gua.core.domain import DomainSpec
from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError
from taaqqul_slot_geometry.gua.core.prior_matrix import PriorDomainMatrix
from taaqqul_slot_geometry.gua.core.slot import TypedSlot
from taaqqul_slot_geometry.gua.core.trace import Trace
from taaqqul_slot_geometry.gua.core.transition import TransitionContract


@dataclass(frozen=True, slots=True)
class LocalGeometry:
    """Local slot-geometry bundle extracted into the general core."""

    slots: tuple[TypedSlot, ...]
    trace: Trace

    def __post_init__(self) -> None:
        if not isinstance(self.slots, tuple) or not self.slots:
            raise GuaCoreSchemaError("LocalGeometry.slots must be a non-empty tuple")
        for slot in self.slots:
            if not isinstance(slot, TypedSlot):
                raise GuaCoreSchemaError("LocalGeometry.slots entries must be TypedSlot")
        if not isinstance(self.trace, Trace):
            raise GuaCoreSchemaError("LocalGeometry.trace must be Trace")


@dataclass(frozen=True, slots=True)
class GeneralCoreExtraction:
    """GUA extraction output before freeze."""

    domain: DomainSpec
    prior_matrix: PriorDomainMatrix
    geometry: LocalGeometry
    transitions: tuple[TransitionContract, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.domain, DomainSpec):
            raise GuaCoreSchemaError("GeneralCoreExtraction.domain must be DomainSpec")
        if not isinstance(self.prior_matrix, PriorDomainMatrix):
            raise GuaCoreSchemaError(
                "GeneralCoreExtraction.prior_matrix must be PriorDomainMatrix"
            )
        if not isinstance(self.geometry, LocalGeometry):
            raise GuaCoreSchemaError("GeneralCoreExtraction.geometry must be LocalGeometry")
        if not isinstance(self.transitions, tuple) or not self.transitions:
            raise GuaCoreSchemaError("GeneralCoreExtraction.transitions must be a non-empty tuple")
        for transition in self.transitions:
            if not isinstance(transition, TransitionContract):
                raise GuaCoreSchemaError(
                    "GeneralCoreExtraction.transitions entries must be TransitionContract"
                )
        if self.domain.domain_id != self.prior_matrix.domain_id:
            raise GuaCoreSchemaError(
                "GeneralCoreExtraction.domain.domain_id must match prior_matrix.domain_id"
            )


@dataclass(frozen=True, slots=True)
class CoreFreeze:
    """Immutable freeze record for an extracted general core."""

    extraction_hash: str
    frozen_fields: tuple[str, ...]
    trace_ref: str

    def __post_init__(self) -> None:
        _require_str(self.__class__.__name__, "extraction_hash", self.extraction_hash)
        _require_tuple_of_str(self.__class__.__name__, "frozen_fields", self.frozen_fields)
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)


def freeze_general_core(extraction: GeneralCoreExtraction) -> CoreFreeze:
    """Freeze an extracted general core into a deterministic immutable record."""

    if not isinstance(extraction, GeneralCoreExtraction):
        raise GuaCoreSchemaError("freeze_general_core expects GeneralCoreExtraction")
    payload = repr(extraction).encode("utf-8")
    digest = sha256(payload).hexdigest()
    return CoreFreeze(
        extraction_hash=digest,
        frozen_fields=("domain", "prior_matrix", "geometry", "transitions"),
        trace_ref=extraction.geometry.trace.trace_ref,
    )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")


def _require_tuple_of_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple) or not value:
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty tuple")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise GuaCoreSchemaError(f"{cls_name}.{field_name} entries must be non-empty strings")
