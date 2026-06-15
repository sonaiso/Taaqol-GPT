"""``taaqqul_slot_geometry.audit`` — the PR-6 audit layer.

PR-6 binding of docs/01 (black-box boundary), docs/07 (ledger
ownership), docs/08 (the emission half), and docs/17 §1 source 3
(``TRANSITION_VERDICT`` generation).

The layer has exactly three parts and no more:

* :class:`ModelClient` — the protocol-only black-box boundary.
  Concrete adapters are forbidden until the dedicated post-PR-6
  milestone (docs/14);
* :func:`emit_successor` — the pure emission of the successor
  graph an ``APPROVED`` verdict licenses;
* :class:`AnswerAudit` / :class:`AuditedAnswer` — the impure shell
  that owns the :class:`~taaqqul_slot_geometry.core.trace_ledger.TraceLedger`
  and wraps every emitted answer with its verdict, rank, evidence
  references, and residual surface.

**PR-22-AUDIT** adds the vertical-chain bridge:

* :func:`bridge_tanzil_to_audit` — pure bridge surfacing a PROVEN
  TanzilVerdict inside the audit layer as an
  :class:`AuditedTanzilBridge`, preserving the full presentation
  envelope. No execution, no adapter call, no model call.

No persistence, no network, no filesystem I/O lives here either:
"impure" in this package means exactly one thing — appending the
kernel's trace candidates to an in-memory ledger.
"""

from __future__ import annotations

from taaqqul_slot_geometry.audit.answer_audit import AnswerAudit, AuditedAnswer
from taaqqul_slot_geometry.audit.model_client import ModelClient
from taaqqul_slot_geometry.audit.successor import emit_successor
from taaqqul_slot_geometry.audit.tanzil_bridge import (
    AuditBridgeState,
    AuditedTanzilBridge,
    AuditedTanzilBridgeVerdict,
    bridge_tanzil_to_audit,
)

__all__ = [
    "AnswerAudit",
    "AuditBridgeState",
    "AuditedAnswer",
    "AuditedTanzilBridge",
    "AuditedTanzilBridgeVerdict",
    "ModelClient",
    "bridge_tanzil_to_audit",
    "emit_successor",
]
