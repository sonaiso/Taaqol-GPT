"""Evidence carriers for transition gating in the GUA core."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class EvidenceContract:
    """Evidence declaration consumed by GUA gates."""

    evidence_id: str
    source_kind: str
    rank_hint: str
    trace_ref: str

    def __post_init__(self) -> None:
        _require_str(self.__class__.__name__, "evidence_id", self.evidence_id)
        _require_str(self.__class__.__name__, "source_kind", self.source_kind)
        _require_str(self.__class__.__name__, "rank_hint", self.rank_hint)
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")
