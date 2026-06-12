"""``InMemoryModelClient`` — the first concrete adapter (PR-8, docs/18).

The first adapter's job is to prove the **boundary**, not to prove a
connection to an external provider. It is a declared in-memory
transcript:

* transport surface: :attr:`TransportSurface.IN_MEMORY` — no I/O of
  any kind (docs/18 §2, §4). No network, no filesystem, no process,
  no environment lookup. The whole transport is a ``dict`` the
  caller declared at construction;
* completion: one prompt in, one **verbatim** emitted string out
  (docs/18 §4). The adapter never rewrites, truncates, or decorates
  an answer;
* no synthesis (docs/18 §2 — "No defaults, no synthesis, no
  best-effort mode"): a prompt absent from the declared transcript
  is refused loudly with ``KeyError``. Inventing an answer for an
  undeclared prompt would make the transport a generator;
* no judge surface: the class exposes ``complete`` and its declared
  ``transport_surface`` — no verdicts, no confidence, no ledger, no
  successor, no rank (docs/18 §6). The :class:`AdapterGuard`
  registries prove this structurally at admission.

Wrong argument *types* are programmer mistakes refused with
``TypeError``, consistent with the PR-6 audit surface; the named
constitutional refusals about adapters live in the guard, not here
— the adapter is a transport, not a judge.
"""

from __future__ import annotations

from collections.abc import Mapping

from taaqqul_slot_geometry.adapters.adapter_boundary import TransportSurface


class InMemoryModelClient:
    """A declared transcript behind the ``ModelClient`` protocol.

    Satisfies the protocol structurally (a ``complete`` method) and
    declares its transport as a class attribute so the guard can
    read it without executing anything (docs/18 §7).
    """

    __slots__ = ("_answers",)

    #: Declared transport (docs/18 §2): in-memory, no I/O at all.
    transport_surface = TransportSurface.IN_MEMORY

    def __init__(self, answers: Mapping[str, str]) -> None:
        if not isinstance(answers, Mapping):
            raise TypeError("InMemoryModelClient requires answers as a Mapping")
        for prompt, answer in answers.items():
            if not isinstance(prompt, str) or not isinstance(answer, str):
                raise TypeError("InMemoryModelClient requires answers entries as str -> str")
        self._answers: dict[str, str] = dict(answers)

    def complete(self, prompt: str) -> str:
        """Return the declared answer for ``prompt``, verbatim."""

        if not isinstance(prompt, str):
            raise TypeError("InMemoryModelClient.complete() requires prompt as a str")
        try:
            return self._answers[prompt]
        except KeyError:
            raise KeyError(
                f"InMemoryModelClient: no declared answer for prompt {prompt!r} — "
                "the transcript adapter never synthesises (docs/18 §2)."
            ) from None


__all__ = ["InMemoryModelClient"]
