"""``taaqqul_slot_geometry.adapters`` — the PR-8 adapter boundary.

PR-8 binding of ``docs/18_ADAPTER_BOUNDARY_LAW.md`` (ratified in
PR-7). The subpackage has exactly four parts and no more:

* :class:`ConcreteAdapterCandidate` + :class:`TransportSurface` —
  the §2 declarations an adapter must carry at birth. No defaults,
  no synthesis;
* :class:`AdapterGuard` + :class:`AdapterAdmission` — the
  structural checkpoint of docs/18 §3: every refusal is a named
  ``FailureCode`` value, and admission is of a transport, never
  approval of an answer (§5);
* :class:`InMemoryModelClient` — the single concrete adapter this
  chain step licenses (docs/18 §6 — no second adapter in PR-8):
  ``IN_MEMORY`` transport, no I/O at all (§4).

An adapter is a transport, not a judge: nothing in this subpackage
touches ``Γ``, the gate, the ledger, or the emission half. Answers
reach a caller only through ``AnswerAudit`` (docs/18 §1, step 4).
"""

from __future__ import annotations

from taaqqul_slot_geometry.adapters.adapter_boundary import (
    AdapterAdmission,
    AdapterGuard,
    ConcreteAdapterCandidate,
    TransportSurface,
)
from taaqqul_slot_geometry.adapters.in_memory import InMemoryModelClient

__all__ = [
    "AdapterAdmission",
    "AdapterGuard",
    "ConcreteAdapterCandidate",
    "InMemoryModelClient",
    "TransportSurface",
]
