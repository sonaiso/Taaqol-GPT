"""Bridge certificates between realizations in the GUA surface."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError


@dataclass(frozen=True, slots=True)
class BridgeCertificate:
    """Typed bridge proof between two realization domains."""

    bridge_id: str
    source_domain: str
    target_domain: str
    evidence_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        _require_str(self.__class__.__name__, "bridge_id", self.bridge_id)
        _require_str(self.__class__.__name__, "source_domain", self.source_domain)
        _require_str(self.__class__.__name__, "target_domain", self.target_domain)
        _require_str(self.__class__.__name__, "evidence_ref", self.evidence_ref)
        _require_str(self.__class__.__name__, "trace_ref", self.trace_ref)


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GuaCoreSchemaError(f"{cls_name}.{field_name} must be a non-empty string")
