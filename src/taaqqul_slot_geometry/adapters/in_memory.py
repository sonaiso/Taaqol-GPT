"""``InMemoryModelClient`` — the one licensed adapter of PR-8 (docs/18).

The narrowest concrete ``ModelClient`` the Adapter Boundary Law
licenses: a frozen, caller-declared prompt → answer table behind
``complete``. It exists to prove the boundary, not a connection to
an external provider:

* declared transport: ``IN_MEMORY`` — *no I/O at all* (docs/18 §4
  rule 5). No network, no filesystem, no environment lookup, no
  process spawn ever happens here, at import time, construction
  time, or call time (§4 rule 1).
* one prompt in, one emitted string out (§4 rule 2). No streaming,
  no partial state, no model internals (§4 rule 4).
* no persistence: the client stores nothing beyond its birth
  declarations (§4 rule 3).
* it carries no verdict surface, no ledger surface, no successor
  surface, and no rank claim — the transport is a carrier, not a
  judge (docs/18 §6).

Its answers reach a caller only through ``AnswerAudit`` (docs/18
§1 step 4): a raw adapter string is an internal value, never a
system output.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InMemoryModelClient:
    """A declared prompt → answer table satisfying ``ModelClient``.

    ``responses`` is a tuple of ``(prompt, answer)`` string pairs
    supplied at birth (docs/18 §2 — configuration enters as
    constructor arguments; the adapter never goes looking for it).
    Malformed declarations are programmer mistakes refused loudly
    with ``TypeError`` at construction, in the audit-surface birth
    guard style.
    """

    responses: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.responses, tuple):
            raise TypeError(
                "InMemoryModelClient.responses must be a tuple of "
                "(prompt, answer) pairs"
            )
        seen: set[str] = set()
        for pair in self.responses:
            if (
                not isinstance(pair, tuple)
                or len(pair) != 2
                or not isinstance(pair[0], str)
                or not isinstance(pair[1], str)
            ):
                raise TypeError(
                    "every InMemoryModelClient.responses entry must be "
                    "a (str, str) pair"
                )
            if pair[0] in seen:
                raise TypeError(
                    "duplicate prompt in InMemoryModelClient.responses: "
                    f"{pair[0]!r}"
                )
            seen.add(pair[0])

    def complete(self, prompt: str) -> str:
        """Return the declared answer for ``prompt`` (docs/01).

        The table is total only over its declarations: an unmapped
        prompt is a programmer mistake in the fixture wiring,
        refused loudly with ``KeyError`` — the adapter synthesises
        nothing (docs/18 §2 — no defaults, no "best-effort" mode).
        """

        if not isinstance(prompt, str):
            raise TypeError("InMemoryModelClient.complete requires a string prompt")
        for known, answer in self.responses:
            if known == prompt:
                return answer
        raise KeyError(
            f"no declared answer for prompt {prompt!r} "
            "(docs/18 §2 — the adapter synthesises nothing)"
        )


__all__ = ["InMemoryModelClient"]
