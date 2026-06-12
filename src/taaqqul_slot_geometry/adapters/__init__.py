"""``taaqqul_slot_geometry.adapters`` — the PR-8 adapter boundary.

PR-8 binding of ``docs/18_ADAPTER_BOUNDARY_LAW.md``. The package has
exactly two parts and no more:

* the boundary carriers — :class:`TransportSurface`,
  :class:`ConcreteAdapterCandidate`, :class:`AdapterGuard`,
  :class:`AdapterAdmission`, and the named surface registries the
  guard's §3 structural rows consult;
* exactly **one** concrete adapter on exactly one transport —
  :class:`InMemoryModelClient` on ``IN_MEMORY`` (docs/18 — *PR-8
  binding*). It proves the boundary, not a provider.

No network adapter, no provider SDK, no streaming, no persistence,
no environment lookup lives here (docs/18 §6); the static guards in
``tests/test_adapter_boundary.py`` prove the import surface.
Admission is not approval (docs/18 §5): everything an admitted
client emits still walks the full ``AnswerAudit`` chain.
"""

from __future__ import annotations

from taaqqul_slot_geometry.adapters.adapter_boundary import (
    CONFIDENCE_SURFACE_NAMES,
    LEDGER_SURFACE_NAMES,
    RANK_SURFACE_NAMES,
    SUCCESSOR_SURFACE_NAMES,
    VERDICT_SURFACE_NAMES,
    AdapterAdmission,
    AdapterGuard,
    ConcreteAdapterCandidate,
    TransportSurface,
)
from taaqqul_slot_geometry.adapters.in_memory import InMemoryModelClient

__all__ = [
    "CONFIDENCE_SURFACE_NAMES",
    "LEDGER_SURFACE_NAMES",
    "RANK_SURFACE_NAMES",
    "SUCCESSOR_SURFACE_NAMES",
    "VERDICT_SURFACE_NAMES",
    "AdapterAdmission",
    "AdapterGuard",
    "ConcreteAdapterCandidate",
    "InMemoryModelClient",
    "TransportSurface",
]
