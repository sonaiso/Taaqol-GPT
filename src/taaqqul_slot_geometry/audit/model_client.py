"""``ModelClient`` — the black-box boundary of docs/01 in protocol form.

PR-6 binding of ``docs/01_BLACK_BOX_BOUNDARY.md``. The protocol is
the *entire* surface the audit layer may see of any model:

* the engine sends a prompt and receives an **emitted** answer —
  a string, nothing else;
* no logits, no token probabilities, no hidden chain-of-thought, no
  self-reported confidence ever crosses this boundary. A model's
  confidence in its own answer is **never** evidence (docs/01) —
  evidence enters the kernel only through an
  :class:`~taaqqul_slot_geometry.core.evidence_contract.EvidenceContract`;
* the repository asserts nothing about what happens inside the
  model. It wraps what comes *out*.

PR-6 ships the protocol **only**. Concrete adapters (OpenAI,
Anthropic, local models) are forbidden until the dedicated
post-PR-6 milestone (docs/14 — *Forbidden surface*); shipping one
here would be a ``FORBIDDEN_LEAP`` regardless of CI status.

``runtime_checkable`` makes ``isinstance(obj, ModelClient)`` check
for the presence of a ``complete`` method — a structural check
only, which is exactly as much as the black-box boundary permits
the audit layer to know about its model.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ModelClient(Protocol):
    """Anything that can turn a prompt into an emitted answer.

    The single method is deliberately minimal: the audit layer may
    *only* request a completion. It may not configure sampling,
    inspect internals, or stream partial states — any of those
    would smuggle model-internal structure across the docs/01
    boundary.
    """

    def complete(self, prompt: str) -> str:
        """Return the model's emitted answer for ``prompt``."""
        ...


__all__ = ["ModelClient"]
