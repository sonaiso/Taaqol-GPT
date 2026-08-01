"""USM residual carriers (USM-C1)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.usm.identifiers import USMSchemaError, require_non_empty_text


class USMResidualKind(StrEnum):
    UNMAPPED_ENTITY = "UNMAPPED_ENTITY"
    MISSING_CAPABILITY = "MISSING_CAPABILITY"
    UNSPECIFIED_RELATION = "UNSPECIFIED_RELATION"
    TRANSFORMATION_NOT_EXECUTABLE = "TRANSFORMATION_NOT_EXECUTABLE"
    EVIDENCE_BRIDGE_MISSING = "EVIDENCE_BRIDGE_MISSING"
    RANK_MAPPING_UNRESOLVED = "RANK_MAPPING_UNRESOLVED"
    KNOWLEDGE_REVISION_DEFERRED = "KNOWLEDGE_REVISION_DEFERRED"
    APPLICATION_SCOPE_UNRESOLVED = "APPLICATION_SCOPE_UNRESOLVED"
    COVERAGE_GAP = "COVERAGE_GAP"
    IRREDUCIBILITY_UNPROVEN = "IRREDUCIBILITY_UNPROVEN"


@dataclass(frozen=True, slots=True)
class USMResidual:
    residual_id: str
    kind: USMResidualKind
    detail: str
    blocking: bool
    visible: bool
    repair_hint: str | None

    def __post_init__(self) -> None:
        require_non_empty_text("USMResidual", "residual_id", self.residual_id)
        if not isinstance(self.kind, USMResidualKind):
            raise USMSchemaError("USMResidual.kind must be USMResidualKind")
        require_non_empty_text("USMResidual", "detail", self.detail)
        if not isinstance(self.blocking, bool):
            raise USMSchemaError("USMResidual.blocking must be bool")
        if not isinstance(self.visible, bool):
            raise USMSchemaError("USMResidual.visible must be bool")
        if not self.visible:
            raise USMSchemaError("USMResidual.visible must be True (no hidden residual)")
        if self.repair_hint is not None:
            require_non_empty_text("USMResidual", "repair_hint", self.repair_hint)


__all__ = ["USMResidual", "USMResidualKind"]
