"""``ConcreteAdapterCandidate`` + ``AdapterGuard`` — the adapter boundary.

PR-8 binding of ``docs/18_ADAPTER_BOUNDARY_LAW.md``. The licensing
chain this module implements (docs/18 §1) is:

    ModelClient protocol → ConcreteAdapterCandidate → AdapterGuard
    → AuditedAnswer only

* :class:`ConcreteAdapterCandidate` carries the §2 declarations at
  birth — adapter identity, model identity, the declared
  :class:`TransportSurface`, the completion callable, and the
  caller-supplied configuration. A declaration that is not supplied
  at all is a programmer mistake refused loudly (required fields,
  no defaults, no synthesis — ``TypeError``); a declaration that is
  supplied but degenerate (empty identity, undeclared transport,
  a completion that is not a ``ModelClient``) is left for the guard
  to refuse with its named code, never repaired.
* :meth:`AdapterGuard.admit` walks the §3 refusal table in order,
  first refusal wins, using only existing :class:`FailureCode`
  members. Every expected refusal is a value
  (:class:`AdapterAdmission`), never a bare exception; a wrong
  *type* handed to the guard is a programmer mistake refused loudly
  with ``TypeError`` (docs/18 §3).
* Admission is structural and grants nothing (docs/18 §5, §7): the
  guard never calls ``complete()``, never probes the transport, and
  :class:`AdapterAdmission` carries no rank, no verdict, no trace,
  and no successor — ``slots`` keeps that surface fixed.

The §3 conduct rows (verdict surface, confidence-as-evidence
surface, ledger writes, successor graphs, rank claims) are checked
structurally by design: the guard inspects which names the
transport exposes, exactly as ``runtime_checkable`` inspects
``complete`` — as much as the docs/01 black-box boundary permits
anyone to know about a model client.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.audit.model_client import ModelClient
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode


class TransportSurface(StrEnum):
    """The declared I/O class of an adapter (docs/18 §2).

    The perimeter of the adapter is its boundary: an ``IN_MEMORY``
    adapter performs no I/O at all, a ``LOCAL_PROCESS`` adapter
    touches no network, and a ``NETWORK`` adapter contacts only the
    endpoint declared at birth (docs/18 §4 rule 5).
    """

    IN_MEMORY = "IN_MEMORY"
    LOCAL_PROCESS = "LOCAL_PROCESS"
    NETWORK = "NETWORK"


# --- §3/§4 structural surfaces ---------------------------------------------
#
# Configuration keys that declare I/O beyond a non-network surface
# (docs/18 §4 rule 5) or persistence on any surface (§4 rule 3).
_NETWORK_CONFIGURATION_KEYS: frozenset[str] = frozenset(
    {"address", "api_base", "base_url", "endpoint", "host", "port", "proxy", "url"}
)
_PERSISTENCE_CONFIGURATION_KEYS: frozenset[str] = frozenset(
    {"cache_dir", "cache_path", "db_path", "log_file", "log_path", "output_file", "state_dir"}
)

# Names whose presence on a transport makes it a judge, a ledger
# writer, a generator, or a rank authority (docs/18 §3, §6).
_VERDICT_SURFACE: frozenset[str] = frozenset(
    {
        "approve",
        "approve_answer",
        "closure_state",
        "decide",
        "gate_state",
        "transition_state",
        "verdict",
    }
)
_CONFIDENCE_SURFACE: frozenset[str] = frozenset(
    {
        "chain_of_thought",
        "confidence",
        "hidden_state",
        "logits",
        "logprobs",
        "self_reported_confidence",
        "token_probabilities",
    }
)
_LEDGER_WRITE_SURFACE: frozenset[str] = frozenset(
    {"append", "append_trace", "ledger", "record_trace", "trace_ledger", "write_trace"}
)
_SUCCESSOR_SURFACE: frozenset[str] = frozenset(
    {"emit_successor", "successor", "successor_graph"}
)
_RANK_SURFACE: frozenset[str] = frozenset(
    {"claimed_rank", "granted_rank", "promote", "promote_rank", "rank"}
)


@dataclass(frozen=True, slots=True)
class ConcreteAdapterCandidate:
    """An adapter at birth — a candidate, not a licensed transport.

    The five §2 declarations are all required, with no defaults
    (docs/18 §2 — no synthesis, no "best-effort" candidate mode):

    * ``adapter_identity`` — the non-empty name of the adapter
      itself; an unnamed adapter cannot be joined to a trace story.
    * ``model_identity`` — the declared identity of the model
      behind the transport, recorded verbatim as a provenance
      claim; it is never evidence (docs/01).
    * ``transport_surface`` — the declared I/O class, or ``None``
      for *undeclared*, which the guard refuses with
      ``BOUNDARY_MISSING`` (§3).
    * ``completion`` — the ``complete(prompt) -> str``
      implementation; the one required slot of the candidate.
    * ``configuration`` — endpoints, credentials, and model
      parameters as ``(key, value)`` pairs supplied by the caller
      at birth. The adapter never goes looking for configuration
      (environment, filesystem, network discovery) on its own.
    """

    adapter_identity: str
    model_identity: str
    transport_surface: TransportSurface | None
    completion: object
    configuration: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.adapter_identity, str):
            raise TypeError(
                "ConcreteAdapterCandidate.adapter_identity must be a string"
            )
        if not isinstance(self.model_identity, str):
            raise TypeError(
                "ConcreteAdapterCandidate.model_identity must be a string"
            )
        if self.transport_surface is not None and not isinstance(
            self.transport_surface, TransportSurface
        ):
            raise TypeError(
                "ConcreteAdapterCandidate.transport_surface must be a "
                "TransportSurface or None"
            )
        if not isinstance(self.configuration, tuple):
            raise TypeError(
                "ConcreteAdapterCandidate.configuration must be a tuple "
                "of (key, value) pairs"
            )
        for pair in self.configuration:
            if (
                not isinstance(pair, tuple)
                or len(pair) != 2
                or not isinstance(pair[0], str)
                or not isinstance(pair[1], str)
            ):
                raise TypeError(
                    "every ConcreteAdapterCandidate.configuration entry "
                    "must be a (str, str) pair"
                )


@dataclass(frozen=True, slots=True)
class AdapterAdmission:
    """The value returned by :meth:`AdapterGuard.admit` (docs/18 §3, §7).

    Exactly one of :attr:`candidate` and :attr:`failure_code` is set:

    * an admission carries the admitted
      :class:`ConcreteAdapterCandidate` and ``failure_code is None``;
    * a refusal carries ``candidate is None`` and a named
      :class:`FailureCode` from the docs/18 §3 table.

    Admission is of a transport, never approval of an answer
    (docs/18 §5): this value carries no rank, no verdict, no trace,
    and no successor, and ``slots`` keeps that surface fixed. The
    schema invariant is enforced at construction time so a refusal
    can never be silently treated as an admission.
    """

    candidate: ConcreteAdapterCandidate | None
    failure_code: FailureCode | None
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.message, str):
            raise TypeError("AdapterAdmission.message must be a string")
        if self.candidate is None and self.failure_code is None:
            raise TypeError(
                "AdapterAdmission must carry either a candidate or a failure_code"
            )
        if self.candidate is not None and self.failure_code is not None:
            raise TypeError(
                "AdapterAdmission cannot carry both a candidate and a failure_code"
            )
        if self.candidate is not None and not isinstance(
            self.candidate, ConcreteAdapterCandidate
        ):
            raise TypeError(
                "AdapterAdmission.candidate must be a ConcreteAdapterCandidate or None"
            )
        if self.failure_code is not None and not isinstance(
            self.failure_code, FailureCode
        ):
            raise TypeError(
                "AdapterAdmission.failure_code must be a FailureCode or None"
            )

    @property
    def is_refusal(self) -> bool:
        """``True`` iff this admission carries a named refusal."""

        return self.failure_code is not None


def _refusal(code: FailureCode, message: str) -> AdapterAdmission:
    return AdapterAdmission(candidate=None, failure_code=code, message=message)


def _exposed(client: object, surface: frozenset[str]) -> tuple[str, ...]:
    """The names from ``surface`` the client structurally exposes."""

    return tuple(sorted(name for name in surface if hasattr(client, name)))


@dataclass(frozen=True, slots=True)
class AdapterGuard:
    """The structural checkpoint of docs/18 §3 — admits or refuses.

    Bound by the same discipline as ``Γ`` and the construction
    surface (docs/18 §7): admission is structural — the guard never
    calls ``complete()``, performs no I/O, and fabricates no missing
    declaration; every candidate either is admitted or refused with
    a named :class:`FailureCode` from the §3 table; admission
    carries no rank and raises none.
    """

    def admit(self, candidate: object) -> AdapterAdmission:
        """Walk the docs/18 §3 refusal table in order, first wins."""

        if not isinstance(candidate, ConcreteAdapterCandidate):
            raise TypeError(
                "AdapterGuard.admit requires a ConcreteAdapterCandidate"
            )

        # §3 — adapter identity missing or empty.
        if not candidate.adapter_identity.strip():
            return _refusal(
                FailureCode.IDENTITY_BROKEN,
                "adapter identity missing or empty (docs/18 §3)",
            )
        # §3 — model identity missing or empty.
        if not candidate.model_identity.strip():
            return _refusal(
                FailureCode.IDENTITY_BROKEN,
                "model identity missing or empty (docs/18 §3)",
            )
        # §3 — transport surface undeclared.
        if candidate.transport_surface is None:
            return _refusal(
                FailureCode.BOUNDARY_MISSING,
                "transport surface undeclared (docs/18 §3)",
            )
        # §3 — completion callable missing / not ModelClient.
        if not isinstance(candidate.completion, ModelClient):
            return _refusal(
                FailureCode.REQUIRED_SLOT_EMPTY,
                "completion callable missing or not a ModelClient (docs/18 §3)",
            )
        # §3 — I/O beyond the declared, licensed surface (§4).
        keys = frozenset(key for key, _ in candidate.configuration)
        persistence = tuple(sorted(keys & _PERSISTENCE_CONFIGURATION_KEYS))
        if persistence:
            return _refusal(
                FailureCode.UNLICENSED_OPENING,
                "configuration declares persistence beyond the licensed "
                f"surface (docs/18 §4): {', '.join(persistence)}",
            )
        if candidate.transport_surface is not TransportSurface.NETWORK:
            network = tuple(sorted(keys & _NETWORK_CONFIGURATION_KEYS))
            if network:
                return _refusal(
                    FailureCode.UNLICENSED_OPENING,
                    "configuration declares network I/O on a "
                    f"{candidate.transport_surface.value} transport "
                    f"(docs/18 §4): {', '.join(network)}",
                )
        # §3 — adapter exposes a verdict surface.
        exposed = _exposed(candidate.completion, _VERDICT_SURFACE)
        if exposed:
            return _refusal(
                FailureCode.FORBIDDEN_STRAIGHT_LINE,
                f"adapter exposes a verdict surface (docs/18 §3): {', '.join(exposed)}",
            )
        # §3 — adapter exposes confidence / internals as evidence.
        exposed = _exposed(candidate.completion, _CONFIDENCE_SURFACE)
        if exposed:
            return _refusal(
                FailureCode.FORBIDDEN_STRAIGHT_LINE,
                "adapter exposes confidence or internals as evidence "
                f"(docs/18 §3): {', '.join(exposed)}",
            )
        # §3 — adapter exposes a TraceLedger write surface.
        exposed = _exposed(candidate.completion, _LEDGER_WRITE_SURFACE)
        if exposed:
            return _refusal(
                FailureCode.OUTPUT_EXCEEDS_LAYER,
                "adapter exposes a trace-ledger write surface "
                f"(docs/18 §3): {', '.join(exposed)}",
            )
        # §3 — adapter exposes a successor-graph surface.
        exposed = _exposed(candidate.completion, _SUCCESSOR_SURFACE)
        if exposed:
            return _refusal(
                FailureCode.GATE_REQUIRED,
                "adapter exposes a successor-graph surface "
                f"(docs/18 §3): {', '.join(exposed)}",
            )
        # §3 — adapter exposes a rank claim.
        exposed = _exposed(candidate.completion, _RANK_SURFACE)
        if exposed:
            return _refusal(
                FailureCode.RANK_PROMOTION_WITHOUT_GATE,
                f"adapter exposes a rank claim (docs/18 §3): {', '.join(exposed)}",
            )

        return AdapterAdmission(candidate=candidate, failure_code=None, message="")


__all__ = [
    "AdapterAdmission",
    "AdapterGuard",
    "ConcreteAdapterCandidate",
    "TransportSurface",
]
